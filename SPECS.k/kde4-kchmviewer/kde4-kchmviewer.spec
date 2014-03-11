%define real_name      kchmviewer
%define version    6.0
%define release    1%{?dist}
%define _dir		build-5.1

%define prefix     /usr
%define sysconfdir /etc

Summary:	A CHM viewer program for KDE.
Summary(zh_CN.UTF-8):	KDE下的一个CHM查看程序
Name:	kde4-%{real_name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Applications/File
Group(zh_CN.UTF-8):	应用程序/文件
Url:		http://www.ulduzsoft.com/linux/kchmviewer/
Source0:	http://downloads.sourceforge.net/project/kchmviewer/kchmviewer/%{version}/%{real_name}-%{version}.tar.gz
Source1:	kchmviewer_zh_CN.po
Source2:	kchmviewer.desktop
Packager:	sejishikong <sejishikong@263.net>
BuildRoot:	%{_tmppath}/%{name}--buildroot

%description
KchmViewer is a chm (MS HTML help file format) viewer, written in C++. Unlike most existing CHM viewers for Unix, it uses Trolltech Qt widget library, and does not depend on KDE or Gnome. However, it may be compiled with full KDE support, including KDE widgets and KIO/KHTML. 

%description -l zh_CN.UTF-8
Kchmviewer是一个chm（微软HTML帮助文件格式）查看器，用C++写成。和许多在Unix
下已有的CHM查看器不一样，它使用了Trolltech Qt组件库，不依赖KDE或Gnome，不过，
它可以编译成完全的KDE支持，包括KDE组件和KIO/KHTML。

%prep
rm -rf %{buildroot}
%setup -q -n %{real_name}-%{version}

%build
qmake
%cmake_kde4
make
rm -rf $RPM_BUILD_ROOT
%install
make install DESTDIR=%{buildroot}
cp -f %{SOURCE2} %{buildroot}%{kde4_xdgappsdir}
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{kde4_bindir}/*
%{kde4_xdgappsdir}/*
%{kde4_localedir}/*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 5.3-3
- 为 Magic 3.0 重建

* Mon Dec 19 2011 Liu Di <liudidi@gmail.com> - 5.3-2
- 为 Magic 3.0 重建

