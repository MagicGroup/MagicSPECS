#define pre_tag rc1
#define pre -%{pre_tag}

# See http://bugzilla.redhat.com/223663
%define multilib_archs x86_64 %{ix86} ppc64 ppc s390x s390 sparc64 sparcv9 mips64el mipsel
%define multilib_basearchs x86_64 ppc64 s390x sparc64 mips64el

%define real_version 4.8.7
%define release_number 1

# switches: whether to build it or not
%define with_phonon 1
# 已经单列包
%define with_webkit 1
%define with_dbus_linked 1
%define with_gtkstyle 1

%define with_mysql 1
%define with_postgresql 1
%define with_odbc 1
%define with_tds 1
%define with_firebird 1

# switches: whether to ship it or not
%define ship_phonon_pkg 1
%define ship_webkit_pkg 1

# Let's hope this is just a temporary glitch...
%define styles_are_gone 1
%define type x11

%if "%type" == "x11"
Name: qt4
%define _qtdir %_libdir/qt4
%else
Name: qt4-%type
%define _qtdir %_libdir/qt4-%type
%endif
%if "%type" == "embedded"
PLUGINS="$PLUGINS -qt-decoration-default"
for decoration in `ls src/plugins/decorations |grep -v .pro |grep -v default`; do
	PLUGINS="$PLUGINS -plugin-decoration-$decoration"
done
for gfx in `ls src/plugins/gfxdrivers |grep -v .pro`; do
	PLUGINS="$PLUGINS -plugin-gfx-$gfx"
done
%endif


Version: %{real_version}
Release:	2%{?dist}
%define ver %version

Source0: http://download.qt.io/official_releases/qt/4.8/%{version}/qt-everywhere-opensource-src-%{version}.tar.gz
#Source0: http://get.qt.nokia.com/qt/source/qt-everywhere-opensource-src-%{version}.tar.gz
#Source1: Trolltech.conf
#Source2: Designer.conf

# multilib hacks
# header file to workaround multilib issue
Source5: qconfig-multilib.h
# set default QMAKE_CFLAGS_RELEASE
Patch2: qt-x11-opensource-src-4.2.2-multilib-optflags.patch
# get rid of timestamp which causes multilib problem
Patch4: qt-everywhere-opensource-src-4.7.0-beta1-uic_multilib.patch

Patch15: qt-x11-opensource-src-4.5.1-enable_ft_lcdfilter.patch
# use system ca-bundle certs, http://bugzilla.redhat.com/521911
#Patch17: qt-x11-opensource-src-4.5.3-system_ca_certificates.patch
#Requires: ca-certificates
# phonon gstreamer services
Patch19: qt-everywhere-opensource-src-4.7.0-beta2-phonon_servicesfile.patch

# may be upstreamable, not sure yet
# workaround for gdal/grass crashers wrt glib_eventloop null deref's
Patch23: qt-everywhere-opensource-src-4.6.3-glib_eventloop_nullcheck.patch

## upstreamable bits
# fix invalid inline assembly in qatomic_{i386,x86_64}.h (de)ref implementations
Patch53: qt-x11-opensource-src-4.5.0-fix-qatomic-inline-asm.patch
# fix invalid assumptions about mysql_config --libs
# http://bugzilla.redhat.com/440673
Patch54: qt-everywhere-opensource-src-4.7.0-beta2-mysql_config.patch
# http://bugs.kde.org/show_bug.cgi?id=180051#c22
Patch55: qt-everywhere-opensource-src-4.6.2-cups.patch
# fix type cast issue on s390x
Patch56: qt-everywhere-opensource-src-4.7.0-beta1-s390x.patch
# qtwebkit to search nspluginwrapper paths too
Patch58: qt-everywhere-opensource-src-4.7.0-beta1-qtwebkit_pluginpath.patch

# indic incorrect rendering
Patch59: qt-4.6.3-bn-rendering-bz562049.patch
Patch60: qt-4.6.3-bn-rendering-bz562058.patch
Patch61: qt-4.6.3-indic-rendering-bz631732.patch
Patch62: qt-4.6.3-indic-rendering-bz636399.patch

Patch80: qt-everywhere-opensource-src-4.8.0-ld-gold.patch

# upstream patches
# upstream patches
# http://codereview.qt-project.org/#change,22006
Patch100: qt-everywhere-opensource-src-4.8.1-qtgahandle.patch
# backported from Qt5 (essentially)
# http://bugzilla.redhat.com/702493
# https://bugreports.qt-project.org/browse/QTBUG-5545
Patch102: qt-everywhere-opensource-src-4.8.5-qgtkstyle_disable_gtk_theme_check.patch
# revert fix for QTBUG-15319, fixes regression QTBUG-32908
# http://bugzilla.redhat.com/968367
# https://bugreports.qt-project.org/browse/QTBUG-32908
Patch103: QTBUG-15319-fix-shortcuts-with-secondary-Xkb-layout.patch
# workaround for MOC issues with Boost headers (#756395)
# https://bugreports.qt-project.org/browse/QTBUG-22829
Patch113: qt-everywhere-opensource-src-4.8.5-QTBUG-22829.patch
# https://codereview.qt-project.org/#change,55874
# REVERT, causes regressions http://bugzilla.redhat.com/968794
#Patch155: qt-everywhere-opensource-src-4.8-QTBUG-27809.patch

## qt-copy patches
# magic patches
Patch1100: qt-4.6.0-use-ft_glyph_embolden-to-fake-bold.patch
Patch1101: qt-4.5.0rc1-add-missing-bold-style.patch
Patch1102: qt-4.5.0rc1-faster-native-graphicssystem.patch
# qt 标签中文竖排支持
Patch1103: qt-4.7.1-qtabbartablabel-vertical_cjk_label.patch
# qt webkit 默认编码设为 gb18030
Patch1104: qt-4.7.0-qwebsettings-gb18030-default.patch
# qt webkit html/xml gb2312/gbk 认作为 gb18030
Patch1105: qt-4.8.0-webkit-htmlxml-gb-gb18030.patch
# qt webkit 在 2.31.0 以上版本的 glib 上编译的补丁
Patch1106: qt-4.8.0-webkit-newglib.patch


# kde-qt git patches
#Patch202: 0002-This-patch-makes-override-redirect-windows-popup-men.patch
#Patch204: 0004-This-patch-adds-support-for-using-isystem-to-allow-p.patch
#Patch205: 0005-When-tabs-are-inserted-or-removed-in-a-QTabBar.patch
#Patch212: 0012-Add-context-to-tr-calls-in-QShortcut.patch

# from opensuse project
Patch1001: use-freetype-default.diff

## qt-copy patches
Patch10118: 0118-qtcopy-define.diff
Patch10180: 0180-window-role.diff
Patch10195: 0195-compositing-properties.diff
Patch10209: 0209-prevent-qt-mixing.diff
Patch10216: 0216-allow-isystem-for-headers.diff
Patch10225: 0225-invalidate-tabbar-geometry-on-refresh.diff
Patch10289: 0289-context-for-shortcuts-tr.diff

Patch20000: qt4-4.8.6-atomics_not_const.diff
# compile patches


Source10: qt4-wrapper.sh
Source11: qt4.sh
Source12: qt4.csh

Source20: assistant.desktop
Source21: designer.desktop
Source22: linguist.desktop
Source23: qtdemo.desktop
Source24: qtconfig.desktop

# upstream qt4-logo, http://trolltech.com/images/products/qt/qt4-logo
Source30: hi128-app-qt4-logo.png
Source31: hi48-app-qt4-logo.png

BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: findutils
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: libjpeg-devel
BuildRequires: libmng-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: libungif-devel
BuildRequires: freetype-devel
BuildRequires: zlib-devel
BuildRequires: glib2-devel
BuildRequires: openssl-devel
%if %with_gtkstyle
BuildRequires: gtk2-devel
%endif
%if %with_phonon
BuildRequires: gstreamer-devel >= 0.10.12
BuildRequires: gstreamer-plugins-base-devel
%endif
%if %with_mysql
BuildRequires: mysql-devel
%endif
%if %with_postgresql
BuildRequires: postgresql-devel
%endif
%if %with_odbc
BuildRequires: unixODBC-devel
%endif
%if %with_tds
BuildRequires: freetds-devel
%endif
%if %with_firebird
BuildRequires: firebird-devel
%endif

Summary: Newer version of the Qt toolkit
Summary(zh_CN.UTF-8): 新版 Qt 开发工具集
URL: http://www.trolltech.com/qt/
License: LGPLv2 with exceptions or GPLv3 with exceptions
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Requires: %name-core = %version-%release
Requires: %name-network = %version-%release
Requires: %name-xml = %version-%release
Requires: %name-gui = %version-%release
Requires: %name-compat = %version-%release
Requires: %name-opengl = %version-%release
Requires: %name-sql = %version-%release
Requires: %name-jpeg = %version-%release
Requires: %name-gif = %version-%release
Requires: %name-svg = %version-%release
Requires: %name-mng = %version-%release
Requires: %name-script = %version-%release
Requires: %name-dbus = %version-%release
Obsoletes: %name-png
Provides: %name-png = %version-%release

%description
This is a newer version of the Qt toolkit than the Qt 3.x.x version
used by most applications at this time.

It is recommended to use this for the development of new applications.

%description -l zh_CN.UTF-8
这是新版的 Qt 开发工具集。

%package devel
Summary: Development files for %name
Summary(zh_CN.UTF-8): %name 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %name = %version-%release
Requires: %name-core-devel = %version-%release
Requires: %name-network-devel = %version-%release
Requires: %name-xml-devel = %version-%release
Requires: %name-gui-devel = %version-%release
Requires: %name-compat-devel = %version-%release
Requires: %name-opengl-devel = %version-%release
Requires: %name-sql-devel = %version-%release
Requires: %name-svg-devel = %version-%release
Requires: %name-script-devel = %version-%release
Requires: %name-dbus-devel = %version-%release
Requires: qmake = %version-%release

