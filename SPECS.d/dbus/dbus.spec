%global _hardened_build 1
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%define gettext_package dbus

%define expat_version           1.95.5
%define libselinux_version      1.15.2

%define dbus_user_uid           81

%define dbus_common_config_opts --enable-libaudit --enable-selinux=yes --with-init-scripts=redhat --with-system-pid-file=%{_localstatedir}/run/messagebus.pid --with-dbus-user=dbus --libdir=/%{_lib} --bindir=/bin --sysconfdir=/etc --exec-prefix=/ --libexecdir=/%{_lib}/dbus-1 --with-systemdsystemunitdir=/lib/systemd/system/ --docdir=%{_pkgdocdir} --enable-doxygen-docs --enable-xml-docs --disable-silent-rules

Summary: D-BUS message bus
Name: dbus
Epoch: 1
Version: 1.6.18
Release: 3%{?dist}
URL: http://www.freedesktop.org/software/dbus/
#VCS: git:git://git.freedesktop.org/git/dbus/dbus
Source0: http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.gz
Source2: 00-start-message-bus.sh
License: GPLv2+ or AFL
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libtool
BuildRequires: expat-devel >= %{expat_version}
BuildRequires: libselinux-devel >= %{libselinux_version}
BuildRequires: audit-libs-devel >= 0.9
BuildRequires: libX11-devel
BuildRequires: libcap-ng-devel
BuildRequires: gettext
BuildRequires: doxygen
BuildRequires: xmlto
BuildRequires: libxslt
BuildRequires:  systemd-units
Requires(post): systemd-units chkconfig
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires: libselinux%{?_isa} >= %{libselinux_version}
Requires: dbus-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires(pre): /usr/sbin/useradd

# Note: These is only required for --enable-tests; when bootstrapping,
# you can remove this and drop the --enable-tests configure argument.
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(dbus-glib-1)
BuildRequires: dbus-python
BuildRequires: pygobject2
BuildRequires: /usr/bin/Xvfb

# FIXME this should be upstreamed; need --daemon-bindir=/bin and --bindir=/usr/bin or something?
Patch0: bindir.patch
Patch1: 0001-name-test-Don-t-run-test-autolaunch-if-we-don-t-have.patch
Patch2: avoid-undefined-7c00ed22d9b5c33f5b33221e906946b11a9bde3b.patch

%description
D-BUS is a system for sending messages between applications. It is
used both for the system-wide message bus service, and as a
per-user-login-session messaging facility.

%package libs
Summary: Libraries for accessing D-BUS
Group: Development/Libraries

%description libs
This package contains lowlevel libraries for accessing D-BUS.

%package doc
Summary: Developer documentation for D-BUS
Group: Documentation
Requires: %{name} = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description doc
This package contains developer documentation for D-Bus along with
other supporting documentation such as the introspect dtd file.

%package devel
Summary: Development files for D-BUS
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
This package contains libraries and header files needed for
developing software that uses D-BUS.

%package x11
Summary: X11-requiring add-ons for D-BUS
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}

%description x11
D-BUS contains some tools that require Xlib to be installed, those are
in this separate package so server systems need not install X.

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1 -b .bindir
%patch1 -p1
%patch2 -p1

%build
if test -f autogen.sh; then env NOCONFIGURE=1 ./autogen.sh; else autoreconf -v -f -i; fi
%configure %{dbus_common_config_opts} --disable-tests --disable-asserts
make

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/%{_libdir}/pkgconfig

#change the arch-deps.h include directory to /usr/lib[64] instead of /lib[64]
sed -e 's@-I${libdir}@-I${prefix}/%{_lib}@' %{buildroot}/%{_lib}/pkgconfig/dbus-1.pc > %{buildroot}/%{_libdir}/pkgconfig/dbus-1.pc
rm -f %{buildroot}/%{_lib}/pkgconfig/dbus-1.pc

