# overwrite the default value of macro.kde4
%define build_type release

%define real_name kde-l10n-zh_TW

# no debuginfo package for l10n
%define debug_package %{nil}


Name: kde4-l10n-zh_TW
Summary: kde-l10n-zh_TW
Summary(zh_TW.UTF-8): KDE4 的中文语言包
License: LGPL v2 or later
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://www.kde.org/
Version: 4.13.2
Release: 1%{?dist}
Source0: http://download.kde.org/stable/%{version}/src/kde-l10n/%{real_name}-%{version}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libkdelibs4-devel
BuildRequires: gettext

%description
kde-l10n-zh_TW.

%description -l zh_TW.UTF-8
KDE4 的中文语言包。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%prep
%setup -q -n %{real_name}-%{version}

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}
magic_rpm_clean.sh

%files
%defattr(-,root,root)
#%{kde4_appsdir}/*
%{kde4_localedir}/*
%doc %lang(zh_TW) %{kde4_htmldir}/zh_TW/*

%changelog
* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Tue Jun 03 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Mon Apr 28 2014 Liu Di <liudidi@gmail.com> - 4.13.0-1.1
- 为 Magic 3.0 重建

* Wed Aug 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0
- 己丑  六月十五

* Wed Jul 1 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- 更新至 4.2.95(KDE 4.3 RC1)
- 己丑  闰五月初九

* Sat May 16 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.85-1mgc
- 更新至 4.2.85(KDE 4.3 beta1)
- 己丑  四月廿二

* Sat Apr 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- 己丑  三月初九  [清明]

* Sun Mar 8 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.1mgc
- 更新至 4.2.1
- 己丑  二月十二

* Sun Jan 25 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.1mgc
- 更新至 4.2.0
- 戊子  十二月三十

* Wed Jan 14 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.1.96-0.1mgc
- 更新至 4.1.96(KDE 4.2 RC1)
- release 编译模式
- 戊子  十二月十九

* Fri Dec 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.85-0.1mgc
- 更新至 4.1.85(KDE 4.2 Beta2)
- 戊子  十一月十五

* Sat Nov 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.80-0.1mgc
- 更新至 4.1.80
- 戊子  十一月初二

* Fri Nov 07 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.3-0.1mgc
- 更新至 4.1.3
- 戊子  十月初十  [立冬]

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.1mgc
- 更新至 4.1.2
- 戊子  九月初一

* Sat Aug 30 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.1mgc
- 更新至 4.1.1(try1 内部版本)
- 戊子  七月三十

* Fri Jul 25 2008 Liu Di <liudidi@gmail.com> - 4.1.0-0.1mgc
- 更新到 4.1.0

* Sat Jul 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.98-0.1mgc
- 更新至 4.0.98(KDE 4.1 rc1)
- 去除 debuginfo 包
- 戊子  六月初十

* Thu Jun 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.83-0.1mgc
- 更新至 4.0.83-try1(第一次 tag 4.1.0-beta2 内部版本)
- 戊子  五月十六

* Sat May 24 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.80-0.1mgc
- 更新至 4.0.80(try1 内部版本)
- 戊子  四月二十

* Sat Apr 26 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.71-0.1mgc
- 更新至 4.0.71
- 戊子  三月廿一

* Wed Apr 2 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.3-0.1mgc
- 更新至 4.0.3
- 定义 kde4 路径
- 戊子  二月廿六

* Fri Mar 7 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.2-0.1mgc
- 更新至 4.0.2
- 戊子  正月三十

* Thu Feb 7 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.1-0.1mgc
- 更新至 4.0.1

* Sat Jan 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.1mgc
- 更新至 4.0.0

* Sat Dec 15 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.97.0-0.1mgc
- 更新至 3.97.0 (KDE4-RC2)

* Sat Nov 24 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.96.0-0.1mgc
- 更新至 3.96.0 (KDE4-RC1)

* Sat Oct 20 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.94.0-0.1mgc
- 首次生成 rpm 包
