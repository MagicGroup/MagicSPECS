# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

%define with_gtk3 1

#define _version_suffix -f256

Name:           spice-gtk
Version:	0.30
Release:	2%{?dist}
Summary:        A GTK+ widget for SPICE clients
Summary(zh_CN.UTF-8): SPICE 客户端的 GTK+ 部件

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://spice-space.org/page/Spice-Gtk
#VCS:           git:git://anongit.freedesktop.org/spice/spice-gtk
Source0:        http://www.spice-space.org/download/gtk/%{name}-%{version}%{?_version_suffix}.tar.bz2

BuildRequires: intltool
BuildRequires: gtk2-devel >= 2.14
BuildRequires: usbredir-devel >= 0.5.2
BuildRequires: libusb1-devel >= 1.0.9
BuildRequires: libgudev1-devel
BuildRequires: perl-Text-CSV
BuildRequires: pixman-devel openssl-devel libjpeg-turbo-devel
BuildRequires: celt051-devel pulseaudio-libs-devel
BuildRequires: pygtk2-devel python-devel zlib-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libcacard-devel
BuildRequires: gobject-introspection-devel
BuildRequires: libacl-devel
BuildRequires: polkit-devel
BuildRequires: gtk-doc
BuildRequires: vala-tools
BuildRequires: usbutils
%if %{with_gtk3}
BuildRequires: gtk3-devel
%endif
# FIXME: should ship the generated files..
BuildRequires: pyparsing
# keep me to get gendeps magic happen
BuildRequires: spice-protocol >= 0.12.10
# Hack because of bz #613466
BuildRequires: libtool
Requires: spice-glib%{?_isa} = %{version}-%{release}

%description
Client libraries for SPICE desktop servers.

%description -l zh_CN.UTF-8
SPICE 客户端的 GTK+ 部件。

%package devel
Summary: Development files to build GTK2 applications with spice-gtk-2.0
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: spice-glib-devel%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk2-devel

%description devel
spice-client-gtk-2.0 provides a SPICE viewer widget for GTK2.

Libraries, includes, etc. to compile with the spice-gtk2 libraries

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package -n spice-glib
Summary: A GObject for communicating with Spice servers
Group: Development/Libraries

%description -n spice-glib
spice-client-glib-2.0 is a SPICE client library for GLib2.

%package -n spice-glib-devel
Summary: Development files to build Glib2 applications with spice-glib-2.0
Group: Development/Libraries
Requires: spice-glib%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: glib2-devel

%description -n spice-glib-devel
spice-client-glib-2.0 is a SPICE client library for GLib2.

Libraries, includes, etc. to compile with the spice-glib-2.0 libraries


%if %{with_gtk3}
%package -n spice-gtk3
Summary: A GTK3 widget for SPICE clients
Group: Development/Libraries
Requires: spice-glib%{?_isa} = %{version}-%{release}

%description -n spice-gtk3
spice-client-glib-3.0 is a SPICE client library for Gtk3.

%package -n spice-gtk3-devel
Summary: Development files to build GTK3 applications with spice-gtk-3.0
Group: Development/Libraries
Requires: spice-gtk3%{?_isa} = %{version}-%{release}
Requires: spice-glib-devel%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk3-devel

%description -n spice-gtk3-devel
spice-client-gtk-3.0 provides a SPICE viewer widget for GTK3.

Libraries, includes, etc. to compile with the spice-gtk3 libraries

%package -n spice-gtk3-vala
Summary: Vala bindings for the spice-gtk-3.0 library
Group: Development/Libraries
Requires: spice-gtk3%{?_isa} = %{version}-%{release}
Requires: spice-gtk3-devel%{?_isa} = %{version}-%{release}

%description -n spice-gtk3-vala
A module allowing use of the spice-gtk-3.0 widget from vala
%endif

%package python
Summary: Python bindings for the spice-gtk-2.0 library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description python
SpiceClientGtk module provides a SPICE viewer widget for GTK2.

A module allowing use of the spice-gtk-2.0 widget from python

%package tools
Summary: Spice-gtk tools
Group: Applications/Internet
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Simple clients for interacting with SPICE servers.
spicy is a client to a SPICE desktop server.
snappy is a tool to capture screen-shots of a SPICE desktop.


%prep
%setup -q -n spice-gtk-%{version}%{?_version_suffix} -c

