# There's not been a release in a long time for dvb-apps
# We use a Release based on the ChangeSet number and hash
%define hgm 1
%define vcsdate 20151029

Name:    dvb-apps
Version: 1.1.2
Release: 0.hg%{vcsdate}%{?dist}.4
Summary: Utility, demo and test applications using the Linux DVB API
Summary(zh_CN.UTF-8): 使用 Linux DVB API 的工具、示例和测试程序

Group:   Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License: GPLv2+
URL:     http://www.linuxtv.org/wiki/index.php/LinuxTV_dvb-apps

%if 0%{hgm}
Source0: %{name}-hg%{vcsdate}.tar.xz
%else
Source0: http://linuxtv.org/hg/dvb-apps/archive/%{hgver}.tar.bz2
%endif
Source1: make_dvb-apps_hg_package.sh
Patch0:  dvb-apps-Make.patch
Patch1:  dvb-apps-Docs.patch

Autoreq: 0
BuildRequires:  libusb-devel
BuildRequires:  kernel-headers

%description
The LinuxTV dvb-apps package contains some Linux DVB API applications and a set 
of utilities that both the developer and end user alike will find quite useful. 
Specifically, the utilities are geared towards the initial setup, testing, and 
operation of a DVB device, whether it be of the software decoding or hardware 
decoding type.

%description -l zh_CN.UTF-8
使用 Linux DVB API 的工具、示例和测试程序。

%prep
%setup -q -n %{name}-hg%{vcsdate}

# Various fixes to fix various upstream build issues
%patch0 -p1 -b .make
%patch1 -p1 -b docs

# Rename to non generic name
mv util/scan/scan.c util/scan/scandvb.c
mv util/zap/zap.c util/zap/dvbzap.c

# Fix libdir for 64 bit arches
%ifarch x86_64 ia64 ppc64 sparc64 s390x arm64 mips64el
sed -i.lib64 's#$(prefix)/lib#$(prefix)/lib64#' Make.rules 
%endif

cd util
install -pm 644 av7110_loadkeys/README ../README.av7110_loadkeys
install -pm 644 scan/README ../README.scandvb
install -pm 644 szap/README ../README.szap
install -pm 644 ttusb_dec_reset/README ../README.ttusb_dec_reset
chmod 644 dvbnet/net_start.*
cd ..

%build
LDFLAGS="$RPM_LD_FLAGS" make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'
chmod -c +x %{buildroot}%{_libdir}/lib*.so

#Remove static libraries
find %{buildroot} -name '*.a' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README COPYING COPYING.LGPL README.* util/szap/channels-conf
%{_bindir}/*
%{_datadir}/dvb
%{_libdir}/libdvbapi.so
%{_libdir}/libdvbcfg.so
%{_libdir}/libdvben50221.so
%{_libdir}/libdvbsec.so
%{_libdir}/libucsi.so
# Exclude for the moment as they're not used by shipped binaries
%exclude %{_libdir}/libesg.so
%exclude %{_includedir}/*

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.1.2-0.hg20151029.4
- 更新到 20151029 日期的仓库源码

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.1.2-0.hg20140324.3
- 为 Magic 3.0 重建

* Mon Mar 24 2014 Liu Di <liudidi@gmail.com> - 1.1.2-0.hg20140324.2
- 更新到 20140324 日期的仓库源码

* Mon Mar 24 2014 Liu Di <liudidi@gmail.com> - 1.1.2-0.hg20140324.1
- 更新到 20140324 日期的仓库源码

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.1.2-0.1457.bec11f78be51.2
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-0.1457.bec11f78be51.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.1.2-0.1457.bec11f78be51
- Update to latest hg snapshot
- Fix release based on upstream hg
- Build with $RPM_LD_FLAGS - RHBZ #759879
- Fix naming conflicts - RHBZ #757609

* Sat Nov 12 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.1.2-0.d4e8bf5658ce
- Move to hg snapshot d4e8bf5658ce

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jun  5 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-22
- Patch to fix dvbnet -h crash (#597604).
- Update tuning files to 20100605.

* Tue Mar 16 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-21
- Apply upstream patch to add tzap AUTO param support (#574112, AUDU Jerome).
- Update tuning files to 20100316.

* Thu Jan 21 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-20
- Apply patch to fix czap config parsing when built w/gcc 4.4.2 (#557580).
- Update tuning files to 20100121.

* Thu Jan 14 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-19
- Update tuning files to 20100114.

* Thu Aug 20 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-18
- Update tuning files to 20090820.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  2 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-16
- Update tuning files to 20090702.
- Drop no longer needed workaround for #483644.

* Thu Feb 26 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-15
- Add workaround for #483644.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-13
- Update tuning files to 20090222.

* Sat Aug 30 2008 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-12
- Update tuning files to 20080830.
- Convert data files to UTF-8.
- Unfuzz optflags patch.

* Thu Feb 14 2008 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-11
- Update tuning files to 20080214.

* Tue Aug 21 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-10
- Update tuning files to 20070821.

* Mon Aug  6 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-9
- Do not build test binaries we don't run or ship.
- Update tuning files to 20070806.
- Change License tag to GPLv2+.

* Sun May 13 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-8
- Update tuning files to 20070513.
- Drop non-upstream license file.

* Mon Oct  2 2006 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-7
- Rebuild.

* Sat Sep 23 2006 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-6
- Include updated set of initial tuning data files from upstream hg (#203328).

* Tue Aug 29 2006 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-5
- Rebuild.

* Thu May 18 2006 Ville Skyttä <ville.skytta@iki.fi> - 1.1.1-4
- Include ATSC initial tuning data files.

* Thu May 18 2006 David Woodhouse <dwmw2@infradead.org> - 1.1.1-2
- Rebuild (to unfix kernel-headers on older distros)

* Thu May 18 2006 David Woodhouse <dwmw2@infradead.org> - 1.1.1-1
- Update to dvb-apps 1.1.1 (add ATSC functionality)
- Fix kernel-headers BR

* Tue Feb 21 2006 Ville Skyttä <ville.skytta@iki.fi> - 1.1.0-2
- Rebuild.

* Sun Jul 17 2005 Ville Skyttä <ville.skytta@iki.fi> - 1.1.0-1
- Include a copy of the GPL.

* Thu Jun 30 2005 Ville Skyttä <ville.skytta@iki.fi> - 1.1.0-0.4
- Update URL.

* Sun May 29 2005 Ville Skyttä <ville.skytta@iki.fi> - 1.1.0-0.3
- Rebuild for FC4.

* Wed Apr 20 2005 Ville Skyttä <ville.skytta@iki.fi> - 1.1.0-0.2
- Switch to recent glibc-kernheaders which includes userspace DVB headers.

* Sun Dec 26 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:1.1.0-0.1
- Remove unnecessary Epochs.

* Mon Oct  4 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:1.1.0-0.scop.1
- First build, loosely based on Mandrake's 1.1.0-4mdk.

