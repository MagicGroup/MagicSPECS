Summary: magic-release
Summary(zh_CN.UTF-8): MagicLinux的发行文件
Name: magic-release
Version: 3.0
Release: 8%{?dist}
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License: GPL
Source: %{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-root
Packager: lovewilliam<williamlovecyl@hotmail.com>
# Following are optional fields
URL: http://www.magiclinux.org
Distribution: Magic Linux
BuildArch: noarch

%description
magic-release
for system Version

%description -l zh_CN.UTF-8
描述系统版本的发行文件

%define fedora_version 21
%define dist_version 30

%define rpm_macros_dir %{_rpmconfigdir}/macros.d

%prep
%setup -q
#%patch

%build

%install
mkdir -p ${RPM_BUILD_ROOT}/etc
cp etc/* ${RPM_BUILD_ROOT}/etc
mkdir -p ${RPM_BUILD_ROOT}/usr/share/doc/magic-release-3.0-Kaibao
cp releasedoc/* ${RPM_BUILD_ROOT}/usr/share/doc/magic-release-3.0-Kaibao
ln -s magic-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s magic-release $RPM_BUILD_ROOT/etc/system-release

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{rpm_macros_dir}
cat >> $RPM_BUILD_ROOT%{rpm_macros_dir}/macros.dist << EOF
# dist macros.

%%fedora                %{fedora_version}
%%magic			%{dist_version}
%%dist          	mgc%{dist_version}
%%fc%{fedora_version}             1
EOF

magic_rpm_clean.sh

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root,-)
%{_sysconfdir}/*
%{_docdir}/magic-release-%{version}-Kaibao/GPL
%{rpm_macros_dir}/*

%changelog
* Thu May 22 2014 Liu Di <liudidi@gmail.com> - 3.0-8
- 为 Magic 3.0 重建

* Thu May 22 2014 Liu Di <liudidi@gmail.com> - 3.0-7
- 为 Magic 3.0 重建

* Thu May 22 2014 Liu Di <liudidi@gmail.com> - 3.0-6
- 调整 rpm 宏定义目录及设置

* Wed Apr 09 2014 Liu Di <liudidi@gmail.com> - 3.0-5
- 修改以符合 LSB 标准

* Fri May 17 2013 Liu Di <liudidi@gmail.com> - 3.0-4
- 重新编译

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.0-3
- 为 Magic 3.0 重建

* Tue Jul 31 2012 Liu Di <liudidi@gmail.com> - 3.0-2
- 为 Magic 3.0 重建

* Fri Apr 22 2011 Liu Di <liudidi@gmail.com> - 3.0-0.1
- 2.9999

* Fri Jul 08 2005 lovewilliam <williamlovecyl@hotmail.com>
- 2.0

* Tue Jul 05 2005 lovewilliam <williamlovecyl@hotmail.com>
- update to 1.9 genius

* Sat Jun 04 2005  lovewilliam<williamlovecyl@hotmail.com>
- Initial spec
