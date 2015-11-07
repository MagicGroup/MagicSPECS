# 必须覆盖 %%install 的默认行为，因为内核包是特殊的。
%global __spec_install_pre %{___build_pre}

Summary: The Linux kernel
Summary(zh_CN.UTF-8): Linux 内核

# 稳定版本的内核 released_kernel 必须设为 1。如果是 rc 或 git 版本，必须设为 0。
%global released_kernel 1

# 在 x86 上的进行内核模块签名，如果添加了其它架构确认好配置文件中也是匹配的设置。
# 为避免麻烦，Magic 默认均不签名。
%ifarch %{ix86} x86_64
%global signmodules 1
%global zipmodules 1
%else
%global signmodules 0
%global zipmodules 0
%endif

# 如果压缩模块
%if %{zipmodules}
%global zipsed -e 's/\.ko$/\.ko.xz/'
%endif

# 保存的 buildid，以便稍后定义它。
%if 0%{?buildid:1}
%global orig_buildid %{buildid}
%undefine buildid
%endif

###################################################################
# 如果要制作自己的内核 rpm 包，可以设置下面的定义，去除 # 号即可。
#
# % define buildid .local
###################################################################

# 上面的 buildid 也可以通过 rpmbuild 的命令行参数指定，方法是在参数中
# 添加 --define="buildid .whatever"。如果上面和命令中都指定了 buildid
# 那么两个就会一块使用。
%if 0%{?orig_buildid:1}
%if 0%{?buildid:1}
%global srpm_buildid %{buildid}
%define buildid %{srpm_buildid}%{orig_buildid}
%else
%define buildid %{orig_buildid}
%endif
%endif

# baserelease 是指 rpm 的 release 号，fedora_build 是一个意思。
# 不要用 rpmdev-bumpspec 自动更新版本号。
#
# 当更改了下面的 base_sublevel 或从 rc 版本到最终版本的内核，
# 把这个改成 1 (或是 0 然后使用 rpmdev-bumpspec)。
# scripts/rebase.sh 可以自动处理这个.
#
# 注意: baserelease 必须大于 0 否则你要切换到稳定内核时可能会出错。
#
# 对非稳定版的 rc 内核这个要添加到 rcX 或 gitX 标签后面，
# 比如这是 3 的话 release 就是 "0.rcX.gitX.3"
#
%global baserelease 6
%global fedora_build %{baserelease}

# base_sublevel 是开始打补丁的内核基础版本，对稳定版本内核基本就是内核
# 版本号的第 2 个数字，对非稳定版本一般是第 2 个数字减 1。
%define base_sublevel 18

## 如果这是稳定版本内核
%if 0%{?released_kernel}

# 是否有 -stable 的更新需要应用，一般是内核版本的第 3 个数字，
# 如果没有，就是 %{nil}
%define stable_update 23
# 是否是 -stable 的 RC 版本，Magic 一般不使用。
%define stable_rc 0
# 设置 rpm 包的版本号
# 如果是 -stable 更新版本
%if 0%{?stable_update}
%define stablerev %{stable_update}
%define stable_base %{stable_update}
%if 0%{?stable_rc}
# 如果是 RC 版本，需要减 1
%define stable_base %(echo $((%{stable_update} - 1)))
%endif
%endif
# 目前用 3.x 的内核
%define rpmversion 3.%{base_sublevel}.%{stable_update}

## 如果是非稳定版本内核 ##
%else
# 下一个上游发布的 sublevel，就是第 3 个数字，需要在现有上加 1。
%define upstream_sublevel %(echo $((%{base_sublevel} + 1)))
# rc 快照版本
%define rcrev 0
# git 快照版本
%define gitrev 100
# 设置 rpm 包版本号
%define rpmversion 3.%{upstream_sublevel}.0
%endif
# 注意：上面的 rcrev 和 gitrev 的值是在下面的 Patch00 和 Patch01 中自动定义的。

# What parts do we want to build?  We must build at least one kernel.
# These are the kernels that are built IF the architecture allows it.
# All should default to 1 (enabled) and be flipped to 0 (disabled)
# by later arch-specific checks.

# 我们想编译哪一部分？我们必须编译至少一个内核，其它的内核如果架构允许
# 的话，也可以编译。所有选项的默认值都是 1，然后在稍后的架构检查中切换
# 为 0。

# 下面的构建选项默认都是启用的。
# 使用 --without <opt> 或修改值为 0 可以禁用它们。
#
# 标准内核
%define with_up        %{?_without_up:        0} %{?!_without_up:        1}
# kernel-PAE (支持大内存的内核，仅在 i686 和 ARM 架构下可用)
%define with_pae       %{?_without_pae:       0} %{?!_without_pae:       1}
# kernel-debug (调试内核)
%define with_debug     %{?_without_debug:     0} %{?!_without_debug:     1}
# kernel-doc (内核的文档)
%define with_doc       %{?_without_doc:       0} %{?!_without_doc:       1}
# kernel-headers (内核的头文件)
%define with_headers   %{?_without_headers:   0} %{?!_without_headers:   1}
# perf 
%define with_perf      %{?_without_perf:      0} %{?!_without_perf:      1}
# tools (内核的工具)
%define with_tools     %{?_without_tools:     0} %{?!_without_tools:     1}
# kernel-debuginfo (内核的调试信息)
%define with_debuginfo %{?_without_debuginfo: 0} %{?!_without_debuginfo: 1}
# kernel-bootwrapper (从内核和 initrd 中创建 zImages)
%define with_bootwrapper %{?_without_bootwrapper: 0} %{?!_without_bootwrapper: 1}
# Want to build a the vsdo directories installed
# 这个不知道是什么意思。
%define with_vdso_install %{?_without_vdso_install: 0} %{?!_without_vdso_install: 1}
#
# 用户友好的一次性内核构建选项。
#
# 只编译基本内核 (--with baseonly)：
%define with_baseonly  %{?_with_baseonly:     1} %{?!_with_baseonly:     0}
# 只编译 pae 内核 (--with paeonly):
%define with_paeonly   %{?_with_paeonly:      1} %{?!_with_paeonly:      0}
# 只编译调试内核 (--with dbgonly):
%define with_dbgonly   %{?_with_dbgonly:      1} %{?!_with_dbgonly:      0}
#
# should we do C=1 builds with sparse
# 这个不知道是什么意思
%define with_sparse    %{?_with_sparse:       1} %{?!_with_sparse:       0}
#
# 是否需要交叉编译?
%define with_cross    %{?_with_cross:         1} %{?!_with_cross:        0}

# 在 rawhide 上编译稳定版本内核
%define with_release   %{?_with_release:      1} %{?!_with_release:      0}

# 设置 debugbuildsenabled 为 1 可以构建单独的调试内核。
# 设为 0 则所有内核均是调试内核。
# 也可以查看 'make debug' 和 'make release'。
%define debugbuildsenabled 1

# 是否编译一个没有任何上游补丁的 vanilla 内核。
%define with_vanilla %{?_with_vanilla: 1} %{?!_with_vanilla: 0}

# 打包 kernel-doc 包，但是即使不成功也不会让内核打包失败。
# 这里是 "true" 意思是继续编译，而 "false" 意思是打包失败。
# 如果是稳定版本，则打包失败，其它情况下则继续打包。
%if 0%{?released_kernel}
%define doc_build_fail false
%else
%define doc_build_fail true
%endif

# 是否跳过文档打包，设为 1 则跳过。
%define rawhide_skip_docs 0
%if 0%{?rawhide_skip_docs}
%define with_doc 0
%define doc_build_fail true
%endif

# pkg_release 就是rpm 包 Release 字段
# 如果是稳定版本内核
%if 0%{?released_kernel}
# 如果是稳定版本的 rc 内核
%if 0%{?stable_rc}
# rc 标签
%define stable_rctag .rc%{stable_rc}
# 整个的 Release ，以 0 开头
%define pkg_release 0%{stable_rctag}.%{fedora_build}%{?buildid}%{?dist}
%else
# 普通稳定内核的 Release。
%define pkg_release %{fedora_build}%{?buildid}%{?dist}
%endif

%else
# 非版本稳定内核
%if 0%{?rcrev}
# rc 标签，如果有则定义
%define rctag .rc%rcrev
%else
# rc 标签没有，则定义成 .rc0
%define rctag .rc0
%endif
%if 0%{?gitrev}
# git 标签，如果有则定义
%define gittag .git%gitrev
%else
# git 标签如果没有，则定义成 .git0
%define gittag .git0
%endif
# 整个的 Release ，以 0 开头。
%define pkg_release 0%{?rctag}%{?gittag}.%{fedora_build}%{?buildid}%{?dist}

%endif

# 内核包的基本版本，Magic 现在用 3
%define kversion 3.%{base_sublevel}

# make 的目标，默认是 bzImage，详情请 Google。
%define make_target bzImage
%define image_install_path boot

# 定义内核真正的版本，即 lib/modules 下的目录
%define KVERREL %{version}-%{release}.%{_target_cpu}
# 应该是定义架构相关的一些东西
%define hdrarch %_target_cpu
%define asmarch %_target_cpu

# 如果设为 1，则不打补丁
%if 0%{!?nopatches:1}
%define nopatches 0
%endif

# 如果编译 vanilla 内核，则不打补丁
%if %{with_vanilla}
%define nopatches 1
%endif

# 如果不打补丁，则定义下面的变量
%if %{nopatches}
%define with_bootwrapper 0
%define variant -vanilla
%endif


# 如果没有允许构建调试内核，则不打包调试内核包
%if !%{debugbuildsenabled}
%define with_debug 0
%endif

# 如果不构建调试信息包，则不打包调试信息包
%if !%{with_debuginfo}
%define _enable_debug_packages 0
%endif
# 定义调试信息目录。
%define debuginfodir /usr/lib/debug

# PAE 内核只可在 i686 和 ARMv7 架构上启用。
%ifnarch i686 armv7hl
%define with_pae 0
%endif

# 只编译基本内核
%if %{with_baseonly}
%define with_pae 0
%define with_debug 0
%endif

# 只编译 PAE 内核
%if %{with_paeonly}
%define with_up 0
%define with_debug 0
%endif

# 只编译调试内核
%if %{with_dbgonly}
# 如果允许了调试内核
%if %{debugbuildsenabled}
%define with_up 0
%endif
%define with_pae 0
%define with_tools 0
%define with_perf 0
%endif

%define all_x86 i386 i686

%if %{with_vdso_install}
# 这些架构安装到 vdso/ 目录。
%define vdso_arches %{all_x86} x86_64 ppc ppc64 ppc64p7 s390 s390x
%endif

# 下面重设默认值

# 除了 i686 和 x86_64 其它架构都不构建调试内核包。
%ifnarch i686 x86_64
%define with_debug 0
%endif

# 不编译 noarch 内核和头文件（这个好像是显然的）
%ifarch noarch
%define with_up 0
%define with_headers 0
%define with_tools 0
%define with_perf 0
%define all_arch_configs kernel-%{version}-*.config
%endif

