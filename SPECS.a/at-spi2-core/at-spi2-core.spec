%define majorver 2.11

Name:           at-spi2-core
Version: 2.11.90
Release:        1%{?dist}
Summary:        Protocol definitions and daemon for D-Bus at-spi
Summary(zh_CN.UTF-8): D-Bus at-spi 的协议定义和服务

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
Source0:        http://download.gnome.org/sources/at-spi2-core/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires:  dbus-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXevie-devel
BuildRequires:  libXext-devel
BuildRequires:  libXi-devel
BuildRequires:  autoconf automake libtool
BuildRequires:  intltool

Requires:       dbus

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

This version of at-spi is a major break from previous versions.
It has been completely rewritten to use D-Bus rather than
ORBIT / CORBA for its transport protocol.

%description -l zh_CN.UTF-8
at-spi 允许采用辅助技术来访问基于 GTK 的应用程序。本质上它是自动把应用程序
内部暴露出来，从面像屏幕阅读器、放大镜，甚至脚本接口等可以查询和使用  GUI
控件进行交互。

这个版本和前一个版本有较大区别，已经用 D-Bus 完全重写，而不在使用 ORBIT 和
CORBA 做为传输协议。

%package devel
Summary: Development files and headers for at-spi2-core
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
The at-spi2-core-devel package includes the header files and
API documentation for libatspi.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --with-dbus-daemondir=/bin

sed -i -e 's+sys_lib_dlsearch_path_spec="/lib /usr/lib+sys_lib_dlsearch_path_spec="/lib /usr/lib /lib64 /usr/lib64+' configure

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh
%{find_lang} %{name}

rm $RPM_BUILD_ROOT%{_libdir}/libatspi.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc COPYING AUTHORS README
%{_libexecdir}/at-spi2-registryd
%{_datadir}/dbus-1/services/org.a11y.atspi.Registry.service
%{_sysconfdir}/at-spi2
%{_sysconfdir}/xdg/autostart/at-spi-dbus-bus.desktop
%{_libdir}/libatspi.so.*
%{_libdir}/girepository-1.0/Atspi-2.0.typelib
%{_libexecdir}/at-spi-bus-launcher
%{_datadir}/dbus-1/services/org.a11y.Bus.service


%files devel
%{_libdir}/libatspi.so
%{_datadir}/gtk-doc/html/libatspi
%{_datadir}/gir-1.0/Atspi-2.0.gir
%{_includedir}/at-spi-2.0
%{_libdir}/pkgconfig/atspi-2.pc

%changelog
* Sun Mar 02 2014 Liu Di <liudidi@gmail.com> - 2.11.90-1
- 更新到 2.11.90

* Mon Mar 25 2013 Kalev Lember <kalevlember@gmail.com> - 2.8.0-1
- Update to 2.8.0

* Wed Mar  6 2013 Matthias Clasen <mclasen@redhat.com> - 2.7.91-1
- Update to 2.7.91

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 2.7.90-1
- Update to 2.7.90

* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com> - 2.7.5-1
- Update to 2.7.5

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.7.4.1-1
- Update to 2.7.4.1

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.7.4-1
- Update to 2.7.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.7.3-1
- Update to 2.7.3

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 2.7.1-1
- Update to 2.7.1

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 2.6.1-1
- Update to 2.6.1

* Tue Sep 25 2012 Richard Hughes <hughsient@gmail.com> - 2.6.0-1
- Update to 2.6.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 2.5.92-1
- Update to 2.5.92

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 2.5.91-1
- Update to 2.5.91

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 2.5.5-1
- Update to 2.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 2.5.4-1
- Update to 2.5.4

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 2.5.3-1
- Update to 2.5.3

* Wed Jun 06 2012 Richard Hughes <hughsient@gmail.com> - 2.5.2-1
- Update to 2.5.2

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 2.5.1-1
- Update to 2.5.1

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 2.4.1-1
- Update to 2.4.1

* Tue Mar 27 2012 Matthias Clasen <mclasen@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 2.3.92-1
- Update to 2.3.92

* Mon Mar  6 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.91-1
- Update to 2.3.91

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.90-1
- Update to 2.3.90

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.5-1
- Update to 2.3.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.4-1
- Update to 2.3.4

* Tue Jan 10 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.3.3-2
- Fix the rpath issue for building gobject-introspection properly as suggested from upstream

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.3-1
- Update to 2.3.3

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.2-1
- Update to 2.3.2

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.1-1
- Update to 2.3.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 2.2.1-1
- Update to 2.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.92-1
- Update to 2.1.92

* Mon Sep 5 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.91-1
- Update to 2.1.91

* Thu Sep 1 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.90-3
- Drop the %%{_isa} again, it seems to give autoqa trouble

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.90-2
- Fix requires

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.90-1
- Update to 2.1.90

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.5-1
- Update to 2.1.5

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.4-1
- Update to 2.1.4

* Thu Jun 16 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.1.2-1
- Update to 2.1.2

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.1.1-1
- Update to 2.1.1

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 2.0.0-1
- Update to 2.0.0

* Fri Apr  1 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.93-2
- Fix 30 second wait during login (#691995)

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.93-1
- Update to 1.91.93

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.92-1
- Update to 2.91.92

* Wed Mar  9 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.91-2
- Fix a crash on logout

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.91-1
- Update to 1.91.91

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.90-1
- Update to 1.91.90

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.91.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> - 1.91.6.1-1
- Update to 1.91.6.1

* Tue Feb  1 2011 Christopher Aillon <caillon@redhat.com> - 1.91.6-1
- Update to 1.91.6

* Fri Jan 21 2011 Christopher Aillon <caillon@redhat.com> - 1.91.5-2
- Add gobject-introspection support

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.5-1
- Update to 1.91.5

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 1.91.2-1
- Update 1.91.2

* Mon Oct  4 2010 Matthias Clasen <mclasen@redhat.com> - 1.91.0-1
- Update to 1.91.0

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.91-1
- Update to 0.3.91

* Wed Aug 18 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.90-1
- Update to 0.3.90

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.4-1
- Update to 0.3.4

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.3-1
- Update to 0.3.3

* Tue Jun  1 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.2-2
- Don't relocate the dbus a11y stack

* Fri May 28 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.2-1
- Update to 0.3.2

* Sat May 15 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.1-1
- Update to 0.3.1

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.8-1
- Update to 0.1.8

* Sat Feb 20 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.7-1
- Update to 0.1.7

* Wed Feb 10 2010 Tomas Bzatek <tbzatek@redhat.com> - 0.1.6-1
- Update to 0.1.6

* Wed Jan 20 2010 Matthias Clasen <mlasen@redhat.com> - 0.1.5-2
- Specify the right location for the dbus daemon

* Sun Jan 16 2010 Matthias Clasen <mlasen@redhat.com> - 0.1.5-1
- Update to 0.1.5

* Tue Dec 22 2009 Matthias Clasen <mlasen@redhat.com> - 0.1.4-1
- Update to 0.1.4

* Sat Dec  4 2009 Matthias Clasen <mlasen@redhat.com> - 0.1.3-1
- Initial packaging
