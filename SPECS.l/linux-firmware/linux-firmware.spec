%global checkout 7560108
%global iwlwifi_release 11

Name:		linux-firmware
Version:	20120720
Release:	0.2.git%{checkout}%{?dist}
Summary:	Firmware files used by the Linux kernel

Group:		System Environment/Kernel
License:	GPL+ and GPLv2+ and MIT and Redistributable, no modification permitted
URL:		http://www.kernel.org/
Source0:	ftp://ftp.kernel.org/pub/linux/kernel/people/dwmw2/firmware/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Provides:	kernel-firmware = %{version} xorg-x11-drv-ati-firmware = 7.0
Obsoletes:	kernel-firmware < %{version} xorg-x11-drv-ati-firmware < 6.13.0-0.22
Obsoletes:	ueagle-atm4-firmware < 1.0-5
# The netxen firmware gets independently updated, so we'll use it instead of 
# whatever happens to be in the last checkout.
Requires:	netxen-firmware
BuildRequires: git

%description
Kernel-firmware includes firmware files required for some devices to
operate.

%package -n iwl100-firmware
Summary:	Firmware for Intel(R) Wireless WiFi Link 100 Series Adapters
License:	Redistributable, no modification permitted
Version:	39.31.5.1
Release:	%{iwlwifi_release}%{?dist}
Obsoletes:	iwl100-firmware < iwl100-firmware-39.31.5.1-4
%description -n iwl100-firmware
This package contains the firmware required by the iwlagn driver
for Linux to support the iwl100 hardware.  Usage of the firmware
is subject to the terms and conditions contained inside the provided
LICENSE file. Please read it carefully.

%package -n iwl105-firmware
Summary:	Firmware for Intel(R) Centrino Wireless-N 105 Series Adapters
License:	Redistributable, no modification permitted
Version:	18.168.6.1
Release:	%{iwlwifi_release}%{?dist}
%description -n iwl105-firmware
This package contains the firmware required by the iwlagn driver
for Linux to support the iwl105 hardware.  Usage of the firmware
is subject to the terms and conditions contained inside the provided
LICENSE file. Please read it carefully.

%package -n iwl135-firmware
Summary:	Firmware for Intel(R) Centrino Wireless-N 135 Series Adapters
License:	Redistributable, no modification permitted
Version:	18.168.6.1
Release:	%{iwlwifi_release}%{?dist}
%description -n iwl135-firmware
This package contains the firmware required by the iwlagn driver
for Linux to support the iwl135 hardware.  Usage of the firmware
is subject to the terms and conditions contained inside the provided
LICENSE file. Please read it carefully.

%package -n iwl1000-firmware
Summary:	Firmware for Intel® PRO/Wireless 1000 B/G/N network adaptors
License:	Redistributable, no modification permitted
Version:	39.31.5.1
Release:	%{iwlwifi_release}%{?dist}
Obsoletes:	iwl1000-firmware < 1:39.31.5.1-3
%description -n iwl1000-firmware
This package contains the firmware required by the iwlagn driver
for Linux to support the iwl1000 hardware.  Usage of the firmware
is subject to the terms and conditions contained inside the provided
LICENSE file. Please read it carefully.

%package -n iwl2000-firmware
Summary:	Firmware for Intel(R) Centrino Wireless-N 2000 Series Adapters
License:	Redistributable, no modification permitted
Version:	18.168.6.1
Release:	%{iwlwifi_release}%{?dist}
%description -n iwl2000-firmware
This package contains the firmware required by the iwlagn driver
for Linux to support the iwl2000 hardware.  Usage of the firmware
is subject to the terms and conditions contained inside the provided
LICENSE file. Please read it carefully.

%package -n iwl2030-firmware
Summary:	Firmware for Intel(R) Centrino Wireless-N 2030 Series Adapters
License:	Redistributable, no modification permitted
Version:	18.168.6.1
Release:	%{iwlwifi_release}%{?dist}
%description -n iwl2030-firmware
This package contains the firmware required by the iwlagn driver
for Linux to support the iwl2030 hardware.  Usage of the firmware
is subject to the terms and conditions contained inside the provided
LICENSE file. Please read it carefully.

