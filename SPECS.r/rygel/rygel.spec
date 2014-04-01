Name:          rygel
Version:       0.21.5
Release:       1%{?dist}
Summary:       A collection of UPnP/DLNA services

Group:         Applications/Multimedia
License:       LGPLv2+
URL:           http://live.gnome.org/Rygel
Source0:       ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/0.20/%{name}-%{version}.tar.xz

BuildRequires: dbus-glib-devel
BuildRequires: desktop-file-utils
BuildRequires: gstreamer1-devel
BuildRequires: gstreamer1-plugins-base-devel
BuildRequires: gtk3-devel
BuildRequires: gupnp-devel
BuildRequires: gupnp-av-devel
BuildRequires: gupnp-dlna-devel
BuildRequires: libgee-devel
BuildRequires: libsoup-devel
BuildRequires: libunistring-devel
BuildRequires: libuuid-devel
BuildRequires: sqlite-devel
BuildRequires: tracker-devel
BuildRequires: intltool
BuildRequires: gupnp-dlna-devel

%description
Rygel is a home media solution that allows you to easily share audio, video and
pictures, and control of media player on your home network. In technical terms
it is both a UPnP AV MediaServer and MediaRenderer implemented through a plug-in
mechanism. Interoperability with other devices in the market is achieved by
conformance to very strict requirements of DLNA and on the fly conversion of
media to format that client devices are capable of handling.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files for development with %{name}.

%package tracker
Summary: Tracker plugin for %{name}
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}
Requires: tracker

%description tracker
A plugin for rygel to use tracker to locate media on the local machine.

%prep
%setup -q

%build
%configure --enable-tracker-plugin --enable-media-export-plugin --enable-external-plugin \
  --enable-mediathek-plugin --enable-gst-launch-plugin --disable-silent-rules

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%find_lang %{name}

