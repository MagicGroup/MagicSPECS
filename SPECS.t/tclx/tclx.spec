%define major_ver 8.4
%define tcltk_ver 8.6.4

Summary: Extensions for Tcl and Tk
Summary(zh_CN.UTF-8): Tcl 的扩展。
Name: tclx
Version: %{major_ver}.0
Release: 12%{?dist}
License: BSD
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
URL: http://tclx.sourceforge.net/
Source: http://prdownloads.sourceforge.net/tclx/tclx%{major_ver}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: tcl >= %{tcltk_ver}, tk >= %{tcltk_ver}
BuildRequires: tcl-devel >= %{tcltk_ver}, tk-devel >= %{tcltk_ver}
BuildRequires: groff, autoconf
Patch1: tclx-%{major_ver}-varinit.patch
Patch2: tclx-%{major_ver}-relid.patch

%description
Extended Tcl (TclX) is a set of extensions to the Tcl programming language.
Extended Tcl is oriented towards system programming tasks and large
application development.  TclX provides additional interfaces to the
operating system, and adds many new programming constructs, text manipulation
and debugging tools.

%description -l zh_CN.UTF-8
扩展的 Tcl (TclX) 是 一组可以自由重发行的Tcl(工具命令语言)的扩展。Tcl 是一个简
单而又功能强大的脚本语言。TclX 面向系统编程任务和大型程序开发。它为自然操作系
统提供了附加的界面，许多新编程结构，文本操作工具，以及调试的功能。 

%package devel
Summary: Extended Tcl development files
Summary(zh_CN.UTF-8): 扩展 Tcl 开发文件
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
Requires: tclx = %{version}-%{release}

%description devel
Extended Tcl (TclX) is a set of extensions to the Tcl programming language.
Extended Tcl is oriented towards system programming tasks and large
application development.  TclX provides additional interfaces to the
operating system, and adds many new programming constructs, text manipulation
and debugging tools.

This package contains the tclx development files needed for building
tix applications.

%description devel -l zh_CN.UTF-8
扩展的 Tcl (TclX) 是 一组可以自由重发行的Tcl(工具命令语言)的扩展。Tcl 是一个简
单而又功能强大的脚本语言。TclX 面向系统编程任务和大型程序开发。它为自然操作系
统提供了附加的界面，许多新编程结构，文本操作工具，以及调试的功能。

这个包包含了建立tix应用程序所需要的tclx开发文件。

%package doc
Summary: Extended Tcl help and documentation
Summary(zh_CN.UTF-8): 扩展 Tcl 帮助和文档
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言

%description doc
Extended Tcl (TclX) is a set of extensions to the Tcl programming language.
Extended Tcl is oriented towards system programming tasks and large
application development.  TclX provides additional interfaces to the
operating system, and adds many new programming constructs, text manipulation
and debugging tools.

This package contains the tclx documentation

%description doc -l zh_CN.UTF-8
扩展的 Tcl (TclX) 是 一组可以自由重发行的Tcl(工具命令语言)的扩展。Tcl 是一个简
单而又功能强大的脚本语言。TclX 面向系统编程任务和大型程序开发。它为自然操作系
统提供了附加的界面，许多新编程结构，文本操作工具，以及调试的功能。

这个包包含了tclx文档。

%prep
%setup -q -n tclx%{major_ver}
%patch1 -p1 -b .1.varinit
%patch2 -p1 -b .2.relid

# patch2 touches tcl.m4
autoconf

%build
export CFLAGS=" $RPM_OPT_FLAGS -DUSE_INTERP_RESULT -DUSE_INTERP_ERRORLINE "
export CXXFLAGS=" $RPM_OPT_FLAGS -DUSE_INTERP_RESULT -DUSE_INTERP_ERRORLINE "
%configure \
   --enable-tk=YES \
   --with-tclconfig=%{_libdir} \
   --with-tkconfig=%{_libdir} \
   --with-tclinclude=%{_includedir} \
   --with-tkinclude=%{_includedir} \
   --enable-gcc \
   --enable-64bit
