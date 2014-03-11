%define build_type release
Summary: A project allowing GTK to use Qt widget styles.
Summary(zh_CN.UTF-8): 一个允许GTK使用Qt控件风格的项目
Name: 	 gtk-qt4-engine 
%define realname gtk-qt-engine
Group:	 User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Version: 1.1
Release: 6%{?dist}

License: GPL
URL:     http://www.freedesktop.org/Software/gtk-qt
Source0: gtk-qt-engine-%{version}.tar.bz2
Patch0:	 gtk-qt-engine-glibh.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: gtk2-devel >= 2.2
#BuildRequires: libbonoboui-devel
BuildRequires: qt-devel 
BuildRequires: libpng-devel


%description
The GTK-Qt Theme Engine is a project allowing GTK to use Qt widget styles.

It behaves like a normal GTK theme engine, but calls functions from Qt 
instead of doing the drawing itself. 

%description -l zh_CN.UTF-8
GTK-Qt主题引擎是一个允许GTK使用QT组件风格的项目。

它的行为就像普通的GTK主题引擎，但是不用自己的函数而用Qt的函数来画界面。

%package kde4
Summary: %name for kde4
Summary(zh_CN.UTF-8): %name 的 KDE4 插件
Group:   User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
BuildRequires: kdebase4-devel
Requires: kdebase4

%description kde4 
%name for kde4.

%description kde4 -l zh_CN.UTF-8
%name 的 KDE4 插件。

%prep
%setup -q  -n %{realname}
%patch0 -p1

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$CFLAGS"
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
        -DINCLUDE_INSTALL_DIR=%{_includedir} \
        -DLIB_INSTALL_DIR=%{_libdir} \
        -DMAN_INSTALL_DIR=%{_mandir} \
        -DCMAKE_BUILD_TYPE=%{build_type}

make



%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

magic_rpm_clean.sh

# locale's
%find_lang gtkqtengine || touch gtkqtengine.lang

%clean
rm -rf $RPM_BUILD_ROOT


%files -f gtkqtengine.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog
%{_datadir}/themes/Qt4/
%{_libdir}/gtk-2.0/*/engines/*

%files kde4
%defattr(-,root,root)
%{kde4_plugindir}/kcm_gtk4.so
%{kde4_xdgappsdir}/kcmgtk4.desktop
%{kde4_iconsdir}/kcmgtk.png

%changelog 
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1-6
- 为 Magic 3.0 重建

* Fri Dec 09 2011 Liu Di <liudidi@gmail.com> - 1.1-5
- 为 Magic 3.0 重建

* Thu Jul 25 2006 Nicholas Wang <abcxyz54321@163.com> 0.70-1
- update to gtk-qt-engine-0.7, drop  the old version's default gtk 2.0 theme  function

* Sat Apr 15 2006 KanKer <kanker@163.com>
- add a patch from 再见情人

* Wed Nov 30 2005 KanKer <kanker@163.com>
- build

