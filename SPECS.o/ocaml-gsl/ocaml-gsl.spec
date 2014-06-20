%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-gsl
Version:        1.13.0
Release:        2%{?dist}
Summary:        Interface to GSL (GNU scientific library) for OCaml
License:        GPLv2

URL:            https://bitbucket.org/mmottl/gsl-ocaml
Source0:        https://bitbucket.org/mmottl/gsl-ocaml/downloads/gsl-ocaml-%{version}.tar.gz

ExcludeArch:    armv7hl sparc64 s390 s390x

BuildRequires:  ocaml >= 3.07
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  gsl-devel >= 1.9
BuildRequires:  /usr/bin/awk


%description
This is an interface to GSL (GNU scientific library), for the
Objective Caml language.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       /sbin/install-info


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n gsl-ocaml-%{version}


%build
make


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install


%files
%doc COPYING.txt
%{_libdir}/ocaml/gsl
%if %opt
%exclude %{_libdir}/ocaml/gsl/*.a
%exclude %{_libdir}/ocaml/gsl/*.cmxs
%exclude %{_libdir}/ocaml/gsl/*.cmxa
%endif
%exclude %{_libdir}/ocaml/gsl/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc COPYING.txt AUTHORS.txt CHANGES.txt README.md NOTES.md
%if %opt
%{_libdir}/ocaml/gsl/*.a
%{_libdir}/ocaml/gsl/*.cmxs
%{_libdir}/ocaml/gsl/*.cmxa
%endif
%{_libdir}/ocaml/gsl/*.mli


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.13.0-1
- New upstream version 1.13.0.
- Switched to Markus Mottl semi-official upstream version which is
  much livelier than the official upstream.
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Info files disappeared from upstream source, probably for the better.
- Missing BR ocamldoc.
- Missing BR ocaml-camlp4-devel.

* Sun Aug  4 2013 Richard W.M. Jones <rjones@redhat.com> - 0.6.0-19
- Exclude armv7hl (not supported by upstream C code).
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 0.6.0-16
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.0-14
- Rebuild for OCaml 4.00.0.

* Sat Jan 07 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.0-13
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 0.6.0-11
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.0-10
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.0-8
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.6.0-6
- Force rebuild.

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.6.0-5
- Rebuild.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.6.0-4
- Rebuild for OCaml 3.11.0

* Fri Apr 25 2008 Richard W.M. Jones <rjones@redhat.com> - 0.6.0-3
- Fixed typo in description.
- Mixed use of buildroot macro / RPM_BUILD_ROOT variable fixed.
- Remove BR gsl (brought in by gsl-devel, so unnecessary).

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.6.0-2
- Rebuild for ppc64.

* Wed Feb 20 2008 Richard W.M. Jones <rjones@redhat.com> - 0.6.0-1
- Initial RPM release.
