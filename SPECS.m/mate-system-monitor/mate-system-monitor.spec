Name:           mate-system-monitor
Version: 1.11.0
Release: 2%{?dist}
Summary:        Process and resource monitor
Summary(zh_CN.UTF-8): 进程和资源监视器

License:        GPLv2+
URL:            http://mate-desktop.org
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://pub.mate-desktop.org/releases/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires: dbus-glib-devel
BuildRequires: desktop-file-utils
BuildRequires: gtk2-devel
BuildRequires: gtkmm24-devel
BuildRequires: libgtop2-devel
BuildRequires: librsvg2-devel
BuildRequires: libwnck-devel
BuildRequires: libxml2-devel
BuildRequires: mate-common
BuildRequires: mate-icon-theme-devel


%description
mate-system-monitor allows to graphically view and manipulate the running
processes on your system. It also provides an overview of available resources
such as CPU and memory.

%description -l zh_CN.UTF-8
进程和资源监视器。

%prep
%setup -q

%build
%configure \
        --disable-static \
        --with-gtk=2.0 \
        --disable-schemas-compile 

make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --delete-original             \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications    \
  $RPM_BUILD_ROOT%{_datadir}/applications/mate-system-monitor.desktop

# remove needless gsettings convert file
rm -f  $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-system-monitor.convert
magic_rpm_clean.sh
%find_lang %{name} --with-gnome --all-name

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS NEWS COPYING README
%{_bindir}/mate-system-monitor
%{_datadir}/applications/mate-system-monitor.desktop
%{_datadir}/pixmaps/mate-system-monitor/
%{_datadir}/glib-2.0/schemas/org.mate.system-monitor.*.xml
%{_mandir}/man1/*


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.11.0-2
- 更新到 1.11.0

* Mon Aug 11 2014 Liu Di <liudidi@gmail.com> - 1.9.0-2
- 为 Magic 3.0 重建

* Tue Jul 15 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0 release
- drop runtime require mate-desktop, no need of it

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-2
- rebuild for libgtop2 soname bump

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Thu Jan 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-1
- update to 1.7.0 release
- add --with-gnome --all-name for find language
- re-worked BR's
- re-worked configure flags
- re-worked file section
- remove usage of hardlink, no need anymore

* Fri Aug 02 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Bump to 1.6.1
- Drop unused patches
- Add disable-schemas-compile configure flag
- Update man page in directive in files section

* Fri Jul 26 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-2
- add upstream patch to fix rhbz (#888696)
- add upstream patch to add manpages
- clean up BRs
- use hardlink to save space by linking identical images in translated docs
- remove --with-gnome find language flag
- remove needless gsettings convert file

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Sun Mar 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.5.1-1
- Latest upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-2
- drop deprecated mate-vfs BR

* Thu Nov 08 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release

* Fri Oct 19 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-2
- add build requires libxml2-devel

* Thu Oct 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-1
- Initial build

