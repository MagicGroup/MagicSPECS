%define glib2_version           2.6.0
%define dbus_version            0.90
%define dbus_glib_version       0.70
%define polkit_version          0.92

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Summary: System daemon for tracking users, sessions and seats
Name: ConsoleKit
Version: 0.4.5
Release: 7%{?dist}
License: GPLv2+
Group: System Environment/Libraries
URL: http://www.freedesktop.org/wiki/Software/ConsoleKit
Source0: http://www.freedesktop.org/software/ConsoleKit/dist/ConsoleKit-%{version}.tar.bz2
# Convert to new upstart syntax
Patch0: ConsoleKit-0.4.1-upstart06.patch
Patch1: ConsoleKit-aarch64.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}
Conflicts: upstart < 0.6.0
Conflicts: filesystem < 3

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: dbus-devel  >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: polkit-devel >= %{polkit_version}
BuildRequires: pam-devel
BuildRequires: libX11-devel
BuildRequires: zlib-devel
BuildRequires: xmlto
BuildRequires: automake, autoconf, libtool

%description
ConsoleKit is a system daemon for tracking what users are logged
into the system and how they interact with the computer (e.g.
which keyboard and mouse they use).

It provides asynchronous notification via the system message bus.

%package x11
Summary: X11-requiring add-ons for ConsoleKit
License: GPLv2+
Group: Development/Libraries
Requires: %name = %{version}-%{release}
Requires: libX11

%description x11
ConsoleKit contains some tools that require Xlib to be installed,
those are in this separate package so server systems need not install
X. Applications (such as xorg-x11-xinit) and login managers (such as
gdm) that need to register their X sessions with ConsoleKit needs to
have a Requires: for this package.

%package libs
Summary: ConsoleKit libraries
License: MIT
Group: Development/Libraries
Requires: pam
Requires: dbus >= %{dbus_version}

%description libs
This package contains libraries and a PAM module for interacting
with ConsoleKit.

%package devel
Summary: Development files for ConsoleKit
License: MIT
Group: Development/Libraries
Requires: dbus-devel >= %{dbus_version}
Requires: pkgconfig

%description devel
This package contains headers and libraries needed for
developing software that is interacting with ConsoleKit.

%package docs
Summary: Developer documentation for ConsoleKit
Group: Development/Libraries
Requires: %name = %{version}-%{release}
#BuildArch: noarch

%description docs
This package contains developer documentation for ConsoleKit.

%prep
%setup -q
%patch0 -p1 -b .upstart06
%patch1 -p1