# bootwrapper 只在 ppc 架构下可用
# sparse 也是。
%ifnarch %{power64}
%define with_bootwrapper 0
%define with_sparse 0
%endif

# 单独的架构调整

# i386 和 i686 下
%ifarch %{all_x86}
%define asmarch x86
%define hdrarch i386
%define pae PAE
%define all_arch_configs kernel-%{version}-i?86*.config
%define kernel_image arch/x86/boot/bzImage
%endif

# x86_64 下
%ifarch x86_64
%define asmarch x86
%define all_arch_configs kernel-%{version}-x86_64*.config
%define kernel_image arch/x86/boot/bzImage
%endif

# ppc 架构下
%ifarch %{power64}
%define asmarch powerpc
%define hdrarch powerpc
%define make_target vmlinux
%define kernel_image vmlinux
%define kernel_image_elf 1
%ifarch ppc64 ppc64p7
%define all_arch_configs kernel-%{version}-ppc64*.config
%endif
%ifarch ppc64le
%define all_arch_configs kernel-%{version}-ppc64le.config
%endif
%endif

# s390x 架构下
%ifarch s390x
%define asmarch s390
%define hdrarch s390
%define all_arch_configs kernel-%{version}-s390x.config
%define make_target image
%define kernel_image arch/s390/boot/image
%define with_tools 0
%endif

# arm 架构下
%ifarch %{arm}
%define all_arch_configs kernel-%{version}-arm*.config
%define asmarch arm
%define hdrarch arm
%define pae lpae
%define make_target bzImage
%define kernel_image arch/arm/boot/zImage
# http://lists.infradead.org/pipermail/linux-arm-kernel/2012-March/091404.html
%define kernel_mflags KALLSYMS_EXTRA_PASS=1
# we only build headers/perf/tools on the base arm arches
# just like we used to only build them on i386 for x86
%ifnarch armv7hl
%define with_headers 0
%define with_perf 0
%define with_tools 0
%endif
%endif

# aarch64 架构下。
%ifarch aarch64
%define all_arch_configs kernel-%{version}-aarch64*.config
%define asmarch arm64
%define hdrarch arm64
%define make_target Image.gz
%define kernel_image arch/arm64/boot/Image.gz
%endif

# mips64el 架构下
# 龙芯用，感觉应该写一个 mips 架构的
%ifarch mips64el
%define asmarch mips
%define hdrarch mips
%define all_arch_configs kernel-%{version}-mips64el*.config
%define make_target vmlinuz
%define kernel_image vmlinuz
# 这个是必须的么？
%define kernel_image_elf 1
%define with_headers 1
%endif


# Should make listnewconfig fail if there's config options
# printed out?

# 如果有新的配置选项，make listnewconfig 是否失败。
# 如果不打补丁，则不失败，否则失败，需要修改 config 文件。
%if %{nopatches}
%define listnewconfig_fail 0
%else
%define listnewconfig_fail 1
%endif

# 如果需要临时排除一些架构，请从下面的 %%nobuildarches 中设置
# 不要设置 ExclusiveArch 字段。

# 下面的架构我们只编译内核的头文件包...
%define nobuildarches i386 s390

%ifarch %nobuildarches
%define with_up 0
%define with_smp 0
%define with_pae 0
%define with_debuginfo 0
%define with_perf 0
%define with_tools 0
%define _enable_debug_packages 0
%endif

# pae 包是否打包调试内核，默认和 with_debug 一致
%define with_pae_debug 0
%if %{with_pae}
%define with_pae_debug %{with_debug}
%endif


# 编译工具和 cpupower 的架构
%define cpupowerarchs %{ix86} x86_64 %{power64}  %{arm} mips64el


#
# 内核包安装之前需要安装的包，因为 %%post 的脚本使用它们。
#
%define kernel_prereq  fileutils, systemd >= 203-2
%define initrd_prereq  dracut >= 027


# 以下是 spec 的主休内核
Name: kernel%{?variant}
Group: System Environment/Kernel
Group(zh_CN.UTF-8): 系统环境/内核
License: GPLv2 and Redistributable, no modification permitted
URL: http://www.kernel.org/
Version: 3.18.21
#Release: %{pkg_release}
Release: 2%{?dist}
# DO NOT CHANGE THE 'ExclusiveArch' LINE TO TEMPORARILY EXCLUDE AN ARCHITECTURE BUILD.
# SET %%nobuildarches (ABOVE) INSTEAD
# 不要更改下面一行，通过设置 %%nobuildarches (在上面) 来代替
ExclusiveArch: noarch %{all_x86} x86_64 ppc ppc64 ppc64p7 s390 s390x %{arm} mips64el
ExclusiveOS: Linux
%ifnarch %{nobuildarches}
Requires: kernel-core-uname-r = %{KVERREL}%{?variant}
Requires: kernel-modules-uname-r = %{KVERREL}%{?variant}
%endif

#
# 下面是内核编译需要的包。
#
BuildRequires: kmod, patch, bash, sh-utils, tar
BuildRequires: bzip2, xz, findutils, gzip, m4, perl, perl-Carp, make, diffutils, gawk
BuildRequires: gcc, binutils, magic-rpm-config, hmaccalc
BuildRequires: net-tools, hostname, bc
%if %{with_sparse}
BuildRequires: sparse
%endif
%if %{with_perf}
BuildRequires: elfutils-devel zlib-devel binutils-devel newt-devel python-devel perl(ExtUtils::Embed) bison flex
%ifnarch s390 s390x %{arm}
BuildRequires: numactl-devel
%endif
%endif
%if %{with_tools}
BuildRequires: pciutils-devel gettext ncurses-devel
%endif
BuildConflicts: rhbuildsys(DiskFree) < 500Mb
%if %{with_debuginfo}
BuildRequires: rpm-build, elfutils
%define debuginfo_args --strict-build-id -r
%endif

%if %{signmodules}
BuildRequires: openssl
BuildRequires: pesign >= 0.10-4
%endif

%if %{with_cross}
BuildRequires: binutils-%{_build_arch}-linux-gnu, gcc-%{_build_arch}-linux-gnu
%define cross_opts CROSS_COMPILE=%{_build_arch}-linux-gnu-
%endif

Source0: ftp://ftp.kernel.org/pub/linux/kernel/v3.0/linux-%{kversion}.tar.xz

Source10: perf-man-%{kversion}.tar.gz
Source11: x509.genkey

# 这是合并 config 用的脚本
Source15: merge.pl
Source16: mod-extra.list
Source17: mod-extra.sh
Source18: mod-sign.sh
Source90: filter-x86_64.sh
Source91: filter-armv7hl.sh
Source92: filter-i686.sh
Source93: filter-aarch64.sh
Source95: filter-ppc64.sh
Source96: filter-ppc64le.sh
Source97: filter-s390x.sh
Source98: filter-ppc64p7.sh
Source99: filter-modules.sh
Source89: filter-mips64el.sh
%define modsign_cmd %{SOURCE18}

# 各个架构的配置
Source19: Makefile.release
Source20: Makefile.config
Source21: config-debug
Source22: config-nodebug
Source23: config-generic
Source24: config-no-extra

Source30: config-x86-generic
Source31: config-i686-PAE
Source32: config-x86-32-generic

Source40: config-x86_64-generic

Source50: config-powerpc-generic
Source51: config-powerpc64-generic
Source53: config-powerpc64
Source54: config-powerpc64p7
Source55: config-powerpc64le

Source70: config-s390x

Source100: config-arm-generic

# Unified ARM kernels
Source101: config-armv7-generic
Source102: config-armv7
Source103: config-armv7-lpae

Source110: config-arm64

Source201: config-mips64el

# 这个文件在官方内核来说一般是空的，如果你定义一些选项重新编译，可以使用这个文件。
Source1000: config-local

# 内核工具包用的文件。 
Source2000: cpupower.service
Source2001: cpupower.config

# 这里的是 Linux 官方内核源码树上的补丁.

# 稳定内核用的
%if 0%{?stable_update}
%if 0%{?stable_base}
%define    stable_patch_00  patch-3.%{base_sublevel}.%{stable_base}.xz
Patch00: https://www.kernel.org/pub/linux/kernel/v3.x/%{stable_patch_00}
%endif
%if 0%{?stable_rc}
%define    stable_patch_01  patch-3.%{base_sublevel}.%{stable_update}-rc%{stable_rc}.xz
Patch01: %{stable_patch_01}
%endif

# 不稳定内核用的，rcrev 和 gitrev 的值从这里自动定义，Magic 一般不使用。
%else
%if 0%{?rcrev}
Patch00: patch-3.%{upstream_sublevel}-rc%{rcrev}.xz
%if 0%{?gitrev}
Patch01: patch-3.%{upstream_sublevel}-rc%{rcrev}-git%{gitrev}.xz
%endif
%else
# pre-{base_sublevel+1}-rc1 case
%if 0%{?gitrev}
Patch00: patch-3.%{base_sublevel}-git%{gitrev}.xz
%endif
%endif
%endif

# -vanilla 需要的编译补丁，正常情况下是空的。
Patch04: compile-fixes.patch

# 调整 build ID 魔数，即使在 -vanilla 内核。
Patch05: kbuild-AFTER_LINK.patch

%if !%{nopatches}

# 回退，一般是空的。
Patch09: upstream-reverts.patch

# 单独的补丁。

Patch450: input-kill-stupid-messages.patch
Patch452: no-pcspkr-modalias.patch

Patch470: die-floppy-die.patch

Patch500: Revert-Revert-ACPI-video-change-acpi-video-brightnes.patch

Patch510: input-silence-i8042-noise.patch
Patch530: silence-fbcon-logo.patch

Patch600: lib-cpumask-Make-CPUMASK_OFFSTACK-usable-without-deb.patch

#rhbz 1126580
Patch601: Kbuild-Add-an-option-to-enable-GCC-VTA.patch

Patch800: crash-driver.patch

# crypto/

# secure boot
Patch1000: Add-secure_modules-call.patch
Patch1001: PCI-Lock-down-BAR-access-when-module-security-is-ena.patch
Patch1002: x86-Lock-down-IO-port-access-when-module-security-is.patch
Patch1003: ACPI-Limit-access-to-custom_method.patch
Patch1004: asus-wmi-Restrict-debugfs-interface-when-module-load.patch
Patch1005: Restrict-dev-mem-and-dev-kmem-when-module-loading-is.patch
Patch1006: acpi-Ignore-acpi_rsdp-kernel-parameter-when-module-l.patch
Patch1007: kexec-Disable-at-runtime-if-the-kernel-enforces-modu.patch
Patch1008: x86-Restrict-MSR-access-when-module-loading-is-restr.patch
Patch1009: Add-option-to-automatically-enforce-module-signature.patch
Patch1010: efi-Disable-secure-boot-if-shim-is-in-insecure-mode.patch
Patch1011: efi-Make-EFI_SECURE_BOOT_SIG_ENFORCE-depend-on-EFI.patch
Patch1012: efi-Add-EFI_SECURE_BOOT-bit.patch
Patch1013: hibernate-Disable-in-a-signed-modules-environment.patch

