Name:           qjson
Version:        0.7.1
Release:        10%{?dist}
Summary:        A qt-based library that maps JSON data to QVariant objects

Group:          Development/Languages
License:        GPLv2+
URL:            http://sourceforge.net/projects/qjson/
Source0:        http://downloads.sourceforge.net/project/qjson/qjson/0.7.1/qjson-0.7.1.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake >= 2.6
BuildRequires:  doxygen
BuildRequires:  pkgconfig(QtCore)

%description
JSON is a lightweight data-interchange format. It can represents integer, real
number, string, an ordered sequence of value, and a collection of
name/value pairs.QJson is a qt-based library that maps JSON data to
QVariant objects.

%package devel
Summary:  Development files for qjson
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
The %{name}-devel package contains the libraries and header files required for
developing applications that use %{name}.

%prep
%setup -qn qjson

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DQJSON_BUILD_TESTS:BOOL=ON \
  -DCMAKE_MODULES_INSTALL_DIR:PATH=%{_datadir}/cmake/Modules/ \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}

# build docs
pushd doc
doxygen
popd

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}
magic_rpm_clean.sh

%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion QJson)" = "%{version}"
make test -C %{_target_platform}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%doc README
%{_libdir}/libqjson.so.0*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_includedir}/qjson/
%{_libdir}/libqjson.so
%{_libdir}/pkgconfig/QJson.pc
# own parent dir(s), avoid dep on cmake
%dir %{_datadir}/cmake
%dir %{_datadir}/cmake/Modules
%{_datadir}/cmake/Modules/FindQJSON.cmake

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.7.1-10
- 为 Magic 3.0 重建

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
