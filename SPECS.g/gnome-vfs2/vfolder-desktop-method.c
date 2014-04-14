/* -*- Mode: C; tab-width: 8; indent-tabs-mode: 8; c-basic-offset: 8 -*- */

/* vfolder-desktop-method.c

   Copyright (C) 2001 Red Hat, Inc.
   Copyright (C) 2001 The Dark Prince

   The Gnome Library is free software; you can redistribute it and/or
   modify it under the terms of the GNU Library General Public License as
   published by the Free Software Foundation; either version 2 of the
   License, or (at your option) any later version.

   The Gnome Library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Library General Public License for more details.

   You should have received a copy of the GNU Library General Public
   License along with the Gnome Library; see the file COPYING.LIB.  If not,
   write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
   Boston, MA 02111-1307, USA.
*/

/* URI scheme for reading the "applications:" vfolder and other
 * vfolder schemes.  Lots of code stolen from the original desktop
 * reading URI scheme.
 */

#ifdef HAVE_CONFIG_H
# include <config.h>
#endif

/* Debugging foo: */
/*#define D(x) x */
#define D(x) ;

#include <glib.h>
#include <sys/types.h>
#include <dirent.h>
#include <errno.h>
#include <string.h>
#include <time.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>

#include <libxml/parser.h>
#include <libxml/tree.h>
#include <libxml/xmlmemory.h>

#include <libgnomevfs/gnome-vfs-mime.h>

#include <libgnomevfs/gnome-vfs-module.h>
#include <libgnomevfs/gnome-vfs-method.h>
#include <libgnomevfs/gnome-vfs-utils.h>
#include <libgnomevfs/gnome-vfs-ops.h>
#include <libgnomevfs/gnome-vfs-module-shared.h>
#include <libgnomevfs/gnome-vfs-monitor-private.h>

#define DOT_GNOME ".gnome2"

typedef struct _VFolderInfo VFolderInfo;
typedef struct _Query Query;
typedef struct _QueryKeyword QueryKeyword;
typedef struct _QueryFilename QueryFilename;
typedef struct _Entry Entry;
typedef struct _Folder Folder;
typedef struct _EntryFile EntryFile;
typedef struct _Keyword Keyword;
typedef struct _FileMonitorHandle FileMonitorHandle;
typedef struct _StatLoc StatLoc;
typedef struct _VFolderURI VFolderURI;

/* TODO before 2.0: */
/* FIXME: also check/monitor desktop_dirs like we do the vfolder
 * file and the item dirs */
/* FIXME: check if thread locks are not completely on crack which
 * is likely given my experience with threads */
/* FIXME: use filename locking, currently we are full of races if
 * multiple processes write to this filesystem */
/* FIXME: implement monitors */

/* TODO for later (star trek future): */
/* FIXME: Maybe when chaining to file:, we should call the gnome-vfs wrapper
 * functions, instead of the file: methods directly.  */
/* FIXME: related to the above: we should support things being on non
 * file: filesystems.  Such as having the vfolder info file on http
 * somewhere or some such nonsense :) */

static GnomeVFSMethod *parent_method = NULL;

static GHashTable *infos = NULL;

/* Note: I have no clue about how to write thread safe code and this
 * is my first attempt, so it's probably wrong
 * -George */
G_LOCK_DEFINE_STATIC (vfolder_lock);

/* Note: all keywords are quarks */
/* Note: basenames are unique */

#define UNSUPPORTED_INFO_FIELDS (GNOME_VFS_FILE_INFO_FIELDS_PERMISSIONS | \
				 GNOME_VFS_FILE_INFO_FIELDS_DEVICE | \
				 GNOME_VFS_FILE_INFO_FIELDS_INODE | \
				 GNOME_VFS_FILE_INFO_FIELDS_LINK_COUNT | \
				 GNOME_VFS_FILE_INFO_FIELDS_ATIME)


enum {
	QUERY_OR,
	QUERY_AND,
	QUERY_KEYWORD,
	QUERY_FILENAME
};

struct _Query {
	int type;
	gboolean not;
	GSList *queries;
};

struct _QueryKeyword {
	int type;
	gboolean not;
	GQuark keyword;
};

struct _QueryFilename {
	int type;
	gboolean not;
	char *filename;
};

enum {
	ENTRY_FILE,
	ENTRY_FOLDER
};

struct _Entry {
	int type;
	int refcount;
	int alloc; /* not really useful for folders,
		      but oh well, whatever.  It's the number
		      of times this is queried in some directory,
		      used for the Unallocated query type */
	char *name;

	GSList *monitors;
};

struct _EntryFile {
	Entry entry;

	char *filename;
	gboolean per_user;
	GSList *keywords;

	gboolean implicit_keywords; /* the keywords were added by us */
};

struct _Folder {
	Entry entry;

	Folder *parent;

	char *desktop_file; /* the .directory file */

	Query *query;

	/* The following is for per file
	 * access */
	/* excluded by filename */
	GHashTable *excludes;
	/* included by filename */
	GSList *includes;
	GHashTable *includes_ht;

	GSList *subfolders;

	/* Some flags */
	gboolean read_only;
	gboolean dont_show_if_empty;
	gboolean only_unallocated; /* include only unallocated items */

	/* lazily done, will run query only when it
	 * needs to */
	gboolean up_to_date;
	gboolean sorted;
	GSList *entries;
};

struct _StatLoc {
	time_t ctime;
	time_t last_stat;
	gboolean trigger_next; /* if true, next check will fail */
	char name[1]; /* the structure will be long enough to
			 fit name */
};

struct _VFolderInfo {
	char *scheme;

	char *filename;
	char *user_filename;
	time_t user_filename_last_write;
	char *desktop_dir; /* directory with .directorys */
	char *user_desktop_dir; /* directory with .directorys */
	gboolean user_file_active; /* if using user_filename and
				      not filename */

	GSList *item_dirs;
	char *user_item_dir; /* dir where user changes to
				items are stored */

	/* old style dirs to merge in */
	GSList *merge_dirs;

	/* if entries are valid, else
	 * they need to be (re)read */
	gboolean entries_valid;

	GSList *entries;

	/* entry hash by basename */
	GHashTable *entries_ht;

	/* The root folder */
	Folder *root;

	/* The unallocated folders, the folder which only
	 * include unallocated items */
	GSList *unallocated_folders;

	/* some flags */
	gboolean read_only;

	gboolean dirty;

	int inhibit_write;

	/* change monitoring stuff */
	GnomeVFSMonitorHandle *filename_monitor;
	GnomeVFSMonitorHandle *user_filename_monitor;

	/* stat locations (in case we aren't monitoring) */
	StatLoc *filename_statloc;
	StatLoc *user_filename_statloc;

	/* for .directory dirs */
	/* FIXME: */GnomeVFSMonitorHandle *desktop_dir_monitor;
	/* FIXME: */GnomeVFSMonitorHandle *user_desktop_dir_monitor;

	/* stat locations (in case we aren't monitoring) */
	/* FIXME: */StatLoc *desktop_dir_statloc;
	/* FIXME: */StatLoc *user_desktop_dir_statloc;

	/* FIXME: */GSList *file_monitors; /* FileMonitorHandle */
	/* FIXME: */GSList *free_file_monitors; /* FileMonitorHandle */
	GSList *folder_monitors; /* FileMonitorHandle */
	GSList *free_folder_monitors; /* FileMonitorHandle */

	GSList *item_dir_monitors; /* GnomeVFSMonitorHandle */

	/* item dirs to stat */
	GSList *stat_dirs;

	/* ctime for folders */
	time_t modification_time;

	guint reread_queue;
};

struct _FileMonitorHandle {
	int refcount;
	gboolean exists;
	gboolean dir_monitor; /* TRUE if dir, FALSE if file */
	GnomeVFSURI *uri;
	GnomeVFSMonitorHandle *handle; /* A real handle if we're monitoring
					  an actual file here, or NULL */
	char *filename; /* Just the basename, used in the free_file_list */
	gboolean is_directory_file;
};

struct _VFolderURI {
	const gchar *scheme;
	gboolean     is_all_scheme;
	gboolean     ends_in_slash;
	gchar       *path;
	gchar       *file;
	GnomeVFSURI *uri;
};


static Entry *	entry_ref			(Entry *entry);
static Entry *	entry_ref_alloc			(Entry *entry);
static void	entry_unref			(Entry *entry);
static void	entry_unref_dealloc		(Entry *entry);
static void	query_destroy			(Query *query);
static void	ensure_folder			(VFolderInfo *info,
						 Folder *folder,
						 gboolean subfolders,
						 Folder *except,
						 gboolean ignore_unallocated);
static void	ensure_folder_unlocked		(VFolderInfo *info,
						 Folder *folder,
						 gboolean subfolders,
						 Folder *except,
						 gboolean ignore_unallocated);
/* An EVIL function for quick reading of .desktop files,
 * only reads in one or two keys, but that's ALL we need */
static void	readitem_entry			(const char *filename,
						 const char *key1,
						 char **result1,
						 const char *key2,
						 char **result2);
static gboolean vfolder_info_reload 		(VFolderInfo *info,
						 GnomeVFSResult *result,
						 GnomeVFSContext *context,
						 gboolean force_read_items);
static gboolean vfolder_info_reload_unlocked	(VFolderInfo *info,
						 GnomeVFSResult *result,
						 GnomeVFSContext *context,
						 gboolean force_read_items);
static void     invalidate_folder_subfolders    (Folder   *folder,
						 gboolean  lock_taken);
static Folder *	resolve_folder			(VFolderInfo *info,
						 const char *path,
						 gboolean ignore_basename,
						 GnomeVFSResult *result,
						 GnomeVFSContext *context);
static gboolean	vfolder_info_read_items		(VFolderInfo *info,
						 GnomeVFSResult *result,
						 GnomeVFSContext *context);

/* assumes vuri->path already set */
static gboolean
vfolder_uri_parse_internal (GnomeVFSURI *uri, VFolderURI *vuri)
{
	vuri->scheme = (gchar *) gnome_vfs_uri_get_scheme (uri);

	vuri->ends_in_slash = FALSE;

	if (strncmp (vuri->scheme, "all-", strlen ("all-")) == 0) {
		vuri->scheme += strlen ("all-");
		vuri->is_all_scheme = TRUE;
	} else
		vuri->is_all_scheme = FALSE;

	if (vuri->path != NULL) {
		int last_slash = strlen (vuri->path) - 1;
		char *first;

		/* Note: This handling of paths is somewhat evil, may need a
		 * bit of a rework */

		/* kill leading slashes, that is make sure there is
		 * only one */
		for (first = vuri->path; *first == '/'; first++)
			;
		if (first != vuri->path) {
			first--;
			vuri->path = first;
		}

		/* kill trailing slashes (leave first if all slashes) */
		while (last_slash > 0 && vuri->path [last_slash] == '/') {
			vuri->path [last_slash--] = '\0';
			vuri->ends_in_slash = TRUE;
		}

		/* get basename start */
		while (last_slash >= 0 && vuri->path [last_slash] != '/')
			last_slash--;

		if (last_slash > -1)
			vuri->file = vuri->path + last_slash + 1;
		else
			vuri->file = vuri->path;

		if (vuri->file[0] == '\0' &&
		    strcmp (vuri->path, "/") == 0) {
			vuri->file = NULL;
		}
	} else {
		vuri->ends_in_slash = TRUE;
		vuri->path = "/";
		vuri->file = NULL;
	}

	vuri->uri = uri;

	return TRUE;
}

#define VFOLDER_URI_PARSE(_uri, _vuri) {                                    \
	gchar *path;                                                        \
	path = gnome_vfs_unescape_string ((_uri)->text, G_DIR_SEPARATOR_S); \
	if (path != NULL) {                                                 \
		(_vuri)->path = g_alloca (strlen (path) + 1);               \
		strcpy ((_vuri)->path, path);                               \
		g_free (path);                                              \
	} else {                                                            \
		(_vuri)->path = NULL;                                       \
	}                                                                   \
	vfolder_uri_parse_internal ((_uri), (_vuri));                       \
}

static FileMonitorHandle *
file_monitor_handle_ref_unlocked (FileMonitorHandle *h)
{
	h->refcount ++;
	return h;
}

static void
file_monitor_handle_unref_unlocked (FileMonitorHandle *h)
{
	h->refcount --;
	if (h->refcount == 0) {
		gnome_vfs_uri_unref (h->uri);
		h->uri = NULL;

		g_free (h->filename);
		h->filename = NULL;

		if (h->handle != NULL) {
			gnome_vfs_monitor_cancel (h->handle);
			h->handle = NULL;
		}
	}
}

/* This includes the .directory files */
static void
emit_monitor (Folder *folder, int type)
{
	GSList *li;
	for (li = ((Entry *)folder)->monitors;
	     li != NULL;
	     li = li->next) {
		FileMonitorHandle *handle = li->data;
		gnome_vfs_monitor_callback ((GnomeVFSMethodHandle *) handle,
					    handle->uri, type);
	}
}

static void
emit_file_deleted_monitor (VFolderInfo *info, Entry *entry, Folder *folder)
{
	GSList *li;
	for (li = entry->monitors;
	     li != NULL;
	     li = li->next) {
		VFolderURI vuri;
		Folder *f;
		GnomeVFSResult result;
		FileMonitorHandle *handle = li->data;

		/* Evil! EVIL URI PARSING. this will eat a lot of
		 * stack if we have lots of monitors */

		VFOLDER_URI_PARSE (handle->uri, &vuri);

		f = resolve_folder (info, 
				    vuri.path,
				    TRUE /* ignore_basename */,
				    &result,
				    NULL);

		if (f == folder)
			gnome_vfs_monitor_callback
				((GnomeVFSMethodHandle *) handle,
				 handle->uri,
				 GNOME_VFS_MONITOR_EVENT_DELETED);
	}
}

static void
emit_and_delete_monitor (VFolderInfo *info, Folder *folder)
{
	GSList *li;
	for (li = ((Entry *)folder)->monitors;
	     li != NULL;
	     li = li->next) {
		FileMonitorHandle *handle = li->data;
		li->data = NULL;

		gnome_vfs_monitor_callback ((GnomeVFSMethodHandle *) handle,
					    handle->uri,
					    GNOME_VFS_MONITOR_EVENT_DELETED);

		if (handle->dir_monitor)
			info->free_folder_monitors = 
				g_slist_prepend (info->free_folder_monitors,
						 handle);
		else
			info->free_file_monitors = 
				g_slist_prepend (info->free_file_monitors,
						 handle);
	}
	g_slist_free (((Entry *)folder)->monitors);
	((Entry *)folder)->monitors = NULL;
}

static gboolean
check_ext (const char *name, const char *ext_check)
{
	const char *ext;

	ext = strrchr (name, '.');
	if (ext == NULL ||
	    strcmp (ext, ext_check) != 0)
		return FALSE;
	else
		return TRUE;
}

static StatLoc *
bake_statloc (const char *name,
	      time_t curtime)
{
	struct stat s;
	StatLoc *sl = NULL;
	if (stat (name, &s) != 0) {
		if (errno == ENOENT) {
			sl = g_malloc0 (sizeof (StatLoc) +
					strlen (name) + 1);
			sl->last_stat = curtime;
			sl->ctime = 0;
			sl->trigger_next = FALSE;
			strcpy (sl->name, name);
		}
		return sl;
	}

	sl = g_malloc0 (sizeof (StatLoc) +
			strlen (name) + 1);
	sl->last_stat = curtime;
	sl->ctime = s.st_ctime;
	sl->trigger_next = FALSE;
	strcpy (sl->name, name);

	return sl;
}

/* returns FALSE if we must reread */
static gboolean
check_statloc (StatLoc *sl,
	       time_t curtime)
{
	struct stat s;

	if (sl->trigger_next) {
		sl->trigger_next = FALSE;
		return FALSE;
	}

	/* don't stat more then once every 3 seconds */
	if (curtime <= sl->last_stat + 3)
		return TRUE;

	sl->last_stat = curtime;

	if (stat (sl->name, &s) != 0) {
		if (errno == ENOENT &&
		    sl->ctime == 0)
			return TRUE;
		else
			return FALSE;
	}

	if (sl->ctime == s.st_ctime)
		return TRUE;
	else
		return FALSE;
}

static gboolean
ensure_dir (const char *dirname, gboolean ignore_basename)
{
	char *parsed, *p;

	if (dirname == NULL)
		return FALSE;

	if (ignore_basename)
		parsed = g_path_get_dirname (dirname);
	else
		parsed = g_strdup (dirname);

	if (g_file_test (parsed, G_FILE_TEST_IS_DIR)) {
		g_free (parsed);
		return TRUE;
	}

	p = strchr (parsed, '/');
	if (p == parsed)
		p = strchr (p+1, '/');

	while (p != NULL) {
		*p = '\0';
		if (mkdir (parsed, 0700) != 0 &&
		    errno != EEXIST) {
			g_free (parsed);
			return FALSE;
		}
		*p = '/';
		p = strchr (p+1, '/');
	}

	if (mkdir (parsed, 0700) != 0 &&
	    errno != EEXIST) {
		g_free (parsed);
		return FALSE;
	}

	g_free (parsed);
	return TRUE;
}

/* check for any directory name other then root */
static gboolean
any_subdir (const char *dirname)
{
	const char *p;
	if (dirname == NULL)
		return FALSE;

	for (p = dirname; *p != '\0'; p++) {
		if (*p != '/') {
			return TRUE;
		}
	}
	return FALSE;
}

static void
destroy_entry_file (EntryFile *efile)
{
	if (efile == NULL)
		return;

	g_free (efile->filename);
	efile->filename = NULL;

	g_slist_free (efile->keywords);
	efile->keywords = NULL;

	g_free (efile);
}

static void
destroy_folder (Folder *folder)
{
	GSList *list;

	if (folder == NULL)
		return;

	if (folder->parent != NULL) {
		folder->parent->subfolders =
			g_slist_remove (folder->parent->subfolders, folder);
		folder->parent->up_to_date = FALSE;
		folder->parent = NULL;
	}

	g_free (folder->desktop_file);
	folder->desktop_file = NULL;

	query_destroy (folder->query);
	folder->query = NULL;

	if (folder->excludes != NULL) {
		g_hash_table_destroy (folder->excludes);
		folder->excludes = NULL;
	}

	g_slist_foreach (folder->includes, (GFunc)g_free, NULL);
	g_slist_free (folder->includes);
	folder->includes = NULL;
	if (folder->includes_ht != NULL) {
		g_hash_table_destroy (folder->includes_ht);
		folder->includes_ht = NULL;
	}

	list = folder->subfolders;
	folder->subfolders = NULL;
	g_slist_foreach (list, (GFunc)entry_unref, NULL);
	g_slist_free (list);

	list = folder->entries;
	folder->entries = NULL;
	g_slist_foreach (list, (GFunc)entry_unref, NULL);
	g_slist_free (list);

	g_free (folder);
}

static Entry *
entry_ref (Entry *entry)
{
	if (entry != NULL)
		entry->refcount++;
	return entry;
}

static Entry *
entry_ref_alloc (Entry *entry)
{
	entry_ref (entry);

	if (entry != NULL)
		entry->alloc++;

	return entry;
}

static void
entry_unref (Entry *entry)
{
	if (entry == NULL)
		return;

	entry->refcount--;

	if (entry->refcount == 0) {
		g_free (entry->name);
		entry->name = NULL;

		g_slist_foreach (entry->monitors,
				 (GFunc)file_monitor_handle_unref_unlocked,
				 NULL);
		g_slist_free (entry->monitors);
		entry->monitors = NULL;

		if (entry->type == ENTRY_FILE)
			destroy_entry_file ((EntryFile *)entry);
		else /* ENTRY_FOLDER */
			destroy_folder ((Folder *)entry);
	}
}

static void
entry_unref_dealloc (Entry *entry)
{
	if (entry != NULL) {
		entry->alloc --;
		entry_unref (entry);
	}
}

/* Handles ONLY files, not dirs */
/* Also allocates the entries as well as refs them */
static GSList *
alloc_entries_from_files (VFolderInfo *info, GSList *filenames)
{
	GSList *li;
	GSList *files;

	files = NULL;
	for (li = filenames; li != NULL; li = li->next) {
		char *filename = li->data;
		GSList *entry_list = g_hash_table_lookup (info->entries_ht, filename);
		if (entry_list != NULL)
			files = g_slist_prepend (files,
						 entry_ref_alloc (entry_list->data));
	}

	return files;
}

static gboolean
matches_query (VFolderInfo *info,
	       Folder *folder,
	       EntryFile *efile,
	       Query *query)
{
	GSList *li;

	if (query == NULL)
		return TRUE;

#define INVERT_IF_NEEDED(val) (query->not ? !(val) : (val))
	switch (query->type) {
	case QUERY_OR:
		for (li = query->queries; li != NULL; li = li->next) {
			Query *subquery = li->data;
			if (matches_query (info, folder, efile, subquery))
				return INVERT_IF_NEEDED (TRUE);
		}
		return INVERT_IF_NEEDED (FALSE);
	case QUERY_AND:
		for (li = query->queries; li != NULL; li = li->next) {
			Query *subquery = li->data;
			if ( ! matches_query (info, folder, efile, subquery))
				return INVERT_IF_NEEDED (FALSE);
		}
		return INVERT_IF_NEEDED (TRUE);
	case QUERY_KEYWORD:
		{
			QueryKeyword *qkeyword = (QueryKeyword *)query;
			for (li = efile->keywords; li != NULL; li = li->next) {
				GQuark keyword = GPOINTER_TO_INT (li->data);
				if (keyword == qkeyword->keyword)
					return INVERT_IF_NEEDED (TRUE);
			}
			return INVERT_IF_NEEDED (FALSE);
		}
	case QUERY_FILENAME:
		{
			QueryFilename *qfilename = (QueryFilename *)query;
			if (strcmp (qfilename->filename, ((Entry *)efile)->name) == 0) {
				return INVERT_IF_NEEDED (TRUE);
			} else {
				return INVERT_IF_NEEDED (FALSE);
			}
		}
	}
#undef INVERT_IF_NEEDED
	g_assert_not_reached ();
	/* huh? */
	return FALSE;
}

