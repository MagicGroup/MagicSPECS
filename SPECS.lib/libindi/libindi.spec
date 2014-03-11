Name: libindi
Version: 0.9
Release: 3%{?dist}
Summary: Instrument Neutral Distributed Interface

Group: Development/Libraries
License: LGPLv2+ and GPLv2+
# See COPYRIGHT file for a description of the licenses and files covered

# Address of FSF is incorrect
# upstream bug https://sourceforge.net/tracker/?func=detail&aid=3367995&group_id=90275&atid=593019

URL: http://www.indilib.org
Source0: http://downloads.sourceforge.net/indi/%{name}_%{version}.tar.gz
Patch0: libindi-usleep.patch
Patch1: libindi-fsf.patch

BuildRequires: cmake cfitsio-devel zlib-devel libnova-devel libfli-devel
BuildRequires: libusb-devel

%description
INDI is a distributed control protocol designed to operate
astronomical instrumentation. INDI is small, flexible, easy to parse,
and scalable. It supports common DCS functions such as remote control,
data acquisition, monitoring, and a lot more.

%package devel
Summary: Libraries, includes, etc. used to develop an application with %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
%description devel
These are the header files needed to develop a %{name} application

%package static
Summary: Static libraries, includes, etc. used to develop an application with %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
%description static
Static library needed to develop a %{name} application

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
chmod -x drivers/telescope/lx200fs2.h
chmod -x drivers/telescope/lx200fs2.cpp


%build
%cmake
make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING.GPL COPYING.LGPL COPYRIGHT LICENSE NEWS README README.drivers TODO
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/indi

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files static
%{_libdir}/*.a

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.9-3
- 为 Magic 3.0 重建

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for c++ ABI breakage

* Tue Jan 24 2012 Sergio Pascual <sergiopr at fedoraproject.org> - 0.9-1
- New upstream source
- All instruments created (solves #653690)
- Library does not call exit()
- Library does not build require boost-devel

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 15 2011 Sergio Pascual <sergiopr at fedoraproject.org> - 0.8-1
- New upstream source
- Submitted a bug upstream, address of FSF is incorrect in some files

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Sergio Pascual <sergiopr at fedoraproject.org> - 0.6.2-2
- Adding manually telescopes missing (bz #653690)

* Thu Jul 29 2010 Sergio Pascual <sergiopr at fedoraproject.org> - 0.6.2-1
- New upstream source (bz #618776)
- Bz #564842 fixed upstream, patch removed
- With pkgconfig file

* Wed Feb 17 2010 Sergio Pascual <sergiopr at fedoraproject.org> - 0.6-11
- Added missing -lm in indi_sbig_stv. Fixes bz #564842

* Fri Jan 08 2010 Sergio Pascual <sergiopr at fedoraproject.org> - 0.6-10
- EVR bump, rebuilt with new libnova

* Tue Dec 22 2009 Sergio Pascual <sergiopr at fedoraproject.org> - 0.6-9
- Static library moved to its own subpackage

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Sergio Pascual <sergiopr at fedoraproject.org> -  0.6-6
- Provides libindi-static

* Tue Feb 17 2009 Sergio Pascual <sergiopr at fedoraproject.org> -  0.6-5
- Need to provide the static library libindidriver.a to build indi-apogee

* Sat Feb 14 2009 Sergio Pascual <sergiopr at fedoraproject.org> -  0.6-4
- Fixed patch to find cfitsio

* Sat Feb 14 2009 Sergio Pascual <sergiopr at fedoraproject.org> -  0.6-3
- Patch to detect cfitsio in all architectures

* Fri Feb 06 2009 Sergio Pascual <sergiopr at fedoraproject.org> -  0.6-2
- Commands (rm, make) instead of macros
- Upstream bug about licenses (GPLv2 missing)
- Upstream bug about libindi calling exit

* Mon Jan 28 2009 Sergio Pascual <sergiopr at fedoraproject.org> -  0.6-1
- First version

