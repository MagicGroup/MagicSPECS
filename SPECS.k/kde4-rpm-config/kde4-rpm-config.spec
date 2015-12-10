# Disable -debuginfo package generation
#define debug_package   %{nil}
#########
# install root
#
%define kde4_prefix /usr
#
# this is main part  ;)
#
# cmake build type
# http://techbase.kde.org/Development/CMake/Build_Types
%define build_type release

# kde4 build type
# http://api.kde.org/cmake/modules.html#module_KDE4Macros
# 是否启用 KDE 风格的 enable-final 多合一式编译
%define enable_final OFF
# 是否编译 KDE 测试小程序
%define build_test OFF
# kdelibs 例外 ;)
%define build_kdelibs_test ON
# 是否使用 gcc 的位置无关型可执行文件特性(Position Independent Executables)
%define enable_fpie OFF

%define rversion 15.08.2

# 定义 kdehome 环境变量的 cmake 编译参数
%define KDE_DEFAULT_HOME .kde4
# KDE 发行版名称信息，用于错误报告条款
%define KDE_DISTRO_TEXT "Magic Linux 3.0"

# path define
%define kde4_bindir %{kde4_prefix}/bin
%define kde4_sbindir %{kde4_prefix}/sbin
#define kde4_sysconfdir %{kde4_prefix}/etc
%define kde4_sysconfdir %{_sysconfdir}
%define kde4_datadir %{kde4_prefix}/share
%define kde4_includedir %{kde4_prefix}/include
%define kde4_libdir %{kde4_prefix}/%{_lib}
# extra 额外的路径定义
%define kde4_appsdir %{kde4_datadir}/apps
%define kde4_configdir %{kde4_datadir}/config
%define kde4_iconsdir %{kde4_datadir}/icons
%define kde4_htmldir %{kde4_datadir}/doc/HTML
%define kde4_mandir %{kde4_datadir}/man
%define kde4_plugindir %{kde4_libdir}/kde4
%define kde4_kcfgdir %{kde4_datadir}/config.kcfg
%define kde4_localedir %{kde4_datadir}/locale
%define kde4_dbus_interfacesdir %{_datadir}/dbus-1/interfaces
%define kde4_dbus_servicesdir %{_datadir}/dbus-1/services
%define kde4_dbus_system_servicesdir %{_datadir}/dbus-1/system-services
%define kde4_xdgappsdir %{kde4_datadir}/applications/kde4
%define kde4_servicesdir %{kde4_datadir}/kde4/services
%define kde4_servicetypesdir %{kde4_datadir}/kde4/servicetypes
%define kde4_auth_policy_filesdir %{_datadir}/polkit-1/actions

%define _kde4_prefix %_prefix
%define _kde4_sysconfdir %_sysconfdir
%define _kde4_libdir %_libdir
%define _kde4_libexecdir %kde4_plugindir/libexec
%define _kde4_datadir %_datadir
%define _kde4_sharedir %_datadir
%define _kde4_iconsdir %_kde4_sharedir/icons
%define _kde4_configdir %_kde4_sharedir/config
%define _kde4_appsdir %_kde4_sharedir/kde4/apps
%define _kde4_docdir %_kde4_prefix/share/doc
%define _kde4_bindir %_kde4_prefix/bin
%define _kde4_sbindir %_kde4_prefix/sbin
%define _kde4_includedir %_kde4_prefix/include/kde4
%define _kde4_buildtype release
%define _kde4_macros_api 2

%define rpm_macros_dir %{_rpmconfigdir}/macros.d

Summary: KDE4 rpm macros 
Name: kde4-rpm-config
Version: %{rversion}
Release: 7%{?dist}

Group: System Environment/Base
License: Public Domain
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1: macros.kde4
# increment whenever dirs change in an incompatible way
# kde4 apps built using macros.kde4 should

Provides: kde4-macros(api) = %{_kde4_macros_api} 

BuildArch: noarch
BuildRequires: gawk

Requires:  rpm

%description
This package provides some directories that are required/used by KDE. 


%prep


%build


%install
rm -f $RPM_BUILD_DIR/%{name}.list
rm -rf $RPM_BUILD_ROOT

# rpm macros
mkdir -p $RPM_BUILD_ROOT%{rpm_macros_dir}
cat >$RPM_BUILD_ROOT%{rpm_macros_dir}/macros.kde4<<EOF

%_kde4_version %((kde4-config --kde-version 2>/dev/null || echo 4.3.98) | cut -d' ' -f1 )
#_kde4_version %((kde4-config --version 2>/dev/null || echo "KDE: 4.3.98") | grep '^KDE' | sed -e 's/KDE[^:]*:[ ]*//g' | cut -d' ' -f1)

