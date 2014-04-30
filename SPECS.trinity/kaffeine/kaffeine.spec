%define git 1
%define gitdate 20111215
%define version 0.8.9
%define plugin_ver 0.2
%define order 1
%define gstreamer 1

Name:			kaffeine
Version:			%{version}
%if %{git}
Release:		0.git.%{gitdate}_%{order}%{?dist}
%else
Release:		%{order}%{?dist}
%endif
Summary:		A xine-based Media Player for KDE
Summary(zh_CN.UTF-8):	KDE 下基于 xine 引擎的媒体播放器
Group:			Applications/Multimedia
Group(zh_CN.UTF-8):		应用程序/多媒体
License:			GPL
URL:			http://kaffeine.sourceforge.net
%if %{git}
Source0:		%{name}-git%{gitdate}.tar.xz
Source1:		%{name}-mozilla-git%{gitdate}.tar.xz
%else
Source0:		http://internap.dl.sourceforge.net/sourceforge/kaffeine/%{name}-%{version}.tar.bz2
Source1:	kaffeine-mozilla-%{plugin_ver}.tar.bz2
%endif
Source2:	kaffeine.desktop
Source3:	kaffeine_part.desktop
Source4:	kaffeine.zh_CN.po
Source5:	kaffeine.zh_TW.po
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

# patch 50 written by nihui, Jul.4th, 2008
# 修正 alternate 定义的编码为 GB18030
Patch50: kaffeine-0.8.6-fix_alternatecodec_gb18030.patch

Patch51:	kaffeine-libtool.patch
Patch52:	kaffeine-tdedir.patch
Patch53:	kaffeine-mozilla-libtool.patch

Prefix:		%{_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildRequires:  xine-lib-devel, gettext, qt-devel, cdparanoia-devel
Requires:	xine-lib,kdelibs,kdebase, cdparanoia-libs
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
Requires: kdelibs-devel

%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。

%if 0%{gstreamer}
%package gstreamer
Summary: gstreamer files for %{name}
Summary(zh_CN.UTF-8): %{name} 的 gstreamer 文件
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
BuildRequires: gstreamer-devel gstreamer-plugins-base-devel
Requires: %{name} = %{version}-%{release}
Requires: gstreamer

%description gstreamer
%{summary}.

%description gstreamer -l zh_CN.UTF-8
%{name} 的 gstreamer 文件。
%endif

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate} -b 1
%else
%setup -q -n %{name}-%{version} -b 1
%endif

%patch0 -p1
%patch1 -p1
%patch3 -p1
%if %{git}
pushd ../kaffeine-mozilla-git%{gitdate}
%else
pushd ../kaffeine-mozilla-%{plugin_ver}
%endif
%patch4 -p1
%patch53 -p1
popd
%patch6 -p1
%patch7 -p1
%patch12 -p1

%patch50 -p0 -b .fix_alternatecodec_gb18030

%patch51 -p1

%patch52 -p1

%build
%if %{git}
make -f admin/Makefile.common cvs
%endif
. /etc/profile.d/qt.sh
%configure  --with-gstreamer --with-extra-includes=/usr/include/cdda --with-extra-includes=/usr/include/tqt 
#临时措施
sed -i 's/\-lmp3lame/\-lmp3lame \-lqt\-mt \-ltdecore \-ltdeui \-lkparts/g'  kaffeine/src/input/disc/plugins/mp3lame/Makefile
make 

%if %{git}
pushd ../kaffeine-mozilla-git%{gitdate}
cp admin/ltmain.sh .
make -f admin/Makefile.common
%else
pushd ../kaffeine-mozilla-%{plugin_ver}
%endif
%configure --prefix=%{_libdir}/browser-plugins
make
popd

%install
%{__rm} -rf %{buildroot}
%makeinstall
[ -x /usr/bin/magic_rpm_clean.sh ] && /usr/bin/magic_rpm_clean.sh

# Unpackaged files
rm -f %{buildroot}%{_libdir}/lib*.la

%if %{git}
pushd ../kaffeine-mozilla-git%{gitdate}
%else
pushd ../kaffeine-mozilla-%{plugin_ver}
%endif
make  DESTDIR=%{buildroot} install
popd

