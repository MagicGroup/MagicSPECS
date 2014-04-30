%{!?php_inidir: %global php_inidir %{_sysconfdir}/php.d/}
%{!?php_extdir: %global php_extdir %{_libdir}/php/modules}
%{!?php_apiver: %global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)}

# Filter out private python and php libs. Does not work on EPEL5,
# therefor we use it conditionally
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_provides_in %{php_extdir}/.*\.so$
%filter_setup
}

Name:           libkolab
Version:        0.5.0
Release:        1%{?dist}
Summary:        Kolab Object Handling Library

License:        LGPLv3+
URL:            http://git.kolab.org/libkolab

Source0:        http://git.kolab.org/%{name}/snapshot/libkolab-%{version}.tar.gz

# Fix #2588: kolabformatchecker uses kolab_static instead of kolab
Patch0:         libkolab-0.5.0_kolab_static.patch

BuildRequires:  cmake
%if 0%{?rhel} > 6 || 0%{?fedora} > 16
BuildRequires:  kdepimlibs-devel >= 4.9
%else
# Note: available within kolabsys.com infrastructure only, as being (essentially) a
# fork of various kde 4.9 libraries that depend on kde*, and that have no place in el6.
BuildRequires:  libcalendaring-devel >= 4.9
%endif
BuildRequires:  libcurl-devel
BuildRequires:  libkolabxml-devel >= 1.0
BuildRequires:  php >= 5.3
BuildRequires:  php-devel >= 5.3
BuildRequires:  python-devel
BuildRequires:  qt-devel

%description
The libkolab library is an advanced library to  handle Kolab objects.

%package devel
Summary:        Kolab library development headers
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} > 6 || 0%{?fedora} > 16
BuildRequires:  kdepimlibs-devel >= 4.9
%else
# Note: available within kolabsys.com infrastructure only, as being (essentially) a
# fork of various kde 4.9 libraries that depend on kde*, and that have no place in el6.
BuildRequires:  libcalendaring-devel >= 4.9
%endif
Requires:       libkolabxml-devel >= 1.0
Requires:       php-devel
Requires:       pkgconfig
Requires:       python-devel

%description devel
Development headers for the Kolab object libraries.

%package -n php-kolab
Summary:        PHP Bindings for libkolab
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
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python-kolabformat >= 1.0.0

%description -n python-kolab
Python bindings for libkolab

%prep
%setup -q -n libkolab-%{version}
%patch0 -p0

%build
mkdir -p build
pushd build
%{cmake} \
    -Wno-fatal-errors -Wno-errors \
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
make install DESTDIR=%{buildroot} -C build

mkdir -p %{buildroot}/%{_datadir}/php
mv %{buildroot}/%{php_extdir}/*.php %{buildroot}/%{_datadir}/php/.

mkdir -p %{buildroot}/%{php_inidir}
cat >%{buildroot}/%{php_inidir}/kolab.ini <<EOF
; Kolab libraries
extension=kolabobject.so
extension=kolabshared.so
extension=kolabcalendaring.so
extension=kolabicalendar.so
EOF

touch %{buildroot}/%{python_sitearch}/kolab/__init__.py

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


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libkolab.so.0
%{_libdir}/libkolab.so.%{version}

%files devel
%{_libdir}/libkolab.so
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
%dir %{python_sitearch}/kolab/
%{python_sitearch}/kolab/__init__.py*
%{python_sitearch}/kolab/_calendaring.so
%{python_sitearch}/kolab/calendaring.py*
%{python_sitearch}/kolab/_icalendar.so
%{python_sitearch}/kolab/icalendar.py*
%{python_sitearch}/kolab/_kolabobject.so*
%{python_sitearch}/kolab/kolabobject.py*
%{python_sitearch}/kolab/_shared.so*
%{python_sitearch}/kolab/shared.py*

%changelog
* Mon Oct 14 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.5.0-1
- New upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Petr Machata <pmachata@redhat.com> - 0.4.2-2
- Rebuild for boost 1.54.0

* Wed May 15 2013 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.2-1
- Update to 0.4.2
- Fix build error with cmake 2.8.11

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 0.4.1-4
- rebuild for http://fedoraproject.org/wiki/Features/Php55

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
