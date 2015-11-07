%if 0%{?fedora} > 15
%bcond_without systemd
%else
%bcond_with systemd
%endif

%global _pkglibdir %{_libdir}/nx
%global _pkgdatadir %{_datadir}/nx
%global _pkglibexecdir %{_libexecdir}/nx

%if 0%{?fedora} || 0%{?rhel} > 5
%global cupsetcdir %{_datadir}/cups/mime
%else
%global cupsetcdir %{_sysconfdir}/cups
%endif

Summary: Free Software (GPL) Implementation of the NX Server
Summary(zh_CN.UTF-8): NX 服务的自由 (GPL) 实现 
Name: freenx-server
Version: 0.7.3
Release: 32%{?dist}
License: GPLv2
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
URL: http://freenx.berlios.de/
Source0: http://download.berlios.de/freenx/%{name}-%{version}.tar.gz
Source1: freenx.logrotate
Source2: freenx-server.service
Source3: freenx-server-check-setup.sh
Patch0: freenx-server-0.7.3-lp-fixes.patch
Patch1: freenx-server-r104-fixes.patch
Patch2: restorecon.patch
Patch3: freenx-server-0.7.3-nxpath-616993.patch
Patch4: freenx-server-0.7.3-nxdialog-627010.patch
Patch5: freenx-server-0.7.3-optflags.patch
Patch6: freenx-server-0.7.3-init.patch
Patch7: freenx-server-0.7.3-nxipp.patch
Patch8: freenx-server-0.7.3-nxagent-version-827176.patch
Patch9: freenx-server-0.7.3-authkeys2-830838.patch
Patch10: freenx-server-0.7.3-ncat-891109-903186.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: imake, magic-release
%if %{with systemd}
BuildRequires: systemd-units
Requires(pre): systemd-sysv chkconfig
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif
Requires: nx%{?_isa} cups
Requires: openssh-server expect which perl
Requires: xorg-x11-server-Xorg xorg-x11-apps xorg-x11-fonts-misc
%if 0%{?fedora} > 17
Requires: nmap-ncat
%else
Requires: nc
%endif

Obsoletes: freenx < %{version}-%{release}
Provides: freenx = %{version}-%{release}

%description
NX is an exciting new technology for remote display. It provides near
local speed application responsiveness over high latency, low
bandwidth links. The core libraries for NX are provided by NoMachine
under the GPL. FreeNX-server is a GPL implementation of the NX Server.

%description -l zh_CN.UTF-8
NX 是一种很好的远程访问技术。NoMachine 基于 GPL 提供了核心库。
这是 NX 服务的一个 GPL 实现。

%prep
%setup -q
%patch0 -p1 -b .lp
%patch1 -p1 -b .fixes
%patch2 -p0 -b .restorecon
%patch3 -p1 -b .nxpath
%patch4 -p1 -b .nxdialog
%patch5 -p1 -b .optflags
%patch6 -p1 -b .init
%patch7 -p1 -b .nxipp
%patch8 -p1 -b .nxagent-version
%patch9 -p1 -b .authkeys2
%if 0%{?fedora} > 17
%patch10 -p1 -b .ncat
%endif

sed -i -e's,\$NX_DIR/bin,%{_pkglibexecdir},g'\
  -e's,\$NX_DIR/lib,%{_pkglibdir},g'\
  nxloadconfig nxserver
sed -i -e's,NX_LOGFILE=/.*,NX_LOGFILE=/var/log/nx/nxserver.log,' \
  -e's,/etc/cups,%{cupsetcdir},' \
  nxloadconfig node.conf.sample

%build
export CFLAGS="%{optflags}" MODULE_CFLAGS="%{optflags}" \
  LDFLAGS="%{?__global_ldflags}" LOCAL_LDFLAGS="%{?__global_ldflags}"
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} NX_ETC_DIR=/etc/nxserver
mkdir -p %{buildroot}%{_sbindir}
ln -s %{_pkglibexecdir}/nx{setup,keygen} %{buildroot}%{_sbindir}
install -pm 755 %{SOURCE3} \
  %{buildroot}%{_pkglibexecdir}/freenx-server-check-setup