static void
dump_unallocated_folders (Folder *folder)
{
	GSList *li;
	for (li = folder->subfolders; li != NULL; li = li->next)
		dump_unallocated_folders (li->data);

	if (folder->only_unallocated &&
	    folder->entries != NULL) {
		g_slist_foreach (folder->entries,
				 (GFunc)entry_unref_dealloc, NULL);
		g_slist_free (folder->entries);
		folder->entries = NULL;
	}
}

/* Run query, allocs and refs the entries */
static void
append_query (VFolderInfo *info, Folder *folder)
{
	GSList *li;

	if (folder->query == NULL &&
	    ! folder->only_unallocated)
		return;

	if (folder->only_unallocated) {
		/* dump all folders that use unallocated
		 * items only.  This sucks if you keep
		 * reading one and then another such
		 * folder, but oh well, life sucks for
		 * you then, but at least you get
		 * consistent results */
		dump_unallocated_folders (info->root);

		/* ensure all other folders, so that
		 * after this we know which ones are
		 * unallocated */
		ensure_folder_unlocked (info,
					info->root,
					TRUE /* subfolders */,
					folder /* except */,
					/* avoid infinite loops */
					TRUE /* ignore_unallocated */);
	}

	for (li = info->entries; li != NULL; li = li->next) {
		Entry *entry = li->data;
		
		if (/* if not file */
		    entry->type != ENTRY_FILE ||
		    /* if already included */
		    (folder->includes_ht != NULL &&
		     g_hash_table_lookup (folder->includes_ht,
					  entry->name) != NULL))
			continue;

		if (folder->only_unallocated &&
		    entry->alloc != 0)
			continue;

		if (matches_query (info, folder, (EntryFile *)entry,
				   folder->query))
			folder->entries = g_slist_prepend
				(folder->entries, entry_ref_alloc (entry));
	}
}

/* get entries in folder */
/* FIXME: support cancellation here */
static void
ensure_folder_unlocked (VFolderInfo *info,
			Folder *folder,
			gboolean subfolders,
			Folder *except,
			gboolean ignore_unallocated)
{
	if (subfolders) {
		GSList *li;
		for (li = folder->subfolders; li != NULL; li = li->next)
			ensure_folder_unlocked (info, li->data, subfolders,
						except, ignore_unallocated);
	}

	if (except == folder)
		return;

	if (ignore_unallocated &&
	    folder->only_unallocated)
		return;

	if (folder->up_to_date)
		return;

	if (folder->entries != NULL) {
		g_slist_foreach (folder->entries,
				 (GFunc)entry_unref_dealloc, NULL);
		g_slist_free (folder->entries);
		folder->entries = NULL;
	}

	/* Include includes */
	folder->entries = alloc_entries_from_files (info, folder->includes);

	/* Run query */
	append_query (info, folder);

	/* We were prepending all this time */
	folder->entries = g_slist_reverse (folder->entries);

	/* Include subfolders */
	/* we always whack them onto the beginning */
	if (folder->subfolders != NULL) {
		GSList *subfolders = g_slist_copy (folder->subfolders);
		g_slist_foreach (subfolders, (GFunc)entry_ref_alloc, NULL);
		folder->entries = g_slist_concat (subfolders, folder->entries);
	}

	/* Exclude excludes */
	if (folder->excludes != NULL) {
		GSList *li;
		GSList *entries = folder->entries;
	       	folder->entries = NULL;
		for (li = entries; li != NULL; li = li->next) {
			Entry *entry = li->data;
			if (g_hash_table_lookup (folder->excludes, entry->name) == NULL)
				folder->entries = g_slist_prepend (folder->entries, entry);
			else
				entry_unref_dealloc (entry);

		}
		g_slist_free (entries);

		/* to preserve the Folders then everything else order */
		folder->entries = g_slist_reverse (folder->entries);
	}

	folder->up_to_date = TRUE;
	/* not yet sorted */
	folder->sorted = FALSE;
}

static void
ensure_folder (VFolderInfo *info,
	       Folder *folder,
	       gboolean subfolders,
	       Folder *except,
	       gboolean ignore_unallocated)
{
	G_LOCK (vfolder_lock);
	ensure_folder_unlocked (info, folder, subfolders, except, ignore_unallocated);
	G_UNLOCK (vfolder_lock);
}

static char *
get_directory_file_unlocked (VFolderInfo *info, Folder *folder)
{
	char *filename;

	/* FIXME: cache dir_files */
	
	if (folder->desktop_file == NULL)
		return NULL;

	if (folder->desktop_file[0] == G_DIR_SEPARATOR)
		return g_strdup (folder->desktop_file);

	/* Now try the user directory */
	if (info->user_desktop_dir != NULL) {
		filename = g_build_filename (info->user_desktop_dir,
					     folder->desktop_file,
					     NULL);
		if (access (filename, F_OK) == 0) {
			return filename;
		}

		g_free (filename);
	}

	filename = g_build_filename (info->desktop_dir, folder->desktop_file, NULL);
	if (access (filename, F_OK) == 0) {
		return filename;
	}
	g_free (filename);

	return NULL;
}

static char *
get_directory_file (VFolderInfo *info, Folder *folder)
{
	char *ret;

	G_LOCK (vfolder_lock);
	ret = get_directory_file_unlocked (info, folder);
	G_UNLOCK (vfolder_lock);

	return ret;
}

static GSList *
get_sort_order (VFolderInfo *info, Folder *folder)
{
	GSList *list;
	char **parsed;
	char *order;
	int i;
	char *filename;

	filename = get_directory_file_unlocked (info, folder);
	if (filename == NULL)
		return NULL;

	order = NULL;
	readitem_entry (filename,
			"SortOrder",
			&order,
			NULL,
			NULL);
	g_free (filename);

	if (order == NULL)
		return NULL;

	parsed = g_strsplit (order, ":", -1);

	g_free (order);

	list = NULL;
	for (i = 0; parsed[i] != NULL; i++) {
		char *word = parsed[i];
		/* steal */
		parsed[i] = NULL;
		/* ignore empty */
		if (word[0] == '\0') {
			g_free (word);
			continue;
		}
		list = g_slist_prepend (list, word);
	}
	/* we've stolen all strings from it */
	g_free (parsed);

	return g_slist_reverse (list);
}

/* get entries in folder */
static void
ensure_folder_sort (VFolderInfo *info, Folder *folder)
{
	GSList *li, *sort_order;
	GSList *entries;
	GHashTable *entry_hash;

	ensure_folder (info, folder,
		       FALSE /* subfolders */,
		       NULL /* except */,
		       FALSE /* ignore_unallocated */);
	if (folder->sorted)
		return;

	G_LOCK (vfolder_lock);

	sort_order = get_sort_order (info, folder);
	if (sort_order == NULL) {
		folder->sorted = TRUE;
		G_UNLOCK (vfolder_lock);
		return;
	}

	entries = folder->entries;
	folder->entries = NULL;

	entry_hash = g_hash_table_new (g_str_hash, g_str_equal);
	for (li = entries; li != NULL; li = li->next) {
		Entry *entry = li->data;
		g_hash_table_insert (entry_hash, entry->name, li);
	}

	for (li = sort_order; li != NULL; li = li->next) {
		char *word = li->data;
		GSList *entry_list;
		Entry *entry;

		/* we kill the words here */
		li->data = NULL;

		entry_list = g_hash_table_lookup (entry_hash, word);
		g_free (word);

		if (entry_list == NULL)
			continue;

		entry = entry_list->data;

		entries = g_slist_delete_link (entries, entry_list);

		folder->entries = g_slist_prepend (folder->entries,
						   entry);
	}

	/* put on those that weren't mentioned in the sort */
	for (li = entries; li != NULL; li = li->next) {
		Entry *entry = li->data;

		folder->entries = g_slist_prepend (folder->entries,
						   entry);
	}

	g_hash_table_destroy (entry_hash);
	g_slist_free (entries);
	g_slist_free (sort_order);

	folder->sorted = TRUE;

	G_UNLOCK (vfolder_lock);
}

static EntryFile *
file_new (const char *name)
{
	EntryFile *efile = g_new0 (EntryFile, 1);

	efile->entry.type = ENTRY_FILE;
	efile->entry.name = g_strdup (name);
	efile->entry.refcount = 1;

	return efile;
}

static Folder *
folder_new (const char *name)
{
	Folder *folder = g_new0 (Folder, 1);

	folder->entry.type = ENTRY_FOLDER;
	folder->entry.name = g_strdup (name);
	folder->entry.refcount = 1;

	return folder;
}

static Query *
query_new (int type)
{
	Query *query;

	if (type == QUERY_KEYWORD)
		query = (Query *)g_new0 (QueryKeyword, 1);
	else if (type == QUERY_FILENAME)
		query = (Query *)g_new0 (QueryFilename, 1);
	else
		query = g_new0 (Query, 1);

	query->type = type;

	return query;
}

static void
query_destroy (Query *query)
{
	if (query == NULL)
		return;

	if (query->type == QUERY_FILENAME) {
		QueryFilename *qfile = (QueryFilename *)query;
		g_free (qfile->filename);
		qfile->filename = NULL;
	} else if (query->type == QUERY_OR ||
		   query->type == QUERY_AND) {
		g_slist_foreach (query->queries, (GFunc)query_destroy, NULL);
		g_slist_free (query->queries);
		query->queries = NULL;
	}

	g_free (query);
}

static void
add_folder_monitor_unlocked (VFolderInfo *info,
			     FileMonitorHandle *handle)
{
	VFolderURI vuri;
	GnomeVFSResult result;
	Folder *folder;

	VFOLDER_URI_PARSE (handle->uri, &vuri);

	file_monitor_handle_ref_unlocked (handle);

	info->folder_monitors = 
		g_slist_prepend (info->folder_monitors, handle);

	folder = resolve_folder (info, 
				 vuri.path,
				 FALSE /* ignore_basename */,
				 &result,
				 NULL);

	if (folder == NULL) {
		file_monitor_handle_ref_unlocked (handle);

		info->free_folder_monitors = 
			g_slist_prepend (info->free_folder_monitors, handle);

		if (handle->exists) {
			handle->exists = FALSE;
			gnome_vfs_monitor_callback
				((GnomeVFSMethodHandle *)handle,
				 handle->uri, 
				 GNOME_VFS_MONITOR_EVENT_DELETED);
		}
	} else {
		file_monitor_handle_ref_unlocked (handle);

		((Entry *)folder)->monitors = 
			g_slist_prepend (((Entry *)folder)->monitors, handle);

		if ( ! handle->exists) {
			handle->exists = TRUE;
			gnome_vfs_monitor_callback
				((GnomeVFSMethodHandle *)handle,
				 handle->uri, 
				 GNOME_VFS_MONITOR_EVENT_CREATED);
		}
	}

}

static inline void
invalidate_folder_T (Folder *folder)
{
	folder->up_to_date = FALSE;

	invalidate_folder_subfolders (folder, TRUE);
}

static inline void
invalidate_folder (Folder *folder)
{
	G_LOCK (vfolder_lock);
	folder->up_to_date = FALSE;
	G_UNLOCK (vfolder_lock);

	invalidate_folder_subfolders (folder, FALSE);
}

static void
invalidate_folder_subfolders (Folder   *folder,
			      gboolean  lock_taken)
{
	GSList *li;

	for (li = folder->subfolders; li != NULL; li = li->next) {
		Folder *subfolder = li->data;

		if (!lock_taken)
			invalidate_folder (subfolder);
		else
			invalidate_folder_T (subfolder);
	}

	emit_monitor (folder, GNOME_VFS_MONITOR_EVENT_CHANGED);
}

/* FIXME: this is UGLY!, we need to figure out when the file
 * got finished changing! */
static gboolean
reread_timeout (gpointer data)
{
	VFolderInfo *info = data;
	gboolean force_read_items = info->file_monitors != NULL;
	vfolder_info_reload (info, NULL, NULL, force_read_items);
	return FALSE;
}

static void
queue_reread_in (VFolderInfo *info, int msec)
{
	G_LOCK (vfolder_lock);
	if (info->reread_queue != 0)
		g_source_remove (info->reread_queue);
	info->reread_queue = g_timeout_add (msec, reread_timeout, info);
	G_UNLOCK (vfolder_lock);
}

static void
vfolder_desktop_dir_monitor (GnomeVFSMonitorHandle *handle,
			     const gchar *monitor_uri,
			     const gchar *info_uri,
			     GnomeVFSMonitorEventType event_type,
			     gpointer user_data)
{
	/* FIXME: implement */
}

static void
vfolder_user_desktop_dir_monitor (GnomeVFSMonitorHandle *handle,
				  const gchar *monitor_uri,
				  const gchar *info_uri,
				  GnomeVFSMonitorEventType event_type,
				  gpointer user_data)
{
	/* FIXME: implement */
}

static void
vfolder_filename_monitor (GnomeVFSMonitorHandle *handle,
			  const gchar *monitor_uri,
			  const gchar *info_uri,
			  GnomeVFSMonitorEventType event_type,
			  gpointer user_data)
{
	VFolderInfo *info = user_data;

	if ((event_type == GNOME_VFS_MONITOR_EVENT_CREATED ||
	     event_type == GNOME_VFS_MONITOR_EVENT_CHANGED) &&
	    ! info->user_file_active) {
		queue_reread_in (info, 200);
	} else if (event_type == GNOME_VFS_MONITOR_EVENT_DELETED &&
		   ! info->user_file_active) {
		/* FIXME: is this correct?  I mean now
		 * there probably isn't ANY vfolder file, so we
		 * init to default values really.  I have no clue what's
		 * right here */
		vfolder_info_reload (info, NULL, NULL,
				     TRUE /* force read items */);
	}
}

static void
vfolder_user_filename_monitor (GnomeVFSMonitorHandle *handle,
			       const gchar *monitor_uri,
			       const gchar *info_uri,
			       GnomeVFSMonitorEventType event_type,
			       gpointer user_data)
{
	VFolderInfo *info = user_data;

	if ((event_type == GNOME_VFS_MONITOR_EVENT_CREATED ||
	     event_type == GNOME_VFS_MONITOR_EVENT_CHANGED) &&
	    info->user_file_active) {
		struct stat s;

		/* see if this was really our own change */
		if (info->user_filename_last_write == time (NULL))
			return;
		/* anal retentive */
		if (stat (info->user_filename, &s) == 0 &&
		    info->user_filename_last_write == s.st_ctime)
			return;

		queue_reread_in (info, 200);
	} else if ((event_type == GNOME_VFS_MONITOR_EVENT_CREATED ||
		    event_type == GNOME_VFS_MONITOR_EVENT_CHANGED) &&
		    ! info->user_file_active) {
		queue_reread_in (info, 200);
	} else if (event_type == GNOME_VFS_MONITOR_EVENT_DELETED &&
		   info->user_file_active) {
		gboolean force_read_items = info->file_monitors != NULL;
		vfolder_info_reload (info, NULL, NULL, force_read_items);
	}
}

static void
item_dir_monitor (GnomeVFSMonitorHandle *handle,
		  const gchar *monitor_uri,
		  const gchar *info_uri,
		  GnomeVFSMonitorEventType event_type,
		  gpointer user_data)
{
	VFolderInfo *info = user_data;

	if (event_type == GNOME_VFS_MONITOR_EVENT_CREATED ||
	    event_type == GNOME_VFS_MONITOR_EVENT_CHANGED) {
		/* first invalidate all folders */
		invalidate_folder (info->root);
		/* second invalidate all entries */
		info->entries_valid = FALSE;

		if (info->file_monitors != NULL) {
			GnomeVFSResult result;
			GSList *li;

			/* Whack all monitors here! */
			for (li = info->file_monitors;
			     li != NULL;
			     li = li->next) {
				FileMonitorHandle *h = li->data;
				if (h->handle != NULL)
					gnome_vfs_monitor_cancel (h->handle);
				h->handle = NULL;
			}

			if (vfolder_info_read_items (info, &result, NULL)) {
				info->entries_valid = TRUE;
			}
		}
	}
}

static gboolean
setup_dir_monitor (VFolderInfo *info, const char *dir, gboolean subdirs,
		   GnomeVFSResult *result,
		   GnomeVFSContext *context)
{
	GnomeVFSMonitorHandle *handle;
	DIR *dh;
	struct dirent *de;
	char *uri;

	uri = gnome_vfs_get_uri_from_local_path (dir);

	if (gnome_vfs_monitor_add (&handle,
				   uri,
				   GNOME_VFS_MONITOR_DIRECTORY,
				   item_dir_monitor,
				   info) != GNOME_VFS_OK) {
		StatLoc *sl = bake_statloc (dir, time (NULL));
		if (sl != NULL)
			info->stat_dirs = g_slist_prepend (info->stat_dirs, sl);
		g_free (uri);
		return TRUE;
	}
	g_free (uri);

	if (gnome_vfs_context_check_cancellation (context)) {
		gnome_vfs_monitor_cancel (handle);
		*result = GNOME_VFS_ERROR_CANCELLED;
		return FALSE;
	}

	info->item_dir_monitors =
		g_slist_prepend (info->item_dir_monitors, handle);

	if ( ! subdirs)
		return TRUE;

	dh = opendir (dir);
	if (dh == NULL)
		return TRUE;

	while ((de = readdir (dh)) != NULL) {
		char *full_path;

		if (gnome_vfs_context_check_cancellation (context)) {
			*result = GNOME_VFS_ERROR_CANCELLED;
			closedir (dh);
			return FALSE;
		}

		if (de->d_name[0] == '.')
			continue;

		full_path = g_build_filename (dir, de->d_name, NULL);
		if (g_file_test (full_path, G_FILE_TEST_IS_DIR)) {
			if ( ! setup_dir_monitor (info, full_path,
						  TRUE /* subdirs */,
						  result, context)) {
				closedir (dh);
				return FALSE;
			}
		}
		g_free (full_path);
	}

	closedir (dh);

	return TRUE;
}

static gboolean
monitor_setup (VFolderInfo *info,
	       gboolean setup_filenames,
	       gboolean setup_itemdirs,
	       gboolean setup_desktop_dirs,
	       GnomeVFSResult *result,
	       GnomeVFSContext *context)
{
	char *uri;
	GSList *li;

	if (setup_filenames) {
		uri = gnome_vfs_get_uri_from_local_path
			(info->filename);

		if (gnome_vfs_monitor_add (&info->filename_monitor,
					   uri,
					   GNOME_VFS_MONITOR_FILE,
					   vfolder_filename_monitor,
					   info) != GNOME_VFS_OK) {
			info->filename_monitor = NULL;
			info->filename_statloc = bake_statloc (info->filename,
							       time (NULL));
		}
		g_free (uri);
	}
	if (setup_filenames &&
	    info->user_filename != NULL) {
		uri = gnome_vfs_get_uri_from_local_path
			(info->user_filename);
		if (gnome_vfs_monitor_add (&info->user_filename_monitor,
					   uri,
					   GNOME_VFS_MONITOR_FILE,
					   vfolder_user_filename_monitor,
					   info) != GNOME_VFS_OK) {
			info->user_filename_monitor = NULL;
			info->user_filename_statloc =
				bake_statloc (info->user_filename,
					      time (NULL));
		}

		g_free (uri);
	}

	if (gnome_vfs_context_check_cancellation (context)) {
		*result = GNOME_VFS_ERROR_CANCELLED;
		return FALSE;
	}

	if (setup_itemdirs) {
		for (li = info->item_dirs; li != NULL; li = li->next) {
			const char *dir = li->data;
			if ( ! setup_dir_monitor (info, dir,
						  FALSE /* subdirs */,
						  result, context))
				return FALSE;
		}
		if (info->user_item_dir != NULL) {
			if ( ! setup_dir_monitor (info, info->user_item_dir,
						  FALSE /* subdirs */,
						  result, context))
				return FALSE;
		}
		for (li = info->merge_dirs; li != NULL; li = li->next) {
			const char *dir = li->data;
			if ( ! setup_dir_monitor (info, dir,
						  TRUE /* subdirs */,
						  result, context))
				return FALSE;
		}
	}

	if (setup_desktop_dirs) {
		uri = gnome_vfs_get_uri_from_local_path
			(info->desktop_dir);

		if (gnome_vfs_monitor_add (&info->desktop_dir_monitor,
					   uri,
					   GNOME_VFS_MONITOR_FILE,
					   vfolder_desktop_dir_monitor,
					   info) != GNOME_VFS_OK) {
			info->desktop_dir_monitor = NULL;
			info->desktop_dir_statloc =
				bake_statloc (info->desktop_dir,
					      time (NULL));
		}
		g_free (uri);
	}
	if (setup_desktop_dirs &&
	    info->user_desktop_dir != NULL) {
		uri = gnome_vfs_get_uri_from_local_path
			(info->user_desktop_dir);
		if (gnome_vfs_monitor_add (&info->user_desktop_dir_monitor,
					   uri,
					   GNOME_VFS_MONITOR_DIRECTORY,
					   vfolder_user_desktop_dir_monitor,
					   info) != GNOME_VFS_OK) {
			info->user_desktop_dir_monitor = NULL;
			info->user_desktop_dir_statloc =
				bake_statloc (info->user_desktop_dir,
					      time (NULL));
		}

		g_free (uri);
	}

	return TRUE;
}

