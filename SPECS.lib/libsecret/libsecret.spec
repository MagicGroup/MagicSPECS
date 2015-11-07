# first two digits of version
%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:           libsecret
Version:	0.18
Release: 2%{?dist}
Summary:        Library for storing and retrieving passwords and other secrets
Summary(zh_CN.UTF-8): 存储和检索密码和其它秘密信息的库 

License:        LGPLv2+
URL:            https://live.gnome.org/Libsecret
Source0:        http://download.gnome.org/sources/libsecret/%{release_version}/libsecret-%{version}.tar.xz

BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  intltool
BuildRequires:  libgcrypt-devel >= 1.2.2
BuildRequires:  vala-devel >= 0.17.2.12
BuildRequires:  vala-tools
BuildRequires:  gtk-doc
BuildRequires:  libxslt-devel
BuildRequires:  docbook-style-xsl

Provides:       bundled(egglib)

%description
libsecret is a library for storing and retrieving passwords and other secrets.
It communicates with the "Secret Service" using DBus. gnome-keyring and
KSecretService are both implementations of a Secret Service.

%description -l zh_CN.UTF-8
存储和检索密码和其它秘密信息的库。


%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang libsecret


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f libsecret.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/secret-tool
%{_libdir}/libsecret-1.so.*
%{_libdir}/girepository-1.0/Secret-1.typelib
#%{_libdir}/girepository-1.0/SecretUnstable-0.typelib
%doc %{_mandir}/man1/secret-tool.1.gz

%files devel
%{_includedir}/libsecret-1/
%{_libdir}/libsecret-1.so
%{_libdir}/pkgconfig/libsecret-1.pc
%{_libdir}/pkgconfig/libsecret-unstable.pc
%{_datadir}/gir-1.0/Secret-1.gir
#%{_datadir}/gir-1.0/SecretUnstable-0.gir
%{_datadir}/vala/vapi/libsecret-1.deps
%{_datadir}/vala/vapi/libsecret-1.vapi
#%{_datadir}/vala/vapi/libsecret-unstable.deps
#%{_datadir}/vala/vapi/libsecret-unstable.vapi
#%{_datadir}/vala/vapi/mock-service-0.vapi
%doc %{_datadir}/gtk-doc/


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.18-2
- 为 Magic 3.0 重建

* Thu Jul 31 2014 Liu Di <liudidi@gmail.com> - 0.18-1
- 更新到 0.18

* Fri May 02 2014 Liu Di <liudidi@gmail.com> - 0.15-2
- 为 Magic 3.0 重建

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.15-1
- Update to 0.15

* Wed Mar 06 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.14-1
- Update to 0.14

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 0.13-1
- Update to 0.13

* Fri Nov 23 2012 Debarshi Ray <rishi@fedoraproject.org> - 0.12-1
- Update to 0.12

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 0.11-1
- Update to 0.11

* Wed Sep 19 2012 Tomas Bzatek <tbzatek@redhat.com> - 0.10-1
- Update to 0.10
- Enable vala

* Mon Aug 06 2012 Stef Walter <stefw@redhat.com> - 0.8-1
- Update to 0.8

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Debarshi Ray <rishi@fedoraproject.org> - 0.7-1
- Update to 0.7

* Sat Jul 14 2012 Kalev Lember <kalevlember@gmail.com> - 0.6-1
- Update to 0.6

* Thu Jun 28 2012 Kalev Lember <kalevlember@gmail.com> - 0.3-1
- Update to 0.3

* Mon Apr 16 2012 Kalev Lember <kalevlember@gmail.com> - 0.2-1
- Update to 0.2
- Enable parallel make

* Fri Mar 30 2012 Kalev Lember <kalevlember@gmail.com> - 0.1-2
- Add provides bundled(egglib) (#808025)
- Use global instead of define

* Thu Mar 29 2012 Kalev Lember <kalevlember@gmail.com> - 0.1-1
- Initial RPM release
