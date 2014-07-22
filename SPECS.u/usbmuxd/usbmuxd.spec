# Tarfile created using git
# git clone https://github.com/libimobiledevice/usbmuxd.git
# git archive --format=tar --prefix=%{name}-%{version}/ %{name}-%{version} | bzip2 > ~/%{name}-%{version}.tar.bz2
# c24463e

%define gittag c24463e
%define tarfile %{name}-%{version}-%{gittag}.tar.bz2

Name:          usbmuxd
Version:       1.0.9
Release:       0.4.%{gittag}%{?dist}
Summary:       Daemon for communicating with Apple's iOS devices

Group:         Applications/System
# All code is dual licenses as GPLv3+ or GPLv2+, except libusbmuxd which is LGPLv2+.
License:       GPLv3+ or GPLv2+
URL:           http://www.libimobiledevice.org/
#ource0:       http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
Source0:       %{tarfile}
Patch0:        usbmuxd-use-systemd-to-start-usbmuxd.patch
Patch1:        usbmuxd-default-source.patch

BuildRequires: libimobiledevice-devel
BuildRequires: libplist-devel
BuildRequires: libusbx-devel
BuildRequires: systemd
BuildRequires: autoconf automake libtool

Requires(pre): shadow-utils
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Obsoletes: usbmuxd-devel < 1.0.9

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch, iPhone, 
iPad and Apple TV devices. It allows multiple services on the device to be 
accessed simultaneously.

%prep
%setup -q
%patch0 -p1 -b .systemd
%patch1 -p1 -b .def-src

# Set the owner of the device node to be usbmuxd
sed -i.owner 's/OWNER="usbmux"/OWNER="usbmuxd"/' udev/39-usbmuxd.rules.in
sed -i.user 's/-U usbmux/-U usbmuxd/' udev/usbmuxd.service.in

%build
NOCONFIGURE=1 ./autogen.sh
CFLAGS=-D_BSD_SOURCE %configure 

make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT
# Short term hack
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
cp udev/usbmuxd.service.in $RPM_BUILD_ROOT/%{_unitdir}/usbmuxd.service

%pre
getent group usbmuxd >/dev/null || groupadd -r usbmuxd -g 113
getent passwd usbmuxd >/dev/null || \
useradd -r -g usbmuxd -d / -s /sbin/nologin \
	-c "usbmuxd user" -u 113 usbmuxd
exit 0

%post
/sbin/ldconfig
%systemd_post usbmuxd.service

%preun
%systemd_preun usbmuxd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart usbmuxd.service 

%files
%doc AUTHORS README COPYING.GPLv2 COPYING.GPLv3
/lib/udev/rules.d/39-usbmuxd.rules
%{_unitdir}/usbmuxd.service
%{_sbindir}/usbmuxd

%changelog
* Mon Jul 21 2014 Liu Di <liudidi@gmail.com> - 1.0.9-0.4.c24463e
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-0.3.c24463e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 21 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.9-0.2
- Minor update

* Mon Apr 21 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.9-0.1
- Initial 1.0.9 snapshot

* Thu Oct 10 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.0.8-10
- Add BR: systemd for systemd.macros (RHBZ #1017493).

* Tue Oct 8  2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.8-9
- Fix rpm scripts

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Bastien Nocera <bnocera@redhat.com> 1.0.8-6
- Fix source URL

* Thu Oct  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.8-5
- Make use of the new systemd macros
- Minor updates to spec

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Bastien Nocera <bnocera@redhat.com> 1.0.8-3
- Use systemd to start usbmuxd instead of udev (#786853)

* Sat Apr 28 2012 Bastien Nocera <bnocera@redhat.com> 1.0.8-2
- Fix usbmuxd not starting under udev

* Mon Apr  9 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.8-1
- New stable 1.0.8 release

* Thu Feb  2 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.7-3
- Add debian patch for CVE-2012-0065. Fixes RHBZ 783523

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 22 2011 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.7-1
- New stable 1.0.7 release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 24 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.6-1
- New stable 1.0.6 release

* Fri Jul 23 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.5-1
- New stable 1.0.5 release

* Fri May 28 2010 Bastien Nocera <bnocera@redhat.com> 1.0.4-3
- Fix udev rule to use the usbmuxd user

* Wed May 12 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.4-2
- Actually upload a source file

* Tue May 11 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.4-1
- New stable 1.0.4 release

* Mon Mar 22 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.3-1
- New stable 1.0.3 release

* Thu Feb 11 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.2-1
- New stable 1.0.2 release

* Tue Feb 09 2010 Bastien Nocera <bnocera@redhat.com> 1.0.0-3
- Use the gid/uid reserved for usbmuxd in setup 2.8.15 and above

* Fri Jan 29 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-2
- Run deamon under the usbmuxd user

* Mon Dec  7 2009 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-1
- New stable 1.0.0 release

* Sat Oct 31 2009 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-0.1.rc2
- New 1.0.0-rc2 test release

* Thu Oct 29 2009 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-0.2.rc1
- Add patch to fix install of 64 bit libs

* Tue Oct 27 2009 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-0.1.rc1
- New 1.0.0-rc1 test release

* Fri Aug 14 2009 Bastien Nocera <bnocera@redhat.com> 0.1.4-2
- Make usbmuxd autostart on newer kernels
- (Still doesn't exit properly though)

* Mon Aug 10 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.4-1
- Update to 0.1.4

* Tue Aug  4 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.3-1
- Update to 0.1.3, review input

* Mon Aug  3 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.2-1
- Update to 0.1.2

* Mon Aug  3 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.1-1
- Initial packaging
