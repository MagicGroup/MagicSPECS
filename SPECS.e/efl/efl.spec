%global _hardened_build 1

%ifarch %{arm} %{ix86} x86_64
%global has_luajit 1
%endif

# Look, you probably don't want this. scim is so 2012. ibus is the new hotness.
# Enabling this means you'll almost certainly need to pass ECORE_IMF_MODULE=xim 
# to get anything to work. (*cough*terminology*cough*)
%global with_scim 0

%global use_wayland 0

Name:		efl
Version:	1.15.2
Release:	3%{?dist}
Summary:	Collection of Enlightenment libraries
Summary(zh_CN.UTF-8): Enlightenment 桌面环境的库集合
License:	BSD and LGPLv2+ and GPLv2 and zlib
URL:		http://enlightenment.org/
Source0:	http://download.enlightenment.org/rel/libs/efl/efl-%{version}.tar.xz
# I think this one is Fedora specific.
Patch0:		efl-1.11.4-tslibfix.patch
# Fix compilation for lua-devel > 5.1
Patch1:		efl-lua-5.2-global.patch
BuildRequires:	bullet-devel libpng-devel libjpeg-devel gstreamer1-devel zlib-devel
BuildRequires:	gstreamer1-plugins-base-devel libtiff-devel openssl-devel
BuildRequires:	curl-devel dbus-devel glibc-devel fontconfig-devel freetype-devel
BuildRequires:	fribidi-devel pulseaudio-libs-devel libsndfile-devel libX11-devel
BuildRequires:	libXau-devel libXcomposite-devel libXdamage-devel libXdmcp-devel
BuildRequires:	libXext-devel libXfixes-devel libXinerama-devel libXrandr-devel
BuildRequires:	libXrender-devel libXScrnSaver-devel libXtst-devel libXcursor-devel
BuildRequires:	libXp-devel libXi-devel mesa-libGL-devel mesa-libEGL-devel
BuildRequires:	libblkid-devel libmount-devel systemd-devel harfbuzz-devel 
BuildRequires:	libwebp-devel tslib-devel SDL2-devel SDL-devel c-ares-devel
%if %{with_scim}
BuildRequires:	scim-devel
%endif
BuildRequires:	ibus-devel
BuildRequires:	doxygen systemd giflib-devel openjpeg-devel libdrm-devel
%if %{use_wayland}
BuildRequires:	mesa-libwayland-egl-devel libwayland-client-devel
%endif
BuildRequires:	autoconf automake libtool gettext-devel mesa-libGLES-devel
BuildRequires:	mesa-libgbm-devel libinput-devel
%if 0%{?has_luajit}
BuildRequires:	luajit-devel
%else
BuildRequires:	lua-devel
%endif
# These are convenience provides to aid in migration
Provides:	e_dbus%{?_isa} = %{version}-%{release}
Provides:	e_dbus = %{version}-%{release}
Obsoletes:	e_dbus <= 1.7.10
Provides:	ecore = %{version}-%{release}
Provides:	ecore%{?_isa} = %{version}-%{release}
Obsoletes:	ecore <= 1.7.10
Provides:	edje = %{version}-%{release}
Provides:	edje%{?_isa} = %{version}-%{release}
Obsoletes:	edje <= 1.7.10
Provides:	eet = %{version}-%{release}
Provides:	eet%{?_isa} = %{version}-%{release}
Obsoletes:	eet <= 1.7.10
Provides:	eeze = %{version}-%{release}
Provides:	eeze%{?_isa} = %{version}-%{release}
Obsoletes:	eeze <= 1.7.10
Provides:	efreet = %{version}-%{release}
Provides:	efreet%{?_isa} = %{version}-%{release}
Obsoletes:	efreet <= 1.7.10
Provides:	eina%{?_isa} = %{version}-%{release}
Provides:	eio = %{version}-%{release}
Provides:	eio%{?_isa} = %{version}-%{release}
Obsoletes:	eio <= 1.7.10
Provides:	eldbus%{?_isa} = %{version}-%{release}
Provides:	elocation%{?_isa} = %{version}-%{release}
Provides:	elua%{?_isa} = %{version}-%{release}
Provides:	embryo = %{version}-%{release}
Provides:	embryo%{?_isa} = %{version}-%{release}
Obsoletes:	embryo <= 1.7.10
Provides:	emotion = %{version}-%{release}
Provides:	emotion%{?_isa} = %{version}-%{release}
Obsoletes:	emotion <= 1.7.10
Provides:	eo%{?_isa} = %{version}-%{release}
Provides:	eolian%{?_isa} = %{version}-%{release}
Provides:	ephysics%{?_isa} = %{version}-%{release}
Provides:	ethumb = %{version}-%{release}
Provides:	ethumb%{?_isa} = %{version}-%{release}
Obsoletes:	ethumb <= 1.7.10
Provides:	evas = %{version}-%{release}
Provides:	evas%{?_isa} = %{version}-%{release}
Obsoletes:	evas <= 1.7.10
Provides:	libeina = %{version}-%{release}
Provides:	libeina%{?_isa} = %{version}-%{release}
Obsoletes:	libeina <= 1.7.10

