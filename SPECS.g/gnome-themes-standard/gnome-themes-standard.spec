%global gtk2_version 2.24.15
%global gtk3_version 3.6.2

Name: gnome-themes-standard
Version: 3.8.1
Release: 1%{?dist}
Summary: Standard themes for GNOME applications

Group: User Interface/Desktops
License: LGPLv2+
URL: http://git.gnome.org/browse/gnome-themes-standard
Source0: http://download.gnome.org/sources/%{name}/3.8/%{name}-%{version}.tar.xz
Source1: settings.ini
Source2: gtkrc

Obsoletes: fedora-gnome-theme <= 15.0-1.fc15
Provides: fedora-gnome-theme = 1:%{version}-%{release}

Obsoletes: gnome-background-standard < 3.0.0-2
Provides: gnome-background-standard = %{version}-%{release}

BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: librsvg2-devel
BuildRequires: intltool gettext autoconf automake libtool
# for gtk-update-icon-cache
BuildRequires: gtk2
Requires: gnome-icon-theme
Requires: abattis-cantarell-fonts
Requires: adwaita-cursor-theme = %{version}-%{release}
Requires: adwaita-gtk2-theme = %{version}-%{release}
Requires: adwaita-gtk3-theme = %{version}-%{release}

%description
The gnome-themes-standard package contains the standard theme for the GNOME
desktop, which provides default appearance for cursors, desktop background,
window borders and GTK+ applications.

%package -n adwaita-cursor-theme
Summary: Adwaita cursor theme
Group: User Interface/Desktops
BuildArch: noarch

%description -n adwaita-cursor-theme
The adwaita-cursor-theme package contains a modern set of cursors originally
designed for the GNOME desktop.

%package -n adwaita-gtk2-theme
Summary: Adwaita gtk2 theme
Group: User Interface/Desktops
Requires: gtk2%{_isa} >= %{gtk2_version}

%description -n adwaita-gtk2-theme
The adwaita-gtk2-theme package contains a gtk2 theme for presenting widgets
with a GNOME look and feel.

%package -n adwaita-gtk3-theme
Summary: Adwaita gtk3 theme
Group: User Interface/Desktops
Requires: gtk3%{_isa} >= %{gtk3_version}

%description -n adwaita-gtk3-theme
The adwaita-gtk3-theme package contains a gtk3 theme for rendering widgets
with a GNOME look and feel.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

for t in HighContrast; do
  rm -f $RPM_BUILD_ROOT%{_datadir}/icons/$t/icon-theme.cache
  touch $RPM_BUILD_ROOT%{_datadir}/icons/$t/icon-theme.cache
done

rm $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/3.0.0/theming-engines/libadwaita.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/2.10.0/engines/libadwaita.la

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-3.0
cp $RPM_SOURCE_DIR/settings.ini $RPM_BUILD_ROOT%{_sysconfdir}/gtk-3.0/settings.ini
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0
cp $RPM_SOURCE_DIR/gtkrc $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/gtkrc

%post
for t in HighContrast; do
  touch --no-create %{_datadir}/icons/$t &>/dev/null || :
done

%posttrans
for t in HighContrast; do
  gtk-update-icon-cache %{_datadir}/icons/$t &>/dev/null || :
done

%files
%doc COPYING NEWS

# Background and WM
%{_datadir}/themes/Adwaita
%exclude %{_datadir}/themes/Adwaita/gtk-2.0
%exclude %{_datadir}/themes/Adwaita/gtk-3.0

