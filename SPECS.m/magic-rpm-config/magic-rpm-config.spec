#                        TO WHOM IT MAY CONCERN
#
# 1) Don't add patches, dist-git is the upstream repository for this package.
# 2) When making changes, update version by +1, leave release alone.
#

Summary: Magic specific rpm configuration files
Summary(zh_CN.UTF-8): Magic 特定的 rpm 配置文件
Name: magic-rpm-config
Version: 3.0
Release: 11%{?dist}
# No version specified.
License: GPL+
Group: Development/System
Group(zh_CN.UTF-8): 开发/系统
URL: http://pkgs.fedoraproject.org/cgit/redhat-rpm-config.git

# Core rpm settings
Source0: macros
Source1: rpmrc

# gcc specs files for hardened builds
Source50: magic-hardened-cc1
Source51: magic-hardened-ld

# 清理无用语言文件脚本
Source60: magic_rpm_clean.sh

# The macros defined by these files are for things that need to be defined
# at srpm creation time when it is not feasible to require the base packages
# that would otherwise be providing the macros. other language/arch specific
# macros should not be defined here but instead in the base packages that can
# be pulled in at rpm build time, this is specific for srpm creation.
Source101: macros.gnat-srpm
Source102: macros.mono-srpm
Source103: macros.nodejs-srpm

# Other misc macros
Source150: macros.dwz
Source151: macros.kmp

# Build policy scripts
Source201: brp-implant-ident-static
Source202: brp-java-repack-jars

# Dependency generator scripts (deprecated)
Source300: find-provides
Source301: find-provides.ksyms
Source304: find-requires
Source305: find-requires.ksyms
Source308: firmware.prov
Source309: modalias.prov

# Misc helper scripts
Source400: dist.sh
Source401: rpmsort
Source402: symset-table
Source403: kmodtool

# 16082013 snapshots from http://git.savannah.gnu.org/gitweb/?p=config.git
Source500: config.guess
Source501: config.sub

# Dependency generators & their rules
Source600: kmod.attr
Source601: kmod.prov
Source602: libsymlink.attr

BuildArch: noarch
Requires: coreutils
Requires: perl-srpm-macros
Requires: ocaml-srpm-macros
Requires: ghc-srpm-macros
Requires: rpm >= 4.11.0
Requires: dwz >= 0.4
Requires: zip
Provides: system-rpm-config = %{version}-%{release}

%global rrcdir /usr/lib/rpm/magic

%description
Red Hat specific rpm configuration files.

%package -n kernel-rpm-macros
Summary: Macros and scripts for building kernel module packages.
Requires: magic-rpm-config >= 3.0

%description -n kernel-rpm-macros
Macros and scripts for building kernel module packages.

%prep
# Not strictly necessary but allows working on file names instead
# of source numbers in install section
%setup -c -T
cp -p %{sources} .

%install
mkdir -p %{buildroot}%{rrcdir}
install -p -m 644 -t %{buildroot}%{rrcdir} macros rpmrc
install -p -m 444 -t %{buildroot}%{rrcdir} magic-hardened-*
install -p -m 755 -t %{buildroot}%{rrcdir} config.*
install -p -m 755 -t %{buildroot}%{rrcdir} dist.sh rpmsort symset-table kmodtool
install -p -m 755 -t %{buildroot}%{rrcdir} brp-*

install -p -m 755 -t %{buildroot}%{rrcdir} find-*
mkdir -p %{buildroot}%{rrcdir}/find-provides.d
install -p -m 644 -t %{buildroot}%{rrcdir}/find-provides.d firmware.prov modalias.prov

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 644 -t %{buildroot}%{_rpmconfigdir}/macros.d macros.*

mkdir -p %{buildroot}%{_fileattrsdir}
install -p -m 644 -t %{buildroot}%{_fileattrsdir} *.attr
install -p -m 755 -t %{buildroot}%{_rpmconfigdir} kmod.prov

mkdir -p %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} magic_rpm_clean.sh

%files
%dir %{rrcdir}
%{_bindir}/magic_rpm_clean.sh
%{rrcdir}/macros
%{rrcdir}/rpmrc
%{rrcdir}/brp-*
%{rrcdir}/dist.sh
%{rrcdir}/magic-hardened-*
%{rrcdir}/config.*
%{rrcdir}/find-provides
%{rrcdir}/find-requires
%{_fileattrsdir}/*.attr
%{_rpmconfigdir}/kmod.prov
%{_rpmconfigdir}/macros.d/macros.*-srpm
%{_rpmconfigdir}/macros.d/macros.dwz

%files -n kernel-rpm-macros
%dir %{rrcdir}/find-provides.d
%{rrcdir}/kmodtool
%{rrcdir}/rpmsort
%{rrcdir}/symset-table
%{rrcdir}/find-provides.ksyms
%{rrcdir}/find-requires.ksyms
%{rrcdir}/find-provides.d/firmware.prov
%{rrcdir}/find-provides.d/modalias.prov
%{_rpmconfigdir}/macros.d/macros.kmp

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 3.0-11
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 3.0-10
- 为 Magic 3.0 重建

* Wed Jul 29 2015 Liu Di <liudidi@gmail.com> - 3.0-9
- 为 Magic 3.0 重建

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 3.0-8
- 为 Magic 3.0 重建

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 3.0-7
- 为 Magic 3.0 重建

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 3.0-3
- 为 Magic 3.0 重建


