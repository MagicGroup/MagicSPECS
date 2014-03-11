%define debug 0
%define final 1

%define qt_version 3.3.8
%define _iconsdir %_datadir/icons

%define git 1
%define gitdate 20111228

Summary: K Desktop Environment - Utilities
Summary(zh_CN.UTF-8): K桌面环境(KDE) - 工具
Name:          tdeutils
Prefix: /usr
Version:       3.5.14
%if %{git}
Release:	0.git%{gitdate}%{?dist}
%else
Release:       0.1%{?dist}
%endif
License:     GPL
URL: http://www.kde.org
Group:      Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
BuildRoot:     %{_tmppath}/%{name}-buildroot
%if %{git}
Source:	%{name}-git%{gitdate}.tar.xz
%else
Source:     ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2 
%endif
Source1: klaptop_acpi_helper.pam
Source2: klaptop_acpi_helper.console
Source3: kcmlaptoprc
Source4: make_tdeutils_git_package.sh

Patch1: kdf-3.0.2-label.patch
Patch2: kdeutils-3.5.4-bz#205553.patch
Patch3: kdeutils-3.5.4-suspend.patch
Patch4: kdeutils-3.5.4-klaptopdaemon-crash.patch
Patch5: kdeutils-3.4.1.ark-rar.patch

Patch6: kdeutils-3.5.6-kdf.patch
Patch7: kdeutils-3.5.10-python26.patch

Patch8:	tdeutils-libtool.patch
#这仅仅是为了通过编译，此补丁是有问题的
Patch9: tdeutils-compile.patch

# upstream patches

#Source1:ark_directory_service.desktop
#Source2:arkservicemenu.desktop
# Patch:kdeutils-3.2.2-tarfix.patch
Requires: qt, arts, kdelibs, kdebase
Requires: %{name}-common
Requires: %{name}-klaptop
Requires: %{name}-kmilo
Requires: %{name}-kfloppy
Requires: %{name}-kdf
Requires: %{name}-khexedit
Requires: %{name}-ark
Requires: %{name}-kcalc
Requires: %{name}-kwalletmanager

%description
Utilities for the K Desktop Environment.
Includes: ark (tar/gzip archive manager); kcalc (scientific calculator);
kcharselect (character selector); kdepasswd (change password);
kdessh (ssh front end); kdf (view disk usage); kedit (simple text editor);
kfloppy (floppy formatting tool); khexedit (hex editor); kjots (note taker);
klaptopdaemon (battery monitoring and management for laptops);
ksim (system information monitor); ktimer (task scheduler);
kwikdisk (removable media utility)

%description -l zh_CN.UTF-8
K桌面环境的工具。
包括：ark (tar/gzip文档管理器); kcalc（科学计算器）；kcharselect（字符选择器）；
kdepasswd（更改密码）；kdessh（ssh前端）；kdf（查看磁盘使用）；kedit（简单文本编
辑器）；kfloppy（软盘格式化工具）；khexedit（十六进制编辑器）；kjots（便签工具）；
ksim（系统信息监视器）；ktimer（计划任务）；kwikdisk（可移动媒体工具）。

这个包不包括：charselectapplet，kgpg，kjots，ksim，ktimer，kdelirc，kdessh，
khexedit，kedit

#-----------------------------------------------------------------------------

%package common
Summary:        Kdeutils common files
Summary(zh_CN.UTF-8): %{name} 的公用文件
Group:      Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL:        http://www.kde.org/
 
%description common
Kdeutils common files

%description common -l zh_CN.UTF-8
%{name} 的公用文件。

#------------------------------------------------------------------------------

%package klaptop
Summary:        Battery and power management
Summary(zh_CN.UTF-8): 笔记本电脑的电池电源管理程序
Group:      Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Provides:       klaptop
 
%description klaptop
Battery and power management, including KControl plugins.

%description klaptop -l zh_CN.UTF-8
适用于ThinkPad等品牌的笔记本电脑的电池电源管理程序，主要由一个后台守护进程、一个KDE
控制中心模块和一个面板小程序组成。它可以监控电脑用电量并在低电量时发出系统警告以便
用户适时保存关机，使用KLaptop的运作要求有较新版内核的高级电源管理支持，完整功能还包
括交流电源适配器和电池监视等更多子项。

#----------------------------------------------------------------------------------

%package kmilo
Summary:        Battery and power management
Summary(zh_CN.UTF-8): 特殊按键通知服务
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Provides:       kmilo
 
