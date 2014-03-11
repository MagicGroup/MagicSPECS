%define _qt4_qmake qmake-qt4
%define _qt4_lrelease lrelease-qt4

%define realname smplayer

%define _prefix /opt/kde4

Name:           smplayer-qt4
Version:        0.7.0
Release:        2%{?dist}
Summary:        A graphical frontend for mplayer
Summary(zh_CN.UTF-8):	mplayer 的图形化前端

Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
License:        GPLv2+
URL:            http://smplayer.sourceforge.net/linux/
Source0:        http://downloads.sourceforge.net/sourceforge/smplayer/smplayer-%{version}.tar.bz2
# Add a servicemenu to enqeue files in smplayer's playlist. 
# The first one is for KDE4, the second one for KDE3.
# see also: 
# https://sourceforge.net/tracker/?func=detail&atid=913576&aid=2052905&group_id=185512
Source1:        smplayer_enqueue_kde4.desktop
Source2:        smplayer_enqueue_kde3.desktop
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# 用以创建 svn 代码 tar 包的脚本,此处仅作备份用。
Source3:        create_tar.sh
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
%setup -qn %{realname}-%{version}

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

%install
rm -rf %{buildroot}
make QMAKE=%{_qt4_qmake} PREFIX=%{_prefix} DESTDIR=%{buildroot}/ install

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
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_datadir}/kde4/services/ServiceMenus/smplayer_enqueue.desktop

# 删除非中文化文件
rm -rf %{buildroot}/opt/kde4/share/doc/smplayer-%{version}/cs
rm -rf %{buildroot}/opt/kde4/share/doc/smplayer-%{version}/de
rm -rf %{buildroot}/opt/kde4/share/doc/smplayer-%{version}/es
rm -rf %{buildroot}/opt/kde4/share/doc/smplayer-%{version}/hu
rm -rf %{buildroot}/opt/kde4/share/doc/smplayer-%{version}/it
rm -rf %{buildroot}/opt/kde4/share/doc/smplayer-%{version}/nl
rm -rf %{buildroot}/opt/kde4/share/doc/smplayer-%{version}/ro
rm -rf %{buildroot}/opt/kde4/share/doc/smplayer-%{version}/ru
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_ar_SY.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_bg.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_ca.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_cs.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_de.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_el_GR.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_es.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_et.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_eu.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_fi.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_fr.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_gl.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_hu.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_it.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_ka.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_ku.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_mk.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_nl.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_pl.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_pt.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_pt_BR.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_pt_PT.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_ro_RO.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_ru_RU.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_sk.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_sl_SI.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_sr.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_sv.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_tr.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_uk_UA.qm
rm -rf %{buildroot}/opt/kde4/share/smplayer/translations/smplayer_vi_VN.qm

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
%dir /opt/kde4/share/doc/smplayer-%{version}
/opt/kde4/share/doc/smplayer-%{version}/*
%{_bindir}/smplayer
%{_datadir}/applications/magic-smplayer*.desktop
%{_datadir}/icons/hicolor/*/apps/smplayer.png
%{_datadir}/smplayer/
/opt/kde4/share/man/man1/smplayer.1.gz
%{_datadir}/kde4/services/ServiceMenus/smplayer_enqueue.desktop

%changelog
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
