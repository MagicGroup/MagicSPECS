Name:          usbmuxd
Version:       1.1.0
Release:       10%{?dist}
Summary:       Daemon for communicating with Apple's iOS devices
Summary(zh_CN.UTF-8): 和苹果 iOS 设备通信的服务

Group:         Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
# All code is dual licenses as GPLv3+ or GPLv2+, except libusbmuxd which is LGPLv2+.
License:       GPLv3+ or GPLv2+
URL:           http://www.libimobiledevice.org/
Source0:       http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2

BuildRequires: libimobiledevice-devel
BuildRequires: libplist-devel
BuildRequires: libusbx-devel
BuildRequires: systemd

Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# for multilib upgrade path
Obsoletes: usbmuxd < 1.0.9

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch, iPhone, 
iPad and Apple TV devices. It allows multiple services on the device to be 
accessed simultaneously.

%description -l zh_CN.UTF-8
和苹果 iOS 设备通信的服务。

%prep
%setup -q

# Set the owner of the device node to be usbmuxd
sed -i.owner 's/OWNER="usbmux"/OWNER="usbmuxd"/' udev/39-usbmuxd.rules.in
sed -i.user 's/--user usbmux/--user usbmuxd/' systemd/usbmuxd.service.in

%build
%configure

make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%pre
getent group usbmuxd >/dev/null || groupadd -r usbmuxd -g 113
getent passwd usbmuxd >/dev/null || \
useradd -r -g usbmuxd -d / -s /sbin/nologin \
	-c "usbmuxd user" -u 113 usbmuxd
exit 0

%post
%systemd_post usbmuxd.service

%preun
%systemd_preun usbmuxd.service

%postun
%systemd_postun_with_restart usbmuxd.service 

%files
%{!?_licensedir:%global license %%doc}
%license COPYING.GPLv2 COPYING.GPLv3
%doc AUTHORS README
%{_unitdir}/usbmuxd.service
/usr/lib/udev/rules.d/39-usbmuxd.rules
%{_sbindir}/usbmuxd
%{_datadir}/man/man1/usbmuxd.1.gz

%changelog
* Mon Jan 18 2016 Liu Di <liudidi@gmail.com> - 1.1.0-10
- 为 Magic 3.0 重建

* Fri Jan 15 2016 Liu Di <liudidi@gmail.com> - 1.1.0-9
- 为 Magic 3.0 重建

* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 1.1.0-8
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 1.1.0-7
- 为 Magic 3.0 重建

* Sat Oct 17 2015 Liu Di <liudidi@gmail.com> - 1.1.0-6
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 11 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.10-4
- Rebuild (libimobiledevice)

* Tue Feb  3 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.10-3
- Use %%license

* Tue Oct 21 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.10-2
- (rebuild)

* Fri Oct 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.10-1
- New stable 1.1.0 release

* Fri Oct 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.9-3
- Bump for correct overrides

* Fri Oct 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.9-2
- Refresh usbmuxd owner bits

* Wed Oct 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.9-1
- New stable 1.0.9 release

* Tue Sep 09 2014 Rex Dieter <rdieter@fedoraproject.org> - 1.0.9-0.6.c24463e
- Obsoletes: usbmuxd < 1.0.9 (multilib upgrade path)
- move Obsoletes: usbmuxd-devel to libusbmuxd-devel

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-0.5.c24463e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 30 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.9-0.4.c24463e
- Add upstream patch for systemd support

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
