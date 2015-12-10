Summary:			fbsplashsystemd - Systemd units for Fbsplash
Summary(zh_CN.UTF-8):		fbsplashsystemd - 用于控制 Fbsplash 的 Systemd units
Name:				fbsplashsystemd
Version:			0.01
Release:			3%{?dist}

Source:				%{name}-%{version}.tar.xz

Group:				Applications/System
Group(zh_CN.UTF-8):		应用程序/系统
Packager:			Jiang Tao < jiangtao9999@163.com >
Distribution:			Magic Linux 3
License:			GPL
BuildRoot:			%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires:			systemd

BuildArch: noarch

%description
Some Systemd units. Used to control Fbsplash.


%description -l zh_CN.UTF-8
一些 Systemd 的 Unit 。用于控制 Fbsplash 。

%prep

%setup

%build

%install

%{__rm} -rf "%{buildroot}"

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -m 0755 splash.ctl $RPM_BUILD_ROOT%{_sbindir}/

mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system
install -m 0644 fbsplash-*.service $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system

#以下的这些是不对的，需要改正。
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/halt.target.wants
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/poweroff.target.wants
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/reboot.target.wants
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/multi-user.target.wants
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/sysinit.target.wants


ln -s ../fbsplash-poweroff.service $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/halt.target.wants/fbsplash-poweroff.service
ln -s ../fbsplash-poweroff.service $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/poweroff.target.wants/fbsplash-poweroff.service
ln -s ../fbsplash-reboot.service $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/reboot.target.wants/fbsplash-reboot.service
ln -s ../fbsplash-settty.service $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/multi-user.target.wants/fbsplash-settty.service
ln -s ../fbsplash-exit.service $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/multi-user.target.wants/fbsplash-exit.service
ln -s ../fbsplash-start.service $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system/sysinit.target.wants/fbsplash-start.service

magic_rpm_clean.sh

%clean
%{__rm} -rf %{name}-%{version}
%{__rm} -rf "%{buildroot}"

%files
%defattr(-,root,root)
%{_prefix}/lib/systemd/system/*.service
%{_prefix}/lib/systemd/system/*wants/*.service
%{_sbindir}/splash.ctl

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.01-3
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 0.01-2
- 为 Magic 3.0 重建

* Sat Jun 16 2012 Jiang Tao <jiangtao9999@163.com> - 0.01-1
- Build for Magic Linux 3.0
