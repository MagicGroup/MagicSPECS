# Default version for this component
%define tdecomp kpilot
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


Name:		trinity-%{tdecomp}
Summary:	TDE Palm Pilot hot-sync tool
Version:	0.7
Release:	5%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{tdecomp}-trinity-%{tdeversion}.tar.xz


BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.2
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.2
BuildRequires:	trinity-tdebase-devel >= 3.5.13.2
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	pilot-link-devel
BuildRequires:	trinity-kdepim-devel

%description
KPilot is an application that synchronizes your Palm Pilot or similar device
(like the Handspring Visor) with your KDE desktop, much like the Palm HotSync
software does for Windows.  KPilot can back-up and restore your Palm Pilot
and synchronize the built-in applications with their KDE counterparts.


%if 0%{?suse_version} || 0%{?pclinuxos}
%debug_package
%endif


%prep
%setup -q -n %{tdecomp}-trinity-%{tdeversion}

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
  --with-extra-includes=%{tde_includedir}/tqt:%{tde_tdeincludedir}

# SMP safe !
%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# Unwanted files
%__rm -f %{?buildroot}%{tde_libdir}/libkpilot.so



%clean
%__rm -rf %{buildroot}


%post
update-desktop-database %{tde_appdir} > /dev/null
for f in hicolor locolor crystalsvg; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig || :

%postun
update-desktop-database %{tde_appdir} > /dev/null
for f in hicolor locolor crystalsvg; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig || :


%files
%defattr(-,root,root,-)
%{tde_bindir}/kpalmdoc
%{tde_bindir}/kpilot
%{tde_bindir}/kpilotDaemon
%{tde_tdeincludedir}/kpilot
%{tde_libdir}/libkpilot.la
%{tde_libdir}/libkpilot.so.0
%{tde_libdir}/libkpilot.so.0.0.0
%{tde_tdelibdir}/conduit_address.la
%{tde_tdelibdir}/conduit_address.so
%{tde_tdelibdir}/conduit_doc.la
%{tde_tdelibdir}/conduit_doc.so
%{tde_tdelibdir}/conduit_knotes.la
%{tde_tdelibdir}/conduit_knotes.so
%{tde_tdelibdir}/conduit_memofile.la
%{tde_tdelibdir}/conduit_memofile.so
%{tde_tdelibdir}/conduit_notepad.la
%{tde_tdelibdir}/conduit_notepad.so
%{tde_tdelibdir}/conduit_popmail.la
%{tde_tdelibdir}/conduit_popmail.so
%{tde_tdelibdir}/conduit_sysinfo.la
%{tde_tdelibdir}/conduit_sysinfo.so
%{tde_tdelibdir}/conduit_time.la
%{tde_tdelibdir}/conduit_time.so
%{tde_tdelibdir}/conduit_todo.la
%{tde_tdelibdir}/conduit_todo.so
%{tde_tdelibdir}/conduit_vcal.la
%{tde_tdelibdir}/conduit_vcal.so
%{tde_tdelibdir}/kcm_kpilot.la
%{tde_tdelibdir}/kcm_kpilot.so
%{tde_tdelibdir}/conduit_mal.la
%{tde_tdelibdir}/conduit_mal.so
%{tde_tdeappdir}/kpalmdoc.desktop
%{tde_tdeappdir}/kpilot.desktop
%{tde_tdeappdir}/kpilotdaemon.desktop
%{tde_datadir}/apps/kaddressbook/contacteditorpages/KPilotCustomFieldEditor.ui
%{tde_datadir}/apps/kconf_update/kpalmdoc.upd
%{tde_datadir}/apps/kconf_update/kpilot.upd
%{tde_datadir}/apps/kpilot
%{tde_datadir}/config.kcfg/*.kcfg
%{tde_datadir}/icons/crystalsvg/*/apps/*.png
%{tde_datadir}/icons/hicolor/*/apps/*.png
%{tde_datadir}/icons/locolor/*/apps/*.png
%{tde_datadir}/services/*.desktop
%{tde_datadir}/servicetypes/kpilotconduit.desktop


%changelog
* Fri Aug 09 2013 Liu Di <liudidi@gmail.com> - 0.7-5.opt
- 为 Magic 3.0 重建

* Mon Jun 03 2013 Francois Andriot <francois.andriot@free.fr> - 0.7-4
- Initial release for TDE 3.5.13.2

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.7-3
- Initial release for TDE 3.5.13.1

* Wed May 02 2012 Francois Andriot <francois.andriot@free.fr> - 0.7-2
- Rebuild for Fedora 17

* Wed Nov 30 2011 Francois Andriot <francois.andriot@free.fr> - 0.7-1
- Initial release for RHEL 5, RHEL 6, Fedora 15, Fedora 16
