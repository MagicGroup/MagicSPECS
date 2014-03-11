Name:           iw
Version:        3.3
Release:        2%{?dist}
Summary:        A nl80211 based wireless configuration tool

Group:          System Environment/Base
License:        ISC
URL:            http://www.linuxwireless.org/en/users/Documentation/iw
Source0:        http://wireless.kernel.org/download/iw/iw-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kernel-headers >= 2.6.24 
BuildRequires:  libnl-devel >= 1.0
BuildRequires:  pkgconfig      

%description
iw is a new nl80211 based CLI configuration utility for wireless devices.
Currently you can only use this utility to configure devices which
use a mac80211 driver as these are the new drivers being written - 
only because most new wireless devices being sold are now SoftMAC.

%prep
%setup -q


%build
make %{?smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} MANDIR=%{_mandir}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%{_datadir}/man/man8/iw.*
%doc COPYING

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.3-2
- 为 Magic 3.0 重建

* Wed Jan 18 2012 John W. Linville <linville@redhat.com> 3.3-1
- Update to 3.3

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov  7 2011 John W. Linville <linville@redhat.com> 3.2-1
- Update to 3.2

* Wed Sep 14 2011 John W. Linville <linville@redhat.com> 3.1-1
- Update to 3.1

* Sun Mar 13 2011 Adel Gadllah <adel.gadllah@gmail.com> 0.9.22-1
- Update to 0.9.22

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.9.21-2
- Rebuilt for gcc bug 634757

* Sun Sep 26 2010 Adel Gadllah <adel.gadllah@gmail.com> 0.9.21-1
- Update to 0.9.21

* Wed Jul 14 2010 John W. Linville <linville@redhat.com> 0.9.20-1
- Update to 0.9.20

* Thu Jan 14 2010 John W. Linville <linville@redhat.com> 0.9.19-2
- Correct license tag from BSD to ISC

* Thu Jan 14 2010 John W. Linville <linville@redhat.com> 0.9.19-1
- Update to 0.9.19

* Tue Dec 21 2009 John W. Linville <linville@redhat.com> 0.9.18-4
- Remove unnecessary explicit Requires of libnl -- oops!

* Tue Dec 21 2009 John W. Linville <linville@redhat.com> 0.9.18-3
- Add libnl to Requires

* Wed Dec 18 2009 John W. Linville <linville@redhat.com> 0.9.18-2
- BuildRequires kernels-headers instead of kernel-devel

* Wed Dec  2 2009 John W. Linville <linville@redhat.com> 0.9.18-1
- Update to 0.9.18

* Thu Oct  1 2009 John W. Linville <linville@redhat.com> 0.9.17-3
- Install in /sbin

* Fri Sep  4 2009 John W. Linville <linville@redhat.com> 0.9.17-2
- Revert "separate commands into sections", section type conflicts on ppc64

* Fri Sep  4 2009 John W. Linville <linville@redhat.com> 0.9.17-1
- Update to 0.9.17

* Mon Aug 17 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.9.16-1
- Update to 0.9.16

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.9.15-1
- Update to 0.9.15

* Wed May 13 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.9.14-1
- Update to 0.9.14

* Tue May  2 2009 John W. Linville <linville@redhat.com> 0.9.13-1
- Update to 0.9.13

* Mon Apr 15 2009 John W. Linville <linville@redhat.com> 0.9.12-1
- Update to 0.9.12

* Mon Apr  6 2009 John W. Linville <linville@redhat.com> 0.9.11-1
- Update to 0.9.11

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 10 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.9.7-1
- Update to 0.9.7

* Sun Oct 26 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.9.6-1
- Update to 0.9.6

* Sun Sep 28 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.9.5-3
- Use offical tarball

* Sun Sep 28 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.9.5-2
- Fix BuildRequires

* Sun Sep 28 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.9.5-1
- Update to 0.9.5

* Tue Jul 22 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.0-0.3.20080703gitf6fc7dc
- Add commitid to version
- Use versioned buildrequires for kernel-devel

* Thu Jul 3 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.0-0.2.20080703git
- Add tarball instructions
- Fix install
- Fix changelog

* Thu Jul 3 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.0-0.1.20080703git
- Initial build