%description
EFL is a collection of libraries for handling many common tasks a
developer may have such as data structures, communication, rendering,
widgets and more.

%description -l zh_CN.UTF-8
Enlightenment 桌面环境的基本库集合。

%package devel
Summary:	Development files for EFL
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:	efl%{?_isa} = %{version}-%{release}
Requires:	pkgconfig, libX11-devel
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
Provides:	e_dbus-devel%{?_isa} = %{version}-%{release}
Provides:	e_dbus-devel = %{version}-%{release}
Obsoletes:	e_dbus-devel <= 1.7.10
Provides:	ecore-devel = %{version}-%{release}
Provides:	ecore-devel%{?_isa} = %{version}-%{release}
Obsoletes:	ecore-devel <= 1.7.10
Provides:	edje-devel = %{version}-%{release}
Provides:	edje-devel%{?_isa} = %{version}-%{release}
Obsoletes:	edje-devel <= 1.7.10
Provides:	eet-devel = %{version}-%{release}
Provides:	eet-devel%{?_isa} = %{version}-%{release}
Obsoletes:	eet-devel <= 1.7.10
Provides:	eeze-devel = %{version}-%{release}
Provides:	eeze-devel%{?_isa} = %{version}-%{release}
Obsoletes:	eeze-devel <= 1.7.10
Provides:	efreet-devel = %{version}-%{release}
Provides:	efreet-devel%{?_isa} = %{version}-%{release}
Obsoletes:	efreet-devel <= 1.7.10
Provides:	eina-devel%{?_isa} = %{version}-%{release}
Provides:	eio-devel = %{version}-%{release}
Provides:	eio-devel%{?_isa} = %{version}-%{release}
Obsoletes:	eio-devel <= 1.7.10
Provides:	eldbus-devel%{?_isa} = %{version}-%{release}
Provides:	elocation-devel%{?_isa} = %{version}-%{release}
Provides:	embryo-devel = %{version}-%{release}
Provides:	embryo-devel%{?_isa} = %{version}-%{release}
Obsoletes:	embryo-devel <= 1.7.10
Provides:	emotion-devel = %{version}-%{release}
Provides:	emotion-devel%{?_isa} = %{version}-%{release}
Obsoletes:	emotion-devel <= 1.7.10
Provides:	eo-devel%{?_isa} = %{version}-%{release}
Provides:	eolian-devel%{?_isa} = %{version}-%{release}
Provides:	ephysics-devel%{?_isa} = %{version}-%{release}
Provides:	ethumb-devel = %{version}-%{release}
Provides:	ethumb-devel%{?_isa} = %{version}-%{release}
Obsoletes:	ethumb-devel <= 1.7.10
Provides:	evas-devel = %{version}-%{release}
Provides:	evas-devel%{?_isa} = %{version}-%{release}
Obsoletes:	evas-devel <= 1.7.10
Provides:	libeina-devel = %{version}-%{release}
Provides:	libeina-devel%{?_isa} = %{version}-%{release}
Obsoletes:	libeina-devel <= 1.7.10

%description devel
Development files for EFL.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1 -b .tslibfix
%if ! 0%{?has_luajit}
%patch1 -p1 -b .luaglobal
%endif
autoreconf -ifv

# This is why hardcoding paths is bad.
sed -i -e 's|/opt/efl-%{version}/share/|%{_datadir}/|' \
  data/libeo.so.%{version}-gdb.py

%build
# The arm-wide disablement of neon is not right
# but i'm not sure which targets allow for neon at compile.
%configure \
	--enable-xinput22 \
	--enable-systemd \
	--enable-image-loader-webp \
	--enable-harfbuzz \
	--enable-sdl \
	--enable-ibus \
