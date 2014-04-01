%define name ddcprobe
%define version 1.2.25
%define release 9%{?dist}

Name:		%{name}
Summary:	DDC Monitor Detection Tool
Summary(zh_CN.UTF-8): DDC 显示器检测工具
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Applications/Tools
Group(zh_CN.UTF-8): 应用程序/工具
Source:		%{name}-%{version}.tar.bz2
Packager:	Yuichiro Nakada <berry@po.yui.mine.nu>
Buildroot:	%{_tmppath}/%{name}-%{version}

BuildArchitectures: i586

%description
This package installs ddcprobe and ddcxinfo for detecting monitor configuration
values using the DDC protocol.

%description -l zh_CN.UTF-8
这个包包含了 ddcprobe 和 ddcxinfo，可以通过 DDC 协议来检测显示器的配置。

## Setup Section
%prep
%setup -q

## Build Section
%build
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT

#CFLAGS="$RPM_OPT_FLAGS" \
#./configure --prefix=/opt/berry
make

## Install Section
%install
strip ddcprobe
strip ddcxinfo-berry
mkdir -p %{buildroot}/opt/berry
install -m 755 ddcprobe %{buildroot}/opt/berry
install -m 755 ddcxinfo-berry %{buildroot}/opt/berry/ddcxinfo
magic_rpm_clean.sh

## Clean Section
%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

## Files Section
%files
%defattr (-,root,root)
/opt/berry/ddc*

## change log
%changelog
* Wed Jun 28 2009 Yuichiro Nakada <berry@po.yui.mine.nu>
- Added PROT_EXEC for 2.6.28
* Mon Nov 17 2008 Yuichiro Nakada <berry@po.yui.mine.nu>
- Added modelines for 1280x800
* Sat Aug 30 2008 Yuichiro Nakada <berry@po.yui.mine.nu>
- Added modelines for 1024x600
- Added modelines for 800x480 @ 60.00 Hz
* Tue Feb 28 2006 Yuichiro Nakada <berry@po.yui.mine.nu>
- Added VESA timing to vesamode.c for X60's 1024x768 @ 54.00 Hz
* Tue Feb 28 2006 Yuichiro Nakada <berry@po.yui.mine.nu>
- Added modelines for 1920x1200 @ 60.00 Hz (GTF)
* Sat Feb 11 2006 Yuichiro Nakada <berry@po.yui.mine.nu>
- Update to kudzu-1.2.25
* Sun May 22 2005 Yuichiro Nakada <berry@po.yui.mine.nu>
- Update to ddcxinfo-knoppix.c 1.1.1.1
* Thu Nov 27 2003 Yuichiro Nakada <berry@po.yui.mine.nu>
- Update to kudzu-1.1.34
- Update to ddcxinfo-knoppix_0.6-5.tar.gz
* Mon Sep 8 2003 Yuichiro Nakada <berry@po.yui.mine.nu>
- Update to ddcxinfo-knoppix_0.6-4.tar.gz
* Mon Sep 8 2003 Yuichiro Nakada <berry@po.yui.mine.nu>
- Update to ddcxinfo-knoppix_0.5.1-1.tar.gz
* Mon Sep 8 2003 Yuichiro Nakada <berry@po.yui.mine.nu>
- Update to ddcxinfo-knoppix_0.5.1-1.tar.gz
* Fri May 23 2003 Yuichiro Nakada <berry@po.yui.mine.nu>
- Added ddcxinfo-berry from ddcxinfo-knoppix_0.5-5.tar.gz
* Mon Apr 28 2003 Yuichiro Nakada <berry@po.yui.mine.nu>
- Strip Binary Code
* Thu Apr 17 2003 Yuichiro Nakada <berry@po.yui.mine.nu>
- Create for Berry Linux
