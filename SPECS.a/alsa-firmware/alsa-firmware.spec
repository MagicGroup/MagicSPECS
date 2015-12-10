# This is a firmware package, so binaries (which are not run on the host)
# in the end package are expected.
%define _binaries_in_noarch_packages_terminate_build   0

Summary:        Firmware for several ALSA-supported sound cards
Summary(zh_CN.UTF-8): ALSA 支持的几个声卡需要的固件
Name:           alsa-firmware
Version:	1.0.29
Release:        4%{?dist}
# See later in the spec for a breakdown of licensing
License:        GPL+ and BSD and GPLv2+ and GPLv2 and LGPLv2+
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL:            http://www.alsa-project.org/
Source:		ftp://ftp.alsa-project.org/pub/firmware/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       alsa-tools-firmware >= %{version}
Requires:       udev
BuildRequires:  automake
BuildRequires:  autoconf

# noarch, since the package is firmware
BuildArch:      noarch

%description
This package contains the firmware binaries for a number of sound cards.
Some (but not all of these) require firmware loaders which are included in
the alsa-tools-firmware package.

%description -l zh_CN.UTF-8
这个包包含一些声卡的二进制固件，一些（但不是全部）需要使用 alsa-tools-firmware
包中的固件载入程序。

%prep
%setup -q


%build

# Leaving this directory in place ends up with the following crazy, broken
# symlinks in the output RPM, with no sign of the actual firmware (*.bin) files
# themselves:
#
# /lib/firmware/turtlebeach:
# msndinit.bin -> /etc/sound/msndinit.bin
# msndperm.bin -> /etc/sound/msndperm.bin
# pndsperm.bin -> /etc/sound/pndsperm.bin
# pndspini.bin -> /etc/sound/pndspini.bin
#
# Probably an upstream package bug.
#sed -i s#'multisound/Makefile \\'## configure.in
#sed -i s#multisound## Makefile.am

%__aclocal
%__automake --add-missing
%__autoconf
%configure --disable-loader
make %{?_smp_mflags}

# Rename README files from firmware subdirs that have them
for i in hdsploader mixartloader pcxhrloader usx2yloader vxloader ca0132
do
  mv ${i}/README README.${i}
done
mv aica/license.txt LICENSE.aica_firmware
mv aica/Dreamcast_sound.txt aica_dreamcast_sound.txt
mv ca0132/creative.txt LICENSE.creative_txt

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=%{buildroot}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README* LICENSE*
%doc aica_dreamcast_sound.txt

# License: KOS (BSD-alike)
/lib/firmware/aica_firmware.bin

# License: No explicit license; default package license is GPLv2+
/lib/firmware/asihpi

# License: GPL (undefined version)
/lib/firmware/digiface_firmware*

%dir /lib/firmware/ea
# The licenses for the Echo Audio firmware vary slightly so each is enumerated
# separately, to be really sure.
# LGPLv2.1+
/lib/firmware/ea/3g_asic.fw
# GPL (undefined version)
/lib/firmware/ea/darla20_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/darla24_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/echo3g_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/gina20_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_301_asic.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_301_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_361_asic.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_361_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_dj_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_djx_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_io_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_iox_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/layla20_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla20_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_1_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_2A_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_2S_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/loader_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/mia_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/mona_2_asic.fw
# GPL (undefined version)
/lib/firmware/ea/mona_301_1_asic_48.fw
# GPL (undefined version)
/lib/firmware/ea/mona_301_1_asic_96.fw
# GPL (undefined version)
/lib/firmware/ea/mona_301_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/mona_361_1_asic_48.fw
# GPL (undefined version)
/lib/firmware/ea/mona_361_1_asic_96.fw
# GPL (undefined version)
/lib/firmware/ea/mona_361_dsp.fw

%dir /lib/firmware/emu
# Licenses vary so are enumerated separately
# GPLv2
/lib/firmware/emu/audio_dock.fw
# GPLv2
/lib/firmware/emu/emu0404.fw
# GPLv2
/lib/firmware/emu/emu1010_notebook.fw
# GPLv2
/lib/firmware/emu/emu1010b.fw
# GPLv2
/lib/firmware/emu/hana.fw
# GPLv2+
/lib/firmware/emu/micro_dock.fw

