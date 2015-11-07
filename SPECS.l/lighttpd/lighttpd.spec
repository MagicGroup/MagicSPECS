%define webroot /var/www/lighttpd

%global _hardened_build 1

# We have an bunch of --with/--without options to pass, make it easy with bcond
%define confswitch() %{expand:%%{?with_%{1}:--with-%{1}}%%{!?with_%{1}:--without-%{1}}}

%bcond_without mysql
%bcond_without ldap
%bcond_without attr
%bcond_without openssl
%bcond_without kerberos5
%bcond_without pcre
%bcond_without fam
%bcond_without lua
# We can't have bcond names with hyphens
%bcond_with    webdavprops
%bcond_with    webdavlocks
%bcond_without gdbm
%bcond_with    memcache

# No poweredby.png image in EL5 and earlier (it's in Fedora and EL6+)
%if 0%{?el5}
%bcond_without systemlogos
%else
%bcond_without systemlogos
%endif

# The /var/run/lighttpd directory uses tmpfiles.d when mounted using tmpfs
%if 0%{?fedora} >= 15
%bcond_without tmpfiles
%else
%bcond_with    tmpfiles
%endif

# Replace sysvinit script with systemd service file for RHEL7+
%if 0%{?fedora} || 0%{?rhel} >= 7
%bcond_without systemd
%else
%bcond_with    systemd
%endif

Summary: Lightning fast webserver with light system requirements
Name: lighttpd
Version: 1.4.35
Release: 3%{?dist}
License: BSD
Group: System Environment/Daemons
URL: http://www.lighttpd.net/
Source0: http://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-%{version}.tar.bz2
Source1: lighttpd.logrotate
Source2: php.d-lighttpd.ini
Source3: lighttpd.init
Source4: lighttpd.service
Source10: index.html
Source11: http://www.lighttpd.net/favicon.ico
Source12: http://www.lighttpd.net/light_button.png
Source13: http://www.lighttpd.net/light_logo.png
Source14: lighttpd-empty.png
Source100: lighttpd-mod_geoip.c
Source101: lighttpd-mod_geoip.txt
Patch0: lighttpd-1.4.28-defaultconf.patch
Patch1: lighttpd-1.4.34-mod_geoip.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# For the target poweredby.png image (skip requirement + provide image on EL5)
%if %{with systemlogos}
Requires: system-logos >= 7.92.1
%endif
Requires(pre): /usr/sbin/useradd
%if %{with systemd}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
%else
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service, /sbin/chkconfig
Requires(postun): /sbin/service
%endif
Provides: webserver
BuildRequires: openssl-devel, pcre-devel, bzip2-devel, zlib-devel, autoconf, automake, libtool
BuildRequires: /usr/bin/awk
%{?with_ldap:BuildRequires: openldap-devel}
%{?with_fam:BuildRequires: gamin-devel}
%{?with_webdavprops:BuildRequires: libxml2-devel}
%{?with_webdavlocks:BuildRequires: sqlite-devel}
%{?with_gdbm:BuildRequires: gdbm-devel}
%{?with_memcache:BuildRequires: memcached-devel}
%{?with_lua:BuildRequires: compat-lua-devel}
# On EL5 we still need this because of the "broken" lua
%if 0%{?el5}
BuildRequires: readline-devel
%endif

%description
Secure, fast, compliant and very flexible web-server which has been optimized
for high-performance environments. It has a very low memory footprint compared
to other webservers and takes care of cpu-load. Its advanced feature-set
(FastCGI, CGI, Auth, Output-Compression, URL-Rewriting and many more) make
it the perfect webserver-software for every server that is suffering load
problems.


%package fastcgi
Summary: FastCGI module and spawning helper for lighttpd and PHP configuration
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
# Not really a requirement, but it used to be included (until 1.4.20-5)
Requires: spawn-fcgi

%description fastcgi
This package contains the spawn-fcgi helper for lighttpd's automatic spawning
of local FastCGI programs. Included is also a PHP .ini file to change a few
defaults needed for correct FastCGI behavior.


%package mod_geoip
Summary: GeoIP module for lighttpd to use for location lookups
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
BuildRequires: GeoIP-devel

%description mod_geoip
GeoIP module for lighttpd to use for location lookups.


%package mod_mysql_vhost
Summary: Virtual host module for lighttpd that uses a MySQL database
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
BuildRequires: mysql-devel

