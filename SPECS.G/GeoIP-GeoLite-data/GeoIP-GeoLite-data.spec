# EPEL-5 Compatibility
# ====================
# The following spec elements are needed for EL-5 support:
#  * BuildRoot: and Group: tags
#  * Cleaning of %%{buildroot} in %%install and %%clean
# Ref: https://fedoraproject.org/wiki/EPEL:Packaging#EPEL_5_and_earlier

Name:		GeoIP-GeoLite-data
# The geolite databases are updated on the first Tuesday of each month,
# hence we use a versioning scheme of YYYY.MM for the Fedora package
Version:	2015.09
Release:	3%{?dist}
Summary:	Free GeoLite IP geolocation country database
Summary(zh_CN.UTF-8): 自由的 GeoLite IP 地理位置国家库
# License specified at http://dev.maxmind.com/geoip/legacy/geolite/#License
License:	CC-BY-SA
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:		http://dev.maxmind.com/geoip/legacy/geolite/
Source0:	http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
Source1:	http://geolite.maxmind.com/download/geoip/database/GeoIPv6.dat.gz
Source2:	http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
Source3:	http://geolite.maxmind.com/download/geoip/database/GeoLiteCityv6-beta/GeoLiteCityv6.dat.gz
Source4:	http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz
Source5:	http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNumv6.dat.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
# This data has previously been available in differently-named packages
Obsoletes:	GeoIP-data < 1.6.4-10
Provides:	GeoIP-data = %{version}
Obsoletes:	geoip-geolite < %{version}
Provides:	geoip-geolite = %{version}
# The data was unbundled from GeoIP at 1.6.4-3
Conflicts:	GeoIP < 1.6.4-3

%description
The GeoLite databases are free IP geolocation databases. This package contains
a database that maps IPv4 addresses to countries.

This product includes GeoLite data created by MaxMind, available from
http://www.maxmind.com/

%description -l zh_CN.UTF-8
自由的 GeoLite IP 地理位置国家库。

%package extra
Summary:	Free GeoLite IP geolocation databases
Summary(zh_CN.UTF-8): 自由的 GeoLite IP 地理位置国家库
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:	CC-BY-SA
Requires:	%{name} = %{version}-%{release}

%description extra
The GeoLite databases are free IP geolocation databases. This package contains
databases that map IPv6 addresses to countries, plus IPv4 and IPv6 addresses
to cities and autonomous system numbers.

This product includes GeoLite data created by MaxMind, available from
http://www.maxmind.com/

%description extra -l zh_CN.UTF-8
自由的 GeoLite IP 地理位置国家库

%prep
%setup -q -T -c

install -p -m 644 %{SOURCE0} GeoLiteCountry.dat.gz;	gunzip GeoLiteCountry.dat
install -p -m 644 %{SOURCE1} GeoIPv6.dat.gz;		gunzip GeoIPv6.dat
install -p -m 644 %{SOURCE2} GeoLiteCity.dat.gz;	gunzip GeoLiteCity.dat
install -p -m 644 %{SOURCE3} GeoLiteCityv6.dat.gz;	gunzip GeoLiteCityv6.dat
install -p -m 644 %{SOURCE4} GeoLiteASNum.dat.gz;	gunzip GeoLiteASNum.dat
install -p -m 644 %{SOURCE5} GeoIPASNumv6.dat.gz;	gunzip GeoIPASNumv6.dat

%build
# This section intentionally left empty

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/GeoIP/
for db in \
	GeoLiteCountry.dat \
	GeoIPv6.dat \
	GeoLiteCity.dat \
	GeoLiteCityv6.dat \
	GeoLiteASNum.dat \
	GeoIPASNumv6.dat
do
	install -p -m 644 $db %{buildroot}%{_datadir}/GeoIP/
done

# Add compat symlinks for GeoIPASNum.dat and GeoLiteASNumv6.dat
# ([upstream] database names used in the old geoip-geolite package)
ln -sf GeoLiteASNum.dat %{buildroot}%{_datadir}/GeoIP/GeoIPASNum.dat
ln -sf GeoIPASNumv6.dat %{buildroot}%{_datadir}/GeoIP/GeoLiteASNumv6.dat

