# TODO:
# - caraca driver (req: caraca, http://caraca.sf.net/)
# - irman driver (req: libirman, http://lirc.sf.net/software/snapshots/)
# - iguanaIR driver (req: http://iguanaworks.net/ir/usb/installation.shtml)
#   -> would cause license change to "GPLv2"
# - move to -devel (?): irw, *mode2, others?
#   note: xmode2 inflicts a dependency on X, and smode2 on svgalib
#   - does someone actually need xmode2/smode2 for something?
# - split utils into subpackage (keep daemons in main package)
# - don't run as root and/or create dedicated group, reduce fifo permissions?
# - Fixup /etc/lirc(m)d.conf %%ghost'ification, existence after erase etc.

%bcond_without  alsa
%bcond_without  portaudio
%bcond_without  x
%bcond_with     svgalib
%bcond_without  irman
%bcond_without  ftdi
%bcond_with     iguanaIR

%global released 1
%define pre     pre1

Name:           lirc
Version:        0.9.0
%if 0%{?released}
Release:        5%{?dist}
%else
Release:        0.1.%{pre}%{?dist}
%endif
Summary:        The Linux Infrared Remote Control package

Group:          System Environment/Daemons
License:        GPLv2+
URL:            http://www.lirc.org/
%if 0%{?released}
Source0:        http://downloads.sourceforge.net/lirc/%{name}-%{version}.tar.bz2
%else
Source0:        http://www.lirc.org/software/snapshots/%{name}-%{version}-%{pre}.tar.bz2
%endif
Source1:        %{name}.init
Source2:        %{name}.sysconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{__perl}
BuildRequires:  libusb-devel, python-devel
BuildRequires:  automake libtool
%if %{with irman}
BuildRequires:  libirman-devel
%endif
%if %{with ftdi}
BuildRequires:  libftdi-devel
%endif
%if %{with alsa}
BuildRequires:  alsa-lib-devel
%endif
%if %{with portaudio}
BuildRequires:  portaudio-devel >= 19
%endif
%if %{with svgalib}
BuildRequires:  svgalib-devel
%endif
%if %{with x}
BuildRequires:  libXt-devel
%endif
%if %{with iguanaIR}
BuildRequires:  iguanaIR-devel
%endif
Requires:       %{name}-libs = %{version}-%{release}
Requires(post): /sbin/chkconfig
Requires(post): /sbin/ldconfig
Requires(preun): /sbin/chkconfig
Requires(postun): /sbin/ldconfig

%description
LIRC is a package that allows you to decode and send infra-red and
other signals of many (but not all) commonly used remote controls.
Included applications include daemons which decode the received
signals as well as user space applications which allow controlling a
computer with a remote control.

%package        libs
Summary:        LIRC libraries
Group:          System Environment/Libraries
# Fix old F8 multilib upgrade path issue
Obsoletes:      %{name} < 0.8.3

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
Requires:       %{name}-libs = %{version}-%{release}

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


%prep
%if 0%{?released}
%setup -q
%else
%setup -q -n %{name}-%{version}-%{pre}
%endif

