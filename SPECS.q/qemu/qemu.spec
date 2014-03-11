# build-time settings that support --with or --without:
#
# = kvmonly =
# Build only KVM-enabled QEMU targets, on KVM-enabled architectures.
#
# Disabled by default.
#
# = exclusive_x86_64 =
# ExclusiveArch: x86_64
#
# Disabled by default, except on RHEL.  Only makes sense with kvmonly.
#
# = rbd =
# Enable rbd support.
#
# Enable by default, except on RHEL.
#
# = separate_kvm =
# Do not build and install stuff that would colide with separately packaged KVM.
#
# Disabled by default, except on EPEL.

%if 0%{?rhel}
# RHEL-specific defaults:
%bcond_without kvmonly          # enabled
%bcond_without exclusive_x86_64 # enabled
%bcond_with    rbd              # disabled
%bcond_without spice            # enabled
%bcond_without seccomp          # enabled
%bcond_with    separate_kvm     # disabled - for EPEL
%else
# General defaults:
%bcond_with    kvmonly          # disabled
%bcond_with    exclusive_x86_64 # disabled
%bcond_without rbd              # enabled
%bcond_without spice            # enabled
%bcond_without seccomp          # enabled
%bcond_with    separate_kvm     # disabled
%endif

%global SLOF_gittagdate 20120731

%if %{without separate_kvm}
%global kvm_archs %{ix86} x86_64 ppc64 s390x
%else
%global kvm_archs %{ix86} ppc64 s390x
%endif
%if %{with exclusive_x86_64}
%global kvm_archs x86_64
%endif


%ifarch %{ix86} x86_64
%if %{with seccomp}
%global have_seccomp 1
%endif
%if %{with spice}
%global have_spice   1
%endif
%endif

%global need_qemu_kvm %{with kvmonly}

# These values for system_xyz are overridden below for non-kvmonly builds.
# Instead, these values for kvm_package are overridden below for kvmonly builds.
# Somewhat confusing, but avoids complicated nested conditionals.

%ifarch %{ix86}
%global system_x86    kvm
%global kvm_package   system-x86
%global kvm_target    i386
%global need_qemu_kvm 1
%endif
%ifarch x86_64
%global system_x86    kvm
%global kvm_package   system-x86
%global kvm_target    x86_64
%global need_qemu_kvm 1
%endif
%ifarch ppc64
%global system_ppc    kvm
%global kvm_package   system-ppc
%global kvm_target    ppc64
%endif
%ifarch s390x
%global system_s390x  kvm
%global kvm_package   system-s390x
%global kvm_target    s390x
%endif

%if %{with kvmonly}
# If kvmonly, put the qemu-kvm binary in the qemu-kvm package
%global kvm_package   kvm
%else
# If not kvmonly, build all packages and give them normal names. qemu-kvm
# is a simple wrapper package and is only build for archs that support KVM.
%global user          user
%global system_alpha  system-alpha
%global system_arm    system-arm
%global system_cris   system-cris
%global system_lm32   system-lm32
%global system_m68k   system-m68k
%global system_microblaze   system-microblaze
%global system_mips   system-mips
%global system_or32   system-or32
%global system_ppc    system-ppc
%global system_s390x  system-s390x
%global system_sh4    system-sh4
%global system_sparc  system-sparc
%global system_x86    system-x86
%global system_xtensa   system-xtensa
%global system_unicore32   system-unicore32
%endif

# libfdt is only needed to build ARM, Microblaze or PPC emulators
%if 0%{?system_arm:1}%{?system_microblaze:1}%{?system_ppc:1}
%global need_fdt      1
%endif

Summary: QEMU is a FAST! processor emulator
Name: qemu
Version: 1.2.0
Release: 25%{?dist}
# Epoch because we pushed a qemu-1.0 package. AIUI this can't ever be dropped
Epoch: 2
License: GPLv2+ and LGPLv2+ and BSD
Group: Development/Tools
URL: http://www.qemu.org/
# RHEL will build Qemu only on x86_64:
%if %{with kvmonly}
ExclusiveArch: %{kvm_archs}
%endif

# OOM killer breaks builds with parallel make on s390(x)
%ifarch s390 s390x
%define _smp_mflags %{nil}
%endif

Source0: http://downloads.sourceforge.net/sourceforge/kvm/qemu-kvm-%{version}.tar.gz

Source1: qemu.binfmt

# Loads kvm kernel modules at boot
Source2: kvm.modules

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

