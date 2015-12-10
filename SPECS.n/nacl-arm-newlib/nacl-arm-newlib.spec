%global gitver 373135e

%define __debug_install_post : > %{_builddir}/%{?buildsubdir}/debugfiles.list
%define debug_package %{nil}

Name:		nacl-arm-newlib
Summary:	C library intended for use on embedded systems
Version:	2.1.0
Release:	3.git%{gitver}%{?dist}
# Generated from git
# git clone https://chromium.googlesource.com/native_client/nacl-newlib
# (Checkout ID taken from native_client/toolchain_build/toolchain_build.py
# well... it used to be there anyways. Now just look at the latest checkout.
# cd nacl-newlib
# git checkout 373135ec5241d09138aa56603742b94b3b64ea1d
# cd ..
# For newlib version, grep PACKAGE_VERSION newlib/libm/configure
# mv nacl-newlib nacl-arm-newlib-2.1.0-git373135e
# tar --exclude-vcs -cjf nacl-arm-newlib-2.1.0-git373135e.tar.bz2 nacl-arm-newlib-2.1.0-git373135e
License:	BSD and MIT and LGPLv2+
Source0:	nacl-arm-newlib-%{version}-git%{gitver}.tar.bz2
# We need to copy some missing header files from chromium
# mkdir ~/nacl-headers-42.0.2311.135
# cd chromium-42.0.2311.135/native_client/
# ./src/trusted/service_runtime/export_header.py src/trusted/service_runtime/include ~/nacl-headers-42.0.2311.135/
# cd ~/nacl-headers-42.0.2311.135
# tar cfj ~/nacl-headers-42.0.2311.135.tar.bz2 .
Source1:	nacl-headers-42.0.2311.135.tar.bz2
# Taken from chromium-42.0.2311.135/native_client/tools/newlib-libc-script
Source2:	newlib-libc-script
# Taken from chromium-42.0.2311.135/native_client/src/untrusted/pthread/pthread.h
Source3:	pthread.h
# Taken from chromium-42.0.2311.135/native_client/src/untrusted/pthread/semaphore.h
Source4:	semaphore.h
# Taken from chromium-42.0.2311.135/native_client/src/untrusted/stubs/crt1.x
Source5:	crt1.x
URL:		http://sourceware.org/newlib/
BuildRequires:	nacl-arm-binutils nacl-arm-gcc texinfo
ExclusiveArch:	i686 x86_64
# This is to avoid the duplicate iconv bits
Requires:	nacl-newlib


%description
Newlib is a C library intended for use on embedded systems. It is a 
conglomeration of several library parts, all under free software licenses
that make them easily usable on embedded products. This is the nacl fork.

%prep
%setup -q -n %{name}-%{version}-git%{?gitver}
pushd newlib/libc/sys/nacl
tar xf %{SOURCE1}
popd
cp -a %{SOURCE2} .

%build
# export NEWLIB_CFLAGS="-O2 -D_I386MACH_ALLOW_HW_INTERRUPTS -DSIGNAL_PROVIDED -mtls-use-call -fPIC"
%configure \
	--disable-libgloss \
	--enable-newlib-iconv \
	--enable-newlib-io-long-long \
	--enable-newlib-io-long-double \
	--enable-newlib-io-c99-formats \
	--enable-newlib-mb \
	libc_cv_initfinit_array=yes \
	CFLAGS="-O2 -fPIC" \
	--target=arm-nacl

make

%install
make DESTDIR=%{buildroot} install

# Conflicts with binutils
rm -rf %{buildroot}%{_infodir}/

# The default pthread.h doesn't work right?
rm -rf %{buildroot}%{_prefix}/arm-nacl/include/pthread.h
cp %{SOURCE3} %{buildroot}%{_prefix}/arm-nacl/include/
cp %{SOURCE4} %{buildroot}%{_prefix}/arm-nacl/include/

# We have to hack up libc.a to get things working.

# 64bit (default)
mv %{buildroot}%{_prefix}/arm-nacl/lib/libc.a %{buildroot}%{_prefix}/arm-nacl/lib/libcrt_common.a
sed 's|@OBJFORMAT@|"elf32-littlearm-nacl", "elf32-bigarm-nacl", "elf32-littlearm-nacl"|' newlib-libc-script > %{buildroot}%{_prefix}/arm-nacl/lib/libc.a
cp -a %{SOURCE5} %{buildroot}%{_prefix}/arm-nacl/lib/crt1.o
# These bits are identical in the nacl-newlib package, so we'll use them from there.
rm -rf %{buildroot}%{_datadir}

%files
# %%{_datadir}/iconv_data/
%{_prefix}/arm-nacl/include/
%{_prefix}/arm-nacl/lib/

%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 2.1.0-3.git373135e
- 为 Magic 3.0 重建

* Thu Oct  1 2015 Tom Callaway <spot@fedoraproject.org> 2.1.0-2.git373135e
- new stuff

* Sat May 23 2015 Tom Callaway <spot@fedoraproject.org> 2.1.0-1.gitbf66148
- initial package (chromium 42)