%description devel
Development files (Headers etc.) for %name.

%description devel -l zh_CN.UTF-8
%name 的开发文件(头文件等)。

%package -n qmake
Summary: Makefile generator for Qt based applications
Summary(zh_CN.UTF-8): 基于 Qt 应用程序的 Makefile 生成器
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Provides: %name-qmake = %version-%release

%description -n qmake
Makefile generator for Qt based applications.

%description -n qmake -l zh_CN.UTF-8
基于 Qt 应用程序的 Makefile 生成器。

%package doc
Summary: Document files for %name
Summary(zh_CN.UTF-8): %name 的开发文档文件
Group: Development/Document
Group(zh_CN.UTF-8): 开发/文档

%description doc
Document files for %name.

%description doc -l zh_CN.UTF-8
%name 的开发文档文件。

%package core
Summary: The core of the %name library
Summary(zh_CN.UTF-8): %name 库的核心
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description core
Basic functionality of the Qt library.

%description core -l zh_CN.UTF-8
%name 库的基本核心功能。

%package core-devel
Summary: Development files for the core of the %name library
Summary(zh_CN.UTF-8): %name 库的核心开发文件
Requires: %name-core = %version-%release
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description core-devel
Development files for Qt basics.

%description core-devel -l zh_CN.UTF-8
%name 库的核心开发文件。

%package network
Summary: Network support for the %name library
Summary(zh_CN.UTF-8): %name 库的网络支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description network
Network support for %name.

%description network -l zh_CN.UTF-8
%name 库的网络支持。

%package network-devel
Summary: Development files for %name network support
Summary(zh_CN.UTF-8): %name 网络支持的开发文件
Requires: %name-network = %version-%release
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description network-devel
Development files for %name network support.

%description network-devel -l zh_CN.UTF-8
%name 网络支持的开发文件。

%package script
Summary: Script support for the %name library
Summary(zh_CN.UTF-8): %name 库的脚本支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Obsoletes: %{name}-qtscript

%description script
Script support for %name.

%description script -l zh_CN.UTF-8
%name 库的脚本支持。

%package script-devel
Summary: Development files for %name script support
Summary(zh_CN.UTF-8): %name 脚本支持的开发文件
Requires: %name-script = %version-%release
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Obsoletes: %{name}-qtscript-devel

%description script-devel
Development files for %name script support.

%description script-devel -l zh_CN.UTF-8
%name 脚本支持的开发文件。

%package scripttools
Summary: Script tools support for the %name library
Summary(zh_CN.UTF-8): %name 库的脚本工具支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Obsoletes: %{name}-qtscripttools

%description scripttools
Script tools support for %name.

%description scripttools -l zh_CN.UTF-8
%name 库的脚本工具支持。

%package scripttools-devel
Summary: Development files for %name scripttools support
Summary(zh_CN.UTF-8): %name 脚本工具支持的开发文件
Requires: %name-scripttools = %version-%release
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Obsoletes: %{name}-qtscripttools-devel

%description scripttools-devel
Development files for %name scripttools support.

%description scripttools-devel -l zh_CN.UTF-8
%name 脚本工具支持的开发文件。

%package xml
Summary: XML support for the %name library
Summary(zh_CN.UTF-8): %name 库的可扩展标记语言支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description xml
XML parsing support for the %name library.

%description xml -l zh_CN.UTF-8
%name 库的可扩展标记语言解析支持。

%package xml-devel
Summary: Development files for %name XML support
Summary(zh_CN.UTF-8): %name 可扩展标记语言支持的开发文件
Requires: %name-xml = %version-%release
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description xml-devel
Development files for %name XML support.

%description xml-devel -l zh_CN.UTF-8
%name 可扩展标记语言支持的开发文件。

%package declarative
Summary: QML declarative support for the %name library
Summary(zh_CN.UTF-8): %name 库的 QML 声明性语言支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description declarative
QML declarative support for the %name library.

%description declarative -l zh_CN.UTF-8
%name 库的 QML 声明性语言支持。

%package declarative-devel
Summary: Development files for %name QML declarative support
Summary(zh_CN.UTF-8): %name QML 声明性语言支持的开发文件
Requires: %name-declarative = %version-%release
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description declarative-devel
Development files for %name QML declarative support.

%description declarative-devel -l zh_CN.UTF-8
%name QML 声明性语言支持的开发文件。

%package gui
Summary: GUI part of the %name library
Summary(zh_CN.UTF-8): %name 库的图形用户界面部分
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description gui
GUI support for the %name library.

%description gui -l zh_CN.UTF-8
%name 库的图形用户界面支持。

%package gui-devel
Summary: Development files for %name GUI support
Summary(zh_CN.UTF-8): %name 图形用户界面支持的开发文件
Requires: %name-gui = %version-%release
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description gui-devel
Development files for %name GUI support.

%description gui-devel -l zh_CN.UTF-8
%name 图形用户界面支持的开发文件。

%package compat
Summary: Qt 3.x compatibility support for %name
Summary(zh_CN.UTF-8): %name 的 Qt 3.x 兼容支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description compat
Qt 3.x compatibility support for %name.

%description compat -l zh_CN.UTF-8
%name 的 Qt 3.x 兼容支持。

%package compat-devel
Summary: Development files for %name Qt 3.x compatibility support
Summary(zh_CN.UTF-8): %name Qt 3.x 兼容支持的开发文件
Requires: %name-compat = %version-%release
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description compat-devel
Development files for %name Qt 3.x compatibility.

%description compat-devel -l zh_CN.UTF-8
%name Qt 3.x 兼容支持的开发文件。

%package designer
Summary: Graphical user interface designer
Summary(zh_CN.UTF-8): 图形用户界面设计器
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具

%description designer
A graphical user interface designer.

%description designer -l zh_CN.UTF-8
图形用户界面设计器。

%package linguist
Summary: Translation tool
Summary(zh_CN.UTF-8): 翻译工具
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具

%description linguist
Application translation tool.

%description linguist -l zh_CN.UTF-8
应用程序翻译工具。

%package opengl
Summary: OpenGL (3D API) support for the %name library
Summary(zh_CN.UTF-8): %name 库的 OpenGL (3D API) 支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description opengl
OpenGL (3D API) support for %name.

%description opengl -l zh_CN.UTF-8
%name 库的 OpenGL (3D API) 支持。

%package opengl-devel
Summary: Development files for %name OpenGL (3D API) support
Summary(zh_CN.UTF-8): %name OpenGL (3D API) 支持的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description opengl-devel
Development files for %name OpenGL (3D) support.

%description opengl-devel -l zh_CN.UTF-8
%name OpenGL (3D API) 支持的开发文件。

%package qtconfig
Summary: %name configuration tool
Summary(zh_CN.UTF-8): %name 配置工具
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具

%description qtconfig
%name configuration tool.

%description qtconfig -l zh_CN.UTF-8
%name 配置工具。

%package sql
Summary: SQL (Database protocol) support for the %name library
Summary(zh_CN.UTF-8): %name 库的结构化查询语言(数据库协议)支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description sql
SQL database connectivity for %name.

%description sql -l zh_CN.UTF-8
%name 库的结构化查询语言(数据库协议)支持。

%package sql-devel
Summary: Development files for %name SQL (database protocol) support
Summary(zh_CN.UTF-8): %name 结构化查询语言(数据库协议)支持的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description sql-devel
Development files for %name SQL support.

%description sql-devel -l zh_CN.UTF-8
%name 结构化查询语言(数据库协议)支持的开发文件。

%package assistant
Summary: Qt development documentation viewer
Summary(zh_CN.UTF-8): Qt 开发文档查看器
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
# assisitant-devel not necessary any more
Obsoletes: %{name}-assistant-devel

%description assistant
API documentation viewer for %name.

%description assistant -l zh_CN.UTF-8
Qt API 开发文档查看器。

#%package assistant-devel
#Summary: Development files for the Qt documentation viewer
#Summary(zh_CN.UTF-8): Qt 文档查看器的开发文件
#Group: Development/Libraries/C++/Documentation
#Group(zh_CN.UTF-8): 开发/库/C++/文档
#
#%description assistant-devel
#Development files for the Qt documentation viewer.
#
#Install this package if you wish to embed Qt Assistant into your own
#applications.
#
#%description assistant-devel -l zh_CN.UTF-8
#Qt 文档查看器的开发文件。可内嵌 Qt 助手到您自己的应用程序中。

%package inputmethods
Summary: Support for non-latin character input
Summary(zh_CN.UTF-8): 非拉丁字符输入支持
Group: System/Libraries
Group(zh_CN.UTF-8): 系统/库
Requires: %name-gui = %version-%release

%description inputmethods
Support for non-latin character input.

%description inputmethods -l zh_CN.UTF-8
非拉丁字符输入支持。

%package chinese
Summary: Chinese character coding support for %name
Summary(zh_CN.UTF-8): %name 的中文字符编码支持
Group: Internationalization/Chinese
Group(zh_CN.UTF-8): 国际化/中文

%description chinese
Chinese character coding support for %name.

%description chinese -l zh_CN.UTF-8
%name 的中文字符编码支持。

%package japanese
Summary: Japanese character coding support for %name
Summary(zh_CN.UTF-8): %name 的日文字符编码支持
Group: Internationalization/Japanese
Group(zh_CN.UTF-8): 国际化/日文

%description japanese
Japanese character coding support for %name.

%description japanese -l zh_CN.UTF-8
%name 的日文字符编码支持。

%package korean
Summary: Korean character coding support for %name
Summary(zh_CN.UTF-8): %name 的韩文字符编码支持
Group: Internationalization/Korean
Group(zh_CN.UTF-8): 国际化/韩文

%description korean
Korean character coding support for %name.

%description korean -l zh_CN.UTF-8
%name 的韩文字符编码支持。

%package taiwanese
Summary: Taiwanese character coding support for %name
Summary(zh_CN.UTF-8): %name 的台湾字字符编码支持
Group: Internationalization/Taiwanese
Group(zh_CN.UTF-8): 国际化/台湾字

