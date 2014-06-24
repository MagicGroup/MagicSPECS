%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

Name:           ocaml-xmlrpc-light
Version:        0.6.1
Release:        16%{?dist}
Summary:        OCaml library for writing XML-RPC clients and servers
License:        LGPLv2 with exceptions

URL:            http://code.google.com/p/xmlrpc-light/
Source0:        http://xmlrpc-light.googlecode.com/files/xmlrpc-light-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-xml-light-devel
BuildRequires:  ocaml-ocamlnet-devel
BuildRequires:  ocaml-ocamlnet-nethttpd-devel
BuildRequires:  dos2unix

Patch1:         debian_patches_0002-Compile-with-ocamlnet-3.3.5.patch


%description
XmlRpc-Light is an XmlRpc library written in OCaml.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n xmlrpc-light-%{version}
dos2unix LICENSE
dos2unix README.txt

%patch1 -p1


%build
make


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install


%files
%doc LICENSE
%{_libdir}/ocaml/xmlrpc-light
%if %opt
%exclude %{_libdir}/ocaml/xmlrpc-light/*.a
%exclude %{_libdir}/ocaml/xmlrpc-light/*.cmxa
%endif
%exclude %{_libdir}/ocaml/xmlrpc-light/*.mli


%files devel
%doc LICENSE doc/xmlrpc-light/{html,latex} README.txt
%if %opt
%{_libdir}/ocaml/xmlrpc-light/*.a
%{_libdir}/ocaml/xmlrpc-light/*.cmxa
%endif
%{_libdir}/ocaml/xmlrpc-light/*.mli


%changelog
* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.6.1-16
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 0.6.1-14
- OCaml 4.01.0 rebuild.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 0.6.1-11
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.1-9
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.1-8
- Rebuild for OCaml 3.12.1.

* Wed Sep 21 2011 Richard W.M. Jones <rjones@redhat.com> - 0.6.1-6
- Rebuilt for updated ocamlnet.
- Apply patch from Debian to fix builds against ocamlnet 3
  (thanks Stephane Glondu).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 0.6.1-5
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.1-4
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.1-2
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Tue Mar 10 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.1-1
- New upstream version 0.6.1.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.6-5
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.6-4
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.6-3
- Rebuild for OCaml 3.10.2

* Mon Mar  3 2008 Richard W.M. Jones <rjones@redhat.com> - 0.6-2
- Added missing BR ocaml-ocamlnet-nethttpd-devel.
- Test build in mock.
- Removed ExcludeArch: ppc64.

* Sat Feb 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.6-1
- Initial RPM release.
