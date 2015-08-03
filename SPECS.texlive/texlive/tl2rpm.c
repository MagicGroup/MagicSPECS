/*
 * tl2rpm 0.0.1, TeX Live to RPM converter.
 * 
 * Copyright (C) 2009-2012 Jindrich Novy (jnovy@users.sf.net)
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#define _GNU_SOURCE

//#define PACKAGE_SOURCE
#define PACKAGE_DOCS
//#define MERGE_DOCS
//#define SRPMS
//#define SHORTEN_FILELISTS
//#define FEDORA_FONTS
#define UNPACK "xz"
#define REQ_POSTTRANS "Requires: "
#define REQ_POST_POSTUN "Requires(post,postun): "
#ifndef TL2010
#  define CTAN_URL "ftp://ftp.ctex.org/mirrors/CTAN/systems/texlive/tlnet/archive/"
#else
#  define CTAN_URL ""
#endif
#ifdef DEBUG
#  define REDIR "\n"
#else
#  define REDIR " > /dev/null 2>&1\n"
#endif

#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include "tl-oldpkgs.h"

char arch[] = "i386-linux";
char *m;
off_t size, pos;

typedef struct {
	char *token;
	int num;
	size_t s;
} match;

enum {CAT_COLLECTION, CAT_DOCUMENTATION, CAT_PACKAGE, CAT_SCHEME, CAT_TLCORE, CAT_CONTEXT};
match category[] = {
	{"Collection", CAT_COLLECTION},
	{"Documentation", CAT_DOCUMENTATION},
	{"Package", CAT_PACKAGE},
	{"Scheme", CAT_SCHEME},
	{"TLCore", CAT_TLCORE},
	{"ConTeXt", CAT_CONTEXT},
	{NULL, 0}
};

enum {
	LIC_GPL		= 1<<0,
	LIC_LPPL	= 1<<1,
	LIC_OTHER_FREE	= 1<<2,
	LIC_PD		= 1<<3,
	LIC_LGPL	= 1<<4,
	LIC_GFSL	= 1<<5,
	LIC_BSD		= 1<<6,
	LIC_GFL		= 1<<7,
	LIC_ARTISTIC2	= 1<<8,
	LIC_FDL		= 1<<9,
	LIC_COLLECTION	= 1<<10,
	LIC_OTHER	= 1<<11,
	LIC_OFL		= 1<<12,
	LIC_APACHE2	= 1<<13,
	LIC_NOINFO	= 1<<14,
	LIC_UNKNOWN	= 1<<15,
	LIC_KNUTH	= 1<<16,
	LIC_ARTISTIC	= 1<<17,
	LIC_NOSOURCE	= 1<<18,
	LIC_NOSELL	= 1<<19,
	LIC_NOCOMMERCIAL= 1<<20,
	LIC_GPL2	= 1<<21,
	LIC_GPL3	= 1<<22,
	LIC_LPPL12	= 1<<23,
	LIC_LPPL13	= 1<<24,
};
#define LIC_PROBLEMATIC (LIC_NOINFO | LIC_UNKNOWN | LIC_ARTISTIC | LIC_NOSOURCE | LIC_NOSELL | LIC_NOCOMMERCIAL | LIC_OTHER)
#define LIC_NOTALLOWED LIC_PROBLEMATIC

match license[] = {
	{"gpl3", LIC_GPL3},
	{"gpl2", LIC_GPL2},
	{"gpl", LIC_GPL},
	{"lppl1.3", LIC_LPPL13},
	{"lppl1.2", LIC_LPPL12},
	{"lppl1", LIC_LPPL},
	{"lppl", LIC_LPPL},
	{"other-free", LIC_OTHER_FREE},
	{"pd", LIC_PD},
	{"noinfo", LIC_NOINFO},
	{"lgpl2.1", LIC_LGPL},
	{"lgpl", LIC_LGPL},
	{"gfsl", LIC_GFSL},
	{"bsd", LIC_BSD},
	{"knuth", LIC_KNUTH},
	{"unknown", LIC_UNKNOWN},
	{"gfl", LIC_GFL},
	{"artistic2", LIC_ARTISTIC2},
	{"fdl", LIC_FDL},
	{"collection", LIC_COLLECTION},
	{"artistic", LIC_ARTISTIC},
	{"other-nonfree", LIC_OTHER},
	{"other", LIC_OTHER},
	{"ofl", LIC_OFL},
	{"apache2", LIC_APACHE2},
	{"nosource", LIC_NOSOURCE},
	{"nosell", LIC_NOSOURCE},
	{"nocommercial", LIC_NOCOMMERCIAL},
	{NULL, 0}
};

match spec_license[] = {
	{"GPL+", LIC_GPL},
	{"GPLv2+", LIC_GPL2},
	{"GPLv3+", LIC_GPL3},
	{"LPPL", LIC_LPPL},
	{"LPPL 1.2", LIC_LPPL12},
	{"LPPL 1.3", LIC_LPPL13},
	{"Freely redistributable without restriction", LIC_OTHER_FREE},
	{"Public Domain", LIC_PD},
	{"No Info", LIC_NOINFO},
	{"LGPLv2+", LIC_LGPL},
	{"GFSL", LIC_GFSL},
	{"BSD", LIC_BSD},
	{"Knuth", LIC_KNUTH},
	{"Unknown", LIC_UNKNOWN},
	{"LPPL", LIC_GFL},
	{"Artistic 2.0", LIC_ARTISTIC2},
	{"GFDL", LIC_FDL},
	{"Public Domain", LIC_COLLECTION},
	{"Artistic", LIC_ARTISTIC},
	{"Other", LIC_OTHER},
	{"OFL", LIC_OFL},
	{"ASL 2.0", LIC_APACHE2},
	{"No Source", LIC_NOSOURCE},
	{"No Sell", LIC_NOSOURCE},
	{"Non-commercial", LIC_NOCOMMERCIAL},
	{NULL, 0}
};

typedef struct pk {
	char *name;
	unsigned long namehash;
	int category;
	char *shortdesc;
	char **longdesc;
	int longdesc_lines;
	char **runf;
	int runfs;
	char **docf;
	int docfs;
	char **srcf;
	int srcfs;
	char **binf;
	int binfs;
	char *revision;
	char *catalogue_ctan;
	int catalogue_license;
	char *fedora_license;
	char *catalogue_date;
	char *catalogue_version;
	char **dep;
	struct pk **req;
	int reqs;
	char **file_req;
	int file_reqs;
	char **file_prov;
	int file_provs;
	char **exe;
	int exes;
	int reloc;
	int has_man;
	int has_info;
	int main_pkg_written;
	int any_pkg_written;
} package;

typedef struct {
	char *dir;
	unsigned long dirhash;
	char **pkg;
	unsigned long *pkghash;
	int *lic;
	int pkgs;
} dir_type;
dir_type *dir;
int dirs;

package *pkg;
int p = 0;

/* Packages to be ignored and not included */
char *pkg_blacklist[] = {
	"getafm",
	"psutils",
	"t1utils",
	"texworks",
	"xindy",	// dependency on clisp
	"asymptote",	// special build procedure
	"asymptote.i386-linux",
	"asymptote-by-example-zh-cn",
	"asymptote-faq-zh-cn",
	"asymptote-manual-zh-cn",
	"latex-tds",	// only source
	"biber",	// no sources
	"euro-ce",	// nonfree license
	"latexmk",	// packaged separately
	NULL,
};

char *rem[] = {		/* any file beginning with this will be removed */
	"texmf-dist/doc/info/kpathsea.info",
	"texmf-dist/scripts/context/stubs/source",
	"readme-txt.dir",
	"tlpkg/installer",
	"install-tl",
	NULL,
};

char *fedora_license[] = {
#include "texlive-fedora-licenses.h"
	NULL, NULL
};

char *get_line() {
	if ( pos<size ) {
		off_t rpos;
		while ( pos<size && m[pos] < ' ' ) pos++;
		if ( pos == size ) return NULL;
		rpos = pos;
		while ( pos<size && m[pos] != '\n' ) pos++;
		if ( pos == size ) return NULL;
		m[pos] = 0;
		return &m[rpos];
	} else {
		return NULL;
	}
}

int get_token( char *s, match *m ) {
	int i, found = -1;
//	char *r;

	for ( i=0; m[i].token; i++ ) {
		if ( !strncmp(s, m[i].token, m[i].s?m[i].s:(m[i].s=strlen(m[i].token))) ) {
			if ( found == -1 ) {
				found = i;
			} else {
				if ( m[found].s < m[i].s ) found = i;
			}
		}
	}

	if ( found != -1 ) {
		return m[found].num;
	}

//	r = strchr(s,'\n');
//	*r = '\0';
//	fprintf(stderr,"No match: '%s'\nin '", s);
//	*r = '\n';
//	for ( i=0; m[i].token; i++ ) {
//		fprintf(stderr, "%s ", m[i].token);
//	}
//	fprintf(stderr, "'\nin package %s\n", pkg[p-1].name);
//	exit(1);

	return 0;
}

char *put_token( int t, match *m ) {
	for ( ;m->token; m++ ) {
		if ( m->num == t ) return m->token;
	}

	return NULL;
}

unsigned long hash(char *str) {
	unsigned long hash = 5381;
	int c;

	while ((c = *str++))
		hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

	return hash;
}

enum {FT_NONE, FT_DOC, FT_RUN, FT_SRC, FT_BIN};

void skipspace(char **sp) {
	char *s = *sp;
	while (*s == ' ' || *s == '\t' || *s == '\n' || *s == '\r') s++;
	while (*s == '%') {
		while ( *s != '\n' ) s++;
		while (*s == ' ' || *s == '\t' || *s == '\n' || *s == '\r') s++;
	}
	*sp = s;
}

