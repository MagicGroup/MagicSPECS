#define debug_package %{nil}

%define git 0
%define gitdate 20130426

%define JAVA 1

%define relname Isengard

#undefine _hardened_build

Name: kodi
Version:	15.2
%if %{git}
Release:	4%{?dist}
%else
Release:	4%{?dist}
%endif
URL: http://www.xbmc.org
%if %{git}
Source: %{name}-git%{gitdate}.tar.xz
%else
Source: https://github.com/xbmc/xbmc/archive/%{version}-%{relname}.tar.gz
%endif
Source1: make_kodi_git_package.sh
Buildroot: %{_tmppath}/%{name}-%{version}
Summary: Xbox Media Center Linux port
Summary(zh_CN): Xbox 媒体中心的 Linux 移植
License: GPL
Group: Applications/Multimedia
Group(zh_CN): 应用程序/多媒体

# filed ticket, but patch still needs work
# http://trac.xbmc.org/ticket/9658
Patch1: xbmc-13.0-dvdread.patch

# need to file trac ticket, this patch just forces external hdhomerun
# functionality, needs to be able fallback internal version
Patch2: kodi-15.0-hdhomerun.patch

# Avoid segfault during goom's configure
# https://bugzilla.redhat.com/1069079
Patch3: xbmc-13.0-libmysqlclient.patch

# Set program version parameters
Patch4: kodi-14.0-versioning.patch

# Remove call to internal ffmpeg function (misued anyway)
Patch5: kodi-14.0-dvddemux-ffmpeg.patch

# Kodi is the renamed XBMC project
Obsoletes: xbmc < 14.0-1
Provides: xbmc = %{version}

%global _with_libbluray 1
%global _with_cwiid 1
%global _with_libssh 1
%global _with_libcec 0
%global _with_external_ffmpeg 1
%global _with_wayland 0

%ifarch x86_64 i686
%global _with_crystalhd 1
%global _with_hdhomerun 1
%endif

# Upstream does not support ppc64
ExcludeArch: ppc64 mips64el

BuildRequires: SDL2-devel
BuildRequires: SDL_image-devel
BuildRequires: a52dec-devel
BuildRequires: afpfs-ng-devel
BuildRequires: avahi-devel
BuildRequires: bluez-libs-devel
BuildRequires: boost-devel
BuildRequires: bzip2-devel
BuildRequires: cmake
%if 0%{?_with_cwiid}
BuildRequires: cwiid-devel
%endif
BuildRequires: dbus-devel
BuildRequires: desktop-file-utils
BuildRequires: e2fsprogs-devel
BuildRequires: enca-devel
BuildRequires: expat-devel
BuildRequires: faad2-devel
%if 0%{?_with_external_ffmpeg}
BuildRequires: ffmpeg-devel
%endif
BuildRequires: flac-devel
BuildRequires: flex
BuildRequires: fontconfig-devel
BuildRequires: fontpackages-devel
BuildRequires: freetype-devel
BuildRequires: fribidi-devel
%if 0%{?el6}
BuildRequires: gettext-devel
%else
BuildRequires: gettext-autopoint
%endif
BuildRequires: glew-devel
BuildRequires: glib2-devel
BuildRequires: gperf
%if 0%{?_with_hdhomerun}
BuildRequires: hdhomerun-devel
%endif
BuildRequires: jasper-devel
BuildRequires: java-devel
BuildRequires: lame-devel
BuildRequires: libXinerama-devel
BuildRequires: libXmu-devel
BuildRequires: libXtst-devel
BuildRequires: libass-devel >= 0.9.7
%if 0%{?_with_libbluray}
BuildRequires: libbluray-devel
%endif
BuildRequires: libcap-devel
BuildRequires: libcdio-devel
%if 0%{?_with_libcec}
BuildRequires: libcec-devel >= 3.0.0
%endif
%if 0%{?_with_crystalhd}
BuildRequires: libcrystalhd-devel
%endif
BuildRequires: libcurl-devel
BuildRequires: libdca-devel
BuildRequires: libdvdread-devel
%if 0%{?el6}
BuildRequires: libjpeg-devel
%else
BuildRequires: libjpeg-turbo-devel
%endif
BuildRequires: libmad-devel
BuildRequires: libmicrohttpd-devel
BuildRequires: libmms-devel
BuildRequires: libmodplug-devel
BuildRequires: libmpcdec-devel
BuildRequires: libmpeg2-devel
BuildRequires: libogg-devel
# for AirPlay support
BuildRequires: libplist-devel
BuildRequires: libpng-devel
BuildRequires: librtmp-devel
BuildRequires: libsamplerate-devel
BuildRequires: libsmbclient-devel
%if 0%{?_with_libssh}
BuildRequires: libssh-devel
%endif
BuildRequires: libtiff-devel
BuildRequires: libtool
%ifnarch %{arm}
BuildRequires: libva-devel
BuildRequires: libvdpau-devel
%endif
BuildRequires: libvorbis-devel
%if 0%{?_with_wayland}
BuildRequires: libwayland-client-devel
%endif
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: lzo-devel
BuildRequires: mysql-devel
# ARM uses GLES
%ifarch %{arm}
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGLES-devel
%endif
BuildRequires: nasm
BuildRequires: pcre-devel
BuildRequires: pixman-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: python-devel
BuildRequires: python-pillow
BuildRequires: sqlite-devel
BuildRequires: swig
BuildRequires: systemd-devel
BuildRequires: taglib-devel >= 1.8
BuildRequires: tinyxml-devel
BuildRequires: tre-devel
BuildRequires: trousers-devel
BuildRequires: wavpack-devel
%if 0%{?_with_wayland}
BuildRequires: weston-devel
%endif
BuildRequires: yajl-devel
BuildRequires: zlib-devel