%package -n iwl3945-firmware
Summary:	Firmware for Intel® PRO/Wireless 3945 A/B/G network adaptors
License:	Redistributable, no modification permitted
Version:	15.32.2.9
Release:	%{iwlwifi_release}%{?dist}
Obsoletes:	iwl3945-firmware < 15.32.2.9-7
%description -n iwl3945-firmware
This package contains the firmware required by the iwl3945 driver
for Linux.  Usage of the firmware is subject to the terms and conditions
contained inside the provided LICENSE file. Please read it carefully.

%package -n iwl4965-firmware
Summary:	Firmware for Intel® PRO/Wireless 4965 A/G/N network adaptors
License:	Redistributable, no modification permitted
Version:	228.61.2.24
Release:	%{iwlwifi_release}%{?dist}
Obsoletes:	iwl4965-firmware < 228.61.2.24-5
%description -n iwl4965-firmware
This package contains the firmware required by the iwl4965 driver
for Linux.  Usage of the firmware is subject to the terms and conditions
contained inside the provided LICENSE file. Please read it carefully.

%package -n iwl5000-firmware
Summary:	Firmware for Intel® PRO/Wireless 5000 A/G/N network adaptors
License:	Redistributable, no modification permitted
Version:	8.83.5.1_1
Release:	%{iwlwifi_release}%{?dist}
Obsoletes:	iwl5000-firmware < 8.83.5.1_1-3
%description -n iwl5000-firmware
This package contains the firmware required by the iwl5000 driver
for Linux.  Usage of the firmware is subject to the terms and conditions
contained inside the provided LICENSE file. Please read it carefully.

%package -n iwl5150-firmware
Summary:	Firmware for Intel® PRO/Wireless 5150 A/G/N network adaptors
License:	Redistributable, no modification permitted
Version:	8.24.2.2
Release:	%{iwlwifi_release}%{?dist}
Obsoletes:	iwl5150-firmware < 8.24.2.2-4
%description -n iwl5150-firmware
This package contains the firmware required by the iwl5150 driver
for Linux.  Usage of the firmware is subject to the terms and conditions
contained inside the provided LICENSE file. Please read it carefully.

%package -n iwl6000-firmware
Summary:	Firmware for Intel(R) Wireless WiFi Link 6000 AGN Adapter
License:	Redistributable, no modification permitted
Version:	9.221.4.1
Release:	%{iwlwifi_release}%{?dist}
Obsoletes:	iwl6000-firmware < 9.221.4.1-4
%description -n iwl6000-firmware
This package contains the firmware required by the iwlagn driver
for Linux.  Usage of the firmware is subject to the terms and conditions
contained inside the provided LICENSE file. Please read it carefully.

%package -n iwl6000g2a-firmware
Summary:	Firmware for Intel(R) Wireless WiFi Link 6005 Series Adapters
License:	Redistributable, no modification permitted
Version:	17.168.5.3
Release:	%{iwlwifi_release}%{?dist}
Obsoletes:	iwl6000g2a-firmware < 17.168.5.3-3
%description -n iwl6000g2a-firmware
This package contains the firmware required by the iwlagn driver
for Linux.  Usage of the firmware is subject to the terms and conditions
contained inside the provided LICENSE file. Please read it carefully.

%package -n iwl6000g2b-firmware
Summary:	Firmware for Intel(R) Wireless WiFi Link 6030 Series Adapters
License:	Redistributable, no modification permitted
Version:	17.168.5.2
Release:	%{iwlwifi_release}%{?dist}
Obsoletes:	iwl6000g2b-firmware < 17.168.5.2-3
%description -n iwl6000g2b-firmware
This package contains the firmware required by the iwlagn driver
for Linux.  Usage of the firmware is subject to the terms and conditions
contained inside the provided LICENSE file. Please read it carefully.

%package -n iwl6050-firmware
Summary:	Firmware for Intel(R) Wireless WiFi Link 6050 Series Adapters
License:	Redistributable, no modification permitted
Version:	41.28.5.1
Release:	%{iwlwifi_release}%{?dist}
Obsoletes:	iwl6050-firmware < 41.28.5.1-5
%description -n iwl6050-firmware
This package contains the firmware required by the iwlagn driver
for Linux.  Usage of the firmware is subject to the terms and conditions
contained inside the provided LICENSE file. Please read it carefully.

%prep
%setup -q -n linux-firmware-%{checkout}
git init .
if [ -z "$GIT_COMMITTER_NAME" ]; then
    git config user.email "nobody@fedoraproject.org"
    git config user.name "Fedora X Ninjas"
