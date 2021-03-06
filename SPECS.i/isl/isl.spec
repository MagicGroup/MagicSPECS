Summary: Integer point manipulation library
Summary(zh_CN.UTF-8): 整点数处理库
Name: isl
Epoch:		1
Version:	0.14
License: MIT
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://isl.gforge.inria.fr/

%global libmajor 13
%global libversion %{libmajor}.1.0

# Please set buildid below when building a private version of this rpm to
# differentiate it from the stock rpm.
#
# % global buildid .local

Release:	4%{?dist}

BuildRequires: gmp-devel
BuildRequires: pkgconfig

Source0: http://isl.gforge.inria.fr/isl-%{version}.tar.xz

%description
isl is a library for manipulating sets and relations of integer points
bounded by linear constraints.  Supported operations on sets include
intersection, union, set difference, emptiness check, convex hull,
(integer) affine hull, integer projection, computing the lexicographic
minimum using parametric integer programming, coalescing and parametric
vertex enumeration.  It also includes an ILP solver based on generalized
basis reduction, transitive closures on maps (which may encode infinite
graphs), dependence analysis and bounds on piecewise step-polynomials.

%description -l zh_CN.UTF-8
整点数处理库。

%package devel
Summary: Development for building integer point manipulation library
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: isl%{?_isa} == %{version}-%{release}
Requires: gmp-devel%{?_isa}
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description devel
isl is a library for manipulating sets and relations of integer points
bounded by linear constraints.  Supported operations on sets include
intersection, union, set difference, emptiness check, convex hull,
(integer) affine hull, integer projection, computing the lexicographic
minimum using parametric integer programming, coalescing and parametric
vertex enumeration.  It also includes an ILP solver based on generalized
basis reduction, transitive closures on maps (which may encode infinite
graphs), dependence analysis and bounds on piecewise step-polynomials.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} V=1

%install
%make_install INSTALL="install -p"
rm -f %{buildroot}/%{_libdir}/libisl.a
rm -f %{buildroot}/%{_libdir}/libisl.la
mkdir -p %{buildroot}/%{_datadir}
%global gdbprettydir %{_datadir}/gdb/auto-load/%{_libdir}
mkdir -p %{buildroot}/%{gdbprettydir}
mv %{buildroot}/%{_libdir}/*-gdb.py* %{buildroot}/%{gdbprettydir}
magic_rpm_clean.sh

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libisl.so.%{libmajor}
%{_libdir}/libisl.so.%{libversion}
%{gdbprettydir}/*
%doc AUTHORS ChangeLog LICENSE README

%files devel
%{_includedir}/*
%{_libdir}/libisl.so
%{_libdir}/pkgconfig/isl.pc
%doc doc/manual.pdf


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1:0.14-4
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1:0.14-3
- 为 Magic 3.0 重建

* Sat Sep 26 2015 Liu Di <liudidi@gmail.com> - 1:0.14-1
- 回退到 0.14

* Sun Aug 02 2015 Liu Di <liudidi@gmail.com> - 0.15-1
- 更新到 0.15

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 5 2015 David Howells <dhowells@redhat.com> - 0.14-3
- Initial packaging.
