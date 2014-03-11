%global minorversion 0.4

Name:           Terminal
Version:        0.4.8
Release:        4%{?dist}
Summary:        X Terminal Emulator for the Xfce Desktop environment

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://www.xfce.org/projects/terminal/
Source0:        http://archive.xfce.org/src/apps/terminal/%{minorversion}/%{name}-%{version}.tar.bz2
# http://bugzilla.xfce.org/show_bug.cgi?id=6686
Patch0:         Terminal-0.4.5-fix_build_with_sealed_vte.patch
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  vte-devel >= 0.17.1
BuildRequires:  exo-devel >= 0.3.4
BuildRequires:  libSM-devel
BuildRequires:  gettext intltool
BuildRequires:  startup-notification-devel
BuildRequires:  dbus-glib-devel >= 0.22
BuildRequires:  desktop-file-utils
# required for Terminal-default-apps.xml
Requires:       control-center-filesystem

%description
Terminal is a lightweight and easy to use terminal emulator application
for the X windowing system, with some new ideas and features that make 
it unique among X terminal emulators. 

%prep
%setup -q
%patch0 -p1 -b .sealed

%build
%configure
make %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
%find_lang %{name}
desktop-file-install                                       \
  --delete-original                                        \
  --add-category="GTK"                                     \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications          \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

# workaround for # 447156 - rpm cannot change directory to symlink
%pre
for dir in ca da fr gl id ja; do
#    [ -d "%{_datadir}/doc/Terminal/$dir/images" -a ! -L "%{_datadir}/doc/Terminal/$dir/images" ] && \
    [ ! -L "%{_datadir}/doc/Terminal/$dir/images" ] && \
    rm -rf %{_datadir}/doc/Terminal/$dir/images  || :
done

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root)
%doc README ChangeLog NEWS COPYING AUTHORS HACKING THANKS
%{_bindir}/Terminal
%{_bindir}/terminal
%{_datadir}/Terminal/
%{_datadir}/doc/Terminal/
%{_datadir}/icons/hicolor/48x48/apps/Terminal.png
%{_datadir}/icons/hicolor/scalable/apps/Terminal.svg
%{_datadir}/icons/hicolor/*/stock/navigation/*.png
%{_datadir}/pixmaps/terminal.xpm
%{_datadir}/applications/Terminal.desktop
%{_datadir}/gnome-control-center/default-apps/Terminal-default-apps.xml
%{_mandir}/man1/Terminal.1.*
%{_mandir}/*/man1/Terminal.1.*

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.4.8-4
- 为 Magic 3.0 重建

* Wed Nov 21 2012 Liu Di <liudidi@gmail.com> - 0.4.8-3
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Kevin Fenzi <kevin@scrye.com> - 0.4.8-1
- Update to 0.4.8

* Tue Apr 05 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.7-1
- Update to 0.4.7
- Remove upstreamed background.patch

* Sun Jan 30 2011 Kevin Fenzi <kevin@tummy.com> - 0.4.6-2
- Add patch to fix cpu and memory issues. 

* Sun Jan 30 2011 Kevin Fenzi <kevin@tummy.com> - 0.4.6-1
- Update to 0.4.6

* Mon Nov 08 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.5-3
- Rebuild for libfxce4gui 4.7.0

