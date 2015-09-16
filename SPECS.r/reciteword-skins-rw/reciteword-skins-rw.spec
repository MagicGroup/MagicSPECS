%define ver      0.8.2
%define rel      1%{?dist}
%define prefix   /usr

Summary: reciteword's rw skin.
Summary(zh_CN.UTF-8): 轻轻松松背单词的皮肤
Name: reciteword-skins-rw
Version: %ver
Release: 2%{?dist}
License: GPL
Group: Applications/Productivity
Group(zh_CN.UTF-8): 应用程序/生产力
Source: reciteword-skins-rw-%{ver}.tar.bz2
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildArchitectures: noarch

URL: http://reciteword.cosoft.org.cn

Requires: reciteword >= 0.8.2

%description
ReciteWord's rw skin files.

%description -l zh_CN.UTF-8
轻轻松松背单词的皮肤。

%prep
%setup -n rw

%build
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/reciteword/skins/rw
cp -rf * $RPM_BUILD_ROOT%{prefix}/share/reciteword/skins/rw
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)

%{prefix}/share/reciteword/skins/rw/*