# Patches queued for 1.2.1 stable
Patch0001: 0001-target-xtensa-convert-host-errno-values-to-guest.patch
Patch0002: 0002-target-cris-Fix-buffer-overflow.patch
Patch0003: 0003-target-xtensa-fix-missing-errno-codes-for-mingw32.patch
Patch0004: 0004-target-sparc-fix-fcmp-s-d-q-instructions-wrt-excepti.patch
Patch0005: 0005-target-s390x-fix-style.patch
Patch0006: 0006-target-s390x-split-FPU-ops.patch
Patch0007: 0007-target-s390x-split-condition-code-helpers.patch
Patch0008: 0008-target-s390x-split-integer-helpers.patch
Patch0009: 0009-target-s390x-split-memory-access-helpers.patch
Patch0010: 0010-target-s390x-rename-op_helper.c-to-misc_helper.c.patch
Patch0011: 0011-target-s390x-avoid-AREG0-for-FPU-helpers.patch
Patch0012: 0012-target-s390x-avoid-AREG0-for-integer-helpers.patch
Patch0013: 0013-target-s390x-avoid-AREG0-for-condition-code-helpers.patch
Patch0014: 0014-target-s390x-avoid-AREG0-for-misc-helpers.patch
Patch0015: 0015-target-s390x-switch-to-AREG0-free-mode.patch
Patch0016: 0016-tcg-s390-fix-ld-st-with-CONFIG_TCG_PASS_AREG0.patch
Patch0017: 0017-target-arm-Fix-potential-buffer-overflow.patch
Patch0018: 0018-tcg-optimize-split-expression-simplification.patch
Patch0019: 0019-tcg-optimize-simplify-or-xor-r-a-0-cases.patch
Patch0020: 0020-tcg-optimize-simplify-and-r-a-0-cases.patch
Patch0021: 0021-tcg-optimize-simplify-shift-rot-r-0-a-movi-r-0-cases.patch
Patch0022: 0022-tcg-optimize-swap-brcond-setcond-arguments-when-poss.patch
Patch0023: 0023-tcg-optimize-add-constant-folding-for-setcond.patch
Patch0024: 0024-tcg-optimize-add-constant-folding-for-brcond.patch
Patch0025: 0025-tcg-optimize-fix-if-else-break-coding-style.patch
Patch0026: 0026-target-s390x-avoid-cpu_single_env.patch
Patch0027: 0027-target-lm32-switch-to-AREG0-free-mode.patch
Patch0028: 0028-target-m68k-switch-to-AREG0-free-mode.patch
Patch0029: 0029-target-m68k-avoid-using-cpu_single_env.patch
Patch0030: 0030-target-unicore32-switch-to-AREG0-free-mode.patch
Patch0031: 0031-target-arm-convert-void-helpers.patch
Patch0032: 0032-target-arm-convert-remaining-helpers.patch
Patch0033: 0033-target-arm-final-conversion-to-AREG0-free-mode.patch
Patch0034: 0034-target-microblaze-switch-to-AREG0-free-mode.patch
Patch0035: 0035-target-cris-Avoid-AREG0-for-helpers.patch
Patch0036: 0036-target-cris-Switch-to-AREG0-free-mode.patch
Patch0037: 0037-target-sh4-switch-to-AREG0-free-mode.patch
Patch0038: 0038-target-mips-switch-to-AREG0-free-mode.patch
Patch0039: 0039-Remove-unused-CONFIG_TCG_PASS_AREG0-and-dead-code.patch
Patch0040: 0040-tcg-i386-allow-constants-in-load-store-ops.patch
Patch0041: 0041-tcg-mark-set_label-with-TCG_OPF_BB_END-flag.patch
Patch0042: 0042-revert-TCG-fix-copy-propagation.patch
Patch0043: 0043-target-mips-Set-opn-in-gen_ldst_multiple.patch
Patch0044: 0044-target-mips-Fix-MIPS_DEBUG.patch
Patch0045: 0045-target-mips-Always-evaluate-debugging-macro-argument.patch
Patch0046: 0046-tcg-optimize-fix-end-of-basic-block-detection.patch
Patch0047: 0047-target-xtensa-fix-extui-shift-amount.patch
Patch0048: 0048-target-xtensa-don-t-emit-extra-tcg_gen_goto_tb.patch
Patch0049: 0049-tcg-Introduce-movcond.patch
Patch0050: 0050-target-alpha-Use-movcond.patch
Patch0051: 0051-tcg-i386-Implement-movcond.patch
Patch0052: 0052-tcg-Optimize-movcond-for-constant-comparisons.patch
Patch0053: 0053-tcg-Optimize-two-address-commutative-operations.patch
Patch0054: 0054-gdbstub-sh4-fix-build-with-USE_SOFTFLOAT_STRUCT_TYPE.patch
Patch0055: 0055-tcg-Fix-USE_DIRECT_JUMP.patch
Patch0056: 0056-tcg-hppa-Fix-brcond2-and-setcond2.patch
Patch0057: 0057-tcg-hppa-Fix-broken-load-store-helpers.patch
Patch0058: 0058-tcg-mips-fix-wrong-usage-of-Z-constraint.patch
Patch0059: 0059-tcg-mips-kill-warnings-in-user-mode.patch
Patch0060: 0060-tcg-mips-use-TCGArg-or-TCGReg-instead-of-int.patch
Patch0061: 0061-tcg-mips-don-t-use-global-pointer.patch
Patch0062: 0062-tcg-mips-use-stack-for-TCG-temps.patch
Patch0063: 0063-tcg-mips-optimize-brcond-arg-0.patch
Patch0064: 0064-tcg-mips-optimize-bswap-16-16s-32-on-MIPS32R2.patch
Patch0065: 0065-tcg-mips-implement-rotl-rotr-ops-on-MIPS32R2.patch
Patch0066: 0066-tcg-mips-implement-deposit-op-on-MIPS32R2.patch
Patch0067: 0067-tcg-mips-implement-movcond-op-on-MIPS32R2.patch
Patch0068: 0068-tcg-optimize-remove-TCG_TEMP_ANY.patch
Patch0069: 0069-tcg-optimize-check-types-in-copy-propagation.patch
Patch0070: 0070-tcg-optimize-rework-copy-progagation.patch
Patch0071: 0071-tcg-optimize-do-copy-propagation-for-all-operations.patch
Patch0072: 0072-tcg-optimize-optimize-op-r-a-a-mov-r-a.patch
Patch0073: 0073-tcg-optimize-optimize-op-r-a-a-movi-r-0.patch
Patch0074: 0074-tcg-optimize-further-optimize-brcond-movcond-setcond.patch
Patch0075: 0075-tcg-optimize-prefer-the-op-a-a-b-form-for-commutativ.patch
Patch0076: 0076-tcg-remove-ifdef-endif-around-TCGOpcode-tests.patch
Patch0077: 0077-tcg-optimize-add-constant-folding-for-deposit.patch
Patch0078: 0078-tcg-README-document-tcg_gen_goto_tb-restrictions.patch
Patch0079: 0079-w64-Fix-TCG-helper-functions-with-5-arguments.patch
Patch0080: 0080-tcg-ppc32-Implement-movcond32.patch
Patch0081: 0081-tcg-sparc-Hack-in-qemu_ld-st64-for-32-bit.patch
Patch0082: 0082-tcg-sparc-Fix-ADDX-opcode.patch
Patch0083: 0083-tcg-sparc-Don-t-MAP_FIXED-on-top-of-the-program.patch
Patch0084: 0084-tcg-sparc-Assume-v9-cpu-always-i.e.-force-v8plus-in-.patch
Patch0085: 0085-tcg-sparc-Fix-qemu_ld-st-to-handle-32-bit-host.patch
Patch0086: 0086-tcg-sparc-Support-GUEST_BASE.patch
Patch0087: 0087-tcg-sparc-Change-AREG0-in-generated-code-to-i0.patch
Patch0088: 0088-tcg-sparc-Clean-up-cruft-stemming-from-attempts-to-u.patch
Patch0089: 0089-tcg-sparc-Mask-shift-immediates-to-avoid-illegal-ins.patch
Patch0090: 0090-tcg-sparc-Use-defines-for-temporaries.patch
Patch0091: 0091-tcg-sparc-Add-g-o-registers-to-alloc_order.patch
Patch0092: 0092-tcg-sparc-Fix-and-enable-direct-TB-chaining.patch
Patch0093: 0093-tcg-sparc-Preserve-branch-destinations-during-retran.patch
Patch0094: 0094-target-alpha-Initialize-env-cpu_model_str.patch
Patch0095: 0095-tcg-mips-fix-MIPS32-R2-detection.patch
Patch0096: 0096-tcg-Adjust-descriptions-of-cond-opcodes.patch
Patch0097: 0097-tcg-i386-fix-build-with-march-i686.patch
Patch0098: 0098-tcg-Fix-MAX_OPC_PARAM_IARGS.patch
Patch0099: 0099-tci-Fix-for-AREG0-free-mode.patch
Patch0100: 0100-spice-abort-on-invalid-streaming-cmdline-params.patch
Patch0101: 0101-spice-notify-spice-server-on-vm-start-stop.patch
Patch0102: 0102-spice-notify-on-vm-state-change-only-via-spice_serve.patch
Patch0103: 0103-spice-migration-add-QEVENT_SPICE_MIGRATE_COMPLETED.patch
Patch0104: 0104-spice-add-migrated-flag-to-spice-info.patch
Patch0105: 0105-spice-adding-seamless-migration-option-to-the-comman.patch
Patch0106: 0106-spice-increase-the-verbosity-of-spice-section-in-qem.patch
Patch0107: 0107-qxl-update_area_io-guest_bug-on-invalid-parameters.patch
Patch0108: 0108-qxl-add-QXL_IO_MONITORS_CONFIG_ASYNC.patch
Patch0109: 0109-configure-print-spice-protocol-and-spice-server-vers.patch
Patch0110: 0110-fix-doc-of-using-raw-values-with-sendkey.patch
Patch0111: 0111-qapi-Fix-potential-NULL-pointer-segfault.patch
Patch0112: 0112-json-parser-Fix-potential-NULL-pointer-segfault.patch
Patch0113: 0113-pcie-drop-version_id-field-for-live-migration.patch
Patch0114: 0114-pcie_aer-clear-cmask-for-Advanced-Error-Interrupt-Me.patch
Patch0115: 0115-fix-entry-pointer-for-ELF-kernels-loaded-with-kernel.patch
Patch0116: 0116-lan9118-fix-multicast-filtering.patch
Patch0117: 0117-MIPS-user-Fix-reset-CPU-state-initialization.patch
Patch0118: 0118-Add-MAINTAINERS-entry-for-leon3.patch
Patch0119: 0119-musicpal-Fix-flash-mapping.patch
Patch0120: 0120-qemu-Use-valgrind-annotations-to-mark-kvm-guest-memo.patch
Patch0121: 0121-hw-wm8750-Fix-potential-buffer-overflow.patch
Patch0122: 0122-hw-mcf5206-Fix-buffer-overflow-for-MBAR-read-write.patch
Patch0123: 0123-use-libexecdir-instead-of-ignoring-it-first-and-rein.patch
Patch0124: 0124-socket-don-t-attempt-to-reconnect-a-TCP-socket-in-se.patch
Patch0125: 0125-Add-ability-to-force-enable-disable-of-tools-build.patch
Patch0126: 0126-usb-controllers-do-not-need-to-check-for-babble-them.patch
Patch0127: 0127-usb-core-Don-t-set-packet-state-to-complete-on-a-nak.patch
Patch0128: 0128-usb-core-Add-a-usb_ep_find_packet_by_id-helper-funct.patch
Patch0129: 0129-usb-core-Allow-the-first-packet-of-a-pipelined-ep-to.patch
Patch0130: 0130-Revert-ehci-don-t-flush-cache-on-doorbell-rings.patch
Patch0131: 0131-ehci-Validate-qh-is-not-changed-unexpectedly-by-the-.patch
Patch0132: 0132-ehci-Update-copyright-headers-to-reflect-recent-work.patch
Patch0133: 0133-ehci-Properly-cleanup-packets-on-cancel.patch
Patch0134: 0134-ehci-Properly-report-completed-but-not-yet-processed.patch
Patch0135: 0135-ehci-check-for-EHCI_ASYNC_FINISHED-first-in-ehci_fre.patch
Patch0136: 0136-ehci-trace-guest-bugs.patch
Patch0137: 0137-ehci-add-doorbell-trace-events.patch
Patch0138: 0138-ehci-Add-some-additional-ehci_trace_guest_bug-calls.patch
Patch0139: 0139-ehci-Fix-memory-leak-in-handling-of-NAK-ed-packets.patch
Patch0140: 0140-ehci-Handle-USB_RET_PROCERR-in-ehci_fill_queue.patch
Patch0141: 0141-ehci-Correct-a-comment-in-fetchqtd-packet-processing.patch
Patch0142: 0142-usb-redir-Never-return-USB_RET_NAK-for-async-handled.patch
Patch0143: 0143-usb-redir-Don-t-delay-handling-of-open-events-to-a-b.patch
Patch0144: 0144-usb-redir-Get-rid-of-async-struct-get-member.patch
Patch0145: 0145-usb-redir-Get-rid-of-local-shadow-copy-of-packet-hea.patch
Patch0146: 0146-usb-redir-Get-rid-of-unused-async-struct-dev-member.patch
Patch0147: 0147-usb-redir-Move-to-core-packet-id-and-queue-handling.patch
Patch0148: 0148-usb-redir-Return-babble-when-getting-more-bulk-data-.patch
Patch0149: 0149-Better-name-usb-braille-device.patch
Patch0150: 0150-usb-audio-fix-usb-version.patch
Patch0151: 0151-xhci-rip-out-background-transfer-code.patch
Patch0152: 0152-xhci-drop-buffering.patch
Patch0153: 0153-xhci-fix-runtime-write-tracepoint.patch
Patch0154: 0154-xhci-allow-bytewise-capability-register-reads.patch
Patch0155: 0155-qxl-dont-update-invalid-area.patch
Patch0156: 0156-usb-host-allow-emulated-non-async-control-requests-w.patch
Patch0157: 0157-qxl-better-cleanup-for-surface-destroy.patch
Patch0158: 0158-ehci-switch-to-new-style-memory-ops.patch
Patch0159: 0159-ehci-Fix-interrupts-stopping-when-Interrupt-Threshol.patch
Patch0160: 0160-ehci-Don-t-process-too-much-frames-in-1-timer-tick-v.patch
Patch0161: 0161-sheepdog-fix-savevm-and-loadvm.patch
Patch0162: 0162-ide-Fix-error-messages-from-static-code-analysis-no-.patch
Patch0163: 0163-block-curl-Fix-wrong-free-statement.patch
Patch0164: 0164-vdi-Fix-warning-from-clang.patch
Patch0165: 0165-block-fix-block-tray-status.patch
Patch0166: 0166-ahci-properly-reset-PxCMD-on-HBA-reset.patch
Patch0167: 0167-Don-t-require-encryption-password-for-qemu-img-info-.patch
Patch0168: 0168-block-Don-t-forget-to-delete-temporary-file.patch
Patch0169: 0169-hw-qxl-tracing-fixes.patch
Patch0170: 0170-configure-usbredir-fixes.patch
Patch0171: 0171-ehci-Don-t-set-seen-to-0-when-removing-unseen-queue-.patch
Patch0172: 0172-ehci-Walk-async-schedule-before-and-after-migration.patch
Patch0173: 0173-usb-redir-Revert-usb-redir-part-of-commit-93bfef4c.patch
Patch0174: 0174-uhci-Don-t-queue-up-packets-after-one-with-the-SPD-f.patch
Patch0175: 0175-slirp-Remove-wrong-type-casts-ins-debug-statements.patch
Patch0176: 0176-slirp-Fix-error-reported-by-static-code-analysis.patch
Patch0177: 0177-slirp-improve-TFTP-performance.patch
Patch0178: 0178-slirp-Handle-more-than-65535-blocks-in-TFTP-transfer.patch
Patch0179: 0179-slirp-Implement-TFTP-Blocksize-option.patch
Patch0180: 0180-srp-Don-t-use-QEMU_PACKED-for-single-elements-of-a-s.patch
Patch0181: 0181-Spelling-fixes-in-comments-and-documentation.patch
Patch0182: 0182-console-Clean-up-bytes-per-pixel-calculation.patch
Patch0183: 0183-qapi-Fix-enumeration-typo-error.patch
Patch0184: 0184-kvm-Fix-warning-from-static-code-analysis.patch
Patch0185: 0185-arch_init.c-add-missing-symbols-before-PRIu64-in-deb.patch
Patch0186: 0186-net-notify-iothread-after-flushing-queue.patch
Patch0187: 0187-e1000-flush-queue-whenever-can_receive-can-go-from-f.patch
Patch0188: 0188-xen-flush-queue-when-getting-an-event.patch
Patch0189: 0189-eepro100-Fix-network-hang-when-rx-buffers-run-out.patch
Patch0190: 0190-net-add-receive_disabled-logic-to-iov-delivery-path.patch
Patch0191: 0191-net-do-not-report-queued-packets-as-sent.patch
Patch0192: 0192-net-add-netdev-options-to-man-page.patch
Patch0193: 0193-net-clean-up-usbnet_receive.patch
Patch0194: 0194-net-fix-usbnet_receive-packet-drops.patch
Patch0195: 0195-net-broadcast-hub-packets-if-at-least-one-port-can-r.patch
Patch0196: 0196-net-asynchronous-send-receive-infrastructure-for-net.patch
Patch0197: 0197-net-EAGAIN-handling-for-net-socket.c-UDP.patch
Patch0198: 0198-net-EAGAIN-handling-for-net-socket.c-TCP.patch
Patch0199: 0199-configure-fix-seccomp-check.patch
Patch0200: 0200-configure-properly-check-if-lrt-and-lm-is-needed.patch
Patch0201: 0201-Revert-455aa1e08-and-c3767ed0eb.patch
Patch0202: 0202-qemu-char-BUGFIX-don-t-call-FD_ISSET-with-negative-f.patch
Patch0203: 0203-cpu_physical_memory_write_rom-needs-to-do-TB-invalid.patch
Patch0204: 0204-arch_init.c-Improve-soundhw-help-for-non-HAS_AUDIO_C.patch
Patch0205: 0205-xilinx_timer-Removed-comma-in-device-name.patch
Patch0206: 0206-xilinx_timer-Send-dbg-msgs-to-stderr-not-stdout.patch
Patch0207: 0207-xilinx.h-Error-check-when-setting-links.patch
Patch0208: 0208-xilinx_timer-Fix-a-compile-error-if-debug-enabled.patch
Patch0209: 0209-pflash_cfi01-fix-vendor-specific-extended-query.patch
Patch0210: 0210-MAINTAINERS-Add-entry-for-QOM-CPU.patch
Patch0211: 0211-iSCSI-We-need-to-support-SG_IO-also-from-iscsi_ioctl.patch
Patch0212: 0212-iSCSI-We-dont-need-to-explicitely-call-qemu_notify_e.patch
Patch0213: 0213-scsi-disk-introduce-check_lba_range.patch
Patch0214: 0214-scsi-disk-fix-check-for-out-of-range-LBA.patch
Patch0215: 0215-SCSI-Standard-INQUIRY-data-should-report-HiSup-flag-.patch
Patch0216: 0216-audio-Fix-warning-from-static-code-analysis.patch
Patch0217: 0217-qemu-ga-Remove-unreachable-code-after-g_error.patch
Patch0218: 0218-qemu-sockets-Fix-potential-memory-leak.patch
Patch0219: 0219-cadence_uart-Fix-buffer-overflow.patch
Patch0220: 0220-lm4549-Fix-buffer-overflow.patch
Patch0221: 0221-ioh3420-Remove-unreachable-code.patch
Patch0222: 0222-pflash_cfi01-Fix-warning-caused-by-unreachable-code.patch
Patch0223: 0223-curses-don-t-initialize-curses-when-qemu-is-daemoniz.patch
Patch0224: 0224-TextConsole-saturate-escape-parameter-in-TTY_STATE_C.patch
Patch0225: 0225-linux-user-Remove-redundant-null-check-and-replace-f.patch
Patch0226: 0226-net-socket-Fix-compiler-warning-regression-for-MinGW.patch
Patch0227: 0227-w32-Always-use-standard-instead-of-native-format-str.patch
Patch0228: 0228-w32-Add-implementation-of-gmtime_r-localtime_r.patch
Patch0229: 0229-blockdev-preserve-readonly-and-snapshot-states-acros.patch
Patch0230: 0230-block-correctly-set-the-keep_read_only-flag.patch
Patch0231: 0231-configure-Allow-builds-without-any-system-or-user-em.patch
Patch0232: 0232-Refactor-inet_connect_opts-function.patch
Patch0233: 0233-Separate-inet_connect-into-inet_connect-blocking-and.patch
Patch0234: 0234-Fix-address-handling-in-inet_nonblocking_connect.patch
Patch0235: 0235-Clear-handler-only-for-valid-fd.patch
Patch0236: 0236-pl190-fix-read-of-VECTADDR.patch
Patch0237: 0237-hw-armv7m_nvic-Correctly-register-GIC-region-when-se.patch
Patch0238: 0238-Versatile-Express-Fix-NOR-flash-0-address-and-remove.patch
Patch0239: 0239-i386-kvm-bit-10-of-CPUID-8000_0001-.EDX-is-reserved.patch
Patch0240: 0240-fpu-softfloat.c-Return-correctly-signed-values-from-.patch
Patch0241: 0241-pseries-Don-t-test-for-MSR_PR-for-hypercalls-under-K.patch
Patch0242: 0242-update-VERSION-for-v1.2.1.patch

