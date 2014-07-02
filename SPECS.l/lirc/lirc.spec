#
# rpmlint warnings:
#     only-non-binary-in-usr-lib:
#         https://bugzilla.redhat.com/show_bug.cgi?id=794777
#     incorrect-fsf-address :
#         https://sf.net/mailarchive/forum.php?forum_name=lirc-list&viewmonth=201310
#

%bcond_without  alsa
%bcond_without  portaudio
%bcond_without  x
%bcond_with     svgalib
%bcond_without  irman
%bcond_without  ftdi
%bcond_without  iguanaIR

%global _hardened_build 1

%global released 1
%define pre     pre1

Name:           lirc
Version:        0.9.0
%if 0%{?released}
Release:        27%{?dist}
%else
Release:        0.8.%{pre}%{?dist}
%endif
Summary:        The Linux Infrared Remote Control package

Group:          System Environment/Daemons
                # Some LGPLv2 files in iguanaIR promoted to GPLv2
License:        GPLv2
URL:            http://www.lirc.org/
%if 0%{?released}
Source0:        http://downloads.sourceforge.net/lirc/%{name}-%{version}.tar.bz2
%else
Source0:        http://www.lirc.org/software/snapshots/%{name}-%{version}-%{pre}.tar.bz2
%endif
Source1:        lircd.service
Source2:        lirc.sysconfig
Source3:        lircmd.service
Source4:        lircd.socket
Source5:        lirc.conf
Source6:        README.magic
Source7:        99-remote-control-lirc.rules
                # Patches 7..17 are from upstream.
Patch7:         0007-Make-lirc_wpc8769l-functional-again.patch
Patch8:         0008-lirc_sir-fix-resource-busy-error-from-bunk-lirc_open.patch
Patch9:         0009-lircd-handle-larger-config-files-in-write_socket-bet.patch
Patch10:        0010-lirc_atiusb-fix-buffer-alloc-to-work-with-new-kfifo.patch
Patch11:        0011-libusb-has-no-libusb-config-any-longer-use-pkg-confi.patch
Patch12:        0012-Silence-some-clang-warnings-courtesy-of-nox.patch
Patch13:        0013-userspace-use-dev-lirc0-as-default-device.patch
Patch14:        0014-lirc-make-chardev-nonseekable.patch
Patch15:        0015-media-lirc_dev-fixes-in-lirc_dev_fop_read.patch
Patch16:        0016-media-lirc_dev-add-some-__user-annotations.patch
Patch17:        0017-media-media-rc-lirc_dev-check-kobject_set_name-resul.patch
Patch18:        0018-Start-lirc-0.9.1-git.patch
Patch19:        0019-lircs-use-systemctl-instead-of-sysV-init.patch
                # 101-104: upstream merge request:
                #    https://sourceforge.net/p/lirc/git/merge-requests/3/
Patch101:       0101-Stripping-some-eol-whitespace.patch
Patch102:       0102-Update-autotools-config-files.patch
Patch103:       0103-xmode2.c-Use-generic-fixed-font-instead-of-Courier.patch
Patch104:       0104-Add-systemd-socket-activation-support.patch
                # local glue which should not go upstream.
Patch105:       0105-configure-ac-back-to-0.9.0.patch
                #https://sourceforge.net/p/lirc/mailman/message/31710217/
Patch200:       0200-Fixing-FTBS-when-using-Werror-format-security.patch

Buildrequires:  autoconf
BuildRequires:  automake

%if %{with alsa}
BuildRequires:  alsa-lib-devel
%endif
%if %{with iguanaIR}
BuildRequires:  iguanaIR-devel
%endif
%if %{with ftdi}
BuildRequires:  libftdi-devel
%endif
%if %{with irman}
BuildRequires:  libirman-devel
%endif
BuildRequires:  libtool
BuildRequires:  libusb-devel
BuildRequires:  libusb1-devel
%if %{with x}
BuildRequires:  libXt-devel
%endif
%if %{with portaudio}
BuildRequires:  portaudio-devel >= 19
%endif
BuildRequires:  python2-devel
%if %{with svgalib}
BuildRequires:  svgalib-devel
%endif
BuildRequires:  systemd-devel

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

Requires(post):    systemd
                   #for triggerun
