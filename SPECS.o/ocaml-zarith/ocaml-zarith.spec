%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%if !%{opt}
%global debug_package %{nil}
%endif

Name:           ocaml-zarith
Version:	1.3
Release:	2%{?dist}
Summary:        OCaml interface to GMP

# The license has a static linking exception
License:        LGPLv2 with exceptions
URL:            http://forge.ocamlcore.org/projects/zarith
Source0:        http://forge.ocamlcore.org/frs/download.php/1471/zarith-%{version}.tgz

BuildRequires:  gmp-devel
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamldoc
BuildRequires:  perl

%description
This library implements arithmetic and logical operations over
arbitrary-precision integers.  

The module is simply named "Z".  Its interface is similar to that of the
Int32, Int64 and Nativeint modules from the OCaml standard library, with
some additional functions.  See the file z.mlip for documentation.

The implementation uses GMP (the GNU Multiple Precision arithmetic
library) to compute over big integers.  However, small integers are
represented as unboxed Caml integers, to save space and improve
performance.  Big integers are allocated in the Caml heap, bypassing
GMP's memory management and achieving better GC behavior than e.g. the
MLGMP library.  Computations on small integers use a special, faster
path (coded in assembly for some platforms and functions) eschewing
calls to GMP, while computations on large integers use the low-level
MPN functions from GMP.

Arbitrary-precision integers can be compared correctly using OCaml's
polymorphic comparison operators (=, <, >, etc.).

Additional features include:
- a module Q for rationals, built on top of Z (see q.mli)
- a compatibility layer Big_int_Z that implements the same API as Big_int,
  but uses Z internally

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gmp-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n zarith-%{version}

# Fix compilation flags
sed -i "s/^asopt=''/asopt='%{optflags}'/" configure
sed -i "s/-ccopt/-g &/;s/-shared/-g &/" project.mak

%build
export CC="gcc -Wa,--noexecstack"
export CFLAGS="%{optflags}"
export OCAMLFLAGS="-g"
export OCAMLOPTFLAGS="-g"
# This is NOT an autoconf-generated configure script; %%configure doesn't work
./configure
# %%{?_smp_mflags} is not safe; same action performed by multiple CPUs
make
make doc

%install
mkdir -p %{buildroot}%{_libdir}/ocaml/stublibs
make install INSTALLDIR=%{buildroot}%{_libdir}/ocaml

%check
# bitest takes a very long time to run; enable it with caution.
export LD_LIBRARY_PATH=$PWD
make tests
%if %{opt}
./test
%else
./testb
%endif

%files
%doc LICENSE Changes
%{_libdir}/ocaml/zarith/
%if %opt
%exclude %{_libdir}/ocaml/zarith/*.a
%exclude %{_libdir}/ocaml/zarith/*.cmxa
%endif
%exclude %{_libdir}/ocaml/zarith/*.mli
%exclude %{_libdir}/ocaml/zarith/*.h
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner

%files devel
%doc README html
%if %opt
%{_libdir}/ocaml/zarith/*.a
%{_libdir}/ocaml/zarith/*.cmxa
%endif
%{_libdir}/ocaml/zarith/*.mli
%{_libdir}/ocaml/zarith/*.h

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.3-2
- 为 Magic 3.0 重建

* Sat Mar 14 2015 Liu Di <liudidi@gmail.com> - 1.3-1
- 更新到 1.3

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.2.1-8
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-6
- Remove ocaml_arches macro (RHBZ#1087794).

* Mon Mar 24 2014 Jerry James <loganjerry@gmail.com> - 1.2.1-5
- Fix bytecode build
- Build and install ocamldoc documentation
- BR ocaml-findlib instead of ocaml-findlib-devel
- The -devel subpackage needs gmp-devel for _libdir/libgmp.so
- Move zarith.h to the -devel subpackage

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-4
- Typo in changelog which confused my autorebuild scripts.

* Mon Sep 16 2013 Jerry James <loganjerry@gmail.com> - 1.2.1-3
- Rebuild for OCaml 4.01.0.
- Enable debuginfo

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Jerry James <loganjerry@gmail.com> - 1.2.1-1
- New upstream release

* Thu May 23 2013 Jerry James <loganjerry@gmail.com> - 1.2-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Jerry James <loganjerry@gmail.com> - 1.1-3
- Rebuild for OCaml 4.00.1

* Wed Oct 31 2012 Jerry James <loganjerry@gmail.com> - 1.1-2
- The -devel subpackage Requires need %%{?_isa}
- Try a different approach to keep the execstack flag off

* Fri Oct 26 2012 Jerry James <loganjerry@gmail.com> - 1.1-1
- Initial RPM