# License: GPL (undefined version)
/lib/firmware/ess

# License: No explicit license; default package license is GPLv2+
/lib/firmware/korg

# License: GPL (undefined version)
/lib/firmware/mixart

# License: GPL (undefined version)
/lib/firmware/multiface_firmware*

# License: GPL (undefined version)
/lib/firmware/pcxhr

# License: GPL (undefined version)
/lib/firmware/rpm_firmware.bin

# License: GPLv2+
/lib/firmware/sb16

# License: GPL (undefined version)
/lib/firmware/vx

# License: No explicit license; default package license is GPLv2+
# See ALSA bug #3412
/lib/firmware/yamaha

# Licence: Redistribution allowed, see ca0132/creative.txt
/lib/firmware/ctefx.bin
/lib/firmware/ctspeq.bin

/lib/firmware/cs46xx/ba1
/lib/firmware/cs46xx/cwc4630
/lib/firmware/cs46xx/cwcasync
/lib/firmware/cs46xx/cwcbinhack
/lib/firmware/cs46xx/cwcdma
/lib/firmware/cs46xx/cwcsnoop
/lib/firmware/turtlebeach/msndinit.bin
/lib/firmware/turtlebeach/msndperm.bin
/lib/firmware/turtlebeach/pndsperm.bin
/lib/firmware/turtlebeach/pndspini.bin

# Even with --disable-loader, we still get usxxx firmware here; looking at the
# alsa-tools-firmware package, it seems like these devices probably use an old- 
# style hotplug loading method
# License: GPL (undefined version)
%{_datadir}/alsa/firmware


%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.0.29-4
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.0.29-3
- 为 Magic 3.0 重建

* Fri Mar 27 2015 Liu Di <liudidi@gmail.com> - 1.0.29-2
- 更新到 1.0.29

* Fri Apr 12 2013 Jaroslav Kysela <perex@perex.cz> - 1.0.27-1
- Update to 1.0.27

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb  1 2012 Jaroslav Kysela <perex@perex.cz> - 1.0.25-1
- Update to 1.0.25

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Tim Jackson <rpm@timj.co.uk> - 1.0.24.1-1
- Update to 1.0.24.1

* Mon May  3 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.23-1
- update to 1.0.23

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 10 2009 Tim Jackson <rpm@timj.co.uk> - 1.0.20-1
- Update to 1.0.20

* Sat Feb 28 2009 Tim Jackson <rpm@timj.co.uk> - 1.0.19-4
- Fix build on recent RPM versions

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Tim Jackson <rpm@timj.co.uk> - 1.0.19-2
- Fix unowned directories problem (#483321)

* Tue Jan 20 2009 Tim Jackson <rpm@timj.co.uk> - 1.0.19-1
- Update to 1.0.19

* Mon Jul 21 2008 Jaroslav Kysela <jkysela@redhat.com> - 1.0.17-1
- Updated to 1.0.17

* Mon May 12 2008 Tim Jackson <rpm@timj.co.uk> - 1.0.16-1
- Update to upstream 1.0.16
- Clarify licensing conditions

* Tue Aug 14 2007 Tim Jackson <rpm@timj.co.uk> - 1.0.14-1
- Update to upstream 1.0.14, but skip turtlebeach firmware as it doesn't seem 
  to install properly
- Remove files from old-style firmware loader locations
- Spec file cosmetics, keep rpmlint quiet

* Sat Nov 25 2006 Tim Jackson <rpm@timj.co.uk> - 1.0.12-1
- Update to 1.0.12
- Add udev dep

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Apr 03 2004 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.4-0.fdr.1
- Update to 1.0.4

* Fri Jan 16 2004 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.1-0.fdr.2
- add missing rm in install section

* Fri Jan 09 2004 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.1-0.fdr.1
- Update to 1.0.1
- Contains now the license -- is "Distributable under GPL"

* Thu Dec 04 2003 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.0.0-0.fdr.0.1.rc1
- Initial build.
