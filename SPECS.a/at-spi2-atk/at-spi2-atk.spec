%global at_spi2_core_version 2.7.5

Name:           at-spi2-atk
Version: 2.18.1
Release:        2%{?dist}
Summary:        A GTK+ module that bridges ATK to D-Bus at-spi
Summary(zh_CN.UTF-8): ATK 到 D-Bus at-spi 桥的 GTK+ 模块

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
#VCS: git:git://git.gnome.org/at-spi-atk
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.gnome.org/sources/at-spi2-atk/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires:  at-spi2-core-devel >= %{at_spi2_core_version}
BuildRequires:  dbus-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  glib2-devel
BuildRequires:  libxml2-devel
BuildRequires:  atk-devel
BuildRequires:  gtk2-devel
BuildRequires:  intltool

Requires:       at-spi2-core >= %{at_spi2_core_version}

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

This version of at-spi is a major break from previous versions.
It has been completely rewritten to use D-Bus rather than
ORBIT / CORBA for its transport protocol.

This package includes a gtk-module that bridges ATK to the new
D-Bus based at-spi.

%description -l zh_CN.UTF-8
at-spi 允许采用辅助技术来访问基于 GTK 的应用程序。本质上它是自动把应用程序
内部暴露出来，从面像屏幕阅读器、放大镜，甚至脚本接口等可以查询和使用  GUI
控件进行交互。

这个版本和前一个版本有较大区别，已经用 D-Bus 完全重写，而不在使用 ORBIT 和
CORBA 做为传输协议。

这个包饮食了一个 gtk 模块，以便联系 ATK 和新的基于 D-Bus 的 at-spi。

%package devel
Summary:        A GTK+ module that bridges ATK to D-Bus at-spi
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package includes the header files for the %{name} library.

%description devel -l zh_CN
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-relocate
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/libatk-bridge.la
rm $RPM_BUILD_ROOT%{_libdir}/libatk-bridge-2.0.la

%files
%doc COPYING AUTHORS README
%dir %{_libdir}/gtk-2.0
%dir %{_libdir}/gtk-2.0/modules
%{_libdir}/gtk-2.0/modules/libatk-bridge.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/at-spi2-atk.desktop
%{_libdir}/libatk-bridge-2.0.so.*

%files devel
%{_includedir}/at-spi2-atk/2.0/atk-bridge.h
%{_libdir}/libatk-bridge-2.0.so
%{_libdir}/pkgconfig/atk-bridge-2.0.pc


%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 2.18.1-2
- 更新到 2.18.1

* Tue Apr 01 2014 Liu Di <liudidi@gmail.com> - 2.12.0-1
- 更新到 2.12.0

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

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.7.3-1
- Update to 2.7.3

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 2.7.1-1
- Update to 2.7.1
- Remove glib-compile-schemas scriptlets now that the schema is gone

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 2.6.1-1
- Update to 2.6.1
- Drop upstreamed multilib patch

* Tue Sep 25 2012 Richard Hughes <hughsient@gmail.com> - 2.6.0-1
- Update to 2.6.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 2.5.92-1
- Update to 2.5.92

* Tue Sep 11 2012 Matthias Clasen <mclasen@redhat.com> - 2.5.91-2
- Avoid a multilib conflict

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 2.5.91-1
- Update to 2.5.91

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 2.5.90-1
- Update to 2.5.90

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 2.5.5-1
- Update to 2.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 2.5.4-1
- Update to 2.5.4

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 2.5.3-1
- Update to 2.5.3

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 2.5.2-1
- Update to 2.5.2

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 2.5.1-1
- Update to 2.5.1

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 2.4.0-2
- Silence glib-compile-schemas output

* Tue Mar 27 2012 Matthias Clasen <mclasen@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 2.3.92-1
- Update to 2.3.92

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.91-1
- Update to 2.3.91

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.90-1
- Update to 2.3.90

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.5-1
- Update to 2.3.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.4-1
- Update to 2.3.4

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.3-1
- Update to 2.3.3

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.2-1
- Update to 2.3.2

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.1-1
- Update to 2.3.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for glibc bug#747377

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> 2.1.92-1
- Update to 2.1.92

* Mon Sep  5 2011 Matthias Clasen <mclasen@redhat.com> 2.1.91-1
- Update to 2.1.91

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> 2.1.90-1
- Update to 2.1.90

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> 2.1.5-1
- Update to 2.1.5

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> 2.1.4-1
- Update to 2.1.4

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> 2.0.1-1
- Update to 2.0.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> 2.0.0-1
- Update to 2.0.0

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> 1.91.93-1
- Update to 1.91.93

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> 1.91.92-1
- Update to 1.91.92

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> 1.91.91-1
- Update to 1.91.91

* Tue Feb 21 2011 Matthias Clasen <mclasen@redhat.com> 1.91.90-1
- Update to 1.91.90

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.91.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Bastien Nocera <bnocera@redhat.com> 1.91.6-3
- Add upstream patches to fix crashers

* Fri Feb 04 2011 Bastien Nocera <bnocera@redhat.com> 1.91.6-2
- Revert crashy part of 1.91.6 release

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> - 1.91.6-1
- Update to 1.91.6

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.5-1
- Update to 1.91.5

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 1.91.2-1
- Update to 1.91.2

* Mon Oct  4 2010 Matthias Clasen <mclasen@redhat.com> - 1.91.0-1
- Update to 1.91.0

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.91.1-1
- Update to 0.3.91.1

* Fri Aug 27 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.90-2
- Make the gtk module resident to prevent crashes

* Wed Aug 18 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.90-1
- Update to 0.3.90

* Mon Aug  2 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.6-1
- Update to 0.3.6

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.5-1
- Update to 0.3.5

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.4-1
- Update to 0.3.4

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.3-1
- Update to 0.3.3
- Include gtk3 module
- Drop gtk deps, since we don't want to depend on both gtk2 and gtk3;
  instead own the directories

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

* Sun Jan 16 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.5-1
- Update to 0.1.5

* Tue Dec 22 2009 Matthias Clasen <mclasen@redhat.com> - 0.1.4-1
- Update to 0.1.4

* Sat Dec  5 2009 Matthias Clasen <mclasen@redhat.com> - 0.1.3-1
- Initial packaging
