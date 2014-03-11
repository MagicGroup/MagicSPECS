%define pre_release 0
%if %{pre_release}
%define pre_version .pre22
%endif

Summary: Wireless ethernet configuration tools
Group: System Environment/Base
License: GPL+
Name: wireless-tools
Version: 29
Release: 9.1%{?pre_version}%{?dist}
Epoch: 1
URL: http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/Tools.html
Source: http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/wireless_tools.%{version}%{?pre_version}.tar.gz
Patch1: wireless-tools-29-makefile.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

# This is artificial, for packaging purposes.  The presumption is that
# wireless users will install this package, so they will want crda too.
# This avoids adding a Requires to the kernel package that would affect
# non-wireless users as well.
Requires: crda

%description
This package contain the Wireless tools, used to manipulate
the Wireless Extensions. The Wireless Extension is an interface
allowing you to set Wireless LAN specific parameters and get the
specific stats for wireless networking equipment.

%package devel
Summary: Development headers for the wireless-tools package
Group: Development/Libraries
Requires: wireless-tools = %{epoch}:%{version}-%{release}

%description devel
Development headers for the wireless-tools package.


%prep
%if %{pre_release}
if [ "$(echo %{release} | sed -e 's/\..*$//')" -ne "0" ]; then
  echo "*** The Release: value for a pre-release version must be less than 1. ***"
  exit 1
fi
%endif

%setup -q -n wireless_tools.%{version}
%patch1 -p1 -b .makefile

%build
make clean
make OPT_FLAGS="$RPM_OPT_FLAGS" BUILD_SHARED=1 FORCE_WEXT_VERSION=16

%install
%{__rm} -rf $RPM_BUILD_ROOT

%{__mkdir_p} $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_includedir},%{_libdir}}

make install INSTALL_DIR=$RPM_BUILD_ROOT%{_sbindir} \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_INC=$RPM_BUILD_ROOT%{_includedir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/libiw.a

magic_rpm_clean.sh

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc INSTALL README DISTRIBUTIONS.txt
%{_sbindir}/*
%{_mandir}/man*/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1:29-9.1
- 为 Magic 3.0 重建

* Mon Apr 23 2012 Liu Di <liudidi@gmail.com> - 1:29-8.1
- 为 Magic 3.0 重建

* Thu Feb 23 2012 Liu Di <liudidi@gmail.com> - 1:29-7.1
- 为 Magic 3.0 重建

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:29-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 01 2009 Karsten Hopp <karsten@redhat.com> 29-5.1
- drop excludearch s390x as at least the headers are required to build p.e. NetworkManager

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 John W. Linville <linville@redhat.com> - 1:29-3
- Add artificial crda requirement for packaging reasons

* Mon Feb 18 2008 Christopher Aillon <caillon@redhat.com> - 1:29-2
- Rebuild to celebrate my birthday (and GCC 4.3)

* Sat Dec 22 2007 Christopher Aillon <caillon@redhat.com> - 1:29-1
- Update to v29 stable release
- Some minor cleanups for merge review

* Fri Aug 24 2007 Christopher Aillon <caillon@redhat.com> - 1:29-0.2.pre22
- Rebuild

* Mon Aug 13 2007 Christopher Aillon <caillon@redhat.com> - 1:29-0.1.pre22
- Update to 29pre22
- Update the license tag

* Tue May 22 2007 Christopher Aillon <caillon@redhat.com> - 1:29-0.1.pre21
- Update to 29pre21

* Mon May 14 2007 Christopher Aillon <caillon@redhat.com> - 1:28-3
- Only the sscanf fixes this time.

* Mon Apr 30 2007 Christopher Aillon <caillon@redhat.com> - 1:28-2
- Backport a few 64bit alignment fixes from the latest betas.

* Tue Aug 29 2006 Christopher Aillon <caillon@redhat.com> - 1:28-1
- Update to the latest stable release
- Create -devel subpackage for headers

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:28-0.pre16.1.6.1
- rebuild

* Thu Apr  6 2006 Dan Williams <dcbw@redhat.com> - 1:28-0.pre16.1
- Update to 28 pre16
- Rebuild for WE-20

* Sun Feb 12 2006 Christopher Aillon <caillon@redhat.com> - 1:28-0.pre13.5.1
- Update to 28 pre13

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:28-0.pre10.5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Oct 17 2005 Christopher Aillon <caillon@redhat.com> 28-0pre10
- Update to version 28 pre10

* Mon Sep 12 2005 Dan Williams <dcbw@redhat.com> 28-0.pre9
- Update to version 28 pre9

* Wed Aug 17 2005 Dan Williams <dcbw@redhat.com> 28-0.pre8
- Update to 28 pre8

* Fri Aug 05 2005 Florian La Roche <laroche@redhat.com>
- build with current rpm

* Mon Jan 17 2005 Dan Williams <dcbw@redhat.com> 28-0.pre4
- Update to latest wireless-tools

* Mon Nov 08 2004 Dan Williams <dcbw@redhat.com> 27-0.pre25-4
- Fix massive leak in iw_process_scan()

* Mon Sep 27 2004 Rik van Riele <riel@redhat.com> 27-0.pre25-2
- compile with RPM_OPT_FLAGS (bz#133651)

* Tue Aug 31 2004 Bill Nottingham <notting@redhat.com> 27-0.pre25.1
- update to 27.pre25

* Wed Jun 23 2004 Dan Williams <dcbw@redhat.com>
- Upgrade to 27.pre23 to get new wireless scanning API

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Mar 15 2004 Bill Nottingham <notting@redhat.com>
- force wireless extensions to current (#115707)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Aug 31 2003 Bill Nottingham <notting@redhat.com> 26-2
- rebuild in different environment (#103475)

* Sun Aug 10 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- release 26

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Mar 09 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- also change destination of the symlink

* Mon Feb 17 2003 Bill Nottingham <notting@redhat.com> 25-8
- fix symlink (#84021)

* Mon Feb 10 2003 Bill Nottingham <notting@redhat.com> 25-7
- fix symlink (#84021)

* Fri Feb  7 2003 Bill Nottingham <notting@redhat.com> 25-6
- remove broken specfile defines, fix makefile (#82423)

* Wed Feb  5 2003 Bill Nottingham <notting@redhat.com> 25-5
- rebuild against new glibc-kernheaders (#82423)

* Fri Jan 31 2003 Elliot Lee <sopwith@redhat.com> 25-4
- Fix for multilib, and fix the .so symlink location.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 25-2
- rebuild on all arches

* Mon Aug 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 25-1
- v25 - fixes encryption usage display, eternal loops for unknown 
  events and matches the v13 wireless extensions as shipped in
  kernel (#72582)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 20 2002 Trond Eivind Glomsrød <teg@redhat.com> 24-1
- v24

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Mar 21 2002 Bill Nottingham <notting@redhat.com> 23-2
- rebuild against new headers

* Thu Feb 28 2002 Elliot Lee <sopwith@redhat.com> 23-1
- Update to version 23, with associated fixes.

* Sun Jul  8 2001 Bill Nottingham <notting@redhat.com>
- rebuild against new kernel

* Tue Jun 19 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add ExcludeArch: s390 s390x

* Sun Apr 22 2001 Bill Nottingham <notting@redhat.com>
- update to version 21

* Wed Feb 14 2001 Bill Nottingham <notting@redhat.com>
- fix build with glibc-2.2
- also, rebuild so it no longer dumps core. :)

* Tue Dec 05 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- added a clean section in the spec file

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Mar 10 2000 Bill Nottingham <notting@redhat.com>
- initial build
