%define         crda_version    3.18
%define         regdb_version   2015.10.22

Name:           crda
Version:        %{crda_version}_%{regdb_version}
Release:        5%{?dist}
Summary:        Regulatory compliance daemon for 802.11 wireless networking

Group:          System Environment/Base
License:        ISC
URL:            http://www.linuxwireless.org/en/developers/Regulatory/CRDA
BuildRoot:      %{_tmppath}/%{name}-%{crda_version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kernel-headers >= 2.6.27
BuildRequires:  libnl3-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  pkgconfig python m2crypto
BuildRequires:  openssl

Requires:       udev, iw
Requires:       systemd >= 190

Source0:        http://www.kernel.org/pub/software/network/crda/crda-%{crda_version}.tar.xz
Source1:        http://www.kernel.org/pub/software/network/wireless-regdb/wireless-regdb-%{regdb_version}.tar.xz
Source2:        setregdomain
Source3:        setregdomain.1

# Add udev rule to call setregdomain on wireless device add
Patch0:         regulatory-rules-setregdomain.patch
# Do not call ldconfig in crda Makefile
Patch2:         crda-remove-ldconfig.patch


%description
CRDA acts as the udev helper for communication between the kernel
and userspace for regulatory compliance. It relies on nl80211
for communication. CRDA is intended to be run only through udev
communication from the kernel.


%package devel
Summary:        Header files for use with libreg. 
Group:          Development/System


%description devel
Header files to make use of libreg for accessing regulatory info.


%prep
%setup -q -c
%setup -q -T -D -a 1

cd crda-%{crda_version}
%patch2 -p1 -b .ldconfig-remove

%build
export CFLAGS="%{optflags}"

# Use our own signing key to generate regulatory.bin
cd wireless-regdb-%{regdb_version}

make %{?_smp_mflags} maintainer-clean
make %{?_smp_mflags} REGDB_PRIVKEY=key.priv.pem REGDB_PUBKEY=key.pub.pem

# Build CRDA using the new key and regulatory.bin from above
cd ../crda-%{crda_version}
cp ../wireless-regdb-%{regdb_version}/key.pub.pem pubkeys

make %{?_smp_mflags} SBINDIR=%{_sbindir}/ LIBDIR=%{_libdir}/ \
	REG_BIN=../wireless-regdb-%{regdb_version}/regulatory.bin


%install
rm -rf %{buildroot}

cd crda-%{crda_version}
cp README README.crda
make install DESTDIR=%{buildroot} MANDIR=%{_mandir}/ \
	SBINDIR=%{_sbindir}/ LIBDIR=%{_libdir}/

cd ../wireless-regdb-%{regdb_version}
cp README README.wireless-regdb
make install DESTDIR=%{buildroot} MANDIR=%{_mandir}

install -D -pm 0755 %SOURCE2 %{buildroot}%{_sbindir}
install -D -pm 0644 %SOURCE3 %{buildroot}%{_mandir}/man1/setregdomain.1


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%{_sbindir}/regdbdump
%{_sbindir}/setregdomain
%{_libdir}/libreg.so
/lib/udev/rules.d/85-regulatory.rules
# location of database is hardcoded to /usr/lib/%{name}
/usr/lib/%{name}
%{_mandir}/man1/setregdomain.1*
%{_mandir}/man5/regulatory.bin.5*
%{_mandir}/man8/crda.8*
%{_mandir}/man8/regdbdump.8*
%doc crda-%{crda_version}/LICENSE crda-%{crda_version}/README.crda
%doc wireless-regdb-%{regdb_version}/README.wireless-regdb


%files devel
%{_includedir}/reglib/nl80211.h
%{_includedir}/reglib/regdb.h
%{_includedir}/reglib/reglib.h



%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 3.18_2015.10.22-5
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 3.18_2015.10.22-4
- 更新到 3.18_2015.10.22

* Fri Feb 28 2014 John W. Linville <linville@redhat.com> - 3.13_2013.11.27-2
- Accomodate relative pathnames in the symlink for /etc/localtime

* Fri Feb 14 2014 John W. Linville <linville@redhat.com> - 3.13_2013.11.27-1
- Update crda to version 3.13
- Remove obsolete patch for regdbdump to display DFS region
- Add patch to use DESTDIR rule for crda libreg installation
- Add patch to avoid calling ldconfig from crda Makefile
- Remove PREFIX='' lines from make commands
- Use SBINDIR and LIBDIR definitions in make commands

* Thu Jan 23 2014 John W. Linville <linville@redhat.com> - 1.1.3_2013.11.27-3
- Correct a typo in setregdomain

* Fri Jan 17 2014 John W. Linville <linville@redhat.com> - 1.1.3_2013.11.27-2
- Add patch for regdbdump to display DFS region

* Mon Dec  2 2013 John W. Linville <linville@redhat.com> - 1.1.3_2013.11.27-1
- Update wireless-regdb to version 2013.11.27

* Fri Nov 22 2013 Xose Vazquez Perez <xose.vazquez@gmail.com> - 1.1.3_2013.02.13-5
- fixed wrong dates
- link with libnl3
- new home for sources

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3_2013.02.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr  3 2013 John W. Linville <linville@redhat.com> - 1.1.3_2013.02.13-3
- setregdomain: remove sed and awk calls
- setregdomain: reimplement COUNTRY assignment with shell function

* Fri Mar  1 2013 John W. Linville <linville@redhat.com> - 1.1.3_2013.02.13-2
- Bump release to prevent upgrade issues from F17...oops!

* Wed Feb 13 2013 John W. Linville <linville@redhat.com> - 1.1.3_2013.02.13-1
- Update wireless-regdb to version 2013.02.13

* Tue Feb 12 2013 John W. Linville <linville@redhat.com> - 1.1.3_2013.02.12-1
- Update wireless-regdb to version 2013.02.12

* Fri Jan 25 2013 John W. Linville <linville@redhat.com> - 1.1.3_2013.01.11-2
- Update setregdomain to determine timezone info from /etc/timezone

* Fri Jan 25 2013 John W. Linville <linville@redhat.com> - 1.1.3_2013.01.11-1
- Update crda to version 1.1.3
- Update wireless-regdb to version 2013.01.11

* Fri Aug 10 2012 John W. Linville <linville@redhat.com>
- Add BuildRequires for openssl

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2_2011.04.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2_2011.04.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 11 2011 John W. Linville <linville@redhat.com> 1.1.2_2011.04.28-1
- Update crda to version 1.1.2
- Update wireless-regdb to version 2011.04.28 
- Fix mis-numbered version comment in changelog for Nov 23 2010

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1_2010.11.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 23 2010 John W. Linville <linville@redhat.com> 1.1.1_2010.11.22-1
- Update wireless-regdb to version 2010.11.22 

* Thu Feb 25 2010 John W. Linville <linville@redhat.com> 1.1.1_2009.11.25-3
- Correct license tag from BSD to ISC
- Comment purpose of regulatory-rules-setregdomain.patch
- Add copyright and license statement to setregdomain
- Add comment for why /lib is hardcoded in files section
- Reformat Dec 21 2009 changelog entry so rpmlint stops complaining

* Tue Jan 26 2010 John W. Linville <linville@redhat.com> 1.1.1_2009.11.25-2
- Change RPM_OPT_FLAGS to optflags
- Leave man page compression to rpmbuild
- Correct date in previous changelog entry

* Tue Jan 26 2010 John W. Linville <linville@redhat.com> 1.1.1_2009.11.25-1
- Update for crda version 1.1.1

* Mon Dec 21 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.11.25-5
- Remove unnecessary explicit Requries for libgcrypt and libnl -- oops!

* Mon Dec 21 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.11.25-4
- Add libgcrypt and libnl to Requires

* Mon Dec 21 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.11.25-3
- Add man page for setregdomain (from Andrew Hecox <ahecox@redhat.com>)
- Change $RPM_BUILD_ROOT to buildroot

* Fri Dec 18 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.11.25-2
- Specify path to iw in setregdomain

* Wed Dec  2 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.11.25-1
- Update wireless-regdb to version 2009.11.25 

* Wed Nov 11 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.11.10-1
- Update wireless-regdb to version 2009.11.10 

* Thu Oct  1 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.09.08-3
- Move regdb to /lib/crda to facilitate /usr mounted over wireless network

* Wed Sep  9 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.09.08-2
- Use kernel-headers instead of kernel-devel

* Wed Sep  9 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.09.08-1
- Update wireless-regdb to version 2009.09.08 
- Start resetting release number with version updates

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0_2009.04.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 13 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.04.17-11
- Update crda version to version 1.1.0
- Update wireless-regdb to version 2009.04.17 

* Fri Apr 17 2009 John W. Linville <linville@redhat.com> 1.0.1_2009.04.16-10
- Update wireless-regdb version to pick-up recent updates and fixes (#496392)

* Tue Mar 31 2009 John W. Linville <linville@redhat.com> 1.0.1_2009.03.09-9
- Add Requires line for iw package (#492762)
- Update setregdomain script to correctly check if COUNTRY is set

* Thu Mar 19 2009 John W. Linville <linville@redhat.com> 1.0.1_2009.03.09-8
- Add setregdomain script to set regulatory domain based on timezone
- Expand 85-regulatory.rules to invoke setregdomain script on device add

* Tue Mar 10 2009 John W. Linville <linville@redhat.com> 1.0.1_2009.03.09-7
- Update wireless-regdb version to pick-up recent updates and fixes (#489560)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1_2009.01.30-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 John W. Linville <linville@redhat.com> 1.0.1_2009.01.30-5
- Recognize regulatory.bin files signed with the upstream key (#484982)

* Tue Feb 03 2009 John W. Linville <linville@redhat.com> 1.0.1_2009.01.30-4
- Change version to reflect new wireless-regdb upstream release practices
- Update wireless-regdb version to pick-up recent updates and fixes (#483816)

* Tue Jan 27 2009 John W. Linville <linville@redhat.com> 1.0.1_2009_01_15-3
- Update for CRDA verion 1.0.1
- Account for lack of "v" in upstream release tarball naming
- Add patch to let wireless-regdb install w/o being root

* Thu Jan 22 2009 John W. Linville <linville@redhat.com> v0.9.5_2009_01_15-2
- Revamp based on package review comments

* Tue Jan 20 2009 John W. Linville <linville@redhat.com> v0.9.5_2009_01_15-1
- Initial build
