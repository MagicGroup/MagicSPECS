%if 0%{?rhel}
%global run_tests 0
%else
%global run_tests 1
%endif

Name:           telepathy-gabble
Version:        0.18.2
Release:        1%{?dist}
Summary:        A Jabber/XMPP connection manager

Group:          Applications/Communications
License:        LGPLv2+
URL:            http://telepathy.freedesktop.org/wiki/
Source0:        http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz
Patch1:         telepathy-gabble-0.18.0-build.patch
Patch2:         0001-xmpp-console-Explicitly-state-python-in-the-shebang.patch

BuildRequires:  dbus-devel >= 1.1.0
BuildRequires:  dbus-glib-devel >= 0.82
BuildRequires:  telepathy-glib-devel >= 0.19.9
BuildRequires:  glib2-devel >= 2.32
BuildRequires:  sqlite-devel
BuildRequires:  libuuid-devel
BuildRequires:  libsoup-devel
BuildRequires:  libnice-devel >= 0.0.11
BuildRequires:  cyrus-sasl-devel
BuildRequires:  libxslt
%if %{run_tests}
# Build Requires needed for tests.
BuildRequires:  python
BuildRequires:  python-twisted
BuildRequires:  dbus-python
BuildRequires:  pygobject2
%endif

Requires:       telepathy-mission-control >= 5.5.0
Requires:       telepathy-filesystem

# Removed in F17
Obsoletes:      telepathy-butterfly < 0.5.15-5


%description
A Jabber/XMPP connection manager, that handles single and multi-user
chats and voice calls.


%prep
%setup -q
%patch1 -p 1 -b .build
%patch2 -p 1 -b .shebang


%if %{run_tests}
%check
#make check
%endif


%build
%configure --enable-static=no
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

