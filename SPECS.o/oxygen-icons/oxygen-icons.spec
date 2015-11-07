%define real_name oxygen-icons

Name: %{real_name}
Summary: The KDE 4 Oxygen Icon Set
Summary(zh_CN.UTF-8): KDE 4 的 Oxygen 图标集
License: GPL v2 or later
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://www.kde.org/
Version: 4.3
Release: 2%{?dist}
Source0: http://download.kde.org/stable/%{version}/src/%{real_name}-%{version}.tar.xz

Source10: 16-start-here-magic.png
Source11: 22-start-here-magic.png
Source12: 32-start-here-magic.png
Source13: 48-start-here-magic.png
Source14: 64-start-here-magic.png
Source15: 128-start-here-magic.png
Source16: 256-start-here-magic.png


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake >= 2.6.2

Conflicts: kdebase4-runtime-oxygen < 4.2.85
Provides: kdebase4-runtime-oxygen = %{version}-%{release}
Provides: oxygen-icon-theme = %{version}-%{release}

%description
The KDE 4 Oxygen icon set.

%description -l zh_CN.UTF-8
KDE 4 Oxygen 图标。

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
make DESTDIR=%{buildroot} install/fast

# install start-here-magic icons
install -D -m 0755 %{SOURCE10} %{buildroot}%{kde4_iconsdir}/oxygen/16x16/places/start-here-magic.png
install -D -m 0755 %{SOURCE11} %{buildroot}%{kde4_iconsdir}/oxygen/22x22/places/start-here-magic.png
install -D -m 0755 %{SOURCE12} %{buildroot}%{kde4_iconsdir}/oxygen/32x32/places/start-here-magic.png
install -D -m 0755 %{SOURCE13} %{buildroot}%{kde4_iconsdir}/oxygen/48x48/places/start-here-magic.png
install -D -m 0755 %{SOURCE14} %{buildroot}%{kde4_iconsdir}/oxygen/64x64/places/start-here-magic.png
install -D -m 0755 %{SOURCE15} %{buildroot}%{kde4_iconsdir}/oxygen/128x128/places/start-here-magic.png
install -D -m 0755 %{SOURCE16} %{buildroot}%{kde4_iconsdir}/oxygen/256x256/places/start-here-magic.png
magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root,-)
%doc COPYING
%{kde4_iconsdir}/oxygen

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 4.3-2
- 更新到 4.3

* Wed Dec 31 2014 Liu Di <liudidi@gmail.com> - 4.14.3-1
- 更新到 4.14.3

* Fri Oct 31 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Sun Apr 27 2014 Liu Di <liudidi@gmail.com> - 4.13.0-1.1
- 为 Magic 3.0 重建

* Sat Dec 5 2009 Ni Hui <shuizhuyuanluo@126.com> 4.3.4-1mgc
- 更新至 4.3.4
- 安装 start-here-magic 图标
- 乙丑  十月十九

* Wed Aug 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0
- 己丑  六月十五

* Mon Jun 29 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- 更新至 4.2.95(KDE 4.3 RC1)
- 己丑  闰五月初七

* Sat May 16 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.85-1mgc
- 更新至 4.2.85(KDE 4.3 Beta1)
- 首次生成 rpm 包
- 己丑  四月廿二
