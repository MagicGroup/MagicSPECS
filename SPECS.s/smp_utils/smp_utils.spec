Summary:        Utilities for SAS management protocol (SMP)
Name:           smp_utils
Version:        0.96
Release:        3%{?dist}
License:        BSD
Group:          Applications/System
URL:            http://sg.danny.cz/sg/smp_utils.html
Source0:        http://sg.danny.cz/sg/p/%{name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
This is a package of utilities. Each utility sends a Serial Attached
SCSI (SAS) Management Protocol (SMP) request to a SMP target.
If the request fails then the error is decoded. If the request succeeds
then the response is either decoded, printed out in hexadecimal or
output in binary. This package supports multiple interfaces since
SMP passthroughs are not mature. This package supports the linux
2.4 and 2.6 series and should be easy to port to other operating
systems.

Warning: Some of these tools access the internals of your system
and the incorrect usage of them may render your system inoperable.


%prep
%setup -q


%build
make %{?smp_mflags} CFLAGS="%{optflags} -DSMP_UTILS_LINUX"


%install
rm -rf %{buildroot}

make install \
        PREFIX=%{_prefix} \
        DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING COVERAGE CREDITS INSTALL README
%{_bindir}/*
%{_mandir}/man8/*


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.96-3
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Dan Horák <dan[at]danny.cz> 0.96-1
- updated to 0.96

* Fri Feb 18 2011 Dan Horák <dan[at]danny.cz> 0.95-1
- updated to 0.95

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.94-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.94-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar  9 2009 Dan Horák <dan[at]danny.cz> 0.94-2
- update BuildRoot

* Mon Feb  2 2009 Dan Horák <dan[at]danny.cz> 0.94-1
- update for Fedora compliance

* Mon Dec 29 2008 - dgilbert at interlog dot com
- adjust sgv4 for lk 2.6.27, sync with sas2r15
  * smp_utils-0.94
* Sun Jan 06 2008 - dgilbert at interlog dot com
- sync with sas2r13, add 'sgv4' interface
  * smp_utils-0.93
* Fri Dec 08 2006 - dgilbert at interlog dot com
- sync against sas2r07, add smp_conf_general
  * smp_utils-0.92
* Tue Aug 22 2006 - dgilbert at interlog dot com
- add smp_phy_test and smp_discover_list, uniform exit status values
  * smp_utils-0.91
* Sun Jun 11 2006 - dgilbert at interlog dot com
- add smp_read_gpio, smp_conf_route_info and smp_write_gpio
  * smp_utils-0.90