%description kmilo
Battery and power management, including KControl plugins.

%description kmilo -l zh_CN.UTF-8
KMilo是一个在后台执行的特殊按键通知服务，一般也是面向笔记本电脑用户的。众所周知这类电脑
的键盘上常会有一些触发某种快捷功能的按键，如关机、睡眠、音量调节之类。通过KMilo守护进程
可以实现对它们的支持，支持的品牌如Apple PowerBooks、Sony Vaio Laptop、IBM Thinkpads、
Asus Laptops、Dell laptops 等。

#-------------------------------------------------------------------------------------

%package ktimer
Summary:        Ktimer program
Summary(zh_CN.UTF-8): 一个简单的倒计时工具
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Provides:       ktimer
URL:        http://www.kde.org/
 
%description ktimer
Ktimer allows to execute programs after some time

%description ktimer -l zh_CN.UTF-8
一个简单的倒计时工具，允许在一次时间倒计数完成之后触发执行指定的程序，可能在某些特殊时候
被用到。

#-----------------------------------------------------------------------------------------

%package kdessh
Summary:        Kdessh program
Summary(zh_CN.UTF-8): KDE 下的 SSH 前端
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Provides:       kdessh
URL:        http://www.kde.org/
 
%description kdessh
Front end to ssh

%description kdessh -l zh_CN.UTF-8
KDE 下的 SSH 前端。

#--------------------------------------------------------------------------------------

%package kjots
Summary:        Kjots program
Summary(zh_CN.UTF-8): 小巧的笔记存档程序
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Provides:       kjots, Kjots
URL:        http://www.kde.org/
 
%description kjots
Manages several "books" with a subject and notes

%description kjots -l zh_CN.UTF-8
小巧的笔记存档程序。它可以当作整理读书笔记用的迷你电子书签。

#-------------------------------------------------------------------------------------------

%package kfloppy
Summary:        Kfloppy program
Summary(zh_CN.UTF-8): 软盘格式化程序
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Requires:       dosfstools
Provides:       kfloppy
URL:        http://www.kde.org/
 
%description kfloppy
Kfloppy allows to format a floppy disks with this app

%description kfloppy -l zh_CN.UTF-8
软盘格式化程序。它支持DOS（即vFAT）、ext2、Minix 三种文件系统格式，是mkfs系列类Unix工具的前端。

#---------------------------------------------------------------------------------------------

%package kdf
Summary:        Kdf program
Summary(zh_CN.UTF-8): 查看磁盘空间情况
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Provides:       kdf
URL:        http://www.kde.org/
 
%description kdf
Like 'df', a graphical free disk space viewer

%description kdf -l zh_CN.UTF-8
类似 'df', 一个图形化的磁盘空间查看器。

#----------------------------------------------------------------------------------------------

%package kcharselect
Summary:        Kcharselect program
Summary(zh_CN.UTF-8): KDE 的字符选择器
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Provides:       kcharselect
 
%description kcharselect
Kcharselect allows to select special characters from any fonts and put them
into the clipboard

%description kcharselect -l zh_CN.UTF-8
KDE的字符选择器。此程序提供了按表分排的全Unicode字符区域，供用户任选特殊字符取用。
相信大多数人都见过许多网络上时常出现的奇模怪样符号，这些符号一般最初正是被通过这样
的字符选择器工具来输入的。

KDE-Utilities中还有一个CharSelect Applet面板小程序，它是KCharSelect的另外一种使用环境。

#--------------------------------------------------------------------------------------------

%package khexedit
Summary:        Khexedit program
Summary(zh_CN.UTF-8): KDE 下的十六进制编辑器
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Provides:       khexedit
 
%description khexedit
A binary file editor

%description khexedit -l zh_CN.UTF-8
一个KDE下的十六进制编辑器，当然它也允许在二、八、十、十六、文本数种编辑模式间任意转换，
包含二进制过滤器、字符表、编码转换等实用的内置工具。为实际应用中的谨慎考虑，它还提供了
一个一键切换以只读还是读写模式查看当前编辑文件的按钮。

#----------------------------------------------------------------------------------------------

%package kedit
Summary:        Kedit program
Summary(zh_CN.UTF-8): KDE 简单文本编辑器
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Provides:       kedit
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
 
%description kedit
A simple text editor, without formatting like bold, italics etc.

