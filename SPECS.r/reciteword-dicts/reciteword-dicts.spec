%define ver      0.8.2
%define rel      1%{?dist}
%define prefix   /usr

Summary: reciteword's dict data files
Summary(zh_CN.UTF-8): 轻轻松松背单词的字典数据文件
Name: reciteword-dicts
Version: %ver
Release: %rel.3
License: GPL
Group: Applications/Productivity
Group(zh_CN.UTF-8): 应用程序/生产力
Source: reciteword-dicts-%{ver}.tar.bz2
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildArchitectures: noarch


URL: http://reciteword.cosoft.org.cn

Requires: reciteword >= 0.8.2

%description
ReciteWord's dict data files.

%description -l zh_CN.UTF-8
轻轻松松背单词的字典数据文件。

%prep
%setup -n dicts

%build
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/reciteword/dicts
cp -f xdicten.idx xdict.lib $RPM_BUILD_ROOT%{prefix}/share/reciteword/dicts/
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)

%{prefix}/share/reciteword/dicts
