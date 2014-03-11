%define	name	smake
%define	version	1.2a49
%define	release	1
%define	serial	7
%define	prefix	/usr

%define	major	1.2

Summary:	The Schily smake program.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{serial}
Prefix:		%{prefix}
License:	GPL
Group:		Developement
Vendor:		Joerg Schilling <schilling@fokus.gmd.de>
URL:		http://www.fokus.gmd.de/research/cc/glone/employees/joerg.schilling/private/smake.html
Source:		%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Smake is the only make program with automake features, it is the only program
that works on unknown platforms..

Smake executes command sequences based on relations of modification dates of
files. The command sequences are taken from a set of rules found in a makefile
or in the set of implicit rules. The argument target is typically a program
that is to be built from the known rules.

If no -f option is present, smake looks for SMakefile then for Makefile and
then for makefile in the named order.

If no target is specified on the command line, smake uses the first target that
could be found in makefilename and that does not start with a dot ('.').

If a target has no explicit entry in the makefile smake tries to use implicit
rules or the .DEFAULT rule.

Unlike most other make programs, smake propagates all com­ mand line macros to
sub makes. This is a big advantage with hierarchical makefile systems.
Propagation is done in a POSIX compliant way using the MAKEFLAGS= environment.

Unlike other make programs, smake includes a set of automake features that
allow to implement portable, layered, object oriented makefiles.

%prep
%setup -q -n %{name}-%{major}

%build
if [ ! -z "`which smake 2>/dev/null`" ]; then
    export MAKEPROG='smake';
elif [ ! -z "`which gmake 2>/dev/null`" ]; then
    export MAKEPROG='gmake';
else
    export MAKEPROG='make';
fi

${MAKEPROG};

%install
[ -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT};

if [ ! -z "`which smake 2>/dev/null`" ]; then
    export MAKEPROG='smake';
elif [ ! -z "`which gmake 2>/dev/null`" ]; then
    export MAKEPROG='gmake';
else
    export MAKEPROG='make';
fi

${MAKEPROG} "INS_BASE=${RPM_BUILD_ROOT}%{prefix}" install

# libschily.a installed by cdrtools, no need for it here...
[ -f "${RPM_BUILD_ROOT}%{prefix}/lib/libschily.a" ] && \
    rm -f "${RPM_BUILD_ROOT}%{prefix}/lib/libschily.a";

