#define debug_package %{nil}

%define git 1
%define gitdate 20130426

%define JAVA 1

Name: xbmc
Version: 12.0
%if %{git}
Release: 0.git%{gitdate}%{?dist}
%else
Release: 1%{?dist}
%endif
URL: http://www.xbmc.org
%if %{git}
Source: %{name}-git%{gitdate}.tar.xz
%else
Source: %{name}-%{version}.tar.bz2
%endif
Source1: make_xbmc_git_package.sh
Patch1:	xbmc-git20130114-samba4.patch
Buildroot: %{_tmppath}/%{name}-%{version}
Summary: Xbox Media Center Linux port
Summary(zh_CN): Xbox 媒体中心的 Linux 移植
License: GPL
Group: Applications/Multimedia
Group(zh_CN): 应用程序/多媒体
BuildRequires: SDL-devel
BuildRequires: SDL_image-devel
BuildRequires: SDL_mixer-devel
BuildRequires: fontconfig-devel
BuildRequires: fribidi-devel
BuildRequires: glibc-devel
BuildRequires: libmpeg2
BuildRequires: libass-devel
BuildRequires: libva-devel
BuildRequires: libvdpau-devel
BuildRequires: yajl-devel
BuildRequires: libsamplerate-devel
BuildRequires: libnfs-devel
BuildRequires: libcrystalhd
BuildRequires: libcec-devel
BuildRequires: afpfs-ng-devel
BuildRequires: rtmpdump-devel
#BuildRequires: hal-devel
BuildRequires: glew-devel
BuildRequires: libstdc++-devel
BuildRequires: glib2-devel
BuildRequires: libjpeg-devel
BuildRequires: libogg-devel
BuildRequires: libpng-devel
BuildRequires: libstdc++-devel
BuildRequires: e2fsprogs-devel
BuildRequires: libvorbis-devel
BuildRequires: lzo-devel
BuildRequires: libmms-devel
BuildRequires: pcre-devel
BuildRequires: zlib-devel
BuildRequires: tre-devel
BuildRequires: boost-devel
BuildRequires: bzip2-devel
BuildRequires: freetype-devel
BuildRequires: libXinerama-devel
BuildRequires: fontconfig-devel
BuildRequires: mysql-libs
BuildRequires: mysql-devel
BuildRequires: jasper-devel
BuildRequires: faac-devel
BuildRequires: enca-devel
BuildRequires: cmake
BuildRequires: gperf
BuildRequires: nasm
BuildRequires: libXmu-devel
BuildRequires: pcre-devel
BuildRequires: gcc-c++
BuildRequires: sqlite-devel
BuildRequires: curl-devel
BuildRequires: libcdio-devel
BuildRequires: libmicrohttpd-devel
BuildRequires: flex
BuildRequires: tinyxml-devel
BuildRequires: jdk
Requires: libvorbis >= 1.2
Requires: libmad >= 0.15
Requires: libogg >= 1.1


%description
XBMC media center is a free cross-platform media-player
jukebox and entertainment hub. XBMC is open source (GPL)
software available for Linux, Mac OS X, Microsoft Windows
operating-system, and the Xbox game-console. XBMC can
play a very complete spectrum of of multimedia formats,
and featuring playlist, audio visualizations, slideshow,
and weather forecast functions, together with a multitude
of third-party plugins. Originally developed as XBMP
(XBox Media Player) for the first-generation Xbox game
console in 2002, XBMC has eventually become a complete
graphical user interface replacement for the original Xbox
Dashboard, and it is currently also being ported to run
natively under Linux, Mac OS X, and Microsoft Window
 operating-system. This, The XBMC Project is also known
as "XBMC Media Center" or simply "XBMC").

%description -l zh_CN
Xbox 媒体中心的 Linux 移植。



%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q
%endif
%patch1 -p1

%ifarch x86_64
CFLAGS=`pkg-config --cflags smbclient`
CFLAGS="-I/usr/lib64/dbus-1.0/include -I/usr/lib64/glib-2.0/include $CFLAGS"
LIBS="-L/usr/lib64/mysql $LIBS"
export LIBS
export CFLAGS
%else
CFLAGS=`pkg-config --cflags smbclient`
LIBS="-L/usr/lib/mysql $LIBS"
export LIBS
export CFLAGS
%endif
./bootstrap
%configure --with-system-libtool

%build
%ifarch x86_64
CFLAGS="-I/usr/lib64/dbus-1.0/include -I/usr/lib64/glib-2.0/include" make
%else
make %{?_smp_mflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
#rm -rf $RPM_BUILD_ROOT/usr/share/xbmc/system/players/dvdplayer/*osx*
magic_rpm_clean.sh

%clean

%files
%defattr(-,root,root)
%{_bindir}/xbmc
%{_bindir}/xbmc-standalone
%dir %{_datadir}/xbmc
%{_datadir}/xbmc/*
%{_datadir}/xsessions/XBMC.desktop
%{_datadir}/applications/xbmc.desktop
%dir %{_libdir}/xbmc
%{_libdir}/xbmc/*
%{_docdir}/xbmc/*
%{_datadir}/icons/hicolor/256x256/apps/xbmc.png
%{_datadir}/icons/hicolor/48x48/apps/xbmc.png

%changelog

