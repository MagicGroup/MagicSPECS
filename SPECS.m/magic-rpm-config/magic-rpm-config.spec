Summary: Magic specific rpm configuration files
Name: magic-rpm-config
Version: 3.0
Release: 6%{?dist}
# No version specified.
License: GPL+
Group: Development/System
URL: http://git.fedorahosted.org/git/redhat-rpm-config
Source: magic-rpm-config-%{version}.tar.xz

# these two implement automagic {c,ld}flags mangling for additional ELF
# hardening when _hardened_build is defined in a spec file.  gcc 4.6.1-7.fc16
# or newer is needed for these to work; prior to that *self_specs was not
# exposed.  If anything goes wrong, blame ajax@
Source1: magic-hardened-cc1
Source2: magic-hardened-ld
Source3: magic_rpm_clean.sh

# up-to-date copies of config.guess and config.sub (from automake 1.13.1)
Source10: config.guess
Source11: config.sub

Patch0: magic-rpm-config-3.0-strict-python-bytecompile.patch
Patch1: magic-rpm-config-3.0-fix-requires.patch
Patch2: magic-rpm-config-3.0-no-strip-note.patch
Patch3: magic-rpm-config-3.0-pkgconfig-private.patch
# the macros defined by this patch are for things that need to be defined
# at srpm creation time when it is not feasable to require the base packages
# that would otherwise be providing the macros. other language/arch specific
# macros should not be defined here but instead in the base packages that can
# be pulled in at rpm build time, this is specific for srpm creation.
Patch4: magic-rpm-config-3.0-arches-macros.patch
Patch5: magic-rpm-config-3.0-arm.patch
Patch6: magic-rpm-config-3.0-relro.patch
Patch7: magic-rpm-config-3.0-hardened.patch
Patch8: magic-rpm-config-3.0-ppc-no-minimal-toc.patch
Patch9: magic-rpm-config-3.0-dwz.patch
Patch10: magic-rpm-config-3.0-minidebuginfo.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=783433
Patch11: magic-rpm-config-3.0-python-hardlink-spaces-in-filenames.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=853216
Patch12:magic-rpm-config-3.0-use-prefix-macro.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=648996
Patch13: magic-rpm-config-3.0-kernel-source.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=465664
Patch14: magic-rpm-config-3.0-java-repack-order.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=741089
Patch15: 0001-Drop-un-setting-LANG-and-DISPLAY-in-various-build-st.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=783932
Patch16: magic-rpm-config-3.0-filtering-spaces-in-filename.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=872737
Patch17: magic-rpm-config-3.0-java-repack-spaces-in-filenames.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=951669
Patch18: magic-rpm-config-3.0-record-switches.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=951442
Patch19: magic-rpm-config-3.0-configfoo.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=909788
Patch20: magic-rpm-config-3.0-aarch64.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=914831
Patch21: magic-rpm-config-3.0-fcflags.patch
BuildArch: noarch
Requires: coreutils
Requires: perl-srpm-macros
Requires: rpm >= 4.8.0
Requires: dwz >= 0.4
Requires: zip
Provides: system-rpm-config = %{version}-%{release}

%description
Magic specific rpm configuration files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1

%build

%install
make DESTDIR=${RPM_BUILD_ROOT} install
install -m 0444 %{SOURCE1} %{SOURCE2} ${RPM_BUILD_ROOT}/usr/lib/rpm/magic
install -m 0775 %{SOURCE10} %{SOURCE11} ${RPM_BUILD_ROOT}/usr/lib/rpm/magic
find ${RPM_BUILD_ROOT} -name \*.orig -delete
# buggy makefile in 9.1.0 leaves changelog in wrong place
find ${RPM_BUILD_ROOT} -name ChangeLog -delete
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
install -m 0755 %{SOURCE3} ${RPM_BUILD_ROOT}%{_bindir}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc ChangeLog
%{_bindir}/magic*
%{_prefix}/lib/rpm/magic
%{_sysconfdir}/rpm/*

%changelog

