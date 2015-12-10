%define desktop_vendor magicgroup

%define _rc %{nil}

Summary: yum's config file
Summary(zh_CN.UTF-8): yum 的配置文件
Name: yum-config
Version: 3.0
Release: 7%{?dist}
License: GPL
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://www.magiclinux.org/

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

%ifarch x86_64
FILESUFFIX=x64
URLSUFFIX=x86_64
%endif

%ifarch %{ix86}
FILESUFFIX=x86
URLSUFFIX=i686
%endif

%ifarch mips64el
FILESUFFIX=mips64el
URLSUFFIIX=mips64el
%endif

cat > %{buildroot}%{_sysconfdir}/yum.repos.d/all_$FILESUFFIX.repo << EOF
[all$FILESUFFIX]
name=Magic-%{version} - All$FILESUFFIX
repo=all$FILESUFFIX
baseurl=http://apt.linuxfans.org/magic/3.0/$URLSUFFIX
gpgcheck=0
EOF

magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%config(noreplace) %{_sysconfdir}/yum.repos.d

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 3.0-7
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 3.0-6
- 为 Magic 3.0 重建

* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 3.0-5
- 为 Magic 3.0 重建

* Mon May 26 2014 Liu Di <liudidi@gmail.com> - 3.0-4
- 为 Magic 3.0 重建

* Mon May 26 2014 Liu Di <liudidi@gmail.com> - 3.0-3
- 为 Magic 3.0 重建

* Mon May 26 2014 Liu Di <liudidi@gmail.com> - 3.0-2
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.5-2
- 为 Magic 3.0 重建