static void
vfolder_info_init (VFolderInfo *info, const char *scheme)
{
	const char *path;
	GSList *list;

	info->scheme = g_strdup (scheme);

	info->filename = g_strconcat (SYSCONFDIR,
				      "/gnome-vfs-2.0/vfolders/",
				      scheme, ".vfolder-info",
				      NULL);
	info->user_filename = g_strconcat (g_get_home_dir (),
					   "/" DOT_GNOME "/vfolders/",
					   scheme, ".vfolder-info",
					   NULL);
	info->desktop_dir = g_strconcat (SYSCONFDIR,
					 "/gnome-vfs-2.0/vfolders/",
					 NULL);
	info->user_desktop_dir = g_strconcat (g_get_home_dir (),
					      "/" DOT_GNOME "/vfolders/",
					      NULL);

	/* Init the desktop paths */
	list = NULL;
	list = g_slist_prepend (list, g_strdup ("/usr/share/applications/"));
	if (strcmp ("/usr/share/applications/", DATADIR "/applications/") != 0)
		list = g_slist_prepend (list, g_strdup (DATADIR "/applications/"));
	path = g_getenv ("DESKTOP_FILE_PATH");
	if (path != NULL) {
		int i;
		char **ppath = g_strsplit (path, ":", -1);
		for (i = 0; ppath[i] != NULL; i++) {
			const char *dir = ppath[i];
			list = g_slist_prepend (list, g_strdup (dir));
		}
		g_strfreev (ppath);
	}
	info->item_dirs = g_slist_reverse (list);

	info->user_item_dir = g_strconcat (g_get_home_dir (),
					   "/" DOT_GNOME "/vfolders/",
					   scheme,
					   NULL);

	info->entries_ht = g_hash_table_new (g_str_hash, g_str_equal);

	info->root = folder_new ("Root");

	info->modification_time = time (NULL);
}

static void
vfolder_info_free_internals_unlocked (VFolderInfo *info)
{
	if (info == NULL)
		return;
	
	if (info->filename_monitor != NULL) {
		gnome_vfs_monitor_cancel (info->filename_monitor);
		info->filename_monitor = NULL;
	}

	if (info->user_filename_monitor != NULL) {
		gnome_vfs_monitor_cancel (info->user_filename_monitor);
		info->user_filename_monitor = NULL;
	}

	g_free (info->filename_statloc);
	info->filename_statloc = NULL;

	g_free (info->user_filename_statloc);
	info->user_filename_statloc = NULL;


	if (info->desktop_dir_monitor != NULL) {
		gnome_vfs_monitor_cancel (info->desktop_dir_monitor);
		info->desktop_dir_monitor = NULL;
	}

	if (info->user_desktop_dir_monitor != NULL) {
		gnome_vfs_monitor_cancel (info->user_desktop_dir_monitor);
		info->user_desktop_dir_monitor = NULL;
	}

	g_free (info->desktop_dir_statloc);
	info->desktop_dir_statloc = NULL;

	g_free (info->user_desktop_dir_statloc);
	info->user_desktop_dir_statloc = NULL;


	g_slist_foreach (info->item_dir_monitors,
			 (GFunc)gnome_vfs_monitor_cancel, NULL);
	g_slist_free (info->item_dir_monitors);
	info->item_dir_monitors = NULL;

	g_free (info->scheme);
	info->scheme = NULL;

	g_free (info->filename);
	info->filename = NULL;

	g_free (info->user_filename);
	info->user_filename = NULL;

	g_free (info->desktop_dir);
	info->desktop_dir = NULL;

	g_free (info->user_desktop_dir);
	info->user_desktop_dir = NULL;

	g_slist_foreach (info->item_dirs, (GFunc)g_free, NULL);
	g_slist_free (info->item_dirs);
	info->item_dirs = NULL;

	g_free (info->user_item_dir);
	info->user_item_dir = NULL;

	g_slist_foreach (info->merge_dirs, (GFunc)g_free, NULL);
	g_slist_free (info->merge_dirs);
	info->merge_dirs = NULL;

	g_slist_foreach (info->entries, (GFunc)entry_unref, NULL);
	g_slist_free (info->entries);
	info->entries = NULL;

	if (info->entries_ht != NULL)
		g_hash_table_destroy (info->entries_ht);
	info->entries_ht = NULL;

	g_slist_foreach (info->unallocated_folders,
			 (GFunc)entry_unref,
			 NULL);
	g_slist_free (info->unallocated_folders);
	info->unallocated_folders = NULL;

	entry_unref ((Entry *)info->root);
	info->root = NULL;

	g_slist_foreach (info->stat_dirs, (GFunc)g_free, NULL);
	g_slist_free (info->stat_dirs);
	info->stat_dirs = NULL;

	g_slist_foreach (info->folder_monitors,
			 (GFunc)file_monitor_handle_unref_unlocked, NULL);
	g_slist_free (info->folder_monitors);
	info->folder_monitors = NULL;

	g_slist_foreach (info->free_folder_monitors,
			 (GFunc)file_monitor_handle_unref_unlocked, NULL);
	g_slist_free (info->free_folder_monitors);
	info->free_folder_monitors = NULL;

	g_slist_foreach (info->file_monitors,
			 (GFunc)file_monitor_handle_unref_unlocked, NULL);
	g_slist_free (info->file_monitors);
	info->file_monitors = NULL;

	g_slist_foreach (info->free_file_monitors,
			 (GFunc)file_monitor_handle_unref_unlocked, NULL);
	g_slist_free (info->free_file_monitors);
	info->free_file_monitors = NULL;

	if (info->reread_queue != 0)
		g_source_remove (info->reread_queue);
	info->reread_queue = 0;
}

static void
vfolder_info_free_internals (VFolderInfo *info)
{
	G_LOCK (vfolder_lock);
	vfolder_info_free_internals_unlocked (info);
	G_UNLOCK (vfolder_lock);
}

static void
vfolder_info_destroy (VFolderInfo *info)
{
	vfolder_info_free_internals (info);
	g_free (info);
}

static Query *
single_query_read (xmlNode *qnode)
{
	Query *query;
	xmlNode *node;

	if (qnode->type != XML_ELEMENT_NODE ||
	    qnode->name == NULL)
		return NULL;

	query = NULL;

	if (g_ascii_strcasecmp (qnode->name, "Not") == 0 &&
	    qnode->xmlChildrenNode != NULL) {
		xmlNode *iter;
		query = NULL;
		for (iter = qnode->xmlChildrenNode;
		     iter != NULL && query == NULL;
		     iter = iter->next)
			query = single_query_read (iter);
		if (query != NULL) {
			query->not = ! query->not;
		}
		return query;
	} else if (g_ascii_strcasecmp (qnode->name, "Keyword") == 0) {
		xmlChar *word = xmlNodeGetContent (qnode);
		if (word != NULL) {
			query = query_new (QUERY_KEYWORD);
			((QueryKeyword *)query)->keyword =
				g_quark_from_string (word);

			xmlFree (word);
		}
		return query;
	} else if (g_ascii_strcasecmp (qnode->name, "Filename") == 0) {
		xmlChar *file = xmlNodeGetContent (qnode);
		if (file != NULL) {
			query = query_new (QUERY_FILENAME);
			((QueryFilename *)query)->filename =
				g_strdup (file);

			xmlFree (file);
		}
		return query;
	} else if (g_ascii_strcasecmp (qnode->name, "And") == 0) {
		query = query_new (QUERY_AND);
	} else if (g_ascii_strcasecmp (qnode->name, "Or") == 0) {
		query = query_new (QUERY_OR);
	} else {
		/* We don't understand */
		return NULL;
	}

	/* This must be OR or AND */
	g_assert (query != NULL);

	for (node = qnode->xmlChildrenNode; node != NULL; node = node->next) {
		Query *new_query = single_query_read (node);

		if (new_query != NULL)
			query->queries = g_slist_prepend
				(query->queries, new_query);
	}

	query->queries = g_slist_reverse (query->queries);

	return query;
}

static void
add_or_set_query (Query **query, Query *new_query)
{
	if (*query == NULL) {
		*query = new_query;
	} else {
		Query *old_query = *query;
		*query = query_new (QUERY_OR);
		(*query)->queries = 
			g_slist_append ((*query)->queries, old_query);
		(*query)->queries = 
			g_slist_append ((*query)->queries, new_query);
	}
}

static Query *
query_read (xmlNode *qnode)
{
	Query *query;
	xmlNode *node;

	query = NULL;

	for (node = qnode->xmlChildrenNode; node != NULL; node = node->next) {
		if (node->type != XML_ELEMENT_NODE ||
		    node->name == NULL)
			continue;

		if (g_ascii_strcasecmp (node->name, "Not") == 0 &&
		    node->xmlChildrenNode != NULL) {
			xmlNode *iter;
			Query *new_query = NULL;

			for (iter = node->xmlChildrenNode;
			     iter != NULL && new_query == NULL;
			     iter = iter->next)
				new_query = single_query_read (iter);
			if (new_query != NULL) {
				new_query->not = ! new_query->not;
				add_or_set_query (&query, new_query);
			}
		} else {
			Query *new_query = single_query_read (node);
			if (new_query != NULL)
				add_or_set_query (&query, new_query);
		}
	}

	return query;
}

static Folder *
folder_read (VFolderInfo *info, xmlNode *fnode)
{
	Folder *folder;
	xmlNode *node;

	folder = folder_new (NULL);

	for (node = fnode->xmlChildrenNode; node != NULL; node = node->next) {
		if (node->type != XML_ELEMENT_NODE ||
		    node->name == NULL)
			continue;

		if (g_ascii_strcasecmp (node->name, "Name") == 0) {
			xmlChar *name = xmlNodeGetContent (node);
			if (name != NULL) {
				g_free (folder->entry.name);
				folder->entry.name = g_strdup (name);
				xmlFree (name);
			}
		} else if (g_ascii_strcasecmp (node->name, "Desktop") == 0) {
			xmlChar *desktop = xmlNodeGetContent (node);
			if (desktop != NULL) {
				g_free (folder->desktop_file);
				folder->desktop_file = g_strdup (desktop);
				xmlFree (desktop);
			}
		} else if (g_ascii_strcasecmp (node->name, "Include") == 0) {
			xmlChar *file = xmlNodeGetContent (node);
			if (file != NULL) {
				GSList *li;
				char *str = g_strdup (file);
				folder->includes = g_slist_prepend
					(folder->includes, str);
				if (folder->includes_ht == NULL) {
					folder->includes_ht =
						g_hash_table_new_full
						(g_str_hash,
						 g_str_equal,
						 NULL,
						 NULL);
				}
				li = g_hash_table_lookup (folder->includes_ht,
							  file);
				if (li != NULL) {
					g_free (li->data);
					/* Note: this will NOT change folder->includes
					 * pointer! */
					folder->includes = g_slist_delete_link
						(folder->includes, li);
				}
				g_hash_table_replace (folder->includes_ht, 
						      file, folder->includes);
				xmlFree (file);
			}
		} else if (g_ascii_strcasecmp (node->name, "Exclude") == 0) {
			xmlChar *file = xmlNodeGetContent (node);
			if (file != NULL) {
				char *s;
				if (folder->excludes == NULL) {
					folder->excludes = g_hash_table_new_full
						(g_str_hash,
						 g_str_equal,
						 (GDestroyNotify)g_free,
						 NULL);
				}
				s = g_strdup (file);
				g_hash_table_replace (folder->excludes, s, s);
				xmlFree (file);
			}
		} else if (g_ascii_strcasecmp (node->name, "Query") == 0) {
			Query *query;

			query = query_read (node);

			if (query != NULL) {
				if (folder->query != NULL)
					query_destroy (folder->query);
				folder->query = query;
			}
		} else if (g_ascii_strcasecmp (node->name, "OnlyUnallocated") == 0) {
			info->unallocated_folders = 
				g_slist_prepend (info->unallocated_folders,
						 (Folder *)entry_ref ((Entry *)folder));
			folder->only_unallocated = TRUE;
		} else if (g_ascii_strcasecmp (node->name, "Folder") == 0) {
			Folder *new_folder = folder_read (info, node);
			if (new_folder != NULL) {
				folder->subfolders =
					g_slist_append (folder->subfolders,
							new_folder);
				new_folder->parent = folder;
			}
		} else if (g_ascii_strcasecmp (node->name, "ReadOnly") == 0) {
			folder->read_only = TRUE;
		} else if (g_ascii_strcasecmp (node->name,
					       "DontShowIfEmpty") == 0) {
			folder->dont_show_if_empty = TRUE;
		}
	}

	/* Name is required */
	if (folder->entry.name == NULL) {
		entry_unref ((Entry *)folder);
		folder = NULL;
	}

	folder->includes = g_slist_reverse (folder->includes);

	return folder;
}

static char *
subst_home (const char *dir)
{
	if (dir[0] == '~')
		return g_strconcat (g_get_home_dir (),
				    &dir[1],
				    NULL);
	else	
		return g_strdup (dir);
}

/* FORMAT looks like:
 * <VFolderInfo>
 *   <!-- Merge dirs optional -->
 *   <MergeDir>/etc/X11/applnk</MergeDir>
 *   <!-- Only specify if it should override standard location -->
 *   <ItemDir>/usr/share/applications</ItemDir>
 *   <!-- This is where the .directories are -->
 *   <DesktopDir>/etc/X11/gnome/vfolders</DesktopDir>
 *   <!-- Root folder -->
 *   <Folder>
 *     <Name>Root</Name>
 *
 *     <Include>important.desktop</Include>
 *
 *     <!-- Other folders -->
 *     <Folder>
 *       <Name>SomeFolder</Name>
 *     </Folder>
 *     <Folder>
 *       <Name>Test_Folder</Name>
 *       <!-- could also be absolute -->
 *       <Desktop>Test_Folder.directory</Desktop>
 *       <Query>
 *         <Or>
 *           <And>
 *             <Keyword>Application</Keyword>
 *             <Keyword>Game</Keyword>
 *           </And>
 *           <Keyword>Clock</Keyword>
 *         </Or>
 *       </Query>
 *       <Include>somefile.desktop</Include>
 *       <Include>someotherfile.desktop</Include>
 *       <Exclude>yetanother.desktop</Exclude>
 *     </Folder>
 *   </Folder>
 * </VFolderInfo>
 */

static gboolean
vfolder_info_read_info (VFolderInfo *info,
			GnomeVFSResult *result,
			GnomeVFSContext *context)
{
	xmlDoc *doc;
	xmlNode *node;
	gboolean got_a_vfolder_dir = FALSE;

	doc = NULL;
	if (info->user_filename != NULL &&
	    access (info->user_filename, F_OK) == 0) {
		doc = xmlParseFile (info->user_filename); 
		if (doc != NULL)
			info->user_file_active = TRUE;
	}
	if (doc == NULL &&
	    access (info->filename, F_OK) == 0)
		doc = xmlParseFile (info->filename); 

	if (gnome_vfs_context_check_cancellation (context)) {
		xmlFreeDoc(doc);
		*result = GNOME_VFS_ERROR_CANCELLED;
		return FALSE;
	}

	if (doc == NULL
	    || doc->xmlRootNode == NULL
	    || doc->xmlRootNode->name == NULL
	    || g_ascii_strcasecmp (doc->xmlRootNode->name, "VFolderInfo") != 0) {
		xmlFreeDoc(doc);
		return TRUE; /* FIXME: really, shouldn't we error out? */
	}

	for (node = doc->xmlRootNode->xmlChildrenNode; node != NULL; node = node->next) {
		if (node->type != XML_ELEMENT_NODE ||
		    node->name == NULL)
			continue;

		if (gnome_vfs_context_check_cancellation (context)) {
			xmlFreeDoc(doc);
			*result = GNOME_VFS_ERROR_CANCELLED;
			return FALSE;
		}

		if (g_ascii_strcasecmp (node->name, "MergeDir") == 0) {
			xmlChar *dir = xmlNodeGetContent (node);
			if (dir != NULL) {
				info->merge_dirs = g_slist_append (info->merge_dirs,
								   g_strdup (dir));
				xmlFree (dir);
			}
		} else if (g_ascii_strcasecmp (node->name, "ItemDir") == 0) {
			xmlChar *dir = xmlNodeGetContent (node);
			if (dir != NULL) {
				if ( ! got_a_vfolder_dir) {
					g_slist_foreach (info->item_dirs,
							 (GFunc)g_free, NULL);
					g_slist_free (info->item_dirs);
					info->item_dirs = NULL;
				}
				got_a_vfolder_dir = TRUE;
				info->item_dirs = g_slist_append (info->item_dirs,
								  g_strdup (dir));
				xmlFree (dir);
			}
		} else if (g_ascii_strcasecmp (node->name, "UserItemDir") == 0) {
			xmlChar *dir = xmlNodeGetContent (node);
			if (dir != NULL) {
				g_free (info->user_item_dir);
				info->user_item_dir = subst_home (dir);
				xmlFree (dir);
			}
		} else if (g_ascii_strcasecmp (node->name, "DesktopDir") == 0) {
			xmlChar *dir = xmlNodeGetContent (node);
			if (dir != NULL) {
				g_free (info->desktop_dir);
				info->desktop_dir = g_strdup (dir);
				xmlFree (dir);
			}
		} else if (g_ascii_strcasecmp (node->name, "UserDesktopDir") == 0) {
			xmlChar *dir = xmlNodeGetContent (node);
			if (dir != NULL) {
				g_free (info->user_desktop_dir);
				info->user_desktop_dir = subst_home (dir);
				xmlFree (dir);
			}
		} else if (g_ascii_strcasecmp (node->name, "Folder") == 0) {
			Folder *folder = folder_read (info, node);
			if (folder != NULL) {
				if (info->root != NULL)
					entry_unref ((Entry *)info->root);
				info->root = folder;
			}
		} else if (g_ascii_strcasecmp (node->name, "ReadOnly") == 0) {
			info->read_only = TRUE;
		}
	}

	xmlFreeDoc(doc);

	return TRUE;
}

static void
add_xml_tree_from_query (xmlNode *parent, Query *query)
{
	xmlNode *real_parent;

	if (query->not)
		real_parent = xmlNewChild (parent /* parent */,
					   NULL /* ns */,
					   "Not" /* name */,
					   NULL /* content */);
	else
		real_parent = parent;

	if (query->type == QUERY_KEYWORD) {
		QueryKeyword *qkeyword = (QueryKeyword *)query;
		const char *string = g_quark_to_string (qkeyword->keyword);

		xmlNewChild (real_parent /* parent */,
			     NULL /* ns */,
			     "Keyword" /* name */,
			     string /* content */);
	} else if (query->type == QUERY_FILENAME) {
		QueryFilename *qfilename = (QueryFilename *)query;

		xmlNewChild (real_parent /* parent */,
			     NULL /* ns */,
			     "Filename" /* name */,
			     qfilename->filename /* content */);
	} else if (query->type == QUERY_OR ||
		   query->type == QUERY_AND) {
		xmlNode *node;
		const char *name;
		GSList *li;

		if (query->type == QUERY_OR)
			name = "Or";
		else /* QUERY_AND */
			name = "And";

		node = xmlNewChild (real_parent /* parent */,
				    NULL /* ns */,
				    name /* name */,
				    NULL /* content */);

		for (li = query->queries; li != NULL; li = li->next) {
			Query *subquery = li->data;
			add_xml_tree_from_query (node, subquery);
		}
	} else {
		g_assert_not_reached ();
	}
}

static void
add_excludes_to_xml (gpointer key, gpointer value, gpointer user_data)
{
	const char *filename = key;
	xmlNode *folder_node = user_data;

	xmlNewChild (folder_node /* parent */,
		     NULL /* ns */,
		     "Exclude" /* name */,
		     filename /* content */);
}

static void
add_xml_tree_from_folder (xmlNode *parent, Folder *folder)
{
	GSList *li;
	xmlNode *folder_node;


	folder_node = xmlNewChild (parent /* parent */,
				   NULL /* ns */,
				   "Folder" /* name */,
				   NULL /* content */);

	xmlNewChild (folder_node /* parent */,
		     NULL /* ns */,
		     "Name" /* name */,
		     folder->entry.name /* content */);

	if (folder->desktop_file != NULL) {
		xmlNewChild (folder_node /* parent */,
			     NULL /* ns */,
			     "Desktop" /* name */,
			     folder->desktop_file /* content */);
	}

	if (folder->read_only)
		xmlNewChild (folder_node /* parent */,
			     NULL /* ns */,
			     "ReadOnly" /* name */,
			     NULL /* content */);
	if (folder->dont_show_if_empty)
		xmlNewChild (folder_node /* parent */,
			     NULL /* ns */,
			     "DontShowIfEmpty" /* name */,
			     NULL /* content */);
	if (folder->only_unallocated)
		xmlNewChild (folder_node /* parent */,
			     NULL /* ns */,
			     "OnlyUnallocated" /* name */,
			     NULL /* content */);

	for (li = folder->subfolders; li != NULL; li = li->next) {
		Folder *subfolder = li->data;
		add_xml_tree_from_folder (folder_node, subfolder);
	}

	for (li = folder->includes; li != NULL; li = li->next) {
		const char *include = li->data;
		xmlNewChild (folder_node /* parent */,
			     NULL /* ns */,
			     "Include" /* name */,
			     include /* content */);
	}

	if (folder->excludes) {
		g_hash_table_foreach (folder->excludes,
				      add_excludes_to_xml,
				      folder_node);
	}

	if (folder->query != NULL) {
		xmlNode *query_node;
		query_node = xmlNewChild (folder_node /* parent */,
					  NULL /* ns */,
					  "Query" /* name */,
					  NULL /* content */);

		add_xml_tree_from_query (query_node, folder->query);
	}
}

