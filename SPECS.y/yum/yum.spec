%define move_yum_conf_back 1
%define auto_sitelib 1
%define yum_updatesd 0
%define disable_check 1
%define yum_cron_systemd 1

%if 0%{?rhel} <= 6
# rhel-6 doesn't have the systemd stuff...
%define yum_cron_systemd 0
%endif

%if 0%{?fedora} <= 18
# yum in Fedora <= 18 doesn't use systemd unit files...
%define yum_cron_systemd 0
%endif

%if %{auto_sitelib}

%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%else
%define python_sitelib /usr/lib/python?.?/site-packages
%endif

# We always used /usr/lib here, even on 64bit ... so it's a bit meh.
%define yum_pluginslib   /usr/lib/yum-plugins
%define yum_pluginsshare /usr/share/yum-plugins

Summary: RPM package installer/updater/manager
Name: yum
Version: 3.4.3
Release: 64%{?dist}
License: GPLv2+
Group: System Environment/Base
Source0: http://yum.baseurl.org/download/3.4/%{name}-%{version}.tar.gz
Source1: yum.conf.fedora
Source2: yum-updatesd.conf.fedora
Patch1: yum-distro-configs.patch
Patch4: no-more-exactarchlist.patch
Patch5: geode-arch.patch
Patch6: yum-HEAD.patch
Patch7: yum-ppc64-preferred.patch
Patch20: yum-manpage-files.patch
Patch21: yum-completion-helper.patch
Patch22: native-drpm-support.patch

URL: http://yum.baseurl.org/
BuildArchitectures: noarch
BuildRequires: python
BuildRequires: gettext
BuildRequires: intltool
# This is really CheckRequires ...
BuildRequires: python-nose
BuildRequires: python >= 2.4
BuildRequires: rpm-python, rpm >= 0:4.4.2
BuildRequires: python-iniparse
BuildRequires: python-sqlite
BuildRequires: python-urlgrabber >= 3.9.0-8
BuildRequires: yum-metadata-parser >= 1.1.0
BuildRequires: pygpgme
# End of CheckRequires
Conflicts: pirut < 1.1.4
Requires: python >= 2.4
Requires: rpm-python, rpm >= 0:4.4.2
Requires: python-iniparse
Requires: python-sqlite
Requires: python-urlgrabber >= 3.9.0-8
Requires: yum-metadata-parser >= 1.1.0
Requires: pygpgme
# rawhide is >= 0.5.3-7.fc18 ... as this is added.
Requires: pyliblzma
# This is really a suggests, but we have none...
Requires: pyxattr

Conflicts: rpm >= 5-0
# Zif is a re-implementation of yum in C, however:
#
# 1. There is no co-operation/etc. with us.
# 2. It touches our private data directly.
#
# ...both of which mean that even if there were _zero_ bugs in zif, we'd
# never be able to change anything after the first user started using it. And
# of course:
#
# 3. Users will never be able to tell that it isn't weird yum bugs, when they
# hit them (and we'll probably never be able to debug them, without becoming
# zif experts).
#
# ...so we have two sane choices: i) Conflict with it. 2) Stop developing yum.
#
#  Upstream says that #2 will no longer be true after this release.
Conflicts: zif <= 0.1.3-3.fc15

Obsoletes: yum-skip-broken <= 1.1.18
Provides: yum-skip-broken = 1.1.18.yum
Obsoletes: yum-basearchonly <= 1.1.9
Obsoletes: yum-plugin-basearchonly <= 1.1.9
Provides: yum-basearchonly = 1.1.9.yum
Provides: yum-plugin-basearchonly = 1.1.9.yum
Obsoletes: yum-allow-downgrade < 1.1.20-0
Obsoletes: yum-plugin-allow-downgrade < 1.1.22-0
Provides: yum-allow-downgrade = 1.1.20-0.yum
Provides: yum-plugin-allow-downgrade = 1.1.22-0.yum
Obsoletes: yum-plugin-protect-packages < 1.1.27-0
Provides: yum-protect-packages = 1.1.27-0.yum
Provides: yum-plugin-protect-packages = 1.1.27-0.yum
Obsoletes: yum-plugin-download-order <= 0.2-2
Obsoletes: yum-plugin-downloadonly <= 1.1.31-7.fc18
Provides: yum-plugin-downloadonly = 3.4.3-44.yum
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Yum is a utility that can check for and automatically download and
install updated RPM packages. Dependencies are obtained and downloaded 
automatically, prompting the user for permission as necessary.

%package updatesd
Summary: Update notification daemon
Group: Applications/System
Requires: yum = %{version}-%{release}
Requires: dbus-python
Requires: pygobject2
Requires(preun): /sbin/chkconfig
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(post): /sbin/service
Requires(postun): /sbin/chkconfig
Requires(postun): /sbin/service


