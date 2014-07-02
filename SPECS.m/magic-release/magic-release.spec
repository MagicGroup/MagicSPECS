Summary: magic-release
Summary(zh_CN.UTF-8): MagicLinux的发行文件
Name: magic-release
Version: 3.0
Release: 11%{?dist}
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
%define dist_version 3

%define rpm_macros_dir %{_rpmconfigdir}/macros.d
%define release_name Kaibao
%define bug_version Kaibao

%prep
%setup -q
#%patch

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
echo "Magic release %{version} (%{release_name})" > $RPM_BUILD_ROOT/etc/magic-release
echo "cpe:/o:magicgroup:magic:%{version}" > $RPM_BUILD_ROOT/etc/system-release-cpe
cp -p $RPM_BUILD_ROOT/etc/magic-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/etc/issue
cp -p $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue
ln -s magic-release $RPM_BUILD_ROOT/etc/system-release

cat << EOF >>$RPM_BUILD_ROOT/etc/os-release
NAME=Magic
VERSION="%{dist_version} (%{release_name})"
ID=magic
VERSION_ID=%{dist_version}
PRETTY_NAME="Magic %{dist_version} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:magicgroup:magic:%{dist_version}"
HOME_URL="http://www.magiclinux.org/"
BUG_REPORT_URL="https://www.magiclinux.org/bugs/"
REDHAT_BUGZILLA_PRODUCT="Magic"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{bug_version}
REDHAT_SUPPORT_PRODUCT="Magic"
REDHAT_SUPPORT_PRODUCT_VERSION=%{bug_version}
EOF

install -D -m 644 releasedoc/GPL %{buildroot}%{_docdir}/magic-release-%{version}-Kaibao/GPL

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
* Wed Jul 02 2014 Liu Di <liudidi@gmail.com> - 3.0-11
- 为 Magic 3.0 重建

* Tue Jul 01 2014 Liu Di <liudidi@gmail.com> - 3.0-10
- 为 Magic 3.0 重建

* Mon May 26 2014 Liu Di <liudidi@gmail.com> - 3.0-9
- 为 Magic 3.0 重建

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
