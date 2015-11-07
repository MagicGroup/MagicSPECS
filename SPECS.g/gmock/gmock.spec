Summary:        Google C++ Mocking Framework
Summary(zh_CN.UTF-8): Google C++ Mock 框架
Name:           gmock
Version:        1.7.0
Release:        2%{?dist}
License:        BSD
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:            http://code.google.com/p/googlemock/
Source0:        http://googlemock.googlecode.com/files/gmock-%{version}.zip
Patch0:		gmock-1.6.0-enable-install.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  gtest-devel >= 1.5.0
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  python
Requires:       gtest >= 1.5.0

%description
Inspired by jMock, EasyMock, and Hamcrest, and designed with C++'s
specifics in mind, Google C++ Mocking Framework (or Google Mock for
short) is a library for writing and using C++ mock classes.

Google Mock:

 o lets you create mock classes trivially using simple macros,
 o supports a rich set of matchers and actions,
 o handles unordered, partially ordered, or completely ordered
   expectations,
 o is extensible by users, and
 o works on Linux, Mac OS X, Windows, Windows Mobile, minGW, and
   Symbian.

%description -l zh_CN.UTF-8
Google C++ Mock 框架。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains development files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package -n gtest
Summary:        Google C++ testing framework
Summary(zh_CN.UTF-8): Google C++ 测试框架
Group:          Development/Tools
Summary(zh_CN.UTF-8): 开发/工具

%description -n gtest
Google's framework for writing C++ tests on a variety of platforms
(GNU/Linux, Mac OS X, Windows, Windows CE, and Symbian). Based on the
xUnit architecture. Supports automatic test discovery, a rich set of
assertions, user-defined assertions, death tests, fatal and non-fatal
failures, various options for running the tests, and XML test report
generation.

%description -n gtest -l zh_CN.UTF-8
Google C++ 测试框架。

%package -n     gtest-devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): gtest 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       automake
Requires:       %{name} = %{version}-%{release}

%description  -n gtest-devel
This package contains development files for %{name}.

%description -n gtest-devel -l zh_CN.UTF-8
gtest 的开发包。

%prep
%setup -q
%patch0 -p1
# Only acx_pthread.m4 needed from gtest, 
# save the rest for use in make check
#mv gtest gtest.rpmbuild
#install -D -p -m 0644 gtest.rpmbuild/m4/acx_pthread.m4 \
#    gtest/m4/acx_pthread.m4 

%build
# needed for mahe check to work without failures
autoreconf -fsvi     
%configure --disable-static #--without-gtest
# Omit unused direct shared library dependencies and rpaths
sed -i -e 's| -shared | -Wl,--as-needed\0|g' libtool
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install INSTALL="%{__install} -p" DESTDIR=%{buildroot}
find %{buildroot} -type f -name "*.la" -delete

%check
# restore gtest for make check to work
#rm -rf gtest
#mv gtest.rpmbuild gtest
make check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc CHANGES CONTRIBUTORS README
%{_libdir}/libgmock.so.*
%{_libdir}/libgmock_main.so.*

%files -n gtest
%defattr(-, root, root, -)
%{_libdir}/libgtest.so.*
%{_libdir}/libgtest_main.so.*

%files devel
%defattr(-, root, root, -)
#%{_bindir}/gmock-config
#%{_bindir}/gmock_doctor.py
%{_libdir}/libgmock.so
%{_libdir}/libgmock_main.so
%{_includedir}/gmock

%files -n gtest-devel
%defattr(-, root, root, -)
%{_includedir}/gtest
%{_libdir}/libgtest.so
%{_libdir}/libgtest_main.so
%{_datadir}/aclocal/gtest.m4

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.7.0-2
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jan 12 2011 Terje Rosten <terje.rosten@ntnu.no> - 1.5.0-1
- 1.5.0
- req gtest 1.5.0
- fix description
- fix group
- fix files section
- remove name macro
- rpmlint error free
- don't build with bundled gtest
- make check works
- add some buildreqs

* Sun Oct 4 2009 Tejas Dinkar <tejas@gja.in> - 1.4.0-1
- Initial gmock 1.4.0
