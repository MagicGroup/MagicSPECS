Name:           goocanvas
Version:        1.0.0
Release:        3%{?dist}
Summary:        A new canvas widget for GTK+ that uses cairo for drawing

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://live.gnome.org/GooCanvas
Source0:        ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/1.0.0/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  pkgconfig, gettext, gtk2-devel
BuildRequires:  cairo-devel >= 1.4.0

%description
GooCanvas is a new canvas widget for GTK+ that uses the cairo 2D library for
drawing. It has a model/view split, and uses interfaces for canvas items and
views, so you can easily turn any application object into canvas items.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# remove static libraries and libtool droppings
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib%{name}.{a,la}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_libdir}/lib%{name}.so\.*

%package devel
Group:          Development/Libraries
Summary:        A new canvas widget for GTK+ that uses cairo for drawing
Requires:       %{name} = %{version}-%{release} pkgconfig

%description devel
GooCanvas is a new canvas widget for GTK+ that uses the cairo 2D library for
drawing. It has a model/view split, and uses interfaces for canvas items and
views, so you can easily turn any application object into canvas items.

These are the files used for development.

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}-1.0
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/gtk-doc/html/%{name}


%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1.0.0-3
- 为 Magic 3.0 重建

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.0.0-2
- Rebuild for new libpng

* Fri Feb 11 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 1.0.0-1
- Upstream 1.0.0 (final release !)
- Re-enable demos

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Apr 26 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 0.15-1
- Update to upstream 0.15

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 23 2009 Denis <denis@poolshark.org> - 0.14-1
- Update to upstream 0.14

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Denis Leroy <denis@poolshark.org> - 0.13-1
- Update to upstream 0.13
- Updated URLs to gnome.org

* Tue Sep 30 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.10-2
- demo application does not build; remove it

* Sun Jun 29 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.10-1
- v 0.10

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9-4
- Autorebuild for GCC 4.3

* Mon Aug 27 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.9-3
- don't explicitely require gtk2; no special versioning needed since FC6+

* Sun Aug 26 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.9-2
- require gtk2 not gtk2-devel (bz #254239)

* Sun Aug 19 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.9-1
- 0.9
- update license tag to LGPLv2+

* Sat May 05 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.6-2
- bump for incorrect tag in buildsys

* Mon Mar 19 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.6-1
- initial release
