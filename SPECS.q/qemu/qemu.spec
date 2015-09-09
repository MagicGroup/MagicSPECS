%ifarch %{ix86}
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch x86_64
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch ppc64 ppc64le
%global kvm_package   system-ppc
%endif
%ifarch s390x
%global kvm_package   system-s390x
%endif
%ifarch armv7hl
%global kvm_package   system-arm
%endif
%ifarch aarch64
%global kvm_package   system-aarch64
%endif

%global have_kvm 0
%if 0%{?kvm_package:1}
%global have_kvm 1
%endif

%ifarch %{ix86} x86_64
%global have_seccomp 1
%global have_spice   1
%endif

# Xen is available only on i386 x86_64 (from libvirt spec)
%ifarch %{ix86} x86_64
%global have_xen 1
%endif


Summary: QEMU is a FAST! processor emulator
Name: qemu
Version: 2.4.0
Release: 2%{?dist}
Epoch: 2
License: GPLv2+ and LGPLv2+ and BSD
Group: Development/Tools
URL: http://www.qemu.org/

Source0: http://wiki.qemu-project.org/download/%{name}-%{version}.tar.bz2

Source1: qemu.binfmt

# Creates /dev/kvm
Source3: 80-kvm.rules

# KSM control scripts
Source4: ksm.service
Source5: ksm.sysconfig
Source6: ksmctl.c
Source7: ksmtuned.service
Source8: ksmtuned
Source9: ksmtuned.conf

Source10: qemu-guest-agent.service
Source11: 99-qemu-guest-agent.rules
Source12: bridge.conf

# qemu-kvm back compat wrapper
Source13: qemu-kvm.sh

# CVE-2015-5255: heap memory corruption in vnc_refresh_server_surface
# (bz #1255899)
Patch0001: 0001-vnc-fix-memory-corruption-CVE-2015-5225.patch


BuildRequires: SDL2-devel
BuildRequires: zlib-devel
BuildRequires: which
BuildRequires: chrpath
BuildRequires: texi2html
BuildRequires: gnutls-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libtool
BuildRequires: libaio-devel
BuildRequires: rsync
BuildRequires: pciutils-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libiscsi-devel
BuildRequires: ncurses-devel
BuildRequires: libattr-devel
BuildRequires: usbredir-devel >= 0.5.2
%ifnarch s390 s390x
BuildRequires: gperftools-devel
%endif
BuildRequires: texinfo
# For /usr/bin/pod2man
BuildRequires: perl-podlators
%if 0%{?have_spice:1}
BuildRequires: spice-protocol >= 0.12.2
BuildRequires: spice-server-devel >= 0.12.0
%endif
%if 0%{?have_seccomp:1}
BuildRequires: libseccomp-devel >= 2.1.0
%endif
# For network block driver
BuildRequires: libcurl-devel
# For rbd block driver
BuildRequires: ceph-devel >= 0.61
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
BuildRequires: systemtap-sdt-devel
# For smartcard NSS support
BuildRequires: nss-devel
# For XFS discard support in raw-posix.c
BuildRequires: xfsprogs-devel
# For VNC JPEG support
BuildRequires: libjpeg-devel
# For VNC PNG support
BuildRequires: libpng-devel
# For uuid generation
BuildRequires: libuuid-devel
# For BlueZ device support
BuildRequires: bluez-libs-devel
# For Braille device support
BuildRequires: brlapi-devel
# For FDT device tree support
BuildRequires: libfdt-devel
# For virtfs
BuildRequires: libcap-devel
# Hard requirement for version >= 1.3
BuildRequires: pixman-devel
# For gluster support
BuildRequires: glusterfs-devel >= 3.4.0
BuildRequires: glusterfs-api-devel >= 3.4.0
# Needed for usb passthrough for qemu >= 1.5
BuildRequires: libusbx-devel
# SSH block driver
BuildRequires: libssh2-devel
# GTK frontend
BuildRequires: gtk3-devel
BuildRequires: vte3-devel
# GTK translations
BuildRequires: gettext
# RDMA migration
%ifnarch s390 s390x
BuildRequires: librdmacm-devel
%endif
# For sanity test
BuildRequires: qemu-sanity-check-nodeps
BuildRequires: kernel
# For acpi compilation
BuildRequires: iasl
# Xen support
%if 0%{?have_xen:1}
BuildRequires: xen-devel
%endif
# memdev hostmem backend added in 2.1
%ifarch %{ix86} x86_64 aarch64
BuildRequires: numactl-devel
%endif
# Added in qemu 2.3
BuildRequires: bzip2-devel
# Added in qemu 2.4 for opengl bits
Requires: libepoxy-devel


Requires: %{name}-user = %{epoch}:%{version}-%{release}
Requires: %{name}-system-alpha = %{epoch}:%{version}-%{release}
Requires: %{name}-system-arm = %{epoch}:%{version}-%{release}
Requires: %{name}-system-cris = %{epoch}:%{version}-%{release}
Requires: %{name}-system-lm32 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-m68k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-microblaze = %{epoch}:%{version}-%{release}
Requires: %{name}-system-mips = %{epoch}:%{version}-%{release}
Requires: %{name}-system-or32 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-ppc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-s390x = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sh4 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sparc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-unicore32 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-x86 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-xtensa = %{epoch}:%{version}-%{release}
Requires: %{name}-system-moxie = %{epoch}:%{version}-%{release}
Requires: %{name}-system-aarch64 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-tricore = %{epoch}:%{version}-%{release}
Requires: %{name}-img = %{epoch}:%{version}-%{release}


%description
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation. QEMU has two operating modes:

 * Full system emulation. In this mode, QEMU emulates a full system (for
   example a PC), including a processor and various peripherials. It can be
   used to launch different Operating Systems without rebooting the PC or
   to debug system code.
 * User mode emulation. In this mode, QEMU can launch Linux processes compiled
   for one CPU on another CPU.

As QEMU requires no host kernel patches to run, it is safe and easy to use.


%if %{have_kvm}
%package kvm
Summary: QEMU metapackage for KVM support
Group: Development/Tools
Requires: qemu-%{kvm_package} = %{epoch}:%{version}-%{release}

%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86
%endif


%package  img
Summary: QEMU command line tool for manipulating disk images
Group: Development/Tools

%description img
This package provides a command line tool for manipulating disk images


%package  common
Summary: QEMU common files needed by all QEMU targets
Group: Development/Tools
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description common
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the common files needed by all QEMU targets


%package guest-agent
Summary: QEMU guest agent
Group: System Environment/Daemons
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description guest-agent
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.

%post guest-agent
%systemd_post qemu-guest-agent.service

%preun guest-agent
%systemd_preun qemu-guest-agent.service

%postun guest-agent
%systemd_postun_with_restart qemu-guest-agent.service


%package -n ksm
Summary: Kernel Samepage Merging services
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
%description -n ksm
Kernel Samepage Merging (KSM) is a memory-saving de-duplication feature,
that merges anonymous (private) pages (not pagecache ones).

This package provides service files for disabling and tuning KSM.


%package user
Summary: QEMU user mode emulation of qemu targets
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
%description user
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets


%package system-x86
Summary: QEMU system emulator for x86
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Provides: kvm = 85
Obsoletes: kvm < 85
Requires: seavgabios-bin
# virtio-blk booting is broken for Windows guests
# if you mix seabios 1.7.4 and qemu 2.1.x
Requires: seabios-bin >= 1.7.5
Requires: sgabios-bin
Requires: ipxe-roms-qemu
%if 0%{?have_seccomp:1}
Requires: libseccomp >= 1.0.0
%endif


%description system-x86
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.


%package system-alpha
Summary: QEMU system emulator for Alpha
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-alpha
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Alpha systems.


%package system-arm
Summary: QEMU system emulator for ARM
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-arm
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ARM boards.


%package system-mips
Summary: QEMU system emulator for MIPS
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-mips
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for MIPS boards.


%package system-cris
Summary: QEMU system emulator for CRIS
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-cris
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for CRIS boards.


%package system-lm32
Summary: QEMU system emulator for LatticeMico32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-lm32
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for LatticeMico32 boards.


%package system-m68k
Summary: QEMU system emulator for ColdFire (m68k)
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-m68k
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ColdFire boards.


%package system-microblaze
Summary: QEMU system emulator for Microblaze
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-microblaze
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Microblaze boards.


%package system-or32
Summary: QEMU system emulator for OpenRisc32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-or32
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for OpenRisc32 boards.


%package system-s390x
Summary: QEMU system emulator for S390
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-s390x
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for S390 systems.


%package system-sh4
Summary: QEMU system emulator for SH4
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-sh4
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SH4 boards.


%package system-sparc
Summary: QEMU system emulator for SPARC
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
%description system-sparc
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SPARC and SPARC64 systems.


%package system-ppc
Summary: QEMU system emulator for PPC
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
Requires: SLOF
%description system-ppc
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for PPC and PPC64 systems.


%package system-xtensa
Summary: QEMU system emulator for Xtensa
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-xtensa
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Xtensa boards.


%package system-unicore32
Summary: QEMU system emulator for Unicore32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-unicore32
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Unicore32 boards.


%package system-moxie
Summary: QEMU system emulator for Moxie
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-moxie
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Moxie boards.


%package system-aarch64
Summary: QEMU system emulator for AArch64
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-aarch64
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for AArch64.


%package system-tricore
Summary: QEMU system emulator for tricore
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-tricore
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Tricore.


%if %{have_kvm}
%package kvm-tools
Summary: KVM debugging and diagnostics tools
Group: Development/Tools

%description kvm-tools
This package contains some diagnostics and debugging tools for KVM,
such as kvm_stat.
%endif


%package -n libcacard
Summary:        Common Access Card (CAC) Emulation
Group:          Development/Libraries

%description -n libcacard
Common Access Card (CAC) emulation library.


%package -n libcacard-tools
Summary:        CAC Emulation tools
Group:          Development/Libraries
Requires:       libcacard = %{epoch}:%{version}-%{release}

%description -n libcacard-tools
CAC emulation tools.


%package -n libcacard-devel
Summary:        CAC Emulation devel
Group:          Development/Libraries
Requires:       libcacard = %{epoch}:%{version}-%{release}

%description -n libcacard-devel
CAC emulation development files.


%prep
%setup -q -n qemu-%{version}
%autopatch -p1


%build

