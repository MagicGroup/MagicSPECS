Name:           caribou
Version:	0.4.19
Release:        4%{?dist}
Summary:        A simplified in-place on-screen keyboard
License:        LGPLv2+
URL:            http://live.gnome.org/Caribou
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.gnome.org/sources/caribou/%{majorver}/caribou-%{version}.tar.xz
Patch0:         caribou-0.4.8-multilib.patch

BuildRequires:  python2-devel
BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel
BuildRequires:  pygobject3-devel
BuildRequires:  intltool
BuildRequires:  gnome-doc-utils
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  clutter-devel
BuildRequires:  vala-devel
BuildRequires:  libXtst-devel
BuildRequires:  libxklavier-devel
BuildRequires:  libgee-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  at-spi2-core-devel

Requires:       python-%{name} = %{version}-%{release}
Requires:       gobject-introspection
Requires:       caribou-gtk2-module
Requires:       caribou-gtk3-module

#Following is needed as package moved from noarch to arch
Obsoletes:      caribou < 0.4.1-3
# Obsolete retired 'gok' to make sure it gets removed with distro upgrade
Obsoletes:      gok < 2.30.1-6

%description
Caribou is a text entry application that currently manifests itself as
a simplified in-place on-screen keyboard.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Obsolete retired 'gok' to make sure it gets removed with distro upgrade
Obsoletes:      gok-devel < 2.30.1-6

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package     -n python-caribou
Summary:        Keyboard UI for %{name}
Requires:       pygobject3
Requires:       pyatspi
Requires:       %{name} = %{version}-%{release}
Obsoletes:      caribou < 0.4.1-3
BuildArch:      noarch

%description  -n python-caribou
This package contains caribou python GUI

%package        gtk2-module
Summary:        Gtk2 module for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      caribou < 0.4.1-3

%description    gtk2-module
This package contains caribou module for gtk2 applications.

%package        gtk3-module
Summary:        Gtk3 module for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      caribou < 0.4.1-3

%description    gtk3-module
This package contains caribou module for gtk3 applications.

%package        antler
Summary:        Keyboard implementation for %{name}
Requires:       python-%{name} = %{version}-%{release}
Obsoletes:      caribou < 0.4.1-3

%description    antler
This package contains caribou keyboard implementation for
non-gnome-shell sessions.

%prep
%setup -q
%patch0 -p1 -b .multilib

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/caribou-autostart.desktop || :
desktop-file-validate $RPM_BUILD_ROOT%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/caribou-gtk-module.desktop || :

%find_lang caribou

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%postun antler
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans antler
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f caribou.lang
%doc NEWS COPYING README
#%{_bindir}/caribou
%{_bindir}/caribou-preferences
%{_datadir}/caribou
%{_libdir}/girepository-1.0/Caribou-1.0.typelib
%{_libexecdir}/caribou
%{_datadir}/dbus-1/services/org.gnome.Caribou.Daemon.service
%{_sysconfdir}/xdg/autostart/caribou-autostart.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.caribou.gschema.xml
%{_libdir}/libcaribou.so.0*
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/caribou-gtk-module.desktop

%files -n python-caribou
%{python_sitelib}/caribou

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/caribou-1.0.pc
%{_datadir}/gir-1.0/Caribou-1.0.gir
%{_datadir}/vala

%files gtk2-module
%{_libdir}/gtk-2.0/modules/libcaribou-gtk-module.so

%files gtk3-module
%{_libdir}/gtk-3.0/modules/libcaribou-gtk-module.so

%files antler
%{_datadir}/antler
%{_datadir}/dbus-1/services/org.gnome.Caribou.Antler.service
%{_libexecdir}/antler-keyboard
%{_datadir}/glib-2.0/schemas/org.gnome.antler.gschema.xml


%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 0.4.19-4
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.4.19-3
- 更新到 0.4.19

* Fri Mar 07 2014 Liu Di <liudidi@gmail.com> - 0.4.13-2
- 更新到 0.4.13

* Sun Apr 28 2013 Liu Di <liudidi@gmail.com> - 0.4.10-2
- 为 Magic 3.0 重建

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 0.4.10-1
- Update to 0.4.10

* Mon Mar 04 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.4.9-1
- Update to 0.4.9

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 0.4.8-2
- Rebuilt for cogl soname bump

* Tue Feb 19 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.4.8-1
- Update to 0.4.8

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.4.7-2
- vala .vapi and .deps files should be installed by -devel

* Wed Jan 16 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.4.7-1
- Update to 0.4.7

