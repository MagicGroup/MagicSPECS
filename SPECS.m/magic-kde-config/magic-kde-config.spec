Summary: K Desktop Environment - Configuration files
Summary(zh_CN.UTF-8): K 桌面环境(KDE) - 配置文件
Name: magic-kde-config
Version: 3.5.x.20081025
Release: 3%{?dist}
License: GPL
URL: http://www.magiclinux.org
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Source0: magic-kde-config-%{version}.tar.bz2
Source1: kdm-np.pamd
Source2: kdm.pamd
Requires: kdelibs >= 3.5.8, kdebase-core >= 3.5.8, magic-system-config, magic-artwork >= 2.1.20071002
#Requires: konversation

%description
Configuration filess for KDE by MagicLinux.

%description -l zh_CN.UTF-8
MagicLinux 下 KDE 的配置文件。

%package -n magic-kdm-config
Summary: K Desktop Environment - KDM Configuration files
Summary(zh_CN.UTF-8): K 桌面环境(KDE) - 登录管理器 (KDM) 配置文件
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: kdebase-kdm >= 3.5.10
Requires: %{name} = %{version}-%{release}

%description
Configuration filess for KDM by MagicLinux.

%description -n magic-kdm-config -l zh_CN.UTF-8
MagicLinux 下 KDM 的配置文件。


%prep
%setup -q

%Build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

# install config files
cp -rf etc usr %{buildroot}/


pushd %{buildroot}
find etc/skel/ -type f | xargs chmod 0644
find etc/skel/ -type d | xargs chmod 0755
find usr/share/config -type f | xargs chmod 0644
popd

