Name:		libjpeg-turbo
Version: 1.3.1
Release:	5%{?dist}
Summary:	A MMX/SSE2 accelerated library for manipulating JPEG image files
Summary(zh_CN.UTF-8): 使用 MMX/SSE2 加速处理 JPEG 图像文件的库

Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	IJG
URL:		http://sourceforge.net/projects/libjpeg-turbo
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	autoconf, automake, libtool
%ifarch %{ix86} x86_64
BuildRequires:	nasm
%endif

# moved this from -utils, in an attempt to get it to better override
# libjpeg in rawhide -- Rex
Obsoletes:	libjpeg < 6b-47
# add provides (even if it not needed) to workaround bad packages, like
# java-1.6.0-openjdk (#rh607554) -- atkac
Provides:	libjpeg = 6b-47%{?dist}
%if "%{?_isa}" != ""
Provides:	libjpeg%{_isa} = 6b-47%{?dist}
%endif

Patch0:		libjpeg-turbo12-noinst.patch

%description
The libjpeg-turbo package contains a library of functions for manipulating
JPEG images.

%description -l zh_CN.UTF-8
使用 MMX/SSE2 加速处理 JPEG 图像文件的库。

%package devel
Summary:	Headers for the libjpeg-turbo library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Obsoletes:	libjpeg-devel < 6b-47
Provides:	libjpeg-devel = 6b-47%{?dist}
%if "%{?_isa}" != ""
Provides:	libjpeg-devel%{_isa} = 6b-47%{?dist}
%endif
Requires:	libjpeg-turbo%{?_isa} = %{version}-%{release}

%description devel
This package contains header files necessary for developing programs which
will manipulate JPEG files using the libjpeg-turbo library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package utils
Summary:	Utilities for manipulating JPEG images
Summary(zh_CN.UTF-8): 处理 JPEG 图像的工具
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:	libjpeg-turbo%{?_isa} = %{version}-%{release}

%description utils
The libjpeg-turbo-utils package contains simple client programs for
accessing the libjpeg functions. It contains cjpeg, djpeg, jpegtran,
rdjpgcom and wrjpgcom. Cjpeg compresses an image file into JPEG format.
Djpeg decompresses a JPEG file into a regular image file. Jpegtran
can perform various useful transformations on JPEG files. Rdjpgcom
displays any text comments included in a JPEG file. Wrjpgcom inserts
text comments into a JPEG file.

%description utils -l zh_CN.UTF-8
处理 JPEG 图像的工具，包括 cjpeg, djpeg, jpegtran, rdjpgcom 和 wrjpgcom.

%package static
Summary:	Static version of the libjpeg-turbo library
Summary(zh_CN.UTF-8): %{name} 的静态库
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Obsoletes:	libjpeg-static < 6b-47
Provides:	libjpeg-static = 6b-47%{?dist}
%if "%{?_isa}" != ""
Provides:	libjpeg-static%{_isa} = 6b-47%{?dist}
%endif
Requires:	libjpeg-turbo-devel%{?_isa} = %{version}-%{release}

%description static
The libjpeg-turbo-static package contains static library for manipulating
JPEG images.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%package -n turbojpeg
Summary:	TurboJPEG library
Summary(zh_CN.UTF-8): TurboJPEG 库
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description -n turbojpeg
The turbojpeg package contains the TurboJPEG shared library.

%description -n turbojpeg -l zh_CN.UTF-8
TurboJPEG 库。

%package -n turbojpeg-devel
Summary:	Headers for the TurboJPEG library
Summary(zh_CN.UTF-8): turbojpeg 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	turbojpeg%{?_isa} = %{version}-%{release}

%description -n turbojpeg-devel
This package contains header files necessary for developing programs which
will manipulate JPEG files using the TurboJPEG library.

%description -n turbojpeg-devel -l zh_CN.UTF-8
turbojpeg 的开发包。

%prep
%setup -q

#%patch0 -p1 -b .noinst

%build
autoreconf -fiv

%configure --with-jpeg8

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Fix perms
chmod -x README-turbo.txt

# Remove unwanted files
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib{,turbo}jpeg.la

# Don't distribute libjpegturbo.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/libturbojpeg.a
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README README-turbo.txt change.log ChangeLog.txt
%{_libdir}/libjpeg.so.8*
%{_libdir}/libturbojpeg.so.*