# Verify the desktop files
desktop-file-validate %{buildroot}/%{_datadir}/applications/rygel.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/rygel-preferences.desktop

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING README TODO NEWS doc/README.Mediathek 
%config(noreplace) %{_sysconfdir}/rygel.conf
%{_bindir}/rygel
%{_bindir}/rygel-preferences
%{_libdir}/librygel*.so.*
%{_libdir}/rygel-2.2/engines/librygel-media-engine-gst.so
%{_libdir}/rygel-2.2/engines/librygel-media-engine-simple.so
%{_libdir}/rygel-2.2/engines/media-engine-gst.plugin
%{_libdir}/rygel-2.2/engines/media-engine-simple.plugin
%{_libdir}/rygel-2.2/plugins/librygel-external.so
%{_libdir}/rygel-2.2/plugins/external.plugin
%{_libdir}/rygel-2.2/plugins/librygel-gst-launch.so
%{_libdir}/rygel-2.2/plugins/gst-launch.plugin
%{_libdir}/rygel-2.2/plugins/librygel-media-export.so
%{_libdir}/rygel-2.2/plugins/media-export.plugin
%{_libdir}/rygel-2.2/plugins/librygel-mediathek.so
%{_libdir}/rygel-2.2/plugins/mediathek.plugin
%{_libdir}/rygel-2.2/plugins/librygel-mpris.so
%{_libdir}/rygel-2.2/plugins/mpris.plugin
%{_libdir}/rygel-2.2/plugins/librygel-playbin.so
%{_libdir}/rygel-2.2/plugins/playbin.plugin
%{_datadir}/rygel/
%{_datadir}/applications/rygel*
%{_datadir}/dbus-1/services/org.gnome.Rygel1.service
%{_datadir}/icons/hicolor/*/apps/rygel*
%{_datadir}/man/man?/rygel*

%files tracker
%{_libdir}/rygel-2.2/plugins/librygel-tracker.so
%{_libdir}/rygel-2.2/plugins/tracker.plugin

%files devel
%doc %{_datadir}/gtk-doc/html/librygel*
%{_libdir}/librygel-*.so
%{_includedir}/rygel-2.2
%{_libdir}/pkgconfig/rygel*.pc
%{_datadir}/vala/vapi/rygel*.deps
%{_datadir}/vala/vapi/rygel*.vapi

%changelog
* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 0.21.4-1
- Update to 0.21.4

* Wed Jan 15 2014 Richard Hughes <rhughes@redhat.com> - 0.21.3-1
- Update to 0.21.3

* Mon Dec 23 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.21.2.1-1
- Update to 0.21.2.1
- Call ldconfig in post scriptlets (fixes RHBZ 1045745)

* Mon Nov 18 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.21.1-1
- Update to 0.21.1

* Mon Nov  4 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.21.0-1
- Update to 0.21.0

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 0.20.1-1
- Update to 0.20.1

* Wed Sep 25 2013 Richard Hughes <rhughes@redhat.com> - 0.20.0-1
- Update to 0.20.0

* Thu Sep 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.7-1
- Update to 0.19.7
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.19/rygel-0.19.7.news

* Tue Aug 20 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.5-1
- Update to 0.19.5
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.19/rygel-0.19.5.news

* Tue Jul 30 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.4-1
- Update to 0.19.4
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.19/rygel-0.19.4.news

* Mon Jun 17 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.3-1
- Update to 0.19.3

* Tue May 28 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.2-1
- Update to 0.19.2

* Tue Apr 30 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.1-1
- Update to 0.19.1

* Wed Apr 17 2013 Richard Hughes <rhughes@redhat.com> - 0.18.1-1
- Update to 0.18.1

* Tue Mar 26 2013 Richard Hughes <rhughes@redhat.com> - 0.18.0-1
- Update to 0.18.0

* Tue Mar 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.17.10-1
- 0.17.10 devel release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.17/rygel-0.17.10.news

* Tue Mar  5 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.17.9-1
- 0.17.9 devel release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.17/rygel-0.17.9.news

* Thu Feb 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.17.8-1
- 0.17.8 devel release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.17/rygel-0.17.8.news

* Sat Jan 26 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.17.7-1
- 0.17.7 devel release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.17/rygel-0.17.7.news

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 0.17.6-1
- Update to 0.17.6

* Wed Jan 09 2013 Richard Hughes <hughsient@gmail.com> - 0.17.5.1-1
- Update to 0.17.5.1

* Wed Dec 26 2012 Bruno Wolff III <bruno@wolff.to> 0.17.5-2
- Rebuild for libgupnp-dlna soname bump

* Fri Dec 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.17.5-1
- 0.17.5 devel release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.17/rygel-0.17.5.news

* Thu Dec  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.17.4-1
- 0.17.4 devel release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.17/rygel-0.17.4.news

* Sat Dec  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.17.3-1
- 0.17.3 devel release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.17/rygel-0.17.3.news

* Sun Nov 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.17.2-1
- 0.17.2 devel release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.17/rygel-0.17.2.news

* Thu Nov  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.17.1-1
- 0.17.1 devel release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.17/rygel-0.17.1.news

* Sat Oct  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.17.0-1
- 0.17.0 devel release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.17/rygel-0.17.0.news

* Tue Sep 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.16.0-1
- 0.16.0 stable release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.16/rygel-0.16.0.news

* Tue Sep 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.15.4-1
- 0.15.4 devel release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.15/rygel-0.15.4.news

* Tue Sep  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.15.3-1
- 0.15.3 devel release

* Tue Aug 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.15.2-1
- 0.15.2 devel release

* Sat Jul 28 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.15.1-1
- 0.15.1 devel release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 30 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.15.0.1-1
- 0.15.0.1 devel release

* Tue May 29 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.15.0-1
- 0.15.0 devel release

* Sun Apr 29 2012 Zeeshan Ali <zeenix@redhat.com> - 0.14.1-1
- 0.14.1 stable release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.14/rygel-0.14.1.news

* Mon Mar 26 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.14.0-1
- 0.14.0 stable release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.14/rygel-0.14.0.news

* Tue Mar 20 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.13.4-1
- devel 0.13.4 release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.13/rygel-0.13.4.news

* Wed Mar  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.13.3-1
- devel 0.13.3 release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.13/rygel-0.13.3.news

* Tue Feb 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.13.2-1
- devel 0.13.2 release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.13/rygel-0.13.2.news

* Fri Feb 10 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.13.1-1
- devel 0.13.1 release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.13/rygel-0.13.1.news

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 24 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.13.0-1
- devel 0.13.0 release
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.13/rygel-0.13.0.news

* Mon Oct 24 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.5-1
- stable release 0.12.5
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.12/rygel-0.12.5.news

* Sun Oct  9 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.4-1
- stable release 0.12.4
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.12/rygel-0.12.4.news

* Tue Sep 27 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.3-1
- stable release 0.12.3
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.12/rygel-0.12.3.news

* Tue Sep 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.2-1
- stable release 0.12.2
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.12/rygel-0.12.2.news

* Wed Sep 14 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-1
- stable release 0.12.1
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.12/rygel-0.12.1.news

* Tue Sep  6 2011 Zeeshan Ali <zeenix@redhat.com> 0.12.0-3
- We don't need vala and gupnp-vala to build from release tarball.

* Tue Sep  6 2011 Zeeshan Ali <zeenix@redhat.com> 0.12.0-2
- Rebuild against latest gssdp and gupnp*.

* Mon Sep  5 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.0-1
- Update to stable release 0.12.0
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.12/rygel-0.12.0.news

* Fri Aug  5 2011 Peter Robinson <pbrobinson@gmail.com> 0.11.3-1
- 0.11.3
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.11/rygel-0.11.3.news

* Sun Jul 17 2011 Peter Robinson <pbrobinson@gmail.com> 0.11.2-1
- 0.11.2
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.11/rygel-0.11.2.news

* Tue Jun 21 2011 Zeeshan Ali <zali@redhat.com> 0.11.1-1
- http://ftp.gnome.org/pub/GNOME/sources/rygel/0.11/rygel-0.11.1.news

* Fri Jun 17 2011 Peter Robinson <pbrobinson@gmail.com> 0.11.0-2
- rebuild for new gupnp/gssdp

* Fri Jun 10 2011 Zeeshan Ali <zali@redhat.com> 0.11.0-1
- Update to 0.11.0
- Update description

* Tue May 31 2011 Christopher Aillon <caillon@redhat.com> 0.10.2-1
- Update to 0.10.2

* Mon Apr 18 2011 Peter Robinson <pbrobinson@gmail.com> 0.10.1-1
- Update to 0.10.1

* Fri Apr 15 2011 Peter Robinson <pbrobinson@gmail.com> 0.10.0-1
- Update to 0.10.0

* Wed Apr 13 2011 Peter Robinson <pbrobinson@gmail.com> 0.9.9-3
- bump for new gupnp-dlna

* Mon Apr 11 2011 Peter Robinson <pbrobinson@gmail.com> 0.9.9-2
- bump for new gupnp-dlna

* Tue Feb 22 2011 Peter Robinson <pbrobinson@gmail.com> 0.9.9-1
- Update to 0.9.9

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 0.9.8-4
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 0.9.8-2
- Rebuild against new gtk

* Mon Jan 31 2011 Peter Robinson <pbrobinson@gmail.com> 0.9.8-1
- Update to 0.9.8

* Mon Jan 31 2011 Peter Robinson <pbrobinson@gmail.com> 0.9.7-1
- Update to 0.9.7

* Thu Jan 27 2011 Peter Robinson <pbrobinson@gmail.com> 0.9.6-2
- Rebuild for new gupnp-dlna

* Wed Jan 12 2011 Peter Robinson <pbrobinson@gmail.com> 0.9.6-1
- Update to 0.9.6

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 0.9.5-1
- Update to 0.9.5

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> 0.9.4-2
- Rebuild against newer gtk

* Mon Nov 29 2010 Peter Robinson <pbrobinson@gmail.com> 0.9.4-1
- New 0.9.4 dev release

* Wed Nov 10 2010 Peter Robinson <pbrobinson@gmail.com> 0.9.3-1
- New 0.9.3 dev release, really support gtk3 this time ;-)

* Tue Nov  9 2010 Peter Robinson <pbrobinson@gmail.com> 0.9.2-1
- New 0.9.2 dev release

* Mon Oct 18 2010 Peter Robinson <pbrobinson@gmail.com> 0.9.1-1
- New 0.9.1 dev release

* Mon Oct  4 2010 Peter Robinson <pbrobinson@gmail.com> 0.9.0-1
- New 0.9.0 dev release

* Wed Sep 29 2010 Peter Robinson <pbrobinson@gmail.com> 0.8.1-1
- New 0.8.1 release

* Tue Sep 28 2010 Peter Robinson <pbrobinson@gmail.com> 0.8.0-1
- New 0.8.0 stable release

* Tue Sep 14 2010 Peter Robinson <pbrobinson@gmail.com> 0.7.8-1
- Update to 0.7.8 development release

* Thu Sep  9 2010 Peter Robinson <pbrobinson@gmail.com> 0.7.7-1
- Update to 0.7.7 development release

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> 0.7.6-1
- Update to 0.7.6

* Mon Jul 12 2010 Peter Robinson <pbrobinson@gmail.com> 0.7.2-1
- Update to 0.7.2 development release

* Fri Jul  2 2010 Peter Robinson <pbrobinson@gmail.com> 0.7.1-2
- Update gtk dep to gtk3 for UI

* Fri Jun 25 2010 Peter Robinson <pbrobinson@gmail.com> 0.7.1-1
- Update to 0.7.1 development release

* Mon Jun  7 2010 Peter Robinson <pbrobinson@gmail.com> 0.7.0-1
- Update to 0.7.0 development release

* Sun May 16 2010 Peter Robinson <pbrobinson@gmail.com> 0.6.0-3
- Add the translations as well.

* Sun May 16 2010 Peter Robinson <pbrobinson@gmail.com> 0.6.0-2
- Increment build

* Sun May 16 2010 Peter Robinson <pbrobinson@gmail.com> 0.6.0-1
- Update to 0.6.0

* Wed Apr 14 2010 Peter Robinson <pbrobinson@gmail.com> 0.5.2-1
- Update to 0.5.2

* Wed Feb 24 2010 Peter Robinson <pbrobinson@gmail.com> 0.5.0-1
- Update to 0.5.0

* Mon Jan 25 2010 Bastien Nocera <bnocera@redhat.com> 0.4.10-1
- Update to 0.4.10

* Sat Dec 26 2009 Peter Robinson <pbrobinson@gmail.com> 0.4.8-2
- Update description

* Tue Dec 22 2009 Peter Robinson <pbrobinson@gmail.com> 0.4.8-1
- Update to 0.4.8

* Sat Nov 21 2009 Peter Robinson <pbrobinson@gmail.com> 0.4.6-1
- Update to 0.4.6

* Tue Oct 27 2009 Peter Robinson <pbrobinson@gmail.com> 0.4.4-2
- Add and change new files.

* Tue Oct 27 2009 Peter Robinson <pbrobinson@gmail.com> 0.4.4-1
- Update to 0.4.4

* Fri Oct  2 2009 Peter Robinson <pbrobinson@gmail.com> 0.4.2-1
- Update to 0.4.2

* Fri Sep 25 2009 Bastien Nocera <bnocera@redhat.com> 0.4.1-1
- Update to 0.4.1

* Thu Sep 24 2009 Bastien Nocera <bnocera@redhat.com> 0.4-5
- Make sure we rebuild the C source code from vala sources

* Thu Sep 24 2009 Bastien Nocera <bnocera@redhat.com> 0.4-4
- Make the prefs work

* Thu Sep 24 2009 Peter Robinson <pbrobinson@gmail.com> 0.4-3
- Enable new plugins, add desktop file verification, add more docs

* Thu Sep 24 2009 Peter Robinson <pbrobinson@gmail.com> 0.4-2
- Update deps for new release

* Wed Sep 23 2009 Peter Robinson <pbrobinson@gmail.com> 0.4-1
- New upstream 0.4 release

* Thu Aug 20 2009 Michel Salim <salimma@fedoraproject.org> - 0.3-6
- Rebuild against compat-libgee01

* Fri Aug  7 2009 Peter Robinson <pbrobinson@gmail.com> 0.3-5
- Own rygel include dir, some spec file cleanups

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  1 2009 Peter Robinson <pbrobinson@gmail.com> 0.3-3
- Rebuild with new libuuid build req

* Wed Jun  3 2009 Peter Robinson <pbrobinson@gmail.com> 0.3-2
- Split tracker plugin out to a sub package. Resolves RHBZ 507032

* Wed Jun  3 2009 Peter Robinson <pbrobinson@gmail.com> 0.3-1
- New upstream release

* Fri Mar 13 2009 Peter Robinson <pbrobinson@gmail.com> 0.2.2-3
- Add a dep on tracker as that is currently the way it finds media

* Mon Mar 2  2009 Peter Robinson <pbrobinson@gmail.com> 0.2.2-2
- Added some missing BuildReqs

* Mon Mar 2  2009 Peter Robinson <pbrobinson@gmail.com> 0.2.2-1
- Initial release