void parse() {
	char *l;
	int filetype = FT_NONE;

	while ( (l=get_line()) ) {
		if ( !*l ) continue;
		if ( *l == ' ' ) {
			char pkgname[0x100];
			unsigned long pkghash;
			char *end = strchr(++l, ' ');
			if ( end ) {
				*end = '\0';
			}
			if ( pkg[p-1].reloc ) {
				char *rel = strstr(l, "RELOC");
				char *new_l = NULL;
				asprintf(&new_l, "texmf-dist%s", rel+5);
				l = new_l;
			}
			if (!strncmp(l, "texmf-dist/doc/man/man", 22)) {  /* does package have any man pages? */
				pkg[p-1].has_man = 1;
				if ( l[strlen(l)-2] == '.' && l[strlen(l)-1] >= '0' && l[strlen(l)-1] <= '9' ) {
					pkg[p-1].runf = realloc(pkg[p-1].runf, (pkg[p-1].runfs+1)*sizeof(char *));
					pkg[p-1].runf[pkg[p-1].runfs] = l;
					pkg[p-1].runfs++;
					snprintf(pkgname, sizeof(pkgname), "%s", pkg[p-1].name);
					goto skip;
				}
				goto skip;
			}
			if (!strncmp(l, "texmf-dist/doc/info/", 20)) {  /* does package have any info pages? */
				pkg[p-1].has_info = 1;
				if ( !strncmp(&l[strlen(l)-5], ".info", 5) ) {
					pkg[p-1].runf = realloc(pkg[p-1].runf, (pkg[p-1].runfs+1)*sizeof(char *));
					pkg[p-1].runf[pkg[p-1].runfs] = l;
					pkg[p-1].runfs++;
					snprintf(pkgname, sizeof(pkgname), "%s", pkg[p-1].name);
					goto skip;
				}
				goto skip;
			}
			switch ( filetype ) {
				case FT_RUN:
#ifdef PACKAGE_DOCS
#ifdef MERGE_DOCS
				case FT_DOC:
#endif
#endif
					pkg[p-1].runf = realloc(pkg[p-1].runf, (pkg[p-1].runfs+1)*sizeof(char *));
					pkg[p-1].runf[pkg[p-1].runfs] = l;
					pkg[p-1].runfs++;
					snprintf(pkgname, sizeof(pkgname), "%s", pkg[p-1].name);
					break;
#ifdef PACKAGE_DOCS
#ifndef MERGE_DOCS
				case FT_DOC:
					pkg[p-1].docf = realloc(pkg[p-1].docf, (pkg[p-1].docfs+1)*sizeof(char *));
					pkg[p-1].docf[pkg[p-1].docfs] = l;
					pkg[p-1].docfs++;
					snprintf(pkgname, sizeof(pkgname), "%s-doc", pkg[p-1].name);
					break;
#endif
#else
				case FT_DOC:
					pkg[p-1].docf = realloc(pkg[p-1].docf, (pkg[p-1].docfs+1)*sizeof(char *));
					pkg[p-1].docf[pkg[p-1].docfs] = l;
					pkg[p-1].docfs++;
					snprintf(pkgname, sizeof(pkgname), "%s-doc", pkg[p-1].name);
					continue;
#endif
				case FT_SRC:
					pkg[p-1].srcf = realloc(pkg[p-1].srcf, (pkg[p-1].srcfs+1)*sizeof(char *));
					pkg[p-1].srcf[pkg[p-1].srcfs] = l;
					pkg[p-1].srcfs++;
					snprintf(pkgname, sizeof(pkgname), "%s-source", pkg[p-1].name);
#ifndef PACKAGE_SOURCE
					continue;
#endif
					break;
				case FT_BIN:
					pkg[p-1].binf = realloc(pkg[p-1].binf, (pkg[p-1].binfs+1)*sizeof(char *));
					pkg[p-1].binf[pkg[p-1].binfs] = l;
					pkg[p-1].binfs++;
					snprintf(pkgname, sizeof(pkgname), "%s", pkg[p-1].name);
					break;
				default:
					fprintf(stderr, "No filetype: %s\n", l);
					exit(1);
			}
skip:
			pkghash = hash(pkgname);
			end = strrchr(l, '/');
			if (!end) end = l;
			if ( end ) {
				int i;
				unsigned long h;
				char saved = *end;
				*end = '\0';
				h = hash(l);
				for ( i=0; i<dirs; i++ ) {
					if ( dir[i].dirhash == h && !strcmp(l, dir[i].dir) ) {
						int n;
						for ( n=0; n<dir[i].pkgs; n++ ) {
							if ( dir[i].pkghash[n] == pkghash && !strcmp(dir[i].pkg[n], pkgname) ) {
								goto exit;
							}
						}
						dir[i].pkg = realloc(dir[i].pkg, (dir[i].pkgs+1)*sizeof(char *));
						dir[i].pkghash = realloc(dir[i].pkghash, (dir[i].pkgs+1)*sizeof(unsigned long));
						dir[i].lic = realloc(dir[i].lic, (dir[i].pkgs+1)*sizeof(int));
						dir[i].pkg[dir[i].pkgs] = strdup(pkgname);
						dir[i].pkghash[dir[i].pkgs] = pkghash;
						dir[i].lic[dir[i].pkgs] = pkg[p-1].catalogue_license;
						dir[i].pkgs++;
						goto exit;
					}
				}
				dirs++;
				dir = realloc(dir, dirs*sizeof(dir_type));
				dir[dirs-1].dir = strdup(l);
				dir[dirs-1].dirhash = h;
				dir[dirs-1].pkgs = 1;
				dir[dirs-1].pkg = malloc(sizeof(char *));
				dir[dirs-1].pkghash = malloc(sizeof(unsigned long));
				dir[dirs-1].lic = malloc(sizeof(int));
				dir[dirs-1].pkg[0] = strdup(pkgname);
				dir[dirs-1].pkghash[0] = pkghash;
				dir[dirs-1].lic[0] = pkg[p-1].catalogue_license;
exit:
				*end = saved;
			}
			continue;
		}
next_name:
		if ( !strncmp(l,"name ", 5) ) {
			size_t sarch, sname;
			int i, blacklisted = 0;
			for (i=0; pkg_blacklist[i]; i++) {
				if ( !strncmp(l+5, pkg_blacklist[i], strlen(pkg_blacklist[i])) ) {
					blacklisted = 1;
					break;
				}
			}
			if (!blacklisted) {
				for (i=0; fedora_license[i]; i+=2) {
					if ( !strcmp(l+5, fedora_license[i]) && !fedora_license[i+1]) {
						blacklisted = 1;
						break;
					}
				}
			}
			if ( blacklisted ) {
				fprintf(stderr, "Blacklisted: %s\n", pkg_blacklist[i]);
				while ( (l=get_line()) ) {
					if ( !strncmp(l, "name ", 5) ) break;
				}
				if (!l) continue;
				goto next_name;
			}
			p++;
			pkg = realloc(pkg, p*sizeof(package));
			memset(&pkg[p-1], 0, sizeof(package));
			sarch = strlen(arch);
			sname = strlen(l+5);
			if ( sname > sarch && !strncmp(&(l+5)[sname-sarch], arch, sarch) ) {
				pkg[p-1].name = calloc(sname-sarch+5, 1);
				memcpy(pkg[p-1].name, l+5, sname-sarch);
				memcpy(&pkg[p-1].name[sname-sarch], "ARCH", 4);
			} else {
				pkg[p-1].name = l+5;
			}
			pkg[p-1].namehash = hash(pkg[p-1].name);
			filetype = FT_NONE;
			/* look for license first */
			{
				off_t opos = pos;
				while ( (l=get_line()) ) {
					m[pos] = '\n';
					if ( !strncmp(l, "name ", 5) ) break;
					if ( !strncmp(l,"catalogue-license ", 18) ) {
						pkg[p-1].catalogue_license = get_token(l+18, license);
						if ( pkg[p-1].catalogue_license & LIC_PROBLEMATIC ) printf("L: %s - %s\n", pkg[p-1].name, put_token(pkg[p-1].catalogue_license, spec_license));
						break;
					}
				}
				pos = opos;
			}
			continue;
		}
		if ( !strncmp(l,"category ", 9) ) {
			pkg[p-1].category = get_token(l+9, category);
			continue;
		}
		if ( !strncmp(l,"shortdesc ", 10) ) {
			size_t len;
			pkg[p-1].shortdesc = l+10;
			len = strlen(pkg[p-1].shortdesc);
			if ( pkg[p-1].shortdesc[len-1] == '.' ) pkg[p-1].shortdesc[len-1] = '\0';
			continue;
		}
		if ( !strncmp(l,"longdesc ", 9) ) {
			pkg[p-1].longdesc = realloc(pkg[p-1].longdesc, (pkg[p-1].longdesc_lines+1)*sizeof(char *));
			pkg[p-1].longdesc[pkg[p-1].longdesc_lines] = l+9;
			pkg[p-1].longdesc_lines++;
			continue;
		}
		if ( !strncmp(l,"docfiles ", 9) ) {
			filetype = FT_DOC;
			continue;
		}
		if ( !strncmp(l,"relocated 1", 11) ) {
			pkg[p-1].reloc = 1;
			continue;
		}
		if ( !strncmp(l,"runfiles ", 9) ) {
			filetype = FT_RUN;
			continue;
		}
		if ( !strncmp(l,"srcfiles ", 9) ) {
			filetype = FT_SRC;
			continue;
		}
		if ( !strncmp(l,"binfiles ", 9) ) {
			filetype = FT_BIN;
			continue;
		}
		if ( !strncmp(l,"depend ", 7) ) {
			pkg[p-1].dep = realloc(pkg[p-1].dep, (pkg[p-1].reqs+1)*sizeof(char *));
			pkg[p-1].req = realloc(pkg[p-1].req, (pkg[p-1].reqs+1)*sizeof(package *));
			pkg[p-1].dep[pkg[p-1].reqs] = l+7;
			pkg[p-1].req[pkg[p-1].reqs] = NULL;
			pkg[p-1].reqs++;
			continue;
		}
		if ( !strncmp(l,"execute ", 8) ) {
			pkg[p-1].exe = realloc(pkg[p-1].exe, (pkg[p-1].exes+1)*sizeof(char *));
			pkg[p-1].exe[pkg[p-1].exes] = l+8;
			pkg[p-1].exes++;
			continue;
		}
		if ( !strncmp(l,"catalogue-ctan ", 15) ) {
			pkg[p-1].catalogue_ctan = l+15;
			continue;
		}
		if ( !strncmp(l,"catalogue-license ", 18) ) {
			pkg[p-1].catalogue_license = get_token(l+18, license);
			{
				int n;
				for (n=0; fedora_license[n]; n+=2) {
					if (!strcmp(fedora_license[n], pkg[p-1].name)) {
						pkg[p-1].fedora_license = fedora_license[n+1];
						break;
					}
				}
			}
			continue;
		}
		if ( !strncmp(l,"catalogue-date ", 15) ) {
			pkg[p-1].catalogue_date = l+15;
			continue;
		}
		if ( !strncmp(l,"catalogue-version ", 18) ) {
			pkg[p-1].catalogue_version = l+18;
			/* substitute unallowed '/', '-', ' ', '~' characters with '_' */
			{
				char *v;
				for ( v=pkg[p-1].catalogue_version; *v; v++ ) {
					if ( *v == '/' || *v == '-' || *v == ' ' || *v == '~' || *v == ',' || *v == '(' || *v == ')') *v = '_';
				}
			}
			continue;
		}
		if ( !strncmp(l,"revision ", 9) ) {
			pkg[p-1].revision = l+9;
			continue;
		}
		if ( !strncmp(l,"containersize ", 14) ||
		     !strncmp(l,"containermd5 ", 13) ||
		     !strncmp(l,"doccontainersize ", 17) ||
		     !strncmp(l,"doccontainermd5 ", 16) ||
		     !strncmp(l,"srccontainersize ", 17) ||
		     !strncmp(l,"srccontainermd5 ", 16) ||
		     !strncmp(l,"catalogue ", 10)
		) {
			continue;
		}
		fprintf(stderr, "unknown token: '%s'\n", l);
	}
}

package **inst;
int installed, srcno=100, mainsrcno = 7000, mainpkg;
FILE *fpack, *ffile, *funpack, *fsrc, *fremove, *ffont;

char *cnf_files[] = {
	"texmf-dist/web2c/fmtutil.cnf",
	"texmf-dist/web2c/updmap.cfg",
	"texmf-dist/web2c/texmf.cnf",
	"texmf-dist/web2c/context.cnf",
	"texmf-dist/web2c/mktex.cnf",
	"texmf-dist/dvips/config/config.ps",		/* rhbz#441171 */
	"texmf-dist/tex/generic/config/language.dat",	/* rhbz#929367 */
	NULL,
};

int main_written;
void append_filelist( char *pkg, char *pkgsuf, int files, char **filelist, char *pkglicense ) {
	char pkgname[0x100];
	unsigned long pkghash;
	int x, y, n, bin = 0;
	char *binpos;

	strncpy(pkgname, pkg, sizeof(pkgname));
	if ( pkgsuf && *pkgsuf ) {
		strcat(pkgname, "-");
		strcat(pkgname, pkgsuf);
	}

	pkghash = hash(pkgname);

	if ( (binpos=strstr(pkgname, ".ARCH")) ) {
		bin = 1;
		*binpos = '\0';
		strcat(binpos, "-bin");
	}
	if ( pkglicense && get_token(pkglicense, license) && !(get_token(pkglicense, license)&LIC_PROBLEMATIC) ) {
			fprintf(ffile, "%%files %s\n%%defattr(-,root,root)\n%%doc %s.txt\n", mainpkg?(!main_written?"":pkgsuf):pkgname, pkglicense);
	} else {
		fprintf(ffile, "%%files %s\n%%defattr(-,root,root)\n", mainpkg?(!main_written?"":pkgsuf):pkgname);
	}
	if ( bin ) {
		*binpos = '\0';
		strcat(binpos, ".ARCH");
	}

	for (y=0; y<dirs; y++) {
		for (x=0; x<dir[y].pkgs; x++) {
			if ( dir[y].pkghash[x] == pkghash && !strcmp(dir[y].pkg[x], pkgname) ) {
				size_t bin_index = 0;
				if ( bin ) bin_index = 5+strlen(arch);
				if ( dir[y].pkgs == 1 ) {
					if ( !bin ) {
#ifdef SHORTEN_FILELISTS
						int found = 0;
#endif
						for (n=0; n<dirs; n++) {
							if ( y==n ) continue;
							if ( !strncmp(dir[n].dir, dir[y].dir, strlen(dir[y].dir)) ) {
#ifdef SHORTEN_FILELISTS
								found = 1;
#endif
								break;
							}
						}
#ifdef SHORTEN_FILELISTS
						if ( !found ) {
							fprintf(ffile, "%%{_texdir}/%s/*\n", dir[y].dir);
							for (n=0; n<files; n++) {			/* stupid styles contain files like ".tex" which are not caught via "*" */
								char *name = strrchr(filelist[n], '/');
								if (name && name[1] == '.') {
									fprintf(ffile, "%%{_texdir}/%s\n", filelist[n]);
								}
							}
							continue;
						}
#endif
					}
				}
				for (n=0; n<files; n++) {
					char *end = strrchr(filelist[n], '/');
					if (!end) end = filelist[n];
					if (end) {
						char saved = *end;
						*end = '\0';
						if ( !strcmp(dir[y].dir, filelist[n]) ) {
							int i;
							*end = saved;
							if ( strstr(&filelist[n][bin_index], arch) ) continue; /* fool texlive.infra - don't install lzma/xz */
							if (strstr(&filelist[n][bin_index], "win32") || strstr(&filelist[n][bin_index], "mswin") ||
							    strstr(&filelist[n][bin_index], "Win32") || strstr(&filelist[n][bin_index], "tlmgr") ||
							    !strncmp(&filelist[n][bin_index], "texmf-dist/source/", 18) ||
							    strstr(&filelist[n][bin_index], ".swf")) {
								fprintf(fremove, "rm -f %%{buildroot}/%s/%s\n", bin?"%{_bindir}":"%{_texdir}", &filelist[n][bin_index]);
								printf("*** %s\n", &filelist[n][bin_index]);
								goto next;
							}
							for (i=0; rem[i]; i++) {
								if (!strncmp(&filelist[n][bin_index], rem[i], strlen(rem[i]))) {
									fprintf(fremove, "rm -f %%{buildroot}/%s/%s\n", bin?"%{_bindir}":"%{_texdir}", &filelist[n][bin_index]);
									printf("*** %s\n", &filelist[n][bin_index]);
									goto next;
								}
							}
							if (!strncmp(&filelist[n][bin_index], "texmf-dist/doc/man/man", 22)) {  /* relocate man pages to correct paths */
								size_t sz = strlen(&filelist[n][bin_index]);
								char *man = &filelist[n][bin_index];
								if (man[sz-1] >= '0' && man[sz-1] <= '9') {
									fprintf(ffile, "%%{_mandir}/%s*\n", &filelist[n][bin_index+19]);
								}
								goto next;
							}
							if (!strncmp(&filelist[n][bin_index], "texmf-dist/doc/info", 19)) {  /* relocate path for info files, ignore all other files such as 'dir' */
								if (!strncmp(&filelist[n][strlen(filelist[n])-5], ".info", 5)) {
									fprintf(ffile, "%%{_infodir}/%s*\n", &filelist[n][bin_index+20]);
								}
								goto next;
							}
							if (!strcmp(&filelist[n][bin_index], "texmf-dist/web2c/updmap.cfg")) {
								fprintf(fremove, "\n# disable all Maps/MixedMaps we add them by scriptlets\n");
								fprintf(fremove, "sed -i '/^M/d' %%{buildroot}%%{_texdir}/texmf-dist/web2c/updmap.cfg\n");
							} else
							if (!strcmp(&filelist[n][bin_index], "texmf-dist/web2c/fmtutil.cnf")) {
								fprintf(fremove, "\n# disable all formats\n");
								fprintf(fremove, "sed -i '/^[a-z].*$/s/^/\\#\\!\\ /' %%{buildroot}%%{_texdir}/texmf-dist/web2c/fmtutil.cnf\n");
							} else
							if (!strcmp(&filelist[n][bin_index], "texmf-dist/tex/generic/config/language.us")) {
								fprintf(fremove, "\n# disable all hyphenations\n");
								fprintf(fremove, "cp -f %%{buildroot}%%{_texdir}/texmf-dist/tex/generic/config/language.us %%{buildroot}%%{_texdir}/texmf-dist/tex/generic/config/language.dat\n");
							} else
							if (!strcmp(&filelist[n][bin_index], "texmf-dist/tex/generic/config/language.us.def")) {
								fprintf(fremove, "\n# disable all hyphenations\n");
								fprintf(fremove, "cp -f %%{buildroot}%%{_texdir}/texmf-dist/tex/generic/config/language.us.def %%{buildroot}%%{_texdir}/texmf-dist/tex/generic/config/language.def\n");
							}
							{			/* add %config(noreplace) for config files */
								int i;

								for ( i=0; cnf_files[i]; i++ ) {
									if ( !strcmp(&filelist[n][bin_index], cnf_files[i]) ) {
										fprintf(ffile, "%%config(noreplace) ");
										break;
									}
								}
							}
							fprintf(ffile, "%s/%s\n", bin?"%{_bindir}":"%{_texdir}", &filelist[n][bin_index]);
						}
next:
						*end = saved;
					}
				}
			}
		}
	}
	fprintf(ffile, "\n");
}

