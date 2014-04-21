# Tests require network access so fail in koji; build using --with tests to run them yourself
%bcond_with tests

# Noarch subpackages available from Fedora 10, RHEL 6
%global noarch_subpkgs 0%{?fedora} > 9 || 0%{?rhel} > 5

Name:		GeoIP
Version:	1.5.1
Release:	5%{?dist}
Summary:	Library for country/city/organization to IP address or hostname mapping
Group:		Development/Libraries
License:	LGPLv2+ and GPLv2+ and CC-BY-SA
URL:		http://www.maxmind.com/app/c
Source0:	http://www.maxmind.com/download/geoip/api/c/GeoIP-%{version}.tar.gz
Source2:	fetch-geoipdata-city.pl
Source3:	fetch-geoipdata.pl
Source5:	geoipupdate.cron
Source6:	geoipupdate6.cron
Source7:	lastmod.pl
# Data sources indexed at http://dev.maxmind.com/geoip/legacy/geolite
Source10:	http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
Source11:	http://geolite.maxmind.com/download/geoip/database/GeoIPv6.dat.gz
Source12:	http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
Source13:	http://geolite.maxmind.com/download/geoip/database/GeoLiteCityv6-beta/GeoLiteCityv6.dat.gz
Source14:	http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz
Source15:	http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNumv6.dat.gz
Patch1:		GeoIP-1.5.0-exitcode.patch
Patch10:	GeoIP-1.5.1-UTF8.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	zlib-devel
Obsoletes:	geoip < %{version}-%{release}
Provides:	geoip = %{version}-%{release}
Obsoletes:	geoip-geolite < 2013.04-2
Provides:	geoip-geolite = 2013.04-2

%description
GeoIP is a C library that enables the user to find the country that any IP
address or hostname originates from.

It uses file based databases that can optionally be updated on a weekly basis
by installing the GeoIP-update (IPv4) and/or GeoIP-update6 (IPv6) packages.

This package includes GeoLite data created by MaxMind, available from
http://www.maxmind.com/

%package update
Summary:	Crontab entry to facilitate automatic updates of IPv4 GeoIP databases
Group:		Applications/Databases
Requires:	crontabs
Requires:	%{name} = %{version}-%{release}
%if %{noarch_subpkgs}
BuildArch:	noarch
%endif

%description update
Crontab entry to provide weekly updates of the GeoIP free IPv4 databases.

%package update6
Summary:	Crontab entry to facilitate automatic updates of IPv6 GeoIP databases
Group:		Applications/Databases
Requires:	crontabs
Requires:	wget
Requires:	%{name} = %{version}-%{release}
%if %{noarch_subpkgs}
BuildArch:	noarch
%endif

%description update6
Crontab entry to provide weekly updates of the GeoIP free IPv6 databases.

%package devel
Summary:	Development headers and libraries for GeoIP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	geoip-devel = %{version}-%{release}
Obsoletes:	geoip-devel < %{version}-%{release}

%description devel
Development headers and static libraries for building GeoIP-based applications.

%prep
%setup -q

# Scripts and license files
install -p -m 644 %{SOURCE2} fetch-geoipdata-city.pl
install -p -m 644 %{SOURCE3} fetch-geoipdata.pl
install -p -m 755 %{SOURCE5} geoipupdate.cron
install -p -m 755 %{SOURCE6} geoipupdate6.cron
install -p -m 755 %{SOURCE7} lastmod.pl

# Data
install -p -m 644 %{SOURCE10} data/GeoLiteCountry.dat.gz;	gunzip data/GeoLiteCountry.dat
install -p -m 644 %{SOURCE11} data/GeoIPv6.dat.gz;		gunzip data/GeoIPv6.dat
install -p -m 644 %{SOURCE12} data/GeoLiteCity.dat.gz;		gunzip data/GeoLiteCity.dat
install -p -m 644 %{SOURCE13} data/GeoLiteCityv6.dat.gz;	gunzip data/GeoLiteCityv6.dat
install -p -m 644 %{SOURCE14} data/GeoLiteASNum.dat.gz;		gunzip data/GeoLiteASNum.dat
install -p -m 644 %{SOURCE15} data/GeoIPASNumv6.dat.gz;		gunzip data/GeoIPASNumv6.dat

