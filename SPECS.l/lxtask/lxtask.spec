Name:           lxtask
Version:        0.1.4
Release:        4%{?dist}
Summary:        Lightweight and desktop independent task manager
Summary(zh_CN.UTF-8): 轻量及桌面无关的任务管理器

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            http://lxde.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz

# https://bugzilla.redhat.com/show_bug.cgi?id=732182
# https://sourceforge.net/tracker/?func=detail&aid=3424325&group_id=180858&atid=894869
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxtask;a=commit;h=be8168d3
Patch0:         lxtask-0.1.4-remove-timer.patch

# https://sourceforge.net/tracker/?func=detail&aid=3469683&group_id=180858&atid=894871
# modified version of
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxtask;a=commit;h=5ff47b84
# but with changes to po files stripped out
Patch1:         lxtask-0.1.4-show-full-cmdline.patch

# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxtask;a=commit;h=6cfc929d
Patch2:         lxtask-0.1.4-remove-column-auto-resize.patch

# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxtask;a=commit;h=2dbcf129
Patch3:         lxtask-0.1.4-fix-integer-overflow.patch

# https://sourceforge.net/tracker/?func=detail&aid=3490254&group_id=180858&atid=894871
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxtask;a=commit;h=0d63e935
Patch4:         lxtask-0.1.4-close-with-escape.patch

# contains all translations from GIT as of 2012-03-03
Patch5:         lxtask-0.1.4-update-translations.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel > 2.6, gettext, intltool, desktop-file-utils

%description
LXTask is a lightweight task manager derived from xfce4 task manager with all
xfce4 dependencies removed, some bugs fixed, and some improvement of UI. 
Although being part of LXDE, the Lightweight X11 Desktop Environment, it's 
totally desktop independent and only requires pure gtk+.

%description -l zh_CN.UTF-8
这是从 xfce4 的任务管理器中移除与 xfce4 相关内容的一个移植，并修正了一些 Bugs，
增强了界面。
尽管它是 LXDE 的一部分，但它是完全桌面无关的，只需要纯 gtk+。

%prep
%setup -q
%patch0 -p1 -b .remove-timer
%patch1 -p1 -b .full-cmdline
%patch2 -p1 -b .column-auto-resize
%patch3 -p1 -b .memory-overflow
%patch4 -p1 -b .close-with-escape
%patch5 -p1 -b .update-translations


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
desktop-file-install                      \
  --delete-original                                        \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications          \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop
magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop


%changelog
* Tue Jul 08 2014 Liu Di <liudidi@gmail.com> - 0.1.4-4
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 03 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.4-2
- Support full cmdline (LXDE #3469683)
- Close dialog with Escape button or CTRL+W (LXDE #3490254)
- Don't resize columns automatically
- Fix integer overflow
- Update translations from Pootle

* Sat Mar 03 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.4-1
- Update to 0.1.4
- Fix crash (#732182)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.1.3-3
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 15 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3

* Tue Apr 06 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2

* Thu Jul 30 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 06 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1

* Mon Feb 23 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1-2
- Fix categories in desktop file

* Sun May 04 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.1-1
- Initial Fedora RPM