Requires(post):    systemd-sysv
Requires(postun):  systemd
Requires(preun):   systemd

%description
LIRC is a package that allows you to decode and send infra-red and
other signals of many (but not all) commonly used remote controls.
Included applications include daemons which decode the received
signals as well as user space applications which allow controlling a
computer with a remote control.

%package        libs
Summary:        LIRC libraries
Group:          System Environment/Libraries

%description    libs
LIRC is a package that allows you to decode and send infra-red and
other signals of many (but not all) commonly used remote controls.
Included applications include daemons which decode the received
signals as well as user space applications which allow controlling a
computer with a remote control.  This package includes shared libraries
that applications use to interface with LIRC.

%package        devel
Summary:        Development files for LIRC
Group:          Development/Libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
LIRC is a package that allows you to decode and send infra-red and
other signals of many (but not all) commonly used remote controls.
Included applications include daemons which decode the received
signals as well as user space applications which allow controlling a
computer with a remote control.  This package includes files for
developing applications that use LIRC.

%package        doc
Summary:        LIRC documentation
Group:          Documentation

%description    doc
LIRC is a package that allows you to decode and send infra-red and
other signals of many (but not all) commonly used remote controls.
Included applications include daemons which decode the received
signals as well as user space applications which allow controlling a
computer with a remote control.  This package contains LIRC
documentation.

%package        remotes
Summary:        LIRC remote definitions
Group:          System Environment/Daemons

%description    remotes
LIRC is a package that allows you to decode and send infra-red and
other signals of many (but not all) commonly used remote controls.
Included applications include daemons which decode the received
signals as well as user space applications which allow controlling a
computer with a remote control.  This package contains a collection
of remote control configuration files.

%package        disable-kernel-rc
Summary:        Disable kernel ir device handling in favor of lirc
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description  disable-kernel-rc
Udev rule which disables the kernel built-in handling of infrared devices
(i. e., rc* ones) by making lirc the only used protocol. An alternative is
to use the LIRCD_IR_DEVICE option in /etc/sysconfig/lirc


# Don't provide or require anything from _docdir, per policy.
%global __provides_exclude_from ^%{_docdir}/.*$
%global __requires_exclude_from ^%{_docdir}/.*$


%prep
%if 0%{?released}
%setup -q
%else
%setup -q -n %{name}-%{version}-%{pre}
%endif

%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1

%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1

%patch200 -p1

