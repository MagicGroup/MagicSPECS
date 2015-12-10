Summary: A tool for creating scanners (text pattern recognizers)
Summary(zh_CN.UTF-8): 生成扫描器的工具（文本模式识别）
Name: flex
Version:	2.5.37
Release: 6%{?dist}
# parse.c and parse.h are under GPLv3+ with exception which allows
#	relicensing.  Since flex is shipped under BDS-style license,
#	let's  assume that the relicensing was done.
# gettext.h (copied from gnulib) is under LGPLv2+
License: BSD and LGPLv2+
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
URL: http://flex.sourceforge.net/
Source: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

# https://sourceforge.net/tracker/?func=detail&aid=3546447&group_id=97492&atid=618177
Patch0: flex-2.5.36-bison-2.6.1.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=925801
Patch1: flex-2.5.37-aarch64.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=993447
Patch2: flex-2.5.37-types.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: m4
BuildRequires: gettext bison m4
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
The flex program generates scanners.  Scanners are programs which can
recognize lexical patterns in text.  Flex takes pairs of regular
expressions and C code as input and generates a C source file as
output.  The output file is compiled and linked with a library to
produce an executable.  The executable searches through its input for
occurrences of the regular expressions.  When a match is found, it
executes the corresponding C code.  Flex was designed to work with
both Yacc and Bison, and is used by many programs as part of their
build process.

You should install flex if you are going to use your system for
application development.

%description -l zh_CN.UTF-8
生成扫描器的工具。扫描器是一种可以识别文本中的指定模式的程序。

# We keep the libraries in separate sub-package to allow for multilib
# installations of flex.
%package devel
Summary: Libraries for flex scanner generator
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Obsoletes: flex-static < 2.5.35-15
Provides: flex-static

%description devel

This package contains the library with default implementations of
`main' and `yywrap' functions that the client binary can choose to use
instead of implementing their own.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: Documentation for flex scanner generator
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Documentation
Group(zh_CN.UTF-8): 文档

%description doc

This package contains documentation for flex scanner generator in
plain text and PDF formats.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%global flexdocdir %{_datadir}/doc/flex-doc-%{version}

%build
%configure --disable-dependency-tracking CFLAGS="-fPIC $RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT docdir=%{flexdocdir} install
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
rm -f $RPM_BUILD_ROOT/%{flexdocdir}/{README.cvs,TODO}

( cd ${RPM_BUILD_ROOT}
  ln -sf flex .%{_bindir}/lex
  ln -sf flex .%{_bindir}/flex++
  ln -s flex.1 .%{_mandir}/man1/lex.1
  ln -s flex.1 .%{_mandir}/man1/flex++.1
  ln -s libfl.a .%{_libdir}/libl.a
)

