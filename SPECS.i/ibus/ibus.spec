%global with_preload_xkb_engine 1
%global with_pygobject2 1
%global with_pygobject3 1

%global with_pkg_config %(pkg-config --version >/dev/null 2>&1 && echo -n "1" || echo -n "0")

%if (0%{?fedora} > 19 || 0%{?rhel} > 7)
%global with_wayland 1
%else
%global with_wayland 0
%endif

%if (0%{?fedora} > 20 || 0%{?rhel} > 7)
%global with_python2_override_pkg 1
%else
%global with_python2_override_pkg 0
%endif

%global ibus_api_version 1.0
%global ibus_xkb_version 1.5.0.20140114

# for bytecompile in %%{_datadir}/ibus/setup
%global __python %{__python3}

%if %with_pkg_config
%{!?gtk2_binary_version: %global gtk2_binary_version %(pkg-config  --variable=gtk_binary_version gtk+-2.0)}
%{!?gtk3_binary_version: %global gtk3_binary_version %(pkg-config  --variable=gtk_binary_version gtk+-3.0)}
%global glib_ver %([ -a %{_libdir}/pkgconfig/glib-2.0.pc ] && pkg-config --modversion glib-2.0 | cut -d. -f 1,2 || echo -n "999")
%else
%{!?gtk2_binary_version: %global gtk2_binary_version ?.?.?}
%{!?gtk3_binary_version: %global gtk3_binary_version ?.?.?}
%global glib_ver 0
%endif

%global dbus_python_version 0.83.0

Name:           ibus
Version:        1.5.6
Release:        4%{?dist}
Summary:        Intelligent Input Bus for Linux OS
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://code.google.com/p/ibus/
Source0:        https://github.com/ibus/ibus/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-xinput
Source2:        %{name}.conf.5
# Actual path is https://github.com/.../%%{ibus_xkb_version}.tar.gz
# Renamed %%{ibus_xkb_version}.tar.gz to ibus-xkb-%%{ibus_xkb_version}.tar.gz
Source3:        https://github.com/ibus/ibus-xkb/archive/ibus-xkb-%{ibus_xkb_version}.tar.gz
# Upstreamed patches.
# Patch0:         %%{name}-HEAD.patch
Patch0:         %{name}-HEAD.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=810211
Patch1:         %{name}-810211-no-switch-by-no-trigger.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=541492
Patch2:         %{name}-541492-xkb.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=530711
Patch3:         %{name}-530711-preload-sys.patch
# Hide minor input method engines on ibus-setup by locale
Patch4:         %{name}-xx-setup-frequent-lang.patch

# Removed the target.
# Even if fedpkg srpm's target is rhel, it can run on fedora box.
# Disable IME on gnome-shell password for the back compatiblity.
Patch96:        %{name}-xx-f19-password.patch


BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  dbus-python-devel >= %{dbus_python_version}
BuildRequires:  desktop-file-utils
BuildRequires:  gtk-doc
BuildRequires:  dconf-devel
BuildRequires:  dbus-x11
BuildRequires:  python3-devel
BuildRequires:  python3-gobject
BuildRequires:  python2-devel
BuildRequires:  vala
BuildRequires:  vala-devel
BuildRequires:  vala-tools
# for AM_GCONF_SOURCE_2 in configure.ac
BuildRequires:  GConf2-devel
BuildRequires:  intltool
BuildRequires:  iso-codes-devel
BuildRequires:  libnotify-devel
%if %with_wayland
BuildRequires:  libwayland-client-devel
%endif

Requires:       %{name}-libs%{?_isa}   = %{version}-%{release}
Requires:       %{name}-gtk2%{?_isa}   = %{version}-%{release}
Requires:       %{name}-gtk3%{?_isa}   = %{version}-%{release}
Requires:       %{name}-setup          = %{version}-%{release}
%if %with_wayland
Requires:       %{name}-wayland%{?_isa} = %{version}-%{release}
%endif

Requires:       iso-codes
Requires:       dbus-python >= %{dbus_python_version}
Requires:       dbus-x11
Requires:       dconf
Requires:       librsvg2
%if ! %with_python2_override_pkg
# Owner of %%python2_sitearch/gi/overrides
Requires:       pygobject3-base
%endif
# Owner of %%python3_sitearch/gi/overrides
Requires:       python3-gobject
# Owner of %%{_sysconfdir}/X11/xinit
Requires:       xorg-x11-xinit
# for setxkbmap
Requires:       xorg-x11-xkb-utils
# The feature in ibus-gnome3 is provided by gnome-shell.
Obsoletes:      ibus-gnome3 < %{version}-%{release}

Requires(post):  desktop-file-utils
Requires(postun):  desktop-file-utils
Requires(postun):  dconf
Requires(posttrans): dconf

Requires(post):  %{_sbindir}/alternatives
Requires(postun):  %{_sbindir}/alternatives

%global _xinputconf %{_sysconfdir}/X11/xinit/xinput.d/ibus.conf

%description
IBus means Intelligent Input Bus. It is an input framework for Linux OS.

%package libs
Summary:        IBus libraries
Group:          System Environment/Libraries

Requires:       dbus >= 1.2.4
Requires:       glib2 >= %{glib_ver}
# Owner of %%{_libdir}/girepository-1.0
Requires:       gobject-introspection

%description libs
This package contains the libraries for IBus

%package gtk2
Summary:        IBus im module for gtk2
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa}        = %{version}-%{release}
Requires:       %{name}-libs%{?_isa}   = %{version}-%{release}
Requires(post): glib2 >= %{glib_ver}
# Added for upgrade el6 to el7
Provides:       ibus-gtk = %{version}-%{release}
Obsoletes:      ibus-gtk < %{version}-%{release}

%description gtk2
This package contains ibus im module for gtk2