# The infamous chardev flow control patches
Patch0400: 0400-char-Split-out-tcp-socket-close-code-in-a-separate-f.patch
Patch0401: 0401-char-Add-a-QemuChrHandlers-struct-to-initialise-char.patch
Patch0402: 0402-iohandlers-Add-enable-disable_write_fd_handler-funct.patch
Patch0403: 0403-char-Add-framework-for-a-write-unblocked-callback.patch
Patch0404: 0404-char-Update-send_all-to-handle-nonblocking-chardev-w.patch
Patch0405: 0405-char-Equip-the-unix-tcp-backend-to-handle-nonblockin.patch
Patch0406: 0406-char-Throttle-when-host-connection-is-down.patch
Patch0407: 0407-virtio-console-Enable-port-throttling-when-chardev-i.patch
Patch0408: 0408-spice-qemu-char.c-add-throttling.patch
Patch0409: 0409-spice-qemu-char.c-remove-intermediate-buffer.patch
Patch0410: 0410-usb-redir-Add-flow-control-support.patch
# 411 superceded by 414 which does the same thing but on top of 413 that is
# going upstream.
Patch0412: 0412-char-Disable-write-callback-if-throttled-chardev-is-.patch
Patch0413: 0413-hw-virtio-serial-bus-post_load-send_event-when-vm-is.patch
Patch0414: 0414-hw-virtio-serial-bus-replay-guest-open-on-destinatio.patch