%description kedit -l zh_CN.UTF-8
KDE简单文本编辑器。KEdit的设计精简，只面向基本的文字记录需求，不过它还是有字体定义、拼写
检查、自动换行这些附加功能，而且也有完善的双向文本渲染（如阿拉伯语）支持。

#-----------------------------------------------------------------------------------------------

%package ark
Summary:        Ark program
Summary(zh_CN.UTF-8): KDE 的压缩档案管理工具
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Provides: ark
Requires: zip
Requires: unzip
Requires: rar
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
 
%description ark
Manager for compressed files and archives

%description ark -l zh_CN.UTF-8
KDE的压缩档案管理工具，它配合若干命令行下的压缩工具工作，支持对7Zip、BZip、GZip、RAR、
TAR、ZIP等各种常见压缩程序的前端处理。使用Ark打开一个压缩包，用户可以得到包内目录结构
的树状列表，并执行各种操作。

Ark有两个重要的额外特性，其一是它允许对几乎所有类型的压缩包内文件进行预览处理，根据文
件类型而调用不同的预览部件；其二是它可以和Konqueror文件管理器的右键菜单集成，帮助用户
快捷地实行压缩、解压工作，不过启用此特性需要安装KDE-Addons包内的Arkplugin插件。

#------------------------------------------------------------------------------------------------

%package kcalc
Summary:        Kcalc program
Summary(zh_CN.UTF-8): 一个计算器程序
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Provides:       kcalc
URL:        http://www.kde.org/
 
%description kcalc
A scientific calculator
 
%description kcalc -l zh_CN.UTF-8
一个计算器程序，对于面向日常生活需求的数字计算要求来说功能非常全面，打开此软件的全部功
能后您会在程序界面上看到约70个按钮。KCalc支持角度、弧度、梯度的转换、进制转换、统计运
算、逻辑运算等，内建一组常用的科学常量，用户也可自定义常量。

#----------------------------------------------------------------------------------------------

%package ksim
Summary:        Ksim program
Summary(zh_CN.UTF-8):	监测系统硬件用的特殊面板
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Provides:       ksim
URL:        http://www.kde.org/
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
 
%description ksim
Ksim program

%description ksim -l zh_CN.UTF-8
这是监测系统硬件用的特殊面板，由主面板Kicker负责加载执行。它可以在您的桌面上实时显示一系列
底层硬件工作状态描述的可视化输出，KSim采用插件式的设计来监测更多硬件指标，现在支持的监测项
如CPU使用率、硬盘空间、网络接口状态、散热风扇状态等。它只会在您呼叫时才弹出界面，平时可缩
退到屏幕顶端，不妨碍正常操作。

#-----------------------------------------------------------------------------------------------

%package kgpg
Summary:        Kgpg Frontend for gpg
Summary(zh_CN.UTF-8): GPG 即 GNUPG，KGPG 提供了它的图形化操作界面
Group:        	Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Provides:       kgpg
URL:        http://www.kde.org/
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
 
%description kgpg
kgpg is a simple, free, open source KDE frontend for gpg.

%description kgpg -l zh_CN.UTF-8
GPG即GNUPG，KGPG提供了它的图形化操作界面。GPG是类Unix系统中常用的隐私保护工具之一。在文件
加密、安全邮件等方面用途广泛，在国外的一些开源组织成员聚会时也常会有交换GPG公钥这样的活动。
但GNUPG本身只有命令行界面，参数繁多，用户需要花费一段时间才能适应，故KGPG作为其前端应需而
生，它在很大程度上使得这套复杂强大的工具平易近人。用户可以创建、编辑、删除、上传、下载指
定的密钥，KGPG不仅力图方便，也尽可能保证在图形界面环境下的操作也同样安全。

#---------------------------------------------------------------------------------------------------

%package superkaramba
Group:      Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Summary:    Program that can display a lot of various information right on your desktop
Summary(zh_CN.UTF-8): 热装卸桌面部件管理器
Provides:       superkaramba
 
%description superkaramba
Karamba is a KDE program that can display a lot of various information
right on your desktop. Karamba uses the same "fake" transparency effect
that e.g., Konsole can use. For the autor this is not a big problem as the
purpose of Karamba is sit on the background.

%description superkaramba -l zh_CN.UTF-8
热装卸桌面部件管理器。对于某些桌面玩家可使自由多变的热装卸部件的KDE用户来说，现在他们有一个
可行的方案在自己的桌面环境上也营造同样的氛围。SuperKaramba可以从互联网上KDE提供的百宝箱服务
器中搜索下载您中意的小部件，例如天气公告牌、硬盘数据吞吐量波状监测器、即时音乐点播器……并
随时安装到桌面上，立即生效，关闭以及卸载都同样即时化。

