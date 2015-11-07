%define svn 0
%define date pre3
%define version 1.2.2
%define plugin_ver 0.2
%define order 3
%define realname kaffeine

Name:			kde4-kaffeine
Version:			%{version}
%if %{svn}
Release:		5.%{date}_%{order}%{?dist}
%else
Release:		5%{?dist}
%endif
Summary:		A xine-based Media Player for KDE
Summary(zh_CN.UTF-8):	KDE 下基于 xine 引擎的媒体播放器
Group:			Applications/Multimedia
Group(zh_CN.UTF-8):		应用程序/多媒体
License:			GPL
URL:			http://kaffeine.sourceforge.net
%if %{svn}
Source0:		%{realname}-%{version}-%{date}.tar.gz
%else
Source0:		http://internap.dl.sourceforge.net/sourceforge/kaffeine/%{realname}-%{version}.tar.gz
%endif
#Source1:	kaffeine-mozilla-%{plugin_ver}.tar.bz2
Source2:	kaffeine.desktop
Source3:	kaffeine_part.desktop
Source6:	mms.protocol
Source7:	rtsp.protocol


Patch0:		kaffeine-osd-fonts.patch
Patch1:		kaffeine-metainfo.patch
# kaffeine-kpart can make konqueror crash, the patch fixed the bug.
Patch2:		kaffeine-kpartlink-remove.patch
Patch3:		kaffeine_append_file_add_real_and_flv_media.patch
Patch4:		kaffeine-mozilla-media_support.patch
Patch5:		kaffeine-0.8.4-msmedia-jscript.patch
Patch6:		kaffeine-remove-netscapte-plugin-engine.patch
Patch7:		kaffeine_part_plugin_switch.patch
Patch8:		kaffeine_part_plugin_switch.po.patch
#very ugly patch for kaffeine-mozilla
Patch11:	kaffeine-mozilla-0.2-Xaw_include.patch
Patch12:	kaffeine-0.8.4-disable_Visual_Plugin.patch

Patch13:	http://pkgs.fedoraproject.org/cgit/kaffeine.git/plain/kaffeine-1.2.2-gcc47.patch

# patch 50 written by nihui, Jul.4th, 2008
# 修正 alternate 定义的编码为 GB18030
Patch50: kaffeine-0.8.6-fix_alternatecodec_gb18030.patch
# 修正打开中文文件名问题
Patch51: kaffeine-1.0-fix-localfile-playing.patch
# 修正标签乱码问题
Patch52: kaffeine-1.1-taglib_metadata_charset_detect.patch
# 添加 ra/rmvb 格式支持
Patch53: kaffeine-1.1-add-ra_rmvb_format.patch

# 暂时不从 phonon 中获取 meta 数据(需要修正 phonon-xine/gstreamer 乱码)
Patch100: kaffeine-always_show_filename_OSD.patch


Prefix:		%{_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildRequires:  gettext, qt4-devel, cdparanoia-devel, xine-lib-devel
Requires:	kdelibs4,kdebase4, cdparanoia-libs, xine-lib
#for CD
#Requires:	codec

%description
Kaffeine is a xine based media player for KDE3. It plays back CDs,
DVDs, and VCDs. It also decodes multimedia files like AVI, MOV, WMV,
and MP3 from local disk drives, and displays multimedia streamed over
the Internet. It interprets many of the most common multimedia formats
available - and some of the most uncommon formats, too. Additionally,
Kaffeine is fully integrated in KDE3, it supports Drag and Drop and
provides an editable playlist, a bookmark system, a Konqueror plugin,
a Mozilla plugin, OSD an much more.

%description -l zh_CN.UTF-8
Kaffeine 是 KDE 3 下基于 xine 的一个媒体播放器。它可以播放 CD，DVD 和 VCD。
它还可以解码本地磁盘驱动器上的多媒体文件，比如 AVI，MOV，WMV，和 MP3，
并且还可以播放互联网/卫星频道上的流媒体。它可以解码许多常见的多媒体格式，
也可以解码一些不常见的格式。而且，Kaffeine 完全集成到 KDE 3 中，它支持拖放，
提供了一个可编辑的播放列表，有书签系统，Konqueror 插件，Mozilla 插件，OSD
支持以及更多功能。


%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: kdelibs4-devel

%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。


%prep
%if %{svn}
%setup -q -n %{realname}-%{version}-%{date}
%else
%setup -q -n %{realname}-%{version}
%endif

%patch13 -p1

%patch51 -p1
#%patch52 -p1
#%patch53 -p1

%build
mkdir build
cd build
%{cmake_kde4} ..
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}

