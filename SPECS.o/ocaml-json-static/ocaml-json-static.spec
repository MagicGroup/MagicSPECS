%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

Name:           ocaml-json-static
Version:        0.9.8
Release:        12%{?dist}
Summary:        OCaml JSON validator and converter (syntax extension)
License:        BSD

URL:            http://martin.jambon.free.fr/json-static.html
Source0:        http://martin.jambon.free.fr/json-static-%{version}.tar.bz2

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel

# Make this dependency explicit because users won't be able
# to do much useful without it, and the automatic dependency
# checking script cannot pick it up.
Requires:       ocaml-json-wheel

%global __ocaml_requires_opts -i Asttypes -i Parsetree


%description
json-static is a tool for converting parsed JSON data with an
unchecked structure into specialized OCaml types and vice-versa.
It is a complement to the json-wheel library which provides a
parser and a (pretty-) printer.


%prep
%setup -q -n json-static-%{version}


%build
make


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install


%files
%doc LICENSE README Changes yahoo.ml
%{_libdir}/ocaml/json-static


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 0.9.8-11
- Rebuild for OCaml 4.01.0.
- Modernize spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 0.9.8-8
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.8-6
- Rebuild for OCaml 4.00.0.

* Sun Jan 08 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.8-5
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 0.9.8-3
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.8-2
- Rebuild for OCaml 3.11.2.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.8-1
- New upstream version 0.9.8.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.6-9
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.6-7
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.6-6
- Rebuild for OCaml 3.11.0

* Tue Jul  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.6-5
- Ignore Asttypes & Parsetree deps.
- Bump release to -5 to avoid upgrade problems between releases.

* Mon May 12 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.6-3
- Fixed the description.

* Wed Mar  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.6-2
- Remove ExcludeArch ppc64.

* Thu Feb 28 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.6-1
- Initial RPM release.
