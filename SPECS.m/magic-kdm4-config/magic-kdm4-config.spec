Summary: K Desktop Environment - KDM Configuration files
Summary(zh_CN.UTF-8): K 桌面环境(KDE) - 登录管理器 (KDM) 配置文件
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Name: magic-kdm4-config
Version: 4.10.3
Release: 4%{?dist}
License: GPL
URL: http://www.magiclinux.org
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Source0: kdm-np.pamd
Source2: kdm.pamd
Source3: kcheckpass.pamd
Source4: kscreensaver.pamd
Requires: kdelibs4, magic-system-config, magic-kde4-config >= 4.10.3

%description
Configuration filess for KDM by MagicLinux.

%description -l zh_CN.UTF-8
MagicLinux 下 KDM4 的配置文件。


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

mkdir -p $RPM_BUILD_ROOT/etc/pam.d
install -p -m644 -D %{SOURCE0} $RPM_BUILD_ROOT/etc/pam.d/kdm-np
install -p -m644 -D %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/kdm
install -p -m644 -D %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/kcheckpass
install -p -m644 -D %{SOURCE4} $RPM_BUILD_ROOT/etc/pam.d/kscreensaver

magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
/etc/pam.d/*

%changelog
* Fri May 09 2014 Liu Di <liudidi@gmail.com> - 4.10.3-4
- 为 Magic 3.0 重建

* Fri May 09 2014 Liu Di <liudidi@gmail.com> - 4.10.3-3
- 为 Magic 3.0 重建

* Fri May 09 2014 Liu Di <liudidi@gmail.com> - 4.10.3-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.3.x.20090614-3
- 为 Magic 3.0 重建

