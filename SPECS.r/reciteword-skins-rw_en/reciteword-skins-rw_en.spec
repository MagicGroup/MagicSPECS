%define ver      0.8.2
%define rel      1%{?dist}
%define prefix   /usr

Summary: reciteword's rw_en skin.
Summary(zh_CN.UTF-8): 轻轻松松背单词的英文皮肤
Name: reciteword-skins-rw_en
Version: %ver
Release: 3%{?dist}
License: GPL
Group: Applications/Productivity
Group(zh_CN.UTF-8): 应用程序/生产力
Source: reciteword-skins-rw_en-%{ver}.tar.bz2
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildArchitectures: noarch


URL: http://reciteword.cosoft.org.cn

Requires: reciteword >= 0.8.2

%description
ReciteWord's rw_en skin files.

%description -l zh_CN.UTF-8
轻轻松松背单词的英文皮肤。

%prep
%setup -n rw_en

%build
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/reciteword/skins/rw_en
cp -rf * $RPM_BUILD_ROOT%{prefix}/share/reciteword/skins/rw_en
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)

%{prefix}/share/reciteword/skins/rw_en/*
