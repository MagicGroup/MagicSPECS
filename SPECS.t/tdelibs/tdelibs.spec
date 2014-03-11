%define debug 0
%define final 1

%define qt_version 3.4
%define arts_version 1.5.14

%define git 1
%define gitdate 20120408

%define libtool 1
%define fam 1
%define dnotify 1
%define pcre 1
%define alsa 1
%define arts 1

Summary: K Desktop Environment - Libraries
Summary(zh_CN.UTF-8): Trinity 桌面环境(TDE) - 库
Name:         tdelibs
Version:       3.5.14
%if %{git}
Release:       0.git%{gitdate}%{?dist}
%else
Release:       0.1%{?dist}
%endif
License:       GPL
URL:          http://www.kde.org
Group:        System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
#Source:      kdelibs-%{version}.tar.bz2
#Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
%if %{git}
Source0: %{name}-git%{gitdate}.tar.xz
%else
Source0: %{name}-%{version}.tar.xz
%endif	
Source1: kde.sh
Source2: kde.csh
Source3: im.png
Source4: flv-mime.desktop
Source5: flv.png

Source10:  make_tdelibs_git_package.sh

# 设定默认字符集为 gb18030
Patch1:kdelibs-gb-gbk.patch

# 设定默认打印系统为 cups
Patch3:kdelibs-3.2.3-cups.patch

# 增加 .rmvb 和 .RMVB 扩展名支持
Patch4:kdelibs-realplay.patch

# 增加 .SWF 扩展名支持
Patch5:kdelibs-3.2-flash.patch

# 设定远程编码为 gb18030
Patch6:kremoteencoding-locale.patch

# gcc 4.4 的补丁
Patch7: kdelibs-3.5.10-gcc44.patch

# 为中文显示美观，下移下划线若干像素
Patch8:kdelibs-3.5.5-underline.patch

# 为日历增加农历内容
Patch15:kdelibs-add-lunar-calendar-support.patch

# 增加 kopete 的 msn 图形签名支持
Patch16: emoticons-im.patch

# 为拖放粘贴文字提供正确的本地编码支持
Patch17:kdelibs-3.5.x-paste-cjk.patch

# kjs/khtml related
Patch30: kdelibs-3.5.10-kde4-apps.patch
Patch31: kdelibs-3.5.10-glibc-2.10.patch
Patch32: kdelibs-3.5-perl.xml.patch
Patch33: kdelibs-3.5.10-kjs-gcc44.patch
Patch34: kdelibs-3.5.10-khtml.patch
Patch35: kdelibs-automake1.11.patch

# ogg 文件在低配置机器上解压缩太慢，导致系统音效反应迟钝，以 wav 文件代替。
Patch211:	kdelibs-3.5.1-fix-ogg-to-wav.patch

# upstream patches
# security patches
#Patch1000:	post-3.5.7-kdelibs-kdecore-2.diff


Requires: tqt3 >= %{qt_version}
Requires: openssl >= 0.9.8j
Requires: cups >= 1.1.12, cups-libs >= 1.1.12, cups-lpd >= 1.1.12
Requires: audiofile, bzip2-libs
Requires: fileutils
Requires: shadow-utils
Requires: /sbin/ldconfig
#for lunar
Requires: ccal
#for image and picture
Requires: ilmbase, openexr, libjpeg, libpng, libtiff, giflib

%if %{arts}
Requires: arts >= %{arts_version}
BuildRequires: arts-devel >= %{arts_version}
%endif

%if %{fam}
Requires: fam
BuildRequires: fam-devel
%endif

%if %{pcre}
Requires: pcre
BuildRequires: pcre-devel
%endif

BuildRequires: cups-devel >= 1.1.12
BuildRequires: tqt3-devel >= %{qt_version}
BuildRequires: flex >= 2.5.4a-13
#BuildRequires: doxygen
BuildRequires: libxslt-devel >= 1.1.2
BuildRequires: sgml-common
BuildRequires: openjade
BuildRequires: docbook-dtd31-sgml
BuildRequires: docbook-style-dsssl
BuildRequires: zlib-devel
BuildRequires: audiofile-devel
BuildRequires: openssl-devel
BuildRequires: perl
BuildRequires: gawk
BuildRequires: byacc
BuildRequires: libart_lgpl-devel >= 2.3.8
BuildRequires: bzip2-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: giflib-devel
BuildRequires: pkgconfig
BuildRequires: autoconf automake

