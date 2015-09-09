
%global snap0 20150318
%global commit0 d0f62e65f0b79fb7724d8d551dc9ff11d085127b
#global gittag0 GIT-TAG
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           qjson
Version:        0.8.1
Release:        11.%{snap0}.%{shortcommit0}git%{?dist}
Summary:        A qt-based library that maps JSON data to QVariant objects

License:        GPLv2+
URL:            http://sourceforge.net/projects/qjson/
#if 0%{?commit0}
Source0:        https://github.com/flavio/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
#else
#Source0:        http://sourceforge.net/projects/%{name}/files/qjson/%{version}/%{name}-%{version}.tar.bz2
#endif

BuildRequires:  cmake >= 2.8.8
BuildRequires:  doxygen
BuildRequires:  pkgconfig(QtCore)

# %%check
BuildRequires: xorg-x11-server-Xvfb

%description
JSON is a lightweight data-interchange format. It can represents integer, real
number, string, an ordered sequence of value, and a collection of
name/value pairs.QJson is a qt-based library that maps JSON data to
QVariant objects.

%package devel
Summary:  Development files for qjson
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
The %{name}-devel package contains the libraries and header files required for
developing applications that use %{name}.


%prep
%setup -q %{?commit0:-n %{name}-%{commit0}}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake} .. \
  -DQJSON_BUILD_TESTS:BOOL=ON \
  -DQT4_BUILD:BOOL=ON
popd

# build docs
pushd doc
doxygen
popd


%install
make install DESTDIR=%{buildroot} -C %{_target_platform}


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion QJson)" = "%{version}"
export CTEST_OUTPUT_ON_FAILURE=1
xvfb-run -a make test -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING.lib
%doc README.md README.license
%{_libdir}/libqjson.so.%{version}
%{_libdir}/libqjson.so.0*

%files devel
%doc doc/html
%{_includedir}/qjson/
%{_libdir}/libqjson.so
%{_libdir}/pkgconfig/QJson.pc
%dir %{_libdir}/cmake
%{_libdir}/cmake/qjson/


%changelog
* Mon Aug 03 2015 Rex Dieter <rdieter@fedoraproject.org> 0.8.1-11.20150318.d0f62e6git
- 20150318 snapshot

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.8.1-9
- Rebuilt for GCC 5 C++11 ABI change

* Thu Feb 19 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.8.1-8
- rebuild (gcc5)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec 13 2013 Rex Dieter <rdieter@fedoraproject.org> 0.8.1-5
- %%check: CTEST_OUTPUT_ON_FAILURE

* Thu Aug 22 2013 Rex Dieter <rdieter@fedoraproject.org> 0.8.1-4
- .spec cleanup

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Rex Dieter <rdieter@fedoraproject.org> 0.8.1-1
- 0.8.1

* Fri Nov 23 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.8.0-2
- %%files: track soname
- -devel: own %%_libdir/cmake

* Thu Nov 22 2012 Jan Grulich <jgrulich@redhat.com> - 0.8.0-1
- 0.8.0

* Thu Aug 09 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.7.1-9
- rebuild

* Sat Jul 21 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.7.1-8
- skip stripping some compiler flags (undocumented)
- %%files: track files closer (lib soname in particular)
- -devel: avoid dep on cmake 
- %%check: +make test, pkgconfig check

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-6
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.7.1-3
- Rebuilt for gcc bug 634757

* Sun Sep 12 2010 Eli Wapniarski <eli@orbsky.homelinux.org> 0.7.1-2
-0.7.1
- Fixed dependancy issue

* Sat Dec 12 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.7.1-1
-0.7.1
- Version upgrade
- Fixed doxygen documentation (Thanks again Orcan)

* Tue Dec 8 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.6.3-6
-0.6.3
- Fixed capitalization of the summary 

* Tue Dec 8 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.6.3-5
-0.6.3
- Moved Doxygen docs to the development package.
- Corrected placement of the cmake project file (Thanks Orcan)
- Fixed the running of the build tests
- Corrected column length of the descriptions
- Changed description of the devlepment package

* Sun Dec 6 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.6.3-4
-0.6.3
- Additional placment of library files fix

* Fri Dec 4 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.6.3-3
-0.6.3
- Fixed placment of library files
- Activated build tests
- Corrected ownership of include directory
- Corrected dependacies
- Added doxygen documentation
- Fixed reported version in the changelogs

* Sun Nov 22 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.6.3-2
-0.6.3
- Split off development libraries to its own package
- Modified licensing in spec file to reflect GPL2 code though docs state that qjson
-   licensed under LPGL
- Uncommeted and corrected sed line in this spec file

* Sun Nov 22 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.6.3-1
-0.6.3
- Initial Build