if [ -n '%{?_version_suffix}' ]; then
  mv spice-gtk-%{version}%{?_version_suffix} spice-gtk-%{version}
fi

#pushd spice-gtk-%{version}
#popd

%if %{with_gtk3}
cp -a spice-gtk-%{version} spice-gtk3-%{version}
%endif


%build

cd spice-gtk-%{version}
%configure --with-gtk=2.0 --enable-gtk-doc --with-usb-acl-helper-dir=%{_libexecdir}/spice-gtk-%{_arch}/
make %{?_smp_mflags}
cd ..

%if %{with_gtk3}
cd spice-gtk3-%{version}
%configure --with-gtk=3.0 --enable-vala --with-usb-acl-helper-dir=%{_libexecdir}/spice-gtk-%{_arch}/
make %{?_smp_mflags}
cd ..
%endif


%install

%if %{with_gtk3}
cd spice-gtk3-%{version}
make install DESTDIR=%{buildroot}
cd ..
%endif

cd spice-gtk-%{version}
make install DESTDIR=%{buildroot}
cd ..

rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.a
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.la

# needed because of the upstream issue described in
# http://lists.freedesktop.org/archives/spice-devel/2012-August/010343.html
# these are unwanted spice-protocol files
rm -rf %{buildroot}%{_includedir}/spice-1
rm -rf %{buildroot}%{_datadir}/pkgconfig/spice-protocol.pc

%find_lang %{name}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n spice-glib -p /sbin/ldconfig
%postun -n spice-glib -p /sbin/ldconfig

%if %{with_gtk3}
%post -n spice-gtk3 -p /sbin/ldconfig
%postun -n spice-gtk3 -p /sbin/ldconfig
%endif


%files
%doc spice-gtk-%{version}/AUTHORS
%doc spice-gtk-%{version}/COPYING
%doc spice-gtk-%{version}/README
%doc spice-gtk-%{version}/NEWS
%{_libdir}/libspice-client-gtk-2.0.so.*
%{_libdir}/girepository-1.0/SpiceClientGtk-2.0.typelib

%files devel
%{_libdir}/libspice-client-gtk-2.0.so
%{_includedir}/spice-client-gtk-2.0
%{_libdir}/pkgconfig/spice-client-gtk-2.0.pc
%{_datadir}/gir-1.0/SpiceClientGtk-2.0.gir

%files -n spice-glib -f %{name}.lang
%{_libdir}/libspice-client-glib-2.0.so.*
%{_libdir}/libspice-controller.so.*
%{_libdir}/girepository-1.0/SpiceClientGLib-2.0.typelib
%{_libexecdir}/spice-gtk-%{_arch}/spice-client-glib-usb-acl-helper
%{_datadir}/polkit-1/actions/org.spice-space.lowlevelusbaccess.policy

%files -n spice-glib-devel
%{_libdir}/libspice-client-glib-2.0.so
%{_libdir}/libspice-controller.so
%{_includedir}/spice-client-glib-2.0
%{_includedir}/spice-controller/*
%{_libdir}/pkgconfig/spice-client-glib-2.0.pc
%{_libdir}/pkgconfig/spice-controller.pc
%{_datadir}/gir-1.0/SpiceClientGLib-2.0.gir
%{_datadir}/vala/vapi/spice-protocol.vapi
%doc %{_datadir}/gtk-doc/html/*

%if %{with_gtk3}
%files -n spice-gtk3
%{_libdir}/libspice-client-gtk-3.0.so.*
%{_libdir}/girepository-1.0/SpiceClientGtk-3.0.typelib

%files -n spice-gtk3-devel
%{_libdir}/libspice-client-gtk-3.0.so
%{_includedir}/spice-client-gtk-3.0
%{_libdir}/pkgconfig/spice-client-gtk-3.0.pc
%{_datadir}/gir-1.0/SpiceClientGtk-3.0.gir

%files -n spice-gtk3-vala
%{_datadir}/vala/vapi/spice-client-glib-2.0.deps
%{_datadir}/vala/vapi/spice-client-glib-2.0.vapi
%{_datadir}/vala/vapi/spice-client-gtk-3.0.deps
%{_datadir}/vala/vapi/spice-client-gtk-3.0.vapi
%endif

%files python
%{_libdir}/python*/site-packages/SpiceClientGtk.so

