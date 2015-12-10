Name:           gcr
Version:	3.18.0
Release:        4%{?dist}
Summary:        A library for bits of crypto UI and parsing
Summary(zh_CN.UTF-8): 一种位密码界面和解析库

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        LGPLv2+
URL:            http://live.gnome.org/CryptoGlue/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.gnome.org/sources/gcr/%{majorver}/gcr-%{version}.tar.xz

BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk3-devel
BuildRequires:  p11-kit-devel
BuildRequires:  gnupg
BuildRequires:  libgcrypt-devel
BuildRequires:  libtasn1-tools
BuildRequires:  libtasn1-devel
BuildRequires:  chrpath

Conflicts: gnome-keyring < 3.3.0

%description
gcr is a library for displaying certificates, and crypto UI, accessing
key stores. It also provides a viewer for crypto files on the GNOME
desktop.

gck is a library for accessing PKCS#11 modules like smart cards.

%description -l zh_CN.UTF-8
一种位密码界面和解析库。

%package devel
Summary: Development files for gcr
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
The gcr-devel package includes the header files for the gcr library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --enable-introspection
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libmock-test-module.*
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/gcr-viewer.desktop
magic_rpm_clean.sh
%find_lang %{name} || touch %{name}.lang

chrpath --delete $RPM_BUILD_ROOT%{_libdir}/lib*.so.*
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gcr-viewer
chrpath --delete $RPM_BUILD_ROOT%{_libexecdir}/gcr-prompter

%post
/usr/sbin/ldconfig
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :
fi


%postun
/usr/sbin/ldconfig
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :


%files -f %{name}.lang
%doc COPYING
%{_bindir}/gcr-viewer
%{_datadir}/applications/gcr-viewer.desktop
%dir %{_datadir}/GConf
%dir %{_datadir}/GConf/gsettings
%{_datadir}/GConf/gsettings/org.gnome.crypto.pgp.convert
%{_datadir}/GConf/gsettings/org.gnome.crypto.pgp_keyservers.convert
%{_datadir}/glib-2.0/schemas/org.gnome.crypto.pgp.gschema.xml
%{_libdir}/girepository-1.0
%{_libdir}/libgck-1.so.*
%{_libdir}/libgcr-3.so.*
%{_libdir}/libgcr-base-3.so.*
%{_libdir}/libgcr-ui-3.so.*
%{_datadir}/gcr-3
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/gcr-crypto-types.xml
%{_libexecdir}/gcr-prompter
%{_datadir}/dbus-1/services/org.gnome.keyring.PrivatePrompter.service
%{_datadir}/dbus-1/services/org.gnome.keyring.SystemPrompter.service
%{_datadir}/applications/gcr-prompter.desktop

%files devel
%{_includedir}/gck-1
%{_includedir}/gcr-3
%{_libdir}/libgck-1.so
%{_libdir}/libgcr-3.so
%{_libdir}/libgcr-base-3.so
%{_libdir}/pkgconfig/gck-1.pc
%{_libdir}/pkgconfig/gcr-3.pc
%{_libdir}/pkgconfig/gcr-base-3.pc
%{_datadir}/gir-1.0
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/gck
%{_datadir}/gtk-doc/html/gcr-3
%{_libdir}/libgcr-ui-3.so
%{_libdir}/pkgconfig/gcr-ui-3.pc
%{_datadir}/vala/vapi/*

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 3.18.0-4
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 3.18.0-3
- 更新到 3.18.0

* Fri Apr 04 2014 Liu Di <liudidi@gmail.com> - 3.12.0-2
- 更新到 3.12.0

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 3.5.3-2
- 为 Magic 3.0 重建

* Mon Jun 25 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Silence glib-compile-schemas output

* Mon Apr 16 2012 Richard Hughes <hughsient@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Mon Mar 26 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.92-2
- Enable introspection, needed for gnome-shell now

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.92-1
- Update to 3.3.92

* Fri Mar 09 2012 Rex Dieter <rdieter@fedoraproject.org> 3.3.90-2
- suppress scriptlet output

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Mon Feb 13 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan  3 2012 Tomas Bzatek <tbzatek@redhat.com> 3.3.3.1-4
- Add a Conflicts directive for older gnome-keyring packages (#771299)

* Wed Dec 21 2011 Matthias Clasen <mclasen@redhat.com> 3.3.3.1-3
- Own some directories

* Wed Dec 21 2011 Matthias Clasen <mclasen@redhat.com> 3.3.3.1-2
- Delete rpaths

* Wed Dec 21 2011 Matthias Clasen <mclasen@redhat.com> 3.3.3.1-1
- Update to 3.3.3.1

* Fri Dec 15 2011 Matthias Clasen <mclasen@redhat.com> 3.3.2.1-1
- Update to 3.3.2.1

* Thu Nov 10 2011 Matthias Clasen <mclasen@redhat.com> 3.3.1-1
- Initial packaging