%description updatesd
yum-updatesd provides a daemon which checks for available updates and 
can notify you when they are available via email, syslog or dbus. 

%package cron
Summary: Files needed to run yum updates as a cron job
Group: System Environment/Base
Requires: yum >= 3.0 cronie crontabs findutils
%if %{yum_cron_systemd}
BuildRequires: systemd-units
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%else
Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service
%endif

%description cron
These are the files needed to run yum updates as a cron job.
Install this package if you want auto yum updates nightly via cron.


%prep
%setup -q
%patch4 -p0
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch1 -p1

%build
make

%if !%{disable_check}
%check
make check
%endif


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%if %{yum_cron_systemd}
INIT=systemd
%else
INIT=sysv
%endif

make DESTDIR=$RPM_BUILD_ROOT UNITDIR=%{_unitdir} INIT=$INIT install

install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/yum.conf
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum/pluginconf.d $RPM_BUILD_ROOT/%{yum_pluginslib}
mkdir -p $RPM_BUILD_ROOT/%{yum_pluginsshare}

%if %{move_yum_conf_back}
# for now, move repodir/yum.conf back
mv $RPM_BUILD_ROOT/%{_sysconfdir}/yum/repos.d $RPM_BUILD_ROOT/%{_sysconfdir}/yum.repos.d
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/yum/yum.conf
%endif

%if %{yum_updatesd}
echo Keeping local yum-updatesd
%else

# yum-updatesd has moved to the separate source version
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/yum/yum-updatesd.conf 
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/yum-updatesd
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/dbus-1/system.d/yum-updatesd.conf
rm -f $RPM_BUILD_ROOT/%{_sbindir}/yum-updatesd
rm -f $RPM_BUILD_ROOT/%{_mandir}/man*/yum-updatesd*
rm -f $RPM_BUILD_ROOT/%{_datadir}/yum-cli/yumupd.py*

%endif

# Ghost files:
mkdir -p $RPM_BUILD_ROOT/var/lib/yum/history
mkdir -p $RPM_BUILD_ROOT/var/lib/yum/plugins
mkdir -p $RPM_BUILD_ROOT/var/lib/yum/yumdb
touch $RPM_BUILD_ROOT/var/lib/yum/uuid

# rpmlint bogus stuff...
chmod +x $RPM_BUILD_ROOT/%{_datadir}/yum-cli/*.py
chmod +x $RPM_BUILD_ROOT/%{python_sitelib}/yum/*.py
chmod +x $RPM_BUILD_ROOT/%{python_sitelib}/rpmUtils/*.py

%find_lang %name

%if %{yum_cron_systemd}
# Remove the yum-cron sysV stuff to make rpmbuild happy..
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/yum-cron
%else
# Remove the yum-cron systemd stuff to make rpmbuild happy..
rm -f $RPM_BUILD_ROOT/%{_unitdir}/yum-cron.service
%endif

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%if %{yum_updatesd}
%post updatesd
/sbin/chkconfig --add yum-updatesd
/sbin/service yum-updatesd condrestart >/dev/null 2>&1
exit 0

%preun updatesd
if [ $1 = 0 ]; then
 /sbin/chkconfig --del yum-updatesd
 /sbin/service yum-updatesd stop >/dev/null 2>&1
fi
exit 0
%endif

%post cron

%if %{yum_cron_systemd}
#systemd_post yum-cron.service
#  Do this manually because it's a fake service for a cronjob, and cronjobs
# are default on atm. This may change in the future.
if [ $1 = 1 ]; then
 systemctl enable yum-cron >/dev/null 2>&1
else
#  Note that systemctl preset is being run here ... but _only_ on initial
# install. So try this...

if [ -f /var/lock/subsys/yum-cron -a -f /etc/rc.d/init.d/yum-cron ]; then
 systemctl enable yum-cron >/dev/null 2>&1
fi
fi

# Also note:
#  systemctl list-unit-files | fgrep yum-cron
%else
# SYSV init post cron
# Make sure chkconfig knows about the service
/sbin/chkconfig --add yum-cron
# if an upgrade:
if [ "$1" -ge "1" ]; then
# if there's a /etc/rc.d/init.d/yum file left, assume that there was an
# older instance of yum-cron which used this naming convention.  Clean 
# it up, do a conditional restart
 if [ -f /etc/init.d/yum ]; then 
# was it on?
  /sbin/chkconfig yum
  RETVAL=$?
  if [ $RETVAL = 0 ]; then
# if it was, stop it, then turn on new yum-cron
   /sbin/service yum stop 1> /dev/null 2>&1
   /sbin/service yum-cron start 1> /dev/null 2>&1
   /sbin/chkconfig yum-cron on
  fi
# remove it from the service list
  /sbin/chkconfig --del yum
 fi
fi 
exit 0
%endif

%preun cron
%if %{yum_cron_systemd}
%systemd_preun yum-cron.service
%else
# SYSV init preun cron
# if this will be a complete removeal of yum-cron rather than an upgrade,
# remove the service from chkconfig control
if [ $1 = 0 ]; then
 /sbin/chkconfig --del yum-cron
 /sbin/service yum-cron stop 1> /dev/null 2>&1
fi
exit 0
%endif

%postun cron
%if %{yum_cron_systemd}
%systemd_postun_with_restart yum-cron.service
%else
# SYSV init postun cron

# If there's a yum-cron package left after uninstalling one, do a
# conditional restart of the service
if [ "$1" -ge "1" ]; then
 /sbin/service yum-cron condrestart 1> /dev/null 2>&1
fi
exit 0
%endif


%files -f %{name}.lang
%defattr(-, root, root, -)
%doc README AUTHORS COPYING TODO INSTALL ChangeLog PLUGINS
%if %{move_yum_conf_back}
%config(noreplace) %{_sysconfdir}/yum.conf
%dir %{_sysconfdir}/yum.repos.d
%else
%config(noreplace) %{_sysconfdir}/yum/yum.conf
%dir %{_sysconfdir}/yum/repos.d
%endif
%config(noreplace) %{_sysconfdir}/yum/version-groups.conf
%dir %{_sysconfdir}/yum
%dir %{_sysconfdir}/yum/protected.d
%dir %{_sysconfdir}/yum/vars
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/bash_completion.d
%dir %{_datadir}/yum-cli
%{_datadir}/yum-cli/*
%exclude %{_datadir}/yum-cli/completion-helper.py?
%if %{yum_updatesd}
%exclude %{_datadir}/yum-cli/yumupd.py*
%endif
%{_bindir}/yum
%{python_sitelib}/yum
%{python_sitelib}/rpmUtils
%dir /var/cache/yum
%dir /var/lib/yum
%ghost /var/lib/yum/uuid
%ghost /var/lib/yum/history
%ghost /var/lib/yum/plugins
%ghost /var/lib/yum/yumdb
%{_mandir}/man*/yum.*
%{_mandir}/man*/yum-shell*
# plugin stuff
%dir %{_sysconfdir}/yum/pluginconf.d 
%dir %{yum_pluginslib}
%dir %{yum_pluginsshare}

