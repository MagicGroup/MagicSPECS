
Name:    libmygpo-qt
Summary: Qt Library that wraps the gpodder.net Web API
Summary(zh_CN.UTF-8): gpodder.net 网页 API 的 Qt 库接口
Version: 1.0.8
Release: 2%{?dist}

License: LGPLv2+
Url:     http://wiki.gpodder.org/wiki/Libmygpo-qt
Source0: http://stefan.derkits.at/files/libmygpo-qt/libmygpo-qt.%{version}.tar.gz

BuildRequires: automoc4
BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: pkgconfig(QJson)
BuildRequires: pkgconfig(QtNetwork) 
 
%description
libmygpo-qt is a Qt Library that wraps the gpodder.net Web API,
http://wiki.gpodder.org/wiki/Web_Services/API_2

%description -l zh_CN.UTF-8
gpodder.net 网页 API 的 Qt 库接口。
http://wiki.gpodder.org/wiki/Web_Services/API_2

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。
 
%prep
%setup -q -n %{name}.%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
magic_rpm_clean.sh

%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion libmygpo-qt)" = "%{version}"
make test -C %{_target_platform}

 
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS LICENSE README 
%{_libdir}/libmygpo-qt.so.1*
 
%files devel
%{_includedir}/mygpo-qt/
%{_libdir}/libmygpo-qt.so
%{_libdir}/pkgconfig/libmygpo-qt.pc
%{_libdir}/cmake/mygpo-qt/
 
 
%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.0.8-2
- 更新到 1.0.8

* Tue Jul 22 2014 Liu Di <liudidi@gmail.com> - 1.0.7-1
- 更新到 1.0.7

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.6-2
- 为 Magic 3.0 重建

* Sat Oct 13 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.6-1
- 1.0.6

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.5-1
- 1.0.5

* Wed Sep 14 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.4-1
- 1.0.4

* Mon May 23 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.3-1
- 1.0.3

* Fri May 20 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.2-2
- drop kde deps/macros, this is a qt-only library

* Tue May 10 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.2-1
- 1.0.2 first try


