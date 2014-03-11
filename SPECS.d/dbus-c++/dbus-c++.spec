%define git_date 20090203
%define git_version 13281b3
Name:		dbus-c++
Version:	0.5.0
Release:	0.14.%{git_date}git%{git_version}%{?dist}
Summary:	Native C++ bindings for D-Bus

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://freedesktop.org/wiki/Software/dbus-c++
# Generate tarball
# git clone git://anongit.freedesktop.org/git/dbus/dbus-c++/
# git-archive --format=tar --prefix=dbus-c++/ %{git_version} | bzip2 > dbus-c++-0.5.0.`date +%Y%m%d`git%{git_version}.tar.bz2
Source0:	%{name}-%{version}.%{git_date}git%{git_version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1:	dbus-c++-get-uid-api.patch
Patch2: gcc-44.patch
Patch3: dbus-c++-build-fix.patch
Patch4: dbus-c++-linkfix.patch

BuildRequires:	dbus-devel
BuildRequires:	glib2-devel
Buildrequires:	gtkmm24-devel
Buildrequires:	libtool
BuildRequires:	expat-devel

%description
Native C++ bindings for D-Bus for use in C++ programs.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}
%{__sed} -i 's/\r//' AUTHORS
%{__sed} -i 's/-O3//' configure.ac
%patch1 -p1 -b .uid
%patch2 -p1 -b .gcc44
%patch3 -p1 -b .buildfix
%patch4 -p1 -b .linkfix

%build
./autogen.sh
export CPPFLAGS='%{optflags}'
%configure --disable-static --enable-glib
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS
%{_bindir}/dbusxx-introspect
%{_bindir}/dbusxx-xml2cpp
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc TODO
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.5.0-0.14.20090203git13281b3
- 为 Magic 3.0 重建

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
