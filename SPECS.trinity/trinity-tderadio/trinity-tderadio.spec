# Default version for this component
%define tdecomp kradio
%define tdeversion 3.5.13.2

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_appdir %{tde_datadir}/applications

%define tde_tdeappdir %{tde_appdir}/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}

%if 0%{?rhel} >= 6 || 0%{?fedora} || 0%{?mdkversion} || 0%{?mgaversion} || 0%{?suse_version}
%define with_lirc 1
%endif

Name:		trinity-tderadio
Summary:	Comfortable Radio Application for KDE [Trinity]
Version:	0.1.1.1
Release:	8%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{tdecomp}-trinity-%{tdeversion}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.2
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.2
BuildRequires:	trinity-tdebase-devel >= 3.5.13.2
BuildRequires:	trinity-arts-devel >= 3.5.13.2
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	libsndfile-devel
%{?with_lirc:BuildRequires:	lirc-devel}

%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}twolame-devel
%endif
%if 0%{?suse_version}
BuildRequires:	libtwolame-devel
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lame-devel
%endif

Obsoletes:		trinity-kradio < %{version}-%{release}
Provides:		trinity-kradio = %{version}-%{release}

%description
KRadio is a comfortable radio application for Trinity with support for 
V4L and V4L2 radio cards drivers.

KRadio currently provides

 * V4L/V4L2 radio support
%if 0%{?with_lirc}
 * Remote control support (LIRC)
%endif
 * Alarms, sleep Countdown
 * Several GUI Controls (Docking Menu, Station Quickbar, Radio Display)
 * Recording capabilities, including MP3 and Ogg/Vorbis encoding
 * Timeshifter functionality
 * Extendable plugin architecture

This package also includes a growing collection of station preset
files for many cities around the world contributed by KRadio users.

As KRadio is based on an extendable plugin architecture, contributions
of new plugins (e.g. Internet Radio Streams, new cool GUIs) are welcome.


%if 0%{?suse_version} || 0%{?pclinuxos}
%debug_package
%endif


%prep
%setup -q -n %{tdecomp}-trinity-%{tdeversion}%{?preversion:~%{preversion}}

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"



%build
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  --disable-rpath \
  --with-extra-includes=%{tde_includedir}/tqt \
  %{?with_lirc:--enable-lirc} %{?!with_lirc:--disable-lirc} \
  --enable-v4l2 \
  --enable-lame \
  --enable-ogg \
  --enable-alsa \
  --enable-oss

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%find_lang kradio

%clean
%__rm -rf %{buildroot}


%post
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
update-desktop-database %{tde_appdir} -q &> /dev/null ||:

%postun
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
update-desktop-database %{tde_appdir} -q &> /dev/null ||:


%files -f kradio.lang
%defattr(-,root,root,-)
%{tde_bindir}/convert-presets
%{tde_bindir}/kradio
%{tde_libdir}/kradio/plugins/*.la
%{tde_libdir}/kradio/plugins/*.so
%{tde_tdeappdir}/kradio.desktop
%{tde_datadir}/apps/kradio/
%{tde_datadir}/icons/hicolor/*/*/kradio*.png
%{tde_datadir}/icons/locolor/*/*/kradio*.png
%lang(de) %{tde_datadir}/locale/de/LC_MESSAGES/*.mo
%lang(ru) %{tde_datadir}/locale/ru/LC_MESSAGES/*.mo

%changelog
* Fri Aug 09 2013 Liu Di <liudidi@gmail.com> - 0.1.1.1-8.opt
- 为 Magic 3.0 重建

* Fri Aug 09 2013 Liu Di <liudidi@gmail.com> - 0.1.1.1-7.opt
- 为 Magic 3.0 重建

* Mon Jun 03 2013 Francois Andriot <francois.andriot@free.fr> - 0.1.1.1-6
- Initial release for TDE 3.5.13.2

* Sat Dec 01 2012 Francois Andriot <francois.andriot@free.fr> - 0.1.1.1-5
- Updates presets

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.1.1.1-4
- Initial release for TDE 3.5.13.1

* Sun Jul 08 2012 Francois Andriot <francois.andriot@free.fr> - 0.1.1.1-3
- Rebuild for RHEL 5
- Fix postinstall

* Wed May 02 2012 Francois Andriot <francois.andriot@free.fr> - 0.1.1.1-2
- Rebuild for Fedora 17
- Fix HTML directory location

* Sat Nov 19 2011 Francois Andriot <francois.andriot@free.fr> - 0.1.1.1-1
- Initial release for RHEL 5, RHEL 6, Fedora 15, Fedora 16
