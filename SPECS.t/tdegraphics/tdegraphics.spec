%define debug 0
%define final 1

%define kpovmodeler 0
%define kfract 1
%define arts 1

%define _iconsdir %_datadir/icons

%define git 1
%define gitdate 20111223

Summary:       KDE graphics package
Summary(zh_CN.UTF-8): KDE 图像程序包
Name:           tdegraphics
Version:       3.5.14
%if %{git}
Release:	0.git%{gitdate}
%else
Release:       0.1%{?dist}
%endif
License:     GPL
URL:            http://www.kde.org
Group:         Applications/Multimedia
Group(zh_CN.UTF-8):  应用程序/多媒体
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
%if %{git}
Source:		%{name}-git%{gitdate}.tar.xz
%else
Source:        %{name}-%{version}.tar.bz2
%endif
Source10:	make_tdegraphics_git_package.sh
Source1:	xpdf.tar.gz
Source3: ftp://ftp.foolabs.com/pub/xpdf/xpdf-chinese-simplified.tar.gz
Source4: ftp://ftp.foolabs.com/pub/xpdf/xpdf-chinese-traditional.tar.gz
Source5: ftp://ftp.foolabs.com/pub/xpdf/xpdf-japanese.tar.gz
Source6: ftp://ftp.foolabs.com/pub/xpdf/xpdf-korean.tar.gz

Source12: xpdfrc

Patch0:	kghostview.desktop.patch
Patch1: tdegraphics-git20111223-ksnapshot.patch

Prefix:        %{_prefix}
Requires:     qt, arts, tdelibs, tdebase, fribidi
Requires:     %{name}-common
Requires:     %{name}-ksnapshot
Requires:     %{name}-kpdf
Requires:     %{name}-kolourpaint

%description
Graphics applications for the K Desktop Environment.

Includes:
  kdvi (displays TeX .dvi files)
  kfax (displays faxfiles)
  kghostview (displays postscript files)
  kcoloredit (palette editor and color chooser)
  kamera (digital camera support)
  kiconedit (icon editor)
  kpaint (a simple drawing program)
  ksnapshot (screen capture utility)
  kview (image viewer for GIF, JPEG, TIFF, etc.)
  kuickshow (quick picture viewer)
  kooka (scanner application)
  kruler (screen ruler and color measurement tool)

%description -l zh_CN.UTF-8
K 桌面环境 (KDE) 的图像应用程序：

包括：
  kdvi (显示 Tex .dvi 文件)
  kfax (显示传真文件)
  kghostview (显示 postscript 文件)
  kcoloredit (调色板编辑和颜色选择)
  kamera (数码相机支持)
  kiconedit (图像编辑器)
  kpaint (简单画图程序)
  ksnapshot (屏幕抓取工具)
  kview (GIF, JPEG, TIFF 等图像查看器)
  kuickshow (快速图像查看器)
  kooka (扫描仪程序)
  kruler (屏幕标尺和颜色测量工具)

这个包不包含 kruler，kgamma，kuickshow，kfax，kamera，
kfaxview，kmrml，kpovmodeler，kdvi，kiconedit，kolourpaint

%package devel
Summary: Development files for kdegraphics
Summary(zh_CN.UTF-8): kdegraphics的开发文件
Requires: %{name} = %{version}-%{release}
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description devel
Graphic applications for the K Desktop Environment.
This package contains header files for developing applications using kdegraphics.

%description devel -l zh_CN.UTF-8
这个包包含了使用 kdegraphics 开发应用程序所需要的头文件。

%package extras
Summary: extras files for kdegraphics
Summary(zh_CN.UTF-8): kdegraphics 的 extras 文件
Requires: %{name} = %{version}-%{release}
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体

%description extras
extras

%description extras -l zh_CN.UTF-8
kdegraphics extras 文件。

这个包包含了 kruler，kgamma，kuickshow，kfax，kamera，
kfaxview，kmrml，kpovmodeler，kdvi，kiconedit，kolourpaint。

#===========================================================================

%package common
Summary:        Common files for kdegraphics
Summary(zh_CN.UTF-8): %{name} 的公用文件
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:   kdelibs
Provides:   kgamma = %version-%release
 
%description common
Common files for kdegraphics

%description common -l zh_CN.UTF-8
%{name} 的公用文件。

#--------------------------------------------------------------------------

%package kolourpaint
Summary:    Free and easy-to-use paint program for KDE
Summary(zh_CN.UTF-8): KDE 下的画图程序
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Obsoletes:      kolourpaint
Provides:       kolourpaint
Requires:	%{name}-common = %{version}-%{release}
 
