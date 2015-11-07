Name:           ocaml-omake
Version:        0.9.8.6
Release:        0.rc1%{?dist}.13
Summary:        Build system with automated dependency analysis
Summary(zh_CN.UTF-8): 自动分析依赖的编译系统
License:        LGPLv2+ with exceptions and GPLv2+ and BSD

URL:            http://omake.metaprl.org/download.html
Source0:        http://omake.metaprl.org/downloads/omake-%{version}-0.rc1.tar.gz

ExcludeArch:    sparc64 s390 s390x

Patch0:         omake-debian-disable-ocaml-warnings.patch
Patch1:         omake-0.9.8.6-fix-and-or-operators.patch
Patch2:         omake-0.9.8.6-kill-warn-error.patch

# omake can be used on non-OCaml projects (RHBZ#548536).
Provides:       omake

BuildRequires:  ocaml >= 3.10.2-2
BuildRequires:  ocaml-findlib-devel
BuildRequires:  gamin-devel
BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
#BuildRequires:  hevea
BuildRequires:  chrpath


%description
OMake is a build system designed for scalability and portability. It
uses a syntax similar to make utilities you may have used, but it
features many additional enhancements, including the following.

 * Support for projects spanning several directories or directory
   hierarchies.

 * Fast, reliable, automated, scriptable dependency analysis using MD5
   digests, with full support for incremental builds.

 * Dependency analysis takes the command lines into account — whenever
   the command line used to build a target changes, the target is
   considered out-of-date.

 * Fully scriptable, includes a library that providing support for
   standard tasks in C, C++, OCaml, and LaTeX projects, or a mixture
   thereof.

%description -l zh_CN.UTF-8
自动分析依赖的编译系统。

%prep
%setup -q -n omake-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
make all \
  PREFIX=%{_prefix} MANDIR=%{_mandir} BINDIR=%{_bindir} LIBDIR=%{_libdir}


%install
make install \
  INSTALL_ROOT=$RPM_BUILD_ROOT \
  PREFIX=%{_prefix} MANDIR=%{_mandir} BINDIR=%{_bindir} LIBDIR=%{_libdir}

chmod 0755 $RPM_BUILD_ROOT%{_bindir}/*
magic_rpm_clean.sh

%files
%doc LICENSE LICENSE.OMake
%doc CHANGELOG.txt
%doc doc/txt/omake-doc.txt doc/ps/omake-doc.pdf doc/html/
%{_libdir}/omake/
%{_bindir}/omake
%{_bindir}/osh
%{_bindir}/cvs_realclean


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.9.8.6-0.rc1.13
- 为 Magic 3.0 重建

* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 0.9.8.6-0.rc1.12
- 为 Magic 3.0 重建

* Tue Mar 10 2015 Liu Di <liudidi@gmail.com> - 0.9.8.6-0.rc1.11
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.9.8.6-0.rc1.10
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8.6-0.rc1.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 0.9.8.6-0.rc1.8
- OCaml 4.01.0 rebuild.
- Modernize the spec file.
- Enable debuginfo.
- Add patch to remove more warnings.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8.6-0.rc1.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8.6-0.rc1.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 10 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.8.6-0.rc1.4
- Change Debian patch to disable all compile warnings.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8.6-0.rc1.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.8.6-0.rc1.3
- Rebuild for OCaml 4.00.0.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8.6-0.rc1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8.6-0.rc1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 0.9.8.6-0.rc1
- New upstream version 0.9.8.6-0.rc1.
- Remove patches - all are upstream.
- Add patch to disable new warning in OCaml 3.12 (by Stephane Glondu).
- No separate omake-ocamldep program.

* Tue Jan  5 2010 Richard W.M. Jones <rjones@redhat.com> - 0.9.8.5-12
- Use upstream RPM 4.8 OCaml dependency generator.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.8.5-11
- Rebuild for OCaml 3.11.2.

* Thu Dec 17 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.8.5-10
- Add 'Provides: omake' (RHBZ#548536).
- Remove OCaml from the summary, since omake is not an OCaml-specific tool.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.8.5-8
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Tue Mar  3 2009 Caolán McNamara <caolanm@redhat.com> - 0.9.8.5-7
- patch src/libmojave-external/cutil/lm_printf.c rather than
  src/clib/lm_printf.c as the latter is created as a link of the
  former during the build

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.8.5-5
- Patch for "attempt to free a non-heap object" (Jakub Jelinek).

* Fri Dec  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.8.5-4
- Rebuild for OCaml 3.11.0.

* Fri May 16 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.8.5-3
- Rebuild with OCaml 3.10.2-2 (fixes bz 445545).

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.8.5-2
- Added stdin/stdout fix patch from Debian.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.8.5-1
- Initial RPM release.
