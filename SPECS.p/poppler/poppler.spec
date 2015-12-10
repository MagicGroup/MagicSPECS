Summary: PDF rendering library
Summary(zh_CN.UTF-8): PDF 渲染库
Name: poppler
Version:	0.37.0
Release: 5%{?dist}
License: GPLv2 and Redistributable, no modification permitted
# the code is GPLv2
# the charmap data in /usr/share/poppler is redistributable
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:     http://poppler.freedesktop.org/
Source0: http://poppler.freedesktop.org/poppler-%{version}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

BuildRequires: gtk2-devel
BuildRequires: cairo-devel >= 1.4
BuildRequires: qt4-devel >= 4.4.0
BuildRequires: qt4-test >= 4.4.0
Requires: poppler-data >= 0.4.5

# not strongly denpendence, but recommended by upstream  ── nihui
BuildRequires: openjpeg-devel

%description
Poppler, a PDF rendering library, it's a fork of the xpdf PDF
viewer developed by Derek Noonburg of Glyph and Cog, LLC.

%description -l zh_CN.UTF-8
Poppler 是一个 PDF 渲染库。它是 xpdf PDF 查看器的派生。
由 Derek Noonburg of Glyph and Cog, LLC 开发。

%package devel
Summary: Libraries and headers for poppler
Summary(zh_CN.UTF-8): Poppler 的库和头文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk-doc

%description devel
Poppler, a PDF rendering library, it's a fork of the xpdf PDF
viewer developed by Derek Noonburg of Glyph and Cog, LLC.

You should install the poppler-devel package if you would like to
compile applications based on poppler.

%description devel -l zh_CN.UTF-8
Poppler 是一个 PDF 渲染库。它是 xpdf PDF 查看器的派生。
由 Derek Noonburg of Glyph and Cog, LLC 开发。

如果您想要基于 poppler 编译应用程序，那么应该安装此 poppler-devel 包。

%package glib
Summary: Glib wrapper for poppler
Summary(zh_CN.UTF-8): Poppler 的 glib 包装
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description glib
%{summary}.

%description glib -l zh_CN.UTF-8
Poppler 的 glib 包装。

%package glib-devel
Summary: Development files for glib wrapper
Summary(zh_CN.UTF-8): Glib 包装的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}-glib = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: pkgconfig
Requires: gtk-doc

%description glib-devel
%{summary}.

%description glib-devel -l zh_CN.UTF-8
Glib 包装的开发文件。

%package qt
Summary: Qt wrapper for poppler
Summary(zh_CN.UTF-8): Poppler 的 Qt 包装
Group:   System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name} = %{version}-%{release}

%description qt
%{summary}.

%description qt -l zh_CN.UTF-8
Poppler 的 Qt 包装。

%package qt-devel
Summary: Development files for Qt wrapper
Summary(zh_CN.UTF-8): Qt 包装的开发文件
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}-qt = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: qt-devel

%description qt-devel
%{summary}.

%description qt-devel -l zh_CN.UTF-8
Qt 包装的开发文件。

%package qt4
Summary: Qt4 wrapper for poppler
Summary(zh_CN.UTF-8): Poppler 的 Qt4 包装
Group:   System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name} = %{version}-%{release}

%description qt4
%{summary}.

%description qt4 -l zh_CN.UTF-8
Poppler 的 Qt4 包装。

%package qt4-devel
Summary: Development files for Qt4 wrapper
Summary(zh_CN.UTF-8): Qt4 包装的开发文件
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}-qt4 = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: qt4-devel

%description qt4-devel
%{summary}.

%description qt4-devel -l zh_CN.UTF-8
Qt4 包装的开发文件。

%package qt5
Summary: Qt5 wrapper for poppler
Summary(zh_CN.UTF-8): Poppler 的 Qt5 包装
Group:   System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name} = %{version}-%{release}

%description qt5
%{summary}.

%description qt5 -l zh_CN.UTF-8
Poppler 的 Qt4 包装。

%package qt5-devel
Summary: Development files for Qt5 wrapper
Summary(zh_CN.UTF-8): Qt5 包装的开发文件
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}-qt4 = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: qt5-qtbase-devel

%description qt5-devel
%{summary}.

%description qt5-devel -l zh_CN.UTF-8
Qt5 包装的开发文件。

%package cpp
Summary: Pure C++ wrapper for poppler
Summary(zh_CN.UTF-8): poppler 的纯 C++ 封装
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description cpp
%{summary}.

%description cpp -l zh_CN.UTF-8
poppler 的纯 C++ 封装。

%package cpp-devel
Summary: Development files for C++ wrapper
Summary(zh_CN.UTF-8): C++ 封装的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}-cpp = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description cpp-devel
%{summary}.

%description cpp-devel -l zh_CN.UTF-8
C++ 封装的开发文件。

%package utils
Summary: Command line utilities for converting PDF files
Summary(zh_CN.UTF-8): 转换 PDF 文件的命令行工具
Group: Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
Requires: %{name} = %{version}-%{release}
Conflicts: xpdf <= 3.01
# There's an extras package that provides pdftohtml

Provides: pdftohtml
Obsoletes: pdftohtml

Provides: xpdf-utils = 3.01
Obsoletes: xpdf-utils <= 3.01

