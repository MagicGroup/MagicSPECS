# Noarch subpackages available from Fedora 10, RHEL6
%global noarch_subpkgs 0%{?fedora} > 9 || 0%{?rhel} > 5

%global _hardened_build 1

Name:		geoipupdate
Version:	2.2.1
Release:	3%{?dist}
Summary:	Update GeoIP2 and GeoIP Legacy binary databases from MaxMind
Group:		Development/Tools
License:	GPLv2
URL:		http://dev.maxmind.com/geoip/geoipupdate/
Source0:	http://github.com/maxmind/geoipupdate/releases/download/v%{version}/geoipupdate-%{version}.tar.gz
Source1:	geoipupdate.cron
Source2:	geoipupdate6.cron
Patch0:		geoipupdate-2.2.1-docdir.patch
Patch1:		geoipupdate-2.2.1-autotools.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	curl-devel
BuildRequires:	zlib-devel
# Perl modules used by IPv6 cron script
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(LWP::Simple)
BuildRequires:	perl(PerlIO::gzip)
BuildRequires:	perl(strict)

%description
The GeoIP Update program performs automatic updates of GeoIP2 and GeoIP
Legacy binary databases.

%package cron
Summary:	Cron job to do weekly updates of GeoIP databases
Group:		Development/Tools
%if %{noarch_subpkgs}
BuildArch:	noarch
%endif
Requires:	%{name} = %{version}-%{release}
Requires:	crontabs
Obsoletes:	GeoIP-update < 1.6.0
Provides:	GeoIP-update = 1.6.0

%description cron
Cron job for weekly updates to GeoIP Legacy database from MaxMind.

%package cron6
Summary:	Cron job to do weekly updates of GeoIP IPv6 databases
Group:		Development/Tools
%if %{noarch_subpkgs}
BuildArch:	noarch
%endif
Requires:	%{name} = %{version}-%{release}
Requires:	crontabs
Requires:	wget
Obsoletes:	GeoIP-update6 < 1.6.0
Provides:	GeoIP-update6 = 1.6.0

%description cron6
Cron job for weekly updates to GeoIP IPv6 Legacy database from MaxMind.

%prep
%setup -q

# GeoIP.conf.default should install into $(docdir) and not $(sysconfdir)
# https://github.com/maxmind/geoipupdate/issues/26
%patch0

# Changes to autotools-generated files as a result of previous patch
%patch1

%build
%configure --disable-static --disable-dependency-tracking
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# We'll package the documentation ourselves
rm -rf %{buildroot}%{_datadir}/doc/geoipupdate

# Fix up the config file to have geoipupdate fetch the free products by default
sed -i \
	-e 's/YOUR_USER_ID_HERE$/999999/' \
	-e 's/YOUR_LICENSE_KEY_HERE$/000000000000/' \
	-e 's/^\(ProductIds\) .*$/\1 506 517 533/' \
	%{buildroot}%{_sysconfdir}/GeoIP.conf

install -D -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/cron.weekly/geoipupdate
install -D -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/cron.weekly/geoipupdate6

# Make the download directory for the IPv6 data cron job and some ghost files
mkdir -p %{buildroot}%{_datadir}/GeoIP/download/
: > %{buildroot}%{_datadir}/GeoIP/download/GeoIPv6.dat.gz
: > %{buildroot}%{_datadir}/GeoIP/download/GeoLiteCityv6.dat.gz
: > %{buildroot}%{_datadir}/GeoIP/download/GeoIPASNumv6.dat.gz

%clean
rm -rf %{buildroot}

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc conf/GeoIP.conf.default README.md ChangeLog.md
%config(noreplace) %{_sysconfdir}/GeoIP.conf
%{_bindir}/geoipupdate
%{_mandir}/man1/geoipupdate.1*
%{_mandir}/man5/GeoIP.conf.5*

%files cron
%config(noreplace) %{_sysconfdir}/cron.weekly/geoipupdate

%files cron6
%config(noreplace) %{_sysconfdir}/cron.weekly/geoipupdate6
%dir %{_datadir}/GeoIP/
%dir %{_datadir}/GeoIP/download/
%ghost %{_datadir}/GeoIP/download/GeoIPv6.dat.gz
%ghost %{_datadir}/GeoIP/download/GeoLiteCityv6.dat.gz
%ghost %{_datadir}/GeoIP/download/GeoIPASNumv6.dat.gz

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 13 2015 Paul Howarth <paul@city-fan.org> - 2.2.1-2
- Split patch for upstream issue #26 into separate patches for upstream changes
  and effect of running autotools

* Wed Mar  4 2015 Philip A. Prindeville <philipp@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1
  - geoipupdate now verifies the MD5 of the new database before deploying it;
    if the database MD5 does not match the expected MD5, geoipupdate will exit
    with an error
  - The copy of 'base64.c' and 'base64.h' was switched to a version under
    GPLv2+ to prevent a license conflict
  - The 'LICENSE' file was added to the distribution
  - Several issues in the documentation were fixed
- Use interim fix for upstream issue #26 until it's accepted:
  https://github.com/maxmind/geoipupdate/issues/26
- Add buildroot and clean, BR: curl-devel rather than libcurl-devel for
  EL-5 compatibility

* Tue Feb 10 2015 Paul Howarth <paul@city-fan.org> - 2.1.0-4
- New geoipupdate6 cron script written in Perl that doesn't download the data
  if it hasn't changed

* Fri Feb  6 2015 Paul Howarth <paul@city-fan.org> - 2.1.0-3
- Add cron6 subpackage, equivalent to old GeoIP-update6 package
- Revise obsoletes/provides

* Sun Feb  1 2015 Philip A. Prindeville <philipp@fedoraproject.org> - 2.1.0-2
- Remove architecture-specific dependency in noarch subpackage

* Mon Jan 26 2015 Philip A. Prindeville <philipp@fedoraproject.org> - 2.1.0-1
- Initial review package (generated by rpmdev-newspec)