* Thu Dec 20 2012 Parag Nemade <pnemade AT redhat DOT com> - 0.4.6-1
- Update to 0.4.6

* Tue Dec 18 2012 Parag Nemade <pnemade AT redhat DOT com> - 0.4.5-1
- Update to 0.4.5
- Resolves:rh#744852 - Pressing | in on-screen keyboard produces <
- Resolves:rh#880379 - Another service acquired %%s, quitting..
- Resolves:rh#880382

* Wed Nov 21 2012 Parag Nemade <pnemade AT redhat DOT com> - 0.4.4.2-6
- Resolves:rh#878716 - need some spec cleanup

* Thu Nov 15 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.4.2-5
- Apply patch1

* Tue Nov 13 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.4.2-4
- Patch from Rui Matos for exec python in shell shim scripts

* Tue Nov 13 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.4.2-3
- Fix multilib patch

* Tue Nov 13 2012 Rui Matos <tiagomatos@gmail.com> - 0.4.4.2-2
- Fix dependencies, caribou and antler both need python-caribou

* Tue Nov 13 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.4.2-1
- Update to 0.4.4.2 release

* Thu Sep 06 2012 Richard Hughes <hughsient@gmail.com> - 0.4.4-1
- Update to 0.4.4

* Wed Jul 25 2012 Kalev Lember <kalevlember@gmail.com> - 0.4.3-3
- Correct the obsoletes

* Tue Jul 24 2012 Kalev Lember <kalevlember@gmail.com> - 0.4.3-2
- Obsolete gok

* Thu Jul 19 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.3-1
- Update to 0.4.3 release

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 27 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.2-1
- Update to 0.4.2 release

* Tue Feb 07 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.1-5
- Resolves:rh#768033 - Update Requires for caribou

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Parag Nemade <pnemade AT redhat.com> - 0.4.1-3
- split package to subpackages -gtk2-module, -gtk3-module, -antler and python-caribou

* Thu Nov 17 2011 Parag Nemade <pnemade AT redhat.com> - 0.4.1-2
- Resolves:rh#753149 - Upgraded F15 -> F16 gnome fails - wrong version of caribou

* Tue Oct 18 2011 Parag Nemade <pnemade AT redhat.com> - 0.4.1-1
- upstream release 0.4.1

* Tue Sep 27 2011 Parag Nemade <pnemade AT redhat.com> - 0.4.0-1
- upstream release 0.4.0

* Tue Sep 20 2011 Parag Nemade <pnemade AT redhat.com> - 0.3.92-1
- upstream release 0.3.92

* Tue Sep 06 2011 Parag Nemade <pnemade AT redhat.com> - 0.3.91-1
- Update to new upstream release 0.3.91

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> - 0.3.5-2
- Rebuild with pygobject3

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> - 0.3.5-1
- Update to 0.3.5

* Tue Jul 05 2011 Parag Nemade <pnemade AT redhat.com> - 0.3.3-1
- Update to new upstream release 0.3.3

* Thu Jun 16 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.3.2-2
- Tweak BuildRequires

* Tue Jun 14 2011 Parag Nemade <pnemade AT redhat.com> - 0.3.2-1
- Update to new upstream release 0.3.2

* Fri May  6 2011 Christopher Aillon <caillon@redhat.com> - 0.2.00-3
- Update scriptlets per packaging guidelines

* Thu May 05 2011 Parag Nemade <pnemade AT redhat.com> - 0.2.00-2
- Caribou now only be shown in GNOME. (rh#698603)
- Add desktop-file-validate for caribou-autostart.desktop
- Add ||: for caribou-autostart.desktop to skip the error.

* Tue Apr  5 2011 Matthias Clasen <mclasen@redhat.com> - 0.2.00-1
- Update to 0.2.00

* Tue Mar 22 2011 Parag Nemade <pnemade AT redhat.com> - 0.1.92-1
- Update to 0.1.92

* Thu Mar 10 2011 Parag Nemade <pnemade AT redhat.com> - 0.1.91-1
- Update to 0.1.91

* Thu Mar 10 2011 Parag Nemade <pnemade AT redhat.com> - 0.1.7-1
- Update to 0.1.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.5-1
- Update to 0.1.5

* Wed Jun 16 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.2-3
- Require pyatspi, not at-spi-python

* Sat May 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.2-2
- Rewrite spec for autotools

* Fri May 28 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.2-1
- Update to 0.1.2

* Wed Jan 21 2009 Ben Konrath <ben@bagu.org> - 0.0.2-1
- Initial release.