mkdir smake-rpmdocs
cp AN-%{version} PORTING README* smake/defaults.smk smake-rpmdocs
chmod 644 smake-rpmdocs/*

rm -rf %{buildroot}%{_includedir}
rm -f  %{buildroot}%{_prefix}/lib/profiled/libschily.a

%clean
[ -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT};

%files
%defattr(-,root,root)
%doc smake-rpmdocs/*

%config(noreplace) %{prefix}/lib/defaults.smk

%{prefix}/bin/smake
#{prefix}/include/align.h
#{prefix}/include/avoffset.h

%{prefix}/man/man1/smake.1*
%{prefix}/man/man5/makerules.5*
%{prefix}/man/man5/makefiles.5*

%changelog
* Thu Nov 17 2005 Ryan Weaver <ryanw@falsehope.com>
  [smake-1.2a34-1]
- Fixed a bug introduced with smake-1.2a33 that caused
  smake to core dump in some cases with "exported" to
  environment make macros.
- Let fileopen() flose the fd in case that it could not
  get a FILE * struct for fd.
- Added support to compile 64 bit versions by calling
  smake CCOM=cc64

* Tue Aug  2 2005 Ryan Weaver <ryanw@falsehope.com>
  [smake-1.2a33-1]
- Make sure that $(VAR:%=PREFIX/%) does expand to nothing
  in case that $(VAR) is empty.
- export VAR now expands the content of the make macro "VAR"
  before putting the content into the environment.
- print a better warning message when smake finds too many
  target items (targets left to a ':') for a rule.
- Now using recent a makefiles-1.5 alpha
  - Avoid an endless loop with 'tr' on Solaris if 
    /usr/ucb/ is before /usr/bin in PATH

* Wed Jul  6 2005 Ryan Weaver <ryanw@falsehope.com>
  [smake-1.2a32-1]
- Smake now may be used to compile Xorg.
- New option -N
  Continue if no source for nonexistent dependencies found.
- Evaluate the SHELL macro acording to POSIX.
  SHELL has been previously ignored completely.
- Do not allow names with a SLASH inside at the right
  side of a Simple Suffix Default Rule.
  This helps smake to ignore the junk at the end of some
  POSIX Suffix rules found in the makefiles of Xorg.
- Let smake warn about junk at the end of POSIX
  suffix rules. This helps to flag broken makefiles
  like those found in the Xorg tree.
- The dynmac expander now correctly handles the case when
  the growable buffer has to be relocated when it grows.
- The dynmac expander now does no longer adds unneded spaces
  in lists. This allows smake to be used to compile Xorg.
- Smake now gives better warnings with illegal dynmac usage.
  This helps to locate illegal dynmac usage in highly complex
  projects like Xorg.

* Mon Jun 13 2005 Ryan Weaver <ryanw@falsehope.com>
  [smake-1.2a31-1]
- Add snprintf.c to allow compilation on HP-UX-10.x
- -k / -S Option implemented according to POSIX
- .s.o: Assembly rules added to default rules and
  to .SUFFIXES
- ...move and ...touch messages now go to stdout as
  the command verbose messages
- messages from exit handler now only if
    excode != 0 && Mlevel > 0
    Debug > 0   && Mlevel > 0
- Check for NAMEMAX in getln() deactivated
- Do not check for default rules in case of 
  final :: rules
- install-sh updated to know that 
  BSDi chown is in /usr/sbin

* Tue May  3 2005 Ryan Weaver <ryanw@falsehope.com>
  [smake-1.2a30-1]
- The top level Makefile in SRCROOT now calls
  psmake/smake -r to make sure that no broken
  internal rules (that could be loaded from
  a file) may be active.

- Support for the ':=' assignement oparator that
  may be used with make macros:

  CFLAGS := $(OTHER_VAR)

  Will not assign the text "$(OTHER_VAR)" to
  CFLAGS but the content if the macro $(OTHER_VAR)

  As this feature is nonportable, smake warns
  when the feature is used. (Note that Sun make
  uses := for conditional macro assignement).

- Smake now detects endless recursions from bad
  default rules.

- Smake now supports Termination pattern matching
  rules
    target:: source
      command

  If a Termination rule is found, smake does not
  search for possible sources for intermediate
  source file names. This allows to e.g. create 
  a pattern rule for fetching SCCS files from 
  the repository:

    %:: s.%
      sccs get $@

  Note that this rule would otherwise result
  in a endless recusion.

- Smake now prints Command line Exit messages for
  failed commaned even if not in debug mode.

- Better messages when exiting with exit code != 0

- Makefile fixed to search for the make default rules
  in $(INS_DIR)/lib/defaults.smk instead of
  $(INS_DIR)/lib/default.smk

- New configure #ifdef DEFAULTS_PATH_SEARCH_FIRST
  tells smake to search for lib/default.smk in
  PATH first.

- Smake now also searches for lib/default.smk in
  case av[0] contains a path name with slashes.

* Fri Apr 29 2005 Ryan Weaver <ryanw@falsehope.com>
  [smake-1.2a29-1]
- Print the current directory in case it a exitcode != 0
- Support for :: rules added.
  This is not POSIX but historic use in makefiles.
- Intermediate target nodes are now fully initialized.
- Smake now appends to dependency lists even when the new definition
  is found in a new makefile (-f option). Before, smake did overwrite
  such definitions.
- Smake now changes the type from environment macro definitions into
  target definitions if the same name is later found in a Makefile.
  This is eg. needed if the environment contains host=foo and the
  Makefile contains host: host.c
- If a second explicit rule for a target is found and it contains
  command definitions, smake now no longer overwrites the list of
  command line definitions with the new list but keeps the first
  definition.
- If a second explicit rule for a target is found and it contains
  no command definitions, smake now no longer kills the old definitions.
- Smake now warns if the dynamic macros '$*' & '$<' are used on commands
  for explicit Target Rules. Note that Sun Make as well as GNU make are
  broken in this area (*) and smake's behavor is the best a make program
  may do.
  *)
  Sun Make calls (even though this is an _explicit_ rule) the implicit
  rule check and looks for possible implicit sources. If a possible
  implicit source file exists, '$<' is set to that name even though it
  is completely unrelated to the explicit rule. If a fitting entry from
  .SUFFIXES: exists, '$@' is stripped to create '$*'.
  GNU make returns the first name from the dependency list for '$<' and
  strips '$@' using a fitting entry from .SUFFIXES: to create '$*'.
- smake no longer tries to "make" the content from o_list of
  a NAME=val type object.
- smake no longer has a command line macro limit of 64, the
  command line macros are now inside allocated memory
- smake no longer has a -f makefile option limit of 32, the
  makefile names are now inside allocated memory

* Mon Apr 25 2005 Ryan Weaver <ryanw@falsehope.com>
  [smake-1.2a28-1]
- make sure a rule like:

  ../somedir/target: ../somedir/source

  will not be falsely detected as Simple Suffix rule
- Expand the right side if a VPATH= statement
  to allow VPATH=$(srcdir) to work.
- .SUFFIXES Target will no longer be overwritten
  but appended if asigned in a new Makefile.
  This allows a .SIFFIXES: .suf line in Makefile
  to append to the likst of the internal makefile.
- CFLAGS += now works again (parser fixed).
- The dynamic macro $O (.OBJDIR or "." if .OBJDIR
  has not been defined) may now be overwritten.
  This makes smake more POSIX compliant as POSIX
  does not include a dynamic macro $O.

* Tue Apr 19 2005 Ryan Weaver <ryanw@falsehope.com>
  [smake-1.2a27-1]
- smake now has been tested with various makefiles from various
  software and is expected to be able to be used to compile
  any piece of software that does not rely on bugs found in specific
  make implementeations. The following problems are currently known:
  - GNU make comes with two files called 'SMakefile' and
    thus feeds two files with the preferred Makefile name
    into smake. Unfortunately, these two file in GNU make do
    not contain valid make syntax.
    Solution: Before you like to compile GNU make using smake,
    you need to remove "SMakefile" and "glob/SMakefile".
  - Samba comes with a Makefile that illegally useses the '$<'
    dynamic macro in commands for explicit rules. The '$<'
    dynamic macro is only expanded in case that an
    implicit (inference) rule is processed. As samba uses '$<'
    inside an explicit rule where this dynamic macro has no
    meaning (see POSIX make standard) it is expanded to nothing
    but space by smake.
    Solution: change '$<' to a manual copy of the source file
    for explicit rules.
  - Samba comes with a Makefile that illegally useses the '$*'
    dynamic macro in commands for explicit rules. The '$*'
    dynamic macro is only expanded in case that an
    implicit (inference) rule is processed. As samba uses '$*'
    inside an explicit rule where this dynamic macro has no useful
    meaning (see POSIX make standard) and smake cannot know the
    'right' suffix, '$*' is expanded to the part of '$@' being
    left to the rightmost '.' character in '$@' by smake.
    Solution: change something like '$*.po.o' to '$@'
    for explicit rules.
  - If you find other problems, plese report and let us find
    the reason..... It is most likely that the related
    Makefile is buggy.
- smake -d now prints make level (in case of recursive make calls)
  and the working directory for smake.
- smake -d now prints .OBJDIR .OBJSEARCH .SEARCHLIST (needed -dd before)
- The parser has been fixed so that white space at the end of a list
  will no longer be expanded into a Null ('') object name:
  DUMMY=
  LIST= 1 2 3 4 $(DUMMY)
  target: $(LIST)
  Did create such a problem.
- Better source comments for FORCE: target type special treatment.
- FORCE: Target type special treatment is now done even when
  the target in question is the current default target.
- Print the .PHONY: state of a target in various debug output
- smake -t does no longer touch targets marked
  as .PHONY:
- Debug print of default target is now also included if the default
  target is explicitly named via arvg[] from main().
- Smake no longer strips off the directory name for targets
  when expanding the '$*' Dynamic macro.
  Smake did previously expand '$*' for dir/name.o -> name
  Smake now           expands '$*' for dir/name.o -> dir/name

* Thu Apr 14 2005 Ryan Weaver <ryanw@falsehope.com>
  [smake-1.2a26-1]
- smake now should be useful as a general make utility
  as it now includes all needed default rules required by POSIX
- Starting to implement Termination pattern rules
  using :: as Terminator (not yet ready).
- Syntax errors now are less verbose again, but
  smake -d will turn on printing the read buffer
  of the parser to help to debug the problem.
- Simple Suffix Rules are no longer allowed to start with "./"
  as this is a valid target name.
- Better EOF checing in the parser to avoid infinite loops.
- A parser bug has been fixed that did cause smake not
  to stop parsing macro definitions in dependency lists
  if not surrounded by () or {}.
- default_cmd() now returns NOTIME in case no default
  rule could be found and the target has no prerequisites.
  This avoids superfluous "all is up to date" messages
  in case that no suffix rules have been defined.
- Switch from our own "Simple Pattern Rules" for implicit rules
  to POSIX Single and Double suffix Rules.
- smake -p now includes comment headlines that allow for better
  identification of the various sections in the output.
- The directory rules for the Schily makefile system have
  been modified to work around a bug in /bin/sh on BSDi 
  systems.

* Wed Apr  6 2005 Ryan Weaver <ryanw@falsehope.com>
  [smake-1.2a24-1]
- .POSIX target documented in the man page
- Command execution now finally has been fixed:
  /bin/sh -ce cmd is called by default to abort on error
  /bin/sh -c cmd is called is for 'smake -i'

  [smake-1.2a25-1]
- Checking vor valid time in dyn macro expansion (e.g. $?)
  because the time stamp of a not yet existent target may
  have been intermediately set to RESURCETIME. This would
  have caused $? to be incorrectly expanded.
- Try to add a workaround for broken Makefiles like:

  all: $(SUBDIRS)

  $(SUBDIRS): FORCE
  	cd $@ && $(MAKE) $(MAKEDEFS)

  FORCE:

  The target FORCE is not only completely unneeded; it would
  cause the Sub directories not to be made except when smake
  introduces a special implict behavior that treats FORCE:
  as a target that could be correctly made altohough there is
  no implicit dependency FORCE.c as there is neither an 
  explicit dependency not an explicit command list.
- Support for Linux on amd64 has been added

* Fri Sep 10 2004 Ryan Weaver <ryanw@falsehope.com>
  [smake-1.2a23-1]
- Add a workaround for a SCO OpenServer C-compiler bug.
  The bug causes the first function in a function to be called
  before the new stack frame has been established and did cause
  scanning the stack frame to fail.
- made snprintf() POSIX compliant
- Try to find sh.exe from PATH on DJGPP
  Thanks to Alex Kopylov <reanimatolog@yandex.ru>
- We now call caommands again via sh -ce 'cmd' instead of
  sh -c 'cmd' (which is what POSIX requires).
  It turned out that POSIX is wrong and causes complex commands
  (e.g. commands that use ';') that fail not to cause smake
  to stop on this error.

  Note that smake originally has been correct and did use sh -ce.
  Missleaded by the fact that GNU make (at this point) follows
  the POSIX standard, smake has been changed to use sh -c.
  We now correct our misstake.

