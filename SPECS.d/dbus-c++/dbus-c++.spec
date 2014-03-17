Name:           dbus-c++
Version:        0.9.0
Release:        2%{?dist}
Summary:        Native C++ bindings for D-Bus

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://sourceforge.net/projects/dbus-cplusplus/
Source0:        http://downloads.sourceforge.net/dbus-cplusplus/lib%{name}-%{version}.tar.gz

Patch1: dbus-c++-gcc4.7.patch
Patch2: dbus-c++-linkfix.patch

BuildRequires: dbus-devel
BuildRequires: glib2-devel
BuildRequires: gtkmm24-devel
BuildRequires: autoconf automake libtool
BuildRequires: expat-devel
BuildRequires: ecore-devel

%description
dbus-c++ attempts to provide a C++ API for D-Bus.
The library has a glib/gtk and an Ecore mainloop integration.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
%description    devel
This package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n lib%{name}-%{version}
%{__sed} -i 's/\r//' AUTHORS
%{__sed} -i 's/libtoolize --force --copy/libtoolize -if --copy/' bootstrap
%patch1 -p1 -b .gcc47
%patch2 -p1 -b .linkfix

%build
./autogen.sh
export CPPFLAGS='%{optflags}'
%configure --disable-static --disable-tests
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING AUTHORS
%{_bindir}/dbusxx-introspect
%{_bindir}/dbusxx-xml2cpp
%{_libdir}/*.so.*

%files devel
%doc TODO
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
* Wed Feb 26 2014 Jiri Popelka <jpopelka@redhat.com> - 0.9.0-2
- fix bootstrap script for ppc64le (#1070306)

* Tue Dec 17 2013 Jiri Popelka <jpopelka@redhat.com> - 0.9.0-1
- 0.9.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.17.20090203git13281b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.16.20090203git13281b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.15.20090203git13281b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.14.20090203git13281b3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.13.20090203git13281b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.12.20090203git13281b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 13 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.11.20090203git13281b3
- Fix FTBS (RH #565052)

* Fri Jul 31 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.10.20090203git13281b3
- Fix build

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.9.20090203git13281b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.8.20090203git13281b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.7.20090203git13281b3
- bump..

* Wed Feb 18 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.6.20090203git13281b3
- Fix build with new gcc

* Wed Feb 18 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.5.20090203git13281b3
- Add the ability to get the senders unix userid (Patch by Jiri Moskovcak)

* Tue Feb 03 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.4.20090203git13281b3
- Update to new git snapshot
- Should fix RH #483418

* Wed Jul 16 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.3.20080716git1337c65
- Generate tarball with git-archive
- Fix cflags

* Wed Jul 16 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.2.20080716git1337c65
- Add commit id to version

* Wed Jul 16 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.0-0.1.20080716git
- Initial package
