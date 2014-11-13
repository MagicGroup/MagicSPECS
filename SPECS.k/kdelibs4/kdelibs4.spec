#不知道为什么没有debugs信息，有时候又行
# define  debug_package %{nil}

%define release_number 1
%define real_name kdelibs
%define apidocs 1
%define udisks2 1

Name: kdelibs4
Summary: KDE Base Libraries
Summary(zh_CN.UTF-8): KDE 基本库
License: LGPL v2 or later
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
URL: http://www.kde.org/
Version: 4.14.2
Release: 1%{?dist}
%define rversion %version
Source0: http://download.kde.org/stable/%{rversion}/src/%{real_name}-%{rversion}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: kde4-macros(api) >= 2
BuildRequires: kde4-filesystem >= 4-23

BuildRequires: qt4-declarative-devel
BuildRequires: qt4-test
BuildRequires: libacl-devel
BuildRequires: flex
BuildRequires: aspell-devel
BuildRequires: cups-devel
BuildRequires: giflib-devel
BuildRequires: hicolor-icon-theme
BuildRequires: libattr-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: libxslt-devel
BuildRequires: unzip
BuildRequires: pcre-devel
BuildRequires: bison-devel
BuildRequires: desktop-file-utils
BuildRequires: shared-mime-info >= 0.20
BuildRequires: gamin-devel
BuildRequires: gettext-devel
BuildRequires: docbook-style-xsl
BuildRequires: qtwebkit-devel
#BuildRequires: alsa-driver-devel
BuildRequires: libXcomposite-devel libXdamage-devel libxkbfile-devel
BuildRequires: libXpm-devel libXScrnSaver-devel libXtst-devel libXv-devel libXxf86misc-devel
BuildRequires: openssh-clients
BuildRequires: openssl-devel
BuildRequires: automoc4 >= 0.9.87
BuildRequires: phonon-devel >= 4.3.1
# cmake-2.6.2
BuildRequires: cmake >= 2.6.2
BuildRequires: qt4-devel >= 4.6.0
# strigi/soprano/nepomuk
BuildRequires: strigi-devel >= 0.6.4
# 纳入支持    by nihui Nov 24th, 2007
# 语义学桌面支持
BuildRequires: soprano-devel >= 2.4.60
# 纳入支持    by nihui Dec 12th, 2007
# 希伯来语拼写检查
BuildRequires: hspell-devel
# 其它拼写检查后端
BuildRequires: enchant-devel
# 纳入支持    by nihui Dec 21st, 2007
# avahi 网络探测支持
BuildRequires: avahi-devel
# jpeg-2000 标准支持
BuildRequires: jasper-devel
# lzma 压缩支持
BuildRequires: xz-devel
# openexr 图像支持
BuildRequires: ilmbase-devel
BuildRequires: openexr-devel

# 可选的支持
BuildRequires: herqq-devel
BuildRequires: qca2-devel
BuildRequires: grantlee-devel

# udev 支持
BuildRequires: libudev-devel

BuildRequires: udisks2

BuildRequires: attica-devel
BuildRequires: shared-desktop-ontologies-devel
BuildRequires: polkit-qt-1-devel >= 0.103

BuildRequires: libdbusmenu-qt-devel

%if %apidocs
BuildRequires: docbook-dtds
BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: qt4-doc
%endif

BuildRequires: media-player-info

Requires: qt4 >= 4.6.0
Requires: libkdelibs4 = %{version}
Requires: dbus-x11
Requires: shared-mime-info >= 0.23
Requires: magic-kde4-config >= 4.10.3

Provides: kross(javascript) = %{version}-%{release}
Provides: kross(qtscript) = %{version}-%{release}

Obsoletes: kdelibs4-experimental
Obsoletes: kde4-webkitkde

# 基本补丁，Patch1-50
# install all .css files and Doxyfile.global in kdelibs-common to build
# kdepimlibs-apidocs against
Patch8: kdelibs-4.3.90-install_all_css.patch
# add Fedora/V-R to KHTML UA string
Patch9: kdelibs-4.10.0-branding.patch
# patch KStandardDirs to use %{_libexecdir}/kde4 instead of %{_libdir}/kde4/libexec
Patch10: kdelibs-4.9.97-libexecdir.patch
# kstandarddirs changes: search /etc/kde, find %{_kde4_libexecdir}
Patch11: kdelibs-4.11.97-kstandarddirs.patch
# set build type
Patch12: kdelibs-4.10.0-cmake.patch
# die rpath die, since we're using standard paths, we can avoid
# this extra hassle (even though cmake is *supposed* to not add standard
# paths (like /usr/lib64) already! With this, we can drop
# -DCMAKE_SKIP_RPATH:BOOL=ON (finally)
Patch13: kdelibs-4.10.0-no_rpath.patch


