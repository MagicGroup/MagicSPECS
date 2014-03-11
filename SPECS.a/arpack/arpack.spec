Summary: Fortran 77 subroutines for solving large scale eigenvalue problems
Summary(zh_CN.UTF-8): 求解大规模特征值问题的 Fortran 77 例程
Name: arpack
Version: 3.1.5
Release: 3%{?dist}
License: BSD
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL: http://forge.scilab.org/index.php/p/arpack-ng/
Source0: http://forge.scilab.org/upload/arpack-ng/files/arpack-ng_%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%if 0%{?rhel} == 4
# The correct dependency would be the following, but it doesn't exist on RHEL4/3
#BuildRequires: lapack-devel
BuildRequires: gcc-g77
BuildRequires: lapack
%else
BuildRequires: gcc-gfortran
BuildRequires: atlas-devel
%endif

Provides: arpack-ng = %{version}-%{release}

%description
ARPACK is a collection of Fortran 77 subroutines designed to solve large 
scale eigenvalue problems. 

The package is designed to compute a few eigenvalues and corresponding
eigenvectors of a general n by n matrix A. It is most appropriate for
large sparse or structured matrices A where structured means that a
matrix-vector product w <- Av requires order n rather than the usual
order n**2 floating point operations. This software is based upon an
algorithmic variant of the Arnoldi process called the Implicitly
Restarted Arnoldi Method (IRAM).

%description -l zh_CN.UTF-8
求解大规模特征值问题的 Fortran 77 例程。

%package devel
Summary: Files needed for developing arpack based applications
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: arpack = %{version}-%{release}
Provides: arpack-ng-devel = %{version}-%{release}

%description devel
ARPACK is a collection of Fortran 77 subroutines designed to solve
large scale eigenvalue problems. This package contains the so
library links used for building arpack based applications.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: Examples for the use of arpack
Summary(zh_CN.UTF-8): 使用 arpack 的例子
Group: Documentation
Group(zh_CN.UTF-8): 文档
%if 0%{?rhel} > 5 || 0%{?fedora} > 12
BuildArch: noarch
%endif

%description doc
This package contains examples for the use of arpack.

%description doc -l zh_CN.UTF-8
使用 arpack 的例子。

%package static
Summary: Static library for developing arpack based applications
Summary(zh_CN.UTF-8): %{name} 的静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: arpack-devel = %{version}-%{release}
Provides: arpack-ng-static = %{version}-%{release}

%description static
ARPACK is a collection of Fortran 77 subroutines designed to solve
large scale eigenvalue problems. This package contains the static
library and so links used for building arpack based applications.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%prep
%setup -q -n arpack-ng-%{version} 

%build
%{configure} --enable-shared --enable-static \
%if 0%{?rhel} == 4
 --with-blas="-lblas" --with-lapack="-llapack"
%else
 --with-blas="-L%{_libdir}/atlas -lf77blas -latlas" --with-lapack="-L%{_libdir}/atlas -llapack -latlas"
%endif
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Get rid of .la files
rm -rf %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES COPYING
%{_libdir}/libarpack.so.*

%files devel
%defattr(-,root,root,-)
%doc DOCUMENTS EXAMPLES
%{_libdir}/libarpack.so
%{_libdir}/pkgconfig/arpack.pc

%files doc
%defattr(-,root,root,-)
%doc EXAMPLES/ DOCUMENTS/

%files static
%defattr(-,root,root,-)
%{_libdir}/libarpack.a

%changelog
* Fri Feb 28 2014 Liu Di <liudidi@gmail.com> - 3.1.5-2
- 更新到 3.1.5

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 3.0.1-2
- 为 Magic 3.0 重建

* Tue Dec 13 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.0.1-1
- Change sources to arpack-ng, which provides an up-to-date version of ARPACK.
- Include examples and documentation in a new -doc package.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul  7 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 2.1-12
- Bump spec to fix update path.

* Wed Apr  7 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1-11
- Change license to BSD (see RH bugs #234191 and #578873).

* Wed Sep 24 2008 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 2.1-10
- fix libarpack.so: undefined reference to `etime_' with recent gfortran

* Mon Aug 25 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1-9
- Patch0 and %%patch make recent rpm silenty fail.

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.1-8
- fix license tag

* Wed Oct 24 2007 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 2.1-7
- apply Frederic Hecht's patch for eigenvalue bug
- move static libs to separate package

* Mon Mar 26 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1-6
- Add license and clarification note
- Add lapack support

* Thu Nov  9 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1-4
- Freshen up for submitting to fedora extras.
- Fix permissions of so file.
- Add forgotten ldconfig
- Remove dot from summaries.

* Wed Jul 16 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.