mkdir -p %{buildroot}/%{_bindir}
mv -f %{buildroot}/bin/dbus-launch %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_libdir}/dbus-1.0/include/
mv -f %{buildroot}/%{_lib}/dbus-1.0/include/* %{buildroot}/%{_libdir}/dbus-1.0/include/
rm -rf %{buildroot}/%{_lib}/dbus-1.0

rm -f %{buildroot}/%{_lib}/*.a
rm -f %{buildroot}/%{_lib}/*.la

install -D -m755 %{SOURCE2} %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/00-start-message-bus.sh

mkdir -p %{buildroot}%{_datadir}/dbus-1/interfaces

# Make sure that when somebody asks for D-Bus under the name of the
# old SysV script, that he ends up with the standard dbus.service name
# now.
ln -s dbus.service %{buildroot}/lib/systemd/system/messagebus.service

## %find_lang %{gettext_package}
# Delete the old legacy sysv init script
rm -rf %{buildroot}%{_initrddir}

mkdir -p %{buildroot}/var/lib/dbus

install -pm 644 -t %{buildroot}%{_pkgdocdir} \
    COPYING doc/introspect.dtd doc/introspect.xsl doc/system-activation.txt

%check
if test -f autogen.sh; then env NOCONFIGURE=1 ./autogen.sh; else autoreconf -v -f -i; fi
%configure %{dbus_common_config_opts} --enable-asserts --enable-verbose-mode --enable-tests

make clean
# TODO: better script for this...
export DISPLAY=42
{ Xvfb :${DISPLAY} -nolisten tcp -auth /dev/null >/dev/null 2>&1 &
  trap "kill -15 $! || true" 0 HUP INT QUIT TRAP TERM; };
if ! env DBUS_TEST_SLOW=1 make check; then
    echo "Tests failed, finding all Automake logs..." 1>&2;
    find . -type f -name '*.trs' | while read trs; do cat ${trs}; cat ${trs%%.trs}.log; done
    echo  "Exiting abnormally due to make check failure above" 1>&2;
    exit 1;
fi

%clean
rm -rf %{buildroot}

%pre
# Add the "dbus" user and group
/usr/sbin/groupadd -r -g %{dbus_user_uid} dbus 2>/dev/null || :
/usr/sbin/useradd -c 'System message bus' -u %{dbus_user_uid} -g %{dbus_user_uid} \
    -s /sbin/nologin -r -d '/' dbus 2> /dev/null || :

%post libs -p /sbin/ldconfig

%preun
if [ $1 = 0 ]; then
  /bin/systemctl stop dbus.service dbus.socket > /dev/null 2>&1 || :
fi

%postun libs -p /sbin/ldconfig

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%triggerun -- dbus < 1.4.10-2
/sbin/chkconfig --del messagebus >/dev/null 2>&1 || :

%files
%defattr(-,root,root)

%dir %{_pkgdocdir}
%{_pkgdocdir}/COPYING

%dir %{_sysconfdir}/dbus-1
%config %{_sysconfdir}/dbus-1/*.conf
%dir %{_sysconfdir}/dbus-1/system.d
%dir %{_sysconfdir}/dbus-1/session.d
%ghost %dir %{_localstatedir}/run/dbus
%dir %{_localstatedir}/lib/dbus/
/bin/dbus-daemon
/bin/dbus-send
/bin/dbus-cleanup-sockets
/bin/dbus-monitor
/bin/dbus-uuidgen
%{_mandir}/man*/dbus-cleanup-sockets.1.gz
%{_mandir}/man*/dbus-daemon.1.gz
%{_mandir}/man*/dbus-monitor.1.gz
%{_mandir}/man*/dbus-send.1.gz
%{_mandir}/man*/dbus-uuidgen.1.gz
%dir %{_datadir}/dbus-1
%{_datadir}/dbus-1/services
%{_datadir}/dbus-1/system-services
%{_datadir}/dbus-1/interfaces
%dir /%{_lib}/dbus-1
# See doc/system-activation.txt in source tarball for the rationale
# behind these permissions
%attr(4750,root,dbus) /%{_lib}/dbus-1/dbus-daemon-launch-helper
/lib/systemd/system/dbus.service
/lib/systemd/system/dbus.socket
/lib/systemd/system/dbus.target.wants/dbus.socket
/lib/systemd/system/messagebus.service
/lib/systemd/system/multi-user.target.wants/dbus.service
/lib/systemd/system/sockets.target.wants/dbus.socket

%files libs
%defattr(-,root,root,-)
/%{_lib}/*dbus-1*.so.*

%files x11
%defattr(-,root,root)

%{_bindir}/dbus-launch
%{_datadir}/man/man*/dbus-launch.1.gz
%{_sysconfdir}/X11/xinit/xinitrc.d/00-start-message-bus.sh

