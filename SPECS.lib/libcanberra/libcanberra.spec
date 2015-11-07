Name: libcanberra
Version: 0.30
Release: 5%{?dist}
Summary: Portable Sound Event Library
Summary(zh_CN.UTF-8): 可移植的声音事件库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source0: http://0pointer.de/lennart/projects/libcanberra/libcanberra-%{version}.tar.xz

License: LGPLv2+
Url: http://git.0pointer.de/?p=libcanberra.git;a=summary
BuildRequires: gtk2-devel
BuildRequires: gtk3-devel
BuildRequires: alsa-lib-devel
BuildRequires: libvorbis-devel
BuildRequires: libtool-ltdl-devel
BuildRequires: gtk-doc
BuildRequires: pulseaudio-libs-devel >= 0.9.15
BuildRequires: gstreamer-devel
BuildRequires: libtdb-devel
BuildRequires: gettext-devel
BuildRequires: systemd-devel
Requires: sound-theme-freedesktop
Requires: pulseaudio-libs >= 0.9.15
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
A small and lightweight implementation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).

%description -l zh_CN.UTF-8
小且轻理级的 XDG 声音主题标准实现。

%package gtk2
Summary: Gtk+ 2.x Bindings for libcanberra
Summary(zh_CN.UTF-8): %{name} 的 GTK+ 2.x 绑定
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name} = %{version}-%{release}
# Some other stuff is included in the gtk3 package, so always pull that in.
Requires: %{name}-gtk3 = %{version}-%{release}

%description gtk2
Gtk+ 2.x bindings for libcanberra

%description gtk2 -l zh_CN.UTF-8
%{name} 的 GTK+ 2.x 绑定。

%package gtk3
Summary: Gtk+ 3.x Bindings for libcanberra
Summary(zh_CN.UTF-8): %{name} 的 GTK+ 3.x 绑定
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name} = %{version}-%{release}

%description gtk3
Gtk+ 3.x bindings for libcanberra

%description gtk3 -l zh_CN.UTF-8
%{name} 的 GTK+ 3.x 绑定。

%package devel
Summary: Development Files for libcanberra Client Development
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: gtk2-devel

%description devel
Development Files for libcanberra Client Development

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%post
/usr/sbin/ldconfig
if [ $1 -eq 1 ]; then
        /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ]; then
        /usr/bin/systemctl --no-reload disable canberra-system-bootup.service canberra-system-shutdown.service canberra-system-shutdown-reboot.service >/dev/null 2>&1 || :
        /usr/bin/systemctl stop canberra-system-bootup.service canberra-system-shutdown.service canberra-system-shutdown-reboot.service >/dev/null 2>&1 || :
fi

%postun
/usr/sbin/ldconfig
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%post gtk2 -p /usr/sbin/ldconfig
%postun gtk2 -p /usr/sbin/ldconfig

%post gtk3 -p /usr/sbin/ldconfig
%postun gtk3 -p /usr/sbin/ldconfig

%prep
%setup -q

%build
%configure --disable-static --enable-pulse --enable-alsa --enable-null --enable-gstreamer --disable-oss --with-builtin=dso --with-systemdsystemunitdir=/usr/lib/systemd/system
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT \( -name *.a -o -name *.la \) -exec rm {} \;
rm $RPM_BUILD_ROOT%{_docdir}/libcanberra/README
magic_rpm_clean.sh

%files
%defattr(-,root,root)
%doc README LGPL
%{_libdir}/libcanberra.so.*
%dir %{_libdir}/libcanberra-%{version}
%{_libdir}/libcanberra-%{version}/libcanberra-alsa.so
%{_libdir}/libcanberra-%{version}/libcanberra-pulse.so
%{_libdir}/libcanberra-%{version}/libcanberra-null.so
%{_libdir}/libcanberra-%{version}/libcanberra-multi.so
%{_libdir}/libcanberra-%{version}/libcanberra-gstreamer.so
%{_prefix}/lib/systemd/system/canberra-system-bootup.service
%{_prefix}/lib/systemd/system/canberra-system-shutdown-reboot.service
%{_prefix}/lib/systemd/system/canberra-system-shutdown.service
%{_bindir}/canberra-boot

%files gtk2
%defattr(-,root,root)
%{_libdir}/libcanberra-gtk.so.*
%{_libdir}/gtk-2.0/modules/libcanberra-gtk-module.so

