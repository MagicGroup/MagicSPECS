Name:          geoclue
Version:       0.12.99
Release:       2%{?dist}
Summary:       A modular geoinformation service
Summary(zh_CN.UTF-8): 模块化的地理信息服务

Group:         System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:       LGPLv2
URL:           http://geoclue.freedesktop.org/
Source0:       http://folks.o-hand.com/jku/geoclue-releases/%{name}-%{version}.tar.gz

BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: glib2-devel
BuildRequires: libxml2-devel
BuildRequires: libsoup-devel
BuildRequires: gtk3-devel
BuildRequires: NetworkManager-devel >= 1:0.8.997
BuildRequires: NetworkManager-glib-devel >= 1:0.8.997
BuildRequires: gypsy-devel
BuildRequires: gtk-doc

Obsoletes: geoclue-gpsd
Requires: dbus

%description
Geoclue is a modular geoinformation service built on top of the D-Bus 
messaging system. The goal of the Geoclue project is to make creating 
location-aware applications as simple as possible. 

%description -l zh_CN.UTF-8
这是一个 D-Bus 顶层的模块化地理信息服务。它的目的是让位置感知的应用程序
尽量简单。

%package devel
Summary: Development package for geoclue
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: dbus-devel
Requires: libxml2-devel
Requires: pkgconfig

%description devel
Files for development with geoclue.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: Developer documentation for geoclue
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Developer documentation for geoclue

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%package gui
Summary: Testing gui for geoclue
Summary(zh_CN.UTF-8): %{name} 的测试界面
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description gui
Testing gui for geoclue

%description gui -l zh_CN.UTF-8
%{name} 的测试图形界面。

%package gypsy
Summary: gypsy provider for geoclue
Summary(zh_CN.UTF-8): %{name} 的 gypsy 模块
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name} = %{version}-%{release}

%description gypsy
A gypsy provider for geoclue

%description gypsy -l zh_CN.UTF-8
%{name} 的 gypsy 模块。

%package gsmloc
Summary: gsmloc provider for geoclue
Summary(zh_CN.UTF-8): %{name} 的 gsmloc 模块
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name} = %{version}-%{release}

%description gsmloc
A gsmloc provider for geoclue

%description gsmloc -l zh_CN.UTF-8
%{name} 的 gsmloc 模块。

%prep
%setup -q
sed -i -e "s/gtk+-2.0/gtk+-3.0/" configure

%build
%configure --disable-static --enable-gtk-doc --enable-networkmanager=yes --enable-gypsy=yes --enable-skyhook=yes --enable-gsmloc=yes --enable-gpsd=no
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Install the test gui as it seems the test isn't installed any more
mkdir $RPM_BUILD_ROOT%{_bindir}
cp test/.libs/geoclue-test-gui $RPM_BUILD_ROOT%{_bindir}/
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%dir %{_datadir}/geoclue-providers
%{_libdir}/libgeoclue.so.0
%{_libdir}/libgeoclue.so.0.0.0
%{_datadir}/GConf/gsettings/geoclue
%{_datadir}/glib-2.0/schemas/org.freedesktop.Geoclue.gschema.xml
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Master.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Example.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Geonames.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Hostip.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Localnet.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Manual.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Nominatim.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Plazes.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Skyhook.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Yahoo.service
%{_datadir}/geoclue-providers/geoclue-example.provider
%{_datadir}/geoclue-providers/geoclue-geonames.provider
%{_datadir}/geoclue-providers/geoclue-hostip.provider
%{_datadir}/geoclue-providers/geoclue-localnet.provider
%{_datadir}/geoclue-providers/geoclue-manual.provider
%{_datadir}/geoclue-providers/geoclue-nominatim.provider
%{_datadir}/geoclue-providers/geoclue-plazes.provider
%{_datadir}/geoclue-providers/geoclue-skyhook.provider
%{_datadir}/geoclue-providers/geoclue-yahoo.provider
%{_libexecdir}/geoclue-example
%{_libexecdir}/geoclue-geonames
%{_libexecdir}/geoclue-hostip
%{_libexecdir}/geoclue-localnet
%{_libexecdir}/geoclue-manual
%{_libexecdir}/geoclue-nominatim
%{_libexecdir}/geoclue-master
%{_libexecdir}/geoclue-plazes
%{_libexecdir}/geoclue-skyhook
%{_libexecdir}/geoclue-yahoo

