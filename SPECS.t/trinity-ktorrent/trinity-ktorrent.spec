# Default version for this component
%define kdecomp ktorrent
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


Name:		trinity-%{kdecomp}
Summary:	BitTorrent client for Trinity
Version:	2.2.8
Release:	3%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://ktorrent.org

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz


BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	gettext


%description
KTorrent is a BitTorrent program for Trinity. Its features include speed capping
(both down and up), integrated searching, UDP tracker support, preview of
certain file types (video and audio) and integration into the KDE Panel
enabling background downloading.
 

%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-trinity-%{tdeversion}

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
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
  --with-extra-includes=%{tde_includedir}/tqt


# Not SMP safe !
%__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}


%find_lang %{kdecomp}

# Unwanted files
%__rm -f %{?buildroot}%{tde_libdir}/libktorrent.so


%clean
%__rm -rf %{buildroot}


%post
update-desktop-database %{tde_appdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
/sbin/ldconfig || :

%postun
update-desktop-database %{tde_appdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
/sbin/ldconfig || :


%files -f %{kdecomp}.lang
%defattr(-,root,root,-)
%{tde_bindir}/ktcachecheck
%{tde_bindir}/ktorrent
%{tde_bindir}/ktshell
%{tde_bindir}/kttorinfo
%{tde_bindir}/ktupnptest
%{tde_libdir}/libktorrent-%{version}.so
%{tde_libdir}/libktorrent.la
%{tde_tdelibdir}/ktinfowidgetplugin.la
%{tde_tdelibdir}/ktinfowidgetplugin.so
%{tde_tdelibdir}/ktipfilterplugin.la
%{tde_tdelibdir}/ktipfilterplugin.so
%{tde_tdelibdir}/ktlogviewerplugin.la
%{tde_tdelibdir}/ktlogviewerplugin.so
%{tde_tdelibdir}/ktpartfileimportplugin.la
%{tde_tdelibdir}/ktpartfileimportplugin.so
%{tde_tdelibdir}/ktrssfeedplugin.la
%{tde_tdelibdir}/ktrssfeedplugin.so
%{tde_tdelibdir}/ktscanfolderplugin.la
%{tde_tdelibdir}/ktscanfolderplugin.so
%{tde_tdelibdir}/ktschedulerplugin.la
%{tde_tdelibdir}/ktschedulerplugin.so
%{tde_tdelibdir}/ktsearchplugin.la
%{tde_tdelibdir}/ktsearchplugin.so
%{tde_tdelibdir}/ktstatsplugin.la
%{tde_tdelibdir}/ktstatsplugin.so
%{tde_tdelibdir}/ktupnpplugin.la
%{tde_tdelibdir}/ktupnpplugin.so
%{tde_tdelibdir}/ktwebinterfaceplugin.la
%{tde_tdelibdir}/ktwebinterfaceplugin.so
%{tde_tdeappdir}/ktorrent.desktop
%{tde_datadir}/apps/ktorrent
%{tde_datadir}/config.kcfg/*.kcfg
%{tde_datadir}/icons/hicolor/*/*/*.png
%{tde_datadir}/icons/hicolor/*/*/*.svgz
%{tde_datadir}/services/*.desktop
%{tde_datadir}/servicetypes/ktorrentplugin.desktop


%changelog
* Tue Aug 06 2013 Liu Di <liudidi@gmail.com> - 2.2.8-3.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 2.2.8-2
- Initial build for TDE 3.5.13.1

* Sat May 05 2012 Francois Andriot <francois.andriot@free.fr> - 2.2.8-1
- Rename old tq methods that no longer need a unique name [Commit #a90eb215]
- Remove additional unneeded tq method conversions [Commit #bb37c405]
- Rename obsolete tq methods to standard names [Commit #0d48fca8]
- Rename a few stragglers [Commit #c3480dfe]
- Fix inadvertent "TQ" changes. [Commit #445a5152]
- Fix configure output message to clarify that missing avahi support is caused by missing avahi-tqt package as well as avahi-client. [Commit #03d0c794]
- Update ktorrent package to 2.2.8 and fix internal geoip database. [Bug #363] [Commit #5af9907f]
- Change default configuration to use external geoip database when found and use internal database only when external database is not found. [Bug #443] [Commit #355c6b69]

* Tue Nov 29 2011 Francois Andriot <francois.andriot@free.fr> - 2.2.6-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16