%files cron
%defattr(-,root,root)
%doc COPYING
%{_sysconfdir}/cron.daily/0yum-update.cron
%config(noreplace) %{_sysconfdir}/yum/yum-cron.conf
%if %{yum_cron_systemd}
%{_unitdir}/yum-cron.service
%else
%{_sysconfdir}/rc.d/init.d/yum-cron
%endif
%{_sbindir}/yum-cron
%{_mandir}/man*/yum-cron.*

%if %{yum_updatesd}
%files updatesd
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/yum-updatesd.conf
%config %{_sysconfdir}/rc.d/init.d/yum-updatesd
%config %{_sysconfdir}/dbus-1/system.d/yum-updatesd.conf
%{_datadir}/yum-cli/yumupd.py*
%{_sbindir}/yum-updatesd
%{_mandir}/man*/yum-updatesd*
%endif

%changelog
* Fri Feb 22 2013 Zdeněk Pavlas <zpavlas@redhat.com> - 3.4.3-64
- use multiple applydeltarpm workers (4 by default)

* Thu Feb 21 2013 Zdeněk Pavlas <zpavlas@redhat.com> - 3.4.3-63
- Added native drpm support.

* Tue Feb 18 2013 James Antill <james at fedoraproject.org> - 3.4.3-62
- update to latest HEAD.
- Add cache-reqs.
- Fixup specfile for Fedora <= 18 usage.

* Mon Feb 18 2013 James Antill <james at fedoraproject.org> - 3.4.3-60
- update to latest HEAD.
- Auto expire caches on repo errors.
- Use xattrs for cache checksum speedup.

* Fri Feb 15 2013 James Antill <james at fedoraproject.org> - 3.4.3-59
- update to latest HEAD.
- Add load-ts helper.
- Update downloadonly plugin version obs.

* Fri Feb  8 2013 James Antill <james at fedoraproject.org> - 3.4.3-58
- update to latest HEAD.
- Add pyxattr require for origin_urls for everyone.
- Fix yum-cron service file and scriptlets.
- Fix instant broken mirrors problem.

* Thu Jan 31 2013 James Antill <james at fedoraproject.org> - 3.4.3-57
- update to latest HEAD.
- Fix autoremove foo.
- Speedup/fix repo-pkgs <foo> update with obsoletes.

