## Minimum required versions.
%global	gtk3_min_version	3.9.4
%global	glib2_min_version	2.37.6
%global	tp_mc_min_version	5.12.0
%global	tp_glib_min_version	0.19.9
%global	enchant_version		1.2.0
%global network_manager_version 0.7.0
%global libcanberra_version	0.4
%global webkit_version		1.3.13
%global goa_version		3.5.1
%global libnotify_version	0.7.0
%global libchamplain_version	0.12.1
%global folks_version		0.9.5
%global gstreamer_version	0.10.32
%global libsecret_version	0.5
%global gcr_version		2.91.4

Name:		empathy
Version:	3.11.90
Release:	2%{?dist}
Summary:	Instant Messaging Client for GNOME

License:	GPLv2+
URL:		http://live.gnome.org/Empathy

Source0:	http://download.gnome.org/sources/%{name}/3.11/%{name}-%{version}.tar.xz
Source1:	%{name}-README.ConnectionManagers

BuildRequires:	enchant-devel >= %{enchant_version}
BuildRequires:	iso-codes-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	glib2-devel >= %{glib2_min_version}
BuildRequires:	libcanberra-devel >= %{libcanberra_version}
BuildRequires:	webkitgtk3-devel >= %{webkit_version}
BuildRequires:	gtk3-devel >= %{gtk3_min_version}
BuildRequires:	intltool
BuildRequires:	libxml2-devel
BuildRequires:	scrollkeeper
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	telepathy-glib-devel >= %{tp_glib_min_version}
BuildRequires:	telepathy-farstream-devel >= 0.2.1
BuildRequires:	libnotify-devel >= %{libnotify_version}
BuildRequires:	NetworkManager-glib-devel >= %{network_manager_version}
BuildRequires:	libchamplain-gtk-devel >= %{libchamplain_version}
BuildRequires:	clutter-gtk-devel >= 1.1.2
BuildRequires:	geoclue2-devel
BuildRequires:	geocode-glib-devel
BuildRequires:	telepathy-logger-devel >= 0.8.0
BuildRequires:	folks-devel >= 1:%{folks_version}
BuildRequires:	clutter-gst2-devel
BuildRequires:	gstreamer1-devel >= %{gstreamer_version}
BuildRequires:	cogl-devel
BuildRequires:	cheese-libs-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	libgudev1-devel
BuildRequires:	telepathy-mission-control-devel
BuildRequires:	gnome-online-accounts-devel >= %{goa_version}
BuildRequires:	libsecret-devel >= %{libsecret_version}
BuildRequires:	gcr-devel >= %{gcr_version}
BuildRequires:	pkgconfig(gee-0.8)
BuildRequires:	itstool
# hack to conserve space on the live cd
BuildRequires:	/usr/bin/convert

Requires:	telepathy-filesystem
Requires:	telepathy-mission-control >= %{tp_mc_min_version}
## We install the following connection managers by default.
Requires:	telepathy-gabble >= 0.16.0
Requires:	telepathy-salut >= 0.8.0
Requires:	telepathy-idle
Requires:	telepathy-haze >= 0.6.0

Requires(post): /usr/bin/gtk-update-icon-cache
Requires(postun): /usr/bin/gtk-update-icon-cache


%description
Empathy is powerful multi-protocol instant messaging client which
supports Jabber, GTalk, MSN, IRC, Salut, and other protocols.
It is built on top of the Telepathy framework.


%prep
%setup -q
# force this to be regenerated
rm data/empathy.desktop


%build
## GCC complains about some unused functions, so we forcibly show those as
## simple warnings instead of build-halting errors.
%configure --disable-static --enable-ubuntu-online-accounts=no
# Parallel builds are broken.
make
install -m 0644 %{SOURCE1} ./README.ConnectionManagers


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang %{name} --with-gnome
%find_lang empathy-tpaw

desktop-file-install --delete-original			\
	--dir %{buildroot}%{_datadir}/applications	\
	%{buildroot}%{_datadir}/applications/%{name}.desktop

# hack to conserve space on the live image
for f in video_overview.png conf_overview.png croom_overview.png; do
  convert %{buildroot}%{_datadir}/help/C/empathy/figures/$f -resize 150x150 $f
  mv $f %{buildroot}%{_datadir}/help/C/empathy/figures
done


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/sbin/ldconfig


%postun
if [ $1 -eq 0 ]; then
   touch --no-create %{_datadir}/icons/hicolor &>/dev/null
   gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
   glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