%files doc
%defattr(-,root,root)
%{_pkgdocdir}/*
%exclude %{_pkgdocdir}/COPYING

%files devel
%defattr(-,root,root)

/%{_lib}/lib*.so
%dir %{_libdir}/dbus-1.0
%{_libdir}/dbus-1.0/include/
%{_libdir}/pkgconfig/dbus-1.pc
%{_includedir}/*

%changelog
* Tue Jan 21 2014 Ville Skyttä <ville.skytta@iki.fi> - 1:1.6.18-3
- Adapt to unversioned docdirs; don't ship all docs in main package.
- Fix bogus dates in %%changelog and tabs vs spaces warning.

* Fri Dec 20 2013 Colin Walters <walters@verbum.org> - 1:1.6.18-2
- Test rebuild to see if we are affected by cast-align warnings now.

* Mon Nov 11 2013 Colin Walters <walters@verbum.org> - 1:1.6.18-1
- New upstream version
- Added backported patch which should fix the test suite; thanks to
  Yanko Kaneti for the suggestion.

* Wed Jul 24 2013 Colin Walters <walters@verbum.org> - 1:1.6.12-4
- Add patch to fix test-marshal on s390.

* Thu Jul 18 2013 Colin Walters <walters@verbum.org> - 1:1.6.12-3
- Find all logs automake has hidden and cat them for visibility
  into the mock logs.

* Thu Jul 18 2013 Colin Walters <walters@verbum.org> - 1:1.6.12-2
- Enable all upstream tests
  Resolves: #955532
  This is fairly hacky; a much better replacement would be
  something like the InstalledTests system.  But we have to live
  with rpm and stuff for now...

* Mon Jun 17 2013 Colin Walters <walters@verbum.org> - 1:1.6.12-1
- New upstream release
- CVE-2013-2168

* Thu Apr 18 2013 Matthias Clasen <mclasen@redhat.com> - 1:1.6.8-5
- Hardened build

* Tue Feb 05 2013 Colin Walters <walters@redhat.com> - 1:1.6.8-4
- Add patch from Matej Cepl to enable check section, modified by me
  to use common configure opts.

* Sun Oct 14 2012 Rex Dieter <rdieter@fedoraproject.org> - 1:1.6.8-3
- minor .spec cleanups
- tighten lib deps via %%{?_isa}
- drop old Conflicts/Obsoletes/patches

* Wed Oct  3 2012 Bill Nottingham <notting@redhat.com> - 1:1.6.8-2
- Drop systemd-sysv-convert in trigger, and resulting dependency (#852822)

* Fri Sep 28 2012 Colin Walters <walters@verbum.org> - 1:1.6.8-1
- 1.6.8

* Fri Sep 28 2012 Colin Walters <walters@verbum.org> - 1:1.6.6-1
- 1.6.6

* Thu Sep 13 2012 Colin Walters <walters@verbum.org> - 1:1.6.0-3
- CVE-2012-3524

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun  5 2012 Colin Walters <walters@verbum.org> - 1:1.6.0-1
- Update to 1.6.0

* Sun Apr 22 2012 Lennart Poettering <lpoetter@redhat.com> - 1:1.4.20-2
- Make D-Bus work in containers

* Fri Apr 13 2012 Colin Walters <walters@verbum.org>
- Update to 1.4.20; closes #806082
- Ensure /var/lib/dbus exists; this seems to have been
  dropped from upstream build rules.
- Adapt to documentation actually being installed

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 22 2011 Lennart Poettering <lpoetter@redhat.com> - 1:1.4.10-3
- Don't restart D-Bus on upgrades, dont' enable D-Bus, since it is statically enabled.
- https://bugzilla.redhat.com/show_bug.cgi?id=732426

* Wed Aug 03 2011 David Zeuthen <davidz@redhat.com> - 1:1.4.10-2
- Drop SysV support, #697523 (from Jóhann B. Guðmundsson <johannbg@gmail.com>)

* Thu Jun  2 2011 Colin Walters <walters@verbum.org> - 1:1.4.10-1
- New upstream version
- Drop XML docs patch which is now upstream
- Drop devhelp stuff; people should be using GDBus now.  If you
  don't, the raw doxygen is fine.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Matthias Clasen <mclasen@redhat.com> - 1:1.4.0-2
- %%ghost /var/run content (#656571)

* Mon Sep  6 2010 Lennart Poettering <lpoetter@redhat.com> - 1:1.4.0-1
- New upstream release

* Thu Jul 29 2010 Lennart Poettering <lpoetter@redhat.com> - 1:1.3.2-0.1.885483%{?dist}
- Conversion from systemd-install to systemctl

* Fri Jul 9 2010 Lennart Poettering <lpoetter@redhat.com> - 1:1.3.2-0.0.885483
- git Snapshot with systemd activation

* Wed Jun 23 2010 Lennart Poettering <lpoetter@redhat.com> - 1:1.3.1-1
- New upstream release

* Wed Mar 24 2010 Colin Walters <walters@verbum.org> - 1:1.2.24-1
- New upstream release
- Drop upstreamed patch

* Mon Mar 22 2010 Colin Walters <walters@verbum.org> - 1:1.2.22-2
- Add patch to fix syslog crasher

* Wed Mar 17 2010 Colin Walters <walters@verbum.org> - 1:1.2.22-1
- New upstream release

* Wed Feb 03 2010 Colin Walters <walters@verbum.org> - 1:1.2.20-1
- New upstream release
- Actually add start-early.patch

* Tue Feb 02 2010 Colin Walters <walters@verbum.org> - 1:1.2.18-1
- New upstream release
  Drop all upstreamed patches.
- start-early.patch had both bindir changes and start-early; the
  latter was upstreamed, so start-early is now bindir.patch.
  Ideally later get this partial-bindir stuff upstream.

* Thu Jan 21 2010 Colin Walters <walters@verbum.org> - 1:1.2.16-11
- Drop dbus-libs requiring dbus; this was unnecessary for programs
  which happened to speak the dbus protocol but don't require
  the daemon.
  Note that libdbus does support autolaunching dbus-daemon in
  the session as an emergency fallback for legacy situations; however,
  these cases were likely to have dbus installed already (via comps).
  If they don't, well one turned to the wrong page in the choose your
  own adventure book.

* Tue Jan 12 2010 Matthias Clasen <mclasen@redhat.com> - 1:1.2.16-10
- Don't link libdub against libcap-ng

* Fri Dec 18 2009 Ray Strode <rstrode@redhat.com> - 1:1.2.16-9
- Fix activation of daemons (#545267)
- Fix reload memleak (fdo #24697)
- Don't forget about pending activations on reload (fdo #24350)
- Fix reload race (fdo #21597)

* Wed Oct  7 2009 Matthias Clasen <mclasen@redhat.com> - 1:1.2.16-8
- Drop capabilities (#518541)

* Wed Oct  7 2009 Matthias Clasen <mclasen@redhat.com> - 1:1.2.16-7
- Add missing diagrams to the docs (#527650)

* Thu Oct  1 2009 Matthias Clasen <mclasen@redhat.com> - 1:1.2.16-6
- Fix timeout accounting

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1:1.2.16-5
- rebuilt with new audit

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Colin Walters <walters@redhat.co> - 1:1.2.16-3
- Remove conflicting -U option to useradd

* Wed Jul 22 2009 Colin Walters <walters@redhat.com> - 1:1.2.16-2
- Explicitly add a dbus group id, fixes dbus files getting a
  random group id in cases where the RPM install order varies.
  Fixes https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=458183

* Tue Jul 14 2009 Colin Walters <walters@redhat.com> - 1:1.2.16-1
- Upstream 1.2.16
- Remove inotify patch, now upstreamed
- Remove timeout patch, obsolete with upstream change to infinite
  timeout maximum by default

* Sat Jun 27 2009 Matthias Clasen <mclasen@redhat.com> - 1:1.2.14-2
- Don't leak inotify fd (#505338)

* Wed Apr 22 2009 Colin Walters <walters@verbum.org> - 1:1.2.14-1
- CVE-2009-1189
  * Update to 1.2.14

* Thu Mar 12 2009 Colin Walters <walters@verbum.org> - 1:1.2.12-1
- Switch to non-permissive branch:
  http://fedoraproject.org/wiki/Features/DBusPolicy

* Fri Feb 27 2009 Matthias Clasen <mclasen@redhat.com> - 1:1.2.4.4permissive-4
- Mark -doc content as %%doc

* Tue Feb 24 2009 Matthias Clasen <mclasen@redhat.com> - 1:1.2.4.4permissive-2
- Make -doc noarch

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.4.4permissive-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Colin Walters <walters@redhat.com> - 1:1.2.4.4.permissive-1
- New upstream

* Thu Dec 18 2008 Colin Walters <walters@redhat.com> - 1:1.2.4.2.permissive-1
- New upstream

* Fri Dec 12 2008 Colin Walters <walters@redhat.com> - 1:1.2.4-2
- Revert to upstream 1.2.4, add epoch

* Thu Dec 11 2008 Colin Walters <walters@redhat.com> - 1.2.8-4
- And drop it again, needs more work

* Wed Dec 10 2008 Colin Walters <walters@redhat.com> - 1.2.8-3
- Add back working syslog patch

* Tue Dec 09 2008 Colin Walters <walters@redhat.com> - 1.2.8-2
- Remove accidentally added syslog patch

* Tue Dec 09 2008 Colin Walters <walters@redhat.com> - 1.2.8-1
- New upstream 1.2.8
  Allows signals by default.

* Fri Dec 05 2008 Colin Walters <walters@redhat.com> - 1.2.6-1
- New upstream 1.2.6

* Fri Nov 21 2008 Matthias Clasen <mclasen@redhat.com> - 1.2.4-2
- Tweak descriptions

* Mon Oct 06 2008 Colin Walters <walters@redhat.com> - 1.2.4-1
- New upstream 1.2.4

* Thu Sep 25 2008 David Zeuthen <davidz@redhat.com> - 1.2.3-2%{?dist}
- Avoid using noreplace for files that aren't really config files

* Wed Aug 06 2008 Colin Walters <walters@redhat.com> - 1.2.3-1
- New upstream 1.2.2
- Drop patches that were upstreamed

* Wed Jul 23 2008 Matthias Clasen <mclasen@redhat.com> - 1.2.1-7
- Own /usr/share/dbus-1/interfaces

* Fri Jul 18 2008 Matthias Clasen <mclasen@redhat.com> - 1.2.1-6
- Add a patch from upstream git that adds a method
  for changing the activation environment on the session bus

* Thu Jul 17 2008 Casey Dahlin <cdahlin@redhat.com> - 1.2.1-5
- Patch to increase max method timeout

* Thu May 29 2008 Casey Dahlin <cdahlin@redhat.com> - 1.2.1-4
- Patches for fd.o bugs 15635, 15571, 15588, 15570

* Mon May 12 2008 Ray Strode <rstrode@redhat.com> - 1.2.1-3
- drop last patch after discussion on dbus list

* Mon May 12 2008 Ray Strode <rstrode@redhat.com> - 1.2.1-2
- ensure uuid is created at post time

* Fri Apr 04 2008 John (J5) Palmieri <johnp@redhat.com> - 1.2.1-1
- update to latest upstream
- major version change is really a maint release for 1.1.20
  please read the NEWS file in the source for more information

* Wed Feb 27 2008 David Zeuthen <davidz@redhat.com> - 1.1.20-1%{?dist}
- Update to latest upstream release. Includes fix for CVE-2008-0595.
- Drop some patches that went upstream already

* Wed Feb 20 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.1.4-6
- Really rebuild against new libcap

* Sun Feb 17 2008 Adam Tkac <atkac redhat com> - 1.1.4-5
- rebuild against new libcap

* Tue Feb  5 2008 Matthias Clasen <mclasen@redhat.com> - 1.1.4-4
- Fix a dbus-launch problem (#430412)

* Mon Feb  4 2008 Ray Strode <rstrode@redhat.com> - 1.1.4-3
- Start message bus from xinitrc.d instead of hard coding it
at the end of Xsession

* Mon Feb  4 2008 Matthias Clasen <mclasen@redhat.com> - 1.1.4-2
- Make it build against the latest gcc/glibc

* Thu Jan 17 2008 John (J5) Palmieri <johnp@redhat.com> - 1.1.4-1
- new upstream version
- fixes inotify patch which was consuming 100% cpu and memory

* Wed Jan 16 2008 John (J5) Palmieri <johnp@redhat.com> - 1.1.3-1
- new upstream version which obsoletes a number of our patches
- doc section added for the devhelp docs

* Thu Nov 15 2007 John (J5) Palmieri <johnp@redhat.com> - 1.1.2-9
- clean up spec file as per the merge review (#225676)

* Thu Oct 25 2007 Bill Nottingham <notting@redhat.com> - 1.1.2-8
- have -libs obsolete older versions of the main package so that yum upgrades work

* Thu Oct  4 2007 Matthias Clasen <mclasen@redhat.com> - 1.1.2-7
- Make the daemon a PIE executable  (#210039)

* Fri Sep 14 2007 Bill Nottingham <notting@redhat.com> - 1.1.2-6%{?dist}
- fix daemon abort when SELinux denies passing on a message (#283231)

* Fri Sep 14 2007 Dan Walsh <dwalsh@redhat.com> - 1.1.2-5%{?dist}
- Reverse we_were_root check to setpcap if we were root.  Also only init
audit if we were root.  So error dbus message will not show up when policy
reload happens.  dbus -session will no longer try to send audit message,
only system will.

* Tue Aug 28 2007 David Zeuthen <davidz@redhat.com> - 1.1.2-4%{?dist}
- Make dbus require dbus-libs (#261721)

* Mon Aug 27 2007 Adel Gadllah <adel.gadllah@gmail.com> - 1.1.2-3
- Add libs to a libs subpackage
- Update license tag

* Wed Aug 01 2007 David Zeuthen <davidz@redhat.com> - 1.1.2-2%{?dist}
- Move system bus activation helper to /{lib,lib64}/dbus-1. Also set
  the correct mode and permissions.
- Own the directory /usr/share/dbus-1/system-services
- Delete the diretory /{lib,lib64}/dbus-1.0 as it's not used
- Pass 'dbus' instead of 81 as --with-dbus-user; otherwise the setuid
  system bus activation helper fails

* Sat Jul 28 2007 Matthias Clasen <mclasen@redhat.com> - 1.1.2-1
- Update to 1.1.2

* Fri Jul  6 2007 Matthias Clasen <mclasen@redhat.com> - 1.1.1-3
- Add LSB header to init script (#246902)

* Thu Jun 28 2007 Ray Strode <rstrode@redhat.com> - 1.1.1-2
- include session.d directory in package manifest

* Thu Jun 28 2007 Ray Strode <rstrode@redhat.com> - 1.1.1-1
- Update to 1.1.1

* Fri Jun 22 2007 Matthias Clasen <mclasen@redhat.com> - 1.0.2-6
- Don't require libxml-python needlessly (#245300)

* Sun Jun 17 2007 Matthias Clasen <mclasen@redhat.com> - 1.0.2-5
- Require pkgconfig in -devel, not in -x11 (#244385)

* Sat Apr 14 2007 Matthias Clasen <mclasen@redhat.com> - 1.0.2-4
- Move the dbus-launch man page to the x11 subpackage

* Thu Apr 12 2007 David Zeuthen <davidz@redhat.com> - 1.0.2-3
- Start SELinux thread after setuid call (#221168)

* Wed Mar 28 2007 Matthias Clasen <mclasen@redhat.com> - 1.0.2-2
- Require pkgconfig in the -devel package

* Sun Mar 25 2007 Matthias Clasen <mclasen@redhat.com> - 1.0.2-1
- Update to 1.0.2
- Drop obsolete patches
- Fix directory ownership issues (#233753)

* Fri Dec 15 2006 David Zeuthen <davidz@redhat.com> - 1.0.1-3%{?dist}
- CVE-2006-6107: D-Bus denial of service

* Sun Nov 26 2006 Matthias Clasen <mclasen@redhat.com> - 1.0.1-2
- Include docs, and make them show up in devhelp

* Mon Nov 20 2006 Ray Strode <rstrode@redhat.com> - 1.0.1-1
- Update to 1.0.1
- Apply patch from Thiago Macieira <thiago@kde.org> to
  fix failed assertion in threading implementation
- Drop some crazy looking build time speed optimization

* Tue Nov 14 2006 John (J5) Palmieri <johnp@redhat.com> - 1.0.0-2
- add patch to fix dbus_threads_init_default

* Mon Nov 13 2006 John (J5) Palmieri <johnp@redhat.com> - 1.0.0-1
- update to D-Bus 1.0.0 "Blue Bird"
- build with verbose mode on but tests and asserts off

* Sun Nov 12 2006 Ray Strode <rstrode@redhat.com> - 0.95-3
- dont let dbus-launch session sitter crash in the
  non-autolaunch code path (bug 214649)

* Mon Nov 06 2006 John (J5) Palmieri <johnp@redhat.com> - 0.95-2
- Add /var/lib/dbus directory to %%files

* Fri Nov 03 2006 John (J5) Palmieri <johnp@redhat.com> - 0.95-1
- Update to D-Bus 1.0 RC 3 (0.95)
- don't build with tests on

* Sat Oct 14 2006 John (J5) Palmieri <johnp@redhat.com> - 0.94-1
- Update to D-Bus 1.0 RC 2 (0.94)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 0.93-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Matthias Clasen <mclasen@redhat.com> - 0.93-2
- Add a Requires for libxml2-python (#201877)

* Thu Sep 14 2006 John (J5) Palmieri <johnp@redhat.com> - 0.93-1
- Updated from upstream D-Bus 1.0 RC 1 (0.93)

* Wed Sep 6 2006 Dan Walsh <dwalsh@redhat.com> - 0.92-2
- Only audit on the system bus

* Fri Aug 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.92-1
- Update to 0.92
- remove old patches

* Sat Jul 22 2006 John (J5) Palmieri <johnp@redhat.com> - 0.90-8
- add patch to fix timeout removal assertion

* Thu Jul 20 2006 John (J5) Palmieri <johnp@redhat.com> - 0.90-7
- add patch to fix taking a connection ref when it is locked

* Wed Jul 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.90-6
- change the arch-deps.h include directory to /usr/lib[64] instead of /lib[64]
  in the dbus-1.pc file after compile

* Wed Jul 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.90-5
- Move arch include file from lib to libdir

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.90-4
- add patch that pregenerates the xml introspect file so d-bus doesn't
  have to be running suring the build.

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.90-3
- s/--libdir=\/lib/--libdir=%%{_lib}/ in configure stage
- add / before %%{_lib}

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.90-2
- Remove some remnants of the GLIB bindings from configure.in

* Mon Jul 17 2006 John (J5) Palmieri <johnp@redhat.com> - 0.90-1
- Update to upstream 0.90
- Split out bindings

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.62-1.1
- rebuild

* Mon Jun 12 2006 John (J5) Palmieri <johnp@redhat.com> - 0.62-1
- Update to upstream 0.62
- Remove mono for s390s

* Tue Jun  6 2006 Matthias Clasen <mclasen@redhat.com> 0.61-6
- Rebuild

* Wed May 17 2006 Karsten Hopp <karsten@redhat.de> 0.61-5.2
- add buildrequires libICE-devel, libSM-devel, libcap-devel
- change buildrequires form libX11 to libX11-devel

* Mon May 15 2006 John (J5) Palmieri <johnp@redhat.com> - 0.61-5.1
- Bump and rebuild.  Add a BR and R for libX11

* Tue Apr 25 2006 John (J5) Palmieri <johnp@redhat.com> - 0.61-5
- Backport patch from dbus-connection.c
  - Allows interfaces to be NULL in the message header as per the spec
  - Fixes a problem with pendings calls blocking on a data starved socket

* Mon Apr 17 2006 John (J5) Palmieri <johnp@redhat.com> 0.61-4
- New audit patch

* Fri Feb 24 2006 John (J5) Palmieri <johnp@redhat.com> 0.61-3
- ABI hasn't changed so add patch that makes dbus-sharp think
  it is still 0.60 (mono uses hard version names so any change
  means apps need to recompile)

* Fri Feb 24 2006 John (J5) Palmieri <johnp@redhat.com> 0.61-2
- Make sure chkconfig rests the priorities so we can start earlier

* Fri Feb 24 2006 John (J5) Palmieri <johnp@redhat.com> 0.61-1
- Upgrade to upstream version 0.61
- remove python callchain patch
- update avc patch

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.60-7.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.60-7.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 John (J5) Palmieri <johnp@redhat.com> 0.60-7
- Add patch to fix the python callchain
- Symlink dbus-send to /usr/bin because some applications
  look for it there

* Fri Jan 20 2006 John (J5) Palmieri <johnp@redhat.com> 0.60-6
- Fix up patch to init script so it refrences /bin not /usr/bin

* Fri Jan 20 2006 John (J5) Palmieri <johnp@redhat.com> 0.60-5
- move base libraries and binaries to /bin and /lib so they can be started
  before /usr is mounted on network mounted /usr systems
- have D-Bus start early

* Thu Jan 19 2006 Alexander Larsson <alexl@redhat.com> 0.60-4
- mono now built on s390x

* Mon Jan  9 2006 Alexander Larsson <alexl@redhat.com> 0.60-3
- Don't exclude non-mono arches

* Mon Jan  9 2006 Alexander Larsson <alexl@redhat.com> - 0.60-2
- Add dbus-sharp sub-package

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 0.60-1.1
- rebuilt

* Thu Dec 01 2005 John (J5) Palmieri <johnp@redhat.com> - 0.60-1
- upgrade to 0.60

* Thu Sep 08 2005 John (J5) Palmieri <johnp@redhat.com> - 0.50-1
- upgrade to 0.50

* Mon Aug 29 2005 John (J5) Palmieri <johnp@redhat.com> - 0.36.2-1
- upgrade to 0.36.2 which fixes an exploit where
  users can attach to another user's session bus (CAN-2005-0201)

* Wed Aug 24 2005 John (J5) Palmieri <johnp@redhat.com> - 0.36.1-1
- Upgrade to dbus-0.36.1
- Install all files to lib64/ on 64bit machines

* Tue Aug 23 2005 John (J5) Palmieri <johnp@redhat.com> - 0.36-1
- Upgrade to dbus-0.36
- Split modules that go into %%{_lib}/python2.4/site-packages/dbus
and those that go into %%{python_sitelib}/dbus (they differ on 64bit)
- Renable Qt bindings since packages in core can use them

* Mon Jul 18 2005 John (J5) Palmieri <johnp@redhat.com> - 0.35.2-1
- Upgrade to dbus-0.35.2
- removed dbus-0.34-kill-babysitter.patch
- removed dbus-0.34-python-threadsync.patch
- removed dbus-0.23-selinux-avc-audit.patch
- added dbus-0.35.2-selinux-avc-audit.patch
- take out restarts on upgrade

* Tue Jun 28 2005 John (J5) Palmieri <johnp@redhat.com> - 0.34-1
- Upgrade to dbus-0.34
- added dbus-0.34-kill-babysitter.patch
- added dbus-0.34-python-threadsync.patch
- remove dbus-0.32-print_child_pid.patch
- remove dbus-0.32-deadlock-fix.patch
- remove dbus-0.33-types.patch

* Wed Jun  8 2005 John (J5) Palmieri <johnp@redhat.com> - 0.33-4
- Add new libaudit patch from Steve Grub and enable in configure
  (Bug #159218)

* Mon May 23 2005 Bill Nottingham <notting@redhat.com> - 0.33-3
- remove static libraries from python bindings

* Sun May 01 2005 John (J5) Palmieri <johnp@redhat.com> - 0.33-2
- Backport patch from CVS that fixes int32's being marshaled as
uint16's in the python bindings

* Mon Apr 25 2005 John (J5) Palmieri <johnp@redhat.com> - 0.33-1
- update to upstream 0.33
- renable selinux audit patch

* Tue Apr 12 2005 John (J5) Palmieri <johnp@redhat.com> - 0.32-6
- Added patch to fix deadlocks when using recursive g_mains

* Tue Apr 12 2005 John (J5) Palmieri <johnp@redhat.com> - 0.32-5
- replace selinux_init patch with selinux_chroot_workaround patch
  to work around bad selinux interactions when using chroots
  on the beehive build machines

* Mon Apr 11 2005 John (J5) Palmieri <johnp@redhat.com> - 0.32-4
- add print_child_pid patch which make sure we prin the child's pid if we fork

* Thu Apr  7 2005 David Zeuthen <davidz@redhat.com> - 0.32-3
- add fix for glib infinite loop (fdo #2889)

* Thu Mar 31 2005 John (J5) Palmieri <johnp@redhat.com> - 0.32-2
- add selinux-init patch to fix dbus from segfaulting when
  building on machines that don't have selinux enabled

* Thu Mar 31 2005 John (J5) Palmieri <johnp@redhat.com> - 0.32-1
- update to upstream version 0.32

* Wed Mar 23 2005 John (J5) Palmieri <johnp@redhat.com> - 0.31-4
- Pyrex has been patched to generate gcc4.0 complient code
- Rebuild for gcc4.0

* Wed Mar 16 2005 John (J5) Palmieri <johnp@redhat.com> - 0.31-3
- change compat-gcc requirement to compat-gcc-32
- rebuild with gcc 3.2

* Tue Mar 08 2005 John (J5) Palmieri <johnp@redhat.com> - 0.31-2
- Remove precompiled init script and let the sources generate it

* Mon Mar 07 2005 John (J5) Palmieri <johnp@redhat.com> - 0.31-1
- update to upstream version 0.31
- take out user has same id patch (merged upstream)
- udi patch updated
- dbus-daemon-1 renamed to dbus-daemon
- dbus-glib-tool renamed to dbus-binding-tool
- force gcc33 because pyrex generate improper lvalue code
- disable audit patch for now

* Tue Feb 01 2005 John (J5) Palmieri <johnp@redhat.com> - 0.23-4
- Explicitly pass in the pid file location to ./configure instead of
  letting it guess based on the build enviornment

* Mon Jan 31 2005 John (J5) Palmieri <johnp@redhat.com> - 0.23-3
- Add patch to fix random users from connecting to a users session bus

* Fri Jan 21 2005 John (J5) Palmieri <johnp@redhat.com> - 0.23-2
- Add Steve Grubb's SE-Linux audit patch (Bug# 144920)

* Fri Jan 21 2005 John (J5) Palmieri <johnp@redhat.com> - 0.23-1
- Update to upstream version 0.23
- Drop all patches except for the UDI patch as they have been
  integrated upstream
- List of API changes:
      * add setgroups() to drop supplementary groups
      * removed dbus_bug_get_with_g_main since it's been replaced by dbus_g_bus_get
      * added support for int64 and uint64 to the python bindings
      * use SerivceOwnerChanges signal instead of ServiceCreated and ServiceDeleted

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 0.22-12
- rebuild against python 2.4

* Tue Nov 02 2004 John (J5) Palmieri <johnp@redhat.com>
- Add a requires for glib2-devel in the devel package
- Add SE-Linux backport from Colin Walters that fixes
  messages getting lost in SE-Linux contexts

* Wed Oct 13 2004 John (J5) Palmieri <johnp@redhat.com>
- Bump up release and rebuild

* Mon Oct 11 2004 Tim Waugh <twaugh@redhat.com>
- Run /sbin/ldconfig for glib sub-package (bug #134062).

* Wed Sep 22 2004 John (J5) Palmieri <johnp@redhat.com>
- Fixed patch to use dbus-1 instead of dbus-1.0
- (configure.in): Exported just the datadir instead of
  the full path to the dbus datadir for consistency

* Wed Sep 22 2004 John (J5) Palmieri <johnp@redhat.com>
- Adding patch to move /usr/lib/dbus-1.0/services to
  /usr/share/dbus-1.0/services

* Thu Sep 16 2004 John (J5) Palmieri <johnp@redhat.com>
- reverting BuildRequires: redhat-release because of issues with build system
- added precompiled version of the messagebus init script

* Thu Sep 16 2004 John (J5) Palmieri <johnp@redhat.com>
- changed /etc/redhat-release to the package redhat-release

* Thu Sep 16 2004 John (J5) Palmieri <johnp@redhat.com>
- added python int64 patch from davidz

* Thu Sep 16 2004 John (J5) Palmieri <johnp@redhat.com>
- added BuildRequires: /etc/redhat-release (RH Bug #132436)

* Wed Aug 18 2004 John (J5) Palmieri <johnp@redhat.com>
- Added Steve Grubb's spec file patch (RH Bug #130201)

* Mon Aug 16 2004 John (J5) Palmieri <johnp@redhat.com>
- Disabled dbus-gtk since dbus-viewer doesn't do anything right now

* Mon Aug 16 2004 John (J5) Palmieri <johnp@redhat.com>
- Moved dbus-viewer to new dbus-gtk package so that dbus-glib
  no longer requires X or GTK libraries. (RH Bug #130029)

* Thu Aug 12 2004 John (J5) Palmieri <johnp@redhat.com>
- Update to new 0.22 release

* Thu Aug 05 2004 John (J5) Palmieri <johnp@redhat.com>
- Added BuildRequires for libselinux-devel and Requires for libselinux

* Mon Aug 02 2004 Colin Walters <walters@redhat.com>
- Add SE-DBus patch

* Fri Jul 30 2004 John (J5) Palmieri <johnp@redhat.com>
- Added lib64 workaround for python bindings installing to
  the wrong lib directory on 64 bit archs

* Fri Jul 30 2004 John (J5) Palmieri <johnp@redhat.com>
- Updated console-auth patch
- rebuild

* Thu Jul 22 2004 John (J5) Palmieri <johnp@redhat.com>
- Update to upstream CVS build
- Added console-auth patch

* Fri Jun 25 2004 John (J5) Palmieri <johnp@redhat.com>
- Workaround added to fix gcc-3.4 bug on ia64

* Fri Jun 25 2004 John (J5) Palmieri <johnp@redhat.com>
- require new Pyrex version and see if it builds this time

* Fri Jun 25 2004 John (J5) Palmieri <johnp@redhat.com>
- rebuild with updated Pyrex (0.9.2.1)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jun 04 2004 John (J5) Palmieri <johnp@redhat.com>
- Moved dbus-viewer, dbus-monitor and dbus-glib-tool
  into the dbus-glib package so that the main dbus
  package does not depend on glib (Bug #125285)

* Thu Jun 03 2004 John (J5) Palmieri <johnp@redhat.com>
- rebuilt

* Thu May 27 2004 John (J5) Palmieri <johnp@redhat.com>
- added my Python patch
- took out the qt build requires
- added a gtk+ build requires

* Fri Apr 23 2004 John (J5) Palmieri <johnp@redhat.com>
- Changed build requirement to version 0.9-3 of Pyrex
  to fix problem with builing on x86_64

* Tue Apr 20 2004 John (J5) Palmieri <johnp@redhat.com>
- update to upstream 0.21
- removed dbus-0.20-varargs.patch patch (fixed upstream)

* Mon Apr 19 2004 John (J5) Palmieri <johnp@redhat.com>
- added a dbus-python package to generate python bindings
- added Pyrex build dependacy

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Bill Nottingham <notting@redhat.com> 0.20-4
- fix dbus error functions on x86-64 (#116324)
- add prereq (#112027)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Tim Waugh <twaugh@redhat.com>
- Conflict with cups prior to configuration file change, so that the
  %%postun service condrestart works.

* Wed Feb 11 2004 Havoc Pennington <hp@redhat.com> 0.20-2
- rebuild in fc2, cups now updated

* Wed Jan  7 2004 Bill Nottingham <notting@redhat.com> 0.20-1
- update to upstream 0.20

* Thu Oct 16 2003 Havoc Pennington <hp@redhat.com> 0.13-6
- hmm, dbus doesn't support uids in the config file. fix.

* Thu Oct 16 2003 Havoc Pennington <hp@redhat.com> 0.13-5
- put uid instead of username in the config file, to keep things working with name change

* Thu Oct 16 2003 Havoc Pennington <hp@redhat.com> 0.13-4
- make subpackages require the specific release, not just version, of base package

* Thu Oct 16 2003 Havoc Pennington <hp@redhat.com> 0.13-3
- change system user "messagebus" -> "dbus" to be under 8 chars

* Mon Sep 29 2003 Havoc Pennington <hp@redhat.com> 0.13-2
- see if removing qt subpackage for now will get us through the build system,
  qt bindings not useful yet anyway

* Sun Sep 28 2003 Havoc Pennington <hp@redhat.com> 0.13-1
- 0.13 fixes a little security oops

* Mon Aug  4 2003 Havoc Pennington <hp@redhat.com> 0.11.91-3
- break the tiny dbus-launch that depends on X into separate package
  so a CUPS server doesn't need X installed

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat May 17 2003 Havoc Pennington <hp@redhat.com> 0.11.91-1
- 0.11.91 cvs snap properly merges system.d

* Fri May 16 2003 Havoc Pennington <hp@redhat.com> 0.11.90-1
- build a cvs snap with a few more fixes

* Fri May 16 2003 Havoc Pennington <hp@redhat.com> 0.11-2
- fix a crash that was breaking cups

* Thu May 15 2003 Havoc Pennington <hp@redhat.com> 0.11-1
- 0.11

* Thu May 15 2003 Havoc Pennington <hp@redhat.com> 0.10.90-1
- use rc.d/init.d not init.d, bug #90192
- include the new man pages

* Fri Apr 11 2003 Havoc Pennington <hp@redhat.com> 0.9-1
- 0.9
- export QTDIR explicitly
- re-enable qt, the problem was most likely D-BUS configure

* Tue Apr  1 2003 Havoc Pennington <hp@redhat.com> 0.6.94-1
- update from CVS with a fix to set uid after gid

* Tue Apr  1 2003 Havoc Pennington <hp@redhat.com> 0.6.93-1
- new cvs snap that actually forks to background and changes
  user it's running as and so forth
- create our system user in pre

* Mon Mar 31 2003 Havoc Pennington <hp@redhat.com> 0.6.92-1
- fix for "make check" test that required a home directory

* Mon Mar 31 2003 Havoc Pennington <hp@redhat.com> 0.6.91-1
- disable qt for now because beehive hates me
- pull a slightly newer cvs snap that creates socket directory
- cat the make check log after make check fails

* Mon Mar 31 2003 Havoc Pennington <hp@redhat.com> 0.6.90-1
- initial build