# api = 2
# initial try, including only items that vary from defaults
#

%_kde4_build_tests -DKDE4_BUILD_TESTS:BOOL=OFF
# rpm macros
# 无下划线开头的宏由 magiclinux project 定义
# 下划线开头的宏为 fedora project 兼容目的
%%kde4_prefix           %{kde4_prefix}
%%kde4_kdelibs_version  %{version}
#
# 定义 kdehome 环境变量的 cmake 编译参数
#
%%kde4_default_home     %{KDE_DEFAULT_HOME}
#
# KDE 发行版名称信息，用于错误报告条款
#
%%kde4_distro_text      %{KDE_DISTRO_TEXT}
#
# cmake 编译模式类型
# http://techbase.kde.org/Development/CMake/Build_Types
# release       # 速度优化，无调试符以及 qDebug/kDebug 消息输出
# relwithdebinfo        # 速度优化，可使用参数(-g)回溯错误调试符
# debug         # 速度优化，可使用参数(-g)进行调试并带有调试符
# debugfull     # 不作优化，完整调试支持(-g3)
# profile               # 对 debugfull 模式添加覆盖率标记(-ftest-coverage -fprofile-arcs)
# none          # 编译标记使用 CMAKE_CXX_FLAGS 选项手动设定
#
%%kde4_build_type       %{build_type}
#
# kde4 编译模式类型
# http://api.kde.org/cmake/modules.html#module_KDE4Macros
# 是否启用 KDE 风格的 enable-final 多合一式编译
#
%%kde4_enable_final_bool        %{enable_final}
#
# 是否编译 KDE 测试小程序
#
%%kde4_build_test_bool  %{build_test}
#
# 是否使用 gcc 的位置无关型可执行文件特性(Position Independent Executables)
#
%%kde4_enable_fpie_bool %{enable_fpie}
#
# path define
#
%%kde4_bindir           %{kde4_bindir}
%%kde4_sbindir          %{kde4_sbindir}
%%kde4_sysconfdir       %{kde4_sysconfdir}
%%kde4_datadir          %{kde4_datadir}
%%kde4_includedir       %{kde4_includedir}
%%kde4_libdir           %{kde4_libdir}
#
# extra 额外的路径定义
#
%%kde4_appsdir          %{kde4_appsdir}
%%kde4_configdir        %{kde4_configdir}
%%kde4_iconsdir         %{kde4_iconsdir}
%%kde4_htmldir          %{kde4_htmldir}
%%kde4_mandir           %{kde4_mandir}
%%kde4_plugindir        %{kde4_plugindir}
%%kde4_kcfgdir          %{kde4_kcfgdir}
%%kde4_localedir        %{kde4_localedir}
%%kde4_dbus_interfacesdir   %{kde4_dbus_interfacesdir}
%%kde4_dbus_servicesdir %{kde4_dbus_servicesdir}
%%kde4_dbus_system_servicesdir  %{kde4_dbus_system_servicesdir}
%%kde4_xdgappsdir       %{kde4_xdgappsdir}
%%kde4_servicesdir      %{kde4_servicesdir}
%%kde4_servicetypesdir  %{kde4_servicetypesdir}
%%kde4_auth_policy_filesdir %{kde4_auth_policy_filesdir}
#
###  以下为 fedora project 兼容部分  ###
#
%%_kde4_prefix %%_prefix
%%_kde4_sysconfdir %%_sysconfdir
%%_kde4_libdir %%_libdir
%%_kde4_libexecdir %%kde4_plugindir/libexec
%%_kde4_datadir %%_datadir
%%_kde4_sharedir %%_datadir
%%_kde4_iconsdir %%_kde4_sharedir/icons
%%_kde4_configdir %%_kde4_sharedir/config
%%_kde4_appsdir %%kde4_appsdir
%%_kde4_docdir %_kde4_prefix/share/doc
%%_kde4_bindir %%_kde4_prefix/bin
%%_kde4_sbindir %%_kde4_prefix/sbin
%%_kde4_includedir %%kde4_includedir
%%_kde4_buildtype %_kde4_buildtype
%%_kde4_macros_api %_kde4_macros_api