static xmlDoc *
xml_tree_from_vfolder (VFolderInfo *info)
{
	xmlDoc *doc;
	xmlNode *topnode;
	GSList *li;

	doc = xmlNewDoc ("1.0");

	topnode = xmlNewDocNode (doc /* doc */,
				 NULL /* ns */,
				 "VFolderInfo" /* name */,
				 NULL /* content */);
	doc->xmlRootNode = topnode;

	for (li = info->merge_dirs; li != NULL; li = li->next) {
		const char *merge_dir = li->data;
		xmlNewChild (topnode /* parent */,
			     NULL /* ns */,
			     "MergeDir" /* name */,
			     merge_dir /* content */);
	}
	
	for (li = info->item_dirs; li != NULL; li = li->next) {
		const char *item_dir = li->data;
		xmlNewChild (topnode /* parent */,
			     NULL /* ns */,
			     "ItemDir" /* name */,
			     item_dir /* content */);
	}

	if (info->user_item_dir != NULL) {
		xmlNewChild (topnode /* parent */,
			     NULL /* ns */,
			     "UserItemDir" /* name */,
			     info->user_item_dir /* content */);
	}

	if (info->desktop_dir != NULL) {
		xmlNewChild (topnode /* parent */,
			     NULL /* ns */,
			     "DesktopDir" /* name */,
			     info->desktop_dir /* content */);
	}

	if (info->user_desktop_dir != NULL) {
		xmlNewChild (topnode /* parent */,
			     NULL /* ns */,
			     "UserDesktopDir" /* name */,
			     info->user_desktop_dir /* content */);
	}

	if (info->root != NULL)
		add_xml_tree_from_folder (topnode, info->root);

	return doc;
}

/* FIXME: what to do about errors */
static void
vfolder_info_write_user (VFolderInfo *info)
{
	xmlDoc *doc;

	if (info->inhibit_write > 0)
		return;

	if (info->user_filename == NULL)
		return;

	doc = xml_tree_from_vfolder (info);
	if (doc == NULL)
		return;

	/* FIXME: errors, anyone? */
	ensure_dir (info->user_filename,
		    TRUE /* ignore_basename */);

	xmlSaveFormatFile (info->user_filename, doc, TRUE /* format */);
	/* not as good as a stat, but cheaper ... hmmm what is
	 * the likelyhood of this not being the same as ctime */
	info->user_filename_last_write = time (NULL);

	xmlFreeDoc(doc);

	info->user_file_active = TRUE;
	info->dirty = FALSE;

	info->modification_time = time (NULL);
}

/* An EVIL function for quick reading of .desktop files,
 * only reads in one or two keys, but that's ALL we need */
static void
readitem_entry (const char *filename,
		const char *key1,
		char **result1,
		const char *key2,
		char **result2)
{
	FILE *fp;
	char buf[1024];
	int keylen1, keylen2;

	*result1 = NULL;
	if (result2 != NULL)
		*result2 = NULL;

	fp = fopen (filename, "r");

	if (fp == NULL)
		return;

	keylen1 = strlen (key1);
	if (key2 != NULL)
		keylen2 = strlen (key2);
	else
		keylen2 = -1;

	/* This is slightly wrong, it should only look
	 * at the correct section */
	while (fgets (buf, sizeof (buf), fp) != NULL) {
		char *p;
		int len;
		int keylen;
		char **result = NULL;

		/* check if it's one of the keys */
		if (strncmp (buf, key1, keylen1) == 0) {
			result = result1;
			keylen = keylen1;
		} else if (keylen2 >= 0 &&
			   strncmp (buf, key2, keylen2) == 0) {
			result = result2;
			keylen = keylen2;
		} else {
			continue;
		}

		p = &buf[keylen];

		/* still not our key */
		if (!(*p == '=' || *p == ' ')) {
			continue;
		}
		do
			p++;
		while (*p == ' ' || *p == '=');

		/* get rid of trailing \n */
		len = strlen (p);
		if (p[len-1] == '\n' ||
		    p[len-1] == '\r')
			p[len-1] = '\0';

		*result = g_strdup (p);

		if (*result1 == NULL ||
		    (result2 != NULL && *result2 == NULL))
			break;
	}

	fclose (fp);
}

static void
vfolder_info_insert_entry (VFolderInfo *info, EntryFile *efile)
{
	GSList *entry_list;

	entry_ref ((Entry *)efile);

	entry_list = g_hash_table_lookup (info->entries_ht, efile->entry.name);

	info->entries = g_slist_prepend (info->entries, efile);
	/* The hash table contains the GSList pointer */
	g_hash_table_replace (info->entries_ht, efile->entry.name, 
			     info->entries);

	if (entry_list != NULL) {
		Entry *entry = entry_list->data;
		info->entries = g_slist_delete_link (info->entries, 
						     entry_list);
		entry_unref (entry);
	}
}

static void
set_keywords (EntryFile *efile, const char *keywords)
{
	if (keywords != NULL) {
		int i;
		char **parsed = g_strsplit (keywords, ";", -1);
		for (i = 0; parsed[i] != NULL; i++) {
			GQuark quark;
			const char *word = parsed[i];
			/* ignore empties (including end of list) */
			if (word[0] == '\0')
				continue;
			quark = g_quark_from_string (word);
			efile->keywords = g_slist_prepend
				(efile->keywords,
				 GINT_TO_POINTER (quark));
		}
		g_strfreev (parsed);
	}
}

static EntryFile *
make_entry_file (const char *dir, const char *name)
{
	EntryFile *efile;
	char *categories;
	char *only_show_in;
	char *filename;
	int i;

	filename = g_build_filename (dir, name, NULL);

	readitem_entry (filename,
			"Categories",
			&categories,
			"OnlyShowIn",
			&only_show_in);

	if (only_show_in != NULL) {
		gboolean show = FALSE;
		char **parsed = g_strsplit (only_show_in, ";", -1);
		for (i = 0; parsed[i] != NULL; i++) {
			if (strcmp (parsed[i], "GNOME") == 0) {
				show = TRUE;
				break;
			}
		}
		g_strfreev (parsed);
		if ( ! show) {
			g_free (filename);
			g_free (only_show_in);
			g_free (categories);
			return NULL;
		}
	}

	efile = file_new (name);
	efile->filename = filename;

	set_keywords (efile, categories);

	g_free (only_show_in);
	g_free (categories);

	return efile;
}

static gboolean
vfolder_info_read_items_from (VFolderInfo *info,
			      const char *item_dir,
			      gboolean per_user,
			      GnomeVFSResult *result,
			      GnomeVFSContext *context)
{
	DIR *dir;
	struct dirent *de;

	dir = opendir (item_dir);
	if (dir == NULL)
		return TRUE;

	while ((de = readdir (dir)) != NULL) {
		EntryFile *efile;

		if (gnome_vfs_context_check_cancellation (context)) {
			closedir (dir);
			*result = GNOME_VFS_ERROR_CANCELLED;
			return FALSE;
		}

		/* files MUST be called .desktop */
		if (de->d_name[0] == '.' ||
		    ! check_ext (de->d_name, ".desktop"))
			continue;

		efile = make_entry_file (item_dir, de->d_name);
		if (efile == NULL)
			continue;

		efile->per_user = per_user;

		vfolder_info_insert_entry (info, efile);
		entry_unref ((Entry *)efile);
	}

	closedir (dir);

	return TRUE;
}

static gboolean
vfolder_info_read_items_merge (VFolderInfo *info,
			       const char *merge_dir,
			       const char *subdir,
			       GQuark inherited_keyword,
			       GnomeVFSResult *result,
			       GnomeVFSContext *context)
{
	DIR *dir;
	struct dirent *de;
	GQuark extra_keyword;
	GQuark Application;
	GQuark Merged;
	GQuark inheritance;
	gboolean pass_down_extra_keyword = TRUE;

	dir = opendir (merge_dir);
	if (dir == NULL)
		return TRUE;

	Application = g_quark_from_static_string ("Application");
	Merged = g_quark_from_static_string ("Merged");

	/* FIXME: this should be a hash or something */
	extra_keyword = 0;
	if (subdir == NULL) {
		extra_keyword = g_quark_from_static_string ("Core");
		pass_down_extra_keyword = FALSE;
	} else if (g_ascii_strcasecmp (subdir, "Development") == 0)
		extra_keyword = g_quark_from_static_string ("Development");
	else if (g_ascii_strcasecmp (subdir, "Editors") == 0)
		extra_keyword = g_quark_from_static_string ("TextEditor");
	else if (g_ascii_strcasecmp (subdir, "Games") == 0)
		extra_keyword = g_quark_from_static_string ("Game");
	else if (g_ascii_strcasecmp (subdir, "Graphics") == 0)
		extra_keyword = g_quark_from_static_string ("Graphics");
	else if (g_ascii_strcasecmp (subdir, "Internet") == 0)
		extra_keyword = g_quark_from_static_string ("Network");
	else if (g_ascii_strcasecmp (subdir, "Multimedia") == 0)
		extra_keyword = g_quark_from_static_string ("AudioVideo");
	else if (g_ascii_strcasecmp (subdir, "Office") == 0)
		extra_keyword = g_quark_from_static_string ("Office");
	else if (g_ascii_strcasecmp (subdir, "Settings") == 0)
		extra_keyword = g_quark_from_static_string ("Settings");
	else if (g_ascii_strcasecmp (subdir, "System") == 0)
		extra_keyword = g_quark_from_static_string ("System");
	else if (g_ascii_strcasecmp (subdir, "Utilities") == 0)
		extra_keyword = g_quark_from_static_string ("Utility");

	while ((de = readdir (dir)) != NULL) {
		EntryFile *efile;

		if (gnome_vfs_context_check_cancellation (context)) {
			closedir (dir);
			*result = GNOME_VFS_ERROR_CANCELLED;
			return FALSE;
		}

		/* ignore hidden */
		if (de->d_name[0] == '.')
			continue;

		/* files MUST be called .desktop, so
		 * treat all others as dirs.  If we're wrong,
		 * the open will fail, which is ok */
		if ( ! check_ext (de->d_name, ".desktop")) {
			/* if this is a directory recurse */
			char *fullname = g_build_filename (merge_dir, de->d_name, NULL);
			if ((pass_down_extra_keyword == TRUE) && (extra_keyword != 0)) {
				inheritance = extra_keyword;
			} else {
				inheritance = inherited_keyword;
			}

			if ( ! vfolder_info_read_items_merge (info,
							      fullname,
							      de->d_name,
							      inheritance,
							      result,
							      context)) {
				g_free (fullname);
				return FALSE;
			}
			g_free (fullname);
			continue;
		}

		/* FIXME: add some keywords about some known apps
		 * like gimp and whatnot, perhaps take these from the vfolder
		 * file or some such */

		efile = make_entry_file (merge_dir, de->d_name);
		if (efile == NULL)
			continue;

		/* If no keywords set, then add the standard ones */
		if (efile->keywords == NULL) {
			efile->keywords = g_slist_prepend
				(efile->keywords,
				 GINT_TO_POINTER (Application));

			efile->keywords = g_slist_prepend
				(efile->keywords,
				 GINT_TO_POINTER (Merged));

			if (inherited_keyword != 0) {
				efile->keywords = g_slist_prepend
					(efile->keywords,
					 GINT_TO_POINTER (inherited_keyword));
			}
			
			if (extra_keyword != 0) {
				efile->keywords = g_slist_prepend
					(efile->keywords,
					 GINT_TO_POINTER (extra_keyword));
			}
			efile->implicit_keywords = TRUE;
		}

		vfolder_info_insert_entry (info, efile);
		entry_unref ((Entry *)efile);
	}

	closedir (dir);

	return TRUE;
}

static Entry *
find_entry (GSList *list, const char *name)
{
	GSList *li;

	for (li = list; li != NULL; li = li->next) {
		Entry *entry = li->data;
		if (strcmp (name, entry->name) == 0)
			return entry;
	}
	return NULL;
}

static void
file_monitor (GnomeVFSMonitorHandle *handle,
	      const gchar *monitor_uri,
	      const gchar *info_uri,
	      GnomeVFSMonitorEventType event_type,
	      gpointer user_data)
{
	FileMonitorHandle *h = user_data;

	/* proxy the event through if it is a changed event
	 * only */

	if (event_type == GNOME_VFS_MONITOR_EVENT_CHANGED &&
	    h->handle != NULL)
		gnome_vfs_monitor_callback ((GnomeVFSMethodHandle *) h,
					    h->uri, event_type);
}

static void
try_free_file_monitors_create_files_unlocked (VFolderInfo *info)
{
	GSList *li, *list;

	list = g_slist_copy (info->free_file_monitors);

	for (li = list; li != NULL; li = li->next) {
		FileMonitorHandle *handle = li->data;
		Entry *entry;
		GnomeVFSResult result;
		char *dirfile = NULL;

		if (handle->is_directory_file) {
			VFolderURI vuri;
			Folder *folder;

			/* Evil! EVIL URI PARSING. this will eat a lot of
			 * stack if we have lots of free monitors */

			VFOLDER_URI_PARSE (handle->uri, &vuri);

			folder = resolve_folder (info, 
						 vuri.path,
						 TRUE /* ignore_basename */,
						 &result,
						 NULL);

			if (folder == NULL)
				continue;

			dirfile = get_directory_file_unlocked (info, folder);
			if (dirfile == NULL)
				continue;

			entry = (Entry *)folder;
		} else {
			VFolderURI vuri;
			Folder *f;
			GnomeVFSResult result;

			entry = NULL;

			/* Evil! EVIL URI PARSING. this will eat a lot of
			 * stack if we have lots of monitors */

			VFOLDER_URI_PARSE (handle->uri, &vuri);

			f = resolve_folder (info, 
					    vuri.path,
					    TRUE /* ignore_basename */,
					    &result,
					    NULL);

			if (f != NULL) {
				ensure_folder_unlocked (
					info, f,
					FALSE /* subfolders */,
					NULL /* except */,
					FALSE /* ignore_unallocated */);
				entry = find_entry (f->entries, vuri.file);
			}

			if (entry == NULL)
				continue;
		}

		info->free_file_monitors =
			g_slist_remove (info->free_file_monitors, handle);
		entry->monitors =
			g_slist_prepend (entry->monitors, handle);

		handle->exists = TRUE;
		gnome_vfs_monitor_callback ((GnomeVFSMethodHandle *)handle,
					    handle->uri, 
					    GNOME_VFS_MONITOR_EVENT_CREATED);

		/* recreate a handle */
		if (handle->handle == NULL &&
		    entry->type == ENTRY_FILE) {
			EntryFile *efile = (EntryFile *)entry;
			char *uri = gnome_vfs_get_uri_from_local_path
				(efile->filename);

			gnome_vfs_monitor_add (&(handle->handle),
					       uri,
					       GNOME_VFS_MONITOR_FILE,
					       file_monitor,
					       handle);

			g_free (uri);
		} else if (handle->handle == NULL &&
			   dirfile != NULL) {
			char *uri = gnome_vfs_get_uri_from_local_path (dirfile);

			gnome_vfs_monitor_add (&(handle->handle),
					       uri,
					       GNOME_VFS_MONITOR_FILE,
					       file_monitor,
					       handle);

			g_free (uri);
		}

		g_free (dirfile);
	}

	g_slist_free (list);
}

static void /* unlocked */
rescan_monitors (VFolderInfo *info)
{
	GSList *li;

	if (info->file_monitors == NULL)
		return;

	for (li = info->file_monitors; li != NULL; li = li->next) {
		FileMonitorHandle *h = li->data;
		GnomeVFSResult result;
		Entry *entry;
		char *dirfile = NULL;

		/* these are handled below */
		if ( ! h->exists)
			continue;

		if (h->is_directory_file) {
			VFolderURI vuri;
			Folder *folder;

			/* Evil! EVIL URI PARSING. this will eat a lot of
			 * stack if we have lots of monitors */

			VFOLDER_URI_PARSE (h->uri, &vuri);

			folder = resolve_folder (info, 
						 vuri.path,
						 TRUE /* ignore_basename */,
						 &result,
						 NULL);
			if (folder != NULL)
				dirfile = get_directory_file_unlocked (info,
								       folder);

			if (dirfile == NULL) {
				h->exists = FALSE;
				gnome_vfs_monitor_callback
					((GnomeVFSMethodHandle *)h,
					 h->uri, 
					 GNOME_VFS_MONITOR_EVENT_DELETED);
				info->free_file_monitors = g_slist_prepend
					(info->free_file_monitors, h);
				file_monitor_handle_ref_unlocked (h);
				/* it has been unreffed when the entry was
				 * whacked */
				continue;
			}

			entry = (Entry *)folder;
		} else {
			VFolderURI vuri;
			Folder *f;
			GnomeVFSResult result;

			entry = NULL;

			/* Evil! EVIL URI PARSING. this will eat a lot of
			 * stack if we have lots of monitors */

			VFOLDER_URI_PARSE (h->uri, &vuri);

			f = resolve_folder (info, 
					    vuri.path,
					    TRUE /* ignore_basename */,
					    &result,
					    NULL);

			if (f != NULL) {
				ensure_folder_unlocked (
					info, f,
					FALSE /* subfolders */,
					NULL /* except */,
					FALSE /* ignore_unallocated */);
				entry = find_entry (f->entries, vuri.file);
			}

			if (entry == NULL) {
				h->exists = FALSE;
				gnome_vfs_monitor_callback
					((GnomeVFSMethodHandle *)h,
					 h->uri, 
					 GNOME_VFS_MONITOR_EVENT_DELETED);
				info->free_file_monitors = g_slist_prepend
					(info->free_file_monitors, h);
				file_monitor_handle_ref_unlocked (h);
				/* it has been unreffed when the entry was
				 * whacked */
				continue;
			}
		}

		/* recreate a handle */
		if (h->handle == NULL &&
		    entry->type == ENTRY_FILE) {
			EntryFile *efile = (EntryFile *)entry;
			char *uri = gnome_vfs_get_uri_from_local_path
				(efile->filename);

			gnome_vfs_monitor_add (&(h->handle),
					       uri,
					       GNOME_VFS_MONITOR_FILE,
					       file_monitor,
					       h);

			g_free (uri);
		} else if (h->handle == NULL &&
			   dirfile != NULL) {
			char *uri = gnome_vfs_get_uri_from_local_path (dirfile);

			gnome_vfs_monitor_add (&(h->handle),
					       uri,
					       GNOME_VFS_MONITOR_FILE,
					       file_monitor,
					       h);

			g_free (uri);
		}

		g_free (dirfile);
	}

	try_free_file_monitors_create_files_unlocked (info);
}

static gboolean /* unlocked */
vfolder_info_read_items (VFolderInfo *info,
			 GnomeVFSResult *result,
			 GnomeVFSContext *context)
{
	GSList *li;

	/* First merge */
	for (li = info->merge_dirs; li != NULL; li = li->next) {
		const char *merge_dir = li->data;

		if ( ! vfolder_info_read_items_merge (info, merge_dir, NULL, FALSE,
						      result, context))
			return FALSE;
	}

	/* Then read the real thing (later overrides) */
	for (li = info->item_dirs; li != NULL; li = li->next) {
		const char *item_dir = li->data;

		if ( ! vfolder_info_read_items_from (info, item_dir,
						     FALSE /* per_user */,
						     result, context))
			return FALSE;
	}

	if (info->user_item_dir != NULL) {
		if ( ! vfolder_info_read_items_from (info,
						     info->user_item_dir,
						     TRUE /* per_user */,
						     result, context))
			return FALSE;
	}

	rescan_monitors (info);

	return TRUE;
}

static gboolean
string_slist_equal (GSList *list1, GSList *list2)
{
	GSList *li1, *li2;

	for (li1 = list1, li2 = list2;
	     li1 != NULL && li2 != NULL;
	     li1 = li1->next, li2 = li2->next) {
		const char *s1 = li1->data;
		const char *s2 = li2->data;
		if (strcmp (s1, s2) != 0)
			return FALSE;
	}
	/* if both are not NULL, then lengths are
	 * different */
	if (li1 != li2)
		return FALSE;
	return TRUE;
}

static gboolean
safe_string_same (const char *string1, const char *string2)
{
	if (string1 == string2 &&
	    string1 == NULL)
		return TRUE;

	if (string1 != NULL && string2 != NULL &&
	    strcmp (string1, string2) == 0)
		return TRUE;
	
	return FALSE;
}

