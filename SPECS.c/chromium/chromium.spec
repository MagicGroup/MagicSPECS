# %%{nil} for Stable; -beta for Beta; -dev for Devel
# dash in -beta and -dev is intentional !
%define chromium_channel %{nil}
%define chromium_browser_channel chromium-browser%{chromium_channel}
%if 0%{?rhel}
%define chromium_path /opt/chromium-browser%{chromium_channel}
%else
%define chromium_path %{_libdir}/chromium-browser%{chromium_channel}
%endif
%define tests 0
%define debug 0

### Google API keys (see http://www.chromium.org/developers/how-tos/api-keys)
### Note: These are for Fedora use ONLY.
### For your own distribution, please get your own set of keys.
### http://lists.debian.org/debian-legal/2013/11/msg00006.html
%define api_key AIzaSyDUIXvzVrt5OkVsgXhQ6NFfvWlA44by-aw
%define default_client_id 449907151817.apps.googleusercontent.com
%define default_client_secret miEreAep8nuvTdvLums6qyLK

Name:		chromium%{chromium_channel}
Version:	46.0.2490.80
Release:	1%{?dist}
Summary:	A WebKit (Blink) powered web browser
Url:		http://www.chromium.org/Home
License:	BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)
Group:		Applications/Internet

# We can't do a functional pointer to macro..
Patch1:		chromium-34.0.1847.132-gnome_keyring_fix.patch
Patch2:		chromium-39.0.2171.36-link_gio.patch

### Chromium Python Patches ###
Patch50:	chromium-31.0.1650.57-python_simplejson.patch
Patch51:	chromium-37.0.2062.20-python_tld_cleanup.patch
Patch52:	chromium-46.0.2490.71-python_re_sub.patch
Patch53:	chromium-45.0.2454.101-python_dict_generators.patch
# We don't have python-argparse in RHEL6, so bundle it like in Firefox package
Patch54:	chromium-35.0.1916.114-python_argparse.patch
Patch55:	chromium-39.0.2171.42-python_zipfile.patch

### Chromium Fedora Patches ###
Patch102:	chromium-46.0.2490.71-gcc5.patch
Patch103:	chromium-45.0.2454.101-linux-path-max.patch
Patch104:	chromium-45.0.2454.101-addrfix.patch
# Google patched their bundled copy of icu 54 to include API functionality that wasn't added until 55.
# :P
Patch105:	chromium-45.0.2454.101-system-icu-54-does-not-have-detectHostTimeZone.patch
Patch106:	chromium-46.0.2490.71-notest.patch

### Chromium Tests Patches ###

### Chromium Debug Build Patches ###

# Use chromium-latest.py to generate clean tarball from released build tarballs, found here:
# http://build.chromium.org/buildbot/official/
# For Chromium RHEL use chromium-latest.py --stable --ffmpegclean --tests
# For Chromium Fedora use chromium-latest.py --stable --ffmpegclean
# https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%%{version}.tar.xz
Source0:	chromium-%{version}-clean.tar.xz
%if %{tests}
Source1:	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}-testdata.tar.xz
%endif
# https://chromium.googlesource.com/chromium/tools/depot_tools.git/+archive/d5a1ab12efbc1c790a9bf3da57a74bf37d7205bc.tar.gz
Source2:	depot_tools.git-master.tar.gz
Source3:	chromium-browser.sh
Source4:	%{chromium_browser_channel}.desktop
# Also, only used if you want to reproduce the clean tarball.
Source5:	clean_ffmpeg.sh
Source6:	chromium-latest.py
Source7:	process_ffmpeg_gyp.py
# GNOME stuff
Source8:	chromium-browser.xml

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?rhel}
BuildRequires:	devtoolset-2-gcc-c++
BuildRequires:	devtoolset-2-gcc
BuildRequires:	devtoolset-2-binutils
%else
# We can assume gcc and binutils.
BuildRequires:	gcc-c++
%endif

BuildRequires:	alsa-lib-devel
BuildRequires:	atk-devel
BuildRequires:	bison
BuildRequires:	cups-devel
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	fontconfig-devel
BuildRequires:	GConf2-devel
BuildRequires:	glib2-devel
BuildRequires:	gnome-keyring-devel
BuildRequires:	gtk2-devel
BuildRequires:	glibc-devel
BuildRequires:	gperf
BuildRequires:	libcap-devel
BuildRequires:	libdrm-devel
BuildRequires:	libexif-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libudev-devel
BuildRequires:	libusb-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXScrnSaver-devel
BuildRequires:	libXtst-devel
BuildRequires:	nss-devel >= 3.12.3
BuildRequires:	pciutils-devel
BuildRequires:	pulseaudio-libs-devel
%if %{?tests}
BuildRequires:	pam-devel
# Tests needs X
BuildRequires:	Xvfb
%endif

