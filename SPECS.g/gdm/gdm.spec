%global _hardened_build 1

%define libauditver 1.0.6
%define pango_version 1.2.0
%define gtk3_version 2.99.2
%define pam_version 0.99.8.1-11
%define desktop_file_utils_version 0.2.90
%define nss_version 3.11.1
%define fontconfig_version 2.6.0

Summary: The GNOME Display Manager
Summary(zh_CN.UTF-8): GNOME 的登录管理器
Name: gdm
Version:	3.18.2
Release: 1%{?dist}
Epoch: 1
License: GPLv2+
Group: User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
URL: http://download.gnome.org/sources/gdm
#VCS: git:git://git.gnome.org/gdm
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source: http://download.gnome.org/sources/gdm/%{majorver}/gdm-%{version}.tar.xz
Source1: org.gnome.login-screen.gschema.override

Requires(pre): /usr/sbin/useradd

Requires: pam >= 0:%{pam_version}
Requires: /sbin/nologin
Requires: system-logos
Requires: xorg-x11-server-utils
Requires: setxkbmap
Requires: xorg-x11-xinit
Requires: systemd >= 186
Requires: accountsservice
Requires: gnome-settings-daemon >= 2.21.92
Requires: gnome-icon-theme-symbolic
Requires: iso-codes
Requires: gnome-session
Requires: gnome-shell
# since we use it, and pam spams the log if the module is missing
Requires: gnome-keyring-pam
Requires: pulseaudio-gdm-hooks
# We need 1.0.4-5 since it lets us use "localhost" in auth cookies
Requires: libXau >= 1.0.4-4
BuildRequires: pkgconfig(libcanberra-gtk)
BuildRequires: pango-devel >= 0:%{pango_version}
BuildRequires: gtk3-devel >= 0:%{gtk3_version}
BuildRequires: pam-devel >= 0:%{pam_version}
BuildRequires: fontconfig >= 0:%{fontconfig_version}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: libtool automake autoconf
BuildRequires: libattr-devel
BuildRequires: gettext
BuildRequires: libdmx-devel
BuildRequires: gobject-introspection-devel
BuildRequires: autoconf automake libtool
BuildRequires: intltool
%ifnarch s390 s390x ppc ppc64
BuildRequires: xorg-x11-server-Xorg
%endif
BuildRequires: nss-devel >= %{nss_version}
BuildRequires: check-devel
BuildRequires: iso-codes-devel
BuildRequires: libxklavier-devel >= 4.0
BuildRequires: upower-devel >= 0.9.7
BuildRequires: libXdmcp-devel
BuildRequires: dbus-glib-devel
BuildRequires: GConf2-devel
BuildRequires: pkgconfig(accountsservice) >= 0.6.3
BuildRequires: pkgconfig(libsystemd-login)
BuildRequires: pkgconfig(libsystemd-daemon)
BuildRequires: pkgconfig(ply-boot-client)
BuildRequires: systemd

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

# these are all just for rewriting gdm.d/00-upstream-settings
Requires(posttrans): dconf

Provides: service(graphical-login) = %{name}


# Swallow up old fingerprint/smartcard plugins
Obsoletes: gdm-plugin-smartcard < 1:3.2.1
Provides: gdm-plugin-smartcard = %{epoch}:%{version}-%{release}

Obsoletes: gdm-plugin-fingerprint < 1:3.2.1
Provides: gdm-plugin-fingerprint = %{epoch}:%{version}-%{release}

%package devel
Summary: Development files for gdm-libs
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description devel
The gdm-devel package contains headers and other
files needed to build custom greeters.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%description
GDM provides the graphical login screen, shown shortly after boot up,
log out, and when user-switching.

%description -l zh_CN.UTF-8
GNOME 的登录管理器。

%prep
%setup -q

autoreconf -i -f
intltoolize -f

%build

%configure --with-pam-prefix=%{_sysconfdir} \
           --with-run-dir=/run/gdm \
           --with-default-path=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin \
	   --enable-split-authentication \
           --enable-profiling      \
           --enable-console-helper \
           --with-plymouth \
	   --with-default-pam-config=redhat \
           --without-selinux

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

