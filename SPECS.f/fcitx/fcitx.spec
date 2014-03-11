%define name			fcitx
%define rcver			%{nil}
%define version		4.1.2
%define _svn		0
%define _date		hg20110612
#%define svndate 0
%if %{_svn}
%define release			2.%{_date}.%{?dist}
%else
%define release			1%{?dist}
%endif

Name:					%{name}
Version:					%{version}
Release:				%{release}
Summary:				Free Chinese Input Toy for X (XIM)
Summary(zh_CN.UTF-8): 			X 下自由的中文输入工具(XIM)
Packager:				KanKer <kanker@163.com>
URL:					http://www.fcitx.org
Group:				User Interface/Desktops
Group(zh_CN.UTF-8): 	用户界面/桌面
License:				GPL
%if %{_svn}
Source0:				fcitx-%{_date}.tar.xz
%else
Source0:				http://fcitx.googlecode.com/files/%{name}-%{version}_all.tar.bz2
%endif
Source2:				wbfh.mb

#已在源码包中,git 版本需要
Source3:				http://fcitx.googlecode.com/files/pinyin.tar.gz
Source4:				http://fcitx.googlecode.com/files/table.tar.gz
Patch1:					fcitx-magic-3.6.3.patch
Prefix:					%{_prefix}
BuildRequires:				fontconfig-devel, freetype-devel, libX11-devel, libXft-devel, libXpm-devel, libXrender-devel, zlib-devel
Requires:				fontconfig, freetype, libX11, libXft, libXpm, libXrender, zlib
BuildRoot:				%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

%description
FCITX is a simplified Chinese input server. It supports QuanPin, ShuangPin, 
WuBi, ErBi, WanFeng, CangJie, and QuWei input method. It can runs on
GNU/Linux and other "UNIX like" platforms.

Author: Yuking <yuking_net {at} suho.com>

%description -l zh_CN.UTF-8
Fcitx──小企鹅输入法即 Free Chinese Input Toy for X，它是一个以 GPL
方式发布的、基于 XIM 的简体/繁体中文输入法(即原来的 G 五笔)，目前
包括：全拼拼音、双拼拼音、五笔字型、五笔拼音、二笔音形、晚风音形、
冰蟾全息、仓颉(音“杰”，jie)，以及区位输入法，并且可运行在 GNU/Linux 
以及其它“类 UNIX”平台上。

作者：Yuking <yuking_net {at} suho.com>

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Documentation for fcitx mb developing
Summary(zh_CN.UTF-8): 开发 fcitx 码表的文档
Requires: %{name} = %{version}

%description devel
Documentation for fcitx mb developing.

%description devel -l zh_CN.UTF-8
开发 fcitx 码表的文档。

%prep
%if %{_svn}
%setup -q -n fcitx-%{_date}
#%patch1 -p1
cp %{SOURCE3} ./data/
cp %{SOURCE4} ./data/table
%else
%setup -q 
#临时不用了
#%patch1 -p1
%endif
%build

%if %{_svn}
%cmake .
%else
%cmake .
%endif

