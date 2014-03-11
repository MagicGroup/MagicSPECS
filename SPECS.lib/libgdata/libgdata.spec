Name:           libgdata
Version:        0.11.0
Release:        4%{?dist}
Summary:        Library for the GData protocol

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://live.gnome.org/libgdata
Source0:        http://download.gnome.org/sources/%{name}/0.11/%{name}-%{version}.tar.xz

BuildRequires:  glib2-devel libsoup-devel libxml2-devel gtk-doc intltool
BuildRequires:  libgnome-keyring-devel
BuildRequires:  gobject-introspection-devel liboauth-devel
Requires:       gobject-introspection

%description
libgdata is a GLib-based library for accessing online service APIs using the
GData protocol --- most notably, Google's services. It provides APIs to access
the common Google services, and has full asynchronous support.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       gtk-doc
Requires:       gobject-introspection-devel

# https://bugzilla.gnome.org/show_bug.cgi?id=610273
BuildRequires:  libtool

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang gdata


%check
# Only the general test can be run without network access
# Actually, the general test doesn't work either without gconf
#cd gdata/tests
#./general

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f gdata.lang
%doc COPYING NEWS README AUTHORS
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/GData-0.0.typelib

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/gtk-doc/html/gdata/
%{_datadir}/gir-1.0/GData-0.0.gir

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.11.0-4
- 为 Magic 3.0 重建

* Tue Jan 17 2012 Dan Horák <dan[at]danny.cz> - 0.11.0-3
- update BR

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 0.11.0-1
- Update to 0.11.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 0.10.1-1
- Update to 0.10.1

* Mon Jul 04 2011 Matthew Barnes <mbarnes@redhat.com> 0.9.1-1
- Update to 0.9.1

* Mon Jun 13 2011 Bastien Nocera <bnocera@redhat.com> 0.9.0-1
- Update to 0.9.0

* Fri May 20 2011 Bastien Nocera <bnocera@redhat.com> 0.8.1-1
- Update to 0.8.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Bastien Nocera <bnocera@redhat.com> 0.8.0-1
- Update to 0.8.0

* Mon Oct 18 2010 Bastien Nocera <bnocera@redhat.com> 0.7.0-1
- Update to 0.7.0

* Wed Sep 29 2010 jkeating - 0.6.4-6
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> - 0.6.4-5
- Rebuild with newer gobject-introspection
- Disable tests

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 0.6.4-4
- Rebuild with new gobject-introspection
- Drop gir-repository-devel

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 0.6.4-2
- Rebuild against new gobject-introspection

* Thu Apr 08 2010 Bastien Nocera <bnocera@redhat.com> 0.6.4-1
- Update to 0.6.4

* Wed Feb 17 2010 Bastien Nocera <bnocera@redhat.com> 0.6.1-2
- Rebuild to update F-13 tag

* Wed Feb 17 2010 Bastien Nocera <bnocera@redhat.com> 0.6.1-1
- Update to 0.6.1

* Mon Feb 15 2010 Bastien Nocera <bnocera@redhat.com> 0.6.0-1
- Update to 0.6.0
- Add introspection support

* Sun Nov 22 2009 Bastien Nocera <bnocera@redhat.com> 0.5.1-1
- Update to 0.5.1
- Fixes queries with non-ASCII characters

* Tue Sep 22 2009 Bastien Nocera <bnocera@redhat.com> 0.5.0-1
- Update to 0.5.0

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 0.4.0-3
- Fix source URL

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Bastien Nocera <bnocera@redhat.com> 0.4.0-1
- Update to 0.4.0

* Tue May 26 2009 Bastien Nocera <bnocera@redhat.com> 0.3.0-1
- Update to 0.3.0

* Sat Apr 25 2009 Bastien Nocera <bnocera@redhat.com> 0.2.0-1
- Update to 0.2.0

* Mon Apr 06 2009 - Bastien Nocera <bnocera@redhat.com> - 0.1.1-2
- Add check, snippet from Jason Tibbitts

* Wed Apr 01 2009 - Bastien Nocera <bnocera@redhat.com> - 0.1.1-1
- Update to 0.1.1

* Wed Apr 01 2009 - Bastien Nocera <bnocera@redhat.com> - 0.1.0-1
- First package

