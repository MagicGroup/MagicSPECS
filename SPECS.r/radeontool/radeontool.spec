Name:           radeontool
Version:        1.5
Release:        6%{?dist}
Summary:        Backlight and video output configuration tool for radeon cards
Summary(zh_CN.UTF-8): radeon 显卡的背光和视频输出配置工具

Group:          System Environment/Base
Group(zh_CN.UTF-8):	系统环境/基本
License:        zlib
URL:            http://fdd.com/software/radeon/
Source0:        http://fdd.com/software/radeon/radeontool-%{version}.tar.gz
Patch20:        radeontool-1.5.diff
Patch21:        radeontool-fix-option-handling.diff
Patch22:        radeontool-get-rid-of-lspci.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  pciutils-devel zlib-devel
# radeontool is included in (some of) these pm-utils releases
Conflicts:      pm-utils <= 0.99.3-11


%description
Radeontool may switch the backlight and external video output on and off.  Use
radeontool at your own risk, it may damage your hardware.

%description -l zh_CN.UTF-8
radeon 显卡的背光和视频输出配置工具

%prep
%setup -q
%patch20 -p0 -b .volatile
%patch21 -p0 -b .options
%patch22 -p0 -b .no-lspci


%build
gcc $RPM_OPT_FLAGS -o radeontool radeontool.c -lpci -lz


%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT

install -D -m 755 radeontool $RPM_BUILD_ROOT/%{_sbindir}/radeontool


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES
%{_sbindir}/radeontool


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.5-6
- 为 Magic 3.0 重建

* Tue Jan 31 2012 Liu Di <liudidi@gmail.com> - 1.5-5
- 为 Magic 3.0 重建