# 必须放前面的补丁，Patch51-80
## upstreamable
# knewstuff2 variant of:
# https://git.reviewboard.kde.org/r/102439/
Patch50: kdelibs-4.7.0-knewstuff2_gpg2.patch
# Toggle solid upnp support at runtime via env var SOLID_UPNP=1 (disabled by default)
Patch52: kdelibs-4.10.0-SOLID_UPNP.patch
# add s390/s390x support in kjs
Patch53: kdelibs-4.7.2-kjs-s390.patch
# return valid locale (RFC 1766)
Patch54: kdelibs-4.8.4-kjs-locale.patch
# patch FindSamba.cmake to find samba4 libs (using pkg-config hints)
# https://git.reviewboard.kde.org/r/106861/
Patch55: FindSamba.cmake-help-find-samba4-more-reliably.patch
# make filter working, TODO: upstream?  -- rex
Patch59: kdelibs-4.9.3-kcm_ssl.patch
# disable dot to reduce apidoc size
Patch61: kdelibs-4.9.3-dot.patch

# 上游补丁，Patch81-150
## upstream
# revert these commits for
#https://bugs.kde.org/315578
# for now, causes regression,
#https://bugs.kde.org/317138
Patch090: return-not-break.-copy-paste-error.patch
Patch091: coding-style-fixes.patch
Patch092: return-application-icons-properly.patch
# workaround "Crash in DialogShadows::Private::freeX11Pixmaps()"

#magic特定的补丁，一般是针对中国用户的
# Patch1000-2000
# qiliang 的 kde4 农历支持
Patch1000: kdelibs-4.6.95-kcalendar-revision-10.patch
# 修正 konqueror/dolphin-part 书签乱码问题
# patch 1101 written by nihui, Jun.19th, 2008
Patch1101: kdelibs-4.0.83-use_gb18030_bookmark_xml.patch
# 回滚字符集为本地编码而不是 iso-8859-1
# patch1102/1103/1104 ported to KDE4 by nihui, Jan.17th, 2009
Patch1102: kdelibs-4.10.3-kcharsets_fallback_to_locale.patch
# 下划线位置下移像素
Patch1103: kdelibs-4.10.3-khtml_draw_underline.patch
# 默认远程编码回滚到本地编码
Patch1104: kdelibs-4.1.96-kremoteencoding_fallback_to_locale.patch
# KDE 程序帮助菜单链接支持
# patch 1105/1106 written by nihui. Jun.5th, 2009
Patch1105: kdelibs-4.10.3-chinese_community_online_support_integration.diff
# KDE 全局关于对话框 magic linux 信息
Patch1106: kdelibs-4.3.90-magiclinux-about.patch
# 更改默认配色，这个不一定合适，再调整
Patch1107: kdelibs-4.10.3-default-magic-colors.patch
# k3procio 默认使用本地编码，而非 ISO-8859-1
# patch 1108 written by nihui, Sep.13rd, 2009
Patch1108: kdelibs-4.3.1-k3procio_local_encoding.patch
# 更改默认字体大小
Patch1109: kdelibs-4.4.2-increase-default-fontsize.patch
# kmultitabbar 中文标签竖排支持
# patch 114 written by nihui, Aug.21st, 2010
Patch1110: kdelibs-4.5.0-kmultitabbar-vertical_cjk_label.patch

%description
This package contains the basic packages of the K Desktop Environment.
It contains the necessary libraries for the KDE desktop.

This package is absolutely necessary for using graphical KDE
applications.

%description -l zh_CN.UTF-8
K 桌面环境 4 的库。
本软件包是图形 KDE 程序所需的。