make %{?_smp_mflags}


%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gdm/Init
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gdm/PreSession
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gdm/PostSession

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/gdm

# add logo to shell greeter
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas

# docs go elsewhere
rm -rf $RPM_BUILD_ROOT/%{_prefix}/doc

# create log dir
mkdir -p $RPM_BUILD_ROOT/var/log/gdm

(cd $RPM_BUILD_ROOT%{_sysconfdir}/gdm; ln -sf ../X11/xinit/Xsession .)

rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gdm/autostart/LoginWindow

mkdir -p $RPM_BUILD_ROOT/run/gdm

find $RPM_BUILD_ROOT -name '*.a' -delete
find $RPM_BUILD_ROOT -name '*.la' -delete

magic_rpm_clean.sh
%find_lang gdm --with-gnome

%pre
/usr/sbin/useradd -M -u 42 -d /var/lib/gdm -s /sbin/nologin -r gdm > /dev/null 2>&1
/usr/sbin/usermod -d /var/lib/gdm -s /sbin/nologin gdm >/dev/null 2>&1
# ignore errors, as we can't disambiguate between gdm already existed
# and couldn't create account with the current adduser.
exit 0

%post
/sbin/ldconfig
touch --no-create /usr/share/icons/hicolor >&/dev/null || :

# if the user already has a config file, then migrate it to the new
# location; rpm will ensure that old file will be renamed

custom=/etc/gdm/custom.conf

if [ $1 -ge 2 ] ; then
    if [ -f /usr/share/gdm/config/gdm.conf-custom ]; then
        oldconffile=/usr/share/gdm/config/gdm.conf-custom
    elif [ -f /etc/X11/gdm/gdm.conf ]; then
        oldconffile=/etc/X11/gdm/gdm.conf
    fi

    # Comment out some entries from the custom config file that may
    # have changed locations in the update.  Also move various
    # elements to their new locations.

    [ -n "$oldconffile" ] && sed \
    -e 's@^command=/usr/X11R6/bin/X@#command=/usr/bin/Xorg@' \
    -e 's@^Xnest=/usr/X11R6/bin/Xnest@#Xnest=/usr/X11R6/bin/Xnest@' \
    -e 's@^BaseXsession=/etc/X11/xdm/Xsession@#BaseXsession=/etc/X11/xinit/Xsession@' \
    -e 's@^BaseXsession=/etc/X11/gdm/Xsession@#&@' \
    -e 's@^BaseXsession=/etc/gdm/Xsession@#&@' \
    -e 's@^Greeter=/usr/bin/gdmgreeter@#Greeter=/usr/libexec/gdmgreeter@' \
    -e 's@^RemoteGreeter=/usr/bin/gdmlogin@#RemoteGreeter=/usr/libexec/gdmlogin@' \
    -e 's@^GraphicalTheme=Bluecurve@#&@' \
    -e 's@^BackgroundColor=#20305a@#&@' \
    -e 's@^DefaultPath=/usr/local/bin:/usr/bin:/bin:/usr/X11R6/bin@#&@' \
    -e 's@^RootPath=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/X11R6/bin@#&@' \
    -e 's@^HostImageDir=/usr/share/hosts/@#HostImageDir=/usr/share/pixmaps/faces/@' \
    -e 's@^LogDir=/var/log/gdm@#&@' \
    -e 's@^PostLoginScriptDir=/etc/X11/gdm/PostLogin@#&@' \
    -e 's@^PreLoginScriptDir=/etc/X11/gdm/PreLogin@#&@' \
    -e 's@^PreSessionScriptDir=/etc/X11/gdm/PreSession@#&@' \
    -e 's@^PostSessionScriptDir=/etc/X11/gdm/PostSession@#&@' \
    -e 's@^DisplayInitDir=/var/run/gdm.pid@#&@' \
    -e 's@^RebootCommand=/sbin/reboot;/sbin/shutdown -r now;/usr/sbin/shutdown -r now;/usr/bin/reboot@#&@' \
    -e 's@^HaltCommand=/sbin/poweroff;/sbin/shutdown -h now;/usr/sbin/shutdown -h now;/usr/bin/poweroff@#&@' \
    -e 's@^ServAuthDir=/var/gdm@#&@' \
    -e 's@^Greeter=/usr/bin/gdmlogin@Greeter=/usr/libexec/gdmlogin@' \
    -e 's@^RemoteGreeter=/usr/bin/gdmgreeter@RemoteGreeter=/usr/libexec/gdmgreeter@' \
    $oldconffile > $custom
