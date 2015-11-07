Name: uClibc
Version: 0.9.33.2
Release: 9%{?dist}
Summary: C library for embedded Linux
Summary(zh_CN.UTF-8): 嵌入式 Linux 使用的 C 库

Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License: LGPLv2
URL: http://www.uclibc.org/
Source0: http://www.uclibc.org/downloads/%{name}-%{version}.tar.xz
Source1: uClibc.config
Patch1: uClibc-0.9.33.2_kernel_long.patch

# This package only contains a static library
%global debug_package %{nil}

# uclibc doesnot support ppc64 aarch64
ExcludeArch: ppc64 aarch64

%description
uClibc is a C library for developing embedded Linux systems.
It is much smaller than the GNU C Library, but nearly all applications
supported by glibc also work perfectly with uClibc.

%description -l zh_CN.UTF-8
嵌入式 Linux 使用的 C 库。

%package devel
Summary: Header files and libraries for uClibc library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Provides: uClibc-static = %{version}-%{release}

%description devel
uClibc is a C library for developing embedded Linux systems.
It is much smaller than the GNU C Library, but nearly all applications
supported by glibc also work perfectly with uClibc.
This package contains the header files and libraries
needed for uClibc package.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{version}
%patch1 -b .kernel_long -p1

cat %{SOURCE1} >.config1
iconv -f windows-1252 -t utf-8 README >README.pom
mv README.pom README

%build
mkdir kernel-include
cp -a /usr/include/asm kernel-include
cp -a /usr/include/asm-generic kernel-include
cp -a /usr/include/linux kernel-include

arch=`uname -m | sed -e 's/i.86/i386/' -e 's/ppc/powerpc/' -e 's/armv7l/arm/' -e 's/armv5tel/arm/'`
echo "TARGET_$arch=y" >.config
echo "TARGET_ARCH=\"$arch\"" >>.config
%ifarch %{arm}
echo "CONFIG_ARM_EABI=y" >>.config
echo "ARCH_ANY_ENDIAN=n" >>.config
echo "ARCH_LITTLE_ENDIAN=y" >>.config
echo "ARCH_WANTS_LITTLE_ENDIAN=y" >>.config
%endif
cat .config1 >>.config

yes "" | make oldconfig %{?_smp_mflags}
make V=1 %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT/lib
make install PREFIX="$RPM_BUILD_ROOT/"
make install_headers PREFIX="$RPM_BUILD_ROOT/" DEVEL_PREFIX=""
cp -a kernel-include/* $RPM_BUILD_ROOT/include/

# move libraries to proper subdirectory
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/uClibc
mv  $RPM_BUILD_ROOT/lib/*  $RPM_BUILD_ROOT/%{_libdir}/uClibc/
rm -rf  $RPM_BUILD_ROOT/lib/

# move the header files to /usr subdirectory
mkdir -p $RPM_BUILD_ROOT/%{_includedir}/uClibc
mv  $RPM_BUILD_ROOT/include/*  $RPM_BUILD_ROOT/%{_includedir}/uClibc
rm -rf  $RPM_BUILD_ROOT/include/
magic_rpm_clean.sh

%files devel
%defattr(-,root,root,-)
%doc README docs/Glibc_vs_uClibc_Differences.txt docs/threads.txt docs/uClibc_vs_SuSv3.txt
%doc TODO DEDICATION.mjn3 MAINTAINERS
%doc docs/PORTING COPYING.LIB
%{_includedir}/uClibc
%{_libdir}/uClibc

%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 0.9.33.2-9
- 为 Magic 3.0 重建

* Fri Oct 16 2015 Liu Di <liudidi@gmail.com> - 0.9.33.2-8
- 为 Magic 3.0 重建

* Tue Jun 30 2015 Liu Di <liudidi@gmail.com> - 0.9.33.2-7
- 为 Magic 3.0 重建

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.33.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.33.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.33.2-5
- No aarch64 support

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.33.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May  6 2013 Denys Vlasenko <dvlasenko@redhat.com> - 0.9.32-3
- Enable UCLIBC_HAS_RESOLVER_SUPPORT, UCLIBC_LINUX_MODULE_26,
  UCLIBC_HAS_SHA256/512_CRYPT_IMPL, UCLIBC_HAS_FOPEN_CLOSEEXEC_MODE
  config options.
- fix __kernel_long_t problem.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.33.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Peter Schiffer <pschiffe@redhat.com> - 0.9.33.2-1
- resolves: #771041
  update to 0.9.33.2

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 18 2011 Peter Schiffer <pschiffe@redhat.com> - 0.9.32-2
- fixed compile error on i686

* Tue Aug 16 2011 Peter Schiffer <pschiffe@redhat.com> - 0.9.32-1
- resolves: #712040
  resolves: #716134
  update to 0.9.32 final

* Mon Jun 13 2011 Peter Robinson <pbrobinson@gmail.com> - 0.9.32-0.5.rc2
- And set the ARM build to little endian

* Sat Jun 11 2011 Peter Robinson <pbrobinson@gmail.com> - 0.9.32-0.4.rc2
- It seems we need to set the ARM ABI to EABI too

* Sat Jun 11 2011 Peter Robinson <pbrobinson@gmail.com> - 0.9.32-0.3.rc2
- Add support for ARM

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.32-0.2.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Tom Callaway <spot@fedoraproject.org> - 0.9.32-0.1.rc2
- update config for 0.9.32-rc2, busybox
- patch getutent

* Tue Nov  9 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.9.31-2
- update to 0.9.31

* Fri Jun  5 2009 Ivana Varekova <varekova@redhat.com> - 0.9.30.1-2
- initial build for Red Hat