# nfs-utils-lib-devel package currently broken
#BuildRequires: nfs-utils-lib-devel

Requires: google-roboto-fonts
# need explicit requires for these packages
# as they are dynamically loaded via XBMC's arcane
# pseudo-DLL loading scheme (sigh)
%if 0%{?_with_libbluray}
Requires: libbluray%{?_isa}
%endif
%if 0%{?_with_libcec}
Requires: libcec%{?_isa} >= 3.0.0
%endif
%if 0%{?_with_crystalhd}
Requires: libcrystalhd%{?_isa}
%endif
Requires: libmad%{?_isa}
Requires: librtmp%{?_isa}

# needed when doing a minimal install, see
# https://bugzilla.rpmfusion.org/show_bug.cgi?id=1844
Requires: glx-utils
Requires: xorg-x11-utils

# This is just symlinked to, but needed both at build-time
# and for installation
Requires: python-pillow%{?_isa}

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

%package devel
Summary: Development files needed to compile C programs against kodi
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: xbmc-devel < 14.0
Provides: xbmc-devel = %{version}

%description devel
Kodi is a free cross-platform media-player jukebox and entertainment hub.
If you want to develop programs which use Kodi's libraries, you need to
install this package.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package eventclients
Summary: Media center event client remotes
Summary(zh_CN.UTF-8): 媒体中心客户端的遥控
Obsoletes: xbmc-eventclients < 14.0
Provides: xbmc-eventclients = %{version}

%description eventclients
This package contains support for using Kodi with the PS3 Remote, the Wii
Remote, a J2ME based remote and the command line xbmc-send utility.
%description eventclients -l zh_CN.UTF-8
这个包包含了对 PS3 遥控器， Wii 遥控器的支持。


%package eventclients-devel
Summary: Media center event client remotes development files
Summary(zh_CN.UTF-8): %{name}-eventclients 的开发包
Requires:	%{name}-eventclients%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Obsoletes: xbmc-eventclients-devel < 14.0
Provides:  xbmc-eventclients-devel = %{version}

%description eventclients-devel
This package contains the development header files for the eventclients
library.

%description eventclients-devel -l zh_CN.UTF-8
%{name}-eventclients 的开发包。

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q -n xbmc-%{version}-%{relname}
%endif

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0

%if 0%{?_with_hdhomerun}
  pushd xbmc/filesystem/
    sed -i DllHDHomeRun.h -e 's/hdhomerun_discover_find_devices_custom/hdhomerun_discover_find_devices_custom_v2/g'
  popd
%else
  # Remove hdhomerun from the build.
  pushd xbmc/filesystem/
    rm HDHomeRunFile.cpp HDHomeRunFile.h
    rm HDHomeRunDirectory.cpp HDHomeRunDirectory.h
    sed -i Makefile.in -e '/HDHomeRunFile\.cpp/d'
    sed -i Makefile.in -e '/HDHomeRunDirectory\.cpp/d'
    sed -i DirectoryFactory.cpp -e '/HomeRun/d'
    sed -i FileFactory.cpp -e '/HomeRun/d'
  popd
%endif

%build
chmod +x bootstrap
./bootstrap
# Can't use export nor %%configure (implies using export), because
# the Makefile pile up *FLAGS in this case.

./configure \
--prefix=%{_prefix} --bindir=%{_bindir} --includedir=%{_includedir} \
--libdir=%{_libdir} --datadir=%{_datadir} \
--with-lirc-device=/var/run/lirc/lircd \
%if 0%{?_with_external_ffmpeg}
--with-ffmpeg=shared \
%endif
%if 0%{?_with_wayland}
--enable-wayland \
%endif
--enable-goom \
--enable-pulse \
--enable-joystick \
%if 0%{?_with_libcec}
--enable-libcec \
%else
--disable-libcec \
%endif
%if 0%{?_with_libssh}
--enable-ssh \
%else
--disable-ssh \
%endif
--disable-dvdcss \
--disable-optimizations --disable-debug \
%ifnarch %{arm}
--enable-gl \
--disable-gles \
--enable-vdpau \
%else
--enable-gles \
--disable-vdpau \
--disable-vaapi \
%ifarch armv7hl \
--enable-tegra \
--disable-neon \
%endif
%ifarch armv7hnl
--enable-neon \
%endif
%endif
CFLAGS="$RPM_OPT_FLAGS -fPIC -I/usr/include/afpfs-ng/ -I/usr/include/samba-4.0/ -D__STDC_CONSTANT_MACROS" \
CXXFLAGS="$RPM_OPT_FLAGS -fPIC -I/usr/include/afpfs-ng/ -I/usr/include/samba-4.0/ -D__STDC_CONSTANT_MACROS" \
LDFLAGS="-fPIC" \
%if 0%{?_with_hdhomerun}
LIBS=" -lhdhomerun $LIBS" \
%endif
ASFLAGS=-fPIC