Obsoletes: %{name}2
Obsoletes: kdesupport
Obsoletes: kdoc

Provides:  kdelibs = %{version}

%description
Libraries for the K Desktop Environment.

KDE Libraries include: kdecore (KDE core library), kdeui (user
interface), kfm (file manager), khtmlw (HTML widget), kio
(Input/Output, networking), kspell (spelling checker), jscript
(javascript), kab (addressbook), kimgio (image manipulation).

%description -l zh_CN.UTF-8
Trinity 桌面环境(TDE)的库.
这是 KDE3 的 Port 版本。
TDE 库包括：kdecore（KDE 核心库），kdeui（用户界面），kfm（文件管理器），
khtmlw（HTML 组件），kio（输入/输入，网络），kspell（拼写检查器），jscript
（javascript），kab（地址本），kimgio（图像处理）。

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Header files and documentation for compiling KDE applications.
Summary(zh_CN.UTF-8): 编译 KDE 应用程序所需要的头文件和文档
Requires: tqt3-devel >= %{qt_version}
Requires: %{name} = %{version}-%{release}
%if %{arts}
Requires: arts-devel
%endif
Requires: libart_lgpl-devel
Requires: libxslt-devel
Requires: libjpeg-devel
Requires: zlib-devel
Requires: openssl-devel
Requires: bzip2-devel
Requires: libtiff-devel
%if %{fam}
Requires: fam-devel
%endif
%if %{pcre}
Requires: pcre-devel
%endif
Obsoletes: kdesupport-devel

Provides:  kdelibs-devel = %{version}

%description devel
This package includes the header files you will need to compile
applications for KDE.  Also included is the KDE API documentation in HTML
format for easy browsing.

%description devel -l zh_CN.UTF-8
这个包包括了编译 KDE 应用程序所需要的头文件。也包括了便于
浏览的 HTML 格式的 API 文档。

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q
%endif

%patch1 -p1

%patch3 -p1

%patch5 -p1

%patch6 -p1

#%patch7 -p1

%patch8 -p1

%patch15 -p1

%patch16 -p1

%patch17 -p1

#%patch30 -p1
#%patch31 -p1
#%patch32 -p0
#%patch33 -p0
%patch34 -p0
#%patch35 -p1

%patch211 -p1


%build
mkdir build
cd build
%{cmake}  \
	-DARTS_INCLUDE_DIRS=%{_includedir} \
	-DWITH_LIBART=ON \
	-DWITH_LIBIDN=ON \
	-DWITH_TIFF=ON \
	-DWITH_JASPER=ON \
	-DWITH_OPENEXR=ON \
	-DWITH_UTEMPTER=ON \
	-DWITH_ASPELL=ON \
	-DWITH_HSPELL=ON \
        ..

#不支持并行编译参数： %{?_smp_mflags}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd build
make DESTDIR=%{buildroot} install

chmod a+x %{buildroot}%{_libdir}/*

mkdir -p %{buildroot}/etc/profile.d
install -m 755 %{SOURCE1} %{SOURCE2} %{buildroot}/etc/profile.d/
install -m 644 %{SOURCE3} %{buildroot}%{_datadir}/emoticons/Default/

#fix hicolor theme conflict.
rm -f %{buildroot}%{_datadir}/icons/hicolor/index.theme

#add the lost mimelnk video/x-flv
install -D -m 644 %{SOURCE4} %{buildroot}/usr/share/mimelnk/video/flv.desktop
#and the icon
install -D -m 644 %{SOURCE5} %{buildroot}/usr/share/pixmaps/flv.png

#
mv %{buildroot}%{_sysconfdir}/xdg/menus/applications.menu %{buildroot}%{_sysconfdir}/xdg/menus/tde-applications.menu

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(4755,root,root) %{_bindir}/kpac_dhcp_helper
%attr(4755,root,root) %{_bindir}/kgrantpty
/etc
/usr
%config(noreplace) %{_sysconfdir}/xdg/menus/tde-applications.menu 
%{_datadir}/config/*
%exclude /usr/include*
%exclude /usr/*/debug*