## Don't package html doc to incorrect doc directory
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}/*.html


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc COPYING AUTHORS
%doc docs/*.html
%{_bindir}/%{name}-xmpp-console
%{_libexecdir}/%{name}
%{_datadir}/dbus-1/services/*.service
%{_datadir}/telepathy/managers/*.manager
%{_mandir}/man8/%{name}.8.gz
## If more connection managers make use of libdir/telepathy this
## be moved to the tp-filesystem spec file.
%dir %{_libdir}/telepathy
%dir %{_libdir}/telepathy/gabble-0
%dir %{_libdir}/telepathy/gabble-0/lib
%dir %{_libdir}/telepathy/gabble-0/plugins
%{_libdir}/telepathy/gabble-0/lib/libgabble-plugins-*.so
%{_libdir}/telepathy/gabble-0/lib/libgabble-plugins.so
%{_libdir}/telepathy/gabble-0/lib/libwocky-telepathy-gabble-*.so
%{_libdir}/telepathy/gabble-0/lib/libwocky.so
%{_libdir}/telepathy/gabble-0/plugins/libconsole.so
%{_libdir}/telepathy/gabble-0/plugins/libgateways.so


%changelog
* Thu Mar 20 2014 Brian Pepple <bpepple@fedoraproject.org> - 0.18.2-1
- Update to 0.18.2.

* Tue Nov  5 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.18.1-2
- Explicitly state python in the shebang

* Fri Sep  6 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.18.1-1
- Update to 0.18.1.

* Sun Aug 11 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.18.0-1
- Update to 0.18.0.
- Bump minimum version of glib2 needed.

* Thu Aug 01 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.17.5-2
- Bump release number

* Thu Aug  1 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.17.5-1
- Update to 0.17.5.

* Fri May 31 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.17.4-1
- Update to 0.17.4.

* Thu Mar  7 2013 Tomáš Mráz <tmraz@redhat.com> - 0.17.3-2
- Try to make it build

* Mon Mar 04 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.17.3-1
- Update to 0.17.3.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.17.2-1
- Update to 0.17.2.
- Bump minimum version of tp-glib.

* Sat Nov 17 2012 Kalev Lember <kalevlember@gmail.com> - 0.17.1-2
- Obsolete telepathy-butterfly (#820858)

* Tue Sep 11 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.17.1-1
- Update to 0.17.1.
- Bump minimum version of tp-glib needed.

* Tue Aug 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.17.0-1
- Update to 0.17.0.
- Bump minimum version of tp-glib needed.

* Tue Aug 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.16.2-1
- Update to 0.16.2.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.16.1-1
- Update to 0.16.1.
- Bump minimum version of glib2 needed.

* Tue Jun 12 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.16.0-2
- Make tests conditional. (#831342)

* Tue Apr  3 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.16.0-1
- Update to 0.16.0.
- Bump minimum version of tp-glib needed.

* Fri Mar 23 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.15.5-1
- Update to 0.15.5.
- Bump minimum version of tp-glib.

* Wed Feb 22 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.15.4-1
- Update to 0.15.4.
- Bump minimum version of tp-glib needed.

* Sun Jan 08 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.15.3-2
- Rebuild for new gcc.

* Thu Dec 22 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.15.3-1
- Update to 0.15.3.
- Re-enable checks.

* Wed Dec 21 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.15.2-1
- Update to 0.15.2.
- Disable checks for now.

* Tue Nov 29 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.15.1-1
- Update to 0.15.1.
- Bump minimum version of tp-glib needed.
- Enable Channel.Type.Call support.

* Thu Nov 24 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.14.1-1
- Update to 0.14.1.

* Mon Nov  7 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.14.0-1
- Update to 0.14.0.

* Thu Sep 29 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.12.7-1
- Update to 0.12.7.

* Wed Aug 24 2011 Matthias Clasen <mclasen@redhat.com> - 0.12.6-2
- Rebuild to match f16

* Thu Aug 18 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.12.6-1
- Update to 0.12.6.

* Fri Jun 24 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.12.3-1
- Update to 0.12.3.

* Thu Jun 16 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.12.2-1
- Update to 0.12.2.

* Thu Jun  2 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.12.1-1
- Update to 0.12.1.

* Thu Apr 21 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.12.0-1
- Update to 0.12.0.
- Bump minimum version of tp-glib needed.
- Enable tests again.

* Mon Mar 14 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.11.8-1
- Update to 0.11.8.

* Wed Feb 16 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.11.7-1
- Update to 0.11.7.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.11.6-1
- Update to 0.11.6.
- Enable tests.

* Wed Jan 26 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.11.5-2
- Rebuild for new libnice.

* Mon Jan 10 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.11.5-1
- Update to 0.11.5.

* Tue Dec 14 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.4-1
- Update to 0.11.4.
- Add BR on python-twisted, dbus-python, and pygobject2 for tests.
- Bump min version of tp-glib.

* Tue Nov 30 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.3-1
- Update to 0.11.3.
- Bump min version of tp-glib needed.

* Mon Nov 22 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.2-1
- Update to 0.11.2.

* Tue Nov 16 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.1-1
- Update to 0.11.1.
- Remove -with-ca-cert config option. No longer needed.

* Thu Nov  4 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.0-1
- Update to 0.11.0.
- Bump min BR version for tp-glib.

* Tue Nov  2 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.10.4-1
- Update to 0.10.4.
- Bump min BR version for glib2.

* Wed Oct  6 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.10.3-1
- Update to 0.10.3.

* Fri Oct  1 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.10.2-1
- Update to 0.10.2.

* Wed Sep 29 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.10.1-1
- Update to 0.10.1.

* Wed Sep 29 2010 jkeating - 0.10.0-2
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.10.0-1
- Update to 0.10.0.
- Add requires on tp-mission-control. Refer to NEWS file.

* Mon Sep 13 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.18-1
- Update to 0.9.18.

* Thu Aug 26 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.17-1
- Update to 0.9.17.
- Add Fedora's CA cert path to config.
- Drop buildroot. No longer needed.

* Fri Aug 20 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.16-1
- Update to 0.9.16.

* Wed Jun 30 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.15-1
- Update to 0.9.15.

* Mon Jun 28 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.14-1
- Update to 0.9.14.
- Drop disco patch. Fixed upstream.

* Thu Jun 24 2010 Matthew Garrett <mjg@redhat.com> - 0.9.13-2
- telepathy-gabble-disco-fix.patch: Fix connections to some servers

* Mon Jun 14 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.13-1
- Update to 0.9.13.
- Add BR on cyrus-sasl-devel for wocky test.
- Add BR on libnice-devel

* Thu Jun  3 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.12-1
- Update to 0.9.12.
- Add BR for sqlite-devel.
- Bump min req for tp-glib.

* Mon Apr 26 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.11-1
- Update to 0.9.11.

* Sun Apr 25 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.9-2
- Drop clean section. No longer needed.

* Sun Mar 28 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.9-1
- Update to 0.9.9.

* Wed Mar 17 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.8-1
- Update to 0.9.8.

* Thu Feb 25 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.6-1
- Update to 0.9.6.

* Fri Feb 19 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.5-1
- Update to 0.9.5.

* Thu Jan 28 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.4-1
- Update to 0.9.4.

* Tue Jan 26 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.3-1
- Update to 0.9.3.
- Drop vcard-manager-hashtable patch.
- Drop try-not-to-set-vcard-fields patch.
- Drop vcard-on-login patch.
- Drop loudmouth-devel BR.

* Tue Dec 22 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.9-3
- Bump.

* Tue Dec 22 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.9-2
- Backport some patches to prevent gabble from setting your VCard
  on every login.

* Mon Dec  7 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.9-1
- Update to 0.8.9.
- Drop proxy patch.  Fixed upstream.

* Thu Nov 26 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.8-2
- Add patch to only query SOCK5 proxies when needed.

* Mon Nov  9 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.8-1
- Update to 0.8.8.

* Wed Oct 14 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.7-1
- Update to 0.8.7.

* Fri Oct  9 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.6-1
- Update to 0.8.6.

* Fri Oct  2 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.5-1
- Update to 0.8.5.

* Wed Sep 30 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.4-1
- Update to 0.8.4.

* Thu Sep 10 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.3-1
- Update to 0.8.3.

* Thu Sep  3 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.2-1
- Update to 0.8.2.

* Thu Aug 20 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.1-2
- Enable libuuid support.

* Thu Aug 20 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.1-1
- Update to 0.8.1.

* Tue Aug 18 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0.
- Bump min version of tp-glib needed.

* Sun Aug  9 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.32-1
- Update to 0.7.32.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.31-1
- Update to 0.7.31.

* Mon Jun 29 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.30-1
- Update to 0.7.30.

* Sun Jun 21 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.29-1
- Update to 0.7.29.

* Wed Jun 10 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.28-1
- Update to 0.7.28.

* Mon May 11 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.27-1
- Update to 0.7.27.
- Drop gthread patch.  Fixed upstream.

* Thu Apr  9 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.26-1
- Update to 0.7.26.

* Fri Apr  3 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.25-1
- Update to 0.7.25.
- Bump minimum version of tp-glib-devel needed.

* Mon Mar 23 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.24-1
- Update to 0.7.24.
- Add BR on libsoup-devel.
- Add patch to have pkgconfig link in gthread-2.0.

* Mon Mar  2 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.22-1
- Update to 0.7.22.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.21-1
- Update to 0.7.21.
- Bump minimum version of tp-glib-devel needed.

* Mon Feb  2 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.20-1
- Update to 0.7.20.

* Thu Jan 29 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.19-1
- Update to 0.7.19.

* Tue Jan  6 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.18-1
- Update to 0.7.18.

* Sun Dec 14 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.17-1
- Update to 0.7.17.

* Tue Dec  2 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.16-1
- Update to 0.7.16.

* Fri Nov  7 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.15-1
- Update to 0.7.15.

* Thu Oct 23 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.12-1
- Update to 0.7.12.

* Wed Oct 15 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.10-1
- Update to 0.7.10.

* Mon Sep 29 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.9-1
- Update to 0.7.9.

* Sat Aug 23 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.8-1
- Update to 0.7.8.
- Drop assertion patch.  Fixed upstream.

* Thu Aug  7 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.7-2
- Add patch to fix assertion. (#457659)

* Thu Jul 31 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.7-1
- Update to 0.7.7.
- Bump min version of tp-glib needed.

* Fri May 16 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.6-1
- Update to 0.7.6.

* Mon May  5 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.5-1
- Update to 0.7.5.

* Fri May  2 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.4-1
- Update to 0.7.4.
- Package new documentation.

* Thu Feb 14 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.6.2-1
- Update to 0.6.2.

* Fri Feb  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.6.1-3
- Rebuild for gcc-4.3.

* Fri Jan 18 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.6.1-2
- Rebuild for new version of loudmouth.

* Wed Nov  7 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.6.1-1
- Update to 0.6.1.

* Mon Oct  1 2007 Matej Cepl <mcepl@redhat.com> - 0.6.0-1
- New upstream version.

* Fri Sep  7 2007 Matej Cepl <mcepl@redhat.com> - 0.5.14-1
- New upstream version

* Thu Aug 30 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.13-1
- Update to 0.5.13.
- Bump minimum version of telepathy-glib.

* Tue Aug 28 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.12-5
- Add python as a BR.

* Tue Aug 21 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.12-4
- Rebuild.

* Sun Aug  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.12-3
- Update license tag.

* Tue Jun 19 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.12-2
- Correct version check for loudmouth

* Tue Jun 19 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.12-1
- Update to 0.5.12.
- Add BR on telepathy-glib-devel

* Tue Feb 20 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.1-2
- Rebuild for new loudmouth.

* Mon Jan 29 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1.

* Tue Dec 12 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0.

* Thu Dec  7 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.4.9-1
- Update to 0.4.9.

* Fri Dec  1 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.4.8-1
- Update to 0.4.8.

* Thu Nov 16 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.4.5-1
- Update to 0.4.5.

* Sat Nov  4 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.4.3-1
- Update to 0.4.3.

* Fri Oct 27 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.4.2-1
- Update to 0.4.2.

* Mon Oct 23 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.4.1-1
- Update to 0.4.1.

* Thu Oct 19 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0.

* Fri Oct 13 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.3.13-1
- Update to 0.3.13.

* Wed Oct 11 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.3.11-1
- Update to 0.3.11.

* Thu Oct  5 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.3.10-1
- Update to 0.3.10.

* Wed Oct  4 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.3.9-1
- Update to 0.3.9.

* Sun Oct  1 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.3.7-1
- Update to 0.3.7.
- Add requires on telepathy-filesystem.

* Thu Sep 21 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.3.6-1
- Update to 0.3.6.

* Sun Sep 17 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.3.5-1
- Update to 0.3.5.

* Mon Sep 11 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.3.4-1
- Update to 0.3.4.
- Use -disable-loudmouth-versioning to build with stable version of loudmouth.

* Sat Sep  9 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.3.1-2
- Bump.

* Mon Aug 28 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.3.1-1
- Initial FE spec.
