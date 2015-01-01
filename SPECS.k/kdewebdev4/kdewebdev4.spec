%define real_name kdewebdev

%define kde4_enable_final_bool OFF

Name: kdewebdev4
Summary: The KDE Weddev Components
Summary(zh_CN.UTF-8): KDE 网络开发组件
License: LGPL v2 or later
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://www.kde.org/
Version: 4.14.3
Release: 1%{?dist}
Source0: http://download.kde.org/stable/%{version}/src/%{real_name}-%{version}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libkdelibs4-devel
BuildRequires: strigi >= 0.6.3
BuildRequires: qt4-devel >= 4.4.3

Requires: %{name}-kfilereplace = %{version}
Requires: %{name}-kimagemapeditor = %{version}
Requires: %{name}-klinkstatus = %{version}
Requires: %{name}-kommander = %{version}

%description
The KDE Weddev Components.

%description -l zh_CN.UTF-8
KDE 网络开发组件。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package -n %{name}-devel
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: KDE Weddev Libraries: Build Environment
Requires: libkdelibs4-devel
Requires: %{name} = %{version}

%description -n %{name}-devel
This package contains all necessary include files and libraries needed
to develop KDE Weddev applications.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kfilereplace
%package -n %{name}-kfilereplace
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kfilereplace

%description -n %{name}-kfilereplace
kfilereplace.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kimagemapeditor
%package -n %{name}-kimagemapeditor
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kimagemapeditor

%description -n %{name}-kimagemapeditor
kimagemapeditor.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- klinkstatus
%package -n %{name}-klinkstatus
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: klinkstatus

%description -n %{name}-klinkstatus
klinkstatus.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kommander
%package -n %{name}-kommander
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kommander

%description -n %{name}-kommander
kommander.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%prep
%setup -q -n %{real_name}-%{version}

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install


%clean_kde4_desktop_files
magic_rpm_clean.sh

%post -n %{name}-klinkstatus -p /sbin/ldconfig
%postun -n %{name}-klinkstatus -p /sbin/ldconfig

%post -n %{name}-kommander -p /sbin/ldconfig
%postun -n %{name}-kommander -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -n %{name}-devel
%defattr(-,root,root)
%{kde4_includedir}/*
%{kde4_libdir}/*.so

%files
%defattr(-,root,root)

%files -n %{name}-kfilereplace
%defattr(-,root,root)
%{kde4_bindir}/kfilereplace
%{kde4_plugindir}/libkfilereplacepart.so
%{kde4_appsdir}/kfilereplace/*
%{kde4_appsdir}/kfilereplacepart/*
%{kde4_dbus_interfacesdir}/org.kde.kfilereplace.xml
%{kde4_iconsdir}/hicolor/*/apps/kfilereplace.*
%{kde4_xdgappsdir}/kfilereplace.desktop
%{kde4_servicesdir}/kfilereplacepart.desktop
%doc %lang(en) %{kde4_htmldir}/en/kfilereplace

%files -n %{name}-kimagemapeditor
%defattr(-,root,root)
%{kde4_bindir}/kimagemapeditor
%{kde4_plugindir}/libkimagemapeditor.so
%{kde4_appsdir}/kimagemapeditor/*
%{kde4_iconsdir}/hicolor/*/apps/kimagemapeditor.*
%{kde4_iconsdir}/hicolor/22x22/actions/addpoint.png
%{kde4_iconsdir}/hicolor/22x22/actions/arrow.png
%{kde4_iconsdir}/hicolor/22x22/actions/circle.png
%{kde4_iconsdir}/hicolor/22x22/actions/circle2.png
%{kde4_iconsdir}/hicolor/22x22/actions/freehand.png
%{kde4_iconsdir}/hicolor/22x22/actions/lower.png
%{kde4_iconsdir}/hicolor/22x22/actions/polygon.png
%{kde4_iconsdir}/hicolor/22x22/actions/raise.png
%{kde4_iconsdir}/hicolor/22x22/actions/rectangle.png
%{kde4_iconsdir}/hicolor/22x22/actions/removepoint.png
%{kde4_xdgappsdir}/kimagemapeditor.desktop
%{kde4_servicesdir}/kimagemapeditorpart.desktop
%doc %lang(en) %{kde4_htmldir}/en/kimagemapeditor

