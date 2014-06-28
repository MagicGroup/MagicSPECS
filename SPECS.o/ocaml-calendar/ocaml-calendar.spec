%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-calendar
Version:        2.03.2
Release:        7%{?dist}
Summary:        Objective Caml library for managing dates and times
License:        LGPLv2

URL:            http://calendar.forge.ocamlcore.org/
Source0:        http://forge.ocamlcore.org/frs/download.php/915/calendar-2.03.2.tar.gz

Patch1:         calendar-2.03.2-enable-debug.patch

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 4.00.1
BuildRequires:  ocaml-findlib-devel >= 1.3.3-3
BuildRequires:  ocaml-ocamldoc
BuildRequires:  gawk

# Ignore all generated modules *except* CalendarLib, since everything
# now appears in that namespace.
%global __ocaml_requires_opts -i Calendar_builder -i Calendar_sig -i Date -i Date_sig -i Fcalendar -i Ftime -i Period -i Printer -i Time -i Time_sig -i Time_Zone -i Utils -i Version
%global __ocaml_provides_opts -i Calendar_builder -i Calendar_sig -i Date -i Date_sig -i Fcalendar -i Ftime -i Period -i Printer -i Time -i Time_sig -i Time_Zone -i Utils -i Version


%description
Objective Caml library for managing dates and times.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n calendar-%{version}
%patch1 -p1


%build
./configure --libdir=%{_libdir}
make
make doc

mv TODO TODO.old
iconv -f iso-8859-1 -t utf-8 < TODO.old > TODO


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install


%files
%doc CHANGES README TODO LGPL COPYING
%{_libdir}/ocaml/calendar
%if %opt
%exclude %{_libdir}/ocaml/calendar/*.cmx
%endif
%exclude %{_libdir}/ocaml/calendar/*.mli


%files devel
%doc CHANGES README TODO LGPL COPYING calendarFAQ-2.6.txt doc/*
%if %opt
%{_libdir}/ocaml/calendar/*.cmx
%endif
%{_libdir}/ocaml/calendar/*.mli


%changelog
* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 2.03.2-7
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 2.03.2-5
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 2.03.2-2
- BR >= OCaml 4.00.1 so we can't be built against the wrong OCaml.

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 2.03.2-1
- New upstream version 2.03.2.
- Rebuild for OCaml 4.00.1.
- Remove upstream patch.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 2.03.1-4
- Rebuild for OCaml 4.00.0.

* Sat Apr 28 2012 Richard W.M. Jones <rjones@redhat.com> - 2.03.1-2
- Bump and rebuild against new OCaml compiler in ARM.

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 2.03.1-1
- New upstream version 2.03.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 2.03-1
- New upstream version 2.03.
- Rebuild for OCaml 3.12.0.
- Remove META file patch, now upstream.

* Tue Jan 12 2010 Richard W.M. Jones <rjones@redhat.com> - 2.01.1-5
- Replace %%define with %%global.
- Use upstream RPM 4.8 OCaml dependency generator.
- Suppress bogus requires as well as provides.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 2.01.1-3
- Rebuild for OCaml 3.11.2.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 2.01.1-2
- New upstream release 2.01.1.
- Patch META file so it doesn't include the library twice.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.0.4-6
- Calendar has a new upstream URL.

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.0.4-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 2.0.4-3
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 2.0.4-2
- Rebuild for OCaml 3.11.0

* Thu Jul 10 2008 Richard W.M. Jones <rjones@redhat.com> - 2.0.4-1
- New upstream version 2.0.4 (rhbz #454789).
- Fix non-UTF-8 characters in TODO.
- *.cmx file moved to -devel subpackage as per packaging guidelines.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 2.0.2-2
- Rebuild for OCaml 3.10.2

* Fri Mar 28 2008 Richard W.M. Jones <rjones@redhat.com> - 2.0.2-1
- New upstream version 2.0.2 (rhbz #439124)

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 2.0-2
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 2.0-1
- New upstream version 2.0.
- Rebuild for OCaml 3.10.1.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 1.10-9
- Force rebuild because of updated requires/provides scripts in OCaml.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 1.10-8
- Force rebuild because of base OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 1.10-7
- Force rebuild because of changed BRs in base OCaml.

* Tue Aug  7 2007 Richard W.M. Jones <rjones@redhat.com> - 1.10-6
- ExcludeArch ppc64
- Clarify license is LGPLv2
- Add LGPL, COPYING, calendarFAQ-2.6.txt and doc/ subdirectory to docs.
- BR +ocaml-ocamldoc

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 1.10-5
- Updated to latest packaging guidelines.

* Sat Jun  2 2007 Richard W.M. Jones <rjones@redhat.com> - 1.10-4
- Handle bytecode-only architectures.

* Tue May 29 2007 Richard W.M. Jones <rjones@redhat.com> - 1.10-3
- Remove Debian DISTDIR patch.

* Fri May 25 2007 Richard W.M. Jones <rjones@redhat.com> - 1.10-2
- Added find-requires and find-provides.

* Fri May 18 2007 Richard W.M. Jones <rjones@redhat.com> - 1.10-1
- Initial RPM release.

