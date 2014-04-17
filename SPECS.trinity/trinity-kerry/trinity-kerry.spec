# Default version for this component
%define kdecomp kerry

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
Summary:	a KDE frontend for the Beagle desktop search daemon [Trinity]
Version:	0.2.1
Release:	2%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://en.opensuse.org/Kerry

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-3.5.13.1.tar.gz
Source1:	kerry.1.docbook


BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	libbeagle-devel >= 0.3.0


%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	docbook2x
%else
BuildRequires:	docbook2X
%endif

%description
Kerry is a Trinity frontend for the Beagle desktop search daemon.

A program for indexing and searching user's data. At the moment, it can index
filesystems, chat logs, mail and data, RSS and other.



%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-3.5.13.1

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
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --disable-rpath \
  --with-extra-includes=%{tde_includedir}/tqt:%{tde_includedir}

%__make %{?_smp_mflags}



%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

#%__install -D -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man1/kerry.1.docbook
#docbook2man %{buildroot}%{_mandir}/man1/kerry.1.docbook

%find_lang %{kdecomp}

%clean
%__rm -rf %{buildroot}


%post
/sbin/ldconfig || :
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
update-desktop-database %{tde_appdir} &> /dev/null

%postun
/sbin/ldconfig || :
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
update-desktop-database %{tde_appdir} &> /dev/null


%files -f %{kdecomp}.lang
%defattr(-,root,root,-)
%{tde_datadir}/locale/*/LC_MESSAGES/kcmbeagle.mo
%{tde_bindir}/beagled-shutdown
%{tde_bindir}/kerry
%{tde_libdir}/libkdeinit_kerry.la
%{tde_libdir}/libkdeinit_kerry.so
%{tde_tdelibdir}/kcm_beagle.la
%{tde_tdelibdir}/kcm_beagle.so
%{tde_tdelibdir}/kerry.la
%{tde_tdelibdir}/kerry.so
%{tde_tdeappdir}/kcmbeagle.desktop
%{tde_tdeappdir}/kerry.desktop
%{tde_datadir}/applnk/.hidden/kcmkerry.desktop
%{tde_datadir}/apps/kerry/search-running.mng
%{tde_datadir}/autostart/beagled.desktop
%{tde_datadir}/autostart/kerry.autostart.desktop
%{tde_datadir}/icons/hicolor/*/*/*


%changelog
* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.2.1-2
- Initial build for TDE 3.5.13.1

* Fri Nov 25 2011 Francois Andriot <francois.andriot@free.fr> - 0.2.1-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16