make %{?_smp_mflags} VERBOSE=1


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
make -C tools/EventClients DESTDIR=$RPM_BUILD_ROOT install
# remove the doc files from unversioned /usr/share/doc/xbmc, they should be in versioned docdir
rm -r $RPM_BUILD_ROOT/%{_datadir}/doc/

desktop-file-install \
 --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
 $RPM_BUILD_ROOT%{_datadir}/applications/kodi.desktop

# Normally we are expected to build these manually. But since we are using
# the system Python interpreter, we also want to use the system libraries
install -d $RPM_BUILD_ROOT%{_libdir}/kodi/addons/script.module.pil/lib
ln -s %{python_sitearch}/PIL $RPM_BUILD_ROOT%{_libdir}/kodi/addons/script.module.pil/lib/PIL
#install -d $RPM_BUILD_ROOT%{_libdir}/xbmc/addons/script.module.pysqlite/lib
#ln -s %{python_sitearch}/pysqlite2 $RPM_BUILD_ROOT%{_libdir}/xbmc/addons/script.module.pysqlite/lib/pysqlite2

# Use external Roboto font files instead of bundled ones
ln -sf %{_fontbasedir}/google-roboto/Roboto-Regular.ttf ${RPM_BUILD_ROOT}%{_datadir}/kodi/addons/skin.confluence/fonts/
ln -sf %{_fontbasedir}/google-roboto/Roboto-Bold.ttf ${RPM_BUILD_ROOT}%{_datadir}/kodi/addons/skin.confluence/fonts/

# Move man-pages into system dir
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/
mv docs/manpages ${RPM_BUILD_ROOT}%{_mandir}/man1/

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
if [ ! -L %{_libdir}/xbmc ] ; then
    rmdir %{_libdir}/xbmc %{_datadir}/xbmc
    ln -s kodi ${RPM_BUILD_ROOT}%{_libdir}/xbmc
    ln -s kodi ${RPM_BUILD_ROOT}%{_datadir}/xbmc
fi


%posttrans devel
if [ ! -L %{_includedir}/xbmc ] ; then
    rmdir %{_includedir}/xbmc
    ln -s kodi ${RPM_BUILD_ROOT}%{_includedir}/xbmc
fi


%files
%license copying.txt LICENSE.GPL
%doc CONTRIBUTING.md README.md docs
%{_bindir}/kodi
%{_bindir}/kodi-standalone
%{_bindir}/xbmc
%{_bindir}/xbmc-standalone
%{_libdir}/kodi
%ghost %{_libdir}/xbmc
%{_datadir}/kodi
%ghost %{_datadir}/xbmc
%{_datadir}/xsessions/kodi.desktop
%{_datadir}/xsessions/xbmc.desktop
%{_datadir}/applications/kodi.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_mandir}/man1/kodi.1.gz
%{_mandir}/man1/kodi.bin.1.gz
%{_mandir}/man1/kodi-standalone.1.gz


%files devel
%{_includedir}/kodi
%ghost %{_includedir}/xbmc


%files eventclients
%license copying.txt LICENSE.GPL
%python_sitelib/kodi
%dir %{_datadir}/pixmaps/kodi
%{_datadir}/pixmaps/kodi/*.png
%{_bindir}/kodi-j2meremote
%{_bindir}/kodi-ps3d
%{_bindir}/kodi-ps3remote
%{_bindir}/kodi-send
%{_bindir}/kodi-wiiremote
%{_mandir}/man1/kodi-j2meremote.1.gz
%{_mandir}/man1/kodi-ps3remote.1.gz
%{_mandir}/man1/kodi-send.1.gz
%{_mandir}/man1/kodi-standalone.1.gz
%{_mandir}/man1/kodi-wiiremote.1.gz


%files eventclients-devel
%{_includedir}/kodi/xbmcclient.h

%changelog
* Sun Jan 17 2016 Liu Di <liudidi@gmail.com> - 15.2-4
- 为 Magic 3.0 重建

* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 15.2-3
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 15.2-2
- 为 Magic 3.0 重建

* Wed Oct 21 2015 Liu Di <liudidi@gmail.com> - 15.2-1
- 更新到 15.2

* Wed Oct 21 2015 Liu Di <liudidi@gmail.com> - 12.0-0.git20130426.2
- 更新到 20151021 日期的仓库源码

* Wed Oct 21 2015 Liu Di <liudidi@gmail.com> - 12.0-0.git20130426.1
- 更新到 20151021 日期的仓库源码


