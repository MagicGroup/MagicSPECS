%global debug_package %{nil}
%global gitcommit 0cf13c015762a9fc573d2219a30100b8f4bf4cc2

Name:		native_client
Summary:	Google Native Client Toolchain
# We'll just resync this when Chromium changes. It's fun!
Version:	46.0.2490.71
Epoch:		1
Release:	3%{?dist}
# Notes: https://sites.google.com/a/chromium.org/dev/nativeclient/pnacl/building-pnacl-components-for-distribution-packagers
# New model for prepping source:
# git branch and rev comes from 
# grep "native_client.git" chromium-46.0.2490.71/DEPS
# NEW: git clone https://chromium.googlesource.com/native_client/src/native_client
# cd native_client
# git checkout 0cf13c015762a9fc573d2219a30100b8f4bf4cc2
# toolchain_build/toolchain_build_pnacl.py --sync-only --verbose --disable-git-cache --no-use-remote-cache --no-use-cached-results
# cd ..
# tar -cJf native_client-46.0.2490.71.tar.xz native_client
License:	BSD and GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and NCSA and MIT
Source0:	%{name}-%{version}.tar.xz
# svn export http://src.chromium.org/native_client/trunk/src/third_party/scons-2.0.1
# tar -cJf scons-2.0.1-nacl.tar.xz scons-2.0.1/
Source1:	scons-2.0.1-nacl.tar.xz
Source2:	i686-nacl-gcc
# svn checkout http://google-breakpad.googlecode.com/svn/trunk/ breakpad
# tar -cJf breakpad-svn1455.tar.xz breakpad/
Source3:	breakpad-svn1455.tar.xz
Patch0:		native_client-gcc-build-fix.patch
Patch1:		native_client-disable-errors.patch
# it normally expects the breakpad source to be unpacked one level higher than the native_client root
# but that's messy. we put it in the one place it is used instead.
Patch4:		native_client-use-local-breakpad.patch
# Use system gcc instead of llvm from wherever.
Patch5:		native_client-system-clang.patch
URL:		http://src.chromium.org/viewvc/native_client/
ExclusiveArch:	i686 x86_64
BuildRequires:	glibc-devel, texinfo, bison, gettext, flex, zlib-devel
BuildRequires:	/usr/bin/pod2man
BuildRequires:	/usr/bin/pod2html
BuildRequires:	groff, libffi-devel, libtool-ltdl-devel, ncurses-devel
BuildRequires:	cmake, python, zip, git, subversion
BuildRequires:	nacl-gcc, nacl-binutils, nacl-newlib
BuildRequires:	nacl-arm-gcc, nacl-arm-binutils, nacl-arm-newlib
BuildRequires:	glibc-devel(x86-32)
# Hold your nose.
# The two binutils are not a packaging mistake.
# compiler-rt and subzero have no versioning I can find.
Provides: bundled(valgrind) = 3.6
Provides: bundled(clang) = 3.7.0
Provides: bundled(breakpad) = 0.1
Provides: bundled(scons) = 2.0.1
Provides: bundled(binutils) = 2.25
Provides: bundled(binutils) = 2.24
Provides: bundled(compiler-rt)
Provides: bundled(llvm) = 3.7.0
Provides: bundled(gcc) = 4.6.2
Provides: bundled(libcxx) = 1.0
Provides: bundled(libcxxabi) = 3.6.0
Provides: bundled(newlib) = 2.1.0
Provides: bundled(subzero)

%description
Google's "pnacl" toolchain for native client support in Chromium. Depends on
their older "nacl" toolchain, packaged separately.

%prep
%setup -q -n %{name} -a1
%patch0 -p1 -b .gccfix
%patch1 -p1 -b .no-errors
%patch4 -p1 -b .local-breakpad
%patch5 -p1 -b .system-clang

mkdir -p toolchain/linux_x86/nacl_x86_newlib_raw/bin
cp -a %{SOURCE2} toolchain/linux_x86/nacl_x86_newlib_raw/bin
chmod +x toolchain/linux_x86/nacl_x86_newlib_raw/bin/i686-nacl-gcc

mkdir -p toolchain/linux_x86/nacl_arm_newlib_raw/bin

pushd src/untrusted/minidump_generator
tar xvf %{SOURCE3}
popd

pushd toolchain/linux_x86/nacl_x86_newlib_raw/bin
ln -s /usr/bin/x86_64-nacl-gcc x86_64-nacl-gcc
ln -s /usr/bin/x86_64-nacl-g++ x86_64-nacl-g++
ln -s /usr/bin/x86_64-nacl-ar x86_64-nacl-ar
ln -s /usr/bin/x86_64-nacl-as x86_64-nacl-as
ln -s /usr/bin/x86_64-nacl-ranlib x86_64-nacl-ranlib
ln -s /usr/bin/x86_64-nacl-strip x86-64-nacl-strip
ln -s /usr/bin/x86_64-nacl-ld x86_64-nacl-ld
popd

pushd toolchain/linux_x86/nacl_x86_newlib_raw
ln -s /usr/x86_64-nacl/lib lib
ln -s /usr/x86_64-nacl x86_64-nacl
popd

pushd toolchain/linux_x86/nacl_arm_newlib_raw/bin
ln -s /usr/bin/arm-nacl-gcc arm-nacl-gcc
ln -s /usr/bin/arm-nacl-g++ arm-nacl-g++
ln -s /usr/bin/arm-nacl-ar arm-nacl-ar
ln -s /usr/bin/arm-nacl-as arm-nacl-as
ln -s /usr/bin/arm-nacl-ranlib arm-nacl-ranlib
ln -s /usr/bin/arm-nacl-strip arm-nacl-strip
ln -s /usr/bin/arm-nacl-ld arm-nacl-ld
popd