kdelibs 涵盖了大量 KDE 核心实现的库封装、二进制程序、数据文件等，在这个包内
几乎没有没有直接面向桌面的程序。虽然仅有 kdelibs 的 KDE 桌面还不能呈现一个
成形的运作，但已经可以支撑起一个普通 KDE 程序的运行环境，kdelibs 是整
个 KDE 环境的支柱，关系方方面面。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package -n libkdelibs4-devel
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: KDE Core Libraries: Build Environment
Summary(zh_CN.UTF-8): KDE 核心库：构建环境
Requires: libkdelibs4 = %{version}
Requires: kdelibs4 = %{version}
Requires: cmake >= 2.6.2
Requires: qt4-devel >= 4.6.0
Requires: openssl-devel
Requires: bzip2-devel gamin-devel
Requires: strigi-devel >= 0.6.4
Requires: automoc4 >= 0.9.87

Provides: kdelibs4-devel = %{version}-%{release}
Provides: plasma-devel = %{version}-%{release}

%description -n libkdelibs4-devel
This package contains all necessary include files and libraries needed
to develop non-graphical KDE applications.

%description -n libkdelibs4-devel -l zh_CN.UTF-8
K 桌面环境 4 的库。
本软件包包含所有用于开发的头文件和库。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package -n libkdelibs4
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: KDE Base Libraries
Summary(zh_CN.UTF-8): KDE 核心库
Requires: qt4 >= 4.6.0
Requires: dbus-x11
Requires: shared-mime-info >= 0.23
Requires: phonon >= 4.3.1
%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }
Requires: magic-kde4-config

Provides: kdelibs4-libs = %{version}-%{release}
Provides: kdelibs4-common = %{version}-%{release}
Provides: plasma = %{version}-%{release}

%description -n libkdelibs4
This package contains the basic packages of the K Desktop Environment.
It contains the necessary libraries for the KDE desktop.

This package is absolutely necessary for using graphical KDE
applications.

%description -n libkdelibs4 -l zh_CN.UTF-8
K 桌面环境 4 的库。
本软件包是图形 KDE 程序所需的。

kdelibs 涵盖了大量 KDE 核心实现的库封装、二进制程序、数据文件等，在这个包内
几乎没有没有直接面向桌面的程序。虽然仅有 kdelibs 的 KDE 桌面还不能呈现一个
成形的运作，但已经可以支撑起一个普通 KDE 程序的运行环境，kdelibs 是整
个 KDE 环境的支柱，关系方方面面。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package apidocs
Group: Development/Documentation
Group(zh_CN.UTF-8): 开发/文档
Summary: KDE 4 API documentation
Summary(zh_CN.UTF-8): KDE 4 API 文档

%description apidocs
This package includes the KDE 4 API documentation in HTML
format for easy browsing.

%description apidocs -l zh_CN.UTF-8
本软件包包含 HTML 格式的 KDE 4 API 文档。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

%prep
%setup -q -n %{real_name}-%{rversion}

%patch8 -p1 -b .install_all_css
%patch9 -p1
# add release version as part of branding (suggested by cailon)
sed -i -e "s|@@VERSION_RELEASE@@|%{version}-%{release}|" kio/kio/kprotocolmanager.cpp
#%patch10 -p1 
%patch11 -p1
%patch12 -p1
%patch13 -p1


# upstreamable patches
#%patch4 -p1 -b .alsa-default
%patch50 -p1 -b .knewstuff2_gpg2
%patch52 -p1 -b .SOLID_UPNP
%patch53 -p1 -b .kjs-s390
%patch54 -p1 -b .kjs-locale
#%patch55 -p1 -b .FindSamba-samba4
%patch59 -p1 -b .filter
%patch61 -p1 -b .dot

# upstream patches
%patch090 -p1 -R -b .return-not-break.-copy-paste-error
%patch091 -p1 -R -b .coding-style-fixes.patch
%patch092 -p1 -R -b .return-application-icons-properly

#magic 的补丁
#农历支持
%patch1000 -p1
%patch1101 -p0
%patch1102 -p1
%patch1103 -p1
%patch1104 -p1
%patch1105 -p1
%patch1106 -p0
%patch1107 -p1
%patch1108 -p1
%patch1109 -p1
%patch1110 -p1

%build

export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$CFLAGS"
mkdir build
pushd build
%cmake_kde4   -DKAUTH_BACKEND:STRING="PolkitQt-1" \
	       -DKDE_DISTRIBUTION_TEXT="%{version}-%{release} Magic Linux" \
	       -DWITH_SOLID_UDISKS2:BOOL=ON \
	       -DHUPNP_ENABLED:BOOL=ON \
	       -DHUPNP_INCLUDE_DIR=%{_qt4_headerdir} \
	       -DHUPNP_LIBS=%{_qt4_libdir}/libHUpnp.so \
  	      ..