# smp building doesn't work
make all

# run "make test" by default
%{?_without_check: %define _without_check 1}
%{!?_without_check: %define _without_check 0}

%if ! %{_without_check}
   make test || :
%endif

%install
rm -rf $RPM_BUILD_ROOT

# utf-8 locale needed to avoid truncating help files
LANG=en_US.UTF-8 make install DESTDIR=%{buildroot}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/%{name}%{major_ver}

%files devel
%defattr(-,root,root,-)
%{_includedir}/*

%files doc
%defattr(-,root,root,-)
%doc ChangeLog README
%{_mandir}/man*

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 8.4.0-12
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 8.4.0-11
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 8.4.0-10
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 8.4.0-9
- 为 Magic 3.0 重建

* Thu Nov 01 2012 Liu Di <liudidi@gmail.com> - 8.4.0-8
- 为 Magic 3.0 重建

* Mon Feb 13 2012 Liu Di <liudidi@gmail.com> - 8.4.0-7
- 为 Magic 3.0 重建

* Sat Apr 29 2006 Liu Di <liudidi@gmail.com> - 8.4.0-2mgc
- Rebuild for MagicLinux
* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 8.4.0-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 8.4.0-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 David Cantrell <dcantrell@redhat.com> - 8.4.0-1
- Upgraded to tclx-8.4.0
- Removed patches that applied to the old build method for tclx
- Removed Tcl and Tk doc archives

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar  9 2005 Jens Petersen <petersen@redhat.com> - 8.3.5-6
- add unversioned symlinks to the static libs (Dave Botsch, 149734)
- rebuild with gcc 4
  - add tclx-8.3.5-clock_t-gcc4.patch to skip clock_t test in configure
  - buildrequire autoconf213

* Sun Feb 13 2005 Jens Petersen <petersen@redhat.com> - 8.3.5-5
- rebuild

* Thu Sep 30 2004 Jens Petersen <petersen@redhat.com> - 8.3.5-4
- buildrequire groff (Maxim Dzumanenko, 124554)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 03 2004 Jens Petersen <petersen@redhat.com> - 8.3.5-2
- install using utf-8 locale so that tclhelp help files get built properly
  (#116804)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> - 8.3.5-1.1
- rebuilt

* Wed Feb 25 2004 Jens Petersen <petersen@redhat.com> - 8.3.5-1
- new package split out from tcltk
- update to 8.3.5 release
- update source url
- no longer need tclx-8.3-argv.patch and tclx-8.3-helpdir.patch
- new devel and doc subpackages
- set TCLX_INST_LIB for configure
- add symlink for libtkx.so too
- clean build remnants from tclxConfig.sh and tkxConfig.sh
- rename memory.n to Memory.n, since tcl provides memory.n
- move help and manpages to -doc subpackage
- filtered out non-tclx changelog entries
- define tcltk_ver and use it
- include copy of tcl and tk manpages for buildhelp and
  apply tclx-8.3.5-tcltk-man-help.patch to point at them

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> 8.3.5-92
- rebuild again for #91211

* Fri Jan 17 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-85
- build all except tclx with _smp_mflags
- add some requires

* Tue Jan 14 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-84
- link all libs with DT_SONAME using tcl.m4 patch (#81297)
- drop synthetic lib provides
- remove obsolete patches from srpm
- update buildrequires
- use buildroot instead of RPM_BUILD_ROOT
- install all man pages under mandir, instead of moving some from /usr/man
- introduce _genfilelist macro for clean single-sweep find filelist generation
  for each package
- use perl to remove buildroot prefix from filelists

* Tue Jan  7 2003 Jeff Johnson <jbj@redhat.com> 8.3.5-80
- rebuild to generate deps for4 DSO's w/o DT_SONAME correctly.

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 8.3.5-79
- set execute bits on library so that requires are generated.

* Tue Dec 10 2002 Jens Petersen <petersen@redhat.com> 8.3.5-78
- make lib symlinks to .so not .so.0

* Tue Dec 10 2002 Jens Petersen <petersen@redhat.com> 8.3.5-77
- build and install tclx with _libdir (not libdir!)
- fix summary-not-capitalized for tclx, tcllib, tcl-html

* Mon Dec  9 2002 Jens Petersen <petersen@redhat.com> 8.3.5-76
- make it build on x86_64 (details below)
- don't explicitly update config.{guess,sub} since %%configure does it for us
- build and install tclx and tkx with INST_RUNTIME files under datadir, and
  EXEC_RUNTIME file under libdir
- generate filelists from datadir and not from mandir from now on

* Tue Dec  3 2002 Jens Petersen <petersen@redhat.com>
- update url for tcl, tk, tclx, itcl, tcllib
- build without all makecfg patches for now
  - in particular use upstream versioned library name convention
- add backward compatible lib symlinks for now
- use make's -C option rather than jumping in and out of source dirs
  during install
- use INSTALL_ROOT destdir-like make variable instead of makeinstall
  for all subpackages except tix and itcl

* Mon Oct 21 2002 Jens Petersen <petersen@redhat.com>
- move tclx HELP_DIR fix to separate patch

* Sat Jul 20 2002 Akira TAGOH <tagoh@redhat.com> 8.3.3-70
- tclx-8.3-nonstrip.patch: applied to fix the stripped binary issue.

* Mon Jan 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix config.guess and config.sub to newer versions

* Mon Aug  8 2001 Adrian Havill <havill@redhat.com>
- re-enable glibc string and math inlines; recent gcc is a-ok.
- optimize at -O2 instead of -O
- rename "soname" patches related to makefile/autoconf changes
- added elf "needed" for tk, tclx, tix, itk
- removed warnings from tclX

* Wed Jul 25 2001 Adrian Havill <havill@redhat.com>
- fixed 64 bit RPM provides for dependencies

* Thu Jul 19 2001 Adrian Havill <havill@redhat.com>
- updated tclX to the latest version
- fixed tclX 8.3's busted help install
- eliminated make TK_LIB kludge for multiple math libs for tclX
- used %%makeinstall to brute force fix any remaining unflexible makefile dirs

* Sun Jul  8 2001 Adrian Havill <havill@redhat.com>
- refresh all sources to latest stable (TODO: separate expect/expectk)
- massage out some build stuff to patches (TODO: libtoolize hacked constants)
- remove patches already rolled into the upstream
- removed RPATH (bugs 45569, 46085, 46086), added SONAMEs to ELFs
- changed shared object filenames to something less gross
- fixed tclX shell's argv parsing (bug 47710)

* Fri Mar 23 2001 Bill Nottingham <notting@redhat.com>
- bzip2 sources

* Mon Mar 19 2001 Bill Nottingham <notting@redhat.com>
- build with -D_GNU_SOURCE - fixes expect on ia64

* Tue Jun  6 2000 Jeff Johnson <jbj@redhat.com>
- tclX had wrong version.

* Fri Jun  2 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging changes.

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Thu Feb 03 2000 Elliot Lee <sopwith@redhat.com>
- Make changes from bug number 7602
- Apply patch from bug number 7537

* Tue Nov 30 1999 Jakub Jelinek <jakub@redhat.com>
- fix tclX symlinks.
- compile on systems where SIGPWR == SIGLOST.

* Tue Feb 16 1999 Jeff Johnson <jbj@redhat.com>
- upgrade tcl/tk/tclX to 8.0.4

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- update tcl/tk/tclX to 8.0.3, expect is updated also.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Mar 25 1998 Cristian Gafton <gafton@redhat.com>
- updated tclX to 8.0.2

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- fixed dangling tclx/tkx symlinks
