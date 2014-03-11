#
# spec file for package chromium
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define chromium_no_dlopen 1
%define chromium_system_libs 1

%define pnacl_version 12534
%define newlib_version 12464
%define glibc_version 12421

Name:           chromium
Version:        33.0.1750.117
Release:        1%{?dist}
Summary:        Google's opens source browser project
Summary(zh_CN.UTF-8): Google 的开放源代码浏览器项目
License:        BSD-3-Clause and LGPL-2.1+
Group:          Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Url:            http://code.google.com/p/chromium/
Source0:        http://gsdview.appspot.com/chromium-browser-official/%{name}-%{version}.tar.xz
Source1:        http://gsdview.appspot.com/nativeclient-archive2/x86_toolchain/r%{glibc_version}/toolchain_linux_x86.tar.bz2
Source2:        http://gsdview.appspot.com/nativeclient-archive2/toolchain/%{newlib_version}/naclsdk_linux_x86.tgz
Source3:        http://gsdview.appspot.com/nativeclient-archive2/toolchain/%{pnacl_version}/naclsdk_pnacl_linux_x86.tgz
Source4:        http://gsdview.appspot.com/nativeclient-archive2/toolchain/%{pnacl_version}/naclsdk_pnacl_translator.tgz
Source20:       chromium-vendor.patch.in
Source30:       master_preferences
Source31:       default_bookmarks.html
Source99:       chrome-wrapper
Source100:      chromium-browser.sh
Source101:      chromium-browser.desktop
Source102:      chromium-browser.xml
Source103:      chromium.default
Source104:      chromium-icons.tar.bz2
Source998:      gn-binaries.tar.xz
# This is the update script to get the new tarballs
Source999:      update_chromium
Provides:       chromium-based-browser = %{version}
Provides:       chromium-browser = %{version}
Provides:       browser(npapi)
Obsoletes:      chromium-browser < %{version}
Conflicts:      otherproviders(chromium-browser)
# There is no v8 for ppc and thus chromium won't run on ppc. For aarch64 certain buildrequires are missing (e.g. valgrind)
ExcludeArch:    aarch64 ppc ppc64 ppc64le

## Start Patches
# Many changes to the gyp systems so we can use system libraries
# PATCH-FIX-OPENSUSE Test sources have been removed to shrink the tarball
Patch1:         chromium-23.0.1245-no-test-sources.patch
# PATCH-FIX-OPENSUSE Make the 1-click-install ymp file always download [bnc#836059]
Patch2:         exclude_ymp.diff
# PATCH-FIX-OPENSUSE Disable the download of the NaCl tarballs
Patch3:         no-download-nacl.diff
# PATCH-FIX-OPENSUSE Remove the sysroot for ARM builds. This is causing issues when finding include-files
Patch4:         chromium-fix-arm-sysroot.patch
# PATCH-FIX-OPENSUSE Don't use -m32 for the ARM builds
Patch5:         chromium-fix-arm-icu.patch
# PATCH-FIX-OPENSUSE Fix the WEBRTC cpu-features for the ARM builds
Patch6:         chromium-arm-webrtc-fix.patch
# PATCH-FIX-OPENSUSE Dont use GN for ARM builds
Patch7:         arm_disable_gn.patch
# PATCH-FIX-OPENSUSE removes build part for courgette
Patch13:        chromium-no-courgette.patch
# PATCH-FIX-OPENSUSE enables reading of the master preference
Patch14:        chromium-master-prefs-path.patch
# PATCH-FIX-OPENSUSE Fix some includes specifically for the GCC version used
Patch20:        chromium-gcc-fixes.patch
# PATCH-FIX-UPSTREAM Add more charset aliases
Patch64:        chromium-more-codec-aliases.patch
# PATCH-FIX-OPENSUSE Compile the sandbox with -fPIE settings
Patch66:        chromium-sandbox-pie.patch
# PATCH-FIX-OPENSUSE Adjust ldflags for better building
Patch67:        adjust-ldflags-no-keep-memory.patch