static gboolean
vfolder_info_item_dirs_same (VFolderInfo *info1, VFolderInfo *info2)
{
	if ( ! string_slist_equal (info1->item_dirs,
				   info2->item_dirs))
		return FALSE;

	if ( ! string_slist_equal (info1->merge_dirs,
				   info2->merge_dirs))
		return FALSE;

	if ( ! safe_string_same (info1->user_item_dir,
				 info2->user_item_dir))
		return FALSE;

	return TRUE;
}

static gboolean
vfolder_info_reload_unlocked (VFolderInfo *info,
			      GnomeVFSResult *result,
			      GnomeVFSContext *context,
			      gboolean force_read_items)
{
	VFolderInfo *newinfo;
	gboolean setup_filenames;
	gboolean setup_itemdirs;
	GSList *li;

	/* FIXME: Hmmm, race, there is no locking YAIKES,
	 * we need filename locking for changes.  eek, eek, eek */
	if (info->dirty) {
		return TRUE;
	}

	newinfo = g_new0 (VFolderInfo, 1);
	vfolder_info_init (newinfo, info->scheme);

	g_free (newinfo->filename);
	g_free (newinfo->user_filename);
	newinfo->filename = g_strdup (info->filename);
	newinfo->user_filename = g_strdup (info->user_filename);

	if (gnome_vfs_context_check_cancellation (context)) {
		vfolder_info_destroy (newinfo);
		*result = GNOME_VFS_ERROR_CANCELLED;
		return FALSE;
	}

	if ( ! vfolder_info_read_info (newinfo, result, context)) {
		vfolder_info_destroy (newinfo);
		return FALSE;
	}

	/* FIXME: reload logic for 'desktop_dir' and
	 * 'user_desktop_dir' */

	setup_itemdirs = TRUE;

	/* Validity of entries and item dirs and all that is unchanged */
	if (vfolder_info_item_dirs_same (info, newinfo)) {
		newinfo->entries = info->entries;
		info->entries = NULL;
		newinfo->entries_ht = info->entries_ht;
		info->entries_ht = NULL /* some places assume this
					   non-null, but we're only
					   going to destroy this */;
		newinfo->entries_valid = info->entries_valid;

		/* move over the monitors/statlocs since those are valid */
		newinfo->item_dir_monitors = info->item_dir_monitors;
		info->item_dir_monitors = NULL;
		newinfo->stat_dirs = info->stat_dirs;
		info->stat_dirs = NULL;

		/* No need to resetup dir monitors */
		setup_itemdirs = FALSE;

		/* No need to do anything with file monitors */
	} else {
		/* Whack all monitors here! */
		for (li = info->file_monitors; li != NULL; li = li->next) {
			FileMonitorHandle *h = li->data;
			if (h->handle != NULL)
				gnome_vfs_monitor_cancel (h->handle);
			h->handle = NULL;
		}
	}

	setup_filenames = TRUE;

	if (safe_string_same (info->filename, newinfo->filename) &&
	    safe_string_same (info->user_filename, newinfo->user_filename)) {
		newinfo->user_filename_last_write =
			info->user_filename_last_write;

		/* move over the monitors/statlocs since those are valid */
		newinfo->filename_monitor = info->filename_monitor;
		info->filename_monitor = NULL;
		newinfo->user_filename_monitor = info->user_filename_monitor;
		info->user_filename_monitor = NULL;

		if (info->filename_statloc != NULL &&
		    info->filename != NULL)
			newinfo->filename_statloc =
				bake_statloc (info->filename,
					      time (NULL));
		if (info->user_filename_statloc != NULL &&
		    info->user_filename != NULL)
			newinfo->user_filename_statloc =
				bake_statloc (info->user_filename,
					      time (NULL));

		/* No need to resetup filename monitors */
		setup_filenames = FALSE;
	}

	/* Note: not cancellable anymore, since we've
	 * already started nibbling on the info structure,
	 * so we'd need to back things out or some such,
	 * too complex, so screw that */
	monitor_setup (info,
		       setup_filenames,
		       setup_itemdirs,
		       /* FIXME: setup_desktop_dirs */ TRUE,
		       NULL, NULL);

	for (li = info->folder_monitors;
	     li != NULL;
	     li = li->next) {
		FileMonitorHandle *handle = li->data;
		li->data = NULL;

		add_folder_monitor_unlocked (newinfo, handle);

		file_monitor_handle_unref_unlocked (handle);
	}
	g_slist_free (info->folder_monitors);
	info->folder_monitors = NULL;

	g_slist_foreach (info->free_folder_monitors,
			 (GFunc)file_monitor_handle_unref_unlocked, NULL);
	g_slist_free (info->free_folder_monitors);
	info->folder_monitors = NULL;

	/* we can just copy these for now, they will be readded
	 * and all the fun stuff will be done with them later */
	newinfo->file_monitors = info->file_monitors;
	info->file_monitors = NULL;
	newinfo->free_file_monitors = info->free_file_monitors;
	info->free_file_monitors = NULL;

	/* emit changed on all folders, a bit drastic, but oh well,
	 * we also invalidate all folders at the same time, but that is
	 * irrelevant since they should all just be invalid to begin with */
	invalidate_folder_T (info->root);

	/* FIXME: make sure if this was enough, I think it was */

	vfolder_info_free_internals_unlocked (info);
	memcpy (info, newinfo, sizeof (VFolderInfo));
	g_free (newinfo);

	/* must rescan the monitors here */
	if (info->entries_valid) {
		rescan_monitors (info);
	}

	if ( ! info->entries_valid &&
	    force_read_items) {
		GnomeVFSResult res;
		/* FIXME: I bet cancelation plays havoc with monitors,
		 * I'm not sure however */
		if (info->file_monitors != NULL) {
			vfolder_info_read_items (info, &res, NULL);
		} else {
			if ( ! vfolder_info_read_items (info, result, context))
				return FALSE;
		}
		info->entries_valid = TRUE;
	}

	return TRUE;
}

static gboolean
vfolder_info_reload (VFolderInfo *info,
		     GnomeVFSResult *result,
		     GnomeVFSContext *context,
		     gboolean force_read_items)
{
	G_LOCK (vfolder_lock);
	if (vfolder_info_reload_unlocked (info, result, context,
					  force_read_items)) {
		G_UNLOCK (vfolder_lock);
		return TRUE;
	} else {
		G_UNLOCK (vfolder_lock);
		return FALSE;
	}
}

static gboolean
vfolder_info_recheck (VFolderInfo *info,
		      GnomeVFSResult *result,
		      GnomeVFSContext *context)
{
	GSList *li;
	time_t curtime = time (NULL);
	gboolean reread = FALSE;

	if (info->filename_statloc != NULL &&
	     ! check_statloc (info->filename_statloc, curtime)) {
		if ( ! vfolder_info_reload_unlocked (info, result, context, 
						     FALSE /* force read items */)) {
			/* we have failed, make sure we fail
			 * next time too */
			info->filename_statloc->trigger_next = TRUE;
			return FALSE;
		}
		reread = TRUE;
	}
	if ( ! reread &&
	    info->user_filename_statloc != NULL &&
	     ! check_statloc (info->user_filename_statloc, curtime)) {
		if ( ! vfolder_info_reload_unlocked (info, result, context, 
						     FALSE /* force read items */)) {
			/* we have failed, make sure we fail
			 * next time too */
			info->user_filename_statloc->trigger_next = TRUE;
			return FALSE;
		}
		reread = TRUE;
	}

	if (info->entries_valid) {
		for (li = info->stat_dirs; li != NULL; li = li->next) {
			StatLoc *sl = li->data;
			if ( ! check_statloc (sl, curtime)) {
				info->entries_valid = FALSE;
				break;
			}		       
		}
	}
	return TRUE;
}

static VFolderInfo *
get_vfolder_info_unlocked (const char      *scheme,
			   GnomeVFSResult  *result,
			   GnomeVFSContext *context)
{
	VFolderInfo *info;

	if (infos != NULL &&
	    (info = g_hash_table_lookup (infos, scheme)) != NULL) {
		if ( ! vfolder_info_recheck (info, result, context)) {
			return NULL;
		}
		if ( ! info->entries_valid) {
			g_slist_foreach (info->entries,
					 (GFunc)entry_unref, NULL);
			g_slist_free (info->entries);
			info->entries = NULL;

			if (info->entries_ht != NULL)
				g_hash_table_destroy (info->entries_ht);
			info->entries_ht = g_hash_table_new (g_str_hash,
							     g_str_equal);

			if ( ! vfolder_info_read_items (info,
							result, context)) {
				info->entries_valid = FALSE;
				return NULL;
			}

			invalidate_folder_T (info->root);

			info->entries_valid = TRUE;
		}
		return info;
	}

	if (gnome_vfs_context_check_cancellation (context)) {
		*result = GNOME_VFS_ERROR_CANCELLED;
		return NULL;
	}

	if (infos == NULL)
		infos = g_hash_table_new_full
			(g_str_hash, g_str_equal,
			 (GDestroyNotify)g_free,
			 (GDestroyNotify)vfolder_info_destroy);

	info = g_new0 (VFolderInfo, 1);
	vfolder_info_init (info, scheme);

	if (gnome_vfs_context_check_cancellation (context)) {
		vfolder_info_destroy (info);
		*result = GNOME_VFS_ERROR_CANCELLED;
		return NULL;
	}

	if ( ! vfolder_info_read_info (info, result, context)) {
		vfolder_info_destroy (info);
		return NULL;
	}

	if ( ! monitor_setup (info,
			      TRUE /* setup_filenames */,
			      TRUE /* setup_itemdirs */,
			      TRUE /* setup_desktop_dirs */,
			      result, context)) {
		vfolder_info_destroy (info);
		return NULL;
	}

	g_hash_table_insert (infos, g_strdup (scheme), info);

	if ( ! vfolder_info_read_items (info, result, context)) {
		info->entries_valid = FALSE;
		return NULL;
	}
	info->entries_valid = TRUE;

	return info;
}

static VFolderInfo *
get_vfolder_info (const char *scheme,
		  GnomeVFSResult *result,
		  GnomeVFSContext *context)
{
	VFolderInfo *info;
	G_LOCK (vfolder_lock);
	info = get_vfolder_info_unlocked (scheme, result, context);
	G_UNLOCK (vfolder_lock);
	return info;
}


static char *
keywords_to_string (GSList *keywords)
{
	GSList *li;
	GString *str = g_string_new (NULL);

	for (li = keywords; li != NULL; li = li->next) {
		GQuark word = GPOINTER_TO_INT (li->data);
		g_string_append (str, g_quark_to_string (word));
		g_string_append_c (str, ';');
	}

	return g_string_free (str, FALSE);
}

/* copy file and add keywords line */
static gboolean
copy_file_with_keywords (const char *from, const char *to, GSList *keywords)
{
	FILE *fp;
	FILE *wfp;
	int wfd;
	char buf[BUFSIZ];
	char *keyword_string;

	if ( ! ensure_dir (to,
			   TRUE /* ignore_basename */))
		return FALSE;

	wfd = open (to, O_CREAT | O_WRONLY | O_TRUNC, 0600);
	if (wfd < 0) {
		return FALSE;
	}

	keyword_string = keywords_to_string (keywords);

	wfp = fdopen (wfd, "w");

	fp = fopen (from, "r");
	if (fp != NULL) {
		gboolean wrote_keywords = FALSE;
		while (fgets (buf, sizeof (buf), fp) != NULL) {
			fprintf (wfp, "%s", buf);
			if ( ! wrote_keywords &&
			    (strncmp (buf, "[Desktop Entry]",
				      strlen ("[Desktop Entry]")) == 0 ||
			     strncmp (buf, "[KDE Desktop Entry]",
				      strlen ("[KDE Desktop Entry]")) == 0)) {
				fprintf (wfp, "Categories=%s\n",
					 keyword_string);
				wrote_keywords = TRUE;
			}
		}

		fclose (fp);
	} else {
		fprintf (wfp, "[Desktop Entry]\nCategories=%s\n",
			 keyword_string);
	}

	/* FIXME: does this close wfd???? */
	fclose (wfp);

	close (wfd);

	g_free (keyword_string);

	return TRUE;
}

static gboolean
copy_file (const char *from, const char *to)
{
	int fd;
	int wfd;

	if ( ! ensure_dir (to,
			   TRUE /* ignore_basename */))
		return FALSE;

	wfd = open (to, O_CREAT | O_WRONLY | O_TRUNC, 0600);
	if (wfd < 0) {
		return FALSE;
	}

	fd = open (from, O_RDONLY);
	if (fd >= 0) {
		char buf[1024];
		ssize_t n;

		while ((n = read (fd, buf, sizeof(buf))) > 0) {
			write (wfd, buf, n);
		}

		close (fd);
	}

	close (wfd);

	return TRUE;
}

static gboolean
make_file_private (VFolderInfo *info, EntryFile *efile)
{
	char *newfname;
	Entry *entry = (Entry *)efile;

	if (efile->per_user)
		return TRUE;

	/* this file already exists so whack its monitors */
	if (efile->filename != NULL) {
		GSList *li;

		for (li = entry->monitors; li != NULL; li = li->next) {
			FileMonitorHandle *h = li->data;
			if (h->handle != NULL)
				gnome_vfs_monitor_cancel (h->handle);
			h->handle = NULL;
		}
	}

	newfname = g_build_filename (g_get_home_dir (),
				     DOT_GNOME,
				     "vfolders",
				     info->scheme,
				     efile->entry.name,
				     NULL);

	if (efile->implicit_keywords) {
		if (efile->filename != NULL &&
		    ! copy_file_with_keywords (efile->filename,
					       newfname,
					       efile->keywords)) {
			/* FIXME: what to do with monitors here, they
			 * have already been whacked, a corner case
			 * not handled! */
			g_free (newfname);
			return FALSE;
		}
	} else {
		if (efile->filename != NULL &&
		    ! copy_file (efile->filename, newfname)) {
			/* FIXME: what to do with monitors here, they
			 * have already been whacked, a corner case
			 * not handled! */
			g_free (newfname);
			return FALSE;
		}
	}

	/* we didn't copy but ensure path anyway */
	if (efile->filename == NULL &&
	    ! ensure_dir (newfname,
			  TRUE /* ignore_basename */)) {
		g_free (newfname);
		return FALSE;
	}

	/* this file already exists so re-add monitors at the new location */
	if (efile->filename != NULL) {
		GSList *li;
		char *uri = gnome_vfs_get_uri_from_local_path (newfname);

		for (li = entry->monitors; li != NULL; li = li->next) {
			FileMonitorHandle *h = li->data;

			gnome_vfs_monitor_add (&(h->handle),
					       uri,
					       GNOME_VFS_MONITOR_FILE,
					       file_monitor,
					       h);
		}

		g_free (uri);
	}

	g_free (efile->filename);
	efile->filename = newfname;
	efile->per_user = TRUE;

	return TRUE;
}

static void
try_free_file_monitors_create_dirfile_unlocked (VFolderInfo *info,
						Folder *folder)
{
	GSList *li, *list;

	list = g_slist_copy (info->free_file_monitors);

	for (li = list; li != NULL; li = li->next) {
		FileMonitorHandle *handle = li->data;
		Folder *f;
		VFolderURI vuri;
		GnomeVFSResult result;

		if ( ! handle->is_directory_file)
			continue;

		/* Evil! EVIL URI PARSING. this will eat a lot of stack if we
		 * have lots of free monitors */

		VFOLDER_URI_PARSE (handle->uri, &vuri);

		f = resolve_folder (info, 
				    vuri.path,
				    TRUE /* ignore_basename */,
				    &result,
				    NULL);

		if (folder != f)
			continue;

		info->free_file_monitors =
			g_slist_remove (info->free_file_monitors, handle);
		((Entry *)folder)->monitors =
			g_slist_prepend (((Entry *)folder)->monitors, handle);

		handle->exists = TRUE;
		gnome_vfs_monitor_callback ((GnomeVFSMethodHandle *)handle,
					    handle->uri, 
					    GNOME_VFS_MONITOR_EVENT_CREATED);
	}

	g_slist_free (list);
}

static void
make_new_dirfile (VFolderInfo *info, Folder *folder)
{
	char *name = g_strdup (folder->entry.name);
	char *fname;
	char *p;
	int i;
	int fd;

	for (p = name; *p != '\0'; p++) {
		if ( ! ( (*p >= 'a' && *p <= 'z') ||
			 (*p >= 'A' && *p <= 'Z') ||
			 (*p >= '0' && *p <= '9') ||
			 *p == '_')) {
			*p = '_';
		}
	}

	i = 0;
	fname = NULL;
	do {
		char *fullname;

		g_free (fname);

		if (i > 0) {
			fname = g_strdup_printf ("%s-%d.directory", name, i);
		} else {
			fname = g_strdup_printf ("%s.directory", name);
		}

		fullname = g_build_filename
			(info->user_desktop_dir, fname, NULL);
		fd = open (fullname, O_CREAT | O_WRONLY | O_EXCL, 0600);
		g_free (fullname);
	} while (fd < 0);

	close (fd);

	folder->desktop_file = fname;
	info->dirty = TRUE;

	try_free_file_monitors_create_dirfile_unlocked (info, folder);
}

static gboolean
make_dirfile_private (VFolderInfo *info, Folder *folder)
{
	char *fname;
	char *desktop_file;
	GSList *li;
	char *uri;
	gboolean ret;

	if (info->user_desktop_dir == NULL)
		return FALSE;

	if ( ! ensure_dir (info->user_desktop_dir,
			   FALSE /* ignore_basename */))
		return FALSE;


	if (folder->desktop_file == NULL) {
		make_new_dirfile (info, folder);
		return TRUE;
	}

	/* FIXME: this is broken!  What if the desktop file exists
	 * in the local but there is a different (but with a same name)
	 * .directory in the system. */
	fname = g_build_filename (info->user_desktop_dir,
				  folder->desktop_file,
				  NULL);

	if (access (fname, F_OK) == 0) {
		g_free (fname);
		return TRUE;
	}

	desktop_file = get_directory_file (info, folder);

	if (desktop_file == NULL) {
		int fd = open (fname, O_CREAT | O_EXCL | O_WRONLY, 0600);
		g_free (fname);
		if (fd >= 0) {
			close (fd);
			return TRUE;
		}
		return FALSE;
	}

	for (li = ((Entry *)folder)->monitors; li != NULL; li = li->next) {
		FileMonitorHandle *h = li->data;
		if (h->is_directory_file) {
			if (h->handle != NULL)
				gnome_vfs_monitor_cancel (h->handle);
			h->handle = NULL;
		}
	}

	ret = TRUE;

	if ( ! copy_file (desktop_file, fname)) {
		ret = FALSE;
		g_free (fname);
		fname = desktop_file;
		desktop_file = NULL;
	}

	uri = gnome_vfs_get_uri_from_local_path (fname);

	for (li = ((Entry *)folder)->monitors; li != NULL; li = li->next) {
		FileMonitorHandle *h = li->data;

		if (h->is_directory_file) {
			gnome_vfs_monitor_add (&(h->handle),
					       uri,
					       GNOME_VFS_MONITOR_FILE,
					       file_monitor,
					       h);
		}
	}

	g_free (uri);

	g_free (desktop_file);
	g_free (fname);

	return ret;
}

static Folder *
resolve_folder (VFolderInfo *info,
		const char *path,
		gboolean ignore_basename,
		GnomeVFSResult *result,
		GnomeVFSContext *context)
{
	char **ppath;
	int i;
	Folder *folder = info->root;

	ppath = g_strsplit (path, "/", -1);

	if (ppath == NULL ||
	    ppath[0] == NULL) {
		g_strfreev (ppath);
		*result = GNOME_VFS_ERROR_INVALID_URI;
		return NULL;
	}

	for (i = 0; ppath [i] != NULL; i++) {
		const char *segment = ppath[i];

		if (*segment == '\0')
			continue;

		if (ignore_basename && ppath [i + 1] == NULL)
			break;
		else {
			folder = (Folder *) find_entry (folder->subfolders, 
							segment);
			if (folder == NULL)
				break;
		}
	}
	g_strfreev (ppath);

	if (gnome_vfs_context_check_cancellation (context)) {
		*result = GNOME_VFS_ERROR_CANCELLED;
		return NULL;
	}

	if (folder == NULL)
		*result = GNOME_VFS_ERROR_NOT_FOUND;

	return folder;
}

static Entry *
resolve_path (VFolderInfo *info,
	      const char *path,
	      const char *basename,
	      Folder **return_folder,
	      GnomeVFSResult *result,
	      GnomeVFSContext *context)
{
	Entry *entry;
	Folder *folder;

	if (strcmp (path, "/") == 0)
		return (Entry *)info->root;

	folder = resolve_folder (info, path,
				 TRUE /* ignore_basename */,
				 result, context);

	if (return_folder != NULL)
		*return_folder = folder;

	if (folder == NULL) {
		return NULL;
	}

	/* Make sure we have the entries here */
	ensure_folder_unlocked (info, folder,
				FALSE /* subfolders */,
				NULL /* except */,
				FALSE /* ignore_unallocated */);

	entry = find_entry (folder->entries, basename);

	if (entry == NULL)
		*result = GNOME_VFS_ERROR_NOT_FOUND;

	return entry;
}

