# The (empty) main package is arch, to have the package built and tests run
# on all arches, but the actual result package is the noarch -devel subpackge.
# Debuginfo packages are disabled to prevent rpmbuild from generating an empty
# debuginfo package for the empty main package.
%global debug_package %{nil}

%global commit c58038c56923

Name:           eigen3
Version:	3.2.6
Release:        5%{?dist}
Summary:        A lightweight C++ template library for vector and matrix math
Summary(zh_CN.UTF-8): 一个处理向量和矩阵数学的轻量级 C++ 模板库

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        MPLv2.0 and LGPLv2+ and BSD
URL:            http://eigen.tuxfamily.org/index.php?title=Main_Page
# Source file is at: http://bitbucket.org/eigen/eigen/get/3.1.3.tar.bz2
# Renamed source file so it's not just a version number
# Source0:        eigen-%{version}.tar.bz2
Source0:	http://bitbucket.org/eigen/eigen/get/%{version}.tar.bz2

BuildRequires:  atlas-devel
BuildRequires:  fftw-devel
BuildRequires:  glew-devel
BuildRequires:  gmp-devel
BuildRequires:  gsl-devel
BuildRequires:  mpfr-devel
BuildRequires:  sparsehash-devel
BuildRequires:  suitesparse-devel
BuildRequires:  gcc-gfortran
BuildRequires:  SuperLU-devel
BuildRequires:  qt4-devel

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  tex(latex)

%description
%{summary}.

%description -l zh_CN.UTF-8
一个线性代数用的 C++ 模板库。

%package devel
Summary:   A lightweight C++ template library for vector and matrix math
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:     Development/Libraries
Group(zh_CN.UTF-8): 开发/库
BuildArch: noarch
# -devel subpkg only atm, compat with other distros
Provides:  %{name} = %{version}-%{release}
# not *strictly* a -static pkg, but the results are the same
Provides:  %{name}-static = %{version}-%{release}
%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary:   Developer documentation for Eigen
Summary(zh_CN.UTF-8): %{name} 的文档
Requires:  %{name}-devel = %{version}-%{release}
BuildArch: noarch
%description doc
Developer documentation for Eigen.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n eigen-eigen-%{commit}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%cmake .. -DBLAS_LIBRARIES="cblas" -DSUPERLU_INCLUDES=%{_includedir}/SuperLU
popd
make -C %{_target_platform} %{?_smp_mflags}
make doc -C %{_target_platform} %{?_smp_mflags}

rm -f %{_target_platform}/doc/html/installdox
rm -f %{_target_platform}/doc/html/unsupported/installdox

%install
%make_install -C %{_target_platform}

magic_rpm_clean.sh

%check
# Run tests but make failures non-fatal. Note that upstream doesn't expect the
# tests to pass consistently since they're seeded randomly.
make -C %{_target_platform} %{?_smp_mflags} buildtests
make -C %{_target_platform} %{?_smp_mflags} test ARGS="-V" || exit 0

%files devel
%doc COPYING.README COPYING.BSD COPYING.MPL2 COPYING.LGPL
%{_includedir}/eigen3
%{_datadir}/pkgconfig/*

%files doc
%doc %{_target_platform}/doc/html

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 3.2.6-5
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 3.2.6-4
- 更新到 3.2.6

* Thu Feb 27 2014 Sandro Mani <manisandro@gmail.com> - 3.2.1-3
- Make doc package noarch

* Thu Feb 27 2014 Sandro Mani <manisandro@gmail.com> - 3.2.1-2
- Split off doc to a separate package

* Wed Feb 26 2014 Sandro Mani <manisandro@gmail.com> - 3.2.1-1
- Udpate to release 3.2.1

* Sun Aug 11 2013 Sandro Mani <manisandro@gmail.com> - 3.2-3
- Build and run tests
- Drop -DBLAS_LIBRARIES_DIR, not used
- Add some BR to enable tests of corresponding backends
- spec cleanup

* Wed Jul 24 2013 Sandro Mani <manisandro@gmail.com> - 3.2-1
- Update to release 3.2

* Sat Jun 29 2013 Rich Mattes <richmattes@gmail.com> - 3.1.3-2
- Add upstream patch to fix malloc/free bugs (rhbz#978971)

* Fri Apr 19 2013 Sandro Mani <manisandro@gmail.com> - 3.1.3-1
- Update to release 3.1.3
- Add patch for unused typedefs warning with gcc4.8

* Tue Mar 05 2013 Rich Mattes <richmattes@gmail.com> - 3.1.2-1
- Update to release 3.1.2

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 28 2012 Tim Niemueller <tim@niemueller.de> - 3.0.6-1
- Update to release 3.0.6 (fixes GCC 4.7 warnings)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 11 2012 Rich Mattes <richmattes@gmail.com> - 3.0.5-1
- Update to release 3.0.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 18 2011 Rich Mattes <richmattes@gmail.com> - 3.0.4-1
- Update to release 3.0.4

* Tue Nov 15 2011 Rich Mattes <richmattes@gmail.com> - 3.0.3-1
- Update to release 3.0.3

* Sun Apr 17 2011 Rich Mattes <richmattes@gmail.com> - 3.0.0-2
- Patched sources to fix build failure
- Removed fixes made upstream
- Added project name to source tarball filename

* Sat Mar 26 2011 Rich Mattes <richmattes@gmail.com> - 3.0.0-1
- Update to release 3.0.0

* Tue Jan 25 2011 Rich Mattes <richmattes@gmail.com> - 3.0-0.2.beta2
- Change blas-devel buildrequirement to atlas-devel
- Don't make the built-in experimental blas library

* Mon Jan 24 2011 Rich Mattes <richmattes@gmail.com> - 3.0-0.1.beta2
- Initial package