%description mod_mysql_vhost
Virtual host module for lighttpd that uses a MySQL database.


%prep
%setup -q
%patch0 -p1 -b .defaultconf
%patch1 -p1 -b .mod_geoip
install -p -m 0644 %{SOURCE100} src/mod_geoip.c
install -p -m 0644 %{SOURCE101} mod_geoip.txt


%build
autoreconf -if
%configure \
    --libdir='%{_libdir}/lighttpd' \
    %{confswitch mysql} \
    %{confswitch ldap} \
    %{confswitch attr} \
    %{confswitch openssl} \
    %{confswitch kerberos5} \
    %{confswitch pcre} \
    %{confswitch fam} \
    %{?with_webdavprops:--with-webdav-props} \
    %{?with_webdavlocks:--with-webdav-locks} \
    %{confswitch gdbm} \
    %{confswitch memcache} \
    %{confswitch lua}
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Install our own logrotate entry
install -D -p -m 0644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/logrotate.d/lighttpd

# Install our own php.d ini file
install -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/php.d/lighttpd.ini

# Install our own init script (included one is old style) or systemd service
%if %{with systemd}
install -D -p -m 0644 %{SOURCE4} \
    %{buildroot}%{_unitdir}/lighttpd.service
%else
install -D -p -m 0755 %{SOURCE3} \
    %{buildroot}%{_sysconfdir}/rc.d/init.d/lighttpd
%endif

# Install our own default web page and images
mkdir -p %{buildroot}%{webroot}
install -p -m 0644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} \
    %{buildroot}%{webroot}/

# Symlink for the powered-by-$DISTRO image (install empty image on EL5)
%if %{with systemlogos}
ln -s %{_datadir}/pixmaps/poweredby.png \
%else
install -p -m 0644 %{SOURCE14} \
%endif
    %{buildroot}%{webroot}/poweredby.png