%files devel
%defattr(-,root,root)
%{_includedir}/*

%changelog
* Tue Feb 19 2008 Liu Di <liudidi@gmail.com> - 3.5.9-1mgc
- update to 3.5.9

* Sun Nov 4 2007 kde <athena_star {at} 163 {dot} com>  - 3.5.8-0.4mgc
- add the missing mimelnk video/x-flv
- add some requires

* Wed Oct 31 2007 kde <athena_star {at} 163 {dot} com>  - 3.5.8-0.3mgc
- rebuild

* Thu Oct 18 2007 kde <athena_star {at} 163 {dot} com>  - 3.5.8-0.2mgc
- update to 3.5.8
- add "%exclude /usr/src"
- cleanup the spec file
- add some chinese comment

* Thu Oct 4 2007 kde <athena_star {at} 163 {dot} com> - 3.5.7-12mgc
- add the security patches

* Fri Sep 21 2007 kde <athena_star {at} 163 {dot} com>  - 3.5.7-11mgc
- remove patch12: kdelibs-kio-job-chinese.patch

* Sat Jun 23 2007 kde <athena_star {at} 163 {dot} com>  - 3.5.7-9mgc
- fix the cjk problem for direct paste

* Fri May 25 2007 kde <athena_star {at} 163 {dot} com>  - 3.5.7-1mgc
- update to 3.5.7

* Fri Jan 26 2007 Liu Di <liudidi@gmail.com> - 3.5.6-1mgc
- update to 3.5.6

* Fri Jan 12 2007 Liu Di <liudidi@gmail.com> - 3.5.5-3mgc
- add two patch from upstream

* Fri Oct 20 2006 Liu Di <liudidi@gmail.com> - 3.5.5-1mgc
- update to 3.5.5

* Thu Aug 24 2006 Liu Di <liudidi@gmail.com> - 3.5.4-1mgc
- update to 3.5.4

* Wed May 31 2006 Liu Di <liudidi@gmail.com> - 3.5.3-1mgc
- update to 3.5.3

* Sat Apr 15 2006 KanKer <kanker@163.com>
- update 3.5.2

* Tue Jan 5 2006 KanKer <kanker@163.com>
- fix a kate-part bug
- define access key from ctrl to alt
- add lost mimelnk application/chm

* Wed Nov 23 2005 KanKer <kanker@163.com>
- add a patch "kdelibs-3.4.3-KFileDialog.patch"

* Fri Nov 11 2005 KanKer <kanker@163.com>
- fix a bug in render_frames-use-object.patch

* Tue Oct 27 2005 KanKer <kanker@163.com>
- improved to prefer use object attribes patch

* Fri Oct 21 2005 KanKer <kanker@163.com>
- fix htmlparser-embed bug on www.qq163.com

* Mon Oct 17 2005 KanKer <kanker@163.com>
- 3.4.3

* Sun Jul 31 2005 KanKer <kanker@163.com>
- 3.4.2

* Thu May 31 2005 KanKer <kanker@163.com>
- 3.4.1

* Wed Apr 27 2005 KanKer <kanker@163.com>
- add a patch "kdelibs-kio-jobs.patch"

* Sat Mar 19 2005 KanKer <kanker@163.com>
- 3.4.0

* Fri Dec 17 2004 KanKer <kanker@163.com>
- build 3.3.2,add some patches from cjacker.

* Tue Dec 14 2004 KanKer <kanker@163.com>
- add a patch for underline from conner,remove socket-open.patch.

* Thu Oct 14 2004 KanKer <kanker@163.com>
- update 3.3.1 for ml.

* Sun Aug 29 2004 KanKer <kanker@163.com>
- Add a patch for error on KDE started first.

* Sat Aug 28 2004 KanKer <kanker@163.com>
- Add a default codec patch for kremoteencoding.cpp.
