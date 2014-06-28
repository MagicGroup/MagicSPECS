
%{?!mono_arches: %global mono_arches %{ix86} x86_64 sparc sparcv9 ia64 %{arm} alpha s390x ppc ppc64}

%ifarch %{mono_arches}
# No linux system is actually using the csharp bindings
%global with_csharp 0
%endif
%global with_java 1
%global with_php 1
%global with_python 1

%if 0%{?with_php} > 0
%{!?php_extdir: %global php_extdir %{_libdir}/php/modules}
%{!?php_inidir: %global php_inidir %{_sysconfdir}/php.d/}
%{!?php_apiver: %global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)}
%endif

%if 0%{?with_python} > 0
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

# Filter out private python and php libs. Does not work on EPEL5,
# therefor we use it conditionally
%if 0%{?with_php} > 0
%if 0%{?with_python} > 0
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_provides_in %{php_extdir}/.*\.so$
%filter_setup
}
%else
%{?filter_setup:
%filter_provides_in %{php_extdir}/.*\.so$
%filter_setup
}
%endif
%else
%if 0%{?with_python} > 0
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}
%endif
%endif

Name:           libkolabxml
Version:        1.0.1
Release:        7%{?dist}
Summary:        Kolab XML format collection parser library

Group:          System Environment/Libraries
License:        LGPLv3+
URL:            http://www.kolab.org

Source0:        http://git.kolab.org/libkolabxml/snapshot/libkolabxml-%{version}.tar.gz

# Fix #2576 csharp bindings not building
Patch0:         libkolabxml-1.0.1_csharp_bindings.patch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  boost-devel
BuildRequires:  cmake >= 2.6
BuildRequires:  e2fsprogs-devel
BuildRequires:  gcc-c++
%if 0%{?rhel} > 6 || 0%{?fedora} >= 16
BuildRequires:  kdelibs4-devel
BuildRequires:  kdepimlibs4-devel
%endif
BuildRequires:  libcurl-devel
BuildRequires:  qt-devel >= 3
BuildRequires:  swig
BuildRequires:  uuid-devel
BuildRequires:  xerces-c-devel
BuildRequires:  xsd

%if 0%{?with_csharp} < 1
Obsoletes:      csharp-kolabformat < %{version}-%{release}
#Provides:       csharp-kolabformat = %{version}-%{release}
%endif

%if 0%{?with_java} < 1
Obsoletes:      java-kolabformat < %{version}-%{release}
#Provides:       java-kolabformat = %{version}-%{release}
%endif

%if 0%{?with_php} < 1
Obsoletes:      php-kolabformat < %{version}-%{release}
#Provides:       php-kolabformat = %{version}-%{release}
%endif

%if 0%{?with_python} < 1
Obsoletes:      python-kolabformat < %{version}-%{release}
#Provides:       python-kolabformat = %{version}-%{release}
%endif

%description
The libkolabxml parsing library interprets Kolab XML formats (xCal, xCard)
with bindings for Python, PHP and other languages. The language bindings
are available through sub-packages.

%package devel
Summary:        Kolab XML library development headers
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       boost-devel
Requires:       cmake >= 2.6
Requires:       e2fsprogs-devel
Requires:       gcc-c++
%if 0%{?rhel} > 6 || 0%{?fedora} >= 16
Requires:       kdelibs4-devel
Requires:       kdepimlibs4-devel
%endif
Requires:       libcurl-devel
%if 0%{?with_php} > 0
Requires:       php-devel >= 5.3
%endif
%if 0%{?with_python} > 0
Requires:       python-devel
%endif
Requires:       qt-devel >= 3
Requires:       swig
Requires:       uuid-devel
Requires:       xerces-c-devel
Requires:       xsd

%description devel
Development headers for the Kolab XML libraries.

%if 0%{?with_csharp} > 0
%package -n csharp-kolabformat
Summary:        C# Bindings for libkolabxml
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  mono-core

%description -n csharp-kolabformat
C# bindings for libkolabxml
%endif

%if 0%{?with_java} > 0
%package -n java-kolabformat
Summary:        Java Bindings for libkolabxml
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n java-kolabformat
Java bindings for libkolabxml
%endif

%if 0%{?with_php} > 0
%package -n php-kolabformat
Summary:        PHP bindings for libkolabxml
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} > 5 || 0%{?fedora} > 15
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
%else
Requires:       php-api = %{php_apiver}
%endif
BuildRequires:  php >= 5.3
BuildRequires:  php-devel >= 5.3

%description -n php-kolabformat
The PHP kolabformat package offers a comprehensible PHP library using the
bindings provided through libkolabxml.
%endif

%if 0%{?with_python} > 0
%package -n python-kolabformat
Summary:        Python bindings for libkolabxml
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  python-devel

%description -n python-kolabformat
The PyKolab format package offers a comprehensive Python library using the
bindings provided through libkolabxml.
%endif

%prep
%setup -q -n libkolabxml-%{version}
%patch0 -p1

%build
mkdir -p build
pushd build
%cmake \
    -Wno-fatal-errors -Wno-errors \
    -DCMAKE_SKIP_RPATH=ON \
    -DCMAKE_PREFIX_PATH=%{_libdir} \
%if 0%{?rhel} < 6 && 0%{?fedora} < 15
    -DBOOST_LIBRARYDIR=%{_libdir}/boost141 \
    -DBOOST_INCLUDEDIR=%{_includedir}/boost141 \
    -DBoost_ADDITIONAL_VERSIONS="1.41;1.41.0" \
%endif
    -DINCLUDE_INSTALL_DIR=%{_includedir} \
