# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man

%define tde_tdeappdir %{tde_datadir}/applications/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}

Name:			trinity-ksensors
Version:		0.7.3
Release:		19p3%{?dist}%{?_variant}

Summary:        KDE frontend to lm_sensors
Group:          Applications/System
License:        GPLv2+
URL:            http://ksensors.sourceforge.net/

Source0:        http://downloads.sourceforge.net/ksensors/ksensors-%{version}.tar.gz

# Debian (upstream) patch
Patch2:         ksensors_0.7.3-18.diff
# Fix 'lmsensor.cpp' for older lm_sensors API (< 3.x)
Patch7:			ksensors-0.7.3-18-lmsensors_2x_fix.patch
# [ksensors] Fix autotools detection
Patch9:			ksensors-0.7.3-fix_autotools_detection.patch
# Fix TDE directories detection
Patch10:		ksensors-0.7.3-tde_includedir.patch
# Fix sound installation
Patch11:		ksensors-0.7.3-fix_sound_installation.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	gettext
BuildRequires:	desktop-file-utils

%if 0%{?suse_version}
BuildRequires:	libsensors4-devel
%else
BuildRequires:	lm_sensors-devel
%endif

# Keep archs in sync with lm_sensors
ExcludeArch:    s390 s390x

%description
KSensors is a nice lm-sensors frontend for the K Desktop Environment.
Install the hddtemp package if you wish to monitor hard disk
temperatures with KSensors.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n ksensors-%{version}
%patch2 -p1 -b .debian
%patch7 -p1 -b .lm2x
%patch9 -p1 -b .autotools
%patch10 -p1 -b .tdeinc
%patch11 -p1 -b .sound

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"

%__sed -i -e 's|$(kde_datadir)/sounds|$(kde_sounddir)|' src/sounds/Makefile.*
for f in ChangeLog LIESMICH LISEZMOI ; do
    iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
done

%build
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

export KDEDIR=%{tde_prefix}

%configure \
	--prefix=%{tde_prefix} \
	--exec-prefix=%{tde_prefix} \
	--disable-dependency-tracking \
	--disable-rpath \
	--with-extra-includes=%{tde_includedir}/tqt \
	--with-qt-libraries=${QTLIB:-${QTDIR}/%{_lib}} \
	--bindir=%{tde_bindir} \
	--libdir=%{tde_libdir} \
	--datadir=%{tde_datadir} \
	--includedir=%{tde_tdeincludedir} 

%__make %{?_smp_mflags} LIBTOOL=$(which libtool)


%install
%__rm -rf $RPM_BUILD_ROOT
%__make install DESTDIR=$RPM_BUILD_ROOT

# Creates autostart shortcut
%__install -dm 755 $RPM_BUILD_ROOT%{tde_datadir}/autostart
%__ln_s ../applnk/Utilities/ksensors.desktop \
    $RPM_BUILD_ROOT%{tde_datadir}/autostart

#__rm -rf $RPM_BUILD_ROOT%{tde_tdedocdir}/HTML

%find_lang ksensors


%clean
%__rm -rf $RPM_BUILD_ROOT


%post
for f in locolor hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null || :
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null || :
done

%postun
for f in locolor hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null || :
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null || :
done


%files -f ksensors.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ README TODO
%lang(es) %doc LEEME
%lang(de) %doc LIESMICH
%lang(fr) %doc LISEZMOI
%{tde_bindir}/ksensors
%{tde_datadir}/applnk/Utilities/ksensors.desktop
%{tde_datadir}/apps/ksensors/
%{tde_datadir}/autostart/ksensors.desktop
%{tde_datadir}/icons/hicolor/*/apps/ksensors.png
%{tde_datadir}/icons/locolor/
%{tde_datadir}/sounds/ksensors_alert.wav
%{tde_tdedocdir}/HTML/en/ksensors/

%changelog
* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.7.3-19p3
- Initial build for TDE 3.5.13.1

* Thu Dec 22 2011 Francois Andriot <francois.andriot@free.fr> - 0.7.3-19p2
- Update Debian patch to -18 release

* Mon Nov 07 2011 Francois Andriot <francois.andriot@free.fr> - 0.7.3-19p1
- Rebuilt for RHEL 6, RHEL 5, Fedora 15 with TDE 3.5.13

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 15 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.7.3-16
- Update Debian patch to -15 release

* Thu Jan  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.7.3-15
- Change BuildRequires: kdelibs-devel into kdelibs3-devel

* Sun Nov 11 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.7.3-14
- Patch for and Rebuild against lm_sensors-3.0.0

* Sun Nov 11 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.7.3-13
- Fix reading of min and max tresholds from libsensors

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.7.3-12
- Update License tag for new Licensing Guidelines compliance

* Fri Jul 27 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.7.3-11
- Remove OnlyShowIn=KDE; from .desktop file (I like using ksensors under GNOME,
  works fine grumbel) 

* Fri Jul 27 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.7.3-10
- Add icon-cache update scriptlets
- Add Requires: hicolor-icon-theme for dir ownership

* Fri Jul 20 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.7.3-9
- Sync Exclu(de|sive)Arch with new lm_sensors (#249060).

* Tue Jun 26 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.7.3-8
- Update Debian patchset to -14 for additional fixes and translations;
  drop our hddtemp detection patch in favour of the one included in it.
- Drop Application and X-Fedora categories from .desktop file, add GenericName.
- Make autostart checkbox effective again (#242570).
- Convert docs to UTF-8.

* Sat Sep 30 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.7.3-7
- Apply Debian -11 patchset for upstream radio button state fix,
  support for hddtemp with SCSI disks and more translations.

* Wed Aug 30 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.7.3-6
- Rebuild.

* Wed Feb 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.7.3-5
- Rebuild.

* Thu Nov  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.3-4
- Clean up build dependencies.

* Thu May 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.3-3
- Sync arch availability with FC4 lm_sensors (%%{ix86}, x86_64, alpha).
- Reduce directory ownership bloat.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.7.3-2
- rebuilt

* Sat Aug 21 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.3-0.fdr.1
- Update to 0.7.3, most patches applied upstream.
- Disable dependency tracking to speed up the build.

* Tue Jul 20 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.2-0.fdr.4
- Force use of multithreaded Qt with --enable-mt to fix build on FC2.
- Sync Debian patch to 0.7.2-16 to get a fix for freeze with hddtemp.
- Apply upstream patches #913569 and #915725.
- Disable RPATH.
- Don't ship the "handbook", it's just a template.
- Other minor improvements here and there.

* Sat Aug  2 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.2-0.fdr.3
- Own dirs under %%{_datadir}/icons and %%{_docdir}/HTML (bug 21).
- Don't tweak path to hddtemp.
- Patch to fix hddtemp detection.
- s/--enable-xinerama/--with-xinerama/
- Borrow man page from Debian.

* Sat May 31 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.2-0.fdr.2
- Spec cleanups.

* Fri Apr  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.2-0.fdr.1
- Update to current Fedora guidelines.
- Move desktop entry to %%{_datadir}/applications using desktop-file-install.

* Sun Feb 23 2003 Warren Togami <warren@togami.com> - 0.7.2-1.fedora.2
- BuildRequires libart_lgpl-devel needed for Red Hat 8.1

* Sun Feb 23 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.7.2-1.fedora.1
- Update to 0.7.2.
- Don't apply startup crash patch, but keep it around for now.

* Sat Feb 15 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.7-1.fedora.2
- Include startup crash patch from upstream SRPM.

* Sun Feb  9 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.7-1.fedora.1
- First Fedora release.
