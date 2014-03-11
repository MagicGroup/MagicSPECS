Name:		libgxim
Version:	0.3.3
Release:	7%{?dist}
License:	LGPLv2+
URL:		http://code.google.com/p/libgxim/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	intltool gettext ruby
BuildRequires:	dbus-devel > 0.23, dbus-glib-devel >= 0.74, glib2-devel >= 2.16, gtk2-devel
Source0:	http://libgxim.googlecode.com/files/%{name}-%{version}.tar.bz2
Patch0:		libgxim-fix-fontset.patch

Summary:	GObject-based XIM protocol library
Group:		System Environment/Libraries

%description
libgxim is a X Input Method protocol library that is implemented by GObject.
this library helps you to implement XIM servers or client applications to
communicate through XIM protocol without using Xlib API directly, particularly
if your application uses GObject-based main loop.

This package contains the shared library.

%package	devel
Summary:	Development files for libgxim
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	glib2-devel >= 2.16.0
Requires:	gtk2-devel

%description	devel
libgxim is a X Input Method protocol library that is implemented by GObject.
this library helps you to implement XIM servers or client applications to
communicate through XIM protocol without using Xlib API directly, particularly
if your application uses GObject-based main loop.

This package contains the development files to make any applications with
libgxim.

%prep
%setup -q
%patch0 -p0 -b 0-fontset


%build
%configure --disable-static --disable-rebuilds

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# clean up the unnecessary files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-, root, root, -)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/libgxim.so.*

%files	devel
%defattr(-, root, root, -)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/libgxim.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libgxim
%{_datadir}/gtk-doc/html/libgxim

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.3.3-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.3.3-5
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr  3 2009 Akira TAGOH <tagoh@redhat.com> - 0.3.3-2
- Fix an error message about FontSet.

* Thu Apr  2 2009 Akira TAGOH <tagoh@redhat.com> - 0.3.3-1
- New upstream release.
  - partly including a fix of freeze issue with switching (#488877)

* Tue Mar  3 2009 Akira TAGOH <tagoh@redhat.com> - 0.3.2-4
- Fix destroying a window unexpectedly. (#488223)

* Mon Mar  2 2009 Akira TAGOH <tagoh@redhat.com> - 0.3.2-3
- Backport a patch to fix the unknown event issue.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 13 2009 Akira TAGOH <tagoh@redhat.com> - 0.3.2-1
- New upstream release.

* Thu Oct 23 2008 Akira TAGOH <tagoh@redhat.com> - 0.3.1-1
- New upstream release.

* Tue Oct 14 2008 Akira TAGOH <tagoh@redhat.com> - 0.3.0-1
- New upstream release.
  - Have a workaround to avoid the race condition issue. (#452849)
  - Fix a freeze issue with ibus. (#465431)

* Wed Sep 17 2008 Akira TAGOH <tagoh@redhat.com> - 0.2.0-1
- New upstream release.
  - Fix discarding some packets when reconnecting.
  - Fix invalid memory access.

* Fri Aug 29 2008 Akira TAGOH <tagoh@redhat.com> - 0.1.1-1
- New upstream release.

* Thu Aug 28 2008 Akira TAGOH <tagoh@redhat.com> - 0.1.0-2
- clean up the spec file a bit.

* Mon Aug 25 2008 Akira TAGOH <tagoh@redhat.com> - 0.1.0-1
- Initial package.

