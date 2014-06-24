%define git 1
%define gitdate 20120120

Name:       amarok
Summary:    Media player for KDE
Summary(zh_CN.UTF-8): KDE 的媒体播放器
Version:    1.4.14
%if %{git}
Release:    0.git%{gitdate}%{?dist}
%else
Release:    1%{?dist}
%endif
Group: 	    Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:    GPL
Url:        http://amarok.kde.org
%if %{git}
Source0:    %{name}-git%{gitdate}.tar.xz
%else
Source0:    http://puzzle.dl.sourceforge.net/sourceforge/amarok/%{name}-%{version}.tar.bz2
%endif
Source1:    make_amarok_git_package.sh
Patch0:     amarok-1.4beta1-gst10.patch
Patch1:     amarok-1.4-gstreamer.patch
Patch2:     amarok-1.4-engines-cfg.patch
Patch3:	    amarok-1.4-beta1-fix-gcc4-compile.patch
Patch4:     amarok-1.4-beta1-fix-gcc4-compile2.patch
Patch5:     amarok-cjk.patch
Patch6:	    amarok-1.4.7-taglocal.patch

# patch 7 rewritten by nihui, Jul.5th, 2008
Patch7:     amarok-1.4.9.1-taglocal_fix_flac.patch

Patch8:	    amarok-1.4.10-gcc44.patch
# 修正 bug 135598
Patch50: fix-amarok-135598.diff
# 修正在 mtp 0.3.1 上不能编译的问题
Patch51: amarok-1.4.10-mtp.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

BuildRequires:  tdemultimedia-devel >= 3.2
BuildRequires:  taglib-devel >= 1.3, esound-devel
BuildRequires:  desktop-file-utils, gettext
BuildRequires:  libGL
BuildRequires:  libmusicbrainz-devel 
#BuildRequires:	xmms-devel >= 1.2
BuildRequires:  libvisual-devel >= 0.2.0, SDL-devel, gtk+-devel
BuildRequires:  libtool-ltdl-devel
#BuildRequires:  mysql-devel, postgresql-devel
BuildRequires:  libtunepimp-devel >= 0.4.0
BuildRequires:  kdebase-devel
BuildRequires:  ruby
BuildRequires:  alsa-lib-devel
BuildRequires:  libacl-devel
#BuildRequires:  akode-devel
BuildRequires:  libifp-devel, libusb-devel
BuildRequires:  libgpod-devel >= 0.5.2
%ifnarch ppc64 x86_64 s390 s390x ia64
#BuildRequires:  HelixPlayer
%endif

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

Obsoletes: amarok-arts < 1.3, amarok-akode < 1.3
Provides:  amarok-devel = %{version}-%{release}
Provides:  amarok-visualisation = %{version}-%{release}

%description
Amarok is a KDE multimedia player with:
 - fresh playlist concept, very fast to use, with drag and drop
 - plays all formats supported by the various engines
 - audio effects, like reverb and compressor
 - compatible with the .m3u and .pls formats for playlists
 - nice GUI, integrates into the KDE look, but with a unique touch

Amarok can use various engines to decode sound : gstreamer, arts,
helix and xine (disabled by default for patent reasons)
To use the helix engine, you'll have to install either HelixPlayer
or RealPlayer

Amarok can use visualisation plugins from different origins.
Right now, only xmms is supported, which means that you can
use any of xmms' visualisation plugins with Amarok.

%description -l zh_CN.UTF-8
Amarok 是 KDE 的多媒体播放器，它可以：
 - 更新的播放列表观念，使用拖放，非常容易上手
 - 播放多种引擎支持的所有格式
 - 声音效果，比如混响和压缩
 - 兼容 .m3u 和 .pls 格式的播放列表
 - 漂亮的界面，集成到 KDE 的观感，但有独特的感觉

Amarok 可以使用以下的多种引擎来解码声音：gstreamer, arts,
helix 和 xine(因为专利的原因默认是禁用的)。MagicLinux 使用
的是 xine 引擎。要使用 helix 引擎，您必须安装 HelixPlayer 或
RealPlayer。

Amarok 可以使用不同来源的可视化插件。现在，只支持 xmms，
意思就是您可以在 Amarok 里使用任何 xmms 的可视化插件。


%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q -n %{name}-%{version}
%endif
# Make Gstreamer a sufficient engine as well (only engine available on x86_64)
# %patch1 -p1 -b .gstreamer
# Gstreamer default sink should be autoaudiosink
# %patch2 -p1 -b .engines-cfg
# Patch for CJK, only on non-utf8
# patch for gcc
# %patch3 -p1
# %patch4 -p1
#%patch5 -p1
#%patch6 -p1
#%patch7 -p1 -b .local_fix_flac

