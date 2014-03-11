%define rversion %{kde4_kdelibs_version}
%define release_number 1
%define real_name kdegraphics


Name: kdegraphics4
Summary: The KDE Graphics Components
License: LGPL v2 or later
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
URL: http://www.kde.org/
Version: %{rversion}
Release: %{release_number}%{?dist}.1

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: kde4-gwenview >= %{version}
Requires: kde4-kamera >= %{version}
Requires: kde4-kcolorchooser >= %{version}
Requires: kde4-kdegraphics-strigi-analyzer >= %{version}
Requires: kde4-kdegraphics-thumbnailers >= %{version}
Requires: kde4-kgamma >= %{version}
Requires: kde4-kolourpaint >= %{version}
Requires: kde4-kruler >= %{version}
Requires: kde4-ksaneplugin >= %{version}
Requires: kde4-ksnapshot >= %{version}
Requires: kde4-okular >= %{version}
Requires: kde4-svgpart >= %{version}


%description
The KDE Graphics Components.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- 开发包
%package -n %{name}-devel
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: KDE Graphics Libraries: Build Environment
Requires: libkdelibs4-devel
Requires: %{name} = %{version}-%{release}
Requires: kde4-libkipi-devel
Requires: kde4-libkdcraw-devel
Requires: kde4-libkexiv2-devel
Requires: kde4-libksane-devel
Requires: kde4-okular-devel

%description -n %{name}-devel
This package contains all necessary include files and libraries needed
to develop KDE Graphics applications.

%prep

%build

%install

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -n %{name}-devel

%files

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-1.1
- 为 Magic 3.0 重建

* Mon Dec 28 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.4-2mgc
- okular md5 hash 文件标注关联(patch 100 written by nihui)
- 乙丑  十一月十三

* Sat Dec 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.4-1mgc
- 更新至 4.3.4
- 乙丑  十月十九

* Sun Aug 2 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0
- 己丑  六月十二

* Tue Jun 30 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- 更新至 4.2.95(KDE 4.3 RC1)
- 己丑  闰五月初八

* Sat Jun 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.91-1mgc
- 更新至 4.2.91
- 己丑  五月廿一

* Sat May 16 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.85-1mgc
- 更新至 4.2.85(KDE 4.3 beta1)
- 己丑  四月廿二

* Sat Apr 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- 己丑  三月初九  [清明]

* Sun Mar 8 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.1mgc
- 更新至 4.2.1
- 己丑  二月十二

* Sun Jan 25 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.1mgc
- 更新至 4.2.0
- 戊子  十二月三十

* Wed Jan 14 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.1.96-0.1mgc
- 更新至 4.1.96(KDE 4.2 RC1)
- relwithdeb 编译模式
- 戊子  十二月十九

* Sat Dec 13 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.85-0.1mgc
- 更新至 4.1.85(KDE 4.2 Beta2)
- 戊子  十一月十六

* Sat Nov 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.80-0.1mgc
- 更新至 4.1.80
- 戊子  十一月初二

* Fri Nov 07 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.3-0.1mgc
- 更新至 4.1.3
- 戊子  十月初十  [立冬]

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.1mgc
- 更新至 4.1.2
- 戊子  九月初一

* Sat Aug 30 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.1mgc
- 更新至 4.1.1
- 戊子  七月三十

* Fri Jul 25 2008 Liu Di <liudidi@gmail.com> - 4.1.0-0.1mgc
- 更新到 4.1.0(KDE 4.1 正式版)

* Fri Jul 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.98-0.1mgc
- 更新至 4.0.98(KDE 4.1 RC1)
- 戊子  六月初九

* Sat Jun 28 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.84-0.1mgc
- 更新至 4.0.84
- 戊子  五月廿五

* Thu Jun 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.83-0.1mgc
- 更新至 4.0.83-try1(第一次 tag 4.1.0-beta2 内部版本)
- FindKSane.cmake 文件从 devel 包移入 libksane-devel 包
- 戊子  五月十六

* Thu Jun 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.82-0.1mgc
- 更新至 4.0.82
- 戊子  五月初九

* Wed Jun 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.81-0.1mgc
- 更新至 4.0.81
- 分出 libkipi, libkdcraw, libkexiv2 等包，extragear-libs died~~~
- 戊子  五月初一

* Fri May 23 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.80-0.1mgc
- 更新至 4.0.80(try1 内部版本)
- 戊子  四月十九

* Fri May 16 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.74-0.1mgc
- 更新至 4.0.74
- 去除 libkscan
- 从 playground-graphics 移入 ksaneplugin
- 从 extragear-libs 移入 libksane，libksane 开发库与头文件移入 devel 包
- 戊子  四月十二

* Sat Apr 26 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.71-0.1mgc
- 更新至 4.0.71
- 戊子  三月廿一

* Sat Apr 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.70-0.1mgc
- 更新至 4.0.70
- 纳入 libspectre 支持(ghostscript 文档格式)
- 纳入 ebook-tools 支持(epub 文档格式)
- 戊子  三月十四

* Tue Apr 1 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.3-0.1mgc
- 更新至 4.0.3
- 定义 kde4 路径
- 细化分包
- 戊子  二月廿五

* Tue Mar 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.2-0.1mgc
- 更新至 4.0.2
- 戊子  正月廿七

* Fri Feb 8 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.1-0.1mgc
- 更新至 4.0.1
- 将 libspectreOkular.so 文件纳入 devel 包(thanks to the upstream!)

* Sat Jan 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.1mgc
- 更新至 4.0.0

* Sat Dec 15 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.97.0-0.1mgc
- 更新至 3.97.0 (KDE4-RC2)
- 纳入 pdf 支持
- 纳入 chm 支持
- 纳入 djvu 支持

* Sat Nov 24 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.96.0-0.1mgc
- 更新至 3.96.0 (KDE4-RC1)

* Sat Oct 20 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.94.0-0.1mgc
- 首次生成 rpm 包