BuildRequires:  alsa-lib-devel
BuildRequires:  bison
BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  flac-devel
BuildRequires:  flex
BuildRequires:  freetype-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gperf
BuildRequires:  hicolor-icon-theme
BuildRequires:  hunspell-devel
BuildRequires:  krb5-devel
BuildRequires:  libcap-devel
BuildRequires:  libdrm-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  expat-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libgnome-keyring-devel
BuildRequires:  libicu-devel >= 4.0
BuildRequires:  pulseaudio-libs-devel
%if !0%{?packman_bs}
BuildRequires:  ninja
%endif
BuildRequires:  pam-devel
BuildRequires:  pciutils-devel
BuildRequires:  pkgconfig
BuildRequires:  python
BuildRequires:  python-devel
BuildRequires:  sqlite-devel
BuildRequires:  util-linux
BuildRequires:  valgrind-devel
BuildRequires:  wdiff
BuildRequires:  perl(Switch)
BuildRequires:  pkgconfig(cairo) >= 1.6
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(nspr) >= 4.9.5
BuildRequires:  pkgconfig(nss) >= 3.14
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xtst)
%if 0%{?chromium_system_libs}
BuildRequires:  libjpeg-devel
%endif
BuildRequires:  perl-JSON
BuildRequires:  usbutils
BuildRequires:  yasm
BuildRequires:  pkgconfig(libevent)
BuildRequires:  pkgconfig(libmtp)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(speex)

# For NaCl
%ifarch x86_64
BuildRequires:  gcc-c++(x86-32)
BuildRequires:  glibc(x86-32)
%endif

Requires:       alsa
Requires:       ffmpegsumo = %{version}
Requires:       hicolor-icon-theme
Requires:       update-alternatives
Requires:       xdg-utils

#Requirements to build a fully functional ffmpeg
# This can only be done on packman OBS
%if 0%{?packman_bs}
BuildRequires:  SDL-devel
BuildRequires:  dirac-devel >= 1.0.0
BuildRequires:  imlib2-devel
BuildRequires:  libdc1394
BuildRequires:  libdc1394-devel
BuildRequires:  libfaac-devel >= 1.28
BuildRequires:  libgsm
BuildRequires:  libgsm-devel
BuildRequires:  libjack-devel
BuildRequires:  libmp3lame-devel
BuildRequires:  libogg-devel
BuildRequires:  liboil-devel >= 0.3.15
BuildRequires:  libopencore-amr-devel
BuildRequires:  libtheora-devel >= 1.1
BuildRequires:  libvdpau-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libvpx-devel
BuildRequires:  libx264-devel
BuildRequires:  libxvidcore-devel
BuildRequires:  ncurses-devel
BuildRequires:  schroedinger-devel
BuildRequires:  slang-devel
BuildRequires:  texinfo
%endif

Requires(pre):  permissions

Requires:       %{name}-suid-helper = %{version}

%description
Chromium is the open-source project behind Google Chrome. We invite you to join us in our effort to help build a safer, faster, and more stable way for all Internet users to experience the web, and to create a powerful platform for developing a new generation of web applications.

%package ffmpegsumo
Summary:        Library to provide ffmpeg support to Chromium
License:        BSD-3-Clause and LGPL-2.1+
Group:          Productivity/Networking/Web/Browsers
Provides:       ffmpegsumo = %{version}
Conflicts:      otherproviders(ffmpegsumo)
Requires:       %{name}

%description ffmpegsumo
The is the multimedia codec library for Chromium. It is based on the internal ffmpeg source code and contains only the open source codecs from ffmpeg. Proprietary codecs (e.g. H.264) are not part of this library, but are provided in an external package

%package desktop-kde

Summary:        Update to chromium to use KDE's kwallet to store passwords
License:        BSD-3-Clause and LGPL-2.1+
Group:          Productivity/Networking/Web/Browsers
Conflicts:      otherproviders(chromium-password)
Provides:       chromium-password = %{version}
Requires(post): chromium = %{version}

%description desktop-kde
By using the openSUSE update-alternatives the password store for Chromium is changed to utilize
KDE's kwallet. Please be aware that by this change the old password are no longer accessible and
are also not converted to kwallet.

%package desktop-gnome

