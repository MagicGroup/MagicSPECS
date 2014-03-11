Name:           eigen3
Version:        3.0.4
Release:        3%{?dist}
Summary:        A lightweight C++ template library for vector and matrix math

Group:          Development/Libraries
License:        LGPLv3+ or GPLv2+
URL:            http://eigen.tuxfamily.org/index.php?title=Main_Page
# Source file is at: http://bitbucket.org/eigen/eigen/get/3.0.3.tar.bz2
# Renamed source file so it's not just a version number
Source0:        eigen-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# Fixes build by adding the cstdef to a source file.
# Not yet submitted upstream
Patch0:         eigen-3.0.0.ptrdiff.patch

BuildRequires:  atlas-devel
BuildRequires:  fftw-devel
BuildRequires:  glew-devel
BuildRequires:  gmp-devel
BuildRequires:  gsl-devel
BuildRequires:  mpfr-devel
BuildRequires:  sparsehash-devel
BuildRequires:  suitesparse-devel

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  tex(latex)

%description
%{summary}

%package devel
Summary: A lightweight C++ template library for vector and matrix math
Group:   Development/Libraries
# -devel subpkg only atm, compat with other distros
Provides: %{name} = %{version}-%{release}
# not *strictly* a -static pkg, but the results are the same
Provides: %{name}-static = %{version}-%{release}
%description devel
%{summary}

%prep
%setup -q -n eigen-eigen-%{version}
%patch0 -p0

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%cmake .. -DBLAS_LIBRARIES="cblas" -DBLAS_LIBRARIES_DIR=%{_libdir}/atlas
popd
make -C %{_target_platform} %{?_smp_mflags}
make doc -C %{_target_platform} %{?_smp_mflags}

rm -f %{_target_platform}/doc/html/installdox
rm -f %{_target_platform}/doc/html/unsupported/installdox

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}

%clean
rm -rf %{buildroot}

%files devel
%defattr(-,root,root,-)
%doc COPYING.GPL COPYING.LGPL
%doc %{_target_platform}/doc/html
%{_includedir}/eigen3
%{_datadir}/pkgconfig/*

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 3.0.4-3
- 为 Magic 3.0 重建

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