Patch1014: Add-EFI-signature-data-types.patch
Patch1015: Add-an-EFI-signature-blob-parser-and-key-loader.patch
Patch1016: KEYS-Add-a-system-blacklist-keyring.patch
Patch1017: MODSIGN-Import-certificates-from-UEFI-Secure-Boot.patch
Patch1018: MODSIGN-Support-not-importing-certs-from-db.patch

Patch1019: Add-sysrq-option-to-disable-secure-boot-mode.patch

# virt + ksm patches

# DRM

# nouveau + drm fixes
# intel drm is all merged upstream
Patch1826: drm-i915-tame-the-chattermouth-v2.patch
Patch1827: drm-i915-Disable-verbose-state-checks.patch

# Quiet boot fixes

# fs fixes

# NFSv4

# patches headed upstream
Patch12016: disable-i8042-check-on-apple-mac.patch

Patch14000: hibernate-freeze-filesystems.patch

Patch14010: lis3-improve-handling-of-null-rate.patch

Patch15000: watchdog-Disable-watchdog-on-virtual-machines.patch

# PPC

# ARM64

# ARMv7
Patch21020: ARM-tegra-usb-no-reset.patch
Patch21021: arm-dts-am335x-boneblack-lcdc-add-panel-info.patch
Patch21022: arm-dts-am335x-boneblack-add-cpu0-opp-points.patch
Patch21023: arm-dts-am335x-bone-common-enable-and-use-i2c2.patch
Patch21024: arm-dts-am335x-bone-common-setup-default-pinmux-http.patch
Patch21025: arm-dts-am335x-bone-common-add-uart2_pins-uart4_pins.patch
Patch21026: pinctrl-pinctrl-single-must-be-initialized-early.patch

Patch21028: arm-i.MX6-Utilite-device-dtb.patch
Patch21029: arm-dts-sun7i-bananapi.patch

Patch21100: arm-highbank-l2-reverts.patch

#rhbz 754518
Patch21235: scsi-sd_revalidate_disk-prevent-NULL-ptr-deref.patch

# https://fedoraproject.org/wiki/Features/Checkpoint_Restore
Patch21242: criu-no-expert.patch

#rhbz 892811
Patch21247: ath9k-rx-dma-stop-check.patch

Patch22000: weird-root-dentry-name-debug.patch

# Patch series from Hans for various backlight and platform driver fixes
Patch26002: samsung-laptop-Add-broken-acpi-video-quirk-for-NC210.patch

#rhbz 1089731
Patch26058: asus-nb-wmi-Add-wapf4-quirk-for-the-X550VB.patch

#rhbz 1173806
Patch26101: powerpc-powernv-force-all-CPUs-to-be-bootable.patch

#rhbz 1163927
Patch26121: Set-UID-in-sess_auth_rawntlmssp_authenticate-too.patch


#rhbz 1163574
Patch26130: acpi-video-Add-disable_native_backlight-quirk-for-De.patch
#rhbz 1094948
Patch26131: acpi-video-Add-disable_native_backlight-quirk-for-Sa.patch

# git clone ssh://git.fedorahosted.org/git/kernel-arm64.git, git diff master...devel
Patch30000: kernel-arm64.patch

# Fix for big-endian arches, already upstream
Patch30001: mpssd-x86-only.patch

#rhbz 1186097
Patch30004: acpi-video-add-disable_native_backlight_quirk_for_samsung_510r.patch

#CVE-XXXX-XXXX rhbz 1189864 1192079
Patch26136: vhost-scsi-potential-memory-corruption.patch

#CVE-2015-0275 rhbz 1193907 1195178
Patch26138: ext4-Allocate-entire-range-in-zero-range.patch

#fbcondecor
Patch50000: 4200_fbcondecor-3.16.patch

#utf8
Patch50001: 3.18.20-utf8.diff

# fs fixes
# aufs
Patch3001: aufs001.patch
Patch3002: aufs3-base.patch
Patch3003: aufs3-kbuild.patch
Patch3004: aufs3-loopback.patch
Patch3005: aufs3-mmap.patch
Patch3006: aufs3-standalone.patch

# 龙芯用补丁

# END OF PATCH DEFINITIONS
%endif

BuildRoot: %{_tmppath}/kernel-%{KVERREL}-root

%description
The kernel meta package

%description -l zh_CN.UTF-8
内核元包。

#
# 下面的宏定义了内核包的 requires, provides, conflicts, obsoletes。
#	%%kernel_reqprovconf <subpackage>
# 任何 kernel_<subpackage>_conflicts 和 kernel_<subpackage>_obsoletes 
# 宏都使用了上面的定义.
#
%define kernel_reqprovconf \
Provides: kernel = %{rpmversion}-%{pkg_release}\
Provides: kernel-%{_target_cpu} = %{rpmversion}-%{pkg_release}%{?1:+%{1}}\
Provides: kernel-drm-nouveau = 16\
Provides: kernel-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
Requires(pre): %{kernel_prereq}\
Requires(pre): %{initrd_prereq}\
Requires(pre): linux-firmware >= 20130724-29.git31f6b30\
Requires(preun): systemd >= 200\
Conflicts: xorg-x11-drv-vmmouse < 13.0.99\
%{expand:%%{?kernel%{?1:_%{1}}_conflicts:Conflicts: %%{kernel%{?1:_%{1}}_conflicts}}}\
%{expand:%%{?kernel%{?1:_%{1}}_obsoletes:Obsoletes: %%{kernel%{?1:_%{1}}_obsoletes}}}\
%{expand:%%{?kernel%{?1:_%{1}}_provides:Provides: %%{kernel%{?1:_%{1}}_provides}}}\
# 我们不能让 RPM 来自动处理依赖关系 \
# 因为有些来自模块头文件的 Perl 依赖 \
# 并不是内核功能所必须的。\
AutoReq: no\
AutoProv: yes\
%{nil}

%package headers
Summary: Header files for the Linux kernel for use by glibc
Summary(zh_CN.UTF-8): glibc 使用的来自内核的头文件
Group: Development/System
Group(zh_CN.UTF-8): 开发/系统
Obsoletes: glibc-kernheaders < 3.0-46
Provides: glibc-kernheaders = 3.0-46
%if "0%{?variant}"
Obsoletes: kernel-headers < %{rpmversion}-%{pkg_release}
Provides: kernel-headers = %{rpmversion}-%{pkg_release}
%endif
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.
%description headers -l zh_CN.UTF-8 
这个包包含了在 Linux 内核和用户空间的库和程序间指定接口的 C 头文件。
编译大部分标准程序和重编译 glibc 均需要使用这里定义的结构体和常量。

%package bootwrapper
Summary: Boot wrapper files for generating combined kernel + initrd images
Summary(zh_CN.UTF-8): 引导包装文件生成组合核+ initrd映像
Group: Development/System
Group(zh_CN.UTF-8): 开发/系统
Requires: gzip binutils
%description bootwrapper
Kernel-bootwrapper contains the wrapper code which makes bootable "zImage"
files combining both kernel and initial ramdisk.
%description bootwrapper -l zh_CN.UTF-8
引导包装文件生成组合核+ initrd映像。

%package debuginfo-common-%{_target_cpu}
Summary: Kernel source files used by %{name}-debuginfo packages
Summary(zh_CN.UTF-8): %{name}-debuginfo 包使用的内核源码文件
Group: Development/Debug
Group(zh_CN.UTF-8): 开发/调试器
%description debuginfo-common-%{_target_cpu}
This package is required by %{name}-debuginfo subpackages.
It provides the kernel source files common to all builds.
%description debuginfo-common-%{_target_cpu} -l zh_CN.UTF-8
%{name}-debuginfo 包使用的内核源码文件。

%if %{with_perf}
%package -n perf
Summary: Performance monitoring for the Linux kernel
Summary(zh_CN.UTF-8): Linux 内核的性能监视程序
Group: Development/System
Group(zh_CN.UTF-8): 开发/系统
License: GPLv2
%description -n perf
This package contains the perf tool, which enables performance monitoring
of the Linux kernel.
%description -n perf -l zh_CN.UTF-8
Linux 内核的性能监视程序。

%package -n perf-debuginfo
Summary: Debug information for package perf
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description -n perf-debuginfo
This package provides debug information for the perf package.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
# 注意这个宏只在 .build-id 链接匹配的情况下才工作。
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '.*%%{_bindir}/perf(\.debug)?|.*%%{_libexecdir}/perf-core/.*|.*%%{_libdir}/traceevent/plugins/.*|XXX' -o perf-debuginfo.list}

%package -n python-perf
Summary: Python bindings for apps which will manipulate perf events
Summary(zh_CN.UTF-8): 处理 perl 事件的 Python 绑定
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
%description -n python-perf
The python-perf package contains a module that permits applications
written in the Python programming language to use the interface
to manipulate perf events.
%description -n python-perf -l zh_CN.UTF-8
处理 perl 事件的 Python 绑定。

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%package -n python-perf-debuginfo
Summary: Debug information for package perf python bindings
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description -n python-perf-debuginfo
This package provides debug information for the perf python bindings.

# python_sitearch 宏应该已经在上面定义了。
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '.*%%{python_sitearch}/perf.so(\.debug)?|XXX' -o python-perf-debuginfo.list}


%endif # with_perf

%if %{with_tools}
%package -n kernel-tools
Summary: Assortment of tools for the Linux kernel
Summary(zh_CN.UTF-8): Linux 内核的一些工具
Group: Development/System
Group(zh_CN.UTF-8): 开发/系统
License: GPLv2
Provides:  cpupowerutils = 1:009-0.6.p1
Obsoletes: cpupowerutils < 1:009-0.6.p1
Provides:  cpufreq-utils = 1:009-0.6.p1
Provides:  cpufrequtils = 1:009-0.6.p1
Obsoletes: cpufreq-utils < 1:009-0.6.p1
Obsoletes: cpufrequtils < 1:009-0.6.p1
Obsoletes: cpuspeed < 1:1.5-16
Requires: kernel-tools-libs = %{version}-%{release}
%description -n kernel-tools
This package contains the tools/ directory from the kernel source
and the supporting documentation.
%description -n kernel-tools -l zh_CN.UTF-8
这个包包含了内核的一些工具。

%package -n kernel-tools-libs
Summary: Libraries for the kernels-tools
Summary(zh_CN.UTF-8): kernel-tools 包使用的运行库
Group: Development/System
Group(zh_CN.UTF-8): 开发/系统
License: GPLv2
%description -n kernel-tools-libs
This package contains the libraries built from the tools/ directory
from the kernel source.
%description -n kernel-tools-libs -l zh_CN.UTF-8
kernel-tools 包使用的运行库。

%package -n kernel-tools-libs-devel
Summary: Assortment of tools for the Linux kernel
Summary(zh_CN.UTF-8): kernel-tools 包的开发包
Group: Development/System
Group(zh_CN.UTF-8): 开发/系统
License: GPLv2
Requires: kernel-tools = %{version}-%{release}
Provides:  cpupowerutils-devel = 1:009-0.6.p1
Obsoletes: cpupowerutils-devel < 1:009-0.6.p1
Requires: kernel-tools-libs = %{version}-%{release}
Provides: kernel-tools-devel
%description -n kernel-tools-libs-devel
This package contains the development files for the tools/ directory from
the kernel source.
%description  -n kernel-tools-libs-devel -l zh_CN.UTF-8
kernel-tools 包的开发包。