pushd toolchain/linux_x86/nacl_arm_newlib_raw
ln -s /usr/arm-nacl/lib lib
ln -s /usr/arm-nacl arm-nacl
popd

pushd toolchain/linux_x86
ln -s nacl_x86_newlib_raw nacl_x86_newlib
popd

%if 0

mkdir -p toolchain/linux_x86_newlib
pushd toolchain/linux_x86_newlib
popd
mkdir -p toolchain/linux_x86_nacl_x86
pushd toolchain/linux_x86_nacl_x86
ln -s ../linux_x86_newlib nacl_x86_newlib
popd
ln -s /usr/x86_64-nacl/lib/ldscripts ldscripts

%endif

%build
export PYTHONPATH=$PYTHONPATH:`pwd`/scons-2.0.1/engine
toolchain_build/toolchain_build_pnacl.py --verbose --clobber --gcc --no-use-cached-results --no-use-remote-cache --build-sbtc
build/package_version/package_version.py --packages pnacl_newlib --tar-dir toolchain_build/out/packages --dest-dir toolchain/ extract --skip-missing
build/package_version/package_version.py --packages pnacl_translator --tar-dir toolchain_build/out/packages --dest-dir toolchain/ extract --skip-missing

# PNACL_VERBOSE=true pnacl/build.sh translator-all
# touch toolchain/linux_x86/pnacl_translator/pnacl_translator.json

%if 0
pushd pnacl
yes | ./build.sh build-all
./build.sh driver-install-translator
popd
%endif

./toolchain/linux_x86/pnacl_newlib/bin/pnacl-ranlib toolchain/linux_x86/pnacl_newlib/x86_64_bc-nacl/lib/libc.a
./toolchain/linux_x86/pnacl_newlib/bin/pnacl-ranlib toolchain/linux_x86/pnacl_newlib/x86_64_bc-nacl/lib/libc++.a
./toolchain/linux_x86/pnacl_newlib/bin/pnacl-ranlib toolchain/linux_x86/pnacl_newlib/x86_64_bc-nacl/lib/libg.a
./toolchain/linux_x86/pnacl_newlib/bin/pnacl-ranlib toolchain/linux_x86/pnacl_newlib/x86_64_bc-nacl/lib/libm.a
# ./toolchain/linux_x86/pnacl_newlib/bin/pnacl-ranlib toolchain/linux_x86/pnacl_newlib/x86_64_bc-nacl/lib/libstdc++.a
./toolchain/linux_x86/pnacl_newlib/bin/pnacl-ranlib toolchain/linux_x86/pnacl_newlib/lib/clang/3.7.0/lib/x86_64_bc-nacl/libpnaclmm.a


%install
mkdir -p %{buildroot}/usr
cp -a toolchain/linux_x86/pnacl_newlib %{buildroot}/usr
cp -a toolchain/linux_x86/pnacl_translator %{buildroot}/usr
# touch %%{buildroot}/usr/pnacl_translator/SOURCE_SHA1
# Fix perms
chmod 755 %{buildroot}/usr/pnacl_newlib/bin/pnacl-*
touch %{buildroot}/usr/pnacl_newlib/stamp.untar
touch %{buildroot}/usr/pnacl_newlib/stamp.prep
touch %{buildroot}/usr/pnacl_translator/stamp.untar
touch %{buildroot}/usr/pnacl_translator/stamp.prep

%files
/usr/pnacl_newlib
/usr/pnacl_translator

%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 1:46.0.2490.71-3
- 为 Magic 3.0 重建

* Thu Oct 15 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.71-1
- update to 46.0.2490.71

* Fri Oct  2 2015 Tom Callaway <spot@fedoraproject.org> 45.0.2454.101-2
- add BuildRequires: /usr/bin/pod2html

* Thu Oct  1 2015 Tom Callaway <spot@fedoraproject.org> 45.0.2454.101-1
- update to 45.0.2454.101

* Thu May 28 2015 Tom Callaway <spot@fedoraproject.org> 43.0.2357.81-1
- update to 43.0.2357.81

* Tue May  5 2015 Tom Callaway <spot@fedoraproject.org> 42.0.2311.135-1
- update to 42.0.2311.135

* Sat Jan 24 2015 Tom Callaway <spot@fedoraproject.og> 40.0.2214.91-1
- update to 40.0.2214.91 (now in git)

* Wed Jan 14 2015 Tom Callaway <spot@fedoraproject.org> 39.0.2171.95-3
- helps if we check out the right branch of the code

* Mon Jan 12 2015 Tom Callaway <spot@fedoraproject.org> 39.0.2171.95-2
- add pnacl-ranlib invocations on the static libs that Chromium uses

* Tue Jan  6 2015 Tom Callaway <spot@fedoraproject.org> 39.0.2171.95-1
- WHEEEEEEEEEEEEEE (gonads and strife)

* Fri Jun  6 2014 Tom Callaway <spot@fedoraproject.org> 20140602-2
- make up a fake file so chromium will use the toolchain. oh this is so silly.

* Mon Jun  2 2014 Tom Callaway <spot@fedoraproject.org> 20140602-1
- once more into the breach, dear friends

* Mon Dec  9 2013 Tom Callaway <spot@fedoraproject.org> 20131209-1
- this package is a war crime. i am so so sorry.