/sbin/ldconfig


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang -f empathy-tpaw.lang
%doc AUTHORS COPYING README README.ConnectionManagers NEWS
%doc COPYING-DOCS COPYING.LGPL COPYING.SHARE-ALIKE
%{_bindir}/%{name}
%{_bindir}/%{name}-accounts
%{_bindir}/%{name}-debugger
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libempathy-%{version}.so
%{_libdir}/%{name}/libempathy-gtk-%{version}.so
%{_libdir}/%{name}/libempathy-gtk.so
%{_libdir}/%{name}/libempathy.so
%{_libdir}/mission-control-plugins.0/mcp-account-manager-goa.so
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/empathy/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Empathy.Call.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Empathy.Chat.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Empathy.Auth.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Empathy.FileTransfer.service
%{_datadir}/GConf/gsettings/empathy.convert
%{_datadir}/glib-2.0/schemas/org.gnome.Empathy.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.telepathy-account-widgets.gschema.xml
%{_datadir}/telepathy/clients/Empathy.Call.client
%{_datadir}/telepathy/clients/Empathy.Chat.client
%{_datadir}/telepathy/clients/Empathy.Auth.client
%{_datadir}/telepathy/clients/Empathy.FileTransfer.client
%{_mandir}/man1/empathy*.1.gz
%{_libexecdir}/empathy-auth-client
%{_libexecdir}/empathy-call
%{_libexecdir}/empathy-chat
%dir %{_datadir}/adium
%dir %{_datadir}/adium/message-styles
%dir %{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle
%dir %{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents
%dir %{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Info.plist
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources/Incoming/Content.html
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources/Incoming/NextContent.html
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources/Status.html
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources/Variants/Blue.css
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources/Variants/Clean.css
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources/Variants/Simple.css
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources/main.css
%dir %{_datadir}/adium/message-styles/Classic.AdiumMessageStyle
%dir %{_datadir}/adium/message-styles/Classic.AdiumMessageStyle/Contents
%dir %{_datadir}/adium/message-styles/Classic.AdiumMessageStyle/Contents/Resources
%{_datadir}/adium/message-styles/Classic.AdiumMessageStyle/Contents/Info.plist
%{_datadir}/adium/message-styles/Classic.AdiumMessageStyle/Contents/Resources/Content.html
%{_datadir}/adium/message-styles/Classic.AdiumMessageStyle/Contents/Resources/Status.html
%{_datadir}/adium/message-styles/Classic.AdiumMessageStyle/Contents/Resources/main.css
%dir %{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle
%dir %{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents
%dir %{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Info.plist
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/Images/corners.png
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/Images/horizontal.png
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/Images/nipple.png
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/Images/vertical.png
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/Incoming/Content.html
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/Incoming/NextContent.html
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/Status.html
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/main.css

%changelog
* Thu Feb 20 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.90-2
- Rebuilt for cogl soname bump

* Mon Feb 17 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Mon Feb 10 2014 Peter Hutterer <peter.hutterer@redhat.com> - 3.11.5-3
- Rebuild for libevdev soname bump

* Wed Feb 05 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.5-2
- Rebuilt for cogl soname bump

* Mon Feb 03 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Mon Jan 20 2014 Brian Pepple <bpepple@fedoraproject.org> - 3.11.4-1
- Update to 3.11.4.

* Thu Dec 19 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.11.3-1
- Update to 3.11.3.
- Drop empathy_ensure_individual_from_tp_contact() patch. Fixed upstream.

* Mon Nov 25 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.11.1-2
- Pull upstream patch to use empathy_ensure_individual_from_tp_contact().

* Thu Oct 31 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.11.1-1
- Update to 3.11.1.
- Add appdata to file list.

* Mon Oct 14 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.10.1-1
- Update to 3.10.1.

* Tue Sep 24 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.10.0-1
- Update to 3.10.0.

* Mon Sep 16 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.9.92-1
- Update to 3.9.92.
- Bump minimum version of gtk3 and folks needed.

* Wed Sep 04 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-2
- Enable geolocation

* Tue Sep  3 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.9.91-1
- Update to 3.9.91
- Bump minimum version of glib2 needed.

* Tue Aug 20 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.9.90-1
- Update to 3.9.90.
- Package telepathy account widget translations and schemas.

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.4-3
- Rebuilt for cogl 1.15.4 soname bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul  9 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.9.4-1
- Update to 3.9.4.

* Mon Jun 17 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.9.3-1
- Update to 3.9.3.

* Thu May 30 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.9.2-1
- Update to 3.9.2.

* Tue May 14 2013 Matthias Clasen <mclasen@redhat.com> - 3.9.1-2
- Save some space by shrinking figures

* Fri May  3 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.9.1-1
- Update to 3.9.1.

* Mon Apr 15 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.8.1-1
- Update to 3.8.1.

* Mon Mar 25 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.8.0-1
- Update to 3.8.0.
- Remove nautilus extension, since nautilus-sendto has removed this functionality.

* Wed Mar 20 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.7.92-2
- Bump minimum verson of folks and add dep on cogl.

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Mon Mar  4 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.7.91-1
- Update to 3.7.91.

* Thu Feb 21 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.7.90-2
- Drop vender from desktop file.
- Add BR on libgee-0.8.

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.5-2
- Rebuilt for libgcr soname bump

* Tue Feb  5 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.7.5-1
- Update to 3.7.5.
- Bump minimum version of tp-logger needed.

* Fri Jan 25 2013 Brian Pepple <bpepple@fedoraproject.org> - 3.7.4-2
- Rebuild for new libcogl.

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Tue Dec 18 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.7.3-1
- Update to 3.7.3.

* Tue Nov 27 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.7.2-1
- Update to 3.7.2

* Wed Nov 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.6.2-1
- Update to 3.6.2
- Drop patches. Fixed upstream.

* Mon Nov 12 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.6.1-4
- Fix GNOME #687762

* Wed Nov  7 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.6.1-3
- Fix GNOME #652546 and #687690

* Wed Oct 31 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.6.1-3
- Rebuild against latest telepathy-logger

* Thu Oct 18 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.6.1-2
- Fix GNOME #686311 and #686314

* Mon Oct 15 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.6.1-1
- Update to 3.6.1

* Mon Oct  8 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.6.0.3-1
- Update to 3.6.0.3.

* Thu Oct  4 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.6.0.1-2
- Build with gstreamer-1.0 support.

* Wed Oct  3 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.6.0.1-1
- Update to 3.6.0.1

* Wed Sep 26 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.6.0-2
- Rebuild against new tp-glib

* Tue Sep 25 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.6.0-1
- Update to 3.6.0.

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.92-2
- Rebuilt for new libcheese-gtk

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 3.5.92-1
- Update to 3.5.92

* Fri Sep  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.5.91.1-1
- Update to 3.5.91.1.

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Thu Aug 30 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.90-3
- Do not remove the rpaths. They are needed to pick up the private libraries.
  (RH #846908)

* Tue Aug 28 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.90-2
- Rebuild against new cogl/clutter

* Wed Aug 22 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.5.90-1
- Update to 3.5.90.
- Remove bits for accounts desktop file. No longer shipped.

* Sun Aug 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.5.5-2
- Rebuild for new libcogl.

* Mon Aug  6 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.5.5-1
- Update to 3.5.5.
- Bump minimum version of tp-glib.
- Add BR on libsecret-devel

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 24 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.5.4.1-1
- Update to 3.5.4.1.
- Bump minimum version of tp-glib needed.

* Mon Jul 16 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.5.4-1
- Update to 3.5.4.
- Bump minimum versions of tp-glib and glib2 needed.

* Tue Jun 26 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.5.3-2
- Bump minimum version of tp-glib and folks.
- Drop BR on eds-devel.

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Tue Jun  5 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.5.2-1
- Update to 3.5.2.
- Bump minimum version of gtk3, tp-glib, goa, and clutter-gtk.

* Mon Apr 30 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.5.1-1
- Update to 3.5.1.
- Update source url.

* Mon Apr 16 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.4.1-1
- Update to 3.4.1.
- Update source url.

* Fri Apr  6 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.4.0.2-1
- Update to 3.4.0.2.

* Thu Apr 05 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.4.0.1-2
- Rebuild against tp-farstream

* Thu Apr  5 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.4.0.1-1
- Update to 3.4.0.1.

* Thu Apr 05 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.4.0-3
- Rebuild against new tp-farstream

* Tue Apr 03 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.4.0-2
- Rebuild against new tp-glib.

* Mon Mar 26 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.4.0-1
- Update to 3.4.0.

* Tue Mar 20 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.3.92-1
- Update to 3.3.92.

* Wed Mar 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.3.91-3
- Rebuild for cogl

* Wed Mar 07 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.3.91-2
- Rebuild for cogl

* Tue Mar  6 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.3.91-1
- Update to 3.3.91.
- Remove en_GB and zh_CN help files until they can be properly handled.

* Mon Mar  5 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.3.90.2-1
- Update to 3.3.90.2.
- Add BR on telepathy-farstream-devel, gstreamer-devel and itstool.
- Drop BR on tp-farsight.
- Bump minimum version of tp-glib.
- Drop requires on tp-butterfly. MSN will use tp-gabble from now on.

* Tue Feb 7 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.3.5-1
- Update to 3.3.5.

* Mon Feb 6 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.3.4-3
- Rebuild against new eds.

* Thu Jan 19 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-2
- Rebuild against new cogl

* Mon Jan 16 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.3.4-1
- Update to 3.3.4.
- Add BR on gcr and remove old BR on gnome-keyring.

* Mon Jan 09 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.3.3-3
- Rebuild for new gcc.

* Mon Dec 19 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.3.3-2
- Build with call logging support.

* Mon Dec 19 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.3.3-1
- Update to 3.3.3.
- Bump minimum version of tp-glib, goa, glib2, and folks.

* Sun Nov 27 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 3.3.2-3
- Fix build by commenting out GOA integration until GOA 3.3.x is released

* Thu Nov 24 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-2
- Rebuild against new clutter

* Thu Nov 24 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.3.2-1
- Update to 3.3.2.
- Bump minimum version of tp-glib needed.
- Add minimum version of GOA needed.

* Tue Nov 22 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.3.1-4
- Rebuild against new eds

* Wed Nov 02 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.3.1-3
- Rebuld against tp-logger.

* Tue Nov  1 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 3.3.1-2
- Rebuild for new telepathy-logger

* Mon Oct 24 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1.

* Tue Oct 18 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.2.1-3
- Rebuld against folks yet again.

* Tue Oct 18 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.2.1-2
- Rebuld against new folks.

* Mon Oct 17 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1.
- Bump minimum version of tp-glib needed.

* Mon Oct 10 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.2.0.1-1
- Update to 3.2.0.1

* Mon Sep 26 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0.

* Wed Sep 21 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.1.92-2
- Rebuld for new libcogl.

* Mon Sep 19 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.1.92-1
- Update to 3.1.92.

* Tue Sep 06 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.1.91-2
- Rebuld against gcr.

* Tue Sep  6 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.1.91-1
- Update to 3.1.91.
- Add BR on tp-mission-control-devel and  gnome-online-accounts-devel.

* Wed Aug 31 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.90.1-2
- Rebuilt for libgcr soname bump

* Wed Aug 31 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.1.90.1-1
- Update to 3.1.90.1.

* Mon Aug 29 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.1.90-1
- Update to 3.1.90.

* Mon Aug 29 2011 Milan Crha <mcrha@redhat.com> - 3.1.5.1-3
- Rebuild against newer evolution-data-server

* Mon Aug 22 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.1.5.1-1
- Update to 3.1.5.1.
- Add BR on libgudev1-devel.
- Bump min requires for tp-glib & webkitgtk.

* Fri Aug 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.5-3
- Rebuild

* Tue Aug 16 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.1.5-1
- Update to 3.1.5.
- Bump min version of folks needed.
- Add BR on pulseaudio-libs-devel.

* Fri Jul 29 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.1.4-2
- Rebuild.

* Wed Jul 27 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.3-4
- Try again

* Sun Jul 24 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.1.3-3
- Rebuild for new eds

* Tue Jul 05 2011 Adam Williamson <awilliam@redhat.com> - 3.1.3-2
- rebuild for new e-d-s

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Fri Jun 24 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.1.2.1-2
- Enable call support.

* Tue Jun 14 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.1.2.1-1
- Update to 3.1.2.1.
- Bump minimum version of tp-logger.
- Use xz tarball.

* Fri Jun 10 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.1.2-1
- Update to 3.1.2.
- Add BR on gstreamer-devel and cheese-libs-devel.
- Bump min required versions of folks, tp-logger, and tp-glib.

* Mon May  9 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1.
- Enable maps again.
- Drop obsoletes/provides. They should no longer be needed.
- Bump minimum version of tp-glib.

* Fri May 06 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.0.1-4
- Rebuild for new tp-logger

* Thu May  5 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.0.1-3
- Update icon cache scriptlets. sigh....

* Tue May  3 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.0.1-2
- Update gsetting scriplets.

* Mon Apr 25 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.0.1-1
- Update to 3.0.1.

* Mon Apr  4 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0.
- Update source url.

* Mon Mar 28 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.93-2
- Rebuild for new tp-logger.

* Mon Mar 28 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.93-1
- Update to 2.91.93.
- Bump minimum tp-glib version.

* Thu Mar 24 2011 Dan Williams <dcbw@redhat.com> 2.91.92-2
- Rebuild for NM 0.9

* Wed Mar 23 2011 Ray Strode <rstrode@redhat.com> 2.91.92-1
- Update to 2.91.92
- Disable libchamplain support for now at the request of bpepple.

* Tue Mar 22 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.91.1-2
- Enable libchamplain support.

* Thu Mar 17 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.91.1-1
- Update to 2.91.91.1.
- Bump min version of folks needed.

* Thu Mar 10 2011 Dan Williams <dcbw@redhat.com> - 2.91.90.2-2
- Update for NetworkManager 0.9

* Tue Mar  8 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.91-1
- Update to 2.91.91.
- Update minimum version of tp-glib & gtk3.

* Sat Feb 26 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.90.2-1
- Update to 2.91.90.2.

* Fri Feb 25 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.90.1-1
- Update to 2.91.90.1.

* Mon Feb 21 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.90-1
- Update to 2.91.90.
- Bump min version for folks and tp-glib.

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-5
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.6.1-3
- Enable single window control center.

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6.1-2
- Rebuild against new gtk

* Tue Feb  1 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.6.1-1
- Update to 2.91.6.1.
- Update min req for folks and tp-glib.

* Thu Jan 27 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.5.1-2
- Rebuild for new farsight2

* Tue Jan 18 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.5.1-1
- Update to 2.91.5.1.

* Mon Jan 10 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.5-1
- Update to 2.91.5.

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4.3-1
- Update to 2.91.4.3

* Tue Dec 14 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.91.3.1-2
- Enable webkit support for Adium themes.

* Tue Dec 14 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.91.3.1-1
- Update to 2.91.3.1.
- Bump min versions for tp-glib & folks.

* Fri Dec  3 2010 Christopher Aillon <caillon@redhat.com> - 2.91.3-2
- Rebuild against newer gtk3

* Mon Nov 29 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.91.3-1
- Update to 2.91.3.
- Drop folks api patch. Fixed upstream.
- Add BR on gsettings-desktop-schemas-devel.
- Drop ca-cert patch. Fixed upstream.
- Drop BR on GConf2.

* Tue Nov 16 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.91.2-2
- Bump min versions for gtk3, glib2, tp-glib, and folks.
- Add patch to use Fedora's ca-cert.
- Drop BR on unique3. No longer needed.

* Mon Nov 15 2010 Bastien Nocera <bnocera@redhat.com> 2.91.2-1
- Update to 2.91.2

* Mon Nov 15 2010 Bastien Nocera <bnocera@redhat.com> 2.91.0-6
- Rebuild against new folks

* Wed Nov 10 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.91.0-5
- Backport libnotify patch for 0.7 api change.
- Bump min BR version for libnotify.
- Add patches to port to GtkComboBox & GtkComboBoxText.

* Sat Oct 30 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.91.0-4
- Rebuild for folks-2.1.

* Thu Oct 21 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.91.0-3
- Rebuild for new folks.

* Tue Oct 19 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.91.0-2
- Rebuild for new eds.
- Disable webkitgtk support for now until a more recent version is in rawhide.
- Add patch to fix build with gcr.

* Mon Oct  4 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.91.0-1
- Update to 2.91.0.
- Drop obsolete/provides on tp-haze-mission-control.
- Drop keyname-fixes patch. Fixed upstream.
- Drop empathy chat GDKKEY patch. Fixed upstream.
- Drop avatar image gdkdisplay patch. Fixed upstream.
- Drop depreciated gtk-dialog-separator patch. Fixed upstream.

* Mon Sep 27 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.32.0-1
- Update to 2.32.0.

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.92-2
- Rebuild

* Tue Sep 14 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.31.92-1
- Update to 2.31.92.
- Clean up gconf->gsetting conversion.

* Thu Sep  2 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.31.91.1-1
- Update to 2.31.91.1.

* Thu Aug 26 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.31.90-1
- Update to 2.31.90.
- Add BR on folks-devel.
- Drop buildroot. No longer needed.

* Fri Jul 16 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.31.5.1-2
- Rebuild for new eds.

* Wed Jul 14 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.5.1-1
- Update to 2.31.5.1

* Fri Jul  9 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.31.4-2
- Update scriptlets for gsettings.

* Fri Jul  9 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.31.4-1
- Update to 2.31.4.
- Disable libchamplain support for now due to api change.
- Drop schemas regeneration since empathy uses gsettings now.
- Add BR on telepathy-logger-devel.

* Tue Jul  6 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.31.3-4
- Rebuild for new libchamplain.

* Sun Jul  4 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.31.3-3
- Rebuild for new webkit.

* Wed Jun 16 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-2
- Don't require scrollkeeper

* Mon Jun  7 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.31.3-1
- Update to 2.31.3.
- Bump min version of tp-glib needed.
- Drop facebook server error patch. Fixed upstream.

* Thu Jun  3 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.31.2-2
- Backport patch to fix facebook server error. (#595925)

* Fri May 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.2-1
- Update to 2.31.2
- drop presence-icon patch, handled upstream (partially)

* Mon May 10 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.31.1-1
- Update to 2.31.1.
- Bump min versions of gtk2 & tp-glib needed.

* Thu May  6 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.30.1-3
- Rebuild for new eds.

* Mon Apr 26 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.30.1-2
- Drop suffix on gconf schemas scriptlets.

* Mon Apr 26 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.30.1-1
- Update to 2.30.1.

* Sat Apr 24 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.30.0.2-2
- Remove clean section. No longer needed.
- Update spec for new gconf macros.

* Tue Apr 20 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.30.0.2-1
- Update to 2.30.0.2.

* Fri Apr  9 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.30.0.1-1
- Update to 2.30.0.1.

* Mon Mar 29 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.30.0-1
- Update to 2.30.0.

* Mon Mar 15 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.29.93-1
- Update to 2.29.93.

* Tue Mar  9 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.29.92-1
- Update to 2.29.92.

* Thu Mar  4 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.29.91.2-1
- Update to 2.29.91.2.

* Wed Mar  3 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.29.91.1-1
- Update to 2.29.91.1.
- Remove DSOLinking patch. Fixed upstream.

* Mon Feb 22 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.29.91-1
- Update to 2.29.91.

* Sat Feb 20 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.29.90-3
- Rebuild for new tp-mission-control.

* Fri Feb 19 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.29.90-2
- Add patch to fix DSOLinking. (#564975)

* Mon Feb  8 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.29.90-1
- Update to 2.29.90.

* Mon Jan 25 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.29.6-1
- Update to 2.29.6.
- Drop xmlCleanupParser patch. Fixed upstream.

* Wed Jan 13 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.29.5.1-2
- Add patch to fix crasher due to misuse of xmlCleanParser. (#532307)

* Tue Jan 12 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.29.5.1-1
- Update to 2.29.5.1.

* Mon Dec 21 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.29.4-1
- Update to 2.29.4.

* Mon Nov 30 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.29.3-1
- Update to 2.29.3.
- Drop nautilus sendto plugin linking patch. Fixed upstream.
- Drop broken NetworkManager patch.  Fixed upstream.

* Wed Nov 18 2009 Bastien Nocera <bnocera@redhat.com> 2.29.2-2
- Rebuild with nautilus-sendto plugin

* Mon Nov 16 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.29.2-1
- Update to 2.29.2.
- Remove devel, libs, and python subpackages since empathy no longer ships
  libempathy and libempathy-gtk as shared libraries.
- Remove configure options no longer available.
- Update source url.
- Drop pkgconfig patch.

* Mon Oct 26 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.28.1.1-2
- Disable panel applets, since they are unmaintained and being dropped from Empathy.

* Mon Oct 26 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.28.1.1-1
- Update to 2.28.1.1.
- See http://download.gnome.org/sources/empathy/2.28/empathy-2.28.1.1.news

* Mon Oct 26 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.1-3
- Another upstream crash fix

* Sun Oct 25 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.1-2
- Include a number of crash fixes from the stable branch

* Mon Oct 19 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.28.1-1
- Update to 2.28.1.
- Drop no-settings patch.  Fixed upstream.

* Sat Oct 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0.1-3
- Include an upstream fix for a possible crash in the accounts dialog

* Tue Oct 13 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.28.0.1-2
- Require tp-idle and tp-butterfly.

* Fri Oct  2 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.28.0.1-1
- Update to 2.28.0.1.
- See http://download.gnome.org/sources/empathy/2.28/empathy-2.28.0.1.news

* Mon Sep 21 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.28.0-1
- Update to 2.28.0.
- Drop video widget patch.  Fixed upstream.
- Update src.

* Mon Sep 14 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.27.92-2
- Back-port patch to prevent video widget from crashing.

* Tue Sep  8 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.27.92-1
- Update to 2.27.92.
- Drop desktop category patch.  Fixed upstream.
- Drop fix-nav-handling patch.  Fixed upstream.

* Tue Sep  1 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.27.91.1-6
- Add patch to workaround NetworkManager pc file name change.

* Sat Aug 29 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.27.91.1-5
- Backport patch to fix incorrect assumption about navigation-request. (#519849)

* Sat Aug 29 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91.1-4
- Rebuild against newer libnm_glib

* Wed Aug 26 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.27.91.1-3
- Sigh.. let's drop the requires on mission-control-devel in the devel sub.

* Wed Aug 26 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.27.91.1-2
- Update broken pkgconfig patch to not include libmissioncontrol.
- Drop BR on telepathy-mission-control-devel. mc is a runtime dep.

* Wed Aug 26 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.27.91.1-1
- Update to 2.27.91.1.
- Add BR on unique-devel.
- Update presence-icons patch.
- Add patch to fix invalid category in desktop file.
- Drop clutter patch.  Fixed upstream.

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.5-3
- Make presence icons show up in the menus

* Mon Aug  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.5-2
- Enable map and location features

* Wed Jul 29 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.5-1
- Update to 2.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.4-2
- Deal with some stubborn buttons

* Wed Jul 15 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.27.4-1
- Update to 2.27.4.
- See http://download.gnome.org/sources/empathy/2.27/empathy-2.27.4.news
- Drop mission-control-convert patch.
- Add BR on NetworkManager-glib-devel.

* Thu Jul  9 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.3-4
- Require telepathy-mission-control

* Thu Jul  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.3-3
- Shrink GConf schemas

* Wed Jun 17 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.27.3-2
- Drop libglade BR, it's no longer needed.

* Wed Jun 17 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.27.3-1
- Update to 2.27.3.
- See http://download.gnome.org/sources/empathy/2.27/empathy-2.27.3.news
- Add BR on webkitgtk-devel.
- Bump version of tp-glib needed.
- Update tp-mission-control-convert patch.
- TODO: Enable libchamplain & geoclue support once deps are met.

* Sat May 30 2009 Peter Gordon <peter@thecodergeek.com> - 2.27.2-1
- Update to new upstream release (2.27.2)

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/empathy/2.26/empathy-2.26.1.news

* Fri Apr  3 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.26.0.1-2
- Update pkgconfig patch to add libcanberra-gtk requires. (#493954)

* Mon Mar 30 2009 Peter Gordon <peter@thecodergeek.com> - 2.26.0.1-1
- Update to new upstream release (2.26.0.1): updated translations, fixes a
  couple of crasher bugs and usage of the UNIX socket address.

* Mon Mar 16 2009 Peter Gordon <peter@thecodergeek.com> - 2.26.0-1
- Update to new upstream release (2.26.0).

* Tue Mar 03 2009 Peter Gordon <peter@thecodergeek.com> - 2.25.92-1
- Update to new upstream release (2.25.92).
- Bump minimum required telepathy-glib version.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.25.91-1
- Update to 2.25.91

* Tue Feb 10 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.25.90-1
- Update to 2.25.90.
- Bump min version of tp-glib needed.
- Add BR on tp-farsight-devel & libnotify-devel.
- Drop Requires on tp-stream-engine.

* Tue Jan  6 2009 Brian Pepple <bpepple@fedoraproject.org> - 2.25.4-1
- Update to 2.25.4.
- Add BR on libcanberra-devel.

* Mon Dec 29 2008 Brian Pepple <bpepple@fedoraproject.org> - 2.25.3-4
- Add patch to work around our broken pkgconfig.

* Mon Dec 29 2008 Brian Pepple <bpepple@fedoraproject.org> - 2.25.3-3
- Rebuild.

* Sat Dec 20 2008 Brian Pepple <bpepple@fedoraproject.org> - 2.25.3-2
- Update mission-control-convert patch.

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.3-1
- Update to 2.25.3

* Mon Dec 01 2008 Peter Gordon <peter@thecodergeek.com> - 2.25.2-1
- Update to new upstream release (2.25.2)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.24.1-4
- Rebuild for Python 2.6

* Fri Nov 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-2
- Tweak %%description

* Thu Nov 20 2008 Peter Gordon <peter@thecodergeek.com>
- Fix Source0 URL.

* Mon Oct 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Tue Sep  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Thu Sep  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Sun Aug 24 2008 Peter Gordon <peter@thecodergeek.com> - 2.23.90-2
- Now that Empathy will be the default IM client in F10+, hardcode a dependency
  on telepathy-haze to keep the same protocol functionality across upgrades,
  for a much improved "out of the box" experience.
- Reference: bug 458935.

* Fri Aug 22 2008 Peter Gordon <peter@thecodergeek.com> - 2.23.90-1
- Update to new upstream release (2.23.90)

* Fri Aug 15 2008 Peter Gordon <peter@thecodergeek.com> - 2.23.6-3
- Apply patch from Colin Walters to automagically update profile namings for
  the switch to using Empathy's provided profiles.
- Drop the upgrade script (no longer needed since it's automatically done).
  - upgrade-haze-profiles.sh

* Wed Aug 13 2008 Peter Gordon <peter@thecodergeek.com> - 2.23.6-2
- Use upstream's AIM, ICQ, MSN-Haze, and Yahoo profiles instead of recommending
  the telepathy-haze-mission-control package. (The Haze-provided ones have grown
  horribly stale...). This makes for better automagic functionality (if Haze is
  installed, Empathy/MC will autodetect it) and tracks upstream more closely.
  + upgrade-haze-profiles.sh

* Mon Aug 04 2008 Peter Gordon <peter@thecodergeek.com> - 2.23.6-1
- Update to new upstream release (2.23.6)
- Use the in-tarball libtool scripts instead of the system copy to workaround
  'make install' errors.

* Wed Jul 16 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.23.4-1
- Update to 0.23.4.
- Update source url.

* Mon Jun  2 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.23.3-1
- Update to 0.23.3.
- Remove reference to stream-engine in connections managers readme.

* Fri May 16 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.23.2-1
- Update to 0.23.2.
- Add man pages.
- Use enchant-devel, instead of aspell-devel.

* Fri May 16 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.23.1-3
- Rebuild for new e-d-s.

* Sun May  4 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.23.1-2
- Drop multiple copies of COPYING file.
- Drop BR on gnome-vfs2-devel.
- Require telepathy-stream-engine for VOIP support.
- Add BR on iso-codes-devel, so spell-checking is enabled.

* Wed Apr 23 2008 Peter Gordon <peter@thecodergeek.com> - 0.23.1-1
- Update to new upstream release (0.23.1)
- Drop libtelepathy dependencies; upstream switched fully to telepathy-glib.

* Fri Apr 11 2008 Peter Gordon <peter@thecodergeek.com> - 0.22.1-1
- Update to new upstream release (0.22.1)

* Mon Mar 10 2008 Peter Gordon <peter@thecodergeek.com> - 0.22.0-1
- Update to new upstream release (0.22.0)

* Sun Mar 09 2008 Peter Gordon <peter@thecodergeek.com> - 0.21.91-1
- Update to new upstream release (0.21.91)

* Fri Feb 22 2008 Peter Gordon <peter@thecodergeek.com> - 0.21.90-1
- Update to new upstream release (0.21.90)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.21.4-2
- Autorebuild for GCC 4.3

* Mon Dec 17 2007 Peter Gordon <peter@thecodergeek.com> - 0.21.4-1
- Update to new upstream release (0.21.4)

* Tue Nov 13 2007 Peter Gordon <peter@thecodergeek.com> - 0.21.2-1
- Update to new upstream release (0.21.2)
- Drop backported drag-and-drop patch (fixed upstream):
    - svn380-fix-contact-DnD.patch
- Update README.ConnectionManagers: Include Haze package note, remove Galago
  note (a feed-only connection manager isn't useful for instant messaging),
  and fix some wording.

* Fri Oct 19 2007 Peter Gordon <peter@thecodergeek.com> - 0.14-5
- Backport upstream patch to fixes crashes when using drag-and-drop of a
  contact from the buddy list to the current conversation window to initiate a
  conversation:
    + svn380-fix-contact-DnD.patch 
- Resolves: GNOME bug 483168 (crash in Empathy Instant Messenger: I had
  dragged a contact ...) 

* Tue Oct 16 2007 Peter Gordon <peter@thecodergeek.com> - 0.14-4
- Depend on Salut and Gabble to enable XMPP by default. Otherwise, Empathy
  is essentially useless due to the need to install an external connection
  manager. Also, add a README.ConnectionManagers to the installed
  documentation which lists other possibilities.
- Resolves: bug 308871 (Make empathy dependent at least on telepathy-gabble)
  and bug 334221 (Default empathy install is useless).

* Wed Oct 10 2007 Peter Gordon <peter@thecodergeek.com> - 0.14-3
- Enable VoIP support for those brave enough to test/break/debug it (F9+
  only). Though it is functional, it is still deemed rather unstable by
  upstream. Use it at your own risk. :)

* Tue Oct 02 2007 Peter Gordon <peter@thecodergeek.com> - 0.14-2
- Disable VoIP support at this time, since it is deemed unstable by upstream
  for now. (Thanks to Brian Pepple for the notice.)
  
* Tue Oct 02 2007 Peter Gordon <peter@thecodergeek.com> - 0.14-1
- Update to new upstream release (0.14).

* Sun Sep 30 2007 Peter Gordon <peter@thecodergeek.com> - 0.13-1
- Update to new upstream release (0.13), which adds a panel applet (Megaphone)
  and python bindings.
- Split shared libraries into a libs subpackage for easier handling
  in multi-lib environments.

* Fri Aug 31 2007 Peter Gordon <peter@thecodergeek.com> - 0.12-2
- Add ldconfig invocations to %%post and %%postun scriptlets.

* Fri Aug 31 2007 Peter Gordon <peter@thecodergeek.com> - 0.12-1
- Update to new upstream release (0.12).
- Build against new mission-control stack.
- Update License tag (GPLv2+).
- Alphabetize BuildRequires list (aesthetic-only change).

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.8-2
- Rebuild for selinux ppc32 issue.

* Mon Aug 13 2007 Peter Gordon <peter@thecodergeek.com> - 0.11-1
- Update to new upstream release (0.11)

* Fri Jun 22 2007 David Nielsen <david@lovesunix.net> - 0.8-1
- bump to 0.8
- Now with aspell support (deat to teh speeling mistaks)

* Sat Jun  9 2007 David Nielsen <david@lovesunix.net> - 0.7-1
- bump to 0.7

* Mon Jun  4 2007 David Nielsen <david@lovesunix.net> - 0.6-3
- Add telepathy-filesystem to Requires
- Move .desktop from autostart to applications
- Nasty hackery to make empathy launch from the menu

* Mon Jun  4 2007 David Nielsen <david@lovesunix.net> - 0.6-2
- Add gettext to BuildRequires

* Fri Jun  1 2007 David Nielsen <david@lovesunix.net> - 0.6-1
- Bump to 0.6

* Fri Jun  1 2007 David Nielsen <david@lovesunix.net> - 0.5-2
- Let Empathy own the directory and not just the files in it

* Wed May 30 2007 David Nielsen <david@lovesunix.net> - 0.5-1
- Initial package