# install config files to root
mkdir -p %{buildroot}/root
chmod 750 %{buildroot}/root
cp -af %{buildroot}/etc/skel/* %{buildroot}/root/
cp -af %{buildroot}/etc/skel/.kderc %{buildroot}/root/
cp -raf %{buildroot}/etc/skel/.kde %{buildroot}/root/

#install kdm config files
mkdir -p %{buildroot}/usr/share/config/
ln -sf /etc/kde/kdm %{buildroot}/usr/share/config/
pushd %{buildroot}/etc/kde/kdm
for i in GiveConsole kdmrc TakeConsole Xaccess xdm-config Xreset Xresources Xservers Xsession Xsetup Xsetup_0 Xstartup Xwilling; do
	ln -sf /etc/X11/xdm/$i ;
done
popd

mkdir -p $RPM_BUILD_ROOT/etc/pam.d
install -p -m644 -D %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/kdm-np
install -p -m644 -D %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/kdm

rm -f %{buildroot}/usr/share/apps/konqsidebartng/virtual_folders/services/lisa.desktop
magic_rpm_clean.sh

%post
## Enable "Start New Session" magic
grep "^:1" /etc/X11/xdm/Xservers >& /dev/null ||
echo ":1 local reserve /usr/X11R6/bin/X :1 -dpi 96" >> /etc/X11/xdm/Xservers
## make kdm and KDE sessions the default, if not otherwise specified
grep "^DESKTOP=" /etc/sysconfig/desktop >& /dev/null ||
echo "DESKTOP=KDE" >> /etc/sysconfig/desktop
grep "^DISPLAYMANAGER=" /etc/sysconfig/desktop >& /dev/null ||
echo "DISPLAYMANAGER=KDE" >> /etc/sysconfig/desktop


%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
/etc/skel/.kde/share/apps/konqueror/bookmarks.xml
/etc/skel/.kde/share/config/*
/etc/skel/.kderc
/etc/skel/Desktop/*.desktop
/root/.kde/share/apps/konqueror/bookmarks.xml
/root/.kde/share/config/*
/root/.kderc
/root/Desktop/*.desktop
%{_bindir}/*
/usr/env/startkmix.sh
%{_datadir}/applnk/autostart/*
%{_datadir}/applnk/autostart/.directory
%{_datadir}/apps/kdisplay/color-schemes/*.kcsrc
%{_datadir}/apps/konqsidebartng/entries/*.desktop
%{_datadir}/apps/konqueror/profiles/*
%{_datadir}/apps/konqueror/servicemenus/*.desktop
%{_datadir}/config/gtkrc
%{_datadir}/config/kcminputrc
%{_datadir}/config/kdeglobals
%{_datadir}/config/kdesktoprc
%{_datadir}/config/kickerrc
%{_datadir}/config/konqiconviewrc
%{_datadir}/config/konquerorrc
%{_datadir}/config/konversationrc
%{_datadir}/config/ksplashrc
%{_datadir}/config/kwindeKoratorrc
%{_datadir}/config/kwinrc
%{_datadir}/config/kwriterc
%{_datadir}/config/konsolerc
%{_datadir}/config/ksmserverrc
%{_datadir}/mimelnk/application/x-nrg.desktop
%{_datadir}/pixmaps/portable-storage-devices.png
%{_datadir}/pixmaps/static-storage-devices.png
%{_datadir}/services/searchproviders/*.desktop

%files -n magic-kdm-config
%defattr(-,root,root)
/etc/pam.d/kdm
/etc/pam.d/kdm-np
/etc/X11/xdm/kdmrc
%dir /etc/kde/kdm
/etc/kde/kdm/*
%_datadir/config/kdm

%changelog
* Mon Mar 16 2009 Liu Di <liudidi@gmail.com> - 3.5.x.20081025-2
- 把 kdm 配置文件单独拆包。

* Sun Nov 9 2008 Ni Hui <shuizhuyuanluo@126.com> - 3.5.x.20081025-0.2mgc
- install kdm config files
- 戊子  十月十二

* Sat Oct 25 2008 Ni Hui <shuizhuyuanluo@126.com> - 3.5.x.20081025-0.1mgc
- 添加 konversation 配置文件(konversation 包中去除)，弱化 konversation 依赖关系
- 添加 konqueror 百度搜索和淘宝网搜索
- 修正 konqueror 书签之 magic linux 臭虫汇报系统的地址
- 戊子  九月廿七

* Tue Jul 29 2008 Liu Di <liudidi@gmail.com> - 3.5.x.20080729-1mgc
- 添加 kcminputrc 以解决小键盘灯反的问题

* Sun Oct 21 2007 kde <athena_star {at} 163 {dot} com> - 3.5.x.20071021-1mgc
- modify the kickerrc
- add minipager_panelappletrc

* Tue Oct 2 2007 kde <athena_star {at} 163 {dot} com> - 3.5.7.20071002-1mgc
- move kicker pics, kdm themes and ksplash themes to magic-artwork package
- update the bookmarks.xml
- brand-new interface

* Sun Sep 16 2007 kde <athena_star {at} 163 {dot} com> - 3.5-12mgc
- add some service menus
- add KDE 4 splash theme

* Mon Apr 23 2007 kde <athena_star {at} 163 {dot} com> 3.5-11mgc
- add autostart config menu
- split the storage.desktop file into portable-storage.desktop and static-storage.desktop

* Fri Feb 23 2007 Liu Di <liudidi@gmail.com> - 3.5-9mgc
- change konsole fonts to DejaVu Sans Mono

* Tue Feb 20 2007 Liu Di <liudidi@gmail.com> - 3.5-8mgc
- change default fonts to wenquanyi

* Fri Feb 09 2007 Liu Di <liudidi@gmail.com> - 3.5-7mgc
- add listFiles servicemenu

* Tue Feb 07 2007 Liu Di <liudidi@gmail.coM> - 3.5-6mgc
- remove mountiso

* Wed Nov 15 2006 Liu Di <liudidi@gmail.com> - 3.5-3mgc
- rebuild for kde 3.5.5

* Sun Jun 25 2006 kde <jack@linux.net.cn> -3.5-2mgc
- remove /usr/share/icons/hicolor/index.theme because it conflict with the file from hicolor-icon-theme package from opendesktop.org

* Sun May 28 2006 KanKer <kanker@163.com> -3.5-1mgc
- update kdeglobals

* Sun Mar 19 2006 KanKer <kanker@163.com> -3.4-15mgc
- update startmix.sh
* Thu Jan 17 2006 KanKer <kanker@163.com>
- set kconsole font to Dejavu

* Sun Jan 15 2006 KanKer <kanker@163.com>
- update spec scripts

* Tue Dec 29 2005 KanKer <kanker@163.com>
- set default timezone to Asia/Shanghai
* Tue Dec 22 2005 KanKer <kanker@163.com>
- fix java path bug
* Mon Dec 19 2005 KanKer <kanker@163.com>
- add two link to Desktop
* Tue Dec 8 2005 KanKer <kanker@163.com>
- add root config files
* Fri Dec 2 2005 KanKer <kanker@163.com>
- set fix font to mono
* Wed Nov 30 2005 KanKer <kanker@163.com>
- update config files
- move wallpapers to Magic-artwork
* Tue Nov 24 2005 KanKer <kanker@163.com>
- set arts server to use autocheck and support fullduplex
* Mon Oct 31 2005 KanKer <kanker@163.com>
- change some themes
* Fri Oct 28 2005 KanKer <kanker@163.com>
- add some themes
* Sun Oct 8 2005 KanKer <kanker@163.com>
- add kicker icons for MagicLinux
* Thu Aug 30 2005 KanKer <kanker@163.com>
- set konqueror to tab mode as default
* Thu Aug 4 2005 KanKer <kanker@163.com>
- rename 3.4.x
* Mon Jul 25 2005 KanKer <kanker@163.com>
- update kdeglobals and konqueror's webbrower profile
* Sat Jun 4 2005 KanKer <kanker@163.com>
- update wallpapers
* Mon May 23 2005 KanKer <kanker@163.com>
- update kdesktoprc file
* Mon Mar 28 2005 KanKer <kanker@163.com>
- fix a spec bug.
* Sat Mar 26 2005 KanKer <kanker@163.com>
- add an auto-decide start kmix scripts.
* Thu Mar 22 2005 KanKer <kanker@163.com>
- fix icons lost bug.
* Sun Mar 19 2005 KanKer <kanker@163.com>
- initlize.