fi
git add .
git commit -m init .

%build
# Remove firmware shipped in separate packages already
# Perhaps these should be built as subpackages of linux-firmware?
rm ql2???_fw.bin LICENCE.qla2xxx
rm -rf ess korg sb16 yamaha
# We have _some_ ralink firmware in separate packages already.
rm rt73.bin rt2561.bin rt2561s.bin rt2661.bin
# And _some_ conexant firmware.
rm v4l-cx23418-apu.fw v4l-cx23418-cpu.fw v4l-cx23418-dig.fw v4l-cx25840.fw
# Netxen firmware
rm phanfw.bin LICENCE.phanfw

# Remove source files we don't need to install
rm -f usbdux/*dux */*.asm

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/lib/firmware
cp -r * $RPM_BUILD_ROOT/usr/lib/firmware
rm $RPM_BUILD_ROOT/usr/lib/firmware/{WHENCE,LICENCE.*,LICENSE.*}
FILEDIR=`pwd`
pushd $RPM_BUILD_ROOT/usr/lib/firmware
find . \! -type d \! -name iwlwifi\* > $FILEDIR/linux-firmware.files.tmp
popd
sed -e 's/\./\/usr\/lib\/firmware\//' linux-firmware.files.tmp > linux-firmware.files
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files -n iwl100-firmware
%defattr(-,root,root,-)
%doc WHENCE LICENCE.iwlwifi_firmware
/usr/lib/firmware/iwlwifi-100-5.ucode

%files -n iwl105-firmware
%defattr(-,root,root,-)
%doc WHENCE LICENCE.iwlwifi_firmware
/usr/lib/firmware/iwlwifi-105-*.ucode

%files -n iwl135-firmware
%defattr(-,root,root,-)
%doc WHENCE LICENCE.iwlwifi_firmware
/usr/lib/firmware/iwlwifi-135-*.ucode

%files -n iwl1000-firmware
%defattr(-,root,root,-)
%doc WHENCE LICENCE.iwlwifi_firmware
/usr/lib/firmware/iwlwifi-1000-*.ucode

%files -n iwl2000-firmware
%defattr(-,root,root,-)
%doc WHENCE LICENCE.iwlwifi_firmware
/usr/lib/firmware/iwlwifi-2000-*.ucode

%files -n iwl2030-firmware
%defattr(-,root,root,-)
%doc WHENCE LICENCE.iwlwifi_firmware
/usr/lib/firmware/iwlwifi-2030-*.ucode

%files -n iwl3945-firmware
%defattr(-,root,root,-)
%doc WHENCE LICENCE.iwlwifi_firmware
/usr/lib/firmware/iwlwifi-3945-*.ucode

%files -n iwl4965-firmware
%defattr(-,root,root,-)
%doc WHENCE LICENCE.iwlwifi_firmware
/usr/lib/firmware/iwlwifi-4965-*.ucode

%files -n iwl5000-firmware
%defattr(-,root,root,-)
%doc WHENCE LICENCE.iwlwifi_firmware
/usr/lib/firmware/iwlwifi-5000-*.ucode

%files -n iwl5150-firmware
%defattr(-,root,root,-)
%doc WHENCE LICENCE.iwlwifi_firmware
/usr/lib/firmware/iwlwifi-5150-*.ucode

%files -n iwl6000-firmware
%defattr(-,root,root,-)
%doc WHENCE LICENCE.iwlwifi_firmware
/usr/lib/firmware/iwlwifi-6000-*.ucode

%files -n iwl6000g2a-firmware
%defattr(-,root,root,-)
%doc WHENCE LICENCE.iwlwifi_firmware
/usr/lib/firmware/iwlwifi-6000g2a-*.ucode

%files -n iwl6000g2b-firmware
%defattr(-,root,root,-)
%doc WHENCE LICENCE.iwlwifi_firmware
/usr/lib/firmware/iwlwifi-6000g2b-*.ucode

%files -n iwl6050-firmware
%defattr(-,root,root,-)
%doc WHENCE LICENCE.iwlwifi_firmware
/usr/lib/firmware/iwlwifi-6050-*.ucode

%files -f linux-firmware.files
%defattr(-,root,root,-)
%doc WHENCE LICENCE.* LICENSE.*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 20120720-0.2.git7560108
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Josh Boyer <jwboyer@redhat.com> 20120720-0.1.git7560108
- Update to latest upstream.  Adds more realtek firmware and bcm4334

