
Name:    libqzeitgeist
Summary: Qt Zeitgeist Library
Summary(zh_CN.UTF-8): Qt Zeitgest 库
Version: 0.8.0
Release: 9%{?dist}

License: LGPLv2+
URL:     http://projects.kde.org/projects/kdesupport/libqzeitgeist 
Source0: http://download.kde.org/download.php?url=stable/libqzeitgeist/%{version}/src/libqzeitgeist-%{version}.tar.bz2

## upstreamable patches

## upstream patches
# fix linking (don't link the Qt world, including QtWebkit, only use QT_DECLARATIVE_LIBRARIES)
# consistently use QT_IMPORTS_DIR
Patch100: libqzeitgeist-0.8.0-declarative.patch
# reduce linking in libqzeitgeist too
Patch101: libqzeitgeist-0.8.0-reduced_linking.patch


BuildRequires: automoc4
BuildRequires: cmake
BuildRequires: pkgconfig(QtDBus) pkgconfig(QtDeclarative) pkgconfig(QtXml)
BuildRequires: zeitgeist

%description
A Qt interface to the Zeitgeist event tracking system.

%description -l zh_CN.UTF-8
Zeitgeist 事件跟踪系统的 Qt 接口

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q 

%patch100 -p1 -b .declarative
%patch101 -p1 -b .reduced_linking


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

magic_rpm_clean.sh

%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion QZeitgeist)" = "%{version}"



%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING README
%{_libdir}/libqzeitgeist.so.%{version}
%{_libdir}/libqzeitgeist.so.1
%{_libdir}/qt4/imports/org/

%files devel
%{_includedir}/QZeitgeist/
%{_libdir}/libqzeitgeist.so
%{_libdir}/cmake/QZeitgeist/
%{_libdir}/pkgconfig/QZeitgeist.pc


%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.8.0-9
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.8.0-8
- 为 Magic 3.0 重建

* Mon Jul 28 2014 Liu Di <liudidi@gmail.com> - 0.8.0-7
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.8.0-6
- 为 Magic 3.0 重建

* Mon Nov 28 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.0-4
- component description has very low information content (#757719)

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.0-3
- reduced linking for libqzeitgeist too

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.0-2
- declarative patch

* Thu Oct 27 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.0-1
- 0.8.0

* Fri May 20 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.0-1
- first try

