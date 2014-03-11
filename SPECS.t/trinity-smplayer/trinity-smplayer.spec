%define kde_support 1
%define _prefix %{tde_prefix}

Summary: A great front-end for MPlayer
Summary(zh_CN.UTF-8): MPlayer 的一个很棒的前端
Name: trinity-smplayer
Version: 0.5.21
Release: 6%{?dist}
License: GPL
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Source0: smplayer-%{version}.tar.gz
Source1: smplayer.desktop
Patch1: smplayer-%{version}-mplayer.patch
Patch2: smplayer-0.5.21-tqt.patch
URL: http://smplayer.sourceforge.net/
Packager: Ni Hui <shuizhuyuanluo@126.com>
Requires: mplayer
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Prefix: %{_prefix}

%description
SMPlayer intends to be a complete front-end for MPlayer, from basic features 
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
%setup -q -n smplayer-%{version}
%patch1 -p1
%patch2 -p1

%build
. /etc/profile.d/qt.sh
%{__make} QMAKE=/usr/%{_lib}/qt-3.3/bin/qmake PREFIX=%{_prefix} KDE_SUPPORT=%{kde_support} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} PREFIX=%{_prefix} DESTDIR=%{buildroot} install
%{__rm} -f %{buildroot}%{_datadir}/applications/smplayer.desktop
%{__rm} -f %{buildroot}%{_datadir}/applications/kde/smplayer.desktop
%{__install} -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/applications/kde/smplayer.desktop
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%{_prefix}
%exclude %{_prefix}/*/debug*
%exclude %{_prefix}/src

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.5.21-5
- 为 Magic 3.0 重建

* Mon Aug 6 2007 kde <athena_star {at} 163 {dot} com> - 0.5.21-2mgc
- modify the spec file

* Mon Jul 30 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.5.21-1mgc
- port to Magic Linux 2.1

* Sun May 20 2007 Ricardo Villalba <rvm@escomposlinux.org>
  - use DESTDIR in make install
* Sat May 5 2007 Ricardo Villalba <rvm@escomposlinux.org>
  - fixed some typos
* Mon Feb 12 2007 Ricardo Villalba <rvm@escomposlinux.org>
  - first spec file