%package gtk3
Summary:        IBus im module for gtk3
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa}        = %{version}-%{release}
Requires:       %{name}-libs%{?_isa}   = %{version}-%{release}
Requires(post): glib2 >= %{glib_ver}

%description gtk3
This package contains ibus im module for gtk3

%if %with_pygobject3
%package setup
Summary:        IBus setup utility
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       python3-gobject
BuildRequires:  gobject-introspection-devel
BuildRequires:  pygobject3-devel
BuildArch:      noarch

%description setup
This is a setup utility for IBus.
%endif

%if %with_pygobject2
%package pygtk2
Summary:        IBus pygtk2 library
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pygtk2
BuildArch:      noarch

%description pygtk2
This is a pygtk2 library for IBus. Now major IBus engines use pygobject3
and this package will be deprecated.
%endif

%if %with_python2_override_pkg
%package py2override
Summary:        IBus python2 override library
Group:          System Environment/Libraries
Requires:       %{name}-libs%{?_isa}   = %{version}-%{release}
# Owner of %%python2_sitearch/gi/overrides
Requires:       pygobject3-base

%description py2override
This is a python2 override library for IBus. The python files override
some functions in gobject-introspection.
%endif

%if %with_wayland
%package wayland
Summary:        IBus im module for Wayland
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa}        = %{version}-%{release}
Requires:       %{name}-libs%{?_isa}   = %{version}-%{release}

%description wayland
This package contains IBus im module for Wayland
%endif

%package devel
Summary:        Development tools for ibus
Group:          Development/Libraries
Requires:       %{name}%{?_isa}        = %{version}-%{release}
Requires:       %{name}-libs%{?_isa}   = %{version}-%{release}
Requires:       dbus-devel
Requires:       glib2-devel
# Owner of %%{_datadir}/gir-1.0
Requires:       gobject-introspection-devel
# Owner of %%{_datadir}/vala/vapi
Requires:       vala

%description devel
The ibus-devel package contains the header files and developer
docs for ibus.

%package devel-docs
Summary:        Developer documents for ibus
Group:          Development/Libraries
%if (0%{?fedora} >= 19 || 0%{?rhel} >= 7)
Requires:       %{name}                = %{version}-%{release}
BuildArch:      noarch
%else
Requires:       %{name}%{?_isa}        = %{version}-%{release}
%endif
# Owner of %%{_datadir}/gtk-doc/html
Requires:       gtk-doc

%description devel-docs
The ibus-devel-docs package contains developer documentation for ibus


%prep
%setup -q
# %%patch0 -p1
%patch0 -p1
%if (0%{?fedora} < 20 && 0%{?rhel} < 8)
%patch96 -p1 -b .passwd
%endif
cp client/gtk2/ibusimcontext.c client/gtk3/ibusimcontext.c ||

%patch1 -p1 -b .noswitch
%if %with_preload_xkb_engine
%patch2 -p1 -b .preload-xkb
rm -f bindings/vala/ibus-1.0.vapi
rm -f data/dconf/00-upstream-settings
%endif
%patch3 -p1 -b .preload-sys
%patch4 -p1 -b .setup-frequent-lang

zcat %SOURCE3 | tar xf -
POS=`(cd ibus-xkb-%ibus_xkb_version/po; ls *.po)`
for PO in $POS
do
  cp po/$PO po/$PO.orig
  msgcat --use-first po/$PO ibus-xkb-%ibus_xkb_version/po/$PO -o po/$PO
done

%build
%if %with_preload_xkb_engine
autoreconf -f -i -v
%endif
%configure \
    --disable-static \
    --enable-gtk2 \
    --enable-gtk3 \
    --enable-xim \
    --enable-gtk-doc \
    --with-no-snooper-apps='gnome-do,Do.*,firefox.*,.*chrome.*,.*chromium.*' \
    --enable-surrounding-text \
    --with-python=python3 \
%if %with_pygobject2
    --enable-python-library \
%endif
%if %with_wayland
    --enable-wayland \
%endif
    --enable-introspection

%if %with_preload_xkb_engine
make -C ui/gtk3 maintainer-clean-generic
%endif
# make -C po update-gmo
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
rm -f $RPM_BUILD_ROOT%{_libdir}/libibus-%{ibus_api_version}.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/%{gtk2_binary_version}/immodules/im-ibus.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/%{gtk3_binary_version}/immodules/im-ibus.la

# install man page
for S in %{SOURCE2}
do
  cp $S .
  MP=`basename $S` 
  gzip $MP
  install -pm 644 -D ${MP}.gz $RPM_BUILD_ROOT%{_datadir}/man/man5/${MP}.gz
done

# install xinput config file
install -pm 644 -D %{SOURCE1} $RPM_BUILD_ROOT%{_xinputconf}

# install .desktop files
echo "NoDisplay=true" >> $RPM_BUILD_ROOT%{_datadir}/applications/ibus-setup.desktop
#echo "X-GNOME-Autostart-enabled=false" >> $RPM_BUILD_ROOT%%{_sysconfdir}/xdg/autostart/ibus.desktop

