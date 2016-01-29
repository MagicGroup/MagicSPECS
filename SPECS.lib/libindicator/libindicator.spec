Name:		libindicator
Version:	12.10.1
Release:	5%{?dist}
Summary:	Shared functions for Ayatana indicators
Summary(zh_CN.UTF-8): Ayatana 指标的共享函数

Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	GPLv3
URL:		https://launchpad.net/libindicator
Source0:	https://launchpad.net/libindicator/12.10/12.10.1/+download/%{name}-%{version}.tar.gz

BuildRequires:	chrpath
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRequires:	pkgconfig

BuildRequires:	dbus-glib-devel
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel


%description
A set of symbols and convenience functions that all Ayatana indicators are
likely to use.

%description -l zh_CN.UTF-8
Ayatana 指标的共享函数。


%package devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package tools
Summary:	Shared functions for Ayatana indicators - Tools
Summary(zh_CN.UTF-8): %{name} 的工具
Group:		Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description tools
This package contains tools used by the %{name} package, the
Ayatana indicators system.

%description tools -l zh_CN.UTF-8
%{name} 的工具。

%package gtk3
Summary:	GTK+3 build of %{name}
Summary(zh_CN.UTF-8): %{name} 的 GTK+3 版本
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description gtk3
A set of symbols and convenience functions that all Ayatana indicators
are likely to use. This is the GTK+ 3 build of %{name}, for use
by GTK+ 3 apps.

%description gtk3 -l zh_CN.UTF-8
%{name} 的 GTK+3 版本。

%package gtk3-devel
Summary:	Development files for %{name}-gtk3
Summary(zh_CN.UTF-8): %{name}-gtk3 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库

Requires:	%{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description gtk3-devel
The %{name}-gtk3-devel package contains libraries and header files for
developing applications that use %{name}-gtk3.

%description gtk3-devel -l zh_CN.UTF-8
%{name}-gtk3 的开发包。

%package gtk3-tools
Summary:	Shared functions for Ayatana indicators - GTK3 Tools
Summary(zh_CN.UTF-8): %{name}-gtk3 的工具
Group:		Development/Tools
Group(zh_CN.UTF-8): 开发/工具

Requires:	%{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description gtk3-tools
This package contains tools used by the %{name}-gtk3 package, the
Ayatana indicators system. This package contains the builds of the
tools for the GTK+3 build of %{name}.

%description gtk3-tools -l zh_CN.UTF-8
%{name}-gtk3 的工具。

%prep
%setup -q

%build
%global _configure ../configure
rm -rf build-gtk2 build-gtk3
mkdir build-gtk2 build-gtk3

pushd build-gtk2
export CFLAGS="%{optflags} -Wno-error=deprecated-declarations"
%configure --with-gtk=2 --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
popd

pushd build-gtk3
export CFLAGS="%{optflags} -Wno-error=deprecated-declarations"
%configure --with-gtk=3 --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
popd


%install
pushd build-gtk2
make install DESTDIR=%{buildroot}
popd

pushd build-gtk3
make install DESTDIR=%{buildroot}
popd


# Ubuntu doesn't package the dummy indicator
rm -f %{buildroot}%{_libdir}/libdummy-indicator*.so

# Remove libtool files
find %{buildroot} -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post gtk3 -p /sbin/ldconfig

%postun gtk3 -p /sbin/ldconfig


%files
%doc AUTHORS COPYING NEWS ChangeLog
%{_libdir}/libindicator.so.*


%files devel
%dir %{_includedir}/libindicator-0.4/
%dir %{_includedir}/libindicator-0.4/libindicator/
%{_includedir}/libindicator-0.4/libindicator/*.h
%{_libdir}/libindicator.so
%{_libdir}/pkgconfig/indicator-0.4.pc


%files tools
%{_libexecdir}/indicator-loader
%dir %{_datadir}/libindicator/
%{_datadir}/libindicator/80indicator-debugging


%files gtk3
%doc AUTHORS COPYING NEWS ChangeLog
%{_libdir}/libindicator3.so.*


%files gtk3-devel
%dir %{_includedir}/libindicator3-0.4/
%dir %{_includedir}/libindicator3-0.4/libindicator/
%{_includedir}/libindicator3-0.4/libindicator/*.h
%{_libdir}/libindicator3.so
%{_libdir}/pkgconfig/indicator3-0.4.pc


%files gtk3-tools
%{_libexecdir}/indicator-loader3

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Eduardo Echeverria  <echevemaster@gmail.com> - 12.10.1-1
- Update to 12.10.1
- Add GTK2 support

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.94-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.94-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 31 2012 Tom Callaway <spot@fedoraproject.org> - 0.4.94-2
- fix typo causing dep issues

* Sat Mar 31 2012 Tom Callaway <spot@fedoraproject.org> - 0.4.94-1
- Update to 0.4.94

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.3.22-2
- Rebuild for new libpng

* Wed Mar 23 2011 Adam Williamson <awilliam@redhat.com> - 0.3.22-1
- new release 0.3.22

* Mon Mar 07 2011 Adam Williamson <awilliam@redhat.com> - 0.3.20-1
- new release 0.3.20

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.3.17-4
 Rebuild against newer gtk3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.3.17-2
 Rebuild against newer gtk3

* Sun Jan 23 2011 Adam Williamson <awilliam@redhat.com> - 0.3.17-1
- new version 0.3.17
- drop both patches (upstream)
- no need for autoreconf any more

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.3.15-2
- Rebuild against newer gtk3

* Fri Dec 03 2010 Adam Williamson <awilliam@redhat.com> - 0.3.15-1
- initial package

