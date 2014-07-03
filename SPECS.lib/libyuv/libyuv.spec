%ifarch %{arm}
%global with_neon --enable-neon
%endif
%define svn 1
%define vcsdate 20140603


Name:		libyuv
Summary:	YUV conversion and scaling functionality library
Version:	0
Release:	0.svn%{vcsdate}%{?dist}.5
License:	BSD
Group:		Development/Libraries
Url:		http://code.google.com/p/libyuv/
## svn -r 389 export http://libyuv.googlecode.com/svn/trunk libyuv-0
## tar -cjvf libyuv-0.tar.bz2 libyuv-0
Source0:	%{name}-svn%{vcsdate}.tar.xz
Source1:	make_libyuv_svn_package.sh
# Fedora-specific. Upstream isn't interested in this.
Patch1:		libyuv-0001-Initial-autotools-support.patch
Patch2:         libyuv-disable-mips64-COPYROW_MIPS.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	gtest-devel
BuildRequires:	libjpeg-devel
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


%description
This is an open source project that includes YUV conversion and scaling
functionality. Converts all webcam formats to YUV (I420). Convert YUV to
formats for rendering/effects. Rotate by 90 degrees to adjust for mobile
devices in portrait mode. Scale YUV to prepare content for compression,
with point, bilinear or box filter.


%package devel
Summary: The development files for %{name}
Group: Development/Libraries
Requires: pkgconfig
Requires: %{name}%{?_isa} = %{version}-%{release}


%description devel
Additional header files for development with %{name}.


%prep
%setup -q -n %{name}-svn%{vcsdate}
%patch1 -p1 -b .autotools
%patch2 -p1 -b .COPYROW_MIPS


%build
sh autogen.sh
%configure --disable-static --with-pic --without-test --with-mjpeg %{?with_neon}
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%check
make check


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc AUTHORS LICENSE PATENTS
%{_libdir}/%{name}.so.*


%files devel
%{_includedir}/%{name}
%{_includedir}/%{name}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Tue Jun 03 2014 Liu Di <liudidi@gmail.com> - 0-0.svn20140603.5
- 为 Magic 3.0 重建

* Tue Jun 03 2014 Liu Di <liudidi@gmail.com> - 0-0.svn20140603.4
- 为 Magic 3.0 重建

* Tue Jun 03 2014 Liu Di <liudidi@gmail.com> - 0-0.svn20140603.3
- 为 Magic 3.0 重建

* Tue Jun 03 2014 Liu Di <liudidi@gmail.com> - 0-0.svn20140603.2
- 为 Magic 3.0 重建

* Tue Jun 03 2014 Liu Di <liudidi@gmail.com> - 0-0.svn20140603.1
- 更新到 20140603 日期的仓库源码

* Tue Jun 03 2014 Liu Di <liudidi@gmail.com> - 0-0.svn20121001.1
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0-0.15.20121001svn389
- 为 Magic 3.0 重建

* Thu Oct 04 2012 Peter Lemenkov <lemenkov@gmail.com> - 0-0.14.20121001svn389
- Next svn snapshot - ver. 389
- Enable NEON on ARM (if detected)

* Sat Sep 15 2012 Peter Lemenkov <lemenkov@gmail.com> - 0-0.13.20120915svn353
- Next svn snapshot - ver. 353
- Dropped upstreamed patch no.3

* Mon Jul 30 2012 Peter Lemenkov <lemenkov@gmail.com> - 0-0.12.20120727svn312
- Next svn snapshot - ver. 312

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.11.20120627svn296
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 05 2012 Peter Lemenkov <lemenkov@gmail.com> - 0-0.10.20120627svn296
- Next svn snapshot - ver. 296
- Dropped patch3 (header conflict) - fixed upstream

* Thu Jun 14 2012 Tom Callaway <spot@fedoraproject.org> - 0-0.9.20120518svn268
- resolve header conflict with duplicate definition in scale*.h

* Fri May 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 0-0.8.20120518svn268
- Next svn snapshot - ver. 268
- Fixed failure on s390x and PPC64 (see rhbz #822494)
- Fixed FTBFS on EL5 (see rhbz #819179)

* Sat May 05 2012 Peter Lemenkov <lemenkov@gmail.com> - 0-0.7.20120505svn256
- Next svn snapshot - ver. 256

* Sun Apr 08 2012 Peter Lemenkov <lemenkov@gmail.com> - 0-0.6.20120406svn239
- Next svn snapshot - ver. 239

* Thu Mar 08 2012 Peter Lemenkov <lemenkov@gmail.com> - 0-0.5.20120308svn209
- Next svn ver. - 209
- Drop upstreamed patches
- Add libjpeg as a dependency

* Thu Feb 02 2012 Peter Lemenkov <lemenkov@gmail.com> - 0-0.4.20120202svn164
- Next svn ver. - 164
- Added two patches - no.2 and no.3

* Thu Jan 12 2012 Peter Lemenkov <lemenkov@gmail.com> - 0-0.3.20120109svn128
- Use bzip2 instead of xz (for EL-5)

* Wed Jan 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 0-0.2.20120109svn128
- Update to svn rev. 128
- Enable unit-tests
- Dropped obsolete defattr directive
- Consistently use macros
- Explicitly add _isa to the Requires for *-devel sub-package

* Fri Jan  6 2012 Peter Lemenkov <lemenkov@gmail.com> - 0-0.1.20120105svn127
- Initial package