%patch8 -p1

%patch50 -p1
#%patch51 -p1

%build
unset QTDIR && . %{_sysconfdir}/profile.d/qt.sh
# work around an improper ${kdelibsuff}
export QTLIB=${QTDIR}/lib QTINC=${QTDIR}/include
mkdir build
cd build
%cmake 	-DWITH_LIBVISUAL=ON \
	-DWITH_KONQSIDEBAR=ON \
	-DWITH_XINE=ON \
	-DWITH_YAUAP=ON \
	-DWITH_IPOD=ON \
	-DWITH_IFP=ON \
	-DWITH_NJB=ON \
	-DWITH_MTP=ON \
	-DWITH_RIOKARMA=OFF \
	-DWITH_DAAP=ON \
	-DBUILD_ALL=ON ..

# smp 会导致编译失败
make


%install
rm -fr %{buildroot}
cd build
make install DESTDIR=%{buildroot} 

# desktop files
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/apps/konqueror/servicemenus

desktop-file-install  --vendor "" \
        --dir %{buildroot}%{_datadir}/applications/kde \
        --delete-original \
        --add-category Application \
        %{buildroot}%{_datadir}/applications/kde/%{name}.desktop

#rm -f %{buildroot}%{_datadir}/applications/kde/amarokapp.desktop
# Amarok crashes without the *.la files !
#find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
# Remove the *.la file in /usr/lib though, those are OK to delete
rm -f %{buildroot}%{_libdir}/*.la

/usr/bin/magic_rpm_clean.sh || :

%find_lang %{name}
# HTML
for lang_dir in %{buildroot}%{_docdir}/HTML/* ; do
  lang=$(basename $lang_dir)
  [ "$lang" == "en" ] && d=en/%{name} || d=$lang
  echo "%lang($lang) %doc %{_docdir}/HTML/$d" >> %{name}.lang
done

%post
# update icon themes if necessary
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
update-desktop-database &> /dev/null ||:
ldconfig

%postun
# update icon themes if necessary
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
update-desktop-database &> /dev/null ||:
ldconfig


%clean
rm -fr %{buildroot} %{_builddir}/%{buildsubdir}


%files 
%defattr(-,root,root)
%{_prefix}
%exclude %{_prefix}/*/debug*
%exclude %{_prefix}/src
%exclude %{_datadir}/apps/%{name}/images/xine_logo.png
# Helix engine
#%ifnarch ppc64 x86_64 s390 s390x ia64
#%{_libdir}/kde3/libamarok_helixengine_plugin.*
#%{_datadir}/services/amarok_helixengine_plugin.desktop
#%endif




%changelog
* Fri Jan 16 2009 Liu Di <liudidi@gmail.com> - 1.4.10-1
- 在 glibc 2.9.90 上重新编译

* Thu Sep 18 2008 Liu Di <liudidi@gmail.com> - 1.4.10-0.2mgc
- 在 mtp 0.3.1 上重新编译

* Fri Aug 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.4.10-0.1mgc
- 更新至 1.4.10
- 修正 konqueror 侧边栏部件中同时开两个 amarok 造成假死的问题(kde bug 135598)
- 戊子  七月廿九

* Thu Jul 10 2008 Liu Di <liudidi@gmail.com> - 1.4.9.1-0.4mgc
- 重建以去除 gnome 依赖

* Sat Jul 5 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.4.9.1-0.3mgc
- 更新编码补丁(patch 7)，修正 flac 文件 utf8 默认编码处理
- 戊子  六月初三

* Tue Apr 15 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.4.9.1-0.1mgc
- 更新至 1.4.9.1
- 本版本修正了 amazon.com 封面获取API调整的问题
- 戊子  三月初十

* Fri Aug 24 2007 Liu Di <liudidi@gmail.com> - 1.4.7-1mgc
- update to 1.4.7

* Thu Aug 23 2007 Ni Hui <shuizhuyuanluo@126.com> -1.4.6-1.1mgc
- modify the cjk patch

* Thu Jun 28 2007 kde <athena_star {at} 163 {dot} com> - 1.4.6-1mgc
- update to 1.4.6
- simplify the spec file

* Thu Mar 15 2007 Liu Di <liudidi@gmail.com> - 1.4.5-1mgc
- update to 1.4.5