# Background
%{_datadir}/gnome-background-properties/*

# A11y themes
%ghost %{_datadir}/icons/HighContrast/icon-theme.cache
%{_datadir}/icons/HighContrast
%{_datadir}/themes/HighContrast

%files -n adwaita-cursor-theme
# Cursors
%{_datadir}/icons/Adwaita

%files -n adwaita-gtk2-theme
# gtk2 Theme and engine
%{_libdir}/gtk-2.0/2.10.0/engines/libadwaita.so
%{_datadir}/themes/Adwaita/gtk-2.0
# Default gtk2 settings
%{_sysconfdir}/gtk-2.0/gtkrc

%files -n adwaita-gtk3-theme
# gtk3 Theme and engine
%{_libdir}/gtk-3.0/3.0.0/theming-engines/libadwaita.so
%{_datadir}/themes/Adwaita/gtk-3.0
# Default gtk3 settings
%{_sysconfdir}/gtk-3.0/settings.ini


%changelog
* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Wed Mar  6 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Sun Feb 24 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.90-2
- Specify required gtk2 and gtk3 versions

* Wed Feb 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Wed Feb 13 2013 Cosimo Cecchi <cosimoc@redhat.com> - 3.7.6-1
- Update to 3.7.6

* Thu Feb 07 2013 Richard Hughes <rhughes@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.4-1
- Update to 3.7.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.3-1
- Update to 3.7.3

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Tue Nov 13 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.2-1
- Update to 3.6.2

* Mon Oct 15 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.6.1-1
- Update to 3.6.1

* Tue Oct  2 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0.2-2
- Drop gtk2-engines dependency

* Tue Sep 25 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.6.0.2-1
- Update to 3.6.0.2

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 3.5.92-1
- Update to 3.5.92

* Tue Sep 04 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.5.91-1
- Update to 3.5.91

* Tue Aug 21 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.5.90.1-1
- Update to 3.5.90.1

* Fri Aug 10 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Fri May 11 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.1-2
- Fix handling of icon caches to be the same as elsewhere

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Mon Apr 16 2012 Richard Hughes <hughsient@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Mon Mar 26 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.4.0-1
- Update to 3.4.0

* Mon Mar 20 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.3.92-1
- Update to 3.3.92

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.91-1
- Update to 3.3.91

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.90.1-1
- Update to 3.3.90.1

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5.1-1
- Update to 3.3.5.1

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Tue Nov 22 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 3.2.0.2-1
- Update to 3.2.0.2

* Tue Sep 27 2011 Cosimo Cecchi <cosimoc@redhat.com> - 3.2.0.1-1
- Update to 3.2.0.1

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Sep 19 2011 Cosimo Cecchi <cosimoc@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> 3.1.91-1
- Update to 3.1.91

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> 3.1.90-1
- Update to 3.1.90
- Make more subpackage deps archful

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> 3.1.5-1
- Update to 3.1.5

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> 3.1.4-2
- Make the gtk2-engines dep arch-specific

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> 3.1.4-1
- Update to 3.1.4

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Tue Jun 14 2011 Cosimo Cecchi <cosimoc@redhat.com> - 3.1.2.1-1
- Update to 3.1.2.1

* Wed May 11 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Mon Apr 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Apr 18 2011 Adam Williamson <awilliam@redhat.com> - 3.0.0-4
- fix up the obsolete (thanks kk)

* Fri Apr 15 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-3
- ...and do the provides/obsoletes dance too.

* Thu Apr 14 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-2
- Drop gnome-themes-standard, apparently we loose the
  provides roulette again (#696832)

* Mon Apr 04 2011 Cosimo Cecchi <cosimoc@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Mon Mar 28 2011 Cosimo Cecchi <cosimoc@redhat.com> 2.91.93-3
- Don't make the cursor theme require gnome-themes-standard

* Mon Mar 28 2011 Cosimo Cecchi <cosimoc@redhat.com> 2.91.93-2
- Rebuild

* Mon Mar 28 2011 Cosimo Cecchi <cosimoc@redhat.com> 2.91.93-1
- Update to 2.91.93
- Make the cursor theme noarch
- Ship the default settings together with the relevant theme

* Mon Mar 28 2011 Ray Strode <rstrode@redhat.com> 2.91.92.1-4
- Fix Obsoletes

* Sat Mar 26 2011 Matthias Clasen <mclasen@redhat.com> 2.91.92.1-3
- Don't specify a nonexisting icon theme in settings.ini

* Thu Mar 24 2011 Matthias Clasen <mclasen@redhat.com> 2.91.92.1-2
- Add a subpackage for the default background

* Mon Mar 21 2011 Cosimo Cecchi <cosimoc@redhat.com> 2.91.92.1-1
- Update to 2.91.92.1

* Mon Mar 21 2011 Cosimo Cecchi <cosimoc@redhat.com> 2.91.92-1
- Update to 2.91.92

* Mon Mar 14 2011 Matthias Clasen <mclasen@redhat.com> 2.91.91.1-1
- Update to 2.91.91.1

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> 2.91.91-1
- Update to 2.91.91

* Fri Mar 04 2011 Ray Strode <rstrode@redhat.com> 2.91.90-6
- Put COPYING and NEWS in correct place

* Fri Mar 04 2011 Ray Strode <rstrode@redhat.com> 2.91.90-5
- Drop icon-theme subpackage, it's empty

* Fri Mar 04 2011 Ray Strode <rstrode@redhat.com> 2.91.90-4
- Split out gtk themes into a subpackage as well
  Resolves: #675509

* Fri Mar 04 2011 Ray Strode <rstrode@redhat.com> 2.91.90-3
- Split cursors out into a subpackage
  Resolves: #675509

* Tue Feb 22 2011 Cosimo Cecchi <cosimoc@redha.com> - 2.91.90-2
- Fix insensitive checkboxes

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> 2.91.90-1
- Update to 2.91.90

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.8-7
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  8 2011 Cosimo Cecchi <cosimoc@redhat.com> 2.91.8-4
- Pull in abattis-cantarell-fonts

* Fri Feb 04 2011 Ray Strode <rstrode@redhat.com> 2.91.8-3
- add gtkrc file for gtk2 apps
- take over fedora-gnome-theme's role

* Fri Feb  4 2011 Cosimo Cecchi <cosimoc@redhat.com> 2.91.8-2
- Add a patch from upstream for active toggle buttons

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.8-1
- Update to 2.91.8
- Add default settings for session-less situations

* Sun Jan 23 2011 Matthias Clasen <mclasen@redhat.com> 2.91.7-1
- Update to 2.91.7

* Wed Jan 19 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-1
- Update to 2.91.6

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-1
- Update to 2.91.5

* Mon Nov 22 2010 Matthias Clasen <mclasen@redhat.com> 2.91.2.1-7
- Require gtk-theme-engine-clearlooks

* Tue Nov 16 2010 Matthias Clasen <mclasen@redhat.com> 2.91.2.1-6
- Obsoleting gnome-themes seems unnecessarily harsh

* Mon Nov 15 2010 Cosimo Cecchi <ccecchi@redhat.com> 2.91.2.1-5
- Add "Provides:" so that packages depending on gnome-themes don't break

* Mon Nov 15 2010 Cosimo Cecchi <ccecchi@redhat.com> 2.91.2.1-4
- Make this package obsolete gnome-themes

* Fri Nov 12 2010 Cosimo Cecchi <ccecchi@redhat.com> 2.91.2.1-3
- Make sure the theme directory is owned by the package too.
- Cleaned up the spec file a bit more to silence some rpmlint
  warnings.

* Fri Nov 12 2010 Cosimo Cecchi <ccecchi@redhat.com> 2.91.2.1-2
- Cleaned up the spec file, removed the %%clean section, and fixed a typo
  in the description.

* Fri Nov 12 2010 Cosimo Cecchi <ccecchi@redhat.com> 2.91.2.1-1
- First packaging of gnome-themes-standard