%files devel
%defattr(-,root,root,-)
%doc coderules.txt jconfig.txt libjpeg.txt structure.txt example.c
%{_includedir}/jconfig.h
%{_includedir}/jerror.h
%{_includedir}/jmorecfg.h
%{_includedir}/jpeglib.h
%{_libdir}/libjpeg.so
%{_docdir}/*.txt
%{_docdir}/README
%{_docdir}/example.c

%files utils
%defattr(-,root,root,-)
%doc usage.txt wizard.txt
%{_bindir}/cjpeg
%{_bindir}/djpeg
%{_bindir}/jpegtran
%{_bindir}/rdjpgcom
%{_bindir}/wrjpgcom
%{_bindir}/tjbench
%{_mandir}/man1/cjpeg.1*
%{_mandir}/man1/djpeg.1*
%{_mandir}/man1/jpegtran.1*
%{_mandir}/man1/rdjpgcom.1*
%{_mandir}/man1/wrjpgcom.1*

%files static
%defattr(-,root,root,-)
%{_libdir}/libjpeg.a

%files -n turbojpeg
%{_libdir}/libturbojpeg.so

%files -n turbojpeg-devel
%{_includedir}/turbojpeg.h

%changelog
* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 1.3.1-5
- 更新到 1.3.1

* Tue Dec 04 2012 Adam Tkac <atkac redhat com> 1.2.1-5
- change license to IJG (#877517)

* Wed Oct 24 2012 Adam Tkac <atkac redhat com> 1.2.1-4
- build with jpeg8 API/ABI (#854695)

* Thu Oct 18 2012 Adam Tkac <atkac redhat com> 1.2.1-3
- minor provides tuning (#863231)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Adam Tkac <atkac redhat com> 1.2.1-1
- update to 1.2.1

* Thu Mar 08 2012 Adam Tkac <atkac redhat com> 1.2.0-1
- update to 1.2.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Orion Poplawski <orion cora nwra com> 1.1.1-3
- Make turobojpeg-devel depend on turbojpeg

* Fri Oct 7 2011 Orion Poplawski <orion cora nwra com> 1.1.1-2
- Ship the turbojpeg library (#744258)

* Mon Jul 11 2011 Adam Tkac <atkac redhat com> 1.1.1-1
- update to 1.1.1
  - ljt11-rh688712.patch merged

* Tue Mar 22 2011 Adam Tkac <atkac redhat com> 1.1.0-2
- handle broken JPEGs better (#688712)

* Tue Mar 01 2011 Adam Tkac <atkac redhat com> 1.1.0-1
- update to 1.1.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Adam Tkac <atkac redhat com> 1.0.90-1
- update to 1.0.90
- libjpeg-turbo10-rh639672.patch merged

* Fri Oct 29 2010 Adam Tkac <atkac redhat com> 1.0.1-3
- add support for arithmetic coded files into decoder (#639672)

* Wed Sep 29 2010 jkeating - 1.0.1-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Adam Tkac <atkac redhat com> 1.0.1-1
- update to 1.0.1
  - libjpeg-turbo10-rh617469.patch merged
- add -static subpkg (#632859)

* Wed Aug 04 2010 Adam Tkac <atkac redhat com> 1.0.0-3
- fix huffman decoder to handle broken JPEGs well (#617469)

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 1.0.0-2
- add libjpeg-devel%%{_isa} provides to -devel subpkg to satisfy imlib-devel
  deps

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 1.0.0-1
- update to 1.0.0
- patches merged
  - libjpeg-turbo-programs.patch
  - libjpeg-turbo-nosimd.patch
- add libjpeg provides to the main package to workaround problems with broken
  java-1.6.0-openjdk package

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 0.0.93-13
- remove libjpeg provides from -utils subpkg

* Wed Jun 30 2010 Rex Dieter <rdieter@fedoraproject.org> 0.0.93-12
- move Obsoletes: libjpeg to main pkg

* Wed Jun 30 2010 Rex Dieter <rdieter@fedoraproject.org> 0.0.93-11
- -utils: Requires: %%name ...

* Wed Jun 30 2010 Adam Tkac <atkac redhat com> 0.0.93-10
- add Provides = libjpeg to -utils subpackage

* Mon Jun 28 2010 Adam Tkac <atkac redhat com> 0.0.93-9
- merge review related fixes (#600243)

* Wed Jun 16 2010 Adam Tkac <atkac redhat com> 0.0.93-8
- merge review related fixes (#600243)

* Mon Jun 14 2010 Adam Tkac <atkac redhat com> 0.0.93-7
- obsolete -static libjpeg subpackage (#600243)

* Mon Jun 14 2010 Adam Tkac <atkac redhat com> 0.0.93-6
- improve package description a little (#600243)
- include example.c as %%doc in the -devel subpackage

* Fri Jun 11 2010 Adam Tkac <atkac redhat com> 0.0.93-5
- don't use "fc12" disttag in obsoletes/provides (#600243)

* Thu Jun 10 2010 Adam Tkac <atkac redhat com> 0.0.93-4
- fix compilation on platforms without MMX/SSE (#600243)

* Thu Jun 10 2010 Adam Tkac <atkac redhat com> 0.0.93-3
- package review related fixes (#600243)

* Wed Jun 09 2010 Adam Tkac <atkac redhat com> 0.0.93-2
- package review related fixes (#600243)

* Fri Jun 04 2010 Adam Tkac <atkac redhat com> 0.0.93-1
- initial package
