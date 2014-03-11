%define ver	10

Name: cdparanoia
Version: 10.2
Release: 5%{?dist}
# the app is GPLv2, everything else is LGPLv2
License: GPLv2 and LGPLv2
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Source: http://downloads.xiph.org/releases/%{name}/%{name}-III-%{version}.src.tgz
# Patch from upstream to fix cdda_interface.h C++ incompatibility ("private")
# https://trac.xiph.org/changeset/15338
# https://bugzilla.redhat.com/show_bug.cgi?id=463009
Patch0: cdparanoia-10.2-#463009.patch
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

%build
rm -rf $RPM_BUILD_ROOT
export OPT="${CFLAGS:-%optflags} -O0 -Wno-pointer-sign -Wno-unused -Werror-implicit-function-declaration"
%configure --includedir=%{_includedir}/cdda
make OPT="$OPT"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_includedir}/cdda
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -m 0755 cdparanoia $RPM_BUILD_ROOT%{_bindir}
install -m 0644 cdparanoia.1 $RPM_BUILD_ROOT%{_mandir}/man1/ 
install -m 0644 utils.h paranoia/cdda_paranoia.h interface/cdda_interface.h \
	$RPM_BUILD_ROOT%{_includedir}/cdda
install -m 0755 paranoia/libcdda_paranoia.so.0.10.? \
	interface/libcdda_interface.so.0.10.? \
	$RPM_BUILD_ROOT%{_libdir}
install -m 0755 paranoia/libcdda_paranoia.a interface/libcdda_interface.a \
	$RPM_BUILD_ROOT%{_libdir}

/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_libdir}

pushd $RPM_BUILD_ROOT%{_libdir}
ln -s libcdda_paranoia.so.0.10.? libcdda_paranoia.so
ln -s libcdda_interface.so.0.10.? libcdda_interface.so
popd

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
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 10.2-5
- 为 Magic 3.0 重建

* Fri Nov 21 2008 Liu Di <liudidi@gmail.com> - 10.2-1%{?dist}
- 更新到 10.2

* Tue Apr 04 2006 liudi <liudidi@gmail.com>
- rebuild for MagicLinux 2.0,fix for kaffeine