%description taiwanese
Taiwanese character coding support for %name.

%description taiwanese -l zh_CN.UTF-8
%name 的台湾字字符编码支持。

%package cjk
Summary: CJK character coding support for %name
Summary(zh_CN.UTF-8): %name 的中日韩字符编码支持
Group: Internationalization/CJK
Group(zh_CN.UTF-8): 国际化/中日韩
Requires: %name = %version-%release
Requires: %name-chinese = %version-%release
Requires: %name-japanese = %version-%release
Requires: %name-korean = %version-%release
Requires: %name-taiwanese = %version-%release
Requires: %name-inputmethods = %version-%release

%description cjk
CJK character coding support for %name.

%description cjk -l zh_CN.UTF-8
%name 的中日韩字符编码支持。

%package jpeg
Summary: JPEG image format support for %name
Summary(zh_CN.UTF-8): %name 的 JPEG 图像格式支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description jpeg
JPEG image format support for %name.

%description jpeg -l zh_CN.UTF-8
%name 的 JPEG 图像格式支持。

%package gif
Summary: GIF image format support for %name
Summary(zh_CN.UTF-8): %name 的 GIF 图像格式支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description gif
GIF image format support for %name.

%description gif -l zh_CN.UTF-8
%name 的 GIF 图像格式支持。

%package tga
Summary: TGA image format support for %name
Summary(zh_CN.UTF-8): %name 的 TGA 图像格式支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description tga
TGA image format support for %name.

%description tga -l zh_CN.UTF-8
%name 的 TGA 图像格式支持。

%package ico
Summary: ICO image format support for %name
Summary(zh_CN.UTF-8): %name 的 ICO 图像格式支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description ico
ICO image format support for %name.

%description ico -l zh_CN.UTF-8
%name 的 ICO 图像格式支持。

%package mng
Summary: MNG image format support for %name
Summary(zh_CN.UTF-8): %name 的 MNG 图像格式支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description mng
MNG image format support for %name.

%description mng -l zh_CN.UTF-8
%name 的 MNG 图像格式支持。

%package svg
Summary: SVG image format support for %name
Summary(zh_CN.UTF-8): %name 的 SVG 图像格式支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description svg
SVG image format support for %name.

%description svg -l zh_CN.UTF-8
%name 的 SVG 图像格式支持。

%package svg-devel
Summary: Development files for SVG image format support for %name
Summary(zh_CN.UTF-8): %name 的 SVG 图像格式支持的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description svg-devel
Development files for SVG image format support for %name.

%description svg-devel -l zh_CN.UTF-8
%name 的 SVG 图像格式支持的开发文件。

%package test
Summary: Qt unit test support
Summary(zh_CN.UTF-8): Qt 单元测试支持
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Requires: %name = %version-%release

%description test
Qt unit test support.

%description test -l zh_CN.UTF-8
Qt 单元测试支持。

%if %with_mysql
%package mysql
Summary: MySQL connectivity support for %name
Summary(zh_CN.UTF-8): %name 的 MySQL 数据库通讯连接支持
Requires: %name-sql = %version-%release
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description mysql
MySQL connectivity support for %name.

%description mysql -l zh_CN.UTF-8
%name 的 MySQL 数据库通讯连接支持。
%endif

%package sqlite
Summary: SQLite connectivity support for %name
Summary(zh_CN.UTF-8): %name 的 SQLite 数据库通讯连接支持
Requires: %name-sql = %version-%release
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description sqlite
SQLite connectivity support for %name.

%description sqlite -l zh_CN.UTF-8
%name 的 SQLite 数据库通讯连接支持。

%if %with_tds
%package tds
Summary: TDS connectivity support for %name
Summary(zh_CN.UTF-8): %name 的 TDS 数据库通讯连接支持
Requires: %name-sql = %version-%release
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description tds
TDS connectivity support for %name.

%description tds -l zh_CN.UTF-8
%name 的 TDS 数据库通讯连接支持。
%endif

%if %with_odbc
%package odbc
Summary: ODBC connectivity support for %name
Summary(zh_CN.UTF-8): %name 的 ODBC 数据库通讯连接支持
Requires: %name-sql = %version-%release
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description odbc
ODBC connectivity support for %name.

%description odbc -l zh_CN.UTF-8
%name 的 ODBC 数据库通讯连接支持。
%endif

%if %with_postgresql
%package postgresql
Summary: PostgreSQL connectivity support for %name
Summary(zh_CN.UTF-8): %name 的 PostgreSQL 数据库通讯连接支持
Requires: %name-sql = %version-%release
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description postgresql
PostgreSQL connectivity support for %name.

%description postgresql -l zh_CN.UTF-8
%name 的 PostgreSQL 数据库通讯连接支持。
%endif

%if %with_firebird
%package firebird
Summary: IBase connectivity support for %name
Summary(zh_CN.UTF-8): %name 的 IBase 数据库通讯连接支持
Requires: %name-sql = %version-%release
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description firebird
IBase connectivity support for %name.

%description firebird -l zh_CN.UTF-8
%name 的 IBase 数据库通讯连接支持。
%endif

%package style-windows
Summary: Qt theme emulating the look of Windows(tm) 9x/Me/NT4/2000
Summary(zh_CN.UTF-8): Windows(tm) 9x/Me/NT4/2000 主题外观模拟
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: %name-gui = %version-%release

%description style-windows
Qt theme emulating the look of Windows(tm) 9x/Me/NT4/2000.

%description style-windows -l zh_CN.UTF-8
Windows(tm) 9x/Me/NT4/2000 主题外观模拟。

%package style-motif
Summary: Qt theme emulating the look of Motif (traditional UNIX)
Summary(zh_CN.UTF-8): Motif (传统 UNIX) 主题外观模拟
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: %name-gui = %version-%release

%description style-motif
Qt theme emulating the look of Motif (traditional UNIX).

%description style-motif -l zh_CN.UTF-8
Motif (传统 UNIX) 主题外观模拟。

%package style-cde
Summary: Qt theme emulating the look of CDE (traditional UNIX)
Summary(zh_CN.UTF-8): CDE (传统 UNIX) 主题外观模拟
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: %name-gui = %version-%release

%description style-cde
Qt theme emulating the look of CDE (traditional UNIX).

%description style-cde -l zh_CN.UTF-8
CDE (传统 UNIX) 主题外观模拟。

%package demos
Summary: Demo programs for the Qt toolkit
Summary(zh_CN.UTF-8): Qt 开发工具集的演示程序
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: %name-gui = %version-%release
Requires: %name-doc = %version-%release

%description demos
%summary.

%description demos -l zh_CN.UTF-8
Qt 开发工具集的演示程序。

%package examples
Summary: Example programs for the Qt toolkit
Summary(zh_CN.UTF-8): Qt 开发工具集的示例程序
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: %name-gui = %version-%release

%description examples
%summary.

%description examples -l zh_CN.UTF-8
Qt 开发工具集的示例程序。

%package dbus
Summary: DBus support for the %name library
Summary(zh_CN.UTF-8): %name 库的进程通讯总线支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Obsoletes: %{name}-qtdbus

%description dbus
DBus support for %name.

%description dbus -l zh_CN.UTF-8
%name 库的进程通讯总线支持。

%package dbus-devel
Summary: Development files for %name dbus support
Summary(zh_CN.UTF-8): %name 进程通讯总线支持的开发文件
Requires: %name-dbus = %version-%release
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Obsoletes: %{name}-qtdbus-devel

%description dbus-devel
Development files for %name dbus support.

%description dbus-devel -l zh_CN.UTF-8
%name 进程通讯总线支持的开发文件。

%package clucene
Summary: clucene support for the %name library
Summary(zh_CN.UTF-8): %name 库的 clucene 支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description clucene
clucene support for %name.

%description clucene -l zh_CN.UTF-8
%name 库的 clucene 支持。

%package clucene-devel
Summary: Development files for %name clucene support
Summary(zh_CN.UTF-8): %name clucene 支持的开发文件
Requires: %name-clucene = %version-%release
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description clucene-devel
Development files for %name clucene support.

%description clucene-devel -l zh_CN.UTF-8
%name clucene 支持的开发文件。

%package xmlpatterns
Summary: xmlpatterns support for the %name library
Summary(zh_CN.UTF-8): %name 库的可扩展标记语言模式支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description xmlpatterns
xmlpatterns support for %name.

%description xmlpatterns -l zh_CN.UTF-8
%name 库的可扩展标记语言模式支持。

%package xmlpatterns-devel
Summary: Development files for %name xmlpatterns support
Summary(zh_CN.UTF-8): %name 可扩展标记语言模式支持的开发文件
Requires: %name-xmlpatterns = %version-%release
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description xmlpatterns-devel
Development files for %name xmlpatterns support.

%description xmlpatterns-devel -l zh_CN.UTF-8
%name 可扩展标记语言模式支持的开发文件。

%package multimedia
Summary: multimedia support for the %name library
Summary(zh_CN.UTF-8): %name 库的多媒体服务支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description multimedia
multimedia support for %name.

%description multimedia -l zh_CN.UTF-8
%name 库的多媒体服务支持。

%package multimedia-devel
Summary: Development files for %name multimedia support
Summary(zh_CN.UTF-8): %name 多媒体服务支持的开发文件
Requires: %name-multimedia = %version-%release
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description multimedia-devel
Development files for %name multimedia support.

%description multimedia-devel -l zh_CN.UTF-8
%name 多媒体服务支持的开发文件。

%package help
Summary: help support for the %name library
Summary(zh_CN.UTF-8): %name 库的帮助支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description help
help support for %name.

%description help -l zh_CN.UTF-8
%name 库的帮助支持。

%package help-devel
Summary: Development files for %name help support
Summary(zh_CN.UTF-8): %name 帮助支持的开发文件
Requires: %name-help = %version-%release
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description help-devel
Development files for %name help support.