%if 0%{?fedora}
# Fedora turns on NaCl
# NaCl needs these
BuildRequires:	libstdc++-devel, openssl-devel
BuildRequires:	nacl-gcc, nacl-binutils, nacl-newlib
BuildRequires:	nacl-arm-gcc, nacl-arm-binutils, nacl-arm-newlib
# pNaCl needs this monster
BuildRequires:	native_client
# Fedora tries to use system libs whenever it can.
BuildRequires:	bzip2-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	elfutils-libelf-devel
BuildRequires:	flac-devel
BuildRequires:	hwdata
BuildRequires:	jsoncpp-devel
BuildRequires:	kernel-headers
BuildRequires:	libevent-devel
BuildRequires:	libexif-devel
%if 0%{?fedora} >= 22
# Chromium needs icu 5.4 now, which isn't in older Fedora.
BuildRequires:	libicu-devel >= 5.4
%global bundleicu 0
%else
%global bundleicu 1
%endif
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libsrtp-devel >= 1.4.4
BuildRequires:	libudev-devel
Requires:	libusbx >= 1.0.20-101
BuildRequires:	libusbx-devel >= 1.0.20-101
# We don't use libvpx anymore because Chromium loves to 
# use bleeding edge revisions here that break other things
# ... so we just use the bundled libvpx.
# Same is true for libwebp.
BuildRequires:	libxslt-devel
# Same here, it seems.
# BuildRequires:	libyuv-devel
BuildRequires:	minizip-devel
BuildRequires:	nspr-devel
BuildRequires:	opus-devel
BuildRequires:	perl(Switch)
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	python-jinja2
BuildRequires:	python-markupsafe
BuildRequires:	python-ply
Requires:	re2 >= 20131024
BuildRequires:	re2-devel >= 20131024
BuildRequires:	speech-dispatcher-devel
BuildRequires:	speex-devel = 1.2
BuildRequires:	yasm
BuildRequires:	pkgconfig(gnome-keyring-1)
%endif

# We pick up an automatic requires on the library, but we need the version check
# because the nss shared library is unversioned.
# This is to prevent someone from hitting http://code.google.com/p/chromium/issues/detail?id=26448
Requires:	nss%{_isa} >= 3.12.3
Requires:	nss-mdns%{_isa}

# GTK modules it expects to find for some reason.
Requires:	libcanberra-gtk2%{_isa}
# semanage
Requires:	policycoreutils-python

# Once upon a time, we tried to split these out... but that's not worth the effort anymore.
Provides:	chromium-ffmpegsumo = %{version}-%{release}
Obsoletes:	chromium-ffmpegsumo <= 35.0.1916.114
# This is a lie. v8 has its own version... but I'm being lazy and not using it here.
# Barring Google getting much faster on the v8 side (or much slower on the Chromium side)
# the true v8 version will be much smaller than the Chromium version that it came from.
Provides:	chromium-v8 = %{version}-%{release}
Obsoletes:	chromium-v8 <= 3.25.28.18
# This is a lie. webrtc never had any real version. 0.2 is greater than 0.1
Provides:	webrtc = 0.2
Obsoletes:	webrtc <= 0.1
# This is a lie, but it keeps older upgrades semi-sane
Provides:	chromium-libs = %{version}-%{release}
Obsoletes:	chromium-libs <= %{version}-%{release}

ExclusiveArch:	x86_64

# Bundled bits (I'm sure I've missed some)
Provides: bundled(angle) = 2422
Provides: bundled(bintrees) = 1.0.1
## This is a fork of openssl.
Provides: bundled(boringssl)
Provides: bundled(brotli)
Provides: bundled(bspatch)
Provides: bundled(cacheinvalidation) = 20150720
Provides: bundled(cardboard) = 0.5.4
Provides: bundled(colorama) = 799604a104
Provides: bundled(crashpad)
Provides: bundled(dmg_fp)
Provides: bundled(expat) = 2.1.0
Provides: bundled(fdmlibm) = 5.3
# Don't get too excited. MPEG and other legally problematic stuff is stripped out.
Provides: bundled(ffmpeg) = 2.6
Provides: bundled(fips181) = 2.2.3
Provides: bundled(fontconfig) = 2.11.0
Provides: bundled(gperftools) = svn144
Provides: bundled(gtk3) = 3.1.4
Provides: bundled(hunspell) = 1.3.2
Provides: bundled(iccjpeg)
%if 0%{?bundleicu}
Provides: bundled(icu) = 54.1 
%endif
Provides: bundled(kitchensink) = 1
Provides: bundled(leveldb) = r80
Provides: bundled(libaddressinput) = 0
Provides: bundled(libjingle) = 9564
Provides: bundled(libphonenumber) = svn584
Provides: bundled(libvpx) = 1.4.0
Provides: bundled(libwebp) = 0.4.3
Provides: bundled(libXNVCtrl) = 302.17
Provides: bundled(libyuv) = 1444
Provides: bundled(lzma) = 9.20
Provides: bundled(libudis86) = 1.7.1
Provides: bundled(mesa) = 9.0.3
Provides: bundled(NSBezierPath) = 1.0
Provides: bundled(mozc)
Provides: bundled(mt19937ar) = 2002.1.26
Provides: bundled(ots) = 767d6040439e6ebcdb867271fcb686bd3f8ac739
Provides: bundled(protobuf) = r476
Provides: bundled(qcms) = 4
Provides: bundled(sfntly) = svn111
Provides: bundled(skia)
Provides: bundled(SMHasher) = 0
Provides: bundled(snappy) = r80
Provides: bundled(speech-dispatcher) = 0.7.1
Provides: bundled(sqlite) = 3.8.7.4
Provides: bundled(superfasthash) = 0
Provides: bundled(talloc) = 2.0.1
Provides: bundled(usrsctp) = 0
Provides: bundled(v8) = 4.5.103.35
Provides: bundled(webrtc) = 90usrsctp
Provides: bundled(woff2) = 445f541996fe8376f3976d35692fd2b9a6eedf2d
Provides: bundled(xdg-mime)
Provides: bundled(xdg-user-dirs)
Provides: bundled(x86inc) = 0
Provides: bundled(zlib) = 1.2.5

