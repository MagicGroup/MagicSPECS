%define testingtag RC
%define git 1
%define vcsdate 20151028

Name:		bangarang
Group:		Applications/Multimedia
Group(zh_CN.UTF-8):   应用程序/多媒体
Version:	2.1.1
%if 0%{?git}
Release:	0.%{vcsdate}.%{?dist}.3
%else
Release:	4%{dist}
%endif
License:	GPL v3
Summary:	A KDE media player
Summary(zh_CN.UTF-8): KDE 媒体播放器
URL:		http://gitorious.org/bangarang
%if 0%{?git}
Source0:	%{name}-git%{vcsdate}.tar.xz
%else
Source0:	http://bangarangissuetracking.googlecode.com/files/%{name}-%{version}.tar.gz
%endif
Source1:	make_bangarang_git_package.sh

Patch2: bangarang-git20130108-gcc47.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libkdelibs4-devel
BuildRequires: phonon-devel

%description
Bangarang is a KDE media player.

%description -l zh_CN.UTF-8
Bangarang 是款 KDE 媒体播放器。

%prep
%if 0%{?git}
%setup -q -n %{name}-git%{vcsdate}
%else
%setup -q -n %{name}-%{name}
%endif

#%patch1 -p1 -b .orig
%patch2 -p1

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?smp_flags}

%install
rm -rf $RPM_BUILD_ROOT
cd build
make DESTDIR=%{buildroot} install

magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr (-,root,root)
%doc COPYING README
%{kde4_bindir}/bangarang*
%{kde4_appsdir}/solid/actions/*
%{kde4_iconsdir}/hicolor/*
%{kde4_xdgappsdir}/bangarang.desktop
%{kde4_localedir}/*

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com>
- 更新到 20151028 日期的仓库源码

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com>
- 为 Magic 3.0 重建

* Tue Mar 04 2014 Liu Di <liudidi@gmail.com>
- 更新到 20140304 日期的仓库源码

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 2.0.1-2
- 为 Magic 3.0 重建

* Wed Nov 02 2011 Liu Di <liudidi@gmail.com> - 2.0.1-1
- 更新到 2.0.1

* Sat Jan 9 2010 Ni Hui <shuizhuyuanluo@126.com> - 1.0-1.RC.1mgc
- 更新至 1.0-RC1
- 乙丑  十一月廿五

* Sun Dec 26 2009 Ni Hui <shuizhuyuanluo@126.com> - 1.0-0.beta3.2mgc
- 更新至 1.0-beta3
- 修正编译
- 优化编码探测
- 乙丑  十一月十一

* Sun Dec 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 1.0-0.beta2.1mgc
- 首次生成 RPM 包