%package -n kernel-tools-debuginfo
Summary: Debug information for package kernel-tools
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description -n kernel-tools-debuginfo
This package provides debug information for package kernel-tools.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
# 这个同上。
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '.*%%{_bindir}/centrino-decode(\.debug)?|.*%%{_bindir}/powernow-k8-decode(\.debug)?|.*%%{_bindir}/cpupower(\.debug)?|.*%%{_libdir}/libcpupower.*|.*%%{_bindir}/turbostat(\.debug)?|.*%%{_bindir}/x86_energy_perf_policy(\.debug)?|.*%%{_bindir}/tmon(\.debug)?|XXX' -o kernel-tools-debuginfo.list}

%endif # with_tools

#
#	%%kernel_debuginfo_package <subpackage>
#
# 这个宏创建 kernel-<subpackage>-debuginfo 包。

%define kernel_debuginfo_package() \
%package %{?1:%{1}-}debuginfo\
Summary: Debug information for package %{name}%{?1:-%{1}}\
Group: Development/Debug\
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}\
Provides: %{name}%{?1:-%{1}}-debuginfo-%{_target_cpu} = %{version}-%{release}\
AutoReqProv: no\
%description %{?1:%{1}-}debuginfo\
This package provides debug information for package %{name}%{?1:-%{1}}.\
This is required to use SystemTap with %{name}%{?1:-%{1}}-%{KVERREL}.\
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '/.*/%%{KVERREL}%{?1:[+]%{1}}/.*|/.*%%{KVERREL}%{?1:\+%{1}}(\.debug)?' -o debuginfo%{?1}.list}\
%{nil}

#
# 这个宏创建 kernel-<subpackage>-devel 包.
#	%%kernel_devel_package <subpackage> <pretty-name>
#
%define kernel_devel_package() \
%package %{?1:%{1}-}devel\
Summary: Development package for building kernel modules to match the %{?2:%{2} }kernel\
Summary(zh_CN.UTF-8): 用来编译 %{?2:%{2} }kernel 模块的内核开发包\
Group: System Environment/Kernel\
Group(zh_CN.UTF-8): 系统环境/内核\
Provides: kernel%{?1:-%{1}}-devel-%{_target_cpu} = %{version}-%{release}\
Provides: kernel-devel-%{_target_cpu} = %{version}-%{release}%{?1:+%{1}}\
Provides: kernel-devel = %{version}-%{release}%{?1:+%{1}}\
Provides: kernel-devel-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
Provides: installonlypkg(kernel)\
AutoReqProv: no\
Requires(pre): /usr/bin/find\
Requires: perl\
%description %{?1:%{1}-}devel\
This package provides kernel headers and makefiles sufficient to build modules\
against the %{?2:%{2} }kernel package.\
%description %{?1:%{1}-}devel -l zh_CN.UTF-8\
用来编译 %{?2:%{2} }kernel 模块的内核开发包。\
%{nil}

#
# 这个宏创建 kernel-<subpackage>-modules-extra 包。
#	%%kernel_modules_extra_package <subpackage> <pretty-name>
#
%define kernel_modules_extra_package() \
%package %{?1:%{1}-}modules-extra\
Summary: Extra kernel modules to match the %{?2:%{2} }kernel\
Summary(zh_CN.UTF-8): %{?2:%{2} }kernel 的额外内核模块\
Group: System Environment/Kernel\
Group(zh_CN.UTF-8): 系统环境/内核\
Provides: kernel%{?1:-%{1}}-modules-extra-%{_target_cpu} = %{version}-%{release}\
Provides: kernel%{?1:-%{1}}-modules-extra-%{_target_cpu} = %{version}-%{release}%{?1:+%{1}}\
Provides: kernel%{?1:-%{1}}-modules-extra = %{version}-%{release}%{?1:+%{1}}\
Provides: installonlypkg(kernel-module)\
Provides: kernel%{?1:-%{1}}-modules-extra-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
Requires: kernel-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
Requires: kernel%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules-extra\
This package provides less commonly used kernel modules for the %{?2:%{2} }kernel package.\
%description %{?1:%{1}-}modules-extra -l zh_CN.UTF-8\
%{?2:%{2} }kernel 的额外内核模块。\
%{nil}

#
# 这个宏创建 kernel-<subpackage>-modules 包。
#	%%kernel_modules_package <subpackage> <pretty-name>
#
%define kernel_modules_package() \
%package %{?1:%{1}-}modules\
Summary: kernel modules to match the %{?2:%{2}-}core kernel\
Summary(zh_CN.UTF-8): %{?2:%{2}-}core kernel 的内核模块\
Group: System Environment/Kernel\
Group(zh_CN.UTF-8): 系统环境/内核\
Provides: kernel%{?1:-%{1}}-modules-%{_target_cpu} = %{version}-%{release}\
Provides: kernel-modules-%{_target_cpu} = %{version}-%{release}%{?1:+%{1}}\
Provides: kernel-modules = %{version}-%{release}%{?1:+%{1}}\
Provides: installonlypkg(kernel-module)\
Provides: kernel%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
Requires: kernel-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules\
This package provides commonly used kernel modules for the %{?2:%{2}-}core kernel package.\
%description %{?1:%{1}-}modules -l zh_CN.UTF-8
%{?2:%{2}-}core kernel 的内核模块\
%{nil}

#
# 这个宏创建 a kernel-<subpackage> 元包。
#	%%kernel_meta_package <subpackage>
#
%define kernel_meta_package() \
%package %{1}\
summary: kernel meta-package for the %{1} kernel\
Summary(zh_CN.UTF-8): %{1} 内核的元包\
Group: system environment/kernel\
Group(zh_CN.UTF-8): 系统环境/内核\
Requires: kernel-%{1}-core-uname-r = %{KVERREL}%{?variant}+%{1}\
Requires: kernel-%{1}-modules-uname-r = %{KVERREL}%{?variant}+%{1}\
%description %{1}\
The meta-package for the %{1} kernel\
%description %{1} -l zh_CN.UTF-8\
%{1} 内核的元包\
%{nil}

#
# 这个宏创建 kernel-<subpackage> 和它的 -devel 及 -debuginfo 包。
#	%%define variant_summary The Linux kernel compiled for <configuration>
#	%%kernel_variant_package [-n <pretty-name>] <subpackage>
#
%define kernel_variant_package(n:) \
%package %{?1:%{1}-}core\
Summary: %{variant_summary}\
Summary(zh_CN.UTF-8): %{variant_summary_zh}\
Group: System Environment/Kernel\
Group(zh_CN.UTF-8): 系统环境/内核\
Provides: kernel-%{?1:%{1}-}core-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
%{expand:%%kernel_reqprovconf}\
%if %{?1:1} %{!?1:0} \
%{expand:%%kernel_meta_package %{?1:%{1}}}\
%endif\
%{expand:%%kernel_devel_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%{expand:%%kernel_modules_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%{expand:%%kernel_modules_extra_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%{expand:%%kernel_debuginfo_package %{?1:%{1}}}\
%{nil}

# Now, each variant package.

%ifnarch armv7hl
%define variant_summary The Linux kernel compiled for PAE capable machines
%define variant_summary_zh 启用 PAE 的 Linux 内核
%kernel_variant_package %{pae}
%description %{pae}-core
This package includes a version of the Linux kernel with support for up to
64GB of high memory. It requires a CPU with Physical Address Extensions (PAE).
The non-PAE kernel can only address up to 4GB of memory.
Install the kernel-PAE package if your machine has more than 4GB of memory.
%description %{pae}-core -l zh_CN.UTF-8
这是一个支持到 64GB 大内存的 Linux 内核，它需要 CPU 支持 PAE，非 PAE 内核
只能支持到 4GB 内存以下。
如果你的机器有大于 4GB 的内存，安装 kernel-PAE 包。
%else
%define variant_summary The Linux kernel compiled for Cortex-A15
%define variant_summary_zh Cortex-A15 的 Linux 内核
%kernel_variant_package %{pae}
%description %{pae}-core
This package includes a version of the Linux kernel with support for
Cortex-A15 devices with LPAE and HW virtualisation support
%description %{pae}-core -l zh_CN.UTF-8
这个包包含了支持 LPAE 和硬件虚拟化的 Cortex-A15 的 Linux 内核。
%endif


# debug 包不翻译了。
%define variant_summary The Linux kernel compiled with extra debugging enabled for PAE capable machines
%kernel_variant_package %{pae}debug
Obsoletes: kernel-PAE-debug
%description %{pae}debug-core
This package includes a version of the Linux kernel with support for up to
64GB of high memory. It requires a CPU with Physical A%description -l zh_CN.UTF-8ress Extensions (PAE).
The non-PAE kernel can only a%description -l zh_CN.UTF-8ress up to 4GB of memory.
Install the kernel-PAE package if your machine has more than 4GB of memory.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather a%description -l zh_CN.UTF-8itional information
on kernel bugs, as some of these options impact performance noticably.


%define variant_summary The Linux kernel compiled with extra debugging enabled
%kernel_variant_package debug
%description debug-core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather a%description -l zh_CN.UTF-8itional information
on kernel bugs, as some of these options impact performance noticably.

# 最后是主要的 -core 包。

%define variant_summary The Linux kernel
%define variant_summary_zh Linux 内核
%kernel_variant_package 
%description core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.
%description core -l zh_CN.UTF-8
这个包包含了 Linux 内核 (vmlinuz)，任何 Linux 操作系统的核心程序。
内核处理操作系统的基本功能：内存分配，进程分配，设备输入输出等。

%prep
# 检查和 --with *only 有关的一些设置
%if %{with_baseonly}
%if !%{with_up}%{with_pae}
echo "Cannot build --with baseonly, up build is disabled"
exit 1
%endif
%endif

# 基本版本必须大于 0
%if "%{baserelease}" == "0"
echo "baserelease must be greater than zero"
exit 1
%endif

# 检查 Patch 是否存在
if [ "%{patches}" != "%%{patches}" ] ; then
  for patch in %{patches} ; do
    if [ ! -f $patch ] ; then
      echo "ERROR: Patch  ${patch##/*/}  listed in specfile but is missing"
      exit 1
    fi
  done
fi 2>/dev/null

# patch 命令的参数，一般情况下 F2 就行
patch_command='patch -p1 -F5 -s'
# 应用补丁的函数，根据这个函数，kernel.spec 必须放在 rpmbuild/SPEC 目录下。
ApplyPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1
  fi
  if ! grep -E "^Patch[0-9]+: $patch\$" %{_specdir}/${RPM_PACKAGE_NAME%%%%%{?variant}}.spec ; then
    if [ "${patch:0:8}" != "patch-3." ] ; then
      echo "ERROR: Patch  $patch  not listed as a source patch in specfile"
      exit 1
    fi
  fi 2>/dev/null
  case "$patch" in
  *.bz2) bunzip2 < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *.gz)  gunzip  < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *.xz)  unxz    < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *) $patch_command ${1+"$@"} < "$RPM_SOURCE_DIR/$patch" ;;
  esac
}

