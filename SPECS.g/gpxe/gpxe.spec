%define formats rom
# ne is only for backwards compat with older versions of qemu
%define qemuroms rtl8029 ne 8086100e pcnet32 rtl8139 virtio-net
%define buildarches %{ix86} x86_64

# debugging firmwares does not goes the same way as a normal program.
# moreover, all architectures providing debuginfo for a single noarch
# package is currently clashing in koji, so don't bother.
%global debug_package %{nil}

Name:    gpxe
Version: 1.0.1
Release: 8%{?dist}
Summary: A network boot loader

Group:   System Environment/Base
License: GPLv2 and BSD
URL:     http://etherboot.org/

Source0: http://git.etherboot.org/releases/%{name}/%{name}-%{version}.tar.bz2
Source1: USAGE
Patch1: %{name}-1.0.1-virtionet-length.patch
Patch2: %{name}-%{version}-banner-timeout.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%ifarch %{buildarches}
BuildRequires: perl syslinux mtools mkisofs

%package bootimgs
Summary: Network boot loader images in bootable USB, CD, floppy and GRUB formats
Group:   Development/Tools
BuildArch: noarch

%package roms
Summary: Network boot loader roms in .rom format
Group:  Development/Tools
Requires: %{name}-roms-qemu = %{version}-%{release}
BuildArch: noarch

%package roms-qemu
Summary: Network boot loader roms supported by QEMU, .rom format
Group:  Development/Tools
BuildArch: noarch


%description bootimgs
gPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

This package contains the gPXE boot images in USB, CD, floppy, and PXE
UNDI formats.

%description roms
gPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

This package contains the gPXE roms in .rom format.


%description roms-qemu
gPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

This package contains the gPXE ROMs for devices emulated by QEMU, in
.rom format.
%endif

%description
gPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
cp -a %{SOURCE1} .

%build
%ifarch %{buildarches}
# Fedora 10 and newer, location is in /usr/share.  Older is in /usr/lib.
ISOLINUX_BIN=/usr/share/syslinux/isolinux.bin
[ -e /usr/lib/syslinux/isolinux.bin ] && ISOLINUX_BIN=/usr/lib/syslinux/isolinux.bin
cd src
# NO_WERROR is needed because of bogus (for us) error: variable '__table_entries' set but not used [-Werror=unused-but-set-variable]
make %{?_smp_mflags} ISOLINUX_BIN=${ISOLINUX_BIN} NO_WERROR=1
make %{?_smp_mflags} bin/gpxe.lkrn
make %{?_smp_mflags} allroms
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ifarch %{buildarches}
mkdir -p %{buildroot}/%{_datadir}/%{name}/
pushd src/bin/

cp -a undionly.kpxe gpxe.{iso,usb,dsk,lkrn} %{buildroot}/%{_datadir}/%{name}/

for fmt in %{formats};do
 for img in *.${fmt};do
      if [ -e $img ]; then
   cp -a $img %{buildroot}/%{_datadir}/%{name}/
   echo %{_datadir}/%{name}/$img >> ../../${fmt}.list
  fi   
 done
done
popd

# the roms supported by qemu will be packaged separatedly
# remove from the main rom list and add them to qemu.list
for fmt in rom ;do 
 for rom in %{qemuroms} ; do
  sed -i -e "/\/${rom}.${fmt}/d" ${fmt}.list
  echo %{_datadir}/%{name}/${rom}.${fmt} >> qemu.${fmt}.list
 done
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%ifarch %{buildarches}
%files bootimgs
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/gpxe.iso
%{_datadir}/%{name}/gpxe.usb
%{_datadir}/%{name}/gpxe.dsk
%{_datadir}/%{name}/gpxe.lkrn
%{_datadir}/%{name}/undionly.kpxe
%doc COPYING COPYRIGHTS USAGE

%files roms -f rom.list
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}
%doc COPYING COPYRIGHTS

%files roms-qemu -f qemu.rom.list
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}
%doc COPYING COPYRIGHTS
%endif

%changelog
* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 1.0.1-8
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 19 2012 Daniel P. Berrange <berrange@redhat.com> - 1.0.1-6
- Remove 2 second sleep on startup (rhbz #804611)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 21 2011 Matt Domsch <mdomsch@fedoraproject.org> - 1.0.1-4
- don't use -Werror, it flags a failure that is not a failure for gPXE

* Mon Feb 21 2011 Matt Domsch <mdomsch@fedoraproject.org> - 1.0.1-3
- Fix virtio-net ethernet frame length (patch by cra), fixes BZ678789

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug  5 2010 Matt Domsch <mdomsch@fedoraproject.org> - 1.0.1-1
- New drivers: Intel e1000, e1000e, igb, EFI snpnet, JMicron jme,
  Neterion X3100, vxge, pcnet32.
- Bug fixes and improvements to drivers, wireless, DHCP, iSCSI,
  COMBOOT, and EFI.
* Tue Feb  2 2010 Matt Domsch <mdomsch@fedoraproject.org> - 1.0.0-1
- bugfix release, also adds wireless card support
- bnx2 builds again
- drop our one patch

* Tue Oct 27 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.9.9-1
- new upstream version 0.9.9
-- plus patches from git up to 20090818 which fix build errors and
   other release-critical bugs.
-- 0.9.9: added Attansic L1E and sis190/191 ethernet drivers.  Fixes
   and updates to e1000 and 3c90x drivers.
-- 0.9.8: new commands: time, sleep, md5sum, sha1sum. 802.11 wireless
   support with Realtek 8180/8185 and non-802.11n Atheros drivers.
   New Marvell Yukon-II gigabet Ethernet driver.  HTTP redirection
   support.  SYSLINUX floppy image type (.sdsk) with usable file
   system.  Rewrites, fixes, and updates to 3c90x, forcedeth, pcnet32,
   e1000, and hermon drivers.

* Mon Oct  5 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.9.7-6
- move rtl8029 from -roms to -roms-qemu for qemu ne2k_pci NIC (BZ 526776)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 19 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.9.7-4
- add undionly.kpxe to -bootimgs

* Tue May 12 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.9.7-3
- handle isolinux changing paths

* Sat May  9 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.9.7-2
- add dist tag

* Thu Mar 26 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.9.7-1
- Initial release based on etherboot spec