static Entry *
get_entry_unlocked (VFolderURI *vuri,
		    Folder **parent,
		    gboolean *is_directory_file,
		    GnomeVFSResult *result,
		    GnomeVFSContext *context)
{
	VFolderInfo *info;
	Entry *entry;

	if (is_directory_file != NULL)
		*is_directory_file = FALSE;
	if (parent != NULL)
		*parent = NULL;

	info = get_vfolder_info_unlocked (vuri->scheme, result, context);
	if (info == NULL)
		return NULL;

	if (gnome_vfs_context_check_cancellation (context)) {
		*result = GNOME_VFS_ERROR_CANCELLED;
		return NULL;
	}

	if (vuri->is_all_scheme) {
		GSList *efile_list;

		if (vuri->file == NULL) {
			entry = resolve_path (info, 
					      vuri->path, 
					      vuri->file, 
					      parent, 
					      result, 
					      context);
			return entry;
		}

		efile_list = g_hash_table_lookup (info->entries_ht, vuri->file);

		if (efile_list == NULL) {
			*result = GNOME_VFS_ERROR_NOT_FOUND;
			return NULL;
		} else {
			return efile_list->data;
		}
	}

	if (vuri->file != NULL && 
	    check_ext (vuri->file, ".directory") == TRUE) {
		Folder *folder;

		folder = resolve_folder (info, vuri->path,
					 TRUE /* ignore_basename */,
					 result, context);
		if (folder == NULL) {
			return NULL;
		}

		if (is_directory_file != NULL)
			*is_directory_file = TRUE;

		if (parent != NULL)
			*parent = folder;

		return (Entry *)folder;
	} else {
		entry = resolve_path (info, vuri->path, vuri->file, parent, 
				      result, context);
		return entry;
	}
}

static Entry *
get_entry (VFolderURI *vuri,
	   Folder **parent,
	   gboolean *is_directory_file,
	   GnomeVFSResult *result,
	   GnomeVFSContext *context)
{
	Entry *entry;

	G_LOCK (vfolder_lock);
	entry = get_entry_unlocked (vuri, 
				    parent, 
				    is_directory_file, 
				    result, context);
	G_UNLOCK (vfolder_lock);

	return entry;
}

/* only works for files and only those that exist */
/* unlocked function */
static GnomeVFSURI *
desktop_uri_to_file_uri (VFolderInfo *info,
			 VFolderURI *desktop_vuri,
			 Entry **the_entry,
			 gboolean *the_is_directory_file,
			 Folder **the_folder,
			 gboolean privatize,
			 GnomeVFSResult *result,
			 GnomeVFSContext *context)
{
	gboolean is_directory_file;
	GnomeVFSURI *ret_uri;
	Folder *folder = NULL;
	Entry *entry;

	entry = get_entry_unlocked (desktop_vuri,
				    &folder,
				    &is_directory_file,
				    result,
				    context);
	if (entry == NULL)
		return NULL;

	if (gnome_vfs_context_check_cancellation (context)) {
		*result = GNOME_VFS_ERROR_CANCELLED;
		return NULL;
	}

	if (the_folder != NULL)
		*the_folder = folder;

	if (the_entry != NULL)
		*the_entry = entry;
	if (the_is_directory_file != NULL)
		*the_is_directory_file = is_directory_file;

	if (is_directory_file &&
	    entry->type == ENTRY_FOLDER) {
		char *desktop_file;

		folder = (Folder *)entry;

		if (the_folder != NULL)
			*the_folder = folder;

		/* we'll be doing something write like */
		if (folder->read_only &&
		    privatize) {
			*result = GNOME_VFS_ERROR_READ_ONLY;
			return NULL;
		}

		if (privatize) {
			char *fname;

			if (gnome_vfs_context_check_cancellation (context)) {
				*result = GNOME_VFS_ERROR_CANCELLED;
				return NULL;
			}

			if ( ! make_dirfile_private (info, folder)) {
				*result = GNOME_VFS_ERROR_GENERIC;
				return NULL;
			}
			fname = g_build_filename (g_get_home_dir (),
						  folder->desktop_file,
						  NULL);
			ret_uri = gnome_vfs_uri_new (fname);
			g_free (fname);
			return ret_uri;
		}

		desktop_file = get_directory_file_unlocked (info, folder);
		if (desktop_file != NULL) {
			char *s = gnome_vfs_get_uri_from_local_path
				(desktop_file);

			g_free (desktop_file);

			ret_uri = gnome_vfs_uri_new (s);
			g_free (s);

			return ret_uri;
		} else {
			*result = GNOME_VFS_ERROR_NOT_FOUND;
			return NULL;
		}
	} else if (entry->type == ENTRY_FILE) {
		EntryFile *efile = (EntryFile *)entry;
		char *s;

		/* we'll be doing something write like */
		if (folder != NULL &&
		    folder->read_only &&
		    privatize) {
			*result = GNOME_VFS_ERROR_READ_ONLY;
			return NULL;
		}

		if (gnome_vfs_context_check_cancellation (context)) {
			*result = GNOME_VFS_ERROR_CANCELLED;
			return NULL;
		}

		if (privatize &&
		    ! make_file_private (info, efile)) {
			*result = GNOME_VFS_ERROR_GENERIC;
			return NULL;
		}

		s = gnome_vfs_get_uri_from_local_path (efile->filename);
		ret_uri = gnome_vfs_uri_new (s);
		g_free (s);

		return ret_uri;
	} else {
		if (the_folder != NULL)
			*the_folder = (Folder *)entry;
		*result = GNOME_VFS_ERROR_IS_DIRECTORY;
		return NULL;
	}
}

static void
remove_file (Folder *folder, const char *basename)
{
	GSList *li;
	char *s;

	if (folder->includes_ht != NULL) {
		li = g_hash_table_lookup (folder->includes_ht, basename);
		if (li != NULL) {
			char *name = li->data;
			folder->includes = g_slist_delete_link
				(folder->includes, li);
			g_hash_table_remove (folder->includes_ht, basename);
			g_free (name);
		}
	}

	if (folder->excludes == NULL) {
		folder->excludes = g_hash_table_new_full
			(g_str_hash, g_str_equal,
			 (GDestroyNotify)g_free,
			 NULL);
	}
	s = g_strdup (basename);
	g_hash_table_replace (folder->excludes, s, s);
}

static void
add_file (Folder *folder, const char *basename)
{
	GSList *li = NULL;

	if (folder->includes_ht != NULL) {
		li = g_hash_table_lookup (folder->includes_ht, basename);
	}

	/* if not found */
	if (li == NULL) {
		char *str = g_strdup (basename);
		folder->includes =
			g_slist_prepend (folder->includes, str);
		if (folder->includes_ht == NULL) {
			folder->includes_ht =
				g_hash_table_new_full (g_str_hash,
						       g_str_equal,
						       NULL,
						       NULL);
		}
		g_hash_table_replace (folder->includes_ht,
				      str, folder->includes);
	}
	if (folder->excludes != NULL)
		g_hash_table_remove (folder->excludes, basename);
}

typedef struct _FileHandle FileHandle;
struct _FileHandle {
	VFolderInfo *info;
	GnomeVFSMethodHandle *handle;
	Entry *entry;
	gboolean write;
	gboolean is_directory_file;
};

static void
make_handle (GnomeVFSMethodHandle **method_handle,
	     GnomeVFSMethodHandle *file_handle,
	     VFolderInfo *info,
	     Entry *entry,
	     gboolean is_directory_file,
	     gboolean write)
{
	if (file_handle != NULL) {
		FileHandle *handle = g_new0 (FileHandle, 1);

		handle->info = info;
		handle->handle = file_handle;
		handle->entry = entry_ref (entry);
		handle->is_directory_file = is_directory_file;
		handle->write = write;

		*method_handle = (GnomeVFSMethodHandle *) handle;
	} else {
		*method_handle = NULL;
	}
}

static void
whack_handle (FileHandle *handle)
{
	entry_unref (handle->entry);
	handle->entry = NULL;

	handle->handle = NULL;
	handle->info = NULL;

	g_free (handle);
}

static GnomeVFSResult
do_open (GnomeVFSMethod *method,
	 GnomeVFSMethodHandle **method_handle,
	 GnomeVFSURI *uri,
	 GnomeVFSOpenMode mode,
	 GnomeVFSContext *context)
{
	GnomeVFSURI *file_uri;
	GnomeVFSResult result = GNOME_VFS_OK;
	VFolderInfo *info;
	Entry *entry;
	gboolean is_directory_file;
	GnomeVFSMethodHandle *file_handle = NULL;
	VFolderURI vuri;

	VFOLDER_URI_PARSE (uri, &vuri);

	/* These can't be very nice FILE names */
	if (vuri.file == NULL ||
	    vuri.ends_in_slash)
		return GNOME_VFS_ERROR_INVALID_URI;

	info = get_vfolder_info (vuri.scheme, &result, context);
	if (info == NULL)
		return result;

	if (mode & GNOME_VFS_OPEN_WRITE && 
	    (info->read_only || vuri.is_all_scheme))
		return GNOME_VFS_ERROR_READ_ONLY;

	G_LOCK (vfolder_lock);
	file_uri = desktop_uri_to_file_uri (info,
					    &vuri,
					    &entry,
					    &is_directory_file,
					    NULL /* the_folder */,
					    mode & GNOME_VFS_OPEN_WRITE,
					    &result,
					    context);

	if (file_uri == NULL) {
		G_UNLOCK (vfolder_lock);
		return result;
	}

	result = (* parent_method->open) (parent_method,
					  &file_handle,
					  file_uri,
					  mode,
					  context);

	if (result == GNOME_VFS_ERROR_CANCELLED) {
		G_UNLOCK (vfolder_lock);
		gnome_vfs_uri_unref (file_uri);
		return result;
	}

	make_handle (method_handle,
		     file_handle,
		     info,
		     entry,
		     is_directory_file,
		     mode & GNOME_VFS_OPEN_WRITE);

	gnome_vfs_uri_unref (file_uri);

	if (info->dirty) {
		vfolder_info_write_user (info);
	}

	G_UNLOCK (vfolder_lock);

	return result;
}

static void
remove_from_all_except (Folder *root,
			const char *name,
			Folder *except)
{
	GSList *li;

	if (root != except) {
		remove_file (root, name);
		if (root->up_to_date) {
			for (li = root->entries; li != NULL; li = li->next) {
				Entry *entry = li->data;
				if (strcmp (name, entry->name) == 0) {
					root->entries = 
						g_slist_delete_link
						   (root->entries, li);
					break;
				}
			}
		}
	}

	for (li = root->subfolders; li != NULL; li = li->next) {
		Folder *subfolder = li->data;

		remove_from_all_except (subfolder, name, except);
	}
}

static GnomeVFSResult
do_create (GnomeVFSMethod *method,
	   GnomeVFSMethodHandle **method_handle,
	   GnomeVFSURI *uri,
	   GnomeVFSOpenMode mode,
	   gboolean exclusive,
	   guint perm,
	   GnomeVFSContext *context)
{
	GnomeVFSResult result = GNOME_VFS_OK;
	GnomeVFSMethodHandle *file_handle;
	GnomeVFSURI *file_uri;
	VFolderURI vuri;
	VFolderInfo *info;
	Folder *parent;
	Entry *entry;
	EntryFile *efile;
	char *s;
	GSList *li;

	VFOLDER_URI_PARSE (uri, &vuri);

	/* These can't be very nice FILE names */
	if (vuri.file == NULL ||
	    vuri.ends_in_slash)
		return GNOME_VFS_ERROR_INVALID_URI;
	
	if ( ! check_ext (vuri.file, ".desktop") &&
	     ! strcmp (vuri.file, ".directory") == 0) {
		return GNOME_VFS_ERROR_INVALID_URI;
	}

	/* all scheme is read only */
	if (vuri.is_all_scheme)
		return GNOME_VFS_ERROR_READ_ONLY;

	info = get_vfolder_info (vuri.scheme, &result, context);
	if (info == NULL)
		return result;

	if (info->user_filename == NULL ||
	    info->read_only)
		return GNOME_VFS_ERROR_READ_ONLY;

	parent = resolve_folder (info, vuri.path,
				 TRUE /* ignore_basename */,
				 &result, context);
	if (parent == NULL)
		return result;

	if (parent->read_only)
		return GNOME_VFS_ERROR_READ_ONLY;

	if (strcmp (vuri.file, ".directory") == 0) {
		char *fname;

		G_LOCK (vfolder_lock);

		if (exclusive) {
			char *desktop_file;
			desktop_file = get_directory_file_unlocked (info, parent);
			if (desktop_file != NULL) {
				g_free (desktop_file);
				G_UNLOCK (vfolder_lock);
				return GNOME_VFS_ERROR_FILE_EXISTS;
			}
		}

		if ( ! make_dirfile_private (info, parent)) {
			G_UNLOCK (vfolder_lock);
			return GNOME_VFS_ERROR_GENERIC;
		}
		fname = g_build_filename (g_get_home_dir (),
					  parent->desktop_file,
					  NULL);
		s = gnome_vfs_get_uri_from_local_path (fname);
		file_uri = gnome_vfs_uri_new (s);
		g_free (fname);
		g_free (s);

		if (file_uri == NULL) {
			G_UNLOCK (vfolder_lock);
			return GNOME_VFS_ERROR_GENERIC;
		}

		result = (* parent_method->create) (parent_method,
						    &file_handle,
						    file_uri,
						    mode,
						    exclusive,
						    perm,
						    context);
		gnome_vfs_uri_unref (file_uri);

		make_handle (method_handle,
			     file_handle,
			     info,
			     (Entry *)parent,
			     TRUE /* is_directory_file */,
			     TRUE /* write */);

		if (info->dirty)
			vfolder_info_write_user (info);

		G_UNLOCK (vfolder_lock);

		return result;
	}

	ensure_folder (info, parent,
		       FALSE /* subfolders */,
		       NULL /* except */,
		       FALSE /* ignore_unallocated */);

	entry = find_entry (parent->entries, vuri.file);

	if (entry != NULL &&
	    entry->type == ENTRY_FOLDER)
		return GNOME_VFS_ERROR_IS_DIRECTORY;

	efile = (EntryFile *)entry;

	if (efile != NULL) {
		if (exclusive)
			return GNOME_VFS_ERROR_FILE_EXISTS;

		G_LOCK (vfolder_lock);
		if ( ! make_file_private (info, efile)) {
			G_UNLOCK (vfolder_lock);
			return GNOME_VFS_ERROR_GENERIC;
		}

		s = gnome_vfs_get_uri_from_local_path (efile->filename);
		file_uri = gnome_vfs_uri_new (s);
		g_free (s);

		if (file_uri == NULL) {
			G_UNLOCK (vfolder_lock);
			return GNOME_VFS_ERROR_GENERIC;
		}

		result = (* parent_method->create) (parent_method,
						    &file_handle,
						    file_uri,
						    mode,
						    exclusive,
						    perm,
						    context);
		gnome_vfs_uri_unref (file_uri);

		make_handle (method_handle,
			     file_handle,
			     info,
			     (Entry *)efile,
			     FALSE /* is_directory_file */,
			     TRUE /* write */);

		G_UNLOCK (vfolder_lock);

		return result;
	}

	G_LOCK (vfolder_lock);
	
	li = g_hash_table_lookup (info->entries_ht, vuri.file);

	if (exclusive && li != NULL) {
		G_UNLOCK (vfolder_lock);
		return GNOME_VFS_ERROR_FILE_EXISTS;
	}

	if (li == NULL) {
		efile = file_new (vuri.file);
		vfolder_info_insert_entry (info, efile);
		entry_unref ((Entry *)efile);
	} else {
		efile = li->data;
	}

	/* this will make a private name for this */
	if ( ! make_file_private (info, efile)) {
		G_UNLOCK (vfolder_lock);
		return GNOME_VFS_ERROR_GENERIC;
	}

	add_file (parent, vuri.file);
	parent->sorted = FALSE;

	if (parent->up_to_date)
		parent->entries = g_slist_prepend (parent->entries, efile);

	/* if we created a brand new name, then we exclude it
	 * from everywhere else to ensure overall sanity */
	if (li == NULL)
		remove_from_all_except (info->root, vuri.file, parent);

	s = gnome_vfs_get_uri_from_local_path (efile->filename);
	file_uri = gnome_vfs_uri_new (s);
	g_free (s);

	result = (* parent_method->create) (parent_method,
					    &file_handle,
					    file_uri,
					    mode,
					    exclusive,
					    perm,
					    context);
	gnome_vfs_uri_unref (file_uri);

	make_handle (method_handle,
		     file_handle,
		     info,
		     (Entry *)efile,
		     FALSE /* is_directory_file */,
		     TRUE /* write */);

	vfolder_info_write_user (info);

	G_UNLOCK (vfolder_lock);

	return result;
}

static GnomeVFSResult
do_close (GnomeVFSMethod *method,
	  GnomeVFSMethodHandle *method_handle,
	  GnomeVFSContext *context)
{
	GnomeVFSResult result;
	FileHandle *handle = (FileHandle *)method_handle;
	if (method_handle == (GnomeVFSMethodHandle *)method)
		return GNOME_VFS_OK;

	G_LOCK (vfolder_lock);
	
	result = (* parent_method->close) (parent_method,
					   handle->handle,
					   context);
	handle->handle = NULL;

	/* we reread the Categories keyword */
	if (handle->write &&
	    handle->entry != NULL &&
	    handle->entry->type == ENTRY_FILE) {
		EntryFile *efile = (EntryFile *)handle->entry;
		char *categories;
		readitem_entry (efile->filename,
				"Categories",
				&categories,
				NULL,
				NULL);
		set_keywords (efile, categories);
		g_free (categories);
		/* FIXME: what about OnlyShowIn */

		/* FIXME: check if the keywords changed, if not, do
		 * nothing */

		/* Perhaps a bit drastic */
		/* also this emits the CHANGED monitor signal */
		invalidate_folder_T (handle->info->root);

		/* the file changed monitor will happen by itself
		 * as the underlying file is changed */
	} else if (handle->write &&
		   handle->entry != NULL &&
		   handle->entry->type == ENTRY_FOLDER &&
		   handle->is_directory_file) {
		/* if we're monitoring this directory, emit the CHANGED
		 * monitor thing, it will also emit a changed on
		 * the file itself.  It is better to emit changed
		 * just in case. */
		emit_monitor ((Folder *)(handle->entry),
			      GNOME_VFS_MONITOR_EVENT_CHANGED);
	}

	whack_handle (handle);

	G_UNLOCK (vfolder_lock);

	return result;
}

static void
fill_buffer (gpointer buffer,
	     GnomeVFSFileSize num_bytes,
	     GnomeVFSFileSize *bytes_read)
{
	char *buf = buffer;
	GnomeVFSFileSize i;
	for (i = 0; i < num_bytes; i++) {
		if (rand () % 32 == 0 ||
		    i == num_bytes-1)
			buf[i] = '\n';
		else
			buf[i] = ((rand()>>4) % 94) + 32;
	}
	if (bytes_read != 0)
		*bytes_read = i;
}

static GnomeVFSResult
do_read (GnomeVFSMethod *method,
	 GnomeVFSMethodHandle *method_handle,
	 gpointer buffer,
	 GnomeVFSFileSize num_bytes,
	 GnomeVFSFileSize *bytes_read,
	 GnomeVFSContext *context)
{
	GnomeVFSResult result;
	FileHandle *handle = (FileHandle *)method_handle;

	if (method_handle == (GnomeVFSMethodHandle *)method) {
		if ((rand () >> 4) & 0x3) {
			fill_buffer (buffer, num_bytes, bytes_read);
			return GNOME_VFS_OK;
		} else {
			return GNOME_VFS_ERROR_EOF;
		}
	}
	
	result = (* parent_method->read) (parent_method,
					  handle->handle,
					  buffer, num_bytes,
					  bytes_read,
					  context);

	return result;
}

static GnomeVFSResult
do_write (GnomeVFSMethod *method,
	  GnomeVFSMethodHandle *method_handle,
	  gconstpointer buffer,
	  GnomeVFSFileSize num_bytes,
	  GnomeVFSFileSize *bytes_written,
	  GnomeVFSContext *context)
{
	GnomeVFSResult result;
	FileHandle *handle = (FileHandle *)method_handle;

	if (method_handle == (GnomeVFSMethodHandle *)method)
		return GNOME_VFS_OK;

	result = (* parent_method->write) (parent_method,
					   handle->handle,
					   buffer, num_bytes,
					   bytes_written,
					   context);

	return result;
}


static GnomeVFSResult
do_seek (GnomeVFSMethod *method,
	 GnomeVFSMethodHandle *method_handle,
	 GnomeVFSSeekPosition whence,
	 GnomeVFSFileOffset offset,
	 GnomeVFSContext *context)
{
	GnomeVFSResult result;
	FileHandle *handle = (FileHandle *)method_handle;

	if (method_handle == (GnomeVFSMethodHandle *)method)
		return GNOME_VFS_OK;
	
	result = (* parent_method->seek) (parent_method,
					  handle->handle,
					  whence, offset,
					  context);

	return result;
}

static GnomeVFSResult
do_tell (GnomeVFSMethod *method,
	 GnomeVFSMethodHandle *method_handle,
	 GnomeVFSFileOffset *offset_return)
{
	GnomeVFSResult result;
	FileHandle *handle = (FileHandle *)method_handle;
	
	result = (* parent_method->tell) (parent_method,
					  handle->handle,
					  offset_return);

	return result;
}


