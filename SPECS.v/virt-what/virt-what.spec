Name:           virt-what
Version:	1.15
Release:	1%{?dist}
Summary:        Detect if we are running in a virtual machine
Summary(zh_CN.UTF-8): 检测你是否在虚拟机中运行

Group:          Applications/Emulators
Group(zh_CN.UTF-8): 应用程序/模拟器
License:        GPLv2+
URL:            http://people.redhat.com/~rjones/virt-what/
Source0:        http://people.redhat.com/~rjones/virt-what/files/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# This is provided by the build root, but we make it explicit
# anyway in case this was dropped from the build root in future.
BuildRequires:  /usr/bin/pod2man

# Required at build time in order to do 'make check' (for getopt).
BuildRequires:  util-linux

# virt-what script uses dmidecode and getopt (from util-linux).
# RPM cannot detect this so make the dependencies explicit here.
%ifarch %{ix86} x86_64
Requires:       dmidecode
%endif
Requires:       util-linux


%description
virt-what is a shell script which can be used to detect if the program
is running in a virtual machine.

The program prints out a list of "facts" about the virtual machine,
derived from heuristics.  One fact is printed per line.

If nothing is printed and the script exits with code 0 (no error),
then it can mean either that the program is running on bare-metal or
the program is running inside a type of virtual machine which we don't
know about or cannot detect.

Current types of virtualization detected:

 - hyperv       Microsoft Hyper-V
 - kvm          Linux Kernel Virtual Machine (KVM)
 - openvz       OpenVZ or Virtuozzo
 - powervm_lx86 IBM PowerVM Lx86 Linux/x86 emulator
 - qemu         QEMU (unaccelerated)
 - uml          User-Mode Linux (UML)
 - virtage      Hitachi Virtualization Manager (HVM) Virtage LPAR
 - virtualbox   VirtualBox
 - virtualpc    Microsoft VirtualPC
 - vmware       VMware
 - xen          Xen
 - xen-dom0     Xen dom0 (privileged domain)
 - xen-domU     Xen domU (paravirtualized guest domain)
 - xen-hvm      Xen guest fully virtualized (HVM)

%description -l zh_CN.UTF-8
检测你是否是在虚拟机中运行，支持的虚拟机类型有：hyperv, kvm,
openvz, powervm_lx86, qemu, uml, virtage,virtualbox, virtualpc,
vmware, xen, xen-dom0, xen-domU, xen-hvm。

%prep
%setup -q


%build
%configure
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README COPYING
%{_sbindir}/virt-what
%{_libexecdir}/virt-what-cpuid-helper
%{_mandir}/man1/*.1*


%changelog
* Sun Oct 18 2015 Liu Di <liudidi@gmail.com> - 1.15-1
- 更新到 1.15

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1.12-1
- New upstream version 1.12.

* Wed Feb 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1.11-3
- Remove ExclusiveArch, but don't require dmidecode except on
  i?86 and x86-64 (RHBZ#791370).

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 27 2011 Richard W.M. Jones <rjones@redhat.com> - 1.11-1
- New upstream version 1.11.

* Wed May 25 2011 Richard W.M. Jones <rjones@redhat.com> - 1.10-1
- New upstream version 1.10.

* Tue Mar  9 2011 Richard W.M. Jones <rjones@redhat.com> - 1.9-1
- New upstream version 1.9.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Richard W.M. Jones <rjones@redhat.com> - 1.8-1
- New upstream version 1.8.

* Thu Jan 20 2011 Richard W.M. Jones <rjones@redhat.com> - 1.7-1
- New upstream version 1.7.

* Wed Jan 19 2011 Richard W.M. Jones <rjones@redhat.com> - 1.6-2
- New upstream version 1.6.
- BuildRequires 'getopt' from util-linux-ng.

* Tue Jan 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1.5-1
- New upstream version 1.5.
- Add 'make check' section.

* Tue Jan 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1.4-1
- New upstream version 1.4.
- More hypervisor types detected.

* Thu Oct 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-4
- Move configure into build (not prep).

* Thu Oct 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-3
- Initial import into Fedora.

* Tue Oct 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-2
- Make changes suggested by reviewer (RHBZ#644259).

* Tue Oct 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-1
- Initial release.