make %{?_smp_mflags}
popd

%if 0%{?apidocs}
export QTDOCDIR="%{?_qt4_docdir}%{?!_qt4_docdir:%(pkg-config --variable=docdir Qt)}"
%if 0%{?apidocs_qch}
export PROJECT_NAME="%{name}"
export PROJECT_VERSION="%{version}%{?alphatag}"
doc/api/doxygen.sh --qhppages .
%else
doc/api/doxygen.sh .
%endif
%endif

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# 不进行菜单处理
#mkdir -p $RPM_BUILD_ROOT/etc/xdg/menus/applications-merged
#mv %{buildroot}%{_sysconfdir}/xdg/menus/applications.menu \
#   %{buildroot}%{_sysconfdir}/xdg/menus/kde4-applications.menu

# install apidocs and generator script
install -p -D ../doc/api/doxygen.sh %{buildroot}%{kde4_bindir}/kde4-doxygen.sh
%if %apidocs
mkdir -p %{buildroot}%{kde4_htmldir}/en
cp -a ../kdelibs-%{version}-apidocs %{buildroot}%{kde4_htmldir}/en/kdelibs4-apidocs
find   %{buildroot}%{kde4_htmldir}/en/ -name 'installdox' -exec rm -fv {} ';'
rm -vf %{buildroot}%{kde4_htmldir}/en/kdelibs4-apidocs/*.tmp
rm -vf %{buildroot}%{kde4_htmldir}/en/kdelibs4-apidocs/index.qhp
rm -vf %{buildroot}%{kde4_htmldir}/en/kdelibs4-apidocs/*/html/index.qhp
%endif


# clean ksgmltools2 customization files
for lang in af bg ca cs da de el en-GB eo es et fi fo fr gl he hu \
            id it ja ko lt nds nl nn no pl pt pt-BR ro ru sk sl sr \
            sr@ijekavian sr@ijekavianlatin sr@latin sv th tr uk wa xh xx
do
    rm -rfv %{buildroot}%{kde4_appsdir}/ksgmltools2/customization/$lang
done
for lang in ca cs da de el en es et fi fr hu it ja ko nds nl nn no \
            pl pt pt_br ro ru sk sl sr sr@ijekavian sr@ijekavianlatin sr@latin sv
do
    rm -fv %{buildroot}%{kde4_appsdir}/ksgmltools2/customization/xsl/$lang.xml
done

# clean .desktop files
%clean_kde4_desktop_files
%clean_kde4_notifyrc_files

# adapt to wav format and magic sound theme
find %{buildroot}%{kde4_appsdir} -regex ".*\.notifyrc$" | LC_ALL=zh_CN.UTF-8 xargs \
    sed -i -e 's/^Sound=\(.*\)\.ogg$/Sound=\1\.wav/g' \
           -e 's/KDE-Sys-App-Error.wav/MGC-Sys-App-Error.wav/g' \
           -e 's/KDE-Sys-App-Error-Serious.wav/MGC-Sys-App-Error-Serious.wav/g' \
           -e 's/KDE-Sys-App-Message.wav/MGC-Sys-App-Message.wav/g' \
           -e 's/KDE-Sys-Log-In-Short.wav/MGC-Sys-Log-In-Short.wav/g' \
           -e 's/KDE-Sys-Log-Out.wav/MGC-Sys-Log-Out.wav/g' \
           -e 's/KDE-Sys-Question.wav/MGC-Sys-Question.wav/g' \
           -e 's/KDE-Sys-Trash-Emptied.wav/MGC-Sys-Trash-Emptied.wav/g' \
           -e 's/KDE-Sys-Warning.wav/MGC-Sys-Warning.wav/g'

# Strip ELF binaries
for f in `find "$RPM_BUILD_ROOT" -type f \( -perm -0100 -or -perm -0010 -or -perm -0001 \) -exec file {} \; | \
        grep -v "^${RPM_BUILD_ROOT}/\?usr/lib/debug"  | \
        grep -v ' shared object,' | \
        sed -n -e 's/^\(.*\):[  ]*ELF.*, not stripped/\1/p'`; do
	echo "$f"
        /usr/bin/strip -g -v "$f" || :