%if %{with_scim}
	--enable-scim \
%else
	--disable-scim \
	--enable-i-really-know-what-i-am-doing-and-that-this-will-probably-break-things-and-i-will-fix-them-myself-and-send-patches-aba \
%endif
	--enable-fb \
%if %{use_wayland}
	--enable-wayland \
%endif
	--enable-drm \
	--enable-drm-hw-accel \
	--with-opengl=full \
	--disable-static \
	--with-profile=release \
%ifarch %{arm}
	--disable-neon \
%endif
%if ! 0%{?has_luajit}
	--enable-lua-old \
%endif
	--with-systemdunitdir=%{_unitdir}
make %{?_smp_mflags} V=1
# This makes doxygen segfault. :/
# make %{?_smp_mflags} doc V=1

%install
make install DESTDIR=%{buildroot}

# fix perms
chmod -x src/bin/edje/edje_cc_out.c

find %{buildroot} -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang %{name}

%post
/sbin/ldconfig
%systemd_post ethumb.service
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi
/sbin/ldconfig
%systemd_postun_with_restart ethumb.service

%posttrans
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%preun
%systemd_preun ethumb.service

%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license COPYING licenses/COPYING.BSD licenses/COPYING.GPL licenses/COPYING.LGPL licenses/COPYING.SMALL
%doc AUTHORS COMPLIANCE NEWS README
%{_libdir}/libefl.so.1*
%{_bindir}/efl_debug
%{_bindir}/efl_debugd
# ecore
%{_bindir}/ecore_evas_convert
%{_libdir}/ecore/
%{_libdir}/ecore_evas/
%{_libdir}/ecore_imf/
%{_libdir}/ecore_x/
%{_libdir}/libecore*.so.*
%{_datadir}/ecore/
%{_datadir}/ecore_imf/
%{_datadir}/ecore_x/
%{_libdir}/libector.so.*
# edje
%{_bindir}/edje*
%{_datadir}/mime/packages/edje.xml
%{_libdir}/edje/
%{_libdir}/libedje.so.1*
# eet
%{_bindir}/diffeet
%{_bindir}/eet
%{_bindir}/eetpack
%{_bindir}/vieet
%{_libdir}/libeet.so.*
# eeze
%{_bindir}/eeze_*
%{_libdir}/eeze/
%{_libdir}/libeeze.so.1*
# efreet
%{_bindir}/efreetd
# we don't depend on dbus, but we want clean dir ownership here.
%dir %{_datadir}/dbus-1/
%dir %{_datadir}/dbus-1/services/
%{_libdir}/efreet/
%{_libdir}/libefreet.so.1*
%{_libdir}/libefreet_mime.so.1*
%{_libdir}/libefreet_trash.so.1*
# eina
%{_bindir}/eina_btlog
%{_libdir}/libeina.so.*
# eio
%{_libdir}/libeio.so.1*
# eldbus
%{_bindir}/eldbus-codegen
%{_libdir}/libeldbus.so.1*
# elocation
%{_libdir}/libelocation.so.1*
# elua
%if 0%{?has_luajit}
%{_bindir}/elua
%{_datadir}/elua/
%{_libdir}/libelua.so.1*
%else
%exclude %{_datadir}/elua/
%endif
# embryo
%{_bindir}/embryo_cc
%{_libdir}/libembryo.so.1*
%{_libdir}/libemile.so.*
# emotion
%{_libdir}/emotion/
%{_libdir}/libemotion.so.1*
# eo
%{_libdir}/libeo.so.1*
# eolian
%{_bindir}/eolian_cxx
%{_bindir}/eolian_gen
%{_libdir}/libeolian.so.1*
# ephysics
%{_libdir}/libephysics.so.1*
# ethumb
%{_bindir}/ethumb
%{_bindir}/ethumbd
%{_bindir}/ethumbd_client
%{_unitdir}/ethumb.service
%{_libdir}/ethumb/
%{_libdir}/ethumb_client/
%{_libdir}/libethumb.so.1*
%{_libdir}/libethumb_client.so.1*
%{_datadir}/dbus-1/services/org.enlightenment.Ethumb.service
%{_datadir}/ethumb
%{_datadir}/ethumb_client
# evas
%{_bindir}/evas_*
%{_libdir}/evas/
%{_libdir}/libevas.so.*
%{_datadir}/evas/

