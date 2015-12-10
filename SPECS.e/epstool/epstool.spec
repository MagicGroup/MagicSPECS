Name:		epstool
Version:	3.08
Release:	5%{?dist}
Summary:	A utility to create or extract preview images in EPS files
Summary(zh_CN.UTF-8): 创建和解压 EPS 文件中预览图像的工具
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:	GPLv2+
URL:		http://pages.cs.wisc.edu/~ghost/gsview/epstool.htm
Source0:	http://mirror.cs.wisc.edu/pub/mirrors/ghost/ghostgum/%{name}-%{version}.tar.gz
# Patch to compile with gcc 4.3 and newer (taken from Gentoo)
Patch0:		epstool-3.08-gcc43.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Epstool is a utility to create or extract preview images in EPS files,
fix bounding boxes and convert to bitmaps.

Features:
* Add EPSI, DOS EPS or Mac PICT previews.
* Extract PostScript from DOS EPS files.
* Uses Ghostscript to create preview bitmaps.
* Create a TIFF, WMF, PICT or Interchange preview from part of a
  bitmap created by Ghostscript.
* works under Win32, Win64, OS/2 and Unix.
* works on little-endian machines (Intel) or big endian (Sun Sparc,
  Motorola) machines.

%description -l zh_CN.UTF-8
创建和解压 EPS 文件中预览图像的工具。

%prep
%setup -q
%patch0 -p1

%build
# SMP build doesn't work.
make

%install
rm -rf %{buildroot}
install -D -p -m 755 bin/epstool %{buildroot}%{_bindir}/epstool
install -D -p -m 644 doc/epstool.1 %{buildroot}%{_mandir}/man1/epstool.1
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENCE doc/epstool.htm doc/gsview.css
%{_bindir}/epstool
%{_mandir}/man1/epstool.1.*

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 3.08-5
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 3.08-4
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 3.08-3
- 为 Magic 3.0 重建

* Mon Jan 16 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.08-2
- Disable SMP build.

* Mon Jan 09 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.08-1
- First release.
