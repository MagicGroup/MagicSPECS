Name:           lxrandr
Version:        0.1.2
Release:        5%{?dist}
Summary:        Simple monitor configuration tool
Summary(zh_CN.UTF-8): 简单的监视器配置工具

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv3+
URL:            http://lxde.org/
#VCS: git:git://lxde.git.sourceforge.net/gitroot/lxde/lxrandr
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel
BuildRequires:  libXrandr-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  intltool
Requires:       xorg-x11-server-utils

%description
LXRandR is a simple monitor configuration tool utilizing X RandR extension. 
It's a GUI frontend of the command line program xrandr and manages screen 
resolution and external monitors. When you run LXRandR with an external 
monitor or projector connected, its GUI will change and show you some options 
to quickly configure the external device.

LXRandR is the standard screen manager of LXDE, the Lightweight X11 Desktop 
Environment, but can be used in other desktop environments as well.

%description -l zh_CN.UTF-8
这是一个使用 X RandR 扩散的简单监视器配置工具。
它是命令行程序 xrandr 的图形界面前端，可以管理屏幕分辨率和外接监视器等。

%prep
%setup -q
# quick fix for the icon
sed -i 's/^Icon=display/Icon=video-display/g' data/lxrandr.desktop.in


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
desktop-file-install                                       \
  --delete-original                                        \
  --add-category="HardwareSettings;GTK;"                   \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications          \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop
magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/%{name}.1.*


%changelog
* Tue Jul 08 2014 Liu Di <liudidi@gmail.com> - 0.1.2-5
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.1.2-2
- Rebuild for new libpng

* Sun Aug 28 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2
- BuildRequire intltool

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 23 2009 Christoph Wickert <fedora christoph-wickert de> - 0.1.1-3
- Workaround for infinite loop that causes FTBFS (#538905)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 07 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1
- Include new manpage

* Sun Nov 09 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.1-1
- Initial Fedora package