%files devel
%defattr(-,root,root,-)
%{_includedir}/geoclue
%{_libdir}/pkgconfig/geoclue.pc
%{_libdir}/libgeoclue.so

%files doc
%defattr(-,root,root,-)
%{_datadir}/gtk-doc/html/geoclue/

%files gui
%defattr(-,root,root,-)
%{_bindir}/geoclue-test-gui

%files gypsy
%defattr(-,root,root,-)
%{_libexecdir}/geoclue-gypsy
%{_datadir}/geoclue-providers/geoclue-gypsy.provider
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Gypsy.service

%files gsmloc
%defattr(-,root,root,-)
%{_libexecdir}/geoclue-gsmloc
%{_datadir}/geoclue-providers/geoclue-gsmloc.provider
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Gsmloc.service

%changelog
* Fri Oct 26 2012 Bastien Nocera <bnocera@redhat.com> 0.12.99-1
- Remove unused gammu BR
- Compile against GTK+ 3.0

* Tue Jul 31 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.99-1
- Update to 0.12.99 devel release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 01 2012 Kalev Lember <kalevlember@gmail.com> - 0.12.0-10
- Add patch to fix build with glib threading changes
- Remove -Werror from CFLAGS

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.12.0-8
- Rebuild for new libpng

* Thu Mar 24 2011 Dan Williams <dcbw@redhat.com> - 0.12.0-7
- Rebuild

* Wed Mar 23 2011 Ray Strode <rstrode@redhat.com> 0.12.0-6
- Rebuild

* Thu Mar 10 2011 Dan Williams <dcbw@redhat.com> - 0.12.0-5
- Updated for NetworkManager 0.9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 20 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.0-3
- Add patch for cache_ap_mac crash

* Tue Sep  7 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.0-2
- Add libtoolize to fix the build until we get a new upstream release

* Thu Mar 25 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.0-1
- New official upstream 0.12.0 release, drop gpsd support

* Fri Jan 29 2010 Bastien Nocera <bnocera@redhat.com> 0.11.1.1-0.11
- Fix crashers in geoclue-master provider (#528897)
- Bump release to be greater than F-12's

* Mon Oct 24 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1.1-0.9
- New git snapshot, enable NetworkManager support for WiFi location, gsmloc and new Skyhook plugin

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1.1-0.8.20090310git3a31d26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1.1-0.7
- Move develop documentation to its own noarch package to fix RHBZ 513488

* Sat Jun 20 2009 Bastien Nocera <bnocera@redhat.com> 0.11.1.1-0.6
- Add developer documentation

* Fri Jun 19 2009 Bastien Nocera <bnocera@redhat.com> 0.11.1.1-0.4
- Fix geoclue-test-gui (#506921)

* Thu Apr 09 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1.1-0.3
- Fix install of test gui

* Sun Mar 29 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.11.1.1-0.2
- Rebuild for new gpsd

* Tue Mar 10 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1.1-0.1
- Move to a git snapshot until we finally get a new stable release

* Wed Mar 4 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1-15
- Move docs to noarch, a few spec file cleanups

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1-13
- Fix summary

* Thu Jul 31 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1-12
- Once more for fun

* Thu Jul 31 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1-11
- Increment build number to allow for clean F-8 and F-9 to F-10 upgrade

* Wed Jul 2 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1-6
- Fixed spec file so gpsd and gypsy are actually properly in a subpackage

* Sun May 18 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1-5
- Added gypsy and gpsd providers to build as sub packages

* Mon Apr 28 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1-4
- Moved api documentation to -devel

* Sat Apr 26 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1-3
- Cleanup requires and group for test gui

* Sat Apr 26 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1-2
- Some spec file cleanups

* Fri Apr 25 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1-1
- Initial package
