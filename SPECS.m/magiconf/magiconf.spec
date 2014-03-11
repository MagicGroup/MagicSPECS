# Initial spec file created by autospec ver. 0.8 with rpm 3 compatibility
Summary: Magic Control Center
# Don't use chinese letters in spec file, because kpackage can not show UTF-8 letters in other code set environment
Summary(zh_CN.UTF-8): Magic 控制中心
Name: magiconf
Version: 1.0.0
Release: 4%{?dist}
Group: User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
License: GPL
Source: %{name}-2008103.tar.bz2
Patch0:	magiconf-2008103-gcc44.patch
Patch1:	magiconf-2008103-admin.patch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot
# Following are optional fields
URL: http://lovewilliam.bokee.com
Distribution: Magic Linux
BuildArch: i686
Packager: lovewilliam <lovewilliam@gmail.com>
Requires: qt-devel kdebase
Provides: Magiconf
Obsoletes: Magiconf <= 0.9.4.2
BuildRequires: qt gcc glib kdelibs-devel kdebase

%description
Magiconf is a control panel for GNU/Linux desktop environment.

%description -l zh_CN.UTF-8
Magic 控制中心

%prep
%setup -q -n %{name}-2008103
%patch0 -p1
%patch1 -p1
chmod 777 admin/*

%build
make -f admin/Makefile.common
%configure --prefix=/usr
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-lDCOP \-lkio/g' src/Makefile
make

%install
rm -rf %{BuildRoot}
mkdir -p $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/usr/share/Magiconf
install -m 664 src/BAK/moduleData.cfg $RPM_BUILD_ROOT/usr/share/Magiconf/moduleData.cfg
install -m 664 src/BAK/line1.png $RPM_BUILD_ROOT/usr/share/Magiconf/line1.png
install -m 664 src/BAK/line2.png $RPM_BUILD_ROOT/usr/share/Magiconf/line2.png

rm %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/bluetooth.png

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
rm -rf $RPM_BUILD_DIR/%{name}-%{version}


%files
%defattr(-,root,root,-)
/usr
#/etc
%exclude /usr/src
%exclude /usr/*/debug*

%changelog
* Mon Sep 15 2008 Liu Di <liudidi@gmail.com> - 1.0.0-2mgc
- 重建

* Thu Aug 21 2008 lovewilliam <lovewilliam@gmail.com>
- update to 1.0.0

* Sat Jul 29 2006 lovewilliam <lovewilliam@gmail.com>
- I went to net-Bar? &
- got kanker's mcc source code version 0.9.4.2
- port all the new feature
- here comes kanker's changelog :
-
- & Wed Feb 8 2006
- update font installer
-& Sun Jan 15 2006
- add disk partition and wireless config tool
-& Sun Jan 8 2006
- add LANG setting to xinput
-& Fri Jan 6 2006
- add system-config-display and system-config-mouse
- 0.9.4.2
-& Mon Nov 28 2005
- set adsl setup command to Magic xDSL Dialer
- add a ppp dialer command
-& Tue Nov 24 2005
- change adsl-config to adsl-setup
-& Mon Nov 21 2005
- remove grubui and mct from Magiconf
- 0.9.4.1
-& Sun Oct 8 2005
- fix autoplay load config file bug
-& Sun Sep 18 2005
- update autoplay
-KanKer <kanker@163.com>

* Fri Jul 28 2006 lovewilliam<lovewilliam@gmail.com> 0.4.9.4
 -Add tuf
 -fix some small bugs

*Sat Oct 1 2005 lovewilliam<lovewilliam@gmail.com> 0.4.9.3
- fixed translation for "filesystem"
- fix cinfo

*Sun Sep 18 2005 lovewilliam<williamlovecyl@hotmail.com> 0.4.9.2
- Add cinfo
- Add processor images
- Add about mcc
- add ProIm() to mcc.h
- destory N_() in MCC, use tr() and I18N_NOOP() instead
- 0.9.4.2

* Sun Aug 14 2005 lovewilliam<williamlovecyl@hotmail.com> 0.9.4.1
- Add kmodule supports
- fixed main.cpp
- use kapplication
- 0.9.4.1