%files gtk3
%defattr(-,root,root)
%{_libdir}/libcanberra-gtk3.so.*
%{_libdir}/gtk-3.0/modules/libcanberra-gtk3-module.so
%{_libdir}/gtk-3.0/modules/libcanberra-gtk-module.so
%{_bindir}/canberra-gtk-play
%{_datadir}/gnome/autostart/libcanberra-login-sound.desktop
%{_datadir}/gnome/shutdown/libcanberra-logout-sound.sh
# co-own these directories to avoid requiring GDM (#522998)
%dir %{_datadir}/gdm/
%dir %{_datadir}/gdm/autostart/
%dir %{_datadir}/gdm/autostart/LoginWindow/
%{_datadir}/gdm/autostart/LoginWindow/libcanberra-ready-sound.desktop
# co-own these directories to avoid requiring g-s-d
%dir %{_libdir}/gnome-settings-daemon-3.0/
%dir %{_libdir}/gnome-settings-daemon-3.0/gtk-modules/
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/canberra-gtk-module.desktop

%files devel
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc
%{_includedir}/canberra-gtk.h
%{_includedir}/canberra.h
%{_libdir}/libcanberra-gtk.so
%{_libdir}/libcanberra-gtk3.so
%{_libdir}/libcanberra.so
%{_libdir}/pkgconfig/libcanberra-gtk.pc
%{_libdir}/pkgconfig/libcanberra-gtk3.pc
%{_libdir}/pkgconfig/libcanberra.pc
# co-own these directories to avoid requiring vala
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/libcanberra-gtk.vapi
%{_datadir}/vala/vapi/libcanberra.vapi

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.30-5
- 为 Magic 3.0 重建

* Fri Jul 11 2014 Liu Di <liudidi@gmail.com> - 0.30-4
- 更新到 0.30

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.29-4
- 为 Magic 3.0 重建

* Mon Jun 04 2012 Kay Sievers <kay@redhat.com> - 0.29-3
- rebuild for libudev1

* Tue May 15 2012 Lennart Poettering <lpoetter@redhat.com> - 0.29-2
- Various minor .spec file fixes

* Tue May 15 2012 Lennart Poettering <lpoetter@redhat.com> - 0.29-1
- New upstream
- Closes #744888, #696194

* Thu Feb 23 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.28-6
- Update systemd service file locations

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 08 2011 Adam Jackson <ajax@redhat.com> - 0.28-4
- Rebuild to break bogus libpng dep