%if 0%{?with_csharp} > 0
    -DCSHARP_BINDINGS=ON \
    -DCSHARP_INSTALL_DIR=%{_datadir}/%{name}/csharp/ \
%endif
%if 0%{?with_java} > 0
    -DJAVA_BINDINGS=ON \
    -DJAVA_INSTALL_DIR=%{_datadir}/%{name}/java/ \
%endif
%if 0%{?with_php} > 0
    -DPHP_BINDINGS=ON \
    -DPHP_INSTALL_DIR=%{php_extdir} \
%endif
%if 0%{?with_python} > 0
    -DPYTHON_BINDINGS=ON \
    -DPYTHON_INCLUDE_DIRS=%{python_include} \
    -DPYTHON_INSTALL_DIR=%{python_sitearch} \
%endif
    ..
make
popd

%install
pushd build
make install DESTDIR=%{buildroot} INSTALL='install -p'
popd

%if 0%{?with_php} > 0
mkdir -p \
    %{buildroot}/%{_datadir}/php \
    %{buildroot}/%{php_inidir}/
mv %{buildroot}/%{php_extdir}/kolabformat.php %{buildroot}/%{_datadir}/php/kolabformat.php
cat > %{buildroot}/%{php_inidir}/kolabformat.ini << EOF
extension=kolabformat.so
EOF
%endif

%check
pushd build
# Make sure libkolabxml.so.* is found, otherwise the tests fail
export LD_LIBRARY_PATH=$( pwd )/src/
pushd tests
./bindingstest ||:
./conversiontest ||:
./parsingtest ||:
popd
%if 0%{?with_php} > 0
php -d enable_dl=On -dextension=src/php/kolabformat.so src/php/test.php ||:
%endif
%if 0%{?with_python} > 0
python src/python/test.py ||:
%endif
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc DEVELOPMENT NEWS README
%{_libdir}/*.so.*

%files devel
%{_includedir}/kolabxml
%{_libdir}/*.so
%{_libdir}/cmake/Libkolabxml

%if 0%{?with_csharp} > 0
%files -n csharp-kolabformat
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/csharp
%endif

%if 0%{?with_java} > 0
%files -n java-kolabformat
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/java
%endif

%if 0%{?with_php} > 0
%files -n php-kolabformat
%{_datadir}/php/kolabformat.php
%{php_extdir}/kolabformat.so
%config(noreplace) %{php_inidir}/kolabformat.ini
%endif

%if 0%{?with_python} > 0
%files -n python-kolabformat
%{python_sitearch}/kolabformat.py*
%{python_sitearch}/_kolabformat.so
%endif

%changelog
* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 1.0.1-7
- 为 Magic 3.0 重建

* Fri May 02 2014 Liu Di <liudidi@gmail.com> - 1.0.1-6
- 为 Magic 3.0 重建

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 1.0.1-5
- 为 Magic 3.0 重建

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 1.0.1-4
- 为 Magic 3.0 重建

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 1.0.1-3
- 为 Magic 3.0 重建

* Mon Jan 13 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0.1-2
- Require php-kolab for php-kolabformat, and void
  /etc/php.d/kolabformat.ini (#2667)

* Wed Oct 30 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0.1-1
- New upstream release

* Mon Oct 14 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0.0-1
- New upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 0.8.4-2
- Rebuild for boost 1.54.0

* Fri Apr 12 2013 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.4-1
- Update to 0.8.4

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 0.8.3-2
- rebuild for http://fedoraproject.org/wiki/Features/Php55

* Tue Feb 26 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.8.3-1
- New upstream release with file format handling

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.8.1-4
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.8.1-3
- Rebuild for Boost-1.53.0

* Wed Aug 22 2012 Dan Horák <dan[at]danny.cz> - 0.8.1-2
- build csharp subpackage only when Mono exists

* Wed Aug 15 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.8.1-1
- New upstream version 0.8.1
- Revert s/qt-devel/qt4-devel/ - just require the latest qt-devel
- Revert s/kdelibs-devel/kdelibs4-devel/ - also require the latest
  kdelibs (frameworks FTW!)

* Sun Aug 12 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.7.0-3
- drop BR: gcc-c++
- s/qt-devel/qt4-devel/ s/kdelibs-devel/kdelibs4-devel/
- fix build against boost-1.50

* Wed Jul 25 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.7.0-2
- Fix build on ppc64
- New upstream version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.6.0-3
- Correct dependency on php

* Tue Jun 26 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.6.0-2
- Also remove xsd-utils requirement for -devel sub-package

* Mon Jun 25 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.6.0-1
- Actual 0.6.0 release

* Sat Jun 23 2012 Christoph Wickert <wickert@kolabsys.com> - 0.6-1
- Update to 0.6 final
- Run ldconfig in %%post and %%postun
- Mark kolabformat.ini as config file
- Export LD_LIBRARY_PATH so tests can be run in %%check
- Add php dependencies to php-kolabformat package
- Make base package requirements are arch-specific
- Filter unwanted provides of php-kolabformat and python-kolabformat

* Wed Jun 20 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.6-0.4
- Some other cleanups to prevent review scrutiny from blocking
  inclusion
- Drop build requirement for xsd-utils

* Sat Jun  9 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.6-0.2
- Git snapshot release

* Wed May 23 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.5-5
- Correct use of Python keyword None
- Snapshot version with attendee cutype support

* Tue May 22 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.5-3
- Snapshot version with attendee delegation support

* Sat May 12 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.5-2
- Snapshot version with build system changes

* Wed May  9 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4.0-3
- Fix PHP kolabformat module packaging

* Wed May  2 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4.0-2
- New version

* Fri Apr 20 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3.0-1
- New version

* Mon Apr  9 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3-0.1
- First package