* Wed Aug 10 2005 lovewilliam<williamlovecyl@hotmail.com> 0.9.4.0
- fixed spefile
- added mcc.cpp
- Add Magiconf Items control
- Add Screen Func.
- use Icon() fun. in .ui file
- fixed magiconf.ui.h
- 0.9.4.0

* Sat Aug 6 2005 lovewilliam<williamlovecyl@hotmail.com> 0.9.3.8-1mgc
- fixed specfile
- fixed console tool

* Mon Jul 18 2005 lovewilliam <williamlovecyl@hotmail.com> 0.9.3.6-1mgc
- Add console-tools
- modifief mcc.h
- add Icon(char) smallIcon(char)
- add iconsdir and so on
- fixed About This Magic
- fixed all modules use mcc.h
- fixed specfile

* Sat Jul 9 2005 lovewilliam <williamlovecyl@hotmail.com> 0.9.3.5-4mgc
- Add AboutMagic's chinese simp. tramslation
 
* Fri Jul 8 2005 lovewilliam <williamlovecyl@hotmail.com> 0.9.3.5-3mgc
- replace QString::fromLocal8Bit(gettext(char)) instead of "N_(char)"
- fixed Magiconf::GrubUI install
- fixed Magcionf::GrubUI setting read and write bug
- fixed Magiconf::mlimecfg add auto choose
- fixed po file
- retranslate po file
- 0.9.3.5
	   
* Thu Jul 7 2005 lovewilliam <williamlovecyl@hotmai.com> 0.9.3.4-1mgc
- fixed Magiconf::Macadd
- Disabled Magiconf::GrubUI::Install
- add header file mcc.h
- replace QString::fromLocal8Bit(gettext(char)) instead of "_(char)"
- 0.9.3.4

* Tue Jul 5 2005 lovewilliam <williamlovecyl@hotmail.com>0.9.3.3-1mgc
- fixed Magiconf::GrubUI
- Added new po file
- fixed specfile
- update to 0.9.3.3

* Sun Jul 3 2005 lovewilliam <williamlovecyl@hotmail.com>0.9.3.1-1mgc
- add aboutthismagic
- add magiclogo
- update to 0.9.3.1

* Thu Jun 30 2005 lovewilliam <williamlovecyl@hotmail.com>0.9.3-1mgc
- port grub_ui in Magiconf
- add grub_ui icons
- Update to 0.9.3
- fixed Magiconf as click->hide->run->rundone->show
- fixed Magiconf::xDSL
- Add icon ppp.png kppp.png(16x16)
- Add dir icon/16x16

* Fri Jun 17 2005 lovewilliam <williamlovecyl@hotmail.com>0.9.1-5mgc
- update ime dir

* Fri Jun 17 2005 lovewilliam <williamlovecyl@hotmail.com>0.9.1-3mgc
- Add new mlimecfg into Magiconf

* Wed Jun 15 2005 KanKer <kanker@163.com>
- fix a error in mlimecfg

* Fri Jun 10 2005 KanKer <kanker@163.com>
- update mlimecfg to support GTK_IM_MODULE and QT_IM_MODULE.

* Fri Apr 22 2005 KanKer <kanker@163.com>
- update mlimecfg,add a label to display default IME.
- fix mlimecfg a code error.
- fix a spec bug.

* Sun Mar 6 2005 lovewilliam <williamlovecyl@hotmail.com>
- fixed prob mount dirs
- add net card mac address editor
- use gettext for multiple languages
- fixed main file

* Fri Feb 25 2005 kde <jack@linux.net.cn>
- fix some errors and update to 0.8

* Fri Feb 25 2005 lovewilliam <williamlovecyl@hotmail.com>
- use more language in MCC
- auto test locale
- auto choose language
- add MCC parameter

* Sun Feb 20 2005 lovewilliam <williamlovecyl@hotmail.com>
- Port Mlimecfg into MCC
- changed icons size
- fix some small bugs
- update to 0.7

* Tue Jan 20 2005 lovewilliam<williamlovecyl@hotmail.com>
- Update to version 0.6
 
* Sat Dec 04 2004 lovewilliam<williamlovecyl@hotmail.com>
- built