# Symlinks for City databases to be where upstream expects them
# (geoiplookup -v ...)
ln -sf GeoLiteCity.dat %{buildroot}%{_datadir}/GeoIP/GeoIPCity.dat
ln -sf GeoLiteCityv6.dat %{buildroot}%{_datadir}/GeoIP/GeoIPCityv6.dat
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%preun
# If the package is being uninstalled (rather than upgraded), we remove
# the GeoIP.dat symlink, provided that it points to GeoLiteCountry.dat;
# rpm will then be able to remove the %%{_datadir}/GeoIP directory
if [ $1 = 0 ]; then
	if [ -h %{_datadir}/GeoIP/GeoIP.dat ]; then
		geoipdat=`readlink %{_datadir}/GeoIP/GeoIP.dat`
		if [ "$geoipdat" = "GeoLiteCountry.dat" ]; then
			rm -f %{_datadir}/GeoIP/GeoIP.dat
		fi
	fi
fi
exit 0

%posttrans
# Create the default GeoIP.dat as a symlink to GeoLiteCountry.dat
#
# This has to be done in %%posttrans rather than %%post because an old
# package's GeoIP.dat may still be present during %%post in an upgrade
#
# Don't do this if there is any existing GeoIP.dat, as we don't want to
# override what the user has put there
#
# Also, if there's an existing GeoIP.dat.rpmsave, we're probably doing
# an upgrade from an old version of GeoIP that packaged GeoIP.dat as
# %%config(noreplace), so rename GeoIP.dat.rpmsave back to GeoIP.dat
# instead of creating a new symlink
if [ ! -e %{_datadir}/GeoIP/GeoIP.dat ]; then
	if [ -e %{_datadir}/GeoIP/GeoIP.dat.rpmsave ]; then
		mv %{_datadir}/GeoIP/GeoIP.dat.rpmsave \
			%{_datadir}/GeoIP/GeoIP.dat
	else
		ln -sf GeoLiteCountry.dat %{_datadir}/GeoIP/GeoIP.dat
	fi
fi
exit 0

%files
%dir %{_datadir}/GeoIP/
# The databases are %%verify(not md5 size mtime) so that they can be updated
# via cron scripts and rpm will not moan about the files having changed
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteCountry.dat

%files extra
# The databases are %%verify(not md5 size mtime) so that they can be updated
# via cron scripts and rpm will not moan about the files having changed
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoIPv6.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteCity.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteCityv6.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteASNum.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoIPASNumv6.dat
# The compat symlinks are just regular files as they should never need to be
# changed
%{_datadir}/GeoIP/GeoIPASNum.dat
%{_datadir}/GeoIP/GeoIPCity.dat
%{_datadir}/GeoIP/GeoIPCityv6.dat
%{_datadir}/GeoIP/GeoLiteASNumv6.dat

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2015.09-3
- 为 Magic 3.0 重建

* Sat Oct 03 2015 Liu Di <liudidi@gmail.com> - 2015.09-2
- 为 Magic 3.0 重建

* Wed Sep  9 2015 Paul Howarth <paul@city-fan.org> - 2015.09-1
- Update to September 2015 databases

* Tue Aug 18 2015 Paul Howarth <paul@city-fan.org> - 2015.08-1
- Update to August 2015 databases

* Wed Jul  8 2015 Paul Howarth <paul@city-fan.org> - 2015.07-1
- Update to July 2015 databases

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2015.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 14 2015 Paul Howarth <paul@city-fan.org> - 2015.06-1
- Update to June 2015 databases

* Tue May 12 2015 Paul Howarth <paul@city-fan.org> - 2015.05-1
- Update to May 2015 databases

* Mon Apr 27 2015 Paul Howarth <paul@city-fan.org> - 2015.04-2
- Add symlinks for City databases to be where upstream expects them
  (thanks to nucleo for the suggestion in #1194798)

* Sun Apr 12 2015 Paul Howarth <paul@city-fan.org> - 2015.04-1
- Update to April 2015 databases
- Add %%preun script to remove GeoIP.dat symlink if package is uninstalled

* Wed Apr  1 2015 Paul Howarth <paul@city-fan.org> - 2015.03-3
- Incorporate review feedback (#1194798)
  - Don't package GeoIP.dat symlink; create it in %%posttrans if it doesn't
    exist
  - Update IPASNum databases to current upstream
  - Wrap comments at 80 characters
  - Comment use of EPEL-5 idioms
  - Comment where upstream declares licensing

* Thu Mar  5 2015 Paul Howarth <paul@city-fan.org> - 2015.03-1
- Update to March 2015 databases

* Fri Feb 20 2015 Paul Howarth <paul@city-fan.org> - 2015.02-1
- Databases unbundled from GeoIP, like the old geoip-geolite package
