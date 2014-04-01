Name:          gupnp-dlna
Version:       0.10.2
Release:       2%{?dist}
Summary:       A collection of helpers for building UPnP AV applications

Group:         System Environment/Libraries
License:       LGPLv2+
URL:           http://www.gupnp.org/
Source0:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.10/%{name}-%{version}.tar.xz

BuildRequires: glib2-devel
BuildRequires: gobject-introspection-devel >= 1.36
BuildRequires: gssdp-devel
BuildRequires: gstreamer1-devel
BuildRequires: gstreamer1-plugins-base-devel
BuildRequires: gupnp-devel
BuildRequires: gupnp-av-devel
BuildRequires: libxml2-devel
BuildRequires: gtk-doc

%description
GUPnP is an object-oriented open source framework for creating UPnP
devices and control points, written in C using GObject and libsoup.
The GUPnP API is intended to be easy to use, efficient and flexible.

GUPnP-dlna is a collection of helpers for building DLNA (Digital 
Living Network Alliance) compliant applications using GUPnP.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Contains libraries and header files for developing applications that 
use %{name}.

%package docs
Summary: Development package for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description docs
Contains developer documentation for %{name}.

%prep
%setup -q

%build
%configure --disable-static

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README TODO
%{_bindir}/gupnp-dlna*
%{_libdir}/lib*.so.*
%{_libdir}/gupnp-dlna/libgstreamer.so
%{_libdir}/girepository-1.0/GUPnPDLNA-2.0.typelib
%{_libdir}/girepository-1.0/GUPnPDLNAGst-2.0.typelib
%{_datadir}/%{name}-2.0/

%files devel
%{_libdir}/lib*.so
%{_libdir}/gupnp-dlna/libgstreamer.so
%{_libdir}/pkgconfig/%{name}-2.0.pc
%{_libdir}/pkgconfig/%{name}-gst-2.0.pc
%{_libdir}/pkgconfig/%{name}-metadata-2.0.pc
%{_datadir}/gir-1.0/GUPnPDLNA-2.0.gir
%{_datadir}/gir-1.0/GUPnPDLNAGst-2.0.gir
%{_includedir}/%{name}-2.0/
%{_datadir}/vala/vapi/gupnp-dlna-*.*

%files docs
%{_datadir}/gtk-doc/html/%{name}
%{_datadir}/gtk-doc/html/%{name}-gst
%{_datadir}/gtk-doc/html/%{name}-metadata

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.2-1
- 0.10.2 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.10/gupnp-dlna-0.10.2.news

 * Wed Apr 10 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.1-1
- 0.10.1 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.10/gupnp-dlna-0.10.1.news

* Thu Feb 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.0-1
- 0.10.0 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.10/gupnp-dlna-0.10.0.news

* Thu Feb 14 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.5-1
- 0.9.5 devel release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.9/gupnp-dlna-0.9.5.news

* Sun Jan 27 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.4-1
- 0.9.4 devel release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.9/gupnp-dlna-0.9.4.news

* Sun Jan 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.3-1
- 0.9.3 devel release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.9/gupnp-dlna-0.9.3.news

* Fri Dec 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.2-1
- 0.9.2 devel release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.9/gupnp-dlna-0.9.2.news

* Thu Dec  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.1-1
- 0.9.1 devel release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.9/gupnp-dlna-0.9.1.news

* Sat Dec  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.0-1
- 0.9.0 devel release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.9/gupnp-dlna-0.9.0.news

* Wed Nov 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.0-1
- 0.7.0 devel release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.7/gupnp-dlna-0.7.0.news

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.6-1
- 0.6.6 stable release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.6/gupnp-dlna-0.6.6.news

* Mon Feb 13 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.5-1
- 0.6.5 stable release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.6/gupnp-dlna-0.6.5.news

* Mon Jan 23 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.4-3
- Enable introspection support - RHBZ 784125

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.4-1
- 0.6.4 stable release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.6/gupnp-dlna-0.6.4.news

* Fri Sep  2 2011 Zeeshan Ali <zeenix@redhat.com> - 0.6.3-1
- 0.6.3 stable release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.6/gupnp-dlna-0.6.3.news

* Sun Jul 17 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.2-1
- 0.6.2 stable release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-dlna/0.6/gupnp-dlna-0.6.2.news

* Sun Apr 10 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.1-1
- 0.6.1 stable release

* Sat Apr  9 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.0-1
- 0.6.0 stable release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 22 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.1-1
- New upstream 0.5.1 release

* Fri Jan  7 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.0-1
- New upstream 0.5.0 release

* Fri Oct 15 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.2-1
- New upstream 0.4.2 release

* Thu Oct 14 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.1-1
- New upstream 0.4.1 release

* Mon Sep 27 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.0-1
- New upstream 0.4.0 release

* Tue Aug 17 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.3.0-1
- New upstream 0.3.0 release

* Fri Jun 25 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.2.1-2
- Updated for review feedback

* Fri Jun 25 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.2.1-1
- Initial release
