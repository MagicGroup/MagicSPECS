Name:         kpowersave
License:      GPL
Group:        User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Summary:      KDE Frontend to powersave Package, Battery Monitor and General Power Management Support
Summary(zh_CN.UTF-8): powersave包的KDE前端，支持电池监视和通用电源管理
Version:      0.7.3
Release:      1%{?dist}
ExclusiveArch: %ix86 x86_64 ia64 ppc
Requires:     powersave >= 0.12.17 powersave-libs >= 0.12.17 /sbin/pidof
Source0:       %{name}-%{version}.tar.bz2
Source1:	%{name}-zh_CN.po
Patch0:		kpowersave-kpowersave.desktop.patch
Patch1:		kpowersave-default_config.patch
Patch2:		kpowersave-0.7.3-admin.patch

%description
The package provides battery monitoring and suspend/standby triggers.
It is based on the powersave package and therefore supports APM and
ACPI. Together with the powersave package and the YaST Powermanagement
module it is the preferred package that should be used for battery
monitoring and control of power management related tasks. See powersave
package for additional features such as CPU frequency scaling(SpeedStep
and PowerNow) and more.



Authors:
--------
    Thomas Renninger (trenn@suse.de, mail@renninger.de)
    Danny Kukawka (dkukawka@suse.de, danny.kukawka@web.de)

%description -l zh_CN.UTF-8
这个包提供了电视监视器和休眠/待机触发器。它基于powersave包，所以支持APM
和ACPI。

%prep
%setup -n %{name}-%{version} -q
%patch1 -p1
%patch2 -p1
#%patch0 -p1
#cp -f %{SOURCE1} po/zh_CN.po
chmod 777 admin/*

%build
make -f admin/Makefile.common cvs
./configure --prefix=/usr
  
make

%install
make DESTDIR=$RPM_BUILD_ROOT install 

magic_rpm_clean.sh
%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README AUTHORS ChangeLog COPYING INSTALL
/usr/bin/kpowersave
/usr/share/config/kpowersaverc
/usr/share/autostart/kpowersave-autostart.desktop
/usr/share/apps/kpowersave
/usr/share/icons/??color
/usr/share/applications/kde/kpowersave.desktop
/usr/share/doc/HTML/*/kpowersave
/usr/lib*/trinity/kpowersave.*
/usr/lib*/libtdeinit_kpowersave.*
/usr/share/locale/*

%changelog -n kpowersave
* Fri Jun 13 2008 Liu Di <liudidi@gmail.com> - 0.7.3-1mgc
- 更新到 0.7.3
