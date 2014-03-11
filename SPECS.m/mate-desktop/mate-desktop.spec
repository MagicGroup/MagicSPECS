Summary:	Shared code among gnome-panel, gnome-session, nautilus, etc
Name:		mate-desktop
Version:	1.4.1
Release:	13%{?dist}
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz

License:    GPLv2+ and LGPLv2+ and MIT
Group:		System Environment/Libraries

BuildRequires: mate-common
BuildRequires: mate-conf-devel
BuildRequires: startup-notification-devel
BuildRequires: mate-doc-utils
BuildRequires: unique-devel
BuildRequires: desktop-file-utils

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	magic-menus
Requires:	pygtk2
#To avoid confusion with the packagegroup and make sure this package pulls all the runtime requirements
Requires:	mate-window-manager mate-session-manager libmateweather mate-corba mate-conf mate-control-center mate-settings-daemon

%description
The mate-desktop package contains an internal library
(libmatedesktop) used to implement some portions of the MATE
desktop, and also some data files and other shared components of the
MATE user environment.

%package libs
Summary: Shared libraries for libmate-desktop
License: LGPLv2+
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description libs
Shared libraries for libmate-desktop

%package devel
Summary: Libraries and headers for libmate-desktop
License: LGPLv2+
Group: Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Libraries and header files for the MATE-internal private library
libmatedesktop.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh


%build

%configure \
	--disable-libtool-lock	\
	--disable-scrollkeeper	\
	--disable-static	\
	--with-pnp-ids-path="%{_datadir}/hwdata/pnp.ids"	\
	--enable-unique	\
	--enable-gtk-doc

make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# stuff we don't want
#rm -rf $RPM_BUILD_ROOT/var/scrollkeeper

# to avoid conflicts with gnome
mkdir $RPM_BUILD_ROOT%{_datadir}/omf/mate
mv -f $RPM_BUILD_ROOT%{_datadir}/omf/{fdl,gpl,lgpl} $RPM_BUILD_ROOT%{_datadir}/omf/mate
magic_rpm_clean.sh
%find_lang %{name} --all-name

%files -f %{name}.lang
%doc AUTHORS COPYING COPYING.LIB NEWS README
%{_datadir}/applications/mate-about.desktop
%doc %{_mandir}/man1/mate-about.1*
# GPL
%{_bindir}/mate-about
# LGPL
%{_datadir}/mate/help/*/*/*.xml
%{_datadir}/omf/mate/
%{_datadir}/mate-about/

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
# LGPL
%{_libdir}/libmate-desktop-2.so.*

%files devel
%{_libdir}/libmate-desktop-2.so
%{_libdir}/pkgconfig/mate-desktop-2.0.pc
%{_includedir}/mate-desktop-2.0/
%doc %{_datadir}/gtk-doc/html/mate-desktop


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.1-13
- 为 Magic 3.0 重建

* Wed Oct 17 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.1-12
- Add runtime requirements to avoid confusion

* Wed Sep 19 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.4.1-11
- drop problematic bg-crossfade patch (breaks mate-settings-daemon)
- remove .desktop Only-Show-In mods

* Sun Aug 12 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.1-10
- fix deps wrt -libs subpkg

* Sat Aug 11 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-9
- add isa tag to -libs

* Sat Aug 11 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-8
- change file section for own directories
- change 'to avoid conflicts with gnome' part
- add libs subpackage for shared libraries

* Fri Aug 03 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-7
- add desktop file install for mate-about.desktop
- add BuildRequires desktop-file-utils
- remove BuildRequires intltool gtk-doc

* Fri Aug 03 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-6
- start initial for fedora
- remove unnecessary buildRequires
- Drop pycairo from Requires
- change --with-pnp-ids-path="/usr/share/hwdata/pnp.ids" to
- --with-pnp-ids-path="%%{_datadir}/hwdata/pnp.ids"

* Sun Dec 25 2011 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.0-1
- mate-desktop.spec based on gnome-desktop-2.32.0-9.fc16 spec