Summary:        Update to chromium to use Gnome keyring to store passwords
License:        BSD-3-Clause and LGPL-2.1+
Group:          Productivity/Networking/Web/Browsers
Conflicts:      otherproviders(chromium-password)
Provides:       chromium-password = %{version}
Requires(post): chromium = %{version}
Requires:       libgnome

%description desktop-gnome
By using the openSUSE update-alternatives the password store for Chromium is changed to utilize
Gnome's Keyring. Please be aware that by this change the old password are no longer accessible and
are also not converted to Gnome's Keyring.

%package suid-helper

Summary:        A suid helper to let a process willingly drop privileges on Linux
License:        BSD-3-Clause and LGPL-2.1+
Group:          Productivity/Networking/Web/Browsers
Url:            http://code.google.com/p/setuid-sandbox/
Requires(pre):  permissions

%description suid-helper
t will allow a process to execute a target executable that will be able to drop privileges:

 * The suid sandbox will create a new PID namespace or will switch uid/gid to isolate the process
 * a helper process, sharing the filesystem view of the existing process, will be created.  It
   will accept a request to chroot() the process to an empty directory

This is convenient because an executable can be launched, load libraries and open files and get
chroot()-ed to an empty directory when it wants to drop filesystem access.

%package -n chromedriver

Summary:        WebDriver for Google Chrome/Chromium
License:        BSD-3-Clause
Group:          Development/Tools/Other
Url:            http://code.google.com/p/chromedriver/

%description -n chromedriver
WebDriver is an open source tool for automated testing of webapps across many browsers. It provides capabilities for navigating to web pages, user input, JavaScript execution, and more. ChromeDriver is a standalone server which implements WebDriver's wire protocol for Chromium. It is being developed by members of the Chromium and WebDriver teams.


%if 0%{?packman_bs}
%package ffmpeg
Summary:        The ffmpeg lib for Google's opens source browser Chromium
License:        BSD-3-Clause and LGPL-2.1+
Group:          Productivity/Networking/Web/Browsers
Provides:       ffmpegsumo = %{version}
Conflicts:      otherproviders(ffmpegsumo)
Requires:       %{name}

%description ffmpeg
FFMPEG library built from the chromium sources.
%endif

%prep
%setup -q -n %{name}-%{version} -a 998

%patch1 -p0
%patch2 -p0
%patch3 -p0
%ifarch armv7hl
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p1
%endif
%patch64 -p0
%patch13 -p0
%patch14 -p0
%patch20 -p0
%patch66 -p0
%patch67 -p0
#Upstream fixes

# apply vendor patch after substitution
sed "s:RPM_VERSION:%{version}:" %{SOURCE20} | patch -p0
sed -i 's|icu)|icu-i18n)|g' build/linux/system.gyp

%if !0%{?packman_bs}
# Install the Native Client tarballs to the right location
mkdir -p native_client/toolchain/.tars
cp %{SOURCE1} native_client/toolchain/.tars/
cp %{SOURCE2} native_client/toolchain/.tars/
cp %{SOURCE3} native_client/toolchain/.tars/
cp %{SOURCE4} native_client/toolchain/.tars/

# Extract the NaCl tarballs 
python ./build/download_nacl_toolchains.py --no-arm-trusted --keep
%endif

%build

PARSED_OPT_FLAGS=`echo \'%{optflags} -D_GNU_SOURCE\' | sed "s/ /',/g" | sed "s/',/', '/g"`
#'
sed -i "s|'-O<(release_optimize)'|$PARSED_OPT_FLAGS|g" build/common.gypi

myconf+="-Dwerror=
                     -Dlinux_sandbox_chrome_path=%{_libdir}/chromium/chromium
                     -Duse_openssl=0
                     -Duse_system_ffmpeg=0
                     -Dbuild_ffmpegsumo=1
                     -Dproprietary_codecs=1
                     -Dremove_webcore_debug_symbols=1
                     -Dlogging_like_official_build=1
                     -Dlinux_fpic=1 
                     -Ddisable_sse2=1"

%if 0%{?packman_bs}
myconf+=" -Dffmpeg_branding=Chrome"
%endif