* Wed Jan 30 2013 James Antill <james at fedoraproject.org> - 3.4.3-56
- update to latest HEAD.
- Add yumvar dumping into yumdb.
- Add ui_repoid_vars configuration.
- Update translations.

* Tue Jan 22 2013 James Antill <james at fedoraproject.org> - 3.4.3-55
- update to latest HEAD.
- Add repo-pkgs update/list and tweak remove-or-sync.

* Mon Jan 21 2013 James Antill <james at fedoraproject.org> - 3.4.3-54
- update to latest HEAD.
- Add repo-pkgs docs. add erase/etc. aliases.
- Fix for 895854.

* Wed Jan 16 2013 James Antill <james at fedoraproject.org> - 3.4.3-53
- update to latest HEAD.
- Add repo-pkgs.
- Add swap.
- Add remove_leaf_only and repopkgremove_leaf_only.
- Add metadata_expire_filter.

* Tue Jan 15 2013 Zdeněk Pavlas <zpavlas@redhat.com> - 3.4.3-52
- update to latest HEAD
- _lock(): yet another exception2msg fix.  BZ 895060
- use yum-cron.service.  BZ 893593
- YumRepo.populate(): always decompresses new database

* Wed Jan  9 2013 Zdeněk Pavlas <zpavlas@redhat.com> - 3.4.3-51
- update to latest HEAD
- Include langpacks when reading and writing comps. BZ 879030
- selectGroup(): Fix a typo. BZ 885139
- move the basename checking into _repos.doSetup(). BZ 885159
- bash completion: offer nvra for multi-install packages
- fixes extra '</pkglist>' tags on multi-collection errata. BZ 887407
- Include the update date in updateinfo xml. BZ 887935
- Complete provides/whatprovides with filenames. BZ 891561
- New locking code.  BZ 865601

* Thu Dec 06 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.4.3-50
- update to latest HEAD.
- Check for possible inf. recursion and workaround in skip-broken. BZ 874065
- Don't error in history list, when we have no history. BZ 802462
- Avoid converting to unicode and back in dump_xml_*.  BZ 716235
- po.xml_dump_{primary,filelists,other}_metadata() cleanup

* Wed Nov 28 2012 Zdenek Pavlas  <zpavlas@redhat.com> - 3.4.3-49
- update to latest HEAD.
- Fix ugly paths in po.xml_dump_*(). BZ 835565.
- Fix yum-cron requires.

* Mon Nov 19 2012 Zdenek Pavlas  <zpavlas@redhat.com> - 3.4.3-48
- update to latest HEAD.
- add skip-broken option to yum-cron.
- get rid of bogus "Downloaded package .. but it was invalid."
- clean up misc.to_xml(), make it faster.  BZ 716235.
- checksum not available implies checksum does not match.  BZ 825272.
- avoid checksumming existing .sqlite.bz2 files.
- fix circular obsoletes in transaction members check. BZ 868840.

* Thu Oct 25 2012 Zdenek Pavlas  <zpavlas@redhat.com> - 3.4.3-47
- replaced yum-cron.sh with the new yum-cron.py (very alpha)

* Thu Oct 25 2012 Nils Philippsen <nils@redhat.com> - 3.4.3-46
- bump release to ensure upgrade path and satisfy PackageKit deps

* Wed Oct 17 2012 James Antill <james at fedoraproject.org> - 3.4.3-44
- update to latest HEAD.
- Add downloadonly into core, and enable background downloads.
- Lots of minor fixes.

* Fri Sep  7 2012 James Antill <james at fedoraproject.org> - 3.4.3-43
- update to latest HEAD.
- Use .ui_id explicitly for backcompat. on strings, *sigh*.

* Sat Sep  1 2012 James Antill <james at fedoraproject.org> - 3.4.3-42
- update to latest HEAD.
- Fix missing self. on last patch.

* Fri Aug 31 2012 James Antill <james at fedoraproject.org> - 3.4.3-41
- update to latest HEAD.
- Don't statvfs when we aren't going to copy, and using relative.

* Thu Aug 30 2012 James Antill <james at fedoraproject.org> - 3.4.3-40
- update to latest HEAD.
- Fix rel-eng problems when repo.repofile is None.
- Don't statvfs when we aren't going to copy.

* Tue Aug 28 2012 James Antill <james at fedoraproject.org> - 3.4.3-36
- update to latest HEAD.
- Fix environment groups write.
- Allow merging of updateinfo.
- Add releasever/arch to repoids on output, if used in urls.
- Merge mirror errors fix.

* Thu Aug 23 2012 Zdenek Pavlas <zpavlas at redhat.com> - 3.4.3-34
- Some users skip setupProgressCallbacks(). BZ 850913.

* Wed Aug 22 2012 Zdenek Pavlas <zpavlas at redhat.com> - 3.4.3-33
- update to latest HEAD.
- Set multi_progress_obj option
- Show full URLs and mirror errors when _getFile() fails.

