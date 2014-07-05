# Review at https://bugzilla.redhat.com/show_bug.cgi?id=452395

Name:           lxlauncher
Version:        0.2.2
Release:        2%{?dist}
Summary:        Open source replacement for Launcher on the EeePC
Summary(zh_CN.UTF-8): EeePC 上的 Launcher 的开源替代品

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            http://lxde.org/
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxlauncher;a=commit;h=56a244f
Patch0:         lxlauncher-0.2.2-Fix-GtkAllocation-to-fix-empty-lxlauncher.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel >= 2.12 startup-notification-devel
BuildRequires:  menu-cache-devel >= 0.3.2
BuildRequires:  gettext intltool

%description
LXLauncher is designed as an open source replacement for the Asus Launcher
included in their EeePC. It is desktop-independent and follows 
freedesktop.org specs, so newly added applications will automatically show 
up in the launcher, and vice versa for the removed ones.
LXLauncher is part of LXDE, the Lightweight X11 Desktop Environment.

%description -l zh_CN.UTF-8
EeePC 上的 Launcher 的开源替代品。

%prep
%setup -q
%patch0 -p1 -b .Fix-GtkAllocation


%build
%configure
# workaround for FTBFS #539147 and #661008
#touch -r po/Makefile po/stamp-it
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
mkdir -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
mkdir -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/backgrounds
mkdir -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%dir %{_sysconfdir}/xdg/lxlauncher/
%config(noreplace) %{_sysconfdir}/xdg/lxlauncher/gtkrc
%config(noreplace) %{_sysconfdir}/xdg/lxlauncher/settings.conf
%config(noreplace) %{_sysconfdir}/xdg/menus/lxlauncher-applications.menu
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/desktop-directories/lxde-*.directory


%changelog
* Fri Jul 04 2014 Liu Di <liudidi@gmail.com> - 0.2.2-2
- 为 Magic 3.0 重建

* Sun Nov 25 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.2-1
- Update to 0.2.2
- Drop upstreamed patches
- Add patch to fix empty lxlauncher

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.2.1-10
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.1-8
- Use workaround for build loop again (#661008)
- Fix segfault if a window manager returns no data for current desktop

* Thu Jun 03 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.1-7
- Proper fix for build loop (#539147)

* Sat Feb 27 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.1-6
- Rebuild for menu-cache 0.3.2 soname bump

* Sun Feb 21 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.1-5
- Fix for the new behavior of menu-cache 0.3.0

* Wed Feb 17 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.1-4
- Add patch to fix DSO linking (#565072)

* Mon Nov 23 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.1-3
- Workaround for infinite loop that causes FTBFS (#539147)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 07 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1
- Switch from libgnome-menu to menu-cache

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jun 21 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.2-1
- Update to 0.2
- Remove empty ChangeLog

* Mon May 12 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.6-1
- Initial Fedora RPM
