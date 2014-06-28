%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-tplib
Version:        1.3
Release:        8%{?dist}
Summary:        Tropical Polyhedra Library

License:        LGPLv2+
URL:            https://gforge.inria.fr/projects/tplib
Source0:        https://gforge.inria.fr/frs/download.php/32084/tplib-%{version}.tar.gz
# Man pages written by Jerry James using text from the sources; i.e., I
# contributed only the formatting.  Thus, the license and copyright for these
# files is the same as for the sources.
Source1:        compute_ext_rays.1
Source2:        compute_ext_rays_polar.1
Source3:        compute_halfspaces.1
Source4:        compute_minimal_external_representations.1
Source5:        compute_tangent_hypergraph.1
Source6:        compute_tropical_complex.1

BuildRequires:  ocaml
BuildRequires:  ocaml-camlidl-devel
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-zarith-devel

# This is an internal symbol that winds up in Requires, but not Provides
%global __requires_exclude ocaml\\\(Numeric_plugin\\\)

# Don't advertise the numeric plugins
%global __provides_exclude plugin

%description
TPLib computes a description by means of vertices and rays of tropical
polyhedra defined by means of inequalities, and conversely.

It also provides a numerical abstract domain based on tropical
polyhedra, in order to infer min-/max- invariants over programs.

%package devel
Summary:        Library files and headers for developing with TPLib
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

%description devel
Library files and headers for developing applications that use TPLib.

%package tools
Summary:        Tools that use TPLib
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools that use TPLib.

%prep
%setup -q -n tplib-%{version}

# Enable debuginfo generation
sed -i 's/@OCAMLBUILD@/& -cflag -g -lflag -g/' Makefile.in

%build
%configure
# Don't use %%{?_smp_mflags}; it leads to build failures
make

%install
export OCAMLFIND_DESTDIR=%{buildroot}%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
mkdir -p %{buildroot}%{_includedir}
make install bindir=%{buildroot}%{_bindir} libdir=%{buildroot}%{_libdir} \
  includedir=%{buildroot}%{_includedir}

mkdir -p %{buildroot}%{_mandir}/man1
cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} \
   %{buildroot}%{_mandir}/man1

%check
make test
_build/tests/test_tplib_double
_build/tests/test_tplib_rational

%files
%doc LICENSE README
%{_libdir}/ocaml/tplib/
%exclude %{_libdir}/ocaml/tplib/*.a
%exclude %{_libdir}/ocaml/tplib/*.cmxa
%exclude %{_libdir}/ocaml/tplib/*.mli

%files devel
%{_includedir}/tplib_*.h
%{_libdir}/*.a
%{_libdir}/ocaml/tplib/*.a
%{_libdir}/ocaml/tplib/*.cmxa
%{_libdir}/ocaml/tplib/*.mli

%files tools
%{_bindir}/*
%doc %{_mandir}/man1/*

%changelog
* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.3-8
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 18 2014 Jerry James <loganjerry@gmail.com> - 1.3-6
- Remove ocaml_arches macro (bz 1087794)
- Drop unnecessary gmp-devel BR

* Mon Sep 16 2013 Jerry James <loganjerry@gmail.com> - 1.3-5
- Rebuild for OCaml 4.01.0
- Enable debuginfo

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Jerry James <loganjerry@gmail.com> - 1.3-3
- Rebuild for ocaml-zarith 1.2.1

* Thu May 23 2013 Jerry James <loganjerry@gmail.com> - 1.3-2
- Rebuild for ocaml-zarith 1.2

* Tue Feb 19 2013 Jerry James <loganjerry@gmail.com> - 1.3-1
- New upstream release
- Upstream dropped MLGMPIDL support in favor of MLGMP, which we don't ship

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Jerry James <loganjerry@gmail.com> - 1.2-2
- Add man pages
- Don't Provide the numeric plugins
- Make -devel also Provide -static

* Wed Oct 31 2012 Jerry James <loganjerry@gmail.com> - 1.2-1
- Initial RPM