SuperKaramba主题的编写语言一般是易学的脚本语言Python，主题开发者不需懂得艰深的C++也一样能在
脚本之间调用KDE的图形界面构件，并制作出半透明、颜色渐变、图像缩放、字幕滚动等一系列养眼特效，
这大大降低了桌面部件的编写难度，SuperKaramba的发展无疑也得益于这较低的上手门槛。

#-----------------------------------------------------------------------------------------------------

%package kwalletmanager
Summary:    Kwalletmanager program
Summary(zh_CN.UTF-8): KDE 钱包管理器
Group:      Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Provides:   kwalletmanager
URL:        http://www.kde.org/
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
 
%description kwalletmanager
Kwalletmanager program

%description kwalletmanager -l zh_CN.UTF-8
这是对应KDE-Libs中KWallet部件的前端管理器，即KDE钱包管理器。在这个程序里用户可以明文查看自己
以往保存的所有明文密码数据，并与用户名、程序、账户一一对应，分类名称有条不紊地区分了不同的认
证密文对，保证了在储存了大量密文对的前提下也能让用户快捷地筛选到想要的资料。

KWalletManager还支持多钱包以及钱包数据的导入、导出，用户可以利用这一特性实施密码的备份和转移。

#----------------------------------------------------------------------------------------------------

%package devel
Summary: Development files for %{name} 
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: kdelibs-devel

%description devel
Development files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。


%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
#%patch4 -p1
#%patch5 -p1
%patch6 -p1
#%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
unset QTDIR || : ; . /etc/profile.d/qt.sh

export KDEDIR=%{prefix}
export CXXFLAGS="$RPM_OPT_FLAGS -DNDEBUG -DNO_DEBUG -fno-use-cxa-atexit -fno-check-new"
export CFLAGS="$RPM_OPT_FLAGS -DNDEBUG -DNO_DEBUG"

make -f admin/Makefile.common

#CFLAGS="$CFLAGS -lXext -lkparts -ldl -lkdecore -lkdeui -lkdesu -lX11 -lDCOP -lkio -lkdefx" \
#CXXFLAGS="$CXXFLAGS -lXext -lkparts -ldl -lkdecore -lkdeui -lkdesu -lX11 -lDCOP -lkio -lkdefx" \
%configure \
   --disable-rpath \
   --enable-closure \
   --with-qt-libraries=$QTDIR/lib \
%if %{final}
   --enable-final	
%endif

make
%install
mkdir -p $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# using pam
install -m 755 -d %{buildroot}/%{_sysconfdir}/pam.d
install -m 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/pam.d/klaptop_acpi_helper

install -m 755 -d %{buildroot}/%{_sysconfdir}/security/console.apps/
install -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/security/console.apps/klaptop_acpi_helper

pushd %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_sbindir}
mv klaptop_acpi_helper ../sbin
ln -s consolehelper klaptop_acpi_helper
popd

# klaptop setting
mkdir -p %{buildroot}/%{_datadir}/config
install -m 644 %{SOURCE3} %{buildroot}/%{_datadir}/config/