static GnomeVFSResult
do_truncate_handle (GnomeVFSMethod *method,
		    GnomeVFSMethodHandle *method_handle,
		    GnomeVFSFileSize where,
		    GnomeVFSContext *context)
{
	GnomeVFSResult result;
	FileHandle *handle = (FileHandle *)method_handle;

	if (method_handle == (GnomeVFSMethodHandle *)method)
		return GNOME_VFS_OK;
	
	result = (* parent_method->truncate_handle) (parent_method,
						     handle->handle,
						     where,
						     context);

	return result;
}

static GnomeVFSResult
do_truncate (GnomeVFSMethod *method,
	     GnomeVFSURI *uri,
	     GnomeVFSFileSize where,
	     GnomeVFSContext *context)
{
	GnomeVFSURI *file_uri;
	GnomeVFSResult result = GNOME_VFS_OK;
	VFolderInfo *info;
	Entry *entry;
	VFolderURI vuri;

	VFOLDER_URI_PARSE (uri, &vuri);

	/* These can't be very nice FILE names */
	if (vuri.file == NULL ||
	    vuri.ends_in_slash)
		return GNOME_VFS_ERROR_INVALID_URI;

	if (vuri.is_all_scheme)
		return GNOME_VFS_ERROR_READ_ONLY;

	info = get_vfolder_info (vuri.scheme, &result, context);
	if (info == NULL)
		return result;

	if (info->read_only)
		return GNOME_VFS_ERROR_READ_ONLY;

	G_LOCK (vfolder_lock);
	file_uri = desktop_uri_to_file_uri (info,
					    &vuri,
					    &entry,
					    NULL /* the_is_directory_file */,
					    NULL /* the_folder */,
					    TRUE /* privatize */,
					    &result,
					    context);
	G_UNLOCK (vfolder_lock);

	if (file_uri == NULL)
		return result;

	result = (* parent_method->truncate) (parent_method,
					      file_uri,
					      where,
					      context);

	gnome_vfs_uri_unref (file_uri);

	if (info->dirty) {
		G_LOCK (vfolder_lock);
		vfolder_info_write_user (info);
		G_UNLOCK (vfolder_lock);
	}

	if (entry->type == ENTRY_FILE) {
		EntryFile *efile = (EntryFile *)entry;

		G_LOCK (vfolder_lock);
		g_slist_free (efile->keywords);
		efile->keywords = NULL;
		G_UNLOCK (vfolder_lock);
	}

	/* Perhaps a bit drastic, but oh well */
	invalidate_folder (info->root);

	return result;
}

typedef struct _DirHandle DirHandle;
struct _DirHandle {
	VFolderInfo *info;
	Folder *folder;

	GnomeVFSFileInfoOptions options;

	/* List of Entries */
	GSList *list;
	GSList *current;
};

static GnomeVFSResult
do_open_directory (GnomeVFSMethod *method,
		   GnomeVFSMethodHandle **method_handle,
		   GnomeVFSURI *uri,
		   GnomeVFSFileInfoOptions options,
		   GnomeVFSContext *context)
{
	GnomeVFSResult result = GNOME_VFS_OK;
	VFolderURI vuri;
	DirHandle *dh;
	Folder *folder;
	VFolderInfo *info;
	char *desktop_file;

	VFOLDER_URI_PARSE (uri, &vuri);

	info = get_vfolder_info (vuri.scheme, &result, context);
	if (info == NULL)
		return result;

	/* In the all- scheme just list all filenames */
	if (vuri.is_all_scheme) {
		if (any_subdir (vuri.path))
			return GNOME_VFS_ERROR_NOT_FOUND;

		dh = g_new0 (DirHandle, 1);
		dh->info = info;
		dh->options = options;
		dh->folder = NULL;

		G_LOCK (vfolder_lock);
		dh->list = g_slist_copy (info->entries);
		g_slist_foreach (dh->list, (GFunc)entry_ref, NULL);
		dh->current = dh->list;
		G_UNLOCK (vfolder_lock);

		*method_handle = (GnomeVFSMethodHandle*) dh;
		return GNOME_VFS_OK;
	}

	folder = resolve_folder (info, vuri.path,
				 FALSE /* ignore_basename */,
				 &result, context);
	if (folder == NULL)
		return result;

	/* Make sure we have the entries and sorted here */
	ensure_folder_sort (info, folder);

	dh = g_new0 (DirHandle, 1);
	dh->info = info;
	dh->options = options;

	G_LOCK (vfolder_lock);
	dh->folder = (Folder *)entry_ref ((Entry *)folder);
	dh->list = g_slist_copy (folder->entries);
	g_slist_foreach (folder->entries, (GFunc)entry_ref, NULL);
	G_UNLOCK (vfolder_lock);

	desktop_file = get_directory_file (info, folder);
	if (desktop_file != NULL) {
		EntryFile *efile = file_new (".directory");
		dh->list = g_slist_prepend (dh->list, efile);
		g_free (desktop_file);
	}

	dh->current = dh->list;

	*method_handle = (GnomeVFSMethodHandle*) dh;

	return GNOME_VFS_OK;
}

static GnomeVFSResult
do_close_directory (GnomeVFSMethod *method,
		    GnomeVFSMethodHandle *method_handle,
		    GnomeVFSContext *context)
{
	DirHandle *dh;

	dh = (DirHandle*) method_handle;

	G_LOCK (vfolder_lock);

	g_slist_foreach (dh->list, (GFunc)entry_unref, NULL);
	g_slist_free (dh->list);
	dh->list = NULL;

	dh->current = NULL;

	if (dh->folder != NULL)
		entry_unref ((Entry *)dh->folder);
	dh->folder = NULL;

	dh->info = NULL;

	g_free (dh);

	G_UNLOCK (vfolder_lock);

	return GNOME_VFS_OK;
}

static GnomeVFSResult
do_read_directory (GnomeVFSMethod *method,
		   GnomeVFSMethodHandle *method_handle,
		   GnomeVFSFileInfo *file_info,
		   GnomeVFSContext *context)
{
	DirHandle *dh;
	Entry *entry;
	GnomeVFSFileInfoOptions options;

	dh = (DirHandle*) method_handle;

read_directory_again:

	if (dh->current == NULL) {
		return GNOME_VFS_ERROR_EOF;
	}

	entry = dh->current->data;
	dh->current = dh->current->next;

	options = dh->options;

	if (entry->type == ENTRY_FILE &&
	    ((EntryFile *)entry)->filename != NULL) {
		EntryFile *efile = (EntryFile *)entry;
		char *furi = gnome_vfs_get_uri_from_local_path (efile->filename);
		GnomeVFSURI *uri = gnome_vfs_uri_new (furi);

		/* we always get mime-type by forcing it below */
		if (options & GNOME_VFS_FILE_INFO_GET_MIME_TYPE)
			options &= ~GNOME_VFS_FILE_INFO_GET_MIME_TYPE;

		file_info->valid_fields = GNOME_VFS_FILE_INFO_FIELDS_NONE;

		/* Get the file info for this */
		(* parent_method->get_file_info) (parent_method,
						  uri,
						  file_info,
						  options,
						  context);

		/* we ignore errors from this since the file_info just
		 * won't be filled completely if there's an error, that's all */

		g_free (file_info->mime_type);
		file_info->mime_type = g_strdup ("application/x-gnome-app-info");
		file_info->valid_fields |= GNOME_VFS_FILE_INFO_FIELDS_MIME_TYPE;

		/* Now we wipe those fields we don't support */
		file_info->valid_fields &= ~(UNSUPPORTED_INFO_FIELDS);

		gnome_vfs_uri_unref (uri);
		g_free (furi);
	} else if (entry->type == ENTRY_FILE) {
		file_info->valid_fields = GNOME_VFS_FILE_INFO_FIELDS_NONE;

		file_info->name = g_strdup (entry->name);
		GNOME_VFS_FILE_INFO_SET_LOCAL (file_info, TRUE);

		file_info->type = GNOME_VFS_FILE_TYPE_REGULAR;
		file_info->valid_fields |= GNOME_VFS_FILE_INFO_FIELDS_TYPE;

		/* FIXME: Is this correct? isn't there an xdg mime type? */
		file_info->mime_type = g_strdup ("application/x-gnome-app-info");
		file_info->valid_fields |= GNOME_VFS_FILE_INFO_FIELDS_MIME_TYPE;

		/* FIXME: get some ctime/mtime */
	} else /* ENTRY_FOLDER */ {
		Folder *folder = (Folder *)entry;

		/* Skip empty folders if they have
		 * the flag set */
		if (folder->dont_show_if_empty) {
			/* Make sure we have the entries */
			ensure_folder (dh->info, folder,
				       FALSE /* subfolders */,
				       NULL /* except */,
				       FALSE /* ignore_unallocated */);

			if (folder->entries == NULL) {
				/* start this function over on the
				 * next item */
				goto read_directory_again;
			}
		}

		file_info->valid_fields = GNOME_VFS_FILE_INFO_FIELDS_NONE;

		file_info->name = g_strdup (entry->name);
		GNOME_VFS_FILE_INFO_SET_LOCAL (file_info, TRUE);

		file_info->type = GNOME_VFS_FILE_TYPE_DIRECTORY;
		file_info->valid_fields |= GNOME_VFS_FILE_INFO_FIELDS_TYPE;

		file_info->mime_type = g_strdup ("x-directory/vfolder-desktop");
		file_info->valid_fields |= GNOME_VFS_FILE_INFO_FIELDS_MIME_TYPE;

		file_info->ctime = dh->info->modification_time;
		file_info->mtime = dh->info->modification_time;
		file_info->valid_fields |= (GNOME_VFS_FILE_INFO_FIELDS_CTIME |
					    GNOME_VFS_FILE_INFO_FIELDS_MTIME);
	}

	return GNOME_VFS_OK;
}

static GnomeVFSResult
do_get_file_info (GnomeVFSMethod *method,
		  GnomeVFSURI *uri,
		  GnomeVFSFileInfo *file_info,
		  GnomeVFSFileInfoOptions options,
		  GnomeVFSContext *context)
{
	GnomeVFSURI *file_uri;
	GnomeVFSResult result = GNOME_VFS_OK;
	Folder *folder;
	VFolderInfo *info;
	VFolderURI vuri;

	VFOLDER_URI_PARSE (uri, &vuri);

	info = get_vfolder_info (vuri.scheme, &result, context);
	if (info == NULL)
		return result;

	G_LOCK (vfolder_lock);
	file_uri = desktop_uri_to_file_uri (info,
					    &vuri,
					    NULL /* the_entry */,
					    NULL /* the_is_directory_file */,
					    &folder,
					    FALSE /* privatize */,
					    &result,
					    context);
	G_UNLOCK (vfolder_lock);

	if (file_uri == NULL &&
	    result != GNOME_VFS_ERROR_IS_DIRECTORY)
		return result;

	if (file_uri != NULL) {
		/* we always get mime-type by forcing it below */
		if (options & GNOME_VFS_FILE_INFO_GET_MIME_TYPE)
			options &= ~GNOME_VFS_FILE_INFO_GET_MIME_TYPE;

		result = (* parent_method->get_file_info) (parent_method,
							   file_uri,
							   file_info,
							   options,
							   context);

		g_free (file_info->mime_type);
		file_info->mime_type = g_strdup ("application/x-gnome-app-info");
		file_info->valid_fields |= GNOME_VFS_FILE_INFO_FIELDS_MIME_TYPE;

		/* Now we wipe those fields we don't support */
		file_info->valid_fields &= ~(UNSUPPORTED_INFO_FIELDS);

		gnome_vfs_uri_unref (file_uri);

		return result;
	} else if (folder != NULL) {
		file_info->valid_fields = GNOME_VFS_FILE_INFO_FIELDS_NONE;

		file_info->name = g_strdup (folder->entry.name);
		GNOME_VFS_FILE_INFO_SET_LOCAL (file_info, TRUE);

		file_info->type = GNOME_VFS_FILE_TYPE_DIRECTORY;
		file_info->valid_fields |= GNOME_VFS_FILE_INFO_FIELDS_TYPE;

		file_info->mime_type = g_strdup ("x-directory/vfolder-desktop");
		file_info->valid_fields |= GNOME_VFS_FILE_INFO_FIELDS_MIME_TYPE;

		file_info->ctime = info->modification_time;
		file_info->mtime = info->modification_time;
		file_info->valid_fields |= (GNOME_VFS_FILE_INFO_FIELDS_CTIME |
					    GNOME_VFS_FILE_INFO_FIELDS_MTIME);

		return GNOME_VFS_OK;
	} else {
		return GNOME_VFS_ERROR_NOT_FOUND;
	}
}

static GnomeVFSResult
do_get_file_info_from_handle (GnomeVFSMethod *method,
			      GnomeVFSMethodHandle *method_handle,
			      GnomeVFSFileInfo *file_info,
			      GnomeVFSFileInfoOptions options,
			      GnomeVFSContext *context)
{
	GnomeVFSResult result;
	FileHandle *handle = (FileHandle *)method_handle;

	if (method_handle == (GnomeVFSMethodHandle *)method) {
		g_free (file_info->mime_type);
		file_info->mime_type = g_strdup ("text/plain");
		file_info->valid_fields |= GNOME_VFS_FILE_INFO_FIELDS_MIME_TYPE;
		return GNOME_VFS_OK;
	}

	/* we always get mime-type by forcing it below */
	if (options & GNOME_VFS_FILE_INFO_GET_MIME_TYPE)
		options &= ~GNOME_VFS_FILE_INFO_GET_MIME_TYPE;

	result = (* parent_method->get_file_info_from_handle) (parent_method,
							       handle->handle,
							       file_info,
							       options,
							       context);

	/* any file is of the .desktop type */
	g_free (file_info->mime_type);
	file_info->mime_type = g_strdup ("application/x-gnome-app-info");
	file_info->valid_fields |= GNOME_VFS_FILE_INFO_FIELDS_MIME_TYPE;

	/* Now we wipe those fields we don't support */
	file_info->valid_fields &= ~(UNSUPPORTED_INFO_FIELDS);

	return result;
}


static gboolean
do_is_local (GnomeVFSMethod *method,
	     const GnomeVFSURI *uri)
{
	return TRUE;
}

static void
try_free_folder_monitors_create_unlocked (VFolderInfo *info,
					  Folder *folder)
{
	GSList *li, *list;

	list = g_slist_copy (info->free_folder_monitors);

	for (li = list; li != NULL; li = li->next) {
		FileMonitorHandle *handle = li->data;
		Folder *f;
		VFolderURI vuri;
		GnomeVFSResult result;

		/* Evil! EVIL URI PARSING. this will eat a lot of stack if we
		 * have lots of free monitors */

		VFOLDER_URI_PARSE (handle->uri, &vuri);

		f = resolve_folder (info, 
					 vuri.path,
					 FALSE /* ignore_basename */,
					 &result,
					 NULL);

		if (folder != f)
			continue;

		info->free_folder_monitors =
			g_slist_remove (info->free_folder_monitors, handle);
		((Entry *)folder)->monitors =
			g_slist_prepend (((Entry *)folder)->monitors, handle);

		handle->exists = TRUE;
		gnome_vfs_monitor_callback ((GnomeVFSMethodHandle *)handle,
					    handle->uri, 
					    GNOME_VFS_MONITOR_EVENT_CREATED);
	}
}


static GnomeVFSResult
do_make_directory (GnomeVFSMethod *method,
		   GnomeVFSURI *uri,
		   guint perm,
		   GnomeVFSContext *context)
{
	GnomeVFSResult result = GNOME_VFS_OK;
	VFolderInfo *info;
	Folder *parent, *folder;
	VFolderURI vuri;

	VFOLDER_URI_PARSE (uri, &vuri);

	if (vuri.is_all_scheme)
		return GNOME_VFS_ERROR_READ_ONLY;

	info = get_vfolder_info (vuri.scheme, &result, context);
	if (info == NULL)
		return result;

	if (info->user_filename == NULL ||
	    info->read_only)
		return GNOME_VFS_ERROR_READ_ONLY;

	parent = resolve_folder (info, vuri.path,
				 TRUE /* ignore_basename */,
				 &result, context);
	if (parent == NULL)
		return result;
	else if (parent->read_only)
		return GNOME_VFS_ERROR_READ_ONLY;

	G_LOCK (vfolder_lock);

	folder = (Folder *)find_entry (parent->subfolders,
				       vuri.file);
	if (folder != NULL) {
		G_UNLOCK (vfolder_lock);
		return GNOME_VFS_ERROR_FILE_EXISTS;
	}

	folder = folder_new (vuri.file);
	parent->subfolders = g_slist_append (parent->subfolders, folder);
	folder->parent = parent;
	parent->up_to_date = FALSE;

	try_free_folder_monitors_create_unlocked (info, folder);

	/* parent changed */
	emit_monitor (parent, GNOME_VFS_MONITOR_EVENT_CHANGED);

	vfolder_info_write_user (info);
	G_UNLOCK (vfolder_lock);

	return GNOME_VFS_OK;
}

static GnomeVFSResult
do_remove_directory (GnomeVFSMethod *method,
		     GnomeVFSURI *uri,
		     GnomeVFSContext *context)
{
	GnomeVFSResult result = GNOME_VFS_OK;
	Folder *folder;
	VFolderInfo *info;
	VFolderURI vuri;

	VFOLDER_URI_PARSE (uri, &vuri);

	if (vuri.is_all_scheme)
		return GNOME_VFS_ERROR_READ_ONLY;

	info = get_vfolder_info (vuri.scheme, &result, context);
	if (info == NULL)
		return result;

	if (info->user_filename == NULL ||
	    info->read_only)
		return GNOME_VFS_ERROR_READ_ONLY;

	G_LOCK (vfolder_lock);

	folder = resolve_folder (info, vuri.path,
				 FALSE /* ignore_basename */,
				 &result, context);
	if (folder == NULL) {
		G_UNLOCK (vfolder_lock);
		return result;
	}

	if (folder->read_only ||
	    (folder->parent != NULL &&
	     folder->parent->read_only)) {
		G_UNLOCK (vfolder_lock);
		return GNOME_VFS_ERROR_READ_ONLY;
	}

	/* don't make removing directories easy */
	if (folder->desktop_file != NULL) {
		G_UNLOCK (vfolder_lock);
		return GNOME_VFS_ERROR_DIRECTORY_NOT_EMPTY;
	}

	/* Make sure we have the entries */
	ensure_folder_unlocked (info, folder,
				FALSE /* subfolders */,
				NULL /* except */,
				FALSE /* ignore_unallocated */);

	/* don't make removing directories easy */
	if (folder->entries != NULL) {
		G_UNLOCK (vfolder_lock);
		return GNOME_VFS_ERROR_DIRECTORY_NOT_EMPTY;
	}

	emit_and_delete_monitor (info, folder);

	if (folder->only_unallocated) {
		GSList *li = g_slist_find (info->unallocated_folders,
					   folder);
		if (li != NULL) {
			info->unallocated_folders = g_slist_delete_link
				(info->unallocated_folders, li);
			entry_unref ((Entry *)folder);
		}
	}

	if (folder == info->root) {
		info->root = NULL;
		entry_unref ((Entry *)folder);
		info->root = folder_new ("Root");
	} else {
		Folder *parent = folder->parent;

		g_assert (parent != NULL);

		parent->subfolders =
			g_slist_remove (parent->subfolders, folder);

		parent->up_to_date = FALSE;

		entry_unref ((Entry *)folder);

		/* parent changed */
		emit_monitor (parent, GNOME_VFS_MONITOR_EVENT_CHANGED);
	}

	vfolder_info_write_user (info);

	G_UNLOCK (vfolder_lock);

	return GNOME_VFS_OK;
}

/* a fairly evil function that does the whole move bit by copy and
 * remove */
static GnomeVFSResult
long_move (GnomeVFSMethod *method,
	   VFolderURI *old_vuri,
	   VFolderURI *new_vuri,
	   gboolean force_replace,
	   GnomeVFSContext *context)
{
	GnomeVFSResult result;
	GnomeVFSMethodHandle *handle;
	GnomeVFSURI *file_uri;
	const char *path;
	int fd;
	char buf[BUFSIZ];
	int bytes;
	VFolderInfo *info;

	info = get_vfolder_info (old_vuri->scheme, &result, context);
	if (info == NULL)
		return result;

	G_LOCK (vfolder_lock);
	file_uri = desktop_uri_to_file_uri (info,
					    old_vuri,
					    NULL /* the_entry */,
					    NULL /* the_is_directory_file */,
					    NULL /* the_folder */,
					    FALSE /* privatize */,
					    &result,
					    context);
	G_UNLOCK (vfolder_lock);

	if (file_uri == NULL)
		return result;

	path = gnome_vfs_uri_get_path (file_uri);
	if (path == NULL) {
		gnome_vfs_uri_unref (file_uri);
		return GNOME_VFS_ERROR_INVALID_URI;
	}

	fd = open (path, O_RDONLY);
	if (fd < 0) {
		gnome_vfs_uri_unref (file_uri);
		return gnome_vfs_result_from_errno ();
	}

	gnome_vfs_uri_unref (file_uri);

	info->inhibit_write++;

	result = method->create (method,
				 &handle,
				 new_vuri->uri,
				 GNOME_VFS_OPEN_WRITE,
				 force_replace /* exclusive */,
				 0600 /* perm */,
				 context);
	if (result != GNOME_VFS_OK) {
		close (fd);
		info->inhibit_write--;
		return result;
	}

	while ((bytes = read (fd, buf, BUFSIZ)) > 0) {
		GnomeVFSFileSize bytes_written = 0;
		result = method->write (method,
					handle,
					buf,
					bytes,
					&bytes_written,
					context);
		if (result == GNOME_VFS_OK &&
		    bytes_written != bytes)
			result = GNOME_VFS_ERROR_NO_SPACE;
		if (result != GNOME_VFS_OK) {
			close (fd);
			method->close (method, handle, context);
			/* FIXME: is this completely correct ? */
			method->unlink (method,
					new_vuri->uri,
					context);
			G_LOCK (vfolder_lock);
			info->inhibit_write--;
			vfolder_info_write_user (info);
			G_UNLOCK (vfolder_lock);
			return result;
		}
	}

	close (fd);

	result = method->close (method, handle, context);
	if (result != GNOME_VFS_OK) {
		G_LOCK (vfolder_lock);
		info->inhibit_write--;
		vfolder_info_write_user (info);
		G_UNLOCK (vfolder_lock);
		return result;
	}

	result = method->unlink (method, old_vuri->uri, context);

	G_LOCK (vfolder_lock);
	info->inhibit_write--;
	vfolder_info_write_user (info);
	G_UNLOCK (vfolder_lock);

	return result;
}