chmod 644 contrib/*
chmod +x contrib/hal
chmod +x daemons/input_map.sh

sed -i -e 's|/usr/local/etc/|/etc/|' contrib/irman2lirc

for f in remotes/chronos/lircd.conf.chronos \
    remotes/creative/lircd.conf.livedrive remotes/atiusb/lircd.conf.atiusb \
    NEWS ChangeLog AUTHORS contrib/lircrc
do
    iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
done


%build
mkdir m4 || :
autoreconf -fi
export CFLAGS="%{optflags} -Werror=format-security"
%configure \
  --libdir=%{_libdir} \
  --disable-static \
  --disable-dependency-tracking \
  --enable-sandboxed \
%if ! %{with x}
  --without-x \
%endif
  --with-syslog=LOG_DAEMON \
  --with-driver=userspace
# make %%{?_smp_mflags}
# parallel makes are currently busted, do single-threaded for now
make


%install
make install DESTDIR=$RPM_BUILD_ROOT
install -pm 755 contrib/irman2lirc $RPM_BUILD_ROOT%{_bindir}
install -Dpm 644 doc/lirc.hwdb $RPM_BUILD_ROOT%{_datadir}/lirc/lirc.hwdb
install -Dpm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/lircd.service
install -Dpm 644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/lircmd.service
install -Dpm 644 %{SOURCE4} $RPM_BUILD_ROOT%{_unitdir}/lircd.socket
install -Dpm 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/lirc
install -Dpm 644 %{SOURCE5} $RPM_BUILD_ROOT/etc/lirc/lircd.conf
install -Dpm 644 %{SOURCE5} $RPM_BUILD_ROOT/etc/lirc/lircmd.conf
install -Dpm 644 %{SOURCE7} \
    $RPM_BUILD_ROOT%{_udevrulesdir}/99-remote-control-lirc.rules
cp -a %{SOURCE6} README.magic

# Put remote definitions in place
cp -ar remotes $RPM_BUILD_ROOT%{_datadir}/lirc-remotes

rm $RPM_BUILD_ROOT%{_libdir}/liblirc_client.la
%if ! %{with svgalib}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/smode2.1*
%endif
%if ! %{with x}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/irxevent.1*
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/xmode2.1*
%endif

rm -rf __docs; mkdir __docs
cp -pR doc contrib __docs
cd __docs
rm -rf doc/Makefile* doc/.libs doc/man* doc/lirc.hwdb
rm -rf contrib/irman2lirc contrib/lirc.* contrib/sendxevent.c
cd ..

mkdir -p $RPM_BUILD_ROOT/%{_tmpfilesdir}
echo "d /var/run/lirc  0755  root  root  10d" \
    > $RPM_BUILD_ROOT/%{_tmpfilesdir}/lirc.conf


%post
%systemd_post lircd.service lircmd.service
systemd-tmpfiles --create %{_tmpfilesdir}/lirc.conf
# Remove stale links after service name change lirc -> lircd:
find /etc/systemd -name lirc.service -xtype l -delete || :

%post libs -p /sbin/ldconfig

%preun
%systemd_preun lircd.service lircmd.service

%postun
%systemd_postun_with_restart lircd.service lircmd.servic

%postun libs -p /sbin/ldconfig


%files
%doc ANNOUNCE AUTHORS ChangeLog COPYING NEWS README TODO README.magic
%dir  /etc/lirc
%config(noreplace) /etc/lirc/lirc*d.conf
%config(noreplace) /etc/sysconfig/lirc
%{_tmpfilesdir}/lirc.conf
%{_unitdir}/lirc*
%{_bindir}/*ir*
%{_bindir}/*mode2
%{_sbindir}/lirc*d
%{_datadir}/lirc/
%{_mandir}/man1/*ir*.1*
%{_mandir}/man1/*mode2*.1*
%{_mandir}/man8/lirc*d.8*

%files libs
%doc COPYING
%{_libdir}/liblirc_client.so.*

%files devel
%{_includedir}/lirc/
%{_libdir}/liblirc_client.so

%files doc
%doc __docs/* COPYING

%files remotes
%doc AUTHORS ChangeLog COPYING README
%{_datadir}/lirc-remotes

%files disable-kernel-rc
%{_udevrulesdir}/99-remote-control-lirc.rules


%changelog
* Tue Jul 01 2014 Liu Di <liudidi@gmail.com> - 0.9.0-27
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.9.0-25
- enable BR iguanaIR again
- add missing isa tags

* Thu May 29 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.9.0-24
- rebuild for libftdi soname bump
- disable BR iguanaIR temporary, it pulls in lirc-0.9.0-23 and build fails

* Wed Jan 08 2014 Alec Leamas <leamas.alec@nowhere.net> - 0.9.0-23
- Remove f16 systemd upgrade snippets.

* Sun Nov 17 2013 leamas.alec@gmail.com - 0.9.0-22
- Fix -Werror=format-security build error (#1037178).
- Not yet built.

* Sun Nov 17 2013 leamas.alec@gmail.com - 0.9.0-21
- lircd.service: add sh wrapper to handle empty argumentes.

* Sun Nov 17 2013 leamas.alec@gmail.com - 0.9.0-20
- Fixing typo in -20.
- Ignore errors in PreExec/PostExec.

* Sat Nov 16 2013 Alec Leamas <leamas.alec@gmail.com> - 0.9.0-19
- Fix missing {} in lircd.service (bz 1025030, comment 24)

* Tue Nov 12 2013 Alec Leamas <leamas.alec@nowhere.net> - 0.9.0-18
- Remove old nowadays stale links to lirc.service.
- Fix broken reference to lirc.service in lircmd.service
- Update README

* Thu Oct 17 2013 Alec Leamas <leamas.alec@nowhere.net> - 0.9.0-17
- Add a udev "Only use lirc" subpackage.
- Revise enabling of lirc protocol.
- Documenting upstream merge request.
- Resurrect contrib/lircs, use systemctl.
- Force creation of /run/lirc after installation.
- Use /lib/tmpfiles.d, not /etc/tmpfiles.d with _tmpfilesdir macro.

* Tue Oct 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.9.0-16
- fix build for f18
- remove BR perl, already called in build system
- fix bogus in changelog date

* Thu Oct 10 2013 Alec Leamas <leamas.alec@nowhere.net> - 0.9.0-15
- Actually use sysconfig files (881976).
- Modify lirc.service to not fork.
- Add support for iguanaIR driver (#954146).
- Add hardened build flag (955144).
- Use actual systemd macros (850191).
- Clean up some nowadays not used directives.
- Run autoreconf by default (926082).
- Cleanup some obsoleted autotools usage, two new patches.
- Deactivate other decoders on start (923978).
- Filter away docdir dependencies.
- Remove obsolete F8 upgrade Obsoletes: (sic!).
- Fix inconsistent/duplicate /usr/share/lirc in %%files.
- Add %%doc (notably COPYING) to remotes subpackage.
- Claim /etc/lirc.
- Update to latest upstream (10 patches).
- Use /var and /etc instead of %%{_sysconfdir} and %%{localstatedir}.
- Removed obsolete code to move config files to /etc/lirc in %%post.
- Renamed main systemd service: lirc.service -> lircd.service.
- Added socket activation support.
- Don't claim temporary files in /run/lirc, they are just transient.
- Initiate lircd.conf, lircmd.conf from external template.
- Bumping release, 14 is published.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Jon Ciesla <limburgher@gmail.com> - 0.9.0-9
- Migrate to systemd, BZ 789760.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Jarod Wilson <jarod@redhat.com> 0.9.0-7
- Only alter protocols for the device lirc is configured to talk to
  and don't try to poke protocols on non-rc-core lirc devices

* Mon Jun 06 2011 Jarod Wilson <jarod@redhat.com> 0.9.0-6
- And now take out the libusb1-devel bit, its actually the removal of
  libusb-config from libusb-devel that broke things, so we need some
  fixage upstream, backported here.

* Tue May 31 2011 Jarod Wilson <jarod@redhat.com> 0.9.0-5
- Add explict BR: libusb1-devel, as some userspace drivers require it, and
  its apparently not getting into the build root any longer

* Sat May 28 2011 Jarod Wilson <jarod@redhat.com> 0.9.0-4
- Apparently, the title of bz656613 wasn't quite correct, some stuff
  in /var/run does need to be installed, not ghosted...

* Tue May 03 2011 Jarod Wilson <jarod@redhat.com> 0.9.0-3
- Properly support tmpfs /var/run/lirc in new systemd world (#656613)
- Don't ghost config files, lay 'em down with pointers in them

* Tue May 03 2011 Jarod Wilson <jarod@redhat.com> 0.9.0-2
- Only disable in-kernel IR decoders if we're not using devinput mode,
  as they're actually required for devinput mode to work right.

* Sat Mar 26 2011 Jarod Wilson <jarod@redhat.com> 0.9.0-1
- Update to lirc 0.9.0 release
- Disable in-kernel IR decoding when starting up lircd, reenable on shutdown

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-0.2.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 26 2010 Jarod Wilson <jarod@redhat.com> 0.9.0-0.1.pre1
- Update to lirc 0.9.0-pre1 snapshot
- Add conditional flag for building with iguanaIR support (there's an
  iguanaIR package awaiting review right now)

* Mon Sep 06 2010 Jarod Wilson <jarod@redhat.com> 0.8.7-1
- Update to lirc 0.8.7 release

* Sat Sep 04 2010 Jarod Wilson <jarod@redhat.com> 0.8.7-0.1.pre3
- Update to lirc 0.8.7-pre3 snapshot

* Mon Aug 02 2010 Jarod Wilson <jarod@redhat.com> 0.8.7-0.1.pre2
- Fix up sub-package license file inclusion per new fedora
  licensing guidelines
- Update to lirc 0.8.7pre2 snapshot

* Fri May 21 2010 Bastien Nocera <bnocera@redhat.com> 0.8.6-7
- Fix Firefly remote definition keycodes

* Sun Apr 11 2010 Jarod Wilson <jarod@redhat.com> 0.8.6-6
- Revert to compat-ioctls per upstream discussion (#581326)

* Wed Mar 17 2010 Jarod Wilson <jarod@redhat.com> 0.8.6-5
- Update devinput lircd.conf with additional keys from input.h

* Mon Feb 15 2010 Jarod Wilson <jarod@redhat.com> 0.8.6-4
- Un-bungle newly introduced segfault in prior build

* Mon Feb 15 2010 Jarod Wilson <jarod@redhat.com> 0.8.6-3
- Fix up ioctl portability between 32-bit and 64-bit

* Thu Nov 12 2009 Jarod Wilson <jarod@redhat.com> 0.8.6-2
- Add devinput mouse event passthru to uinput support from lirc cvs

* Sun Sep 13 2009 Jarod Wilson <jarod@redhat.com> 0.8.6-1
- Update to lirc 0.8.6 release

* Sat Aug 29 2009 Jarod Wilson <jarod@redhat.com> 0.8.6-0.6.pre2
- Rediff patches so they actually apply still

* Sat Aug 29 2009 Jarod Wilson <jarod@redhat.com> 0.8.6-0.5.pre2
- Update to lirc 0.8.6pre2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-0.4.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Jarod Wilson <jarod@redhat.com> 0.8.6-0.3.pre1
- Set up tools to use /dev/lirc0 instead of /dev/lirc by default
- Set a default font for xmode2 most people actually have (#467339)

* Wed Jun 24 2009 Jarod Wilson <jarod@redhat.com> 0.8.6-0.2.pre1
- Fix things up so the relocated socket actually works out of the box

* Tue Jun 23 2009 Jarod Wilson <jarod@redhat.com> 0.8.6-0.1.pre1
- Update to lirc 0.8.6pre1
- Adds Linux input layer support to lircmd
- Adds XMP protocol support
- Moves lircd socket from /dev/ to /var/run/lirc/ and pid file from
  /var/run/ to /var/run/lirc/

* Thu May 28 2009 Jarod Wilson <jarod@redhat.com> 0.8.5-2
- Update to lirc 0.8.5
- Add irman support, now that libirman is in Fedora (#474992)

* Sun May 17 2009 Jarod Wilson <jarod@redhat.com> 0.8.5-1.pre3
- Update to lirc 0.8.5pre3 cvs snapshot

* Fri Apr 10 2009 Jarod Wilson <jarod@redhat.com> 0.8.5-1.pre2
- Update to lirc 0.8.5pre2 cvs snapshot

* Thu Feb 26 2009 Jarod Wilson <jarod@redhat.com> 0.8.5-1.pre1
- Update to lirc 0.8.5pre1 cvs snapshot
- Adds support for usb-connected ftdi-based homebrew transceivers
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 09 2008 Jarod Wilson <jarod@redhat.com> 0.8.4a-3
- BR: automake and libtool to get cvs additions building

* Mon Dec 08 2008 Jarod Wilson <jarod@redhat.com> 0.8.4a-2
- Nuke bogus and harmful %%postun --try-restart (#474960)
- Assorted updates from lirc cvs:
  * Add uinput injection support
  * Add support for binding lircd listener to a specific ip

* Sun Oct 26 2008 Jarod Wilson <jarod@redhat.com> 0.8.4a-1
- Update to lirc 0.8.4a release (fixes mode2 irrecord failures)
- Really fix the mceusb remote config file this time

* Thu Oct 16 2008 Jarod Wilson <jarod@redhat.com> 0.8.4-2
- Make all remote configs have unique names (#467303)
- Fix up some key names that got screwed up by standardization script

* Sun Oct 12 2008 Jarod Wilson <jarod@redhat.com> 0.8.4-1
- Update to 0.8.4 release

* Fri Oct 10 2008 Jarod Wilson <jarod@redhat.com> 0.8.4-0.5.pre2
- Re-enable portaudio driver by default, require v19 or later

* Mon Oct 06 2008 Jarod Wilson <jarod@redhat.com> 0.8.4-0.4.pre2
- Update to 0.8.4pre2

* Mon Oct 06 2008 Bastien Nocera <bnocera@redhat.com> 0.8.4-0.3.pre1
- Fix more keycodes for the streamzap remote

* Wed Oct 01 2008 Bastien Nocera <bnocera@redhat.com> 0.8.4-0.2.pre1
- Don't create a backup for the keycodes patch, or all the original files
  will also get installed, and get used in gnome-lirc-properties

* Wed Sep 24 2008 Jarod Wilson <jarod@redhat.com> 0.8.4-0.1.pre1
- Update to 0.8.4pre1
- Drop upstream patches
- Adds support for the CommandIR II userspace driver

* Tue Sep 16 2008 Jarod Wilson <jarod@redhat.com> 0.8.3-7
- Fix multilib upgrade path from F8 (Nicolas Chauvet, #462435)

* Thu Aug 14 2008 Bastien Nocera <bnocera@redhat.com> 0.8.3-6
- Make lircd not exit when there's no device available, so that the
  daemon is running as expected when the hardware is plugged back in
  (#440231)

* Thu Aug 14 2008 Bastien Nocera <bnocera@redhat.com> 0.8.3-5
- Add huge patch to fix the majority of remotes to have sensible keycodes,
  so they work out-of-the-box (#457273)

* Mon Jun 23 2008 Jarod Wilson <jwilson@redhat.com> 0.8.3-4
- Drop resume switch patch, no longer required
- Add support for config option style used by gnome-lirc-properties (#442341)

* Mon Jun 02 2008 Jarod Wilson <jwilson@redhat.com> 0.8.3-3
- Add additional required patches for gnome-lirc-properties (#442248)
- Put remote definitions in their own sub-package (#442328)

* Mon May 12 2008 Jarod Wilson <jwilson@redhat.com> 0.8.3-2
- Include upstream patch for lircd.conf remote include directives (#442248)
- Include upstream patch to validate transmit buffers

* Sun May 04 2008 Jarod Wilson <jwilson@redhat.com> 0.8.3-1
- Update to 0.8.3 release

* Sun Apr 27 2008 Jarod Wilson <jwilson@redhat.com> 0.8.3-0.4.pre3
- Update to 0.8.3pre3

* Sun Apr 06 2008 Jarod Wilson <jwilson@redhat.com> 0.8.3-0.3.pre2
- Update to 0.8.3pre2

* Tue Feb 12 2008 Ville Skyttä <ville.skytta at iki.fi> 0.8.3-0.2.pre1
- Split libraries into -libs subpackage.
- Refresh autotools re-run avoidance hack.

* Thu Oct 18 2007 Jarod Wilson <jwilson@redhat.com> 0.8.3-0.1.pre1
- 0.8.3pre1
- adds Mac IR support, resolves bz #284291

* Wed Aug 15 2007 Ville Skyttä <ville.skytta at iki.fi> 0.8.2-2
- License: GPLv2+

* Sun Jun 10 2007 Ville Skyttä <ville.skytta at iki.fi> 0.8.2-1
- 0.8.2.

* Wed Jun  6 2007 Ville Skyttä <ville.skytta at iki.fi> 0.8.2-0.1.pre3
- 0.8.2pre3.
- Fix up linefeeds and char encodings of more docs.

* Fri May 18 2007 Ville Skyttä <ville.skytta at iki.fi> 0.8.2-0.1.pre2
- 0.8.2pre2.

* Sun Jan  7 2007 Ville Skyttä <ville.skytta at iki.fi> 0.8.1-1
- 0.8.1.

* Sat Dec 30 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.1-0.2.pre5
- 0.8.1pre5.

* Tue Dec 12 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.1-0.2.pre4
- 0.8.1pre4.

* Thu Nov 30 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.1-0.2.pre3
- 0.8.1pre3.

* Sun Oct 15 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.1-0.2.pre2
- 0.8.1pre2, optflags patch no longer needed.

* Mon Aug 28 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.1-0.2.pre1
- Rebuild.

* Sat Jul  1 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.1-0.1.pre1
- 0.8.1pre1.
- Add rpmbuild options for enabling/disabling ALSA, portaudio and/or X
  support, ALSA and X enabled by default, portaudio not.
- Split most of the documentation to -doc subpackage.
- Install irman2lirc as non-doc.

* Tue Feb 14 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.0-3
- Avoid standard rpaths on lib64 archs.

* Sat Jan 21 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.0-2
- 0.8.0.

* Sat Jan 14 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.0-0.2.pre4
- 0.8.0pre4.

* Sun Jan  1 2006 Ville Skyttä <ville.skytta at iki.fi> 0.8.0-0.2.pre3
- 0.8.0pre3.

* Tue Dec 27 2005 Ville Skyttä <ville.skytta at iki.fi>
- Split kernel modules into separate package.
- Disable debugging features.

* Wed Dec 14 2005 Ville Skyttä <ville.skytta at iki.fi> 0.8.0-0.2.pre2
- 0.8.0pre2, kernel >= 2.6.15 USB patch applied upstream.
- lirc_clientd renamed to lircrcd.

* Tue Nov 29 2005 Ville Skyttä <ville.skytta at iki.fi> 0.8.0-0.2.pre1
- Pull security fix for the new lirc_clientd from upstream CVS, and
  while at it, some other useful post-0.8.0pre1 changes.
- Kernel >= 2.6.15 patchwork based on initial patch from Andy Burns (#172404).
- Disable lirc_cmdir kernel module (unknown symbols).
- Adapt to modular X.Org packaging.

* Wed Nov  9 2005 Ville Skyttä <ville.skytta at iki.fi> 0.8.0-0.1.pre1
- 0.8.0pre1, usage message patch applied upstream.

* Sun Oct 30 2005 Ville Skyttä <ville.skytta at iki.fi> 0.7.3-0.1.pre1
- 0.7.3pre1, "no device" crash fix applied upstream.
- Fix lircd and lircmd usage messages.

* Wed Aug 31 2005 Ville Skyttä <ville.skytta at iki.fi> 0.7.2-3
- Make the init script startup earlier and shutdown later by default.

* Sun Aug 14 2005 Ville Skyttä <ville.skytta at iki.fi> 0.7.2-2
- 0.7.2, patch to fix crash at startup when no device is specified.
- Enable audio input driver support (portaudio).
- Improve package description.
- Don't ship static libraries.
- Drop pre Fedora Extras backwards compatibility hacks.
- Make svgalib support (smode2) build conditional, disabled by default.
- Simplify module package build (still work in progress, disabled by default).
- Other minor specfile cleanups and maintainability improvements.

* Thu May 26 2005 Ville Skyttä <ville.skytta at iki.fi> 0.7.1-3
- Adjust kernel module build for FC4 and add hauppauge, igorplugusb, imon,
  sasem, and streamzap to the list of modules to build.  This stuff is still
  disabled by default, rebuild with "--with modules --target $arch" to enable.

* Sun Apr 17 2005 Ville Skyttä <ville.skytta at iki.fi> 0.7.1-2
- 0.7.1.

* Thu Apr 7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Dec  5 2004 Ville Skyttä <ville.skytta at iki.fi> 0.7.0-1
- Update to 0.7.0; major rework of the package:
- Change default driver to "any".
- Add -devel subpackage.
- Improve init script, add /etc/sysconfig/lirc for options.
- Rename init script to "lirc" to follow upstream; the script is not only
  for lircd, but lircmd as well.
- Log to syslog instead of separate log file.
- %%ghost'ify /dev/lirc*.
- Build kernel modules when rebuilt with "--with kmod".  This stuff was mostly
  borrowed from Axel Thimm's packages, and is not really ready for FC3+ yet.
- Enable debugging features.
- Specfile cleanups.

* Mon Aug 30 2004 Matthias Saou <http://freshrpms.net/> 0.6.6-3
- Added missing /sbin/ldconfig calls.

* Wed May 19 2004 Matthias Saou <http://freshrpms.net/> 0.6.6-2
- Rebuild for Fedora Core 2... this spec file still _really_ needs reworking!

* Fri Nov  7 2003 Matthias Saou <http://freshrpms.net/> 0.6.6-2
- Rebuild for Fedora Core 1... this spec file _really_ needs reworking!

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9... this spec file needs some reworking!

* Mon Oct  7 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.6.6 final.

* Mon Sep 16 2002 Matthias Saou <http://freshrpms.net/>
- Updated to latest pre-version.
- Kernel modules still need to be compiled separately and with a custom
  kernel :-(

* Thu May  2 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.6.5.
- Rebuilt against Red Hat Linux 7.3.
- Added the %%{?_smp_mflags} expansion.

* Thu Oct  4 2001 Matthias Saou <http://freshrpms.net/>
- Initial RPM release.