# 可选的补丁，如果是空的就不应用
ApplyOptionalPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1
  fi
  local C=$(wc -l $RPM_SOURCE_DIR/$patch | awk '{print $1}')
  if [ "$C" -gt 9 ]; then
    ApplyPatch $patch ${1+"$@"}
  fi
}

# 首先我们解压内核压缩包，如果这不是第一次 make prep，我们使用
# 链接来清理压缩包，可以加快一点儿速度。

# 更新到最新版本。
%if 0%{?released_kernel}
%define vanillaversion 3.%{base_sublevel}
# non-released_kernel case
%else
%if 0%{?rcrev}
%define vanillaversion 3.%{upstream_sublevel}-rc%{rcrev}
%if 0%{?gitrev}
%define vanillaversion 3.%{upstream_sublevel}-rc%{rcrev}-git%{gitrev}
%endif
%else
# pre-{base_sublevel+1}-rc1 case
%if 0%{?gitrev}
%define vanillaversion 3.%{base_sublevel}-git%{gitrev}
%else
%define vanillaversion 3.%{base_sublevel}
%endif
%endif
%endif

# %%{vanillaversion} : the full version name, e.g. 2.6.35-rc6-git3
# %%{kversion}       : the base version, e.g. 2.6.34

# %%{vanillaversion} : 整个的版本，比如 2.6.35-rc6-git3
# %%{kversion}	     : 基本的版本，比如 2.6.34

# Use kernel-%%{kversion}%%{?dist} as the top-level directory name
# so we can prep different trees within a single git directory.
# 使用 kernel-%%{kversion}%%{?dist} 作为顶级目录
# 这样我可以在一个 git 目录中准备不同的树。

# 生成其它顶级内核目录树的列表。
sharedirs=$(find "$PWD" -maxdepth 1 -type d -name 'kernel-3.*' \
            | grep -x -v "$PWD"/kernel-%{kversion}%{?dist}) ||:

# 删除所有的旧稳定版的目录。
if [ -d kernel-%{kversion}%{?dist} ]; then
  cd kernel-%{kversion}%{?dist}
  for i in linux-*
  do
     if [ -d $i ]; then
       # Just in case we ctrl-c'd a prep already
       rm -rf deleteme.%{_target_cpu}
       # Move away the stale away, and delete in background.
       mv $i deleteme-$i
       rm -rf deleteme* &
     fi
  done
  cd ..
fi

# 生成新树。
if [ ! -d kernel-%{kversion}%{?dist}/vanilla-%{vanillaversion} ]; then

  if [ -d kernel-%{kversion}%{?dist}/vanilla-%{kversion} ]; then

    # The base vanilla version already exists.
    cd kernel-%{kversion}%{?dist}

    # Any vanilla-* directories other than the base one are stale.
    for dir in vanilla-*; do
      [ "$dir" = vanilla-%{kversion} ] || rm -rf $dir &
    done

  else

    rm -f pax_global_header
    # Look for an identical base vanilla dir that can be hardlinked.
    for sharedir in $sharedirs ; do
      if [[ ! -z $sharedir  &&  -d $sharedir/vanilla-%{kversion} ]] ; then
        break
      fi
    done
    if [[ ! -z $sharedir  &&  -d $sharedir/vanilla-%{kversion} ]] ; then
%setup -q -n kernel-%{kversion}%{?dist} -c -T
      cp -rl $sharedir/vanilla-%{kversion} .
    else
%setup -q -n kernel-%{kversion}%{?dist} -c
      mv linux-%{kversion} vanilla-%{kversion}
    fi

  fi

%if "%{kversion}" != "%{vanillaversion}"

  for sharedir in $sharedirs ; do
    if [[ ! -z $sharedir  &&  -d $sharedir/vanilla-%{vanillaversion} ]] ; then
      break
    fi
  done
  if [[ ! -z $sharedir  &&  -d $sharedir/vanilla-%{vanillaversion} ]] ; then

    cp -rl $sharedir/vanilla-%{vanillaversion} .

  else

    # Need to apply patches to the base vanilla version.
    cp -rl vanilla-%{kversion} vanilla-%{vanillaversion}
    cd vanilla-%{vanillaversion}

# Update vanilla to the latest upstream.
# (non-released_kernel case only)
%if 0%{?rcrev}
    ApplyPatch patch-3.%{upstream_sublevel}-rc%{rcrev}.xz
%if 0%{?gitrev}
    ApplyPatch patch-3.%{upstream_sublevel}-rc%{rcrev}-git%{gitrev}.xz
%endif
%else
# pre-{base_sublevel+1}-rc1 case
%if 0%{?gitrev}
    ApplyPatch patch-3.%{base_sublevel}-git%{gitrev}.xz
%endif
%endif

    cd ..

  fi

%endif

else

  # 已经准备好了所有的 vanilla 目录，切换到顶级目录。
  cd kernel-%{kversion}%{?dist}

fi

# 现在开始编译 Magic 内核。先复制一份。
cp -rl vanilla-%{vanillaversion} linux-%{KVERREL}

cd linux-%{KVERREL}

# 官方的稳定内核，如果有更新，打上补丁
%if 0%{?stable_base}
ApplyPatch %{stable_patch_00}
%endif
%if 0%{?stable_rc}
ApplyPatch %{stable_patch_01}
%endif

# Drop some necessary files from the source dir into the buildroot
cp $RPM_SOURCE_DIR/config-* .
cp %{SOURCE15} .

%if !%{debugbuildsenabled}
%if %{with_release}
# 正常情况实际编译的是调试版本，如果用户有明确需要，可以把配置更改到非调试版本。
make -f %{SOURCE19} config-release
%endif
%endif

# 从 config-* 文件中动态的生成内核的 .config 文件
make -f %{SOURCE20} VERSION=%{version} configs

# 把用户定义的本地配置选项更改合并到 .config。
for i in kernel-%{version}-*.config
do
  mv $i $i.tmp
  ./merge.pl %{SOURCE1000} $i.tmp > $i
  rm $i.tmp
done

ApplyPatch kbuild-AFTER_LINK.patch

#
# misc small stuff to make things compile
#
ApplyOptionalPatch compile-fixes.patch

%if !%{nopatches}

# revert patches from upstream that conflict or that we get via other means
ApplyOptionalPatch upstream-reverts.patch -R

# 架构相关补丁
# x86(-64)
ApplyPatch lib-cpumask-Make-CPUMASK_OFFSTACK-usable-without-deb.patch

# PPC

# ARM64

#
# ARM
#
ApplyPatch ARM-tegra-usb-no-reset.patch

ApplyPatch arm-dts-am335x-boneblack-lcdc-add-panel-info.patch
ApplyPatch arm-dts-am335x-boneblack-add-cpu0-opp-points.patch
ApplyPatch arm-dts-am335x-bone-common-enable-and-use-i2c2.patch
ApplyPatch arm-dts-am335x-bone-common-setup-default-pinmux-http.patch
ApplyPatch arm-dts-am335x-bone-common-add-uart2_pins-uart4_pins.patch
ApplyPatch pinctrl-pinctrl-single-must-be-initialized-early.patch

ApplyPatch arm-i.MX6-Utilite-device-dtb.patch
ApplyPatch arm-dts-sun7i-bananapi.patch

ApplyPatch arm-highbank-l2-reverts.patch

#
# 驱动和文件系统的修正
#

# ext4

# xfs

# btrfs

# eCryptfs

# NFSv4

# USB

# WMI

# ACPI

#
# PCI
#

#
# SCSI Bits.
#

# ACPI

ApplyPatch Revert-Revert-ACPI-video-change-acpi-video-brightnes.patch

# ALSA

# Networking

# Misc fixes
# The input layer spews crap no-one cares about.
ApplyPatch input-kill-stupid-messages.patch

# stop floppy.ko from autoloading during udev...
ApplyPatch die-floppy-die.patch

ApplyPatch no-pcspkr-modalias.patch

# Silence some useless messages that still get printed with 'quiet'
ApplyPatch input-silence-i8042-noise.patch

# Make fbcon not show the penguins with 'quiet'
ApplyPatch silence-fbcon-logo.patch

# Changes to upstream defaults.
#rhbz 1126580
ApplyPatch Kbuild-Add-an-option-to-enable-GCC-VTA.patch

# /dev/crash driver.
ApplyPatch crash-driver.patch

# crypto/

# secure boot
ApplyPatch Add-secure_modules-call.patch
ApplyPatch PCI-Lock-down-BAR-access-when-module-security-is-ena.patch
ApplyPatch x86-Lock-down-IO-port-access-when-module-security-is.patch
ApplyPatch ACPI-Limit-access-to-custom_method.patch
ApplyPatch asus-wmi-Restrict-debugfs-interface-when-module-load.patch
ApplyPatch Restrict-dev-mem-and-dev-kmem-when-module-loading-is.patch
ApplyPatch acpi-Ignore-acpi_rsdp-kernel-parameter-when-module-l.patch
ApplyPatch kexec-Disable-at-runtime-if-the-kernel-enforces-modu.patch
ApplyPatch x86-Restrict-MSR-access-when-module-loading-is-restr.patch
ApplyPatch Add-option-to-automatically-enforce-module-signature.patch
ApplyPatch efi-Disable-secure-boot-if-shim-is-in-insecure-mode.patch
ApplyPatch efi-Make-EFI_SECURE_BOOT_SIG_ENFORCE-depend-on-EFI.patch
ApplyPatch efi-Add-EFI_SECURE_BOOT-bit.patch
ApplyPatch hibernate-Disable-in-a-signed-modules-environment.patch

ApplyPatch Add-EFI-signature-data-types.patch
ApplyPatch Add-an-EFI-signature-blob-parser-and-key-loader.patch
ApplyPatch KEYS-Add-a-system-blacklist-keyring.patch
ApplyPatch MODSIGN-Import-certificates-from-UEFI-Secure-Boot.patch
ApplyPatch MODSIGN-Support-not-importing-certs-from-db.patch

ApplyPatch Add-sysrq-option-to-disable-secure-boot-mode.patch

# Assorted Virt Fixes

# DRM core

# Nouveau DRM

# Intel DRM
ApplyPatch drm-i915-tame-the-chattermouth-v2.patch
ApplyPatch drm-i915-Disable-verbose-state-checks.patch 

# Radeon DRM

# Patches headed upstream
ApplyPatch disable-i8042-check-on-apple-mac.patch

# FIXME: REBASE
#ApplyPatch hibernate-freeze-filesystems.patch

ApplyPatch lis3-improve-handling-of-null-rate.patch

# Disable watchdog on virtual machines.
ApplyPatch watchdog-Disable-watchdog-on-virtual-machines.patch

#rhbz 754518
ApplyPatch scsi-sd_revalidate_disk-prevent-NULL-ptr-deref.patch

#pplyPatch weird-root-dentry-name-debug.patch

