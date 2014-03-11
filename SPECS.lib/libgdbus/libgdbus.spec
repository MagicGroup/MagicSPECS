Name:           libgdbus
Version:        0.2
Release:        8%{?dist}
Summary:        Library for simple D-Bus integration with GLib

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.bluez.org/
Source0:        http://www.kernel.org/pub/linux/bluetooth/%{name}-%{version}.tar.bz2
Patch0:		libgdbus-0.2-newglib.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  glib2-devel
BuildRequires:  dbus-devel
BuildRequires:  gtk-doc

%description
libgdbus is a helper library for D-Bus integration with GLib.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1

%build
%configure --disable-static --enable-gtk-doc
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/libgdbus/
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.2-8
- 为 Magic 3.0 重建

* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 0.2-7
- 为 Magic 3.0 重建

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.2-5
- Use bzipped upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 06 2008 Fabian Affolter <fabian@bernewireless.net> - 0.2-2
- Added more Docs

* Wed Nov 12 2008 Fabian Affolter <fabian@bernewireless.net> - 0.2-1
- Initial package for Fedora
