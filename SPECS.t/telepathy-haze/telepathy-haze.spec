Name:		telepathy-haze
Version:	0.8.0
Release:	1%{?dist}
Summary:	A multi-protocol Libpurple connection manager for Telepathy

Group:		Applications/Communications
License:	GPLv2+
URL:		http://developer.pidgin.im/wiki/Telepathy

Source0:	http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildRequires:	dbus-python
BuildRequires:	libpurple-devel >= 2.7
BuildRequires:	pygobject2
BuildRequires:	python-twisted-words
BuildRequires:	telepathy-glib-devel >= 0.15.1
BuildRequires:  libxslt
  
Requires:	telepathy-filesystem    

%description
telepathy-haze is a connection manager built around libpurple, the core of
Pidgin (formerly Gaim), as a Summer of Code project under the Pidgin umbrella.
Ultimately, any protocol supported by libpurple will be supported by
telepathy-haze; for now, XMPP, MSN and AIM are known to work acceptably, and
others will probably work too.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_datadir}/telepathy/managers/haze.manager


%check
make check


%files
%doc COPYING NEWS
%{_libexecdir}/telepathy-haze
%{_datadir}/dbus-1/services/*.haze.service
%{_mandir}/man8/telepathy-haze.8*


%changelog
* Wed Oct  2 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0.

* Thu Sep 26 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.7.1-2
- Add %%check to run the upstream test suite on each build

* Tue Sep 17 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.7.1-1
- Update to 0.7.1.
- Drop patches included in this release.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Apr 14 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.7.0-4
- Drop def attribute bits. No longer needed.

* Thu Apr 11 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.7.0-3
- Pull some upstream patches to fix OCS support & memory leaks. (#754395)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr  4 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0.
- Add BR on libxslt.

* Mon Jan 09 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.5.0-2
- Rebuild for new gcc.

* Sun Jul 10 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0.
- Drop media manager patch. Fixed upstream.
- Bump minimum versions of libpurple and tp-glib needed.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.4.0-2
- Add patch to instantiate the media manager only if the protocol support calls.
- Drop buildroot and clean section. No longer needed.

* Thu Aug  5 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0.

* Sun Aug  1 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.3.6-1
- Update to 0.3.6.

* Sat Feb 20 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.3.3-2
- Drop manager file, so Empathy can connect to ICQ. (#566968)

* Mon Jan 25 2010 Peter Gordon <peter@thecodergeek.com> - 0.3.3-1
- Update to new upstream release (0.3.3).
- Remove upstream Yahoo! IM fix:
  - no-yahoo-japan.patch
- Bump minimum telepathy-glib version.

* Thu Aug 13 2009 Peter Gordon <peter@thecodergeek.com> - 0.3.1-3
- Add upstream patch to remove the Yahoo! Japan from the manager profile,
  which fixes Yahoo! IM connectivity issues as reported in GNOME bug #591381.
  + no-yahoo-japan.patch
- Resolves: Fedora bug #514998 (Yahoo! Instant Messenger accounts do not work
  in empathy).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1.

* Sun Apr 12 2009 Peter Gordon <peter@thecodergeek.com> - 0.3.0-1
- Update to new upstream release (0.3.0)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 12 2008 Peter Gordon <peter@thecodergeek.com> - 0.2.1-1
- Update to new upstream release (0.2.1)

* Wed Aug 13 2008 Peter Gordon <peter@thecodergeek.com> - 0.2.0-3
- Remove the mission-control subpackage in favor of using the profiles from
  Empathy upstream.

* Tue Jul 29 2008 Peter Gordon <peter@thecodergeek.com> - 0.2.0-2
- Fix the ICQ Mission Control profile to properly use the "icq" configuration
  UI, rather than the one for jabber.
- Resolves: bug #456565 (Wrong entry in haze-icq.profile)

* Sat Mar 01 2008 Peter Gordon <peter@thecodergeek.com> - 0.2.0-1
- Update to new upstream release (0.2.0)
- Add ICQ Mission-Control profile.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.4-3
- Autorebuild for GCC 4.3

* Sun Dec 16 2007 Peter Gordon <peter@thecodergeek.com> - 0.1.4-2
- Add patch from upstream Darcs to fix bug 425870 (bad apostrophe escaping with
  Yahoo! messages).
  + fix-yahoo-apostrophe-escaping.patch

* Thu Nov 22 2007 Peter Gordon <peter@thecodergeek.com> - 0.1.4-1
- Update to new upstream build-fix release (0.1.4).
- Add Yahoo! IM support to the mission-control profiles, with default
  login/server information taken from Pidgin/Finch.

* Wed Nov 14 2007 Peter Gordon <peter@thecodergeek.com> - 0.1.3-1
- Update to new upstream release (0.1.3), which fixes the accidental
  ~/.purple directory deletion with Pidgin 2.3.0+ (among other notable fixes
  and enhancements).
- Drop compile fix with recent telepathy-glib releases (fixed upstream):
  - fix-deprecated-tp_debug-call.patch

* Tue Nov 13 2007 Peter Gordon <peter@thecodergeek.com> - 0.1.2-4
- Add patch to fix build error due to calling deprecated
  tp_debug_set_flags_from_env function.
  + fix-deprecated-tp_debug-call.patch

* Sun Nov 11 2007 Peter Gordon <peter@thecodergeek.com> - 0.1.2-3
- Fix Source0 URL.

* Thu Nov 01 2007 Peter Gordon <peter@thecodergeek.com> - 0.1.2-2
- Add haze-msn.profile (based on the profile provided by the PyMSN-based
  Butterfly connection manager) so that MC-using applications (such as
  Empathy) can use the libpurple-based MSN connection manager instead of
  Butterfly, at the user's option. 
  
* Sun Sep 16 2007 Peter Gordon <peter@thecodergeek.com> - 0.1.2-1
- Update to new upstream release (0.1.2), which fixes sending messages with
  <, >, and & characters and properly cleans up zombie children.   

* Fri Aug 17 2007 Peter Gordon <peter@thecodergeek.com> - 0.1.1-1
- Update to new upstream release (0.1.1), which fixes segfaults when closing
  text and list channels, and some potential g_free corruptions.
- Sync %%description with upstream release announcements.

* Mon Aug 13 2007 Peter Gordon <peter@thecodergeek.com> - 0.1.0-1
- Initial packaging for Fedora.