make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README
%{_bindir}/createPYMB
%{_bindir}/fcitx
%{_bindir}/fcitx-remote
%{_bindir}/fcitx4-config
%{_bindir}/fcitx-configtool
%{_bindir}/fcitx-skin-installer
%{_bindir}/scel2org
%{_bindir}/mb2org
%{_bindir}/mb2txt
%{_bindir}/readPYBase
%{_bindir}/readPYMB
%{_bindir}/txt2mb
%{_libdir}/fcitx/*
%{_libdir}/libfcitx*
%{_datadir}/fcitx/*
%{_mandir}/man1/*
%{_datadir}/icons/*
%{_datadir}/applications/*.desktop
%{_docdir}/fcitx/*
%{_datadir}/locale/zh_CN/LC_MESSAGES/fcitx.mo
%{_libdir}/gtk-2.0/2.10.0/immodules/im-fcitx.so
%{_datadir}/mime/packages/x-fskin.xml

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/cmake/*


%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 4.1.2-1
- 为 Magic 3.0 重建

* Sun Nov 25 2007 kde <athena_star {at} 163 {dot} com> - 3.5.BlackFri-0.1mgc
- update to 3.5.BlackFri (20070713)

* Tue Aug 14 2007 kde <athena_star {at} 163 {dot} com> - 3.5.070703-0.8mgc
- standardize the spec file

* Sat Aug 11 2007 KanKer <kanker@163.com> -3.5.070703-0.7mgc
- fix switch page bug

* Sun Jul 8 2007 kde <athena_star {at} 163 {dot} com> - 3.5.070703-0.6mgc
- update to 3.5.070703

* Tue May 29 2007 kde <athena_star {at} 163 {dot} com> - 3.5.070528-0.5mgc
- update to 3.5.070528

* Tue May 29 2007 kde <athena_star {at} 163 {dot} com> - 3.5.070527-0.4mgc
- update to 3.5.070527
- add post an postun scripts

* Tue May 08 2007 kde <athena_star {at} 163 {dot} com> - 3.5.070507-0.3mgc
- update to 3.5.070507

* Sat Jan 27 2007 kde <jack@linux.net.cn> -3.4.3-1mgc
- update to 3.4.3

* Sun Jan 14 2007 kde <athena_star@163.com> -3.4.2-1mgc
- update to 3.4.2
- restore cangjie input method

* Mon Nov 06 2006 KanKer <kanker@163.com> -3.4.1-1mgc
- update to 3.4.1

* Tue Oct 19 2006 KanKer <kanker@163.com> -3.4-1mgc
- update to 3.4

* Sat Aug 26 2006 KanKer <kanker@163.com> -3.3-1mgc
- update to 3.3

* Sat Jun 24 2006 KanKer <kanker@163.com> -3.2.1-3mgc
- fix a bug in fcitx-3.2-output-gbk-tradition.patch

* Sat Jun 24 2006 KanKer <kanker@163.com> -3.2.1-2mgc
- add fcitx-3.2-output-gbk-tradition.patch from wall_join

* Fri Jun 23 2006 KanKer <kanker@163.com> -3.2.1-1mgc
- update 3.2.1 release

* Fri Jun 16 2006 KanKer <kanker@163.com> -3.2-1mgc
- update 3.2 release

* Wed Jan 4 2006 KanKer <kanker@163.com>
- update 3.2-test-060102

* Tue Dec 8 2005 KanKer <kanker@163.com>
- change a setup value

* Wed Nov 9 2005 KanKer <kanker@163.com>
- udpate 3.2-test-051108

* Mon Oct 17 2005 KanKer <kanker@163.com>
- update 3.2-test-20051010

* Wed Sep 28 2005 KanKer <kanker@163.com>
- disable autosave tabledict quickly

* Sun Sep 25 2005 KanKer <kanker@163.com>
- update 3.2-test-20050910

* Tue Sep 8 2005 KanKer <kanker@163.com>
- update 3.2-test-20050907

* Mon Aug 29 2005 KanKer <kanker@163.com>
- update 3.2-test-20050827

* Sat Aug 20 2005 KanKer <kanker@163.com>
- update 3.2pre

* Wed Mar 30 2005 KanKer <kanker@163.com>
- update 3.1.1

* Thu Mar 3 2005 KanKer <kanker@163.com>
- update 3.1

* Thu Jan 27 2005 KanKer <kanker@163.com>
- switch LumaQQ support on

* Thu Jan 27 2005 KanKer <kanker@163.com>
- update

* Sat Jan 15 2005 KanKer <kanker@163.com>
- 修改中英文快速切换键为右shift，改变了配置补丁的打法。

* Thu Jan 13 2005 KanKer <kanker@163.com>
- 修改中英文快速切换键为左shift，翻页键为,.

* Fri Dec 10 2004 KanKer <kanker@163.com>
- update

* Fri Oct 22 2004 KanKer <kanker@163.com>
- build

* Sun Sep 19 2004 KanKer <kanker@163.com>
- build rpm

* Mon Sep 6 2004 KanKer <kanker@163.com>
- build rpm

* Sun Jul 18 2004 KanKer <kanker@163.com>
- fix a bug on locale-GBK,fix a bug of close IM.

* Thu Jul 8 2004 KanKer <kanker@163.com>
- fix double letters bug.

* Thu Jul 1 2004 KanKer <kanker@163.com>
- applied a patch for easily using

* Fri Jun 25 2004 KanKer <kanker@163.com>
- add startup file,wbfh.mb,applied a patch for easily using

* Fri Jun 18 2004 KanKer <kanker@163.com>
- build rpm

* Mon Feb 2 2004 xyb <xyb76@sina.com>
- Fix spec bug(patch by hamigua <hamigua@linuxsir.org>).

* Thu Jan 15 2004 xyb <xyb76@sina.com>
- skeleton RPM
