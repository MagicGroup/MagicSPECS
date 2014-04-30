Summary:       An fdisk-like partitioning tool for GPT disks
Summary(zh_CN.UTF-8): 给 GPT 磁盘使用的类似 fdisk 的工具
Name:          gdisk
Version:	0.8.6
Release:       2%{?dist}
License:       GPLv2
URL:           http://www.rodsbooks.com/gdisk/
Group:         System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Source0:       http://downloads.sourceforge.net/gptfdisk/gptfdisk-%{version}.tar.gz
BuildRequires: popt-devel
BuildRequires: libicu-devel
BuildRequires: libuuid-devel
BuildRequires: ncurses-devel
BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%description
An fdisk-like partitioning tool for GPT disks. GPT fdisk features a
command-line interface, fairly direct manipulation of partition table
structures, recovery tools to help you deal with corrupt partition
tables, and the ability to convert MBR disks to GPT format.

%description -l zh_CN.UTF-8
给 GPT 磁盘使用的类似 fdisk 的工具。也可以转换 MBR 磁盘到 GPT 格式。

%prep
%setup -q -n gptfdisk-%{version}
chmod 0644 gdisk_test.sh

%build
%{__make} CXXFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64"

%install
%{__rm} -rf %{buildroot}
for f in gdisk sgdisk cgdisk fixparts ; do 
    %{__install} -D -p -m 0755 $f %{buildroot}%{_sbindir}/$f
    %{__install} -D -p -m 0644 $f.8 %{buildroot}%{_mandir}/man8/$f.8
done
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc COPYING README gdisk_test.sh
%{_sbindir}/gdisk
%{_sbindir}/cgdisk
%{_sbindir}/sgdisk
%{_sbindir}/fixparts
%{_mandir}/man8/gdisk.8*
%{_mandir}/man8/cgdisk.8*
%{_mandir}/man8/sgdisk.8*
%{_mandir}/man8/fixparts.8*

%changelog
* Fri Apr 18 2014 Liu Di <liudidi@gmail.com> - 0.8.6-2
- 为 Magic 3.0 重建

* Sat Apr 05 2014 Liu Di <liudidi@gmail.com> - 0.8.6-1
- 更新到 0.8.6

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.8.2-4
- 为 Magic 3.0 重建

* Fri Nov 23 2012 Liu Di <liudidi@gmail.com> - 0.8.2-3
- 为 Magic 3.0 重建

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for c++ ABI breakage

* Sun Jan 29 2012 Terje Rosten <terje.rosten@ntnu.no> - 0.8.2-1
- 0.8.2

* Thu Jan 05 2012 Terje Rosten <terje.rosten@ntnu.no> - 0.8.1-3
- Add patch to build with gcc 4.7

* Mon Oct 17 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.8.1-2
- Add cgdisk and fixparts

* Mon Oct 17 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.8.1-1
- 0.8.1
- Add ncurses-devel to buildreq

* Thu Sep 08 2011 Orion Poplawski <orion@cora.nwra.com> - 0.7.2-2
- Rebuild for libicu 4.8.1

* Sun Jul 10 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.7.2-1
- 0.7.2

* Mon Apr 12 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.7.1-1
- 0.7.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 29 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.6.14-1
- 0.6.14

* Thu Nov 11 2010 Terje Rosten <terje.rosten@ntnu.no> - 0.6.13-1
- 0.6.13

* Fri Jun 18 2010 Terje Rosten <terje.rosten@ntnu.no> - 0.6.8-1
- 0.6.8

* Thu Mar 25 2010 Terje Rosten <terje.rosten@ntnu.no> - 0.6.6-1
- 0.6.6
- Compile with -D_FILE_OFFSET_BITS=64, recommended upstream

* Sat Mar 20 2010 Terje Rosten <terje.rosten@ntnu.no> - 0.6.5-1
- 0.6.5
- Add alignment patch (bz #575297)

* Thu Mar 11 2010 Terje Rosten <terje.rosten@ntnu.no> - 0.6.3-2
- Fix source url

* Sun Feb 14 2010 Terje Rosten <terje.rosten@ntnu.no> - 0.6.3-1
- 0.6.3

* Sun Jan 31 2010 Terje Rosten <terje.rosten@ntnu.no> - 0.6.2-1
- 0.6.2

* Mon Jan 25 2010 Terje Rosten <terje.rosten@ntnu.no> - 0.6.1-1
- 0.6.1
- add popt-devel to buildreq
- random clean up

* Fri Jan 15 2010 R Smith <rodsmith@rodsbooks.com> - 0.6.0
- created spec file for 0.6.0 release
