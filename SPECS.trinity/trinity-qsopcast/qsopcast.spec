Name:		qsopcast
Group:		Applications/Internet
Group(zh_CN.UTF-8):   应用程序/互联网
Version:	0.3.6
Release:	1%{?dist}
License:	GPL
Summary:	A P2P Stream program
Summary(zh_CN.UTF-8): P2P流媒体程序
URL:		http://www.sopcast.org
Source0:	%{name}-%{version}.tar.bz2
#don't need
#Source2:	getchannel
#Source3:        sopcast
Source4:        sopcast.xpm
Patch2:		%{name}-0.3.6-magicconfig.patch
BuildRoot:	%{_tmppath}/%{name}-root

Requires:	sopcast

%description
A P2P Stream program

%description -l zh_CN.UTF-8
SoP 是 Streaming over P2P 的缩写， SopCast是一个基于 P2P 的流媒体直播系统，
其核心是由 SopCast 开发组自己定义和开发的一种通讯协议，
称之为 sop:// ，也可以称为sop 技术。我们的目的是使世界
上任何人都可以以一种非常简单的方式在Internet上建立起一个自己的个人媒体世界。

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q 
%patch2 -p1

%build
pushd src
. /etc/profile.d/qt.sh
/usr/bin/qmake
lrelease qsopcast.pro
%{__make} %{?_smp_mflags}
popd

%install
mkdir -p %{buildroot}/usr/bin
install -m 755 src/qsopcast %{buildroot}%{_bindir}/qsopcast
install -D -m 644 src/language/language_zh.qm %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/language_zh_CN.qm
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/pixmaps/qsopcast.xpm

#Install application link for X-Windows
mkdir -p %{buildroot}%{_datadir}/applications
cat > cat > %{buildroot}%{_datadir}/applications/sopcast.desktop <<EOF
[Desktop Entry]
Name=%{name}
GenericName[zh_CN]=网络电视客户端
Comment[zh_CN]=P2P 的网络电视客户端
Comment=%{summary}
Exec=qsopcast
Icon=%{name}.xpm
Terminal=0
Type=Application
Categories=Application;Network;
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root)
%{_bindir}/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_datadir}/locale/*

%changelog
* Thu May 07 2009 Liu Di <liudidi@gmail.com> - 0.3.6-1
- 与 sopcast 分开打包
- 升级到 0.3.6

* Tue Nov 28 2006 Liu Di <liudidi@gmail.com> - 0.2.4-4mgc
- update sp-sc to 1.0.1

* Mon Oct 23 2006 Liu Di <liudidi@gmail.com> - 0.2.4-1mgc
- initial RPM
