%global svnrel 1063
%global tarver 1.0

%define svn 1
%define vcsdate 20151101

# Disable unhelpful RPM test.
%global _binaries_in_noarch_packages_terminate_build 0

%define with_sparc 0

Name:           openbios
%if 0%{?svn}
Version:	1.0.svn%{vcsdate}
Release:	5%{?dist}
%else
Version:        %{tarver}.svn%{svnrel}
Release:        5%{?dist}
%endif
Summary:        OpenBIOS implementation of IEEE 1275-1994
Summary(zh_CN.UTF-8): IEEE 1275-1994 的 OpenBIOS 实现

License:        GPLv2
URL:            http://www.openfirmware.info/OpenBIOS
BuildArch:      noarch

# There are no upstream tarballs.  This tarball is prepared as follows:
#
# svn export -r %{svnrel} \
#     svn://username@openbios.org/openbios/trunk/openbios-devel \
#     %{name}-%{tarver}
# tar czf %{name}-%{tarver}-svn%{svnrel}.tar.gz %{name}-%{tarver}
# rm -r %{name}-%{tarver}
%if 0%{?svn}
Source0:	%{name}-svn%{vcsdate}.tar.xz
%else
Source0:        %{name}-%{tarver}-svn%{svnrel}.tar.gz
%endif
Source1:	make_openbios_svn_package.sh

# Use 64bit gcc for 32bit ppc + sparc
# keep: Not suitable for upstream, change is specific to Fedora cross-gcc
Patch0:         0001-Use-64bit-gcc-for-32bit-ppc-sparc.patch

# Note that these packages build 32 bit binaries with the -m32 flag.
BuildRequires:  gcc-powerpc64-linux-gnu
%if 0%{?with_sparc}
BuildRequires:  gcc-sparc64-linux-gnu
%endif

BuildRequires:  libxslt

Obsoletes:      openbios-common
Obsoletes:      openbios-ppc
Obsoletes:      openbios-sparc32
Obsoletes:      openbios-sparc64


%description
The OpenBIOS project provides you with most free and open source Open
Firmware implementations available. Here you find several
implementations of IEEE 1275-1994 (Referred to as Open Firmware)
compliant firmware. Among its features, Open Firmware provides an
instruction set independent device interface. This can be used to boot
the operating system from expansion cards without native
initialization code.

It is Open Firmware's goal to work on all common platforms, like x86,
AMD64, PowerPC, ARM and Mips. With its flexible and modular design,
Open Firmware targets servers, workstations and embedded systems,
where a sane and unified firmware is a crucial design goal and reduces
porting efforts noticably.

Open Firmware is found on many servers and workstations and there are
sever commercial implementations from SUN, Firmworks, CodeGen, Apple,
IBM and others.

In most cases, the Open Firmware implementations provided on this site
rely on an additional low-level firmware for hardware initialization,
such as coreboot or U-Boot.

%description -l zh_CN.UTF-8
OpenBIOS 项目提供了自由开源的开放固件实现。

%prep
%if 0%{?svn}
%setup -q -n %{name}-svn%{vcsdate}
%else
%setup -q -n %{name}-%{tarver}
%endif
%patch0 -p1


%build
/bin/sh config/scripts/switch-arch ppc
%if 0%{with_sparc}
/bin/sh config/scripts/switch-arch sparc32
/bin/sh config/scripts/switch-arch sparc64
%endif
make build-verbose V=1 %{?_smp_mflags}


%install
qemudir=$RPM_BUILD_ROOT%{_datadir}/qemu
mkdir -p $qemudir
cp -a obj-ppc/openbios-qemu.elf $qemudir/openbios-ppc
%if 0%{with_sparc}
cp -a obj-sparc32/openbios-builtin.elf $qemudir/openbios-sparc32
cp -a obj-sparc64/openbios-builtin.elf $qemudir/openbios-sparc64
%endif

%files
%doc COPYING
%doc README
%doc VERSION
%dir %{_datadir}/qemu
%{_datadir}/qemu/openbios-ppc
%if 0%{with_sparc}
%{_datadir}/qemu/openbios-sparc32
%{_datadir}/qemu/openbios-sparc64
%endif

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.0.svn20151101-5
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.0.svn20151101-4
- 更新到 20151101 日期的仓库源码

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.0.svn20150327-3
- 为 Magic 3.0 重建

* Fri Mar 27 2015 Liu Di <liudidi@gmail.com> - 1.0.svn20150327-2
- 更新到 20150327 日期的仓库源码

* Fri Mar 27 2015 Liu Di <liudidi@gmail.com> - 1.0.svn20150326-2
- 为 Magic 3.0 重建

* Tue Oct 16 2012 Paolo Bonzini <pbonzini@redhat.com> - 1.0.svn1063-1
- Move date from release to version.

* Mon Sep 17 2012 Cole Robinson <crobinso@redhat.com> - 1.0-6.svn1063
- Update to r1063, version qemu 1.2 shipped with

* Tue Jul 31 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0-5.svn1061
- Initial release in Fedora.
