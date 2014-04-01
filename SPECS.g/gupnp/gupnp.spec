Name:          gupnp
Version:       0.20.10
Release:       1%{?dist}
Summary:       A framework for creating UPnP devices & control points

Group:         System Environment/Libraries
License:       LGPLv2+
URL:           http://www.gupnp.org/
Source0:       http://download.gnome.org/sources/%{name}/0.20/%{name}-%{version}.tar.xz

BuildRequires: gssdp-devel >= 0.14.0
BuildRequires: gtk-doc
BuildRequires: gobject-introspection-devel >= 1.36
BuildRequires: libsoup-devel
BuildRequires: libxml2-devel
BuildRequires: libuuid-devel
BuildRequires: NetworkManager-devel

Requires: dbus

%description
GUPnP is an object-oriented open source framework for creating UPnP 
devices and control points, written in C using GObject and libsoup. 
The GUPnP API is intended to be easy to use, efficient and flexible. 

%package devel
Summary: Development package for gupnp
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel
Requires: gssdp-devel
Requires: libsoup-devel
Requires: libxml2-devel
Requires: libuuid-devel
Requires: pkgconfig
Obsoletes: gupnp-vala

%description devel
Files for development with %{name}.

%package docs
Summary: Documentation files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description docs
This package contains developer documentation for %{name}.

%prep
%setup -q

%build
%configure --disable-static --with-context-manager=network-manager
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README
%{_libdir}/libgupnp-1.0.so.*
%{_bindir}/gupnp-binding-tool
%{_libdir}/girepository-1.0/GUPnP-1.0.typelib

%files devel
%{_libdir}/pkgconfig/gupnp-1.0.pc
%{_libdir}/libgupnp-1.0.so
%{_includedir}/gupnp-1.0
%{_datadir}/gir-1.0/GUPnP-1.0.gir
%{_datadir}/vala/vapi/gupnp-1.0.*

%files docs
%doc %{_datadir}/gtk-doc/html/%{name}

%changelog
* Tue Feb  4 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.10-1
- 0.20.10 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.10.news

* Sun Dec 15 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.9-1
- 0.20.9 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.9.news

* Sun Nov  3 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.8-1
- 0.20.8 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.8.news

* Wed Oct 16 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.7-1
- 0.20.7 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.7.news

* Mon Sep  9 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.6-1
- 0.20.6 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.6.news

* Wed Aug 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.5-1
- 0.20.5 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.5.news

* Tue Jul 30 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.4-1
- 0.20.4 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.4.news

* Thu May 30 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.3-1
- 0.20.3 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.3.news

* Sat Apr 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.2-1
- 0.20.2 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.2.news

* Tue Mar  5 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.1-1
- 0.20.1 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.1.news

* Thu Feb 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.0-2
- Obsolete gupnp-vala

* Thu Feb 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.0-2
- bump

* Thu Feb 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.0-1
- 0.20.0 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.0.news

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.4-1
- 0.19.4 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.19/gupnp-0.19.4.news

* Thu Dec  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.3-1
- 0.19.3 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.19/gupnp-0.19.3.news

* Sat Dec  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.2-1
- 0.19.2 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.19/gupnp-0.19.2.news

* Mon Oct 29 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.1-1
- 0.19.1 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.19/gupnp-0.19.1.news

* Sun Oct  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.19.0-1
- 0.19.0 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.19/gupnp-0.19.0.news

* Sun Aug 19 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.18.4-1
- 0.18.4 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.18/gupnp-0.18.4.news

* Mon Aug 13 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.18.3-3
- Use NetworkManager for connectivity detection

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.18.3-1
- 0.18.3 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.18/gupnp-0.18.3.news

* Thu Apr 26 2012 Zeeshan Ali <zeenix@redhat.com> - 0.18.2-2
- Remove bogus dependency on libgdbus-devel.

* Sun Mar 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.18.2-1
- 0.18.2 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.18/gupnp-0.18.2.news

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 10 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.18.1-1
- 0.18.1 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.18/gupnp-0.18.1.news

* Mon Sep  5 2011 Zeeshan Ali <zeenix@redhat.com> - 0.18.0-2
- Push a new release to build against latest gssdp.

* Fri Sep  2 2011 Zeeshan Ali <zeenix@redhat.com> - 0.18.0-1
- 0.18.0 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.18/gupnp-0.18.0.news

* Fri Aug  5 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.17.2-1
- 0.17.2 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.17/gupnp-0.17.2.news

* Sun Jul 17 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.17.1-1
- 0.17.1 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.17/gupnp-0.17.1.news

* Thu Jun 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.17.0-1
- 0.17.0 release

* Sun May  1 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.16.1-1
- 0.16.1 stable release

* Sat Apr  9 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.16.0-1
- 0.16.0 stable release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.15.1-1
- Update to 0.15.1

* Tue Nov 30 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.15.0-1
- Update to 0.15.0

* Wed Sep 29 2010 jkeating - 0.14.0-3
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> 0.14.0-2
- Rebuild against newer gobject-introspection

* Fri Sep 17 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.0-1
- Update to 0.14.0

* Tue Aug 17 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.5-2
- Update source URL

* Sat Aug 14 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.5-1
- Update to 0.13.5

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 0.13.4-4
- Rebuild with new gobject-introspection

* Mon Jun 21 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.4-2
- Add patch to fix build

* Mon Jun 21 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.4-1
- Update to 0.13.4

* Fri Apr  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.3-4
- Once more with feeling!

* Fri Apr  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.3-3
- add back missing line to spec

* Fri Apr  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.3-2
- bump build

* Fri Apr  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.3-1
- Update to 0.13.3

* Mon Mar  1 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.2-2
- Add patch to fix DSO linking. Fixes bug 564855

* Fri Dec  4 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.2-1
- Update to 0.13.2

* Wed Oct  7 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.1-1
- Update to 0.13.1

* Thu Sep 17 2009 Bastien Nocera <bnocera@redhat.com> 0.13.0-1
- Update to 0.13.0

* Mon Aug 31 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.8-4
- some spec file cleanups, depend on libuuid instead of e2fsprogs-devel

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  1 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.8-2
- Rebuild with new libuuid build req

* Wed Jun  3 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.8-1
- New upstream release

* Mon Apr 27 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.7-1
- New upstream release

* Wed Mar  4 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.6-4
- Move docs to noarch sub package

* Mon Mar  2 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.6-3
- Add some extra -devel Requires packages

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.6-1
- New upstream release

* Wed Jan 14 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.5-1
- New upstream release

* Thu Dec 18 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.4-3
- Add gtk-doc build req

* Sat Nov 22 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.4-2
- Fix summary

* Mon Nov 17 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.4-1
- New upstream release

* Mon Oct 27 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.3-1
- New upstream release

* Mon Oct 20 2008 Colin Walters <walters@verbum.org> 0.12.2-2
- devel package requires gssdp-devel

* Sun Aug 31 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.2-1
- New upstream release

* Thu Aug 28 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-7
- Yet again. Interesting it builds fine in mock and not koji

* Thu Aug 28 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-6
- Once more with feeling

* Thu Aug 28 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-5
- Second go

* Thu Aug 28 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-4
- Fix build on rawhide

* Wed Aug 13 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-3
- Fix changelog entries

* Wed Aug 13 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-2
- Fix a compile issue on rawhide

* Mon Jun 16 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-1
- Initial release