%description help-devel -l zh_CN.UTF-8
%name 帮助支持的开发文件。

%if %with_phonon
%package phonon
Summary: Phonon support for %name library
Summary(zh_CN.UTF-8): %name 库的通用多媒体后端支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
# FIXME
#Conflicts: kdelibs4-devel < 4.1

%description phonon
%summary.

%description phonon -l zh_CN.UTF-8
%name 库的通用多媒体后端支持。

%package phonon-gstreamer
Summary: Phonon gstreamer backend
Summary(zh_CN.UTF-8): Phonon gstreamer 后端
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
# FIXME
#Conflicts: phonon-gstreamer

%description phonon-gstreamer
%summary.

%description phonon-gstreamer -l zh_CN.UTF-8
Phonon gstreamer 后端。

%package phonon-devel
Summary: Development files for %name phonon support
Summary(zh_CN.UTF-8): %name 通用多媒体后端支持的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %name-phonon = %version-%release
# FIXME
#Conflicts: kdelibs4-devel < 4.1

%description phonon-devel
%summary.

%description phonon-devel -l zh_CN.UTF-8
%name 通用多媒体后端支持的开发文件。
%endif

%if %with_webkit
%package webkit
Summary: WebKit support for %name library
Summary(zh_CN.UTF-8): %name 库的 WebKit 网页渲染支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
# FIXME
#Conflicts: WebKit-qt-devel

%description webkit
%summary.

%description webkit -l zh_CN.UTF-8
%name 库的 WebKit 网页渲染支持。

%package webkit-devel
Summary: Development files for %name WebKit support
Summary(zh_CN.UTF-8): %name WebKit 网页渲染支持的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
# FIXME
#Conflicts: WebKit-qt-devel
Requires: %name-webkit = %version-%release

%description webkit-devel
%summary.

%description webkit-devel -l zh_CN.UTF-8
%name WebKit 网页渲染支持的开发文件。

%endif

%prep

%setup -q -n qt-everywhere-opensource-src-%{version}%{?pre}

#export QTDIR=%_qtdir
#export QMAKE=`pwd`/qmake/qmake

# multilib hacks
# don't use -b on mkspec files, else they get installed too.
# multilib hacks no longer required
#%patch2 -p1
#%patch4 -p1 -b .uic_multilib

%patch15 -p1 -b .enable_ft_lcdfilter
#%patch17 -p1 -b .system_ca_certificates
%patch19 -p1 -b .phonon_servicesfile
%patch23 -p1 -b .glib_eventloop_nullcheck

%patch53 -p1 -b .qatomic-inline-asm
%patch54 -p1 -b .mysql_config
%patch55 -p1 -b .cups-1
#%patch56 -p1 -b .typecast_s390x
#%patch57 -p1 -b .typecast_sparc64
%patch58 -p1 -b .qtwebkit_pluginpath

#%patch59 -p1 -b .bn-rendering-bz562049
#%patch60 -p1 -b .bn-rendering-bz562058
#%patch61 -p1 -b .indic-rendering-bz631732
#%patch62 -p1 -b .indic-rendering-bz636399

#%patch80 -p1 -b .gold_ld

# upstream patches
%patch102 -p1 -b .qgtkstyle_disable_gtk_theme_check
%patch113 -p1 -b .QTBUG-22829

# patches from magic
#%patch100 -p1
#%patch101 -p1
#%patch102 -p0
%patch1103 -p1
%patch1104 -p1
%patch1105 -p1
#%patch106 -p1

# opensuse patches
# %patch1001 -p0

## qt-copy patches
#%patch10118 -p0
#%patch10180 -p1
#%patch10195 -p0
#%patch10209 -p0
#%patch10216 -p0
#%patch10225 -p1
#%patch10289 -p1

%patch20000 -p1
# compile patches