* Tue Jul 17 2012 Josh Boyer <jwboyer@redhat.com> 20120717-0.1.gitf1f86bb
- Update to latest upstream.  Adds updated realtek firmware

* Thu Jun 07 2012 Josh Boyer <jwboyer@redhat.com> 20120510-0.5.git375e954
- Bump release to get around koji

* Thu Jun 07 2012 Josh Boyer <jwboyer@redhat.com> 20120510-0.4.git375e954
- Drop udev requires.  Systemd now provides udev

* Tue Jun 05 2012 Josh Boyer <jwboyer@redhat.com> 20120510-0.3.git375e954
- Fix location of BuildRequires so git is inclued in the buildroot
- Create iwlXXXX-firmware subpackages (rhbz 828050)

* Thu May 10 2012 Josh Boyer <jwboyer@redhat.com> 20120510-0.1.git375e954
- Update to latest upstream.  Adds new bnx2x and radeon firmware

* Wed Apr 18 2012 Josh Boyer <jwboyer@redhat.com> 20120418-0.1.git85fbcaa
- Update to latest upstream.  Adds new rtl and ath firmware

* Wed Mar 21 2012 Dave Airlie <airlied@redhat.com> 20120206-0.3.git06c8f81
- use git to apply the radeon firmware

* Wed Mar 21 2012 Dave Airlie <airlied@redhat.com> 20120206-0.2.git06c8f81
- add radeon southern islands/trinity firmware

* Tue Feb 07 2012 Josh Boyer <jwboyer@redhat.com> 20120206-0.1.git06c8f81
- Update to latest upstream git snapshot.  Fixes rhbz 786937

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110731-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 04 2011 Tom Callaway <spot@fedoraproject.org> 20110731-2
- resolve conflict with netxen-firmware

* Wed Aug 03 2011 David Woodhouse <dwmw2@infradead.org> 20110731-1
- Latest firmware release with v1.3 ath9k firmware (#727702)

* Sun Jun 05 2011 Peter Lemenkov <lemenkov@gmail.com> 20110601-2
- Remove duplicated licensing files from /lib/firmware

* Wed Jun 01 2011 Dave Airlie <airlied@redhat.com> 20110601-1
- Latest firmware release with AMD llano support.

* Thu Mar 10 2011 Dave Airlie <airlied@redhat.com> 20110304-1
- update to latest upstream for radeon ni/cayman, drop nouveau fw we don't use it anymore

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110125-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 David Woodhouse <dwmw2@infradead.org> 20110125-1
- Update to linux-firmware-20110125 (new bnx2 firmware)

* Fri Jan 07 2011 Dave Airlie <airlied@redhat.com> 20101221-1
- rebase to upstream release + add new radeon NI firmwares.

* Thu Aug 12 2010 Hicham HAOUARI <hicham.haouari@gmail.com> 20100806-4
- Really obsolete ueagle-atm4-firmware

* Thu Aug 12 2010 Hicham HAOUARI <hicham.haouari@gmail.com> 20100806-3
- Obsolete ueagle-atm4-firmware

* Fri Aug 06 2010 David Woodhouse <dwmw2@infradead.org> 20100806-2
- Remove duplicate radeon firmwares; they're upstream now

* Fri Aug 06 2010 David Woodhouse <dwmw2@infradead.org> 20100806-1
- Update to linux-firmware-20100806 (more legacy firmwares from kernel source)

* Fri Apr 09 2010 Dave Airlie <airlied@redhat.com> 20100106-4
- Add further radeon firmwares

* Wed Feb 10 2010 Dave Airlie <airlied@redhat.com> 20100106-3
- add radeon RLC firmware - submitted upstream to dwmw2 already.

* Tue Feb 09 2010 Ben Skeggs <bskeggs@redhat.com> 20090106-2
- Add firmware needed for nouveau to operate correctly (this is Fedora
  only - do not upstream yet - we just moved it here from Fedora kernel)

* Wed Jan 06 2010 David Woodhouse <David.Woodhouse@intel.com> 20090106-1
- Update

* Fri Aug 21 2009 David Woodhouse <David.Woodhouse@intel.com> 20090821-1
- Update, fix typos, remove some files which conflict with other packages.

* Thu Mar 19 2009 David Woodhouse <David.Woodhouse@intel.com> 20090319-1
- First standalone kernel-firmware package.