%files devel
%{_includedir}/efl-1/
%{_includedir}/efl-cxx-1/
%{_libdir}/cmake/Efl/
%{_libdir}/libefl.so
%{_libdir}/pkgconfig/efl-cxx.pc
%{_libdir}/pkgconfig/efl.pc
# ecore-devel
%{_includedir}/ecore-1/
%{_includedir}/ecore-audio-1/
%{_includedir}/ecore-audio-cxx-1/
%{_includedir}/ecore-avahi-1/
%{_includedir}/ecore-con-1/
%{_includedir}/ecore-cxx-1/
%{_includedir}/ecore-drm-1/
%{_includedir}/ecore-evas-1/
%{_includedir}/ecore-fb-1/
%{_includedir}/ecore-file-1/
%{_includedir}/ecore-imf-1/
%{_includedir}/ecore-imf-evas-1/
%{_includedir}/ecore-input-1/
%{_includedir}/ecore-input-evas-1/
%{_includedir}/ecore-ipc-1/
%{_includedir}/ecore-sdl-1/
%if %{use_wayland}
%{_includedir}/ecore-wayland-1/
%endif
%{_includedir}/ecore-x-1/
%{_libdir}/cmake/Ecore*/
%{_libdir}/libecore*.so
%{_libdir}/pkgconfig/ecore*.pc
%{_includedir}/ector-1/
%{_libdir}/libector.so
%{_libdir}/pkgconfig/ector.pc
# edje-devel
%{_libdir}/libedje.so
%{_libdir}/pkgconfig/edje*.pc
%{_datadir}/edje
%{_includedir}/edje-*
%{_libdir}/cmake/Edje/
# eet-devel
%{_includedir}/eet-1/
%{_includedir}/eet-cxx-1/
%{_libdir}/cmake/Eet/
%{_libdir}/cmake/EetCxx/
%{_libdir}/pkgconfig/eet*.pc
%{_libdir}/libeet.so
# eeze-devel
%{_includedir}/eeze-1/
%{_libdir}/cmake/Eeze/
%{_libdir}/libeeze.so
%{_datadir}/eeze/
%{_libdir}/pkgconfig/eeze.pc
# efreet-devel
%{_includedir}/efreet-1/
%{_libdir}/cmake/Efreet/
%{_libdir}/libefreet.so
%{_libdir}/libefreet_mime.so
%{_libdir}/libefreet_trash.so
%{_datadir}/efreet/
%{_libdir}/pkgconfig/efreet.pc
%{_libdir}/pkgconfig/efreet-mime.pc
%{_libdir}/pkgconfig/efreet-trash.pc
# eina-devel
%{_bindir}/eina-bench-cmp
%{_includedir}/eina-1/
%{_includedir}/eina-cxx-1/
%{_libdir}/cmake/Eina*/
%{_libdir}/pkgconfig/eina*.pc
%{_libdir}/libeina.so
# eio-devel
%{_includedir}/eio-1/
%{_includedir}/eio-cxx-1/
%{_libdir}/libeio.so
%{_libdir}/pkgconfig/eio.pc
%{_libdir}/pkgconfig/eio-cxx.pc
%{_libdir}/cmake/Eio/
# eldbus-devel
%{_includedir}/eldbus-1/
%{_includedir}/eldbus_cxx-1/
%{_libdir}/cmake/Eldbus/
%{_libdir}/libeldbus.so
%{_libdir}/pkgconfig/eldbus.pc
# elocation-devel
%{_includedir}/elocation-1/
%{_libdir}/libelocation.so
%{_libdir}/pkgconfig/elocation.pc
# elua-devel
%if 0%{?has_luajit}
%{_includedir}/elua-1/
%{_libdir}/libelua.so
%{_libdir}/pkgconfig/elua.pc
%{_libdir}/cmake/Elua/
%else
%exclude %{_libdir}/cmake/Elua/
%endif
# embryo-devel
%{_includedir}/embryo-1/
%{_libdir}/libembryo.so
%{_libdir}/pkgconfig/embryo.pc
%{_datadir}/embryo/
%{_includedir}/emile-1/
%{_libdir}/cmake/Emile/
%{_libdir}/libemile.so
%{_libdir}/pkgconfig/emile.pc
# emotion-devel
%{_includedir}/emotion-1/
%{_libdir}/cmake/Emotion/
%{_libdir}/libemotion.so
%{_libdir}/pkgconfig/emotion.pc
%{_datadir}/emotion/
# eo-devel
%{_includedir}/eo-1/
%{_includedir}/eo-cxx-1/
%{_libdir}/cmake/Eo/
%{_libdir}/cmake/EoCxx/
%{_libdir}/libeo.so
%{_libdir}/pkgconfig/eo.pc
%{_libdir}/pkgconfig/eo-cxx.pc
%{_datadir}/eo/
%{_datadir}/gdb/auto-load/%{_libdir}/libeo.so*
# eolian-devel
%{_includedir}/eolian-1/
%{_includedir}/eolian-cxx-1/
%{_libdir}/cmake/Eolian/
%{_libdir}/cmake/EolianCxx/
%{_libdir}/pkgconfig/eolian.pc
%{_libdir}/pkgconfig/eolian-cxx.pc
%{_libdir}/libeolian.so
%{_datadir}/eolian/
# ephysics-devel
%{_includedir}/ephysics-1/
%{_libdir}/libephysics.so
%{_libdir}/pkgconfig/ephysics.pc
# ethumb-devel
%{_includedir}/ethumb-1/
%{_includedir}/ethumb-client-1/
%{_libdir}/cmake/Ethumb/
%{_libdir}/cmake/EthumbClient/
%{_libdir}/libethumb.so
%{_libdir}/libethumb_client.so
%{_libdir}/pkgconfig/ethumb.pc
%{_libdir}/pkgconfig/ethumb_client.pc
# evas-devel
%{_includedir}/evas-1/
%{_includedir}/evas-cxx-1/
%{_libdir}/libevas.so
%{_libdir}/cmake/Evas/
%{_libdir}/cmake/EvasCxx/
%{_libdir}/pkgconfig/evas*.pc

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.15.2-3
- 为 Magic 3.0 重建