done
for f in `find "$RPM_BUILD_ROOT" -type f -a -exec file {} \; | \
        grep -v "^${RPM_BUILD_ROOT}/\?usr/lib/debug"  | \
        grep ' shared object,' | \
        sed -n -e 's/^\(.*\):[  ]*ELF.*, not stripped/\1/p'`; do
	echo "$f" 
        /usr/bin/strip -v --strip-unneeded "$f"
done


#不可以用这个，也不需要，仅为了保持兼容性
#magic_rpm_clean.sh

#%check
#cd build
#make test || :

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n libkdelibs4 -p /sbin/ldconfig
%postun -n libkdelibs4 -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -n libkdelibs4-devel
%defattr(-,root,root)
%doc KDE4PORTING.html
%{kde4_bindir}/kconfig_compiler
%{kde4_bindir}/makekdewidgets
%{kde4_bindir}/kde4-doxygen.sh
%{kde4_includedir}/*
%{kde4_appsdir}/cmake
%{kde4_appsdir}/kdewidgets
%{kde4_libdir}/*.so
%{kde4_libdir}/cmake/KDeclarative/*.cmake
%exclude %{kde4_libdir}/libkdeinit4_*.so
%{_libdir}/kde4/plugins/designer/kdewidgets.so
%{_libdir}/kde4/plugins/designer/kde3supportwidgets.so
%{kde4_mandir}/man1/makekdewidgets.1*

%files -n libkdelibs4
%defattr(-,root,root)
%{kde4_libdir}/*.so.*
%{kde4_localedir}/all_languages
%config %{kde4_configdir}/kdebug.areas
%config %{kde4_configdir}/kdebugrc
%dir %{kde4_configdir}/ui
%{kde4_configdir}/ui/ui_standards.rc
%{kde4_appsdir}/kdeui
%{kde4_htmldir}/en/common/*

%files
%defattr(-,root,root)
%doc COPYING COPYING.DOC COPYING.LIB README
%{kde4_bindir}/*
%{_sysconfdir}/xdg/menus/*
%{kde4_libdir}/kde4
%{kde4_libdir}/libkdeinit4_*.so
%{kde4_appsdir}/*
%config %{kde4_configdir}/*
%{kde4_dbus_interfacesdir}/*
%doc %lang(en) %{kde4_htmldir}/en/sonnet
%doc %lang(en) %{kde4_htmldir}/en/kioslave
%{kde4_localedir}/*
%{kde4_servicesdir}/*
%{kde4_servicetypesdir}/*
%{kde4_datadir}/mime/packages/kde.xml
%{kde4_iconsdir}/hicolor/*/actions/*
#%{kde4_iconsdir}/hicolor/*/apps/*
%{kde4_mandir}/man*/*

%{kde4_sysconfdir}/dbus-1/system.d/org.kde.auth.conf

%{kde4_datadir}/applications/kde4/kmailservice.desktop
%{kde4_datadir}/applications/kde4/ktelnetservice.desktop

%exclude %{kde4_bindir}/kconfig_compiler
%exclude %{kde4_appsdir}/cmake
%exclude %{kde4_configdir}/kdebug.areas
%exclude %{kde4_configdir}/kdebugrc
%exclude %{kde4_localedir}/all_languages
%exclude %{kde4_configdir}/ui/ui_standards.rc
%exclude %{kde4_appsdir}/kdeui
%exclude %{kde4_bindir}/makekdewidgets
%exclude %{kde4_appsdir}/kdewidgets
%exclude %{kde4_mandir}/man1/makekdewidgets.1*
%exclude %{kde4_bindir}/kde4-doxygen.sh

%if %apidocs
%files apidocs
%defattr(-,root,root,-)
%{kde4_htmldir}/en/kdelibs4-apidocs
%endif


%changelog
* Tue Oct 21 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Thu May 22 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-1.1
- 为 Magic 3.0 重建

* Mon May 27 2013 Liu Di <liudidi@gmail.com> - 4.10.3-1
- 对 spec 做了调整，将 rpm 配置部分单独成 kde4-rpm-config

* Tue Oct 02 2012 Liu Di <liudidi@gmail.com> - 4.9.1-1
- 升级到 4.9.1
- 改变安装路径为 /usr
- 不再支持 kde3

* Sun Apr 01 2012 Liu Di <liudidi@gmail.com> - 4.8.1-1.1
- 为 Magic 3.0 重建