desktop-file-install --delete-original          \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  $RPM_BUILD_ROOT%{_datadir}/applications/*

# FIXME: no version number
%find_lang %{name}10

%post
# recreate icon cache
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%{_sbindir}/alternatives --install %{_sysconfdir}/X11/xinit/xinputrc xinputrc %{_xinputconf} 83 || :

%postun
if [ "$1" -eq 0 ]; then
  # recreate icon cache
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

  %{_sbindir}/alternatives --remove xinputrc %{_xinputconf} || :
  # if alternative was set to manual, reset to auto
  [ -L %{_sysconfdir}/alternatives/xinputrc -a "`readlink %{_sysconfdir}/alternatives/xinputrc`" = "%{_xinputconf}" ] && %{_sbindir}/alternatives --auto xinputrc || :

  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
  # 'dconf update' sometimes does not update the db...
  dconf update || :
  [ -f %{_sysconfdir}/dconf/db/ibus ] && \
      rm %{_sysconfdir}/dconf/db/ibus || :
  # 'ibus write-cache --system' updates the system cache.
  [ -f /var/cache/ibus/bus/registry ] && \
      rm /var/cache/ibus/bus/registry || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
dconf update || :
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post gtk2
if [ $1 -eq 1 ] ; then
    # For upgrades, the cache will be regenerated by the new package's %%postun
    %{_bindir}/update-gtk-immodules %{_host} || :
fi

%postun gtk2
%{_bindir}/update-gtk-immodules %{_host} || :

%post gtk3
if [ $1 -eq 1 ] ; then
    # For upgrades, the cache will be regenerated by the new package's %%postun
    /usr/bin/gtk-query-immodules-3.0-%{__isa_bits} --update-cache &> /dev/null || :
fi

%postun gtk3
/usr/bin/gtk-query-immodules-3.0-%{__isa_bits} --update-cache &> /dev/null || :


# FIXME: no version number
%files -f %{name}10.lang
%doc AUTHORS COPYING README
%dir %{_datadir}/ibus/
%{_bindir}/ibus
%{_bindir}/ibus-daemon
%{_datadir}/bash-completion/completions/ibus.bash
%{_datadir}/GConf/gsettings/*
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/ibus/component
%{_datadir}/ibus/engine
%{_datadir}/ibus/keymaps
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/man/man1/ibus.1.gz
%{_datadir}/man/man1/ibus-daemon.1.gz
%{_datadir}/man/man5/ibus.conf.5.gz
%{_libexecdir}/ibus-engine-simple
%{_libexecdir}/ibus-dconf
%{_libexecdir}/ibus-ui-gtk3
%{_libexecdir}/ibus-x11
%{_sysconfdir}/dconf/db/ibus.d
%{_sysconfdir}/dconf/profile/ibus
%python3_sitearch/gi/overrides/__pycache__/*.py*
%python3_sitearch/gi/overrides/IBus.py
%if ! %with_python2_override_pkg
%python2_sitearch/gi/overrides/IBus.py*
%endif
# ibus owns xinput.d because gnome does not like to depend on imsettings.
%dir %{_sysconfdir}/X11/xinit/xinput.d
# Do not use %%config(noreplace) to always get the new keywords in _xinputconf
# For user customization, $HOME/.xinputrc can be used instead.
%config %{_xinputconf}

%files libs
%{_libdir}/libibus-%{ibus_api_version}.so.*
%{_libdir}/girepository-1.0/IBus-1.0.typelib

%files gtk2
%{_libdir}/gtk-2.0/%{gtk2_binary_version}/immodules/im-ibus.so

%files gtk3
%{_libdir}/gtk-3.0/%{gtk3_binary_version}/immodules/im-ibus.so

%if %with_pygobject3
%files setup
%{_bindir}/ibus-setup
%{_datadir}/applications/ibus-setup.desktop
%{_datadir}/ibus/setup
%{_datadir}/man/man1/ibus-setup.1.gz
%endif

%if %with_pygobject2
%files pygtk2
%dir %{python2_sitelib}/ibus
%{python2_sitelib}/ibus/*
%endif

%if %with_python2_override_pkg
%files py2override
%python2_sitearch/gi/overrides/IBus.py*
%endif

%if %with_wayland
%files wayland
%{_libexecdir}/ibus-wayland
%endif

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/gir-1.0/IBus-1.0.gir
%{_datadir}/vala/vapi/ibus-1.0.vapi
%{_datadir}/vala/vapi/ibus-1.0.deps

%files devel-docs
%{_datadir}/gtk-doc/html/*

%changelog
* Tue Jun 24 2014 Liu Di <liudidi@gmail.com> - 1.5.6-4
- 为 Magic 3.0 重建

* Thu Apr 17 2014 Liu Di <liudidi@gmail.com> - 1.5.6-3
- 为 Magic 3.0 重建

* Fri Mar 28 2014 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.6-2
- Updated ibus-HEAD.patch for Czech (qwerty) keymap.

* Thu Mar 06 2014 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.6-1
- Bumped to 1.5.6
- Deleted ibus-xx-ctrl-space.patch

* Fri Jan 31 2014 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.5-2
- Enabled python3 ibus-setup

* Tue Jan 14 2014 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.5-1
- Bumped to 1.5.5
- Deleted notify-python in Requires

* Fri Oct 04 2013 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.4-2
- Added ibus-HEAD.patch to sync upstream.

* Fri Sep 20 2013 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.4-1
- Bumped to 1.5.4
- Added ibus.conf.5
- Added ibus-xkb-1.5.0.tar.gz for po files.
- Added ibus-xx-f19-password.patch for back compatibility.
- Added ibus-wayland in f20 or later.

* Fri Jul 26 2013 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.3-1
- Bumped to 1.5.3
- Deleted ibus-xx-g-s-disable-preedit.patch as EOL.
- Deleted ibus-gjs as EOL.
- Removed imsettings-gnome, im-chooser, libgnomekbd dependencies.

* Thu Jul 11 2013 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.2-8
- Updated ibus-HEAD.patch to delete pyxdg dependencies.

* Mon Jun 17 2013 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.2-7
- Bug 972328 - Deleted ibus-panel

* Mon Jun 17 2013 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.2-6
- Bug 972328 - Bring back the dependency of ibus-setup.

* Tue Jun 11 2013 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.2-5
- Removed dependencies of ibus-setup and ibus-pygtk2

* Wed Jun 05 2013 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.2-4
- Updated ibus-HEAD.patch for upstream.
- Added ibus-xx-1.5.2.patch until 1.5.3 will be released.
- Added ibus-xx-ctrl-space.patch for back compatible triggers.

* Wed May 01 2013 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.2-3
- Updated ibus-HEAD.patch for upstream.
- Deleted ibus-947318-reconnect-gtk-client.patch

* Sun Apr 21 2013 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.2-2
- Separate python files in f19 or later.

* Thu Apr 18 2013 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.2-1
- Bumped to 1.5.2
- Created noarch packages for python files due to .pyc and .pyo.
- Added man pages.

* Mon Feb 18 2013 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.1-3
- Copied gtk2 module to gtk3 one.

* Thu Jan 31 2013 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.1-2
- Updated ibus-530711-preload-sys.patch. Fixes #904799

* Tue Jan 08 2013 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.1-1
- Bumped to 1.5.1
- Bumped to ibus-gjs 3.4.1.20130115 for f17
- Removed ibus-xx-no-use.diff

* Fri Dec 14 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20121109-9
- Updated ibus-xx-no-use.diff not to use variant.dup_strv()

* Fri Dec 07 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20121109-8
- Resolves #869584 - Removed libgnomekbd dependency in f18.

* Fri Nov 30 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20121109-7
- Set time stamp of ibus/_config.py

* Fri Nov 30 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20121109-6
- Set time stamp of ibus/_config.py

* Fri Nov 30 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20121109-5
- Updated spec file to work witout pkgconfig.

* Tue Nov 27 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20121109-4
- Added comment lines for patches.

* Tue Nov 27 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20121109-3
- Fixed misc issues.

* Thu Oct 11 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20121109-2
- Obsoleted ibus-gnome3

* Thu Oct 11 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20121109-1
- Bumped to 1.4.99.20121109
- Removed im-chooser, imsettings-gnome, gnome-icon-theme-symbolic
  dependencies in f18 because ibus gnome integration is done.
  Use ibus-keyboard instead of input-keyboard-symbolic.
- Disabled ibus-gjs build because of ibus gnome integration.

* Thu Oct 11 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20121006-2
- Updated ibus-HEAD.patch to fix typo in data/dconf/profile/ibus

* Thu Oct 11 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20121006-2
- Updated ibus-HEAD.patch to fix typo in data/dconf/profile/ibus

* Sat Oct 06 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20121006-1
- Bumped to 1.4.99.20121006
- Removed ibus-xx-segv-reg-prop.patch

* Fri Sep 14 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120914-2
- Added ibus-xx-segv-reg-prop.patch to avoid segv

* Fri Sep 14 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120914-1
- Bumped to 1.4.99.20120914

* Thu Sep 06 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120822-2
- Updated ibus-530711-preload-sys.patch
- Updated ibus-541492-xkb.patch
- Updated ibus-xx-no-use.diff
  Fixed Bug 854161 - not able to add keymap with ibus-setup

* Wed Aug 22 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120822-1
- Bumped to 1.4.99.20120822
- Bumped to ibus-gjs 3.4.1.20120815
  Fixed Bug 845956 - ibus backward trigger key is not customized
  Fixed Bug 844580 - ibus-dconf does not load the system gvdb
- Separated ibus-810211-no-switch-by-no-trigger.patch from ibus-HEAD.patch

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.99.20120712-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 19 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120712-2
- Updated ibus-HEAD.patch
  Support dconf 0.13.4

* Tue Jul 17 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120712-1
- Bumped to 1.4.99.20120712
- Removed ibus-xx-branding-switcher-ui.patch as upstreamed.

* Fri Jun  8 2012 Matthias Clasen <mclasen@redhat.com> - 1.4.99.20120428-3
- Rebuild against new libgnomekbd

* Fri Apr 27 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120428-2
- Updated ibus-HEAD.patch
- Updated ibus-541492-xkb.patch
- Updated ibus-xx-branding-switcher-ui.patch
  Fixed Bug 810211 - Cancel Control + space pressing Control key.
- Updated ibus-xx-no-use.diff
  Enabled to customize trigger keys with non-modifier trigger keys.

* Fri Apr 27 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120428-1
- Bumped to 1.4.99.20120428
  Fixed Bug 799571 - no IME list at the session login.
  Fixed Bug 810415 - ibus does not handle Ctrl+space with BUTTON_PRESS.
- Bumped to ibus-gjs 3.4.1.20120428
  Fixed Bug 802052 - no modifiers trigger keys.
  Fixed Bug 803244 - IME switch Ctrl+space not working on shell text entry.

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 1.4.99.20120317-4
- Update the dconf and icon cache rpm scriptlets

* Wed Apr 18 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120317-3
- Added a RHEL flag.

* Tue Mar 27 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120317-2
- Bumped to ibus-gjs 3.3.92.20120327
  
* Sat Mar 17 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120317-1
- Bumped to 1.4.99.20120317
  Fixed Bug 718668 - focus move is slow with ibus-gnome3
  Fixed Bug 749497 - Enhance IME descriptions in status icon active menu
- Bumped to ibus-gjs 3.3.90.20120317
- Added ibus-xx-no-use.diff
  Fixed Bug 803260 - Disable non-global input method mode
- Updated ibus-HEAD.patch
  Fixed Bug 803250 - ibus lookup window font customization
  Fixed Bug 803177 - language id on ibus-ui-gtk3 switcher
- Update ibus-530711-preload-sys.patch
  Fixed Bug 797023 - port preload engines

* Thu Mar 08 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120303-3
- Bumped to ibus-gjs 3.3.90.20120308 to work with gnome-shell 3.3.90
- Fixed Bug 786906 - Added ifnarch ppc ppc64 s390 s390x
- Updated ibus-HEAD.patch
  Fixed Bug 800897 - After doing "ctrl+space", ibus tray icon freezes

* Mon Mar 05 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120303-2
- Added ibus-HEAD.patch to fix python library to load libibus.so.

* Sun Mar 04 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120303-1
- Bumped to 1.4.99.20120303
  Fixed Bug 796070 - ibus-setup without no ibus-daemon

* Wed Feb 08 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120203-3
- Fixed ibus-setup on C locale
- Fixed to show no registered engines from g-c-c.
- Enabled Alt_R keybinding on ko locales for ibus gtk only.

* Fri Feb 03 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.99.20120203-1
- Updated to 1.4.99.20120203
- Removed ibus-xx-bridge-hotkey.patch
- Updated ibus-541492-xkb.patch to use libgnomekbd.
- Updated ibus-xx-setup-frequent-lang.patch for 1.4.99.20120203

* Wed Jan 04 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.0-17
- Added ibus-771115-property-compatible.patch for f16
  Fixed Bug 771115 - IBusProperty back compatibility.

* Fri Dec 30 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.0-16
- Enhanced ibus-gnome3 shell lookup window.
- Updated ibus-HEAD.patch from upstream
  Fixed Bug 769135 - ibus-x11 SEGV in _process_key_event_done.
- Updated ibus-541492-xkb.patch
  Fixed Bug 757889 - ibus-setup SEGV without active engine.
  Fixed Bug 760213 - ibus-setup saves XKB variants correctly.
  Fixed Bug 769133 - ibus-engine-xkb returns FALSE for ASCII typings.
- Updated ibus-xx-bridge-hotkey.patch for an enhancement.

* Wed Nov 30 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.0-14
- Enabled dconf.
- Updated ibus-HEAD.patch
  Fixed Bug 618229 - engine setup buton on ibus-setup.
- Removed ibus-711632-fedora-fallback-icon.patch as upstreamed.
- Updated ibus-xx-bridge-hotkey.patch
  Removed Enable/Disable buttons on ibus-setup

* Fri Nov 18 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.0-11
- Updated ibus-541492-xkb.patch
  Fixed Bug 750484 - support reloading Xmodmap
- Updated ibus-HEAD.patch
  Fixed Bug 753781 - ibus-x11 needs async for hangul ibus_commit_text.

* Fri Nov 04 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.0-10
- Updated ibus-xx-bridge-hotkey.patch for f16
  Fixed no XKB languages from layout only. e.g. in(eng).
- Updated ibus-541492-xkb.patch
  Fixed not to show 'eng' on GUI for in(eng).

* Wed Nov 02 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.0-9
- Updated ibus-HEAD.patch
  Fixed prev/next keys without global engine.
- Updated ibus-xx-bridge-hotkey.patch for f16
  Fixed Bug 747902 - mouse and ctrl+space not working
  Fixed Bug 749770 - IME hotkey after Control + Space
- Updated ibus-711632-fedora-fallback-icon.patch
  Fixed Bug 717831 - use old icon for desktops other than gnome

* Fri Oct 28 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.0-8
- Updated ibus-xx-bridge-hotkey.patch for f16
- Fixed Bug 747902 - mouse and ctrl+space not working

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-6
- Rebuilt for glibc bug#747377

* Fri Oct 21 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.0-5
- Fixed Bug 747845 - ibus icon cannot open menu item on gnome-shell

* Thu Oct 20 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.0-4
- Fixed Bug 746869 - no keymaps if the XKB has no group and no variant

* Fri Sep 30 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.0-3
- Rebuilt for f16 gnome-shell 3.2 and gjs 1.30

* Wed Sep 28 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.0-2
- Updated to 1.4.0
- Updated ibus-gjs 3.0.2.20110928 for f15.
- Updated ibus-gjs 3.2.0.20110928 for f16. (#740588)
- Updated ibus-530711-preload-sys.patch
  Fixed not to show duplicated engine names in setup treeview (#740447)
- Updated bus-gjs-xx-gnome-shell-3.1.4-build-failure.patch for f16.
- Updated ibus-xx-bridge-hotkey.patch
  Fixed a XKB configuration without the input focus for f16 (#739165)
  Fixed not to show null strings in case of no variants (#738130)

* Tue Sep 13 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.99.20110817-5
- Updated ibus-gjs 3.1.91.20110913 for f16.

* Thu Sep 08 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.99.20110817-4
- Updated ibus-gjs 3.1.91.20110908 and 3.0.2.20110908 for gnome-shell.
  Fixed preedit active segments on gnome-shell and X11 apps.
- Added ibus-xx-g-s-disable-preedit.patch
  Disabled preedit on gnome-shell for a workaround.
- Updated ibus.spec
  Fixed Bug 735879 pre/postun scripts

* Thu Sep 01 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.99.20110817-3
- Fixed Bug 700472 Use a symbol icon instead of an image icon.
- Updated ibus-HEAD.patch for upstream.
- Removed ibus-435880-surrounding-text.patch as upstream.
- Added ibus-711632-fedora-fallback-icon.patch
  Fixed SEGV with no icon in oxygen-gtk icon theme.
- Added ibus-xx-bridge-hotkey.patch
  Triaged Bug 707370 SetEngine timeout
  Fixed Bug 731610 Keep IM state when text input focus changes
- Added transitional ibus-gnome3 package.
  Fixed Bug 718110 Use a shell icon instead of pygtk2 icon.

* Thu May 26 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.99.20110419-1
- Updated to 1.3.99.20110419
- Added ibus-HEAD.patch
  Fixed Bug 697471 - ibus-gconf zombie when restart ibus from ibus panel.
- Updated ibus-541492-xkb.patch
  Fixed Bug 701202 - us(dvorak) does not show up in list
  Updated ibus-1.0.pc for ibus-xkb
  Showed XKB variant descriptions only without layout descriptions.
- Updated ibus-xx-setup-frequent-lang.patch
  Updated UI strings

* Tue Apr 19 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.99.20110408-1
- Updated to 1.3.99.20110408
  Fixed Bug 683484 - Timed out SetEngine when select an engine from panel.
  Fixed Bug 657165 - IBus for gnome-shell for Fedora 15.
- Upstreamed ibus-657165-panel-libs.patch
- Removed ibus-675503-gnome-shell-workaround.patch
- Added ibus-xx-setup-frequent-lang.patch
- Updated ibus-541492-xkb.patch
  Fixed Bug 696481 - no the variant maps without language codes
- Added dependency of imsettings-gnome.
  Fixed Bug 696510 - need a dependency in ibus-gtk3 for imsettings-gnome

* Thu Mar 10 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.99.20110228-1
- Updated to 1.3.99.20110228
- Integrated the part of gjs in Bug 657165 ibus for gnome-shell.
  Added ibus-657165-panel-libs.patch
  Added gnome-shell-ibus-plugins-20110304.tar.bz2
- Fixed Bug 675503 - a regression in sync mode
  Added ibus-675503-gnome-shell-workaround.patch until gnome-shell is updated.
- Fixed Bug 677856 - left ibus snooper when im client is switched.
- Fixed Bug 673047 - abrt ibus_xkb_get_current_layout for non-XKB system
  Updated ibus-541492-xkb.patch

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.99.20110127-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.99.20110127-1
- Updated to 1.3.99.20110127
- Updated ibus-HEAD.patch from upstream.

* Wed Jan 26 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.99.20110117-1
- Updated to 1.3.99.20110117
- Fixed Bug 666427 - ibus requires dbus-x11
- Fixed Bug 670137 - QT_IM_MODULE=xim in ibus.conf without ibus-qt

* Thu Dec 09 2010 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.99.20101202-1
- Updated to 1.3.99.20101202
- Added ibus-530711-preload-sys.patch
  Fixed Bug 530711 - Reload preloaded engines by login

* Fri Oct 29 2010 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.99.20101028-1
- Updated to 1.3.99.20101028
- Integrated gdbus
- Merged notify.patch into ibus-HEAD.patch

* Fri Oct 22 2010 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.8-1
- Updated to 1.3.8
- Added ibus-541492-xkb.patch
  Fixes Bug 541492 - ibus needs to support some xkb layout switching
- Added ibus-435880-surrounding-text.patch
  Fixes Bug 435880 - ibus-gtk requires surrounding-text support
- Added ibus-xx-workaround-gtk3.patch
  Workaround for f14 http://koji.fedoraproject.org/koji/taskinfo?taskID=2516604

* Mon Aug 23 2010 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.7-1
- Updated to 1.3.7

* Wed Jul 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.6-5
- Rebuild against python 2.7

* Thu Jul 22 2010 Jens Petersen <petersen@redhat.com> - 1.3.6-4
- keep bumping ibus-gtk obsoletes to avoid upgrade problems

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 1.3.6-2
- Rebuild with new gobject-introspection

* Tue Jul 06 2010 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.6-1
- Update to 1.3.6

* Wed Jun 30 2010 Jens Petersen <petersen@redhat.com>
- version the ibus-gtk obsolete and provides
- drop the old redundant ibus-qt obsoletes

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> - 1.3.5-3
- Rebuild against newer gtk

* Tue Jun 22 2010 Colin Walters <walters@verbum.org> - 1.3.5-2
- Bump Release to keep ahead of F-13

* Sat Jun 12 2010 Peng Huang <phuang@redhat.com> - 1.3.5-1
- Update to 1.3.5
- Support gtk3, gobject-introspection and vala.

* Sat May 29 2010 Peng Huang <phuang@redhat.com> - 1.3.4-2
- Update to 1.3.4

* Sat May 29 2010 Peng Huang <phuang@redhat.com> - 1.3.4-1
- Update to 1.3.4

* Tue May 04 2010 Peng Huang <phuang@redhat.com> - 1.3.3-1
- Update to 1.3.3

* Sun May 02 2010 Peng Huang <phuang@redhat.com> - 1.3.2-3
- Embedded language bar in menu by default.
- Fix bug 587353 - [abrt] crash in ibus-1.3.2-2.fc12

* Sat Apr 24 2010 Peng Huang <phuang@redhat.com> - 1.3.2-2
- Add requires librsvg2
- Update ibus-HEAD.patch: Update po files and and setting 

* Wed Apr 21 2010 Peng Huang <phuang@redhat.com> - 1.3.2-1
- Update to 1.3.2
- Fix bug 583446 - [abrt] crash in ibus-1.3.1-1.fc12

* Mon Apr 05 2010 Peng Huang <phuang@redhat.com> - 1.3.1-1
- Update to 1.3.1

* Fri Mar 26 2010 Peng Huang <phuang@redhat.com> - 1.3.0-3
- Update ibus-HEAD.patch
- Fix bug - some time panel does not show candidates.
- Update some po files

* Mon Mar 22 2010 Peng Huang <phuang@redhat.com> - 1.3.0-2
- Does not check glib micro version in ibus im module.

* Mon Mar 22 2010 Peng Huang <phuang@redhat.com> - 1.3.0-1
- Update to 1.3.0

* Tue Feb 02 2010 Peng Huang <phuang@redhat.com> - 1.2.99.20100202-1
- Update to 1.2.99.20100202

* Mon Jan 11 2010 Peng Huang <phuang@redhat.com> - 1.2.0.20100111-1
- Update to 1.2.0.20100111

* Fri Dec 25 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20091225-1
- Update to 1.2.0.20091225
- Fix bug 513895 - new IME does not show up in ibus-setup
- Fix bug 531857 - applet order should correspond with preferences order
- Fix bug 532856 - should not list already added input-methods in Add selector

* Tue Dec 15 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20091215-1
- Update to 1.2.0.20091215

* Thu Dec 10 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20091204-2
- Fix rpmlint warnings and errors.

* Fri Dec 04 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20091204-1
- Update to 1.2.0.20091204
- Fix Bug 529920 - language panel pops up on the wrong monitor
- Fix Bug 541197 - Ibus crash

* Tue Nov 24 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20091124-1
- Update to 1.2.0.20091124
- Update some translations.
- Fix bug 538147 - [abrt] crash detected in firefox-3.5.5-1.fc12 

* Sat Oct 24 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20091024-1
- Update to 1.2.0.20091024

* Wed Oct 14 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20091014-2
- Update to 1.2.0.20091014
- Change ICON in ibus.conf 

* Sun Sep 27 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090927-1
- Update to 1.2.0.20090927

* Tue Sep 15 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090915-1
- Update to 1.2.0.20090915
- Fix bug 521591 - check if the icon filename is a real file before trying to open it
- Fix bug 522310 - Memory leak on show/hide
- Fix bug 509518 - ibus-anthy should only override to jp layout for kana input

* Fri Sep 04 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090904-2
- Refresh the tarball.

* Fri Sep 04 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090904-1
- Update to 1.2.0.20090904

* Mon Aug 31 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090828-2
- Change icon path in ibus.conf

* Fri Aug 28 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090828-1
- Update to 1.2.0.20090828
- Change the icon on systray.
- Fix segment fault in ibus_hotkey_profile_destroy
- Fix some memory leaks.

* Wed Aug 12 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090812-1
- Update to 1.2.0.20090812

* Mon Aug 10 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090807-4
- Update ibus-HEAD.patch
- Fix Numlock problem.
- Fix some memory leaks.

* Fri Aug 07 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090807-2
- Update ibus-HEAD.patch
- Fix bug 516154.

* Fri Aug 07 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090807-1
- Update to 1.2.0.20090807

* Thu Aug 06 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090806-1
- Update to 1.2.0.20090806
- Fix bug 515106 - don't install duplicate files

* Tue Jul 28 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090723-3
- Update xinput-ibus: setup QT_IM_MODULE if the ibus qt input method plugin exists. 

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.20090723-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090723-1
- Update to 1.2.0.20090723
- Fix dead loop in ibus-gconf

* Wed Jul 22 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090722-1
- Update to 1.2.0.20090722

* Sun Jul 19 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090719-1
- Update to 1.2.0.20090719

* Mon Jun 22 2009 Peng Huang <phuang@redhat.com> - 1.2.0.20090617-1
- Update to 1.2.0.20090617

* Fri Jun 12 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090612-1
- Update to 1.1.0.20090612
- Fix bug 504942 - PageUp and PageDown do not work in candidate list
- Fix bug 491040 - Implememnt mouse selection in candidate list

* Wed Jun 10 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090609-1
- Update to Update to 1.1.0.20090609
- Fix bug 502414 - Implemented on-screen help facility
- Fix bug 502561 - iBus should show keymap name on iBus panel
- Fix bug 498043 - ibus Alt-grave trigger conflicts with openoffice.org
- Implemented API for setting labels for candidates in LookupTable

* Sun May 31 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090531-1
- Update to Update to 1.1.0.20090531

* Tue May 26 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090508-5
- Update ibus-HEAD.patch.
- Show the default input method with bold text
- Add information text below input methods list

* Mon May 25 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090508-4
- Update ibus-HEAD.patch.
- Fix bug 501211 - ibus-setup window should be raised if running or just stay on top/grab focus
- Fix bug 501640 - ibus should adds new IMEs at end of engine list not beginning
- Fix bug 501644 - [IBus] focus-out and disabled IME should hide language panel

* Thu May 14 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090508-2
- Remove requires notification-daemon
- Fix bug 500588 - Hardcoded requirement for notification-daemon

* Fri May 08 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090508-1
- Update to 1.1.0.20090508
- Fix bug 499533 - [Indic] ibus should allow input in KDE using all supported Indic locales
- Fix bug 498352 - hotkey config table should list keys in same order as on main setup page
- Fix bug 497707 - ibus French translation update

* Fri May 08 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090423-3
- Fix bug 498541 - ibus-libs should not contain devel file libibus.so

* Tue May 05 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090423-2
- Fix bug 498141 - new ibus install needs gtk immodules
- Separate ibus document from ibus-devel to ibus-devel-docs

* Thu Apr 23 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090423-1
- Update to ibus-1.1.0.20090423.
- Fix bug 497265 - [mai_IN] Maithili language name is not correct.
- Fix bug 497279 - IBus does not works with evolution correctly.
- Enhance authentication both in daemon & clients

* Fri Apr 17 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090417-1
- Update to ibus-1.1.0.20090417.
- Fix bug 496199 -  cannot remove Ctrl+Space hotkey with ibus-setup

* Fri Apr 17 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090413-4
- Update ibus-HEAD.patch.
- Next Engine hotkey will do nothing if the IM is not active.

* Wed Apr 15 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090413-3
- Update ibus-HEAD.patch.
- Fix bug 495431 -  ibus Release modifier doesn't work with Alt
- Fix bug 494445 -  ibus-hangul missing Hangul Han/En mode
  (and Alt_R+release hotkey)
- Update te.po

* Tue Apr 14 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090413-2
- Update ibus-HEAD.patch.
- Change the mode of /tmp/ibus-$USER to 0700 to improve security
- Change the mode of /tmp/ibus-$USER/socket-address to 0600 to improve security
- Update as.po

* Mon Apr 13 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090413-1
- Update to ibus-1.1.0.20090413.
- Fix crash when restart the ibus-daemon
- Add some translations.

* Tue Apr 07 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090407-3
- Update the tarball.
- Fix bug 494511 - ibus-gtk makes gnome-terminal abort 
  when a key is pressed

* Tue Apr 07 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090407-2
- Update default hotkey settings.

* Tue Apr 07 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090407-1
- Update to ibus-1.1.0.20090407.
- Fix bug 491042 - ibus default trigger hotkeys
- Fix bug 492929 - ibus-hangul can cause gtk app to lockup
- Fix bug 493701 -  (ibus) imsettings disconnect/reconnect kills gtk app
- Fix bug 493687 -  ibus-hangul should default to vertical candidate selection
- Fix bug 493449 -  ibus broke Alt-F2 command auto-completion

* Tue Mar 31 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090331-1
- Update to ibus-1.1.0.20090331.
- Fix bug 492956 - screws up keyboard input in firefox
- Fix bug 490143 - ibus issue with gnome-keyring

* Sun Mar 29 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090311-3
- Recreate the ibus-HEAD.patch from upstream git source tree
- Fix bug 491999 - up/down arrow keys broken in xchat

* Sat Mar 28 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090311-2
- Recreate the ibus-HEAD.patch from upstream git source tree.
- Fix bug 490009 - Deleting Next Engine shortcuts doesn't work
- Fix bug 490381 - Change "Next/Previous engine" labels

* Wed Mar 11 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090311-1
- Update to ibus-1.1.0.20090311.
- Update setup ui follow GNOME Human Interface Guidelines 2.2 (#489497).

* Fri Mar  6 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090306-1
- Update to ibus-1.1.0.20090306.

* Tue Mar  3 2009 Jens Petersen <petersen@redhat.com>
- use post for ibus-gtk requires glib2

* Mon Mar  2 2009 Jens Petersen <petersen@redhat.com> - 1.1.0.20090225-2
- drop the superfluous ibus-0.1 engine obsoletes
- move glib2 requires to gtk package

* Wed Feb 25 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090225-1
- Update to ibus-1.1.0.20090225.
- Fix problems in %%post and %%postun scripts.
- Hide ibus & ibus preferences menu items.

* Tue Feb 17 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090211-10
- Recreate the ibus-HEAD.patch from upstream git source tree.
- Put 'Select an input method' in engine select combobox (#485861).

* Tue Feb 17 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090211-9
- Add requires im-chooser >= 1.2.5.

* Tue Feb 17 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090211-8
- Recreate the ibus-HEAD.patch from upstream git source tree.
- Fix ibus-hangul segfault (#485438).

* Mon Feb 16 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090211-6
- Recreate the ibus-HEAD.patch from upstream git source tree.
- The new patch fixes ibus-x11 segfault (#485661).

* Sun Feb 15 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090211-5
- Recreate the ibus-HEAD.patch from upstream git source tree.

* Sun Feb 15 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090211-4
- Remove gnome-python2-gconf from requires.

* Fri Feb 13 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090211-3
- Update ibus-HEAD.patch, to fix bug 484652.

* Fri Feb 13 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090211-2
- Add patch ibus-HEAD.patch, to update ibus to HEAD version.

* Wed Feb 11 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090211-1
- Add --xim argument in xinput-ibus
- Add Obsoletes:  ibus-qt <= 1.1.0
- Move libibus.so.* to ibus-libs to make ibus multilib.
- Update to 1.1.0.20090211.

* Thu Feb 05 2009 Peng Huang <phuang@redhat.com> - 1.1.0.20090205-1
- Update to 1.1.0.20090205.

* Tue Feb 03 2009 Peng Huang <phuang@redhat.com> - 0.1.1.20090203-1
- Update to 0.1.1.20090203.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1.1.20081023-3
- Rebuild for Python 2.6

* Wed Nov 19 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20081023-2
- Move libibus-gtk.so from ibus.rpm to ibus-gtk.rpm to fix bug 472146.

* Thu Oct 23 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20081023-1
- Update to 0.1.1.20081023.

* Thu Oct 16 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20081016-1
- Update to 0.1.1.20081016.

* Tue Oct  7 2008 Jens Petersen <petersen@redhat.com> - 0.1.1.20081006-3
- remove the empty %%doc file entries

* Tue Oct  7 2008 Jens Petersen <petersen@redhat.com> - 0.1.1.20081006-2
- add xinputrc alternative when installing or uninstalling

* Mon Oct 06 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20081006-1
- Update to 0.1.1.20081006.

* Sun Oct 05 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20081005-1
- Update to 0.1.1.20081005.

* Sat Oct 04 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20081004-1
- Update to 0.1.1.20081004.

* Wed Oct 01 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20081001-1
- Update to 0.1.1.20081001.

* Tue Sep 30 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20080930-1
- Update to 0.1.1.20080930.

* Tue Sep 23 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20080923-1
- Update to 0.1.1.20080923.

* Wed Sep 17 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20080917-1
- Update to 0.1.1.20080917.

* Tue Sep 16 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20080916-1
- Update to 0.1.1.20080916.

* Mon Sep 15 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20080914-1
- Update to 0.1.1.20080914.

* Mon Sep 08 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20080908-1
- Update to 0.1.1.20080908.

* Mon Sep 01 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20080901-1
- Update to 0.1.1.20080901.

* Sat Aug 30 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20080830-1
- Update to 0.1.1.20080830.

* Mon Aug 25 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20080825-1
- Update to 0.1.1.20080825.

* Sat Aug 23 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20080823-1
- Update to 0.1.1.20080823.

* Fri Aug 15 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20080815-1
- Update to 0.1.1.20080815.

* Tue Aug 12 2008 Peng Huang <phuang@redhat.com> - 0.1.1.20080812-1
- Update to 0.1.1.20080812.

* Mon Aug 11 2008 Peng Huang <phuang@redhat.com> - 0.1.0.20080810-2
- Add gnome-python2-gconf in Requires.

* Thu Aug 07 2008 Peng Huang <phuang@redhat.com> - 0.1.0.20080810-1
- The first version.
