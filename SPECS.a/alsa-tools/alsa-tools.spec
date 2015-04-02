# If you want to skip building the firmware subpackage, define the macro
# _without_firmware to 1. This is not the actual firmware itself 
# (see alsa-firmware), it is some complementary tools.
# Do *NOT* set it to zero or have a commented out define here, or it will not
# work. (RPM spec file voodoo)
%if 0%{?rhel}	
%global _without_tools 1 	
%endif

%ifarch ppc ppc64
# sb16_csp doesn't build on PPC; see bug #219010
%{?!_without_tools:     %global builddirstools as10k1 echomixer envy24control hdspconf hdspmixer hwmixvolume rmedigicontrol sbiload sscape_ctl us428control hda-verb hdajackretask }
%else
%{?!_without_tools:     %global builddirstools as10k1 echomixer envy24control hdspconf hdspmixer hwmixvolume rmedigicontrol sbiload sb16_csp sscape_ctl us428control hda-verb hdajackretask }
%endif

%{?!_without_firmware:  %global builddirsfirmw hdsploader mixartloader usx2yloader vxloader }

# Note that the Version is intended to coincide with the version of ALSA
# included with the Fedora kernel, rather than necessarily the very latest
# upstream version of alsa-tools

Summary:        Specialist tools for ALSA
Summary(zh_CN.UTF-8): ALSA 的一些专门工具
Name:           alsa-tools
Version:	1.0.29
Release:        3%{?dist}

# Checked at least one source file from all the sub-projects contained in
# the source tarball and they are consistent GPLv2+ - TJ 2007-11-15
License:        GPLv2+
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL:            http://www.alsa-project.org/
Source:		ftp://ftp.alsa-project.org/pub/tools/%{name}-%{version}.tar.bz2

# The icons below were created by Tim Jackson from screenshots of the
# apps in question. They suck, a lot. Better alternatives welcome!
Source1:        envy24control.desktop
Source2:        envy24control.png
Source3:        echomixer.desktop
Source4:        echomixer.png
Source5:        90-alsa-tools-firmware.rules
# Resized version of public domain clipart found here:
# http://www.openclipart.org/detail/17428
Source6:        hwmixvolume.png
Source7:        hwmixvolume.desktop
Source9:        hdajackretask.desktop

# build fix for non-x86 arches
Patch0:         %{name}-1.0.27-non-x86.patch

BuildRequires:  alsa-lib-devel >= 1.0.24
%if 0%{!?_without_tools:1}
BuildRequires:  gtk+-devel
BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel
BuildRequires:  fltk-devel
Buildrequires:  desktop-file-utils
Requires:       xorg-x11-fonts-misc
# Needed for hwmixvolume
Requires:       python-alsa
%endif

%description
This package contains several specialist tools for use with ALSA, including
a number of programs that provide access to special hardware facilities on
certain sound cards.

* as10k1 - AS10k1 Assembler
%ifnarch ppc ppc64
* cspctl - Sound Blaster 16 ASP/CSP control program
%endif
* echomixer - Mixer for Echo Audio (indigo) devices
* envy24control - Control tool for Envy24 (ice1712) based soundcards
* hdspmixer - Mixer for the RME Hammerfall DSP cards
* hwmixvolume - Control the volume of individual streams on sound cards that
  use hardware mixing
* rmedigicontrol - Control panel for RME Hammerfall cards
* sbiload - An OPL2/3 FM instrument loader for ALSA sequencer
* sscape_ctl - ALSA SoundScape control utility
* us428control - Control tool for Tascam 428
* hda-verb - Direct HDA codec access
* hdajackretask - Reassign the I/O jacks on the HDA hardware

%description -l zh_CN.UTF-8
这个包提供了一些 ALSA 使用的专门工具，包括在某些声卡访问专用功能需要的程序。
具体可以查看包内的命令帮助。

%package firmware
Summary:        ALSA tools for uploading firmware to some soundcards
Summary(zh_CN.UTF-8): 给某些声卡上传固件用的 ALSA 工具
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Requires:       udev
Requires:       alsa-firmware
Requires:       fxload


%description firmware
This package contains tools for flashing firmware into certain sound cards.
The following tools are available:

* hdsploader   - for RME Hammerfall DSP cards
* mixartloader - for Digigram miXart soundcards
* vxloader     - for Digigram VX soundcards
* usx2yloader  - second phase firmware loader for Tascam USX2Y USB soundcards