# Fix exit codes for various cases (MaxMind support #129155)
%patch1 -p1 -b .exitcode

# Recode docs as UTF-8
%patch10 -p1 -b .utf8

%build
# Fix timestamp order to avoid trying to re-run autotools and configure,
# thus clobbering our hacked libtool later on
touch aclocal.m4
touch configure
touch config.h.in
touch config.status
find . -name Makefile.in -exec touch {} \;

%configure --disable-static --disable-dependency-tracking

# Kill bogus rpaths
sed -i -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
	-e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} INSTALL="install -p" install

# nix the stuff we don't need like .la files.
rm -f %{buildroot}%{_libdir}/*.la

# fix up the config file to have geoipupdate fetch the free products by default
sed -i \
	-e 's/YOUR_LICENSE_KEY_HERE$/000000000000/' \
	-e 's/YOUR_USER_ID_HERE$/999999/' \
	-e 's/106$/506 533 517/' \
	%{buildroot}%{_sysconfdir}/GeoIP.conf

# install GeoLite databases
for db in \
	GeoLiteCountry.dat \
	GeoIPv6.dat \
	GeoLiteCity.dat \
	GeoLiteCityv6.dat \
	GeoLiteASNum.dat \
	GeoIPASNumv6.dat
do
	install -p -m 644 data/$db %{buildroot}%{_datadir}/GeoIP/
done

%{__mkdir_p} %{buildroot}%{_libexecdir}

install -p -m 755 lastmod.pl %{buildroot}%{_libexecdir}/

# make the default GeoIP.dat a symlink to GeoLiteCountry.dat,
# since it's actually an old snapshot of that database
ln -sf GeoLiteCountry.dat %{buildroot}%{_datadir}/GeoIP/GeoIP.dat

# add compat symlinks for GeoIPASNum.dat and GeoLiteASNumv6.dat
ln -sf GeoLiteASNum.dat %{buildroot}%{_datadir}/GeoIP/GeoIPASNum.dat
ln -sf GeoIPASNumv6.dat %{buildroot}%{_datadir}/GeoIP/GeoLiteASNumv6.dat

# fetch database updates weekly
install -D -m 755 geoipupdate.cron %{buildroot}%{_sysconfdir}/cron.weekly/geoipupdate
install -D -m 755 geoipupdate6.cron %{buildroot}%{_sysconfdir}/cron.weekly/geoipupdate6

%check
# Tests require network access so fail in koji; build using --with tests to run them yourself
%{?with_tests:LD_LIBRARY_PATH=%{buildroot}%{_libdir} make check}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
# LGPLv2+
%doc AUTHORS COPYING ChangeLog README TODO fetch-*
%config(noreplace) %{_sysconfdir}/GeoIP.conf
%config(noreplace) %{_sysconfdir}/GeoIP.conf.default
%{_bindir}/geoiplookup
%{_bindir}/geoiplookup6
%{_libdir}/libGeoIP.so.1
%{_libdir}/libGeoIP.so.1.*
%{_mandir}/man1/geoiplookup.1*
%{_mandir}/man1/geoiplookup6.1*
# GPLv2+
%{_bindir}/geoipupdate
%{_libdir}/libGeoIPUpdate.so.0
%{_libdir}/libGeoIPUpdate.so.0.*
%{_mandir}/man1/geoipupdate.1*
# CC-BY-SA
%dir %{_datadir}/GeoIP/
# This is %%config(noreplace) so that it can be replaced by a commercial database if desired by the end user
%config(noreplace) %{_datadir}/GeoIP/GeoIP.dat
# The other databases are %%verify(not md5 size mtime) so that they can be updated via the cron scripts
# and rpm will not moan about the files having changed
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteCountry.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoIPv6.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteCity.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteCityv6.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteASNum.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoIPASNumv6.dat
# The compat symlinks are just regular files as they should never need to be changed
%{_datadir}/GeoIP/GeoIPASNum.dat
%{_datadir}/GeoIP/GeoLiteASNumv6.dat

%files update
%{_sysconfdir}/cron.weekly/geoipupdate

%files update6
%{_sysconfdir}/cron.weekly/geoipupdate6
%{_libexecdir}/lastmod.pl

%files devel
# LGPLv2+
%{_includedir}/GeoIP.h
%{_includedir}/GeoIPCity.h
%{_includedir}/GeoIPUpdate.h
%{_libdir}/libGeoIP.so
%{_libdir}/pkgconfig/geoip.pc
# GPLv2+
%{_libdir}/libGeoIPUpdate.so

%changelog
* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 1.5.1-5
- 为 Magic 3.0 重建

* Tue Feb 25 2014 Paul Howarth <paul@city-fan.org> - 1.5.1-4
- Add %%check, so we can run tests by building using --with tests
- Update databases from upstream

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 18 2013 Paul Howarth <paul@city-fan.org> - 1.5.1-2
- Properly provide all of the GeoLite databases and their IPv6 equivalents, as
  per the geoip-geolite package that we're obsoleting/providing
- Provide compatibility symlinks for database files that historically had
  different names in GeoIP and geoip-geolite
- Don't distribute unbundled LICENSE files, as per packaging guidelines
- Update license tag to reflect distribution of CC-BY-SA database content
- No longer try to update the databases in %%post
- Maintain timestamps where possible
- Set up GeoIP.dat symlink in package and don't touch it again
- Add update6 package to update the IPv6 databases; have to use wget for this
  rather than geoipupdate as the databases are still in beta

* Wed Jun 12 2013 Philip Prindeville <philipp@fedoraproject.org> - 1.5.1-1
- Bump to version 1.5.1
- Fix exit codes for various situations (MaxMind support #129155)
- Use versioned obsoletes/provides for geoip-geolite
- Update UTF8 patch
- Change symlink from GeoIP-initial.dat to GeoLiteCountry.dat if we had a
  successful download and now have the latter file.

* Mon Jun 10 2013 Philip Prindeville <philipp@fedoraproject.org> - 1.5.0-7
- Annotate conflict with geoip-geolite package (#968074)

* Mon Jun 10 2013 Paul Howarth <paul@city-fan.org> - 1.5.0-6
- Update sub-package requires main package for geoipupdate script

* Sat Jun  8 2013 Paul Howarth <paul@city-fan.org> - 1.5.0-5
- Make GeoIP.dat -> GeoIP-initial.dat symlink in %%install, not %%post,
  and don't %%ghost it
- Run geoipupdate silently in %%post and cron job
- Create empty database files for %%ghost to work with old rpm versions
- Don't try to use noarch subpackages on old rpm versions
- Update %%description to mention database updates
- Drop outdated README.Fedora

* Sat Jun 08 2013 Philip Prindeville <philipp@fedoraproject.org> - 1.5.0-4
- Revert ability to replace 3rd-party package

* Fri Jun 07 2013 Philip Prindeville <philipp@fedoraproject.org> - 1.5.0-3
- Add attributes for %%ghost files

* Fri Jun 07 2013 Philip Prindeville <philipp@fedoraproject.org> - 1.5.0-2
- Make update subpackage be noarch.

* Fri Jun 07 2013 Philip Prindeville <philipp@fedoraproject.org> - 1.5.0-1
- Version bump to 1.5.0
- Have GeoIP.dat be a symlink to the real data, and install the canned
  GeoIP.dat as GeoIP-initial.dat
- Change config as per Boris' instructions to use 'lite' databases which are
  regularly updated.
- Add pkgconfig (.pc) file into devel subpackage
- Add cron support for refreshing the lite databases and make a separate
  subpackage.

* Sun Mar 24 2013 Paul Howarth <paul@city-fan.org> - 1.4.8-6
- Fix config.guess and config.sub to add aarch64 support (#925403)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 22 2012 Paul Howarth <paul@city-fan.org> - 1.4.8-4
- libGeoIPUpdate and geoipupdate (which is linked against it) are GPL-licensed
  rather than LGPL-licensed (#840896)
- Don't package generic INSTALL file (#661625)
- Kill bogus rpaths on x86_64
- Hardcode library sonames in %%files list to avoid nasty surprises in the
  future
- Drop %%defattr, redundant since rpm 4.4
- Recode docs as UTF-8
- Don't use macros for commands
- Use tabs

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 6 2011 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 1.4.8-1.1
- Remove -ipv6 patch
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
