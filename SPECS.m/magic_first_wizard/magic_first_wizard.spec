Summary: Networking manager tools
Summary(zh_CN.UTF-8): 一个网络设置工具
Name: magic_first_wizard
Version: 0.0.2
Release: 4%{?dist}
License: GPL+
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL: http://www.linuxfans.org/
Source0: %{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Netmanager Tools。

Author:
	nihui
	zy_sunshine

%description -l zh_CN.UTF-8
一个简单的有线网络管理工具。

%prep
%setup -q

%build
qmake-qt4
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{name} %{buildroot}%{_bindir}
install -m 755 magicfirstrun %{buildroot}/%{_bindir}

mkdir -p %{buildroot}/opt/kde4/share/autostart
install -m 644 magic_first_wizard.desktop %{buildroot}/opt/kde4/share/autostart

mkdir -p %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES
install -m 644 language/zh_CN/LC_MESSAGES/magic_first_wizard.mo %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -m 644 magic_first_wizard.png %{buildroot}%{_datadir}/pixmaps
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post

%preun

%postun

%files
%defattr(-,root,root)
%{_bindir}/magic_first_wizard
%{_bindir}/magicfirstrun
/opt/kde4/share/autostart/magic_first_wizard.desktop
%{_datadir}/locale/zh_CN/LC_MESSAGES/magic_first_wizard.mo
%{_datadir}/pixmaps/magic_first_wizard.png

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.0.2-4
- 为 Magic 3.0 重建

* Fri Apr 30 2010 zy_sunshine <zy.netsec@gmail.com> - 0.0.2
- 将全局静态变量改为类静态变量
- 添加了QProcessBar以表示重启网卡的执行状态, 测试阶段
