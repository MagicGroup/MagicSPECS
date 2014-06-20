%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-augeas
Version:        0.5
Release:        7%{?dist}
Summary:        OCaml bindings for Augeas configuration API
License:        LGPLv2+ with exceptions

URL:            http://people.redhat.com/~rjones/augeas/files/
Source0:        http://people.redhat.com/~rjones/augeas/files/%{name}-%{version}.tar.gz

Patch1:         ocaml-augeas-0.5-use-ocamlopt-g.patch

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.09.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  augeas-devel >= 0.1.0
BuildRequires:  chrpath


%description
Augeas is a unified system for editing arbitrary configuration
files. This provides complete OCaml bindings for Augeas.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q
%patch1 -p1


%build
%configure
make
make doc


%check
make check


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs

# The upstream 'make install' rule is missing '*.so' and distributes
# '*.cmi' instead of just the augeas.cmi file.  Temporary fix:
#make install
ocamlfind install augeas META *.mli *.cmx *.cma *.cmxa *.a augeas.cmi *.so

chrpath --delete $OCAMLFIND_DESTDIR/stublibs/dll*.so


%files
%doc COPYING.LIB
%{_libdir}/ocaml/augeas
%if %opt
%exclude %{_libdir}/ocaml/augeas/*.a
%exclude %{_libdir}/ocaml/augeas/*.cmxa
%exclude %{_libdir}/ocaml/augeas/*.cmx
%endif
%exclude %{_libdir}/ocaml/augeas/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc html
%if %opt
%{_libdir}/ocaml/augeas/*.a
%{_libdir}/ocaml/augeas/*.cmxa
%{_libdir}/ocaml/augeas/*.cmx
%endif
%{_libdir}/ocaml/augeas/*.mli


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 0.5-6
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 0.5-3
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 0.5-1
- New upstream version 0.5.
- Update URLs.
- Add check section.
- Bring spec file up to modern standards.

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4-11
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4-10
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 0.4-8
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.4-7
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.4-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4-3
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4-2
- Rebuild for OCaml 3.11.0

* Wed May  7 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4-1
- Initial RPM release.