# Spice features from upstream master: seamless migration & dynamic monitors
Patch0500: 0500-qxl-disallow-unknown-revisions.patch
Patch0501: 0501-spice-make-number-of-surfaces-runtime-configurable.patch
Patch0502: 0502-qxl-Add-set_client_capabilities-interface-to-QXLInte.patch
Patch0503: 0503-Remove-ifdef-QXL_COMMAND_FLAG_COMPAT_16BPP.patch
Patch0504: 0504-spice-switch-to-queue-for-vga-mode-updates.patch
Patch0505: 0505-spice-split-qemu_spice_create_update.patch
Patch0506: 0506-spice-add-screen-mirror.patch
Patch0507: 0507-spice-send-updates-only-for-changed-screen-content.patch
Patch0508: 0508-qxl-Ignore-set_client_capabilities-pre-post-migrate.patch
Patch0509: 0509-qxl-add-trace-event-for-QXL_IO_LOG.patch
Patch0510: 0510-hw-qxl-support-client-monitor-configuration-via-devi.patch
Patch0511: 0511-qxl-always-update-displaysurface-on-resize.patch
Patch0512: 0512-qxl-update_area_io-cleanup-invalid-parameters-handli.patch
Patch0513: 0513-qxl-fix-range-check-for-rev3-io-commands.patch
Patch0514: 0514-hw-qxl-exit-on-failure-to-register-qxl-interface.patch
Patch0515: 0515-hw-qxl-fix-condition-for-exiting-guest_bug.patch
Patch0516: 0516-hw-qxl-qxl_dirty_surfaces-use-uintptr_t.patch
Patch0517: 0517-spice-raise-requirement-to-0.12.patch
Patch0518: 0518-qxl-set-default-revision-to-4.patch

# usb-redir live-migration and misc bits, will be in before 1.3.0
Patch0600: 0600-usb-redir-Convert-to-new-libusbredirparser-0.5-API.patch
Patch0601: 0601-usb-redir-Set-ep-max_packet_size-if-available.patch
Patch0602: 0602-usb-redir-Add-a-usbredir_reject_device-helper-functi.patch
Patch0603: 0603-usb-redir-Ensure-our-peer-has-the-necessary-caps-whe.patch
Patch0604: 0604-usb-redir-Enable-pipelining-for-bulk-endpoints.patch
Patch0605: 0605-xhci-move-device-lookup-into-xhci_setup_packet.patch
Patch0606: 0606-xhci-implement-mfindex.patch
Patch0607: 0607-xhci-iso-xfer-support.patch
Patch0608: 0608-xhci-trace-cc-codes-in-cleartext.patch
Patch0609: 0609-xhci-add-trace_usb_xhci_ep_set_dequeue.patch
Patch0610: 0610-xhci-update-register-layout.patch
Patch0611: 0611-xhci-update-port-handling.patch
Patch0612: 0612-usb3-superspeed-descriptors.patch
Patch0613: 0613-usb3-superspeed-endpoint-companion.patch
Patch0614: 0614-usb3-bos-decriptor.patch
Patch0615: 0615-usb-storage-usb3-support.patch
Patch0616: 0616-xhci-fix-cleanup-msi.patch
Patch0617: 0617-xhci-rework-interrupt-handling.patch
Patch0618: 0618-xhci-add-msix-support.patch
Patch0619: 0619-xhci-move-register-update-into-xhci_intr_raise.patch
Patch0620: 0620-xhci-add-XHCIInterrupter.patch
Patch0621: 0621-xhci-prepare-xhci_runtime_-read-write-for-multiple-i.patch
Patch0622: 0622-xhci-pick-target-interrupter.patch
Patch0623: 0623-xhci-support-multiple-interrupters.patch
Patch0624: 0624-xhci-kill-xhci_mem_-read-write-dispatcher-functions.patch
Patch0625: 0625-usb-redir-Change-cancelled-packet-code-into-a-generi.patch
Patch0626: 0626-usb-redir-Add-an-already_in_flight-packet-id-queue.patch
Patch0627: 0627-usb-redir-Store-max_packet_size-in-endp_data.patch
Patch0628: 0628-usb-redir-Add-support-for-migration.patch
Patch0629: 0629-usb-redir-Add-chardev-open-close-debug-logging.patch
Patch0630: 0630-usb-redir-Revert-usb-redir-part-of-commit-93bfef4c.patch
Patch0631: 0631-ehci-Fix-interrupt-packet-MULT-handling.patch
Patch0632: 0632-usb-redir-Adjust-pkg-config-check-for-usbredirparser.patch
Patch0633: 0633-usb-redir-Change-usbredir_open_chardev-into-usbredir.patch
Patch0634: 0634-usb-redir-Don-t-make-migration-fail-in-none-seamless.patch

# Non upstream build fix, http://www.spinics.net/lists/kvm/msg80589.html
Patch0800: 0800-mips-Fix-link-error-with-piix4_pm_init.patch
# Add ./configure --disable-kvm-options
# keep: Carrying locally until qemu-kvm is fully merged into qemu.git
Patch0801: 0801-configure-Add-disable-kvm-options.patch
# Fix loading arm initrd if kernel is very large (bz 862766)
Patch802: 0802-arm_boot-Change-initrd-load-address-to-halfway-throu.patch
# Don't use reserved word 'function' in systemtap files (bz 870972)
Patch803: 0803-dtrace-backend-add-function-to-reserved-words.patch
# Drop assertion that was triggering when pausing guests w/ qxl (bz
# 870972)
Patch804: 0804-wip-hw-qxl-inject-interrupts-in-any-state.patch
# 38f419f (configure: Fix CONFIG_QEMU_HELPERDIR generation, 2012-10-17)
Patch805: 0805-configure-Fix-CONFIG_QEMU_HELPERDIR-generation.patch

# libcacard
Patch1001: 1001-libcacard-fix-missing-symbols-in-libcacard.so.patch
Patch1002: 1002-configure-move-vscclient-binary-under-libcacard.patch