# QEMU already knows how to set _FORTIFY_SOURCE
%global optflags %(echo %{optflags} | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')

# drop -g flag to prevent memory exhaustion by linker
%ifarch s390
%global optflags %(echo %{optflags} | sed 's/-g//')
sed -i.debug 's/"-g $CFLAGS"/"$CFLAGS"/g' configure
%endif

# OOM killer breaks builds with parallel make on s390(x)
%ifarch s390 s390x
%define _smp_mflags %{nil}
%endif


# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

# As of qemu 2.1, --enable-trace-backends supports multiple backends,
# but there's a performance impact for non-dtrace so we don't use them
tracebackends="dtrace"

    buildarch="i386-softmmu x86_64-softmmu alpha-softmmu arm-softmmu \
cris-softmmu lm32-softmmu m68k-softmmu microblaze-softmmu \
microblazeel-softmmu mips-softmmu mipsel-softmmu mips64-softmmu \
mips64el-softmmu or32-softmmu ppc-softmmu ppcemb-softmmu ppc64-softmmu \
s390x-softmmu sh4-softmmu sh4eb-softmmu sparc-softmmu sparc64-softmmu \
xtensa-softmmu xtensaeb-softmmu unicore32-softmmu moxie-softmmu \
tricore-softmmu \
i386-linux-user x86_64-linux-user aarch64-linux-user alpha-linux-user \
arm-linux-user armeb-linux-user cris-linux-user m68k-linux-user \
microblaze-linux-user microblazeel-linux-user mips-linux-user \
mipsel-linux-user mips64-linux-user mips64el-linux-user \
mipsn32-linux-user mipsn32el-linux-user \
or32-linux-user ppc-linux-user ppc64-linux-user ppc64le-linux-user \
ppc64abi32-linux-user s390x-linux-user sh4-linux-user sh4eb-linux-user \
sparc-linux-user sparc64-linux-user sparc32plus-linux-user \
unicore32-linux-user aarch64-softmmu"

# gperftools providing tcmalloc is not ported to s390(x)
%ifarch s390 s390x
    %define tcmallocflag --disable-tcmalloc
%else
    %define tcmallocflag --enable-tcmalloc
%endif

%if 0%{?have_spice:1}
    %define spiceflag --enable-spice
%else
    %define spiceflag --disable-spice
%endif

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir} \
    --interp-prefix=%{_prefix}/qemu-%%M \
    --localstatedir=%{_localstatedir} \
    --libexecdir=%{_libexecdir} \
    --with-pkgversion=%{name}-%{version}-%{release} \
    --disable-strip \
%ifnarch aarch64
    --extra-ldflags="$extraldflags -pie -Wl,-z,relro -Wl,-z,now" \
    --extra-cflags="%{optflags}" \
%endif
%ifarch aarch64
    --extra-cflags="%{optflags} -fPIC" \
%endif
    --enable-pie \
    --disable-werror \
    --target-list="$buildarch" \
    --audio-drv-list=pa,sdl,alsa,oss \
    --enable-trace-backend=$tracebackends \
    --enable-kvm \
    %{tcmallocflag} \
    %{spiceflag} \
    --with-sdlabi="2.0" \
    --with-gtkabi="3.0" \
%ifarch s390
    --enable-tcg-interpreter \
%endif
    "$@"

echo "config-host.mak contents:"
echo "==="
cat config-host.mak
echo "==="

# These is some problem upstream where libcacard is not built
# with --extra-cflags the first time, but if you remove some
# files and rerun make, lo and behold --extra-cflags is used.
# Hence the following hack:
make V=1 %{?_smp_mflags} $buildldflags ||:
rm ./libcacard/vcard_emul_nss.o ./libcacard/.libs/vcard_emul_nss.o
# End of hack.

make V=1 %{?_smp_mflags} $buildldflags

gcc %{_sourcedir}/ksmctl.c -O2 -g -o ksmctl


%install

%define _udevdir /lib/udev/rules.d
%define qemudocdir %{_docdir}/%{name}