%description firmware -l zh_CN.UTF-8
这个包包含了给一些声卡上传固件用的 ALSA 工具。具体查看包内命令帮助。

%prep
%setup -q -n %{name}-%{version}
#%patch0 -p1 -b .non-x86

%build
mv seq/sbiload . ; rm -rf seq
for i in %{?builddirstools:%builddirstools} %{?builddirsfirmw:%builddirsfirmw}
do
  cd $i ; %configure
  %{__make} %{?_smp_mflags} || exit 1
  cd ..
done


%install
mkdir -p %{buildroot}%{_datadir}/{pixmaps,applications}

for i in %{?builddirstools:%builddirstools} %{?builddirsfirmw:%builddirsfirmw}
do
  case $i in
    echomixer)
      (cd $i ; %makeinstall ; install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/pixmaps/ ; install -m 644 %{SOURCE3} %{buildroot}%{_datadir}/applications/ ) || exit 1
      ;;
    envy24control)
      (cd $i ; %makeinstall ; install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/ ; install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/applications/ ) || exit 1
      ;;
    hdspconf)
      (cd $i ; %makeinstall pixmapdir=%{buildroot}%{_datadir}/pixmaps desktopdir=%{buildroot}%{_datadir}/applications ) || exit 1
      ;;
    hdspmixer)
      (cd $i ; %makeinstall pixmapdir=%{buildroot}%{_datadir}/pixmaps desktopdir=%{buildroot}%{_datadir}/applications ) || exit 1
      ;;
    hwmixvolume)
      (cd $i ; %makeinstall ; install -m 644 %{SOURCE6} %{buildroot}%{_datadir}/pixmaps/ ; install -m 644 %{SOURCE7} %{buildroot}%{_datadir}/applications/ ) || exit 1
      ;;
    usx2yloader)
      (cd $i ; %makeinstall hotplugdir=%{buildroot}%{_sysconfdir}/hotplug/usb) || exit 1
      ;;
    hdajackretask)
      (cd $i ; %makeinstall ; install -m 644 %{SOURCE9} %{buildroot}%{_datadir}/applications/ ) || exit 1
      ;;
    *) (cd $i ; %makeinstall) || exit 1
   esac
   if [[ -s "${i}"/README ]]
   then
      if [[ ! -d "%{buildroot}%{_docdir}/%{name}-%{version}/${i}" ]]
      then
         mkdir -p "%{buildroot}%{_docdir}/%{name}-%{version}/${i}"
      fi
      cp "${i}"/README "%{buildroot}%{_docdir}/%{name}-%{version}/${i}"
   fi
   if [[ -s "${i}"/COPYING ]]
   then
      if [[ ! -d "%{buildroot}%{_docdir}/%{name}-%{version}/${i}" ]]
      then
         mkdir -p "%{buildroot}%{_docdir}/%{name}-%{version}/${i}"
      fi
      cp "${i}"/COPYING "%{buildroot}%{_docdir}/%{name}-%{version}/${i}"
   fi
   if [[ -s %{buildroot}%{_datadir}/applications/${i}.desktop ]] ; then
      desktop-file-install --dir %{buildroot}%{_datadir}/applications \
        %{buildroot}%{_datadir}/applications/${i}.desktop
   fi
done