#
# cmake 编译参数
# 环境变量定义
# 安装路径定义
# 编译模式定义
#
%%cmake_kde4 \\
  QTDIR="%%{qt4_prefix}" ; export QTDIR ; \\
  PATH="%%{qt4_bindir}:\$PATH" ; export PATH ; \\
  PKG_CONFIG_PATH="%%{kde4_libdir}/pkgconfig:\$PKG_CONFIG_PATH" ; export PKG_CONFIG_PATH ; \\
  CFLAGS="\${CFLAGS:-%%optflags}" ; export CFLAGS ; \\
  CXXFLAGS="\${CXXFLAGS:-%%optflags}" ; export CXXFLAGS ; \\
  FFLAGS="\${FFLAGS:-%%optflags}" ; export FFLAGS ; \\
    cmake \\\\\\
    -DCMAKE_INSTALL_PREFIX=%%{kde4_prefix} \\\\\\
    -DSYSCONF_INSTALL_DIR=%%{kde4_sysconfdir} \\\\\\
    -DINCLUDE_INSTALL_DIR=%%{kde4_includedir} \\\\\\
    -DLIB_INSTALL_DIR=%%{kde4_libdir} \\\\\\
    -DDATA_INSTALL_DIR=%%{kde4_appsdir} \\\\\\
    -DICON_INSTALL_DIR=%%{kde4_iconsdir} \\\\\\
    -DHTML_INSTALL_DIR=%%{kde4_htmldir} \\\\\\
    -DMAN_INSTALL_DIR=%%{kde4_mandir} \\\\\\
    -DPLUGIN_INSTALL_DIR=%%{kde4_plugindir} \\\\\\
    -DKCFG_INSTALL_DIR=%%{kde4_kcfgdir} \\\\\\
    -DLOCALE_INSTALL_DIR=%%{kde4_localedir} \\\\\\
    -DDBUS_INTERFACES_INSTALL_DIR=%%{kde4_dbus_interfacesdir} \\\\\\
    -DDBUS_SERVICES_INSTALL_DIR=%%{kde4_dbus_servicesdir} \\\\\\
    -DDBUS_SYSTEM_SERVICES_INSTALL_DIR=%%{kde4_dbus_system_servicesdir} \\\\\\
    -DXDG_APPS_INSTALL_DIR=%%{kde4_xdgappsdir} \\\\\\
    -DSERVICES_INSTALL_DIR=%%{kde4_servicesdir} \\\\\\
    -DSERVICETYPES_INSTALL_DIR=%%{kde4_servicetypesdir} \\\\\\
    -DKDE_DEFAULT_HOME=%%{kde4_default_home} \\\\\\
    -DKDE_DISTRIBUTION_TEXT=%%{kde4_distro_text} \\\\\\
    -DKDE4_AUTH_BACKEND_NAME=POLKITQT-1 \\\\\\
    -DKDE4_AUTH_POLICY_FILES_INSTALL_DIR=%%{kde4_auth_policy_filesdir} \\\\\\
    -DCMAKE_BUILD_TYPE=%%{kde4_build_type} \\\\\\
    -DKDE4_BUILD_TESTS=%%{kde4_build_test_bool} \\\\\\
    -DKDE4_ENABLE_FINAL=%%{kde4_enable_final_bool} \\\\\\
    -DKDE4_ENABLE_FPIE=%%{kde4_enable_fpie_bool} \\\\\\
    -DLIB_SUFFIX=\$(echo %%{_lib} | cut -b4-)

#
# 清理 desktop 文件中的语言条目
#
%%clean_kde4_desktop_files \\
  find %%{buildroot}%%{kde4_datadir} -regex ".*\\\\.desktop\$" | LC_ALL=zh_CN.UTF-8 xargs \\\\\\
    sed -i '/^..*\\\\[[^z]..*\\\\]=..*\$/d'
%%clean_kde4_notifyrc_files \\
  find %%{buildroot}%%{kde4_appsdir} -regex ".*\\\\.notifyrc\$" | LC_ALL=zh_CN.UTF-8 xargs \\\\\\
    sed -i '/^..*\\\\[[^z]..*\\\\]=..*\$/d'

#
# 适应 wav 文件格式通知以及 Magic Linux 音效主题
#
%%adapt_kde4_notifyrc_files \\
  find %%{buildroot}%%{kde4_appsdir} -regex ".*\\\\.notifyrc\$" | LC_ALL=zh_CN.UTF-8 xargs \\\\\\
    sed -i -e 's/^Sound=\\\\(.*\\\\)\\\\.ogg\$/Sound=\\\\1\\\\.wav/g' \\\\\\
           -e 's/KDE-Sys-App-Error.wav/MGC-Sys-App-Error.wav/g' \\\\\\
           -e 's/KDE-Sys-App-Error-Serious.wav/MGC-Sys-App-Error-Serious.wav/g' \\\\\\
           -e 's/KDE-Sys-App-Message.wav/MGC-Sys-App-Message.wav/g' \\\\\\
           -e 's/KDE-Sys-Log-In-Short.wav/MGC-Sys-Log-In-Short.wav/g' \\\\\\
           -e 's/KDE-Sys-Log-Out.wav/MGC-Sys-Log-Out.wav/g' \\\\\\
           -e 's/KDE-Sys-Question.wav/MGC-Sys-Question.wav/g' \\\\\\
           -e 's/KDE-Sys-Trash-Emptied.wav/MGC-Sys-Trash-Emptied.wav/g' \\\\\\
           -e 's/KDE-Sys-Warning.wav/MGC-Sys-Warning.wav/g'