# https://fedoraproject.org/wiki/Features/Checkpoint_Restore
ApplyPatch criu-no-expert.patch

#rhbz 892811
ApplyPatch ath9k-rx-dma-stop-check.patch

# Patch series from Hans for various backlight and platform driver fixes
ApplyPatch samsung-laptop-Add-broken-acpi-video-quirk-for-NC210.patch

#rhbz 1089731
ApplyPatch asus-nb-wmi-Add-wapf4-quirk-for-the-X550VB.patch

#rhbz 1173806
ApplyPatch powerpc-powernv-force-all-CPUs-to-be-bootable.patch

#rhbz 1163927
ApplyPatch Set-UID-in-sess_auth_rawntlmssp_authenticate-too.patch

#rhbz 1163574
ApplyPatch acpi-video-Add-disable_native_backlight-quirk-for-De.patch
#rhbz 1094948
ApplyPatch acpi-video-Add-disable_native_backlight-quirk-for-Sa.patch

# Fix for big-endian arches, already upstream
ApplyPatch mpssd-x86-only.patch

#rhbz 1186097
ApplyPatch acpi-video-add-disable_native_backlight_quirk_for_samsung_510r.patch

#CVE-XXXX-XXXX rhbz 1189864 1192079
ApplyPatch vhost-scsi-potential-memory-corruption.patch

#CVE-2015-0275 rhbz 1193907 1195178
ApplyPatch ext4-Allocate-entire-range-in-zero-range.patch

%if 0%{?aarch64patches}
ApplyPatch kernel-arm64.patch
%ifnarch aarch64 # this is stupid, but i want to notice before secondary koji does.
ApplyPatch kernel-arm64.patch -R
%endif
%endif

# fbconder 补丁
ApplyPatch 4200_fbcondecor-3.16.patch

# aufs3 补丁
ApplyPatch aufs001.patch
ApplyPatch aufs3-base.patch
ApplyPatch aufs3-kbuild.patch
ApplyPatch aufs3-loopback.patch
ApplyPatch aufs3-mmap.patch
ApplyPatch aufs3-standalone.patch

# UTF-8 字符补丁
ApplyPatch 3.18.20-utf8.diff

# END OF PATCH APPLICATIONS

%endif

# Any further pre-build tree manipulations happen here.

chmod +x scripts/checkpatch.pl

# This Prevents scripts/setlocalversion from mucking with our version numbers.
touch .scmversion

# 只有要编译的架构才处理 config
%ifnarch %nobuildarches

mkdir configs

%if !%{debugbuildsenabled}
rm -f kernel-%{version}-*debug.config
%endif


# 现在在所有的配置文件上运行 oldconfig
for i in *.config
do
  mv $i .config
# Arch 来自 .config 里，所以 .config 的第一行必须是架构
  Arch=`head -1 .config | cut -b 3-`
  make ARCH=$Arch listnewconfig | grep -E '^CONFIG_' >.newoptions || true
# 如果 listnewconfig_fail 是 true，则显示出新的选项出退出
%if %{listnewconfig_fail}
  if [ -s .newoptions ]; then
    cat .newoptions
    exit 1
  fi
%endif
  rm -f .newoptions
  make ARCH=$Arch oldnoconfig
  echo "# $Arch" > configs/$i
  cat .config >> configs/$i
done
# end of kernel config
%endif

# get rid of unwanted files resulting from patch fuzz
find . \( -name "*.orig" -o -name "*~" \) -exec rm -f {} \; >/dev/null

# remove unnecessary SCM files
find . -name .gitignore -exec rm -f {} \; >/dev/null

cd ..

###
### build
###
%build

%if %{with_sparse}
%define sparse_mflags	C=1
%endif

%if %{with_debuginfo}
# This override tweaks the kernel makefiles so that we run debugedit on an
# object before embedding it.  When we later run find-debuginfo.sh, it will
# run debugedit again.  The edits it does change the build ID bits embedded
# in the stripped object, but repeating debugedit is a no-op.  We do it
# beforehand to get the proper final build ID bits into the embedded image.
# This affects the vDSO images in vmlinux, and the vmlinux image in bzImage.
# 不知道做什么。和 debuginfo 包有关。
export AFTER_LINK=\
'sh -xc "/usr/lib/rpm/debugedit -b $$RPM_BUILD_DIR -d /usr/src/debug \
    				-i $@ > $@.id"'
%endif

#
cp_vmlinux()
{
  eu-strip --remove-comment -o "$2" "$1"
}

# 编译内核
# 参数 1 是编译目标，2 是内核镜像，3 是 ?
BuildKernel() {
    MakeTarget=$1
    KernelImage=$2
    Flavour=$3
    Flav=${Flavour:++${Flavour}}
    InstallName=${4:-vmlinuz}

    # 选择正确的内核配置文件
    Config=kernel-%{version}-%{_target_cpu}${Flavour:+-${Flavour}}.config
    DevelDir=/usr/src/kernels/%{KVERREL}${Flav}

    # 如果启动镜像是一个 ELF 内核，strip 它。
    # 我们已经复制 unstripped 文件到 debuginfo 包了。
    if [ "$KernelImage" = vmlinux ]; then
      CopyKernel=cp_vmlinux
    else
      CopyKernel=cp
    fi

    KernelVer=%{version}-%{release}.%{_target_cpu}${Flav}
    echo BUILDING A KERNEL FOR ${Flavour} %{_target_cpu}...

    %if 0%{?stable_update}
    # make sure SUBLEVEL is incremented on a stable release.  Sigh 3.x.
    perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{?stablerev}/" Makefile
    %endif

    # make sure EXTRAVERSION says what we want it to say
    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}.%{_target_cpu}${Flav}/" Makefile

    # if pre-rc1 devel kernel, must fix up PATCHLEVEL for our versioning scheme
    %if !0%{?rcrev}
    %if 0%{?gitrev}
    perl -p -i -e 's/^PATCHLEVEL.*/PATCHLEVEL = %{upstream_sublevel}/' Makefile
    %endif
    %endif

    # and now to start the build process

    make -s mrproper
    cp configs/$Config .config

    %if %{signmodules}
    cp %{SOURCE11} .
    %endif

    chmod +x scripts/sign-file

    Arch=`head -1 .config | cut -b 3-`
    echo USING ARCH=$Arch

    make -s ARCH=$Arch oldnoconfig >/dev/null
    %{__make} -s ARCH=$Arch V=1 %{?_smp_mflags} $MakeTarget %{?sparse_mflags} %{?kernel_mflags}
    %{__make} -s ARCH=$Arch V=1 %{?_smp_mflags} modules %{?sparse_mflags} || exit 1

%ifarch %{arm} aarch64
    %{__make} -s ARCH=$Arch V=1 dtbs dtbs_install INSTALL_DTBS_PATH=$RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer
    find arch/$Arch/boot/dts -name '*.dtb' -type f | xargs rm -f
%endif

    # Start installing the results
%if %{with_debuginfo}
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/boot
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/%{image_install_path}
%endif
    mkdir -p $RPM_BUILD_ROOT/%{image_install_path}
    install -m 644 .config $RPM_BUILD_ROOT/boot/config-$KernelVer
    install -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-$KernelVer

    # We estimate the size of the initramfs because rpm needs to take this size
    # into consideration when performing disk space calculations. (See bz #530778)
    dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initramfs-$KernelVer.img bs=1M count=20

    if [ -f arch/$Arch/boot/zImage.stub ]; then
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/%{image_install_path}/zImage.stub-$KernelVer || :
    fi
    %if %{signmodules}
    # Sign the image if we're using EFI
    %pesign -s -i $KernelImage -o vmlinuz.signed
    if [ ! -s vmlinuz.signed ]; then
        echo "pesigning failed"
        exit 1
    fi
    mv vmlinuz.signed $KernelImage
    %endif
    $CopyKernel $KernelImage \
    		$RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    chmod 755 $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer

    # hmac sign the kernel for FIPS
    echo "Creating hmac file: $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac"
    ls -l $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    sha512hmac $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer | sed -e "s,$RPM_BUILD_ROOT,," > $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac;

    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer
    # Override $(mod-fw) because we don't want it to install any firmware
    # we'll get it from the linux-firmware package and we don't want conflicts
    %{__make} -s ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_install KERNELRELEASE=$KernelVer mod-fw=

