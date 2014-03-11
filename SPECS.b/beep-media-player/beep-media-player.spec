Name:          beep-media-player
Version:        0.9.7.1
Release:        4%{?dist}
Summary:        A GTK2 based media player similar to xmms
Summary(zh_CN): 基于 GTK2 的类似 xmms 的媒体播放器

Group:         Applications/Multimedia
Group(zh_CN):	应用程序/多媒体
License:       GPLv2
URL:             http://audacious-media-player.org/

Source0:       bmp-%{version}.tar.gz
Source1:	     Skins.tar.gz
Patch0:		bmp-0.9.7.1-gtk2.patch
Patch1: 	bmp-0.9.7.1-gmodule.patch
Patch2:		bmp-0.9.7.1-lm.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gtk2-devel >= 2.6

%description
beep-media-player  is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

%description -l zh_CN
基于 GTK2 的类似 xmms 的媒体播放器。

%prep
%setup -q -n bmp-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_datadir}/bmp/Skins/
tar xvf %{SOURCE1} -C $RPM_BUILD_ROOT%{_datadir}/bmp/
magic_rpm_clean.sh
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/ldconfig

%postun
/usr/sbin/ldconfig

%files 
%{_bindir}/*
%{_libdir}/bmp/*
%{_libdir}/lib*.so*
%{_datadir}/*
%{_includedir}/*
%{_libdir}/pkgconfig/bmp.pc

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.9.7.1-4
- 为 Magic 3.0 重建

* Fri Nov 02 2012 Liu Di <liudidi@gmail.com> - 0.9.7.1-3
- 为 Magic 3.0 重建

* Wed Nov 02 2011 Liu Di <liudidi@gmail.com> - 0.9.7.1-2
- 为 Magic 3.0 重建 
- *注意*：这是此软件的最后一个版本