%ifarch armv7hl
myconf+=" -Dlinux_use_tcmalloc=0
          -DCAN_USE_ARMV7_INSTRUCTIONS=1
          -DV8_TARGET_ARCH_ARM
          -Dtarget_arch=arm
          -DARMV7=1
          -Darm_neon=0
          -Darm_fpu=vfpv3-d16
          -Drelease_extra_cflags=$CFLAGS -DUSE_EABI_HARDFLOAT
          -Dv8_use_arm_eabi_hardfloat=true
          -Darm_float_abi=hard
          -Ddisable_nacl=1
          -Ddisable_glibc=1
          -Ddisable_pnacl=1
          -Ddisable_newlib_untar=0
          -Darm_version=7"
%else
myconf+=" -Ddisable_nacl=0
          -Ddisable_glibc=1
          -Ddisable_pnacl=0
          -Ddisable_newlib_untar=0"
%endif

%ifarch x86_64
myconf+=" -Dtarget_arch=x64"
%endif

%if 0%{?chromium_system_libs}
myconf+=" -Duse_system_flac=1
                     -Duse_system_speex=1
                     -Duse_system_libexif=1 
                     -Duse_system_libevent=1 
                     -Duse_system_libmtp=1
                     -Duse_system_opus=1 
                     -Duse_system_bzip2=1 
                     -Duse_system_harfbuzz=1 
                     -Duse_system_libjpeg=1 
                     -Duse_system_libpng=1 
                     -Duse_system_libxslt=1 
                     -Duse_system_libyuv=1 
                     -Duse_system_nspr=1 
                     -Duse_system_protobuf=1 
                     -Duse_system_yasm=1"

myconf+=" -Duse_system_icu=1"

%endif

%if 0%{?chromium_no_dlopen}
myconf+=" -Duse_pulseaudio=1 
                     -Dlinux_link_libpci=1 
                     -Dlinux_link_gnome_keyring=1
                     -Dlinux_link_gsettings=1 
                     -Dlinux_link_libgps=1"

%ifnarch %ix86
#myconf+=" -Dlinux_link_kerberos=1" 
%endif

%endif

myconf+=" -Dpython_ver=2.7"
%ifarch x86_64
myconf+=" -Dsystem_libdir=lib64"
%endif

myconf+=" -Djavascript_engine=v8 
                     -Dlinux_use_gold_binary=0 
                     -Dlinux_use_gold_flags=0"

# Set up Google API keys, see http://www.chromium.org/developers/how-tos/api-keys
# Note: these are for the openSUSE Chromium builds ONLY. For your own distribution,
# please get your own set of keys.

myconf+=" -Dgoogle_api_key=AIzaSyD1hTe85_a14kr1Ks8T3Ce75rvbR1_Dx7Q 
          -Dgoogle_default_client_id=4139804441.apps.googleusercontent.com 
          -Dgoogle_default_client_secret=KDTRKEZk2jwT_7CDpcmMA--P"

build/linux/unbundle/replace_gyp_files.py $myconf

%if 0%{?packman_bs}
    ./build/gyp_chromium -f make third_party/ffmpeg/ffmpeg.gyp --no-parallel --depth . $myconf
    cd third_party/ffmpeg
    make -r %{?_smp_mflags} -f ffmpeg.Makefile BUILDTYPE=Release V=1
%else
%if 0
    export GYP_GENERATORS='ninja'
    ./build/gyp_chromium build/all.gyp --depth .  $myconf

    ninja -C out/Release chrome

    # Build the required SUID_SANDBOX helper
    ninja -C out/Release chrome_sandbox

    # Build the ChromeDriver test suite
    ninja -C out/Release chromedriver
%else
    ./build/gyp_chromium -f make build/all.gyp --depth . $myconf

    make -r %{?_smp_mflags} chrome V=1 BUILDTYPE=Release

    # Build the required SUID_SANDBOX helper
    make -r %{?_smp_mflags} chrome_sandbox V=1 BUILDTYPE=Release

    # Build the ChromeDriver test suite
    make -r %{?_smp_mflags} chromedriver V=1 BUILDTYPE=Release