BuildRequires: SDL-devel
BuildRequires: zlib-devel
BuildRequires: which
BuildRequires: texi2html
BuildRequires: gnutls-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libtool
BuildRequires: libaio-devel
BuildRequires: rsync
BuildRequires: pciutils-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: ncurses-devel
BuildRequires: libattr-devel
BuildRequires: usbredir-devel >= 0.5.2
BuildRequires: texinfo
%if 0%{?have_spice:1}
BuildRequires: spice-protocol >= 0.12.2
BuildRequires: spice-server-devel >= 0.12.0
%endif
%if 0%{?have_seccomp:1}
BuildRequires: libseccomp-devel >= 1.0.0
%endif
# For network block driver
BuildRequires: libcurl-devel
%if %{with rbd}
# For rbd block driver
BuildRequires: ceph-devel
%endif
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
%if 0%{?need_fdt:1}
# For FDT device tree support
BuildRequires: libfdt-devel
%endif
# For test suite
BuildRequires: check-devel
# For virtfs
BuildRequires: libcap-devel
%if 0%{?user:1}
Requires: %{name}-%{user} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_alpha:1}
Requires: %{name}-%{system_alpha} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_arm:1}
Requires: %{name}-%{system_arm} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_cris:1}
Requires: %{name}-%{system_cris} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_lm32:1}
Requires: %{name}-%{system_lm32} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_m68k:1}
Requires: %{name}-%{system_m68k} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_microblaze:1}
Requires: %{name}-%{system_microblaze} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_mips:1}
Requires: %{name}-%{system_mips} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_or32:1}
Requires: %{name}-%{system_or32} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_ppc:1}
Requires: %{name}-%{system_ppc} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_s390x:1}
Requires: %{name}-%{system_s390x} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_sh4:1}
Requires: %{name}-%{system_sh4} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_sparc:1}
Requires: %{name}-%{system_sparc} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_unicore32:1}
Requires: %{name}-%{system_unicore32} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_x86:1}
Requires: %{name}-%{system_x86} = %{epoch}:%{version}-%{release}
%endif
%if 0%{?system_xtensa:1}
Requires: %{name}-%{system_xtensa} = %{epoch}:%{version}-%{release}
%endif
%if %{without separate_kvm}
Requires: %{name}-img = %{epoch}:%{version}-%{release}
%else
Requires: %{name}-img
%endif

%define qemudocdir %{_docdir}/%{name}

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

%if %{without kvmonly}
%ifarch %{kvm_archs}
%package kvm
Summary: QEMU metapackage for KVM support
Group: Development/Tools
Requires: qemu-%{kvm_package} = %{epoch}:%{version}-%{release}

%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86
%endif
%endif

%package  img
Summary: QEMU command line tool for manipulating disk images
Group: Development/Tools
%if %{with rbd}
# librbd (from ceph) added new symbol rbd_flush recently.  If you
# update qemu-img without updating librdb you get:
# qemu-img: undefined symbol: rbd_flush
# ** NB ** This can be removed after Fedora 17 is released.
Conflicts: ceph < 0.37-2
%endif

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
if [ $1 -eq 1 ] ; then
    # Initial installation.
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun guest-agent
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade.
    /bin/systemctl stop qemu-guest-agent.service > /dev/null 2>&1 || :
fi

%postun guest-agent
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall.
    /bin/systemctl try-restart qemu-guest-agent.service >/dev/null 2>&1 || :
fi



%if 0%{?user:1}
%package %{user}
Summary: QEMU user mode emulation of qemu targets
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
%description %{user}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets
%endif

%if 0%{?system_x86:1}
%package %{system_x86}
Summary: QEMU system emulator for x86
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Provides: kvm = 85
Obsoletes: kvm < 85
Requires: vgabios >= 0.6c-2
Requires: seabios-bin >= 0.6.0-2
Requires: sgabios-bin
Requires: ipxe-roms-qemu
%if 0%{?have_seccomp:1}
Requires: libseccomp >= 1.0.0
%endif

%description %{system_x86}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.
%endif

%if 0%{?system_alpha:1}
%package %{system_alpha}
Summary: QEMU system emulator for Alpha
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_alpha}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Alpha systems.
%endif

%if 0%{?system_arm:1}
%package %{system_arm}
Summary: QEMU system emulator for ARM
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_arm}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ARM boards.
%endif

%if 0%{?system_mips:1}
%package %{system_mips}
Summary: QEMU system emulator for MIPS
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_mips}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for MIPS boards.
%endif

%if 0%{?system_cris:1}
%package %{system_cris}
Summary: QEMU system emulator for CRIS
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_cris}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for CRIS boards.
%endif

%if 0%{?system_lm32:1}
%package %{system_lm32}
Summary: QEMU system emulator for LatticeMico32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_lm32}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for LatticeMico32 boards.
%endif

%if 0%{?system_m68k:1}
%package %{system_m68k}
Summary: QEMU system emulator for ColdFire (m68k)
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_m68k}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ColdFire boards.
%endif

%if 0%{?system_microblaze:1}
%package %{system_microblaze}
Summary: QEMU system emulator for Microblaze
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_microblaze}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Microblaze boards.
%endif

%if 0%{?system_or32:1}
%package %{system_or32}
Summary: QEMU system emulator for OpenRisc32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_or32}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for OpenRisc32 boards.
%endif

%if 0%{?system_s390x:1}
%package %{system_s390x}
Summary: QEMU system emulator for S390
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_s390x}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for S390 systems.
%endif

%if 0%{?system_sh4:1}
%package %{system_sh4}
Summary: QEMU system emulator for SH4
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_sh4}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SH4 boards.
%endif

%if 0%{?system_sparc:1}
%package %{system_sparc}
Summary: QEMU system emulator for SPARC
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
%description %{system_sparc}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SPARC and SPARC64 systems.
%endif

%if 0%{?system_ppc:1}
%package %{system_ppc}
Summary: QEMU system emulator for PPC
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
Requires: SLOF = 0.1.git%{SLOF_gittagdate}
%description %{system_ppc}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for PPC and PPC64 systems.
%endif

%if 0%{?system_xtensa:1}
%package %{system_xtensa}
Summary: QEMU system emulator for Xtensa
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_xtensa}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Xtensa boards.
%endif

%if 0%{?system_unicore32:1}
%package %{system_unicore32}
Summary: QEMU system emulator for Unicore32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description %{system_unicore32}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Unicore32 boards.
%endif