chmod 644 contrib/*
chmod +x contrib/hal

sed -i -e 's|/usr/local/etc/|/etc/|' contrib/irman2lirc

sed -i -e 's|/sbin/init.d/lircd|%{_initrddir}/lirc|' contrib/lircs

for f in remotes/chronos/lircd.conf.chronos \
    remotes/creative/lircd.conf.livedrive remotes/atiusb/lircd.conf.atiusb \
    NEWS ChangeLog AUTHORS contrib/lircrc ; do
    iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
done

# use /dev/lirc0 by default instead of /dev/lirc
sed -i -e 's|#define DEV_LIRC	"lirc"|#define DEV_LIRC	"lirc0"|' config.h.in

# use fixed instead of Courier w/xmode2, should be more prevalent on linux boxen
sed -i -e 's|char.*font1_name.*Courier.*$|char		font1_name[]="-misc-fixed-*-r-*-*-12-*-*-*-*-*-iso8859-1";|g' tools/xmode2.c

sed -i -e 's|"/lib /usr/lib |"/%{_lib} %{_libdir} |' configure # lib64 rpath

# *cough* I wish there was a good way to disable alsa/portaudio/svgalib...
%if ! %{with alsa}
sed -i -e 's/asoundlib.h/ALSA_DISABLED/g' configure*
%endif
%if ! %{with portaudio}
sed -i -e 's/portaudio.h/PORTAUDIO_DISABLED/g' configure*
%endif
%if ! %{with svgalib}
sed -i -e 's/vga.h/SVGALIB_DISABLED/g' configure*
%endif

touch -r aclocal.m4 configure.ac # avoid autofoo re-run

# Re-run autofoo for new cvs features
#autoreconf -i -f
#automake
chmod +x daemons/input_map.sh

%build
%configure \
  --disable-static \
  --disable-dependency-tracking \
  --enable-sandboxed \
%if ! %{with x}
  --without-x \
%endif
  --with-syslog=LOG_DAEMON \
  --with-driver=userspace
# make %{?_smp_mflags}
# parallel makes are currently busted, do single-threaded for now
make

%install
rm -rf $RPM_BUILD_ROOT __docs

make install DESTDIR=$RPM_BUILD_ROOT
install -pm 755 contrib/irman2lirc $RPM_BUILD_ROOT%{_bindir}
%if ! %{with svgalib}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/smode2.1*
%endif
%if ! %{with x}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/irxevent.1*
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/xmode2.1*
%endif

install -Dpm 644 doc/lirc.hwdb $RPM_BUILD_ROOT%{_datadir}/lirc/lirc.hwdb

install -Dpm 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/lirc
%{__perl} -pi -e \
  's|/etc/|%{_sysconfdir}/|g ;
   s|/var/|%{_localstatedir}/|g ;
   s|/usr/sbin/|%{_sbindir}/|g' \
  $RPM_BUILD_ROOT%{_initrddir}/lirc
install -Dpm 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/lirc

mkdir __docs
cp -pR doc contrib __docs
cd __docs
rm -rf doc/Makefile* doc/.libs doc/man* doc/lirc.hwdb
rm -rf contrib/irman2lirc contrib/lirc.* contrib/sendxevent.c
cd ..

install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/lirc
for f in lircd.conf lircmd.conf
do
  echo "# Populated config files can be found in the lirc-remotes sub-package
# or at http://lirc.sourceforge.net/remotes/" > $RPM_BUILD_ROOT%{_sysconfdir}/lirc/$f
done

install -dm 755 $RPM_BUILD_ROOT%{_localstatedir}/run/lirc/
touch $RPM_BUILD_ROOT%{_localstatedir}/run/lirc/lirc{d,m}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d
echo "d	%{_localstatedir}/run/lirc	0755	root	root	10d" > $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d/lirc.conf

rm $RPM_BUILD_ROOT%{_libdir}/liblirc_client.la

# Put remote definitions in place
cp -ar remotes $RPM_BUILD_ROOT%{_datadir}/lirc-remotes

%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/chkconfig --add lirc
# If we're upgrading, move config files into their new location, if need be
if [ $1 -ge 2 ] ; then
  if [ -e %{_sysconfdir}/lircd.conf -a ! -e %{_sysconfdir}/lirc/lircd.conf ]; then
    mv %{_sysconfdir}/lircd.conf %{_sysconfdir}/lirc/lircd.conf
  fi
  if [ -e %{_sysconfdir}/lircmd.conf -a ! -e %{_sysconfdir}/lirc/lircmd.conf ]; then
    mv %{_sysconfdir}/lircmd.conf %{_sysconfdir}/lirc/lircmd.conf
  fi
fi

%post libs -p /sbin/ldconfig

%preun
if [ $1 -eq 0 ] ; then
  %{_initrddir}/lirc stop >/dev/null || :
  /sbin/chkconfig --del lirc || :
fi

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ANNOUNCE AUTHORS ChangeLog COPYING NEWS README TODO
%config(noreplace) %{_sysconfdir}/lirc/lirc*d.conf
%config(noreplace) %{_sysconfdir}/sysconfig/lirc
%config(noreplace) %{_sysconfdir}/tmpfiles.d/lirc.conf
%{_initrddir}/lirc
%{_bindir}/*ir*
%{_bindir}/*mode2
%{_sbindir}/lirc*d
%dir %{_datadir}/lirc/
%{_datadir}/lirc/
%{_mandir}/man1/*ir*.1*
%{_mandir}/man1/*mode2*.1*
%{_mandir}/man8/lirc*d.8*
%ghost %dir %{_localstatedir}/run/lirc/
%ghost %{_localstatedir}/run/lirc/lirc*

%files libs
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/liblirc_client.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/lirc/
%{_libdir}/liblirc_client.so

%files doc
%defattr(-,root,root,-)
%doc __docs/* COPYING

%files remotes
%defattr(-,root,root,-)
%dir %{_datadir}/lirc-remotes
%{_datadir}/lirc-remotes/*


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.9.0-5
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Liu Di <liudidi@gmail.com> - 0.9.0-4
- 为 Magic 3.0 重建

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

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Dec  5 2004 Ville Skyttä <ville.skytta at iki.fi> 0.7.0-1
- Update to 0.7.0; major rework of the package:
- Change default driver to "any".
- Add -devel subpackage.
- Improve init script, add %%{_sysconfdir}/sysconfig/lirc for options.
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