* Thu Mar 24 2011 Christopher Aillon <caillon@redhat.com> - 0.28-3
- Workaround a hang (fdo#35024)

* Tue Mar  1 2011 Bill Nottingham <notting@redhat.com> - 0.28-2
- own gnome-settings-daemon desktop dir, don't require g-s-d

* Fri Feb 25 2011 Lennart Poettering <lpoetter@redhat.com> - 0.28-1
- New upstream release

* Fri Feb 18 2011 Lennart Poettering <lpoetter@redhat.com> - 0.27-1
- New upstream Release

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 0.26-8
- Rebuild against newer gtk

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 0.26-6
- Rebuild

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> 0.26-5
- Rebuild against newer gtk

* Fri Dec 3 2010 Matthias Clasen <mclasen@redhat.com> 0.26-4
- Rebuild against new gtk

* Mon Nov 1 2010 Matthias Clasen <mclasen@redhat.com> 0.26-3
- Rebuild against newer gtk3

* Mon Oct 4 2010 Lennart Poettering <lpoetter@redhat.com> 0.26-2
- Use final 0.26 tarball

* Mon Oct 4 2010 Lennart Poettering <lpoetter@redhat.com> 0.26-1
- New version 0.26

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> 0.25-3
- Co-own /usr/share/gtk-doc (#604379)

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> 0.25-2
- Rebuild

* Sun Jun 13 2010 Lennart Poettering <lpoetter@redhat.com> 0.25-1
- New version 0.25

* Sat Feb 20 2010 Lennart Poettering <lpoetter@redhat.com> 0.23-1
- New version 0.23

* Tue Oct 20 2009 Lennart Poettering <lpoetter@redhat.com> 0.22-1
- New version 0.22

* Fri Oct 16 2009 Lennart Poettering <lpoetter@redhat.com> 0.21-1
- New version 0.21

* Thu Oct 15 2009 Lennart Poettering <lpoetter@redhat.com> 0.20-1
- New version 0.20

* Wed Oct 14 2009 Lennart Poettering <lpoetter@redhat.com> 0.19-1
- New version 0.19

* Fri Sep 25 2009 Matthias Clasen <mclasen@redhat.com> - 0.18-2
- Don't require vala in -devel (#523473)

* Sat Sep 19 2009 Lennart Poettering <lpoetter@redhat.com> 0.18-1
- New version 0.18

* Wed Sep 16 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.17-2
- Don't require gdm in -gtk2 (#522998)

* Fri Sep 12 2009 Lennart Poettering <lpoetter@redhat.com> 0.17-1
- New version 0.17

* Thu Aug 27 2009 Lennart Poettering <lpoetter@redhat.com> 0.16-1
- New version 0.16

* Wed Aug 5 2009 Lennart Poettering <lpoetter@redhat.com> 0.15-2
- Fix mistag

* Wed Aug 5 2009 Lennart Poettering <lpoetter@redhat.com> 0.15-1
- New version 0.15

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 2 2009 Lennart Poettering <lpoetter@redhat.com> 0.14-2
- Upload the right tarball

* Thu Jul 2 2009 Lennart Poettering <lpoetter@redhat.com> 0.14-1
- New version 0.14

* Tue Jun 23 2009 Lennart Poettering <lpoetter@redhat.com> 0.13-1
- New version 0.13

* Tue Jun 16 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.12-2
- Rebuild for new libtdb.

* Mon Apr 13 2009 Lennart Poettering <lpoetter@redhat.com> 0.12-1
- New version 0.12

* Wed Apr 1 2009 Lennart Poettering <lpoetter@redhat.com> 0.11-9
- Another preview for 0.12

* Wed Feb 25 2009 Lennart Poettering <lpoetter@redhat.com> 0.11-8
- Add missing dependency on gettext-devel

* Wed Feb 25 2009 Lennart Poettering <lpoetter@redhat.com> 0.11-7
- Preview for 0.12

* Thu Feb  5 2009 Matthias Clasen  <mclasen@redhat.com> 0.11-6
- Fix up Requires (#484225)

* Wed Jan 21 2009 Lennart Poettering <lpoetter@redhat.com> 0.11-5
- New version

* Sun Dec 14 2008 Lennart Poettering <lpoetter@redhat.com> 0.10-4
- Moved login sound to "Application" startup phase.

* Thu Nov 13 2008 Matthias Clasen <mclasen@redhat.com> 0.10-3
- Rebuild

* Fri Oct 10 2008 Lennart Poettering <lpoetter@redhat.com> 0.10-2
- Drop libcanberra-gtk-module.sh since the gconf stuff is supported just fine in current gnome-session already.

* Mon Oct 6 2008 Lennart Poettering <lpoetter@redhat.com> 0.10-1
- New version

* Thu Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.9-1
- New version

* Thu Aug 28 2008 Lennart Poettering <lpoetter@redhat.com> 0.8-2
- Fix build-time dep on Gstreamer

* Thu Aug 28 2008 Lennart Poettering <lpoetter@redhat.com> 0.8-1
- New version

* Thu Aug 14 2008 Lennart Poettering <lpoetter@redhat.com> 0.7-1
- New version

* Mon Aug 4 2008 Lennart Poettering <lpoetter@redhat.com> 0.6-1
- New version

* Wed Jul 30 2008 Lennart Poettering <lpoetter@redhat.com> 0.5-4
- Really add versioned dependency on libpulse

* Wed Jul 30 2008 Lennart Poettering <lpoetter@redhat.com> 0.5-3
- Ship libcanberra-gtk-module.sh directly in CVS

* Wed Jul 30 2008 Lennart Poettering <lpoetter@redhat.com> 0.5-2
- Fix build

* Wed Jul 30 2008 Lennart Poettering <lpoetter@redhat.com> 0.5-1
- New version

* Mon Jul 28 2008 Lennart Poettering <lpoetter@redhat.com> 0.4-3
- Add versioned dependency on libpulse

* Sun Jul 27 2008 Lennart Poettering <lpoetter@redhat.com> 0.4-2
- Fix module name in libcanberra-gtk-module.sh

* Fri Jul 25 2008 Lennart Poettering <lpoetter@redhat.com> 0.4-1
- New version
- Install libcanberra-gtk-module.sh

* Mon Jun 16 2008 Lennart Poettering <lpoetter@redhat.com> 0.3-2
- Add dependency on sound-theme-freedesktop

* Fri Jun 13 2008 Lennart Poettering <lpoetter@redhat.com> 0.3-1
- Initial package, based on Colin Guthrie's Mandriva package