%build
%configure --with-pid-file=%{_localstatedir}/run/console-kit-daemon.pid --enable-pam-module --with-pam-module-dir=/%{_lib}/security --enable-docbook-docs --docdir=%{_pkgdocdir}

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_lib}/security/*.a
rm -f $RPM_BUILD_ROOT/%{_lib}/security/*.la

# make sure we don't package a history log
rm -f $RPM_BUILD_ROOT/%{_var}/log/ConsoleKit/history

# The sample upstart files are good enough for us.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init
cp data/ck-log-system-{start,stop,restart}.conf $RPM_BUILD_ROOT%{_sysconfdir}/init

cp README AUTHORS NEWS COPYING $RPM_BUILD_ROOT%{_pkgdocdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/log/ConsoleKit/history ]; then
       chmod a+r /var/log/ConsoleKit/history
fi
if [ $1 -eq 1 ]; then
        /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ]; then
        /bin/systemctl stop console-kit-daemon.service >/dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README
%doc %{_pkgdocdir}/AUTHORS
%doc %{_pkgdocdir}/NEWS
%doc %{_pkgdocdir}/COPYING
%{_sysconfdir}/dbus-1/system.d/*
%dir %{_sysconfdir}/init
%config(noreplace) %{_sysconfdir}/init/*
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/polkit-1/actions/*.policy
%dir %{_sysconfdir}/ConsoleKit
%dir %{_sysconfdir}/ConsoleKit/seats.d
%dir %{_sysconfdir}/ConsoleKit/run-seat.d
%dir %{_sysconfdir}/ConsoleKit/run-session.d
%dir %{_prefix}/lib/ConsoleKit
%dir %{_prefix}/lib/ConsoleKit/scripts
%dir %{_prefix}/lib/ConsoleKit/run-seat.d
%dir %{_prefix}/lib/ConsoleKit/run-session.d
%ghost %dir %{_var}/run/ConsoleKit
%attr(755,root,root) %dir %{_var}/log/ConsoleKit
%config %{_sysconfdir}/ConsoleKit/seats.d/00-primary.seat
%{_sbindir}/console-kit-daemon
%{_sbindir}/ck-log-system-restart
%{_sbindir}/ck-log-system-start
%{_sbindir}/ck-log-system-stop
%{_bindir}/ck-history
%{_bindir}/ck-launch-session
%{_bindir}/ck-list-sessions
%{_prefix}/lib/ConsoleKit/scripts/*
%{_prefix}/lib/systemd/system/console-kit-daemon.service
%{_prefix}/lib/systemd/system/console-kit-log-system-start.service
%{_prefix}/lib/systemd/system/console-kit-log-system-stop.service
%{_prefix}/lib/systemd/system/console-kit-log-system-restart.service
%{_prefix}/lib/systemd/system/basic.target.wants/console-kit-log-system-start.service
%{_prefix}/lib/systemd/system/halt.target.wants/console-kit-log-system-stop.service
%{_prefix}/lib/systemd/system/poweroff.target.wants/console-kit-log-system-stop.service
%{_prefix}/lib/systemd/system/reboot.target.wants/console-kit-log-system-restart.service
%{_prefix}/lib/systemd/system/kexec.target.wants/console-kit-log-system-restart.service

%files x11
%defattr(-,root,root,-)
%{_libexecdir}/*

%files libs
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*
/%{_lib}/security/*.so
%{_mandir}/man8/pam_ck_connector.8.gz

%files devel
%defattr(-,root,root,-)

%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/dbus-1/interfaces/org.freedesktop.ConsoleKit.*.xml

%files docs
%defattr(-,root,root,-)
%doc %dir %{_pkgdocdir}/spec
%doc %{_pkgdocdir}/spec/*

%changelog
* Mon Aug 12 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.4.5-7
- Install docs to %%{_pkgdocdir} where available (#993708).

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 29 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 0.4.5-5
- Fix aarch64 support (925181)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb  7 2012 Lennart Poettering <lpoetter@redhat.com> - 0.4.5-2
- Forward port changes from f15 which were never applied to master

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue May  3 2011 Lennart Poettering <lpoetter@redhat.com> - 0.4.5-1
- New upstream release

* Thu Feb 17 2011 Lennart Poettering <lpoetter@redhat.com> - 0.4.4-1
- New upstream release

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 0.4.3-4
- Co-own /etc/init directory (#645082)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Matthias Clasen <mclasen@redhat.com> - 0.4.3-2
- %%ghost /var/run content

* Wed Nov 17 2010 Lennart Poettering <lpoetter@redhat.com> - 0.4.3-1
- New upstream

* Tue Oct 05 2010 jkeating - 0.4.2-2.1
- Rebuilt for gcc bug 634757

* Tue Sep 14 2010 Lennart Poettering <lpoetter@redhat.com> - 0.4.2-2
- Fix systemd execution ordering

* Fri Sep  3 2010 Lennart Poettering <lpoetter@redhat.com> - 0.4.2-1
- New upstream release

* Wed Jan 20 2010 Ray Strode <rstrode@redhat.com> 0.4.1-4
- Register object methods with dbus-glib before taking bus name
  (fix 545267)

* Tue Dec 15 2009 Matthias Clasen <mclasen@redhat.com> 0.4.1-3
- Don't daemonize when activated

* Wed Dec  9 2009 Bill Nottingham <notting@redhat.com> 0.4.1-2
- Adjust for upstart 0.6

* Tue Sep 29 2009 Jon McCann <jmccann@redhat.com> 0.4.1-1
- Update to 0.4.1

* Fri Jul 31 2009 Matthias Clasen <mclasen@redhat.com> 0.3.1-2
- Fix a small memory leak

* Fri Jul 31 2009 Ray Strode <rstrode@redhat.com> 0.3.1-1
- Update to 0.3.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Ray Strode  <rstrode@redhat.com> - 0.3.0-11
- Rebuild

* Fri Jun 12 2009 Matthias Clasen  <mclasen@redhat.com> - 0.3.0-10
- Update dbus configuration for new api

* Mon May 11 2009 Matthias Clasen  <mclasen@redhat.com> - 0.3.0-9
- Port to PolicyKit 1

* Tue Apr 21 2009 Matthias Clasen  <mclasen@redhat.com> - 0.3.0-8
- Fix a warning on login (#496636)

* Wed Apr  8 2009 Matthias Clasen  <mclasen@redhat.com> - 0.3.0-7
- Allow GetSessions calls in the dbus policy

* Fri Feb 27 2009 Matthias Clasen  <mclasen@redhat.com> - 0.3.0-6
- Fix the build

* Tue Feb 24 2009 Matthias Clasen  <mclasen@redhat.com> - 0.3.0-5
- Make -docs noarch

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 14 2009 Colin Walters <walters@verbum.org> - 0.3.0-4
- Add patch to fix up dbus permissions

* Fri Nov 21 2008 Matthias Clasen  <mclasen@redhat.com> - 0.3.0-3
- Tweak descriptions

* Tue Sep 16 2008 Ray Strode  <rstrode@redhat.com> - 0.3.0-2
- Grab X server display device from XFree86_VT root window property,
  if X server doesn't have a controlling terminal.

* Wed Jul 30 2008 Jon McCann  <jmccann@redhat.com> - 0.3.0-1
- Update to 0.3.0

* Tue Jul 22 2008 Jon McCann  <jmccann@redhat.com> - 0.2.11-0.2008.07.22.2
- Update to a new snapshot

* Tue Jul 22 2008 Jon McCann  <jmccann@redhat.com> - 0.2.11-0.2008.07.22.1
- Update to snapshot

* Mon Jul 21 2008 Jon McCann  <jmccann@redhat.com> - 0.2.11-0.2008.07.21.2
- Fix file list

* Mon Jul 21 2008 Jon McCann  <jmccann@redhat.com> - 0.2.11-0.2008.07.21
- Update to snapshot

* Sat Apr  5 2008 Matthias Clasen  <mclasen@redhat.com> - 0.2.10-3
- Return PolicyKit results

* Fri Mar 14 2008 Matthias Clasen  <mclasen@redhat.com> - 0.2.10-2
- Fix trivial dir ownership issue

* Mon Feb 25 2008 Jon McCann  <jmccann@redhat.com> - 0.2.10-1
- Update to 0.2.10

* Tue Feb 12 2008 Jon McCann  <jmccann@redhat.com> - 0.2.9-1
- Update to 0.2.9

* Mon Feb 11 2008 Jon McCann  <jmccann@redhat.com> - 0.2.8-1
- Update to 0.2.8

* Wed Jan 30 2008 Jon McCann  <jmccann@redhat.com> - 0.2.7-1
- Update to 0.2.7

* Thu Jan 24 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.2.6-3
- Fix Requires

* Thu Jan 24 2008 Jon McCann  <jmccann@redhat.com> - 0.2.6-2
- Require libz for log decompression

* Thu Jan 24 2008 Jon McCann  <jmccann@redhat.com> - 0.2.6-1
- Update to 0.2.6

* Sun Nov 11 2007 Matthias Clasen  <mclasen@redhat.com> - 0.2.3-3
- Correct the URL (#375571)

* Mon Oct 22 2007 Matthias Clasen  <mclasen@redhat.com> - 0.2.3-2
- Rebuild against new dbus-glib

* Tue Sep 18 2007 Matthias Clasen  <mclasen@redhat.com> - 0.2.3-1
- Update to 0.2.3

* Mon Sep 17 2007 Matthias Clasen  <mclasen@redhat.com> - 0.2.2-1
- Update to 0.2.2

* Mon Aug  6 2007 Matthias Clasen  <mclasen@redhat.com> - 0.2.1-4
- Update license field

* Fri Jul  6 2007 Matthias Clasen  <mclasen@redhat.com> - 0.2.1-3
- Add LSB header to init script (#246894)

* Mon Apr 16 2007 David Zeuthen <davidz@redhat.com> - 0.2.1-2
- Set doc directory correctly

* Mon Apr 16 2007 David Zeuthen <davidz@redhat.com> - 0.2.1-1
- Update to upstream release 0.2.1
- Drop the patch to daemonize properly as that was merged upstream

* Mon Apr 02 2007 David Zeuthen <davidz@redhat.com> - 0.2.1-0.git20070402
- Update to git snapshot to get a lot of bug fixes
- Use libX11 rather than gtk2 to verify X11 sessions; update BR and R
- Split X11-using bits into a new subpackage ConsoleKit-x11 (#233982)
- Use correct location for PAM module on 64-bit (#234545)
- Build developer documentation and put them in ConsoleKit-docs

* Mon Mar 19 2007 David Zeuthen <davidz@redhat.com> - 0.2.0-2
- BR gtk2-devel and make ConsoleKit Require gtk2 (could just be
  libX11 with a simple patch)

* Mon Mar 19 2007 David Zeuthen <davidz@redhat.com> - 0.2.0-1
- Update to upstream release 0.2.0
- Daemonize properly (#229206)

* Sat Mar  3 2007 David Zeuthen <davidz@redhat.com> - 0.1.3-0.git20070301.1
- Allow caller to pass uid=0 in libck-connector

* Thu Mar  1 2007 David Zeuthen <davidz@redhat.com> - 0.1.3-0.git20070301
- Update to git snapshot
- Drop all patches as they are committed upstream
- New tool ck-list-sessions
- New -libs subpackage with run-time libraries and a PAM module
- New -devel subpackage with headers

* Tue Feb  6 2007 David Zeuthen <davidz@redhat.com> - 0.1.0-5%{?dist}
- Start ConsoleKit a bit earlier so it starts before HAL (98 -> 90)
- Minimize stack usage so VIRT size is more reasonable (mclasen)
- Make session inactive when switching to non-session (davidz)

* Fri Jan 12 2007 Matthias Clasen <mclasen@redhat.com> - 0.1.0-4
- Don't mark initscripts %%config
- Use proper lock and pid ile names

* Fri Jan 12 2007 Matthias Clasen <mclasen@redhat.com> - 0.1.0-3
- More package review feedback

* Fri Jan 12 2007 Matthias Clasen <mclasen@redhat.com> - 0.1.0-2
- Incorporate package review feedback

* Thu Jan 11 2007 Matthias Clasen <mclasen@redhat.com> - 0.1.0-1
- Update to the first public release 0.1.0
- Some spec cleanups

* Mon Oct 23 2006 David Zeuthen <davidz@redhat.com> - 0.0.3-1
- Initial build.
