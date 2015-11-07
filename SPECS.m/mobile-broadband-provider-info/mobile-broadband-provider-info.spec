%define upstream_version 20120614

Summary: Mobile broadband provider database
Summary(zh_CN.UTF-8): 移动宽带提供商信息
Name: mobile-broadband-provider-info
Version: 1.%{upstream_version}
Release: 5%{?dist}
#
# Source from git://git.gnome.org/mobile-broadband-provider-info
# tarball built with:
#    ./autogen.sh --prefix=/usr
#    make distcheck
#
#Source: mobile-broadband-provider-info-%{upstream_version}.tar.bz2
Source: http://ftp.gnome.org/pub/gnome/sources/mobile-broadband-provider-info/%{upstream_version}/mobile-broadband-provider-info-%{upstream_version}.tar.xz
License: Public Domain
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本

BuildArch: noarch
URL: http://live.gnome.org/NetworkManager/MobileBroadband/ServiceProviders
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: libxml2

%description
The mobile-broadband-provider-info package contains listings of mobile
broadband (3G) providers and associated network and plan information.

%description -l zh_CN.UTF-8
移动宽带（3G）提供商信息。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains files necessary for
developing developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{upstream_version}

%build
%configure
make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644, root, root, 0755)
%doc COPYING README
%dir %{_datadir}/%{name}
%attr(0644,root,root) %{_datadir}/%{name}/*
	
%files devel
%defattr(0644, root, root, 0755)
%{_datadir}/pkgconfig/%{name}.pc

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.20120614-5
- 为 Magic 3.0 重建

* Fri Oct 17 2014 Liu Di <liudidi@gmail.com> - 1.20120614-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.20110218-3
- 为 Magic 3.0 重建

* Mon Jan 16 2012 Liu Di <liudidi@gmail.com> - 1.20110218-2
- 为 Magic 3.0 重建

* Fri Feb 18 2011 Matěj Cepl <mcepl@redhat.com> - 1.20110218-1
- Update to latest upstream checkout including:
	* south africa: add 8.ta (Telkom) provider (bgo #641916),
	  remove username for Cell-C (bgo #640794)
	* switzerland: update Orange plans and APNs (bgo #638115)
	* tanzania: add Sasatel and TTCL, add CDMA for Zantel (bgo #634609)
	* india: new unified BSNL APNs (rh #667280)
	* ec: add Movistar Ecuador (bgo #638223)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20101231-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.20101231-2
- Own the %%{_datadir}/%%{name} dir.
- Remove duplicate "make check".

* Fri Dec 31 2010 Matěj Cepl <mcepl@redhat.com> - 1.20101231-1
- Update to latest upstream checkout including:
	Afghanistan, Argentina, Armenia, Australia, Austria, Bahrain, Canada,
	Croatia, Denmark, Dominican Republic, Finland, France, French Polynesia,
	Germany, Greece, Hong Kong, Hungary, China, Iceland, India, Indonesia,
	Iran, Israel, Israel, Italy, Latvia, Luxembourg, Mexico, Montenegro,
	Netherlands, New Zealand, Nicaragua, Norway, Paraguay, Philippines,
	Poland, Portugal, Romania, Rwanda/Burundi, Slovakia, Slovenia, Spain,
	Sudan, Sweden, Switzerland, Thailand, Tunisia, Uganda, United Arab
, 
* Fri Jan 22 2010 Dan Williams <dcbw@redhat.com> - 1.20100122-1
- Update to latest upstream release including:
- Cyprus, Austria, Ireland, Ukraine, Romainia, Cambodia (rh #530981), 
- Iraq, India, Sri Lanka, UK, Australia, Singapore,
- South Korea, Italy, United States, China (rh #517253), Nigeria,
- Tanzania, Germany, Qatar, Russia, and Finland (rh #528988)

* Fri Sep 18 2009 Dan Williams <dcbw@redhat.com> - 1.20090918-1
- Update to latest upstream release including:
- Algeria, Australia, Belarus, Belgium, Brazil
- Brunei, Bulgaria, Egypt, Finland, Ghana, Greece
- India, Italy, Kazakhstan, Korean CDMA operators
- Kuwait, Mali, Netherlands, Paraguay, Serbia
- Spain, Sweden, UK

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 1.20090707-3
- Add -devel sub-package with pkg-config file (#511318)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20090707-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 7 2009 Dan Williams <dcbw@redhat.com> - 1.20090707-1
- Update to latest upstream release including:
- T-Mobile USA
- Brazil
- Bangladesh
- Sweden
- Spain
- Moldova

* Tue Jun 3 2009 Dan Williams <dcbw@redhat.com> 0.20090602-2
- Package review fixes

* Tue Jun 2 2009 Dan Williams <dcbw@redhat.com> 0.20090602-1
- Initial version

