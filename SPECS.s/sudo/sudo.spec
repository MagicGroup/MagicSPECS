Summary: Allows restricted root access for specified users
Summary(zh_CN.UTF-8): 允许指定的用户使用 root 权限
Name: sudo
Version:	1.8.14p3
Release:	1%{?dist}
License: ISC
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://www.courtesan.com/sudo/
Source0: http://www.courtesan.com/sudo/dist/sudo-%{version}.tar.gz
Source1: sudo-1.7.4p4-sudoers
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: /etc/pam.d/system-auth, vim-minimal

BuildRequires: pam-devel
BuildRequires: groff
BuildRequires: openldap-devel
BuildRequires: flex
BuildRequires: bison
BuildRequires: automake autoconf libtool
BuildRequires: libcap-devel
BuildRequires: sendmail
BuildRequires: gettext

# don't strip
Patch1: sudo-1.6.7p5-strip.patch
# Patch to read ldap.conf more closely to nss_ldap
Patch2: sudo-1.8.14p1-ldapconfpatch.patch
# Patch makes changes in documentation bz:1162070
Patch3: sudo-1.8.14p1-docpassexpire.patch
# Patch initialize variable before executing sudo_strsplit
Patch4: sudo-1.8.14p3-initialization.patch
# Patch resolves deadcode in visudo.c from coverity scan.
Patch5: sudo-1.8.14p3-deadcode_visudo_c.patch
Patch6: sudo-1.8.14p3-extra_while.patch

%description
Sudo (superuser do) allows a system administrator to give certain
users (or groups of users) the ability to run some (or all) commands
as root while logging all commands and arguments. Sudo operates on a
per-command basis.  It is not a replacement for the shell.  Features
include: the ability to restrict what commands a user may run on a
per-host basis, copious logging of each command (providing a clear
audit trail of who did what), a configurable timeout of the sudo
command, and the ability to use the same configuration file (sudoers)
on many different machines.

%description -l zh_CN.UTF-8
允许指定的用户使用 root 权限运行一些（或全部）命令。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains header files developing sudo
plugins that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%patch1 -p1 -b .strip
%patch2 -p1 -b .envdebug
%patch3 -p1 -b .m4path
%patch4 -p1 -b .pipelist
%patch5 -p1 -b .CVE-2012-0809
%patch6 -p1 -b .sssd-support

# Remove execute permission on this script so we don't pull in perl deps
chmod -x plugins/sudoers/sudoers2ldif

%build
autoreconf -fv --install

%ifarch s390 s390x sparc64
F_PIE=-fPIE
%else
F_PIE=-fpie
%endif

export CFLAGS="$RPM_OPT_FLAGS $F_PIE" LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"

%configure \
        --prefix=%{_prefix} \
        --sbindir=%{_sbindir} \
        --libdir=%{_libdir} \
	--docdir=%{_datadir}/doc/%{name}-%{version} \
        --with-logging=syslog \
        --with-logfac=authpriv \
        --with-pam \
	--with-pam-login \
        --with-editor=/bin/vi \
        --with-env-editor \
        --with-ignore-dot \
        --with-tty-tickets \
        --with-ldap \
	--without-selinux \
	--with-passprompt="[sudo] password for %p: " \
	--without-linux-audit	  \
	--without-sssd

#	--without-kerb5 \
#	--without-kerb4
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT" install_uid=`id -u` install_gid=`id -g` sudoers_uid=`id -u` sudoers_gid=`id -g`

