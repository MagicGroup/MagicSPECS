Name:          qmmp
Version:	0.9.3
Release:	2%{?dist}
Summary:        A qt4 based media player similar to xmms
Summary(zh_CN): 基于 qt4 的类似 xmms 的媒体播放器

Group:         Applications/Multimedia
Group(zh_CN):	应用程序/多媒体
License:       GPLv2
URL:           http://qmmp.ylsoftware.com

Source0:       http://qmmp.ylsoftware.com/files/qmmp-%{version}.tar.bz2
Source1:	     skins.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  qt4-devel

%description
beep-media-player  is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

%description -l zh_CN
基于 qt4 的类似 xmms 的媒体播放器。

%prep
%setup -q -n  qmmp-%{version}
%build

install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	..

make

%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/qmmp
mkdir -p $RPM_BUILD_ROOT/usr/share/applications/
tar xvf %{SOURCE1} -C $RPM_BUILD_ROOT/usr/share/qmmp

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
#devel
%{_includedir}/qmmp/*.h
%{_includedir}/qmmpui/*.h
%{_libdir}/libqmmp.so
%{_libdir}/libqmmpui.so
%{_libdir}/pkgconfig/qmmp*.pc
##
%{_libdir}/libqmmp.so.*
%{_libdir}/libqmmpui.so.*
%{_bindir}/qmmp
%{_libdir}/qmmp/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/qmmp*
%{_datadir}/qmmp/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.9.3-2
- 更新到 0.9.3

* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 0.9.1-2
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 0.9.1-1
- 更新到 0.9.1

* Tue Jan 15 2013 Liu Di <liudidi@gmail.com> - 0.6.5-2
- 为 Magic 3.0 重建

