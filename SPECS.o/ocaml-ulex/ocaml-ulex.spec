%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

Name:           ocaml-ulex
Version:        1.1
Release:        20%{?dist}
Summary:        OCaml lexer generator for Unicode
License:        MIT

URL:            http://www.cduce.org/download.html#side
Source0:        http://www.cduce.org/download/ulex-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.0-7, ocaml-findlib-devel, ocaml-camlp4-devel
BuildRequires:  gawk

%global __ocaml_requires_opts -i Asttypes -i Parsetree

%description
Ulex is an OCaml lexer generator for Unicode

- ulex is a lexer generator.

- it is implemented as an OCaml syntax extension:
  lexer specifications are embedded in regular OCaml code.

- the lexers work with a new kind of "lexbuf" that supports Unicode;
  a single lexer can work with arbitrary encodings of the input stream.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n ulex-%{version}


%build
make all
%if %opt
make all.opt
%endif


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
make install


%files
%doc CHANGES README LICENSE
%{_libdir}/ocaml/ulex
%if %opt
%exclude %{_libdir}/ocaml/ulex/*.a
%exclude %{_libdir}/ocaml/ulex/*.cmxa
%endif
%exclude %{_libdir}/ocaml/ulex/*.mli


%files devel
%doc CHANGES README LICENSE
%if %opt
%{_libdir}/ocaml/ulex/*.a
%{_libdir}/ocaml/ulex/*.cmxa
%endif
%{_libdir}/ocaml/ulex/*.mli


%changelog
* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.1-20
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1-18
- OCaml 4.01.0 rebuild.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1-15
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1-13
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1-12
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1.1-10
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1-9
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1-7
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1-5
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1-4
- Rebuild for OCaml 3.11.0

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-3
- fix license tag

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1-2
- Rebuild for OCaml 3.10.2

* Mon Apr 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1-1
- New upstream version 1.1.
- Fixed upstream URL.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0-8
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0-7
- Rebuild for OCaml 3.10.1

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 1.0-6
- Ignore Parsetree module.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 1.0-5
- Force rebuild because of updated requires/provides scripts in OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 1.0-4
- Force rebuild because of changed BRs in base OCaml.

* Wed Jul 25 2007 Richard W.M. Jones <rjones@redhat.com> - 1.0-3
- ExcludeArch ppc64

* Wed Jul 25 2007 Richard W.M. Jones <rjones@redhat.com> - 1.0-2
- BuildRequires ocaml-camlp4

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 1.0-1
- Upstream release to match OCaml 3.10.
- Updated to latest packaging guidelines.

* Sat May 26 2007 Richard W.M. Jones <rjones@redhat.com> - 0.8-1
- Initial RPM release.
