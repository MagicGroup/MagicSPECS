Name:		xdg-user-dirs-gtk
Version:	0.10
Release:	4%{?dist}
Summary:	Gnome integration of special directories

Group:		User Interface/Desktops
License:	GPL+
URL:		http://freedesktop.org/wiki/Software/xdg-user-dirs
Source0:	http://download.gnome.org/sources/xdg-user-dirs-gtk/%{version}/%{name}-%{version}.tar.xz

# upstream fix
Patch0: 0001-Make-the-Don-t-ask-again-checkbox-work-properly.patch

Patch1: show-in-mate.patch
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gtk3-devel
BuildRequires:	intltool
BuildRequires:	xdg-user-dirs

Requires:	xdg-user-dirs

%description
Contains some integration of xdg-user-dirs with the gnome
desktop, including creating default bookmarks and detecting
locale changes.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %name

desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/user-dirs-update-gtk.desktop


%files -f %{name}.lang
%doc NEWS AUTHORS README ChangeLog COPYING
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/xdg/autostart/user-dirs-update-gtk.desktop


%changelog
* Mon Jan 27 2014 Matthias Clasen <mclasen@redhat.com> - 0.10-4
- Add Mate to OnlyShowIn

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Matthias Clasen <mclasen@redhat.com> - 0.10-2
- Make 'Don't ask again' checkbox work properly (#968955)

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 0.10-1
- Update to 0.10

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 11 2012 Kalev Lember <kalevlember@gmail.com> - 0.9-1
- Update to 0.9
- Adjust BuildRequires to build with gtk3
- Drop lxde patch, merged upstream
- Validate the desktop file

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Adam Jackson <ajax@redhat.com> 0.8-7
- Rebuild to break bogus libpng dep

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 13 2010 Matthias Clasen <mclasen@redhat.com>
- Work in LXDE too (#563827)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep  8 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.8-2
- Require intltool

* Fri Sep  5 2008 Matthias Clasen  <mclasen@redhat.com> - 0.8-1
- Update to 0.8
 
* Tue Aug 12 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.7-2
- Fix license tag.

* Tue Feb 12 2008 Alexander Larsson <alexl@redhat.com> - 0.7-1
- Update to 0.7
- Uncomment missing patches

* Sun Nov  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.6-4
- Correct the URL

* Mon Oct  1 2007 Matthias Clasen <mclasen@redhat.com> - 0.6-2
- Fix the special case for en_US  (#307881)

* Tue Aug 21 2007 Alexander Larsson <alexl@redhat.com> - 0.6-1
- Update to 0.6 (new translations)

* Fri Jul  6 2007  Matthias Clasen  <mclasen@redhat.com> - 0.5-2
- Make the autostart file work in KDE (#247304)

* Wed Apr 25 2007  <alexl@redhat.com> - 0.5-1
- Update to 0.5
- Fixes silly dialog when no translations (#237384)

* Wed Apr 11 2007 Alexander Larsson <alexl@redhat.com> - 0.4-1
- update to 0.4 (#234512)

* Tue Mar  6 2007 Alexander Larsson <alexl@redhat.com> - 0.3-1
- update to 0.3
- Add xdg-user-dirs buildreq

* Fri Mar  2 2007 Alexander Larsson <alexl@redhat.com> - 0.2-1
- Update to 0.2

* Fri Mar  2 2007 Alexander Larsson <alexl@redhat.com> - 0.1-2
- Add buildrequires
- Mark autostart file as config

* Wed Feb 28 2007 Alexander Larsson <alexl@redhat.com> - 0.1-1
- Initial version

