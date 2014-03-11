%define desktop_vendor magicgroup

%define _rc %{nil}
%define mgcver 3.0

Summary: smart's config file
Summary(zh_CN.UTF-8): smart 的配置文件
Name: smart-config
Version: 1.2
Release: 10%{?dist}
License: GPL
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://www.smartpm.org/

BuildRoot: %{_tmppath}/%{name}-%{version}-root

Requires: smart >= %{version}

%description
Smart's config files。

%description -l zh_CN.UTF-8
smart 的配置文件。

%prep

name='Magic Linux';version='%{mgcver}'

%{__cat} >rpm-db.channel<<EOF
[rpm-db]
name = RPM Database on this system
type = rpm-sys
EOF

%{__cat} >all.channel<<EOF
[all-magiclinux3]
type = apt-rpm
name = $name $version APT All Repository from magiclinux0
baseurl = http://apt.linuxfans.org/magic/3.0/%{_target_cpu}
components = 3 9 a b c d e f g h i j k l m n o p q r s t u v w x y z A C D F G I J M N O P R S T W X
 
[all-321211]
type = apt-rpm
name = $name $version APT All Repository from magiclinux0
baseurl = http://www.321211.net/magic/3.0/%{_target_cpu}
components = 3 9 a b c d e f g h i j k l m n o p q r s t u v w x y z A C D F G I J M N O P R S T W X
EOF

%build

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/smart/channels/

%{__cp} -apv *.channel %{buildroot}%{_sysconfdir}/smart/channels/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%config(noreplace) %{_sysconfdir}/smart/channels/

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.2-8
- 为 Magic 3.0 重建

* Tue Dec 18 2007 Liu Di <liudidi@gmail.com> - 0.5%{mgcver}mgc
- update to magic %{mgcver} config

* Fri Apr 06 2007 Liu Di <liudidi@gmail.com> - 0.50-1mgc
- first spec
