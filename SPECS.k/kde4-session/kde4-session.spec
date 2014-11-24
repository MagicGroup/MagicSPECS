Name: kde4-session
Summary: The KDE 4 Session
Summary(zh_CN.UTF-8): KDE 4 会话
License: GPL v2 or later
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://www.kde.org/
Version: 4.14.2
Release: 1%{?dist}

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: kdebase4-runtime >= %{version}
Requires: phonon-backend
Requires: kde4-kdm >= %{version}
Requires: kdebase4-workspace >= %{version}
Requires: kdebase4-workspace-wallpapers >= %{version}
Requires: oxygen-cursor-themes >= %{version}
Requires: kdebase4 >= %{version}
Requires: kdelibs4 >= %{version}
Requires: kdepimlibs4 >= %{version}

BuildRequires: kdebase4-workspace
BuildRequires: kde4-kdm

%description
This package contains the basic packages for a K Desktop Environment
workspace.

%description -l zh_CN.UTF-8
这个包是 K 桌面环境的基本包。

%prep

%install

install -d -m 755 %{buildroot}%{_datadir}/apps/kdm/sessions/
ln -s %{_datadir}/xsessions/kde4.desktop %{buildroot}%{_datadir}/apps/kdm/sessions/kde4.desktop

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_datadir}/apps/kdm/sessions/kde4.desktop

%changelog
* Fri Oct 31 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Thu Jun 05 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Sun Apr 27 2014 Liu Di <liudidi@gmail.com> - 4.13.0-1.2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-1.1
- 为 Magic 3.0 重建

* Sat Apr 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- 己丑  三月初九  [清明]

* Sun Mar 8 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.1mgc
- 更新至 4.2.1
- 己丑  二月十二

* Sun Jan 25 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.1mgc
- 更新至 4.2.0
- 戊子  十二月三十

* Thu Jan 15 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.1.96-0.1mgc
- 更新至 4.1.96(KDE 4.2 RC1)
- 戊子  十二月二十

* Fri Nov 07 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.3-0.1mgc
- 更新至 4.1.3
- 戊子  十月初十  [立冬]

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.1mgc
- 更新至 4.1.2
- 添加依赖 phonon-backend、kdebase4-workspace-wallpapers 和 oxygen-cursor-themes
- 戊子  九月初一

* Sat Aug 30 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.1mgc
- 更新至 4.1.1(try1 内部版本)
- 戊子  七月三十

* Sat Jul 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.98-0.1mgc
- 更新至 4.0.98(KDE 4.1 rc1)
- 戊子  六月初十

* Thu Jun 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.83-0.1mgc
- 更新至 4.0.83-try1(第一次 tag 4.1.0-beta2 内部版本)
- 去除 startkde 启动脚本(已移入 kdebase-workspace 作为补丁使用了~~)
- 戊子  五月十六

* Sat May 24 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.80-0.1mgc
- 更新至 4.0.80
- 戊子  四月二十

* Sat Apr 26 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.71-0.1mgc
- 更新至 4.0.71
- 戊子  三月廿一

* Sat Apr 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.70-0.1mgc
- 更新至 4.0.70
- 戊子  三月十四

* Sat Apr 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.69-0.1mgc
- 更新至 4.0.69
- 戊子  三月初七

* Wed Apr 2 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.3-0.2mgc
- 修正菜单项为“KDE 4”
- 戊子  二月廿六

* Mon Mar 31 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.3-0.1mgc
- 更新至 4.0.3
- 定义 kde4 路径
- 去除 KDEHOME 环境变量的定义，以对 kde3 程序使用 ~/.kde/ 的配置文件
- 链接 xsession 菜单(moved to kde4-kdm)
- 戊子  二月廿四

* Mon Mar 3 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.2-0.1mgc
- 更新至 4.0.2
- 戊子  正月廿六

* Thu Feb 7 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.1-0.1mgc
- 更新至 4.0.1
- 添加 kdepimlibs 依赖

* Sat Jan 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.1mgc
- 分离 kde3 会话菜单以及 startkde 脚本
- 首次生成 rpm 包