* Sun Dec 27 2009 Ni Hui <shuizhuyuanluo@126.com> -4.3.4-2mgc
- release 编译模式
- enable final 编译模式
- 乙丑  十一月十二

* Sat Dec 5 2009 Ni Hui <shuizhuyuanluo@126.com> -4.3.4-1mgc
- 更新至 4.3.4
- 乙丑  十月十九

* Sun Sep 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.1-2mgc
- k3procio 默认使用本地编码
- 恢复 patch 999(4.4 trunk)
- 己丑  七月廿五

* Tue Sep 08 2009 Liu Di <liudidi@gmail.com> - 4.3.1-1
- 升级到 4.3.1
- 己丑  七月二十

* Thu Aug 20 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-3mgc
- 添加 kde4.csh 和 kde4.sh
- 己丑  七月初一

* Tue Aug 18 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-2mgc
- gb2312/gbk 映射到 gb18030 编码
- 一些上游 bug 修正
- 己丑  六月廿八

* Thu Jul 30 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0(KDE 4.3 try2)
- 更改默认配色(patch 110)
- kio network access API，用于 webkit 引擎编译
- 己丑  六月初九

* Fri Jul 10 2009 Liu Di <liudidi@gmail.com> - 4.2.96-1
- 更新到 4.2.96

* Sat Jun 27 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- 更新至 4.2.95(KDE 4.3 RC1)
- 己丑  闰五月初五

* Fri Jun 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.90-1mgc
- 更新至 4.2.90(KDE 4.3 Beta2)
- 修正 khtml 渲染大型表单(patch 107 imported from mandriva project)
- KDE 程序帮助菜单链接支持(patch 108 written by nihui)
- KDE 全局关于对话框 magic linux 信息(patch 109 written by nihui)
- 己丑  五月十三  [芒种]

* Fri May 29 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.88-1mgc
- 更新至 4.2.88
- 当系统编码不是 UTF-8 时默认回滚为 GB18030，而非 ISO-8859-1(patch 106 written by nihui)
- 己丑  五月初六

* Sat May 16 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.85-1mgc
- 更新至 4.2.85(KDE 4.3 Beta1)
- 己丑  四月廿二

* Fri May 1 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.3-1mgc
- 更新至 4.2.3
- 己丑  四月初七

* Fri Apr 3 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- 发行版名称信息改为 "Magic Linux 2.4+"
- 禁用 patch 102(seem to be fixed by upstream)
- 禁用 patch 104(need review...)
- 己丑  三月初八

* Fri Mar 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.3mgc
- apply patch to fix issue in CSS style that causes konqueror shows a blank page(patch 10000 imported from fedora project)
- apply patch to fix encoding for Qt-4.5.0(patch 10001 imported from fedora project)
- 己丑  二月十七

* Sat Mar 7 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.2mgc
- 宏定义默认关闭 KDE 测试程序编译选项
- 己丑  二月十一

* Sun Mar 1 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.1mgc
- 更新至 4.2.1
- rpm 宏定义
- 启用 64 位编译参数
- 己丑  二月初五

