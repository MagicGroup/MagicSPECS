Name:		system-setup-keyboard
Version:	0.8.8
Release:	5%{?dist}
Summary:	xorg.conf keyboard layout callout

Group:		Applications/System
License:	MIT
URL:		http://git.fedorahosted.org/git/system-setup-keyboard.git/
Source0:	https://fedorahosted.org/released/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	glib2-devel
BuildRequires:	system-config-keyboard

Requires:	xorg-x11-server-Xorg >= 1.7.99
Requires:	systemd-units
Conflicts:	xorg-x11-server-Xorg < 1.6.0-7

Provides:	fedora-setup-keyboard = %{version}-%{release}
Obsoletes:	fedora-setup-keyboard < 0.7

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
%{name} is a daemon to monitor the keyboard layout configured in 
/etc/sysconfig/keyboard and transfer this into the matching xorg.conf.d
snippet.

%prep
%setup -q
sed -i 's/\/lib\/systemd/\/usr\/lib\/systemd/g' Makefile

%build
make CFLAGS="%{optflags}" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/X11/xorg.conf.d
touch $RPM_BUILD_ROOT/%{_sysconfdir}/X11/xorg.conf.d/00-system-setup-keyboard.conf
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq 1 ]; then
    # Package install, not upgrade
	/usr/bin/systemctl enable system-setup-keyboard.service >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /usr/bin/systemctl disable system-setup-keyboard.service >/dev/null 2>&1 || :
    /usr/bin/systemctl stop system-setup-keyboard.service > /dev/null 2>&1 || :
fi

%postun  
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /usr/bin/systemctl try-restart system-setup-keyboard.service >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_sysconfdir}/init/%{name}.conf
%{_mandir}/man1/system-setup-keyboard.1*
%{_prefix}/lib/systemd/system/system-setup-keyboard.service
# Own directories to avoid hard requirement on a upstart
# can be removed once we decided to stay with systemd
%dir %{_sysconfdir}/init/

%ghost %{_sysconfdir}/X11/xorg.conf.d/00-system-setup-keyboard.conf

%doc COPYING

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.8.8-5
- 为 Magic 3.0 重建

* Sun Apr 22 2012 Liu Di <liudidi@gmail.com> - 0.8.8-4
- 为 Magic 3.0 重建

* Sun Apr 22 2012 Liu Di <liudidi@gmail.com> - 0.8.8-3
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.8.8-1
- 0.8.8 release - Don't ignore the keytable (#744641)

* Wed Sep 28 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.8.7-2
- Oops. Drop the man page permissions patch, it's upstream now.

* Wed Sep 28 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.8.7-1
- 0.8.7 release - fix suspend/resume errors (#741800)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 08 2011 Adel Gadllah <adel.gadllah@gmail.com> 0.8.6-4
- Fix systemd support to match latest draft

* Mon Jan 17 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.8.6-3
- Pull in two changes from F14 branch

* Mon Jan 17 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.8.6-2
- Fix man page permissions

* Tue Oct 05 2010 jkeating - 0.8.6-2.1
- Rebuilt for gcc bug 634757

* Tue Sep 14 2010 Bill Nottingham <notting@redhat.com> 0.8.6-2
- Flip requires from systemd to the correct systemd-units

* Sat Aug 28 2010  Adel Gadllah <adel.gadllah@gmail.com> 0.8.6-1
- 0.8.6 release - systemd support

* Mon Jun 21 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.8.5-2
- Update description, we don't use HAL anymore after all.
- %ghost the generated 00-system-setup-keyboard.conf file.

* Thu Apr 15 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.8.5-1
- 0.8.5 release - uses /etc/X11/xorg.conf.d as default directory.

* Thu Mar 25 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.8.4-1
- 0.8.4 release. Adds layout conversion table in man page. (related #574301)

* Fri Mar 12 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.8.3-1
- 0.8.3 release, now includes man page.

* Sat Feb 27 2010 Adel Gadllah <adel.gadllah@gmail.com> 0.8.2-1
- 0.8.2 release
- Actually install the upstart config file

* Thu Feb 18 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.8.1-1
- 0.8.1 release (makefile fixes)

* Tue Feb 16 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.8-1
- 0.8 release (xorg.conf.d support)
- drop HAL requires.

* Tue Feb 09 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.7-1
- Rename to system-setup-keyboard, update the URL and Source0 accordingly.
  Obsoletes fedora-setup-keyboard.

* Sat Dec 26 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.6-1
- 0.6 release
- Fixes RH #545970

* Fri Nov 20 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.5-1
- Patch merged upstream

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.4-4
- rhpl was replaced by system-config-keyboard.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 27 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.4-2
- Rebuild to pick up rhpl changes

* Mon Apr 13 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.4-1
- 0.4 release
- Dropped patch, merged upstream

* Thu Apr 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.3-4
- fedora-setup-keyboard-0.3-merge-terminate.patch: merge xkb options for
  termination.

* Thu Mar 05 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.3-3
- Conflict xorg-x11-server-Xorg < 1.6.0-7 (10-x11-keymap.fdi and
  fedora-setup-keyboard up to 1.6.0-5)

* Mon Mar 02 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.3-2
- Fix license tag

* Wed Feb 25 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.3-1
- 0.3 release
- Require hal

* Sat Feb 21 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.2-1
- Initial package