rename .sample "" %{buildroot}/etc/nxserver/node.conf.sample

for file in users.id_dsa client.id_dsa.key server.id_dsa.pub.key \
  passwords{,.orig} ; do
  touch %{buildroot}/etc/nxserver/$file
  chmod 600 %{buildroot}/etc/nxserver/$file
done
touch %{buildroot}/etc/nxserver/users.id_dsa.pub

# Create the nx user home
mkdir -p %{buildroot}/var/lib/nxserver/home/.ssh
chmod -R 0700 %{buildroot}/var/lib/nxserver
touch %{buildroot}/var/lib/nxserver/home/.ssh/authorized_keys
touch %{buildroot}/var/lib/nxserver/home/.ssh/authorized_keys.disabled
touch %{buildroot}/var/lib/nxserver/home/.ssh/client.id_dsa.key
touch %{buildroot}/var/lib/nxserver/home/.ssh/known_hosts
touch %{buildroot}/var/lib/nxserver/home/.ssh/server.id_dsa.pub.key
chmod 0600 %{buildroot}/var/lib/nxserver/home/.ssh/*
mkdir -p %{buildroot}/var/lib/nxserver/db/closed
mkdir -p %{buildroot}/var/lib/nxserver/db/running
mkdir -p %{buildroot}/var/lib/nxserver/db/failed
chmod -R 0700 %{buildroot}/var/lib/nxserver/db

mkdir -p %{buildroot}/var/log/nx
chmod 0700 %{buildroot}/var/log/nx

ln -s ipp %{buildroot}/usr/lib/cups/backend/nxipp

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -p %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/freenx-server

%if %{with systemd}
install -Dpm 644 %{SOURCE2} %{buildroot}%{_unitdir}/freenx-server.service
%else
mkdir -p %{buildroot}%{_sysconfdir}/init.d
install -p init.d/freenx-server %{buildroot}%{_sysconfdir}/init.d/freenx-server
%endif

%clean
rm -rf %{buildroot}

%pre
%{_sbindir}/useradd -r -d /var/lib/nxserver/home -s %{_pkglibexecdir}/nxserver nx 2>/dev/null \
  || %{_sbindir}/usermod -d /var/lib/nxserver/home -s %{_pkglibexecdir}/nxserver nx 2>/dev/null || :
%if %{with systemd}
if [ $1 -gt 1 ] && [ ! -e %{_unitdir}/freenx-server.service ] && \
   [ -e %{_sysconfdir}/init.d/freenx-server ] ; then
        systemd-sysv-convert --save freenx-server &>/dev/null
        chkconfig --del freenx-server &>/dev/null || :
fi
%endif

%post
%if %{with systemd}
systemctl daemon-reload &>/dev/null
%else
/sbin/chkconfig --add freenx-server
%endif
if [ $1 -gt 1 ]; then # for migrating to >= 0.7.3-27
    cd /var/lib/nxserver/home/.ssh
    [ -e authorized_keys2 ] && [ ! -e authorized_keys ] && \
        mv authorized_keys2 authorized_keys
    [ -e authorized_keys2.disabled ] && [ ! -e authorized_keys.disabled ] && \
        mv authorized_keys2.disabled authorized_keys.disabled
fi
exit 0

%preun
if [ $1 = 0 ]; then
%if %{with systemd}
        systemctl --no-reload disable freenx-server.service &>/dev/null
        systemctl stop freenx-server.service &>/dev/null
%else
        /sbin/service freenx-server stop > /dev/null 2>&1
        /sbin/chkconfig --del freenx-server
%endif
        exit 0
fi

%if %{with systemd}
%postun
systemctl daemon-reload &>/dev/null || :
%endif

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog CONTRIB
%{_sbindir}/nx*
%{_pkglibexecdir}/*
%{_pkglibdir}/*
/usr/lib/cups/backend/nxipp
/usr/lib/cups/backend/nxsmb
%config(noreplace) %{_sysconfdir}/logrotate.d/freenx-server
%if %{with systemd}
%{_unitdir}/freenx-server.service
%else
%{_sysconfdir}/init.d/freenx-server
%endif
%defattr(-,nx,nx,-)
%ghost /etc/nxserver/client.id_dsa.key
%ghost /etc/nxserver/server.id_dsa.pub.key
%defattr(-,nx,root,-)
%dir /etc/nxserver
%config(noreplace) /etc/nxserver/node.conf
%ghost /etc/nxserver/users.id_dsa
%ghost /etc/nxserver/users.id_dsa.pub
%ghost /etc/nxserver/passwords
%ghost /etc/nxserver/passwords.orig
%dir /var/lib/nxserver
/var/lib/nxserver/db
%dir /var/lib/nxserver/home
%dir /var/lib/nxserver/home/.ssh
%ghost /var/lib/nxserver/home/.ssh/*
/var/log/nx

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 0.7.3-32
- 为 Magic 3.0 重建

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 24 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-30
- Hush ncat output that confuses NoMachine NX client (#903186, Rok Mandeljc).

* Wed Jan  9 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-29
- Patch to work with ncat in F-18+ (#891109).
- Add Documentation field to systemd service.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-27
- Use authorized_keys instead of *_keys2 for OpenSSH 5.9p1 compat (#830838).
- Drop EL < 5 build support.

* Mon Jun  4 2012 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-26
- Hush bogus NX 3.[45] incompatibility warning (Christian Ziemski, #827176).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 31 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-24
- Check that nxsetup has run before starting freenx-server.service (#770814).
- Make freenx-server.service require sshd.service.
- Symlink nxipp to cups' ipp instead of copying it.
- Build with %%{__global_ldflags}.
- Drop nx and cups dir dependencies, just require the packages (#602267).
- Sync /etc/nxserver/* ownership and permissions with what nxsetup sets.
- Own/ghost more files created by nxsetup.
- Drop node.conf.sample.

* Wed Aug 17 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-23
- Migrate to systemd on F-16+ (#714446).
- Fix init script to actually clean up sessions and to enable/disable logins,
  ship service disabled by default.
- Fix default CUPS config dir on Fedora and EL-6+.
- Build everything with %%{optflags}.
- Use %%global instead of %%define.
- Clean up list of installed files.

* Mon Jun 20 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-22
- Fix nxdialog when /usr/bin/dialog is available but xterm isn't (#627010).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-20
- Fix incorrect service start status when restorecon doesn't exist.

* Wed Jul 21 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-19
- Apply improvements from Fedora bug #616993:
- Install nxkeygen and nxsetup symlinks in /usr/sbin.
- Patch nxkeygen and nxsetup to work when invoked via a symlink.
- Drop nxsetup from docs.

* Mon Nov 23 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.3-17
- Rebase to launchpad development bzr code.
- Add status to init file.
- Fix persistent session switch.
- Use md5sum (instead of openssl md5) for consistent hashes.

* Sat Jul 25 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.3-14
- Use some patches from up to svn 613 (dated 2008-09-01).
- Add keymap.patch from Fedora bug #506470.
- Add cups listing patch from Fedora bug #509879.
- Add dependency for misc fonts Fedora bug #467494.
- Fix stale X11 displays from Fedora bug #492402.
- Fix authorized_keys*2* syncing, may fix Fedora bug #503822.
- Move %%post parts to nxserver startup, fixes Fedora bug #474720.
- Copy ssh keys on first start, fixes Fedora bug #235592.
- Add init script with CentOS patches that ensures /tmp/.X11-unix
  always exists, fixes Fedora bug #437655.

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.3-11
- Rebase patch to 0.7.2 to avoid fuzz=0 rejection on recent rpm.
- Update to 0.7.3.
- NX_ETC_DIR needs to be passed on command line (workaround).

* Tue Apr  8 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.2-7
- Rename the logrotate file to match the package name.

* Sat Mar 29 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.2-6
- Update to 0.7.2.
- Upstream project renamed to freenx-server.

* Mon Dec 31 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.1-4
- Apply Jeffrey J. Kosowsky's patches to enable multimedia and
  file/print sharing support (Fedora bug #216802).
- Silence %%post output, when openssh's server has never been started
  before (Fedora bug #235592).
- Add dependency on which (Fedora bug #250343).

* Mon Dec 10 2007 Jon Ciesla <limb@jcomserv.net> - 0.7.1-3
- Fix syntax error in logrotate file, BZ 418221.

* Mon Nov 19 2007 Jon Ciesla <limb@jcomserv.net> - 0.7.1-2
- Added logrotate, BZ 379761.

* Mon Nov 19 2007 Jon Ciesla <limb@jcomserv.net> - 0.7.1-1
- Update to 0.7.1, many bugfixes, BZ 364751, 373771.

* Sun Sep 23 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.7.0-2
- Do not try to set up KDE_PRINTRC if ENABLE_KDE_CUPS is not 1, deal better
  with errors when it is (#290351).

* Thu Sep 6 2007 Jon Ciesla <limb@jcomserv.net> - 0.7.0-1
- CM = Christian Mandery mail@chrismandery.de,  BZ 252976
- Version bump to 0.7.0 upstream release (CM)
- Fixed download URL (didn't work, Berlios changed layout). (CM)
- Changed license field from GPL to GPLv2 in RPM. (CM)
- Fixed release.

* Mon Feb 19 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6.0-9
- Update to 0.6.0.

* Sat Sep 17 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.4.4.

* Sat Jul 30 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.4.2.

* Sat Jul  9 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.4.1.

* Tue Mar 22 2005 Rick Stout <zipsonic[AT]gmail.com> - 0:0.3.1
- Updated to 0.3.1 release

* Tue Mar 08 2005 Rick Stout <zipsonic[AT]gmail.com> - 0:0.3.0
- Updated to 0.3.0 release
- Removed home directory patch as it is now default

* Mon Feb 14 2005 Rick Stout <zipsonic[AT]gmail.com> - 0:0.2.8
- Updated to 0.2.8 release
- Fixes some security issues
- Added geom-fix patch for windows client resuming issues

* Thu Dec 02 2004 Rick Stout <zipsonic[AT]gmail.com> - 1:0.2.7
- Fixed package removal not removing the var session directories

* Tue Nov 23 2004 Rick Stout <zipsonic[AT]gmail.com> - 0:0.2.7
- Updated to 0.2.7 release
- fixes some stability issues with 0.2.6

* Fri Nov 12 2004 Rick Stout <zipsonic[AT]gmail.com> - 1:0.2.6
- Fixed a problem with key backup upon removal

* Fri Nov 12 2004 Rick Stout <zipsonic[AT]gmail.com> - 0:0.2.6
- Updated to 0.2.6 release
- Changed setup to have nx user account added as a system account.
- Changed nx home directory to /var/lib/nxserver/nxhome

* Thu Oct 14 2004 Rick Stout <zipsonic[AT]gmail.com> - 0:0.2.5
- updated package to 0.2.5 release
- still applying patch for netcat and useradd

* Fri Oct 08 2004 Rick Stout <zipsonic[AT]gmail.com> - 3:0.2.4
- Added nxsetup functionality to the rpm
- patched nxsetup (fnxncuseradd) script for occasional path error.
- Added patch (fnxncuseradd) to resolve newer client connections (netcat -> nc)
- Changed name to be more friendly (lowercase)
- Added known dependencies

* Thu Sep 30 2004 Rick Stout <zipsonic[AT]gmail.com> - 2:0.2.4
- Patch (fnxpermatch) to fix permissions with key generation

* Wed Sep 29 2004 Rick Stout <zipsonic[AT]gmail.com> - 1:0.2.4
- Initial Fedora RPM release.
- Updated SuSE package for Fedora