static void provide_file(package *p, char *suf) {
	int n;
	for (n=0; n<p->runfs; n++) {
		if ( !strncmp(&p->runf[n][strlen(p->runf[n])-strlen(suf)], suf, strlen(suf)) ) {
			fprintf(fpack, "Provides: tex(%s) = %%{tl_version}\n", strrchr(p->runf[n], '/')+1);
		   }
	}
}

static void fill_provide_file(package *p, char *suf) {
	int n;
	for (n=0; n<p->runfs; n++) {
		if ( !strncmp(&p->runf[n][strlen(p->runf[n])-strlen(suf)], suf, strlen(suf)) ) {
			fprintf(fpack, "Provides: tex(%s) = %%{tl_version}\n", strrchr(p->runf[n], '/')+1);
		   }
	}
}

static void fill_file_reqprov() {
	int i, j, n, k;
	char ss[0x100];
	char *se;
	char *sufs[] = { ".tfm", ".ttf", ".ttc", ".pfa", ".pfb", ".pcf",
			 ".otf", ".tex", ".cnf", ".cfg", ".def", ".dat",
			 ".ldf", ".fd", ".enc", ".map", ".vf", ".vpl",
			 ".clo", ".bug", ".bg2", ".cbx", ".bbx", ".cls",
			 ".sty", NULL };

	for (i=0; i<p; i++) {
		for (n=0; n<pkg[i].runfs; n++) {
			for (k=0; sufs[k]; k++) {
				if (!strncmp(&pkg[i].runf[n][strlen(pkg[i].runf[n])-strlen(sufs[k])], sufs[k], strlen(sufs[k]))) {
					pkg[i].file_prov = realloc(pkg[i].file_prov, (pkg[i].file_provs+1)*sizeof(char *));
					pkg[i].file_prov[pkg[i].file_provs] = strdup(strrchr(pkg[i].runf[n], '/')+1);
					pkg[i].file_provs++;
				}
			}

			if ( !strncmp(&pkg[i].runf[n][strlen(pkg[i].runf[n])-4], ".sty", 4) ||
			     !strncmp(&pkg[i].runf[n][strlen(pkg[i].runf[n])-4], ".cls", 4) ||
			     !strncmp(&pkg[i].runf[n][strlen(pkg[i].runf[n])-4], ".ldf", 4) ||
			     !strncmp(&pkg[i].runf[n][strlen(pkg[i].runf[n])-4], ".bbx", 4) ||
			     !strncmp(&pkg[i].runf[n][strlen(pkg[i].runf[n])-4], ".cbx", 4) ||
			     !strncmp(&pkg[i].runf[n][strlen(pkg[i].runf[n])-4], ".bug", 4) ||
			     !strncmp(&pkg[i].runf[n][strlen(pkg[i].runf[n])-4], ".bg2", 4) ||
			     !strncmp(&pkg[i].runf[n][strlen(pkg[i].runf[n])-4], ".clo", 4)
			   ) {
				char fl[0x100] = "texlive.expanded/";
				FILE *f;
				char *m, *s;
				off_t size;

				strcat(fl, pkg[i].runf[n]);
				if ( !(f=fopen(fl,"rt")) ) {
					printf("file missing: %s\n", pkg[i].runf[n]);
					exit(1);
				}
				fseek(f, 0, SEEK_END);
				size = ftell(f);
				fseek(f, 0, SEEK_SET);
				m = malloc(size+1);
				fread(m, size, 1, f);
				fclose(f);
				m[size] = '\0';

				if ( !strncmp(&pkg[i].runf[n][strlen(pkg[i].runf[n])-4], ".bbx", 4) ) {
					for ( s=m; (s=strstr(s,"\\RequireBibliographyStyle{")); ) {
						s += 26;
						se = strchr(s, '}');
						*se = '\0';
						strcpy(ss, s);
						strcat(ss, ".bbx");
						for (k=0; k<pkg[i].file_reqs; k++) {
							if (!strcmp(pkg[i].file_req[k], ss)) goto next_bbx;
						}
						pkg[i].file_req = realloc(pkg[i].file_req, (pkg[i].file_reqs+1)*sizeof(char *));
						pkg[i].file_req[pkg[i].file_reqs] = strdup(ss);
						pkg[i].file_reqs++;
next_bbx:
						*se = '}';
					}
					goto skip;
				}

				if ( !strncmp(&pkg[i].runf[n][strlen(pkg[i].runf[n])-4], ".cbx", 4) ) {
					for ( s=m; (s=strstr(s,"\\RequireCitationStyle{")); ) {
						s += 22;
						se = strchr(s, '}');
						*se = '\0';
						strcpy(ss, s);
						strcat(ss, ".cbx");
						for (k=0; k<pkg[i].file_reqs; k++) {
							if (!strcmp(pkg[i].file_req[k], ss)) goto next_cbx;
						}
						pkg[i].file_req = realloc(pkg[i].file_req, (pkg[i].file_reqs+1)*sizeof(char *));
						pkg[i].file_req[pkg[i].file_reqs] = strdup(ss);
						pkg[i].file_reqs++;
next_cbx:
						*se = '}';
					}
					goto skip;
				}

				for ( s=strstr(m, "\\ProvidesPackage"); s; s=strstr(s, "\\ProvidesPackage") ) {
					char *os = s+16;
					char dep[0x100], *d;
					dep[0] = '\0';
					for (; s>=m; s--) {
						if (*s == '\n') break;
					}
					while (*s == ' ' || *s == '\t' || *s == '\n' || *s == '\r') s++;
					if ( *s == '%' ) goto nextprov;
					s = os;
					skipspace(&s);
					if ( *s == '[' ) {
						s++;
						while (*s != ']') if (*s == '%') skipspace(&s); else s++;
						s++;
						skipspace(&s);
					}
					if ( *s != '{' ) goto nextprov;
					s++;
					for ( d=dep, os=s; ; s++ ) {
						if ( *s == ' ' || *s == '\t' || *s == '\n' || *s == '\r' ) continue;
						if ( (*s >= 'a' && *s <= 'z') || (*s >= 'A' && *s <= 'Z') || (*s >= '0' && *s <= '9') || *s == '-' ) {
							*d = *s;
							d++;
							continue;
						}
						if ( *s == '%') {
							skipspace(&s);
							s--;
							continue;
						}
						if ( *s == ',' || *s == '}' ) {
							*d = '\0';
							strcpy(ss, dep);
							strcat(ss, ".sty");

							for (k=0; k<pkg[i].file_provs; k++) {
								if (!strcmp(ss, pkg[i].file_prov[k])) goto nextprov;
							}

							if ( *dep ) {
								pkg[i].file_prov = realloc(pkg[i].file_prov, (pkg[i].file_provs+1)*sizeof(char *));
								pkg[i].file_prov[pkg[i].file_provs] = strdup(ss);
								pkg[i].file_provs++;
							}

							if ( *s == '}' ) break;
							d = dep;
							continue;
						}
						goto nextprov;
					}
nextprov:
					s = os;
				}

				for ( s=strstr(m, "\\RequirePackage"); s; s=strstr(s, "\\RequirePackage") ) {
					char *os = s+15;
					char dep[0x100], *d;
					for (; s>=m; s--) {
						if (*s == '\n') break;
					}
					while (*s == ' ' || *s == '\t' || *s == '\n' || *s == '\r') s++;
					if ( *s == '%' ) goto nextreq;
					s = os;
					if (!strncmp(s, "WithOptions", 11)) s+=11;
					skipspace(&s);
					if ( *s == '[' ) {
						s++;
						while (*s != ']') if (*s == '%') skipspace(&s); else s++;
						s++;
						skipspace(&s);
					}
					if ( *s != '{' ) goto nextreq;
					s++;
					for ( d=dep, os=s; ; s++ ) {
					if ( *s == ' ' || *s == '\t' || *s == '\n' || *s == '\r' ) continue;
						if ( (*s >= 'a' && *s <= 'z') || (*s >= 'A' && *s <= 'Z') || (*s >= '0' && *s <= '9') || *s == '-' ) {
							*d = *s;
							d++;
							continue;
						}
						if ( *s == '%') {
							skipspace(&s);
							s--;
							continue;
						}
						if ( *s == ',' || *s == '}' ) {
							*d = '\0';
							strcpy(ss, dep);
							strcat(ss, ".sty");

							for (k=0; k<pkg[i].file_reqs; k++) {
								if (!strcmp(ss, pkg[i].file_req[k])) goto nextreq;
							}

							for (k=0; k<pkg[i].file_provs; k++) {
								if (!strcmp(ss, pkg[i].file_prov[k])) goto nextreq;
							}

							if ( *dep ) {
								pkg[i].file_req = realloc(pkg[i].file_req, (pkg[i].file_reqs+1)*sizeof(char *));
								pkg[i].file_req[pkg[i].file_reqs] = strdup(ss);
								pkg[i].file_reqs++;
							}

							if ( *s == '}' ) break;
							d = dep;
							continue;
						}
						goto nextreq;
					}
nextreq:
					s = os;
				}

				for ( s=strstr(m, "\\input"); s; s=strstr(s, "\\input") ) {
					char *os = s+6;
					char dep[0x100], *d;
					int has_space = 0;
					for (s--; s>=m; s--) {
						if (*s == '\n') break;
						if (*s != ' ' || *s != '\t') goto nextinput;
					}
					s++;
					while (*s == ' ' || *s == '\t') s++;
					if ( *s == '%' ) goto nextinput;
					s = os;
					if (*s == ' ' || *s == '\t') {
						has_space = 1;
						while (*s == ' ' || *s == '\t') s++;
					}
					if (*s == '{') {
						has_space = 1;
						s++;
						while (*s == ' ' || *s == '\t') s++;
					}
					if ( !has_space ) goto nextinput;
					for (d=dep; (*s >= 'a' && *s <= 'z') || (*s >= 'A' && *s <= 'Z') || (*s >= '0' && *s <= '9') || *s == '-' || *s == '.'; s++) {
						*d = *s;
						d++;
					}
					if ( d == dep ) goto nextinput;
					while (*s == ' ' || *s == '\t') s++;
					if ( *s == '}' || *s == '%' || *s == '\n' || *s == '\r') {
						int x;
						size_t sz;
						*d = '\0';
						if (!strchr(dep, '.')) strcat(dep, ".tex");
						sz = strlen(dep);
						for ( x=0; x<pkg[i].runfs; x++ ) {
							if ( !strcmp(&pkg[i].runf[x][strlen(pkg[i].runf[x])-sz], dep) && pkg[i].runf[x][strlen(pkg[i].runf[x])-sz-1] == '/' ) {
								goto nextinput;
							}
						}
						pkg[i].file_req = realloc(pkg[i].file_req, (pkg[i].file_reqs+1)*sizeof(char *));
						pkg[i].file_req[pkg[i].file_reqs] = strdup(dep);
						pkg[i].file_reqs++;
					}
nextinput:
					s = os;
				}
skip:
				free(m);
			}
		}
		/* Do not require self-provided files */
		for (k=0; k<pkg[i].file_reqs; k++) {
			for (n=0; n<pkg[i].file_provs; n++) {
				if (!strcmp(pkg[i].file_prov[n], pkg[i].file_req[k])) {
					memmove(&pkg[i].file_req[k], &pkg[i].file_req[k+1], (pkg[i].file_reqs-k-1)*sizeof(char*));
					pkg[i].file_reqs--;
					break;
				}
			}
		}
	}

	for (i=0; i<p; i++) {
		for (n=0; n<pkg[i].file_reqs; n++) {
			int found = 0;
			for (k=0; k<p; k++) {
				for (j=0; j<pkg[k].file_provs; j++) {
					if ( !strcmp(pkg[k].file_prov[j], pkg[i].file_req[n]) ) {
						found = 1;
						break;
					}
				}
				if (found) break;
			}
			if (!found) {
				fprintf(stderr, "Nothing provides: %s required by %s\n", pkg[i].file_req[n], pkg[i].name);
				memmove(&pkg[i].file_req[n], &pkg[i].file_req[n+1], (pkg[i].file_reqs-n-1)*sizeof(char*));
				pkg[i].file_reqs--;
				n--;
			}
		}
	}
}

