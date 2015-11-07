%global         basever 0.8.8

Name:           ccsm
Version:        0.8.4
Release:        16%{?dist}
Epoch:          1
Summary:        Plugin and configuration tool - Compiz Fusion Project

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://www.compiz.org/
Source0:        http://releases.compiz.org/%{version}/%{name}-%{version}.tar.bz2
BuildArch:      noarch

# libdrm is not available on these arches
ExcludeArch:    s390 s390x ppc64

Patch0:       ccsm_removeshebangs.patch
Patch1:       ccsm_widgets_filter.patch
Patch2:       ccsm_widget_dialog.patch
Patch3:       ccsm_primary-is-control.patch
Patch4:       ccsm_no-icons-and-text-in-main-screen.patch

BuildRequires:  python2-devel
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  intltool

Requires:       compizconfig-python >= %{version}
Requires:       libcompizconfig >= %{basever}
Requires:       python-sexy
Requires:       compiz-manager
Requires:       pygtk2 >= 2.10

%description
The Compiz Project brings 3D desktop visual effects that improve
usability of the X Window System and provide increased productivity
though plugins and themes contributed by the community giving a
rich desktop experience.

This package contains a gui configuration tool to configure Compiz
plugins and the composite window manager.

%prep
%setup -q
sed -i -e 's,Encoding=UTF-8,,g' ccsm.desktop.in ccsm.desktop.in
sed -i -e 's,Categories=Compiz;Settings;DesktopSettings;,Categories=Settings;DesktopSettings;,g' ccsm.desktop.in ccsm.desktop.in

%patch0 -p1 -b .removeshebangs
%patch1 -p1 -b .widgets_filter
%patch2 -p1 -b .widget_dialog
%patch3 -p1 -b .primary-is-control
%patch4 -p1 -b .no-icons

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT

# for fixing rpmlint error
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/md/LC_MESSAGES/ccsm.mo

%find_lang %{name}


%check
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/ccsm.desktop


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING VERSION
%{_bindir}/ccsm
%{_datadir}/applications/ccsm.desktop
%dir %{_datadir}/ccsm
%{_datadir}/ccsm/*
%{_datadir}/icons/hicolor/*/apps/ccsm.*
%dir %{python_sitelib}/ccm
%{python_sitelib}/ccm/*
%{python_sitelib}/ccsm-%{version}-py?.?.egg-info


%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1:0.8.4-16
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1:0.8.4-15
- 为 Magic 3.0 重建

* Tue Sep 24 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.4-14
- fix no icons and text in main screen

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 18 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.4-12
- add ccsm_primary-is-control.patch
- fix (#910977)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.4-10
- remove commented out require
- drop gettext BR

* Sun Dec 02 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.4-9
- remove compizconfig-backend-mateconf require

* Mon Oct 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.4-8
- build for fedora
- rename patches
- fix invalid-lc-messages-dir
- add Epoch tag

* Mon Oct 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.4-7
- remove python sitelib stuff

* Wed Sep 19 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.4-6
- improve spec file

* Tue May 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.4-5
- build for mate