# convert hotplug stuff to udev
rm -f %{buildroot}%{_sysconfdir}/hotplug/usb/tascam_fw.usermap
mkdir -p %{buildroot}/lib/udev
mv %{buildroot}%{_sysconfdir}/hotplug/usb/* %{buildroot}/lib/udev
mkdir -p %{buildroot}/lib/udev/rules.d
install -m 644 %{SOURCE5} %{buildroot}/lib/udev/rules.d

%if 0%{!?_without_tools:1}
%files
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/as10k1
%doc %{_docdir}/%{name}-%{version}/echomixer
%doc %{_docdir}/%{name}-%{version}/envy24control
%doc %{_docdir}/%{name}-%{version}/hdspconf
%doc %{_docdir}/%{name}-%{version}/hdspmixer
%doc %{_docdir}/%{name}-%{version}/hwmixvolume
%doc %{_docdir}/%{name}-%{version}/rmedigicontrol
%doc %{_docdir}/%{name}-%{version}/sbiload
%doc %{_docdir}/%{name}-%{version}/hda-verb
%doc %{_docdir}/%{name}-%{version}/hdajackretask
%{_bindir}/as10k1
%{_bindir}/echomixer
%{_bindir}/envy24control
%{_bindir}/hdspconf
%{_bindir}/hdspmixer
%{_bindir}/hwmixvolume
%{_bindir}/rmedigicontrol
%{_bindir}/sbiload
%{_bindir}/sscape_ctl
%{_bindir}/us428control
%{_bindir}/hda-verb
%{_bindir}/hdajackretask
%{_datadir}/applications/echomixer.desktop
%{_datadir}/applications/envy24control.desktop
%{_datadir}/applications/hdspconf.desktop
%{_datadir}/applications/hdspmixer.desktop
%{_datadir}/applications/hwmixvolume.desktop
%{_datadir}/applications/hdajackretask.desktop
%{_datadir}/man/man1/envy24control.1.gz
%{_datadir}/pixmaps/echomixer.png
%{_datadir}/pixmaps/envy24control.png
%{_datadir}/pixmaps/hdspconf.png
%{_datadir}/pixmaps/hdspmixer.png
%{_datadir}/pixmaps/hwmixvolume.png
%{_datadir}/sounds/*

# sb16_csp stuff which is excluded for PPCx
%ifnarch ppc ppc64
%doc %{_docdir}/%{name}-%{version}/sb16_csp
%{_bindir}/cspctl
%{_datadir}/man/man1/cspctl.1.gz
%endif

%endif

%if 0%{!?_without_firmware:1}
%files firmware
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/hdsploader
%doc %{_docdir}/%{name}-%{version}/mixartloader
%doc %{_docdir}/%{name}-%{version}/usx2yloader
%doc %{_docdir}/%{name}-%{version}/vxloader
/lib/udev/rules.d/*.rules
/lib/udev/tascam_fpga
/lib/udev/tascam_fw
%{_bindir}/hdsploader
%{_bindir}/mixartloader
%{_bindir}/usx2yloader
%{_bindir}/vxloader
%endif

%changelog
* Fri Mar 27 2015 Liu Di <liudidi@gmail.com> - 1.0.29-3
- 更新到 1.0.29

* Tue May 21 2013 Dan Horák <dan[at]danny.cz> - 1.0.27-2
- fix build on non-x86 arches

* Fri Apr 12 2013 Jaroslav Kysela <jkysela@redhat.com> - 1.0.27-1
- Updated to 1.0.27

* Sat Feb 09 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.0.26.1-3
- remove vendor tag from desktop file. https://fedorahosted.org/fpc/ticket/247
- clean up spec to follow current guidelines
- don't build -tools for RHEL. Bill Nottingham patch. Resolves rhbz#586030

* Fri Sep  7 2012 Jaroslav Kysela <jkysela@redhat.com> - 1.0.26.1-2
- Fixed gtk3-devel dependency (hdajackretask)
- Added description for hda-verb and hdajackretask

* Thu Sep  6 2012 Jaroslav Kysela <jkysela@redhat.com> - 1.0.26.1-1
- Updated to 1.0.26.1
- Added hda-verb and hdajackretask tools

* Thu Sep  6 2012 Jaroslav Kysela <jkysela@redhat.com> - 1.0.26-1
- Updated to 1.0.26

* Wed Aug 29 2012 Tim Jackson <rpm@timj.co.uk> - 1.0.25-4
- Move udev rules to /lib/udev/rules.d (rhbz #748206)
- remove %%BuildRoot and %%clean sections; no longer required

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.25-2
- Bump build for ARM

* Tue Jan 31 2012 Jaroslav Kysela <perex@perex.cz> - 1.0.25-1
- Update to 1.0.25

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.0.24.1-4
- Rebuild for new libpng

* Fri Jun 10 2011 Adam Jackson <ajax@redhat.com> 1.0.24.1-3
- Rebuild for new libfltk

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Tim Jackson <rpm@timj.co.uk> - 1.0.24.1-1
- Update to 1.0.24.1

* Mon May 03 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.23-1
- update to 1.0.23

* Sat Mar 06 2010 Tim Jackson <rpm@timj.co.uk> - 1.0.22-2
- Don't own /usr/share/sounds (#569415)

* Sun Jan 10 2010 Tim Jackson <rpm@timj.co.uk> - 1.0.22-1
- Update to 1.0.22
- use %%global instead of %%define

* Thu Sep 03 2009 Tim Jackson <rpm@timj.co.uk> - 1.0.21-1
- Update to 1.0.21

* Wed Aug 26 2009 Tim Jackson <rpm@timj.co.uk> - 1.0.20-4
- Add missing dep on xorg-x11-fonts-misc (#503284)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Tim Jackson <rpm@timj.co.uk> - 1.0.20-2

* Sun May 10 2009 Tim Jackson <rpm@timj.co.uk> - 1.0.20-1.fc12.2
- Update to 1.0.20

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Tim Jackson <rpm@timj.co.uk> - 1.0.19-2
- Fix unowned directory problem (#483323)

* Sat Jan 24 2009 Tim Jackson <rpm@timj.co.uk> - 1.0.19-1
- Update to version 1.0.19
- Mark udev rules as config

* Fri Dec  5 2008 Jon McCann <jmccann@redhat.com> - 1.0.17-2
- Convert hotplug stuff to udev

* Thu Jul 17 2008 Tim Jackson <rpm@timj.co.uk> - 1.0.17-1
- Update to version 1.0.17

* Mon May 19 2008 Tim Jackson <rpm@timj.co.uk> - 1.0.16-4
- Make it build cleanly on ppc and ppc64 by excluding sb16_csp

* Sun May 18 2008 Tim Jackson <rpm@timj.co.uk> - 1.0.16-3
- Really enable firmware subpackage

* Sun May 18 2008 Tim Jackson <rpm@timj.co.uk> - 1.0.16-2
- Enable firmware subpackage - the accompanying alsa-firmware package is
  finally in Fedora

* Sat Mar 01 2008 Tim Jackson <rpm@timj.co.uk> - 1.0.16-1
- Update to upstream 1.0.16 (fixes #434473)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.15-3
- Autorebuild for GCC 4.3

* Sat Jan 05 2008 Tim Jackson <rpm@timj.co.uk> - 1.0.15-2
- Update License tag to GPLv2+
- ExcludeArch ppc64 (bug #219010)

* Sat Jan 05 2008 Tim Jackson <rpm@timj.co.uk> - 1.0.15-1
- Update to upstream 1.0.15
- Add icon for envy24control
- Build echomixer

* Sat Dec 09 2006 Tim Jackson <rpm@timj.co.uk> - 1.0.12-4
- ExcludeArch ppc (#219010)

* Sun Nov 26 2006 Tim Jackson <rpm@timj.co.uk> - 1.0.12-3
- Add gtk2-devel BR

* Sun Nov 26 2006 Tim Jackson <rpm@timj.co.uk> - 1.0.12-2
- Own our docdir explicitly

* Sat Nov 25 2006 Tim Jackson <rpm@timj.co.uk> - 1.0.12-1
- Update to 1.0.12
- Resubmit to Fedora Extras 6
- Replace hotplug requirement with udev

* Mon Feb 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info>
- Rebuild for Fedora Extras 5

* Tue Dec 06 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.10-1
- Update to 1.0.10

* Fri May 06 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.9-1
- Update to 1.0.9
- Use disttag
- Remove gcc4 patch

* Fri May 06 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.8-3
- prune ac3dec from sources

* Thu May 05 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.8-2
- don't build ac3dec -- use a52dec instead

* Wed Apr 06 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.8-1
- Update to 1.0.8

* Sun Mar 29 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 0:1.0.6-2
- Add "--without tools" and "--with firmware" options
- Drop unneeded BR: automake

* Sun Jan 02 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 0:1.0.6-0.fdr.1
- Update to 1.0.6 for FC3
- add new files in {_datadir}/sounds/
- add patch0 for as10k1 

* Sat Apr 03 2004 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 0:1.0.4-0.fdr.1
- Update to 1.0.4

* Fri Jan 16 2004 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 0:1.0.1-0.fdr.2
- Integrate Michaels patch that fixes:
- fix desktop files for fedora.us, adds buildreq desktop-file-utils
- fix %%install section for short-circuit installs

* Fri Jan 09 2004 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 0:1.0.1-0.fdr.1
- Update to 1.0.1

* Sun Dec 14 2003 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.0.0-0.fdr.0.3.rc2
- exit if error during build or install
- fix install errors hdspconf, hdspmixer, usx2yloader
- Split package in alsa-tools and alsa-tools-firmware
- Integrate more docs

* Fri Dec 06 2003 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.0.0-0.fdr.0.2.rc2
- Update to 1.0.0rc2
- some minor corrections in style

* Thu Dec 04 2003 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.0.0-0.fdr.0.1.rc1
- Update to 1.0.0rc1
- Remove firmware files -- extra package now.
- Add description

* Wed Aug 13 2003 Dams <anvil[AT]livna.org> 0:tools-0.fdr.1
- Initial build.