* Tue Feb 17 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.6mgc
- 使用 Qt 4.5-rc1 编译
- kded/kdirwatch patch (kde#182472)
- Fix duplicated applications in the K menu and in keditfiletype
- make plasma working better with qt-4.5
- 优化文件分包，libkdelibs4 将提供 KDE4 程序最小运行时环境
- 己丑  正月廿三

* Sat Jan 31 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.5mgc
- 上游补丁(patch 1010/1011/1012/1013)
- Emit the correct FilesRemoved signal if the job was aborted in the middle of its operation,
  otherwise it can result in confusion and data loss (overwriting files with files
  that don't exist). kdebug:118593
- Fix "klauncher hangs when kdeinit4 dies" -- this happened because
  klauncher was doing a blocking read forever.
- Repair klauncher support for unique-applications like konsole.
  kdebug:162729, kdebug:75492
- kded/kdirwatch patch (kde#182472)
- 己丑  正月初六

* Tue Jan 27 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.4mgc
- plasma on screensaver 安全问题修正源码包更新(KDE 4.2 final)
- 己丑  正月初二

* Sat Jan 24 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.3mgc
- kate vi mode 按键 fix 源码包更新(KDE 4.2 try3)
- 戊子  十二月廿九

* Fri Jan 23 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.2mgc
- rebuild against soprano 2.1.67
- klockfile fix 源码包更新(KDE 4.2 try2)
- 戊子  十二月廿八

* Thu Jan 22 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.1mgc
- 更新至 4.2.0(KDE 4.2 try1)
- 戊子  十二月廿七

* Sat Jan 17 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.1.96-0.2mgc
- 允许墙纸主题中的符号链接(patch 1001 from fedora project/upstream)
- 回滚字符集为本地编码而不是 iso-8859-1(patch 102 ported to KDE4 by nihui)
- 下划线位置下移像素(patch 103 ported to KDE4 by nihui)
- 默认远程编码回滚到本地编码(patch 104 ported to KDE4 by nihui)
- 戊子  十二月廿二

* Tue Jan 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.1.96-0.1mgc
- 更新至 4.1.96(KDE 4.2 RC1)
- relwithdeb 编译模式
- 戊子  十二月十八

* Fri Dec 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.85-0.1mgc
- 更新至 4.1.85(KDE 4.2 Beta2)
- 戊子  十一月十五

* Sat Nov 22 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.80-0.1mgc
- 更新至 4.1.80
- 戊子  十月廿五  [小雪]

* Sun Oct 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.69-0.1mgc
- 更新至 4.1.69
- debugfull 编译模式
- 戊子  九月十四

* Fri Oct 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.2mgc
- 上游补丁，修正 kded4 启动时崩溃的 bug   :>
- 戊子  九月十二

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.1mgc
- 更新至 4.1.2
- kross 版本升级为 11(patch 201 from debian project)
- 更改 qt4 设计师插件安装路径(patch 213 from debian project)
- display 键盘键支持(patch 501 from opensuse project)
- kde3 程序热插拔支持(patch 502 from opensuse project)
- 戊子  九月初一

* Sun Sep 14 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.2mgc
- 上游补丁(patch 200-204)
- 戊子  八月十五

* Fri Aug 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.1mgc
- 更新至 4.1.1-try1(内部版本)
- 戊子  七月廿九

* Thu Jul 24 2008 Liu Di <liudidi@gmail.com> - 4.1.0-0.1mgc
- 更新到 4.1.0(KDE 4.1 正式版)

* Thu Jul 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.98-0.1mgc
- 更新至 4.0.98(KDE 4.1 RC1)
- 禁用 patch 15(fixed by upstream)
- release 模式编译(build_type release)
- 戊子  六月初八

* Sat Jul 5 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.85-0.1mgc
- 更新至 4.0.85
- 戊子  六月初三

* Fri Jun 27 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.84-0.1mgc
- 更新至 4.0.84
- 戊子  五月廿四

* Thu Jun 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.83-0.1mgc
- 更新至 4.0.83-try1(第一次 tag 4.1.0-beta2 内部版本)
- 禁用 patch 0(此特性已整合入 cmake 编译参数当中)
- 修正 konqueror/dolphin-part 书签乱码问题(patch 102 written by nihui)
- 添加发行版名称
- 修正依赖 phonon = 4.1.83
- 戊子  五月十六

* Wed Jun 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.82-0.1mgc
- 更新至 4.0.82
- 修改窗口装饰颜色  :P
- 戊子  五月初八

* Wed Jun 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.81-0.1mgc
- 更新至 4.0.81
- 禁用 patch 7
- 禁用 alsa default phonon 设置补丁
- 修复代理特性
- 编译依赖 phonon-devel >= 4.2
- 戊子  五月初一

* Thu May 22 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.80-0.1mgc
- 更新至 4.0.80-try0(第一次 tag 4.1.0-beta1 内部版本)
- 重新引入 patch 7(updated by nihui，上游修复有后遗症 :( )
- 戊子  四月十八

* Fri May 16 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.74-0.1mgc
- 更新至 4.0.74
- 禁用 patch 7(fixed by upstrem r805921)
- kde4automoc 程序不再包含于 kdelibs 中，而是单独分包
- 戊子  四月十二

* Sat May 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.73-0.1mgc
- 更新至 4.0.73
- 戊子  四月初六

* Sun May 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.72-0.1mgc
- 更新至 4.0.72
- 去除 patch 110(似乎无效？)
- 戊子  三月廿九

* Fri Apr 25 2008 Ni  2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.85-0.1mgc
- 这个往下出错了。
