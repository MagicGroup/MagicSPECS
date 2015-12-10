%global _changelog_trimtime %(date +%s -d "1 year ago")


Name:		xdg-user-dirs
Version:	0.15
Release:	7%{?dist}
Summary:	Handles user special directories
Summary(zh_CN.UTF-8): 处理用户指定的目录

Group:		User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:	GPLv2+ and MIT
URL:		http://freedesktop.org/wiki/Software/xdg-user-dirs
Source0:	http://user-dirs.freedesktop.org/releases/%{name}-%{version}.tar.gz
Source1:	xdg-user-dirs.sh

# use fuzzy translations (for Downloads)
# https://bugzilla.redhat.com/show_bug.cgi?id=532399
Patch0:		use-fuzzy.patch

BuildRequires:	gettext
BuildRequires:  docbook-style-xsl
BuildRequires:  libxslt
Requires:	%{_sysconfdir}/X11/xinit/xinitrc.d

%description
Contains xdg-user-dirs-update that updates folders in a users
homedirectory based on the defaults configured by the administrator.

%description -l zh_CN.UTF-8
处理用户指定的目录。

%prep
%setup -q
%patch0 -p1 -b .use-fuzzy

%build
%configure
make %{?_smp_mflags}

cd po
touch *.po
make update-gmo

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d
magic_rpm_clean.sh 
%find_lang %name || :


%files -f %{name}.lang
%doc NEWS AUTHORS README COPYING
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/xdg/user-dirs.conf
%config(noreplace) %{_sysconfdir}/xdg/user-dirs.defaults
%{_sysconfdir}/X11/xinit/xinitrc.d/*
%{_mandir}/man1/*
%{_mandir}/man5/*


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 0.15-7
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.15-6
- 为 Magic 3.0 重建

* Thu Oct 22 2015 Liu Di <liudidi@gmail.com> - 0.15-5
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 0.15-4
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 0.15-3
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 27 2013 Matthias Clasen <mclasen@redhat.com> - 0.15-1
- Man pages
- Translation updates
- Trim %%changelog

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue May  3 2011 Alexander Larsson <alexl@redhat.com> - 0.14-1
- Update to 0.14 (new translations)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.13-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Alexander Larsson <alexl@redhat.com> - 0.13-1
- Update to 0.13 with new translations

* Wed Mar 24 2010 Tomas Bzatek <tbzatek@redhat.com> - 0.12-1
- Update to 0.12 which only has a few new translations of Downloads
- Use fuzzy translations (for Downloads)  (#532399)
- Fix a typo in README

* Fri Sep 25 2009 Alexander Larsson <alexl@redhat.com> - 0.11-1
- Update to 0.11

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun May  4 2008 Matthias Clasen <mclasen@redhat.com> - 0.10-3
- Fix source url again
- Fix license tag

* Mon Mar 17 2008 Matthias Clasen <mclasen@redhat.com> - 0.10-2
- Fix Source URL

* Tue Feb 12 2008 Alexander Larsson <alexl@redhat.com> - 0.10-1
- Update to 0.10 (new translations)

* Tue Aug 21 2007 Alexander Larsson <alexl@redhat.com> - 0.9-1
- Update to 0.9 (new translations)

* Tue May 29 2007 Matthias Clasen <mclasen@redhat.com> - 0.8-2
- Fix a possible crash.

* Wed May 16 2007  <alexl@redhat.com> - 0.8-1
- Update to 0.8, (only) fixing bug that always recreated deleted directories (#240139)

* Wed Apr 11 2007 Alexander Larsson <alexl@redhat.com> - 0.6-1
- Update to 0.6 (minor fixes)

* Mon Mar 26 2007 Alexander Larsson <alexl@redhat.com> - 0.5-1
- update to 0.5 (more translations)

* Wed Mar  7 2007 Alexander Larsson <alexl@redhat.com> - 0.4-1
- Update to 0.4

* Thu Mar  1 2007 Alexander Larsson <alexl@redhat.com> - 0.3-1
- Update to 0.3

* Fri Feb 23 2007 Alexander Larsson <alexl@redhat.com> - 0.2-1
- initial version