* Thu Aug 16 2012 James Antill <james at fedoraproject.org> - 3.4.3-32
- update to latest HEAD.
- Some fixes for new environment groups.
- Fix "yum upgrade" download verification. BZ 848811.

* Fri Aug 10 2012 James Antill <james at fedoraproject.org> - 3.4.3-31
- update to latest HEAD.
- Big update, mostly for "environment groups".

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.3-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Zdenek Pavlas <zpavlas at redhat.com> - 3.4.3-29
- update to latest HEAD.
- quote uids to keep cachedir ascii-clean.  BZ 832195
- show_lock_owner: report errors if we fail.  BZ 745281

* Thu Jun 14 2012 Zdenek Pavlas <zpavlas at redhat.com> - 3.4.3-28
- update to latest HEAD.
- No async downloading when --cacheonly.  BZ 830523
- misc.decompress(): compare mtime without sub second precision. BZ 831918
- preload_from_sys to user dir with --cacheonly, BZ 830523

* Fri Jun  8 2012 James Antill <james at fedoraproject.org> - 3.4.3-27
- update to latest HEAD.
- Fix for ppc64p7 detection.

* Wed May 16 2012 Zdenek Pavlas <zpavlas at redhat.com> - 3.4.3-26
- update to latest master HEAD
- Fix using available packages as installed, due to strong_requires.
- Remove tracebacks on MD downloads. BZ 822009.

* Mon May 14 2012 Zdenek Pavlas <zpavlas at redhat.com> - 3.4.3-25
- update to latest HEAD.
- merged multi-downloader code
- rebased yum-ppc64-preferred.patch
- dropped arm-arch-detection.patch (moved to HEAD)
- renamed yum-update.cron to 0yum-update.cron

* Fri Apr 27 2012 James Antill <james at fedoraproject.org> - 3.4.3-24
- Add code for arm detection.

* Fri Mar 16 2012 James Antill <james at fedoraproject.org> - 3.4.3-23
- update to latest HEAD.
- Also fix "yum check" for strong requires. bug 795907.
- Fix for "Only update available" on downgrade. bug 803346.

* Fri Mar  9 2012 James Antill <james at fedoraproject.org> - 3.4.3-22
- update to latest HEAD.
- Fail on bad reinstall/downgrade arguments. bug 800285.
- Fix weird multiple obsoletion bug. BZ 800016
- Check for a compat. arch. as well, when hand testing for upgradability.
- Allow changing the exit code on non-fatal errors.

* Thu Mar  1 2012 James Antill <james at fedoraproject.org> - 3.4.3-21
- update to latest HEAD.
- Translation update.

* Wed Feb 29 2012 James Antill <james at fedoraproject.org> - 3.4.3-20
- update to latest HEAD.
- Lazy setup pkgSack, for localinstall/etc.
- add support for 64 bit arm hardware.
- Hack for "info install blah" to never look at repos.
- Fixup resolvedep command for mock users.

* Mon Feb 20 2012 James Antill <james at fedoraproject.org> - 3.4.3-19
- update to latest HEAD.
- Add a yum group convert command, so people can use groups as objects easily.
- Document the new group stuff.
- Generic provide markers for installonlypkgs (for kernel/vms).
- Minor updates/fixes merge some older branches.

* Fri Jan 20 2012 James Antill <james at fedoraproject.org> - 3.4.3-18
- update to latest HEAD
- Added group_command, but didn't change to groups as objects by default.
- Minor updates.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 James Antill <james at fedoraproject.org> - 3.4.3-16
- update to latest HEAD
- Have users always use their own dirs.
- Minor updates.

* Fri Dec  2 2011 James Antill <james at fedoraproject.org> - 3.4.3-15
- update to latest HEAD
- Init "found" variable for distro-sync full. BZ 752407.
- Fix _conv_pkg_state when calling with history as checksum. BZ 757736.
- When a repo. fails in repolist, manually populate the ones after it.A
- Fix a corner case in exception2msg(). BZ 749239.
- Transifex sync.
- Hand fix the plural forms gettext stuff.

* Wed Nov 30 2011 Dennis Gilmore <dennis@ausil.us> - 3.4.3-13
- add patch from upstream for arm hardware floating point support

* Mon Oct 17 2011 James Antill <james at fedoraproject.org> - 3.4.3-12
- update to latest HEAD
- Basically just an update for transifex sync.

* Fri Oct 14 2011 James Antill <james at fedoraproject.org> - 3.4.3-11
- update to latest HEAD
- Some edge case depsolver bug fixes.
- Output the GPG fingerprint when showing the GPG key.
- Update bugtracker URL back to redhat.
- Allow reinstall and remove arguments to history redo command.
- Let resolvedep look for installed packages.

