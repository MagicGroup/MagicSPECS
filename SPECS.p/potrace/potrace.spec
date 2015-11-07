Name:		potrace
Version:	1.13
Release:	2%{?dist}
Summary:	Transform bitmaps into vector graphics
Summary(zh_CN.UTF-8): 转换位图到向量图形
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
# README defines license as GPLv2+
License:	GPLv2+
URL:		http://potrace.sourceforge.net
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Documentation
Source1:	http://potrace.sourceforge.net/potrace.pdf
Source2:	http://potrace.sourceforge.net/potracelib.pdf
# Patch for supporting 64 bit ARM from upstream
Patch0:		potrace-1.11-autoconf.diff

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	zlib-devel

%description
Potrace is a utility for tracing a bitmap, which means, transforming a bitmap 
into a smooth, scalable image. The input is a bitmap (PBM, PGM, PPM, or BMP
format), and the default output is an encapsulated PostScript file (EPS).
A typical use is to create EPS files from scanned data, such as company or
university logos, handwritten notes, etc. The resulting image is not "jaggy"
like a bitmap, but smooth. It can then be rendered at any resolution.

Potrace can currently produce the following output formats: EPS, PostScript,
PDF, SVG (scalable vector graphics), Xfig, Gimppath, and PGM (for easy
antialiasing). Additional backends might be added in the future.

Mkbitmap is a program distributed with Potrace which can be used to pre-process
the input for better tracing behavior on greyscale and color images.

%description -l zh_CN.UTF-8
转换位图到向量图形。

%package devel
Summary:	Potrace development library and headers
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the potrace development library and headers.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary:	Documentation on how to use the potrace library
Summary(zh_CN.UTF-8): %{name} 的文档
Group:		Documentation
Group(zh_CN.UTF-8): 文档
%if 0%{?fedora} > 10 || 0%{?rhel} > 5
BuildArch:	noarch
%endif

%description doc
This package contains documentation for the potrace algorithm and the potrace
library.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q
cp -a %{SOURCE1} .
cp -a %{SOURCE2} .

%build
%configure --enable-shared --disable-static \
 --enable-metric --with-libpotrace --with-pic
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -name *.la -exec rm -rf {} \;

# Get rid of installed copy of placement.pdf
rm -rf %{buildroot}%{_docdir}/%{name}
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README doc/placement.pdf
%{_bindir}/potrace
%{_bindir}/mkbitmap
%{_libdir}/libpotrace.so.*
%{_mandir}/man1/potrace.1.*
%{_mandir}/man1/mkbitmap.1.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libpotrace.so
%{_includedir}/potracelib.h

%files doc
%defattr(-,root,root,-)
%doc potrace.pdf potracelib.pdf

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.13-2
- 更新到 1.13

* Sun Aug 02 2015 Liu Di <liudidi@gmail.com> - 1.12-1
- 更新到 1.12

* Mon Apr 14 2014 Liu Di <liudidi@gmail.com> - 1.11-4
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 15 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.11-2
- Support for 64 bit ARM architecture (BZ #926364).

* Wed Feb 20 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.11-1
- Update to 1.11.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Aug 21 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.10-1
- Update to 1.10.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.9-1
- Update to 1.9.

* Thu Aug 06 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.8-4
- Corrected license tag.

* Mon Aug 03 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.8-3
- Added missing BuildRequires.

* Mon Aug 03 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.8-2
- Adjusted descriptions as per review comments. 

* Mon Aug 03 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.8-1
- First release.