# drop -fexceptions from $RPM_OPT_FLAGS
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`

%define platform linux-g++

# some 64bit platforms assume -64 suffix, https://bugzilla.redhat.com/569542
%if "%{?__isa_bits}"  == "64"
%define platform linux-g++-64
%endif

# https://bugzilla.redhat.com/478481
%ifarch x86_64 mips64el
%define platform linux-g++
%endif

sed -i \
  -e "s|-O2|$RPM_OPT_FLAGS|g" \
  -e "s|g++.conf|g++-multilib.conf|g" \
  mkspecs/%{platform}/qmake.conf

# undefine QMAKE_STRIP, so we get useful -debuginfo pkgs
sed -i -e "s|^QMAKE_STRIP.*=.*|QMAKE_STRIP             =|" mkspecs/common/linux.conf

# set correct lib path
if [ "%{_lib}" == "lib64" ] ; then
  sed -i -e "s,/usr/lib /lib,/usr/%{_lib} /%{_lib},g" config.tests/{unix,x11}/*.test
  sed -i -e "s,/lib /usr/lib,/%{_lib} /usr/%{_lib},g" config.tests/{unix,x11}/*.test
fi

# let makefile create missing .qm files, the .qm files should be included in qt upstream
for f in translations/*.ts ; do
  touch ${f%.ts}.qm
done

#perl -pi -e 's,^QMAKE_CFLAGS_RELEASE	=.*,QMAKE_CFLAGS_RELEASE	= %optflags,g' mkspecs/*g++*/qmake.conf

# undefine QMAKE_STRIP, so we get useful -debuginfo pkgs
#sed -i -e "s|^QMAKE_STRIP.*=.*|QMAKE_STRIP             =|" mkspecs/common/linux.conf

%build
# build shared, threaded (default) libraries
./configure -v \
%ifarch mips64el
    -platform %{platform} \
%endif
    -confirm-license \
    -opensource \
	-optimized-qmake \
	-prefix %_qtdir \
	-sysconfdir %{_sysconfdir} \
	-release \
	-shared \
	-system-zlib \
	-system-libmng \
	-system-libpng \
	-system-libjpeg \
	-system-libtiff \
	-no-nis \
	-no-rpath \
	-cups \
	-stl \
%ifarch mips64el
	-no-pch \
%else
	-pch \
%endif
	-accessibility \
	-reduce-exports \
	-reduce-relocations \
	-no-separate-debug-info \
%if "%type" == "x11"
	-no-nas-sound \
	-sm \
	-stl \
	-xshape \
	-xinerama \
	-xinput \
	-xcursor \
	-xrandr \
	-xrender \
	-xkb \
	-fontconfig \
%endif
%if "%type" == "embedded"
	-freetype -depths 4,8,16,24,32 \
	-qt-kbd-tty \
	-qt-kbd-usb \
	-qt-mouse-pc \
%endif
	-openssl-linked \
	-xmlpatterns \
%if %with_gtkstyle
	-gtkstyle \
%endif
%if %with_dbus_linked
	-dbus-linked \
%else
	-no-dbus \
%endif
%if %with_phonon
	-phonon -gstreamer \
%else
	-no-phonon -no-gstreamer \
%endif
%if %with_webkit
	-webkit \
%else
	-no-webkit \
%endif
%if %with_postgresql
	-plugin-sql-psql \
%endif
%if %with_mysql
	-plugin-sql-mysql \
%endif
%if %with_odbc
	-plugin-sql-odbc \
%endif
%if %with_tds
	-plugin-sql-tds \
%endif
%if %with_firebird
	-plugin-sql-ibase \
%endif
	-plugin-sql-sqlite

export QTDIR=`pwd`
make %?_smp_mflags

# recreate .qm files
LD_LIBRARY_PATH=`pwd`/lib bin/lrelease translations/*.ts

%install
rm -rf $RPM_BUILD_ROOT
export QTDIR=`pwd`

# Kill some build root references
sed -i -e "s,`pwd`,%_qtdir,g" lib/*.prl lib/*.la

make %?_smp_mflags install INSTALL_ROOT="$RPM_BUILD_ROOT"
cp -a plugins/codecs $RPM_BUILD_ROOT%_qtdir/plugins

# FHS-ify a bit... And remove buildroot references
mkdir -p $RPM_BUILD_ROOT%_libdir $RPM_BUILD_ROOT%_includedir $RPM_BUILD_ROOT%_bindir
mkdir -p $RPM_BUILD_ROOT%_libdir/pkgconfig
mv $RPM_BUILD_ROOT%_qtdir/lib/pkgconfig/*.pc $RPM_BUILD_ROOT%_libdir/pkgconfig
perl -pi -e "s,-L$RPM_BUILD_DIR/.*/lib ,," $RPM_BUILD_ROOT%_libdir/pkgconfig/*

# 删除 *.la 文件
rm -f %{buildroot}%_qtdir/lib/lib*.la

# 添加 qt4 对 /usr/lib/ 目录的链接
pushd %{buildroot}%_qtdir/lib
for i in *.so* *.a *.prl; do
	ln -sf %_qtdir/lib/$i %{buildroot}%_libdir
done
popd

# 添加 qt4 对 /usr/include/ 目录的链接
pushd %{buildroot}%_qtdir/include
for i in *; do
	ln -sf %_qtdir/include/$i %{buildroot}%_includedir
done
popd

# 添加 qt4 对 /usr/bin/ 目录的链接
pushd %{buildroot}%_qtdir/bin
for i in *; do
	if [ "$i" = "qt3to4" -o "$i" = "uic3" -o "$i" = "qdoc3" ]; then
		ln -sf %_qtdir/bin/$i %{buildroot}%_bindir
	else
		ln -sf %_qtdir/bin/$i %{buildroot}%_bindir/${i}4
		ln -sf %_qtdir/bin/$i %{buildroot}%_bindir/${i}-qt4
	fi
done
popd

# 添加菜单项
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --vendor="%{name}" \
  %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24}

# qt4-logo (generic) icons
install -p -m 644 -D %{SOURCE30} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/qt4-logo.png
install -p -m 644 -D %{SOURCE31} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/qt4-logo.png
# linguist icons
for icon in tools/linguist/linguist/images/icons/linguist-*-32.png ; do
  size=$(echo $(basename ${icon}) | cut -d- -f2)
  install -p -m644 -D ${icon} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/linguist4.png
done

%ifarch %{multilib_archs}
# multilib: qconfig.h
  mv %{buildroot}%{_qt4_headerdir}/Qt/qconfig.h %{buildroot}%{_qt4_headerdir}/QtCore/qconfig-%{__isa_bits}.h
  install -p -m644 -D %{SOURCE5} %{buildroot}%{_qt4_headerdir}/QtCore/qconfig-multilib.h
  ln -sf qconfig-multilib.h %{buildroot}%{_qt4_headerdir}/QtCore/qconfig.h
  ln -sf ../QtCore/qconfig.h %{buildroot}%{_qt4_headerdir}/Qt/qconfig.h
%endif

# ld 目录支持
%if "%{_qt4_libdir}" != "%{_libdir}"
  mkdir -p %{buildroot}/etc/ld.so.conf.d
  echo "%{_qt4_libdir}" > %{buildroot}/etc/ld.so.conf.d/qt4-%{__isa_bits}.conf
%endif

# 添加 qt4.sh/qt4.csh 以方便编译
mkdir -p %{buildroot}/etc/profile.d
cp %SOURCE11 %{buildroot}/etc/profile.d
cp %SOURCE12 %{buildroot}/etc/profile.d

magic_rpm_clean.sh

# FIXME do we really need to remove the following files? --- nihui
%if 0
# 删除其它平台编译器的 qmake 配置文件
# rm -rfv %{buildroot}%_qtdir/mkspecs/aix*
# rm -rfv %{buildroot}%_qtdir/mkspecs/cygwin*
# rm -rfv %{buildroot}%_qtdir/mkspecs/darwin*
# rm -rfv %{buildroot}%_qtdir/mkspecs/features/mac
# rm -rfv %{buildroot}%_qtdir/mkspecs/features/win32
# rm -rfv %{buildroot}%_qtdir/mkspecs/freebsd*
# rm -rfv %{buildroot}%_qtdir/mkspecs/hpux*
# rm -rfv %{buildroot}%_qtdir/mkspecs/hurd*
# rm -rfv %{buildroot}%_qtdir/mkspecs/irix*
# rm -rfv %{buildroot}%_qtdir/mkspecs/lynxos*
# rm -rfv %{buildroot}%_qtdir/mkspecs/macx*
# rm -rfv %{buildroot}%_qtdir/mkspecs/netbsd*
# rm -rfv %{buildroot}%_qtdir/mkspecs/openbsd*
# rm -rfv %{buildroot}%_qtdir/mkspecs/sco*
# rm -rfv %{buildroot}%_qtdir/mkspecs/solaris*
# rm -rfv %{buildroot}%_qtdir/mkspecs/tru64*
# rm -rfv %{buildroot}%_qtdir/mkspecs/win*
%endif

# 不提供的第三方已有的软件包文件
%if %with_phonon && !%ship_phonon_pkg
rm -rfv %{buildroot}%_libdir/libphonon.*
rm -rfv %{buildroot}%_qtdir/lib/libphonon.*
rm -rfv %{buildroot}%_includedir/phonon
rm -rfv %{buildroot}%_qtdir/include/phonon/
#rm -rfv %{buildroot}%_qtdir/include/Qt/phonon
rm -rfv %{buildroot}%_libdir/pkgconfig/phonon.pc
rm -rfv %{buildroot}%_qtdir/plugins/phonon_backend
%endif
%if %with_webkit && !%ship_webkit_pkg
rm -rfv %{buildroot}%_libdir/libQtWebKit.*
rm -rfv %{buildroot}%_qtdir/lib/libQtWebKit.*
rm -rfv %{buildroot}%_includedir/QtWebKit
rm -rfv %{buildroot}%_qtdir/include/QtWebKit
rm -rfv %{buildroot}%_qtdir/include/Qt/QtWebKit
rm -rfv %{buildroot}%_libdir/pkgconfig/QtWebKit.pc
%endif

# Qt.pc
cat >%{buildroot}%{_libdir}/pkgconfig/Qt.pc<<EOF
prefix=%{_qt4_prefix}
bindir=%{_qt4_bindir}
datadir=%{_qt4_datadir}
demosdir=%{_qt4_demosdir}
docdir=%{_qt4_docdir}
examplesdir=%{_qt4_examplesdir}
headerdir=%{_qt4_headerdir}
importdir=%{_qt4_importdir}
libdir=%{_qt4_libdir}
moc=%{_qt4_bindir}/moc
plugindir=%{_qt4_plugindir}
qmake=%{_qt4_bindir}/qmake
sysconfdir=%{_qt4_sysconfdir}
translationdir=%{_qt4_translationdir}

Name: Qt
Description: Qt Configuration
Version: %{version}
EOF

# rpm macros
# 无下划线开头的宏由 magiclinux project 定义
# 下划线开头的宏为 fedora project 兼容目的
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat >%{buildroot}%{_sysconfdir}/rpm/macros.qt4<<EOF
%%qt4_name		%{name}
%%qt4_version		%{version}
%%qt4_prefix		%{_qtdir}
%%qt4_bindir		%%{qt4_prefix}/bin
%%qt4_libdir		%%{qt4_prefix}/lib
%%qt4_docdir		%%{qt4_prefix}/doc
%%qt4_includedir	%%{qt4_prefix}/include
%%qt4_pluginsdir	%%{qt4_prefix}/plugins
%%qt4_qmake		%%{qt4_prefix}/bin/qmake
%%qt4_importdir		%%{qt4_prefix}/imports
#
###  以下为 fedora project 兼容部分  ###
#
%%_qt4			%%{qt4_name}
%%_qt4_version		%%{qt4_version}
%%_qt4_prefix		%%{qt4_prefix}
%%_qt4_bindir		%%{qt4_bindir}
%%_qt4_datadir		%%{qt4_prefix}
%%_qt4_demosdir		%%{qt4_prefix}/demos
%%_qt4_docdir		%%{qt4_docdir}
%%_qt4_examples		%%{qt4_prefix}/examples
%%_qt4_headerdir	%%{qt4_includedir}
%%_qt4_libdir		%%{qt4_libdir}
%%_qt4_plugindir	%%{qt4_pluginsdir}
%%_qt4_qmake		%%{qt4_qmake}
%%_qt4_sysconfdir	%%{_sysconfdir}
%%_qt4_translationdir	%%{qt4_prefix}/translations
%%_qt4_importdir	%%{qt4_importdir}
EOF

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files

%files devel
%defattr(-,root,root)
%_qtdir/include/Qt/*.h
%_includedir/Qt
%{_sysconfdir}/rpm/macros.qt4
%_libdir/pkgconfig/Qt.pc

%files doc
%defattr(-,root,root)
%doc %_qtdir/doc

%files -n qmake
%defattr(-,root,root)
%_bindir/qmake*
%_qtdir/bin/qmake
%_qtdir/mkspecs
%exclude %_qtdir/mkspecs/modules/qt_webkit_version.pri 

%files script
%defattr(-,root,root)
%_libdir/libQtScript.so.*
%_qtdir/lib/libQtScript.so.*

%files script-devel
%defattr(-,root,root)
%_libdir/libQtScript.so
%_qtdir/lib/libQtScript.so
%_libdir/libQtScript.prl
%_qtdir/lib/libQtScript.prl
%_includedir/QtScript
%_qtdir/include/QtScript
%_qtdir/include/Qt/QtScript
%_libdir/pkgconfig/QtScript.pc

%files scripttools
%defattr(-,root,root)
%_libdir/libQtScriptTools.so.*
%_qtdir/lib/libQtScriptTools.so.*

%files scripttools-devel
%defattr(-,root,root)
%_libdir/libQtScriptTools.so
%_qtdir/lib/libQtScriptTools.so
%_libdir/libQtScriptTools.prl
%_qtdir/lib/libQtScriptTools.prl
%_includedir/QtScriptTools
%_qtdir/include/QtScriptTools
%_qtdir/include/Qt/QtScriptTools
%_libdir/pkgconfig/QtScriptTools.pc

%files core
%defattr(-,root,root)
%{_sysconfdir}/ld.so.conf.d/*
%{_sysconfdir}/profile.d/qt4.*
%dir %_qtdir
%dir %_qtdir/lib
%_qtdir/lib/libQtCore.so.*
%_libdir/libQtCore.so.*
%dir %_qtdir/plugins
%dir %_qtdir/plugins/codecs
%dir %_qtdir/plugins/imageformats
%dir %_qtdir/plugins/sqldrivers
%if ! %styles_are_gone
%dir %_qtdir/plugins/styles
%endif
%dir %_qtdir/translations
%_qtdir/translations/*

%files core-devel
%defattr(-,root,root)
%_qtdir/lib/libQtCore.so
%_libdir/libQtCore.so
%_qtdir/lib/libQtCore.prl
%_libdir/libQtCore.prl
%dir %_qtdir/include
%_qtdir/include/QtCore
%_includedir/QtCore
%_qtdir/include/Qt/QtCore
%_libdir/pkgconfig/QtCore*.pc
%_bindir/lrelease*
%_bindir/lupdate*
%_bindir/moc*
%_qtdir/bin/lrelease
%_qtdir/bin/lupdate
%_qtdir/bin/moc
%{_bindir}/qmlplugindump*
%_qtdir/bin/qmlplugindump

%files network
%defattr(-,root,root)
%_qtdir/lib/libQtNetwork.so.*
%_libdir/libQtNetwork.so.*

%files network-devel
%defattr(-,root,root)
%_qtdir/lib/libQtNetwork.so
%_libdir/libQtNetwork.so
%_qtdir/lib/libQtNetwork.prl
%_libdir/libQtNetwork.prl
%_qtdir/include/QtNetwork
%_includedir/QtNetwork
%_qtdir/include/Qt/QtNetwork
%_libdir/pkgconfig/QtNetwork*.pc

%files xml
%defattr(-,root,root)
%_qtdir/lib/libQtXml.so.*
%_libdir/libQtXml.so.*

%files xml-devel
%defattr(-,root,root)
%_qtdir/lib/libQtXml.so
%_libdir/libQtXml.so
%_qtdir/lib/libQtXml.prl
%_libdir/libQtXml.prl
%_qtdir/include/QtXml
%_includedir/QtXml
%_qtdir/include/Qt/QtXml
%_libdir/pkgconfig/QtXml.pc

%files declarative
%defattr(-,root,root)
%_bindir/qmlviewer*
%_qtdir/bin/qmlviewer
%_qtdir/lib/libQtDeclarative.so.*
%_libdir/libQtDeclarative.so.*
%_qtdir/plugins/designer/libqdeclarativeview.so
%_qtdir/plugins/qmltooling/libqmldbg_tcp.so
%_qtdir/plugins/qmltooling/libqmldbg_inspector.so

%_qtdir/imports/Qt/labs/folderlistmodel/libqmlfolderlistmodelplugin.so
%_qtdir/imports/Qt/labs/folderlistmodel/qmldir
%_qtdir/imports/Qt/labs/gestures/libqmlgesturesplugin.so
%_qtdir/imports/Qt/labs/gestures/qmldir
%_qtdir/imports/Qt/labs/particles/libqmlparticlesplugin.so
%_qtdir/imports/Qt/labs/particles/qmldir
%_qtdir/imports/Qt/labs/shaders/libqmlshadersplugin.so
%_qtdir/imports/Qt/labs/shaders/qmldir
%_qtdir/plugins/bearer/libqconnmanbearer.so
%_qtdir/plugins/bearer/libqgenericbearer.so
%_qtdir/plugins/bearer/libqnmbearer.so

%files declarative-devel
%defattr(-,root,root)
%_qtdir/lib/libQtDeclarative.so
%_libdir/libQtDeclarative.so
%_qtdir/lib/libQtDeclarative.prl
%_libdir/libQtDeclarative.prl
%_qtdir/include/QtDeclarative
%_includedir/QtDeclarative
%_qtdir/include/Qt/QtDeclarative
%_libdir/pkgconfig/QtDeclarative.pc

%files gui
%defattr(-,root,root)
%_bindir/qttracereplay*
%_qtdir/bin/qttracereplay
%dir %_qtdir/plugins/accessible
%dir %_qtdir/plugins/imageformats
%_qtdir/plugins/accessible/libqtaccessiblewidgets.so
%_qtdir/plugins/graphicssystems/libqtracegraphicssystem.so
%_qtdir/lib/libQtGui.so.*
%_libdir/libQtGui.so.*
%_qtdir/plugins/imageformats/libqtiff.so
%{_datadir}/icons/hicolor/*/apps/qt4-logo.*

%files gui-devel
%defattr(-,root,root)
%_qtdir/lib/libQtGui.so
%_libdir/libQtGui.so
%_qtdir/lib/libQtGui.prl
%_libdir/libQtGui.prl
%_bindir/uic*
%_qtdir/include/QtGui
%_qtdir/include/QtDesigner
%_qtdir/include/QtUiTools
%_qtdir/bin/uic
%_includedir/QtGui
%_includedir/QtDesigner
%_includedir/QtUiTools
%_qtdir/include/Qt/QtGui
%_libdir/pkgconfig/QtGui*.pc
%_libdir/pkgconfig/QtUiTools.pc
%_libdir/pkgconfig/QtDesigner*.pc

%files compat
%defattr(-,root,root)
%_qtdir/lib/libQt3Support.so.*
%_libdir/libQt3Support.so.*
%_qtdir/plugins/accessible/libqtaccessiblecompatwidgets.so
%_qtdir/plugins/designer/libqt3supportwidgets.so

%files compat-devel
%defattr(-,root,root)
%_qtdir/lib/libQt3Support.so
%_libdir/libQt3Support.so
%_qtdir/lib/libQt3Support.prl
%_libdir/libQt3Support.prl
%_qtdir/include/Qt3Support
%_qtdir/q3porting.xml
%_includedir/Qt3Support
%_qtdir/include/Qt/Qt3Support
%_libdir/pkgconfig/Qt3Support*.pc
%_bindir/qt3to*
%_bindir/uic3
%_qtdir/bin/qt3to*
%_qtdir/bin/uic3

%files designer
%defattr(-,root,root)
%_qtdir/lib/libQtDesigner.*
%_qtdir/lib/libQtDesignerComponents.*
%_libdir/libQtDesigner.*
%_libdir/libQtDesignerComponents.*
%_libdir/libQtUiTools.*
%_qtdir/lib/libQtUiTools.*
%_qtdir/bin/designer
%_qtdir/bin/rcc
%_qtdir/plugins/designer/libarthurplugin.so
%_qtdir/plugins/designer/libcontainerextension.so
%_qtdir/plugins/designer/libcustomwidgetplugin.so
%_qtdir/plugins/designer/libtaskmenuextension.so
%_qtdir/plugins/designer/libworldtimeclockplugin.so
%_bindir/designer*
%_bindir/rcc*
%_qtdir/bin/pixeltool
%_bindir/pixeltool*
%{_datadir}/applications/qt4-designer.desktop

%files linguist
%defattr(-,root,root)
%_qtdir/bin/linguist
%_qtdir/bin/lconvert
%dir %_qtdir/phrasebooks
%_qtdir/phrasebooks/*
%_bindir/linguist*
%_bindir/lconvert*
%{_datadir}/applications/qt4-linguist.desktop
%{_datadir}/icons/hicolor/*/apps/linguist4.png

%files opengl
%defattr(-,root,root)
%_qtdir/lib/libQtOpenGL.so.*
%_libdir/libQtOpenGL.so.*
%_qtdir/plugins/graphicssystems/libqglgraphicssystem.so

%files opengl-devel
%defattr(-,root,root)
%_qtdir/lib/libQtOpenGL.so
%_libdir/libQtOpenGL.so
%_qtdir/lib/libQtOpenGL.prl
%_libdir/libQtOpenGL.prl
%_qtdir/include/QtOpenGL
%_includedir/QtOpenGL
%_qtdir/include/Qt/QtOpenGL
%_libdir/pkgconfig/QtOpenGL*.pc

%files qtconfig
%defattr(-,root,root)
%_bindir/qtconfig*
%_qtdir/bin/qtconfig
%{_datadir}/applications/qt4-qtconfig.desktop

%files sql
%defattr(-,root,root)
%_qtdir/lib/libQtSql.so.*
%_libdir/libQtSql.so.*

%files sql-devel
%defattr(-,root,root)
%_qtdir/lib/libQtSql.so
%_libdir/libQtSql.so
%_qtdir/lib/libQtSql.prl
%_libdir/libQtSql.prl
%_qtdir/include/QtSql
%_includedir/QtSql
%_qtdir/include/Qt/QtSql
%_libdir/pkgconfig/QtSql*.pc

%files xmlpatterns
%defattr(-,root,root)
%_bindir/xmlpatterns*
%_qtdir/bin/xmlpatterns*
%_qtdir/lib/libQtXmlPatterns.so.*
%_libdir/libQtXmlPatterns.so.*

%files xmlpatterns-devel
%defattr(-,root,root)
%_qtdir/lib/libQtXmlPatterns.so
%_libdir/libQtXmlPatterns.so
%_qtdir/lib/libQtXmlPatterns.prl
%_libdir/libQtXmlPatterns.prl
%_qtdir/include/QtXmlPatterns
%_includedir/QtXmlPatterns
%_qtdir/include/Qt/QtXmlPatterns
%_libdir/pkgconfig/QtXmlPatterns.pc

%files multimedia
%defattr(-,root,root)
%_qtdir/lib/libQtMultimedia.so.*
%_libdir/libQtMultimedia.so.*

%files multimedia-devel
%defattr(-,root,root)
%_qtdir/lib/libQtMultimedia.so
%_libdir/libQtMultimedia.so
%_qtdir/lib/libQtMultimedia.prl
%_libdir/libQtMultimedia.prl
%_qtdir/include/QtMultimedia
%_includedir/QtMultimedia
%_qtdir/include/Qt/QtMultimedia
%_libdir/pkgconfig/QtMultimedia.pc

%files clucene
%defattr(-,root,root)
%_qtdir/lib/libQtCLucene.so.*
%_libdir/libQtCLucene.so.*

%files clucene-devel
%defattr(-,root,root)
%_qtdir/lib/libQtCLucene.so
%_libdir/libQtCLucene.so
%_qtdir/lib/libQtCLucene.prl
%_libdir/libQtCLucene.prl
%_libdir/pkgconfig/QtCLucene.pc

%files help
%defattr(-,root,root)
%_bindir/qhelp*
%_qtdir/bin/qhelp*
%_qtdir/lib/libQtHelp.so.*
%_libdir/libQtHelp.so.*

%files help-devel
%defattr(-,root,root)
%_qtdir/lib/libQtHelp.so
%_libdir/libQtHelp.so
%_qtdir/lib/libQtHelp.prl
%_libdir/libQtHelp.prl
%_qtdir/include/QtHelp
%_includedir/QtHelp
%_qtdir/include/Qt/QtHelp
%_libdir/pkgconfig/QtHelp.pc

%files test
%defattr(-,root,root)
%_includedir/QtTest
%_libdir/libQtTest.*
%_libdir/pkgconfig/QtTest.pc
%_qtdir/lib/libQtTest.*
%_qtdir/include/QtTest
%_qtdir/include/Qt/QtTest

%files assistant
%defattr(-,root,root)
%_qtdir/bin/assistant*
%_bindir/assistant*
%{_datadir}/applications/qt4-assistant.desktop
# FIXME:
%_bindir/qcollectiongenerator*
%_qtdir/bin/qcollectiongenerator
%_bindir/qdoc3*
%_qtdir/bin/qdoc3*

#%files assistant-devel
#%defattr(-,root,root)
#%_includedir/QtAssistant
#%_libdir/libQtAssistantClient.*
#%_qtdir/include/QtAssistant
#%_qtdir/lib/libQtAssistantClient.*
#%_libdir/pkgconfig/QtAssistantClient.pc

%files inputmethods
%defattr(-,root,root)
%_qtdir/plugins/inputmethods

%files chinese
%defattr(-,root,root)
%_qtdir/plugins/codecs/libqcncodecs.so

%files japanese
%defattr(-,root,root)
%_qtdir/plugins/codecs/libqjpcodecs.so

%files korean
%defattr(-,root,root)
%_qtdir/plugins/codecs/libqkrcodecs.so

%files taiwanese
%defattr(-,root,root)
%_qtdir/plugins/codecs/libqtwcodecs.so

%files cjk

%files jpeg
%defattr(-,root,root)
%_qtdir/plugins/imageformats/libqjpeg.so

%files gif
%defattr(-,root,root)
%_qtdir/plugins/imageformats/libqgif.so

%files tga
%defattr(-,root,root)
%_qtdir/plugins/imageformats/libqtga.so

%files ico
%defattr(-,root,root)
%_qtdir/plugins/imageformats/libqico.so

%files mng
%defattr(-,root,root)
%_qtdir/plugins/imageformats/libqmng.so

%files svg
%defattr(-,root,root)
%_libdir/libQtSvg.so.*
%_qtdir/lib/libQtSvg.so.*
%_qtdir/plugins/imageformats/libqsvg.so
%_qtdir/plugins/iconengines/libqsvgicon.so

%files svg-devel
%defattr(-,root,root)
%_libdir/libQtSvg.so
%_qtdir/lib/libQtSvg.so
%_libdir/libQtSvg.prl
%_qtdir/lib/libQtSvg.prl
%_qtdir/include/QtSvg
%_includedir/QtSvg
%_qtdir/include/Qt/QtSvg
%_libdir/pkgconfig/QtSvg*

%if %with_mysql
%files mysql
%defattr(-,root,root)
%_qtdir/plugins/sqldrivers/libqsqlmysql.so
%endif

%files sqlite
%defattr(-,root,root)
%_qtdir/plugins/sqldrivers/libqsqlite*.so

%if %with_tds
%files tds
%defattr(-,root,root)
%_qtdir/plugins/sqldrivers/libqsqltds.so
%endif

%if %with_odbc
%files odbc
%defattr(-,root,root)
%_qtdir/plugins/sqldrivers/libqsqlodbc.so
%endif

%if %with_postgresql
%files postgresql
%defattr(-,root,root)
%_qtdir/plugins/sqldrivers/libqsqlpsql.so
%endif

%if %with_firebird
%files firebird
%defattr(-,root,root)
%_qtdir/plugins/sqldrivers/libqsqlibase.so
%endif

%files demos
%defattr(-,root,root)
%_qtdir/bin/qtdemo
%_qtdir/demos
%_bindir/qtdemo*
%{_datadir}/applications/qt4-qtdemo.desktop

%files examples
%defattr(-,root,root)
%_qtdir/examples

%if ! %styles_are_gone
%files style-windows
%defattr(-,root,root)
%_qtdir/plugins/styles/libqwindowsstyle.so

%files style-motif
%defattr(-,root,root)
%_qtdir/plugins/styles/libqmotifstyle.so

%files style-cde
%defattr(-,root,root)
%_qtdir/plugins/styles/libqcdestyle.so
%endif

%files dbus
%defattr(-,root,root)
# qdbus4 qdbuscpp2xml-qt4 qdbusviewer4 qdbusxml2cpp4 qdbuscpp2xml4
# qdbus-qt4 qdbusviewer-qt4 qdbusxml2cpp-qt4
%_bindir/qdbus*
%_qtdir/bin/qdbus
#%_bindir/qdbuscpp2xml*
%_qtdir/bin/qdbuscpp2xml
#%_bindir/qdbusxml2cpp*
%_qtdir/bin/qdbusxml2cpp
#%_bindir/qdbusviewer*
%_qtdir/bin/qdbusviewer
%_qtdir/lib/libQtDBus.so.*
%_libdir/libQtDBus.so.*

%_qtdir/plugins/script/libqtscriptdbus.so

%files dbus-devel
%defattr(-,root,root)
%_qtdir/lib/libQtDBus.so
%_libdir/libQtDBus.so
%_qtdir/lib/libQtDBus.prl
%_libdir/libQtDBus.prl
%_qtdir/include/QtDBus
%_libdir/pkgconfig/QtDBus*
%_includedir/QtDBus
%_qtdir/include/Qt/QtDBus

%if %with_phonon && %ship_phonon_pkg
%files phonon
%defattr(-,root,root,-)
%_qtdir/lib/libphonon.so.*
%_libdir/libphonon.so.*
%_qtdir/plugins/designer/libphononwidgets.so
%{_datadir}/dbus-1/interfaces/org.kde.Phonon.AudioOutput.xml

%files phonon-gstreamer
%defattr(-,root,root,-)
%_qtdir/plugins/phonon_backend/libphonon_gstreamer.so
%{_datadir}/kde4/services/phononbackends/gstreamer.desktop

%files phonon-devel
%defattr(-,root,root,-)
%_qtdir/include/phonon/
#%_qtdir/include/Qt/phonon
%_includedir/phonon
%_qtdir/lib/libphonon.so
%_libdir/libphonon.so
%_qtdir/lib/libphonon.prl
%_libdir/libphonon.prl
%_libdir/pkgconfig/phonon.pc
%endif

%if %with_webkit && %ship_webkit_pkg
%files webkit
%defattr(-,root,root,-)
%_qtdir/lib/libQtWebKit.so.*
%_libdir/libQtWebKit.so.*
%_qtdir/plugins/designer/libqwebview.so
%_qtdir/imports/QtWebKit/libqmlwebkitplugin.so
%_qtdir/imports/QtWebKit/qmldir

%files webkit-devel
%defattr(-,root,root,-)
%_qtdir/lib/libQtWebKit.so
%_libdir/libQtWebKit.so
%_qtdir/lib/libQtWebKit.prl
%_libdir/libQtWebKit.prl
%_qtdir/mkspecs/modules/qt_webkit_version.pri 
%_libdir/pkgconfig/QtWebKit.pc
%_includedir/QtWebKit
%_qtdir/include/QtWebKit
%_qtdir/include/Qt/QtWebKit
%_qtdir/tests/*
%endif

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 4.8.7-2
- 为 Magic 3.0 重建

* Thu Sep 10 2015 Liu Di <liudidi@gmail.com> - 4.8.7-1
- 更新到 4.8.7

* Tue Aug 05 2014 Liu Di <liudidi@gmail.com> - 4.8.6-2
- 为 Magic 3.0 重建

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 4.8.6-1.4
- 为 Magic 3.0 重建

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 4.8.6-1.3
- 为 Magic 3.0 重建

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 4.8.6-1.2
- 为 Magic 3.0 重建

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 4.8.6-1.1
- 为 Magic 3.0 重建

* Wed Mar 28 2012 Liu Di <liudidi@gmail.com> - 4.8.0-1.4
- 为 Magic 3.0 重建

* Tue Mar 27 2012 Liu Di <liudidi@gmail.com> - 4.8.0-1.3
- 为 Magic 3.0 重建

* Tue Mar 13 2012 Liu Di <liudidi@gmail.com> - 4.8.0-1.2
- 为 Magic 3.0 重建

* Tue Mar 13 2012 Liu Di <liudidi@gmail.com> - 4.8.0-1.1
- 为 Magic 3.0 重建

* Tue Oct 20 2011 Liu Di <liudidi@gmail.com> - 4.8.0-1
- 更新到 4.8.0
- 添加在新版本 glib 上编译的补丁
- 修正一些文件打包问题

* Wed Oct 13 2010 Ni Hui <shuizhuyuanluo@126.com> 4.7.0-2mgc
- qt webkit 默认编码设为 gb18030(patch 104 written by nihui)
- qt webkit gb2312/gbk 直接认作为 gb18030(patch 105 written by nihui)
- 庚寅  九月初六

* Mon Oct 11 2010 Ni Hui <shuizhuyuanluo@126.com> 4.7.0-1mgc
- 更新至 4.7.0
- core-devel 包添加 qt4.sh 和 qt4.csh
- qt4-qtscript/qt4-qtscripttools/qt4-qtdbus 重命名为 qt4-script/qt4-scripttools/qt4-dbus
- qtabbar 标签中文竖排支持(patch 103 written by nihui)
- 庚寅  九月初四

* Sat Mar 20 2010 Ni Hui <shuizhuyuanluo@126.com> 4.6.2-1mgc
- 更新至 4.6.2
- 庚寅  二月初五

* Thu Dec 3 2009 Ni Hui <shuizhuyuanluo@126.com> 4.6.0-1mgc
- 更新至 4.6.0
- 新设立 multimedia 包
- 未纳入 declarative 模块
- 未纳入 openvg 支持
- qttracereplay 和 libqtracegraphicssystem.so 归入 gui 包
- 乙丑  十月十七

* Fri Oct 2 2009 Ni Hui <shuizhuyuanluo@126.com> 4.5.3-1mgc
- 更新至 4.5.3
- 为何没有翻译文件
- 乙丑  八月十四

* Tue Aug 18 2009 Ni Hui <shuizhuyuanluo@126.com> 4.5.2-3mgc
- 删除其它平台编译器的 qmake 配置
- ldconfig 目录支持
- 乙丑  六月廿八

* Fri Jul 31 2009 Ni Hui <shuizhuyuanluo@126.com> 4.5.2-2mgc
- 更新 qt-copy 补丁
- qt4-webkit 安全补丁 CVE-2009-1725
- 己丑  六月初十

* Fri Jun 26 2009 Ni Hui <shuizhuyuanluo@126.com> 4.5.2-1mgc
- 更新至 4.5.2
- with_tds 开关
- 默认禁用 raster 图形渲染
- 己丑  闰五月初四

* Fri May 29 2009 Ni Hui <shuizhuyuanluo@126.com> 4.5.1-2mgc
- 更新 qt-copy 补丁
- 己丑  五月初六

* Sat Apr 25 2009 Ni Hui <shuizhuyuanluo@126.com> 4.5.1-1mgc
- 更新至 4.5.1
- 更新 qt-copy 补丁
- 启用 FT_LCD_FILTER
- 修复 (i386/x86_64) qatomic 内联汇编，以修复 Kolourpaint 崩溃
- -no-exceptions 编译参数
- 新设立 tds sql 连接插件包
- 己丑  四月初一

* Fri Mar 6 2009 Ni Hui <shuizhuyuanluo@126.com> 4.5.0-1mgc
- 更新至 4.5.0 正式版
- qdoc3 组件(用于生成 Qt 参考文档的工具)，纳入 assistant 包
- 去除 patch 8 和 patch 9
- 己丑  二月初十

* Sat Feb 28 2009 Ni Hui <shuizhuyuanluo@126.com> 4.5.0-0.rc1.5mgc
- qgtkstyle 编译参数开关开启
- qhostaddress.h 头文件修正(patch 50 from fedora project)
- 更新 qt-copy 补丁
- 去除编译时进行 strip 操作，以便留下有用的 debuginfo rpm 包
- 编译参数： -reduce-relocations -no-separate-debug-info -stl
- 不删除 debug 文件
- 对共享库添加 debug 链接
- 添加 qt4 安装路径的 rpm 宏定义(兼容 fedora project)
- ship_phonon_pkg 和 ship_webkit_pkg 开关，phonon 包不予提供(FIXME: use external phonon module)
- 己丑  二月初四

* Thu Feb 12 2009 Ni Hui <shuizhuyuanluo@126.com> 4.5.0-0.rc1.4mgc
- spec 开关修正
- 己丑  正月十八

* Sun Feb 8 2009 Ni Hui <shuizhuyuanluo@126.com> 4.5.0-0.rc1.3mgc
- 新设立 qt-qtconfig 包，避免 qt-gui 库包依赖其它包
- %_qtdir/plugins/graphicssystems/libqglgraphicssystem.so 从 gui 移入 opengl 包
- 己丑  正月十四

* Sun Feb 8 2009 Ni Hui <shuizhuyuanluo@126.com> 4.5.0-0.rc1.2mgc
- patch 10255
- 优先使用 native 渲染图形(patch 102 imported)
- -xinput 编译参数
- 己丑  正月十四

* Fri Feb 6 2009 Ni Hui <shuizhuyuanluo@126.com> 4.5.0-0.rc1.1mgc
- 更新至 4.5.0-rc1
- 恢复 Qt 窗体控件样式编译
- 纳入 phonon/gstreamer 支持(独立于 KDE 4.x phonon)
- FIXME: qt4-phonon 开发包与 phonon 开发包冲突
- 新设立 qtscripttools 包(qtscript 附加工具和调试器)、phonon-gstreamer 包
- lconvert 翻译辅助程序纳入 linguist 包
- %_qtdir/plugins/imageformats/libqsvg.so 从 gui 包移入 svg 包
- %_qtdir/plugins/graphicssystems/libqglgraphicssystem.so 纳入 gui 包(new in Qt 4.5，opengl 图形渲染)
- 许可证添加 LGPL
- 更新 qt4 中文字体伪粗体补丁
- 弃用 qt-4.4.x 补丁
- 己丑  正月十二

* Sat Jan 31 2009 Ni Hui <shuizhuyuanluo@126.com> 4.4.3-0.4mgc
- 更新 qt-copy 补丁
- 己丑  正月初六

* Mon Jan 12 2009 Ni Hui <shuizhuyuanluo@126.com> 4.4.3-0.3mgc
- 更新 qt-copy 补丁，调整(patch 10259 未使用)
- 添加一个输入法光标跟随补丁(replace patch 1008)
- mysql/postgresql/odbc 数据库插件编译支持开关
- 戊子  十二月十七

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> 4.4.3-0.2mgc
- opensuse patches
- 戊子  九月初一

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> 4.4.3-0.1mgc
- 更新至 4.4.3 正式版
- 菜单项中文化
- 戊子  九月初一

* Sun Sep 28 2008 Ni Hui <shuizhuyuanluo@126.com> 4.4.2-0.1mgc
- 更新至 4.4.2 正式版
- 禁用 systray 修正补丁(fixed by upstream)
- 更新 qt-copy 补丁
- 戊子  八月廿九

* Thu Aug 28 2008 Ni Hui <shuizhuyuanluo@126.com> 4.4.1-0.1mgc
- 更新至 4.4.2-20080827 快照(4.4.1 正式版发布时没有来得及加入中文翻译，参见 http://feeds.feedburner.com/~r/cavendish/~3/351445241/qt-441.html)
- 纳入 odbc 数据库插件支持
- 更新 qt-copy 补丁，禁用一些上游已应用的补丁
- 将 %_includedir/Qt 符号链接文件加入 qt4-devel 包中(FIXME!)
- 戊子  七月廿八

* Thu May 29 2008 Ni Hui <shuizhuyuanluo@126.com> 4.4.0-1.2mgc
- 添加 qt-copy 补丁
- 纳入 mysql 数据库插件支持
- qt4-core-devel 中的 phrasebooks 文档移入 linguist 包避免重复
- 添加参数 -optimized-qmake
- 重新引入中文伪粗体补丁
- 戊子  四月廿五

* Fri May 09 2008 Ni Hui <shuizhuyuanluo@126.com> 4.4.0-1.1mgc
- 更新至 4.4.0 正式版
- 添加 qt4-demos 对 qt4-doc 的依赖关系(否则演示程序的描述文字不可用)
- 使用 pushd/popd 替换 spec 中的“cd”，规范化安装流程
- 修正 linguist 的菜单项图标
- qt4-core 中的 phrasebooks 文档移入 qt4-core-devel
- 将 qt4-devel 包中的非头文件分类至子包中，%_qtdir/include/Qt 文件夹仅保留 *.h 文件
- 删除无用的 %_qtdir/lib/*.la 编译残留文件
- %_qtdir/lib/*.{so,prl} 文件移入各自的 devel 包，assistant/designer/test 相关文件不移动
- 戊子  四月初五

* Mon Apr 07 2008 Ni Hui <shuizhuyuanluo@126.com> 4.4.0-0.rc1.1mgc
- 修正 release 版本号为 0.rc1.1mgc
- 从 qt4-devel 中拆出 doc 包
- 戊子  三月初二

* Sat Apr 05 2008 Ni Hui <shuizhuyuanluo@126.com> 4.4.0-0.1.rc1mgc
- 更新至 4.4.0-rc1
- FIXME: lib/*.{so,prl} 文件应该纳入 devel 包，而 lib/*.la 应该去除
- FIXME: %_bindir/qcollectiongenerator-qt4，%_bindir/qcollectiongenerator4，%_qtdir/bin/qcollectiongenerator 暂时纳入 assisitant 中，以后考虑独立分包
- -reduce-relocations, -dbus-linked, -openssl-linked
- -no-nas
- -no-phonon (-no-gstreamer), -no-webkit (for now, at least until conflicts with WebKit-qt and kdelibs4 are sorted out)
- nihui 注：KDE 4.0.x 提供 phonon 4.0，Qt 4.4.x 提供 phonon 4.1，KDE 4.1.x 提供 phonon 4.2
- 未纳入 gstreamer 支持
- 未纳入 phonon 支持
- -no-exceptions 以用于编译 QtXmlPatterns
- 去掉了所有补丁 ;)
- docdir/qch/ 新增，放入 qt4-devel
- docdir/src/ 新增，放入 qt4-devel
- lib/pkgconfig/QtDesigner.pc 新增，放入 qt4-gui-devel
- lib/pkgconfig/QtDesignerComponents.pc 新增，放入 qt4-gui-devel
- 新设立 webkit、webkit-devel、phonon、phonon-devel 包
- 新设立 help、help-devel、clucene、clucene-devel 包
- 新设立 ico 包
- 新设立 xmlpatterns、xmlpatterns-devel 包
- 戊子  二月廿九

* Thu Apr 03 2008 Ni Hui <shuizhuyuanluo@126.com> 4.3.4-1.1mgc
- 添加 fedora patches 4 5 6
- 修正 qt4 对于 openssl 库的支持
- 戊子  二月廿七

* Thu Mar 06 2008 haulm <haulm@126.com> 4.3.4-1mgc
- Add build postgresql-plugin

* Wed Mar 01 2008 Ni Hui <shuizhuyuanluo@126.com> 4.3.4-0.1mgc
- 更新至 4.3.4
- 添加依赖：qt4-devel -> qmake & qt4-{svg,qtscript,qtdbus}-devel
- 添加依赖：qt4 -> qt4-{svg,mng,qtscript,qtdbus}
- 添加分包 qt4-cjk 依赖 qt4-{chinese,japanese,korean,taiwanese,inputmethods}
- 戊子  正月廿四

* Wed Feb 06 2008 Ni Hui <shuizhuyuanluo@126.com> 4.3.3-1.3mgc
- 添加菜单项和部分 logo 图标
- rebuild against MagicLinux-2.1beta1

* Tue Jan 08 2008 Ni Hui <shuizhuyuanluo@126.com> 4.3.3-1.1mgc
- 启用 dbus 支持(用于 KDE4 编译)

* Fri Dec 28 2007 KanKer <kanker@163.com> 4.3.3-1mgc
- build for MagicLinux
- Add Designer.conf
- Add resume_rpmbuild define to resume build rpm process
- Add two font patches from cjacker

*  Wed Oct 8 2006 haulm <haulm@126.com> 4.2.0-1mgc
- First build for MagicLinux