%ifarch %{vdso_arches}
    %{__make} -s ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT vdso_install KERNELRELEASE=$KernelVer
    if [ ! -s ldconfig-kernel.conf ]; then
      echo > ldconfig-kernel.conf "\
# Placeholder file, no vDSO hwcap entries used in this kernel."
    fi
    %{__install} -D -m 444 ldconfig-kernel.conf \
        $RPM_BUILD_ROOT/etc/ld.so.conf.d/kernel-$KernelVer.conf
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/vdso/.build-id
%endif

    # And save the headers/makefiles etc for building modules against
    #
    # This all looks scary, but the end result is supposed to be:
    # * all arch relevant include/ files
    # * all Makefile/Kconfig files
    # * all script/ files

    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/source
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    (cd $RPM_BUILD_ROOT/lib/modules/$KernelVer ; ln -s build source)
    # dirs for additional modules per module-init-tools, kbuild/modules.txt
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/extra
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/updates
    # first copy everything
    cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp Module.symvers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp System.map $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -s Module.markers ]; then
      cp Module.markers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi
    # then drop all but the needed Makefiles/Kconfig files
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Documentation
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    cp .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -d arch/$Arch/scripts ]; then
      cp -a arch/$Arch/scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch} || :
    fi
    if [ -f arch/$Arch/*lds ]; then
      cp -a arch/$Arch/*lds $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch}/ || :
    fi
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*.o
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*/*.o
%ifarch %{power64}
    cp -a --parents arch/powerpc/lib/crtsavres.[So] $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    if [ -d arch/%{asmarch}/include ]; then
      cp -a --parents arch/%{asmarch}/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
%ifarch aarch64
    # arch/arm64/include/asm/xen references arch/arm
    cp -a --parents arch/arm/include/asm/xen $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    # include the machine specific headers for ARM variants, if available.
%ifarch %{arm}
    if [ -d arch/%{asmarch}/mach-${Flavour}/include ]; then
      cp -a --parents arch/%{asmarch}/mach-${Flavour}/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
%endif
    cp -a include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include

    # Make sure the Makefile and version.h have a matching timestamp so that
    # external modules can be built
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/generated/uapi/linux/version.h

    # Copy .config to include/config/auto.conf so "make prepare" is unnecessary.
    cp $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/.config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/config/auto.conf

%if %{with_debuginfo}
    if test -s vmlinux.id; then
      cp vmlinux.id $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/vmlinux.id
    else
      echo >&2 "*** ERROR *** no vmlinux build ID! ***"
      exit 1
    fi

    #
    # save the vmlinux file for kernel debugging into the kernel-debuginfo rpm
    #
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    cp vmlinux $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
%endif

    find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name "*.ko" -type f >modnames

    # mark modules executable so that strip-to-file can strip them
    xargs --no-run-if-empty chmod u+x < modnames

    # Generate a list of modules for block and networking.

    grep -F /drivers/ modnames | xargs --no-run-if-empty nm -upA |
    sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

    collect_modules_list()
    {
      sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef |
        LC_ALL=C sort -u > $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
      if [ ! -z "$3" ]; then
        sed -r -e "/^($3)\$/d" -i $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
      fi
    }

    collect_modules_list networking \
    			 'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register|rt(l_|2x00)(pci|usb)_probe|register_netdevice'
    collect_modules_list block \
    			 'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_alloc_queue|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler|blk_queue_physical_block_size' 'pktcdvd.ko|dm-mod.ko'
    collect_modules_list drm \
    			 'drm_open|drm_init'
    collect_modules_list modesetting \
    			 'drm_crtc_init'

    # detect missing or incorrect license tags
    ( find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name '*.ko' | xargs /sbin/modinfo -l | \
        grep -E -v 'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' ) && exit 1

    # remove files that will be auto generated by depmod at rpm -i time
    pushd $RPM_BUILD_ROOT/lib/modules/$KernelVer/
        rm -f modules.{alias*,builtin.bin,dep*,*map,symbols*,devname,softdep}
    popd

    # Call the modules-extra script to move things around
    %{SOURCE17} $RPM_BUILD_ROOT/lib/modules/$KernelVer %{SOURCE16}

    #
    # Generate the kernel-core and kernel-modules files lists
    #

    # Copy the System.map file for depmod to use, and create a backup of the
    # full module tree so we can restore it after we're done filtering
    cp System.map $RPM_BUILD_ROOT/.
    pushd $RPM_BUILD_ROOT
    mkdir restore
    cp -r lib/modules/$KernelVer/* restore/.

    # don't include anything going into k-m-e in the file lists
    rm -rf lib/modules/$KernelVer/extra

    # Find all the module files and filter them out into the core and modules
    # lists.  This actually removes anything going into -modules from the dir.
    find lib/modules/$KernelVer/kernel -name *.ko | sort -n > modules.list
	cp $RPM_SOURCE_DIR/filter-*.sh .
    %{SOURCE99} modules.list %{_target_cpu}
	rm filter-*.sh

    # Run depmod on the resulting module tree and make sure it isn't broken
    depmod -b . -aeF ./System.map $KernelVer &> depmod.out
    if [ -s depmod.out ]; then
        echo "Depmod failure"
        cat depmod.out
        exit 1
    else
        rm depmod.out
    fi
    # remove files that will be auto generated by depmod at rpm -i time
    pushd $RPM_BUILD_ROOT/lib/modules/$KernelVer/
        rm -f modules.{alias*,builtin.bin,dep*,*map,symbols*,devname,softdep}
    popd

    # Go back and find all of the various directories in the tree.  We use this
    # for the dir lists in kernel-core
    find lib/modules/$KernelVer/kernel -type d | sort -n > module-dirs.list

    # Cleanup
    rm System.map
    cp -r restore/* lib/modules/$KernelVer/.
    rm -rf restore
    popd

    # Make sure the files lists start with absolute paths or rpmbuild fails.
    # Also add in the dir entries
    sed -e 's/^lib*/\/lib/' %{?zipsed} $RPM_BUILD_ROOT/k-d.list > ../kernel${Flavour:+-${Flavour}}-modules.list
    sed -e 's/^lib*/%dir \/lib/' %{?zipsed} $RPM_BUILD_ROOT/module-dirs.list > ../kernel${Flavour:+-${Flavour}}-core.list
    sed -e 's/^lib*/\/lib/' %{?zipsed} $RPM_BUILD_ROOT/modules.list >> ../kernel${Flavour:+-${Flavour}}-core.list

    # Cleanup
    rm -f $RPM_BUILD_ROOT/k-d.list
    rm -f $RPM_BUILD_ROOT/modules.list
    rm -f $RPM_BUILD_ROOT/module-dirs.list

%if %{signmodules}
    # Save the signing keys so we can sign the modules in __modsign_install_post
    cp signing_key.priv signing_key.priv.sign${Flav}
    cp signing_key.x509 signing_key.x509.sign${Flav}
%endif

    # Move the devel headers out of the root file system
    mkdir -p $RPM_BUILD_ROOT/usr/src/kernels
    mv $RPM_BUILD_ROOT/lib/modules/$KernelVer/build $RPM_BUILD_ROOT/$DevelDir

    # This is going to create a broken link during the build, but we don't use
    # it after this point.  We need the link to actually point to something
    # when kernel-devel is installed, and a relative link doesn't work across
    # the F17 UsrMove feature.
    ln -sf $DevelDir $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    # prune junk from kernel-devel
    find $RPM_BUILD_ROOT/usr/src/kernels -name ".*.cmd" -exec rm -f {} \;
}

###
# DO it...
###

# prepare directories
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/boot
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}

cd linux-%{KVERREL}

%if %{with_debug}
BuildKernel %make_target %kernel_image debug
%endif

%if %{with_pae_debug}
BuildKernel %make_target %kernel_image PAEdebug
%endif

%if %{with_pae}
BuildKernel %make_target %kernel_image PAE
%endif

%if %{with_up}
BuildKernel %make_target %kernel_image
%endif

# 编译 perf
%global perf_make \
  make -s EXTRA_CFLAGS="${RPM_OPT_FLAGS}" LDFLAGS="%{__global_ldflags}" %{?cross_opts} %{?_smp_mflags} -C tools/perf V=1 NO_PERF_READ_VDSO32=1 WERROR=0 NO_LIBUNWIND=1 HAVE_CPLUS_DEMANGLE=1 NO_GTK2=1 NO_STRLCPY=1 NO_BIONIC=1 prefix=%{_prefix}
%if %{with_perf}
# perf
%{perf_make} DESTDIR=$RPM_BUILD_ROOT all
%endif

# 编译工具
%if %{with_tools}
%ifarch %{cpupowerarchs}
# cpupower
# make sure version-gen.sh is executable.
chmod +x tools/power/cpupower/utils/version-gen.sh
%{__make} %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false
%ifarch %{ix86}
    pushd tools/power/cpupower/debug/i386
    %{__make} %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    %{__make} %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch %{ix86} x86_64
   pushd tools/power/x86/x86_energy_perf_policy/
   %{__make}
   popd
   pushd tools/power/x86/turbostat
   %{__make}
   popd
%endif #turbostat/x86_energy_perf_policy
%endif
pushd tools/thermal/tmon/
%{__make}
popd
%endif

# In the modsign case, we do 3 things.  1) We check the "flavour" and hard
# code the value in the following invocations.  This is somewhat sub-optimal
# but we're doing this inside of an RPM macro and it isn't as easy as it
# could be because of that.  2) We restore the .tmp_versions/ directory from
# the one we saved off in BuildKernel above.  This is to make sure we're
# signing the modules we actually built/installed in that flavour.  3) We
# grab the arch and invoke mod-sign.sh command to actually sign the modules.
#
# We have to do all of those things _after_ find-debuginfo runs, otherwise
# that will strip the signature off of the modules.
# 和签名模块有关。

%define __modsign_install_post \
  if [ "%{signmodules}" -eq "1" ]; then \
    if [ "%{with_pae}" -ne "0" ]; then \
      %{modsign_cmd} signing_key.priv.sign+%{pae} signing_key.x509.sign+%{pae} $RPM_BUILD_ROOT/lib/modules/%{KVERREL}+%{pae}/ \
    fi \
    if [ "%{with_debug}" -ne "0" ]; then \
      %{modsign_cmd} signing_key.priv.sign+debug signing_key.x509.sign+debug $RPM_BUILD_ROOT/lib/modules/%{KVERREL}+debug/ \
    fi \
    if [ "%{with_pae_debug}" -ne "0" ]; then \
      %{modsign_cmd} signing_key.priv.sign+%{pae}debug signing_key.x509.sign+%{pae}debug $RPM_BUILD_ROOT/lib/modules/%{KVERREL}+%{pae}debug/ \
    fi \
    if [ "%{with_up}" -ne "0" ]; then \
      %{modsign_cmd} signing_key.priv.sign signing_key.x509.sign $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/ \
    fi \
  fi \
  if [ "%{zipmodules}" -eq "1" ]; then \
    find $RPM_BUILD_ROOT/lib/modules/ -type f -name '*.ko' | xargs xz; \
  fi \
%{nil}

###
### Special hacks for debuginfo subpackages.
###

# This macro is used by %%install, so we must redefine it before that.
%define debug_package %{nil}

# In the modsign case, we do 3 things.  1) We check the "flavour" and hard
# code the value in the following invocations.  This is somewhat sub-optimal
# but we're doing this inside of an RPM macro and it isn't as easy as it
# could be because of that.  2) We restore the .tmp_versions/ directory from
# the one we saved off in BuildKernel above.  This is to make sure we're
# signing the modules we actually built/installed in that flavour.  3) We
# grab the arch and invoke 'make modules_sign' and the mod-extra-sign.sh
# commands to actually sign the modules.
#
# We have to do all of those things _after_ find-debuginfo runs, otherwise
# that will strip the signature off of the modules.

%if %{with_debuginfo}
%define __debug_install_post \
  /usr/lib/rpm/find-debuginfo.sh %{debuginfo_args} %{_builddir}/%{?buildsubdir}\
%{nil}

%ifnarch noarch
%global __debug_package 1
%files -f debugfiles.list debuginfo-common-%{_target_cpu}
%defattr(-,root,root)
%endif
%endif

#
# Disgusting hack alert! We need to ensure we sign modules *after* all
# invocations of strip occur, which is in __debug_install_post if
# find-debuginfo.sh runs, and __os_install_post if not.
#
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__modsign_install_post}

###
### install
###

%install

cd linux-%{KVERREL}

# 我们必须在工具安装前安装头文件，不然 headers_install 会移除 /usr/include
# 中的所有头文件。

%if %{with_headers}
# Install kernel headers
make ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

find $RPM_BUILD_ROOT/usr/include \
     \( -name .install -o -name .check -o \
     	-name ..install.cmd -o -name ..check.cmd \) | xargs rm -f

%endif

# perl 安装
%if %{with_perf}
# perf tool binary and supporting scripts/binaries
%{perf_make} DESTDIR=$RPM_BUILD_ROOT lib=%{_lib} install-bin install-traceevent-plugins
# remove the 'trace' symlink.
rm -f %{buildroot}%{_bindir}/trace

# python-perf extension
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-python_ext

# perf man pages (note: implicit rpm magic compresses them later)
mkdir -p %{buildroot}/%{_mandir}/man1
pushd %{buildroot}/%{_mandir}/man1
tar -xf %{SOURCE10}
popd
%endif