%description
Chromium is an open-source web browser, powered by WebKit (Blink).

%prep
%setup -q -T -c -n depot_tools -a 2
%if %{tests}
%setup -q -n chromium-%{version} -b 1
%else
%setup -q -n chromium-%{version}
%endif

# %%patch0 -p1 -b .libudev_extern_c
%patch1 -p1 -b .gnome_keyring_fix
%patch2 -p1 -b .link_gio

### Chromium Python Patches ###
%patch50 -p1 -b .python_simplejson
%patch51 -p1 -b .python_tld_cleanup
%patch52 -p1 -b .python_re_sub
%patch53 -p1 -b .python_dict_generators
%if 0%{?rhel}
%patch54 -p1 -b .python_argparse
%patch55 -p1 -b .python_zipfile.patch
%endif

### Chromium Fedora Patches ###
%patch102 -p1 -b .gcc5
%patch103 -p1 -b .pathmax
%patch104 -p1 -b .addrfix
%patch105 -p1 -b .system-icu
%patch106 -p1 -b .notest

### Chromium Tests Patches ###

### Chromium Debug Build Patches ###

%if 0%{?rhel}
# Set PYTHON PATH to directory which contains python argparse module
export PYTHONPATH=`pwd`/third_party/python-argparse
# Use the compiler from Red Hat Developer ToolSet 2.0 to get the C++11 compliant compiler.
export CC=/opt/rh/devtoolset-2/root/usr/bin/gcc
export CXX=/opt/rh/devtoolset-2/root/usr/bin/g++
export AR=/opt/rh/devtoolset-2/root/usr/bin/gcc-ar
export RANLIB=/opt/rh/devtoolset-2/root/usr/bin/gcc-ranlib
%else
export CC="gcc"
export CXX="g++"
export AR="ar"
export RANLIB="ranlib"
%endif

