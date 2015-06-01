%global upstream_build 4126

Name:           pcsc-lite
Version:	1.8.13
Release:	1%{?dist}
Summary:        PC/SC Lite smart card framework and applications
Summary(zh_CN.UTF-8): PC/SC Lite 智能卡框架和应用程序

Group:          System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
License:        BSD
URL:            http://pcsclite.alioth.debian.org/
Source0:        http://alioth.debian.org/download.php/%{upstream_build}/%{name}-%{version}.tar.bz2

BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  systemd-devel
BuildRequires:  systemd-units

Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires:       pcsc-ifd-handler
Requires:       %{name}-libs = %{version}-%{release}

%description
The purpose of PC/SC Lite is to provide a Windows(R) SCard interface
in a very small form factor for communicating to smartcards and
readers.  PC/SC Lite uses the same winscard API as used under
Windows(R).  This package includes the PC/SC Lite daemon, a resource
manager that coordinates communications with smart card readers and
smart cards that are connected to the system, as well as other command
line tools.

%description -l zh_CN.UTF-8
PC/SC Lite 智能卡框架和应用程序。

%package        libs
Summary:        PC/SC Lite libraries
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description    libs
PC/SC Lite libraries.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package        devel
Summary:        PC/SC Lite development files
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}-libs = %{version}-%{release}

%description    devel
PC/SC Lite development files.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        doc
Summary:        PC/SC Lite developer documentation
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
BuildArch:      noarch
Requires:       %{name}-libs = %{version}-%{release}

%description    doc
%{summary}.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q

# Convert to utf-8
for file in ChangeLog; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done


%build
%configure \
  --disable-static \
  --enable-usbdropdir=%{_libdir}/pcsc/drivers
