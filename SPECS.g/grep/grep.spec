Summary: Pattern matching utilities
Summary(zh_CN.UTF-8): 文本模式匹配工具
Name: grep
Version: 2.18
Release: 3%{?dist}
License: GPLv3+
Group: Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
Source: ftp://ftp.gnu.org/pub/gnu/grep/grep-%{version}.tar.xz
Source1: colorgrep.sh
Source2: colorgrep.csh
Source3: GREP_COLORS
Patch1: grep-2.11-gnulib-tests-rm-f.patch
URL: http://www.gnu.org/software/grep/
Requires(post): /usr/sbin/install-info
Requires(preun): /usr/sbin/install-info
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: pcre-devel >= 3.9-10, texinfo, gettext
BuildRequires: autoconf automake
Provides:	/bin/grep, /bin/fgrep, /bin/egrep

%description
The GNU versions of commonly used grep utilities. Grep searches through
textual input for lines which contain a match to a specified pattern and then
prints the matching lines. GNU's grep utilities include grep, egrep and fgrep.

GNU grep is needed by many scripts, so it shall be installed on every system.

%description -l zh_CN.UTF-8
文本匹配查找工具，包括 grep, egrep 和 fgrep。

许多脚本都用这个命令，所以它应该安装在每个系统上。

%prep
%setup -q
%patch1 -p1 -b .gnulib-tests-rm-f

%build
%global BUILD_FLAGS $RPM_OPT_FLAGS

# Currently gcc on ppc uses double-double arithmetic for long double and it
# does not conform to the IEEE floating-point standard. Thus force
# long double to be double and conformant.
%ifarch ppc ppc64
%global BUILD_FLAGS %{BUILD_FLAGS} -mlong-double-64
%endif

%configure --without-included-regex CPPFLAGS="-I%{_includedir}/pcre" \
  CFLAGS="%{BUILD_FLAGS}"
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT install
gzip $RPM_BUILD_ROOT%{_infodir}/grep*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}
magic_rpm_clean.sh
%find_lang %name

%if 0%{?with_check}
%check
make check
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/usr/sbin/install-info --quiet --info-dir=%{_infodir} %{_infodir}/grep.info.gz || :

%preun
if [ $1 = 0 ]; then
	/usr/sbin/install-info --quiet --info-dir=%{_infodir} --delete %{_infodir}/grep.info.gz || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ABOUT-NLS AUTHORS THANKS TODO NEWS README ChangeLog COPYING

%{_bindir}/*
%config(noreplace) %{_sysconfdir}/profile.d/colorgrep.*sh
%config(noreplace) %{_sysconfdir}/GREP_COLORS
%{_infodir}/*.info*.gz
%{_mandir}/*/*

%changelog
* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 2.18-3
- 更新到 2.18

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 2.11-3
- 为 Magic 3.0 重建

* Mon Apr 16 2012 Liu Di <liudidi@gmail.com> - 2.11-2
- 为 Magic 3.0 重建

* Fri Mar  2 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.11-1
- New version

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.10-3
- Rebuild against PCRE 8.30

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.10-1
- New version

* Mon Jul 11 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9-3
- Use rm -f in gnulib-tests (gnulib-tests-rm-f patch)
  Resolves: rhbz#716330

* Mon Jul 04 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9-2
- Fixed build failure on ppc - long double forced to double on ppc

* Wed Jun 22 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9-1
- New version: grep-2.9
- Removed dfa-buffer-overrun-fix patch

* Mon Jun 20 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.8-4
- dfa: don't overrun a malloc'd buffer for certain regexps
  (patch dfa-buffer-overrun-fix)
  Resolves: rhbz#713328

* Mon May 16 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.8-3
- Added coloring aliases to csh script as well

* Mon May 16 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.8-2
- Added coloring to egrep and fgrep
  Resolves: rhbz#697895

* Mon May 16 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.8-1
- New version: grep-2.8
  Resolves: rhbz#704710
- Removed const-range-exp patch (upstreamed)

