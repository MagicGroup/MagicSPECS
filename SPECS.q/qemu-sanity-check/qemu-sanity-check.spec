# _hardened_build breaks building the static 'init' binary.
# https://bugzilla.redhat.com/1204162
%undefine _hardened_build

%global debug_package %{nil}

Name:            qemu-sanity-check
Version:         1.1.5
Release:         6%{?dist}
Summary:         Simple qemu and Linux kernel sanity checker
Summary(zh_CN.UTF-8): 简单的 qemu 和 Linux 内核完整性检查
License:         GPLv2+

URL:             http://people.redhat.com/~rjones/qemu-sanity-check
Source0:         http://people.redhat.com/~rjones/qemu-sanity-check/files/%{name}-%{version}.tar.gz

# Non-upstream patch to disable test which fails on broken kernels
# which don't respond to panic=1 option properly.
Patch4:          0004-Disable-bad-userspace-test-Fedora-only.patch

# Because the above patch touches configure.ac/Makefile.am:
BuildRequires:   autoconf, automake

# For building manual pages.
BuildRequires:   /usr/bin/perldoc

# For building the initramfs.
BuildRequires:   cpio
BuildRequires:   glibc-static

# BuildRequire these in order to let 'make check' run.  These are
# not required unless you want to run the tests.  Note don't run the
# tests on ARM since qemu isn't likely to work.
%ifarch %{ix86} x86_64
BuildRequires:   qemu-system-x86
%endif

BuildRequires:   kernel

# For complicated reasons, this is required so that
# /bin/kernel-install puts the kernel directly into /boot, instead of
# into a /boot/<machine-id> subdirectory (in Fedora >= 23).  Read the
# kernel-install script to understand why.
BuildRequires: grubby

%ifarch %{ix86} x86_64
Requires:        qemu-system-x86
%endif
%ifarch armv7hl
Requires:        qemu-system-arm
%endif

Requires:        kernel

# Require the -nodeps subpackage.
Requires:        %{name}-nodeps = %{version}-%{release}


%description
Qemu-sanity-check is a short shell script that test-boots a Linux
kernel under qemu, making sure it boots up to userspace.  The idea is
to test the Linux kernel and/or qemu to make sure they are working.

Most users should install the %{name} package.

If you are testing qemu or the kernel in those packages and you want
to avoid a circular dependency on qemu or kernel, you should use
'BuildRequires: %{name}-nodeps' instead.

%description -l zh_CN.UTF-8
简单的 qemu 和 Linux 内核完整性检查。

%package nodeps
Summary:         Simple qemu and Linux kernel sanity checker (no dependencies)
Summary(zh_CN.UTF-8): 简单的 qemu 和 Linux 内核完整性检查（无依赖）
License:         GPLv2+


%description nodeps
This is the no-depedencies version of %{name}.  It is exactly the same
as %{name} except that this package does not depend on qemu or kernel.

%description nodeps -l zh_CN.UTF-8
简单的 qemu 和 Linux 内核完整性检查（无依赖）

%prep
%setup -q

%patch4 -p1

# Rerun autotools because the patches touch configure.ac and Makefile.am.
autoreconf -i


%build
# NB: canonical_arch is a variable in the final script, so it
# has to be escaped here.
%configure --with-qemu-list="qemu-system-\$canonical_arch" || {
  cat config.log
  exit 1
}
make %{?_smp_mflags}


%check
%ifarch %{ix86} x86_64
make check || {
  cat test-suite.log
  exit 1
}
%endif


%install
make DESTDIR=$RPM_BUILD_ROOT install
magic_rpm_clean.sh

%files
%doc COPYING


%files nodeps
%doc COPYING README
%{_bindir}/qemu-sanity-check
%{_libdir}/qemu-sanity-check
%{_mandir}/man1/qemu-sanity-check.1*


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.1.5-6
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 1.1.5-5
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Richard W.M. Jones <rjones@redhat.com> - 1.1.5-4
- +BR grubby.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1.1.5-1
- New upstream version 1.1.5.
- Adds --accel option to select qemu acceleration mode.
- Remove upstream patch.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 28 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.4-2
- New upstream version 1.1.4.
- Remove 3 x patches which are now upstream.
- This version can handle debug kernels (RHBZ#1002189).

* Thu Aug 22 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.3-4
- +BR autoconf, automake.
- Run autoreconf after patching.

* Thu Aug 22 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.3-2
- Fedora kernels don't respond properly to panic=1 parameter (appears
  to be related to having debug enabled).  Add some upstream and one
  non-upstream patches to work around this.

* Thu Aug 22 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.3-1
- Initial release (RHBZ#999108).
