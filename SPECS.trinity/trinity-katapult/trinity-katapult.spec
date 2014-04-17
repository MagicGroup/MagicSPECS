# Default version for this component
%define kdecomp katapult
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
Summary:	Faster access to applications, bookmarks, and other items.
Version:	0.3.2.1
Release:	6%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz


BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils

%description
Katapult is an application for TDE, designed to allow faster access to
applications, bookmarks, and other items. It is plugin-based, so it can
launch anything that is has a plugin for. Its display is driven by
plugins as well, so its appearance is completely customizable. It was
inspired by Quicksilver for OS X. 


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-trinity-%{tdeversion}

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i "admin/acinclude.m4.in" \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f admin/Makefile.common


%build
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --disable-rpath \
  --with-extra-includes=%{tde_includedir}/tqt \
  --enable-closure

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%find_lang %{kdecomp}

# Removes useless files (-devel ?)
%__rm -f %{?buildroot}%{tde_libdir}/*.so
%__rm -f %{?buildroot}%{tde_libdir}/*.la

%clean
%__rm -rf %{buildroot}


%post
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig || :
update-desktop-database %{tde_appdir} &> /dev/null

%postun
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig || :
update-desktop-database %{tde_appdir} &> /dev/null


%files -f %{kdecomp}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_bindir}/katapult
%{tde_libdir}/libkatapult.so.2
%{tde_libdir}/libkatapult.so.2.0.0
%{tde_tdelibdir}/katapult_amarokcatalog.la
%{tde_tdelibdir}/katapult_amarokcatalog.so
%{tde_tdelibdir}/katapult_bookmarkcatalog.la
%{tde_tdelibdir}/katapult_bookmarkcatalog.so
%{tde_tdelibdir}/katapult_calculatorcatalog.la
%{tde_tdelibdir}/katapult_calculatorcatalog.so
%{tde_tdelibdir}/katapult_documentcatalog.la
%{tde_tdelibdir}/katapult_documentcatalog.so
%{tde_tdelibdir}/katapult_execcatalog.la
%{tde_tdelibdir}/katapult_execcatalog.so
%{tde_tdelibdir}/katapult_glassdisplay.la
%{tde_tdelibdir}/katapult_glassdisplay.so
%{tde_tdelibdir}/katapult_googlecatalog.la
%{tde_tdelibdir}/katapult_googlecatalog.so
%{tde_tdelibdir}/katapult_o2display.la
%{tde_tdelibdir}/katapult_o2display.so
%{tde_tdelibdir}/katapult_programcatalog.la
%{tde_tdelibdir}/katapult_programcatalog.so
%{tde_tdelibdir}/katapult_puredisplay.la
%{tde_tdelibdir}/katapult_puredisplay.so
%{tde_tdelibdir}/katapult_spellcatalog.la
%{tde_tdelibdir}/katapult_spellcatalog.so
%{tde_tdeappdir}/katapult.desktop
%{tde_datadir}/icons/crystalsvg/128x128/actions/katapultspellcheck.png
%{tde_datadir}/icons/crystalsvg/scalable/actions/katapultspellcheck.svgz
%{tde_datadir}/icons/hicolor/128x128/actions/checkmark.png
%{tde_datadir}/icons/hicolor/128x128/actions/no.png
%{tde_datadir}/icons/hicolor/128x128/apps/xcalc.png
%{tde_datadir}/icons/hicolor/*/apps/katapult.png
%{tde_datadir}/icons/hicolor/scalable/apps/katapult.svgz
%{tde_datadir}/services/katapult_amarokcatalog.desktop
%{tde_datadir}/services/katapult_bookmarkcatalog.desktop
%{tde_datadir}/services/katapult_calculatorcatalog.desktop
%{tde_datadir}/services/katapult_documentcatalog.desktop
%{tde_datadir}/services/katapult_execcatalog.desktop
%{tde_datadir}/services/katapult_glassdisplay.desktop
%{tde_datadir}/services/katapult_googlecatalog.desktop
%{tde_datadir}/services/katapult_o2display.desktop
%{tde_datadir}/services/katapult_programcatalog.desktop
%{tde_datadir}/services/katapult_puredisplay.desktop
%{tde_datadir}/services/katapult_spellcatalog.desktop
%{tde_datadir}/servicetypes/katapultcatalog.desktop
%{tde_datadir}/servicetypes/katapultdisplay.desktop
%{tde_tdedocdir}/HTML/en/katapult/


%changelog
* Wed Jul 31 2013 Liu Di <liudidi@gmail.com> - 0.3.2.1-6.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.3.2.1-5
- Initial build for TDE 3.5.13.1

* Tue May 01 2012 Francois Andriot <francois.andriot@free.fr> - 0.3.2.1-4
- Rebuilt for Fedora 17
- Fix post and postun

* Fri Nov 25 2011 Francois Andriot <francois.andriot@free.fr> - 0.3.2.1-3
- Fix HTML directory location

* Sun Oct 30 2011 Francois Andriot <francois.andriot@free.fr> - 0.3.2.1-2
- Rebuilt for TDE 3.5.13 on RHEL 6, RHEL 5 and Fedora 15

* Tue Sep 14 2011 Francois Andriot <francois.andriot@free.fr> - 0.3.2.1-1
- Initial build for RHEL 6.0
- Import to GIT

