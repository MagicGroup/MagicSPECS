Summary: Audio/Video Control library for IEEE-1394 devices
Summary(zh_CN.UTF-8): IEEE-1394 设备的音频/视频控制库
Name: libavc1394
Version: 0.5.4
Release: 3%{?dist}
License: LGPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source: http://downloads.sourceforge.net/project/libavc1394/libavc1394/libavc1394-%{version}.tar.gz
Patch: libavc1394-0.5.1-librom.patch
BuildRequires: libraw1394-devel
BuildRequires: autoconf automake libtool
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
ExcludeArch: s390 s390x

%description
The libavc1394 library allows utilities to control IEEE-1394 devices
using the AV/C specification.  Audio/Video Control allows applications
to control devices like the tape on a VCR or camcorder.

%description -l zh_CN.UTF-8
libavc1394 库允许实用工具使用 AV/C 规范控制 IEEE-1394 设备。
音频/视频控制允许应用程序控制诸如录像机或者便携摄像机上的
磁带之类的设备。

%package devel
Summary: Development libs for libavc1394
Summary(zh_CN.UTF-8): libavc1394 的开发库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: libraw1394-devel

%description devel
Header files and static libraries for libavc1394.

%description -l zh_CN.UTF-8
libavc1394 的头文件和静态库。

%prep
%setup -q
%patch -p1 -b .librom

%build
# Rerun autotools to pick up newer libtool
autoreconf -f -i
%configure
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
%{__rm} -f %{buildroot}%{_libdir}/*.la


%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README ChangeLog
%{_bindir}/dvcont
%{_bindir}/mkrfc2734
%{_bindir}/panelctl
%{_libdir}/libavc1394.so.*
%{_libdir}/librom1394.so.*
%{_mandir}/man1/dvcont.1.gz
%{_mandir}/man1/panelctl.1.gz
%{_mandir}/man1/mkrfc2734.1*


%files devel
%defattr(-,root,root,-)
%{_includedir}/libavc1394/
%{_libdir}/pkgconfig/libavc1394.pc
%{_libdir}/*.so
%{_libdir}/*.a


%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.5.4-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.5.4-2
- 为 Magic 3.0 重建

* Thu Jul 10 2014 Liu Di <liudidi@gmail.com> - 0.5.4-1
- 更新到 0.5.4

* Thu Jul 10 2014 Liu Di <liudidi@gmail.com> - 0.5.3-5
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.5.3-4
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Liu Di <liudidi@gmail.com> - 0.5.3-3
- 为 Magic 3.0 重建

* Sat Sep 22 2007 kde <athena_star@163.com> - 0.9-1mgc
- Initial build
