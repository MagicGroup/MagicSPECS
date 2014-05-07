Name:           telepathy-salut
Version:        0.8.1
Release:        5%{?dist}
Summary:        Link-local XMPP telepathy connection manager

Group:          Applications/Communications
License:        LGPLv2+
URL:            http://telepathy.freedesktop.org/wiki/FrontPage
Source0:        http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  dbus-devel >= 1.1.0
BuildRequires:	dbus-glib-devel >= 0.61
BuildRequires:	dbus-python
BuildRequires:	avahi-gobject-devel
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	cyrus-sasl-devel
BuildRequires:	libxslt
BuildRequires:	libasyncns-devel >= 0.3
BuildRequires:	pygobject2
BuildRequires:	python-twisted-words
BuildRequires:	telepathy-glib-devel >= 0.17.1
BuildRequires:  libuuid-devel
BuildRequires:	libsoup-devel
BuildRequires:	sqlite-devel
BuildRequires:  gtk-doc

Requires:	telepathy-filesystem

%description
%{name} is a Telepathy connection manager for link-local XMPP.
Normally, XMPP does not support direct client-to-client interactions,
since it requires authentication with a server.  This package makes
it is possible to establish an XMPP-like communications system on a
local network using zero-configuration networking.


%prep
%setup -q

%build
%configure --enable-ssl --enable-olpc --disable-avahi-tests --enable-static=no
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

## Don't package html doc to incorrect doc directory
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}/*.html


%check
make check


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc COPYING AUTHORS NEWS README docs/clique.xml
%{_libexecdir}/%{name}
%{_datadir}/dbus-1/services/*.service
%{_datadir}/telepathy/managers/*.manager
%{_mandir}/man8/%{name}.8.gz
%dir %{_libdir}/telepathy
%dir %{_libdir}/telepathy/salut-0
%dir %{_libdir}/telepathy/salut-0/lib
%{_libdir}/telepathy/salut-0/lib/libsalut-plugins-*.so
%{_libdir}/telepathy/salut-0/lib/libsalut-plugins.so
%{_libdir}/telepathy/salut-0/lib/libwocky-telepathy-salut-*.so
%{_libdir}/telepathy/salut-0/lib/libwocky.so


%changelog
* Thu Oct 17 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.8.1-5
- Add %%check to run the upstream test suite on each build

* Wed Oct 16 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.8.1-4
- Resolve possible multilib conflict

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 16 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.8.1-1
- Update to 0.8.1.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr  4 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0.

* Mon Mar 26 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.7.2-1
- Update to 0.7.2.
- Add BR on libuuid-devel.

* Tue Feb 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.7.1-1
- Update to 0.7.1.

* Sun Jan 08 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.7.0-2
- Rebuild for new gcc.

* Wed Nov 16 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0.
- Bump minimum version of tp-glib needed.

* Tue Oct 18 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0.

* Wed Oct  5 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.5.2-1
- Update to 0.5.2.
- Bump minimum version of tp-glib needed.
- Drop olpc-activity-properties patch. Fix upstream.
- Drop buildroot. No longer necessary
- Drop no-xmldiff patch. No longer needed.

* Wed Sep 28 2011 Daniel Drake <dsd@laptop.org> - 0.5.1-1
- Update to 0.5.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct  6 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0.

* Thu Aug 19 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.3.13-1
- Update to 0.3.13.

* Thu May 20 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.3.12-1
- Update to 0.3.12.
- Drop DSO linking patch. Fixed upstream.

* Sun Apr 25 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.3.10-3
- Drop clean section. No longer needed.

* Fri Mar  5 2010 Peter Robinson <pbrobinson@gmail.com> 0.3.10-2
- Fix DSO linking. Fixes 565145

* Thu Sep 10 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.3.10-1
- Update to 0.3.10.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.3.9-3
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr  2 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.3.9-1
- Update to 0.3.9.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.3.8-1
- Update to 0.3.8.
- Bump minimum version of tp-glib-devel needed.

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 0.3.7-2
- rebuild with new openssl

* Mon Jan  5 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.3.7-1
- Update to 0.3.7.
- Change BR to libsoup-devel, since they support it now.

* Mon Dec  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.6-2
- Enable OLPC support code. It is not used unless a client explicitely requests them.

* Sat Dec  6 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.6-1
- Update to 0.3.6.
- Add BR on libsoup22-devel.

* Wed Sep 17 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.5-1
- Update to 0.3.5.

* Sun Aug 24 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.4-2
- Build with libasyncns support.

* Sat Aug 23 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.4-1
- Update to 0.3.4.
- bump minimum tp-glib version needed.

* Mon Mar 24 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.2.3-1
- Update to 0.2.3.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.2-3
- Autorebuild for GCC 4.3

* Fri Feb  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.2.2-2
- Rebuild for gcc-4.3.

* Wed Jan 30 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.2.2-1
- Update to 0.2.2.

* Tue Jan  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1.

* Fri Dec  7 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0.

* Wed Dec  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.1.11-2
- rebuild for new libssl.so.6/libcrypto.so.6

* Sat Dec  1 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.1.11-1
- Update to 0.1.11.
- Add min. version of check needed.

* Tue Nov 27 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-1
- Update to 0.1.10.

* Wed Nov 14 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.1.9-1
- Update to 0.1.9.

* Tue Nov 13 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.1.8-1
- Update to 0.1.8.

* Mon Nov 12 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.1.7-1
- Update to 0.1.7.

* Wed Nov  7 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.1.6-1
- Update to 0.1.6.
- Add man page.
- Bump min version of telepathy-glib-devel needed.

* Sat Aug 25 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.1.4-1
- Update to 0.1.4.
- Update minimum BR versions needed.

* Tue Aug 21 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.1.3-3
- Rebuild.

* Fri Aug  3 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.1.3-2
- Update license tag.

* Tue Jun 26 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3.
- Add BR on telepathy-glib-devel & libxslt.

* Mon Apr 16 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1
- Add BR on openssl-devel & cyrus-sasl-devel.

* Sun Jan 21 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.1.0-1
- Initial Fedora spec file.