fi

if [ $1 -ge 2 -a -f $custom ] && grep -q /etc/X11/gdm $custom ; then
   sed -i -e 's@/etc/X11/gdm@/etc/gdm@g' $custom
fi

%systemd_post gdm.service

%preun
%gconf_schema_remove gdm-simple-greeter
%systemd_preun gdm.service

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
%systemd_postun

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f gdm.lang
%doc AUTHORS COPYING NEWS README

%dir %{_sysconfdir}/gdm
%config(noreplace) %{_sysconfdir}/gdm/custom.conf
%config %{_sysconfdir}/gdm/Init/*
%config %{_sysconfdir}/gdm/PostLogin/*
%config %{_sysconfdir}/gdm/PreSession/*
%config %{_sysconfdir}/gdm/PostSession/*
%config %{_sysconfdir}/pam.d/gdm-autologin
%config %{_sysconfdir}/pam.d/gdm-password
# not config files
%{_sysconfdir}/gdm/Xsession
%{_datadir}/gdm/gdm.schemas
%{_sysconfdir}/dbus-1/system.d/gdm.conf
%dir %{_sysconfdir}/gdm/Init
%dir %{_sysconfdir}/gdm/PreSession
%dir %{_sysconfdir}/gdm/PostSession
%dir %{_sysconfdir}/gdm/PostLogin
%{_datadir}/pixmaps/*.png
%{_datadir}/glib-2.0/schemas/org.gnome.login-screen.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.login-screen.gschema.override
%{_libexecdir}/gdm-host-chooser
%{_libexecdir}/gdm-session-worker
%{_libexecdir}/gdm-simple-chooser
%{_libexecdir}/gdm-wayland-session
%{_libexecdir}/gdm-x-session
%{_sbindir}/gdm
%{_bindir}/gdmflexiserver
%{_bindir}/gdm-screenshot
%{_datadir}/dconf/profile/gdm
%{_datadir}/gdm/greeter/applications/*
%{_datadir}/gdm/greeter/autostart/*
%{_datadir}/gdm/greeter-dconf-defaults
%{_datadir}/gdm/locale.alias
%{_datadir}/gdm/gdb-cmd
%{_libdir}/girepository-1.0/Gdm-1.0.typelib
%{_libdir}/libgdm*.so*
%dir %{_localstatedir}/log/gdm
%attr(1770, gdm, gdm) %dir %{_localstatedir}/lib/gdm
%attr(0711, root, gdm) %dir /run/gdm
%attr(1755, root, gdm) %dir %{_localstatedir}/cache/gdm
%{_datadir}/icons/hicolor/*/*/*.png
%config %{_sysconfdir}/pam.d/gdm-pin
%config %{_sysconfdir}/pam.d/gdm-smartcard
%config %{_sysconfdir}/pam.d/gdm-fingerprint
%{_sysconfdir}/pam.d/gdm-launch-environment
%{_unitdir}/gdm.service

%files devel
%dir %{_includedir}/gdm
%{_includedir}/gdm/*.h
%{_datadir}/gir-1.0/Gdm-1.0.gir
%{_libdir}/pkgconfig/gdm.pc


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1:3.18.0-3
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1:3.18.0-2
- 更新到 3.18.0

* Sat Apr 05 2014 Liu Di <liudidi@gmail.com> - 1:3.12.0-1
- 更新到 3.12.0