static char *print_noarch_version( package *p ) {
	static char noarchver[0x100];

	if ( p->catalogue_version ) {
		snprintf(noarchver, sizeof(noarchver), "svn%s.%s", p->revision, p->catalogue_version );
	} else {
		snprintf(noarchver, sizeof(noarchver), "svn%s.0", p->revision);
	}

	return noarchver;
}

static char *skipspaces( char *s ) {
	while ( isblank(*s) ) s++;

	return s;
}

int level;
void solve(char *name) {
	unsigned long h;
	int i, found = 0, doc_expanded = 0;
#ifdef SRPMS
	FILE *ofpack = NULL, *offile = NULL, *ofunpack = NULL, *ofsrc = NULL, *ofremove = NULL, *offont = NULL;
#endif
	h = hash(name);

	if ( !fpack ) {
		fpack = fopen("_packages.spec", "wt");
	}
	if ( !ffile ) {
		ffile = fopen("_files.spec", "wt");
	}
	if ( !funpack ) {
		funpack = fopen("_unpack.spec", "wt");
	}
	if ( !fsrc ) {
		fsrc = fopen("_sources.spec", "wt");
	}
	if ( !fremove ) {
		fremove = fopen("_remove.spec", "wt");
	}
	if ( !ffont ) {
		ffont = fopen("_font.spec", "wt");
	}

	for (i=0; i<installed; i++) {
		if ( inst[i]->namehash == h && !strcmp(inst[i]->name, name) ) {
			return;
		}
	}

	for (i=0; i<level; i++) printf("\t");
	printf("%s\n", name);

	for (i=0; i<p; i++) {
		if ( pkg[i].namehash == h && !strcmp(pkg[i].name, name)) {
			int n, has_noarch_pkg = 0;
			if ( pkg[i].catalogue_license & LIC_NOTALLOWED ) {
				printf("Bad license: %s\n", pkg[i].name);
				continue;
			}
			if ( pkg[i].srcfs && !(pkg[i].runfs || pkg[i].docfs || pkg[i].exes || pkg[i].reqs) ) {
				printf("onlysrc: %s\n", name);
				continue;
			}
			level++;
			inst = realloc(inst, (installed+1)*sizeof(package*));
			inst[installed++] = &pkg[i];

			if ( pkg[i].exes ) {
				for (n=0; n<pkg[i].exes; n++) {
					int m;
					for (m=0; m<level; m++) printf("\t");
					printf("> %s\n", pkg[i].exe[n]);
				}
			}
			if ( pkg[i].binfs ) {
				char s[0x100], *pp;
				unsigned long hh;
				strcpy(s, name);
				pp = strstr(s, ".ARCH");
				*pp = 0;
				hh = hash(s);
				for (n=0; n<p; n++) {
					if ( pkg[n].namehash == hh && !strcmp(pkg[n].name, s)) {
						has_noarch_pkg = pkg[n].main_pkg_written;
						break;
					}
				}
				if ( has_noarch_pkg && pkg[n].catalogue_license & LIC_NOTALLOWED ) {
					printf("Bad license: %s\n", pkg[n].name);
					continue;
				}
				fprintf(fsrc, "Source%04d: "CTAN_URL"%s.%s.tar."UNPACK"\n", mainsrcno, s, arch);
				fprintf(funpack, UNPACK" -dc %%{SOURCE%d} | tar x -C %%{buildroot}\n", mainsrcno);
				mainsrcno++;
			}
			/* is it collection or scheme? then don't create a separate package for it and put it to main one */
			if ( !strncmp(name, "collection-", 11) || !strncmp(name, "scheme-", 7) ) {
				pkg[i].any_pkg_written = 1;
				fprintf(funpack, UNPACK" -dc %%{SOURCE%d} | tar x -C %%{buildroot}%%{_texdir}%s\n", mainsrcno, pkg[i].reloc?"/texmf-dist":"");
				fprintf(fpack, "%%package %s\n", name);
				if ( pkg[i].shortdesc ) {
					fprintf(fpack, "Summary: %s\n", pkg[i].shortdesc);
				} else {
					fprintf(fpack, "Summary: %s package\n", name);
				}
				fprintf(fpack, "Version: %s\n", print_noarch_version(&pkg[i]));
				fprintf(fpack, "Release: %%{tl_release}\n");
				fprintf(fpack, "BuildArch: noarch\n");
				fprintf(fsrc, "Source%04d: "CTAN_URL"%s.tar."UNPACK"\n", mainsrcno++, name);
				fprintf(fpack, "Requires: texlive-base\n");
				for (n=0; n<pkg[i].reqs; n++) {
					if ( pkg[i].req[n] ) {
						if ( pkg[i].req[n]->catalogue_license & LIC_NOTALLOWED ) {
							continue;
						}
						if ( pkg[i].req[n]->reqs || pkg[i].req[n]->runfs || pkg[i].req[n]->exes ) {
							if (strncmp(pkg[i].dep[n], "collection-", 11)) {
								fprintf(fpack, "Requires: tex-%s\n", pkg[i].dep[n]);
							} else {
								fprintf(fpack, "Requires: texlive-%s\n", pkg[i].dep[n]);
							}
							continue;
						}
#ifdef PACKAGE_DOCS
						if ( pkg[i].req[n]->docfs ) {
							fprintf(fpack, "Requires: texlive-%s-doc\n", pkg[i].dep[n]);
							continue;
						}
#endif
#ifdef PACKAGE_SOURCE
						if ( pkg[i].req[n]->srcfs ) {
							fprintf(fpack, "Requires: texlive-%s-source\n", pkg[i].dep[n]);
							continue;
						}
#endif
						if ( pkg[i].req[n]->binfs ) {
							size_t spost = strlen(pkg[i].dep[n])-5;
							if (strcmp(&pkg[i].dep[n][spost], ".ARCH")) {
								printf("Doesn't have .ARCH suffix!\n");
								exit(1);
							}
							pkg[i].dep[n][spost] = '\0';
							fprintf(fpack, "Requires: texlive-%s-bin\n", pkg[i].dep[n]);
							pkg[i].dep[n][spost] = '.';
							continue;
						}
					}
				}
				/* write virtual provides */
				if ( !strncmp(name, "collection-", 11) ) {
					if (!strcmp(name+11, "latexrecommended")) {
						fprintf(fpack, "Provides: tex(latex) = %%{tl_version}, texlive-latex = %%{tl_version}\n");
						fprintf(fpack, "Requires: texlive-collection-fontsrecommended\n");
					} else if (!strcmp(name+11, "latex")) {
						fprintf(fpack, "Provides: tex(latex-base) = %%{tl_version}\n");
					} else if (!strcmp(name+11, "basic")) {
						fprintf(fpack, "Provides: tex(tex) = %%{tl_version}, tex = %%{tl_version}\n");
						fprintf(fpack, "Requires: dvipdfmx, xdvik\n");
					} else if (!strcmp(name+11, "langcjk")) {
						fprintf(fpack, "Provides: tex(japanese) = %%{tl_version}\n");
						fprintf(fpack, "Provides: tex(east-asian) = %%{tl_version}\n");
						fprintf(fpack, "Obsoletes: texlive-east-asian < %%{tl_version}\n");
						fprintf(fpack, "Obsoletes: texlive-texmf-east-asian < %%{tl_version}\n");
					} else if (!strcmp(name+11, "documentation-base")) {
						fprintf(fpack, "Provides: texlive-texmf-doc = %%{tl_version}\n");
						fprintf(fpack, "Obsoletes: texlive-texmf-doc < %%{tl_version}\n");
					} else if (!strcmp(name+11, "fontsrecommended")) {
						fprintf(fpack, "Provides: tetex-fonts = 3.1-99\n");
						fprintf(fpack, "Obsoletes: tetex-fonts < 3.1-99\n");
						fprintf(fpack, "Provides: texlive-texmf-fonts = %%{tl_version}\n");
						fprintf(fpack, "Obsoletes: texlive-texmf-fonts < %%{tl_version}\n");
					} else if (!strcmp(name+11, "binextra")) {
						fprintf(fpack, "Obsoletes: texlive-utils < %%{tl_version}\n");
						fprintf(fpack, "Requires: dvipng\n");
					} else if (!strcmp(name+11, "xetex")) {
						fprintf(fpack, "Provides: tex(xetex) = %%{tl_version}\n");
						fprintf(fpack, "Obsoletes: texlive-texmf-xetex < %%{tl_version}\n");
					} else if (!strcmp(name+11, "fontutils")) {
						fprintf(fpack, "Requires: t1utils, psutils, lcdf-typetools\n");
					}

				}
				if ( !strcmp(name, "scheme-tetex") ) {
					fprintf(fpack, "Provides: tetex = 3.1-99\n");
					fprintf(fpack, "Obsoletes: tetex < 3.1-99\n");
					fprintf(fpack, "Obsoletes: texlive-dviutils < %%{tl_version}\n");
				}
				if ( !strcmp(name, "scheme-context") ) {
					fprintf(fpack, "Provides: tex(context) = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: texlive-texmf-context < %%{tl_version}\n");
				}
				/* description */
				fprintf(fpack, "\n%%description %s\n", name);
				for (n=0; n<pkg[i].longdesc_lines; n++) {
					fprintf(fpack, "%s\n", pkg[i].longdesc[n]);
				}
				if ( !pkg[i].longdesc_lines ) fprintf(fpack, "%s package\n", name);
				if ( pkg[i].catalogue_date ) fprintf(fpack, "\ndate: %s\n", pkg[i].catalogue_date);
				fprintf(fpack, "\n");
				fprintf(ffile, "%%files %s\n%%defattr(-,root,root)\n\n", name);
				goto slv;
			}
#ifdef SRPMS
			if ( !pkg[i].binfs ) {
				char path[0x100];
				char p[0x100];

				ofpack = fpack;
				offile = ffile;
				ofunpack = funpack;
				ofsrc = fsrc;
				ofremove = fremove;
				offont = ffont;

				snprintf(path, sizeof(path), "specs/tex-%s", name);
				mkdir(path, 0775);
				snprintf(p, sizeof(p), "%s/_packages.spec", path);
				fpack = fopen(p, "wt");
				snprintf(p, sizeof(p), "%s/_files.spec", path);
				ffile = fopen(p, "wt");
				snprintf(p, sizeof(p), "%s/_unpack.spec", path);
				funpack = fopen(p, "wt");
				snprintf(p, sizeof(p), "%s/_sources.spec", path);
				fsrc = fopen(p, "wt");
				snprintf(p, sizeof(p), "%s/_remove.spec", path);
				fremove = fopen(p, "wt");
				snprintf(p, sizeof(p), "%s/_font.spec", path);
				ffont = fopen(p, "wt");
				snprintf(p, sizeof(p), "%s/_main.spec", path);
				symlink("../../_main_subpackage.spec", p);

				srcno = 0;
			}
			if ( pkg[i].catalogue_license ) fprintf(funpack, "ln -s %%{_texdir}/licenses/%s.txt %s.txt\n", put_token(pkg[i].catalogue_license, license), put_token(pkg[i].catalogue_license, license));
#endif
			/* write main packages */
			if ( pkg[i].runfs || pkg[i].reqs || pkg[i].exes ) {
				pkg[i].main_pkg_written = pkg[i].any_pkg_written = 1;
				fprintf(funpack, UNPACK" -dc %%{SOURCE%d} | tar x -C %%{buildroot}%%{_texdir}%s\n", srcno, pkg[i].reloc?"/texmf-dist":"");
#ifndef SRPMS
				fprintf(fpack, "%%package %s\n", name);
				fprintf(fpack, "Provides: tex-%s = %%{tl_version}\n", name);
#else
				fprintf(fpack, "Name: tex-%s\n", name);
				fprintf(fpack, "Obsoletes: texlive-%s texlive-%s-doc texlive-%s-fedora-fonts\n", name, name, name);
#endif
				fprintf(fpack, "License: %s\n", pkg[i].fedora_license?pkg[i].fedora_license:(put_token(pkg[i].catalogue_license, spec_license)?put_token(pkg[i].catalogue_license, spec_license):"LPPL"));
				if ( pkg[i].shortdesc ) {
					fprintf(fpack, "Summary: %s\n", pkg[i].shortdesc);
				} else {
					fprintf(fpack, "Summary: %s package\n", name);
				}
				fprintf(fpack, "Version: %s\n", print_noarch_version(&pkg[i]));
				fprintf(fpack, "Release: %%{tl_noarch_release}\n");
				fprintf(fpack, "BuildArch: noarch\n");
				if (!strcmp(name,"pdfcrop")) {
					fprintf(fpack, "AutoReqProv: No\n");
				}
				fprintf(fsrc, "Source%04d: "CTAN_URL"%s.tar."UNPACK"\n", srcno++, name);
				if ( pkg[i].has_man || pkg[i].has_info ) {
					char nm[0x100];
					FILE *f;
					snprintf(nm, sizeof(nm), "texlive/archive/%s.doc.tar."UNPACK, name);
					f = fopen(nm, "rb");
					if ( f ) {
						fprintf(funpack, UNPACK" -dc %%{SOURCE%d} | tar x -C %%{buildroot}%%{_texdir}%s\n", srcno, pkg[i].reloc?"/texmf-dist":"");
						fprintf(fsrc, "Source%04d: "CTAN_URL"%s.doc.tar."UNPACK"\n", srcno++, name);
						doc_expanded = 1;
						fclose(f);
					}
				}

				if ( strncmp(name, "kpathsea", 8) ) {
					fprintf(fpack, "Requires: texlive-base\n");
				} else {
					fprintf(fpack, "Provides: kpathsea = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: kpathsea < %%{tl_version}\n");
					fprintf(funpack, "\n# add reference to support old texmf tree\n"
					"sed -i 's|TEXMFLOCAL = $SELFAUTOPARENT/../texmf-local|TEXMFLOCAL = $SELFAUTOPARENT/../texmf|g' %%{buildroot}%%{_texdir}/texmf-dist/web2c/texmf.cnf\n\n");
				}
				if ( !strncmp(name, "asana-math", 10) ) {
					fprintf(fpack, "Provides: texlive-Asana-Math = %%{tl_version}.1\n");
					fprintf(fpack, "Obsoletes: texlive-Asana-Math < %%{tl_version}.1\n");
					fprintf(fpack, "Obsoletes: texlive-Asana-Math-fedora-fonts < %%{tl_version}.1\n");
				}
				if ( !strncmp(name, "lineara", 10) ) {
					fprintf(fpack, "Provides: texlive-linearA = %%{tl_version}.1\n");
					fprintf(fpack, "Obsoletes: texlive-linearA < %%{tl_version}.1\n");
					fprintf(fpack, "Obsoletes: texlive-linearA-fedora-fonts < %%{tl_version}.1\n");
				}
				if ( !strncmp(name, "minted", 6) ) {
					fprintf(fpack, "Requires: python-pygments\n");
				}
/*				if ( !strncmp(name, "asymptote", 9) ) {
					fprintf(fpack, "Provides: asymptote = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: asymptote < %%{tl_version}\n");
				}*/
				if ( !strncmp(name, "jadetex", 7) ) {
					fprintf(fpack, "Provides: jadetex = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: jadetex < %%{tl_version}\n");
				}
				fprintf(fpack, REQ_POSTTRANS"texlive-kpathsea-bin, tex-kpathsea\n");
				if ( pkg[i].exes ) {
					fprintf(fpack, REQ_POSTTRANS"texlive-tetex-bin, tex-tetex\n");
					fprintf(fpack, REQ_POST_POSTUN"texlive-tetex-bin, tex-tetex, tex-hyphen-base, texlive-base, texlive-texlive.infra\n");
				}
				/* require coreutils if there is %post scriptlet present */
				if ( pkg[i].exes || pkg[i].runfs ) fprintf(fpack, REQ_POST_POSTUN"coreutils\n");
//				if ( pkg[i].runfs ) fprintf(fpack, REQ_POST_POSTUN"texlive-kpathsea-bin, tex-kpathsea\n");
				if ( pkg[i].has_info ) fprintf(fpack, REQ_POST_POSTUN"/sbin/install-info\n");
				for (n=0; n<pkg[i].reqs; n++) {
					if ( pkg[i].req[n] ) {
						if ( pkg[i].req[n]->catalogue_license & LIC_NOTALLOWED ) {
							continue;
						}
						if ( pkg[i].req[n]->reqs || pkg[i].req[n]->runfs || pkg[i].req[n]->exes ) {
							fprintf(fpack, "Requires: tex-%s\n", pkg[i].dep[n]);
							continue;
						}
#ifdef PACKAGE_DOCS
						if ( pkg[i].req[n]->docfs ) {
							fprintf(fpack, "Requires: tex-%s-doc\n", pkg[i].dep[n]);
							continue;
						}
#endif
#ifdef PACKAGE_SOURCE
						if ( pkg[i].req[n]->srcfs ) {
							fprintf(fpack, "Requires: tex-%s-source\n", pkg[i].dep[n]);
							continue;
						}
#endif
						if ( pkg[i].req[n]->binfs ) {
							size_t spost = strlen(pkg[i].dep[n])-5;
							if (strcmp(&pkg[i].dep[n][spost], ".ARCH")) {
								printf("Doesn't have .ARCH suffix!\n");
								exit(1);
							}
							pkg[i].dep[n][spost] = '\0';
							fprintf(fpack, "Requires: texlive-%s-bin\n", pkg[i].dep[n]);
							pkg[i].dep[n][spost] = '.';
							continue;
						}
					}
				}
				/* Ruby dependencies */
				for (n=0; n<pkg[i].runfs; n++) {
					if ( !strncmp(&pkg[i].runf[n][strlen(pkg[i].runf[n])-3], ".rb", 3)
					   ) {
						fprintf(fpack, "Requires: ruby\n");
						break;
					   }
				}
				/* Require needed files */
				for (n=0; n<pkg[i].file_reqs; n++) {
					fprintf(fpack, "Requires: tex(%s)\n", pkg[i].file_req[n]);
				}
				/* Provide all important files */
				for (n=0; n<pkg[i].file_provs; n++) {
					fprintf(fpack, "Provides: tex(%s) = %%{tl_version}\n", pkg[i].file_prov[n]);
				}
#ifdef FEDORA_FONTS
				/* check for fonts */
				for (n=0; n<pkg[i].runfs; n++) {
					size_t s = strlen(pkg[i].runf[n]);
					if (s > 4) {
						if (!strcmp(&pkg[i].runf[n][s-4], ".ttf") ||
						    !strcmp(&pkg[i].runf[n][s-4], ".ttc") ||
						    !strcmp(&pkg[i].runf[n][s-4], ".pfa") ||
						    !strcmp(&pkg[i].runf[n][s-4], ".pfb") ||
						    !strcmp(&pkg[i].runf[n][s-4], ".pcf") ||
						    !strcmp(&pkg[i].runf[n][s-4], ".otf")
						) {
							fprintf(fpack, "Requires: tex-%s-fedora-fonts\n", name);
							break;
						}
					}
				}
#endif
				/* write virtual provides */
				if ( !strcmp(name, "dvips") ) {
					fprintf(fpack, "Provides: tex(dvips) = %%{tl_version}, tetex-dvips = 3.1-99, texlive-texmf-dvips = %%{tl_version}, texlive-dvips = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: tetex-dvips < 3.1-99, texlive-texmf-dvips < %%{tl_version}\n");
					fprintf(fpack, "Requires: texlive-latex-fonts\n");
				}
				if ( !strcmp(name, "tex4ht") ) {
					fprintf(fpack, "Provides: tetex-tex4ht = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: tetex-tex4ht < %%{tl_version}\n");
				}
				if ( !strcmp(name, "latex") ) {
					fprintf(fpack, "Provides: tetex-latex = 3.1-99, texlive-texmf-latex = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: tetex-latex < 3.1-99, texlive-texmf-latex < %%{tl_version}\n");
				}
				if ( !strcmp(name, "IEEEtran") ) {
					fprintf(fpack, "Provides: tetex-IEEEtran = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: tetex-IEEEtran < %%{tl_version}\n");
				}
				if ( !strcmp(name, "bytefield") ) {
					fprintf(fpack, "Provides: tetex-bytefield = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: tetex-bytefield < %%{tl_version}\n");
				}
				if ( !strcmp(name, "elsevier") ) {
					fprintf(fpack, "Provides: tetex-elsevier = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: tetex-elsevier < %%{tl_version}\n");
				}
				if ( !strcmp(name, "perltex") ) {
					fprintf(fpack, "Provides: tetex-perltex = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: tetex-perltex < %%{tl_version}\n");
				}
				if ( !strcmp(name, "prosper") ) {
					fprintf(fpack, "Provides: tetex-prosper = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: tetex-prosper < %%{tl_version}\n");
				}
				if ( !strcmp(name, "texdoc") ) {
					fprintf(fpack, "Provides: texlive-doc = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: texlive-doc < %%{tl_version}\n");
				}
				if ( !strcmp(name, "pdfjam") ) {
					fprintf(fpack, "Provides: pdfjam = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: pdfjam < %%{tl_version}\n");
				}
				if ( !strcmp(name, "ptex") ) {
					fprintf(fpack, "Provides: mendexk = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: mendexk < %%{tl_version}\n");
				}
				if ( !strcmp(name, "japanese") ) {
					fprintf(fpack, "Provides: texlive-east-asian = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: texlive-east-asian < %%{tl_version}\n");
				}
				if ( !strcmp(name, "preview") ) {
					fprintf(fpack, "Provides: tex-preview = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: tex-preview < %%{tl_version}\n");
				}
/*				if ( !strcmp(name, "latexmk") ) {	// rhbz#868996
					fprintf(fpack, "Provides: latexmk = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: latexmk < %%{tl_version}\n");
				}*/
				if ( !strcmp(name, "chktex") ) {	/* rhbz#864211 */
					fprintf(fpack, "Provides: chktex = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: chktex < %%{tl_version}\n");
				}
				if ( !strcmp(name, "metauml") ) {	/* rhbz#573863 */
					fprintf(fpack, "Provides: metapost-metauml = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: metapost-metauml < %%{tl_version}\n");
				}
				if ( !strcmp(name, "cm-lgc") ) {	/* rhbz#907728 */
					fprintf(fpack, "Obsoletes: tex-cm-lgc < %%{tl_version}\n");
				}
				if ( !strcmp(name, "simplecv") ) {	/* rhbz#907728 */
					fprintf(fpack, "Obsoletes: tex-simplecv < %%{tl_version}\n");
				}
				if ( !strcmp(name, "kerkis") ) {	/* rhbz#907728 */
					fprintf(fpack, "Obsoletes: tex-kerkis < %%{tl_version}\n");
				}
				if ( !strcmp(name, "detex") ) {		/* rhbz#913678 */
					fprintf(fpack, "Obsoletes: detex < %%{tl_version}\n");
				}
				if ( !strcmp(name, "latexdiff") ) {	/* rhbz#913678 */
					fprintf(fpack, "Obsoletes: latexdiff < %%{tl_version}\n");
				}
				if ( !strcmp(name, "pdfjam") ) {	/* rhbz#913678 */
					fprintf(fpack, "Obsoletes: pdfbook < %%{tl_version}1212\n");
				}
				if ( !strcmp(name, "musixtex-fnts") ) {
					fprintf(fpack, "Provides: ctan-musixtex-fonts = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: ctan-musixtex-fonts < %%{tl_version}\n");
				}
				if ( !strcmp(name, "musixtex-doc") ) {
					fprintf(fpack, "Provides: tex-musixtex-doc = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: tex-musixtex-doc < %%{tl_version}\n");
				}
				if ( !strcmp(name, "musixtex") ) {
					fprintf(fpack, "Provides: tex-musixtex = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: tex-musixtex < %%{tl_version}\n");
				}
				if ( !strcmp(name, "dvipdfmx") ) {	/* rhbz#968358 */
					fprintf(fpack, "Provides: texlive-dvipdfm = 3:%%{tl_version}\n");
					fprintf(fpack, "Obsoletes: texlive-dvipdfm < 3:%%{tl_version}\n");
				}
				/* description */
#ifndef SRPMS
				fprintf(fpack, "\n%%description %s\n", name);
#else
				fprintf(fpack, "\n%%description\n");
#endif
				for (n=0; n<pkg[i].longdesc_lines; n++) {
					fprintf(fpack, "%s\n", pkg[i].longdesc[n]);
				}
				if ( !pkg[i].longdesc_lines ) fprintf(fpack, "%s package\n", name);
				if ( pkg[i].catalogue_date ) fprintf(fpack, "\ndate: %s\n", pkg[i].catalogue_date);
				fprintf(fpack, "\n");
				/* preun/post/postun scriptlets */
				if ( pkg[i].has_info ) {
					int k;
#ifndef SRPMS
					fprintf(fpack, "%%preun %s\n", name);
#else
					fprintf(fpack, "%%preun\n");
#endif
					fprintf(fpack, "if [ \"$1\" == \"0\" ]; then\n");
					for (k=0; k<pkg[i].runfs; k++) {
						if (!strncmp(pkg[i].runf[k], "texmf-dist/doc/info/", 20)) {
							fprintf(fpack, "  /sbin/install-info --delete %%{_infodir}/%s %%{_infodir}/dir 2>/dev/null || :\n", &pkg[i].runf[k][20]);
						}
					}
					fprintf(fpack, "fi\n\n");
				}
				if ( pkg[i].exes ) {
					int run_updmap, run_fmtutil;
#ifndef SRPMS
					fprintf(fpack, "%%post %s\n", name);
#else
					fprintf(fpack, "%%post\n");
#endif
					fprintf(fpack, "mkdir -p /var/run/texlive\ntouch /var/run/texlive/run-texhash\n");
					if ( pkg[i].has_info ) {
						int k;

						for (k=0; k<pkg[i].runfs; k++) {
							if (!strncmp(pkg[i].runf[k], "texmf-dist/doc/info/", 20)) {
								fprintf(fpack, "/sbin/install-info %%{_infodir}/%s %%{_infodir}/dir 2>/dev/null\n", &pkg[i].runf[k][20]);
							}
						}
					}
					fprintf(fpack, "if [ $1 -gt 0 ] ; then\n");
					for (run_updmap=run_fmtutil=n=0; n<pkg[i].exes; n++) {
						if ( !strncmp(pkg[i].exe[n], "addLuaMap ", 9) ) {
							continue;
						}
						if ( !strncmp(pkg[i].exe[n], "addMap ", 7) ) {
							fprintf(fpack, "%%{_bindir}/updmap-sys --quiet --nomkmap --enable Map=%s"REDIR, skipspaces(&pkg[i].exe[n][7]));
							run_updmap = 1;
							continue;
						}
						if ( !strncmp(pkg[i].exe[n], "addMixedMap ", 12) ) {
							fprintf(fpack, "%%{_bindir}/updmap-sys --quiet --nomkmap --enable MixedMap=%s"REDIR, skipspaces(&pkg[i].exe[n][12]));
							run_updmap = 1;
							continue;
						}
						if ( !strncmp(pkg[i].exe[n], "addKanjiMap ", 12) ) {
							fprintf(fpack, "%%{_bindir}/updmap-sys --quiet --nomkmap --enable KanjiMap=%s"REDIR, skipspaces(&pkg[i].exe[n][12]));
							run_updmap = 1;
							continue;
						}
						if ( !strncmp(pkg[i].exe[n], "BuildFormat ", 12) ) {
							fprintf(fpack, "%%{_bindir}/fmtutil-sys --enablefmt %s"REDIR, &pkg[i].exe[n][12]);
							run_fmtutil = 1;
							continue;
						}
						if ( !strncmp(pkg[i].exe[n], "AddFormat ", 10) ) {
							char *name	= strstr(pkg[i].exe[n], "name="),
							     *engine	= strstr(pkg[i].exe[n], "engine="),
							     *patterns	= strstr(pkg[i].exe[n], "patterns="),
							     *options	= strstr(pkg[i].exe[n], "options=");
							char *opt, opt_char;

							if ( !name || !engine || !options ) {
								fprintf(stderr, "Invalid AddFormat entry in package %s: '%s' '%s' '%s' '%s'.\n", pkg[i].name, name, engine, patterns, options);
								exit(1);
							}
							name += 5;
							engine += 7;
							if ( patterns ) patterns += 9;
							options += 8;

							*strchr(name, ' ') = '\0';
							*strchr(engine, ' ') = '\0';
							if ( patterns && strchr(patterns, ' ') ) *strchr(patterns, ' ') = '\0';
							if ( *options == '"' ) {
								options++;
								opt = strchr(options, '"');
							} else {
								for (opt=options; *opt != ' ' && *opt != '\n'; opt++);
							}
							opt_char = *opt;
							*opt = '\0';

							fprintf(fpack, "sed -i 's/^\\#\\!\\ %s.*$/%s %s %s %s/' %%{_texdir}/texmf-dist/web2c/fmtutil.cnf\n", name, name, engine, patterns?patterns:"-", options);

							name[strlen(name)] = ' ';
							engine[strlen(engine)] = ' ';
							if ( patterns ) patterns[strlen(patterns)] = ' ';
							*opt = opt_char;

							run_fmtutil = 1;
							continue;
						}
						if ( !strncmp(pkg[i].exe[n], "AddHyphen ", 10) ) {
							char *name		= strstr(pkg[i].exe[n], "name="),
							     *synonyms		= strstr(pkg[i].exe[n], "synonyms="),
							     *lefthyphenmin	= strstr(pkg[i].exe[n], "lefthyphenmin="),
							     *righthyphenmin	= strstr(pkg[i].exe[n], "righthyphenmin="),
							     *file		= strstr(pkg[i].exe[n], "file=");
							int k;

							if ( !name || !lefthyphenmin || !righthyphenmin || !file ) {
								fprintf(stderr, "Invalid AddHyphen entry in package %s.\n", pkg[i].name);
								exit(1);
							}
							name += 5;
							if ( synonyms ) synonyms += 9;
							lefthyphenmin += 14;
							righthyphenmin += 15;
							file += 5;
							for (k=10; pkg[i].exe[n][k]; k++) if ( pkg[i].exe[n][k] == ' ' ) pkg[i].exe[n][k] = '\0';

							fprintf(fpack, "sed -i '/%s.*/d' %%{_texdir}/texmf-dist/tex/generic/config/language.dat\n", name);
							fprintf(fpack, "echo \"%s %s\" >> %%{_texdir}/texmf-dist/tex/generic/config/language.dat\n", name, file);
							if ( synonyms ) {
								char *syn = synonyms, *s;
								while ( (s=strchr(syn, ',')) ) {
									*s = '\0';
									fprintf(fpack, "sed -i '/=%s/d' %%{_texdir}/texmf-dist/tex/generic/config/language.dat\n", syn);
									fprintf(fpack, "echo \"=%s\" >> %%{_texdir}/texmf-dist/tex/generic/config/language.dat\n", syn);
									*s = ',';
									syn = s+1;
								}
								fprintf(fpack, "sed -i '/=%s/d' %%{_texdir}/texmf-dist/tex/generic/config/language.dat\n", syn);
								fprintf(fpack, "echo \"=%s\" >> %%{_texdir}/texmf-dist/tex/generic/config/language.dat\n", syn);
							}
							fprintf(fpack, "sed -i '/\\\\addlanguage{%s}.*/d' %%{_texdir}/texmf-dist/tex/generic/config/language.def\n", name);
							fprintf(fpack, "echo \"\\addlanguage{%s}{%s}{}{%s}{%s}\" >> %%{_texdir}/texmf-dist/tex/generic/config/language.def\n", name, file, lefthyphenmin, righthyphenmin);
							if ( synonyms ) {
								char *syn = synonyms, *s;
								while ( (s=strchr(syn, ',')) ) {
									*s = '\0';
									fprintf(fpack, "sed -i '/\\\\addlanguage{%s}.*/d' %%{_texdir}/texmf-dist/tex/generic/config/language.def\n", syn);
									fprintf(fpack, "echo \"\\addlanguage{%s}{%s}{}{%s}{%s}\" >> %%{_texdir}/texmf-dist/tex/generic/config/language.def\n", syn, file, lefthyphenmin, righthyphenmin);
									*s = ',';
									syn = s+1;
								}
								fprintf(fpack, "sed -i '/\\\\addlanguage{%s}.*/d' %%{_texdir}/texmf-dist/tex/generic/config/language.def\n", syn);
								fprintf(fpack, "echo \"\\addlanguage{%s}{%s}{}{%s}{%s}\" >> %%{_texdir}/texmf-dist/tex/generic/config/language.def\n", syn, file, lefthyphenmin, righthyphenmin);
							}
							for (--k; k>=10; k--) if ( pkg[i].exe[n][k] == '\0' ) pkg[i].exe[n][k] = ' ';
							run_fmtutil = 1;
							continue;
						}
						fprintf(stderr, "Unknown exec format: %s\n", pkg[i].exe[n]);
						exit(1);
						continue;
					}
					if ( run_updmap ) fprintf(fpack, "touch /var/run/texlive/run-updmap\n");
					if ( run_fmtutil ) fprintf(fpack, "touch /var/run/texlive/run-fmtutil\n");
					fprintf(fpack, "fi\n:\n");
#ifndef SRPMS
					fprintf(fpack, "\n%%postun %s\n", name);
#else
					fprintf(fpack, "\n%%postun\n");
#endif
					fprintf(fpack, "if [ $1 == 0 ] ; then\n");
					for (run_updmap=n=0; n<pkg[i].exes; n++) {
						if ( !strncmp(pkg[i].exe[n], "addLuaMap", 9) ) {
							continue;
						}
						if ( !strncmp(pkg[i].exe[n], "addMap ", 7) ) {
							fprintf(fpack, "%%{_bindir}/updmap-sys --nomkmap --disable Map=%s"REDIR, skipspaces(&pkg[i].exe[n][7]));
							run_updmap = 1;
							continue;
						}
						if ( !strncmp(pkg[i].exe[n], "addMixedMap ", 12) ) {
							fprintf(fpack, "%%{_bindir}/updmap-sys --nomkmap --disable MixedMap=%s"REDIR, skipspaces(&pkg[i].exe[n][12]));
							run_updmap = 1;
							continue;
						}
						if ( !strncmp(pkg[i].exe[n], "addKanjiMap ", 12) ) {
							fprintf(fpack, "%%{_bindir}/updmap-sys --nomkmap --disable KanjiMap=%s"REDIR, skipspaces(&pkg[i].exe[n][12]));
							run_updmap = 1;
							continue;
						}
						if ( !strncmp(pkg[i].exe[n], "BuildFormat ", 12) ) {
							fprintf(fpack, "%%{_bindir}/fmtutil-sys --disablefmt %s"REDIR, &pkg[i].exe[n][12]);
							run_fmtutil = 1;
							continue;
						}
						if ( !strncmp(pkg[i].exe[n], "AddFormat ", 10) ) {
							char *name	= strstr(pkg[i].exe[n], "name="),
							     *engine	= strstr(pkg[i].exe[n], "engine="),
							     *patterns	= strstr(pkg[i].exe[n], "patterns="),
							     *options	= strstr(pkg[i].exe[n], "options=");
							char *opt, opt_char;

							if ( !name || !engine || !options ) {
								fprintf(stderr, "Invalid AddFormat entry in package %s: '%s' '%s' '%s' '%s'.\n", pkg[i].name, name, engine, patterns, options);
								exit(1);
							}
							name += 5;
							engine += 7;
							if ( patterns ) patterns += 9;
							options += 8;

							*strchr(name, ' ') = '\0';
							*strchr(engine, ' ') = '\0';
							if ( patterns ) *strchr(patterns, ' ') = '\0';
							if ( *options == '"' ) {
								options++;
								opt = strchr(options, '"');
							} else {
								for (opt=options; *opt != ' ' && *opt != '\n'; opt++);
							}
							opt_char = *opt;
							*opt = '\0';

							fprintf(fpack, "sed -i 's/^%s.*$/\\#\\!\\ %s %s %s %s/' %%{_texdir}/texmf-dist/web2c/fmtutil.cnf"REDIR, name, name, engine, patterns?patterns:"-", options);

							name[strlen(name)] = ' ';
							engine[strlen(engine)] = ' ';
							if ( patterns ) patterns[strlen(patterns)] = ' ';
							*opt = opt_char;

							run_fmtutil = 1;
							continue;
						}
						if ( !strncmp(pkg[i].exe[n], "AddHyphen ", 10) ) {
							char *name		= strstr(pkg[i].exe[n], "name="),
							     *synonyms		= strstr(pkg[i].exe[n], "synonyms="),
							     *lefthyphenmin	= strstr(pkg[i].exe[n], "lefthyphenmin="),
							     *righthyphenmin	= strstr(pkg[i].exe[n], "righthyphenmin="),
							     *file		= strstr(pkg[i].exe[n], "file=");
							int k;

							if ( !name || !lefthyphenmin || !righthyphenmin || !file ) {
								fprintf(stderr,"Invalid AddHyphen entry in package %s.\n", pkg[i].name);
								exit(1);
							}
							name += 5;
							if ( synonyms ) synonyms += 9;
							lefthyphenmin += 14;
							righthyphenmin += 15;
							file += 5;
							for (k=10; pkg[i].exe[n][k]; k++) if ( pkg[i].exe[n][k] == ' ' ) pkg[i].exe[n][k] = '\0';

							fprintf(fpack, "sed -i '/%s.*/d' %%{_texdir}/texmf-dist/tex/generic/config/language.dat"REDIR, name);
							if ( synonyms ) {
								char *syn = synonyms, *s;
								while ( (s=strchr(syn, ',')) ) {
									*s = '\0';
									fprintf(fpack, "  sed -i '/=%s/d' %%{_texdir}/texmf-dist/tex/generic/config/language.dat"REDIR, syn);
									*s = ',';
									syn = s+1;
								}
								fprintf(fpack, "  sed -i '/=%s/d' %%{_texdir}/texmf-dist/tex/generic/config/language.dat"REDIR, syn);
							}
							fprintf(fpack, "sed -i '/\\\\addlanguage{%s}.*/d' %%{_texdir}/texmf-dist/tex/generic/config/language.def"REDIR, name);
							if ( synonyms ) {
								char *syn = synonyms, *s;
								while ( (s=strchr(syn, ',')) ) {
									*s = '\0';
									fprintf(fpack, "sed -i '/\\\\addlanguage{%s}.*/d' %%{_texdir}/texmf-dist/tex/generic/config/language.def"REDIR, syn);
									*s = ',';
									syn = s+1;
								}
								fprintf(fpack, "sed -i '/\\\\addlanguage{%s}.*/d' %%{_texdir}/texmf-dist/tex/generic/config/language.def"REDIR, syn);
							}
							for (--k; k>=10; k--) if ( pkg[i].exe[n][k] == '\0' ) pkg[i].exe[n][k] = ' ';
							run_fmtutil = 1;
							continue;
						}
					}
					fprintf(fpack, "mkdir -p /var/run/texlive\ntouch /var/run/texlive/run-texhash\ntouch /var/run/texlive/run-mtxrun\n");
					if ( run_updmap ) fprintf(fpack, "touch /var/run/texlive/run-updmap\n");
					if ( run_fmtutil ) fprintf(fpack, "touch /var/run/texlive/run-fmtutil\n");
					fprintf(fpack, "fi\n:\n\n");
#ifndef SRPMS
					fprintf(fpack, "%%posttrans %s\n", name);
#else
					fprintf(fpack, "%%posttrans\n");
#endif
					fprintf(fpack, "if [ -e /var/run/texlive/run-texhash ]; then %%{_bindir}/texhash 2> /dev/null; rm -f /var/run/texlive/run-texhash; fi\n");
					if ( run_updmap ) fprintf(fpack, "if [ -e /var/run/texlive/run-updmap ]; then %%{_bindir}/updmap-sys --quiet --nomkmap &> /dev/null;rm -f /var/run/texlive/run-updmap; fi\n");
					if ( run_fmtutil ) fprintf(fpack, "if [ -e /var/run/texlive/run-fmtutil ]; then %%{_bindir}/fmtutil-sys --all &> /dev/null; rm -f /var/run/texlive/run-fmtutil; fi\n");
					fprintf(fpack, "if [ -e /var/run/texlive/run-mtxrun ]; then export TEXMF=/usr/share/texlive/texmf-dist; export TEXMFCNF=/usr/share/texlive/texmf-dist/web2c; export TEXMFCACHE=/var/lib/texmf; %%{_bindir}/mtxrun --generate &> /dev/null; rm -f /var/run/texlive/run-mtxrun; fi\n");
					fprintf(fpack, ":\n\n");
				} else if ( pkg[i].runfs ) {
#ifndef SRPMS
					fprintf(fpack, "%%post %s\n", name);
#else
					fprintf(fpack, "%%post\n");
#endif
					fprintf(fpack, "mkdir -p /var/run/texlive\ntouch /var/run/texlive/run-texhash\ntouch /var/run/texlive/run-mtxrun\n");
					if ( pkg[i].has_info ) {
						int k;

						for (k=0; k<pkg[i].runfs; k++) {
							if (!strncmp(pkg[i].runf[k], "texmf-dist/doc/info/", 20)) {
								fprintf(fpack, "/sbin/install-info %%{_infodir}/%s %%{_infodir}/dir 2>/dev/null\n", &pkg[i].runf[k][20]);
							}
						}
					}
					fprintf(fpack, ":\n");
#ifndef SRPMS
					fprintf(fpack, "\n%%postun %s\n", name);
#else
					fprintf(fpack, "\n%%postun\n");
#endif
					fprintf(fpack, "if [ $1 == 1 ]; then\n  mkdir -p /var/run/texlive\n  touch /var/run/run-texhash\nelse\n  %%{_bindir}/texhash 2> /dev/null\nfi\n");
					fprintf(fpack, ":\n\n");
#ifndef SRPMS
					fprintf(fpack, "%%posttrans %s\n", name);
#else
					fprintf(fpack, "%%posttrans\n");
#endif
					fprintf(fpack, "if [ -e /var/run/texlive/run-texhash ] && [ -e %%{_bindir}/texhash ]; then %%{_bindir}/texhash 2> /dev/null; rm -f /var/run/texlive/run-texhash; fi\n");
					fprintf(fpack, "if [ -e /var/run/texlive/run-mtxrun ]; then export TEXMF=/usr/share/texlive/texmf-dist; export TEXMFCNF=/usr/share/texlive/texmf-dist/web2c; export TEXMFCACHE=/var/lib/texmf; %%{_bindir}/mtxrun --generate &> /dev/null; rm -f /var/run/texlive/run-mtxrun; fi\n");
					fprintf(fpack, ":\n\n");
				}

				/* ... and main files */
#ifdef SRPMS
				mainpkg = 1;
#endif
				main_written = 0;
				append_filelist(pkg[i].name, "", pkg[i].runfs, pkg[i].runf, pkg[i].fedora_license?pkg[i].fedora_license:put_token(pkg[i].catalogue_license, license));
#ifdef SRPMS
				mainpkg = 0;
#endif
			}
			main_written = pkg[i].runfs || pkg[i].reqs || pkg[i].exes;
#ifdef PACKAGE_DOCS
			/* write doc package if exists */
			if ( pkg[i].docfs ) {
				pkg[i].any_pkg_written = 1;
				if ( !doc_expanded ) {
					fprintf(funpack, UNPACK" -dc %%{SOURCE%d} | tar x -C %%{buildroot}%%{_texdir}%s\n", srcno, pkg[i].reloc?"/texmf-dist":"");
					fprintf(fsrc, "Source%04d: "CTAN_URL"%s.doc.tar."UNPACK"\n", srcno++, name);
				}
				doc_expanded = 0;
#ifdef SRPMS
				if ( !main_written ) {
					fprintf(fpack, "Name: tex-%s-doc\n", name);
					fprintf(fpack, "Obsoletes: texlive-%s-doc\n", name);
					fprintf(fpack, "License: %s\n", pkg[i].fedora_license?pkg[i].fedora_license:(put_token(pkg[i].catalogue_license, spec_license)?put_token(pkg[i].catalogue_license, spec_license):"LPPL"));
				} else {
					fprintf(fpack, "%%package doc\n");
				}
#else
				fprintf(fpack, "%%package %s-doc\n", name);
#endif
				fprintf(fpack, "Summary: Documentation for %s\n", name);
				fprintf(fpack, "Version: %s\n", print_noarch_version(&pkg[i]));
				fprintf(fpack, "Release: %%{tl_noarch_release}\n");
				fprintf(fpack, "Provides: tex-%s-doc\n", name);
				fprintf(fpack, "BuildArch: noarch\nAutoReqProv: No\n");
				for (n=0; n<pkg[i].reqs; n++) {
					if ( !pkg[i].req[n] ) continue;
					if ( pkg[i].req[n]->catalogue_license & LIC_NOTALLOWED ) continue;
					if ( pkg[i].req[n]->docfs )
						fprintf(fpack, "Requires: tex-%s-doc\n", pkg[i].dep[n]);
				}
				if ( main_written ) {
#ifndef SRPMS
					fprintf(fpack, "\n%%description %s-doc\n", name);
#else
					fprintf(fpack, "\n%%description doc\n");
#endif
				} else {
#ifdef SRPMS
					fprintf(fpack, "\n%%description\n");
#else
					fprintf(fpack, "\n%%description %s-doc\n", name);
#endif
				}
				fprintf(fpack, "Documentation for %s\n\n", name);

				/* ... and doc files */
#ifdef SRPMS
				mainpkg = 1;
#endif
				append_filelist(pkg[i].name, "doc", pkg[i].docfs, pkg[i].docf, pkg[i].fedora_license?pkg[i].fedora_license:put_token(pkg[i].catalogue_license, license));
#ifdef SRPMS
				mainpkg = 0;
#endif

			}
#endif
#ifdef PACKAGE_SOURCE
			/* write source package if exists */
			if ( pkg[i].srcfs ) {
				fprintf(funpack, UNPACK" -dc %%{SOURCE%d} | tar x -C %%{buildroot}%%{_texdir}%s\n", srcno, pkg[i].reloc?"/texmf-dist":"");
				fprintf(fsrc, "Source%04d: "CTAN_URL"%s.source.tar."UNPACK"\n", srcno++, name);
#ifndef SRPMS
				fprintf(fpack, "%%package %s-source\n", name);
#else
				fprintf(fpack, "%%package source\n");
#endif
				fprintf(fpack, "Summary: Sources for %s\n", name);
				fprintf(fpack, "Version: %s\n", print_noarch_version(&pkg[i]));
				fprintf(fpack, "Release: %%{tl_noarch_release}\n");
				if ( strncmp(name, "kpathsea", 8) ) fprintf(fpack, "Requires: texlive-base\n");
				fprintf(fpack, "BuildArch: noarch\nAutoReqProv: No\n");
				for (n=0; n<pkg[i].reqs; n++) {
					if ( !pkg[i].req[n] ) continue;
					if ( pkg[i].req[n]->catalogue_license & LIC_NOTALLOWED ) continue;
					if ( pkg[i].req[n]->srcfs )
						fprintf(fpack, "Requires: tex-%s-source\n", pkg[i].dep[n]);
				}
#ifndef SRPMS
				fprintf(fpack, "\n%%description %s-source\n", name);
#else
				fprintf(fpack, "\n%%description source\n");
#endif
				fprintf(fpack, "Sources for %s\n\n", name);

				/* ... and src files */
#ifdef SRPMS
				mainpkg = 1;
#endif
				append_filelist(pkg[i].name, "source", pkg[i].srcfs, pkg[i].srcf, pkg[i].fedora_license?pkg[i].fedora_license:put_token(pkg[i].catalogue_license, license));
#ifdef SRPMS
				mainpkg = 0;
#endif
			}
#else
			/* write just link to source */
			if ( pkg[i].srcfs ) {
				fprintf(fsrc, "Source%04d: "CTAN_URL"%s.source.tar."UNPACK"\n", srcno++, name);
			}
#endif
#ifdef FEDORA_FONTS
			/* fonts */
			{
				int n, has_fonts = 0, k;

				for (n=0; n<pkg[i].runfs; n++) {
					size_t s = strlen(pkg[i].runf[n]);
					if (s > 4) {
						if (!strcmp(&pkg[i].runf[n][s-4], ".ttf") ||
						    !strcmp(&pkg[i].runf[n][s-4], ".ttc") ||
						    !strcmp(&pkg[i].runf[n][s-4], ".pfa") ||
						    !strcmp(&pkg[i].runf[n][s-4], ".pfb") ||
						    !strcmp(&pkg[i].runf[n][s-4], ".pcf") ||
						    !strcmp(&pkg[i].runf[n][s-4], ".otf")
						) {
							if ( !has_fonts ) {
#ifdef SRPMS
								fprintf(fpack, "%%package fedora-fonts\n");
#else
								fprintf(fpack, "%%package %s-fedora-fonts\n", name);
#endif
								fprintf(fpack, "Summary: Fonts for %s\n", name);
								fprintf(fpack, "Version: %s\n", print_noarch_version(&pkg[i]));
								fprintf(fpack, "Release: %%{tl_noarch_release}\n");
								fprintf(fpack, "Requires: fontpackages-filesystem\n");
								fprintf(fpack, "BuildRequires: fontpackages-devel\n");
								fprintf(fpack, "Requires: tex-%s\n", name);
								fprintf(fpack, "BuildArch: noarch\n");
#ifdef SRPMS
								fprintf(fpack, "\n%%description fedora-fonts\n");
#else
								fprintf(fpack, "\n%%description %s-fedora-fonts\n", name);
#endif
								for (k=0; k<pkg[i].longdesc_lines; k++) {
									fprintf(fpack, "%s\n", pkg[i].longdesc[k]);
								}
								if ( !pkg[i].longdesc_lines ) fprintf(fpack, "Fonts for %s package.\n", name);
								if ( pkg[i].catalogue_date ) fprintf(fpack, "\ndate: %s\n", pkg[i].catalogue_date);
								fprintf(fpack, "\n");
								fprintf(ffont, "\n# link installed fonts with Fedora\n");
								fprintf(ffont, "install -d -m 0755 %%{buildroot}%%{_fontdir}\n");
								fprintf(ffont, "pushd %%{buildroot}%%{_fontdir}\n");
#ifdef SRPMS
								fprintf(ffile, "%%files fedora-fonts\n");
#else
								fprintf(ffile, "%%files %s-fedora-fonts\n", name);
#endif
								fprintf(ffile, "%%defattr(-,root,root)\n%%dir %%{_fontdir}\n");
							}
							has_fonts = 1;
							for (--s; pkg[i].runf[n][s] != '/'; s--);
							fprintf(ffont, "mv %%{buildroot}%%{_texdir}/%s .\n", pkg[i].runf[n]);
							fprintf(ffont, "ln -s %%{_fontdir}%s %%{buildroot}%%{_texdir}/%s\n", &pkg[i].runf[n][s], pkg[i].runf[n]);
							fprintf(ffile, "%%{_fontdir}%s\n", &pkg[i].runf[n][s]);
							printf("%%{_fontdir}%s\n", &pkg[i].runf[n][s]);
						}
					}
				}
				if ( has_fonts ) {
					fprintf(ffont, "popd\n");
#ifdef SRPMS
					fprintf(ffont, "%%_font_pkg -n fedora *\n");
#endif
				}
			}
#endif
#ifdef SRPMS
			if (pkg[i].has_man) {
				fprintf(fremove, "mkdir -p %%{buildroot}/%%{_datadir}/\n");
				fprintf(fremove, "mv %%{buildroot}/%%{_texdir}/texmf-dist/doc/man %%{buildroot}/%%{_datadir}/\n");
			}
			if (pkg[i].has_info) {
				fprintf(fremove, "mkdir -p %%{buildroot}/%%{_infodir}/\n");
				fprintf(fremove, "mv %%{buildroot}/%%{_texdir}/texmf-dist/doc/info/* %%{buildroot}/%%{_infodir}/\n");
			}
#endif
#ifdef SRPMS
			if ( !pkg[i].binfs ) {
				fclose(ffont);
				fclose(fremove);
				fclose(fsrc);
				fclose(funpack);
				fclose(ffile);
				fclose(fpack);

				fpack = ofpack;
				ffile = offile;
				funpack = ofunpack;
				fsrc = ofsrc;
				fremove = ofremove;
				ffont = offont;
			}
#endif
			if ( pkg[i].binfs && (has_noarch_pkg || pkg[i].binfs > 1) ) {
				char *ar = strstr(name, ".ARCH");
				pkg[i].any_pkg_written = 1;
				*ar = '\0';
				fprintf(fpack, "%%package %s-bin\n", name);
				fprintf(fpack, "Summary: Binaries for %s\n", name);
				fprintf(fpack, "Version: %s\n", print_noarch_version(&pkg[i]));
				if ( strncmp(name, "kpathsea", 8) ) fprintf(fpack, "Requires: texlive-base\n");
				if ( has_noarch_pkg ) fprintf(fpack, "Requires: texlive-%s\n", name);
				if ( !strcmp(name, "xetex") ) {
					fprintf(fpack, "Requires: teckit\n");
					fprintf(fpack, "Provides: xdvipdfmx = %%{version}-%%{release}\n");
					fprintf(fpack, "Obsoletes: xdvipdfmx < %%{version}-%%{release}\n");
				}
				if ( !strcmp(name, "dvipdfmx") ) {
					fprintf(fpack, "Provides: dvipdfmx = %%{tl_version}, dvipdfm = %%{tl_version}, texlive-dvipdfm-bin = 3:%%{tl_version}\n");
					fprintf(fpack, "Obsoletes: dvipdfmx < %%{tl_version}, dvipdfm < %%{tl_version}, texlive-dvipdfm-bin < 3:%%{tl_version}\n");
				}
				if ( !strcmp(name, "xdvi") ) {
					fprintf(fpack, "Provides: xdvi = %%{tl_version}, xdvik = %%{tl_version}, tetex-xdvi = 3.1-99\n");
					fprintf(fpack, "Obsoletes: xdvi < %%{tl_version}, xdvik < %%{tl_version}, tetex-xdvi < 3.1-99\n");
				}
				if ( !strcmp(name, "dvipng") ) {
					fprintf(fpack, "Provides: dvipng = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: dvipng < %%{tl_version}\n");
				}
				if ( !strcmp(name, "pdfcrop") ) {
					fprintf(fpack, "Requires: ghostscript-devel\n");
				}
				if ( !strcmp(name, "dvisvgm") ) {
					fprintf(fpack, "Provides: dvisvgm = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: dvisvgm < %%{tl_version}\n");
				}
				if ( !strcmp(name, "lcdftypetools") ) {
					fprintf(fpack, "Provides: lcdf-typetools = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: lcdf-typetools < %%{tl_version}\n");
				}
				if ( !strcmp(name, "xmltex") ) {
					fprintf(fpack, "Provides: xmltex = %%{tl_version}0101\n");
					fprintf(fpack, "Obsoletes: xmltex < %%{tl_version}0101\n");
				}
				if ( !strcmp(name, "pstools") ) {
					fprintf(fpack, "Provides: ps2eps = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: ps2eps < %%{tl_version}\n");
				}
/*				if ( !strcmp(name, "asymptote") ) {
					fprintf(fpack, "Provides: asymptote = %%{tl_version}\n");
					fprintf(fpack, "Obsoletes: asymptote < %%{tl_version}\n");
				}*/

				printf("bin-package %s contains %d files\n", pkg[i].name, pkg[i].binfs);
				{
					int n, noarch = 1;
					char s[0x100];

					for (n=0; n<pkg[i].binfs; n++) {
						FILE *f;
						struct stat sb;

						snprintf(s, sizeof(s), "texlive.expanded/%s", pkg[i].binf[n]);
						lstat(s, &sb);

						if ((sb.st_mode&S_IFMT) == S_IFLNK) continue;

						if ( (f=fopen(s,"rb")) ) {
							unsigned char d[4];
							fread(d, 4, 1, f);
							fclose(f);
							if ( d[0] == 0x7f && d[1] == 0x45 && d[2] == 0x4c && d[3] == 0x46 ) {
								noarch = 0;
								break;
							}
						} else {
							printf("Unable to open: %s\n", s);
							exit(1);
						}
					}
					fprintf(fpack, "Release: %%{tl_release}\n");
					if ( noarch ) {
						fprintf(fpack, "BuildArch: noarch\n");
					} else {
						fprintf(fpack, "Requires: texlive-kpathsea-lib%{?_isa} = %%{epoch}:%%{tl_version}\n");
					}
				}
				fprintf(fpack, "\n%%description %s-bin\n", name);
				fprintf(fpack, "Binaries for %s\n\n", name);
				*ar = '.';

				/* ... and add bin files */
				{
					char s[0x100], *lic_name = NULL;
					int ii, lic_code = LIC_LPPL;
					unsigned long h;

					strcpy(s, pkg[i].name);
					*strstr(s,".ARCH") = 0;
					h = hash(s);
					for (ii=0; ii<p; ii++) {
						if ( pkg[ii].namehash == h && !strcmp(pkg[ii].name, s)) {
							lic_code = pkg[ii].catalogue_license?pkg[ii].catalogue_license:LIC_LPPL;
							lic_name = pkg[ii].fedora_license;
							break;
						}
					}
					append_filelist(pkg[i].name, "", pkg[i].binfs, pkg[i].binf, lic_name?lic_name:put_token(lic_code, license));
				}
			}
slv:
			for (n=0; n<pkg[i].reqs; n++) {
				solve(pkg[i].dep[n]);
			}
			level--;
			found = 1;
			break;
		}
	}

	if ( !found ) fprintf(stderr, "Unknown dep: %s\n", name);
}