%files tools
#{_bindir}/snappy
%{_bindir}/spicy
%{_bindir}/spicy-stats
%{_bindir}/spicy-screenshot
%{_mandir}/man1/spice-client.1*

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.30-2
- 为 Magic 3.0 重建

* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 0.30-1
- 更新到 0.30

* Fri Dec 21 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.15-2
- Update to spice-gtk 0.15

* Thu Oct 25 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.14-2
- Add various upstream patches

* Fri Sep 21 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.14-1
- Update to 0.14 release

* Fri Sep 14 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.13.29-4
- Add patch fixing CVE 2012-4425

* Thu Sep 13 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.13.29-3
- Run autoreconf after applying patch 2 as it only modifies Makefile.am

* Tue Sep 11 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.13.29-2
- Add patch to fix symbol versioning

* Fri Sep  7 2012 Hans de Goede <hdegoede@redhat.com> - 0.13.29-1
- Update to the spice-gtk 0.13.29 development release
- Rebuild for new usbredir

* Mon Sep 03 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.13-2
- Update to spice-gtk 0.13

* Tue Aug 07 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.12.101-1
- Update to the spice-gtk 0.12.101 development release (needed by Boxes
  3.5.5)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.12-4
- re-Add back spice-protocol BuildRequires to help some deps magic happen

* Thu May 10 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.12-3
- Fix Spice.Audio constructor Python binding
  https://bugzilla.redhat.com/show_bug.cgi?id=820335

* Wed May  2 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.12-2
- Fix virt-manager console not showing up, rhbz#818169

* Tue Apr 24 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.12-1
- New upstream release 0.12

* Tue Apr 10 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.11-5
- Fix build on PPC
- Remove ExclusiveArch. While spice-gtk will build on ARM and PPC, it
  hasn't been tested on these arch, so there may be some bugs.

* Tue Mar 20 2012 Hans de Goede <hdegoede@redhat.com> - 0.11-4
- Add missing BuildRequires: usbutils, so that we get proper USB device
  descriptions in the USB device selection menu

* Wed Mar 14 2012 Hans de Goede <hdegoede@redhat.com> - 0.11-3
- Fix a crash triggered when trying to view a usbredir enabled vm from
  virt-manager

* Mon Mar 12 2012 Hans de Goede <hdegoede@redhat.com> - 0.11-2
- Add back spice-protocol BuildRequires to help some deps magic happen

* Fri Mar  9 2012 Hans de Goede <hdegoede@redhat.com> - 0.11-1
- New upstream release 0.11
- Fix multilib conflict in spice-glib

* Thu Feb 23 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.10-1
- New upstream release 0.10

* Mon Jan 30 2012 Hans de Goede <hdegoede@redhat.com> - 0.9-1
- New upstream release 0.9

* Mon Jan 16 2012 Hans de Goede <hdegoede@redhat.com> - 0.8-1
- New upstream release 0.8
- Various small specfile improvements
- Enable vala bindings

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> 0.7.39-2
- Rebuild to break bogus libpng dependency
- Fix summaries for gtk3 subpackages to not talk about gtk2

* Fri Sep  2 2011 Hans de Goede <hdegoede@redhat.com> - 0.7.39-1
- Update to git snapshot 0.7.39-ab64, to add usbredir support

* Tue Jul 26 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7.1-1
- Upstream version 0.7.1-d5a8 (fix libtool versionning)

* Tue Jul 19 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7-1
- Upstream release 0.7

* Wed May 25 2011 Christophe Fergeau <cfergeau@redhat.com> - 0.6-1
- Upstream release 0.6

* Tue Mar  1 2011 Hans de Goede <hdegoede@redhat.com> - 0.5-6
- Fix spice-glib requires in .pc file (#680314)

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 0.5-5
- Fix build against glib 2.28

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.5-4
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.5-2
- Rebuild against newer gtk

* Thu Jan 27 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.5-1
- Upstream release 0.5

* Fri Jan 14 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4-2
- Add support for parallel GTK3 build

* Mon Jan 10 2011 Dan Horák <dan[at]danny.cz> - 0.4-2
- add ExclusiveArch as only x86 is supported

* Sun Jan 09 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.4-1
- Upstream release 0.4
- Initial release (#657403)

* Thu Nov 25 2010 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.1.0-1
- Initial packaging