EOF

%clean
rm -rf $RPM_BUILD_ROOT %{name}.list


%files 
%defattr(-,root,root,-)

# KDE4
%{rpm_macros_dir}/macros.kde4

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 15.08.2-7
- 为 Magic 3.0 重建

* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 15.08.2-6
- 为 Magic 3.0 重建

* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 4.14.7-5
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 4.14.7-4
- 为 Magic 3.0 重建

* Mon May 04 2015 Liu Di <liudidi@gmail.com> - 4.14.7-3
- 为 Magic 3.0 重建

* Tue Dec 30 2014 Liu Di <liudidi@gmail.com> - 4.14.3-2
- 更新到 4.14.3

* Tue Oct 21 2014 Liu Di <liudidi@gmail.com> - 4.14.2-2
- 更新到 4.14.2

* Fri Aug 22 2014 Liu Di <liudidi@gmail.com> - 4.13.3-2
- 为 Magic 3.0 重建

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Thu May 22 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Thu May 22 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 更新到

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Sat Mar 16 2013 Rex Dieter <rdieter@fedoraproject.org> 4-45
- use %%{_rpmconfigdir}/macros.d/macros.kde4 (f19+)

* Sat Mar 09 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 4-44
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Ville Skyttä <ville.skytta@iki.fi> - 4-42
- Sync FFLAGS and LDFLAGS in the %%cmake_kde4 macro with redhat-rpm-config (#737386)

* Mon Dec 03 2012 Rex Dieter <rdieter@fedoraproject.org> 4-41
- macros.kde4: %%cmake_kde4 add -DKDE4_BUILD_TESTS=OFF

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Rex Dieter <rdieter@fedoraproject.org> - 4-37
- Unowned /usr/lib*/kde4/plugins/{gui_platform,styles} dirs (#645059)

* Tue Oct 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 4-36
- own /usr/lib*/kde3,/usr/lib*/kde4 (#644571)
- simplify stuff, remove crud

* Sat Feb 13 2010 Rex Dieter <rdieter@fedoraproject.org> - 4-35
- macros.kde4: restore %%cmake_lib_suffix64

* Mon Feb 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 4-34
- macros.kde4: %%cmake_kde4: drop %%cmake_skip_rpath, %%cmake_lib_suffix64

* Wed Jan 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 4-33
- macros.kde4: %%{_kde4_version} using (upstreamed) --kde-version now 

* Wed Jan 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 4-32
- macros.kde4: make %%{_kde4_version} actually work right (using
  old --version output, for now)

* Wed Jan 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 4-31
- macros.kde4: +%%{_kde4_version}

* Wed Aug 05 2009 Rex Dieter <rdieter@fedoraproject.org> - 4-30
- kill the ownership of %%_datadir/sounds (#515745)

* Tue Aug 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4-29
- drop unused (and confusing) /etc/kde4/ crud

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 13 2009 Rex Dieter <rdieter@fedoraproject.org> 4-27
- Should own /usr/share/kde4/services/ServiceMenus (#505735)

* Mon May 11 2009 Rex Dieter <rdieter@fedoraproject.org> 4-26
- own %%_docdir/HTML/<lang>/{common,docs/common} (#445108)

* Thu Mar 12 2009 Rex Dieter <rdieter@fedoraproject.org> 4-25
- own %%_kde4_datadir/wallpapers (revert -20)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 08 2009 Rex Dieter <rdieter@fedoraproject.org> 4-23
- macros.kde4: use %%_cmake_lib_suffix64, %%_cmake_lib_suffix64

* Thu Dec 04 2008 Rex Dieter <rdieter@fedoraproject.org> 4-22
- macros.kde4: (re)add -DCMAKE_SKIP_RPATH:BOOL=ON

* Tue Dec 02 2008 Rex Dieter <rdieter@fedoraproject.org> 4-21
- sync latest cmake macros
- macros.kde4: add -DCMAKE_VERBOSE_MAKEFILE=ON to %%cmake_kde4 (#474053)

* Wed Oct 08 2008 Than Ngo <than@redhat.com> 4-20
- /usr/share/wallpapers owned by desktop-backgrounds-basic

* Sat Sep 13 2008 Than Ngo <than@redhat.com> 4-19
- it's not needed to bump _kde4_macros_api
- use macro

* Sat Sep 13 2008 Than Ngo <than@redhat.com> 4-18
- remove redundant FEDORA, use CMAKE_BUILD_TYPE=release

* Mon Jul 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4-17
- + %%_kde4_sharedir/kde4

* Sun Jun 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4-16
- + %%_datadir/apps/konqueror(/servicemenus)

* Fri May 16 2008 Rex Dieter <rdieter@fedoraproject.org> 4-15
- omit %%_sysconfdir/kde/xdg (see also #249109)

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4-14
- don't define %%{_kde4_debug} in macros.kde4 anymore

* Wed Apr 02 2008 Rex Dieter <rdieter@fedoraproject.org> 4-13
- define %%{_kde4_buildtype} in macros.kde4 too

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4-12
- actually define %%{_kde4_libexecdir} in macros.kde4

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4-11
- add %%{_kde4_libexecdir}, set LIBEXEC_INSTALL_DIR to it
- don't own %%{_kde4_libdir} which is just %%{_libdir}

* Mon Mar 31 2008 Rex Dieter <rdieter@fedoraproject.org> 4-10
- macros.kde4: _kde4_buildtype=FEDORA

* Fri Mar 28 2008 Than Ngo <than@redhat.com>  4-9
- internal services shouldn't be displayed in menu, bz#321771

* Sun Jan 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4-8
- should not own %%_datadir/desktop-directories/ (#430420)

* Fri Jan 25 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4-7
- own %%{_kde4_appsdir}/color-schemes

* Mon Jan 07 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4-6
- -Requires: redhat-rpm-config (revert 4-1 addition)

* Sun Dec 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4-5
- +%%_datadir/autostart, %%_kde4_datadir/autostart

* Tue Dec 11 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 4-4
- set INCLUDE_INSTALL_DIR in %%cmake_kde4

* Tue Dec 11 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 4-3
- actually create the directory listed in the file list

* Tue Dec 11 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 4-2
- set kde4_includedir to %%_kde4_prefix/include/kde4

* Mon Nov 19 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4-1
- Version: 4
- %%cmake_kde4: add -DCMAKE_SKIP_RPATH:BOOL=ON
- Requires: redhat-rpm-config (for proper rpm macro defs)
  (hmm... may need a new -devel pkg somewhere)

* Mon Aug 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.92-9
- BR: gawk
- - %%_prefix/{env,shutdown} (non-FHS)

* Wed Aug 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.92-8
- simplify macros a bit

* Tue Aug 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.92-7
- kde4-macros(api), %%_kde4_macros_api

* Fri Aug 10 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.92-6
- restore kde3 dirs

* Thu Aug 09 2007 Than Ngo <than@redhat.com> - 3.92-5
- use macros

* Thu Aug 09 2007 Than Ngo <than@redhat.com> - 3.92-4
- fix kde4 macro

* Thu Aug 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.92-3
- cleanup macros.kde4 (mostly use _kde4_ prefix)
- Requires: rpm

* Tue Aug 07 2007 Than Ngo <than@redhat.com> 3.92-2
- add missing macros.kde4

* Mon Aug 06 2007 Than Ngo <than@redhat.com> - 3.92-1
- kde4 filesystem
- add KDE4 macros

* Thu Jul 19 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-9
- +%%_datadir/{sounds,templates/.source,wallpapers}

* Wed Jul 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-8
- +%%_datadir/{autostart,emoticons,mimelnk/*}
- +%%_sysconfdir/kde/xdg

* Wed Jul 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-7
- - %%_datadir/icons (owned by filesystem)
- + %%_datadir/icons/locolor (until owned elsewhere)

* Fri Dec 01 2006 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-6
- + %%_datadir/templates (kdebase,koffice)

* Wed Oct 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-5
- + %%_datadir/icons/locolor

* Tue Oct 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-4
- drop/omit %%_datadir/locale/all_languages

* Fri Oct 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-3
- + %%_datadir/desktop-directories
- + %%_datadir/locale/all_languages

* Thu Oct 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-2
- + %%_datadir/applnk/.hidden
- + %%_sysconfdir/kde/kdm
- + %%docdir/HTML/en

* Wed Oct 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-1
- first try