%description kolourpaint
KolourPaint is a free, easy-to-use paint program for KDE.
It aims to be conceptually simple to understand; providing a level of
functionality targeted towards the average user. It's designed for daily
tasks like:
  Painting - drawing diagrams and "finger painting"
  Image Manipulation - editing screenshots and photos; applying effects
  Icon Editing - drawing clipart and logos with transparency
It's not an unusable and monolithic program where simple tasks like drawing
lines become near impossible. Nor is it so simple that it lacks essential
features like Undo/Redo. KolourPaint is opensource software written in C++
using the Qt and KDE libraries

%description kolourpaint -l zh_CN.UTF-8
KDE中的绘图工具。它虽然不面向专业的图像绘制，但就简单图像处理来说功能却很齐全，
各类基本画笔工具、选取工具、线条工具等都不缺，也可实行自动裁剪、颜色反转、缩放、
对比度调整等处理。

KolourPaint可以打开所有KIMGIO兼容的图像格式，但有少数专业格式如EXR不能作为保存输出。

#----------------------------------------------------------------------------------

%package mrmlsearch
Summary:        MRML is short for Multimedia Retrieval Markup Language
Summary(zh_CN.UTF-8): MRML图像搜索客户端
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Provides: mrmlsearch
 
%description mrmlsearch
MRML is short for Multimedia Retrieval Markup Language,
which defines a protocol for querying a server for images
based on their content. See http://www.mrml.net about MRML
and the GNU Image Finding Tool (GIFT), an MRML server.
 
This package consists of an mrml kio-slave that handles
the communication with the MRML server and a KPart to
be embedded e.g. into Konqueror.
 
With those, you can search for images by giving an example
image and let the server look up similar images. The query
result can be refined by giving positive/negative feedback.

%description mrmlsearch -l zh_CN.UTF-8
MRML即Multimedia Retrieval Markup Language，媒体索引标记语言，
被用于基于索引的“相似图像搜索”服务，适合海量图片收藏在网络上
的共享，用户可以通过图像索引尽量高效地搜索到自己要找的图片资源。

#---------------------------------------------------------------------------------

%package kooka
Summary:    Kooka is a raster image scan program for the KDE system
Summary(zh_CN.UTF-8): KDE 下的扫描仪工具
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:       kdelibs 
Requires:       gocr
Provides:       kooka
Provides:       scanner-gui
 
%description kooka
This package contains a raster image scan program, based on SANE and libkscan.