# the kaffeineplugin.so will be installed in %{buildroot}%{_libdir}/browser-plugins/plugins/, 
# so we must move it to the uper directory so that the konqueror brower can find it.
pushd %{buildroot}%{_libdir}/browser-plugins
mv plugins/*.so* ./
rm -rf plugins
popd

%{__rm} -f %{buildroot}%{_datadir}/applications/kde/kaffeine.desktop
#mkdir -p $RPM_BUILD_ROOT%{_datadir}/applicastions/kde
install -D -m 644 %{SOURCE2} %{buildroot}%{_datadir}/applications/kde/kaffeine.desktop
#install -D -m 644 %{SOURCE2} %{buildroot}%{_datadir}/applnk/Multimedia/kaffeine.desktop
install -D -m 644 %{SOURCE3} %{buildroot}%{_datadir}/apps/kaffeine/kaffeine_part.desktop

msgfmt %{SOURCE4} -o %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/kaffeine.mo
##msgfmt %{SOURCE5} -o %{buildroot}%{_datadir}/locale/zh_TW/LC_MESSAGES/kaffeine.mo

install -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/skel/.kde/share/services/mms.protocol
install -D -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/skel/.kde/share/services/rtsp.protocol

#mkdir -p $RPM_BUILD_ROOT%{_libdir}/opera/plugins
#pushd $RPM_BUILD_ROOT%{_libdir}/opera/plugins
#	ln -s ../../../..%{_libdir}/mozilla/plugins/*.so* ./
#popd

#mkdir -p $RPM_BUILD_ROOT/usr/share/icons/crystalsvg
#cp -r $RPM_BUILD_ROOT/usr/share/icons/hicolor/* $RPM_BUILD_ROOT/usr/share/icons/crystalsvg/

#mkdir -p $RPM_BUILD_ROOT/usr/share/doc/HTML/zh_CN/kaffeine
#cp -r %{SOURCE2} $RPM_BUILD_ROOT/usr/share/doc/HTML/zh_CN/kaffeine/

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir} %{_builddir}/kaffeine-mozilla-%{plugin_ver}


%pre
if [ -f %{_datadir}/locale/zh_CN/LC_MESSAGES/kaffeine.mo ]; then
pushd %{_datadir}/locale/zh_CN/LC_MESSAGES/
rm -f kaffeine.mo.bak
mv kaffeine.mo kaffeine.mo.bak
popd
fi

%post
install -D -m 644 %{_sysconfdir}/skel/.kde/share/services/mms.protocol /root/.kde/share/services/mms.protocol
install -D -m 644 %{_sysconfdir}/skel/.kde/share/services/rtsp.protocol /root/.kde/share/services/rtsp.protocol
for D in `cat /etc/passwd | grep ':/home/' | cut -f 6 -d:`; do
if [ -d $D ];then
install -D -m 644 %{_sysconfdir}/skel/.kde/share/services/mms.protocol $D/.kde/share/services/mms.protocol
install -D -m 644 %{_sysconfdir}/skel/.kde/share/services/rtsp.protocol $D/.kde/share/services/rtsp.protocol
USRHOME=`ls -la $D | grep "[^\.\.]\.$"`
OWNER=`echo $USRHOME | cut -f 3 -d\ `
GROUP=`echo $USRHOME | cut -f 4 -d\ `
chown -hR ${OWNER}:${GROUP} $D/.kde/share/services/mms.protocol
chown -hR ${OWNER}:${GROUP} $D/.kde/share/services/rtsp.protocol
fi
done
echo "Rescaning the browsers' plugins..."
nspluginscan > /dev/null 2>&1 && \
echo "Done."

%postun
read -p "kaffeine 已成功卸载，是否同时解除 kaffeine 与 mms 和 rtsp 流媒体协议的关联(默认不解除)[y/n]?" -t 60 ANSWER
if [ "$ANSWER"="y" -o "$ANSWER"="Y" ]; then
rm -f /root/.kde/share/services/mms.protocol
rm -f /root/.kde/share/services/rtsp.protocol
for D in `cat /etc/passwd | grep ':/home/' | cut -f 6 -d:`; do
if [ -d $D ];then
rm -f $D/.kde/share/services/mms.protocol
rm -f $D/.kde/share/services/rtsp.protocol
fi
done
fi
if [ "$1" = "0" ] ; then
echo "Rescaning the browsers' plugins..."
nspluginscan > /dev/null 2>&1 && \
echo "Done."
fi

%files
%defattr(-,root,root)
%{_sysconfdir}
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/kaffeine
%{_libdir}/browser-plugins/*
%{_libdir}/trinity/libkaffeine*
%{_libdir}/trinity/libxinepart.*
%{_libdir}/lib*.so.*
%{_libdir}/libkaffeinepart.so
%{_datadir}/apps/konqueror/servicemenus/kaffeine*.desktop
%{_datadir}/apps/profiles/kaffeine.profile.xml
%{_datadir}/apps/kaffeine/*
%{_datadir}/mimelnk/application/*.desktop
%{_datadir}/applications/kde/kaffeine.desktop
%doc %{_datadir}/doc/HTML/*/kaffeine
%{_datadir}/icons/*/*/*/*.png
%{_datadir}/locale/
%{_datadir}/services/*.desktop
%exclude %{_datadir}/services/gstreamer_part.desktop
%{_datadir}/servicetypes/*
# 以下文件与 kdelibs 中文件产生冲突
%exclude %{_datadir}/mimelnk/application/x-mplayer2.desktop

%files devel
%defattr(-,root,root,-)
%{_includedir}/kaffeine/
%{_libdir}/lib*.so
%exclude %{_libdir}/libkaffeinepart.so

%if 0%{gstreamer}
%files gstreamer
%defattr(-,root,root,-)
%{_libdir}/trinity/libgstreamerpart.*
%{_datadir}/apps/gstreamerpart/*
%{_datadir}/services/gstreamer_part.desktop
%endif

%changelog
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