%description utils
Poppler, a PDF rendering library, it's a fork of the xpdf PDF
viewer developed by Derek Noonburg of Glyph and Cog, LLC.

This utils package installs a number of command line tools for
converting PDF files to a number of other formats.

%description utils -l zh_CN.UTF-8
Poppler 是一个 PDF 渲染库。它是 xpdf PDF 查看器的派生。
由 Derek Noonburg of Glyph and Cog, LLC 开发。

本工具软件包会安装一系列转换 PDF 文件至其他格式的命令行工具。

%prep
%setup -q

%build
chmod -x goo/GooTimer.h

iconv -f iso-8859-1 -t utf-8 < "utils/pdftohtml.1" > "utils/pdftohtml.1.utf8"
mv "utils/pdftohtml.1.utf8" "utils/pdftohtml.1"

# hammer to nuke rpaths, recheck on new releases
autoreconf -i -f

# Hack around borkage, http://cgit.freedesktop.org/poppler/poppler/commit/configure.ac?id=9250449aaa279840d789b3a7cef75d06a0fd88e7
PATH=%{_qt4_bindir}:$PATH; export PATH

%configure \
  --disable-static \
  --disable-zlib \
  --enable-gtk-doc \
  --enable-cairo-output \
  --enable-libjpeg \
  --enable-libopenjpeg \
  --enable-poppler-qt4 \
  --enable-xpdf-headers

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

rm %{buildroot}%{_libdir}/lib*.la

magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post glib -p /sbin/ldconfig
%postun glib -p /sbin/ldconfig

%post qt -p /sbin/ldconfig
%postun qt -p /sbin/ldconfig

%post qt4 -p /sbin/ldconfig
%postun qt4 -p /sbin/ldconfig

%post cpp -p /sbin/ldconfig
%postun cpp -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root,-)
%{_libdir}/libpoppler.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/poppler.pc
%{_libdir}/pkgconfig/poppler-splash.pc
%{_libdir}/libpoppler.so
%{_includedir}/poppler/
%{_datadir}/gtk-doc/html/poppler

%files glib
%defattr(-,root,root,-)
%{_libdir}/libpoppler-glib.so.*

%files glib-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/poppler-glib.pc
%{_libdir}/pkgconfig/poppler-cairo.pc
%{_libdir}/libpoppler-glib.so
%{_libdir}/girepository-1.0/Poppler-0.18.typelib
%{_datadir}/gir-1.0/Poppler-0.18.gir

%files qt4
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt4.so.*

%files qt4-devel
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt4.so
%{_libdir}/pkgconfig/poppler-qt4.pc
%{_includedir}/poppler/qt4/

%files qt5
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt5.so.*

%files qt5-devel
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt5.so
%{_libdir}/pkgconfig/poppler-qt5.pc
%{_includedir}/poppler/qt5/

%files cpp
%defattr(-,root,root,-)
%{_libdir}/libpoppler-cpp.so.0*

%files cpp-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/poppler-cpp.pc
%{_libdir}/libpoppler-cpp.so

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.37.0-5
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.37.0-4
- 更新到 0.37.0

* Tue Jul 28 2015 Liu Di <liudidi@gmail.com> - 0.34.0-3
- 为 Magic 3.0 重建

* Tue Jul 28 2015 Liu Di <liudidi@gmail.com> - 0.34.0-2
- 更新到 0.34.0

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 0.24.5-2
- 更新到 0.24.5

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.20.5-2
- 为 Magic 3.0 重建

* Wed Nov 21 2012 Liu Di <liudidi@gmail.com> - 0.20.4-2
- 为 Magic 3.0 重建

* Tue Mar 27 2012 Liu Di <liudidi@gmail.com> - 0.18.4-2
- 为 Magic 3.0 重建

* Thu Jul 30 2009 Ni Hui <shuizhuyuanluo@126.com> - 0.10.7-1mgc
- 更新至 0.10.7
- automake 编译
- 纳入 openjpeg 支持
- 己丑  六月初九

* Wed Jan 14 2009 Ni Hui <shuizhuyuanluo@126.com> - 0.10.3-0.1mgc
- 更新至 0.10.3
- 数据包更新至 0.2.1
- 使用 cmake 编译
- 戊子  十二月十九

* Fri Aug 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.8.6-0.1mgc
- 更新至 0.8.6
- 戊子  七月廿九

* Wed Jun 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.8.3-0.1mgc
- 更新至 0.8.3
- 戊子  五月初一

* Sat May 31 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.8.2-0.1mgc
- 更新至 0.8.2
- 拆出 glib & glib-devel 包
- 戊子  四月廿七

* Fri Feb 8 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.6.4-0.1mgc
- 更新至 0.6.4

* Thu Jan 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.6.3-0.1mgc
- 更新至 0.6.3
- qt4-devel >= 4.3.3

* Wed Dec 05 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.6.2-0.1mgc
- rebuild for MagicLinux-2.1

* Thu Nov 30 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.2-1
- package xpdf headers in poppler-devel (Jindrich Novy)
- Fix qt3 detection (Denis Leroy)
- Update to 0.6.2

* Thu Oct 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.6-2
- include qt4 wrapper