# Example configuration to be included as %%doc
rm -rf config
cp -a doc/config config
find config -name 'Makefile*' | xargs rm -f
# Remove +x from scripts to be included as %%doc to avoid auto requirement
chmod -x doc/scripts/*.sh

# Install (*patched above*) sample config files
mkdir -p %{buildroot}%{_sysconfdir}/lighttpd
cp -a config/*.conf config/*.d %{buildroot}%{_sysconfdir}/lighttpd/

# Install empty log directory to include
mkdir -p %{buildroot}%{_var}/log/lighttpd

# Install empty run directory to include (for the example fastcgi socket)
mkdir -p %{buildroot}%{_var}/run/lighttpd
%if %{with tmpfiles}
# Setup tmpfiles.d config for the above
mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
echo 'D /var/run/lighttpd 0750 lighttpd lighttpd -' > \
    %{buildroot}%{_sysconfdir}/tmpfiles.d/lighttpd.conf
%endif


%clean
rm -rf %{buildroot}


%pre
/usr/sbin/useradd -s /sbin/nologin -M -r -d %{webroot} \
    -c 'lighttpd web server' lighttpd &>/dev/null || :

%post
%if %{with systemd}
%systemd_post lighttpd.service
%else
/sbin/chkconfig --add lighttpd
%endif

%preun
%if %{with systemd}
%systemd_preun lighttpd.service
%else
if [ $1 -eq 0 ]; then
    /sbin/service lighttpd stop &>/dev/null || :
    /sbin/chkconfig --del lighttpd
fi
%endif

%postun
%if %{with systemd}
%systemd_postun_with_restart lighttpd.service
%else
if [ $1 -ge 1 ]; then
    /sbin/service lighttpd condrestart &>/dev/null || :
fi
%endif


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%doc config/ doc/scripts/rrdtool-graph.sh
%dir %{_sysconfdir}/lighttpd/
%dir %{_sysconfdir}/lighttpd/conf.d/
%dir %{_sysconfdir}/lighttpd/vhosts.d/
%config(noreplace) %{_sysconfdir}/lighttpd/*.conf
%config(noreplace) %{_sysconfdir}/lighttpd/conf.d/*.conf
%config %{_sysconfdir}/lighttpd/conf.d/mod.template
%config %{_sysconfdir}/lighttpd/vhosts.d/vhosts.template
%config(noreplace) %{_sysconfdir}/logrotate.d/lighttpd
%if %{with systemd}
%{_unitdir}/lighttpd.service
%else
%{_sysconfdir}/rc.d/init.d/lighttpd
%endif
%if %{with tmpfiles}
%config(noreplace) %{_sysconfdir}/tmpfiles.d/lighttpd.conf
%endif
%{_sbindir}/lighttpd
%{_sbindir}/lighttpd-angel
%{_libdir}/lighttpd/
%exclude %{_libdir}/lighttpd/*.la
%exclude %{_libdir}/lighttpd/mod_fastcgi.so
%exclude %{_libdir}/lighttpd/mod_geoip.so
%exclude %{_libdir}/lighttpd/mod_mysql_vhost.so
%{_mandir}/man8/lighttpd.8*
%attr(0750, lighttpd, lighttpd) %{_var}/log/lighttpd/
%if %{with tmpfiles}
%ghost %attr(0750, lighttpd, lighttpd) %{_var}/run/lighttpd/
%else
%attr(0750, lighttpd, lighttpd) %{_var}/run/lighttpd/
%endif
%dir %{webroot}/
%{webroot}/*.ico
%{webroot}/*.png
# This is not really configuration, but prevent loss of local changes
%config %{webroot}/index.html

%files fastcgi
%defattr(-,root,root,-)
%doc doc/outdated/fastcgi*.txt doc/scripts/spawn-php.sh
%config(noreplace) %{_sysconfdir}/php.d/lighttpd.ini
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_fastcgi.so

%files mod_geoip
%defattr(-,root,root,-)
%doc mod_geoip.txt
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_geoip.so

%files mod_mysql_vhost
%defattr(-,root,root,-)
%doc doc/outdated/mysqlvhost.txt
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_mysql_vhost.so


%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.4.35-3
- 更新到 1.4.37

* Sun Jun 08 2014 Liu Di <liudidi@gmail.com> - 1.4.35-2
- 为 Magic 3.0 重建

* Wed Mar 12 2014 Jon Ciesla <limburgher@gmail.com> - 1.4.35-1
- 1.4.35, SA-2014-01.

* Fri Feb 21 2014 Jon Ciesla <limburgher@gmail.com> - 1.4.34-4
- Enable lua, BZ 912546.

* Mon Feb 10 2014 Jon Ciesla <limburgher@gmail.com> - 1.4.34-3
- Enable PIE, BZ 955145.

* Mon Feb 10 2014 Jon Ciesla <limburgher@gmail.com> - 1.4.34-2
- Apply Ken Dreyer's spec patches from BZ 850188.

* Wed Feb 05 2014 Jon Ciesla <limburgher@gmail.com> - 1.4.34-1
- 1.4.34, multiple security fixes.

* Mon Aug 26 2013 Jon Ciesla <limburgher@gmail.com> - 1.4.32-1
- Update to 1.4.32, BZ 878915.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun  6 2012 Matthias Saou <matthias@saou.eu> 1.4.31-1
- Update to 1.4.31 (#828198).

* Tue Apr 17 2012 Jon Ciesla <limburgher@gmail.com> - 1.4.30-2
- service file patch per BZ 720210.

* Mon Mar 26 2012 Matthias Saou <matthias@saou.eu> 1.4.30-1
- Update to 1.4.30 (#768903).
- Update mod_geoip patch.
- Remove upstreamed ssl_no_ecdh patch.

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1.4.29-3
- Rebuild against PCRE 8.30

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Aug 21 2011 Matthias Saou <matthias@saou.eu> 1.4.29-1
- Re-update to 1.4.29, including ssl_no_ecdh to fix build (#625737).

* Mon Jul 11 2011 Matthias Saou <matthias@saou.eu> 1.4.28-3
- Update the defaultconf patch to hint at selinux change to fix server.max-fds.
- Start using %%bcond, including quick defines to also support EL4.
- Include systemd service for F16+, don't add all of the ugly trigger for sysv
  migration (yet : new versions might be released before F16 final) (#720210).

* Sat Jul  9 2011 Matthias Saou <matthias@saou.eu> 1.4.28-2
- Rebase F15 master to the 1.4.28 update.
- Try to update to 1.4.29 (#625737).
- Rebase geoip patch for 1.4.29.
- Update /var/run to work with F15+ (#656612).
- Include all of the new example configuration, with conf.d files and vhosts.d.
- Disable server.max-fds by default since SELinux denies it.

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 1.4.26-4
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  8 2010 Matthias Saou <matthias@saou.eu> 1.4.28-1
- Update to 1.4.28.
- Update defaultconf patch.
- Remove upstreamed ssl-2157 patch.

* Fri Apr 16 2010 Matthias Saou <matthias@saou.eu> 1.4.26-2
- Update to 1.4.26.
- Update the geoip patch.
- Remove no longer provided ChangeLog from %%doc.
- Include patch to fix upstream SSL related bug #2157.

* Thu Sep  3 2009 Matthias Saou <matthias@saou.eu> 1.4.23-1
- Update to 1.4.23.
- Update defaultconf and mod_geoip patches.
- Remove no longer shipped spawn-fcgi, it's a separate source package now.
- Remove unused patch to the init script.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.22-5
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Matthias Saou <matthias@saou.eu> 1.4.22-3
- Update init script to new style.
- No longer include a sysconfig file, though one can be set to override the
  default configuration file location.

* Mon Mar 30 2009 Matthias Saou <matthias@saou.eu> 1.4.22-2
- Update to 1.4.22.
- Add missing defattr for the spawn-fcgi package.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Saou <matthias@saou.eu> 1.4.21-1
- Update to 1.4.21.

* Sat Jan 24 2009 Caolán McNamara <caolanm@redhat.com> 1.4.20-7
- rebuild for dependencies

* Wed Dec 24 2008 Matthias Saou <matthias@saou.eu> 1.4.20-6
- Partially revert last change by creating a "spawn-fastcgi" symlink, so that
  nothing breaks currently (especially for EL).
- Install empty poweredby image on RHEL since the symlink's target is missing.
- Split spawn-fcgi off in its own sub-package, have fastcgi package require it
  to provide backwards compatibility.

* Mon Dec 22 2008 Matthias Saou <matthias@saou.eu> 1.4.20-3
- Rename spawn-fastcgi to lighttpd-spawn-fastcgi to avoid clash with other
  packages providing it for their own needs (#472749). It's not used as-is
  by lighttpd, so it shouldn't be a problem... at worst, some custom scripts
  will need to be updated.

* Mon Dec 22 2008 Matthias Saou <matthias@saou.eu> 1.4.20-2
- Include conf.d/*.conf configuration snippets (#444953).
- Mark the default index.html in order to not loose changes upon upgrade if it
  was edited or replaced with a different file (#438564).
- Include patch to add the INIT INFO block to the init script (#246973).

* Mon Oct 13 2008 Matthias Saou <matthias@saou.eu> 1.4.20-1
- Update to 1.4.20 final.

* Mon Sep 22 2008 Matthias Saou <matthias@saou.eu> 1.4.20-0.1.r2303
- Update to 1.4.20 r2303 pre-release.

* Mon Sep 22 2008 Matthias Saou <matthias@saou.eu> 1.4.19-5
- Include memory leak patch (changeset #2305 from ticket #1774).

* Thu Apr 24 2008 Matthias Saou <matthias@saou.eu> 1.4.19-4
- Merge in second changest from upstream fix for upstream bug #285.

* Thu Mar 27 2008 Matthias Saou <matthias@saou.eu> 1.4.19-3
- Include sslshutdown patch, upstream fix to upstream bug #285 (#439066).

* Sat Mar 22 2008 Matthias Saou <matthias@saou.eu> 1.4.19-2
- Provide "webserver" (#437884).

* Wed Mar 12 2008 Matthias Saou <matthias@saou.eu> 1.4.19-1
- Update to 1.4.19, which includes all previous security fixes + bugfixes.

* Tue Mar  4 2008 Matthias Saou <matthias@saou.eu> 1.4.18-6
- Include patch for CVE-2008-0983 (crash when low on file descriptors).
- Include patch for CVE-2008-1111 (cgi source disclosure).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org>
 - Rebuild for deps

* Wed Oct 31 2007 Matthias Saou <matthias@saou.eu> 1.4.18-3
- Update mod_geoip source to fix segfault upon stopping lighttpd.

* Mon Oct 22 2007 Matthias Saou <matthias@saou.eu> 1.4.18-2
- Include mod_geoip additional source, make it an optional sub-package.
- Reorder sub-packages alphabetically in spec file.
- Make sub-packages require exact release, just in case.
- Change default webroot back from /srv to /var.

* Mon Sep 10 2007 Matthias Saou <matthias@saou.eu> 1.4.18-1
- Update to 1.4.18.
- Include newly installed lighttpd-angel ("angel" process meant to always run
  as root and restart lighttpd when it crashes, spawn processes on SIGHUP), but
  it's in testing stage and must be run with -D for now.

* Wed Sep  5 2007 Matthias Saou <matthias@saou.eu> 1.4.17-1
- Update to 1.4.17.
- Update defaultconf patch to match new example configuration.
- Include patch to fix log file rotation with max-workers set (trac #902).
- Add /var/run/lighttpd/ directory where to put fastcgi sockets.

* Thu Aug 23 2007 Matthias Saou <matthias@saou.eu> 1.4.16-3
- Add /usr/bin/awk build requirement, used to get LIGHTTPD_VERSION_ID.

* Wed Aug 22 2007 Matthias Saou <matthias@saou.eu> 1.4.16-2
- Rebuild to fix wrong execmem requirement on ppc32.

* Thu Jul 26 2007 Matthias Saou <matthias@saou.eu> 1.4.16-1
- Update to 1.4.16 security fix release.

* Mon Apr 16 2007 Matthias Saou <matthias@saou.eu> 1.4.15-1
- Update to 1.4.15.
- Remove now included previous patch.
- Switch to using the bz2 source.
- Add optional --with-webdav-locks support.

* Fri Feb 16 2007 Matthias Saou <matthias@saou.eu> 1.4.13-6
- Include patch to fix 99% cpu bug when client connection is dropped.

* Fri Feb  2 2007 Matthias Saou <matthias@saou.eu> 1.4.13-5
- Update defaultconf patch to change php binary to /usr/bin/php-cgi (#219723).
- Noticed %%{?_smp_mflags} was missing, so add it as it works fine.

* Mon Jan 29 2007 Matthias Saou <matthias@saou.eu> 1.4.13-4
- Remove readline-devel build req, added by lua but since fixed (#213895).

* Mon Nov  6 2006 Matthias Saou <matthias@saou.eu> 1.4.13-3
- Switch to using killall for log rotation to fix it when using workers.

* Mon Oct 16 2006 Matthias Saou <matthias@saou.eu> 1.4.13-2
- Remove gcc-c++ build req, it's part of the defaults.
- Add readline-devel build req, needed on RHEL4.

* Wed Oct 11 2006 Matthias Saou <matthias@saou.eu> 1.4.13-1
- Update to 1.4.13, which contains the previous fix.

* Tue Oct  3 2006 Matthias Saou <matthias@saou.eu> 1.4.12-3
- Include fix for segfaults (lighttpd bug #876, changeset 1352).

* Mon Sep 25 2006 Matthias Saou <matthias@saou.eu> 1.4.12-1
- Update to 1.4.12 final.

* Fri Sep 22 2006 Matthias Saou <matthias@saou.eu> 1.4.12-0.1.r1332
- Update to latest 1.4.12 pre-release, fixes SSL issues and other bugs.
- Update powered_by_fedora.png to the new logo.

* Mon Aug 28 2006 Matthias Saou <matthias@saou.eu> 1.4.11-2
- FC6 rebuild.

* Thu Mar  9 2006 Matthias Saou <matthias@saou.eu> 1.4.11-1
- Update to 1.4.11.

* Mon Mar  6 2006 Matthias Saou <matthias@saou.eu> 1.4.10-2
- FC5 rebuild.

* Wed Feb  8 2006 Matthias Saou <matthias@saou.eu> 1.4.10-1
- Update to 1.4.10.
- Remove now included fix.

* Wed Jan 25 2006 Matthias Saou <matthias@saou.eu> 1.4.9-2
- Add mod_fastcgi-fix patch to fix crash on backend overload.

* Mon Jan 16 2006 Matthias Saou <matthias@saou.eu> 1.4.9-1
- Update to 1.4.9.

* Wed Nov 23 2005 Matthias Saou <matthias@saou.eu> 1.4.8-1
- Update to 1.4.8.

* Fri Nov  4 2005 Matthias Saou <matthias@saou.eu> 1.4.7-1
- Update to 1.4.7.

* Wed Oct 12 2005 Matthias Saou <matthias@saou.eu> 1.4.6-1
- Update to 1.4.6.

* Mon Oct  3 2005 Matthias Saou <matthias@saou.eu> 1.4.5-1
- Update to 1.4.5.
- Disable gamin/fam support for now, it does not work.

* Tue Sep 27 2005 Matthias Saou <matthias@saou.eu> 1.4.4-3
- Update to current SVN to check if it fixes the remaining load problems.

* Wed Sep 21 2005 Matthias Saou <matthias@saou.eu> 1.4.4-2
- Patch to SVN 722 revision : Fixes a crash in mod_mysql_vhost and a problem
  with keepalive and certain browsers.

* Mon Sep 19 2005 Matthias Saou <matthias@saou.eu> 1.4.4-1
- Update to 1.4.4 final.
- Enable ldap auth, gdbm and gamin/fam support by default.

* Thu Sep 15 2005 Matthias Saou <matthias@saou.eu> 1.4.4-0
- Update to 1.4.4 pre-release (fixes another fastcgi memleak).
- Enable lua (cml module) by default.
- Add --with-webdav-props conditional option.

* Tue Sep 13 2005 Matthias Saou <matthias@saou.eu> 1.4.3-2
- Include lighttpd-1.4.3-stat_cache.patch to fix memleak.

* Fri Sep  2 2005 Matthias Saou <matthias@saou.eu> 1.4.3-1.1
- Rearrange the included index.html to include the new logo, button and
  favicon from lighttpd.net.

* Fri Sep  2 2005 Matthias Saou <matthias@saou.eu> 1.4.3-1
- Update to 1.4.3.
- No longer override libdir at make install stage, use DESTDIR instead, as
  the resulting binary would now have referenced to %%{buildroot} :-(

* Tue Aug 30 2005 Matthias Saou <matthias@saou.eu> 1.4.2-1
- Update to 1.4.2.

* Mon Aug 22 2005 Matthias Saou <matthias@saou.eu> 1.4.1-1
- Update to 1.4.1.

* Sun Aug 21 2005 Matthias Saou <matthias@saou.eu> 1.4.0-1
- Update to 1.4.0.
- Add conditional of gamin, gdbm, memcache and lua options.

* Mon Aug  1 2005 Matthias Saou <matthias@saou.eu> 1.3.16-2
- Update to 1.3.16, rebuild.

* Mon Jul 18 2005 Matthias Saou <matthias@saou.eu> 1.3.15-1
- Update to 1.3.15.

* Mon Jun 20 2005 Matthias Saou <matthias@saou.eu> 1.3.14-1
- Update to 1.3.14.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.3.13-5
- rebuild on all arches

* Mon Apr  4 2005 Matthias Saou <matthias@saou.eu> 1.3.13-4
- Change signal sent from the logrotate script from USR1 to HUP, as that's the
  correct one.

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1.3.13-2
- Include /etc/lighttpd directory.

* Sun Mar  6 2005 Matthias Saou <matthias@saou.eu> 1.3.13-1
- Update to 1.3.13.

* Wed Mar  2 2005 Matthias Saou <matthias@saou.eu> 1.3.12-1
- Update to 1.3.12.
- Remove obsolete empty_cgi_handler patch.

* Tue Mar  1 2005 Matthias Saou <matthias@saou.eu> 1.3.11-2
- Add missing defattr to sub-packages (#150018).

* Mon Feb 21 2005 Matthias Saou <matthias@saou.eu> 1.3.11-0
- Update to 1.3.11.
- Remove cleanconf and init.d patches (merged upstream).
- Add empty_cgi_handler patch.

* Fri Feb 18 2005 Matthias Saou <matthias@saou.eu> 1.3.10-0
- Split off -fastcgi sub-package.
- Include php.d entry to set sane FastCGI defaults.

* Wed Feb 16 2005 Matthias Saou <matthias@saou.eu> 1.3.10-0
- Spec file cleanup for freshrpms.net/Extras.
- Compile OpenSSL support unconditionally.
- Put modules in a subdirectory of libdir.
- Don't include all of libdir's content to avoid debuginfo content.
- Add optional LDAP support.
- Add patch to change the default configuration.
- Add dedicated lighttpd user/group creation.
- Add logrotate entry.
- Include a nice little default page for the default setup.
- Split off mod_mysql_vhost sub-package, get dep only there.
- Use webroot in /srv by default.
- Exclude .la files, I doubt anyone will need them.

* Thu Sep 30 2004 <jan@kneschke.de> 1.3.1
- upgraded to 1.3.1

* Tue Jun 29 2004 <jan@kneschke.de> 1.2.3
- rpmlint'ed the package
- added URL
- added (noreplace) to start-script
- change group to Networking/Daemon (like apache)

* Sun Feb 23 2003 <jan@kneschke.de>
- initial version