mkdir -p %{buildroot}%{_udevdir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/qemu

install -D -p -m 0644 %{_sourcedir}/ksm.service %{buildroot}%{_unitdir}
install -D -p -m 0644 %{_sourcedir}/ksm.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl %{buildroot}%{_libexecdir}/ksmctl

install -D -p -m 0644 %{_sourcedir}/ksmtuned.service %{buildroot}%{_unitdir}
install -D -p -m 0755 %{_sourcedir}/ksmtuned %{buildroot}%{_sbindir}/ksmtuned
install -D -p -m 0644 %{_sourcedir}/ksmtuned.conf %{buildroot}%{_sysconfdir}/ksmtuned.conf

# Install qemu-guest-agent service and udev rules
install -m 0644 %{_sourcedir}/qemu-guest-agent.service %{buildroot}%{_unitdir}
install -m 0644 %{_sourcedir}/99-qemu-guest-agent.rules %{buildroot}%{_udevdir}

# Install kvm specific bits
%if %{have_kvm}
mkdir -p %{buildroot}%{_bindir}/
install -m 0755 scripts/kvm/kvm_stat %{buildroot}%{_bindir}/
install -m 0644 %{_sourcedir}/80-kvm.rules %{buildroot}%{_udevdir}
%endif


make DESTDIR=%{buildroot} install

%find_lang %{name}

chmod -x %{buildroot}%{_mandir}/man1/*
install -D -p -m 0644 -t %{buildroot}%{qemudocdir} Changelog README COPYING COPYING.LIB LICENSE
for emu in %{buildroot}%{_bindir}/qemu-system-*; do
    ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/$(basename $emu).1.gz
done

%if 0%{?need_qemu_kvm}
install -m 0755 %{_sourcedir}/qemu-kvm.sh %{buildroot}%{_bindir}/qemu-kvm
ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/qemu-kvm.1.gz
%endif

install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

# Provided by package openbios
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-ppc
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc32
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc64
# Provided by package SLOF
rm -rf %{buildroot}%{_datadir}/%{name}/slof.bin
# Provided by package ipxe
rm -rf %{buildroot}%{_datadir}/%{name}/pxe*rom
rm -rf %{buildroot}%{_datadir}/%{name}/efi*rom
# Provided by package seavgabios
rm -rf %{buildroot}%{_datadir}/%{name}/vgabios*bin
# Provided by package seabios
rm -rf %{buildroot}%{_datadir}/%{name}/bios.bin
rm -rf %{buildroot}%{_datadir}/%{name}/bios-256k.bin
rm -rf %{buildroot}%{_datadir}/%{name}/acpi-dsdt.aml
rm -rf %{buildroot}%{_datadir}/%{name}/q35-acpi-dsdt.aml
# Provided by package sgabios
rm -rf %{buildroot}%{_datadir}/%{name}/sgabios.bin

# the pxe gpxe images will be symlinks to the images on
# /usr/share/ipxe, as QEMU doesn't know how to look
# for other paths, yet.
pxe_link() {
  ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/%{name}/pxe-$1.rom
  ln -s ../ipxe.efi/$2.rom %{buildroot}%{_datadir}/%{name}/efi-$1.rom
}

pxe_link e1000 8086100e
pxe_link ne2k_pci 10ec8029
pxe_link pcnet 10222000
pxe_link rtl8139 10ec8139
pxe_link virtio 1af41000

rom_link() {
    ln -s $1 %{buildroot}%{_datadir}/%{name}/$2
}

rom_link ../seavgabios/vgabios-isavga.bin vgabios.bin
rom_link ../seavgabios/vgabios-cirrus.bin vgabios-cirrus.bin
rom_link ../seavgabios/vgabios-qxl.bin vgabios-qxl.bin
rom_link ../seavgabios/vgabios-stdvga.bin vgabios-stdvga.bin
rom_link ../seavgabios/vgabios-vmware.bin vgabios-vmware.bin
rom_link ../seavgabios/vgabios-virtio.bin vgabios-virtio.bin
rom_link ../seabios/bios.bin bios.bin
rom_link ../seabios/bios-256k.bin bios-256k.bin
rom_link ../seabios/acpi-dsdt.aml acpi-dsdt.aml
rom_link ../seabios/q35-acpi-dsdt.aml q35-acpi-dsdt.aml
rom_link ../sgabios/sgabios.bin sgabios.bin

# Install binfmt
mkdir -p %{buildroot}%{_exec_prefix}/lib/binfmt.d
for i in dummy \
%ifnarch %{ix86} x86_64
    qemu-i386 \
%endif
%ifnarch alpha
    qemu-alpha \
%endif
%ifnarch %{arm}
    qemu-arm \
%endif
    qemu-armeb \
    qemu-cris \
    qemu-microblaze qemu-microblazeel \
%ifnarch mips
    qemu-mips qemu-mips64 \
%endif
%ifnarch mipsel
    qemu-mipsel qemu-mips64el \
%endif
%ifnarch m68k
    qemu-m68k \
%endif
%ifnarch ppc ppc64 ppc64le
    qemu-ppc qemu-ppc64abi32 qemu-ppc64 \
%endif
%ifnarch sparc sparc64
    qemu-sparc qemu-sparc32plus qemu-sparc64 \
%endif
%ifnarch s390 s390x
    qemu-s390x \
%endif
%ifnarch sh4
    qemu-sh4 \
%endif
    qemu-sh4eb \
; do
  test $i = dummy && continue
  grep /$i:\$ %{_sourcedir}/qemu.binfmt > %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i.conf
  chmod 644 %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i.conf
done < %{_sourcedir}/qemu.binfmt


# Install rules to use the bridge helper with libvirt's virbr0
install -m 0644 %{_sourcedir}/bridge.conf %{buildroot}%{_sysconfdir}/qemu

# Install libcacard.so
find %{buildroot} -name '*.la' -or -name '*.a' | xargs rm -f
find %{buildroot} -name "libcacard.so*" -exec chmod +x \{\} \;

# When building using 'rpmbuild' or 'fedpkg local', RPATHs can be left in
# the binaries and libraries (although this doesn't occur when
# building in Koji, for some unknown reason). Some discussion here:
#
# https://lists.fedoraproject.org/pipermail/devel/2013-November/192553.html
#
# In any case it should always be safe to remove RPATHs from
# the final binaries:
for f in %{buildroot}%{_bindir}/* %{buildroot}%{_libdir}/* \
         %{buildroot}%{_libexecdir}/*; do
  if file $f | grep -q ELF; then chrpath --delete $f; fi
done


%check

# 2.3.0-rc2 tests are hanging on s390
# https://bugzilla.redhat.com/show_bug.cgi?id=1206057
# Tests seem to be a recurring problem on s390, so I'd suggest just leaving
# it disabled.
%global archs_skip_tests s390
%global archs_ignore_test_failures 0

%ifnarch %{archs_skip_tests}

# Check the binary runs (see eg RHBZ#998722).
b="./x86_64-softmmu/qemu-system-x86_64"
if [ -x "$b" ]; then "$b" -help; fi

%ifarch %{archs_ignore_test_failures}
make check V=1
%else
make check V=1 || :
%endif

# Sanity-check current kernel can boot on this qemu.
# The results are advisory only.
%ifarch %{arm}
hostqemu=arm-softmmu/qemu-system-arm
%endif
%ifarch aarch64
hostqemu=arm-softmmu/qemu-system-aarch64
%endif
%ifarch %{ix86}
hostqemu=i386-softmmu/qemu-system-i386
%endif
%ifarch x86_64
hostqemu=x86_64-softmmu/qemu-system-x86_64
%endif
if test -f "$hostqemu"; then qemu-sanity-check --qemu=$hostqemu ||: ; fi

%endif  # archs_skip_tests


%if %{have_kvm}
%post %{kvm_package}
# Default /dev/kvm permissions are 660, we install a udev rule changing that
# to 666. However trying to trigger the re-permissioning via udev has been
# a neverending source of trouble, so we just force it with chmod. For
# more info see: https://bugzilla.redhat.com/show_bug.cgi?id=950436
chmod --quiet 666 /dev/kvm || :
%endif


%post common
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu


%post -n ksm
%systemd_post ksm.service
%systemd_post ksmtuned.service
%preun -n ksm
%systemd_preun ksm.service
%systemd_preun ksmtuned.service
%postun -n ksm
%systemd_postun_with_restart ksm.service
%systemd_postun_with_restart ksmtuned.service


%post -n libcacard -p /sbin/ldconfig
%postun -n libcacard -p /sbin/ldconfig


%post user
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%postun user
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :


%global kvm_files \
%{_udevdir}/80-kvm.rules


%files

%if %{have_kvm}
%files kvm
%endif

%files common -f %{name}.lang
%dir %{qemudocdir}
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/README
%doc %{qemudocdir}/qemu-doc.html
%doc %{qemudocdir}/qemu-tech.html
%doc %{qemudocdir}/qmp-commands.txt
%doc %{qemudocdir}/COPYING
%doc %{qemudocdir}/COPYING.LIB
%doc %{qemudocdir}/LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/qemu-icon.bmp
%{_datadir}/%{name}/qemu_logo_no_text.svg
%{_datadir}/%{name}/keymaps/
%{_datadir}/%{name}/trace-events
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/virtfs-proxy-helper.1*
%{_bindir}/virtfs-proxy-helper
%attr(4755, root, root) %{_libexecdir}/qemu-bridge-helper
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
%dir %{_sysconfdir}/qemu
%config(noreplace) %{_sysconfdir}/qemu/bridge.conf


%files -n ksm
%{_libexecdir}/ksmctl
%{_sbindir}/ksmtuned
%{_unitdir}/ksmtuned.service
%{_unitdir}/ksm.service
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ksm


%files guest-agent
%doc COPYING README
%{_bindir}/qemu-ga
%{_unitdir}/qemu-guest-agent.service
%{_udevdir}/99-qemu-guest-agent.rules


%files user
%{_exec_prefix}/lib/binfmt.d/qemu-*.conf
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-aarch64
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-mips64
%{_bindir}/qemu-mips64el
%{_bindir}/qemu-mipsn32
%{_bindir}/qemu-mipsn32el
%{_bindir}/qemu-or32
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64abi32
%{_bindir}/qemu-ppc64le
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-unicore32
%{_datadir}/systemtap/tapset/qemu-i386*.stp
%{_datadir}/systemtap/tapset/qemu-x86_64*.stp
%{_datadir}/systemtap/tapset/qemu-aarch64*.stp
%{_datadir}/systemtap/tapset/qemu-alpha*.stp
%{_datadir}/systemtap/tapset/qemu-arm*.stp
%{_datadir}/systemtap/tapset/qemu-cris*.stp
%{_datadir}/systemtap/tapset/qemu-m68k*.stp
%{_datadir}/systemtap/tapset/qemu-microblaze*.stp
%{_datadir}/systemtap/tapset/qemu-mips*.stp
%{_datadir}/systemtap/tapset/qemu-or32*.stp
%{_datadir}/systemtap/tapset/qemu-ppc*.stp
%{_datadir}/systemtap/tapset/qemu-s390x*.stp
%{_datadir}/systemtap/tapset/qemu-sh4*.stp
%{_datadir}/systemtap/tapset/qemu-sparc*.stp
%{_datadir}/systemtap/tapset/qemu-unicore32*.stp


%files system-x86
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_datadir}/systemtap/tapset/qemu-system-i386*.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64*.stp
%{_mandir}/man1/qemu-system-i386.1*
%{_mandir}/man1/qemu-system-x86_64.1*

%if 0%{?need_qemu_kvm}
%{_bindir}/qemu-kvm
%{_mandir}/man1/qemu-kvm.1*
%endif

%{_datadir}/%{name}/acpi-dsdt.aml
%{_datadir}/%{name}/q35-acpi-dsdt.aml
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/bios-256k.bin
%{_datadir}/%{name}/sgabios.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/kvmvapic.bin
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/vgabios-stdvga.bin
%{_datadir}/%{name}/vgabios-vmware.bin
%{_datadir}/%{name}/vgabios-virtio.bin
%{_datadir}/%{name}/pxe-e1000.rom
%{_datadir}/%{name}/efi-e1000.rom
%{_datadir}/%{name}/pxe-virtio.rom
%{_datadir}/%{name}/efi-virtio.rom
%{_datadir}/%{name}/pxe-pcnet.rom
%{_datadir}/%{name}/efi-pcnet.rom
%{_datadir}/%{name}/pxe-rtl8139.rom
%{_datadir}/%{name}/efi-rtl8139.rom
%{_datadir}/%{name}/pxe-ne2k_pci.rom
%{_datadir}/%{name}/efi-ne2k_pci.rom
%ifarch %{ix86} x86_64
%{?kvm_files:}
%endif


%if %{have_kvm}
%files kvm-tools
%{_bindir}/kvm_stat
%endif


%files system-alpha
%{_bindir}/qemu-system-alpha
%{_datadir}/systemtap/tapset/qemu-system-alpha*.stp
%{_mandir}/man1/qemu-system-alpha.1*
%{_datadir}/%{name}/palcode-clipper


%files system-arm
%{_bindir}/qemu-system-arm
%{_datadir}/systemtap/tapset/qemu-system-arm*.stp
%{_mandir}/man1/qemu-system-arm.1*
%ifarch armv7hl
%{?kvm_files:}
%endif


%files system-mips
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%{_datadir}/systemtap/tapset/qemu-system-mips*.stp
%{_mandir}/man1/qemu-system-mips.1*
%{_mandir}/man1/qemu-system-mipsel.1*
%{_mandir}/man1/qemu-system-mips64el.1*
%{_mandir}/man1/qemu-system-mips64.1*


%files system-cris
%{_bindir}/qemu-system-cris
%{_datadir}/systemtap/tapset/qemu-system-cris*.stp
%{_mandir}/man1/qemu-system-cris.1*


%files system-lm32
%{_bindir}/qemu-system-lm32
%{_datadir}/systemtap/tapset/qemu-system-lm32*.stp
%{_mandir}/man1/qemu-system-lm32.1*


%files system-m68k
%{_bindir}/qemu-system-m68k
%{_datadir}/systemtap/tapset/qemu-system-m68k*.stp
%{_mandir}/man1/qemu-system-m68k.1*


%files system-microblaze
%{_bindir}/qemu-system-microblaze
%{_bindir}/qemu-system-microblazeel
%{_datadir}/systemtap/tapset/qemu-system-microblaze*.stp
%{_mandir}/man1/qemu-system-microblaze.1*
%{_mandir}/man1/qemu-system-microblazeel.1*
%{_datadir}/%{name}/petalogix*.dtb


%files system-or32
%{_bindir}/qemu-system-or32
%{_datadir}/systemtap/tapset/qemu-system-or32*.stp
%{_mandir}/man1/qemu-system-or32.1*


%files system-s390x
%{_bindir}/qemu-system-s390x
%{_datadir}/systemtap/tapset/qemu-system-s390x*.stp
%{_mandir}/man1/qemu-system-s390x.1*
%{_datadir}/%{name}/s390-zipl.rom
%{_datadir}/%{name}/s390-ccw.img
%ifarch s390x
%{?kvm_files:}
%endif


%files system-sh4
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb
%{_datadir}/systemtap/tapset/qemu-system-sh4*.stp
%{_mandir}/man1/qemu-system-sh4.1*
%{_mandir}/man1/qemu-system-sh4eb.1*


%files system-sparc
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-sparc64
%{_datadir}/systemtap/tapset/qemu-system-sparc*.stp
%{_mandir}/man1/qemu-system-sparc.1*
%{_mandir}/man1/qemu-system-sparc64.1*
%{_datadir}/%{name}/QEMU,tcx.bin
%{_datadir}/%{name}/QEMU,cgthree.bin


%files system-ppc
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
%{_bindir}/qemu-system-ppcemb
%{_datadir}/systemtap/tapset/qemu-system-ppc*.stp
%{_datadir}/systemtap/tapset/qemu-system-ppc64*.stp
%{_datadir}/systemtap/tapset/qemu-system-ppcemb*.stp
%{_mandir}/man1/qemu-system-ppc.1*
%{_mandir}/man1/qemu-system-ppc64.1*
%{_mandir}/man1/qemu-system-ppcemb.1*
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/ppc_rom.bin
%{_datadir}/%{name}/spapr-rtas.bin
%{_datadir}/%{name}/u-boot.e500
%ifarch ppc64 ppc64le
%{?kvm_files:}
%endif


%files system-unicore32
%{_bindir}/qemu-system-unicore32
%{_datadir}/systemtap/tapset/qemu-system-unicore32*.stp
%{_mandir}/man1/qemu-system-unicore32.1*


%files system-xtensa
%{_bindir}/qemu-system-xtensa
%{_bindir}/qemu-system-xtensaeb
%{_datadir}/systemtap/tapset/qemu-system-xtensa*.stp
%{_mandir}/man1/qemu-system-xtensa.1*
%{_mandir}/man1/qemu-system-xtensaeb.1*


%files system-moxie
%{_bindir}/qemu-system-moxie
%{_datadir}/systemtap/tapset/qemu-system-moxie*.stp
%{_mandir}/man1/qemu-system-moxie.1*


%files system-aarch64
%{_bindir}/qemu-system-aarch64
%{_datadir}/systemtap/tapset/qemu-system-aarch64*.stp
%{_mandir}/man1/qemu-system-aarch64.1*
%ifarch aarch64
%{?kvm_files:}
%endif


%files system-tricore
%{_bindir}/qemu-system-tricore
%{_datadir}/systemtap/tapset/qemu-system-tricore*.stp
%{_mandir}/man1/qemu-system-tricore.1*


%files img
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*


%files -n libcacard
%{_libdir}/libcacard.so.*


%files -n libcacard-tools
%{_bindir}/vscclient


%files -n libcacard-devel
%{_includedir}/cacard
%{_libdir}/libcacard.so
%{_libdir}/pkgconfig/libcacard.pc


%changelog
* Mon Aug 31 2015 Cole Robinson <crobinso@redhat.com> - 2:2.4.0-2
- CVE-2015-5255: heap memory corruption in vnc_refresh_server_surface (bz
  #1255899)

* Tue Aug 11 2015 Cole Robinson <crobinso@redhat.com> - 2:2.4.0-1
- Rebased to version 2.4.0
- Support for virtio-gpu, 2D only
- Support for virtio-based keyboard/mouse/tablet emulation
- x86 support for memory hot-unplug
- ACPI v5.1 table support for 'virt' board

* Sun Aug 09 2015 Cole Robinson <crobinso@redhat.com> - 2:2.4.0-0.2.rc4
- CVE-2015-3209: pcnet: multi-tmd buffer overflow in the tx path (bz #1230536)
- CVE-2015-3214: i8254: out-of-bounds memory access (bz #1243728)
- CVE-2015-5158: scsi stack buffer overflow (bz #1246025)
- CVE-2015-5154: ide: atapi: heap overflow during I/O buffer memory access (bz
  #1247141)
- CVE-2015-5165: rtl8139 uninitialized heap memory information leakage to
  guest (bz #1249755)
- CVE-2015-5166: BlockBackend object use after free issue (bz #1249758)
- CVE-2015-5745: buffer overflow in virtio-serial (bz #1251160)

* Tue Jul 14 2015 Cole Robinson <crobinso@redhat.com> 2:2.4.0-0.1-rc0
- Rebased to version 2.4.0-rc0

* Fri Jul  3 2015 Richard W.M. Jones <rjones@redhat.com> - 2:2.3.0-15
- Bump and rebuild.

* Fri Jul  3 2015 Daniel P. Berrange <berrange@redhat.com> - 2:2.3.0-14
- Use explicit --(enable,disable)-spice args (rhbz #1239102)

* Thu Jul  2 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2:2.3.0-13
- Build aarch64 with -fPIC (rhbz 1232499)

* Wed Jul 01 2015 Nick Clifton <nickc@redhat.com> - 2:2.3.0-12
- Disable stack protection for AArch64.  F23's GCC thinks that it is available but F23's glibc does not support it.

* Fri Jun 26 2015 Paolo Bonzini <pbonzini@redhat.com> - 2:2.3.0-10
- Rebuild for libiscsi soname bump

* Fri Jun 19 2015 Paolo Bonzini <pbonzini@redhat.com> - 2:2.3.0-10
- Re-enable tcmalloc on arm

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Dan Horák <dan[at]danny.cz> - 2:2.3.0-8
- gperftools not available on s390(x)

* Fri Jun 05 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-7
- CVE-2015-4037: insecure temporary file use in /net/slirp.c (bz #1222894)

* Mon Jun  1 2015 Daniel P. Berrange <berrange@redhat.com> - 2:2.3.0-6
- Disable tcmalloc on arm since it currently hangs (rhbz #1226806)
- Re-enable tests on arm

* Wed May 13 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-5
- Backport upstream 2.4 patch to link with tcmalloc, enable it
- CVE-2015-3456: (VENOM) fdc: out-of-bounds fifo buffer memory access (bz
  #1221152)

* Sun May 10 2015 Paolo Bonzini <pbonzini@redhat.com> 2:2.3.0-4
- Backport upstream 2.4 patch to link with tcmalloc, enable it
- Add -p1 to autopatch

* Wed May 06 2015 Cole Robinson <crobinso@redhat.com> 2:2.3.0-3
- Fix ksm.service (bz 1218814)

* Tue May  5 2015 Dan Horák <dan[at]danny.cz> - 2:2.3.0-2
- Require libseccomp only when built with it

* Tue Mar 24 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-1
- Rebased to version 2.3.0 GA
- Another attempt at fixing default /dev/kvm permissions (bz 950436)

* Tue Mar 24 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-0.5.rc3
- Drop unneeded kvm.modules
- Fix s390/ppc64 FTBFS (bz 1212328)

* Tue Mar 24 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-0.4.rc3
- Rebased to version 2.3.0-rc3

* Tue Mar 24 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-0.3.rc2
- Rebased to version 2.3.0-rc2
- Don't install ksm services as executable (bz #1192720)
- Skip hanging tests on s390 (bz #1206057)
- CVE-2015-1779 vnc: insufficient resource limiting in VNC websockets decoder
  (bz #1205051, bz #1199572)

* Tue Mar 24 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-0.2.rc1
- Rebased to version 2.3.0-rc1

* Sun Mar 22 2015 Cole Robinson <crobinso@redhat.com> - 2:2.3.0-0.1.rc0
- Rebased to version 2.3.0-rc0

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 2:2.2.0-7
- Add -fPIC flag to build to avoid
  'relocation R_X86_64_PC32 against undefined symbol' errors.
- Add a hopefully temporary hack so that -fPIC is used to build
  NSS files in libcacard.

* Wed Feb  4 2015 Richard W.M. Jones <rjones@redhat.com> - 2:2.2.0-5
- Add UEFI support for aarch64.

* Tue Feb  3 2015 Daniel P. Berrange <berrange@redhat.com> - 2:2.2.0-4
- Re-enable SPICE after previous build fixes circular dep

* Tue Feb  3 2015 Daniel P. Berrange <berrange@redhat.com> - 2:2.2.0-3
- Rebuild for changed xen soname
- Temporarily disable SPICE to break circular build-dep on libcacard
- Stop libcacard linking against the entire world

* Wed Jan 28 2015 Daniel P. Berrange <berrange@redhat.com> - 2:2.2.0-2
- Pass package information to configure

* Tue Dec 09 2014 Cole Robinson <crobinso@redhat.com> - 2:2.2.0-1
- Rebased to version 2.2.0

* Sun Nov 30 2014 Cole Robinson <crobinso@redhat.com> - 2:2.2.0-0.2.rc3
- Update to qemu-2.2.0-rc3

* Sat Nov 15 2014 Cole Robinson <crobinso@redhat.com> - 2:2.2.0-0.1.rc1
- Update to qemu-2.2.0-rc1

* Wed Oct 29 2014 Cole Robinson <crobinso@redhat.com> - 2:2.1.2-6
- CVE-2014-7815 vnc: insufficient bits_per_pixel from the client sanitization
  (bz #1157647, bz #1157641)
- CVE-2014-3689 vmware_vga: insufficient parameter validation in rectangle
  functions (bz #1153038, bz #1153035)

* Fri Oct 24 2014 Danel P. Berrange <berrange@redhat.com> - 2:2.1.2-5
- Fix dep on numactl-devel to be build time not install time

* Mon Oct 06 2014 Cole Robinson <crobinso@redhat.com> - 2:2.1.2-4
- Fix PPC virtio regression (bz #1144490)

* Tue Sep 30 2014 Dan Horák <dan[at]danny.cz> - 2:2.1.2-3
- Enable KVM on ppc64le

* Fri Sep 26 2014 Richard W.M. Jones <rjones@redhat.com> - 2:2.1.2-2
- Add Requires seabios >= 1.7.5, otherwise Windows virtio booting does
  not work.

* Fri Sep 26 2014 Cole Robinson <crobinso@redhat.com> - 2:2.1.2-1
- Rebased to version 2.1.2
- CVE-2014-3640 qemu: slirp: NULL pointer (bz #1144821, bz #1144818)

* Sun Sep 21 2014 Cole Robinson <crobinso@redhat.com> - 2:2.1.1-2
- Fix crash on migration/snapshot (bz #1144490)

* Thu Sep 11 2014 Cole Robinson <crobinso@redhat.com> - 2:2.1.1-1
- Rebased to version 2.1.1
- CVE-2014-5388: out of bounds memory access (bz #1132962, bz #1132956)
- CVE-2014-3615 crash when guest sets high resolution (bz #1139121, bz
  #1139115)

* Wed Sep  3 2014 Richard W.M. Jones <rjones@redhat.com> 2:2.1.0-6
- Add upstream patches to:
  * Fix crash in curl driver.
  * Add curl timeout option.
  * Add curl cookie option.
- Add upstream commit hashes to patches.

* Wed Aug 20 2014 Richard W.M. Jones <rjones@redhat.com> 2:2.1.0-5
- Add patch for aarch64 which uncompresses -kernel parameter (in arm.next).

* Mon Aug 18 2014 Dan Horák <dan[at]danny.cz> - 2:2.1.0-4
- Don't fail build due failing tests on s390 (#1100971)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Aug 03 2014 Richard W.M. Jones <rjones@redhat.com> 2:2.1.0-2
- Update to qemu 2.1.0 final released version.
- Drop optimization flags when compiling on aarch64 (see RHBZ#1126199).

* Fri Jul 25 2014 Cole Robinson <crobinso@redhat.com> 2:2.1.0-0.5.rc3
- Update to qemu-2.1.0-rc3

* Wed Jul 16 2014 Cole Robinson <crobinso@redhat.com> 2:2.1.0-0.4.rc2
- Update to qemu-2.1.0-rc2

* Mon Jul 14 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2:2.1.0-0.3.rc1
- Build qemu-system-aarch64 on all arches
- Run check on ARM arches, just don't fail the build ATM

* Wed Jul 09 2014 Cole Robinson <crobinso@redhat.com> - 2:2.1.0-0.2.rc1
- Update to qemu-2.1.0-rc1
- Enable SDL2 frontend, it's improved recently
- Fix drive-mirror segfaults if source size is not cluster-aligned (bz
  #1114791)
- Fix crash with virtio-blk hotunplug (bz #1117181)

* Fri Jul 04 2014 Cole Robinson <crobinso@redhat.com> - 2:2.1.0-0.1.rc0
- Update to qemu 2.1-rc0

* Sun Jun 15 2014 Cole Robinson <crobinso@redhat.com> - 2:2.0.0-7
- Don't use libtool on dtrace, fixes rawhide build (bz #1106968)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 31 2014 Cole Robinson <crobinso@redhat.com> - 2:2.0.0-5
- QCOW1 validation CVEs: CVE-2014-0222, CVE-2014-0223 (bz #1097232, bz
  #1097238, bz #1097222, bz #1097216)
- CVE-2014-3461: Issues in USB post load checks (bz #1097260, bz #1096821)

* Sun May 11 2014 Cole Robinson <crobinso@redhat.com> - 2:2.0.0-4
- Migration CVEs: CVE-2014-0182 etc.

* Wed Apr 30 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2:2.0.0-3
- Fix aarch64 build

* Mon Apr 21 2014 Cole Robinson <crobinso@redhat.com> - 2:2.0.0-2
- Don't use SDL2 API support, it's incomplete
- Build qemu-system-aarch64 only on aarch64 for now

* Thu Apr 17 2014 Cole Robinson <crobinso@redhat.com> - 2:2.0.0-1
- Update to 2.0.0 GA

* Tue Apr 15 2014 Cole Robinson <crobinso@redhat.com> - 2:2.0.0-0.3.rc3
- Update to qemu 2.0-rc3
- Fix crash when restoring from snapshot (bz #1085632)

* Mon Mar 24 2014 Cole Robinson <crobinso@redhat.com> - 2:2.0.0-0.2.rc0
- Change gtk quit accelerator to ctrl+shift+q (bz #1062393)
- Fix mouse with spice
- Enable xen support for xen 4.4

* Tue Mar 18 2014 Cole Robinson <crobinso@redhat.com> 2:2.0.0-0.1.rc0
- Update to qemu 2.0.0-rc0

* Tue Feb 18 2014 Richard W.M. Jones <rjones@redhat.com> - 2:1.7.0-5
- Run qemu-sanity-check on x86 and armv7 too.  The results are still
  only advisory.

* Mon Jan 13 2014 Richard W.M. Jones <rjones@redhat.com> - 2:1.7.0-4
- Disable make check on aarch64.

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 2:1.7.0-3
- Add libcacard ldconfig %%post* scriptlets.

* Wed Dec 18 2013 Cole Robinson <crobinso@redhat.com> - 2:1.7.0-2
- Add kill() to seccomp whitelist, fix AC97 with -sandbox on (bz #1043521)
- Changing streaming mode default to off for spice (bz #1038336)
- Fix guest scsi verify command (bz #1001617)

* Mon Dec 02 2013 Cole Robinson <crobinso@redhat.com> - 2:1.7.0-1
- Fix qemu-img create with NBD backing file (bz #1034433)
- Rebase to qemu-1.7 GA
- New monitor command blockdev-add for full featured block device hotplug.
- Performance and functionality improvements for USB 3.0.
- Many VFIO improvements
- ACPI tables can be generated by QEMU and can be used by firmware directly.
- Support creating and writing .vhdx images.
- qemu-img map: dump detailed image file metadata

* Fri Nov 29 2013 Richard W.M. Jones <rjones@redhat.com> - 2:1.7.0-0.2.rc1
- Run chrpath on binaries, so qemu can be built using rpmbuild.

* Thu Nov 21 2013 Cole Robinson <crobinso@redhat.com> - 2:1.7.0-0.1.rc1
- Update qemu-1.7.0-rc1

* Sun Nov 17 2013 Cole Robinson <crobinso@redhat.com> - 2:1.6.1-2
- Fix drive discard options via libvirt (bz #1029953)
- Fix process exit with -sandbox on (bz #1027421)

* Tue Nov 05 2013 Cole Robinson <crobinso@redhat.com> - 2:1.6.1-1
- Reduce CPU usage when audio is playing (bz #1017644)
- Base on qemu 1.6.1 tarball
- ksmtuned: Fix matching qemu w/o set_process_name (bz #1012604)
- ksmtuned: Fix committed_memory when no qemu running (bz #1012610)
- Make sure bridge helper is setuid (bz #1017660)

* Wed Oct 09 2013 Cole Robinson <crobinso@redhat.com> - 2:1.6.0-10
- Fix migration from qemu <= 1.5

* Sun Oct 06 2013 Cole Robinson <crobinso@redhat.com> - 2:1.6.0-9
- Rebase to pending 1.6.1 stable
- CVE-2013-4377: Fix crash when unplugging virtio devices (bz #1012633, bz
  #1012641)
- Fix 'new snapshot' slowness after the first snap (bz #988436)
- Fix 9pfs xattrs on kernel 3.11 (bz #1013676)
- CVE-2013-4344: buffer overflow in scsi_target_emulate_report_luns (bz
  #1015274, bz #1007330)

* Tue Sep 24 2013 Cole Robinson <crobinso@redhat.com> - 2:1.6.0-8
- Fix -vga qxl with -display vnc (bz #948717)
- Fix USB crash when installing reactos (bz #1005495)
- Don't ship x86 kvm wrapper on arm (bz #1005581)

* Thu Sep 12 2013 Dan Horák <dan[at]danny.cz> - 2:1.6.0-7
- Enable TCG interpreter for s390 as the native backend supports 64-bit only
- Don't require RDMA on s390(x)

* Tue Sep 03 2013 Cole Robinson <crobinso@redhat.com> - 2:1.6.0-6
- Fix qmp capabilities calls on i686 (bz #1003162)
- Fix crash with -M isapc -cpu Haswell (bz #986790)
- Fix crash in lsi_soft_reset (bz #1000947)
- Fix initial /dev/kvm permissions (bz #993491)

* Wed Aug 28 2013 Richard W.M. Jones <rjones@redhat.com> - 2:1.6.0-5
- Enable qemu-sanity-check, however do not fail the build if it fails.

* Wed Aug 21 2013 Richard W.M. Jones <rjones@redhat.com> - 2:1.6.0-4
- Require newer libssh2 to fix missing libssh2_sftp_fsync (bz #999161)

* Tue Aug 20 2013 Cole Robinson <crobinso@redhat.com> - 2:1.6.0-3
- Require newer ceph-libs to fix symbol error (bz #995883)

* Tue Aug 20 2013 Richard W.M. Jones <rjones@redhat.com> - 2:1.6.0-2
- Try to rebuild since previous i686 build was broken (RHBZ#998722).
- In build, qemu -help just to check the binary is not broken.

* Fri Aug 16 2013 Cole Robinson <crobinso@redhat.com> - 2:1.6.0-1
- Rebased to version 1.6.0
- Support for live migration over RDMA
- TCG target for aarch64.
- Support for auto-convergence in live migration ("CPU stunning")
- The XHCI (USB 3.0) controller supports live migration.
- New device "nvme" provides a PCI device that implements the NVMe
  standard.
- ACPI hotplug of devices behind a PCI bridge is supported

* Sun Aug 04 2013 Dennis Gilmore <dennis@ausil.us> - 2:1.5.2-4
- re-enable spice support

* Fri Aug 02 2013 Dennis Gilmore <dennis@ausil.us> - 2:1.5.2-3
- build without spice support to build against new libiscsi
- spice requires parts of qemu

* Fri Aug 2 2013 Paolo Bonzini <pbonzini@redhat.com> - 2:1.5.2-2
- Rebuild for libiscsi soname bump

* Mon Jul 29 2013 Cole Robinson <crobinso@redhat.com> - 2:1.5.2-1
- Rebased to version 1.5.2
- Fix mouse display with spice and latest libvirt (bz #981094)

* Tue Jul 09 2013 Cole Robinson <crobinso@redhat.com> - 2:1.5.1-2
- Update to work with seabios 1.7.3

* Fri Jun 28 2013 Cole Robinson <crobinso@redhat.com> - 2:1.5.1-1
- Rebased to version 1.5.1

* Wed Jun 19 2013 Cole Robinson <crobinso@redhat.com> - 2:1.5.0-9
- Don't install conflicting binfmt handler on arm (bz #974804)
- Use upstream patch for libfdt build fix

* Fri Jun 14 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2:1.5.0-8
- Put ARM kvm bits in right sub package

* Thu Jun 13 2013 Cole Robinson <crobinso@redhat.com> - 2:1.5.0-7
- Fix build with both new and old fdt

* Wed Jun 12 2013 Cole Robinson <crobinso@redhat.com> - 2:1.5.0-6
- Fix build with rawhide libfdt

* Tue Jun 11 2013 Cole Robinson <crobinso@redhat.com> - 2:1.5.0-5
- Fix rtl8139 + windows 7 + large transfers (bz #970240)

* Sat Jun  1 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2:1.5.0-4
- build qemu-kvm on ARMv7

* Mon May 27 2013 Dan Horák <dan[at]danny.cz> - 2:1.5.0-3
- Install the qemu-kvm.1 man page only on arches with kvm

* Sat May 25 2013 Cole Robinson <crobinso@redhat.com> - 2:1.5.0-2
- Alias qemu-system-* man page to qemu.1 (bz #907746)
- Drop execute bit on service files (bz #963917)
- Conditionalize KSM service on host virt support (bz #963681)
- Split out KSM package, make it not pulled in by default

* Tue May 21 2013 Cole Robinson <crobinso@redhat.com> - 2:1.5.0-1
- Update to qemu 1.5
- KVM for ARM support
- A native GTK+ UI with internationalization support
- Experimental VFIO support for VGA passthrough
- Support for VMware PVSCSI and VMXNET3 device emulation
- CPU hot-add support

* Thu May 16 2013 Paolo Bonzini <pbonzini@redhat.com> - 2:1.4.1-3
- Drop loading of vhost-net module (bz #963198)

* Wed May 15 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.1-2
- Fix crash with usbredir (bz #962826)
- Drop unneeded kvm.modules on x86 (bz #963198)
- Make ksmtuned handle set_progname usage (bz #955230)
- Enable gluster support

* Sat Apr 20 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.1-1
- Rebased to version 1.4.1
- qemu stable release 1.4.1 (bz 952599)
- CVE-2013-1922: qemu-nbd block format auto-detection vulnerability (bz
  952574, bz 923219)

* Thu Apr 04 2013 Richard W.M. Jones <rjones@redhat.com> - 2:1.4.0-11
- Rebuild to attempt to fix broken dep on libbrlapi.so.0.5

* Wed Apr 03 2013 Nathaniel McCallum <nathaniel@themccallums.org> - 2:1.4.0-10
- Sorted qemu.binfmt
- Remove mipsn32 / mipsn32el binfmt support (it is broken and can't be fixed)
- Fix binfmt support for mips / mipsel to match what qemu can do
- Add binfmt support for cris
- Add binfmt support for microblaze / microblazeel
- Add binfmt support for sparc64 / sparc32plus
- Add binfmt support for ppc64 / ppc64abi32

* Wed Apr 03 2013 Hans de Goede <hdegoede@redhat.com> - 2:1.4.0-9
- Fix USB-tablet not working with some Linux guests (bz #929068)

* Tue Apr 02 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.0-8
- Fix dep on seavgabios-bin

* Mon Apr 01 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.0-7
- Fixes for iscsi dep
- Fix TCG ld/st optimization (lp 1127369)
- Fix possible crash with VNC and qxl (bz #919777)
- Fix kvm module permissions after first install (bz #907215)
- Switch to seavgabios by default

* Sun Mar 31 2013 Richard W.M. Jones <rjones@redhat.com> - 2:1.4.0-6
- Fix TCG ld/st optimization. https://bugs.launchpad.net/bugs/1127369

* Thu Mar 14 2013 Paolo Bonzini <pbonzini@redhat.com> - 2:1.4.0-5
- do not package libcacard in the separate_kvm case
- backport xfsprogs and usbredir flags from el6

* Mon Mar 11 2013 Paolo Bonzini <pbonzini@redhat.com> - 2:1.4.0-4
- Use pkg-config to search for libiscsi

* Mon Mar 11 2013 Paolo Bonzini <pbonzini@redhat.com> - 2:1.4.0-3
- Added libiscsi-devel BuildRequires

* Fri Mar 01 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.0-2
- Fix test ordering with latest glib

* Tue Feb 19 2013 Cole Robinson <crobinso@redhat.com> - 2:1.4.0-1
- Rebased to version 1.4.0
- block: dataplane for virtio, potentially large performance improvment
- migration: threaded live migration
- usb-tablet: usb 2.0 support, significantly lowering CPU usage
- usb: improved support for pass-through of USB serial devices
- virtio-net: added support supports multiqueue operation

* Sat Feb  2 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 2:1.3.0-9
- add BR perl-podlators for pod2man (F19 development)
- fix "bogus date" entries in %%changelog to fix rebuild

* Fri Feb 01 2013 Alon Levy <alevy@redhat.com> - 2:1.3.0-8
- rebuilt, removing the two added Provides & Obsoletes lines, since
  the current EVR already does that by being 1.3.0 > 1.2.2 , and having
  the same package name of "libcacard"

* Tue Jan 29 2013 Alon Levy <alevy@redhat.com> - 2:1.3.0-7
- Bump and rebuild for updated Provides & Obsoletes of libcacard 1.2.2-4

* Mon Jan 28 2013 Richard W.M. Jones <rjones@redhat.com> - 2:1.3.0-6
- Bump and rebuild for updated libseccomp.

* Tue Jan 22 2013 Alon Levy <alevy redhat com> - 2:1.3.0-5
- Fix missing error_set symbol in libcacard.so (bz #891552)

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 2:1.3.0-4
- rebuild due to "jpeg8-ABI" feature drop

* Tue Jan 15 2013 Cole Robinson <crobinso@redhat.com> - 2:1.3.0-3
- Fix migration from qemu-kvm
- Fix the test suite on i686
- Use systemd macros in specfile (bz #850285)

* Tue Jan 15 2013 Hans de Goede <hdegoede@redhat.com> - 2:1.3.0-2
- Fix 0110-usb-redir-Add-flow-control-support.patch being mangled on rebase
  to 1.3.0, breaking usbredir support

* Fri Dec 07 2012 Cole Robinson <crobinso@redhat.com> - 2:1.3.0-1
- Switch base tarball from qemu-kvm to qemu
- qemu 1.3 release
- Option to use linux VFIO driver to assign PCI devices
- Many USB3 improvements
- New paravirtualized hardware random number generator device.
- Support for Glusterfs volumes with "gluster://" -drive URI
- Block job commands for live block commit and storage migration

* Wed Nov 28 2012 Alon Levy <alevy@redhat.com> - 2:1.2.0-25
* Merge libcacard into qemu, since they both use the same sources now.

* Thu Nov 22 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-24
- Move vscclient to qemu-common, qemu-nbd to qemu-img

* Tue Nov 20 2012 Alon Levy <alevy@redhat.com> - 2:1.2.0-23
- Rewrite fix for bz #725965 based on fix for bz #867366
- Resolve bz #867366

* Fri Nov 16 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-23
- Backport --with separate_kvm support from EPEL branch

* Fri Nov 16 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-22
- Fix previous commit

* Fri Nov 16 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-21
- Backport commit 38f419f (configure: Fix CONFIG_QEMU_HELPERDIR generation,
  2012-10-17)

* Thu Nov 15 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-20
- Install qemu-bridge-helper as suid root
- Distribute a sample /etc/qemu/bridge.conf file

* Thu Nov  1 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-19
- Sync spice patches with upstream, minor bugfixes and set the qxl pci
  device revision to 4 by default, so that guests know they can use
  the new features

* Tue Oct 30 2012 Cole Robinson <crobinso@redhat.com> - 2:1.2.0-18
- Fix loading arm initrd if kernel is very large (bz #862766)
- Don't use reserved word 'function' in systemtap files (bz #870972)
- Drop assertion that was triggering when pausing guests w/ qxl (bz
  #870972)

* Sun Oct 28 2012 Cole Robinson <crobinso@redhat.com> - 2:1.2.0-17
- Pull patches queued for qemu 1.2.1

* Fri Oct 19 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-16
- add s390x KVM support
- distribute pre-built firmware or device trees for Alpha, Microblaze, S390
- add missing system targets
- add missing linux-user targets
- fix previous commit

* Thu Oct 18 2012 Dan Horák <dan[at]danny.cz> - 2:1.2.0-15
- fix build on non-kvm arches like s390(x)

* Wed Oct 17 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-14
- Change SLOF Requires for the new version number

* Thu Oct 11 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-13
- Add ppc support to kvm.modules (original patch by David Gibson)
- Replace x86only build with kvmonly build: add separate defines and
  conditionals for all packages, so that they can be chosen and
  renamed in kvmonly builds and so that qemu has the appropriate requires
- Automatically pick libfdt dependancy
- Add knob to disable spice+seccomp

* Fri Sep 28 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-12
- Call udevadm on post, fixing bug 860658

* Fri Sep 28 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-11
- Rebuild against latest spice-server and spice-protocol
- Fix non-seamless migration failing with vms with usb-redir devices,
  to allow boxes to load such vms from disk

* Tue Sep 25 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-10
- Sync Spice patchsets with upstream (rhbz#860238)
- Fix building with usbredir >= 0.5.2

* Thu Sep 20 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-9
- Sync USB and Spice patchsets with upstream

* Sun Sep 16 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.2.0-8
- Use 'global' instead of 'define', and underscore in definition name,
  n-v-r, and 'dist' tag of SLOF, all to fix RHBZ#855252.

* Fri Sep 14 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-4
- add versioned dependency from qemu-system-ppc to SLOF (BZ#855252)

* Wed Sep 12 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.2.0-3
- Fix RHBZ#853408 which causes libguestfs failure.

* Sat Sep  8 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-2
- Fix crash on (seamless) migration
- Sync usbredir live migration patches with upstream

* Fri Sep  7 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-1
- New upstream release 1.2.0 final
- Add support for Spice seamless migration
- Add support for Spice dynamic monitors
- Add support for usb-redir live migration

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 1.2.0-0.5.rc1
- Flip Requires: ceph >= foo to Conflicts: ceph < foo, so we pull in only the
  libraries which we need and not the rest of ceph which we don't.

* Tue Aug 28 2012 Cole Robinson <crobinso@redhat.com> 1.2.0-0.4.rc1
- Update to 1.2.0-rc1

* Mon Aug 20 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2-0.3.20120806git3e430569
- Backport Bonzini's vhost-net fix (RHBZ#848400).

* Tue Aug 14 2012 Cole Robinson <crobinso@redhat.com> - 1.2-0.2.20120806git3e430569
- Bump release number, previous build forgot but the dist bump helped us out

* Tue Aug 14 2012 Cole Robinson <crobinso@redhat.com> - 1.2-0.1.20120806git3e430569
- Revive qemu-system-{ppc*, sparc*} (bz 844502)
- Enable KVM support for all targets (bz 844503)

* Mon Aug 06 2012 Cole Robinson <crobinso@redhat.com> - 1.2-0.1.20120806git3e430569.fc18
- Update to git snapshot

* Sun Jul 29 2012 Cole Robinson <crobinso@redhat.com> - 1.1.1-1
- Upstream stable release 1.1.1
- Fix systemtap tapsets (bz 831763)
- Fix VNC audio tunnelling (bz 840653)
- Don't renable ksm on update (bz 815156)
- Bump usbredir dep (bz 812097)
- Fix RPM install error on non-virt machines (bz 660629)
- Obsolete openbios to fix upgrade dependency issues (bz 694802)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.1.0-8
- Re-diff previous patch so that it applies and actually apply it

* Tue Jul 10 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.1.0-7
- Add patch to fix default machine options.  This fixes libvirt
  detection of qemu.
- Back out patch 1 which conflicts.

* Fri Jul  6 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.1.0-5
- Fix qemu crashing (on an assert) whenever USB-2.0 isoc transfers are used

* Thu Jul  5 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.1.0-4
- Disable tests since they hang intermittently.
- Add kvmvapic.bin (replaces vapic.bin).
- Add cpus-x86_64.conf.  qemu now creates /etc/qemu/target-x86_64.conf
  as an empty file.
- Add qemu-icon.bmp.
- Add qemu-bridge-helper.
- Build and include virtfs-proxy-helper + man page (thanks Hans de Goede).

* Wed Jul  4 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.1.0-1
- New upstream release 1.1.0
- Drop about a 100 spice + USB patches, which are all upstream

* Mon Apr 23 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.0-17
- Fix install failure due to set -e (rhbz #815272)

* Mon Apr 23 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.0-16
- Fix kvm.modules to exit successfully on non-KVM capable systems (rhbz #814932)

* Thu Apr 19 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.0-15
- Add a couple of backported QXL/Spice bugfixes
- Add spice volume control patches

* Fri Apr 6 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.0-12
- Add back PPC and SPARC user emulators
- Update binfmt rules from upstream

* Mon Apr  2 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.0-11
- Some more USB bugfixes from upstream

* Thu Mar 29 2012 Eduardo Habkost <ehabkost@redhat.com> - 2:1.0-12
- Fix ExclusiveArch mistake that disabled all non-x86_64 builds on Fedora

* Wed Mar 28 2012 Eduardo Habkost <ehabkost@redhat.com> - 2:1.0-11
- Use --with variables for build-time settings

* Wed Mar 28 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-10
- Switch to use iPXE for netboot ROMs

* Thu Mar 22 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-9
- Remove O_NOATIME for 9p filesystems

* Mon Mar 19 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-8
- Move udev rules to /lib/udev/rules.d (rhbz #748207)

* Fri Mar  9 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.0-7
- Add a whole bunch of USB bugfixes from upstream

* Mon Feb 13 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-6
- Add many more missing BRs for misc QEMU features
- Enable running of test suite during build

* Tue Feb 07 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-5
- Add support for virtio-scsi

* Sun Feb  5 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.0-4
- Require updated ceph for latest librbd with rbd_flush symbol.

* Tue Jan 24 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-3
- Add support for vPMU
- e1000: bounds packet size against buffer size CVE-2012-0029

* Fri Jan 13 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-2
- Add patches for USB redirect bits
- Remove palcode-clipper, we don't build it

* Wed Jan 11 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-1
- Add patches from 1.0.1 queue

* Fri Dec 16 2011 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-1
- Update to qemu 1.0

* Tue Nov 15 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.1-3
- Enable spice for i686 users as well

* Thu Nov 03 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.1-2
- Fix POSTIN scriplet failure (#748281)

* Fri Oct 21 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.1-1
- Require seabios-bin >= 0.6.0-2 (#741992)
- Replace init scripts with systemd units (#741920)
- Update to 0.15.1 stable upstream
  
* Fri Oct 21 2011 Paul Moore <pmoore@redhat.com>
- Enable full relro and PIE (rhbz #738812)

* Wed Oct 12 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-6
- Add BR on ceph-devel to enable RBD block device

* Wed Oct  5 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-5
- Create a qemu-guest-agent sub-RPM for guest installation

* Tue Sep 13 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-4
- Enable DTrace tracing backend for SystemTAP (rhbz #737763)
- Enable build with curl (rhbz #737006)

* Thu Aug 18 2011 Hans de Goede <hdegoede@redhat.com> - 2:0.15.0-3
- Add missing BuildRequires: usbredir-devel, so that the usbredir code
  actually gets build

* Thu Aug 18 2011 Richard W.M. Jones <rjones@redhat.com> - 2:0.15.0-2
- Add upstream qemu patch 'Allow to leave type on default in -machine'
  (2645c6dcaf6ea2a51a3b6dfa407dd203004e4d11).

* Sun Aug 14 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-1
- Update to 0.15.0 stable release.

* Thu Aug 04 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-0.3.201108040af4922
- Update to 0.15.0-rc1 as we prepare for 0.15.0 release

* Thu Aug  4 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-0.3.2011072859fadcc
- Fix default accelerator for non-KVM builds (rhbz #724814)

* Thu Jul 28 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-0.1.2011072859fadcc
- Update to 0.15.0-rc0 as we prepare for 0.15.0 release

* Tue Jul 19 2011 Hans de Goede <hdegoede@redhat.com> - 2:0.15.0-0.2.20110718525e3df
- Add support usb redirection over the network, see:
  http://fedoraproject.org/wiki/Features/UsbNetworkRedirection
- Restore chardev flow control patches

* Mon Jul 18 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-0.1.20110718525e3df
- Update to git snapshot as we prepare for 0.15.0 release

* Wed Jun 22 2011 Richard W.M. Jones <rjones@redhat.com> - 2:0.14.0-9
- Add BR libattr-devel.  This caused the -fstype option to be disabled.
  https://www.redhat.com/archives/libvir-list/2011-June/thread.html#01017

* Mon May  2 2011 Hans de Goede <hdegoede@redhat.com> - 2:0.14.0-8
- Fix a bug in the spice flow control patches which breaks the tcp chardev

* Tue Mar 29 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-7
- Disable qemu-ppc and qemu-sparc packages (#679179)

* Mon Mar 28 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-6
- Spice fixes for flow control.

* Tue Mar 22 2011 Dan Horák <dan[at]danny.cz> - 2:0.14.0-5
- be more careful when removing the -g flag on s390

* Fri Mar 18 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-4
- Fix thinko on adding the most recent patches.

* Wed Mar 16 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-3
- Fix migration issue with vhost
- Fix qxl locking issues for spice

* Wed Mar 02 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-2
- Re-enable sparc and cris builds

* Thu Feb 24 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-1
- Update to 0.14.0 release

* Fri Feb 11 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-0.1.20110210git7aa8c46
- Update git snapshot
- Temporarily disable qemu-cris and qemu-sparc due to build errors (to be resolved shorly)

* Tue Feb 08 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-0.1.20110208git3593e6b
- Update to 0.14.0 rc git snapshot
- Add virtio-net to modules

* Wed Nov  3 2010 Daniel P. Berrange <berrange@redhat.com> - 2:0.13.0-2
- Revert previous change
- Make qemu-common own the /etc/qemu directory
- Add /etc/qemu/target-x86_64.conf to qemu-system-x86 regardless
  of host architecture.

* Wed Nov 03 2010 Dan Horák <dan[at]danny.cz> - 2:0.13.0-2
- Remove kvm config file on non-x86 arches (part of #639471)
- Own the /etc/qemu directory

* Mon Oct 18 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-1
- Update to 0.13.0 upstream release
- Fixes for vhost
- Fix mouse in certain guests (#636887)
- Fix issues with WinXP guest install (#579348)
- Resolve build issues with S390 (#639471)
- Fix Windows XP on Raw Devices (#631591)

* Tue Oct 05 2010 jkeating - 2:0.13.0-0.7.rc1.1
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.7.rc1
- Flip qxl pci id from unstable to stable (#634535)
- KSM Fixes from upstream (#558281)

* Tue Sep 14 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.6.rc1
- Move away from git snapshots as 0.13 is close to release
- Updates for spice 0.6

* Tue Aug 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.5.20100809git25fdf4a
- Fix typo in e1000 gpxe rom requires.
- Add links to newer vgabios

* Tue Aug 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.4.20100809git25fdf4a
- Disable spice on 32bit, it is not supported and buildreqs don't exist.

* Mon Aug 9 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.3.20100809git25fdf4a
- Updates from upstream towards 0.13 stable
- Fix requires on gpxe
- enable spice now that buildreqs are in the repository.
- ksmtrace has moved to a separate upstream package

* Tue Jul 27 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.2.20100727gitb81fe95
- add texinfo buildreq for manpages.

* Tue Jul 27 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.1.20100727gitb81fe95
- Update to 0.13.0 upstream snapshot
- ksm init fixes from upstream

* Tue Jul 20 2010 Dan Horák <dan[at]danny.cz> - 2:0.12.3-8
- Add avoid-llseek patch from upstream needed for building on s390(x)
- Don't use parallel make on s390(x)

* Tue Jun 22 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.3-7
- Add vvfat hardening patch from upstream (#605202)

* Fri Apr 23 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-6
- Change requires to the noarch seabios-bin
- Add ownership of docdir to qemu-common (#572110)
- Fix "Cannot boot from non-existent NIC" error when using virt-install (#577851)

* Thu Apr 15 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-5
- Update virtio console patches from upstream

* Thu Mar 11 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-4
- Detect cdrom via ioctl (#473154)
- re add increased buffer for USB control requests (#546483)

* Wed Mar 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-3
- Migration clear the fd in error cases (#518032)

* Tue Mar 09 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-2
- Allow builds --with x86only
- Add libaio-devel buildreq for aio support

* Fri Feb 26 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-1
- Update to 0.12.3 upstream
- vhost-net migration/restart fixes
- Add F-13 machine type
- virtio-serial fixes

* Tue Feb 09 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.2-6
- Add vhost net support.

* Thu Feb 04 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.2-5
- Avoid creating too large iovecs in multiwrite merge (#559717)
- Don't try to set max_kernel_pages during ksm init on newer kernels (#558281)
- Add logfile options for ksmtuned debug.

* Wed Jan 27 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.2-4
- Remove build dependency on iasl now that we have seabios

* Wed Jan 27 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.2-3
- Remove source target for 0.12.1.2

* Wed Jan 27 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.2-2
- Add virtio-console patches from upstream for the F13 VirtioSerial feature

* Mon Jan 25 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.2-1
- Update to 0.12.2 upstream

* Sun Jan 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.1.2-3
- Point to seabios instead of bochs, and add a requires for seabios

* Mon Jan  4 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.1.2-2
- Remove qcow2 virtio backing file patch

* Mon Jan  4 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.1.2-1
- Update to 0.12.1.2 upstream
- Remove patches included in upstream

* Fri Nov 20 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-12
- Fix a use-after-free crasher in the slirp code (#539583)
- Fix overflow in the parallels image format support (#533573)

* Wed Nov  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-11
- Temporarily disable preadv/pwritev support to fix data corruption (#526549)

* Tue Nov  3 2009 Justin M. Forbes <jforbes@redhat.com> - 2:0.11.0-10
- Default ksm and ksmtuned services on.

* Thu Oct 29 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-9
- Fix dropped packets with non-virtio NICs (#531419)

* Wed Oct 21 2009 Glauber Costa <gcosta@redhat.com> - 2:0.11.0-8
- Properly save kvm time registers (#524229)

* Mon Oct 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-7
- Fix potential segfault from too small MSR_COUNT (#528901)

* Fri Oct  9 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-6
- Fix fs errors with virtio and qcow2 backing file (#524734)
- Fix ksm initscript errors on kernel missing ksm (#527653)
- Add missing Requires(post): getent, useradd, groupadd (#527087)

* Tue Oct  6 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-5
- Add 'retune' verb to ksmtuned init script

* Mon Oct  5 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-4
- Use rtl8029 PXE rom for ne2k_pci, not ne (#526777)
- Also, replace the gpxe-roms-qemu pkg requires with file-based requires

* Thu Oct  1 2009 Justin M. Forbes <jmforbes@redhat.com> - 2:0.11.0-3
- Improve error reporting on file access (#524695)

* Mon Sep 28 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-2
- Fix pci hotplug to not exit if supplied an invalid NIC model (#524022)

* Mon Sep 28 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-1
- Update to 0.11.0 release
- Drop a couple of upstreamed patches

* Wed Sep 23 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-5
- Fix issue causing NIC hotplug confusion when no model is specified (#524022)

* Wed Sep 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-4
- Fix for KSM patch from Justin Forbes

* Wed Sep 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-3
- Add ksmtuned, also from Dan Kenigsberg
- Use %_initddir macro

* Wed Sep 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-2
- Add ksm control script from Dan Kenigsberg

* Mon Sep  7 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-1
- Update to qemu-kvm-0.11.0-rc2
- Drop upstreamed patches
- extboot install now fixed upstream
- Re-place TCG init fix (#516543) with the one gone upstream

* Mon Sep  7 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.10.rc1
- Fix MSI-X error handling on older kernels (#519787)

* Fri Sep  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.9.rc1
- Make pulseaudio the default audio backend (#519540, #495964, #496627)

* Thu Aug 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2:0.10.91-0.8.rc1
- Fix segfault when qemu-kvm is invoked inside a VM (#516543)

* Tue Aug 18 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.7.rc1
- Fix permissions on udev rules (#517571)

* Mon Aug 17 2009 Lubomir Rintel <lkundrak@v3.sk> - 2:0.10.91-0.6.rc1
- Allow blacklisting of kvm modules (#517866)

* Fri Aug  7 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.5.rc1
- Fix virtio_net with -net user (#516022)

* Tue Aug  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.4.rc1
- Update to qemu-kvm-0.11-rc1; no changes from rc1-rc0

* Tue Aug  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.3.rc1.rc0
- Fix extboot checksum (bug #514899)

* Fri Jul 31 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.2.rc1.rc0
- Add KSM support
- Require bochs-bios >= 2.3.8-0.8 for latest kvm bios updates

* Thu Jul 30 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.1.rc1.rc0
- Update to qemu-kvm-0.11.0-rc1-rc0
- This is a pre-release of the official -rc1
- A vista installer regression is blocking the official -rc1 release
- Drop qemu-prefer-sysfs-for-usb-host-devices.patch
- Drop qemu-fix-build-for-esd-audio.patch
- Drop qemu-slirp-Fix-guestfwd-for-incoming-data.patch
- Add patch to ensure extboot.bin is installed

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.10.50-14.kvm88
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Glauber Costa <glommer@redhat.com> - 2:0.10.50-13.kvm88
- Fix bug 513249, -net channel option is broken

* Thu Jul 16 2009 Daniel P. Berrange <berrange@redhat.com> - 2:0.10.50-12.kvm88
- Add 'qemu' user and group accounts
- Force disable xen until it can be made to build

* Thu Jul 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-11.kvm88
- Update to kvm-88, see http://www.linux-kvm.org/page/ChangeLog
- Package mutiboot.bin
- Update for how extboot is built
- Fix sf.net source URL
- Drop qemu-fix-ppc-softmmu-kvm-disabled-build.patch
- Drop qemu-fix-pcspk-build-with-kvm-disabled.patch
- Cherry-pick fix for esound support build failure

* Wed Jul 15 2009 Daniel Berrange <berrange@lettuce.camlab.fab.redhat.com> - 2:0.10.50-10.kvm87
- Add udev rules to make /dev/kvm world accessible & group=kvm (rhbz #497341)
- Create a kvm group if it doesn't exist (rhbz #346151)

* Tue Jul 07 2009 Glauber Costa <glommer@redhat.com> - 2:0.10.50-9.kvm87
- use pxe roms from gpxe, instead of etherboot package.

* Fri Jul  3 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-8.kvm87
- Prefer sysfs over usbfs for usb passthrough (#508326)

* Sat Jun 27 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-7.kvm87
- Update to kvm-87
- Drop upstreamed patches
- Cherry-pick new ppc build fix from upstream
- Work around broken linux-user build on ppc
- Fix hw/pcspk.c build with --disable-kvm
- Re-enable preadv()/pwritev() since #497429 is long since fixed
- Kill petalogix-s3adsp1800.dtb, since we don't ship the microblaze target

* Fri Jun  5 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-6.kvm86
- Fix 'kernel requires an x86-64 CPU' error
- BuildRequires ncurses-devel to enable '-curses' option (#504226)

* Wed Jun  3 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-5.kvm86
- Prevent locked cdrom eject - fixes hang at end of anaconda installs (#501412)
- Avoid harmless 'unhandled wrmsr' warnings (#499712)

* Thu May 21 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-4.kvm86
- Update to kvm-86 release
- ChangeLog here: http://marc.info/?l=kvm&m=124282885729710

* Fri May  1 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-3.kvm85
- Really provide qemu-kvm as a metapackage for comps

* Tue Apr 28 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-2.kvm85
- Provide qemu-kvm as a metapackage for comps

* Mon Apr 27 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-1.kvm85
- Update to qemu-kvm-devel-85
- kvm-85 is based on qemu development branch, currently version 0.10.50
- Include new qemu-io utility in qemu-img package
- Re-instate -help string for boot=on to fix virtio booting with libvirt
- Drop upstreamed patches
- Fix missing kernel/include/asm symlink in upstream tarball
- Fix target-arm build
- Fix build on ppc
- Disable preadv()/pwritev() until bug #497429 is fixed
- Kill more .kernelrelease uselessness
- Make non-kvm qemu build verbose

* Fri Apr 24 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-15
- Fix source numbering typos caused by make-release addition

* Thu Apr 23 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-14
- Improve instructions for generating the tarball

* Tue Apr 21 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-13
- Enable pulseaudio driver to fix qemu lockup at shutdown (#495964)

* Tue Apr 21 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-12
- Another qcow2 image corruption fix (#496642)

* Mon Apr 20 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-11
- Fix qcow2 image corruption (#496642)

* Sun Apr 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-10
- Run sysconfig.modules from %post on x86_64 too (#494739)

* Sun Apr 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-9
- Align VGA ROM to 4k boundary - fixes 'qemu-kvm -std vga' (#494376)

* Tue Apr  14 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-8
- Provide qemu-kvm conditional on the architecture.

* Thu Apr  9 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-7
- Add a much cleaner fix for vga segfault (#494002)

* Sun Apr  5 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-6
- Fixed qcow2 segfault creating disks over 2TB. #491943

* Fri Apr  3 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-5
- Fix vga segfault under kvm-autotest (#494002)
- Kill kernelrelease hack; it's not needed
- Build with "make V=1" for more verbose logs

* Thu Apr 02 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-4
- Support botting gpxe roms.

* Wed Apr 01 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-2
- added missing patch. love for CVS.

* Wed Apr 01 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-1
- Include debuginfo for qemu-img
- Do not require qemu-common for qemu-img
- Explicitly own each of the firmware files
- remove firmwares for ppc and sparc. They should be provided by an external package.
  Not that the packages exists for sparc in the secondary arch repo as noarch, but they
  don't automatically get into main repos. Unfortunately it's the best we can do right
  now.
- rollback a bit in time. Snapshot from avi's maint/2.6.30
  - this requires the sasl patches to come back.
  - with-patched-kernel comes back.

* Wed Mar 25 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-0.12.kvm20090323git
- BuildRequires pciutils-devel for device assignment (#492076)

* Mon Mar 23 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.11.kvm20090323git
- Update to snapshot kvm20090323.
- Removed patch2 (upstream).
- use upstream's new split package.
- --with-patched-kernel flag not needed anymore
- Tell how to get the sources.

* Wed Mar 18 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.10.kvm20090310git
- Added extboot to files list.

* Wed Mar 11 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.9.kvm20090310git
- Fix wrong reference to bochs bios.

* Wed Mar 11 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.8.kvm20090310git
- fix Obsolete/Provides pair
- Use kvm bios from bochs-bios package.
- Using RPM_OPT_FLAGS in configure
- Picked back audio-drv-list from kvm package

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.7.kvm20090310git
- modify ppc patch

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.6.kvm20090310git
- updated to kvm20090310git
- removed sasl patches (already in this release)

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.5.kvm20090303git
- kvm.modules were being wrongly mentioned at %%install.
- update description for the x86 system package to include kvm support
- build kvm's own bios. It is still necessary while kvm uses a slightly different
  irq routing mechanism

* Thu Mar 05 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.4.kvm20090303git
- seems Epoch does not go into the tags. So start back here.

* Thu Mar 05 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.1.kvm20090303git
- Use bochs-bios instead of bochs-bios-data
- It's official: upstream set on 0.10

* Thu Mar  5 2009 Daniel P. Berrange <berrange@redhat.com> - 2:0.9.2-0.2.kvm20090303git
- Added BSD to license list, since many files are covered by BSD

* Wed Mar 04 2009 Glauber Costa <glommer@redhat.com> - 0.9.2-0.1.kvm20090303git
- missing a dot. shame on me

* Wed Mar 04 2009 Glauber Costa <glommer@redhat.com> - 0.92-0.1.kvm20090303git
- Set Epoch to 2
- Set version to 0.92. It seems upstream keep changing minds here, so pick the lowest
- Provides KVM, Obsoletes KVM
- Only install qemu-kvm in ix86 and x86_64
- Remove pkgdesc macros, as they were generating bogus output for rpm -qi.
- fix ppc and ppc64 builds

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.3.kvm20090303git
- only execute post scripts for user package.
- added kvm tools.

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.2.kvm20090303git
- put kvm.modules into cvs

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.1.kvm20090303git
- Set Epoch to 1
- Build KVM (basic build, no tools yet)
- Set ppc in ExcludeArch. This is temporary, just to fix one issue at a time.
  ppc users (IBM ? ;-)) please wait a little bit.

* Tue Mar  3 2009 Daniel P. Berrange <berrange@redhat.com> - 1.0-0.5.svn6666
- Support VNC SASL authentication protocol
- Fix dep on bochs-bios-data

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.4.svn6666
- use bios from bochs-bios package.

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.3.svn6666
- use vgabios from vgabios package.

* Mon Mar 02 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.2.svn6666
- use pxe roms from etherboot package.

* Mon Mar 02 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.1.svn6666
- Updated to tip svn (release 6666). Featuring split packages for qemu.
  Unfortunately, still using binary blobs for the bioses.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 11 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.9.1-12
- Updated build patch. Closes Red Hat Bugzilla bug #465041.

* Wed Dec 31 2008 Dennis Gilmore <dennis@ausil.us> - 0.9.1-11
- add sparcv9 and sparc64 support

* Fri Jul 25 2008 Bill Nottingham <notting@redhat.com>
- Fix qemu-img summary (#456344)

* Wed Jun 25 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-10.fc10
- Rebuild for GNU TLS ABI change

* Wed Jun 11 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-9.fc10
- Remove bogus wildcard from files list (rhbz #450701)

* Sat May 17 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.9.1-8
- Register binary handlers also for shared libraries

* Mon May  5 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-7.fc10
- Fix text console PTYs to be in rawmode

* Sun Apr 27 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.9.1-6
- Register binary handler for SuperH-4 CPU

* Wed Mar 19 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-5.fc9
- Split qemu-img tool into sub-package for smaller footprint installs

* Wed Feb 27 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-4.fc9
- Fix block device checks for extendable disk formats (rhbz #435139)

* Sat Feb 23 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-3.fc9
- Fix block device extents check (rhbz #433560)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.1-2
- Autorebuild for GCC 4.3

* Tue Jan  8 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-1.fc9
- Updated to 0.9.1 release
- Fix license tag syntax
- Don't mark init script as a config file

* Wed Sep 26 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-5.fc8
- Fix rtl8139 checksum calculation for Vista (rhbz #308201)

* Tue Aug 28 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-4.fc8
- Fix debuginfo by passing -Wl,--build-id to linker

* Tue Aug 28 2007 David Woodhouse <dwmw2@infradead.org> 0.9.0-4
- Update licence
- Fix CDROM emulation (#253542)

* Tue Aug 28 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-3.fc8
- Added backport of VNC password auth, and TLS+x509 cert auth
- Switch to rtl8139 NIC by default for linkstate reporting
- Fix rtl8139 mmio region mappings with multiple NICs

* Sun Apr  1 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.0-2
- Fix direct loading of a linux kernel with -kernel & -initrd (bz 234681)
- Remove spurious execute bits from manpages (bz 222573)

* Tue Feb  6 2007 David Woodhouse <dwmw2@infradead.org> 0.9.0-1
- Update to 0.9.0

* Wed Jan 31 2007 David Woodhouse <dwmw2@infradead.org> 0.8.2-5
- Include licences

* Mon Nov 13 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.8.2-4
- Backport patch to make FC6 guests work by Kevin Kofler
  <Kevin@tigcc.ticalc.org> (bz 207843).

* Mon Sep 11 2006 David Woodhouse <dwmw2@infradead.org> 0.8.2-3
- Rebuild

* Thu Aug 24 2006 Matthias Saou <http://freshrpms.net/> 0.8.2-2
- Remove the target-list iteration for x86_64 since they all build again.
- Make gcc32 vs. gcc34 conditional on %%{fedora} to share the same spec for
  FC5 and FC6.

* Wed Aug 23 2006 Matthias Saou <http://freshrpms.net/> 0.8.2-1
- Update to 0.8.2 (#200065).
- Drop upstreamed syscall-macros patch2.
- Put correct scriplet dependencies.
- Force install mode for the init script to avoid umask problems.
- Add %%postun condrestart for changes to the init script to be applied if any.
- Update description with the latest "about" from the web page (more current).
- Update URL to qemu.org one like the Source.
- Add which build requirement.
- Don't include texi files in %%doc since we ship them in html.
- Switch to using gcc34 on devel, FC5 still has gcc32.
- Add kernheaders patch to fix linux/compiler.h inclusion.
- Add target-sparc patch to fix compiling on ppc (some int32 to float).

* Thu Jun  8 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-3
- More header abuse in modify_ldt(), change BuildRoot:

* Wed Jun  7 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-2
- Fix up kernel header abuse

* Tue May 30 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-1
- Update to 0.8.1

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-6
- Update linker script for PPC

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-5
- Just drop $RPM_OPT_FLAGS. They're too much of a PITA

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-4
- Disable stack-protector options which gcc 3.2 doesn't like

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-3
- Use -mcpu= instead of -mtune= on x86_64 too
- Disable SPARC targets on x86_64, because dyngen doesn't like fnegs

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-2
- Don't use -mtune=pentium4 on i386. GCC 3.2 doesn't like it

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-1
- Update to 0.8.0
- Resort to using compat-gcc-32
- Enable ALSA

* Mon May 16 2005 David Woodhouse <dwmw2@infradead.org> 0.7.0-2
- Proper fix for GCC 4 putting 'blr' or 'ret' in the middle of the function,
  for i386, x86_64 and PPC.

* Sat Apr 30 2005 David Woodhouse <dwmw2@infradead.org> 0.7.0-1
- Update to 0.7.0
- Fix dyngen for PPC functions which end in unconditional branch

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Feb 13 2005 David Woodhouse <dwmw2@infradead.org> 0.6.1-2
- Package cleanup

* Sun Nov 21 2004 David Woodhouse <dwmw2@redhat.com> 0.6.1-1
- Update to 0.6.1

* Tue Jul 20 2004 David Woodhouse <dwmw2@redhat.com> 0.6.0-2
- Compile fix from qemu CVS, add x86_64 host support

* Wed May 12 2004 David Woodhouse <dwmw2@redhat.com> 0.6.0-1
- Update to 0.6.0.

* Sat May 8 2004 David Woodhouse <dwmw2@redhat.com> 0.5.5-1
- Update to 0.5.5.

* Sun May 2 2004 David Woodhouse <dwmw2@redhat.com> 0.5.4-1
- Update to 0.5.4.

* Thu Apr 22 2004 David Woodhouse <dwmw2@redhat.com> 0.5.3-1
- Update to 0.5.3. Add init script.

* Thu Jul 17 2003 Jeff Johnson <jbj@redhat.com> 0.4.3-1
- Create.