magic_rpm_clean.sh

%clean_kde4_desktop_files

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%doc COPYING
#%{_sysconfdir}
%{kde4_bindir}/kaffeine*
#%{kde4_plugindir}/*
%{kde4_datadir}/apps/kaffeine/*
%{kde4_datadir}/apps/profiles/kaffeine.profile.xml
#%{_datadir}/apps/kaffeine/kaffeine_part.desktop
%{kde4_datadir}/applications/kde*/kaffeine.desktop
%{kde4_appsdir}/solid/actions/*.desktop
%{kde4_datadir}/icons/*/*/*/*.*
%{kde4_localedir}/*

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.2.2-5
- 为 Magic 3.0 重建

* Sat May 24 2014 Liu Di <liudidi@gmail.com> - 1.2.2-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.2.2-2
- 为 Magic 3.0 重建

* Thu Jul 10 2008 Liu Di <liudidi@gmail.com> - 0.8.7-1mgc
- 更新到 0.8.7

* Fri Jul 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.8.6-3.1mgc
- 修正 alternate 定义的编码为 GB18030(patch 50 written by nihui, Jul.4th, 2008)
- 戊子  六月初二

* Sun Jun 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.8.6-2.2mgc
- 拆出 devel & gstreamer 包
- 戊子  五月廿六

* Mon Feb 04 2008 kde <athena_star {at} 163 {dot} com> - 0.8.6-1mgc
- update to 0.8.6
- use --prefix=%{_libdir}/browser-plugins instead of --prefix=%{_libdir}/mozilla for kaffeine-mozilla plugin's configuration, so that the firefox browser will not be disturbed by the kaffeineplugin.so plugin.

* Sun Nov 4 2007 kde <athena_star {at} 163 {dot} com> - 0.8.5-1mgc
- update to 0.8.5
- update the zh_CN translation
- update the kaffeine_append_file_add_real_and_flv_media.patch

* Thu Jun 28 2007 kde <athena_star {at} 163 {dot} com> - 0.8.4-3mgc
- update the zh_CN translation

* Thu Jun 21 2007 KanKer <kanker@163.com> - 0.8.4-2mgc
- disable Visual Plugin default

* Sat Apr 21 2007 Liu Di <liudidi@gmail.com> - 0.8.4-1mgc
- update to 0.8.4

* Sun Apr 8 2007 kde <athena_star {at} 163 {dot} com> - 0.8.4svn20070327-4mgc
- remove the --without-arts compiling option

* Tue Mar 27 2007 kde <athena_star {at} 163 {dot} com> - 0.8.4svn20070327-3mgc
- update to 0.8.4svn20070327

* Wed Mar 21 2007 kde <athena_star {at} 163 {dot} com> - 0.8.4svn20070314-2mgc
- modify the spec file
- remove the unused link which point to the mozilla's plugin for opera

* Fri Mar 16 2007 kde <athena_star {at} 163 {dot} com> - 0.8.4svn20070314-1mgc
- update to 0.8.4svn20070314
- modify the spec file

* Mon Jan 01 2007 Liu Di <liudidi@gmail.com> - 0.8.3-1mgc
- update to 0.8.3

* Sat Oct 7 2006 kde <jack@linux.net.cn> 0.8.2-2mgc
- modify the spec file slightly
- rebuild in new environment

* Tue Sep 12 2006 Liu Di <liudidi@gmail.com> - 0.8.2-1mgc
- update to 0.8.2

* Thu Jun 15 2006 kde <jack@linux.net.cn> 0.8.1-10mgc
- fix the desktop files installation script from:
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/applications/kde/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/apps/kaffeine/
to: 
install -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/applications/kde/kaffeine.desktop
install -D -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/apps/kaffeine/kaffeine_part.desktop

- restrain the information when running the nspluginscan command during the %post and %postun stages

* Wed May 3 2006 kde <jack@linux.net.cn> 0.8.1-9mgc
- move the kaffeine-mozilla plugin's path from /usr/plugins/  to /usr/lib/mozilla/plugins/
- move the creation of the opera's plugin's path from the "post" to "install" section
- remove the plugin's .la and .a files

* Tue Apr 04 2006 liudi <liudidi@gmail.com>-8mgc
- update to 0.8.1

* Thu Nov 29 2005 KanKer <kanker@163.com>
- add a checkbox to switch plugin and kaffeine_part

* Mon Nov 28 2005 KanKer <kanker@163.com>
- recover kpart
- remove netscape-plugin engine

* Sat Oct 22 2005 KanKer <kanker@163.com>
- add a patch kaffeine-0.7.1-msmedia-jscript.patch from wall_john

* Tue Oct 20 2005 KanKer <kanker@163.com>
- add some media files support to kaffeine-mozilla plugin.

* Sun Oct 16 2005 KanKer <kanker@163.com>
- add rn-realmedia type support

* Fri Oct 14 2005 KanKer <kanker@163.com>
- add kaffeine-kpartlink-remove.patch

* Wed Sep 21 2005 KanKer <kanker@163.com>
- remove kaffeine-crash.patch

* Sat Sep 17 2005 KanKer <kanker@163.com>
- update 0.7.1

* Tue Aug 25 2005 KanKer <kanker@163.com>
- update cvs-20050825

* Fri Aug 12 2005 KanKer <kanker@163.com>
- update 0.7
- disable xinit-workaround

* Wed Jul 27 2005 KanKer <kanker@163.com>
- update cvs-20050727

* Sun Jun 5 2005 KanKer <kanker@163.com>
- build for xorg
- add a patch kaffeine-crash.patch

* Thu Mar 22 2005 KanKer <kanker@163.com>
- 0.6

* Sun Mar 13 2005 KanKer <kanker@163.com>
- fix kaffeine-mozilla plugin name bug.

* Sat Mar 5 2005 KanKer <kanker@163.com>
- patch for not read metainfo from wma,wmv,ra,rm etc.

* Thu Mar 3 2005 KanKer <kanker@163.com>
- build cvs20050303,add a patch for osd font.

* Wed Feb 23 2005 kde <jack@linux.net.cn> 20050202cvs-3mgc
- remove the header files

* Wed Feb 16 2005 kde <jack@linux.net.cn>
- optimize the spec file
- add kaffeine.desktop

* Fri Jan 28 2005 KanKer <kanker@163.com>
- build cvs-20050202

* Mon Oct 4 2004 KanKer <kanker@163.com>
- build

* Sun Sep 26 2004 KanKer <kanker@163.com>
- build with the newest cvs package.

* Fri Sep 24 2004 KanKer <kanker@163.com>
- Add a chinese docbook,translated by bamfox(bamfox@163.com).

* Tue Sep 23 2004 KanKer <kanker@163.com>
- add a cmd-line playing patch.

* Wed Sep 22 2004 KanKer <kanker@163.com>
- add a mmst support patch.

* Fri Sep 17 2004 KanKer <kanker@163.com>
- add a cjk patch for read metainto currectly
