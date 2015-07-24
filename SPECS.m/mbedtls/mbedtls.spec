%if 0%{?fedora} || 0%{?rhel} >= 7
%global _docdir_fmt %{name}
%endif

Name: mbedtls
Version: 1.3.11
Release: 2%{?dist}
Summary: Light-weight cryptographic and SSL/TLS library
Group: System Environment/Libraries
License: GPLv2+ with exceptions
URL: https://tls.mbed.org/
Source0: https://tls.mbed.org/download/%{name}-%{version}-gpl.tgz

BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: graphviz

%if 0%{?rhel} == 5
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif

# replace polarssl with mbedtls

Obsoletes: polarssl < 1.3.10
Provides:  polarssl = %{version}-%{release}

%description
Mbed TLS is a light-weight open source cryptographic and SSL/TLS
library written in C. Mbed TLS makes it easy for developers to include
cryptographic and SSL/TLS capabilities in their (embedded)
applications with as little hassle as possible.
FOSS License Exception: https://tls.mbed.org/foss-license-exception

%package        utils
Summary:        Utilities for %{name}
Group:          Applications/System
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      polarssl-utils < 1.3.10
Provides:       polarssl-utils = %{version}-%{release}

%description    utils
Cryptographic utilities based on %{name}. 

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      polarssl-devel < 1.3.10
Provides:       polarssl-devel = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        static
Summary:        Static files for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    static
The %{name}-static package contains static files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
Group:          Documentation
%if 0%{?fedora} || 0%{?rhel} >= 6
BuildArch:      noarch
%endif

%description    doc
The %{name}-doc package contains documentation.

%prep
%setup -q

%if 0%{?rhel} == 5
sed -e 's/-Wlogical-op//' -i CMakeLists.txt
%endif

%build
%cmake -D CMAKE_BUILD_TYPE:String="Release" -D USE_SHARED_MBEDTLS_LIBRARY:BOOL=1 .
make %{?_smp_mflags} all apidoc

%install
%if 0%{?fedora} || 0%{?rhel} >= 6
%make_install
%else
make DESTDIR=$RPM_BUILD_ROOT install
%endif
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
mv $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_libexecdir}/mbedtls

%check
LD_LIBRARY_PATH=$PWD/library ctest --output-on-failure -V

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc ChangeLog
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/*.so.*

%files utils
%{_libexecdir}/%{name}/

%files devel
%{_includedir}/polarssl/
%{_libdir}/*.so

%files static
%{_libdir}/*.a

%files doc
%doc apidoc/*

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Morten Stevens <mstevens@imt-systems.com> - 1.3.11-1
- Update to 1.3.11

* Mon Jun 01 2015 Robert Scheck <robert@fedoraproject.org> - 1.3.10-2
- Spec file changes to cover Red Hat Enterprise Linux 5 and 6

* Thu May 14 2015 Morten Stevens <mstevens@imt-systems.com> - 1.3.10-1
- Initial Fedora Package
- Added subpackage for documentation files
- Added subpackage for static files
