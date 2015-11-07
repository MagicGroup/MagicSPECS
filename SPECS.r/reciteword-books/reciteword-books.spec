%define ver      0.8.5
%define rel      1%{?dist}
%define prefix   /usr

Summary: reciteword's book files
Summary(zh_CN.UTF-8): 轻轻松松背单词的书籍文件
Name: reciteword-books
Version: %ver
Release: %rel.3
License: GPL
Group: Applications/Productivity
Group(zh_CN.UTF-8): 应用程序/生产力
Source: reciteword-books-%{ver}.tar.bz2
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildArchitectures: noarch
Requires: reciteword

URL: http://reciteword.cosoft.org.cn

Requires: reciteword >= 0.8.3

%description
ReciteWord's book files.

%description -l zh_CN.UTF-8
轻轻松松背单词的书籍文件。

%prep
%setup -n books

%build
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/reciteword/books
cp -rf * $RPM_BUILD_ROOT%{prefix}/share/reciteword/books/
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)

%{prefix}/share/reciteword/books

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.8.5-1.3
- 为 Magic 3.0 重建

* Sat Sep 12 2015 Liu Di <liudidi@gmail.com> - 0.8.5-1.2
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.8.4-1.1
- 为 Magic 3.0 重建

