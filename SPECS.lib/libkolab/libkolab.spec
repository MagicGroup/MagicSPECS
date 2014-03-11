%{!?php_inidir: %global php_inidir %{_sysconfdir}/php.d/}

# Filter out private python and php libs. Does not work on EPEL5,
# therefor we use it conditionally
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_provides_in %{php_extdir}/.*\.so$
%filter_setup
}

Name:           libkolab
Version:        0.4.1
Release:        3%{?dist}
Summary:        Kolab Object Handling Library

License:        LGPLv3+
URL:            http://git.kolab.org/libkolab

# From http://git.kolab.org/%{name}/snapshot/f60ac8df94c5412c26ee89c6dda3f3f32e22b275.tar.gz
Source0:        http://git.kolab.org/%{name}/snapshot/%{name}-%{version}.tar.gz

%if 0%{?rhel} > 6 || 0%{?fedora} > 16
BuildRequires:  kdepimlibs4-devel >= 4.9
%else
# Note: available within kolabsys.com infrastructure only, as being (essentially) a
# fork of various kde 4.9 libraries that depend on kde*, and that have no place in el6.
BuildRequires:  libcalendaring-devel >= 4.9
%endif
BuildRequires:  libcurl-devel
BuildRequires:  libkolabxml-devel >= 0.8
BuildRequires:  php-devel
BuildRequires:  python-devel
BuildRequires:  qt-devel

%description
The libkolab library is an advanced library to  handle Kolab objects.

%package devel
Summary:        Kolab library development headers
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} > 6 || 0%{?fedora} > 16
BuildRequires:  kdepimlibs4-devel >= 4.9
%else
# Note: available within kolabsys.com infrastructure only, as being (essentially) a
# fork of various kde 4.9 libraries that depend on kde*, and that have no place in el6.
BuildRequires:  libcalendaring-devel >= 4.9
%endif
Requires:       libkolabxml-devel >= 0.8
Requires:       php-devel
Requires:       pkgconfig
Requires:       python-devel

%description devel
Development headers for the Kolab object libraries.

%package -n php-kolab
Summary:        PHP Bindings for libkolab
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} > 5 || 0%{?fedora} > 15
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
%else
Requires:       php-api = %{php_apiver}
%endif

%description -n php-kolab
PHP Bindings for libkolab

%package -n python-kolab
Summary:        Python bindings for libkolab
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python-kolab
Python bindings for libkolab

%prep
%setup -q

%build
rm -rf build
mkdir -p build
pushd build
%{cmake} -Wno-fatal-errors -Wno-errors \
    -DINCLUDE_INSTALL_DIR=%{_includedir} \
%if 0%{?rhel} < 7 && 0%{?fedora} < 17
    -DUSE_LIBCALENDARING=ON \
%endif
    -DPHP_BINDINGS=ON \
    -DPHP_INSTALL_DIR=%{php_extdir} \
    -DPYTHON_BINDINGS=ON \
    -DPYTHON_INSTALL_DIR=%{python_sitearch} \
    ..
make
popd

%install
rm -rf %{buildroot}
pushd build
make install DESTDIR=%{buildroot}
popd

mkdir -p %{buildroot}/%{_datadir}/php
mv %{buildroot}/%{php_extdir}/*.php %{buildroot}/%{_datadir}/php/.

mkdir -p %{buildroot}/%{php_inidir}
cat >%{buildroot}/%{php_inidir}/kolab.ini <<EOF
; Kolab libraries
extension=kolabformat.so
extension=kolabshared.so
extension=kolabobject.so
extension=kolabcalendaring.so
EOF

%check
pushd build/tests
./benchmarktest || :
./calendaringtest || :
./formattest || :
./freebusytest || :
./icalendartest || :
./kcalconversiontest || :
./upgradetest || :
popd

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/%{name}.so.0
%{_libdir}/%{name}.so.%{version}

%files devel
%{_libdir}/%{name}.so
%{_libdir}/cmake/Libkolab
%{_includedir}/kolab

%files -n php-kolab
%config(noreplace) %{php_inidir}/kolab.ini
%{_datadir}/php/kolabcalendaring.php
%{php_extdir}/kolabcalendaring.so
%{_datadir}/php/kolabicalendar.php
%{php_extdir}/kolabicalendar.so
%{_datadir}/php/kolabobject.php
%{php_extdir}/kolabobject.so
%{_datadir}/php/kolabshared.php
%{php_extdir}/kolabshared.so

%files -n python-kolab
%{python_sitearch}/kolab/_calendaring.so
%{python_sitearch}/kolab/calendaring.py*
%{python_sitearch}/kolab/_icalendar.so
%{python_sitearch}/kolab/icalendar.py*
%{python_sitearch}/kolab/_shared.so*
%{python_sitearch}/kolab/shared.py*

%changelog
* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.4.1-3
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.4.1-2
- Rebuild for Boost-1.53.0

* Wed Jan  9 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4.1-1
- Update version to 0.4.1

* Tue Nov 20 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4-0.1
- New upstream release
- Correct php.d/kolab.ini

* Wed Aug 15 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3.1-3
- Fix build (patch1)
- Merge back with Fedora,
- Rebuilt for boost (Christoph Wickert, 0.3-10)

* Wed Aug  8 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3.1-1
- New upstream version 0.3.1
- Correct locations and naming of PHP bindings modules

* Thu Aug  2 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3-9
- New snapshot
- Ship PHP and Python bindings
- Conditionally build with libcalendaring
- Execute tests
- Correct installation directory for headers

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3-5
- Fix some review issues (#833853)
- Rebuild after some packaging fixes (4)

* Sat Jun  9 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3-3
- Check in latest snapshot

* Sat May 12 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3-1
- Snapshot version after buildsystem changes

* Wed May  2 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.2.0-1
- First package