rm -f %{buildroot}%{_libdir}/*.la
magic_rpm_clean.sh
%find_lang flex

%post
if [ -f %{_infodir}/flex.info.gz ]; then # for --excludedocs
   /sbin/install-info %{_infodir}/flex.info.gz --dir-file=%{_infodir}/dir ||:
fi

%preun
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/flex.info.gz ]; then # for --excludedocs
	/sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir ||:
    fi
fi

%check
echo ============TESTING===============
make check
echo ============END TESTING===========

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f flex.lang
%defattr(-,root,root)
%doc COPYING NEWS README
%{_bindir}/*
%{_mandir}/man1/*
%{_includedir}/FlexLexer.h
%{_infodir}/flex.info*
#%{_libdir}/libfl*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
#%{_libdir}/*.so

%files doc
%defattr(-,root,root)
%{_datadir}/doc/flex-doc-%{version}

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 2.5.37-6
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 2.5.37-5
- 为 Magic 3.0 重建

* Thu Apr 03 2014 Liu Di <liudidi@gmail.com> - 2.5.39-4
- 更新到 2.5.39

* Tue Sep  3 2013 Petr Machata <pmachata@redhat.com> - 2.5.37-4
- Add a patch for "comparison between signed and unsigned" warnings
  that GCC produces when compiling flex-generated scanners
  (flex-2.5.37-types.patch)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr  4 2013 Petr Machata <pmachata@redhat.com> - 2.5.37-2
- Update config.sub and config.guess to support aarch64

* Wed Mar 20 2013 Petr Machata <pmachata@redhat.com> - 2.5.37-1
- Rebase to 2.5.37

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 26 2012 Petr Machata <pmachata@redhat.com> - 2.5.36-2
- Bump for rebuild

* Tue Jul 31 2012 Petr Machata <pmachata@redhat.com> - 2.5.36-1
- Rebase to 2.5.36
  - Drop flex-2.5.35-sign.patch, flex-2.5.35-hardening.patch,
    flex-2.5.35-gcc44.patch, flex-2.5.35-missing-prototypes.patch
  - Add flex-2.5.36-bison-2.6.1.patch
  - Add a subpackage doc
- Resolves #842073

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.35-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 12 2012 Petr Machata <pmachata@redhat.com> - 2.5.35-15
- Rename flex-static to flex-devel so that it gets to repositories of
  minor multi-lib arch (i386 on x86_64 etc.)
- Resolves: #674301

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.35-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.35-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 17 2010 Petr Machata <pmachata@redhat.com> - 2.5.35-12
- Drop the dependency of core package on flex-static.
- Resolves: #624549

* Wed Jul 14 2010 Petr Machata <pmachata@redhat.com> - 2.5.35-11
- Forgot that the changes in flex.skl won't propagate to skel.c
- Resolves: #612465

* Tue Jul 13 2010 Petr Machata <pmachata@redhat.com> - 2.5.35-10
- Declare yyget_column and yyset_column in reentrant mode.
- Resolves: #612465

* Wed Jan 20 2010 Petr Machata <pmachata@redhat.com> - 2.5.35-9
- Move libraries into a sub-package of their own.

* Tue Jan 12 2010 Petr Machata <pmachata@redhat.com> - 2.5.35-8
- Add source URL

* Mon Aug 24 2009 Petr Machata <pmachata@redhat.com> - 2.5.35-7
- Fix installation with --excludedocs
- Resolves: #515928

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.35-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 20 2009 Debarshi Ray <rishi@fedoraproject.org> - 2.5.35-5
- Resolves: #496548.

* Mon Apr 20 2009 Petr Machata <pmachata@redhat.com> - 2.5.35-4
- Get rid of warning caused by ignoring return value of fwrite() in
  ECHO macro.  Debian patch.
- Resolves: #484961

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon May 12 2008 Petr Machata <pmachata@redhat.com> - 2.5.35-2
- Resolves: #445950

* Wed Feb 27 2008 Petr Machata <pmachata@redhat.com> - 2.5.35-1
- Rebase to 2.5.35. Drop two patches.
- Resolves: #434961
- Resolves: #435047

* Mon Feb 25 2008 Petr Machata <pmachata@redhat.com> - 2.5.34-1
- Rebase to 2.5.34. Drop five patches.
- Resolves: #434676

* Mon Feb 11 2008 Petr Machata <pmachata@redhat.com> - 2.5.33-17
- Generate prototypes for accessor functions.  Upstream patch.
- Related: #432203

* Mon Feb  4 2008 Petr Machata <pmachata@redhat.com> - 2.5.33-16
- Fix comparison between signed and unsigned in generated scanner.
  Patch by Roland McGrath.
- Resolves: #431151

* Tue Jan 15 2008 Stepan Kasal <skasal@redhat.com> - 2.5.33-15
- Do not run autogen.sh, it undoes the effect of includedir patch.
- Adapt test-linedir-r.patch so that it fixes Makefile.in and works
  even though autogen.sh is not run.

* Thu Jan 10 2008 Stepan Kasal <skasal@redhat.com> - 2.5.33-14
- Insert the "-fPIC" on configure command-line.
- Drop the -fPIC patch.

* Tue Jan  8 2008 Petr Machata <pmachata@redhat.com> - 2.5.33-13
- Patch with -fPIC only after the autogen.sh is run.

* Thu Jan  3 2008 Petr Machata <pmachata@redhat.com> - 2.5.33-12
- Run autogen.sh before the rest of the build.
- Add BR autoconf automake gettext-devel.

* Thu Aug 30 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-11
- Add BR gawk
- Fix use of awk in one of the tests

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.5.33-10
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-9
- Remove wrong use of @includedir@ in Makefile.in.
- Spec cleanups.
- Related: #225758

* Fri Jun 22 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-8
- Don't emit yy-prefixed variables in C++ mode.  Thanks Srinivas Aji.
- Related: #242742
- Related: #244259

* Fri May 11 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-7
- Allow joining short options into one commandline argument.
- Resolves: #239695

* Fri Mar 30 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-5
- Make yy-prefixed variables available to scanner even with -P.

* Fri Feb  2 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-4
- Use %%find_lang to package locale files.

* Wed Jan 31 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-3
- Compile with -fPIC.

* Tue Jan 30 2007 Petr Machata <pmachata@redaht.com> - 2.5.33-2
- Add Requires:m4.

* Fri Jan 19 2007 Petr Machata <pmachata@redhat.com> - 2.5.33-1
- Rebase to 2.5.33

* Tue Jul 18 2006 Petr Machata <pmachata@redhat.com> - 2.5.4a-41
- Reverting posix patch.  Imposing posix because of warning is too
  much of a restriction.

* Sun Jul 16 2006 Petr Machata <pmachata@redhat.com> - 2.5.4a-40
- using dist tag

* Fri Jul 14 2006 Petr Machata <pmachata@redhat.com> - 2.5.4a-39
- fileno is defined in posix standard, so adding #define _POSIX_SOURCE
  to compile without warnings (#195687)
- dropping 183098 test, since the original bug was already resolved

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4a-38.1
- rebuild

* Fri Mar 10 2006 Petr Machata <pmachata@redhat.com> - 2.5.4a-38
- Caught the real cause of #183098.  It failed because the parser
  built with `flex -f' *sometimes* made it into the final package, and
  -f assumes seven-bit tables.  Solution has two steps.  Move `make
  bigcheck' to `%%check' part, where it belongs anyway, so that flexes
  built during `make bigcheck' don't overwrite original build.  And
  change makefile so that `make bigcheck' will *always* execute *all*
  check commands.

* Wed Mar  8 2006 Petr Machata <pmachata@redhat.com> - 2.5.4a-37.4
- adding test for #183098 into build process

* Fri Mar  2 2006 Petr Machata <pmachata@redhat.com> - 2.5.4a-37.3
- rebuilt, no changes inside. In hunt for #183098

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4a-37.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4a-37.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Feb 02 2006 Petr Machata <pmachata@redhat.com> 2.5.4a-37
- adding `make bigcheck' into build process.  Refreshing initscan.c to
  make this possible.

* Wed Jan 18 2006 Petr Machata <pmachata@redhat.com> 2.5.4a-36
- Applying Jonathan S. Shapiro's bugfix-fixing patch. More std:: fixes
  and better way to silent warnings under gcc.

* Fri Jan 13 2006 Petr Machata <pmachata@redhat.com> 2.5.4a-35
- Adding `std::' prefixes, got rid of `using namespace std'. (#115354)
- Dummy use of `yy_flex_realloc' to silent warnings. (#30943)
- Adding URL of flex home page to spec (#142675)

* Sun Dec 18 2005 Jason Vas Dias<jvdias@redhat.com>
- rebuild with 'flex-pic.patch' to enable -pie links
  on x86_64 (patch from Jesse Keating) .

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Apr 10 2005 Jakub Jelinek <jakub@redhat.com> 2.5.4a-34
- rebuilt with GCC 4
- add %%check script

* Tue Aug 24 2004 Warren Togami <wtogami@redhat.com> 2.5.4a-33
- #116407 BR byacc

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Jeff Johnson <jbj@redhat.com> 2.5.4a-28
- don't include -debuginfo files in package.

* Mon Nov  4 2002 Than Ngo <than@redhat.com> 2.5.4a-27
- YY_NO_INPUT patch from Jean Marie

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 18 2002 Than Ngo <than@redhat.com> 2.5.4a-25
- don't forcibly strip binaries

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr  2 2002 Than Ngo <than@redhat.com> 2.5.4a-23
- More ISO C++ 98 fixes (#59670)

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 2.5.4a-22
- rebuild in new enviroment

* Wed Feb 20 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.5.4a-21
- More ISO C++ 98 fixes (#59670)

* Tue Feb 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.5.4a-20
- Fix ISO C++ 98 compliance (#59670)

* Wed Jan 23 2002 Than Ngo <than@redhat.com> 2.5.4a-19
- fixed #58643

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Nov  6 2001 Than Ngo <than@redhat.com> 2.5.4a-17
- fixed for working with gcc 3 (bug #55778)

* Sat Oct 13 2001 Than Ngo <than@redhat.com> 2.5.4a-16
- fix wrong License (bug #54574)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Sat Sep 30 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix generation of broken code (conflicting isatty() prototype w/ glibc 2.2)
  This broke, among other things, the kdelibs 2.0 build
- Fix source URL

* Thu Sep  7 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging (64bit systems need to use libdir).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun  6 2000 Bill Nottingham <notting@redhat.com>
- rebuild, FHS stuff.

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- add a libl.a link to libfl.a

* Wed Aug 25 1999 Jeff Johnson <jbj@redhat.com>
- avoid uninitialized variable warning (Erez Zadok).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0 tree

* Mon Aug 10 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from 2.5.4 to 2.5.4a

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Mar 20 1997 Michael Fulbright <msf@redhat.com>
- Updated to v. 2.5.4