make %{?_smp_mflags}
doxygen doc/doxygen.conf ; rm -f doc/api/*.{map,md5}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Create empty directories
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/reader.conf.d
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pcsc/drivers
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/pcscd

rm $RPM_BUILD_ROOT%{_libdir}/*.la

# Remove documentation installed in a wrong directory
rm $RPM_BUILD_ROOT%{_docdir}/pcsc-lite/README.DAEMON
magic_rpm_clean.sh

%post
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl enable pcscd.socket >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable pcscd.service pcscd.socket >/dev/null 2>&1 || :
    /bin/systemctl stop pcscd.service pcscd.socket >/dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart pcscd.service >/dev/null 2>&1 || :
fi

%triggerun -- pcsc-lite < 1.7.4-2
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply pcscd
# to migrate them to systemd targets
%{_bindir}/systemd-sysv-convert --save pcscd >/dev/null 2>&1 ||:

# Enable pcscd socket activation
/bin/systemctl enable pcscd.socket >/dev/null 2>&1 || :

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del pcscd >/dev/null 2>&1 || :

# Restart the service if it's already running
if /bin/systemctl is-active pcscd.service >/dev/null 2>&1 ; then
    /bin/systemctl stop pcscd.service >/dev/null 2>&1 ||:
    /bin/systemctl start pcscd.socket pcscd.service >/dev/null 2>&1 ||:
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog* DRIVERS HELP README SECURITY TODO
%dir %{_sysconfdir}/reader.conf.d/
%{_unitdir}/pcscd.service
%{_unitdir}/pcscd.socket
%{_sbindir}/pcscd
%dir %{_libdir}/pcsc/
%dir %{_libdir}/pcsc/drivers/
%{_mandir}/man5/reader.conf.5*
%{_mandir}/man8/pcscd.8*
%ghost %dir %{_localstatedir}/run/pcscd/

%files libs
%doc COPYING
%{_libdir}/libpcsclite.so.*

%files devel
%{_bindir}/pcsc-spy
%{_includedir}/PCSC/
%{_libdir}/libpcsclite.so
%{_libdir}/libpcscspy.so*
%{_libdir}/pkgconfig/libpcsclite.pc
%{_mandir}/man1/pcsc-spy.1*

%files doc
%doc doc/api/ doc/example/pcsc_demo.c


%changelog
* Thu Apr 16 2015 Liu Di <liudidi@gmail.com> - 1.8.13-1
- 更新到 1.8.13

* Fri Nov 30 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.7-1
- Update to 1.8.7

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.6-1
- Update to 1.8.6

* Mon Aug 06 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.5-1
- Update to 1.8.5

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.4-1
- Update to 1.8.4

* Thu Jun 14 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.3-2
- Rebuild for new libudev (#831987)

* Fri Mar 30 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.3-1
- Update to 1.8.3

* Mon Feb 06 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.2-1
- Update to 1.8.2
- Drop the systemd support patches which are now upstreamed
- Package the new pcsc-spay tool in -devel subpackage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Kalev Lember <kalevlember@gmail.com> - 1.7.4-6
- Remove the automatic card power down disabling patch again;
  no longer needed with latest libusb1 1.0.9 rc1 (#737988)

* Fri Sep 16 2011 Kalev Lember <kalevlember@gmail.com> - 1.7.4-5
- Reapply the patch to disable automatic card power down (#737988)

* Sun Sep 04 2011 Kalev Lember <kalevlember@gmail.com> - 1.7.4-4
- Ignore errors from 'systemctl enable' (#734852)

* Sat Aug 20 2011 Kalev Lember <kalevlember@gmail.com> - 1.7.4-3
- Use /var/run/pcscd for ipc directory (#722449)

* Fri Jul 15 2011 Kalev Lember <kalevlember@gmail.com> - 1.7.4-2
- Converted initscript to systemd service file (#617330)

* Fri Jun 24 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.4-1
- Update to 1.7.4

* Wed Jun 22 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.3-1
- Update to 1.7.3
- Dropped upstreamed patches
- Dropped the lib64 rpath patch; pcsc-lite now uses system libtool
- Cleaned up the spec file for modern rpmbuild

* Wed May 25 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.2-2
- Don't fill log files with repeating messages (#657658, #707412)

* Thu Mar 31 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.2-1
- Update to 1.7.2

* Wed Mar 30 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.1-1
- Update to 1.7.1

* Thu Mar 17 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.0-2
- Explicitly create and own drivers directory

* Wed Mar 09 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.0-1
- Update to 1.7.0
- Use libudev for hotplugging instead of hal

* Fri Feb 25 2011 Kalev Lember <kalev@smartlink.ee> - 1.6.7-1
- Update to 1.6.7
- Rebased noautostart patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.6-2
- Disabled automatic card power down which seems to be unreliable at this point

* Mon Dec 13 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.6-1
- Update to 1.6.6

* Mon Dec 13 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.4-2
- Disabled pcscd on-demand startup (#653903)

* Sun Aug 15 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.4-1
- Update to 1.6.4
- Buildrequire graphviz for apidoc generation

* Wed Aug 04 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.2-1
- Update to 1.6.2
- Dropped upstreamed patches
- Removed configure --disable-dependency-tracking option which is the
  default with configure macro.

* Thu Jul 08 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.1-5
- Include COPYING in libs subpackage as per new licensing guidelines

* Mon Jul 05 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.1-4
- Patch to fix crash with empty config directory

* Sun Jul 04 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.1-3
- Patch to fix config dir handling

* Sun Jul 04 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.1-2
- Removed call to non-existent update-reader.conf in init script

* Fri Jun 18 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.1-1
- Update to 1.6.1

* Tue Apr 13 2010 Kalev Lember <kalev@smartlink.ee> - 1.5.5-4
- Fix init script start / stop priorities (#580322)
- Don't require pkgconfig as the dep is now automatically generated by rpm

* Wed Mar 03 2010 Kalev Lember <kalev@smartlink.ee> - 1.5.5-3
- Added patch to fix init script LSB header (#565241)
- Dropped BR: libusb-devel as configure script really picks up libhal instead
- Use %%global instead of %%define

* Mon Dec 21 2009 Kalev Lember <kalev@smartlink.ee> - 1.5.5-2
- Require -libs subpackage from main pcsc-lite package
- Build -doc subpackage as noarch
- Dropped --enable-runpid configure option which was removed in 1.4.99
- Dropped obsolete provides
- Spec file cleanup

* Wed Nov 18 2009 Kalev Lember <kalev@smartlink.ee> - 1.5.5-1
- Updated to pcsc-lite 1.5.5
- Rebased rpath64 patch
- Dropped upstreamed pcsc-lite-1.5-permissions.patch

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Bob Relyea <rrelyea@redhat.com> - 1.5.2-2
- Pick up security fixes from upstream

* Fri Feb 27 2009 Bob Relyea <rrelyea@redhat.com> - 1.5.2-1
- Pick up 1.5.2
- Add FD_CLOEXEC flag
- make reader.conf a noreplace config file

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.102-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Karsten Hopp <karsten@redhat.com> 1.4.102-4
- remove excludearch s390, s390x (#467788)
  even though s390 does not have libusb or smartCards, the libusb
  packages are required to build other packages.

* Thu Aug 18 2008 Bob Relyea <rrelyea@redhat.com> - 1.4.102-3
- bump tag becaue the build system can't deal with mistakes.

* Thu Aug 18 2008 Bob Relyea <rrelyea@redhat.com> - 1.4.102-2
- mock build changes

* Wed Aug 17 2008 Bob Relyea <rrelyea@redhat.com> - 1.4.102-1
- Pick up 1.4.102

* Wed May 6 2008 Bob Relyea <rrelyea@redhat.com> - 1.4.101-1
- Pick up 1.4.101

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.4-3
- Autorebuild for GCC 4.3

* Wed Jan 16 2008 Bob Relyea <rrelyea@redhat.com> - 1.4.4-2
- Silence libpcsc-lite even when the daemon isn't running.
- fix typo in init file which prevents the config file from being read.

* Tue Nov 22 2007 Bob Relyea <rrelyea@redhat.com> - 1.4.4-1
- Pick up 1.4.4

* Tue Feb 06 2007 Bob Relyea <rrelyea@redhat.com> - 1.3.3-1
- Pick up 1.3.3

* Thu Nov 02 2006 Bob Relyea <rrelyea@redhat.com> - 1.3.2-1
- Pick up 1.3.2

* Thu Sep 14 2006  Bob Relyea <rrelyea@redhat.com> - 1.3.1-7
- Incorporate patch from Ludovic to stop the pcsc daemon from
  unnecessarily waking up.

* Mon Jul 31 2006 Ray Strode <rstrode@redhat.com> - 1.3.1-6
- follow packaging guidelines for setting up init service
  (bug 200778)

* Sun Jul 24 2006 Bob Relyea <rrelyea@redhat.com> - 1.3.1-5
- start pcscd when pcsc-lite is installed

* Sun Jul 16 2006 Florian La Roche <laroche@redhat.com> - 1.3.1-4
- fix excludearch line

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3.1-3.1
- rebuild

* Mon Jul 10 2006 Bob Relyea <rrelyea@redhat.com> - 1.3.1-3
- remove s390 from the build

* Mon Jun 5 2006 Bob Relyea <rrelyea@redhat.com> - 1.3.1-2
- Move to Fedora Core. 
- Remove dependency on graphviz. 
- Removed %%{_dist}

* Sat Apr 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.3.1-1
- 1.3.1.

* Sun Mar  5 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.3.0-1
- 1.3.0, init script and reader.conf updater included upstream.
- Split developer docs into a -doc subpackage, include API docs.
- libmusclecard no longer included, split into separate package upstream.

* Mon Feb 13 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.2.0-14
- Avoid standard rpaths on multilib archs.
- Fine tune dependencies.

* Fri Nov 11 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.0-13
- Don't ship static libraries.
- Don't mark the init script as a config file.
- Use rm instead of %%exclude.
- Specfile cleanups.

* Thu May 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.0-12
- Rebuild.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.0-11
- rebuilt

* Tue Aug 17 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-10
- Disable dependency tracking to speed up the build.
- Drop reader.conf patch, it's not needed any more.
- Rename update-reader-conf to update-reader.conf for consistency with Debian,
  and improve it a bit.

* Sat Jul 31 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.9
- Add update-reader-conf, thanks to Fritz Elfert.

* Thu Jul  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.8
- Own the %%{_libdir}/pcsc hierarchy.

* Thu May 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.7
- Make main package require pcsc-ifd-handler (idea from Debian).

* Wed May 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.6
- Improve package summary.
- Improvements based on suggestions from Ludovic Rousseau:
  - Don't install pcsc_demo but do include its source in -devel.
  - Sync reader.conf with current upstream CVS HEAD (better docs, less
    intrusive in USB-only setups where it's not needed).

* Fri Apr 16 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.5
- Move PDF API docs to -devel.
- Improve main package and init script descriptions.

* Thu Jan 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.4
- Init script fine tuning.

* Fri Jan  9 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.3
- BuildRequires libusb-devel 0.1.6 or newer.

* Thu Oct 30 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.2
- s/pkgconfi/pkgconfig/ in -devel requirements.

* Tue Oct 28 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.1
- Update to 1.2.0.
- Add libpcsc-lite and libmusclecard provides to -libs and -devel.

* Thu Oct 16 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.0.2.rc3
- Update to 1.2.0-rc3.
- Trivial init script improvements.
- Enable %%{_smp_mflags}.
- Don't bother trying to enable SCF.

* Sun Sep 14 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.0.2.rc2
- Specfile cleanups.

* Fri Sep  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.0.1.rc2
- Update to 1.2.0-rc2.

* Wed Aug 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.0.1.rc1
- Update to 1.2.0-rc1.

* Sun Jun  1 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-0.fdr.0.1.beta5
- Update to 1.1.2beta5.

* Sat May 24 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-0.fdr.0.1.beta4
- First build, based on PLD's 1.1.1-2.