%description kooka -l zh_CN.UTF-8
扫描仪操作工具，基于SANE。支持对网络扫描仪的访问，内置基本的图像处理
如缩放、反转等功能，协同外部的一些OCR（Optical Character Recongntion）
光学字符识别软件也能够在一定程度上实现直接的图文识别转换功能。但有个
问题是，Kooka似乎已失去后继维护很久了:(。

#----------------------------------------------------------------------------------


%package kdvi
Summary:    Kdvi is a DVI Viewer
Summary(zh_CN.UTF-8): KDE 下的 DVI 查看器
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Provides:       kdvi
Requires:       %name-common = %version-%release
# kdvi requires kviewpart which is in kview, do NOT remove this provide
# or kdvi won't work
Requires:       tdegraphics-kview
Requires:       texlive
 
%description kdvi
Kdvi package

%description kdvi -l zh_CN.UTF-8
基于KViewShell的DVI文档查看器。DVI即Device Indepentent，设备无关文档，这是
TeX排版系统由源文档编译成的可读文档格式，它应能在任何平台上的输出程序里以
不变的版式显示，且可直接交付排印。TeX官方提供的DVI阅读器是XDVI，KDVI则被设
计成能够和KDE环境平滑集成的另一种选择，它现在能够显示绝大部分的DVI页面元素，
不过尚缺乏多语言搜索、页面背景色等少量实现。

KDVI也支持DVI>PS、DVI>PDF、DVI>文本的转换，在拥有TeX源文件的情况下也可以集成
外部的编辑器对文档内容实行编辑。不过要让KDVI正常工作，前提是您需要事先安装好
可用的TeTeX系统。

#---------------------------------------------------------------------------------

%package kfax
Summary:    Kfax package
Summary(zh_CN.UTF-8): KDE 传真图像查看器
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Provides:       kfax
Requires:   %name-common = %version-%release
Requires:   tdegraphics-kview
 
%description kfax
A program to display raw and tiffed fax images (g3, g3-2d, g4).

%description kfax -l zh_CN.UTF-8
基于KViewShell的KDE传真图像查看器，支持G3、G32d、G4三种格式规范。

#---------------------------------------------------------------------------------

%package kruler
Summary:    Kruler package
Summary(zh_CN.UTF-8): 屏幕标尺工具
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Provides:       kruler
 
%description kruler
A ruler in inch, centimeter and pixel to check distances on the screen

%description kruler -l zh_CN.UTF-8
从KDE1起就有的屏幕标尺工具。其界面就是一把仿真的黄色计量尺，用于在显示屏幕上
按用户所需测量某两点间长度，它采用的测量单位是可选的。

#-----------------------------------------------------------------------------------

%package kghostview
Summary:    Kghostview package
Summary(zh_CN.UTF-8): 基于 KViewShell 的 PS/PDF 查看器
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Provides:       kghostview
Requires:       ghostscript
 
%description kghostview
A program (and embeddable KPart) to display *.PDF and *.PS

%description kghostview -l zh_CN.UTF-8
基于KViewShell的PS/PDF查看器，但主要还是用于查看PS文档，PS（PostScript）是一
种打印机语言。KGhostView提供浏览PS文档所需的独立应用程序和KParts组件，故经常
以嵌入在文件管理器中的形式工作，同时它也可以作为简单的PDF查看器来用，不过KDE-
Graphics中另有单独的PDF阅读软件，KGhostView保留对PDF的支持是开发历史缘故。

#---------------------------------------------------------------------------------

%package kpdf
Summary:    Kpdf package
Summary(zh_CN.UTF-8): KDE 中的 PDF 文档查看器
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Provides:       kpdf
 
%description kpdf
kpdf program

%description kpdf -l zh_CN.UTF-8
KDE中的PDF文档查看器。PDF（Portable Document Format）是一种可移植文档格式，现
已成为现世界上行业标准级的电子文档发布、交换、出版规范。

KPDF是一个开源的PDF查看器，包含了独立应用程序和KParts嵌入组件。它虽然并不涵盖
Adode Acrobat Reader的100%完整PDF兼容性，但已经提供了满足实用要求的PDF阅读需求，
而且它的运行速度要快得多。KPDF现在拥有文档索引（即目录）解析、链接跳转、文档缩
放、页面文字复制或读出（适用于西文，请参看KTTSD子系统）、书签插入、缩略图预览、
全文搜索、幻灯片模式等特性。当然，只要提供中文字库，KPDF对非内嵌字体的中文PDF文
档也照样能很好地支持。

KPDF及KFax、KDVI、KGhostView这一系列文档查看器现在仍然各自独立，不过在下一代的
KDE中它们将整合为“N in 1”的通用文档查看器Okular。

#-----------------------------------------------------------------------------------

%package ksnapshot
Summary:    Ksnaphot package
Summary(zh_CN.UTF-8): KDE 的屏幕抓图工具
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Provides:       ksnapshot
 
%description ksnapshot
KSnapshot is intended to be an easy to use program for making
screenshots. I can be bound to the Print Screen key, as the program
takes a snapshot of the desktop on startup (before it displays it
window), so it's a simple way of of making snapshots.

%description ksnapshot -l zh_CN.UTF-8
KDE的屏幕抓图工具。支持全屏、窗口、区域、窗口节四种抓取模式，具备延时抓取功能。

#------------------------------------------------------------------------------------

%package kpovmodeler
Summary:    Kpovmodeler package
Summary(zh_CN.UTF-8): 场景建模引擎 Pov-Ray 的官方推荐前端
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Provides:       kpovmodeler
 
%description kpovmodeler
Program to enter scenes for the 3D rendering engine PovRay.

%description kpovmodeler -l zh_CN.UTF-8
KPovModeler是一个免费3D场景建模引擎Pov-Ray的官方推荐前端，您可以使用它创作渲染出
复杂精致的3D展示图，并导出为多种图像格式。Pov-Ray本身没有图形界面，它根据外部输入
的建模脚本完成场景的渲染输出，KPovModeler的作用就是在所见即所得的环境下设计建模脚
本，此程序附带若干个样例脚本，您可以从中体验到Pov-Ray所能完成的高级效果。

这是一个专业软件，也许对真正的工程设计人员是个选择。

#--------------------------------------------------------------------------------------

%package kiconedit
Summary:    Kiconedit package
Summary(zh_CN.UTF-8): KDE 图标编辑器
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Provides:       kiconedit
 
%description kiconedit
An icon editor.

%description kiconedit -l zh_CN.UTF-8
KDE图标编辑器。一个基于像素的图像编辑器，即以可见的一个个网格为图像编辑的最小单位，
网格的数量由被编辑图像的分辨率决定。KIconEdit内置了一批简单的图像操作工具，如手绘轨
迹笔、喷涂器、线/矩形/圆形渲染、选取框等，并可同步预览效果图，操作非常容易。

#--------------------------------------------------------------------------------------

%package kview
Summary:    Kview package
Summary(zh_CN.UTF-8): 基于KViewShell的图片查看器
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Provides:       kview
 
%description kview
Kview is a  picture viewer, provided as standalone program and embeddable KPart

%description kview -l zh_CN.UTF-8
基于KViewShell的图片查看器，它也是KDE中图像预览的默认程序。它和KuickShow作用近似但并
不重复，KuickShow用于图片浏览，KView只为单一图像的查看而设计，在KDE中被广泛用于嵌入
部件，其独立的应用程序其实很少被用到。

#----------------------------------------------------------------------------------------

%package kuickshow
Summary:    Kuickshow package
Summary(zh_CN.UTF-8): 一个轻型图片浏览器
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Provides:       kuickshow
 
%description kuickshow
A fast and comfortable imageviewer.

%description kuickshow -l zh_CN.UTF-8
一个轻型图片浏览器。使用了Imlib图像优化算法所以对图像的读取预览速度很快，结合它提供的
图片浏览队列和自动修饰功能，KuickShow 应是一个适合简单主义者的选择。

#--------------------------------------------------------------------------------------------

%package kcoloredit
Summary:    Kcoloredit package
Summary(zh_CN.UTF-8): 调色板编辑器
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Provides:       kcoloredit
 
%description kcoloredit
A fast and comfortable imageviewer.

%description kcoloredit -l zh_CN.UTF-8
调色板编辑器KColorEdit。允许用户以自定义、渐变色版、屏幕撷取等多种途径调制自己需要的
配色板，提供了色调-饱和度-亮度模式HSV、红-绿-蓝模式RGB及其十六进制标识几种颜色定义规范。

#-------------------------------------------------------------------------------------------

%package kcolorchooser
Summary:    Kcolorchooser package
Summary(zh_CN.UTF-8): 屏幕撷色程序
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Provides:       kcolorchooser
 
%description kcolorchooser
A fast and comfortable imageviewer.

%description kcolorchooser -l zh_CN.UTF-8
屏幕撷色程序，是 KColorEdit 中一个子功能附加上颜色模版特性的独立版本。
KColorChooser 拥有一个撷色滴管部件，在屏幕上点到哪里，那里的的当前颜色就会被记录下来。

#-----------------------------------------------------------------------------------------------

%package ksvg
Summary:    Ksvg package
Summary(zh_CN.UTF-8): SVG 查看程序
Group:      Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Provides:       ksvg
 
%description ksvg
KSVG is a KDE implementation of the Scalable Vector Graphics Specifications.

%description ksvg -l zh_CN.UTF-8
这是一个示例性质的 SVG 查看器，没有任何设置项，要在命令行中指定图片路径参数。
SVG是Scalable Vector Graphics，一种新兴的矢量图像标准，SVG文件的存储不同于传统的栅格类
图像，它根据纯文本形式的XML文件描述图案。无损缩放是SVG的基本特征，无关尺寸和分辨率，它
甚至可以产生出诸如色彩线性变化、自定义内置字体、双向文本、透明、动态效果、滤镜效果等各
式常见的图像特效，存在一种趋势显示它也许是网络图像的未来新贵。

#----------------------------------------------------------------------------------------------

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate} -a 3 -a 4 -a 5 -a 6
%else
%setup -q -n %{name}-%{version} -a 3 -a 4 -a 5 -a 6
%endif

