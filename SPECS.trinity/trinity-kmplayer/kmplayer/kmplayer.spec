%define		version 0.10.0c
%define		testver %{nil}
%define		with_gstreamer 0
%define		with_xine 1
%define		with_mplayer 1

Name:		kmplayer
Version:		%{version}
Release:	1%{?dist}
Summary:	A multimedia mplayer/gstreamer/libxine frontend for KDE
Summary(zh_CN.UTF-8): KDE 下的 mplayer/gstreamer/libxine 的媒体播放器前端
License:		GPL
Group:		Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
Url:		http://kmplayer.kde.org/
Source:		http://kmplayer.kde.org/pkgs/%{name}-%{version}.tar.bz2
Patch1:		kmplayer-0.10.0c-admin.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildRequires: kdelibs-devel
%if %with_gstreamer
BuildRequires: gstreamer-devel
BuildRequires: gstreamer-plugins-base-devel
%endif
%if %with_xine
BuildRequires: xine-lib-devel
%endif
%if %with_mplayer
Requires:	mplayer
%endif



%description
KMPlayer can play all the audio/video supported by mplayer/libxine/Gstreamer from local
file or url, be embedded inside Konqueror and KHTML and play DVD's.

%description -l zh_CN.UTF-8
KDE 下的 mplayer/gstreamer/libxine 的媒体播放器前端。

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
chmod 777 admin/*

%build
unset QTDIR && . %{_sysconfdir}/profile.d/qt.sh
# work around an improper ${kdelibsuff}
make -f admin/Makefile.common
export QTLIB=${QTDIR}/lib QTINC=${QTDIR}/include
./configure --prefix=%{_prefix} --disable-debug --enable-shared \
	--disable-static --disable-rpath \
	--disable-embedded --with-xinerama \
%if ! %{with_gstreamer}
	--without-gstreamer \
%endif
	--enable-final
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lX11/g' src/Makefile
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# conflicts with file from package kdelibs
rm -f %{buildroot}%{_datadir}/mimelnk/application/x-mplayer2.desktop
magic_rpm_clean.sh

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README
%{_bindir}/*
%{_libdir}/libk*
%{_libdir}/trinity/*
%{_libdir}/libtdeinit_kmplayer.*
#%{_datadir}/applications/kde/kmplayer.desktop
%{_datadir}


%changelog
* Fri Aug 24 2007 kde <athena_star {at} 163 {dot} com> - 0.10.0-pre2-1mgc
- init the spec file