* Wed Sep 21 2011 James Antill <james at fedoraproject.org> - 3.4.3-10
- update to latest HEAD
- Fix for history sync, and saving on install.
- Lots of minor bug fixes.
- Speedups for upgrade_requirements_on_install=true.
- Fix generated data using bad caches.
- Changes for yum-cron.

* Tue Aug 23 2011 James Antill <james at fedoraproject.org> - 3.4.3-9
- update to latest HEAD
- Update translations.
- Minor UI tweaks for transaction output.
- Minor tweak for update_reqs_on_install.

* Mon Aug 22 2011 James Antill <james at fedoraproject.org> - 3.4.3-8
- update to latest HEAD
- Fix upgrade_requirements_on_install breaking upgrade typos.

* Fri Aug 19 2011 James Antill <james at fedoraproject.org> - 3.4.3-7
- update to latest HEAD
- Fix syncing of yum DB data in history.
- Add upgrade_requirements_on_install config. option.
- Don't look for releasever if it's set directly (anaconda).
- Expose ip_resolve urlgrabber option.

* Fri Aug  5 2011 James Antill <james at fedoraproject.org> - 3.4.3-6
- update to latest HEAD
- Add new yum DB data.
- Add hack to workaround broken python readline in yum shell.
- Make "yum -q history addon-info last saved_tx" valid input for load-ts.
- Add "history packages-info/stats/sync" sub-commnands.

* Fri Jul 29 2011 James Antill <james at fedoraproject.org> - 3.4.3-5
- update to latest HEAD
- Lots of really minor changes. Docs. and yum-cron mainly.
- Output yum_saved_tx file.

* Fri Jul 15 2011 James Antill <james at fedoraproject.org> - 3.4.3-4
- update to latest HEAD
- Weird old bugs fixed for new createrepo code.
- Add --assumeno and an easter egg! Also allow remove to use alwaysprompt.
- Fix \r appearing on serial console etc. BZ 720088.
- Fix umask on mkdir() as well as open. BZ 719467.
- Fix traceback when enabling/disabling repos. in GUI.

* Thu Jun 30 2011 James Antill <james at fedoraproject.org> - 3.4.3-3
- Fix the skip broken tuples => dict. bug. BZ 717973.

* Wed Jun 29 2011 James Antill <james at fedoraproject.org> - 3.4.3-2
- Add ppc64 arch. change for BZ 713791.

* Tue Jun 28 2011 James Antill <james at fedoraproject.org> - 3.4.3-1
- update to 3.4.3
- Real upstream workaround for rpm chroot and history insanity.
- Minor bugfixes.

* Wed Jun 22 2011 James Antill <james at fedoraproject.org> - 3.4.2-2
- Workaround rpm chroot insanity.

* Wed Jun 22 2011 James Antill <james at fedoraproject.org> - 3.4.2-1
- update to 3.4.2
- Lots of smallish bug fixes/tweaks.
- Lookup erase transaction members, by their name, if we can.
- Added pluralized translation messages.

* Tue Jun 14 2011 James Antill <james at fedoraproject.org> - 3.4.1-5
- update to latest HEAD
- Lots of smallish bug fixes.
- New groups command.

* Thu Jun  2 2011 James Antill <james at fedoraproject.org> - 3.4.1-4
- update to latest HEAD
- Fix RepoStorage problem for pulp.
- Add list of not found packages.
- Minor bug fixes.

* Tue May 24 2011 James Antill <james at fedoraproject.org> - 3.4.1-3
- update to latest HEAD
- Tweak "yum provides"
- Don't access the repos. for saved_tx, if doing a removal.
- Fix a couple of old minor bugs:
- Remove usage of INFO_* from yumcommands, as -q supresses that. BZ 689241.
- Don't show depsolve failure messages for non-depsolving problems. BZ 597336.

* Wed May  4 2011 James Antill <james at fedoraproject.org> - 3.4.1-2
- update to latest HEAD
- Fix consolidate_libc.
- Update translations.
- Add history rollback.

* Wed Apr 20 2011 James Antill <james at fedoraproject.org> - 3.4.1-1
- Fix umask override.
- Remove double baseurl display, BZ 697885.

* Fri Apr 15 2011 James Antill <james at fedoraproject.org> - 3.4.0-1
- update to 3.4.0.

* Fri Apr  8 2011 James Antill <james at fedoraproject.org> - 3.2.29-10
- update to latest HEAD 
- Likely last HEAD before 3.2.30.

* Fri Mar 25 2011 Seth Vidal <skvidal at fedoraproject.org> - 3.2.29-9
- update to latest HEAD 

* Mon Feb 28 2011 Seth Vidal <skvidal at fedoraproject.org> - 3.2.29-8
- take out the hack-patch from 2 weeks ago.

