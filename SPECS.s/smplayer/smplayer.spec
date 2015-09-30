%define _qt4_qmake qmake-qt4
%define _qt4_lrelease lrelease-qt4

%define realname smplayer

%define _prefix %{kde4_prefix}
%define themes_ver 15.6.0
%define skins_ver 15.2.0

Name:           smplayer
Version:	14.9.0.6994
Release:	4%{?dist}
Summary:        A graphical frontend for mplayer
Summary(zh_CN.UTF-8):	mplayer 的图形化前端

Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
License:        GPLv2+
URL:            http://smplayer.sourceforge.net/linux/
Source0:        http://downloads.sourceforge.net/sourceforge/smplayer/smplayer-%{version}.tar.bz2
Source1:	http://downloads.sourceforge.net/smplayer/smplayer-themes-%{themes_ver}.tar.bz2
Source2:	http://downloads.sourceforge.net/smplayer/smplayer-skins-%{skins_ver}.tar.bz2
# Add a servicemenu to enqeue files in smplayer's playlist. 
# The first one is for KDE4, the second one for KDE3.
# see also: 
# https://sourceforge.net/tracker/?func=detail&atid=913576&aid=2052905&group_id=185512
Source3:        smplayer_enqueue_kde4.desktop
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# 用以创建 svn 代码 tar 包的脚本,此处仅作备份用。
Source4:        create_tar.sh
BuildRequires:  desktop-file-utils
BuildRequires:  qt4-devel
# smplayer without mplayer is quite useless
Requires:       mplayer

%description
smplayer intends to be a complete front-end for Mplayer, from basic features
like playing videos, DVDs, and VCDs to more advanced features like support
for Mplayer filters and more. One of the main features is the ability to
remember the state of a played file, so when you play it later it will resume
at the same point and with the same settings. smplayer is developed with
the Qt toolkit, so it's multi-platform.

%description -l zh_CN.UTF-8
SMPlayer 意在成为 MPlayer 的完整前端，从基本的特性，比如播放视频，
DVD，和 VCD 到更多高级特性，像对 MPlayer 过滤器的支持还有更多。
一个主要特性是可以记忆播放文件的位置，这样您就可以以相同的设置
重新在同一位置恢复播放。smplayer 是用 Qt 工具开发的，所以它也是
跨平台的。

%prep
%setup -qn %{realname}-%{version} -a1 -a2

# correction for wrong-file-end-of-line-encoding
%{__sed} -i 's/\r//' *.txt
# fix files which are not UTF-8 
iconv -f Latin1 -t UTF-8 -o Changelog.utf8 Changelog 
mv Changelog.utf8 Changelog

# use lrelease from qt4-devel
sed -i 's|LRELEASE=lrelease|LRELEASE=%{_qt4_lrelease}|' Makefile

sed -i 's|QMAKE=qmake|QMAKE=%{_qt4_qmake}|' Makefile

# fix path of docs
sed -i 's|DOC_PATH=$(PREFIX)/share/doc/packages/smplayer|DOC_PATH=$(PREFIX)/share/doc/smplayer-%{version}|' Makefile

# use %{?_smp_mflags}
sed -i '/cd src && $(QMAKE) $(QMAKE_OPTS) && $(DEFS) make/s!$! %{?_smp_mflags}!' Makefile

# don't show smplayer_enqueue.desktop in KDE and use servicemenus instead
echo "NotShowIn=KDE;" >> smplayer_enqueue.desktop

%build
make QMAKE=%{_qt4_qmake} PREFIX=%{_prefix}

#themes
pushd smplayer-themes-%{themes_ver}
make QMAKE=%{_qt4_qmake} PREFIX=%{_prefix}
popd

#skins
pushd smplayer-skins-%{skins_ver}
make QMAKE=%{_qt4_qmake} PREFIX=%{_prefix}
popd


%install
rm -rf %{buildroot}
make QMAKE=%{_qt4_qmake} PREFIX=%{_prefix} DESTDIR=%{buildroot}/ install

#themes
pushd smplayer-themes-%{themes_ver}
make QMAKE=%{_qt4_qmake} PREFIX=%{_prefix} DESTDIR=%{buildroot}/ install
popd

#skins
pushd smplayer-skins-%{skins_ver}
make QMAKE=%{_qt4_qmake} PREFIX=%{_prefix} DESTDIR=%{buildroot}/ install
popd


desktop-file-install --delete-original                   \
        --vendor "magic"                             \
        --dir %{buildroot}%{_datadir}/applications/      \
        %{buildroot}%{_datadir}/applications/%{realname}.desktop


desktop-file-install --delete-original                   \
        --vendor "magic"                             \
        --dir %{buildroot}%{_datadir}/applications/      \
        %{buildroot}%{_datadir}/applications/%{realname}_enqueue.desktop

# Add servicemenus dependend on the version of KDE:
# https://sourceforge.net/tracker/index.php?func=detail&aid=2052905&group_id=185512&atid=913576
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_datadir}/kde4/services/ServiceMenus/smplayer_enqueue.desktop

# 删除非中文化文件
rm -rf `ls %{buildroot}%{_prefix}/share/doc/smplayer-%{version}/*|egrep -v zh_CN`
rm -rf `ls %{buildroot}%{_prefix}/share/smplayer/translations/smplayer_ar_SY.qm|egrep -v zh_`

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
update-desktop-database &> /dev/null || :

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
update-desktop-database &> /dev/null || :

%files
%defattr(-,root,root,-)
%dir %{_docdir}/smplayer-%{version}
%{_docdir}/smplayer-%{version}/*
%{_bindir}/smplayer
%{_datadir}/applications/magic-smplayer*.desktop
%{_datadir}/icons/hicolor/*/apps/smplayer.*
%{_datadir}/smplayer/
%{_mandir}/man1/smplayer.1.gz
%{_datadir}/kde4/services/ServiceMenus/smplayer_enqueue.desktop

%changelog
* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 14.9.0.6994-4
- 为 Magic 3.0 重建

* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 14.9.0.6994-3
- 为 Magic 3.0 重建

* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 14.9.0.6994-2
- 为 Magic 3.0 重建

* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 14.9.0.6994-1
- 更新到 14.9.0.6994

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.7.0-2
- 为 Magic 3.0 重建

* Sun May 30 2010 Liu Songhe <athena_star {at} 163 {dot} com> - 0.6.9_svn_r3541-0.1%{?dist}
- 更新至 0.6.9_svn_r3541

* Wed Dec 9 2009 Liu Songhe <athena_star {at} 163 {dot} com> - 0.6.8.svn.r3338-0.1%{?dist}
- 更新至 0.6.8.svn.r3338

* Wed Aug 12 2009 Ni Hui <shuizhuyuanluo@126.com> - 0.6.8-1mgc
- 更新至 0.6.8
- 删除非中文化文件
- 己丑  六月廿二
