# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           grilo
Version:        0.2.5
Release:        1%{?dist}
Summary:        Content discovery framework

Group:          Applications/Multimedia
License:        LGPLv2+
Source0:        http://ftp.gnome.org/pub/GNOME/sources/grilo/%{release_version}/grilo-%{version}.tar.xz
Url:            http://live.gnome.org/Grilo

BuildRequires:  chrpath
BuildRequires:  gnome-common
BuildRequires:  vala-devel >= 0.7.2
BuildRequires:  vala-tools >= 0.7.2
BuildRequires:  gtk-doc
BuildRequires:  gobject-introspection-devel >= 0.9.0
BuildRequires:  libxml2-devel
BuildRequires:  libsoup-devel
# For the test UI
BuildRequires:  gtk3-devel

Requires:       gobject-introspection

%description
Grilo is a framework that provides access to different sources of
multimedia content, using a pluggable system.
This package contains the core library and elements.

%package devel
Summary:        Libraries/include files for Grilo framework
Group:          Development/Libraries

Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel gobject-introspection-devel

%description devel
Grilo is a framework that provides access to different sources of
multimedia content, using a pluggable system.
This package contains the core library and elements, as well as
general and API documentation.

%package vala
Summary:        Vala language bindings for Grilo framework
Group:          Development/Libraries

Requires:       %{name}-devel = %{version}-%{release}
Requires:       vala >= 0.7.2

%description vala
Grilo is a framework that provides access to different sources of
multimedia content, using a pluggable system.
This package contains the Vala language bindings.

%prep
%setup -q

# Fix vala detection for version 0.20
sed -i.vala 's/libvala-0.18/libvala-0.20/g' configure*

%build
%configure                      \
        --enable-vala           \
        --enable-gtk-doc        \
        --enable-introspection  \
        --enable-grl-net        \
        --disable-tests

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/grilo-%{release_version}/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/grilo-%{release_version}/plugins/

# Remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/grl-inspect-%{release_version}
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/grilo-test-ui-%{release_version}
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgrlnet-%{release_version}.so.*

# Remove files that will not be packaged
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_bindir}/grilo-simple-playlist

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING NEWS README TODO
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/*.typelib
%{_bindir}/grl-inspect-%{release_version}
%{_bindir}/grilo-test-ui-%{release_version}
%{_libdir}/grilo-%{release_version}/
%{_datadir}/grilo-%{release_version}/plugins/
%{_mandir}/man1/grl-inspect.1.gz

%files devel
%doc AUTHORS COPYING NEWS README TODO
%{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}-%{release_version}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir

%files vala
%doc AUTHORS COPYING NEWS README TODO
%{_datadir}/vala/vapi/*

%changelog
* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.2.5-1
- Update to 0.2.5

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 04 2012 Bastien Nocera <bnocera@redhat.com> 0.2.4-1
- Update to 0.2.4

* Tue Nov 13 2012 Kalev Lember <kalevlember@gmail.com> 0.2.3-1
- Update to 0.2.3

* Fri Oct 05 2012 Bastien Nocera <bnocera@redhat.com> 0.2.2-1
- Update to 0.2.2

* Wed Oct 03 2012 Bastien Nocera <bnocera@redhat.com> 0.2.1-1
- Update to 0.2.1

* Fri Aug 31 2012 Debarshi Ray <rishi@fedoraproject.org> 0.2.0-1
- update to 0.2.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Bastien Nocera <bnocera@redhat.com> 0.1.19-1
- Update to 0.1.19

* Wed Mar  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.18-3
- fix build with vala 0.15/0.16

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Bastien Nocera <bnocera@redhat.com> 0.1.18-1
- Update to 0.1.18

* Fri Oct 14 2011 Adam Williamson <awilliam@redhat.com> 0.1.17-1
- update to 0.1.17

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 0.1.16-1
- Update to 0.1.16

* Fri May 20 2011 Bastien Nocera <bnocera@redhat.com> 0.1.15-3
- Own the grilo plugins directories

* Wed Apr 27 2011 Bastien Nocera <bnocera@redhat.com> 0.1.15-2
- Update with review comments

* Thu Apr 21 2011 Bastien Nocera <bnocera@redhat.com> 0.1.15-1
- Fist package, based on upstream work by Juan A.
  Suarez Romero <jasuarez@igalia.com>