* Mon Feb 28 2011 Seth Vidal <skvidal at fedoraproject.org> - 3.2.29-7
- latest head including all of Panu's rpmutils/callback patches

* Thu Feb 17 2011 Seth Vidal <skvidal at fedoraproject.org> - 3.2.29-6
- add rpmutils-recursive-import.patch to work around recursive import problems

* Wed Feb 16 2011 Seth Vidal <skvidal at fedoraproject.org> - 3.2.29-5
- lots of hopefully NOT exciting changes to rpmutils/rpmsack from head.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Seth Vidal <skvidal at fedoraproject.org> - 3.2.29-3
- latest from head - fixing a number of minor bugs

* Thu Jan 13 2011 Seth Vidal <skvidal at fedoraproject.org> - 3.2.29-2
- grumble broken skip-broken test :(


* Thu Jan 13 2011 Seth Vidal <skvidal at fedoraproject.org> - 3.2.29-1
- 3.2.29
- add yum-cron subpkg

* Thu Jan  6 2011 James Antill <james at fedoraproject.org> - 3.2.28-17
- Allow kernel installs with multilib protection ... oops!
- Don't conflict with fixed versions of Zif.
- Add locks for non-root.

* Tue Jan  4 2011 Seth Vidal <skvidal at fedoraproject.org> - 3.2.28-16
- fix skip-broken conflict - thanks dgilmore for the catch

* Tue Jan  4 2011 Seth Vidal <skvidal at fedoraproject.org> - 3.2.28-15
- latest head
- conflicts zif

* Thu Nov 11 2010 James Antill <james at fedoraproject.org> - 3.2.28-14
- latest head
- Perf. fixes/improvements.

* Tue Nov  9 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.28-13
- once again with head

* Fri Nov  5 2010 James Antill <james at fedoraproject.org> - 3.2.28-12
- latest head
- Add load-ts command.
- Fix verifying symlinks.

* Wed Oct 20 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.28-11
- latest head
- depsolve enhancements on update/obsoletes
- show recent pkgs in history package-list instead of a specific pkg
- bz: 644432, 644265
- make sure urlgrabber is using the right config settings for fetching gpg keys


* Fri Oct 15 2010 James Antill <james at fedoraproject.org> - 3.2.28-10
- latest head 
- Fix major breakage from the "list updates" speedup :).
- Close curl/urlgrabber after downloading packages.
- Allow remove+update in "yum shell".
- Fix output of distro tags.

* Thu Oct  7 2010 James Antill <james at fedoraproject.org> - 3.2.28-9
- latest head 
- Add localpkg_gpgcheck option.
- Speedup "list updates"
- Doc fixes.

* Sat Sep 25 2010 James Antill <james at fedoraproject.org> - 3.2.28-8
- latest head 
- Speedup install/remove/etc a lot.
- Add merged history.
- Fix unique comps/pkgtags leftovers.

* Tue Sep 14 2010 James Antill <james at fedoraproject.org> - 3.2.28-7
- latest head 
- Fix PK/auto-close GPG import bug.
- Fix patch for installonly_limit and enable it again.
- Fix rpmlint warnings.
- Remove color=never config.

* Fri Sep 10 2010 Seth Vidal <skvidal at fedoraproject.org>
- latest head 

* Fri Aug 27 2010 Seth Vidal <skvidal at fedoraproject.org>
- obsoleted yum-plugin-download-order

* Thu Aug 12 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.28-3
- latest head
- fix gpg key import
- more unicode fixes
- output slightly more clear depsovling error msgs

* Mon Aug  9 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.28-2
- latest head
- unicide fixes
- sqlite history db conversion fixes


* Fri Jul 30 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.28-1
- 3.2.28


* Wed Jul 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3.2.27-21
- Again rebuild against python 2.7

* Mon Jul 26 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.27-20
- latest head
- minor fixes and doc updates
- hardlink yumdb files to conserve spacde
- cache yumdb results

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.2.27-19
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 16 2010 James Antill <james@fedoraproject.org> - 3.2.27-18
- Latest head.
- Add history addon-info.
- Add new callbacks, verify and compare_providers.
- Fix rpm transaction fail API break, probably only for anaconda.
- Bug fixes.

* Fri Jun 25 2010 James Antill <james@fedoraproject.org> - 3.2.27-17
- Latest head.
- Allow reinstalls of kernel, etc.
- Tweaks to some user output.
- Allow Fedora GPG keys to be removed.
- Add history extra data API, and history plugin hooks.
- Bunch of minor bug fixes.

