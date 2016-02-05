Name:		mate-applet-softupd
Version: 0.4.3
Release: 2%{?dist}
Summary:	MATE Software Update Applet 
Summary(zh_CN.UTF-8): MATE 软件更新小部件
Group:		Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
License:	GPLv2+
URL:		http://www.zavedil.com/mate-software-updates-applet/
Source:		http://www.zavedil.com/wp-content/uploads/2015/10/mate-applet-softupd-%{version}.tar.gz
BuildRequires:	mate-panel-devel >= 1.3.0
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	PackageKit-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	PackageKit
BuildRequires:	yumex
# BuildRequires:	autoconf
# BuildRequires:	automake
Requires:	PackageKit%{?_isa}
Requires:	yumex

%description
Software updates notification applet for the MATE desktop environment.

%description -l zh_CN.UTF-8
MATE 软件更新小部件。

%prep
%setup -q


%build
%configure --enable-notify=libnotify
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

#	Do not install doc files: they are handled as rpm doc files.
rm -rf $RPM_BUILD_ROOT%{_docdir}
magic_rpm_clean.sh
%find_lang %{name} || :


%post
/bin/touch --nocreate %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ]
then	/bin/touch --nocreate %{_datadir}/icons/hicolor &>/dev/null
	/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files 
%doc AUTHORS BUGS COPYING ChangeLog README TODO
%{_libexecdir}/softupd_applet
%{_datadir}/pixmaps/applet_softupd_on.png
%{_datadir}/pixmaps/applet_softupd_off.png
%{_datadir}/icons/hicolor/16x16/apps/applet_softupd.png
%{_datadir}/icons/hicolor/22x22/apps/applet_softupd.png
%{_datadir}/icons/hicolor/24x24/apps/applet_softupd.png
%{_datadir}/icons/hicolor/32x32/apps/applet_softupd.png
%{_datadir}/mate-panel/applets/org.mate.applets.SoftupdApplet.mate-panel-applet
%{_datadir}/dbus-1/services/org.mate.panel.applet.SoftupdApplet.service


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.4.3-2
- 更新到 0.4.3

* Sun Aug 10 2014 Liu Di <liudidi@gmail.com> - 0.2.11-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Patrick Monnerat <pm@datasphere.ch> 0.2.11-1
- New upstream release.
- Stop timers on applet destroy.
  https://bugzilla.redhat.com/show_bug.cgi?id=1086989

* Wed Dec 11 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 0.2.10-2
- Add %%{?_isa} to PackageKit Requires to avoid arch-independent deps on
  PackageKit causing multiarch conflicts (#972571).

* Mon Nov 11 2013 Patrick Monnerat <pm@datasphere.ch> 0.2.10-1
- New upstream release.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Patrick Monnerat <pm@datasphere.ch> 0.2.8-1
- New upstream release.

* Fri May 10 2013 Patrick Monnerat <pm@datasphere.ch> 0.2.7-1
- New upstream release.

* Tue Apr 16 2013 Patrick Monnerat <pm@datasphere.ch> 0.2.5-4
- Patch "notify" for Mate 1.6 to replace use of obsolete "libmatenotify" by
  "libnotify".

* Tue Mar 12 2013 Patrick Monnerat <pm@datasphere.ch> 0.2.5-3
- Patch "morefrench" to add a missing french translation string.

* Mon Mar 11 2013 Patrick Monnerat <pm@datasphere.ch> 0.2.5-2
- Update according to https://bugzilla.redhat.com/show_bug.cgi?id=919469#c2

* Fri Mar  8 2013 Patrick Monnerat <pm@datasphere.ch> 0.2.5-1
- New upstream release.
- Patch "misc" fixes various discrepancies.

* Wed Mar  6 2013 Patrick Monnerat <pm@datasphere.ch> 0.2.4-1
- New upstream release.
- Patch "badvarset" to fix a variable setting in configure.ac.

* Tue Mar  5 2013 Patrick Monnerat <pm@datasphere.ch> 0.2.2-1
- Initial Fedora rpm spec file.
- Patch "lmpa4" to migrate to libmatepanelapplet-4.0.
- Patch "cflags" to allow external specification of compilation/linking options.
- Patch "nowarnings" to suppress compilation warnings.
- Patch "french" to implement a french translation.
