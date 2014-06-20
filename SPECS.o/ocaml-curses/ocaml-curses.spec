%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-curses
Version:        1.0.3
Release:        20%{?dist}
Summary:        OCaml bindings for ncurses
License:        LGPLv2+

URL:            http://savannah.nongnu.org/projects/ocaml-tmk/
Source0:        http://download.savannah.gnu.org/releases/ocaml-tmk/%{name}-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 4.00.1
BuildRequires:  ocaml-findlib-devel >= 1.3.3-3
BuildRequires:  ncurses-devel
BuildRequires:  gawk

# Doesn't include a configure script, so we have to make one.
BuildRequires:  autoconf, automake, libtool


%description
OCaml bindings for ncurses.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

# On aarch64, it is reported that ncurses-devel is not pulled in
# implicitly by ocaml (as is the case on x86-64 for some reason).  In
# any case, it is likely that people installing ocaml-curses-devel
# will desire ncurses-devel, hence:
Requires:       ncurses-devel


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q

autoreconf


%build
%configure --enable-widec
make all opt


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
ocamlfind install curses META *.cmi *.cmx *.cma *.cmxa *.a *.so *.mli


%files
%doc COPYING
%{_libdir}/ocaml/curses
%if %opt
%exclude %{_libdir}/ocaml/curses/*.a
%exclude %{_libdir}/ocaml/curses/*.cmxa
%exclude %{_libdir}/ocaml/curses/*.cmx
%endif
%exclude %{_libdir}/ocaml/curses/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc COPYING
%if %opt
%{_libdir}/ocaml/curses/*.a
%{_libdir}/ocaml/curses/*.cmxa
%{_libdir}/ocaml/curses/*.cmx
%endif
%{_libdir}/ocaml/curses/*.mli


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May  9 2014 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-19
- Add explicit requires ncurses to ocaml-curses-devel subpackage.

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-18
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-15
- BR >= OCaml 4.00.1 so we can't be built against the wrong OCaml.

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-14
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-12
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-11
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-9
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-8
- Rebuild for OCaml 3.11.2.

* Mon Oct  5 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-7
- Use ncursesw for wide character support.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-3
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-2
- Rebuild for OCaml 3.11.0

* Mon Nov 17 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-1
- Major version leap to the latest, supported, released version.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-8
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-7.20020319
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-6.20020319
- Rebuild for OCaml 3.10.1

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.1-5.20020319
- Force rebuild because of updated requires/provides scripts in OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 0.1-4.20020319
- Force rebuild because of changed BRs in base OCaml.

* Mon Aug 27 2007 Richard W.M. Jones <rjones@redhat.com> - 0.1-3.20020319
- License is LGPL 2.1 or any later version.

* Mon Aug  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.1-2.20020319
- The archive is called 'mlcurses.*'.

* Mon Aug  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.1-1.20020319
- Initial RPM release.