* Sat Nov 04 2006 Liu Di <liudidi@gmail.com> - 1.4.4-1mgc
- update to 1.4.4

* Fri Sep 15 2006 Liu Di <liudidi@gmail.com> - 1.4.3-1mgc
- update to 1.4.3

* Thu Jul  1 2006 Liu Di <liudidi@gmail.com> 1.4.0a-1mgc
- update to 1.4.0a

* Fri Apr 14 2006 Aurelien Bompard <gauret[AT]free.fr> 1.4-0.12.beta3
- add patch to make Gstreamer sufficient to build (only engine available
  on x86_64

* Sun Apr 09 2006 Aurelien Bompard <gauret[AT]free.fr> 1.4-0.11.beta3
- drop the non-free bits
- beta 3 (akode has been disabled)

* Wed Mar 22 2006 Aurelien Bompard <gauret[AT]free.fr> 1.4-0.10.beta2
- enable libgpod support

* Wed Mar 22 2006 Aurelien Bompard <gauret[AT]free.fr> 1.4-0.9.beta2
- make amarok build even with gstreamer only

* Sun Mar 05 2006 Aurelien Bompard <gauret[AT]free.fr> 1.4-0.8.beta2
- version 1.4 beta2

* Wed Feb 22 2006 Aurelien Bompard <gauret[AT]free.fr> 1.4-0.7.beta1
- disable build of Helix engine on x86_64

* Wed Feb 22 2006 Aurelien Bompard <gauret[AT]free.fr> 1.4-0.6.beta1
- remove requirement on HelixPlayer for x86_64, amarok include the headers

* Wed Feb 22 2006 Aurelien Bompard <gauret[AT]free.fr> 1.4-0.5.beta1
- build Helix engine on x86_64

* Wed Feb 22 2006 Aurelien Bompard <gauret[AT]free.fr> 1.4-0.4.beta1
- fix gstramer 0.10 detection again

* Mon Feb 20 2006 Aurelien Bompard <gauret[AT]free.fr> 1.4-0.3.beta1
- fix gstreamer 0.10 detection

* Fri Feb 17 2006 Aurelien Bompard <gauret[AT]free.fr> 1.4-0.1.beta1
- fix gstreamer dependency

* Wed Feb 15 2006 Aurelien Bompard <gauret[AT]free.fr> 1.4-0.1.beta1
- version 1.4-beta1

* Sun Feb 12 2006 Aurelien Bompard <gauret[AT]free.fr> 1.3.8-2
- fix BR for gstreamer < 0.10

* Sat Jan 21 2006 Aurelien Bompard <gauret[AT]free.fr> 1.3.8-1
- version 1.3.8

* Wed Dec 07 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3.7-1
- version 1.3.7

* Sun Nov 20 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3.6-2
- build with libtunepimp
- add patch to use libtunepimp 0.4.0 (api changed)

* Tue Nov 08 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3.6-1
- version 1.3.6
- BR libGL instead of xorg-x11-Mesa-libGL to prepare for X11R7

* Tue Oct 25 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3.5-1
- version 1.3.5

* Mon Oct 24 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3.4-1
- version 1.3.4
- add mysql and postgresql support
- update desktop database
- add %%doc files

* Thu Oct 13 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3.3-1
- version 1.3.3
- drop endian patch

* Wed Sep 21 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3.2-1
- version 1.3.2
- remove patch 4 (applied upstream)

* Sat Sep 10 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3.1-2
- add patch from upstream to fix alsasink in gstreamer
- default to autoaudiosink for gstreamer

* Mon Sep 05 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3.1-1
- version 1.3.1

* Tue Aug 23 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3-6
- add version to obsoletes

* Tue Aug 23 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3-5
- add missing Obsoletes.

* Mon Aug 22 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3-4
- fix endian declaration on ppc

* Mon Aug 22 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3-3
- dont build the Helix engine on arches where HelixPlayer is not built

* Mon Aug 22 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3-2
- disable the akode engine (disabled upstream, see Changelog)
- merge in the Helix engine, since it does not have special Requires.
  HelixPlayer or RealPlayer need to be installed manually (either one)
- updated description

* Mon Aug 22 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3-1
- update to version 1.3
- add Michel Salim's improvements:
  - call gtk-update-icon-cache to (de-)register icons
  - new output plugin subpackage: helix
  - patched gst and helix plugins' default settings

* Fri Jul 01 2005 Aurelien Bompard <gauret[AT]free.fr> 1.2.4-6
- remove -arts subpackage, it is useless

* Thu Jun  2 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.4-6.fc5
- remove temporary work-around from 1.2.4-2.fc4
- add patch to fix several missing forward declarations which let
  compilation with gcc >= 4.0.0-9 fail
- re-enable SMP make flags

* Thu Jun  2 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.4-5.fc4
- disable SMP make flags, since previous release failed miserably on
  i386 while the one before it succeeded

* Thu Jun  2 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.4-4.fc4
- set QTLIB and QTINC, so configure script does not search for Qt in
  QTDIR/lib64 on 64-bit multilib platforms

* Thu Jun  2 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.4-3.fc4
- try to fix build problems (#158654): always set QTDIR, always
  buildrequire libtool-ltdl-devel, disable %%fedora conditional BR

* Thu Jun  2 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.4-2.fc4
- temporarily add patch to work around Fedora Core bug 159090

* Mon May 23 2005 Aurelien Bompard <gauret[AT]free.fr> 1.2.4-1
- version 1.2.4
- use dist tag
- conditional builds for fc3 and fc4

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.2.3-2.fc4
- rebuild on all arches

* Tue Mar 29 2005 Aurelien Bompard <gauret[AT]free.fr> 1.2.3-1.fc4
- version 1.2.3
- add libtool to BuildRequirements
- change release tag for FC4
- add a subpackage for aKode engine

* Mon Mar 14 2005 Aurelien Bompard <gauret[AT]free.fr> 1.2.2-1
- version 1.2.2

* Sat Mar 05 2005 Aurelien Bompard <gauret[AT]free.fr> 1.2.1-1
- version 1.2.1 (bugfixes)

* Mon Feb 14 2005 Aurelien Bompard <gauret[AT]free.fr> 1.2-2
- show in the GNOME menus too

* Sun Feb 13 2005 Aurelien Bompard <gauret[AT]free.fr> 1.2-1
- version 1.2 final
- drop --disable-rpath, won't build with it.
- drop epoch

* Thu Feb 10 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.2-0.2.beta4
- version 1.2 beta 4

* Sat Nov 27 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.2-0.fdr.0.1.beta1
- version 1.2beta 1
- minor cleanups
- don't ship the desktop files, split the provided one instead

* Sun Oct 24 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1.1-0.fdr.2
- clean-up buildrequires
- fix --with xine switch
- make a -visualisation subpackage for visualisation plugins
- make a -arts subpackage to lower dependencies

* Wed Oct 20 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1.1-0.fdr.1
- version 1.1.1

* Mon Sep 27 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1.0-0.fdr.2
- improve buildrequires

* Sun Sep 26 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1.0-0.fdr.1
- version 1.1 final

* Tue Sep 14 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1.0-0.fdr.0.1.beta2
- version 1.1 beta2

* Thu Aug 05 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.2-0.fdr.1
- version 1.0.2
- added new xine engine

* Tue Jul 13 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.1-0.fdr.3
- remove BR: libselinux-devel: RH fixed the bug

* Wed Jun 30 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.1-0.fdr.2
- add Requires: xorg-x11-devel because of a qt packaging bug

* Tue Jun 29 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.1-0.fdr.1
- version 1.0.1 (bugfixes)

* Mon Jun 21 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0-0.fdr.3
- remove BR: xine-lib-devel
- add BR: xorg-x11-Mesa-libGL and libselinux-devel

* Thu Jun 17 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0-0.fdr.2
- add translations

* Thu Jun 17 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0-0.fdr.1
- version 1.0 final

* Tue Jun 01 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0-0.fdr.0.1.beta4
- update to beta4

* Sun May 09 2004 Aurelien Bompard <gauret[AT]free.fr> 1.0-0.fdr.0.1.beta3
- version 1.0-beta3

* Fri Apr 23 2004 Aurelien Bompard <gauret[AT]free.fr> 1.0-0.fdr.0.1.beta2
- version 1.0-beta2
- use desktop-file-install
- remove .la files
- remove --enable-final (won't build with it)

* Thu Apr 15 2004 Aurelien Bompard <gauret[AT]free.fr> 1.0-0.fdr.0.1.beta1
- version 1.0-beta1
- reduce BuildRequires : arts-devel already requires arts, libvorbis-devel
  and audiofile-devel

* Mon Mar 08 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.9-0.fdr.1
- version 0.9

* Wed Feb 11 2004 Aurelien Bompard <gauret[AT]free.fr> 0.8.3-0.fdr.1
- initial package