* Wed Oct 14 2015 Liu Di <liudidi@gmail.com> - 1.15.2-2
- 为 Magic 3.0 重建

* Wed Oct 14 2015 Liu Di <liudidi@gmail.com> - 1.15.2-1
- 更新到 1.15.2

* Sun Sep 06 2015 Liu Di <liudidi@gmail.com> - 1.15.1-2
- 为 Magic 3.0 重建

* Fri Aug 28 2015 Tom Callaway <spot@fedoraproject.org> - 1.15.1-1
- update to 1.15.1

* Mon Aug 10 2015 Tom Callaway <spot@fedoraproject.org> - 1.15.0-1
- update to 1.15.0

* Tue Jul  7 2015 Tom Callaway <spot@fedoraproject.org> - 1.14.2-1
- disable scim by default
- update to 1.14.2

* Sun Jul  5 2015 Conrad Meyer <cemeyer@uw.edu> - 1.14.1-3
- Install eo_gdb autoload script with correct path

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun  3 2015 Tom Callaway <spot@fedoraproject.org> - 1.14.1-1
- update to 1.14.1

* Thu May 28 2015 Tom Callaway <spot@fedoraproject.org> - 1.14.0-1
- update to 1.14.0
- disable wayland support (bz 1214597)

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.13.2-3
- Rebuilt for GCC 5 C++11 ABI change

* Wed Apr  8 2015 Dan Horák <dan[at]danny.cz> - 1.13.2-2
- use luajit only where available

* Mon Apr  6 2015 Tom Callaway <spot@fedoraproject.org> - 1.13.2-1
- update to 1.13.2

* Tue Mar 31 2015 Tom Callaway <spot@fedoraproject.org> - 1.13.1-7
- add dbus dir ownership

* Mon Mar 30 2015 Tom Callaway <spot@fedoraproject.org> - 1.13.1-6
- fix provides/obsoletes to replace old split out packages with efl
- add scriptlets for mimeinfo handling
- mark COPYING as a license file

* Wed Mar 18 2015 Tom Callaway <spot@fedoraproject.org> - 1.13.1-5
- own cmake dirs, not just cmake files

* Mon Mar 16 2015 Tom Callaway <spot@fedoraproject.org> - 1.13.1-4
- drop incorrect patch, do not enable gl-drm

* Thu Mar  5 2015 Tom Callaway <spot@fedoraproject.org> - 1.13.1-3
- add e_dbus Provides/Obsoletes

* Fri Feb 27 2015 Tom Callaway <spot@fedoraproject.org> - 1.13.1-1
- drop subpackages
- update to 1.13.1

* Mon Dec 15 2014 Tom Callaway <spot@fedoraproject.org> - 1.12.2-1
- initial package