* Mon Apr 04 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7-5
- colorgrep scripts no longer overwrites COLORS envvar (#693058),
  thanks to Ville Skyttä

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 01 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7-3
- Fixed inconsistency with range expressions, const-range-exp patch (#583011)

* Wed Sep 29 2010 jkeating - 2.7-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7-1
- New version: grep-2.7
- Removed patches (already in upstream): dfa-optimize-period,
  glibc-matcher-fallback, mmap-option-fix, dfa-convert-to-wide-char,
  dfa-speedup-digit-xdigit

* Fri Jun 11 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.3-4
- Colors can be globally disabled via /etc/GREP_COLORS (#602867)
- Fixed indentation in spec
- Fixed defattr in spec

* Mon Jun 07 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.3-3
- Added auto-color profile.d scripts (thanks to Ville Skyttä #600832)
- Removed description macro from changelog

* Tue May 06 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.3-2
- Added dfa-optimize-period patch (speedup for . patterns in UTF-8)
- Added glibc-matcher-fallback patch (speedup for [a-z] patterns in UTF-8)
- Added mmap-option-fix patch
- Added dfa-convert-to-wide-char patch (speedup for -m and remove quadratic
  complexity when going to glibc)
- Added dfa-speedup-digit-xdigit patch (speedup for [[:digit:]] [:xdigit:]])

* Sun Apr 04 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.3-1
- New version: grep-2.6.3
- make check is not silent now

* Fri Mar 26 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.1-1
- New version: grep-2.6.1
- Dropped sigsegv patch (integrated upstream)

* Tue Mar 23 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6-1
- New version: grep-2.6
- Added sigsegv patch (after release patch from upstream)
- Dropped obsoleted patches: fedora-tests, pcrewrap, case, egf-speedup,
  bz460641, utf8, dfa-optional, w

* Fri Mar 05 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.5.4-2
- Added w patch to fix -w switch behaviour broken by dfa-optional patch

* Wed Feb 10 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.5.4-1
- New version: grep-2.5.4
- Fixed typos in description
- Updated utf-8 patch
- Added dfa-optional patch (#538423)

* Tue Aug 11 2009 Lubomir Rintel <lkundrak@v3.sk> 2.5.3-6
- Silence possible scriptlets errors

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Stepan Kasal <skasal@redhat.com> 2.5.3-3
- remove grep-mem-exhausted.patch (#481765, #198165)

* Thu Jan  8 2009 Stepan Kasal <skasal@redhat.com> 2.5.3-2
- fix bug #460641 (a.k.a. 479152)

* Thu Nov 20 2008 Lubomir Rintel <lkundrak@v3.sk> 2.5.3-1
- Update to latest upstream version
- Drop upstreamed patches
- Add a couple of regression tests
- Temporarily disable tests
- Minor cleanup

* Wed Oct 1 2008 Lubomir Rintel <lkundrak@v3.sk> 2.5.1a-61
- Fix pcre-mode (-P) line wrapping (bug #324781)
- Match the version with upstream
- Recode AUTHORS to utf8

* Fri Jul 25 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.5.1-60
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.5.1-59
- Autorebuild for GCC 4.3

* Fri Apr 20 2007 Stepan Kasal <skasal@redhat.com> - 2.5.1-58
- Adhere to packaging guidelines.
- Resolves: #225857
- Use CPPFLAGS= argument to configure to add an -I option.
- Do not set LDFLAGS=-s for "make install".

* Mon Jan 22 2007 Tim Waugh <twaugh@redhat.com> 2.5.1-57
- Make preun scriptlet unconditionally succeed (bug #223697).

* Wed Nov 22 2006 Tim Waugh <twaugh@redhat.com> 2.5.1-56
- Fixed count of patterns when the last is an empty string (bug #204255).

* Wed Nov 22 2006 Tim Waugh <twaugh@redhat.com> 2.5.1-55
- Fix 'memory exhausted' errors by limiting in-memory buffer (bug #198165).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.5.1-54.1
- rebuild

* Wed May 31 2006 Tim Waugh <twaugh@redhat.com> 2.5.1-54
- Applied upstream patch to fix '-D skip' (bug #189580).

* Mon Feb 20 2006 Tim Waugh <twaugh@redhat.com> 2.5.1-53
- Applied Tim Robbins' patch for 'grep -w' (bug #179698).

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.5.1-52.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.5.1-52.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb  3 2006 Tim Waugh <twaugh@redhat.com> 2.5.1-52
- Prevent 'grep -P' from segfaulting (bug #171379).

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Sep 29 2005 Tim Waugh <twaugh@redhat.com> 2.5.1-51
- Prevent 'grep -Fw ""' from busy-looping (bug #169524).

* Tue Jun 28 2005 Tim Waugh <twaugh@redhat.com> 2.5.1-50
- Further fixing for bug #161700.

* Mon Jun 27 2005 Tim Waugh <twaugh@redhat.com> 2.5.1-49
- Fix 'grep -Fw' for encodings other than UTF-8 (bug #161700).

* Wed Apr 13 2005 Tim Waugh <twaugh@redhat.com>
- Build requires recent pcre-devel (bug #154626).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 2.5.1-48
- Rebuild for new GCC.

* Fri Jan  7 2005 Tim Waugh <twaugh@redhat.com> 2.5.1-47
- Run 'make check'.
- Fixed -w handling for EGexecute.  Now 'make check' passes.
- Cache MB_CUR_MAX value in egf-speedup patch.
- Fixed variable shadowing in egf-speedup patch.
- Removed redundant (and incorrect) code in prline.

* Fri Jan  7 2005 Tim Waugh <twaugh@redhat.com> 2.5.1-46
- More -w tests from Jakub Jelinek.
- Rebased on 2.5.1a.

* Fri Dec 31 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-45
- More tests (Jakub Jelinek).
- Jakub Jelinek's much improved -Fi algorithm.
- Removed bogus part of grep-2.5.1-fgrep patch.

* Tue Dec 21 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-44
- Fixed -Fi for multibyte input (bug #143079).

* Thu Dec 16 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-43
- Bypass kwset matching when ignoring case and processing multibyte input
  (bug #143079).

* Tue Dec 14 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-42
- Further UTF-8 processing avoided since a '\n' byte is always an
  end-of-line character in that encoding.

* Fri Dec  3 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-41
- Fixed a busy loop in the egf-speedup patch (bug #140781).

* Thu Nov 18 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-40
- Fixed a bug in the fgrep patch, exposed by the dfa-optional patch
  (bug #138558).

* Tue Nov 16 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-39
- Fixed last patch.

* Tue Nov 16 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-38
- Applied patch from Karsten Hopp to fix background colour problems with
  --color output (bug #138913).

* Wed Nov 10 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-37
- Prevent false matches when DFA is disabled (bug #138558).

* Mon Nov  8 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-36
- Automatically disable DFA when processing multibyte input.  GREP_USE_DFA
  environment variable overrides.

* Fri Nov  5 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-35
- Fixes to egf-speedup patch: now it does not change any functionality,
  as intended.
- GREP_NO_DFA now turns off the DFA engine, for performance testing.

* Thu Nov  4 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-34
- More improvements to egf-speedup patch (bug #138076).

* Thu Nov  4 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-33
- Small improvements to egf-speedup patch.

* Wed Nov  3 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-32
- Remove mb-caching hack.
- Better multibyte handling in EGexecute() and Fexecute().
- Don't need regex.c changes in grep-2.5-i18n.patch.

* Wed Oct 13 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-31
- Make 'grep -F' avoid UTF-8 processing if the pattern contains no
  multibyte characters (bug #133932).

* Mon Oct 11 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-30
- Applied patch from Robert Scheck to tidy spec file and add a URL
  tag (bug #135185).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jun  4 2004 Tim Waugh <twaugh@redhat.com>
- More build requirements (bug #125323).

* Tue May 18 2004 Jeremy Katz <katzj@redhat.com> 2.5.1-28
- rebuild

* Tue May 18 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-27
- Fix dfa multibyte character class matching when -i is used (bug #123363).
- Use bracket patch before i18n patch to make it clear that the bug exists
  upstream.

* Thu Feb 26 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-26
- Fix fgrep (bug #116909).

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan  5 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-24
- Work around glibc bug #112869 (segfault in re_compile_pattern).
- Avoid patching Makefile.am, to avoid automake/autoconf weirdness.

* Wed Dec 10 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-23
- Another multibyte efficiency bug-fix (bug #111800).

* Mon Dec  8 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-22
- Fixed [:alpha:]-type character classes (bug #108484).
- Fixed -o -i properly (bug #111489).

* Sat Dec  6 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-21
- Fixed 'fgrep -i' (bug #111614).

* Fri Nov 21 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-20
- Another two multibyte efficiency bug-fixes (bug #110524).

* Thu Nov  6 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-19
- Fixed a multibyte efficiency bug.

* Thu Nov  6 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-18
- Turn on multibyte efficiency patch again to shake out bugs.

* Wed Oct  8 2003 Tim Waugh <twaugh@redhat.com>
- Fixed man page bug (bug #106267).

* Thu Sep 18 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-17
- Use symlinks for egrep/fgrep, rather than shell script wrappers.

* Fri Jun 27 2003 Tim Waugh <twaugh@redhat.com>
- Fix debuginfo package.

* Fri Jun 27 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-16.1
- Rebuilt.

* Fri Jun 27 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-16
- Finally give up on making grep go fast. :-(

* Thu Jun 26 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-15.1
- Rebuilt.

* Thu Jun 26 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-15
- Fixed grep -i bug introduced by cache.

* Mon Jun 23 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-14.1
- Rebuilt.

* Mon Jun 23 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-14
- Redo the gofast patch (bug #97785).

* Thu Jun 12 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-13.1
- Rebuilt.

* Thu Jun 12 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-13
- Fixed a bug in the gofast patch (bug #97266).

* Tue Jun 10 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-12.1
- Rebuilt.

* Tue Jun 10 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-12
- Go faster (bug #69900).
- Fix man page.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 29 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-10.1
- Rebuilt.

* Thu May 29 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-10
- Use system regex again.

* Thu May 29 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-9
- Fixed bug in go-fast patch.

* Wed May 28 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-8
- Go fast (bug #69900).
- Run test suite.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 2.5.1-7
- rebuilt

* Tue Nov 19 2002 Tim Waugh <twaugh@redhat.com> 2.5.1-6
- i18n patch.

* Mon Oct 21 2002 Tim Waugh <twaugh@redhat.com> 2.5.1-5
- Don't install /usr/share/info/dir.
- Fix -o -i (bug #72641).

* Sat Jul 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- install all info files #69204

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Mar 26 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.5.1-1
- 2.5.1

* Wed Mar 13 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.5-1
- 2.5 final

* Wed Jan 23 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.5-0.g.1
- 2.5g

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Nov 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5-0.f.4
- Update CVS to reduce bloat

* Thu Nov  8 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5-0.f.3
- Don't fail %%post with --excludedocs

* Wed Sep 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5-0.f.2
- Fix up echo A |grep '[A-Z0-9]' in locales other than C

* Tue Sep 25 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5-0.f.1
- 2.5f, fixes #53603

* Wed Jul 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.4.2-7
- Fix up the i18n patch - it used to break "grep '[]a]'" (#49003)
- revert to 2.4.2 (latest official release) for now

* Mon May 28 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5e-4
- Fix "echo Linux forever |grep -D skip Linux"

* Mon May 21 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5e-3
- Add new -D, --devices option
- Fix a bug with "directories" being uninitialized

* Sun May 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5e-2
- Fix up the --color option to behave like the one from ls (--color=auto)
  Sooner or later, some people will alias grep="grep --color" and wonder why
  their scripts break.
- Update docs accordingly
- Get rid of the annoying blinking in grep --color

* Sun May 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5e-1
- 2.5e

* Tue Feb 27 2001 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath}
- langify

* Sun Aug 20 2000 Jakub Jelinek <jakub@redhat.com>
- i18n character ranges patch from Ulrich Drepper

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHSify

* Tue Mar 21 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 2.4.2
- fix download URL

* Thu Feb 03 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- gzip info pages (Bug #9035)

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Wed Dec 22 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.4.

* Wed Oct 20 1999 Bill Nottingham <notting@redhat.com>
- prereq install-info

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- upgraded to grep 2.3, added install-info %%post/%%preun for info

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Sat May 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.2

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- updated from 2.0 to 2.1
- spec file cleanups
- added BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
