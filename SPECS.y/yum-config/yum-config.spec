%define desktop_vendor magicgroup

%define _rc %{nil}

Summary: yum's config file
Summary(zh_CN.UTF-8): yum 的配置文件
Name: yum-config
Version: 2.5
Release: 2%{?dist}
License: GPL
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://www.magiclinux.org/

Source0: all.repo
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Requires: yum

%description
Smart's config files。

%description -l zh_CN.UTF-8
smart 的配置文件。

%prep

%build

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d

install -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/yum.repos.d
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%config(noreplace) %{_sysconfdir}/yum.repos.d

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.5-2
- 为 Magic 3.0 重建

