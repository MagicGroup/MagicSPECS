Summary: Graphical FTP client for the K Desktop Environment.
Summary(zh_CN.UTF-8): K桌面环境（KDE）下的图形FTP客户端
Name: kuftp
Version: 1.5.0
Release: 2%{?dist}
License: GPL
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
URL: http://kuftp.sourceforge.net/

Source0: %{name}-%{version}.tar.bz2
#only for Magic & zh_CN.UTF-8
Patch0:	 kuftp-1.5.0-zh.patch
Patch1: kuftp-1.5.0-defaultencoding.patch
Patch2:	kuftp-1.5.0-admin.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: qt-devel >= 3.3.2, kdelibs-devel >= 3.2.0, openssl-devel >= 0.9.7
BuildRequires: libpng-devel, libart_lgpl-devel, desktop-file-utils, gcc-c++
BuildRequires: arts-devel, libjpeg-devel, gettext, zlib-devel

%description
KuFTP is a graphical FTP client for the K Desktop Environment.

Most notable features is Tab Sessions like Konqueror or Firefox,
that is,you can have multiple simultaneous FTP session in tabs. 
Other features like bookmark manager,queue manager, multi charsets 
support,proxy support,speed limit and some small nifty features 
are currently available in the latest version

%description -l zh_CN.UTF-8
KuFTP是一个KDE下的图形FTP客户端。

像其它的标签会话，比如 Konqueror 和 Firefox，你可以在标签中连接多
个 FTP 会话。其它的特性包括站点管理器，队列管理器，多字符支持，代
理支持，速度限制和其它一些小的特性，在最新版本中都支持。
的书签系统，也内建了零配置站点搜索支持。

%prep
%setup -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
chmod 777 admin/*

%build
make -f admin/Makefile.common
%configure
make

%install
%{__rm} -rf %{buildroot}
%makeinstall

magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 755)
#%doc %{_docdir}/HTML/en/kftpgrabber/
%{_bindir}/kuftp
%{_libdir}/libkuftpbookmarks.a
%{_datadir}/applnk/Utilities/kuftp.desktop
%{_datadir}/apps/kuftp/kuftpui.rc
%{_datadir}/doc/*
%{_datadir}/icons/*
%{_datadir}/locale/*
 
%changelog
* Mon Jul 21 2008 Liu Di <liudidi@gmail.com> - 1.5.0-2mgc
- 添加了默认编码的补丁，现在默认的服务器编译是 GB18030

* Tue Jul 15 2008 Liu Di <liudidi@gmail.com> - 1.5.0-1mgc
- 首次为 Magic 打包
- 添加了针对中文 .desktop 文件的补丁