%endif
%endif

%install
mkdir -p %{buildroot}%{_libdir}/chromium/
%if 0%{?packman_bs}
	pushd third_party/ffmpeg/out/Release
	cp -a lib*.so %{buildroot}%{_libdir}/chromium/
	popd
%else
	%ifarch x86_64
	mkdir -p %{buildroot}%{_prefix}/lib/
	%endif
	install -m 755 %{SOURCE100} %{buildroot}%{_libdir}/chromium/chromium-generic

	# x86_64 capable systems need this
	sed -i "s|/usr/lib/chromium|%{_libdir}/chromium|g" %{buildroot}%{_libdir}/chromium/chromium-generic

	#update the password-store settings for each alternative
	sed "s|password-store=basic|password-store=kwallet|g" %{buildroot}%{_libdir}/chromium/chromium-generic > %{buildroot}%{_libdir}/chromium/chromium-kde
	sed "s|password-store=basic|password-store=gnome|g" %{buildroot}%{_libdir}/chromium/chromium-generic > %{buildroot}%{_libdir}/chromium/chromium-gnome
	mkdir -p %{buildroot}%{_mandir}/man1/
	pushd out/Release

	# Install the file /etc/default/chromium which defines the chromium flags
	mkdir -p %{buildroot}%{_sysconfdir}/default
	install -m 644 %{SOURCE103} %{buildroot}%{_sysconfdir}/default/chromium

	# Recent Chromium builds now wants to have the sandbox in the same directory. So let's create a symlink to the one in /usr/lib
	cp -a chrome_sandbox %{buildroot}%{_prefix}/lib/
	ln -s -f %{_prefix}/lib/chrome_sandbox %{buildroot}/%{_libdir}/chromium/chrome-sandbox

	cp -a *.pak locales xdg-mime %{buildroot}%{_libdir}/chromium/
	cp -a chromedriver %{buildroot}%{_libdir}/chromium/

	# Patch xdg-settings to use the chromium version of xdg-mime as that the system one is not KDE4 compatible
	sed "s|xdg-mime|%{_libdir}/chromium/xdg-mime|g" xdg-settings > %{buildroot}%{_libdir}/chromium/xdg-settings

	cp -a resources.pak %{buildroot}%{_libdir}/chromium/
	cp -a chrome %{buildroot}%{_libdir}/chromium/chromium
	cp -a chrome.1 %{buildroot}%{_mandir}/man1/chrome.1
	cp -a chrome.1 %{buildroot}%{_mandir}/man1/chromium.1
	%fdupes %{buildroot}%{_mandir}/man1/

%ifarch armv7hl
# Native Client doesn't build yet for ARM
%else
	# NaCl
	cp -a nacl_helper %{buildroot}%{_libdir}/chromium/
	cp -a nacl_helper_bootstrap %{buildroot}%{_libdir}/chromium/
	cp -a nacl_irt_*.nexe %{buildroot}%{_libdir}/chromium/
	cp -a libppGoogleNaClPluginChrome.so %{buildroot}%{_libdir}/chromium/
%endif

	#libffmpegsumo
	cp -a libffmpegsumo.so %{buildroot}%{_libdir}/chromium/
	popd

	mkdir -p %{buildroot}%{_datadir}/icons/
	pushd %{buildroot}%{_datadir}/icons/
	tar -xjf %{SOURCE104}
	mv oxygen hicolor
	popd

	mkdir -p %{buildroot}%{_datadir}/applications/
	desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE101}

	mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps/
	cp -a %{SOURCE102} %{buildroot}%{_datadir}/gnome-control-center/default-apps/

	# link to browser plugin path.  Plugin patch doesn't work. Why?
	mkdir -p %{buildroot}%{_libdir}/browser-plugins
	pushd %{buildroot}%{_libdir}/%{name}
	ln -s ../browser-plugins plugins

	# Install the master_preferences file
	mkdir -p %{buildroot}%{_sysconfdir}/%{name}
	install -m 0644 %{SOURCE30} %{buildroot}%{_sysconfdir}/%{name}
	install -m 0644 %{SOURCE31} %{buildroot}%{_sysconfdir}/%{name}

	# Set the right attributes
	chmod 755 %{buildroot}%{_libdir}/%{name}/xdg-settings
	chmod 755 %{buildroot}%{_libdir}/%{name}/xdg-mime

	# create a dummy target for /etc/alternatives/chromium
	mkdir -p %{buildroot}%{_sysconfdir}/alternatives
	mkdir -p %{buildroot}%{_bindir}
	touch %{buildroot}%{_sysconfdir}/alternatives/chromium
	ln -s -f %{_sysconfdir}/alternatives/chromium %{buildroot}/%{_bindir}/chromium
