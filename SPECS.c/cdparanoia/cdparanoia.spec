%define ver	10

Name: cdparanoia
Version: 10.2
Release: 7%{?dist}
# the app is GPLv2, everything else is LGPLv2
License: GPLv2 and LGPLv2
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Source: http://downloads.xiph.org/releases/%{name}/%{name}-III-%{version}.src.tgz
# Patch from upstream to fix cdda_interface.h C++ incompatibility ("private")
# https://trac.xiph.org/changeset/15338
# https://bugzilla.redhat.com/show_bug.cgi?id=463009
Patch0: cdparanoia-10.2-#463009.patch
# #466659
Patch1: cdparanoia-10.2-endian.patch
Patch2: cdparanoia-10.2-install.patch
Patch3: cdparanoia-10.2-format-security.patch
Patch4: cdparanoia-use-proper-gnu-config-files.patch

Url: http://www.xiph.org/paranoia/index.html
BuildRoot: %{_tmppath}/cdparanoia-%{version}-root
Requires: cdparanoia-libs = %{version}-%{release}
Obsoletes: cdparanoia-III
Summary: A Compact Disc Digital Audio (CDDA) extraction tool (or ripper).
Summary(zh_CN.UTF-8): 从 CDDA 中抓取音轨的工具

%description 
Cdparanoia (Paranoia III) reads digital audio directly from a CD, then
writes the data to a file or pipe in WAV, AIFC or raw 16 bit linear
PCM format.  Cdparanoia doesn't contain any extra features (like the ones
included in the cdda2wav sampling utility).  Instead, cdparanoia's strength
lies in its ability to handle a variety of hardware, including inexpensive
drives prone to misalignment, frame jitter and loss of streaming during
atomic reads.  Cdparanoia is also good at reading and repairing data from
damaged CDs.

%description -l zh_CN.UTF-8
它可以从一个支持CDDA的CDROM中提取wave文件. 实际上,linux支持的所有光驱都能用.

%package -n cdparanoia-devel
Summary: Development tools for libcdda_paranoia (Paranoia III).
Summary(zh_CN.UTF-8): libcdda_paranoia的开发工具
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: cdparanoia-libs = %{version}-%{release}
License: LGPLv2

%description -n cdparanoia-devel
The cdparanoia-devel package contains the static libraries and header
files needed for developing applications to read CD Digital Audio disks.

%description -n cdparanoia-devel -l zh_CN.UTF-8
cdparanoia-devel包包含了开发读取CD数字音轨所需要析静态库和头文件。

%package -n cdparanoia-libs
Summary: Libraries for libcdda_paranoia (Paranoia III).
Summary(zh_CN.UTF-8): libcdda_paranoia的库文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License: LGPLv2

%description -n cdparanoia-libs
The cdparanoia-libs package contains the dynamic libraries needed for
applications which read CD Digital Audio disks.

%description -n cdparanoia-libs -l zh_CN.UTF-8
cdparanoia-libs包包含了读取CD数字音轨的应用程序所需要的动态库文件。

%prep
%setup -q -n %{name}-III-%{version}
%patch0 -p3 -b .#463009
%patch1 -p1 -b .endian
%patch2 -p1 -b .install
%patch3 -p1 -b .fmt-sec
%patch4 -p1 -b .config

# Update config.guess/sub for newer architectures
cp /usr/lib/rpm/magic/config.* .

%build
rm -rf $RPM_BUILD_ROOT
%configure --includedir=%{_includedir}/cdda
# Using -O0 is mandatory, the build fails otherwise...
# Also remove many warnings which we are aware of
# Lastly, don't use _smp_mflags since it also makes the build fail
make OPT="$RPM_OPT_FLAGS -O0 -Wno-pointer-sign -Wno-unused"

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%post -n cdparanoia-libs
/sbin/ldconfig

%postun -n cdparanoia-libs
if [ "$1" -ge "1" ]; then
  /sbin/ldconfig
fi

%clean
[ "$RPM_BUILD_ROOT" != "/" -a -d "$RPM_BUILD_ROOT" ] && rm -rf "$RPM_BUILD_ROOT"

%files -n cdparanoia
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_mandir}/man1/*

%files -n cdparanoia-libs
%defattr(-,root,root)
%{_libdir}/*.so*

%files -n cdparanoia-devel
%defattr(-,root,root)
%{_includedir}/cdda
%{_libdir}/*.a

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 10.2-7
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 10.2-6
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 10.2-5
- 为 Magic 3.0 重建

* Fri Nov 21 2008 Liu Di <liudidi@gmail.com> - 10.2-1%{?dist}
- 更新到 10.2

* Tue Apr 04 2006 liudi <liudidi@gmail.com>
- rebuild for MagicLinux 2.0,fix for kaffeine
