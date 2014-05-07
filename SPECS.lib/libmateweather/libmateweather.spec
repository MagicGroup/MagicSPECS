Name:          libmateweather
Version:       1.8.0
Release:       1%{?dist}
Summary:       Libraries to allow MATE Desktop to display weather information
License:       GPLv2+ and LGPLv2+
URL:           http://mate-desktop.org
Source0:       http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz

BuildRequires: gtk2-devel
BuildRequires: libsoup-devel
BuildRequires: mate-common
BuildRequires: pygtk2-devel
BuildRequires: pygobject2-devel

Requires:      %{name}-data = %{version}-%{release}

%description
Libraries to allow MATE Desktop to display weather information

%package data
Summary: Data files for the libmateweather
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description data
This package contains shared data needed for libmateweather.

%package devel
Summary:  Development files for libmateweather
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for libmateweather


%prep
%setup -q


%build
%configure --disable-static           \
           --disable-schemas-compile  \
           --with-gtk=2.0             \
           --enable-gtk-doc-html      \
           --enable-python

# fix unused-direct-shlib-dependency
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool 

make %{?_smp_mflags} V=1

%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -fv {} ';'
find %{buildroot} -name '*.a' -exec rm -fv {} ';'

%find_lang %{name} --with-gnome --all-name


%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%post data
/bin/touch --no-create %{_datadir}/icons/mate &>/dev/null || :

%postun data
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/mate &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/mate &>/dev/null || :
fi

%posttrans data
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/mate &>/dev/null || :


%files
%doc AUTHORS COPYING README
%{_datadir}/glib-2.0/schemas/org.mate.weather.gschema.xml
%{_libdir}/libmateweather.so.1*
%{python2_sitearch}/mateweather/

%files data -f %{name}.lang
%{_datadir}/icons/mate/*/status/*
%{_datadir}/libmateweather/

%files devel
%doc %{_datadir}/gtk-doc/html/libmateweather/
%{_libdir}/libmateweather.so
%{_includedir}/libmateweather/
%{_libdir}/pkgconfig/mateweather.pc


%changelog
* Tue Mar 04 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Mon Feb 17 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90 release
- use --with-gnome --all-name for find locale
- enable python bindings, add BR pygtk2-devel

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Wed Dec 04 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Fri Sep 13 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-3
- add requires to -data package, fix rhbz (#1007706)

* Mon Sep 02 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-2
- disable python bindings
- add --disable-schemas-compile configure flag
- use modern make install macro
- fix unused-direct-shlib-dependency
- add LGPLv2+ license
- move huge data in /usr/share in -data subpackage

* Sat Aug 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-1
- remove BR gsettings-desktop-schemas-devel
- fix icon-cache scriptlets
- remove autogen call

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Apr 13 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Update to latest upstream release

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Update to latest release 
- Update configure flags

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- change build requires style
- remove mateconf scriplets and replace with schema scriptlets
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel
- move gtk-doc files to devel package

* Mon Aug 27 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.4.0-5
- fix deps, a few cosmetics

* Sat Aug 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-4
- Fix mateconf scriptlets for schemas, bump release version

* Sat Aug 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-3
- Move python files to main package, drop libs subpackage, update mateconf scriptlets, move shared library to devel package

* Sat Aug 18 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-2
- Fix directory ownership

* Sun Aug 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-1
- Initial build
