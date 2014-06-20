%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

Name:           ocaml-pa-monad
Version:        6.0
Release:        14%{?dist}
Summary:        OCaml syntax extension for monads
License:        LGPLv2+ with exceptions

URL:            http://www.cas.mcmaster.ca/~carette/pa_monad/
Source0:        http://www.cas.mcmaster.ca/~carette/pa_monad/pa_monad.tar.gz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel

%global __ocaml_requires_opts -i Asttypes -i Parsetree


%description
This Camlp4 parser adds some syntactic sugar to beautify monadic
expressions.  The name of the syntax extension is a bit misleading as
it does not provide any monad nor monadic computation.


%prep
%setup -q -c


%build
make all doc


%check
make test


%install
# These rules work if the library uses 'ocamlfind install' to install itself.
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make findlib-install


%files
%doc COPYING README ChangeLog html-doc
%{_libdir}/ocaml/monad


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 6.0-13
- OCaml 4.01.0 rebuild.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 6.0-10
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 6.0-8
- Rebuild for OCaml 4.00.0.

* Sat Jan 07 2012 Richard W.M. Jones <rjones@redhat.com> - 6.0-7
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 6.0-5
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 6.0-4
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 6.0-2
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Tue Mar 10 2009 Richard W.M. Jones <rjones@redhat.com> - 6.0-1
- New upstream version 6.0 [sic].
- Patch no longer required, now upstream.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-7
- Remove -warn-error which caused tests to fail.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-6
- Rebuild for OCaml 3.11.0

* Tue Jul  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-5
- Ignore Asttypes & Parsetree deps.
- Bump release to avoid EVR problems across branches.

* Mon May 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-3
- Added a check section.

* Wed Mar  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-2
- Remove ExcludeArch ppc64.

* Thu Feb 28 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-1
- Initial RPM release.
