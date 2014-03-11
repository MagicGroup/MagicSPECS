%define version 1.1
%define release 1%{?dist}

Name: konversation
Summary: Konversation is a user friendly IRC client for KDE
Summary(zh_CN.UTF-8): Konversation 是一款 KDE 下用户友好 IRC 客户端
Version: %{version}
Release: %{release}
License: GPL
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
URL: http://konversation.kde.org
Source0: http://download.berlios.de/konversation/%{name}-%{version}.tar.bz2
Source1: konversation.po
Source2: konversation.desktop
Patch1:	konversation-1.1-admin.patch
#Source10: konversationrc
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: kdebase-devel  >= 3.4, desktop-file-utils, gettext
BuildRequires: magic-rpm-config
Requires: kdebase >= 3.4
Prefix: %{_prefix}

%description
A simple and easy to use IRC client for KDE with support for
strikeout; multi-channel joins; away / unaway messages;
ignore list functionality; (experimental) support for foreign
language characters; auto-connect to server; optional timestamps
to chat windows; configurable background colors and much more

%description -l zh_CN.UTF-8
一款 KDE 下的简单好用的 IRC 客户端，支持多频道加入、离开/在线消息、忽略列表功能、多国
语言字符(实验中)、自动连接至服务器、聊天窗口时间戳、可配置的背景颜色以及更多功能

%prep
%setup
%patch1 -p1
chmod 777 admin/*

%build
make -f admin/Makefile.common
%configure
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-lX11 \-lDCOP \-lkio/g' konversation/src/Makefile
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

/usr/bin/magic_rpm_clean.sh

# Replace absolute symlinks with relative ones
# 主要是一些帮助文件的 common 符号链接替换
#pushd %{buildroot}%{_docdir}/HTML
#for lang in *; do
#  if [ -d $lang ]; then
#    pushd $lang
#    for i in */*; do
#      [ -d $i -a -L $i/common ] && rm -f $i/common && ln -sf ../../en/common $i/common
#    done
#    popd
#  fi
#done
#popd

install -d -m 755 %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/
msgfmt %{SOURCE1} -o %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/%{name}.mo

install -D -m 644 %{SOURCE2} %{buildroot}%{_datadir}/applications/kde/%{name}.desktop

# 准备初始化数据
#mkdir -p %{buildroot}/etc/skel/.kde/share/config
#mkdir -p %{buildroot}/root/.kde/share/config
# irc 服务器 & channel 地址更新地址列表
#install -m 600 %{SOURCE10} %{buildroot}/etc/skel/.kde/share/config/konversationrc
#install -m 600 %{SOURCE10} %{buildroot}/root/.kde/share/config/konversationrc


%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post
#for D in `cat /etc/passwd | grep ':/home/' | cut -f 6 -d:`; do
#if [ -d $D ];then
#  cp -auf /etc/skel/.kde/share/config/konversationrc $D/.kde/share/config/
#  USRHOME=`ls -la $D | grep "[^\.\.]\.$"`
#  OWNER=`echo $USRHOME | cut -f 3 -d\ `
#  GROUP=`echo $USRHOME | cut -f 4 -d\ `
#  chown -hR ${OWNER}:${GROUP} $D/.kde/share/config
#  chmod 600 $D/.kde/share/config/konversationrc
#fi
#done
#

%postun


%files
%defattr(-,root,root)
%doc AUTHORS COPYING COPYING-DOCS ChangeLog INSTALL README TODO VERSION
%{_bindir}/*
%{_datadir}/applications/kde/konversation.desktop
%{_datadir}/apps/kconf_update/*
%{_datadir}/apps/konversation/*
%{_datadir}/config.kcfg/konversation.kcfg
%{_datadir}/doc/HTML/en/*
%{_datadir}/icons/crystalsvg/*/actions/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/locale/*
%{_datadir}/services/*.protocol
#/etc/skel/.kde/share/config/konversationrc
#/root/.kde/share/config/konversationrc

%changelog
* Sat Oct 25 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.1-0.1mgc
- 更新至 1.1(KDE3 告别版本)
- 去除配置文件(移入 magic-kde-config 包)
- 戊子  九月廿七

* Fri Feb 22 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.0.1-3.2mgc
- 添加配置文件
- 戊子  正月十六

* Sat Nov 17 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.0.1-3.1mgc
- rebuild
- 去除多余语言文件

* Wed Aug 8 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.0.1-3mgc
- 修正 common 文件夹的链接关系
- 菜单项中文翻译

* Sat Jul 28 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.0.1-2mgc
- 改善了一点翻译
- 修改 spec 文件，重新建包

* Sun Apr 22 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.0.1-1mgc
- first port to Magiclinux 2.1
