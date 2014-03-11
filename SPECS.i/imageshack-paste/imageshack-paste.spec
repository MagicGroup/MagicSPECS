%define version 0.0.2
%define release 3%{?dist}

Name: imageshack-paste
Summary: Script to paste pictures to imageshack
Summary(zh_CN): 方便的贴图脚本
Version: %{version}
Release: %{release}
License: GPL
Group: User Interface/Desktops
Group(zh_CN): 用户界面/桌面
Url: http://bigsnakecat.blogspot.com
Source0: %{name}-%{version}.tar.gz
#Source1: imageshack-paste.desktop
Source2: imageshack-paste-konqueror.desktop
Source3: imageshack-upurl
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Packager: Ni Hui <shuizhuyuanluo@126.com>
Requires: kdebase

%description
Script to paste pictures to imageshack website and you will get the picture URLs.

%description -l zh_CN
方便的贴图脚本，截图 > 贴图 > 获得 imageshack 提供的 url。

%prep
%setup -q -n %{name}

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -m 755 %{_builddir}/%{name}/* %{buildroot}%{_datadir}/%{name}
#install -D -m 755 %{SOURCE1} %{buildroot}%{_datadir}/applnk/imageshack-paste.desktop
install -D -m 755 %{SOURCE2} %{buildroot}%{_datadir}/apps/konqueror/servicemenus/imageshack-paste-konqueror.desktop
install -d -m 755 %{buildroot}%{_bindir}
install -m 755 %{SOURCE3} %{buildroot}%{_bindir}

cd %{buildroot}%{_bindir}
ln -s ../share/%{name}/imageshack ./imageshack
#ln -s ../share/%{name}/screenshot ./screenshot

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%{_bindir}
%{_datadir}

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.0.2-3
- 为 Magic 3.0 重建

* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 0.0.2-2
- 为 Magic 3.0 重建

* Tue Sep 18 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.0.2-1mgc
- 更新主 perl 脚本，添加右键菜单功能

* Sun Jul 29 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.0.1-1mgc
- 首次生成 rpm 包
