%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-ounit
Version:        1.1.2
Release:        12%{?dist}
Summary:        Unit test framework for OCaml
Summary(zh_CN.UTF-8): OCaml 的单元测试框架

License:        MIT
URL:            http://ounit.forge.ocamlcore.org/
Source0:        http://forge.ocamlcore.org/frs/download.php/886/ounit-%{version}.tar.gz
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel


%description
OUnit is a unit test framework for OCaml. It allows one to easily
create unit-tests for OCaml code. It is based on HUnit, a unit testing
framework for Haskell. It is similar to JUnit, and other xUnit testing
frameworks.

%description -l zh_CN.UTF-8
OCaml 的单元测试框架。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n ounit-%{version}
sh ./configure --destdir $RPM_BUILD_ROOT


%build
make all
make doc


%check
make test


%install
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install

# Remove this, reinstall it properly with a %%doc rule below.
rm -rf $RPM_BUILD_ROOT/usr/local/share/doc
magic_rpm_clean.sh

%files
%doc LICENSE.txt
%{_libdir}/ocaml/oUnit
%if %opt
%exclude %{_libdir}/ocaml/oUnit/*.a
%exclude %{_libdir}/ocaml/oUnit/*.cmxa
%endif
%exclude %{_libdir}/ocaml/oUnit/*.mli


%files devel
%doc LICENSE.txt README.txt
%doc _build/src/api-ounit.docdir/*
%if %opt
%{_libdir}/ocaml/oUnit/*.a
%{_libdir}/ocaml/oUnit/*.cmxa
%endif
%{_libdir}/ocaml/oUnit/*.mli


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.1.2-12
- 为 Magic 3.0 重建

* Tue Mar 10 2015 Liu Di <liudidi@gmail.com> - 1.1.2-11
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.1.2-10
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 14 2014 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-8
- Rebuild for updated Arg module (RHBZ#1065447).

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-7
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-4
- Rebuild for OCaml 4.00.1.
- Clean up the spec file.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-3
- Bump and rebuild against new OCaml 4.00.0 official release.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-1
- New upstream version 1.1.2, fixed for OCaml 4.00.0.

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-6
- Rebuild for OCaml 4.00.0.

* Mon May 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-5
- Bump release and rebuild for new OCaml on ARM.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-4
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-2
- New upstream version 1.1.0.
- Project has moved to new upstream URL and Source0.
- Rebuild for OCaml 3.12.0.
- New build system:
    + doesn't need 'make allopt'
    + DESTDIR logic changed (see OASIS bug 852)
    + docdir moved
- LICENSE and README files renamed.
- BR camlp4.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-7
- Rebuild for OCaml 3.11.2.

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

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-1
- New upstream version 1.0.3.

* Mon May 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-2
- License is MIT.

* Sat May  3 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-1
- Initial RPM release.