chmod 755 $RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT%{_sbindir}/* 
install -p -d -m 700 $RPM_BUILD_ROOT/var/db/sudo
install -p -d -m 750 $RPM_BUILD_ROOT/etc/sudoers.d
install -p -c -m 0440 %{SOURCE1} $RPM_BUILD_ROOT/etc/sudoers

# Remove examples; Examples can be found in man pages too.
rm -rf $RPM_BUILD_ROOT%{_datadir}/examples/sudo

#Remove all .la files
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

magic_rpm_clean.sh
%find_lang sudo
%find_lang sudoers

cat sudo.lang sudoers.lang > sudo_all.lang
rm sudo.lang sudoers.lang

mkdir -p $RPM_BUILD_ROOT/etc/pam.d
cat > $RPM_BUILD_ROOT/etc/pam.d/sudo << EOF
#%PAM-1.0
auth       include      system-auth
account    include      system-auth
password   include      system-auth
session    optional     pam_keyinit.so revoke
session    required     pam_limits.so
EOF

cat > $RPM_BUILD_ROOT/etc/pam.d/sudo-i << EOF
#%PAM-1.0
auth       include      sudo
account    include      sudo
password   include      sudo
session    optional     pam_keyinit.so force revoke
session    required     pam_limits.so
EOF


%clean 
rm -rf $RPM_BUILD_ROOT

%files -f sudo_all.lang
%defattr(-,root,root)
%attr(0440,root,root) %config(noreplace) /etc/sudoers
%attr(0750,root,root) %dir /etc/sudoers.d/
%config(noreplace) /etc/pam.d/sudo
%config(noreplace) /etc/pam.d/sudo-i
%attr(0644,root,root) %{_tmpfilesdir}/sudo.conf
%dir /var/db/sudo
%attr(4111,root,root) %{_bindir}/sudo
%{_bindir}/sudoedit
%attr(0111,root,root) %{_bindir}/sudoreplay
%attr(0755,root,root) %{_sbindir}/visudo
%dir %{_libexecdir}/sudo
%attr(0644,root,root) %{_libexecdir}/sudo/sudo_noexec.so
%attr(0644,root,root) %{_libexecdir}/sudo/sudoers.so
%attr(0644,root,root) %{_libexecdir}/sudo/group_file.so
%attr(0644,root,root) %{_libexecdir}/sudo/system_group.so
%attr(0644,root,root) %{_libexecdir}/sudo/libsudo_util.so.?.?.?
%{_libexecdir}/sudo/libsudo_util.so.?
%{_mandir}/man5/sudoers.5*
%{_mandir}/man5/sudoers.ldap.5*
%{_mandir}/man5/sudo.conf.5*
%{_mandir}/man8/sudo.8*
%{_mandir}/man8/sudoedit.8*
%{_mandir}/man8/sudoreplay.8*
%{_mandir}/man8/visudo.8*
%dir %{_pkgdocdir}/
%{_pkgdocdir}/*
%{!?_licensedir:%global license %%doc}
%license doc/LICENSE
%exclude %{_pkgdocdir}/ChangeLog


# Make sure permissions are ok even if we're updating
%post
/bin/chmod 0440 /etc/sudoers || :

%files devel
%defattr(-,root,root,-)
%doc plugins/sample/sample_plugin.c
%{_includedir}/sudo_plugin.h
%{_mandir}/man8/sudo_plugin.8*
%{_libexecdir}/sudo/libsudo_util.so

%changelog
* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 1.8.14p3-1
- 更新到 1.8.14p3

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.8.3p1-5
- 为 Magic 3.0 重建

* Tue Feb  7 2012 Daniel Kopecek <dkopecek@redhat.com> - 1.8.3p1-4
- added SSSD support

* Thu Jan 26 2012 Daniel Kopecek <dkopecek@redhat.com> - 1.8.3p1-3
- added patch for CVE-2012-0809

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3p1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 10 2011 Daniel Kopecek <dkopecek@redhat.com> - 1.8.3p1-1
- update to 1.8.3p1
- disable output word wrapping if the output is piped 

* Wed Sep  7 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8.1p2-2
- Remove execute bit from sample script in docs so we don't pull in perl

* Tue Jul 12 2011 Daniel Kopecek <dkopecek@redhat.com> - 1.8.1p2-1
- rebase to 1.8.1p2
- removed .sudoi patch
- fixed typo: RELPRO -> RELRO
- added -devel subpackage for the sudo_plugin.h header file
- use default ldap configuration files again

* Fri Jun  3 2011 Daniel Kopecek <dkopecek@redhat.com> - 1.7.4p5-4
- build with RELRO

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4p5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Daniel Kopecek <dkopecek@redhat.com> - 1.7.4p5-2
- rebase to 1.7.4p5
- fixed sudo-1.7.4p4-getgrouplist.patch
- fixes CVE-2011-0008, CVE-2011-0010

* Tue Nov 30 2010 Daniel Kopecek <dkopecek@redhat.com> - 1.7.4p4-5
- anybody in the wheel group has now root access (using password) (rhbz#656873)
- sync configuration paths with the nss_ldap package (rhbz#652687)

* Wed Sep 29 2010 Daniel Kopecek <dkopecek@redhat.com> - 1.7.4p4-4
- added upstream patch to fix rhbz#638345

* Mon Sep 20 2010 Daniel Kopecek <dkopecek@redhat.com> - 1.7.4p4-3
- added patch for #635250
- /var/run/sudo -> /var/db/sudo in .spec

* Tue Sep  7 2010 Daniel Kopecek <dkopecek@redhat.com> - 1.7.4p4-2
- sudo now uses /var/db/sudo for timestamps

* Tue Sep  7 2010 Daniel Kopecek <dkopecek@redhat.com> - 1.7.4p4-1
- update to new upstream version
- new command available: sudoreplay
- use native audit support
- corrected license field value: BSD -> ISC

* Wed Jun  2 2010 Daniel Kopecek <dkopecek@redhat.com> - 1.7.2p6-2
- added patch that fixes insufficient environment sanitization issue (#598154)

* Wed Apr 14 2010 Daniel Kopecek <dkopecek@redhat.com> - 1.7.2p6-1
- update to new upstream version
- merged .audit and .libaudit patch
- added sudoers.ldap.5* to files

* Mon Mar  1 2010 Daniel Kopecek <dkopecek@redhat.com> - 1.7.2p5-2
- update to new upstream version

* Tue Feb 16 2010 Daniel Kopecek <dkopecek@redhat.com> - 1.7.2p2-5
- fixed no valid sudoers sources found (#558875)

* Wed Feb 10 2010 Daniel Kopecek <dkopecek@redhat.com> - 1.7.2p2-4
- audit related Makefile.in and configure.in corrections
- added --with-audit configure option
- removed call to libtoolize

* Wed Feb 10 2010 Daniel Kopecek <dkopecek@redhat.com> - 1.7.2p2-3
- fixed segfault when #include directive is used in cycles (#561336)

* Fri Jan  8 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.7.2p2-2
- Add /etc/sudoers.d dir and use it in default config (#551470).
- Drop *.pod man page duplicates from docs.

* Thu Jan 07 2010 Daniel Kopecek <dkopecek@redhat.com> - 1.7.2p2-1
- new upstream version 1.7.2p2-1
- commented out unused aliases in sudoers to make visudo happy (#550239)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.7.1-7
- rebuilt with new audit

* Thu Aug 20 2009 Daniel Kopecek <dkopecek@redhat.com> 1.7.1-6
- moved secure_path from compile-time option to sudoers file (#517428)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 09 2009 Daniel Kopecek <dkopecek@redhat.com> 1.7.1-4
- moved the closefrom() call before audit_help_open() (sudo-1.7.1-auditfix.patch)
- epoch number sync

* Mon Jun 22 2009 Daniel Kopecek <dkopecek@redhat.com> 1.7.1-1
- updated sudo to version 1.7.1
- fixed small bug in configure.in (sudo-1.7.1-conffix.patch)

* Tue Feb 24 2009 Daniel Kopecek <dkopecek@redhat.com> 1.6.9p17-6
- fixed building with new libtool
- fix for incorrect handling of groups in Runas_User
- added /usr/local/sbin to secure-path

* Tue Jan 13 2009 Daniel Kopecek <dkopecek@redhat.com> 1.6.9p17-3
- build with sendmail installed
- Added /usr/local/bin to secure-path

* Tue Sep 02 2008 Peter Vrabec <pvrabec@redhat.com> 1.6.9p17-2
- adjust audit patch, do not scream when kernel is
  compiled without audit netlink support (#401201)

* Fri Jul 04 2008 Peter Vrabec <pvrabec@redhat.com> 1.6.9p17-1
- upgrade

* Wed Jun 18 2008 Peter Vrabec <pvrabec@redhat.com> 1.6.9p13-7
- build with newer autoconf-2.62 (#449614)

* Tue May 13 2008 Peter Vrabec <pvrabec@redhat.com> 1.6.9p13-6
- compiled with secure path (#80215)

* Mon May 05 2008 Peter Vrabec <pvrabec@redhat.com> 1.6.9p13-5
- fix path to updatedb in /etc/sudoers (#445103)

* Mon Mar 31 2008 Peter Vrabec <pvrabec@redhat.com> 1.6.9p13-4
- include ldap files in rpm package (#439506)

* Thu Mar 13 2008 Peter Vrabec <pvrabec@redhat.com> 1.6.9p13-3
- include [sudo] in password prompt (#437092)

* Tue Mar 04 2008 Peter Vrabec <pvrabec@redhat.com> 1.6.9p13-2
- audit support improvement

* Thu Feb 21 2008 Peter Vrabec <pvrabec@redhat.com> 1.6.9p13-1
- upgrade to the latest upstream release

* Wed Feb 06 2008 Peter Vrabec <pvrabec@redhat.com> 1.6.9p12-1
- upgrade to the latest upstream release
- add selinux support

* Mon Feb 02 2008 Dennis Gilmore <dennis@ausil.us> 1.6.9p4-6
- sparc64 needs to be in the -fPIE list with s390

* Mon Jan 07 2008 Peter Vrabec <pvrabec@redhat.com> 1.6.9p4-5
- fix complains about audit_log_user_command(): Connection 
  refused (#401201)

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.6.9p4-4
- Rebuild for deps

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.6.9p4-3
- Rebuild for openssl bump

* Thu Aug 30 2007 Peter Vrabec <pvrabec@redhat.com> 1.6.9p4-2
- fix autotools stuff and add audit support

* Mon Aug 20 2007 Peter Vrabec <pvrabec@redhat.com> 1.6.9p4-1
- upgrade to upstream release

* Thu Apr 12 2007 Peter Vrabec <pvrabec@redhat.com> 1.6.8p12-14
- also use getgrouplist() to determine group membership (#235915)

* Mon Feb 26 2007 Peter Vrabec <pvrabec@redhat.com> 1.6.8p12-13
- fix some spec file issues

* Thu Dec 14 2006 Peter Vrabec <pvrabec@redhat.com> 1.6.8p12-12
- fix rpmlint issue

* Thu Oct 26 2006 Peter Vrabec <pvrabec@redhat.com> 1.6.8p12-11
- fix typo in sudoers file (#212308)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.6.8p12-10
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Peter Vrabec <pvrabec@redhat.com> 1.6.8p12-9
- fix sudoers file, X apps didn't work (#206320)

* Tue Aug 08 2006 Peter Vrabec <pvrabec@redhat.com> 1.6.8p12-8
- use Red Hat specific default sudoers file

* Sun Jul 16 2006 Karel Zak <kzak@redhat.com> 1.6.8p12-7
- fix #198755 - make login processes (sudo -i) initialise session keyring
  (thanks for PAM config files to David Howells)
- add IPv6 support (patch by Milan Zazrivec)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.6.8p12-6.1
- rebuild

* Mon May 29 2006 Karel Zak <kzak@redhat.com> 1.6.8p12-6
- fix #190062 - "ssh localhost sudo su" will show the password in clear

* Tue May 23 2006 Karel Zak <kzak@redhat.com> 1.6.8p12-5
- add LDAP support (#170848)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.6.8p12-4.1
- bump again for double-long bug on ppc(64)

* Wed Feb  8 2006 Karel Zak <kzak@redhat.com> 1.6.8p12-4
- reset env. by default

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.6.8p12-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Dan Walsh <dwalsh@redhat.com> 1.6.8p12-3
- Remove selinux patch.  It has been decided that the SELinux patch for sudo is
- no longer necessary.  In tageted policy it had no effect.  In strict/MLS policy
- We require the person using sudo to execute newrole before using sudo.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 25 2005 Karel Zak <kzak@redhat.com> 1.6.8p12-1
- new upstream version 1.6.8p12

* Tue Nov  8 2005 Karel Zak <kzak@redhat.com> 1.6.8p11-1
- new upstream version 1.6.8p11

* Thu Oct 13 2005 Tomas Mraz <tmraz@redhat.com> 1.6.8p9-6
- use include instead of pam_stack in pam config

* Tue Oct 11 2005 Karel Zak <kzak@redhat.com> 1.6.8p9-5
- enable interfaces in selinux patch
- merge sudo-1.6.8p8-sesh-stopsig.patch to selinux patch

* Mon Sep 19 2005 Karel Zak <kzak@redhat.com> 1.6.8p9-4
- fix debuginfo

* Mon Sep 19 2005 Karel Zak <kzak@redhat.com> 1.6.8p9-3
- fix #162623 - sesh hangs when child suspends

* Mon Aug 1 2005 Dan Walsh <dwalsh@redhat.com> 1.6.8p9-2
- Add back in interfaces call, SELinux has been fixed to work around

* Tue Jun 21 2005 Karel Zak <kzak@redhat.com> 1.6.8p9-1
- new version 1.6.8p9 (resolve #161116 - CAN-2005-1993 sudo trusted user arbitrary command execution)

* Tue May 24 2005 Karel Zak <kzak@redhat.com> 1.6.8p8-2
- fix #154511 - sudo does not use limits.conf

* Mon Apr  4 2005 Thomas Woerner <twoerner@redhat.com> 1.6.8p8-1
- new version 1.6.8p8: new sudoedit and sudo_noexec

* Wed Feb  9 2005 Thomas Woerner <twoerner@redhat.com> 1.6.7p5-31
- rebuild

* Mon Oct  4 2004 Thomas Woerner <twoerner@redhat.com> 1.6.7p5-30.1
- added missing BuildRequires for libselinux-devel (#132883) 

* Wed Sep 29 2004 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-30
- Fix missing param error in sesh

* Mon Sep 27 2004 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-29
- Remove full patch check from sesh

* Thu Jul 8 2004 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-28
- Fix selinux patch to switch to root user

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 13 2004 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-26
- Eliminate tty handling from selinux

* Thu Apr  1 2004 Thomas Woerner <twoerner@redhat.com> 1.6.7p5-25
- fixed spec file: sesh in file section with selinux flag (#119682)

* Thu Mar 30 2004 Colin Walters <walters@redhat.com> 1.6.7p5-24
- Enhance sesh.c to fork/exec children itself, to avoid
  having sudo reap all domains.
- Only reinstall default signal handlers immediately before
  exec of child with SELinux patch

* Thu Mar 18 2004 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-23
- change to default to sysadm_r 
- Fix tty handling

* Thu Mar 18 2004 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-22
- Add /bin/sesh to run selinux code.
- replace /bin/bash -c with /bin/sesh

* Tue Mar 16 2004 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-21
- Hard code to use "/bin/bash -c" for selinux 

* Tue Mar 16 2004 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-20
- Eliminate closing and reopening of terminals, to match su.

* Mon Mar 15 2004 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-19
- SELinux fixes to make transitions work properly

* Fri Mar  5 2004 Thomas Woerner <twoerner@redhat.com> 1.6.7p5-18
- pied sudo

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-16
- Eliminate interfaces call, since this requires big SELinux privs
- and it seems to be useless.

* Tue Jan 27 2004 Karsten Hopp <karsten@redhat.de> 1.6.7p5-15
- visudo requires vim-minimal or setting EDITOR to something useful (#68605)

* Mon Jan 26 2004 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-14
- Fix is_selinux_enabled call

* Tue Jan 13 2004 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-13
- Clean up patch on failure 

* Tue Jan 6 2004 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-12
- Remove sudo.te for now.

* Fri Jan 2 2004 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-11
- Fix usage message

* Mon Dec 22 2003 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-10
- Clean up sudo.te to not blow up if pam.te not present

* Thu Dec 18 2003 Thomas Woerner <twoerner@redhat.com>
- added missing BuildRequires for groff

* Tue Dec 16 2003 Jeremy Katz <katzj@redhat.com> 1.6.7p5-9
- remove left-over debugging code

* Tue Dec 16 2003 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-8
- Fix terminal handling that caused Sudo to exit on non selinux machines.

* Mon Dec 15 2003 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-7
- Remove sudo_var_run_t which is now pam_var_run_t

* Fri Dec 12 2003 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-6
- Fix terminal handling and policy

* Thu Dec 11 2003 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-5
- Fix policy

* Thu Nov 13 2003 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-4.sel
- Turn on SELinux support

* Tue Jul 29 2003 Dan Walsh <dwalsh@redhat.com> 1.6.7p5-3
- Add support for SELinux

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 19 2003 Thomas Woerner <twoerner@redhat.com> 1.6.7p5-1

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Nov 12 2002 Nalin Dahyabhai <nalin@redhat.com> 1.6.6-2
- remove absolute path names from the PAM configuration, ensuring that the
  right modules get used for whichever arch we're built for
- don't try to install the FAQ, which isn't there any more

* Thu Jun 27 2002 Bill Nottingham <notting@redhat.com> 1.6.6-1
- update to 1.6.6

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Apr 18 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.6.5p2-2
- Fix bug #63768

* Thu Mar 14 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.6.5p2-1
- 1.6.5p2

* Fri Jan 18 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.6.5p1-1
- 1.6.5p1
- Hope this "a new release per day" madness stops ;)

* Thu Jan 17 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.6.5-1
- 1.6.5

* Tue Jan 15 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.6.4p1-1
- 1.6.4p1

* Mon Jan 14 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.6.4-1
- Update to 1.6.4

* Mon Jul 23 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.6.3p7-2
- Add build requirements (#49706)
- s/Copyright/License/
- bzip2 source

* Sat Jun 16 2001 Than Ngo <than@redhat.com>
- update to 1.6.3p7
- use %%{_tmppath}

* Fri Feb 23 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.6.3p6, fixes buffer overrun

* Tue Oct 10 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.6.3p5

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 06 2000 Karsten Hopp <karsten@redhat.de>
- fixed owner of sudo and visudo

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- modify PAM setup to use system-auth
- clean up buildrooting by using the makeinstall macro

* Tue Apr 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- initial build in main distrib
- update to 1.6.3
- deal with compressed man pages

* Tue Dec 14 1999 Preston Brown <pbrown@redhat.com>
- updated to 1.6.1 for Powertools 6.2
- config files are now noreplace.

* Thu Jul 22 1999 Tim Powers <timp@redhat.com>
- updated to 1.5.9p2 for Powertools 6.1

* Wed May 12 1999 Bill Nottingham <notting@redhat.com>
- sudo is configured with pam. There's no pam.d file. Oops.

* Mon Apr 26 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 1.59p1 for powertools 6.0

* Tue Oct 27 1998 Preston Brown <pbrown@redhat.com>
- fixed so it doesn't find /usr/bin/vi first, but instead /bin/vi (always installed)

* Fri Oct 08 1998 Michael Maher <mike@redhat.com>
- built package for 5.2 

* Mon May 18 1998 Michael Maher <mike@redhat.com>
- updated SPEC file

* Thu Jan 29 1998 Otto Hammersmith <otto@redhat.com>
- updated to 1.5.4

* Tue Nov 18 1997 Otto Hammersmith <otto@redhat.com>
- built for glibc, no problems

* Fri Apr 25 1997 Michael Fulbright <msf@redhat.com>
- Fixed for 4.2 PowerTools 
- Still need to be pamified
- Still need to move stmp file to /var/log

* Mon Feb 17 1997 Michael Fulbright <msf@redhat.com>
- First version for PowerCD.

