%define         basever 0.9.5.92.1

Name:           libcompizconfig
Version:        0.9.5.92
Release:        1%{?dist}
Summary:        Configuration backend for compiz

Group:          System Environment/Libraries
# backends/libini.so is GPLv2+, other parts are LGPLv2+
License:        LGPLv2+ and GPLv2+
URL:            http://www.compiz.org/

Source0:        http://releases.compiz-fusion.org/%{version}/%{name}-%{version}.tar.bz2
# Set GNOME to use ini backend for now, while there's a bug with gconf
# backend (compiz fails to reload correctly)
Patch0:         libcompizconfig-0.9.2.1-gnome_ini.patch
# revert upstream commit
# http://gitweb.compiz.org/?p=compiz/compizconfig/libcompizconfig;a=commit;h=9d32d80e86dc820b512c7fb68a0191e5184762ed
Patch1:         fix_libdir.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# libdrm is not available on these arches
ExcludeArch:    s390 s390x
BuildRequires:  compiz-devel >= %{basever}
BuildRequires:  libX11-devel, gettext, intltool
BuildRequires:  cmake
BuildRequires:  perl(XML::Parser)
BuildRequires:  mesa-libGL-devel
BuildRequires:  protobuf-devel
BuildRequires:  boost-devel

%description
The Compiz Project brings 3D desktop visual effects that improve
usability of the X Window System and provide increased productivity
through plugins and themes contributed by the community giving a
rich desktop experience.

This package contains the library for plugins to configure compiz 
settings.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release} , pkgconfig , compiz-devel >= %{version}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1


%build
rm -rf $RPM_BUILD_ROOT
mkdir build
pushd build
%cmake -DCOMPIZ_BUILD_WITH_RPATH=OFF -DCOMPIZ_PACKAGING_ENABLED=ON -DCOMPIZ_PLUGIN_INSTALL_TYPE=package -DCOMPIZ_DISABLE_SCHEMAS_INSTALL=ON -DCOMPIZ_INSTALL_GCONF_SCHEMA_DIR=%{_sysconfdir}/gconf/schemas ..
make VERBOSE=1 %{?_smp_mflags}
popd


%install
pushd build
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# This should work, but is buggy upstream:
# make DESTDIR=$RPM_BUILD_ROOT findcompizconfig_install
# So we do this instead:
mkdir -p $RPM_BUILD_ROOT%{_datadir}/cmake/Modules
%__cmake -E copy ../cmake/FindCompizConfig.cmake $RPM_BUILD_ROOT%{_datadir}/cmake/Modules

popd

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# schema is useless
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/gconf/schemas/compiz-ccp.schemas

# install the config file
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/compizconfig
install -m 0644  config/config $RPM_BUILD_ROOT/%{_sysconfdir}/compizconfig/config

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS VERSION
%{_libdir}/*.so.*
%{_datadir}/compiz/ccp.xml
%{_libdir}/compiz/*.so
%{_sysconfdir}/compizconfig/config
%dir %{_libdir}/compizconfig/
%dir %{_libdir}/compizconfig/backends/
%{_libdir}/compizconfig/backends/libini.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_datadir}/cmake/Modules/FindCompizConfig.cmake
%{_datadir}/compiz/cmake/LibCompizConfigCommon.cmake
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcompizconfig.pc


%changelog
* Tue Oct 18 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.9.5.92-1
- new release 0.9.5.92

* Thu Jul 21 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.9.5.0-2
- rebuild against boost 1.47.0

* Fri Jul 15 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.9.5.0-1
- new release 0.9.5.0

* Fri Jun 10 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.9.4-3
- rebuilt against protobuf 2.4

* Thu Apr 07 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.9.4-2
- rebuilt against boost 1.46.1

* Mon Mar 14 2011 Adam Williamson <awilliam@redhat.com> - 0.9.4-1
- new release 0.9.4

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.9.2.1-6
- rebuilt for boost

* Sun Jan 23 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.1-5
- rebuild for cflags

* Wed Jan 19 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.1-4
- set GNOME sessions to use ini backend, while there's a bug with
  gconf

* Wed Jan 19 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.1-3
- package the default config file (creates different sessions for
  different desktops)

* Sun Jan 16 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.1-2
- drop gconf stuff entirely

* Sat Jan 15 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.1-1
- new release 0.9.2.1
- switch to cmake build system

* Sat Nov 06 2010 leigh scott <leigh123linux@googlemail.com> - 0.8.4-4
- rebuilt

* Wed May 05 2010 Leigh Scott <leigh123linux@googlemail.com> - 0.8.4-3
- rebuilt for protobuf soname change

* Tue Mar 30 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.4-2
- Rebuild against new compiz

* Sat Jan 16 2010 Leigh Scott <leigh123linux@googlemail.com> - 0.8.4-1
- Update to 0.8.4
- drop upstream patches

* Sat Sep 29 2009 leigh scott <leigh123linux@googlemail.com> - 0.8.2-7
- add patch for protobuf version and re-enable protobuf support

* Sat Sep 19 2009 leigh scott <leigh123linux@googlemail.com> - 0.8.2-6
- disable protobuf support

* Fri Jul 31 2009 leigh scott <leigh123linux@googlemail.com> - 0.8.2-5
- add patch to Update .pb when an older .xml is used

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Leigh Scott <leigh123linux@googlemail.com> 0.8.2-3
- remove dead files from files section

* Thu Jul 23 2009 Leigh Scott <leigh123linux@googlemail.com> 0.8.2-2
- drop the libcompizconfig-fix-weak-symbols.patch

* Thu Jul 23 2009 Leigh Scott <leigh123linux@googlemail.com> 0.8.2-1
- update to 0.8.2
- add protobuf-devel BuildRequires

* Sat Feb 28 2009 Caolán McNamara <caolanm@redhat.com> - 0.7.8-3
- add mesa-libGL-devel BuildRequires

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 30 2008 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.7.8-1
- update to 0.7.8

* Tue Jul 15 2008 Nikolay Vladimirof <nikolay@vladimiroff.com> - 0.7.6-2
- rebuild for ppc64

* Sat Jun 7 2008 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.7.6-1
- 0.7.6 update

* Tue Mar 27 2008 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.7.2-1
- 0.7.2 update

* Sun Feb 10 2008 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.6.0-7
- rebuild for gcc43

* Tue Jan 08 2008 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.6.0-5
- patched also the configure script

* Tue Jan 08 2008 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.6.0-4
- applied gcc43 buildfix

* Wed Oct 24 2007 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.6.0-3
- -devel requires compiz-devel >= version

* Wed Oct 24 2007 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.6.0-2
- >= instead of = to allow compiz upgrade flexibility

* Tue Oct 23 2007 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.6.0-1
- official 0.6.0 release

* Tue Oct 16 2007 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.6.0-0.3.20071011git5615ca
- added LICENSE.gpl and LICENSE.lgpl into doc
- license tag changed to LGPLv2+ and GPLv2+

* Tue Oct 16 2007 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.6.0-0.2.20071011git5615ca
- 20071011git
- added BuildDep libX11-devel
- added patch to fix weak symbols

* Sat Oct 6 2007 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.5.2-0.3
- owns created directories
- updated license tag

* Tue Aug 14 2007 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.5.2-0.1
- 0.5.2 release

* Sun Jul 03 2007 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.0.1-0.4.20070703git
- 20070703git

* Sun Jun 24 2007 Mohd Izhar Firdaus Ismail <mohd.izhar.firdaus@gmail.com> 0.0.1-20070622git
- Initial specfile, borrowing descriptions from Trevino ubuntu debs

