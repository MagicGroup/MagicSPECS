%define realname qsopcast
Name:		qsopcast-qt4
Group:		Applications/Internet
Group(zh_CN.UTF-8):   应用程序/互联网
Version:	0.4.85
Release:	2%{?dist}
License:	GPL v3
Summary:	A P2P Stream program
Summary(zh_CN.UTF-8): P2P 流媒体程序
URL:		http://www.sopcast.org
Source0:	%{realname}-%{version}.tar.gz
Patch1:		qsopcast-0.4.85-qstring.patch
Patch2:		qsopcast-0.4.85-unistd.patch

BuildRoot:	%{_tmppath}/%{name}-root

Requires:	sopcast
#pplive
#Requires: xpplive
#pps
#Requires: libpps
#Requires: xpps

%description
A P2P Stream program

%description -l zh_CN.UTF-8
P2P 的流媒体直播系统。

%prep

%setup -q -n %{realname}-%{version}
%patch1 -p1
%patch2 -p1

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=release ..

make %{?smp_flags}

%install
rm -rf $RPM_BUILD_ROOT
cd build
make DESTDIR=%{buildroot} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root)
%{_bindir}/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_datadir}/apps/qsopcast/*

%changelog
* Thu Jan 03 2013 Liu Di <liudidi@gmail.com> - 0.4.85-2
- 为 Magic 3.0 重建

* Thu May 07 2009 Liu Di <liudidi@gmail.com> - 0.3.6-1
- 与 sopcast 分开打包
- 升级到 0.3.6

* Tue Nov 28 2006 Liu Di <liudidi@gmail.com> - 0.2.4-4mgc
- update sp-sc to 1.0.1

* Mon Oct 23 2006 Liu Di <liudidi@gmail.com> - 0.2.4-1mgc
- initial RPM
