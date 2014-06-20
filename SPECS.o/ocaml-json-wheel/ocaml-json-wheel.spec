%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-json-wheel
Version:        1.0.6
Release:        14%{?dist}
Summary:        OCaml library for parsing JSON
License:        BSD

URL:            http://martin.jambon.free.fr/json-wheel.html
Source0:        http://martin.jambon.free.fr/json-wheel-%{version}.tar.bz2

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-ocamlnet-devel
BuildRequires:  ocaml-pcre-devel
BuildRequires:  pcre-devel


%description
JSON library for OCaml following RFC 4627.

If you use this library, consider installing ocaml-json-static, the
syntax extension to the language which makes using JSON much easier.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n json-wheel-%{version}


%build
# Parallel builds don't work.
unset MAKEFLAGS
make \
%if %opt
  OCAMLOPT="ocamlopt -g"
%endif


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
mkdir -p $RPM_BUILD_ROOT%{_bindir}

make BINDIR=$RPM_BUILD_ROOT%{_bindir} install


%files
%doc LICENSE
%{_libdir}/ocaml/json-wheel
%if %opt
%exclude %{_libdir}/ocaml/json-wheel/*.a
%exclude %{_libdir}/ocaml/json-wheel/*.o
%exclude %{_libdir}/ocaml/json-wheel/*.cmxa
%exclude %{_libdir}/ocaml/json-wheel/*.cmx
%endif
%exclude %{_libdir}/ocaml/json-wheel/*.cmo
%exclude %{_libdir}/ocaml/json-wheel/*.mli
%exclude %{_libdir}/ocaml/json-wheel/*.ml
%{_bindir}/jsoncat


%files devel
%doc LICENSE Changes README html
%if %opt
%{_libdir}/ocaml/json-wheel/*.a
%{_libdir}/ocaml/json-wheel/*.o
%{_libdir}/ocaml/json-wheel/*.cmxa
%{_libdir}/ocaml/json-wheel/*.cmx
%endif
%{_libdir}/ocaml/json-wheel/*.cmo
%{_libdir}/ocaml/json-wheel/*.mli
%{_libdir}/ocaml/json-wheel/*.ml


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.6-13
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Modernize spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 1.0.6-10
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.6-8
- Rebuild for OCaml 4.00.0.

* Sun Jan 08 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.6-7
- Rebuild for OCaml 3.12.1.

* Wed Sep 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.6-5
- Bump for rebuilt ocamlnet.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.6-4
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.6-3
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.6-1
- New upstream version 1.0.6.
- Rebuild for OCaml 3.11.1.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-7
- Rebuild.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-6
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-5
- Rebuild for OCaml 3.10.2

* Wed Mar  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-4
- Remove ExcludeArch ppc64.

* Wed Mar  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3
- Don't distribute the *.cmo and *.o files.
- Better way to install jsoncat in the right directory.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-2
- Missing BR ocaml-pcre-devel.
- Missing BR pcre-devel.

* Thu Feb 28 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-1
- Initial RPM release.
