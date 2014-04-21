Name: fxload
Version: 2002_04_11
Release: 12%{?dist}
Summary: A helper program to download firmware into FX and FX2 EZ-USB devices
Summary(zh_CN.UTF-8): 下载固件到 FX 和 FX2 EZ-USB 设备的帮助程序

Group: System Environment/Kernel
Group(zh_CN.UTF-8): 系统环境/内核
License: GPLv2+
URL: http://linux-hotplug.sourceforge.net/
Source0: fxload-2002_04_11-noa3load.tar.gz
# The above file is derived from:
# http://downloads.sourceforge.net/linux-hotplug/fxload-2002_04_11.tar.gz
# This file contains code that is copyright Cypress Semiconductor Inc,
# and cannot be distributed. Therefore we use this script to remove the
# copyright code before shipping it. Download the upstream tarball and
# invoke this script while in the tarball's directory:
# ./fxload-generate-tarball.sh 2002_04_11
Source1: fxload-generate-tarball.sh
Patch0: fxload-header.patch
Patch1: fxload-noa3load.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: kernel-headers
Requires: udev
Conflicts: hotplug-gtk hotplug

%description 
This program is conveniently able to download firmware into FX and FX2
EZ-USB devices, as well as the original AnchorChips EZ-USB.  It is
intended to be invoked by udev scripts when the unprogrammed device
appears on the bus.

%description -l zh_CN.UTF-8
下载固件到 FX 和 FX2 EZ-USB 设备的帮助程序。

%prep
%setup -q 
%patch0 -p0 -b .fxload-header
%patch1 -p1 -b .fxload-noa3load

%build 
make

%install
rm -rf %{buildroot}
mkdir -p -m 755 %{buildroot}/sbin
install -m 755 fxload %{buildroot}/sbin
mkdir -p -m 755 %{buildroot}/%{_mandir}/man8/
install -m 644 fxload.8 %{buildroot}/%{_mandir}/man8/
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc COPYING
%doc README.txt
%attr(0755, root, root) /sbin/fxload
%{_mandir}/*/*

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 2002_04_11-12
- 为 Magic 3.0 重建

* Fri Nov 25 2011 Liu Di <liudidi@gmail.com> - 2002_04_11-11
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2002_04_11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2002_04_11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2002_04_11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 9 2008 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2002_04_11-7
- Bump version to rebuild with gcc-4.3

* Sat Nov 16 2007 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2002_04_11-6
- Rework the spec file formatting to match templates from rpmdev
- Be explicit about file attributes, just in case

* Sat Nov 16 2007 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2002_04_11-5
- Updates after reading packaging guide-lines more thoroughly:
- Make license version more explicit
- Add generate-tarball.sh, and associated comments
- Added BuildRequires on kernel-headers
- Added COPYING as a doc
- Use dollar v.s. percent macros more consitently

* Fri Nov 15 2007 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2002_04_11-4
- Repackage the source tarball to remove a3load.hex
- Added instructions to spec file on how to do the above
- Remove reference to a3load.hex from the man page too

* Thu Nov 15 2007 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2002_04_11-3
- Update BuildRoot per Fedora wiki
- Fixed rpmlint complaint about not cleaning buildroot
- Updated source patch file to match latest kernel file layout
- Add patch to remove reference to non-shipped non-free a3load.hex firmware

* Fri Dec 8 2006 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 2002_04_11-2
- Fixed some rpmlint complaints
- Added patch to fix an include header
- Added dist tag

* Wed Apr 12 2006 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 2002_04_11-1
- First version of fxload spec based on hotplug spec