* Thu Sep 09 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.5-2
- Fix build error with vte >= 0.25.90 (#631447,bugzilla.xfce.org #6686)

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 0.4.5-1
- Update to 0.4.5

* Mon Feb 01 2010 Kevin Fenzi <kevin@tummy.com> - 0.4.4-1
- Update to 0.4.4

* Wed Dec 10 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.3-1
- Update to 0.4.3

* Thu Oct 08 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.2-2
- Fix locale problems in the UI (bugzilla.xfce.org #5842)

* Tue Oct 06 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.2-1
- Update to 0.4.2
- Update icon cache scriptlets

* Thu Oct 01 2009 Kevin Fenzi <kevin@tummy.com> - 0.4.1-1
- Update to 0.4.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0
- Use desktop-file-install

* Sun Jul 19 2009 Kevin Fenzi <kevin@tummy.com> - 0.2.99.1-1
- Update to 0.2.99.1

* Mon Apr 29 2009 Kevin Fenzi <kevin@tummy.com> - 0.2.12-3
- Fix patch fuzz

* Sun Apr 28 2009 Kevin Fenzi <kevin@tummy.com> - 0.2.12-2
- Add patch for MiscAlwaysShowTabs segfault (fixes bug 502135)

* Sun Apr 19 2009 Kevin Fenzi <kevin@tummy.com> - 0.2.12-1
- Update to 0.2.12

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.8.3-1
- Update to 0.2.8.3
- BuildRequire intltool
- Fix rpm group

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 0.2.8-3
- Rebuild for gcc43

* Mon Dec  3 2007 Kevin Fenzi <kevin@tummy.com> - 0.2.8-2
- Remove no longer shipped .ui file. 

* Sun Dec  2 2007 Kevin Fenzi <kevin@tummy.com> - 0.2.8-1
- Update to 0.2.8
- Drop unneeded patch. 

* Tue Aug 14 2007 Kevin Fenzi <kevin@tummy.com> - 0.2.6-3
- Add patch for CVE-2007-3770. 
- Update License tag

* Sat Mar 24 2007 Kevin Fenzi <kevin@tummy.com> - 0.2.6-2
- Fix unowned directories (#233787)

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 0.2.6-1
- Upgrade to 0.2.6

* Thu Nov 16 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.5.8-0.2.rc2
- Add startup-notification-devel and dbus-glib-devel to BuildRequires

* Fri Nov 10 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.5.8-0.1.rc2
- Update to 0.2.5.8rc2

* Thu Oct  5 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.5.6-0.4.rc1
- Added gtk-update-icon-cache to post/postun

* Wed Oct  4 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.5.6-0.3.rc1
- Bump release for devel checkin

* Thu Sep  7 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.5.6-0.2.rc1
- Bump release for xfce rc repo

* Sun Sep  3 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.5.6-0.1.rc1
- Upgrade to 0.2.5.6-0.1.rc1

* Sun Aug 13 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.5.4-0.2.beta2
- Bump release for 4.4 beta repo

* Wed Aug  2 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.5.4-0.1.beta2
- Fix release

* Wed Jul 12 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.5.4-0.beta2
- Update to 0.2.5.4-0.beta2

* Fri Jun 23 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.5.1-0.beta1.fc6
- Update to 0.2.5.1-0.beta1

* Thu Feb 16 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.4-6.fc5
- Rebuild for fc5

* Wed Aug 17 2005 Kevin Fenzi <kevin@tummy.com> - 0.2.4-5.fc5
- Rebuild for new libcairo and libpixman

* Thu Aug  4 2005 Kevin Fenzi <kevin@tummy.com> - 0.2.4-4.fc5
- Add dist tag

* Mon May 30 2005 Kevin Fenzi <kevin@tummy.com> - 0.2.4-3
- Removed incorrect Requires
- Changed the description text

* Fri May 27 2005 Kevin Fenzi <kevin@tummy.com> - 0.2.4-2
- Fix group to be User Interface/X

* Sat Mar 19 2005 Kevin Fenzi <kevin@tummy.com> - 0.2.4-1
- Upgraded to 0.2.4 version
- Added Terminal/apps desktops files. 

* Tue Mar  8 2005 Kevin Fenzi <kevin@tummy.com> - 0.2.2-2
- Fixed to use %%find_lang
- Removed generic INSTALL from %%doc
- Change description wording: "makes it" to "make it"
- Fixed to include terminal.css 

* Sun Mar  6 2005 Kevin Fenzi <kevin@tummy.com> - 0.2.2-1
- Inital Fedora Extras version
