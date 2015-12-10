%define gettext_package gnome-terminal

%define glib2_version 2.33.0
%define gtk3_version 3.6.0
%define vte_version 0.34.0
%define desktop_file_utils_version 0.2.90

Summary: Terminal emulator for GNOME
Summary(zh_CN.UTF-8): GNOME 的终端模拟器
Name: gnome-terminal
Version:	3.18.2
Release: 1%{?dist}
License: GPLv3+ and GFDL
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://www.gnome.org/
#VCS: git:git://git.gnome.org/gnome-terminal
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0: http://download.gnome.org/sources/gnome-terminal/%{majorver}/gnome-terminal-%{version}.tar.xz
Source1: org.gnome.Terminal.gschema.override

Patch0: 0001-build-Don-t-treat-warnings-as-errors.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=755825
Patch1: gnome-terminal-symbolic-new-tab-icon.patch

Patch100: gnome-terminal-dark-transparency-notify.patch

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: GConf2-devel
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: vte3-devel >= %{vte_version}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: gnome-common
BuildRequires: autoconf automake libtool
BuildRequires: itstool
BuildRequires: dconf-devel
BuildRequires: libuuid-devel

Requires: gsettings-desktop-schemas

%description
gnome-terminal is a terminal emulator for GNOME. It features the ability to use
multiple terminals in a single window (tabs) and profiles support.

%description -l zh_CN.UTF-8
GNOME 下的终端模拟器，支持多标签窗口和配置文件。

%prep
%setup -q
%patch0 -p1 -b .warnings
%patch1 -p1 -b .new-tab-icon
%patch100 -p1 -b .dark-transparency-notify

%build
autoreconf -f -i
%configure --disable-static --disable-gterminal --disable-migration --with-gtk=3.0 --with-nautilus-extension

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-3.0/*.la

cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas

magic_rpm_clean.sh
%find_lang %{gettext_package} --with-gnome

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{gettext_package}.lang
%doc AUTHORS COPYING NEWS

%{_bindir}/gnome-terminal
%{_datadir}/applications/gnome-terminal.desktop
%{_libexecdir}/gnome-terminal-migration
%{_libexecdir}/gnome-terminal-server
%{_datadir}/dbus-1/services/org.gnome.Terminal.service
%{_datadir}/glib-2.0/schemas/org.gnome.Terminal.gschema.xml

%{_libdir}/nautilus/extensions-3.0/libterminal-nautilus.so
%{_datadir}/appdata/gnome-terminal.appdata.xml
%{_datadir}/gnome-shell/search-providers/gnome-terminal-search-provider.ini

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.18.2-1
- 更新到 3.18.2

* Wed Apr 09 2014 Liu Di <liudidi@gmail.com> - 3.12.0-1
- 更新到 3.12.0

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Tue Apr 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0.1-1
- Update to 3.8.0.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Thu Mar  7 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Tue Feb 26 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.2-3
- Bring back titlebars on maximized terminals

* Fri Jan 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.2-2
- Backport a fix for a crash in terminal_screen_container_style_updated

* Fri Jan 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Wed Jan 09 2013 Richard Hughes <hughsient@gmail.com> - 3.7.0-1
- Update to 3.7.0

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1.1-1
- Update to 3.4.1.1

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0.1-1
- Update to 3.4.0.1
- Avoid listing files twice in %%files

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.0-1
- Update to 3.3.0

* Thu Jan 12 2012 Matthias Clasen <mclasen@redhat.com> - 3.2.1-2
- Update license field (#639132)

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Apr 25 2011 Matthias Clasen <mclasen@redhat.com> 3.0.1-1
- Update to 3.0.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> 3.0.0-1
- Update to 3.0.0

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> 2.33.90-1
- Update to 2.33.90

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 2.33.5-3
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.5-1
- Update to 2.33.5

* Wed Jan 12 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.4-2
- Make the find dialog work again

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.4-1
- Update to 2.33.4

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.3-1
- Update to 2.33.3

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.2-2
- Rebuild against new gtk

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.2-1
- Update to 2.33.2
- Back to gtk3

* Fri Oct  8 2010 Owen Taylor <otaylor@redhat.com> - 2.33.0-3
- Revert back to a gtk2 build - the gtk3 build has major sizing issues
  (rhbz #641337)

* Thu Oct  7 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.0-2
- Build against gtk3

* Mon Oct  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.0-1
- Update to 2.33.0

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.91-1
- Update to 2.31.91

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.90-1
- Update to 2.31.90

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-1
- Update to 2.31.3

* Tue May  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.2-2
- Add more translations for search UI

* Tue May  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.2-1
- Update to 2.31.2
- Add translations for search UI

* Tue May  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.1-1
- Update to 2.31.1

* Mon Apr 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Thu Mar 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.92-1
- Update to 2.29.92

* Sun Feb 14 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.6-3
- Add missing libs

* Thu Jan 14 2010 Behdad Esfahbod <behdad@redhat.com> - 2.29.6-2
- Second try
- Drop stale patch

* Thu Jan 14 2010 Behdad Esfahbod <behdad@redhat.com> - 2.29.6-1
- Update to 2.29.6
