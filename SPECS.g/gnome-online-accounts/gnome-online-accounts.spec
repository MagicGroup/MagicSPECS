Name:		gnome-online-accounts
Version:	3.19.1
Release:	4%{?dist}
Summary:	Single sign-on framework for GNOME
Summary(zh_CN.UTF-8): GNOME 的单点登录框架

Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	LGPLv2+
URL:		https://live.gnome.org/GnomeOnlineAccounts
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:	http://download.gnome.org/sources/gnome-online-accounts/%{majorver}/%{name}-%{version}.tar.xz

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
BuildRequires:	telepathy-glib-devel
BuildRequires:	libxml2-devel

Requires:	realmd

%description
GNOME Online Accounts provides interfaces so that applications and libraries
in GNOME can access the user's online accounts. It has providers for Google,
ownCloud, Facebook, Flickr, Windows Live, Microsoft Exchange and Kerberos.

%description -l zh_CN.UTF-8
GNOME 的单点登录框架，支持 Google, ownCloud, Facebook, Flickr, Window Live,
微软 Exchage 和 kerberos。

%package devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	gobject-introspection-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure \
  --disable-static \
  --enable-gtk-doc \
  --enable-exchange \
  --enable-facebook \
  --enable-flickr \
  --enable-google \
  --enable-imap-smtp \
  --enable-kerberos \
  --enable-owncloud \
  --enable-telepathy \
  --enable-windows-live
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la $RPM_BUILD_ROOT/%{_libdir}/control-center-1/panels/*.la   $RPM_BUILD_ROOT%{_libdir}/goa-1.0/web-extensions/*.la

magic_rpm_clean.sh
%find_lang %{name}
%find_lang %{name}-tpaw

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang -f %{name}-tpaw.lang
%doc NEWS COPYING
%{_libdir}/girepository-1.0/Goa-1.0.typelib
%{_libdir}/libgoa-1.0.so.0
%{_libdir}/libgoa-1.0.so.0.0.0
%{_libdir}/libgoa-backend-1.0.so.1
%{_libdir}/libgoa-backend-1.0.so.1.0.0
%{_prefix}/libexec/goa-daemon
%{_datadir}/dbus-1/services/org.gnome.*.service
%{_datadir}/icons/hicolor/*/apps/goa-*.png
%{_datadir}/icons/hicolor/*/apps/im-*.png
%{_datadir}/icons/hicolor/*/apps/im-*.svg
%{_datadir}/man/man8/goa-daemon.8.gz

%dir %{_datadir}/%{name}
#{_datadir}/%{name}/goawebview.css
%{_datadir}/%{name}/irc-networks.xml
%{_libdir}/goa-1.0/web-extensions/libgoawebextension.so
%{_libexecdir}/goa-identity-service
%{_datadir}/glib-2.0/schemas/org.gnome.online-accounts.gschema.xml



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
* Fri Dec 04 2015 Liu Di <liudidi@gmail.com> - 3.19.1-4
- 为 Magic 3.0 重建

* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 3.19.1-3
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.19.1-2
- 更新到 3.19.1

* Wed Apr 09 2014 Liu Di <liudidi@gmail.com> - 3.12.0-1
- 更新到 3.12.0

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Wed Jan 15 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Wed Dec 18 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.11.3-1
- Update to 3.11.3

* Mon Nov 25 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Tue Nov 12 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.10.2-1
- Update to 3.10.2

* Fri Oct 18 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.10.1-2
- Adapt to changes in the redirect URI used by Facebook (GNOME #710363)

* Wed Oct 16 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Tue Oct 08 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.10.0-3
- Add a Requires on realmd (Red Hat #949741)

* Fri Sep 27 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.10.0-2
- Fix GNOME #708462 and #708832

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-1
- Update to 3.9.91

* Thu Aug 29 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-2
- Update to new webkitgtk-2.1.90 API

* Thu Aug 22 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.9.90-1
- Update to 3.9.90

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 11 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.9.4-1
- Update to 3.9.4
- Update summary and description to match upstream DOAP file

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.2-1
- Update to 3.9.2

* Sat May 04 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.1-1
- Update to 3.9.1

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

