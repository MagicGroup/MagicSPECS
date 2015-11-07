Name:           kde-plasma-daisy
Version:        0.0.4.26
Release:        3%{?dist}
Summary:        A simple application launcher for Plasma
Summary(zh_CN.UTF-8): Plasma 的简单程序载入器
Group:          User Interface/Desktops
Group(zh_CN.UTF-8):	用户界面/桌面
License:        GPLv3
URL:            http://www.kde-look.org/content/show.php?content=102077
Source0:        http://cdlszm.org/downloads/plasma-applet-daisy-%{version}.tar.gz
Source1: plasma_applet_daisy.po

Patch1: plasma-applet-daisy-desktop-zh_CN.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kdelibs4-devel


%description
Daisy is a  free open-source widget for Plasma/KDE released under the GNU General Public License version 3.
Main features:
   *  Three types of roles: circular dock, media controller and linear dock;
   *  Can dock in any screen position and be used in Horizontal or Vertical mode (linear dock role);
   *  Configuration tools to access all configurable options;
   *  Launchers can be edited with a simple right-click;
   *  Hybrid launchers to launch applications and control running tasks;
   *  Plugins to provide information and execute several tasks;
   *  Various backgrounds available.

%description -l zh_CN.UTF-8
Plasma 的简单程序载入器

%prep
%setup -q -n plasma-applet-daisy-%{version}

pushd applet
%patch1 -p0
popd

cp %{SOURCE1} applet/po/zh_CN.po

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}

magic_rpm_clean.sh

%clean_kde4_desktop_files

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{kde4_plugindir}/plasma_applet_daisy.so
%{kde4_servicesdir}/plasma-applet-daisy.desktop
%{kde4_appsdir}/desktoptheme/default/widgets/circular-background.svgz
%{kde4_appsdir}/desktoptheme/default/widgets/dock-background-mach.svgz
%{kde4_appsdir}/desktoptheme/default/widgets/dock-background.svgz
%{kde4_appsdir}/desktoptheme/default/widgets/dock-background-shiny-black.svgz
%{kde4_appsdir}/desktoptheme/default/widgets/dock-background-vidro.svgz
%{kde4_appsdir}/desktoptheme/default/widgets/tasks-indicators.svgz
%{kde4_appsdir}/desktoptheme/default/widgets/dock-animations.svgz
%{kde4_appsdir}/desktoptheme/default/widgets/dock-background-mach-2.svgz
%{kde4_localedir}/*

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.0.4.26-3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.0.4.25-2
- 为 Magic 3.0 重建

