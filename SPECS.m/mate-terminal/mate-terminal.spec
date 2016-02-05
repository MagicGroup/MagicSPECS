Summary:        Terminal emulator for MATE
Summary(zh_CN.UTF-8): MATE 的终端模拟器
Name:           mate-terminal
Version: 1.12.1
Release: 1%{?dist}
License:        GPLv3+
URL:            http://mate-desktop.org
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://pub.mate-desktop.org/releases/%{majorver}/%{name}-%{version}.tar.xz

#Default to black bg white fg, unlimited scrollback, turn off use theme default
Patch0:        mate-terminal_better_defaults.patch

BuildRequires: dconf-devel
BuildRequires: desktop-file-utils
BuildRequires: glib2-devel
BuildRequires: gtk2-devel
BuildRequires: libSM-devel
BuildRequires: mate-common
BuildRequires: vte-devel
BuildRequires: mate-desktop-devel

# needed to get a gsettings schema, rhbz #908105
Requires:      mate-desktop-libs
Requires:      gsettings-desktop-schemas

%description
Mate-terminal is a terminal emulator for MATE. It supports translucent
backgrounds, opening multiple terminals in a single window (tabs) and
clickable URLs.

%description -l zh_CN.UTF-8
MATE 的终端模拟器。

%prep
%setup -q
%patch0 -p1

%build
%configure --disable-static                \
           --with-gtk=2.0                  \
           --disable-schemas-compile       

make %{?_smp_mflags} V=1


%install
%{make_install}

desktop-file-install                                                    \
        --delete-original                                               \
        --dir=%{buildroot}%{_datadir}/applications                      \
%{buildroot}%{_datadir}/applications/mate-terminal.desktop
magic_rpm_clean.sh
%find_lang %{name} --with-gnome --all-name


%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README ChangeLog
%{_bindir}/mate-terminal
%{_bindir}/mate-terminal.wrapper
%{_datadir}/mate-terminal/
%{_datadir}/applications/mate-terminal.desktop
%{_datadir}/glib-2.0/schemas/org.mate.terminal.gschema.xml
%{_datadir}/appdata/mate-terminal.appdata.xml
%{_mandir}/man1/*


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.11.0-2
- 更新到 1.11.0

* Mon Aug 11 2014 Liu Di <liudidi@gmail.com> - 1.9.0-2
- 为 Magic 3.0 重建

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Sat Jan 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1 release
- remove obsolete configure flags
- clean up BR's
- use modern 'make install' macro
- add --with-gnome --all-name for find language
- clean up file section

* Fri Dec 06 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Thu Aug 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-11
- switch to runtime require mate-desktop-libs, fix rhbz #908105

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1.9
- another fix for better default patch

* Sat Jun 29 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1.8
- add runtime require gsettings-desktop-schemas to have proxy support
- from gnome gsettings schema

* Fri Jun 28 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1.7
- improve better_default patch
- remove BR gsettings-desktop-schemas-devel
- remove update-desktop-database scriptlet

* Mon Jun 17 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-6
- Update patch for bold colors

* Fri May 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-5
- Update patch again

* Fri May 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-4
- Update patch (again) to really fix annoying default settings

* Fri May 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-3
- Update patch to really fix annoying default settings
- New defaults: unlimited scrollback black bg

* Fri May 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-2
- Add patch to fix annoying default settings

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Bugfix release. See Cangelog.

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to stable 1.6.0 release

* Tue Mar 26 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Update to latest upstream release

* Mon Feb 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-3
- Add hard requires for mate-desktop to fix RHBZ #908105

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 19 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-1
- Update to latest upstream release
- Special thanks to Shawn Sterling for his help

* Wed Oct 24 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-4
- Add requires libmate

* Mon Oct 15 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-3
- add build requires rarian-compat

* Mon Oct 15 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-2
- remove surplus build requires

* Sun Oct 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-1
- initial build