%files -n %{name}-klinkstatus
%defattr(-,root,root)
%{kde4_bindir}/klinkstatus
%{kde4_plugindir}/automationklinkstatus.so
%{kde4_plugindir}/klinkstatuspart.so
%{kde4_plugindir}/krossmoduleklinkstatus.so
%{kde4_libdir}/libklinkstatuscommon.so.*
%{kde4_appsdir}/klinkstatus/*
%{kde4_appsdir}/klinkstatuspart/*
%config %{kde4_configdir}/klinkstatus.knsrc
%{kde4_dbus_interfacesdir}/org.kde.kdewebdev.klinkstatus.SearchManager.xml
%{kde4_iconsdir}/hicolor/*/apps/klinkstatus.*
%{kde4_xdgappsdir}/klinkstatus.desktop
%{kde4_servicesdir}/klinkstatus_automation.desktop
%{kde4_servicesdir}/klinkstatus_part.desktop
%{kde4_servicesdir}/krossmoduleklinkstatus.desktop
%doc %lang(en) %{kde4_htmldir}/en/klinkstatus

%files -n %{name}-kommander
%defattr(-,root,root)
%{kde4_bindir}/kommander
%{kde4_libdir}/libkommandercore.so.*
%{kde4_libdir}/libkommanderwidgets.so.*
#%{kde4_appsdir}/kommander/*
%{kde4_datadir}/applnk/.hidden/kommander.desktop
#%{kde4_iconsdir}/hicolor/*/apps/kommander.*
#%{kde4_xdgappsdir}/kommander.desktop
#%doc %lang(en) %{kde4_htmldir}/en/kommander


%changelog
* Tue Dec 30 2014 Liu Di <liudidi@gmail.com> - 4.14.3-1
- 更新到 4.14.3

* Fri Oct 24 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Fri Apr 25 2014 Liu Di <liudidi@gmail.com> - 4.13.0-1.1
- 为 Magic 3.0 重建

* Tue Aug 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0
- 己丑  六月十四

* Tue Jun 30 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- 更新至 4.2.95(KDE 4.3 RC1)
- 己丑  闰五月初八

* Sat Jun 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.91-1mgc
- 更新至 4.2.91
- 己丑  五月廿一

* Sat May 16 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.85-1mgc
- 更新至 4.2.85(KDE 4.3 beta1)
- 己丑  四月廿二

* Sun Apr 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- 己丑  三月初十

* Sun Mar 8 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.1mgc
- 更新至 4.2.1
- 己丑  二月十二

* Sun Jan 25 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.1mgc
- 更新至 4.2.0
- 戊子  十二月三十

* Thu Jan 15 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.1.96-0.1mgc
- 更新至 4.1.96(KDE 4.2 RC1)
- relwithdeb 编译模式
- 戊子  十二月二十

* Fri Nov 07 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.3-0.1mgc
- 更新至 4.1.3
- 戊子  十月初十  [立冬]

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.1mgc
- 更新至 4.1.2
- 戊子  九月初一

* Sat Aug 30 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.1mgc
- 更新至 4.1.1
- 戊子  七月三十

* Fri Jul 25 2008 Liu Di <liudidi@gmail.com> - 4.1.0-1mgc
- 更新到 4.1.0(KDE 4.1 正式版)

* Fri Jul 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.98-0.1mgc
- 更新至 4.0.98(KDE 4.1 RC1)
- 戊子  六月初九

* Sat Jun 28 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.84-0.1mgc
- 更新至 4.0.84
- 戊子  五月廿五

* Thu Jun 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.83-0.1mgc
- 更新至 4.0.83-try1(第一次 tag 4.1.0-beta2 内部版本)
- 戊子  五月十六

* Thu Jun 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.82-0.1mgc
- 更新至 4.0.82
- 戊子  五月初九

* Wed Jun 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.81-0.1mgc
- 更新至 4.0.81
- 戊子  五月初一

* Sat May 24 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.80-0.1mgc
- 更新至 4.0.80(try1 内部版本)
- 戊子  四月二十

* Sat Apr 26 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.71-0.1mgc
- 更新至 4.0.71
- 定义 kde4 路径
- 戊子  三月廿一

* Fri Feb 8 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.1-0.1mgc
- 更新至 4.0.1

* Sat Jan 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.1mgc
- 更新至 4.0.0

* Sat Dec 15 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.97.0-0.1mgc
- 更新至 3.97.0 (KDE4-RC2)

* Sat Nov 24 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.96.0-0.1mgc
- 更新至 3.96.0 (KDE4-RC1)

* Sat Oct 20 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.94.0-0.1mgc
- 首次生成 rpm 包