void gen_obsoletes() {
	size_t i, op = sizeof(old_pkgs)/sizeof(old_pkgs[0]);
	FILE *fobs = fopen("_obsoletes.spec","wt");

	for (i=0; i<op; i++) {
		size_t n, fnd=0;
		unsigned long h = hash(old_pkgs[i]);

		for (n=0; n<p; n++) {
			if (h == pkg[n].namehash && !strcmp(pkg[n].name, old_pkgs[i]) && pkg[n].any_pkg_written) {
				fnd = 1;
				break;
			}
		}

		if (!fnd) {
			fprintf(fobs,"Obsoletes: texlive-%s <= 3:%%{tl_version}\n", old_pkgs[i]);
			if (strncmp(old_pkgs[i], "collection-", 11)) {
				fprintf(fobs,"Obsoletes: texlive-%s-bin <= 3:%%{tl_version}\n", old_pkgs[i]);
				fprintf(fobs,"Obsoletes: texlive-%s-doc <= 3:%%{tl_version}\n", old_pkgs[i]);
				fprintf(fobs,"Obsoletes: texlive-%s-fedora-fonts <= 3:%%{tl_version}\n", old_pkgs[i]);
			}
		}
	}

	fclose(fobs);
}

int main() {
	FILE *f = fopen("texlive.tlpdb","rt");

	if ( !f ) {
		fprintf(stderr, "Unable to open TeX Live package database\n");
		return 1;
	}

	fseek(f,0,SEEK_END);
	size=ftell(f);
	fseek(f,0,SEEK_SET);
	m=malloc(size);
	if ( fread(m, size, 1, f) != 1 ) {
		fprintf(stderr,"Error reading TeX Live package database\n");
		return 1;
	}

	parse();

	{
		int i, n;

		for (i=0; i<p; i++) {
			for (n=0; n<pkg[i].reqs; n++) {
				if ( pkg[i].req[n] ) continue;
				{
					int x, y, found = 0;
					unsigned long h;
					package *pk = NULL;
					char *depname = pkg[i].dep[n];

					h = hash(depname);

					for (x=0; x<p; x++) {
						if ( pkg[x].namehash == h && !strcmp(pkg[x].name, depname) ) {
							pk = &pkg[x];
							found = 1;
							break;
						}
					}

					if ( !found ) {
						fprintf(stderr, "Unknown dependency: %s\n", depname);
						continue;
					}

					for (x=0; x<p; x++) {
						for (y=0; y<pkg[x].reqs; y++) {
							if ( !strcmp(pkg[x].dep[y], pk->name) ) {
								pkg[x].req[y] = pk;
							}
						}
					}
				}
			}
		}
#ifdef SRPMS
		system("rm -rf ./specs; mkdir specs");
#endif
		fill_file_reqprov();
		for (i=0; i<p; i++) solve(pkg[i].name);
	}

	gen_obsoletes();

	{
		int i, n, ndirs;
		FILE *fdirs = fopen("_dirs.spec","wt");
#ifdef SRPMS
		FILE *fmkdirs = fopen("_mkdirs.spec","wt");
#endif

		ndirs = dirs;
		for ( i=0; i<ndirs; i++ ) {
			char *end, *d;
			int pass;

			if ( !strncmp(dir[i].dir, "bin/", 4) || !strncmp(dir[i].dir, "tlpkg/", 6) || dir[i].pkgs < 1 ) continue;

			for ( pass=n=0; n<dir[i].pkgs; n++ ) {
				if ( !(dir[i].lic[0]&LIC_NOTALLOWED) ) {
					pass = 1;
					break;
				}
			}
			if ( !pass ) continue;

			if ( !(strstr(dir[i].pkg[0], "win32") || strstr(dir[i].dir, "win32")) ) {
				fprintf(fdirs, "%%dir %%{_texdir}/%s\n", dir[i].dir);
#ifdef SRPMS
				fprintf(fmkdirs, "mkdir -p %%{buildroot}%%{_texdir}/%s\n", dir[i].dir);
#endif
			} else continue;

			d = strdup(dir[i].dir);
			while ( (end=strrchr(d, '/')) ) {
				unsigned long h;
				*end = '\0';
				h = hash(d);
				for ( n=0; n<dirs; n++ ) {
					if ( h == dir[n].dirhash && !strcmp(d, dir[n].dir) ) {
						goto done;
					}
				}
				dirs++;
				dir = realloc(dir, dirs*sizeof(dir_type));
				dir[dirs-1].dir = strdup(d);
				dir[dirs-1].dirhash = h;
				dir[dirs-1].pkgs = 0;
				fprintf(fdirs, "%%dir %%{_texdir}/%s\n", d);
			}
done:
			free(d);
		}
#ifdef SRPMS
		fclose(fmkdirs);
#endif
		fclose(fdirs);
	}

	fclose(fpack);
	fclose(ffile);
	fclose(funpack);
	fclose(fsrc);
	fclose(fremove);
	fclose(ffont);

	return 0;
}