%ifarch %{kvm_archs}
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
%setup -q -n qemu-kvm-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1
%patch0012 -p1
%patch0013 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
%patch0017 -p1
%patch0018 -p1
%patch0019 -p1
%patch0020 -p1
%patch0021 -p1
%patch0022 -p1
%patch0023 -p1
%patch0024 -p1
%patch0025 -p1
%patch0026 -p1
%patch0027 -p1
%patch0028 -p1
%patch0029 -p1
%patch0030 -p1
%patch0031 -p1
%patch0032 -p1
%patch0033 -p1
%patch0034 -p1
%patch0035 -p1
%patch0036 -p1
%patch0037 -p1
%patch0038 -p1
%patch0039 -p1
%patch0040 -p1
%patch0041 -p1
%patch0042 -p1
%patch0043 -p1
%patch0044 -p1
%patch0045 -p1
%patch0046 -p1
%patch0047 -p1
%patch0048 -p1
%patch0049 -p1
%patch0050 -p1
%patch0051 -p1
%patch0052 -p1
%patch0053 -p1
%patch0054 -p1
%patch0055 -p1
%patch0056 -p1
%patch0057 -p1
%patch0058 -p1
%patch0059 -p1
%patch0060 -p1
%patch0061 -p1
%patch0062 -p1
%patch0063 -p1
%patch0064 -p1
%patch0065 -p1
%patch0066 -p1
%patch0067 -p1
%patch0068 -p1
%patch0069 -p1
%patch0070 -p1
%patch0071 -p1
%patch0072 -p1
%patch0073 -p1
%patch0074 -p1
%patch0075 -p1
%patch0076 -p1
%patch0077 -p1
%patch0078 -p1
%patch0079 -p1
%patch0080 -p1
%patch0081 -p1
%patch0082 -p1
%patch0083 -p1
%patch0084 -p1
%patch0085 -p1
%patch0086 -p1
%patch0087 -p1
%patch0088 -p1
%patch0089 -p1
%patch0090 -p1
%patch0091 -p1
%patch0092 -p1
%patch0093 -p1
%patch0094 -p1
%patch0095 -p1
%patch0096 -p1
%patch0097 -p1
%patch0098 -p1
%patch0099 -p1
%patch0100 -p1
%patch0101 -p1
%patch0102 -p1
%patch0103 -p1
%patch0104 -p1
%patch0105 -p1
%patch0106 -p1
%patch0107 -p1
%patch0108 -p1
%patch0109 -p1
%patch0110 -p1
%patch0111 -p1
%patch0112 -p1
%patch0113 -p1
%patch0114 -p1
%patch0115 -p1
%patch0116 -p1
%patch0117 -p1
%patch0118 -p1
%patch0119 -p1
%patch0120 -p1
%patch0121 -p1
%patch0122 -p1
%patch0123 -p1
%patch0124 -p1
%patch0125 -p1
%patch0126 -p1
%patch0127 -p1
%patch0128 -p1
%patch0129 -p1
%patch0130 -p1
%patch0131 -p1
%patch0132 -p1
%patch0133 -p1
%patch0134 -p1
%patch0135 -p1
%patch0136 -p1
%patch0137 -p1
%patch0138 -p1
%patch0139 -p1
%patch0140 -p1
%patch0141 -p1
%patch0142 -p1
%patch0143 -p1
%patch0144 -p1
%patch0145 -p1
%patch0146 -p1
%patch0147 -p1
%patch0148 -p1
%patch0149 -p1
%patch0150 -p1
%patch0151 -p1
%patch0152 -p1
%patch0153 -p1
%patch0154 -p1
%patch0155 -p1
%patch0156 -p1
%patch0157 -p1
%patch0158 -p1
%patch0159 -p1
%patch0160 -p1
%patch0161 -p1
%patch0162 -p1
%patch0163 -p1
%patch0164 -p1
%patch0165 -p1
%patch0166 -p1
%patch0167 -p1
%patch0168 -p1
%patch0169 -p1
%patch0170 -p1
%patch0171 -p1
%patch0172 -p1
%patch0173 -p1
%patch0174 -p1
%patch0175 -p1
%patch0176 -p1
%patch0177 -p1
%patch0178 -p1
%patch0179 -p1
%patch0180 -p1
%patch0181 -p1
%patch0182 -p1
%patch0183 -p1
%patch0184 -p1
%patch0185 -p1
%patch0186 -p1
%patch0187 -p1
%patch0188 -p1
%patch0189 -p1
%patch0190 -p1
%patch0191 -p1
%patch0192 -p1
%patch0193 -p1
%patch0194 -p1
%patch0195 -p1
%patch0196 -p1
%patch0197 -p1
%patch0198 -p1
%patch0199 -p1
%patch0200 -p1
%patch0201 -p1
%patch0202 -p1
%patch0203 -p1
%patch0204 -p1
%patch0205 -p1
%patch0206 -p1
%patch0207 -p1
%patch0208 -p1
%patch0209 -p1
%patch0210 -p1
%patch0211 -p1
%patch0212 -p1
%patch0213 -p1
%patch0214 -p1
%patch0215 -p1
%patch0216 -p1
%patch0217 -p1
%patch0218 -p1
%patch0219 -p1
%patch0220 -p1
%patch0221 -p1
%patch0222 -p1
%patch0223 -p1
%patch0224 -p1
%patch0225 -p1
%patch0226 -p1
%patch0227 -p1
%patch0228 -p1
%patch0229 -p1
%patch0230 -p1
%patch0231 -p1
%patch0232 -p1
%patch0233 -p1
%patch0234 -p1
%patch0235 -p1
%patch0236 -p1
%patch0237 -p1
%patch0238 -p1
%patch0239 -p1
%patch0240 -p1
%patch0241 -p1
%patch0242 -p1

%patch0400 -p1
%patch0401 -p1
%patch0402 -p1
%patch0403 -p1
%patch0404 -p1
%patch0405 -p1
%patch0406 -p1
%patch0407 -p1
%patch0408 -p1
%patch0409 -p1
%patch0410 -p1
# 411 superceded by 414
%patch0412 -p1
%patch0413 -p1
%patch0414 -p1

%patch0500 -p1
%patch0501 -p1
%patch0502 -p1
%patch0503 -p1
%patch0504 -p1
%patch0505 -p1
%patch0506 -p1
%patch0507 -p1
%patch0508 -p1
%patch0509 -p1
%patch0510 -p1
%patch0511 -p1
%patch0512 -p1
%patch0513 -p1
%patch0514 -p1
%patch0515 -p1
%patch0516 -p1
%patch0517 -p1
%patch0518 -p1

%patch0600 -p1
%patch0601 -p1
%patch0602 -p1
%patch0603 -p1
%patch0604 -p1
%patch0605 -p1
%patch0606 -p1
%patch0607 -p1
%patch0608 -p1
%patch0609 -p1
%patch0610 -p1
%patch0611 -p1
%patch0612 -p1
%patch0613 -p1
%patch0614 -p1
%patch0615 -p1
%patch0616 -p1
%patch0617 -p1
%patch0618 -p1
%patch0619 -p1
%patch0620 -p1
%patch0621 -p1
%patch0622 -p1
%patch0623 -p1
%patch0624 -p1
%patch0625 -p1
%patch0626 -p1
%patch0627 -p1
%patch0628 -p1
%patch0629 -p1
%patch0630 -p1
%patch0631 -p1
%patch0632 -p1
%patch0633 -p1
%patch0634 -p1

%patch0800 -p1
%patch0801 -p1
%patch802 -p1
%patch803 -p1
%patch804 -p1
%patch805 -p1

# libcacard
%patch1001 -p1
%patch1002 -p1

%build
%if %{with kvmonly}
    buildarch="%{kvm_target}-softmmu"
%else
buildarch="i386-softmmu x86_64-softmmu alpha-softmmu arm-softmmu cris-softmmu \
    lm32-softmmu m68k-softmmu microblaze-softmmu microblazeel-softmmu \
    mips-softmmu mipsel-softmmu mips64-softmmu mips64el-softmmu \
    or32-softmmu ppc-softmmu ppcemb-softmmu ppc64-softmmu s390x-softmmu \
    sh4-softmmu sh4eb-softmmu sparc-softmmu sparc64-softmmu \
    xtensa-softmmu xtensaeb-softmmu unicore32-softmmu \
    i386-linux-user x86_64-linux-user alpha-linux-user arm-linux-user \
    armeb-linux-user cris-linux-user m68k-linux-user \
    microblaze-linux-user microblazeel-linux-user mips-linux-user \
    mipsel-linux-user or32-linux-user ppc-linux-user ppc64-linux-user \
    ppc64abi32-linux-user s390x-linux-user sh4-linux-user sh4eb-linux-user \
    sparc-linux-user sparc64-linux-user sparc32plus-linux-user \
    unicore32-linux-user"
%endif

# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

%ifarch s390
# drop -g flag to prevent memory exhaustion by linker
%global optflags %(echo %{optflags} | sed 's/-g//')
sed -i.debug 's/"-g $CFLAGS"/"$CFLAGS"/g' configure
%endif


dobuild() {
    ./configure \
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --sysconfdir=%{_sysconfdir} \
        --interp-prefix=%{_prefix}/qemu-%%M \
        --audio-drv-list=pa,sdl,alsa,oss \
        --disable-strip \
        --extra-ldflags="$extraldflags -pie -Wl,-z,relro -Wl,-z,now" \
        --extra-cflags="%{optflags} -fPIE -DPIE" \
%if 0%{?have_spice:1}
        --enable-spice \
%endif
        --enable-mixemu \
%if 0%{?have_seccomp:1}
        --enable-seccomp \
%endif
%if %{without rbd}
        --disable-rbd \
%endif
%if 0%{?need_fdt:1}
        --enable-fdt \
%else
        --disable-fdt \
%endif
        --enable-trace-backend=dtrace \
        --disable-werror \
        --disable-xen \
        --enable-kvm \
        "$@"

    echo "config-host.mak contents:"
    echo "==="
    cat config-host.mak
    echo "==="

    make V=1 %{?_smp_mflags} $buildldflags
    make V=1 %{?_smp_mflags} $buildldflags libcacard.la
    make V=1 %{?_smp_mflags} $buildldflags libcacard/vscclient
}

# This is kind of confusing. We run ./configure + make twice here to
# preserve some back compat: if on x86, we want to provide a qemu-kvm
# binary that defaults to KVM=on. All other qemu-system* should be
# able to use KVM, but default to KVM=off (upstream qemu semantics).
#
# Once qemu-kvm and qemu fully merge, and we base off qemu releases,
# all qemu-system-* will default to KVM=off, so we hopefully won't need
# to do these double builds. But then I'm not sure how we are going to
# generate a back compat qemu-kvm binary...

%if 0%{?need_qemu_kvm}
# Build qemu-kvm back compat binary
dobuild --target-list=%{kvm_target}-softmmu

# Setup back compat qemu-kvm binary which defaults to KVM=on
./scripts/tracetool.py --backend dtrace --format stap \
  --binary %{_bindir}/qemu-kvm --target-arch %{kvm_target} --target-type system \
  --probe-prefix qemu.kvm < ./trace-events > qemu-kvm.stp

cp -a %{kvm_target}-softmmu/qemu-system-%{kvm_target} qemu-kvm

%endif

%if %{without kvmonly}
%if 0%{?need_qemu_kvm}
make clean
%endif

