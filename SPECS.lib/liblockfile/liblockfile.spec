Name:           liblockfile
Version:        1.08
Release:        13%{?dist}
Summary:        This implements a number of functions found in -lmail on SysV systems

Group:          Applications/System
# regarding license please see file COPYRIGHT
License:        GPLv2+ 
URL:            http://packages.qa.debian.org/libl/liblockfile.html
Source0:        http://ftp.de.debian.org/debian/pool/main/libl/liblockfile/liblockfile_1.08.orig.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This library implements a number of functions found in -lmail on SysV
systems. These functions are designed to lock the standard mailboxes in
/var/mail (or wherever the system puts them).

In additions, this library adds a number of functions to create,
manage and remove generic lockfiles.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel 
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}

# remove -g root from install
sed -i "s/install -g root -m 755 dotlockfile \$(ROOT)\$(bindir);/install -m 755 dotlockfile \$(ROOT)\$(bindir);/" Makefile.in


%build
%configure --enable-shared
make %{?_smp_mflags} 


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_includedir}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_mandir}/man1
mkdir -p %{buildroot}/%{_mandir}/man3
make ROOT=%{buildroot} install

ldconfig -N -n %{buildroot}/%{_libdir}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/dotlockfile
%{_libdir}/liblockfile.so.1.0
%{_libdir}/liblockfile.so.1
%{_mandir}/man1/dotlockfile.1*
%doc README COPYRIGHT Changelog


%files devel
%defattr(-,root,root,-)
%{_libdir}/liblockfile.so
%{_includedir}/maillock.h
%{_includedir}/lockfile.h
%{_mandir}/man3/lockfile_create.3*
%{_mandir}/man3/maillock.3*


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.08-13
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Aug 14 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08.10
- replace linking of libs with ldconfig

* Fri Aug 6 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-9
- change description and summary of -devel-subpackage
- make wildcard for man-pages even match against uncompressed files

* Fri Aug 6 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-8
- rename to liblockfile
- sorting file to main and -devel package
- explicitly list files in files-section

* Fri Aug 6 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-7
- remove COPYRIGHT from devel
- just fix one missing link from upstream

* Thu Aug 5 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-6
- include COPYRIGHT in -devel, too
- remove unnecessary exclude

* Tue Aug 3 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-5
- fix shared lib warning, sort lib to devel
- choose GPLv2+ as License (until we know better)

* Wed Jul 28 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-4
- rename to lockfile
- sort lib to top package, fix license, build shared lib

* Sun Jul 18 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-3
- fix up hidden dirs, and links

* Wed Jun 30 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-2
- replace patch by sed-script

* Sat May 22 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-1
- initial build
