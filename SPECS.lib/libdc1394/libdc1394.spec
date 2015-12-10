# $Id$

#define svn_snapshot .svn459  
#define real_version 2.0.0-rc8%{svn_snapshot}
#%define real_version 2.1.0
%define svn_build %{?svn_snapshot:1}%{!?svn_snapshot:0}

Summary: 1394-based digital camera control library
Summary(zh_CN.UTF-8): 基于 1394 的数码相机控制库
Name: libdc1394
Version: 2.2.1
Release: 4%{?svn_snapshot}%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://sourceforge.net/projects/libdc1394/
Source: http://downloads.sourceforge.net/project/libdc1394/libdc1394-2/%{version}/libdc1394-%{version}.tar.gz
Patch1: libdc1394-videodev.h.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
ExcludeArch: s390 s390x

BuildRequires: kernel-headers
BuildRequires: libraw1394-devel libusb1-devel
BuildRequires: doxygen
BuildRequires: libX11-devel libXv-devel
%if %{svn_build}
BuildRequires: libtool
%endif

%description
Libdc1394 is a library that is intended to provide a high level programming
interface for application developers who wish to control IEEE 1394 based
cameras that conform to the 1394-based Digital Camera Specification.

%description -l zh_CN.UTF-8
基于 1394 的数码相机控制库。

%package devel
Summary: Header files and libraries for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}, libraw1394-devel
Requires: pkgconfig

%description devel
This package contains the header files and libraries
for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package docs
Summary: Development documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Documentation
Group(zh_CN.UTF-8): 文档

%description docs
This package contains the development documentation for %{name}.

%description docs -l zh_CN.UTF-8
%{name} 的文档。

%package tools
Summary: Tools for use with %{name}
Summary(zh_CN.UTF-8): %{name} 的工具
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Requires: %{name} = %{version}

%description tools
This package contains tools that are useful when working and
developing with %{name}.

%description tools -l zh_CN.UTF-8
%{name} 的工具。

%prep
%setup -q -n libdc1394-%{version}

%build
%if %{svn_build}
cp /usr/share/libtool/ltmain.sh .
aclocal
autoheader
autoconf
automake --add-missing
%endif
autoreconf -fisv
%configure --disable-static --enable-doxygen-html --enable-doxygen-dot
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
make doc

%install
%{__rm} -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
mkdir -p %{buildroot}%{_docdir}/%{name}-docs-%{version}
%{__install} -p -m 0644 doc/html/* %{buildroot}%{_docdir}/%{name}-docs-%{version}
for p in grab_color_image grab_gray_image grab_partial_image ladybug grab_partial_pvn; do
	%{__install} -p -m 0644 examples/$p %{buildroot}%{_bindir}/dc1394_$p
done
%{__install} -p -m 0644 examples/dc1394_multiview %{buildroot}%{_bindir}/dc1394_multiview
for f in grab_color_image grab_gray_image grab_partial_image; do
	mv %{buildroot}%{_mandir}/man1/$f.1 %{buildroot}%{_mandir}/man1/dc1394_$f.1
done

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libdc1394*.so.*

%files devel
%defattr(-, root, root, 0755)
%doc examples/*.h examples/*.c
%{_includedir}/dc1394/
%{_libdir}/libdc1394*.so
%{_libdir}/pkgconfig/%{name}-2.pc
%exclude %{_libdir}/*.la

%files docs
%defattr(-, root, root, 0755)
%{_docdir}/%{name}-docs-%{version}

%files tools
%defattr(-, root, root, 0755)
%{_bindir}/dc1394_*
%{_mandir}/man1/dc1394_*.1.gz

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 2.2.1-4
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.2.1-3
- 为 Magic 3.0 重建

* Mon Jul 14 2014 Liu Di <liudidi@gmail.com> - 2.2.1-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.2.0-2
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Liu Di <liudidi@gmail.com> - 2.1.3-2
- 为 Magic 3.0 重建

* Thu Sep 10 2009 Karsten Hopp <karsten@redhat.com> 2.1.2-3
- excludearch s390 s390x where we don't have libraw1394

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Tim Niemueller <tim@niemueller.de> - 2.1.2-1
- Update to latest stable release 2.1.2

* Tue Mar 17 2009 Tim Niemueller <tim@niemueller.de> - 2.1.0-1
- Update to latest stable release 2.1.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon May 12 2008 Tim Niemueller <tim@niemueller.de> - 2.0.2-1
- Update to latest stable release 2.0.2

* Sat Jan 19 2008 Tim Niemueller <tim@niemueller.de> - 2.0.1-3
- Made autotools calls optional, only called if svn_snapshot is defined
- devel subpackage now requires pkgconfig

* Wed Jan 16 2008 Tim Niemueller <tim@niemueller.de> - 2.0.1-2
- Add docs subpackage to contain development documentation
- Incoroprate multilib tricks
- BuildReqire automake, autoconf, libtool and doxygen
- Removed unused BuildRequires
- Use header file from kernel-headers instead of kernel-devel
- BuildRequire kernel-devel
- Added tools subpackage to contain the resetbus and vloopback tools

* Wed Jan 16 2008 Tim Niemueller <tim@niemueller.de> - 2.0.1-1
- Update to 2.0.1, now patent-free!

* Mon Jan 07 2008 Tim Niemueller <tim@niemueller.de> - 2.0.0-1
- Update to 2.0.0

* Thu Dec 16 2007 Tim Niemueller <tim@niemueller.de> - 2.0.0-rc9
- Update to 2.0.0-rc9

* Wed Nov 28 2007 Tim Niemueller <tim@niemueller.de> - 2.0.0-rc7.3.svn459
- Updated to release 2.0.0-rc7+svn459 (not yet released)

* Fri Nov 02 2007 Tim Niemueller <tim@niemueller.de> - 2.0.0-rc7.1.svn443
- Updated to release 2.0.0-rc7+svn443 (not yet released) for juju support
- Added --without juju to disable juju support (necessary for FC6)

* Fri Feb 02 2007 Tim Niemueller <tim@niemueller.de> - 2.0.0-rc5.1
- Updated to release 2.0.0-rc5.

* Wed Aug 16 2006 Tim Niemueller <tim@niemueller.de> - 2.0.0-rc3.1
- Updated to release 2.0.0-rc3.

* Mon May 08 2006 Dries Verachtert <dries@ulyssis.org> - 2.0.0-0.1.pre7
- Updated to release 2.0.0-0.1.pre7.

* Sat Apr 08 2006 Dries Verachtert <dries@ulyssis.org> - 2.0.0-0.1.pre5.2
- Rebuild for Fedora Core 5.

* Thu Dec  8 2005 Matthias Saou <http://freshrpms.net/> 2.0.0-0.1.pre5
- Update to 2.0.0-pre5.
- Add missing libraw1394-devel dependency to the devel package.

* Tue Aug 30 2005 Dries Verachtert <dries@ulyssis.org> - 2.0.0-0.pre4
- Update to release 2.0.0-0.pre4.

* Thu Aug 25 2005 Dries Verachtert <dries@ulyssis.org> - 1.1.0-1
- Initial package.
