Name:		gnome-online-accounts
Version:	3.8.1
Release:	1%{?dist}
Summary:	Provide online accounts information

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		https://live.gnome.org/GnomeOnlineAccounts
Source0:	http://download.gnome.org/sources/gnome-online-accounts/3.8/%{name}-%{version}.tar.xz

BuildRequires:	gcr-devel
BuildRequires:	glib2-devel >= 2.35
BuildRequires:	gtk3-devel >= 3.5.1
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	krb5-devel
BuildRequires:	webkitgtk3-devel
BuildRequires:	json-glib-devel
BuildRequires:	libsecret-devel >= 0.7
BuildRequires:	libsoup-devel >= 2.41
BuildRequires:	rest-devel
BuildRequires:	libxml2-devel

%description
gnome-online-accounts provides interfaces so applications and
libraries in GNOME can access the user's online accounts.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	gobject-introspection-devel

%description devel
The gnome-online-accounts-devel package contains libraries and header
files for developing applications that use gnome-online-accounts.

%prep
%setup -q

%build
%configure \
  --disable-static \
  --enable-gtk-doc \
  --enable-exchange \
  --enable-facebook \
  --enable-google \
  --enable-imap-smtp \
  --enable-kerberos \
  --enable-owncloud \
  --enable-windows-live
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la $RPM_BUILD_ROOT/%{_libdir}/control-center-1/panels/*.la

%find_lang %{name}

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
%doc NEWS COPYING
%{_libdir}/girepository-1.0/Goa-1.0.typelib
%{_libdir}/libgoa-1.0.so.0
%{_libdir}/libgoa-1.0.so.0.0.0
%{_libdir}/libgoa-backend-1.0.so.0
%{_libdir}/libgoa-backend-1.0.so.0.0.0
%{_prefix}/libexec/goa-daemon
%{_datadir}/dbus-1/services/org.gnome.OnlineAccounts.service
%{_datadir}/icons/hicolor/*/apps/goa-*.png
%{_datadir}/man/man8/goa-daemon.8.gz
%{_datadir}/%{name}/goawebview.css

%files devel
%{_includedir}/goa-1.0/
%{_libdir}/libgoa-1.0.so
%{_libdir}/libgoa-backend-1.0.so
%{_datadir}/gir-1.0/Goa-1.0.gir
%{_libdir}/pkgconfig/goa-1.0.pc
%{_libdir}/pkgconfig/goa-backend-1.0.pc
%{_datadir}/gtk-doc/html/goa/

%dir %{_libdir}/goa-1.0
%{_libdir}/goa-1.0/include

%changelog
* Mon Apr 15 2013 Richard Hughes <rhughes@redhat.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Tue Mar 05 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.7.91-1
- Update to 3.7.91

* Tue Feb 26 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.7.90-2
- Enable IMAP / SMTP

* Fri Feb 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.90-1
- Update to 3.7.90

* Wed Feb 06 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.7.5-1
- Update to 3.7.5

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.4-2
- Rebuilt for libgcr soname bump

* Mon Jan 14 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.7.4-1
- Update to 3.7.4

* Thu Jan 03 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.7.3-1
- Update to 3.7.3

* Sun Nov 18 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.7.2-1
- Update to 3.7.2

* Tue Oct 23 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.7.1-1
- Update to 3.7.1

* Mon Oct 15 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Mon Sep 17 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.92-1
- Update to 3.5.92

* Tue Sep 04 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.91-1
- Update to 3.5.91

* Tue Aug 21 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.90-1
- Update to 3.5.90

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.4-1
- Update to 3.5.4

* Mon Jun 25 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.3-1
- Update to 3.5.3

* Tue Jun 05 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.2-1
- Update to 3.5.2

* Wed May 02 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.1-1
- Update to 3.5.1

* Tue Apr 17 2012 Richard Hughes <hughsient@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Mon Mar 26 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.3.92.1-1
- Update to 3.3.92.1

* Tue Mar 20 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.3.92-1
- Update to 3.3.92

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.3.0-2
- Enable Windows Live provider.

* Mon Dec 19 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.3.0-1
- Update to 3.3.0.
- Update source url.

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 3.2.0.1-1
- Update to 3.2.0.1

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Fri Jul 01 2011 Bastien Nocera <bnocera@redhat.com> 3.1.1-1
- Update to 3.1.1

* Tue Jun 14 2011 Bastien Nocera <bnocera@redhat.com> 3.1.0-3
- Add more necessary patches

* Tue Jun 14 2011 Bastien Nocera <bnocera@redhat.com> 3.1.0-2
- Update with review comments from Peter Robinson

* Mon Jun 13 2011 Bastien Nocera <bnocera@redhat.com> 3.1.0-1
- First version

