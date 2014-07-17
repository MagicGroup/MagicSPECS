Summary: Control operation of a CD-ROM when playing audio CDs
Summary(zh_CN.UTF-8): 当播放音频 CD 时控制光驱
Name: libcdaudio
Version: 0.99.12p2
Release: 17%{?dist}
# COPYING is a copy of GPLv2, but the code and the README clearly indicate
# that the code is LGPLv2+. Probably want to let upstream know about COPYING.
License: LGPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://libcdaudio.sourceforge.net/
Source0: http://prdownloads.sourceforge.net/libcdaudio/%{name}-%{version}.tar.gz
Patch0: libcdaudio-0.99.12-buffovfl.patch
Patch1: libcdaudio-0.99.12p2-libdir.patch
Patch2: libcdaudio-0.99-CAN-2005-0706.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gcc-c++

%description
libcdaudio is a library designed to provide functions to control
operation of a CD-ROM when playing audio CDs.  It also contains
functions for CDDB and CD Index lookup.

%description -l zh_CN.UTF-8
当播放音频 CD 时控制光驱，它也包括了 CDDB 和 CD 索引查找函数。

%package devel
Summary: Development files for libcdaudio
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains development files for linking against libcdaudio.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1

%build
%configure \
  --enable-dependency-tracking \
  --disable-static \
  --enable-threads
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README NEWS
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%exclude %{_libdir}/*.la
%{_bindir}/%{name}-config
%{_datadir}/aclocal/%{name}.m4
%{_libdir}/pkgconfig/libcdaudio.pc

%changelog
* Fri Jul 11 2014 Liu Di <liudidi@gmail.com> - 0.99.12p2-17
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.99.12p2-16
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Liu Di <liudidi@gmail.com> - 0.99.12p2-15
- 为 Magic 3.0 重建

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.12p2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.12p2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.12p2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 27 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.99.12p2-11
- Fix CVE-2005-0706.

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.99.12p2-10
- took COPYING out of doc (it is simply wrong)
- fixed license tag

* Fri Dec 29 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.99.12p2-8
- Change Group tag.
- Fix libcdaudio-config for libdir != %%{_prefix}/lib.

* Wed Dec 27 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.99.12p2-7
- Update to 0.99.12p2.

* Tue Sep 13 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Patch to fix buffer overflow by Brian C. Huffman
  <huffman@graze.net>.

* Sat Jul 23 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.99.12.

* Wed May 14 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.


