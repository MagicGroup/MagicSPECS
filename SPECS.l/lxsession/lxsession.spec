# review https://bugzilla.redhat.com/show_bug.cgi?id=502404
# renamed from lxsession-lite. Original review at
# https://bugzilla.redhat.com/show_bug.cgi?id=442268

Name:           lxsession
Version:        0.4.6.1
Release:        9%{?dist}
Summary:        Lightweight X11 session manager
Summary(zh_CN.UTF-8): 轻量级的 X11 会话管理器

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            http://lxde.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
Patch0:         lxsession-0.4.1-dsofix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel > 2.6 dbus-glib-devel
BuildRequires:  docbook-utils intltool gettext
# name changed back from lxsession-lite to lxsession
Obsoletes:      lxsession-lite <= 0.3.6-6
Provides:       lxsession-lite = %{version}-%{release}
# lxde-settings-daemon was merged into lxsession
Obsoletes:      lxde-settings-daemon <= 0.4.1-2
Provides:       lxde-settings-daemon = 0.4.1-3
# required for suspend and hibernate
Requires:       ConsoleKit
Requires:       upower


%description
LXSession is a standard-compliant X11 session manager with shutdown/
reboot/suspend support via HAL. In connection with gdm it also supports user 
switching.

LXSession is derived from XSM and is developed as default X11 session manager 
of LXDE, the Lightweight X11 Desktop Environment. Though being part of LXDE, 
it's totally desktop-independent and only has few dependencies.

%description -l zh_CN.UTF-8
轻量级的 X11 会话管理器。

%prep
%setup -q

%build
%configure --enable-man
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
magic_rpm_clean.sh
%find_lang %{name}
mkdir -p -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/xdg/%{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README desktop.conf.example
%{_bindir}/%{name}
%{_bindir}/%{name}-logout
%{_bindir}/lxlock
%{_datadir}/%{name}/
%{_mandir}/man*/%{name}*.*
# we need to own
%dir %{_sysconfdir}/xdg/%{name}

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.4.6.1-9
- 为 Magic 3.0 重建

* Tue Jul 08 2014 Liu Di <liudidi@gmail.com> - 0.4.6.1-8
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 0.4.6.1-7
- 为 Magic 3.0 重建

* Tue Jan 15 2013 Liu Di <liudidi@gmail.com> - 0.4.6.1-6
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 21 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.6.1-3
- Require ConsoleKit (#800658)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.6.1-1
- Update to 0.4.6.1
- Require upower (#755376)

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.4.5-4
- Rebuild for new libpng

* Fri Mar 25 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.5-3
- No longer require hal (#688959)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 17 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.5-1
- Update to 0.4.5

* Tue Apr 06 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.4-1
- Update to 0.4.4

* Sat Mar 20 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.3-1
- Update to 0.4.3
- Fix labels of the German logout dialog

* Mon Mar 08 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.2-1
- Update to 0.4.2

* Wed Feb 17 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.1-2
- Add patch to fix DSO linking (#564645)

* Fri Dec 11 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.1-1
- Update to 0.4.1

* Tue Dec 08 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0
- Obsolete lxde-settings-deamon

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.8-1
- Update to 0.3.8 and remove all patches
- Rename back to lxsession again (upstream)

* Mon Apr 27 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.6-5
- Fix Session name (Andrew Lee)

* Mon Apr 27 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.6-4
- Support user switching also with newer gdm
- Add patch to fix icon search path (Marty Jack)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 09 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.6-2
- Preserve timestamps during install

* Thu Jun 12 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.6-1
- Update to 0.3.6
- Remove docbook hack

* Sun Apr 20 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.5-1
- Switch to LXSession lite and drop xorg-x11-xsm requirement again.

* Sat Apr 12 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.2-2
- Require xorg-x11-xsm

* Sat Apr 12 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.2-1
- Update to 0.3.2

* Mon Mar 10 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.0-1
- Initial Fedora RPM