# Build qemu-system-* with consistent default of kvm=off
dobuild --target-list="$buildarch" --disable-kvm-options
%endif

gcc %{SOURCE6} -O2 -g -o ksmctl


%install

%define _udevdir /lib/udev/rules.d

install -D -p -m 0755 %{SOURCE4} $RPM_BUILD_ROOT/lib/systemd/system/ksm.service
install -D -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl $RPM_BUILD_ROOT/lib/systemd/ksmctl

install -D -p -m 0755 %{SOURCE7} $RPM_BUILD_ROOT/lib/systemd/system/ksmtuned.service
install -D -p -m 0755 %{SOURCE8} $RPM_BUILD_ROOT%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/ksmtuned.conf

%ifarch %{kvm_archs}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_udevdir}

install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 scripts/kvm/kvm_stat $RPM_BUILD_ROOT%{_bindir}/
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_udevdir}
%endif

make DESTDIR=$RPM_BUILD_ROOT install

%if 0%{?need_qemu_kvm}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset

install -m 0755 qemu-kvm $RPM_BUILD_ROOT%{_bindir}/
install -m 0644 qemu-kvm.stp $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/
%endif

%if %{with kvmonly}
rm $RPM_BUILD_ROOT%{_bindir}/qemu-system-%{kvm_target}
rm $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/qemu-system-%{kvm_target}.stp
%endif

chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
install -D -p -m 0644 -t ${RPM_BUILD_ROOT}%{qemudocdir} Changelog README TODO COPYING COPYING.LIB LICENSE

install -D -p -m 0644 qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl2/qemu.conf

# Provided by package openbios
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-ppc
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-sparc32
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-sparc64
# Provided by package SLOF
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/slof.bin

# Remove possibly unpackaged files.  Unlike others that are removed
# unconditionally, these firmware files are still distributed as a binary
# together with the qemu package.  We should try to move at least s390-zipl.rom
# to a separate package...  Discussed here on the packaging list:
# https://lists.fedoraproject.org/pipermail/packaging/2012-July/008563.html
%if 0%{!?system_alpha:1}
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/palcode-clipper
%endif
%if 0%{!?system_microblaze:1}
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/petalogix*.dtb
%endif
%if 0%{!?system_ppc:1}
rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{name}/bamboo.dtb
rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{name}/ppc_rom.bin
rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{name}/spapr-rtas.bin
%endif
%if 0%{!?system_s390x:1}
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/s390-zipl.rom
%endif

# Provided by package ipxe
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/pxe*rom
# Provided by package vgabios
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/vgabios*bin
# Provided by package seabios
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/bios.bin
# Provided by package sgabios
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/sgabios.bin

%if 0%{?system_x86:1}
# the pxe gpxe images will be symlinks to the images on
# /usr/share/ipxe, as QEMU doesn't know how to look
# for other paths, yet.
pxe_link() {
  ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/%{name}/pxe-$1.rom
}

pxe_link e1000 8086100e
pxe_link ne2k_pci 10ec8029
pxe_link pcnet 10222000
pxe_link rtl8139 10ec8139
pxe_link virtio 1af41000

rom_link() {
    ln -s $1 %{buildroot}%{_datadir}/%{name}/$2
}

rom_link ../vgabios/VGABIOS-lgpl-latest.bin vgabios.bin
rom_link ../vgabios/VGABIOS-lgpl-latest.cirrus.bin vgabios-cirrus.bin
rom_link ../vgabios/VGABIOS-lgpl-latest.qxl.bin vgabios-qxl.bin
rom_link ../vgabios/VGABIOS-lgpl-latest.stdvga.bin vgabios-stdvga.bin
rom_link ../vgabios/VGABIOS-lgpl-latest.vmware.bin vgabios-vmware.bin
rom_link ../seabios/bios.bin bios.bin
rom_link ../sgabios/sgabios.bin sgabios.bin
%endif

%if 0%{?user:1}
mkdir -p $RPM_BUILD_ROOT%{_exec_prefix}/lib/binfmt.d
for i in dummy \
%ifnarch %{ix86} x86_64
    qemu-i386 \
%endif
%ifnarch alpha
    qemu-alpha \
%endif
%ifnarch arm
    qemu-arm \
%endif
    qemu-armeb \
%ifnarch mips
    qemu-mips qemu-mipsn32 qemu-mips64 \
%endif
%ifnarch mipsel
    qemu-mipsel qemu-mipsn32el qemu-mips64el \
%endif
%ifnarch m68k
    qemu-m68k \
%endif
%ifnarch ppc ppc64
    qemu-ppc \
%endif
%ifnarch sparc sparc64
    qemu-sparc \
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
  grep /$i:\$ %{SOURCE1} > $RPM_BUILD_ROOT%{_exec_prefix}/lib/binfmt.d/$i.conf
  chmod 644 $RPM_BUILD_ROOT%{_exec_prefix}/lib/binfmt.d/$i.conf
done < %{SOURCE1}
%endif

# For the qemu-guest-agent subpackage install the systemd
# service and udev rules.
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_udevdir}
install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT%{_unitdir}
install -m 0644 %{SOURCE11} $RPM_BUILD_ROOT%{_udevdir}

# Install rules to use the bridge helper with libvirt's virbr0
install -m 0644 %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/qemu
chmod u+s $RPM_BUILD_ROOT%{_libexecdir}/qemu-bridge-helper

%if %{with separate_kvm}
rm $RPM_BUILD_ROOT%{_bindir}/qemu-img
rm $RPM_BUILD_ROOT%{_bindir}/qemu-io
rm $RPM_BUILD_ROOT%{_bindir}/qemu-nbd
rm $RPM_BUILD_ROOT%{_mandir}/man1/qemu-img.1*
rm $RPM_BUILD_ROOT%{_mandir}/man8/qemu-nbd.8*

rm $RPM_BUILD_ROOT%{_bindir}/qemu-ga
rm $RPM_BUILD_ROOT%{_unitdir}/qemu-guest-agent.service
rm $RPM_BUILD_ROOT%{_udevdir}/99-qemu-guest-agent.rules
%endif
make %{?_smp_mflags} $buildldflags DESTDIR=$RPM_BUILD_ROOT install-libcacard
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f
find $RPM_BUILD_ROOT -name "libcacard.so*" -exec chmod +x \{\} \;

%check
make check

%ifarch %{kvm_archs}
%post %{kvm_package}
# load kvm modules now, so we can make sure no reboot is needed.
# If there's already a kvm module installed, we don't mess with it
sh %{_sysconfdir}/sysconfig/modules/kvm.modules || :
udevadm trigger --sysname-match=kvm || :
%endif

%if %{without separate_kvm}
%post common
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl enable ksm.service >/dev/null 2>&1 || :
    /bin/systemctl enable ksmtuned.service >/dev/null 2>&1 || :
fi

getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu

%preun common
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable ksmtuned.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable ksm.service > /dev/null 2>&1 || :
    /bin/systemctl stop ksmtuned.service > /dev/null 2>&1 || :
    /bin/systemctl stop ksm.service > /dev/null 2>&1 || :
fi

%postun common
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart ksmtuned.service >/dev/null 2>&1 || :
    /bin/systemctl try-restart ksm.service >/dev/null 2>&1 || :
fi
%endif


%if 0%{?user:1}
%post %{user}
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%postun %{user}
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%endif

%global kvm_files \
%{_sysconfdir}/sysconfig/modules/kvm.modules \
%{_udevdir}/80-kvm.rules

%if 0%{?need_qemu_kvm}
%global qemu_kvm_files \
%{_bindir}/qemu-kvm \
%{_datadir}/systemtap/tapset/qemu-kvm.stp
%endif

%files
%defattr(-,root,root)

%ifarch %{kvm_archs}
%files kvm
%defattr(-,root,root)
%endif

%files common
%defattr(-,root,root)
%dir %{qemudocdir}
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/README
%doc %{qemudocdir}/TODO
%doc %{qemudocdir}/qemu-doc.html
%doc %{qemudocdir}/qemu-tech.html
%doc %{qemudocdir}/qmp-commands.txt
%doc %{qemudocdir}/COPYING
%doc %{qemudocdir}/COPYING.LIB
%doc %{qemudocdir}/LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/keymaps/
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/virtfs-proxy-helper.1*
%{_bindir}/virtfs-proxy-helper
%{_libexecdir}/qemu-bridge-helper
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
%if %{without separate_kvm}
/lib/systemd/system/ksm.service
/lib/systemd/ksmctl
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
/lib/systemd/system/ksmtuned.service
%{_sbindir}/ksmtuned
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%endif
%dir %{_sysconfdir}/qemu
%config(noreplace) %{_sysconfdir}/qemu/bridge.conf