%if 0%{?fedora}
# prep the nacl tree
mkdir -p out/Release/gen/sdk/linux_x86/nacl_x86_newlib
cp -a --no-preserve=context /usr/%{_arch}-nacl/* out/Release/gen/sdk/linux_x86/nacl_x86_newlib

mkdir -p out/Release/gen/sdk/linux_x86/nacl_arm_newlib
cp -a --no-preserve=context /usr/arm-nacl/* out/Release/gen/sdk/linux_x86/nacl_arm_newlib

# Not sure if we need this or not, but better safe than sorry.
pushd out/Release/gen/sdk/linux_x86
ln -s nacl_x86_newlib nacl_x86_newlib_raw
ln -s nacl_arm_newlib nacl_arm_newlib_raw
popd

mkdir -p out/Release/gen/sdk/linux_x86/nacl_x86_newlib/bin
pushd out/Release/gen/sdk/linux_x86/nacl_x86_newlib/bin
ln -s /usr/bin/%{_arch}-nacl-gcc gcc
ln -s /usr/bin/%{_arch}-nacl-gcc %{_arch}-nacl-gcc
ln -s /usr/bin/%{_arch}-nacl-g++ g++
ln -s /usr/bin/%{_arch}-nacl-g++ %{_arch}-nacl-g++
# ln -s /usr/bin/x86_64-nacl-ar ar
ln -s /usr/bin/%{_arch}-nacl-ar %{_arch}-nacl-ar
# ln -s /usr/bin/x86_64-nacl-as as
ln -s /usr/bin/%{_arch}-nacl-as %{_arch}-nacl-as
# ln -s /usr/bin/x86_64-nacl-ranlib ranlib
ln -s /usr/bin/%{_arch}-nacl-ranlib %{_arch}-nacl-ranlib
popd

mkdir -p out/Release/gen/sdk/linux_x86/nacl_arm_newlib/bin
pushd out/Release/gen/sdk/linux_x86/nacl_arm_newlib/bin
ln -s /usr/bin/arm-nacl-gcc gcc
ln -s /usr/bin/arm-nacl-gcc arm-nacl-gcc
ln -s /usr/bin/arm-nacl-g++ g++
ln -s /usr/bin/arm-nacl-g++ arm-nacl-g++
ln -s /usr/bin/arm-nacl-ar arm-nacl-ar
ln -s /usr/bin/arm-nacl-as arm-nacl-as
ln -s /usr/bin/arm-nacl-ranlib arm-nacl-ranlib
popd

touch out/Release/gen/sdk/linux_x86/nacl_x86_newlib/stamp.untar out/Release/gen/sdk/linux_x86/nacl_x86_newlib/stamp.prep
touch out/Release/gen/sdk/linux_x86/nacl_x86_newlib/nacl_x86_newlib.json
touch out/Release/gen/sdk/linux_x86/nacl_arm_newlib/stamp.untar out/Release/gen/sdk/linux_x86/nacl_arm_newlib/stamp.prep
touch out/Release/gen/sdk/linux_x86/nacl_arm_newlib/nacl_arm_newlib.json

pushd out/Release/gen/sdk/linux_x86/
mkdir -p pnacl_newlib pnacl_translator
# Might be able to do symlinks here, but eh.
cp -a --no-preserve=context /usr/pnacl_newlib/* pnacl_newlib/
cp -a --no-preserve=context /usr/pnacl_translator/* pnacl_translator/
for i in lib/libc.a lib/libc++.a lib/libg.a lib/libm.a; do
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/x86_64_bc-nacl/$i
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/i686_bc-nacl/$i
done

for i in lib/clang/3.7.0/lib/x86_64_bc-nacl/libpnaclmm.a lib/clang/3.7.0/lib/i686_bc-nacl/libpnaclmm.a; do
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/$i
done

popd

mkdir -p native_client/toolchain/.tars/linux_x86
touch native_client/toolchain/.tars/linux_x86/pnacl_translator.json

pushd native_client/toolchain
ln -s ../../out/Release/gen/sdk/linux_x86 linux_x86
popd

%endif

export CHROMIUM_BROWSER_GYP_DEFINES="\
%ifarch x86_64
	-Dtarget_arch=x64 \
	-Dsystem_libdir=lib64 \
%endif
	-Dgoogle_api_key="%{api_key}" \
	-Dgoogle_default_client_id="%{default_client_id}" \
	-Dgoogle_default_client_secret="%{default_client_secret}" \
	-Ddisable_glibc=1 \
%if 0%{?rhel}
	-Ddisable_nacl=1 \
%else
	-Ddisable_newlib_untar=1 \
	-Ddisable_pnacl_untar=1 \
%endif
	-Ddisable_sse2=1 \
	-Duse_gconf=0 \
	-Duse_gio=0 \
	-Duse_gnome_keyring=1 \
	-Duse_pulseaudio=1 \
%if 0%{?fedora}
	-Duse_system_bzip2=1 \
	-Duse_system_flac=1 \
	-Duse_system_harfbuzz=1 \
%if 0%{?fedora} >= 22
	-Duse_system_icu=1 \
%endif
	-Dicu_use_data_file_flag=0 \
	-Duse_system_jsoncpp=1 \
	-Duse_system_libevent=1 \
	-Duse_system_libexif=1 \
	-Duse_system_libjpeg=1 \
	-Duse_system_libpng=1 \
	-Duse_system_libusb=1 \
	-Duse_system_libxml=1 \
	-Duse_system_libxslt=1 \
	-Duse_system_minizip=1 \
	-Duse_system_nspr=1 \
	-Duse_system_opus=1 \
	-Duse_system_protobuf=0 \
	-Duse_system_re2=1 \
	-Duse_system_speex=1 \
	-Duse_system_libsrtp=1 \
	-Duse_system_xdg_utils=1 \
	-Duse_system_yasm=1 \
	-Duse_system_zlib=0 \
	-Duse_system_libevent=1 \
	-Dusb_ids_path=/usr/share/hwdata/usb.ids \
	-Dlinux_link_libspeechd=1 \
	-Dlibspeechd_h_prefix=speech-dispatcher/ \
	-Dpnacl_newlib_toolchain=out/Release/gen/sdk/linux_x86/pnacl_newlib/ \
	-Dpnacl_translator_dir=/usr/pnacl_translator \
%endif
	-Dffmpeg_branding=Chromium \
	-Dproprietary_codecs=0 \
	-Dlinux_link_gnome_keyring=1 \
	-Dlinux_link_gsettings=1 \
	-Dlinux_link_libpci=1 \
	-Dlinux_link_libgps=0 \
	-Dlinux_sandbox_path=%{chromium_path}/chrome-sandbox \
	-Dlinux_sandbox_chrome_path=%{chromium_path}/chromium-browser \
	-Dlinux_strip_binary=1 \
	-Dlinux_use_bundled_binutils=0 \
	-Dlinux_use_bundled_gold=0 \
	-Dlinux_use_gold_binary=0 \
	-Dlinux_use_gold_flags=0 \
	-Dlinux_use_libgps=0 \
	-Dno_strict_aliasing=1 \
	-Dv8_no_strict_aliasing=1 \
	-Dclang=0 \
	-Dhost_clang=0 \
	-Dremove_webcore_debug_symbols=1 \
	-Dlogging_like_official_build=1 \
	-Denable_hotwording=0 \
	-Dwerror="

%if 0%{?fedora}
# Look, I don't know. This package is spit and chewing gum. Sorry.
rm -rf third_party/jinja2 third_party/markupsafe
ln -s %{python_sitelib}/jinja2 third_party/jinja2
ln -s %{python_sitearch}/markupsafe third_party/markupsafe
%endif

# Update gyp files according to our configuration
# If you will change something in the configuration please update it
# for build/gyp_chromium as well (and vice versa).
build/linux/unbundle/replace_gyp_files.py $CHROMIUM_BROWSER_GYP_DEFINES

build/gyp_chromium \
	--depth . \
	$CHROMIUM_BROWSER_GYP_DEFINES

%build

%if %{?tests}
# Tests targets taken from testing/buildbot/chromium.linux.json
export CHROMIUM_BROWSER_UNIT_TESTS="\
	aura_unittests \
	base_unittests \
	browser_tests \
	cacheinvalidation_unittests \
	cast_unittests \
	cc_unittests \
	chromedriver_unittests \
	components_unittests \
	compositor_unittests \
	content_browsertests \
	content_unittests \
	crypto_unittests \
	dbus_unittests \
	device_unittests \
	display_unittests \
	events_unittests \
	extensions_unittests \
	gcm_unit_tests \
	gfx_unittests \
	google_apis_unittests \
	gpu_unittests \
	interactive_ui_tests \
	ipc_mojo_unittests \
	ipc_tests \
	jingle_unittests \
	media_unittests \
	mojo_application_manager_unittests \
	mojo_apps_js_unittests \
	mojo_common_unittests \
	mojo_js_unittests \
	mojo_public_bindings_unittests \
	mojo_public_environment_unittests \
	mojo_public_system_unittests \
	mojo_public_utility_unittests \
	mojo_shell_tests \
	mojo_system_unittests \
	mojo_view_manager_unittests \
%if 0%{?fedora}
	nacl_loader_unittests \
%endif
	net_unittests \
	ppapi_unittests \
	printing_unittests \
	remoting_unittests \
	sandbox_linux_unittests \
	sql_unittests \
	sync_integration_tests \
	ui_unittests \
	sync_unit_tests \
	unit_tests \
	url_unittests \
	views_unittests \
	wm_unittests"
# We are disabling the following tests on RHEL :
# nacl_loader_unittests - we have NaCl disabled
%else
export CHROMIUM_BROWSER_UNIT_TESTS=
%endif

%if %{?debug}
%define target out/Debug
%else
%define target out/Release
%endif

%if 0%{?rhel}
# Set PYTHON PATH to directory which contains python argparse module
export PYTHONPATH=`pwd`/third_party/python-argparse
%endif

../depot_tools/ninja -C %{target} -vvv chrome chrome_sandbox $CHROMIUM_BROWSER_UNIT_TESTS

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromium_path}
cp -a %{SOURCE3} %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
export BUILDTARGET=`cat /etc/redhat-release`
export CHROMIUM_PATH=%{chromium_path}
export CHROMIUM_BROWSER_CHANNEL=%{chromium_browser_channel}
sed -i "s|@@BUILDTARGET@@|$BUILDTARGET|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
sed -i "s|@@CHROMIUM_PATH@@|$CHROMIUM_PATH|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
sed -i "s|@@CHROMIUM_BROWSER_CHANNEL@@|$CHROMIUM_BROWSER_CHANNEL|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
ln -s %{chromium_path}/%{chromium_browser_channel}.sh %{buildroot}%{_bindir}/%{chromium_browser_channel}
mkdir -p %{buildroot}%{_mandir}/man1/

pushd %{target}
cp -a *.pak *.bin locales resources %{buildroot}%{chromium_path}
%if 0%{?fedora}
cp -a nacl_helper* *.nexe %{buildroot}%{chromium_path}
# libppGoogleNaClPluginChrome.so went away?
cp -a protoc pnacl pseudo_locales pyproto tls_edit %{buildroot}%{chromium_path}
chmod -x %{buildroot}%{chromium_path}/nacl_helper_bootstrap* *.nexe
%endif
cp -a chrome %{buildroot}%{chromium_path}/%{chromium_browser_channel}
cp -a chrome_sandbox %{buildroot}%{chromium_path}/chrome-sandbox
cp -a chrome.1 %{buildroot}%{_mandir}/man1/%{chromium_browser_channel}.1
# This is now compiled in too... :/
# cp -a libffmpegsumo.so %%{buildroot}%%{chromium_path}
# Looks like this is compiled in now? *sigh*
# cp -a libpdf.so %%{buildroot}%%{chromium_path}/libpdf.so
%if 0%{?rhel}
cp -a icudtl.dat %{buildroot}%{chromium_path}
%endif
popd

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
cp -a chrome/app/theme/chromium/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{chromium_browser_channel}.png

mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE4}

mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps/
cp -a %{SOURCE8} %{buildroot}%{_datadir}/gnome-control-center/default-apps/

%check
%if %{tests}
	Xvfb :9 -screen 0 1024x768x24 &

	export XVFB_PID=$!
	export DISPLAY=:9
	export LC_ALL="en_US.utf8"

	sleep 5

	# Run tests and disable the failed ones
	# In sandbox_linux_unittests we are disabling most of the tests
	# as RHEL 6 does not have suport for BPF in kernel.
	pushd %{target}
	(
	cp chrome-sandbox chrome-test-sandbox
	echo "Test sandbox needs to be owned by root and have the suid set"
	sudo chown root:root chrome-test-sandbox
	sudo chmod 4755 chrome-test-sandbox

	export CHROME_DEVEL_SANDBOX=`pwd`/chrome-test-sandbox

	./aura_unittests && \
	./base_unittests \
		--gtest_filter=-"\
			OutOfMemoryDeathTest.ViaSharedLibraries\
		" \
	&& \
	./browser_tests \
		--gtest_filter=-"\
			PrerenderBrowserTestWithNaCl.PrerenderNaClPluginEnabled:\
			SandboxStatusUITest.testBPFSandboxEnabled:\
			PlatformAppBrowserTest.AppWindowRestoreState:\
			SyncFileSystemApiTest.GetFileStatuses:\
			SyncFileSystemTest.AuthorizationTest\
			AutofillEditAddressAsyncWebUITest.testAutofillPhoneValueListDoneValidating:\
			BrowserViewTest.DevToolsUpdatesBrowserWindow:\
			CalculatorBrowserTest.Model:\
			ChromeWhispernetClientTest.Audible:\
			ChromeWhispernetClientTest.DecodeSamples:\
			ChromeWhispernetClientTest.DetectBroadcast:\
			ChromeWhispernetClientTest.EncodeToken:\
			ChromeWhispernetClientTest.Initialize:\
			HotwordPrivateApiTest.AlwaysOnEnabled:\
			OptionsUIBrowserTest.VerifyManagedSignout:\
			ProfileManagerBrowserTest.DeletePasswords\
		" \
	&& \
	./cacheinvalidation_unittests && \
	./cast_unittests && \
	./cc_unittests && \
	./chromedriver_unittests && \
	./components_unittests && \
	./compositor_unittests && \
	./content_browsertests && \
	./content_unittests \
		--gtest_filter=-"\
			SharedCryptoTest.AesKwRawSymkeyUnwrapCorruptData\
		" \
	&& \
	./crypto_unittests && \
	./dbus_unittests \
		--gtest_filter=-"\
			EndToEndAsyncTest.InvalidObjectPath:\
			EndToEndAsyncTest.InvalidServiceName:\
			EndToEndSyncTest.InvalidObjectPath:\
			EndToEndSyncTest.InvalidServiceName:\
			MessageTest.SetInvalidHeaders\
		" \
	&& \
	./device_unittests && \
	./display_unittests && \
	./events_unittests && \
	./extensions_unittests && \
	./gcm_unit_tests && \
	./gfx_unittests \
		--gtest_filter=-"\
			FontListTest.Fonts_GetHeight_GetBaseline:\
			FontRenderParamsTest.Default:\
			FontRenderParamsTest.ForceFullHintingWhenAntialiasingIsDisabled:\
			FontRenderParamsTest.MissingFamily:\
			FontRenderParamsTest.OnlySetConfiguredValues:\
			FontRenderParamsTest.Scalable:\
			FontRenderParamsTest.Size:\
			FontRenderParamsTest.Style:\
			FontRenderParamsTest.SubstituteFamily:\
			FontRenderParamsTest.UseBitmaps:\
			FontTest.GetActualFontNameForTesting:\
			FontTest.LoadArial:\
			FontTest.LoadArialBold:\
			PlatformFontPangoTest.FamilyList:\
			RenderTextTest.SetFontList:\
			RenderTextTest.StringSizeRespectsFontListMetrics\
		" \
	&& \
	./google_apis_unittests && \
	./gpu_unittests && \
	./interactive_ui_tests \
		--gtest_filter=-"\
			OmniboxViewViewsTest.DeactivateTouchEditingOnExecuteCommand:\
			OmniboxViewViewsTest.SelectAllOnTap\
		" \
	&& \
	./ipc_mojo_unittests && \
	./ipc_tests && \
	./jingle_unittests && \
	./media_unittests && \
	./mojo_application_manager_unittests && \
	./mojo_apps_js_unittests && \
	./mojo_common_unittests && \
	./mojo_js_unittests && \
	./mojo_public_bindings_unittests && \
	./mojo_public_environment_unittests && \
	./mojo_public_system_unittests && \
	./mojo_public_utility_unittests && \
	./mojo_shell_tests && \
	./mojo_system_unittests && \
	./mojo_view_manager_unittests && \
%if 0%{?fedora}
	./nacl_loader_unittests && \
%endif
	./net_unittests \
		--gtest_filter=-"\
			EndToEndTests/EndToEndTest.*:\
			QuicEndToEndTest.LargeGetWithNoPacketLoss:\
			QuicEndToEndTest.LargePostWithPacketLoss:\
			QuicEndToEndTest.UberTest:\
			Spdy/SpdyNetworkTransactionNoTLSUsageCheckTest.TLSCipherSuiteSucky/0:\
			Spdy/SpdyNetworkTransactionNoTLSUsageCheckTest.TLSCipherSuiteSucky/1:\
			Spdy/SpdyNetworkTransactionNoTLSUsageCheckTest.TLSCipherSuiteSucky/2:\
			Spdy/SpdyNetworkTransactionNoTLSUsageCheckTest.TLSVersionTooOld/0:\
			Spdy/SpdyNetworkTransactionNoTLSUsageCheckTest.TLSVersionTooOld/1:\
			Spdy/SpdyNetworkTransactionNoTLSUsageCheckTest.TLSVersionTooOld/2:\
			Spdy/SpdyNetworkTransactionTLSUsageCheckTest.TLSCipherSuiteSucky/0:\
			Spdy/SpdyNetworkTransactionTLSUsageCheckTest.TLSVersionTooOld/0\
		" \
	&& \
	./ppapi_unittests && \
	./printing_unittests && \
	./remoting_unittests && \
	./sandbox_linux_unittests \
		--gtest_filter=-"\
			BaselinePolicy.*:\
			SandboxBPF.*:\
			BPFDSL.*:\
			BPFTest.*:\
			ParameterRestrictions.*:\
			Syscall.SyntheticSixArgs\
		" \
	./sql_unittests && \
	./ui_unittests && \
	./sync_unit_tests && \
	./unit_tests \
		--gtest_filter=-"\
			SpellCheckTest.CreateTextCheckingResults:\
			SpellCheckTest.DictionaryFiles:\
			SpellCheckTest.EnglishWords:\
			SpellCheckTest.GetAutoCorrectionWord_EN_US:\
			SpellCheckTest.LogicalSuggestions:\
			SpellCheckTest.MisspelledWords:\
			SpellCheckTest.NoSuggest:\
			SpellCheckTest.SpellCheckParagraphLongSentenceMultipleMisspellings:\
			SpellCheckTest.SpellCheckParagraphMultipleMisspellings:\
			SpellCheckTest.SpellCheckParagraphSingleMisspellings:\
			SpellCheckTest.SpellCheckStrings_EN_US:\
			SpellCheckTest.SpellCheckSuggestions_EN_US:\
			SpellCheckTest.SpellingEngine_CheckSpelling:\
			SpellCheckTest.RequestSpellCheckWithMisspellings:\
			SpellCheckTest.RequestSpellCheckWithMultipleRequests:\
			SpellCheckTest.RequestSpellCheckWithSingleMisspelling\
		" \
	&& \
	./url_unittests && \
	./views_unittests \
		--gtest_filter=-"\
			DesktopWindowTreeHostX11Test.Shape:\
			LabelTest.FontPropertySymbol:\
			WidgetTest.WindowMouseModalityTest\
		" \
	&& \
	./wm_unittests \
	) || (kill $XVFB_PID || unset XVFB_PID)
	popd

	kill $XVFB_PID
	unset XVFB_PID
%endif

%clean
rm -rf %{buildroot}

%post
# Set SELinux labels
# Not sure how to fix this yet. Changing the pathing in the semanage commands does not work.
# ValueError: File spec /usr/lib64/chromium-browser/chromium-browser conflicts with equivalency rule '/usr/lib64 /usr/lib'; Try adding '/usr/lib/chromium-browser/chromium-browser' instead
# ValueError: File spec /usr/lib64/chromium-browser/chromium-browser.sh conflicts with equivalency rule '/usr/lib64 /usr/lib'; Try adding '/usr/lib/chromium-browser/chromium-browser.sh' instead
# ValueError: File spec /usr/lib64/chromium-browser/chrome-sandbox conflicts with equivalency rule '/usr/lib64 /usr/lib'; Try adding '/usr/lib/chromium-browser/chrome-sandbox' instead

semanage fcontext -a -t execmem_exec_t %{chromium_path}/%{chromium_browser_channel}
semanage fcontext -a -t bin_t %{chromium_path}/%{chromium_browser_channel}.sh
semanage fcontext -a -t chrome_sandbox_exec_t %{chromium_path}/chrome-sandbox
restorecon -R -v %{chromium_path}/%{chromium_browser_channel}

touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root,-)
%{_bindir}/%{chromium_browser_channel}
%dir %{chromium_path}
%{chromium_path}/*.bin
%{chromium_path}/*.pak
%{chromium_path}/%{chromium_browser_channel}
%{chromium_path}/%{chromium_browser_channel}.sh
%if 0%{?fedora}
%{chromium_path}/nacl_helper*
%{chromium_path}/protoc
%{chromium_path}/tls_edit
%{chromium_path}/*.nexe
# %%{chromium_path}/libppGoogleNaClPluginChrome.so
# %%{chromium_path}/remoting_locales/
%{chromium_path}/pseudo_locales/
%{chromium_path}/pnacl/
# %%{chromium_path}/plugins/
%{chromium_path}/pyproto/
%endif
%attr(4755, root, root) %{chromium_path}/chrome-sandbox
# %%{chromium_path}/libffmpegsumo.so
# %%{chromium_path}/libpdf.so
%if 0%{?rhel}
%{chromium_path}/icudtl.dat
%endif
%{chromium_path}/locales/
%{chromium_path}/resources/
%{_mandir}/man1/%{chromium_browser_channel}.*
%{_datadir}/icons/hicolor/256x256/apps/%{chromium_browser_channel}.png
%{_datadir}/applications/*.desktop
%{_datadir}/gnome-control-center/default-apps/chromium-browser.xml

%changelog
* Fri Oct 23 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.80-1
- update to 46.0.2490.80

* Thu Oct 15 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.71-1
- update to 46.0.2490.71

* Thu Oct 15 2015 Tom Callaway <spot@fedoraproject.org> 45.0.2454.101-2
- fix icu handling for f21 and older

* Mon Oct  5 2015 Tom Callaway <spot@fedoraproject.org> 45.0.2454.101-1
- update to 45.0.2454.101

* Thu Jun 11 2015 Tom Callaway <spot@fedoraproject.org> 43.0.2357.124-1
- update to 43.0.2357.124

* Tue Jun  2 2015 Tom Callaway <spot@fedoraproject.org> 43.0.2357.81-1
- update to 43.0.2357.81

* Thu Feb 26 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.115-1
- update to 40.0.2214.115

* Thu Feb 19 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.111-1
- update to 40.0.2214.111

* Mon Feb  2 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.94-1
- update to 40.0.2214.94

* Tue Jan 27 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.93-1
- update to 40.0.2214.93

* Sat Jan 24 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.91-1
- update to 40.0.2214.91

* Wed Jan 21 2015 Tom Callaway <spot@fedoraproject.org> 39.0.2171.95-3
- use bundled icu on Fedora < 21, we need 5.2

* Tue Jan  6 2015 Tom Callaway <spot@fedoraproject.org> 39.0.2171.95-2
- rebase off Tomas's spec file for Fedora

* Fri Dec 12 2014 Tomas Popela <tpopela@redhat.com> 39.0.2171.95-1
- Update to 39.0.2171.95
- Resolves: rhbz#1173448

* Wed Nov 26 2014 Tomas Popela <tpopela@redhat.com> 39.0.2171.71-1
- Update to 39.0.2171.71
- Resolves: rhbz#1168128

* Wed Nov 19 2014 Tomas Popela <tpopela@redhat.com> 39.0.2171.65-2
- Revert the chrome-sandbox rename to chrome_sandbox
- Resolves: rhbz#1165653

* Wed Nov 19 2014 Tomas Popela <tpopela@redhat.com> 39.0.2171.65-1
- Update to 39.0.2171.65
- Use Red Hat Developer Toolset for compilation
- Set additional SELinux labels
- Add more unit tests
- Resolves: rhbz#1165653

* Fri Nov 14 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.122-1
- Update to 38.0.2125.122
- Resolves: rhbz#1164116

* Wed Oct 29 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.111-1
- Update to 38.0.2125.111
- Resolves: rhbz#1158347

* Fri Oct 24 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.104-2
- Fix the situation when the return key (and keys from numpad) does not work
  in HTML elements with input
- Resolves: rhbz#1153988
- Dynamically determine the presence of the PepperFlash plugin
- Resolves: rhbz#1154118

* Thu Oct 16 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.104-1
- Update to 38.0.2125.104
- Resolves: rhbz#1153012

* Thu Oct 09 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.101-2
- The boringssl is used for tests, without the possibility of using
  the system openssl instead. Remove the openssl and boringssl sources
  when not building the tests.
- Resolves: rhbz#1004948

* Wed Oct 08 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.101-1
- Update to 38.0.2125.101
- System openssl is used for tests, otherwise the bundled boringssl is used
- Don't build with clang
- Resolves: rhbz#1004948

* Wed Sep 10 2014 Tomas Popela <tpopela@redhat.com> 37.0.2062.120-1
- Update to 37.0.2062.120
- Resolves: rhbz#1004948

* Wed Aug 27 2014 Tomas Popela <tpopela@redhat.com> 37.0.2062.94-1
- Update to 37.0.2062.94
- Include the pdf viewer library

* Wed Aug 13 2014 Tomas Popela <tpopela@redhat.com> 36.0.1985.143-1
- Update to 36.0.1985.143
- Use system openssl instead of bundled one
- Resolves: rhbz#1004948

* Thu Jul 17 2014 Tomas Popela <tpopela@redhat.com> 36.0.1985.125-1
- Update to 36.0.1985.125
- Add libexif as BR
- Resolves: rhbz#1004948

* Wed Jun 11 2014 Tomas Popela <tpopela@redhat.com> 35.0.1916.153-1
- Update to 35.0.1916.153
- Resolves: rhbz#1004948

* Wed May 21 2014 Tomas Popela <tpopela@redhat.com> 35.0.1916.114-1
- Update to 35.0.1916.114
- Bundle python-argparse
- Resolves: rhbz#1004948

* Wed May 14 2014 Tomas Popela <tpopela@redhat.com> 34.0.1847.137-1
- Update to 34.0.1847.137
- Resolves: rhbz#1004948

* Mon May 5 2014 Tomas Popela <tpopela@redhat.com> 34.0.1847.132-1
- Update to 34.0.1847.132
- Bundle depot_tools and switch from make to ninja
- Remove PepperFlash
- Resolves: rhbz#1004948

* Mon Feb 3 2014 Tomas Popela <tpopela@redhat.com> 32.0.1700.102-1
- Update to 32.0.1700.102

* Thu Jan 16 2014 Tomas Popela <tpopela@redhat.com> 32.0.1700.77-1
- Update to 32.0.1700.77
- Properly kill Xvfb when tests fails
- Add libdrm as BR
- Add libcap as BR

* Tue Jan 7 2014 Tomas Popela <tpopela@redhat.com> 31.0.1650.67-2
- Minor changes in spec files and scripts
- Add Xvfb as BR for tests
- Add policycoreutils-python as Requires
- Compile unittests and run them in chech phase, but turn them off by default
  as many of them are failing in Brew

* Thu Dec 5 2013 Tomas Popela <tpopela@redhat.com> 31.0.1650.67-1
- Update to 31.0.1650.63

* Thu Nov 21 2013 Tomas Popela <tpopela@redhat.com> 31.0.1650.57-1
- Update to 31.0.1650.57

* Wed Nov 13 2013 Tomas Popela <tpopela@redhat.com> 31.0.1650.48-1
- Update to 31.0.1650.48
- Minimal supported RHEL6 version is now RHEL 6.5 due to GTK+

* Fri Oct 25 2013 Tomas Popela <tpopela@redhat.com> 30.0.1599.114-1
- Update to 30.0.1599.114
- Hide the infobar with warning that this version of OS is not supported
- Polished the chromium-latest.py

* Thu Oct 17 2013 Tomas Popela <tpopela@redhat.com> 30.0.1599.101-1
- Update to 30.0.1599.101
- Minor changes in scripts

* Wed Oct 2 2013 Tomas Popela <tpopela@redhat.com> 30.0.1599.66-1
- Update to 30.0.1599.66
- Automated the script for cleaning the proprietary sources from ffmpeg.

* Thu Sep 19 2013 Tomas Popela <tpopela@redhat.com> 29.0.1547.76-1
- Update to 29.0.1547.76
- Added script for removing the proprietary sources from ffmpeg. This script is called during cleaning phase of ./chromium-latest --rhel

* Mon Sep 16 2013 Tomas Popela <tpopela@redhat.com> 29.0.1547.65-2
- Compile with Dproprietary_codecs=0 and Dffmpeg_branding=Chromium to disable proprietary codecs (i.e. MP3)

* Mon Sep 9 2013 Tomas Popela <tpopela@redhat.com> 29.0.1547.65-1
- Initial version based on Tom Callaway's <spot@fedoraproject.org> work