static GnomeVFSResult
move_directory_file (VFolderInfo *info,
		     Folder *old_folder,
		     Folder *new_folder)
{
	if (old_folder->desktop_file == NULL)
		return GNOME_VFS_ERROR_NOT_FOUND;

	/* "move" the desktop file */
	g_free (new_folder->desktop_file);
	new_folder->desktop_file = old_folder->desktop_file;
	old_folder->desktop_file = NULL;

	/* is this too drastic, it will requery the folder? */
	new_folder->up_to_date = FALSE;
	old_folder->up_to_date = FALSE;

	emit_monitor (new_folder, GNOME_VFS_MONITOR_EVENT_CHANGED);
	emit_monitor (old_folder, GNOME_VFS_MONITOR_EVENT_CHANGED);

	vfolder_info_write_user (info);

	return GNOME_VFS_OK;
}

static gboolean
is_sub (Folder *master, Folder *sub)
{
	GSList *li;

	for (li = master->subfolders; li != NULL; li = li->next) {
		Folder *subfolder = li->data;

		if (subfolder == sub ||
		    is_sub (subfolder, sub))
			return TRUE;
	}

	return FALSE;
}

static GnomeVFSResult
move_folder (VFolderInfo *info,
	     Folder *old_folder, Entry *old_entry,
	     Folder *new_folder, Entry *new_entry)
{
	Folder *source = (Folder *)old_entry;
	Folder *target;

	if (new_entry != NULL &&
	    new_entry->type != ENTRY_FOLDER)
		return GNOME_VFS_ERROR_NOT_A_DIRECTORY;
	
	if (new_entry != NULL) {
		target = (Folder *)new_entry;
	} else {
		target = new_folder;
	}

	/* move to where we are, yay, we're done :) */
	if (source->parent == target)
		return GNOME_VFS_OK;

	if (source == target ||
	    is_sub (source, target))
		return GNOME_VFS_ERROR_LOOP;

	/* this will never happen, but we're paranoid */
	if (source->parent == NULL)
		return GNOME_VFS_ERROR_LOOP;

	source->parent->subfolders = g_slist_remove (source->parent->subfolders,
						     source);
	target->subfolders = g_slist_append (target->subfolders,
					     source);

	source->parent = target;

	source->up_to_date = FALSE;
	target->up_to_date = FALSE;

	emit_monitor (source, GNOME_VFS_MONITOR_EVENT_CHANGED);
	emit_monitor (target, GNOME_VFS_MONITOR_EVENT_CHANGED);

	vfolder_info_write_user (info);

	return GNOME_VFS_OK;
}

static GnomeVFSResult
do_move (GnomeVFSMethod *method,
	 GnomeVFSURI *old_uri,
	 GnomeVFSURI *new_uri,
	 gboolean force_replace,
	 GnomeVFSContext *context)
{
	GnomeVFSResult result = GNOME_VFS_OK;
	VFolderInfo *info;
	Folder *old_folder, *new_folder;
	Entry *old_entry, *new_entry;
	gboolean old_is_directory_file, new_is_directory_file;
	VFolderURI old_vuri, new_vuri;

	VFOLDER_URI_PARSE (old_uri, &old_vuri);
	VFOLDER_URI_PARSE (new_uri, &new_vuri);

	if (old_vuri.file == NULL)
		return GNOME_VFS_ERROR_INVALID_URI;

	if (old_vuri.is_all_scheme)
		return GNOME_VFS_ERROR_READ_ONLY;

	if (strcmp (old_vuri.scheme, new_vuri.scheme) != 0)
		return GNOME_VFS_ERROR_NOT_SAME_FILE_SYSTEM;

	info = get_vfolder_info (old_vuri.scheme, &result, context);
	if (info == NULL)
		return result;

	if (info->read_only)
		return GNOME_VFS_ERROR_READ_ONLY;

	old_entry = get_entry (&old_vuri,
			       &old_folder,
			       &old_is_directory_file,
			       &result,
			       context);
	if (old_entry == NULL)
		return result;

	if (old_folder != NULL && old_folder->read_only)
		return GNOME_VFS_ERROR_READ_ONLY;

	new_entry = get_entry (&new_vuri,
			       &new_folder,
			       &new_is_directory_file,
			       &result,
			       context);
	if (new_entry == NULL && new_folder == NULL)
		return result;

	if (new_folder != NULL && new_folder->read_only)
		return GNOME_VFS_ERROR_READ_ONLY;

	if (new_is_directory_file != old_is_directory_file) {
		/* this will do another set of lookups
		 * perhaps this can be done in a nicer way,
		 * but is this the common case? I don't think so */
		return long_move (method, &old_vuri, &new_vuri,
				  force_replace, context);
	}
	
	if (new_is_directory_file) {
		g_assert (old_entry != NULL);
		g_assert (new_entry != NULL);
		G_LOCK (vfolder_lock);
		result = move_directory_file (info,
					      (Folder *)old_entry,
					      (Folder *)new_entry);
		G_UNLOCK (vfolder_lock);
		return result;
	}

	if (old_entry->type == ENTRY_FOLDER) {
		G_LOCK (vfolder_lock);
		result = move_folder (info,
				      old_folder, old_entry,
				      new_folder, new_entry);
		G_UNLOCK (vfolder_lock);
		return result;
	}

	/* move into self, just whack the old one */
	if (old_entry == new_entry) {
		/* same folder */
		if (new_folder == old_folder)
			return GNOME_VFS_OK;

		if ( ! force_replace)
			return GNOME_VFS_ERROR_FILE_EXISTS;

		G_LOCK (vfolder_lock);

		remove_file (old_folder, old_vuri.file);

		old_folder->entries = g_slist_remove (old_folder->entries, 
						      old_entry);
		entry_unref (old_entry);

		emit_monitor (old_folder, GNOME_VFS_MONITOR_EVENT_CHANGED);

		vfolder_info_write_user (info);

		G_UNLOCK (vfolder_lock);

		return GNOME_VFS_OK;
	}

	/* this is a simple move */
	if (new_entry == NULL ||
	    new_entry->type == ENTRY_FOLDER) {
		if (new_entry != NULL) {
			new_folder = (Folder *)new_entry;
		} else {
			/* a file and a totally different one */
			if (strcmp (new_vuri.file, old_entry->name) != 0) {
				/* yay, a long move */
				/* this will do another set of lookups
				 * perhaps this can be done in a nicer way,
				 * but is this the common case? I don't think
				 * so */
				return long_move (method, &old_vuri, &new_vuri,
						  force_replace, context);
			}
		}

		/* same folder */
		if (new_folder == old_folder)
			return GNOME_VFS_OK;

		G_LOCK (vfolder_lock);

		remove_file (old_folder, old_entry->name);
		add_file (new_folder, old_entry->name);

		new_folder->entries = g_slist_prepend (new_folder->entries, 
						       old_entry);
		entry_ref (old_entry);
		new_folder->sorted = FALSE;

		old_folder->entries = g_slist_remove (old_folder->entries, 
						      old_entry);
		entry_unref (old_entry);

		emit_monitor (new_folder, GNOME_VFS_MONITOR_EVENT_CHANGED);
		emit_monitor (old_folder, GNOME_VFS_MONITOR_EVENT_CHANGED);

		vfolder_info_write_user (info);

		G_UNLOCK (vfolder_lock);

		return GNOME_VFS_OK;
	}

	/* do we EVER get here? */

	/* this will do another set of lookups
	 * perhaps this can be done in a nicer way,
	 * but is this the common case? I don't think so */
	return long_move (method, &old_vuri, &new_vuri,
			  force_replace, context);
}

static GnomeVFSResult
do_unlink (GnomeVFSMethod *method,
	   GnomeVFSURI *uri,
	   GnomeVFSContext *context)
{
	GnomeVFSResult result = GNOME_VFS_OK;
	Entry *entry;
	Folder *the_folder;
	gboolean is_directory_file;
	VFolderInfo *info;
	VFolderURI vuri;
	GSList *li;

	VFOLDER_URI_PARSE (uri, &vuri);

	if (vuri.file == NULL)
		return GNOME_VFS_ERROR_INVALID_URI;
	
	if (vuri.is_all_scheme == TRUE)
		return GNOME_VFS_ERROR_READ_ONLY;

	info = get_vfolder_info (vuri.scheme, &result, context);
	if (info == NULL)
		return result;
	else if (info->read_only)
		return GNOME_VFS_ERROR_READ_ONLY;

	entry = get_entry (&vuri,
			   &the_folder,
			   &is_directory_file,
			   &result, context);
	if (entry == NULL) 
		return result;
	else if (the_folder != NULL &&
		 the_folder->read_only)
		return GNOME_VFS_ERROR_READ_ONLY;

	if (entry->type == ENTRY_FOLDER &&
	    is_directory_file) {
		Folder *folder = (Folder *)entry;

		if (folder->desktop_file == NULL)
			return GNOME_VFS_ERROR_NOT_FOUND;

		G_LOCK (vfolder_lock);

		g_free (folder->desktop_file);
		folder->desktop_file = NULL;

		emit_monitor (folder, GNOME_VFS_MONITOR_EVENT_CHANGED);

		vfolder_info_write_user (info);

		G_UNLOCK (vfolder_lock);

		return GNOME_VFS_OK;
	} else if (entry->type == ENTRY_FOLDER) {
		return GNOME_VFS_ERROR_IS_DIRECTORY;
	} else if (the_folder == NULL) {
		return GNOME_VFS_ERROR_NOT_FOUND;
	}

	G_LOCK (vfolder_lock);

	the_folder->entries = g_slist_remove (the_folder->entries,
					      entry);
	entry_unref (entry);

	remove_file (the_folder, vuri.file);

	emit_monitor (the_folder, GNOME_VFS_MONITOR_EVENT_CHANGED);

	/* evil, we must remove this from the unallocated folders as well
	 * so that it magically doesn't appear there.  But it's not so simple.
	 * We only want to remove it if it isn't in that folder already. */
	for (li = info->unallocated_folders;
	     li != NULL;
	     li = li->next) {
		Folder *folder = li->data;
		GSList *l;

		/* This is actually really evil since ensuring 
		 * an unallocated folder clears all other unallocated
		 * folders in it's wake.  I'm not sure it's worth
		 * optimizing however */
		ensure_folder_unlocked (info, folder,
					FALSE /* subfolders */,
					NULL /* except */,
					FALSE /* ignore_unallocated */);
		l = g_slist_find (folder->entries, entry);
		if (l == NULL) {
			remove_file (folder, vuri.file);
		}
	}

	emit_file_deleted_monitor (info, entry, the_folder);

	/* FIXME: if this was a user file and this is the only
	 * reference to it, unlink it. */

	vfolder_info_write_user (info);

	G_UNLOCK (vfolder_lock);

	return GNOME_VFS_OK;
}

static GnomeVFSResult
do_check_same_fs (GnomeVFSMethod *method,
		  GnomeVFSURI *source_uri,
		  GnomeVFSURI *target_uri,
		  gboolean *same_fs_return,
		  GnomeVFSContext *context)
{
	VFolderURI source_vuri, target_vuri;

	*same_fs_return = FALSE;

	VFOLDER_URI_PARSE (source_uri, &source_vuri);
	VFOLDER_URI_PARSE (target_uri, &target_vuri);

	if (strcmp (source_vuri.scheme, target_vuri.scheme) != 0 ||
	    source_vuri.is_all_scheme != target_vuri.is_all_scheme)
		*same_fs_return = FALSE;
	else
		*same_fs_return = TRUE;

	return GNOME_VFS_OK;
}

static GnomeVFSResult
do_set_file_info (GnomeVFSMethod *method,
		  GnomeVFSURI *uri,
		  const GnomeVFSFileInfo *info,
		  GnomeVFSSetFileInfoMask mask,
		  GnomeVFSContext *context)
{
	VFolderURI vuri;

	VFOLDER_URI_PARSE (uri, &vuri);

	if (vuri.file == NULL)
		return GNOME_VFS_ERROR_INVALID_URI;

	if (mask & GNOME_VFS_SET_FILE_INFO_NAME) {
		GnomeVFSResult result = GNOME_VFS_OK;
		char *dirname = gnome_vfs_uri_extract_dirname (uri);
		GnomeVFSURI *new_uri = gnome_vfs_uri_dup (uri);

		G_LOCK (vfolder_lock);
		g_free (new_uri->text);
		new_uri->text = g_build_path ("/", dirname, info->name, NULL);
		G_UNLOCK (vfolder_lock);

		result = do_move (method,
				  uri,
				  new_uri,
				  FALSE /* force_replace */,
				  context);

		g_free (dirname);
		gnome_vfs_uri_unref (new_uri);	
		return result;
	} else {
		/* We don't support setting any of this other permission,
		 * times and all that voodoo */
		return GNOME_VFS_ERROR_NOT_SUPPORTED;
	}
}

static GnomeVFSResult
do_monitor_add (GnomeVFSMethod *method,
		GnomeVFSMethodHandle **method_handle_return,
		GnomeVFSURI *uri,
		GnomeVFSMonitorType monitor_type)
{
	VFolderInfo *info;
	VFolderURI vuri;
	GnomeVFSResult result;
	Folder *folder;
	Entry *entry;
	GnomeVFSURI *file_uri;
	FileMonitorHandle *handle;
	gboolean is_directory_file;

	VFOLDER_URI_PARSE (uri, &vuri);

	info = get_vfolder_info (vuri.scheme, &result, NULL);
	if (info == NULL)
		return result;

	if (monitor_type == GNOME_VFS_MONITOR_DIRECTORY) {
		G_LOCK (vfolder_lock);

		folder = resolve_folder (info, 
					 vuri.path,
					 FALSE /* ignore_basename */,
					 &result,
					 NULL);

		handle = g_new0 (FileMonitorHandle, 1);
		handle->refcount = 2;
		handle->uri = gnome_vfs_uri_dup (uri);
		handle->dir_monitor = TRUE;
		handle->handle = NULL;
		handle->filename = NULL;

		if (folder == NULL) {
			handle->exists = FALSE;
			info->free_folder_monitors = 
				g_slist_prepend (info->free_folder_monitors,
						 handle);
		} else {
			handle->exists = TRUE;
			((Entry *)folder)->monitors = 
				g_slist_prepend (((Entry *)folder)->monitors,
						 handle);
		}

		info->folder_monitors = 
			g_slist_prepend (info->folder_monitors, handle);

		G_UNLOCK (vfolder_lock);

		*method_handle_return = (GnomeVFSMethodHandle *) handle;

		return GNOME_VFS_OK;
	} else {
		/* These can't be very nice FILE names */
		if (vuri.file == NULL ||
		    vuri.ends_in_slash)
			return GNOME_VFS_ERROR_INVALID_URI;

		G_LOCK (vfolder_lock);
		file_uri = desktop_uri_to_file_uri (info,
						    &vuri,
						    &entry,
						    &is_directory_file,
						    NULL /* the_folder */,
						    FALSE,
						    &result,
						    NULL);

		handle = g_new0 (FileMonitorHandle, 1);
		handle->refcount = 2;
		handle->uri = gnome_vfs_uri_dup (uri);
		handle->dir_monitor = FALSE;
		handle->handle = NULL;
		handle->filename = g_strdup (vuri.file);
		handle->is_directory_file = is_directory_file;

		info->file_monitors = 
			g_slist_prepend (info->file_monitors, handle);


		if (file_uri == NULL) {
			handle->exists = FALSE;
			info->free_file_monitors = 
				g_slist_prepend (info->free_file_monitors,
						 handle);
		} else {
			char *uri_string = gnome_vfs_uri_to_string (file_uri, 0);
			handle->exists = TRUE;
			gnome_vfs_monitor_add (&(handle->handle),
					       uri_string,
					       GNOME_VFS_MONITOR_FILE,
					       file_monitor,
					       handle);
			g_free (uri_string);
			
			entry->monitors = g_slist_prepend (entry->monitors,
							   handle);
			gnome_vfs_uri_unref (file_uri);
		}

		*method_handle_return = (GnomeVFSMethodHandle *) handle;

		G_UNLOCK (vfolder_lock);

		return GNOME_VFS_OK;
	}
}

static GnomeVFSResult
do_monitor_cancel (GnomeVFSMethod *method,
		   GnomeVFSMethodHandle *method_handle)
{
	FileMonitorHandle *handle;
	VFolderInfo *info;
	VFolderURI vuri;
	GnomeVFSResult result;
	Folder *folder;
	GSList *li;

	handle = (FileMonitorHandle *)method_handle;

	/* FIXME: is this correct? */
	if (method_handle == NULL)
		return GNOME_VFS_OK;

	VFOLDER_URI_PARSE (handle->uri, &vuri);

	info = get_vfolder_info (vuri.scheme, &result, NULL);
	if (info == NULL)
		return result;

	if (handle->dir_monitor) {
		G_LOCK (vfolder_lock);

		folder = resolve_folder (info, 
					 vuri.path,
					 FALSE /* ignore_basename */,
					 &result,
					 NULL);

		for (li = info->folder_monitors; li != NULL; li = li->next) {
			FileMonitorHandle *h = li->data;
			if (h != handle)
				continue;
			info->folder_monitors = g_slist_delete_link
				(info->folder_monitors, li);
			file_monitor_handle_unref_unlocked (h);
			break;
		}

		if (folder == NULL) {
			for (li = info->free_folder_monitors;
			     li != NULL;
			     li = li->next) {
				FileMonitorHandle *h = li->data;
				if (h != handle)
					continue;
				info->free_folder_monitors = g_slist_delete_link
					(info->free_folder_monitors, li);
				file_monitor_handle_unref_unlocked (h);
				break;
			}
		} else {
			for (li = ((Entry *)folder)->monitors;
			     li != NULL;
			     li = li->next) {
				FileMonitorHandle *h = li->data;
				if (h != handle)
					continue;
				((Entry *)folder)->monitors =
					g_slist_delete_link
					(((Entry *)folder)->monitors, li);
				file_monitor_handle_unref_unlocked (h);
				break;
			}
		}

		G_UNLOCK (vfolder_lock);

		return GNOME_VFS_OK;
	} else {
		G_LOCK (vfolder_lock);

		for (li = info->file_monitors; li != NULL; li = li->next) {
			FileMonitorHandle *h = li->data;
			if (h != handle)
				continue;
			info->file_monitors = g_slist_delete_link
				(info->file_monitors, li);
			file_monitor_handle_unref_unlocked (h);
			break;
		}

		for (li = info->free_file_monitors;
		     li != NULL;
		     li = li->next) {
			FileMonitorHandle *h = li->data;
			if (h != handle)
				continue;
			info->free_file_monitors = g_slist_delete_link
				(info->free_file_monitors, li);
			file_monitor_handle_unref_unlocked (h);
			break;
		}

		for (li = info->entries; li != NULL; li = li->next) {
			Entry *e = li->data;
			GSList *link = g_slist_find (e->monitors, handle);

			if (link == NULL)
				continue;
			link->data = NULL;
			e->monitors = g_slist_delete_link (e->monitors, link);

			file_monitor_handle_unref_unlocked (handle);
			break;
		}

		G_UNLOCK (vfolder_lock);

		/* Note: last unref of our monitor will cancel the
		 * underlying handle */

		return GNOME_VFS_OK;
	}
}


/* gnome-vfs bureaucracy */

static GnomeVFSMethod method = {
	sizeof (GnomeVFSMethod),
	do_open,
	do_create,
	do_close,
	do_read,
	do_write,
	do_seek,
	do_tell,
	do_truncate_handle,
	do_open_directory,
	do_close_directory,
	do_read_directory,
	do_get_file_info,
	do_get_file_info_from_handle,
	do_is_local,
	do_make_directory,
	do_remove_directory,
	do_move,
	do_unlink,
	do_check_same_fs,
	do_set_file_info,
	do_truncate,
	NULL /* find_directory */,
	NULL /* create_symbolic_link */,
	do_monitor_add,
	do_monitor_cancel
};

GnomeVFSMethod *
vfs_module_init (const char *method_name, 
		 const char *args)
{
	parent_method = gnome_vfs_method_get ("file");

	if (parent_method == NULL) {
		g_error ("Could not find 'file' method for gnome-vfs");
		return NULL;
	}

	return &method;
}

void
vfs_module_shutdown (GnomeVFSMethod *method)
{
	if (infos == NULL)
		return;

	g_hash_table_destroy (infos);
	infos = NULL;
}