%patch0 -p1
%patch1 -p1

%build
mkdir build
cd build
%cmake 	-DWITH_T1LIB=ON \
	-DWITH_LIBPAPER=ON \
	-DWITH_TIFF=ON \
	-DWITH_OPENEXR=ON \
	-DWITH_PDF=ON \
	-DBUILD_ALL=ON ..
#临时措施
sed -i 's/lICE/lICE \-lXext/g' ksnapshot/CMakeFiles/ksnapshot.dir/link.txt

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd build
make DESTDIR=%{buildroot} install
cd ..

#configure kpdf
mkdir -p %{buildroot}%{_datadir}/xpdf/chinese \
         %{buildroot}%{_datadir}/xpdf/chinese-traditional \
         %{buildroot}%{_datadir}/xpdf/japanese \
         %{buildroot}%{_datadir}/xpdf/korean

cp -rf xpdf-chinese-simplified/* %{buildroot}%{_datadir}/xpdf/chinese/
cp -rf xpdf-chinese-traditional/* %{buildroot}%{_datadir}/xpdf/chinese-traditional/
cp -rf xpdf-japanese/* %{buildroot}%{_datadir}/xpdf/japanese/
cp -rf xpdf-korean/* %{buildroot}%{_datadir}/xpdf/korean/
mkdir -p %{buildroot}/etc
cp -r %{SOURCE12} %{buildroot}/etc

rm %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%{_includedir}/*

%files extras
%defattr(-,root,root)

%files kolourpaint
%defattr(-,root,root)
%_bindir/kolourpaint
%_datadir/applications/kde/kolourpaint.desktop
%dir %_datadir/apps/kolourpaint
%_datadir/apps/kolourpaint/*
%doc %_docdir/kde/HTML/en/kolourpaint
%_iconsdir/*/*/*/kolourpaint*

%files mrmlsearch
%defattr(-,root,root)
%_bindir/mrmlsearch
%_libdir/trinity/kcm_kmrml.*
%_libdir/trinity/kio_mrml.*
%_libdir/trinity/libkmrmlpart.*
%_libdir/trinity/kded_daemonwatcher.*
%_datadir/applications/kde/kcmkmrml.desktop
%_datadir/services/mrml.protocol
%_datadir/services/mrml_part.desktop
%_datadir/services/kded/daemonwatcher.desktop
%_datadir/apps/konqueror/servicemenus/mrml-servicemenu.desktop
%_datadir/mimelnk/text/mrml.desktop
%_libdir/trinity/mrmlsearch.*
%_libdir/libtdeinit_mrmlsearch.*

%files kooka
%defattr(-,root,root)
%doc %_docdir/kde/HTML/en/kooka
%dir %_datadir/apps/kooka
%_datadir/apps/kooka/*
%_datadir/config/kookarc
%_bindir/kooka
%_datadir/applications/kde/kooka.desktop
%_libdir/libkscan.so.*
%_libdir/libkscan.so

%files kdvi
%defattr(-,root,root)
%doc %_docdir/kde/HTML/en/kdvi
%_libdir/trinity/kdvipart.*
%_iconsdir/*/*/*/kdvi.*
%_datadir/services/kdvimultipage.desktop
%_datadir/config.kcfg/kdvi.kcfg
%_bindir/kdvi
%_datadir/applications/kde/kdvi.desktop
%dir %_datadir/apps/kdvi/
%_datadir/apps/kdvi/*

%files kfax
%defattr(-,root,root)
%_libdir/trinity/djvuviewpart.*
%_libdir/libdjvu.*
%_datadir/apps/djvumultipage.rc
%_datadir/config.kcfg/djvumultipage.kcfg
%_datadir/services/djvumultipage.desktop
%_bindir/kfax
%_bindir/kfaxview
%_datadir/applications/kde/kfax.desktop
%_datadir/applications/kde/kfaxview.desktop
%dir %_datadir/apps/kfax/
%_datadir/apps/kfax/*
%dir %_datadir/apps/kfaxview
%_datadir/apps/kfaxview/*
%_iconsdir/*/*/*/kfax*
%_datadir/services/kfaxmultipage.desktop
%_datadir/services/kfaxmultipage_tiff.desktop
%_libdir/trinity/kfaxviewpart.*
# This is a module, not library. We will not change buildsystem
# on kde 3 and the install should be fixed on kde4
%_libdir/libkfaximage.*

%files kruler
%defattr(-,root,root)
%_bindir/kruler
%_datadir/applnk/Graphics/kruler.desktop
%_iconsdir/*/*/*/kruler*
%_datadir/applications/kde/kruler.desktop
%dir %_datadir/apps/kruler/
%_datadir/apps/kruler/*
%doc %_docdir/kde/HTML/en/kruler

%files kghostview
%defattr(-,root,root)
%doc %_docdir/kde/HTML/en/kghostview
%_iconsdir/*/*/*/kghostview.*
%_datadir/apps/kconf_update/kghostview.upd
%dir %_datadir/config.kcfg/
%_datadir/config.kcfg/kghostview.kcfg
%_bindir/kghostview
%_datadir/applications/kde/kghostview.desktop
%_datadir/services/kghostview_part.desktop
%dir %_datadir/apps/kghostview/
%_datadir/apps/kghostview/*
%_libdir/trinity/libkghostviewpart.*
%_libdir/trinity/gsthumbnail.*
%_datadir/services/gsthumbnail.desktop
%_libdir/libkghostviewlib.so.*
%_libdir/libkghostviewlib.so

%files kpdf
%defattr(-,root,root)
/etc/xpdfrc
%_bindir/kpdf
%dir %_datadir/apps/kpdf/
%_datadir/apps/kpdf/*
%dir %_datadir/apps/kpdfpart/
%_datadir/apps/kpdfpart/*
%_datadir/services/kpdf_part.desktop
%_iconsdir/*/*/*/kpdf*
%_libdir/trinity/kfile_pdf.*
%_datadir/services/kfile_pdf.desktop
%_libdir/trinity/libkpdfpart.*
%_libdir/libpoppler-tqt.so*
%_datadir/config.kcfg/kpdf.kcfg
%doc %_docdir/kde/HTML/en/kpdf
%_datadir/applications/kde/kpdf.desktop
%_datadir/xpdf/*


%files ksnapshot
%defattr(-,root,root)
%doc %_docdir/kde/HTML/en/ksnapshot
%_bindir/ksnapshot
%_datadir/applications/kde/ksnapshot.desktop
%_iconsdir/*/*/*/ksnapshot*

%files kpovmodeler
%defattr(-,root,root)
%_bindir/kpovmodeler
%doc %_docdir/kde/HTML/en/kpovmodeler
%_libdir/trinity/libkpovmodelerpart.*
%_iconsdir/*/*/*/kpovmodeler*
%dir %_datadir/apps/kpovmodeler/
%_datadir/apps/kpovmodeler/*
%_datadir/applications/kde/kpovmodeler.desktop
%_libdir/libkpovmodeler.so.*
%_libdir/libkpovmodeler.so

%files kiconedit
%defattr(-,root,root)
%doc %_docdir/kde/HTML/en/kiconedit
%_datadir/applications/kde/kiconedit.desktop
%dir %_datadir/apps/kiconedit
%_datadir/apps/kiconedit/*
%_iconsdir/*/*/*/kiconedit*
%_bindir/kiconedit

%files kview
%defattr(-,root,root)
%doc %_docdir/kde/HTML/en/kview
%_bindir/kview
%_bindir/kviewshell
%_datadir/config.kcfg/kviewshell.kcfg
%_libdir/trinity/kviewerpart.*
%_datadir/applications/kde/kview.desktop
%_libdir/trinity/kview.*
%_libdir/libtdeinit_kview.*
%_libdir/trinity/kcm_kview*.*
%_datadir/services/kviewviewer.desktop
%dir %_datadir/services/kconfiguredialog/
%_datadir/services/kconfiguredialog/kviewcanvasconfig.desktop
%_datadir/services/kconfiguredialog/kviewgeneralconfig.desktop
%_datadir/services/kconfiguredialog/kviewpluginsconfig.desktop
%_datadir/services/kconfiguredialog/kviewviewerpluginsconfig.desktop
%_datadir/services/kconfiguredialog/kviewpresenterconfig.desktop
%dir %_datadir/apps/kview/
%_datadir/apps/kview/*
%_datadir/services/kviewcanvas.desktop
%_datadir/servicetypes/kimageviewercanvas.desktop
%_datadir/servicetypes/kimageviewer.desktop
%dir %_datadir/apps/kviewviewer/
%_datadir/apps/kviewviewer/*
%_libdir/trinity/kview_*
%_libdir/trinity/libkview*
%_libdir/trinity/libphotobook.*
%_iconsdir/*/*/*/photobook*
%_iconsdir/*/*/*/kview*
%_datadir/services/photobook.desktop
%dir %_datadir/apps/kviewerpart/
%_datadir/apps/kviewerpart/*
%dir %_datadir/apps/kviewshell/
%_datadir/apps/kviewshell/*
%dir %_datadir/apps/photobook/
%_datadir/apps/photobook/*
%_libdir/libkimageviewer.so.*
%_libdir/libkimageviewer.so
%_datadir/cmake/kviewshell.cmake

%files kuickshow
%defattr(-,root,root)
%doc %_docdir/kde/HTML/en/kuickshow
%_bindir/kuickshow
%_iconsdir/*/*/*/kuickshow*
%_datadir/applications/kde/kuickshow.desktop
%dir %_datadir/apps/kuickshow/
%_datadir/apps/kuickshow/*
%_libdir/trinity/kuickshow.*
%_libdir/libtdeinit_kuickshow.*

%files kcoloredit
%defattr(-,root,root)
%doc %_docdir/kde/HTML/en/kcoloredit
%dir %_datadir/apps/kcoloredit
%_datadir/applications/kde/kcoloredit.desktop
%_datadir/apps/kcoloredit/*
%_bindir/kcoloredit
%_iconsdir/*/*/*/kcoloredit*

%files kcolorchooser
%defattr(-,root,root)
%_bindir/kcolorchooser
%_datadir/applications/kde/kcolorchooser.desktop
%_iconsdir/*/*/*/kcolorchooser*

%files ksvg
%defattr(-,root,root)
%_bindir/svgdisplay
%_bindir/printnodetest
%_libdir/trinity/libksvg*
%_libdir/trinity/svgthumbnail.*
%_datadir/servicetypes/ksvgrenderer.desktop
%_datadir/services/svgthumbnail.desktop
%_datadir/services/ksvglibartcanvas.desktop
%_datadir/services/ksvgplugin.desktop
%dir %_datadir/apps/ksvg/
%_datadir/apps/ksvg/ksvgplugin.rc
%_libdir/libksvg.so.*
%_libdir/libtext2path.so.*
%_libdir/libksvg.so
%_libdir/libtext2path.so

%files common
%defattr(-,root,root)
%_bindir/xf86gammacfg
%_libdir/trinity/emptymultipagepart.la
%_libdir/trinity/emptymultipagepart.so
%_libdir/trinity/kcm_kamera.la
%_libdir/trinity/kcm_kamera.so
%_libdir/trinity/kcm_kgamma.la
%_libdir/trinity/kcm_kgamma.so
%_libdir/trinity/kfile_bmp.la
%_libdir/trinity/kfile_bmp.so
%_libdir/trinity/kfile_dds.la
%_libdir/trinity/kfile_dds.so
%_libdir/trinity/kfile_dvi.la
%_libdir/trinity/kfile_dvi.so
%_libdir/trinity/kfile_exr.la
%_libdir/trinity/kfile_exr.so
%_libdir/trinity/kfile_gif.la
%_libdir/trinity/kfile_gif.so
%_libdir/trinity/kfile_ico.la
%_libdir/trinity/kfile_ico.so
%_libdir/trinity/kfile_jpeg.la
%_libdir/trinity/kfile_jpeg.so
%_libdir/trinity/kfile_pcx.la
%_libdir/trinity/kfile_pcx.so
%_libdir/trinity/kfile_png.la
%_libdir/trinity/kfile_png.so
%_libdir/trinity/kfile_pnm.la
%_libdir/trinity/kfile_pnm.so
%_libdir/trinity/kfile_ps.la
%_libdir/trinity/kfile_ps.so
%_libdir/trinity/kfile_raw.la
%_libdir/trinity/kfile_raw.so
%_libdir/trinity/kfile_rgb.la
%_libdir/trinity/kfile_rgb.so
%_libdir/trinity/kfile_tga.la
%_libdir/trinity/kfile_tga.so
%_libdir/trinity/kfile_tiff.la
%_libdir/trinity/kfile_tiff.so
%_libdir/trinity/kfile_xbm.la
%_libdir/trinity/kfile_xbm.so
%_libdir/trinity/kfile_xpm.la
%_libdir/trinity/kfile_xpm.so
%_libdir/trinity/kio_kamera.la
%_libdir/trinity/kio_kamera.so
%_libdir/libkmultipage.so
%_libdir/libkmultipage.so.0
%_libdir/libkmultipage.so.0.0.0
%_datadir/applications/kde/kamera.desktop
%_datadir/applications/kde/kgamma.desktop
%_datadir/apps/kconf_update/update-to-xt-names.pl
%_datadir/apps/kgamma/pics/background.png
%_datadir/apps/kgamma/pics/cmyscale.png
%_datadir/apps/kgamma/pics/darkgrey.png
%_datadir/apps/kgamma/pics/greyscale.png
%_datadir/apps/kgamma/pics/lightgrey.png
%_datadir/apps/kgamma/pics/midgrey.png
%_datadir/apps/kgamma/pics/rgbscale.png
%_datadir/doc/kde/HTML/en/kamera/common
%_datadir/doc/kde/HTML/en/kamera/index.cache.bz2
%_datadir/doc/kde/HTML/en/kamera/index.docbook
%_datadir/doc/kde/HTML/en/kgamma/common
%_datadir/doc/kde/HTML/en/kgamma/index.cache.bz2
%_datadir/doc/kde/HTML/en/kgamma/index.docbook
%_datadir/icons/crystalsvg/16x16/actions/camera_test.png
%_datadir/icons/crystalsvg/16x16/actions/palette_color.png
%_datadir/icons/crystalsvg/16x16/actions/palette_gray.png
%_datadir/icons/crystalsvg/16x16/actions/palette_halftone.png
%_datadir/icons/crystalsvg/16x16/actions/palette_lineart.png
%_datadir/icons/crystalsvg/16x16/apps/camera.png
%_datadir/icons/crystalsvg/16x16/devices/camera.png
%_datadir/icons/crystalsvg/22x22/devices/camera.png
%_datadir/icons/crystalsvg/22x22/filesystems/camera.png
%_datadir/icons/crystalsvg/32x32/devices/camera.png
%_datadir/icons/crystalsvg/32x32/filesystems/camera.png
%_datadir/icons/hicolor/16x16/apps/kgamma.png
%_datadir/icons/hicolor/32x32/apps/kgamma.png
%_datadir/icons/hicolor/48x48/apps/kgamma.png
%_datadir/services/camera.protocol
%_datadir/services/emptymultipage.desktop
%_datadir/services/kfile_bmp.desktop
%_datadir/services/kfile_dds.desktop
%_datadir/services/kfile_dvi.desktop
%_datadir/services/kfile_exr.desktop
%_datadir/services/kfile_gif.desktop
%_datadir/services/kfile_ico.desktop
%_datadir/services/kfile_jpeg.desktop
%_datadir/services/kfile_pcx.desktop
%_datadir/services/kfile_png.desktop
%_datadir/services/kfile_pnm.desktop
%_datadir/services/kfile_ps.desktop
%_datadir/services/kfile_raw.desktop
%_datadir/services/kfile_rgb.desktop
%_datadir/services/kfile_tga.desktop
%_datadir/services/kfile_tiff.desktop
%_datadir/services/kfile_xbm.desktop
%_datadir/services/kfile_xpm.desktop
%_datadir/services/scanservice.desktop
%_datadir/servicetypes/kmultipage.desktop
%_datadir/cmake/libksane.cmake

%changelog
* Mon Sep 01 2008 Liu Di <liudidi@gmail.com> - 3.5.10-1mgc
- 更新到 3.5.10

* Sat May 31 2008 Ni Hui <shuizhuyuanluo@126.com> - 3.5.9-1.1mgc
- 重建(基于 poppler-0.8.2)
- 添加上游补丁，修正 kpdf 多处 crash 问题
- 拆出 extras 包
- 戊子  四月廿七

* Wed Feb 19 2008 Liu Di <liudidi@gmail.com> - 3.5.9-1mgc
- update to 3.5.9

* Sat Dec 08 2007 Liu Di <liudidi@gmail.com> - 3.5.8-2mgc
- rebuild against new poppler

* Fri Oct 19 2007 Liu Di <liudidi@gmail.com> - 3.5.8-1mgc
- update to 3.5.8

* Fri May 25 2007 kde <athena_star {at} 163 {dot} com>  - 3.5.7-1mgc
- update to 3.5.7

* Fri Jan 26 2007 Liu Di <liudidi@gmail.com> - 3.5.6-1mgc
- update to 3.5.6

* Sat Oct 21 2006 Liu Di <liudidi@gmail.com> - 3.5.5-1mgc
- update to 3.5.5

* Fri Aug 25 2006 Liu Di <liudidi@gmail.com> - 3.5.4-1mgc
- update to 3.5.4

* Thu Jul  1 2006 Liu Di <liudidi@gmail.com> - 3.5.3-1mgc
- update to 3.5.3

* Sun Apr 16 2006 KanKer <kanker@163.com>
- 3.5.2

* Tue Nov 24 2005 KanKer <kanker@163.com>
- remove some apps

* Thu Oct 18 2005 KanKer <kanker@163.com>
- 3.4.3

* Sun Jul 31 2005 KanKer <kanker@163.com>
- 3.4.2
- replaced kpdf with 0.4.1

* Wed Jun 1 2005 KanKer <kanker@163.com>
- 3.4.1

* Sun Mar 20 2005 KanKer <kanker@163.com>
- 3.4.0

* Fri Dec 17 2004 KanKer <kanker@163.com>
- rebuild to remove libselinux.

* Thu Dec 15 2004 tingxx <tingxx@21cn.com>
- update to 3.3.2 for ML

* Sun Dec 12 2004 KanKer <kanker@163.com>
- recovered kfract and kpovmodeler,change requires liblcms to lcms.

* Mon Oct 25 2004 KanKer <kanker@163.com>
- update kpdf to cvs20041022

*Fri Oct 22 2004 KanKer <kanker@163.com>
- update kpdf to 0.4.

* Sat Oct 16 2004 KanKer <kanker@163.com>
- patched kpdf to display chinese normally.

* Fri Oct 15 2004 KanKer <kanker@163.com>
- update to 3.3.1 for ML.

* Mon Oct 4 2004 kde <jack@linux.net.cn>
- fix the spec file and rebuild

* Sat Oct 2 2004 kanker <kanker@163.com>
- initialize the first spec file