* Tue Jun 15 2010 James Antill <james@fedoraproject.org> - 3.2.27-16
- Latest head.
- Fix install being recorded as reinstall.
- Make localinstall not install obsoleted only by installed.
- Fix info -v, on available packages.
- Fix man page stuff.
- Deal with unicide on rpmdb problems.
- Allow ipkg.repo.name to work.
- Add ville's epoch None vs. 0 code, in compareEVR.

* Fri Jun 11 2010 James Antill <james@fedoraproject.org> - 3.2.27-15
- Latest head.
- Add filtering requires code for createrepo.
- Add installed_by/changed_by yumdb values.
- Tweak output for install/reinstall/downgrade callbacks.
- Add plugin hooks for pre/post verifytrans.
- Deal with local pkgs. which only obsolete.
- No chain removals on downgrade.
- Bunch of speedups for "list installed blah", and "remove blah".

* Wed Jun  2 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.27-14
- merge in latest yum head:
- change decompressors to support lzma, if python module is available
- finnish translation fixes
- pyint vs pylong fix for formatRequire() so we stop spitting back the wrong requires strings to mock on newish rpm
- add exit_on_lock option
- Deal with RHEL-5 loginuid damage
- Fix pkgs. that are excluded after being put in yb.up ... BZ#597853
- Opt. for rpmdb.returnPackages(patterns=...). Drops about 30%% from remove time.
- Fix "remove name-version", really minor API bug before last patch

* Wed May 26 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.27-13
- minor cleanups for yum-utils with --setopt
- translation updates

* Thu May 13 2010 James Antill <james@fedoraproject.org> - 3.2.27-12
- Latest head.
- History db version 2
- Some bug fixes
- More paranoid/leanient with rpmdb cache problems.

* Wed May  5 2010 James Antill <james@fedoraproject.org> - 3.2.27-11
- Fix from head for mock, mtime=>ctime due to caches and fixed installroot
- Fix for typo in new problems code, bug 589008

* Mon May  3 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.27-10
- latest head
- fixes yum chroot path duplication
- yum.log perms

* Thu Apr 29 2010 James Antill <james@fedoraproject.org> - 3.2.27-9
- Latest yum-3_2_X head.
- Added protect packages.
- Bug fixes from the yum bug day.
- Added removed size output.
- Added glob: to all list config. options.
- Fix fsvars.

* Thu Apr 22 2010 James Antill <james@fedoraproject.org> - 3.2.27-8
- Latest yum-3_2_X head.
- Add deselections.
- Add simple depsolve into compare_providers
- Speedup distro-sync blah.

* Fri Apr 16 2010 James Antill <james@fedoraproject.org> - 3.2.27-7
- Latest yum-3_2_X head.
- Add the "big update" speedup patch.
- Add nocontexts ts flag.
- Add provides and obsoleted to "yum check".
- Add new dump_xml stuff for createrepo/modifyrepo.
- Move /var/lib/yum/vars to /etc/yum/vars

* Mon Apr 12 2010 James Antill <james@fedoraproject.org> - 3.2.27-6
- Latest yum-3_2_X head.
- Fix the caching changes.

* Sat Apr 10 2010 James Antill <james@fedoraproject.org> - 3.2.27-5
- Latest yum-3_2_X head.
- Remove the broken assert in sqlitesack

* Thu Apr  8 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.27-4
- more latest headness

* Fri Mar 26 2010 James Antill <james@fedoraproject.org> - 3.2.27-3
- Latest yum-3_2_X head.

* Tue Mar 23 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.27-2
- broke searching in PK, this patch fixes it.

* Thu Mar 18 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.27-1
- 3.2.27 from upstream (more or less the same as 3.2.26-6 but with a new number

* Thu Mar 11 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.26-6
- should be the final HEAD update before 3.2.27

* Wed Feb 24 2010 James Antill <james@fedoraproject.org> - 3.2.26-5
- new HEAD, minor features and speed.

* Wed Feb 17 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.26-4
- new HEAD to fix the fix to the fix

* Tue Feb 16 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.26-3
- latest head - including fixes to searchPrcos

* Wed Feb 10 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.26-2
- grumble.

* Tue Feb  9 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.26-1
- final 3.2.26

* Mon Feb  8 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.25-14
- $uuid, pkgtags searching, latest HEAD patch - pre 3.2.26

* Thu Jan 28 2010 James Antill <james at fedoraproject.org> - 3.2.25-13
- A couple of bugfixes, most notably:
-  you can now install gpg keys again!
-  bad installed file requires don't get cached.

* Fri Jan 22 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.25-12
- someone forgot to push their changes

* Fri Jan 22 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.25-11
- more fixes, more fun

* Fri Jan 15 2010 James Antill <james at fedoraproject.org> - 3.2.25-10
- latest head
- Fixes for pungi, rpmdb caching and kernel-PAE-devel duplicates finding
- among others.

* Mon Jan  4 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.25-8
- latest head