%clean   
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%files devel
%defattr(-,root,root,-)
%{_includedir}/*

%files klaptop
%defattr(-,root,root)
%attr(-,root,nogroup) %_sysconfdir/pam.d/klaptop_acpi_helper
%attr(-,root,nogroup) %_sysconfdir/security/console.apps/klaptop_acpi_helper
%_bindir/klaptop_check
%_iconsdir/*/*/*/laptop*
%dir %_datadir/apps/klaptopdaemon/
%_datadir/apps/klaptopdaemon/*
%_datadir/services/kded/klaptopdaemon.desktop
%doc %_docdir/HTML/en/kcontrol/kcmlowbatcrit
%doc %_docdir/HTML/en/kcontrol/kcmlowbatwarn
%doc %_docdir/HTML/en/kcontrol/laptop
%doc %_docdir/HTML/en/kcontrol/powerctrl
%_datadir/applications/kde/pcmcia.desktop
%_datadir/applications/kde/laptop.desktop
%_libdir/trinity/kcm_laptop.*
%_libdir/trinity/kded_klaptopdaemon.*
%_libdir/libkcmlaptop.la
%_libdir/libkcmlaptop.so.*

%files kmilo
%defattr(-,root,root)
%_libdir/trinity/kded_kmilod.*
%_libdir/trinity/kmilo_asus.*
%_libdir/trinity/kmilo_delli8k.*
%_libdir/trinity/kmilo_generic.*
%_libdir/trinity/kmilo_kvaio.*
%_libdir/trinity/kmilo_thinkpad.*
%_libdir/trinity/kcm_kvaio.*
%_libdir/trinity/kcm_thinkpad.*
%_datadir/services/kded/kmilod.desktop
%_datadir/applications/kde/thinkpad.desktop
%_datadir/applications/kde/kvaio.desktop
%dir %_datadir/services/kmilo
%_datadir/services/kmilo/*
%dir %_datadir/servicetypes/kmilo
%_datadir/servicetypes/kmilo/kmilopluginsvc.desktop
%_libdir/libkmilo.la
%_libdir/libkmilo.so.*

%files ktimer
%defattr(-,root,root)
%doc %_docdir/HTML/en/ktimer
%_bindir/ktimer
%_datadir/applications/kde/ktimer.desktop
%_iconsdir/*/*/*/ktimer*

%files kdessh
%defattr(-,root,root)
%_bindir/kdessh

%files kjots
%defattr(-,root,root)
%doc %_docdir/HTML/en/kjots
%_iconsdir/*/*/*/kjots.*
%_bindir/kjots
%dir %_datadir/apps/kjots
%_datadir/apps/kjots/*
%_datadir/applications/kde/Kjots.desktop
%_datadir/config.kcfg/kjots.kcfg

%files kfloppy
%defattr(-,root,root)
%doc %_docdir/HTML/en/kfloppy
%_iconsdir/*/*/*/kfloppy.*
%_bindir/kfloppy
%_datadir/applications/kde/KFloppy.desktop
%_datadir/apps/konqueror/servicemenus/floppy_format.desktop

%files kdf
%defattr(-,root,root)
%doc %_docdir/HTML/en/kdf
%_bindir/kdf
%_bindir/kwikdisk
%_iconsdir/*/*/*/kwikdisk.*
%_iconsdir/*/*/*/kdf.*
%_iconsdir/*/*/*/kcmdf.*
%dir %_datadir/apps/kdf
%_datadir/apps/kdf/*
%_datadir/applications/kde/kdf.desktop
%_datadir/applications/kde/kwikdisk.desktop
%_datadir/applications/kde/kcmdf.desktop
%_libdir/trinity/kcm_kdf.*

%files kcharselect
%defattr(-,root,root)
%doc %_docdir/HTML/en/kcharselect
%_bindir/kcharselect
%_libdir/trinity/kcharselect_panelapplet.*
%_datadir/apps/kicker/applets/kcharselectapplet.desktop
%_iconsdir/*/*/*/kcharselect.*
%dir %_datadir/apps/kcharselect
%_datadir/apps/kcharselect/*
%_datadir/applications/kde/KCharSelect.desktop
%_datadir/apps/kconf_update/kcharselect.upd

%files khexedit
%defattr(-,root,root)
%doc %_docdir/HTML/en/khexedit
%_bindir/khexedit
%_iconsdir/*/*/*/khexedit.*
%_datadir/services/khexedit2part.desktop
%_datadir/apps/khexedit2part/khexedit2partui.rc
%dir %_datadir/apps/khexedit
%_datadir/apps/khexedit/*
%_datadir/applications/kde/khexedit.desktop
%_datadir/services/kbyteseditwidget.desktop
%_libdir/trinity/libkbyteseditwidget.*
%_libdir/trinity/libkhexedit2part.*
%_libdir/libkhexeditcommon.la
%_libdir/libkhexeditcommon.so.*

%files kedit
%defattr(-,root,root)
%_bindir/kedit
%_libdir/trinity/kedit.*
%_libdir/libtdeinit_kedit.*
%doc %_docdir/HTML/en/kedit
%dir %_datadir/apps/kedit
%_datadir/apps/kedit/*
%_datadir/config.kcfg/kedit.kcfg
%_iconsdir/*/*/*/kedit.*
%_datadir/applications/kde/KEdit.desktop

%files ark
%defattr(-,root,root)
%doc %_docdir/HTML/en/ark
%_iconsdir/*/*/*/ark.*
%_bindir/ark
%dir %_datadir/apps/
%_datadir/apps/ark/*
%_datadir/applications/kde/ark.desktop
%_libdir/trinity/ark.*
%_libdir/trinity/libarkpart.*
%_datadir/config.kcfg/ark.kcfg
%_datadir/services/ark_part.desktop
%_libdir/libtdeinit_ark.*

%files kcalc
%defattr(-,root,root)
%_bindir/kcalc
%_datadir/applications/kde/kcalc.desktop
%_iconsdir/*/*/*/kcalc.*
%_libdir/trinity/kcalc.*
%_datadir/config.kcfg/kcalc.kcfg
%dir %_datadir/apps/kcalc/
%_datadir/apps/kcalc/*
%_datadir/apps/kconf_update/kcalcrc.upd
%doc %_docdir/HTML/en/kcalc
%_libdir/libtdeinit_kcalc.*

%files ksim
%defattr(-,root,root)
%_datadir/apps/kicker/extensions/ksim.desktop
%_libdir/trinity/ksim_*.*
%dir %_datadir/apps/ksim
%_datadir/apps/ksim/*
%_datadir/config/ksim_panelextensionrc
%doc %_docdir/HTML/en/ksim
%_iconsdir/*/*/*/ksim*
%_libdir/libksimcore.la
%_libdir/libksimcore.so.*

%files kgpg
%defattr(-,root,root)
%_bindir/kgpg
%_datadir/applications/kde/kgpg.desktop
%_datadir/config.kcfg/kgpg.kcfg
%_iconsdir/*/*/*/kgpg.*
%dir %_datadir/apps/kgpg
%_datadir/apps/kgpg/*
%doc %_docdir/HTML/en/kgpg
%_datadir/autostart/kgpg.desktop
%_datadir/apps/konqueror/servicemenus/encryptfile.desktop
%_datadir/apps/konqueror/servicemenus/encryptfolder.desktop

%files superkaramba
%defattr(-,root,root,-)
%_bindir/superkaramba
%_datadir/applnk/Utilities/superkaramba.desktop
%_datadir/apps/superkaramba/superkarambaui.rc
%doc %_docdir/HTML/en/superkaramba
%_iconsdir/*/*/*/superkaramba*
%_datadir/mimelnk/application/x-superkaramba.desktop

%files kwalletmanager
%defattr(-,root,root)
%_bindir/kwalletmanager
%_iconsdir/*/*/*/kwalletmanager.*
%_datadir/applications/kde/kwalletmanager-kwalletd.desktop
%doc %_docdir/HTML/en/kwallet
%_datadir/applications/kde/kwalletconfig.desktop
%_datadir/applications/kde/kwalletmanager.desktop
%_libdir/trinity/kcm_kwallet.*
%_datadir/services/kwallet_config.desktop
%_datadir/services/kwalletmanager_show.desktop
%dir %_datadir/apps/kwalletmanager/
%_datadir/apps/kwalletmanager/*

%files common 
%defattr(-,root,root)
%_bindir/irkick
%_bindir/klaptop_acpi_helper
%_bindir/kregexpeditor
%_libdir/trinity/irkick.la
%_libdir/trinity/irkick.so
%_libdir/trinity/kcm_kcmlirc.la
%_libdir/trinity/kcm_kcmlirc.so
%_libdir/trinity/libkregexpeditorgui.la
%_libdir/trinity/libkregexpeditorgui.so
%_libdir/libkcmlaptop.so
%_libdir/libtdeinit_irkick.la
%_libdir/libtdeinit_irkick.so
%_libdir/libkhexeditcommon.so
%_libdir/libkmilo.so
%_libdir/libkregexpeditorcommon.la
%_libdir/libkregexpeditorcommon.so
%_libdir/libkregexpeditorcommon.so.1
%_libdir/libkregexpeditorcommon.so.1.0.0
%_libdir/libksimcore.so
/usr/sbin/klaptop_acpi_helper
%_datadir/applications/kde/irkick.desktop
%_datadir/applications/kde/kcmlirc.desktop
%_datadir/applications/kde/kregexpeditor.desktop
%_datadir/apps/irkick/icons/hicolor/16x16/actions/irkick.png
%_datadir/apps/irkick/icons/hicolor/16x16/actions/irkickflash.png
%_datadir/apps/irkick/icons/hicolor/16x16/actions/irkickoff.png
%_datadir/apps/irkick/icons/hicolor/16x16/actions/ledblue.png
%_datadir/apps/irkick/icons/hicolor/16x16/actions/ledgreen.png
%_datadir/apps/irkick/icons/hicolor/16x16/actions/ledlightblue.png
%_datadir/apps/irkick/icons/hicolor/16x16/actions/ledlightgreen.png
%_datadir/apps/irkick/icons/hicolor/16x16/actions/ledorange.png
%_datadir/apps/irkick/icons/hicolor/16x16/actions/ledpurple.png
%_datadir/apps/irkick/icons/hicolor/16x16/actions/ledred.png
%_datadir/apps/irkick/icons/hicolor/16x16/actions/ledyellow.png
%_datadir/apps/irkick/icons/hicolor/32x32/actions/ledblue.png
%_datadir/apps/irkick/icons/hicolor/32x32/actions/ledgreen.png
%_datadir/apps/irkick/icons/hicolor/32x32/actions/ledlightblue.png
%_datadir/apps/irkick/icons/hicolor/32x32/actions/ledlightgreen.png
%_datadir/apps/irkick/icons/hicolor/32x32/actions/ledorange.png
%_datadir/apps/irkick/icons/hicolor/32x32/actions/ledpurple.png
%_datadir/apps/irkick/icons/hicolor/32x32/actions/ledred.png
%_datadir/apps/irkick/icons/hicolor/32x32/actions/ledyellow.png
%_datadir/apps/kregexpeditor/pics/altn.png
%_datadir/apps/kregexpeditor/pics/anychar.png
%_datadir/apps/kregexpeditor/pics/autoverify.png
%_datadir/apps/kregexpeditor/pics/begline.png
%_datadir/apps/kregexpeditor/pics/characters.png
%_datadir/apps/kregexpeditor/pics/compound.png
%_datadir/apps/kregexpeditor/pics/endline.png
%_datadir/apps/kregexpeditor/pics/error.png
%_datadir/apps/kregexpeditor/pics/neglookahead.png
%_datadir/apps/kregexpeditor/pics/nonwordboundary.png
%_datadir/apps/kregexpeditor/pics/poslookahead.png
%_datadir/apps/kregexpeditor/pics/repeat.png
%_datadir/apps/kregexpeditor/pics/select.png
%_datadir/apps/kregexpeditor/pics/text.png
%_datadir/apps/kregexpeditor/pics/verify.png
%_datadir/apps/kregexpeditor/pics/wordboundary.png
%_datadir/apps/kregexpeditor/predefined/general/anything.regexp
%_datadir/apps/kregexpeditor/predefined/general/spaces.regexp
%_datadir/apps/profiles/klauncher.profile.xml
%_datadir/apps/profiles/konqueror.profile.xml
%_datadir/apps/profiles/noatun.profile.xml
%_datadir/apps/profiles/profile.dtd
%_datadir/apps/remotes/RM-0010.remote.xml
%_datadir/apps/remotes/cimr100.remote.xml
%_datadir/apps/remotes/hauppauge.remote.xml
%_datadir/apps/remotes/remote.dtd
%_datadir/apps/remotes/sherwood.remote.xml
%_datadir/apps/remotes/sonytv.remote.xml
%_datadir/autostart/irkick.desktop
%_datadir/config/kcmlaptoprc
%_datadir/doc/HTML/en/KRegExpEditor/altn.png
%_datadir/doc/HTML/en/KRegExpEditor/altntool.png
%_datadir/doc/HTML/en/KRegExpEditor/anychar.png
%_datadir/doc/HTML/en/KRegExpEditor/anychartool.png
%_datadir/doc/HTML/en/KRegExpEditor/begline.png
%_datadir/doc/HTML/en/KRegExpEditor/boundarytools.png
%_datadir/doc/HTML/en/KRegExpEditor/characters.png
%_datadir/doc/HTML/en/KRegExpEditor/charactertool.png
%_datadir/doc/HTML/en/KRegExpEditor/common
%_datadir/doc/HTML/en/KRegExpEditor/compound.png
%_datadir/doc/HTML/en/KRegExpEditor/compoundtool.png
%_datadir/doc/HTML/en/KRegExpEditor/endline.png
%_datadir/doc/HTML/en/KRegExpEditor/index.cache.bz2
%_datadir/doc/HTML/en/KRegExpEditor/index.docbook
%_datadir/doc/HTML/en/KRegExpEditor/linestartendtool.png
%_datadir/doc/HTML/en/KRegExpEditor/lookaheadtools.png
%_datadir/doc/HTML/en/KRegExpEditor/neglookahead.png
%_datadir/doc/HTML/en/KRegExpEditor/nonwordboundary.png
%_datadir/doc/HTML/en/KRegExpEditor/poslookahead.png
%_datadir/doc/HTML/en/KRegExpEditor/repeat.png
%_datadir/doc/HTML/en/KRegExpEditor/repeattool.png
%_datadir/doc/HTML/en/KRegExpEditor/select.png
%_datadir/doc/HTML/en/KRegExpEditor/text.png
%_datadir/doc/HTML/en/KRegExpEditor/texttool.png
%_datadir/doc/HTML/en/KRegExpEditor/theEditor.png
%_datadir/doc/HTML/en/KRegExpEditor/wordboundary.png
%_datadir/doc/HTML/en/irkick/common
%_datadir/doc/HTML/en/irkick/index.cache.bz2
%_datadir/doc/HTML/en/irkick/index.docbook
%_datadir/doc/HTML/en/kcmlirc/common
%_datadir/doc/HTML/en/kcmlirc/index.cache.bz2
%_datadir/doc/HTML/en/kcmlirc/index.docbook
%_datadir/doc/HTML/en/kinfocenter/blockdevices/common
%_datadir/doc/HTML/en/kinfocenter/blockdevices/index.cache.bz2
%_datadir/doc/HTML/en/kinfocenter/blockdevices/index.docbook
%_datadir/icons/hicolor/128x128/apps/kregexpeditor.png
%_datadir/icons/hicolor/16x16/apps/irkick.png
%_datadir/icons/hicolor/16x16/apps/kregexpeditor.png
%_datadir/icons/hicolor/22x22/apps/irkick.png
%_datadir/icons/hicolor/22x22/apps/kregexpeditor.png
%_datadir/icons/hicolor/32x32/apps/irkick.png
%_datadir/icons/hicolor/32x32/apps/kregexpeditor.png
%_datadir/icons/hicolor/48x48/apps/kregexpeditor.png
%_datadir/icons/hicolor/64x64/apps/kregexpeditor.png
%_datadir/icons/locolor/16x16/apps/irkick.png
%_datadir/icons/locolor/32x32/apps/irkick.png
%_datadir/services/kregexpeditorgui.desktop

%changelog
* Fri Aug 29 2008 Liu Di <liudidi@gmail.com> - 3.5.10-1mgc
- 更新到 3.5.10
- 拆个 devel 出来，不过据我所知，没有东西会找这个 devel 编译.....

* Wed Feb 19 2008 Liu Di <liudidi@gmail.com> - 3.5.9-1mgc
- updaet to 3.5.9

* Fri Oct 17 2007 Liu Di <liudidi@gmail.com> - 3.5.8-1mgc
- update to 3.5.8

* Tue May 29 2007 Liu Di <liudidi@gmail.com> - 3.5.7-1mgc
- update to 3.5.7

* Fri Jan 26 2007 Liu Di <liudidi@gmail.com> - 3.5.6-1mgc
- update to 3.5.6

* Sat Oct 21 2006 Liu Di <liudidi@gmail.com> - 3.5.5-1mgc
- update to 3.5.5

* Fri Aug 25 2006 Liu Di <liudidi@gmail.com> - 3.5.4-1mgc
- update to 3.5.4

* Thu Jul  1 2006 Liu Di <liudidi@gmail.com> - 3.5.3-1mgc
- update to 3.5.3

* Sun Apr 16 2006 KanKer <kanker@163.com>
- 3.5.2

* Thu Oct 18 2005 KanKer <kanker@163.com>
- 3.4.3

* Sun Jul 31 2005 KanKer <kanker@163.com>
- 3.4.2

* Sat Jul 9 2005 KanKer <kanker@163.com>
- add a patch 'kdeutils-3.4.1.ark-rar.patch' from hew

* Wed Jun 1 2005 KanKer <kanker@163.com>
- 3.4.1

* Wed Apr 27 2005 KanKer <kanker@163.com>
- remove /usr/share/services/khexedit2part.desktop.

* Mon Mar 21 2005 KanKer <kanker@163.com>
- 3.4.0
* Fri Dec 17 2004 KanKer <kanker@163.com>
- rebuild to remove libselinux
*Tue Dec 14 2004 tingxx <tingxx@21cn.com>
- update to 3.3.2 for ML

* Fri Oct 15 2004 KanKer <kanker@163.com>
- update to 3.3.1 for ML