%endif

%clean
rm -rf %{buildroot}

%pre
if [ -f %{_bindir}/chromium -a ! -L %{_bindir}/chromium ] ; then rm -f %{_bindir}/chromium
fi

# Add snipplets to update the GTK cache on package install.

%verifyscript suid-helper
%verify_permissions -e %{_prefix}/lib/chrome_sandbox 

%post suid-helper
%set_permissions %{_prefix}/lib/chrome_sandbox

%post
%icon_theme_cache_post
%desktop_database_post
"%_sbindir/update-alternatives" --install %{_bindir}/chromium chromium %{_libdir}/chromium/chromium-generic 10

%postun
%icon_theme_cache_postun
%desktop_database_postun
if [ $1 -eq 0 ]; then
update-alternatives --remove-all chromium
fi

%post desktop-kde 
if [ ! -e /.buildenv ]; then
"%_sbindir/update-alternatives" --install %{_bindir}/chromium chromium %{_libdir}/chromium/chromium-kde 15
"%_sbindir/update-alternatives" --auto chromium
fi

%preun desktop-kde
if [ $1 -eq 0 -a ! -e /.buildenv ]; then
"%_sbindir/update-alternatives" --remove chromium %{_libdir}/chromium/chromium-kde
"%_sbindir/update-alternatives" --auto chromium
fi

%post desktop-gnome
if [ ! -e /.buildenv ]; then
"%_sbindir/update-alternatives" --install %{_bindir}/chromium chromium %{_libdir}/chromium/chromium-gnome 15
"%_sbindir/update-alternatives" --auto chromium
fi

%postun desktop-gnome
if [ $1 -eq 0 -a ! -e /.buildenv ]; then
"%_sbindir/update-alternatives" --remove chromium %{_libdir}/chromium/chromium-gnome
"%_sbindir/update-alternatives" --auto chromium
fi

# Files!

%if 0%{?packman_bs}

%files ffmpeg
%defattr(-,root,root,-)
%dir %{_libdir}/chromium
%{_libdir}/chromium/lib*.so

%else

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE
%config %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/default/chromium
%dir %{_datadir}/gnome-control-center
%dir %{_datadir}/gnome-control-center/default-apps
%{_libdir}/chromium/
%{_mandir}/man1/chrom*
%{_datadir}/applications/*.desktop
%{_datadir}/gnome-control-center/default-apps/chromium-browser.xml
%{_datadir}/icons/hicolor/
%exclude %{_libdir}/chromium/libffmpegsumo.so
%exclude %{_libdir}/chromium/chromium-kde
%exclude %{_libdir}/chromium/chromium-gnome
%exclude %{_libdir}/chromium/chromedriver
%exclude %{_libdir}/chromium/chrome-sandbox
%_bindir/chromium
%ghost %_sysconfdir/alternatives/chromium

%files ffmpegsumo
%defattr(-,root,root,-)
%{_libdir}/chromium/libffmpegsumo.so

%files desktop-kde
%attr(755, root, root) %{_libdir}/chromium/chromium-kde

%files desktop-gnome
%attr(755, root, root) %{_libdir}/chromium/chromium-gnome

%files suid-helper
%defattr(-,root,root,-)
%verify(not mode) %{_prefix}/lib/chrome_sandbox
%{_libdir}/chromium/chrome-sandbox

%files -n chromedriver
%defattr(-,root,root,-)
%{_libdir}/chromium/chromedriver
%endif

%changelog