# 工具安装
%if %{with_tools}
%ifarch %{cpupowerarchs}
%{__make} -C tools/power/cpupower DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false install
rm -f %{buildroot}%{_libdir}/*.{a,la}
magic_rpm_clean.sh
# 暂时没有中文翻译
#find_lang cpupower
#mv cpupower.lang ../
%ifarch %{ix86}
    pushd tools/power/cpupower/debug/i386
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
chmod 0755 %{buildroot}%{_libdir}/libcpupower.so*
mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig
install -m644 %{SOURCE2000} %{buildroot}%{_unitdir}/cpupower.service
install -m644 %{SOURCE2001} %{buildroot}%{_sysconfdir}/sysconfig/cpupower
%endif
%ifarch %{ix86} x86_64
   mkdir -p %{buildroot}%{_mandir}/man8
   pushd tools/power/x86/x86_energy_perf_policy
   make DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/turbostat
   make DESTDIR=%{buildroot} install
   popd
%endif #turbostat/x86_energy_perf_policy
pushd tools/thermal/tmon
make INSTALL_ROOT=%{buildroot} install
popd
%endif

# bootwrapper
%if %{with_bootwrapper}
make DESTDIR=$RPM_BUILD_ROOT bootwrapper_install WRAPPER_OBJDIR=%{_libdir}/kernel-wrapper WRAPPER_DTSDIR=%{_libdir}/kernel-wrapper/dts
%endif


###
### clean
###

%clean
rm -rf $RPM_BUILD_ROOT

###
### scripts
###

# tools 包的 post 脚本
%if %{with_tools}
%post -n kernel-tools
/sbin/ldconfig

%postun -n kernel-tools
/sbin/ldconfig
%endif

#
# 这个宏定义了 kernel*-devel 包的 %%post 脚本。
#	%%kernel_devel_post [<subpackage>]
#
%define kernel_devel_post() \
%{expand:%%post %{?1:%{1}-}devel}\
if [ -f /etc/sysconfig/kernel ]\
then\
    . /etc/sysconfig/kernel || exit $?\
fi\
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ]\
then\
    (cd /usr/src/kernels/%{KVERREL}%{?1:.%{1}} &&\
     /usr/bin/find . -type f | while read f; do\
       hardlink -c /usr/src/kernels/*.fc*.*/$f $f\
     done)\
fi\
%{nil}

#
# 这个宏定义了 kernel*-modules-extra 包的 %%post 脚本。
#	%%kernel_modules_extra_post [<subpackage>]
#
%define kernel_modules_extra_post() \
%{expand:%%post %{?1:%{1}-}modules-extra}\
/sbin/depmod -a %{KVERREL}%{?1:.%{1}}\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules-extra}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

#
# 这个宏定义了 kernel*-modules 包的 %%post 和 %%postun 脚本。
#	%%kernel_modules_post [<subpackage>]
#
%define kernel_modules_post() \
%{expand:%%post %{?1:%{1}-}modules}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

# 这个宏定义了 kernel 包的 %%posttrans 脚本。
#	%%kernel_variant_posttrans [<subpackage>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_posttrans() \
%{expand:%%posttrans %{?1:%{1}-}core}\
/bin/kernel-install add %{KVERREL}%{?1:+%{1}} /%{image_install_path}/vmlinuz-%{KVERREL}%{?1:+%{1}} || exit $?\
%{nil}

#
# 这个宏定义了内核包和它的开发的 %%post 脚本。
#	%%kernel_variant_post [-v <subpackage>] [-r <replace>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_post(v:r:) \
%{expand:%%kernel_devel_post %{?-v*}}\
%{expand:%%kernel_modules_post %{?-v*}}\
%{expand:%%kernel_modules_extra_post %{?-v*}}\
%{expand:%%kernel_variant_posttrans %{?-v*}}\
%{expand:%%post %{?-v*:%{-v*}-}core}\
%{-r:\
if [ `uname -i` == "x86_64" -o `uname -i` == "i386" ] &&\
   [ -f /etc/sysconfig/kernel ]; then\
  /bin/sed -r -i -e 's/^DEFAULTKERNEL=%{-r*}$/DEFAULTKERNEL=kernel%{?-v:-%{-v*}}/' /etc/sysconfig/kernel || exit $?\
fi}\
%{nil}

#
# 这个宏定义了内核包的 %%preun 脚本。
#	%%kernel_variant_preun <subpackage>
# /usr/bin/kernel-install 来自 systemd。
%define kernel_variant_preun() \
%{expand:%%preun %{?1:%{1}-}core}\
/usr/bin/kernel-install remove %{KVERREL}%{?1:+%{1}} /%{image_install_path}/vmlinuz-%{KVERREL}%{?1:+%{1}} || exit $?\
%{nil}

%kernel_variant_preun
%kernel_variant_post -r kernel-smp

%kernel_variant_preun %{pae}
%kernel_variant_post -v %{pae} -r (kernel|kernel-smp)

%kernel_variant_post -v %{pae}debug -r (kernel|kernel-smp)
%kernel_variant_preun %{pae}debug

%kernel_variant_preun debug
%kernel_variant_post -v debug

if [ -x /sbin/ldconfig ]
then
    /sbin/ldconfig -X || exit $?
fi

###
### 文件列表
###

%if %{with_headers}
%files headers
%defattr(-,root,root)
/usr/include/*
%endif

%if %{with_bootwrapper}
%files bootwrapper
%defattr(-,root,root)
/usr/sbin/*
%{_libdir}/kernel-wrapper
%endif

%if %{with_perf}
%files -n perf
%defattr(-,root,root)
%{_bindir}/perf
%dir %{_libdir}/traceevent/plugins
%{_libdir}/traceevent/plugins/*
%dir %{_libexecdir}/perf-core
%{_libexecdir}/perf-core/*
%{_mandir}/man[1-8]/perf*
%{_sysconfdir}/bash_completion.d/perf
%doc linux-%{KVERREL}/tools/perf/Documentation/examples.txt

%files -n python-perf
%defattr(-,root,root)
%{python_sitearch}

%if %{with_debuginfo}
%files -f perf-debuginfo.list -n perf-debuginfo
%defattr(-,root,root)

%files -f python-perf-debuginfo.list -n python-perf-debuginfo
%defattr(-,root,root)
%endif
%endif # with_perf

%if %{with_tools}
# 暂时没有中文翻译
#files -n kernel-tools -f cpupower.lang
%files -n kernel-tools
%defattr(-,root,root)
%ifarch %{cpupowerarchs}
%{_bindir}/cpupower
%ifarch %{ix86} x86_64
%{_bindir}/centrino-decode
%{_bindir}/powernow-k8-decode
%endif
%{_unitdir}/cpupower.service
%{_mandir}/man[1-8]/cpupower*
%config(noreplace) %{_sysconfdir}/sysconfig/cpupower
%ifarch %{ix86} x86_64
%{_bindir}/x86_energy_perf_policy
%{_mandir}/man8/x86_energy_perf_policy*
%{_bindir}/turbostat
%{_mandir}/man8/turbostat*
%endif
%{_bindir}/tmon
%endif

%if %{with_debuginfo}
%files -f kernel-tools-debuginfo.list -n kernel-tools-debuginfo
%defattr(-,root,root)
%endif

%ifarch %{cpupowerarchs}
%files -n kernel-tools-libs
%{_libdir}/libcpupower.so.0
%{_libdir}/libcpupower.so.0.0.0

%files -n kernel-tools-libs-devel
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%endif
%endif # with_tools-libs

# empty meta-package
%files
%defattr(-,root,root)

# This is %%{image_install_path} on an arch where that includes ELF files,
# or empty otherwise.
%define elf_image_install_path %{?kernel_image_elf:%{image_install_path}}

#
# This macro defines the %%files sections for a kernel package
# and its devel and debuginfo packages.
#	%%kernel_variant_files [-k vmlinux] <condition> <subpackage>
#
%define kernel_variant_files(k:) \
%if %{1}\
%{expand:%%files -f kernel-%{?2:%{2}-}core.list %{?2:%{2}-}core}\
%defattr(-,root,root)\
%{!?_licensedir:%global license %%doc}\
%license linux-%{KVERREL}/COPYING\
/%{image_install_path}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-%{KVERREL}%{?2:+%{2}}\
/%{image_install_path}/.vmlinuz-%{KVERREL}%{?2:+%{2}}.hmac \
%ifarch %{arm} aarch64\
/%{image_install_path}/dtb-%{KVERREL}%{?2:+%{2}} \
%endif\
%attr(600,root,root) /boot/System.map-%{KVERREL}%{?2:+%{2}}\
/boot/config-%{KVERREL}%{?2:+%{2}}\
%ghost /boot/initramfs-%{KVERREL}%{?2:+%{2}}.img\
%dir /lib/modules\
%dir /lib/modules/%{KVERREL}%{?2:+%{2}}\
%dir /lib/modules/%{KVERREL}%{?2:+%{2}}/kernel\
/lib/modules/%{KVERREL}%{?2:+%{2}}/build\
/lib/modules/%{KVERREL}%{?2:+%{2}}/source\
/lib/modules/%{KVERREL}%{?2:+%{2}}/updates\
%ifarch %{vdso_arches}\
/lib/modules/%{KVERREL}%{?2:+%{2}}/vdso\
/etc/ld.so.conf.d/kernel-%{KVERREL}%{?2:+%{2}}.conf\
%endif\
/lib/modules/%{KVERREL}%{?2:+%{2}}/modules.*\
%{expand:%%files -f kernel-%{?2:%{2}-}modules.list %{?2:%{2}-}modules}\
%defattr(-,root,root)\
%{expand:%%files %{?2:%{2}-}devel}\
%defattr(-,root,root)\
/usr/src/kernels/%{KVERREL}%{?2:+%{2}}\
%{expand:%%files %{?2:%{2}-}modules-extra}\
%defattr(-,root,root)\
/lib/modules/%{KVERREL}%{?2:+%{2}}/extra\
%if %{with_debuginfo}\
%ifnarch noarch\
%{expand:%%files -f debuginfo%{?2}.list %{?2:%{2}-}debuginfo}\
%defattr(-,root,root)\
%endif\
%endif\
%if %{?2:1} %{!?2:0}\
%{expand:%%files %{2}}\
%defattr(-,root,root)\
%endif\
%endif\
%{nil}


%kernel_variant_files %{with_up}
%kernel_variant_files %{with_debug} debug
%kernel_variant_files %{with_pae} %{pae}
%kernel_variant_files %{with_pae_debug} %{pae}debug

# plz don't put in a version string unless you're going to tag
# and build.

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.18.21-2
- 更新到 3.18.23

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 3.18.21-1
- 更新到 3.18.21

* Thu Aug 27 2015 Liu Di <liudidi@gmail.com> - 3.18.20-5
- 更新到 3.18.20
- 更改中文补丁为 cjktty
- 整理 spec
- 添加 mips64el 支持，目前只支持龙芯 3a
- 更新 fbconder 和 aufs3 补丁

* Wed Mar 04 2015 Liu Di <liudidi@gmail.com> - 3.10.70-4.3
- 更新到 3.10.70

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 3.10.44-4.3
- 更新到 3.10.44

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 3.10.41-4.3
- 为 Magic 3.0 重建

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 3.10.41-3.2
- 为 Magic 3.0 重建

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 3.10.41-2.1
- 为 Magic 3.0 重建

* Fri Oct 4 2013 Justin M. Forbes <jforbes@fedoraproject.org> 3.10.14-100
- Linux v3.10.14
