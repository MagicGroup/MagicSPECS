#
# spec file for package kmplayer (version R14)
#
# Copyright (c) 2014 Trinity Desktop Environment
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg qsopcast
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.3.6
Release:	%{?!preversion:8}%{?preversion:7_%{preversion}}%{?dist}%{?_variant}.1
Summary:        A P2P Stream program
Summary(zh_CN.UTF-8): P2P流媒体程序
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL:		http://www.trinitydesktop.org/
#URL:		http://kmplayer.kde.org

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{version}%{?preversion:~%{preversion}}.tar.gz
Source4:	sopcast.xpm

BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	libtool

%description
A P2P Stream program

%description -l zh_CN.UTF-8
SoP 是 Streaming over P2P 的缩写， SopCast是一个基于 P2P 的流媒体直播系统，
其核心是由 SopCast 开发组自己定义和开发的一种通讯协议，
称之为 sop:// ，也可以称为sop 技术。我们的目的是使世界
上任何人都可以以一种非常简单的方式在Internet上建立起一个自己的个人媒体世界。

##########

%prep
%setup -q -n %{name}-%{version}%{?preversion:~%{preversion}}

%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig:${PKG_CONFIG_PATH}"
export kde_confdir="%{tde_confdir}"

pushd src
/usr/bin/tqmake
/usr/bin/tqlrelease qsopcast.pro
%__make %{?_smp_mflags} || %__make
popd

%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}

mkdir -p %{buildroot}%{tde_bindir}
install -m 755 src/qsopcast %{buildroot}%{tde_bindir}/qsopcast
install -D -m 644 src/language/language_zh.qm %{buildroot}%{tde_datadir}/locale/zh_CN/LC_MESSAGES/language_zh_CN.qm
mkdir -p %{buildroot}%{tde_datadir}/pixmaps
install -m 644 %{SOURCE4} %{buildroot}%{tde_datadir}/pixmaps/qsopcast.xpm

#Install application link for X-Windows
mkdir -p %{buildroot}%{tde_appdir}
cat > cat > %{buildroot}%{tde_appdir}/sopcast.desktop <<EOF
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
%__rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{tde_bindir}/*
%{tde_datadir}/*


%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:0.3.6-8.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.10.0c-1
- Initial release for TDE 14.0.0
