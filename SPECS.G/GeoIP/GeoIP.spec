Name: GeoIP           
Version: 1.4.8
Release: 2.1%{?dist}
Summary: C library for country/city/organization to IP address or hostname mapping     
Group: Development/Libraries         
License: LGPLv2+
URL: http://www.maxmind.com/app/c            
Source0: http://www.maxmind.com/download/geoip/api/c/GeoIP-%{version}.tar.gz 
Source1: LICENSE.txt
Source2: fetch-geoipdata-city.pl
Source3: fetch-geoipdata.pl
Source4: README.Fedora
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: geoip < %{version}-%{release}
Provides: geoip = %{version}-%{release}
BuildRequires: zlib-devel

%description
GeoIP is a C library that enables the user to find the country that any IP
address or hostname originates from. It uses a file based database that is
accurate as of March 2003. This database simply contains IP blocks as keys, and
countries as values. This database should be more complete and accurate than
using reverse DNS lookups.

%package devel
Summary: Development headers and libraries for GeoIP     
Group: Development/Libraries         
Requires: %{name} = %{version}-%{release}
Provides: geoip-devel = %{version}-%{release}
Obsoletes: geoip-devel < %{version}-%{release}

%description devel
Development headers and static libraries for building GeoIP-based applications

%prep
%setup -q
install -D -m644 %{SOURCE1} LICENSE.txt
install -D -m644 %{SOURCE2} fetch-geoipdata-city.pl
install -D -m644 %{SOURCE3} fetch-geoipdata.pl
install -D -m644 %{SOURCE4} README.fedora

%build
autoreconf -sivf
%configure --disable-static --disable-dependency-tracking
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# nix the stuff we don't need like .la files.
rm -f %{buildroot}/%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO INSTALL LICENSE* fetch-*
%{_libdir}/libGeoIP.so.*
%{_libdir}/libGeoIPUpdate.so.*
%{_bindir}/geoiplookup6
%{_bindir}/geoiplookup
%{_bindir}/geoipupdate
%config(noreplace) %{_sysconfdir}/GeoIP.conf.default
%config(noreplace) %{_sysconfdir}/GeoIP.conf
%{_datadir}/GeoIP
%{_mandir}/man1/geoiplookup.1*
%{_mandir}/man1/geoiplookup6.1*
%{_mandir}/man1/geoipupdate.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/GeoIP.h
%{_includedir}/GeoIPCity.h
%{_includedir}/GeoIPUpdate.h
%{_libdir}/libGeoIP.so
%{_libdir}/libGeoIPUpdate.so

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.4.8-2.1
- 为 Magic 3.0 重建

* Tue Sep 6 2011 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 1.4.8-1.1
- Remove -ipv6 path
- Bump to 1.4.8 release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-0.2.20090931cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 31 2009 Matt Domsch <mdomsch@fedoraproject.org> - 1.4.7.0.1.20090931
- apply CVS HEAD 20090931 which includes IPv6 functions

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 08 2009 Michael Fleming <mfleming+rpm@enlartenment.com> - 1.4.6-1
- Add geoiplookup6 man page
- Update to 1.4.6

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.5-2
- Update to 1.4.5
- Fix database URL locations in Perl helper scripts

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.4-2
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.4-1
- New upstream release.

* Wed Sep 5 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.3-1
- New upstream release.
- Fix GeoIPCity fetcher script
- Update License tag

* Mon Feb 12 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.2-1
- New upstream release.

* Mon Jan 8 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.1-2
- License is actually LGPL now.

* Sun Jan 7 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.1-1
- New upstream release
- Add fetch-geoipdata* scripts to pull free databases automatically if
  desired (bz #198137)
- README.fedora added to briefly explain above.

* Mon Nov 27 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.0-4
- Fix %%install scripts to satisfy newer mock builds

* Sun Sep 3 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.0-3
- Upstream upgrade
- Added LICENSE.txt file to %%doc, covering GeoIP country/city data license
  (bz #198137)

* Mon May 15 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.3.17-1
- New upstream release (minor fixes)

* Mon May 1 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.3.16-1
- New upstream release 
- Add INSTALL document to package.

* Sat Feb 18 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.3.14-3
- Fix Obsoletes/Provides for old "geoip"-convention packages
- Move .so symlinks to -devel where they should be

* Fri Feb 10 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.3.14-2
- Remamed to match upstream tarball name
- Removed static libraries
- Added symlinks to packages
- Mark config file noreplace

* Sun Feb 5 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.3.14-1
- Initial review package for Extras
