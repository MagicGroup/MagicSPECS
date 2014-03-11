# Review at https://bugzilla.redhat.com/show_bug.cgi?id=549593

%global minorversion 0.1

Name:           tumbler
Version:        0.1.26
Release:        1%{?dist}
Summary:        D-Bus service for applications to request thumbnails

License:        GPLv2+ and LGPLv2+
Group:          Applications/System
URL:            http://git.xfce.org/xfce/tumbler/
#VCS git:git://git.xfce.org/xfce/tumbler
Source0:        http://archive.xfce.org/src/apps/tumbler/%{minorversion}/%{name}-%{version}.tar.bz2
BuildRequires:  dbus-glib-devel
BuildRequires:  freetype-devel
BuildRequires:  gettext
BuildRequires:  gtk2-devel >= 2.10.0
BuildRequires:  intltool
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  poppler-glib-devel
# extra thumbnailers
BuildRequires:  gstreamer-devel
%{?fedora:BuildRequires: libgsf-devel}
%{?fedora:BuildRequires: libopenraw-gnome-devel}


%description
Tumbler is a D-Bus service for applications to request thumbnails for various
URI schemes and MIME types. It is an implementation of the thumbnail
management D-Bus specification described on
http://live.gnome.org/ThumbnailerSpec written in an object-oriented fashion

Additional thumbnailers can be found in the tumbler-extras package


%package devel
Summary:       Development files for %{name}
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains libraries and header files for developing applications 
that use %{name}.

%prep
%setup -q


%build
%configure --disable-static

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' libtool

# Remove rpaths.
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1


%install
make install INSTALL="%{__install} -p" DESTDIR=%{buildroot}

find %{buildroot} -type f -name "*.la" -delete

%find_lang %{name}


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_datadir}/dbus-1/services/org.xfce.Tumbler.*.service
%{_libdir}/libtumbler-*.so.*

%dir %{_libdir}/%{name}-*
%{_libdir}/%{name}-*/tumblerd
%{_libdir}/tumbler-*/plugins/


%files devel
%defattr(-,root,root,-)
%{_libdir}/libtumbler-*.so
%{_libdir}/pkgconfig/%{name}-1.pc

%doc %{_datadir}/gtk-doc/

%dir %{_includedir}/%{name}-1
%{_includedir}/%{name}-1/tumbler

%changelog
* Sun Dec 09 2012 Kevin Fenzi <kevin@scrye.com> 0.1.26-1
- Update to 0.1.26

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 16 2012 Marek Kasik <mkasik@redhat.com> - 0.1.25-2
- Rebuild (poppler-0.20.0)

* Sun Apr 29 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.25-1
- Update to 0.1.25 (Xfce 4.10 final)
- Add VCS key

* Tue Apr 03 2012 Kevin Fenzi <kevin@scrye.com> - 0.1.24-1
- Update to 0.1.24

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 08 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.23-1
- Update to 0.1.23

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.1.22-5
- Rebuild for new libpng

* Sun Oct 16 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.22-4
- Fix thumbnail generation of the GStreamer plugin (#746110)
- Fix ownership race conditions when started twice (bugzilla.xfce.org #8001)

* Fri Sep 30 2011 Marek Kasik <mkasik@redhat.com> - 1.22-3
- Rebuild (poppler-0.18.0)

* Wed Sep 21 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.22-2
- Build the new GStreamer video thumbnailer

* Wed Sep 21 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.22-1
- Update to 1.22

* Mon Sep 19 2011 Marek Kasik <mkasik@redhat.com> - 1.21-3
- Rebuild (poppler-0.17.3)

* Fri Jul 15 2011 Marek Kasik <mkasik@redhat.com> - 1.21-2
- Rebuild (poppler-0.17.0)

* Mon Feb 14 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.21-1
- Update to 1.21

* Sat Feb 12 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.20-1
- Update to 1.20

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 0.1.6-1
- Update to 0.1.6

* Sun Dec 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.5-1
- Update to 0.1.5

* Thu Nov 18 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.4-1
- Update to 0.1.4

* Wed Nov 03 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3
- Enable PDF thumbnails (BR poppler-glib-devel)

* Sat Jul 17 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2
- Own %%{_datadir}/gtk-doc/{html/} (#604169)
- Include NEWS in %%doc

* Thu Feb 25 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.1-2
- Fix thumbnail support by including necessary BR's

* Fri Jan 15 2010 Debarshi Ray <rishi@fedoraproject.org> - 0.1.1-1
- Version bump to 0.1.1.
  * New fast JPEG thumbnailer with EXIF support
  * Report unsupported flavors back to clients via error signals
  * Translation updates: Swedish, Catalan, Galician, Japanese, Danish,
    Portuguese, Chinese
- Added 'BuildRequires: gtk2-devel'.
- Use sed instead of chrpath to remove rpaths. Remove 'BuildRequires: chrpath'.

* Tue Dec 22 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.0-2
- Updated spec for review

* Sun Dec 20 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.1.0-1
- Initial build.
