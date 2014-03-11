Name: libmng
Version: 1.0.10
Release: 8%{?dist}
URL: http://www.libmng.com/
Summary: A library which supports MNG graphics.
Summary(zh_CN.UTF-8): 支持 MNG 图形的库。
License: BSD-like
Source: http://osdn.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildPrereq: gcc glibc-devel zlib-devel libjpeg-devel

%package devel
Summary: Development files for the LibMNG library.
Summary(zh_CN.UTF-8): LibMNG 库的开发文件。
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}

%package static
Summary: A statically linked version of the LibMNG library.
Summary(zh_CN.UTF-8): 一个 LibMNG 库的静态链接的版本。
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description
LibMNG is a library for accessing graphics in MNG (Multi-image Network
Graphics) and JNG (JPEG Network Graphics) formats.  MNG graphics are
basically animated PNGs.  JNG graphics are basically JPEG streams
integrated into a PNG chunk.

%description -l zh_CN.UTF-8
LibMNG 是一个用来访问 MNG(多图像网络图形) 和 JNG(JPEG 网络图形)格式的图
形的库。MNG 图形基本上可说是动画的 PNG。JNG 图形基本上可说是集成到 PNG 
主体中的 JPEG 流。

%description devel
LibMNG is a library for accessing MNG and JNG format graphics.  The
libmng-devel package contains files needed for developing or compiling
applications which use MNG graphics.

%description devel -l zh_CN.UTF-8
LibMNG 是一个用来访问 MNG 和 JNG 格式图形的库。 libmng-devel 软件包包括
开发或编译使用 MNG 图形的程序所需的文件。

%description static
LibMNG is a library for accessing MNG and JNG format graphics.  The
libmng-static package contains a statically linked version of the
LibMNG library, which you need if you want to develop or compile
applications using MNG graphics without depending upon LibMNG being
installed on the user's system.

%description static -l zh_CN.UTF-8
LibMNG 是一个用来访问 MNG 和 JNG 格式图形的库。 libmng-static 软件包包
括 LibMNG 库的静态链接版本，如果您要开发或编译使用 MNG 图形的程序，但
不想依赖于安装在用户系统上的 LibMNG 时，您需要这个软件包。

%prep
%setup -q

%build
cp makefiles/configure.in .
cp makefiles/Makefile.am .
sed -i '/AM_C_PROTOTYPES/d' configure.in
autoreconf -if
%configure --enable-shared --enable-static --with-zlib --with-jpeg \
	--with-gnu-ld
make %{?_smp_mflags}

%install
%makeinstall

#rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_mandir}/man3
%{_mandir}/man5

%files static
%defattr(-,root,root)
%{_libdir}/*.a

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.10-8
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 1.0.10-7
- 为 Magic 3.0 重建

* Wed May 18 2005 KanKer <kanker@163.com>
- rebuild

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> 1.0.9-1
- Update to 1.0.9
- Work around autogen.sh brokenness

* Fri Feb 11 2005 Matthias Clasen <mclasen@redhat.com> 1.0.8-2
- Remove .la files (#145970)
- Remove some unneeded Requires

* Tue Oct 12 2004 Matthias Clasen <mclasen@redhat.com> 1.0.8-1
- Upgrade to 1.0.8

* Mon Jul 19 2004 Matthias Clasen <mclasen@redhat.com> 1.0.7-4
- Add missing Requires

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 19 2004 Matthias Clasen <mclasen@redhat.com> 1.0.7-1
- Upgrade to 1.0.7

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Dec 13 2002 Elliot Lee <sopwith@redhat.com> 1.0.4-2
- Rebuild, _smp_mflags

* Mon Jun 24 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.4-1
- 1.0.4

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Apr 25 2002 Than Ngo <than@redhat.com> 1.0.3-3
- rebuild in new enviroment

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Sep 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.3-1
- 1.0.3

* Tue Jul 31 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.2-1
- Update to 1.0.2 (bugfix release - fixes a memory leak and file corruption)

* Wed Jun 20 2001 Than Ngo <rtthan@redhat.com> 1.0.1-2
- requires %%{name} = %%{version}

* Thu May  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.1-1
- 1.0.1

* Wed Feb 28 2001 Trond Eivind Glomsr鴇 <teg@redhat.com>
- remove bogus symlink trick

* Mon Feb 26 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to 1.0.0 to make Qt 2.3.0 happy

* Sat Jan 19 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.9.4, fixes MNG 1.0 spec compliance

* Tue Dec 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.9.3
- Add ldconfig calls in %%post and %%postun

* Tue Dec 05 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- added a clean section to the spec file

* Tue Sep 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- initial rpm