%if %{without separate_kvm}
%files guest-agent
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/qemu-ga
%{_unitdir}/qemu-guest-agent.service
%{_udevdir}/99-qemu-guest-agent.rules
%endif

%if 0%{?user:1}
%files %{user}
%defattr(-,root,root)
%{_exec_prefix}/lib/binfmt.d/qemu-*.conf
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-or32
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64abi32
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-unicore32
%{_datadir}/systemtap/tapset/qemu-i386.stp
%{_datadir}/systemtap/tapset/qemu-x86_64.stp
%{_datadir}/systemtap/tapset/qemu-alpha.stp
%{_datadir}/systemtap/tapset/qemu-arm.stp
%{_datadir}/systemtap/tapset/qemu-armeb.stp
%{_datadir}/systemtap/tapset/qemu-cris.stp
%{_datadir}/systemtap/tapset/qemu-m68k.stp
%{_datadir}/systemtap/tapset/qemu-microblaze.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel.stp
%{_datadir}/systemtap/tapset/qemu-mips.stp
%{_datadir}/systemtap/tapset/qemu-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-or32.stp
%{_datadir}/systemtap/tapset/qemu-ppc.stp
%{_datadir}/systemtap/tapset/qemu-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-ppc64abi32.stp
%{_datadir}/systemtap/tapset/qemu-s390x.stp
%{_datadir}/systemtap/tapset/qemu-sh4.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb.stp
%{_datadir}/systemtap/tapset/qemu-sparc.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus.stp
%{_datadir}/systemtap/tapset/qemu-sparc64.stp
%{_datadir}/systemtap/tapset/qemu-unicore32.stp
%endif

%if 0%{?system_x86:1}
%files %{system_x86}
%defattr(-,root,root)
%if %{without kvmonly}
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_datadir}/systemtap/tapset/qemu-system-i386.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64.stp
%endif
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/sgabios.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/kvmvapic.bin
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/vgabios-stdvga.bin
%{_datadir}/%{name}/vgabios-vmware.bin
%{_datadir}/%{name}/pxe-e1000.rom
%{_datadir}/%{name}/pxe-virtio.rom
%{_datadir}/%{name}/pxe-pcnet.rom
%{_datadir}/%{name}/pxe-rtl8139.rom
%{_datadir}/%{name}/pxe-ne2k_pci.rom
%{_datadir}/%{name}/cpus-x86_64.conf
%{_datadir}/%{name}/qemu-icon.bmp
%config(noreplace) %{_sysconfdir}/qemu/target-x86_64.conf
%if %{without separate_kvm}
%ifarch %{ix86} x86_64
%{?kvm_files:}
%{?qemu_kvm_files:}
%endif
%endif
%endif

%ifarch %{kvm_archs}
%files kvm-tools
%defattr(-,root,root,-)
%{_bindir}/kvm_stat
%endif

%if 0%{?system_alpha:1}
%files %{system_alpha}
%defattr(-,root,root)
%{_bindir}/qemu-system-alpha
%{_datadir}/systemtap/tapset/qemu-system-alpha.stp
%{_datadir}/%{name}/palcode-clipper
%endif

%if 0%{?system_arm:1}
%files %{system_arm}
%defattr(-,root,root)
%{_bindir}/qemu-system-arm
%{_datadir}/systemtap/tapset/qemu-system-arm.stp
%endif

%if 0%{?system_mips:1}
%files %{system_mips}
%defattr(-,root,root)
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%{_datadir}/systemtap/tapset/qemu-system-mips.stp
%{_datadir}/systemtap/tapset/qemu-system-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64el.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64.stp
%endif

%if 0%{?system_cris:1}
%files %{system_cris}
%defattr(-,root,root)
%{_bindir}/qemu-system-cris
%{_datadir}/systemtap/tapset/qemu-system-cris.stp
%endif

%if 0%{?system_lm32:1}
%files %{system_lm32}
%defattr(-,root,root)
%{_bindir}/qemu-system-lm32
%{_datadir}/systemtap/tapset/qemu-system-lm32.stp
%endif

%if 0%{?system_m68k:1}
%files %{system_m68k}
%defattr(-,root,root)
%{_bindir}/qemu-system-m68k
%{_datadir}/systemtap/tapset/qemu-system-m68k.stp
%endif

%if 0%{?system_microblaze:1}
%files %{system_microblaze}
%defattr(-,root,root)
%{_bindir}/qemu-system-microblaze
%{_bindir}/qemu-system-microblazeel
%{_datadir}/systemtap/tapset/qemu-system-microblaze.stp
%{_datadir}/systemtap/tapset/qemu-system-microblazeel.stp
%{_datadir}/%{name}/petalogix*.dtb
%endif

%if 0%{?system_or32:1}
%files %{system_or32}
%defattr(-,root,root)
%{_bindir}/qemu-system-or32
%{_datadir}/systemtap/tapset/qemu-system-or32.stp
%endif

%if 0%{?system_s390x:1}
%files %{system_s390x}
%defattr(-,root,root)
%{_bindir}/qemu-system-s390x
%{_datadir}/systemtap/tapset/qemu-system-s390x.stp
%{_datadir}/%{name}/s390-zipl.rom
%ifarch s390x
%{?kvm_files:}
%{?qemu_kvm_files:}
%endif
%endif

%if 0%{?system_sh4:1}
%files %{system_sh4}
%defattr(-,root,root)
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb
%{_datadir}/systemtap/tapset/qemu-system-sh4.stp
%{_datadir}/systemtap/tapset/qemu-system-sh4eb.stp
%endif

%if 0%{?system_sparc:1}
%files %{system_sparc}
%defattr(-,root,root)
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-sparc64
%{_datadir}/systemtap/tapset/qemu-system-sparc.stp
%{_datadir}/systemtap/tapset/qemu-system-sparc64.stp
%endif

%if 0%{?system_ppc:1}
%files %{system_ppc}
%defattr(-,root,root)
%if %{without kvmonly}
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
%{_bindir}/qemu-system-ppcemb
%{_datadir}/systemtap/tapset/qemu-system-ppc.stp
%{_datadir}/systemtap/tapset/qemu-system-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-system-ppcemb.stp
%endif
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/ppc_rom.bin
%{_datadir}/%{name}/spapr-rtas.bin
%ifarch ppc64
%{?kvm_files:}
%{?qemu_kvm_files:}
%endif
%endif

%if 0%{?system_unicore32:1}
%files %{system_unicore32}
%defattr(-,root,root)
%{_bindir}/qemu-system-unicore32
%{_datadir}/systemtap/tapset/qemu-system-unicore32.stp
%endif

%if 0%{?system_xtensa:1}
%files %{system_xtensa}
%defattr(-,root,root)
%{_bindir}/qemu-system-xtensa
%{_bindir}/qemu-system-xtensaeb
%{_datadir}/systemtap/tapset/qemu-system-xtensa.stp
%{_datadir}/systemtap/tapset/qemu-system-xtensaeb.stp
%endif

%if %{without separate_kvm}
%files img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*
%endif


%files -n libcacard
%defattr(-,root,root,-)
%{_libdir}/libcacard.so.*

%files -n libcacard-tools
%defattr(-,root,root,-)
%{_bindir}/vscclient

%files -n libcacard-devel
%defattr(-,root,root,-)
%{_includedir}/cacard
%{_libdir}/libcacard.so
%{_libdir}/pkgconfig/libcacard.pc

%changelog
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

* Mon Mar 11 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-4
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

* Fri Jan 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.1.2-3
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

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Feb 13 2005 David Woodhouse <dwmw2@infradead.org> 0.6.1-2
- Package cleanup

* Sun Nov 21 2004 David Woodhouse <dwmw2@redhat.com> 0.6.1-1
- Update to 0.6.1

* Tue Jul 20 2004 David Woodhouse <dwmw2@redhat.com> 0.6.0-2
- Compile fix from qemu CVS, add x86_64 host support

* Mon May 12 2004 David Woodhouse <dwmw2@redhat.com> 0.6.0-1
- Update to 0.6.0.

* Sat May 8 2004 David Woodhouse <dwmw2@redhat.com> 0.5.5-1
- Update to 0.5.5.

* Thu May 2 2004 David Woodhouse <dwmw2@redhat.com> 0.5.4-1
- Update to 0.5.4.

* Thu Apr 22 2004 David Woodhouse <dwmw2@redhat.com> 0.5.3-1
- Update to 0.5.3. Add init script.

* Thu Jul 17 2003 Jeff Johnson <jbj@redhat.com> 0.4.3-1
- Create.
