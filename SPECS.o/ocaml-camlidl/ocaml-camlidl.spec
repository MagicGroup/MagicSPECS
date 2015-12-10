%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-camlidl
Version:        1.05
Release:        29%{?dist}
Summary:        Stub code generator and COM binding for Objective Caml
Summary(zh_CN.UTF-8): OCaml 的 COM 绑定和 Stub 代码生成器
License:        QPL and LGPLv2 with exceptions

URL:            http://caml.inria.fr/pub/old_caml_site/camlidl/
Source0:        http://caml.inria.fr/pub/old_caml_site/distrib/bazar-ocaml/camlidl-%{version}.tar.gz
Source1:        http://caml.inria.fr/pub/old_caml_site/distrib/bazar-ocaml/camlidl-%{version}.doc.pdf
# META file from Debian (RHBZ#1026991).
Source2:        META.camlidl.in

# Build the compiler into a native code program using ocamlopt.
Patch1:         camlidl-1.05-use-ocamlopt-for-compiler.patch

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml
BuildRequires:  ocaml-ocamldoc
BuildRequires:  perl


%description
CamlIDL is a stub code generator and COM binding for Objective Caml.

CamlIDL comprises two parts:

* A stub code generator that generates the C stub code required for
  the Caml/C interface, based on an MIDL specification. (MIDL stands
  for Microsoft's Interface Description Language; it looks like C
  header files with some extra annotations, plus a notion of object
  interfaces that look like C++ classes without inheritance.)

* A (currently small) library of functions and tools to import COM
  components in Caml applications, and export Caml code as COM
  components.

%description -l zh_CN.UTF-8
OCaml 的 COM 绑定和 Stub 代码生成器。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n camlidl-%{version}

%patch1 -p1

sed -e 's|^OCAMLLIB=.*|OCAMLLIB=%{_libdir}/ocaml|' \
    -e 's|^BINDIR=.*|BINDIR=%{_bindir}|' \
%if %opt
    -e 's|^OCAMLC=.*|OCAMLC=ocamlc.opt -g|' \
    -e 's|^OCAMLOPT=.*|OCAMLOPT=ocamlopt.opt -g|' \
%endif
    < config/Makefile.unix \
    > config/Makefile

%if %opt
# compiler/ contains a module called 'Array' which conflicts with the
# OCaml stdlib module (although only when using ocamlopt for some
# reason).
mv compiler/array.ml compiler/idlarray.ml
mv compiler/array.mli compiler/idlarray.mli

perl -pi.bak -e 's/array/idlarray/g' \
  compiler/Makefile compiler/.depend
perl -pi.bak -e 's/Array(?!\d)/Idlarray/g' \
  compiler/*.ml
%endif

cp %{SOURCE1} .


%build
make all


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/ocaml
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/ocaml/caml
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/ocaml/stublibs
mkdir -p $RPM_BUILD_ROOT/%{_bindir}

# Install META file (RHBZ#1026991).
sed 's/@VERSION@/%{version}/' < %{SOURCE2} > $RPM_BUILD_ROOT/%{_libdir}/ocaml/META.camlidl

make OCAMLLIB=$RPM_BUILD_ROOT/%{_libdir}/ocaml \
     BINDIR=$RPM_BUILD_ROOT/%{_bindir} \
     install
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/ocaml/*.*
%if %opt
%exclude %{_libdir}/ocaml/*.a
%exclude %{_libdir}/ocaml/*.cmxa
%endif
%{_bindir}/camlidl


%files devel
%defattr(-,root,root,-)
%doc LICENSE README Changes camlidl-%{version}.doc.pdf tests
%if %opt
%{_libdir}/ocaml/*.a
%{_libdir}/ocaml/*.cmxa
%endif
%{_libdir}/ocaml/caml/*.h


%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 1.05-29
- 为 Magic 3.0 重建

* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 1.05-28
- 为 Magic 3.0 重建

* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 1.05-27
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.05-26
- 为 Magic 3.0 重建

* Thu Mar 05 2015 Liu Di <liudidi@gmail.com> - 1.05-25
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.05-24
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov  5 2013 Richard W.M. Jones <rjones@redhat.com> - 1.05-22
- Add META file (RHBZ#1026991).

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.05-21
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Orion Poplawski <orion@cora.nwra.com> - 1.05-17
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 8 2012 Orion Poplawski <orion@cora.nwra.com> - 1.05-15
- Rebuild for OCaml 4.00.0.

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 1.05-14
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 5 2011 Orion Poplawski <orion@cora.nwra.com> - 1.05-12
- Rebuild for OCaml 3.12

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.05-11
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.05-9
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.05-7
- Rebuild for OCaml 3.11.0 release.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.05-6
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.05-5
- Rebuild for OCaml 3.10.2.

* Wed Mar  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.05-4
- Added tests subdirectory to the documentation.

* Wed Mar  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.05-3
- Removed -doc subpackage and placed documentation in -devel.

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.05-2
- Rebuild for ppc64.

* Wed Feb 20 2008 Richard W.M. Jones <rjones@redhat.com> - 1.05-1
- Initial RPM release.
