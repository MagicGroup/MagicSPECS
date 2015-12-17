
# base pkg default to SQLITE now, install -mysql if you want that instead
%global database_backend SQLITE

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

%if 0%{?rhel} == 6
%define cmake_pkg cmake28
%else
%define cmake_pkg cmake
%endif

Summary: PIM Storage Service
Summary(zh_CN.UTF-8): 个人信息管理存储服务
Name:    akonadi
Version: 1.13.0
Release: 4%{?dist}

License: LGPLv2+
URL:     http://community.kde.org/KDE_PIM/Akonadi 
%if 0%{?snap}
# git clone git://git.kde.org/akonadi
# git archive --prefix=akonadi-%{version}/ master | bzip2 > akonadi-%{version}-%{snap}.tar.bz2
Source0: akonadi-%{version}-%{snap}.tar.bz2
%else
# Official release
Source0: http://download.kde.org/stable/akonadi/src/akonadi-%{version}.tar.bz2
%endif

## mysql config
Source10: akonadiserverrc.mysql

## upstreamable patches

## upstream patches

%define mysql_conf_timestamp 20130607

BuildRequires: automoc4
BuildRequires: boost-devel
BuildRequires: %{cmake_pkg} >= 2.8.8
# for xsltproc
BuildRequires: libxslt
BuildRequires: pkgconfig(QtDBus) pkgconfig(QtSql) pkgconfig(QtXml)
BuildRequires: pkgconfig(shared-mime-info)
BuildRequires: pkgconfig(soprano) 
BuildRequires: pkgconfig(sqlite3) >= 3.6.23
# %%check
BuildRequires: dbus-x11 xorg-x11-server-Xvfb
# backends, used at buildtime to query known locations of server binaries
# FIXME/TODO: set these via cmake directives, avoids needless buildroot items
BuildRequires: mysql-server
BuildRequires: postgresql-server

#%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
Requires: qt4%{?_isa} >= 4.8.5-1

Requires(postun): /sbin/ldconfig

%description
%{summary}.

%description -l zh_CN.UTF-8
个人信息管理存储服务。

%package devel
Summary: Developer files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
 %{name} 的开发文件。

%package mysql
Summary: Akonadi MySQL backend support
Summary(zh_CN.UTF-8): Akonadi 的 MySQL 后端支持
# upgrade path
Obsoletes: akonadi < 1.7.90-2
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: mysql-server
Requires: qt4-mysql%{?_isa}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
%description mysql
Configures akonadi to use mysql backend by default.

Requires an available instance of mysql server at runtime.
Akonadi can spawn a per-user one automatically if the mysql-server
package is installed on the machine.
See also: %{_sysconfdir}/akonadi/mysql-global.conf

%description mysql -l zh_CN.UTF-8
配置 akonadi 默认使用 mysql 的后端。

在运行时需要一个可用的 mysql 服务实例。
如果机器上安装有 mysql-server，Akonadi 可以自动生成每个用户的。
也可以查看：%{_sysconfdir}/akonadi/mysql-global.conf


%prep
%setup -q -n akonadi-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{?cmake28}%{!?cmake28:%{?cmake}} \
  -DCONFIG_INSTALL_DIR=%{_sysconfdir} \
  %{?database_backend:-DDATABASE_BACKEND=%{database_backend}} \
  -DINSTALL_QSQLITE_IN_QT_PREFIX:BOOL=ON \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot} 
make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}

install -p -m644 -D %{SOURCE10} %{buildroot}%{_sysconfdir}/xdg/akonadi/akonadiserverrc.mysql

mkdir -p %{buildroot}%{_datadir}/akonadi/agents

# create "big" config (analog to -mobile.conf)
install -p \
  %{buildroot}%{_sysconfdir}/akonadi/mysql-global.conf \
  %{buildroot}%{_sysconfdir}/akonadi/mysql-global-big.conf

# default to small/mobile config
install -p \
  %{buildroot}%{_sysconfdir}/akonadi/mysql-global-mobile.conf \
  %{buildroot}%{_sysconfdir}/akonadi/mysql-global.conf

touch -d %{mysql_conf_timestamp} \
  %{buildroot}%{_sysconfdir}/akonadi/mysql-global*.conf \
  %{buildroot}%{_sysconfdir}/akonadi/mysql-local.conf

# create/own %{_libdir}/akondi
mkdir -p %{buildroot}%{_libdir}/akonadi

# %%ghost'd global akonadiserverrc 
touch akonadiserverrc 
install -p -m644 -D akonadiserverrc %{buildroot}%{_sysconfdir}/xdg/akonadi/akonadiserverrc

magic_rpm_clean.sh

%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion akonadi)" = "%{version}"
# this one (still) fails in mock (local build ok):
# 14/14 Test #14: akonadi-dbconfigtest
xvfb-run -a dbus-launch --exit-with-session make test -C %{_target_platform}  ||:


%post -p /sbin/ldconfig

%posttrans
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
/sbin/ldconfig ||:
if [ $1 -eq 0 ] ; then
  update-mime-database %{_datadir}/mime &> /dev/null ||:
fi

%files
%doc AUTHORS lgpl-license
%dir %{_sysconfdir}/xdg/akonadi/
%ghost %config(missingok,noreplace) %{_sysconfdir}/xdg/akonadi/akonadiserverrc
%dir %{_sysconfdir}/akonadi/
%{_bindir}/akonadi_agent_launcher
%{_bindir}/akonadi_agent_server
%{_bindir}/akonadi_control
%{_bindir}/akonadi_rds
%{_bindir}/akonadictl
%{_bindir}/akonadiserver
%{_libdir}/akonadi/
%{_libdir}/libakonadiprotocolinternals.so.1*
%{_datadir}/dbus-1/interfaces/org.freedesktop.Akonadi.*.xml
%{_datadir}/dbus-1/services/org.freedesktop.Akonadi.*.service
%{_datadir}/mime/packages/akonadi-mime.xml
%{_datadir}/akonadi/
%{_qt4_plugindir}/sqldrivers/libqsqlite3.so

%files devel
%{_bindir}/asapcat
%{_includedir}/akonadi/
%{_libdir}/pkgconfig/akonadi.pc
%{_libdir}/libakonadiprotocolinternals.so
%{_libdir}/cmake/Akonadi/

%post mysql
%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/xdg/akonadi/akonadiserverrc \
  akonadiserverrc \
  %{_sysconfdir}/xdg/akonadi/akonadiserverrc.mysql \
  10

%postun mysql
if [ $1 -eq 0 ]; then
%{_sbindir}/update-alternatives \
  --remove akonadiserverrc \
  %{_sysconfdir}/xdg/akonadi/akonadiserverrc.mysql 
fi

%files mysql
%config(noreplace) %{_sysconfdir}/xdg/akonadi/akonadiserverrc.mysql
%config(noreplace) %{_sysconfdir}/akonadi/mysql-global.conf
%config(noreplace) %{_sysconfdir}/akonadi/mysql-local.conf
# example conf's
%{_sysconfdir}/akonadi/mysql-global-big.conf
%{_sysconfdir}/akonadi/mysql-global-mobile.conf


%changelog
* Fri Dec 26 2014 Liu Di <liudidi@gmail.com> - 1.13.0-4
- 为 Magic 3.0 重建

* Fri Dec 26 2014 Liu Di <liudidi@gmail.com> - 1.13.0-3
- 为 Magic 3.0 重建

* Wed Oct 22 2014 Liu Di <liudidi@gmail.com> - 1.13.0-2
- 更新到 1.13.0

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 1.12.1-2
- 更新到 1.12.1

* Thu Mar 06 2014 Liu Di <liudidi@gmail.com> - 1.11.80-2
- 更新到 1.11.80

* Sat Nov 30 2013 Rex Dieter <rdieter@fedoraproject.org> 1.11.0-1
- 1.11.0

* Fri Nov 15 2013 Rex Dieter <rdieter@fedoraproject.org> 1.10.80-1
- 1.10.80

* Mon Oct 07 2013 Daniel Vrátil <dvratil@redhat.com> - 1.10.3-1
- 1.10.3

* Sun Jul 28 2013 Daniel Vrátil <dvratil@redhat.com> - 1.10.2-1
- 1.10.2

* Sat Jul 27 2013 pmachata@redhat.com - 1.10.1-2
- Rebuild for boost 1.54.0

* Thu Jul 25 2013 Rex Dieter <rdieter@fedoraproject.org> 1.10.1-1
- akonadi-1.10.1
- mysql_conf_timestamp 20130607

* Sat Jul 13 2013 Rex Dieter <rdieter@fedoraproject.org> 1.10.0-1
- 1.10.0

* Thu Jun 27 2013 Rex Dieter <rdieter@fedoraproject.org> 1.9.80-1
- 1.9.80

* Wed May 08 2013 Rex Dieter <rdieter@fedoraproject.org> 1.9.2-1
- 1.9.2

* Mon Mar 11 2013 Rex Dieter <rdieter@fedoraproject.org> 1.9.1-3
- revert hard-coding mariadb on f19+

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> 1.9.1-1
- 1.9.1

* Mon Feb 11 2013 Rex Dieter <rdieter@fedoraproject.org> 1.9.0-5
- drop boost patch, qt/moc has workaround now

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.9.0-4
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.9.0-3
- Rebuild for Boost-1.53.0

* Fri Feb 08 2013 Rex Dieter <rdieter@fedoraproject.org> 1.9.0-2
- pull in a few upstream fixes

* Thu Jan 03 2013 Rex Dieter <rdieter@fedoraproject.org> 1.9.0-1
- 1.9.0

* Mon Dec 03 2012 Rex Dieter <rdieter@fedoraproject.org> 1.8.80-1
- 1.8.80

* Tue Oct 16 2012 Rex Dieter <rdieter@fedoraproject.org> 1.8.1-1
- 1.8.1

* Sat Oct 13 2012 Rex Dieter <rdieter@fedoraproject.org> 1.8.0-3
- include a couple upstream patches

* Mon Jul 30 2012 Rex Dieter <rdieter@fedoraproject.org> 1.8.0-2
- rebuild (boost)

* Thu Jul 26 2012 Rex Dieter <rdieter@fedoraproject.org> 1.8.0-1
- 1.8.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Rex Dieter <rdieter@fedoraproject.org> 1.7.90-2
- -mysql subpkg

* Mon Jun 25 2012 Rex Dieter <rdieter@fedoraproject.org> 1.7.90-1
- 1.7.90

* Sat Mar 31 2012 Rex Dieter <rdieter@fedoraproject.org> 1.7.2-1
- 1.7.2

* Thu Mar 15 2012 Rex Dieter <rdieter@fedoraproject.org> 1.7.1-2
- New cleanup in "akonadictl fsck"

* Tue Mar 06 2012 Rex Dieter <rdieter@fedoraproject.org> 1.7.1-1
- 1.7.1

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for c++ ABI breakage

* Tue Jan 24 2012 Rex Dieter <rdieter@fedoraproject.org> 1.7.0-1
- 1.7.0

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.90-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jan 11 2012 Rex Dieter <rdieter@fedoraproject.org> 1.6.90-3
- BR: +postgresql-server, -mysql-devel
- -devel: drop explicit BR: qt4-devel, pulled in via auto-pkgconfig deps

* Sat Dec 31 2011 Rex Dieter <rdieter@fedoraproject.org> 1.6.90-2
- %%check: try harder to make work in mock (using xvfb)
- default to sqlite on 'small' platforms (arm)

* Fri Dec 23 2011 Rex Dieter <rdieter@fedoraproject.org> 1.6.90-1
- 1.6.90

* Sun Nov 20 2011 Rex Dieter <rdieter@fedoraproject.org> 1.6.2-5
- rebuild (boost)

* Thu Oct 27 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.6.2-4
- rebuild against fixed glibc headers in Rawhide

* Wed Oct 19 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.6.2-3
- rebuild against fixed Qt headers in Rawhide

* Sat Oct 15 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.6.2-2.1
- rebuild against known working Qt headers for F16 final

* Thu Oct 13 2011 Rex Dieter <rdieter@fedoraproject.org> 1.6.2-2
- switch back to mysql backend default
- pkgconfig-style deps
- own/ghost /etc/xdg/akonadi/akonadiserverrc

* Tue Oct 04 2011 Rex Dieter <rdieter@fedoraproject.org> 1.6.2-1
- 1.6.2

* Fri Sep 16 2011 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-1
- 1.6.1

* Mon Aug 15 2011 Kalev Lember <kalevlember@gmail.com> 1.6.0-4
- Rebuilt for rpm bug #728707

* Thu Jul 21 2011 Rex Dieter <rdieter@fedoraproject.org> 1.6.0-3
- rebuild (boost)

* Wed Jul 13 2011 Rex Dieter <rdieter@fedoraproject.org> 1.6.0-2
- -DDATABASE_BACKEND=SQLITE 

* Tue Jul 12 2011 Rex Dieter <rdieter@fedoraproject.org> 1.6.0-1
- 1.6.0

* Wed Jun 29 2011 Rex Dieter <rdieter@fedoraproject.org> 1.5.80-2
- drop mysql_config patch, use -mobile.conf instead
- use database_backend macro more

* Thu Jun 02 2011 Jaroslav Reznik <jreznik@redhat.com> 1.5.80-1
- 1.5.80

* Sun May 15 2011 Rex Dieter <rdieter@fedoraproject.org> 1.5.3-1
- 1.5.3

* Tue Apr 05 2011 Rex Dieter <rdieter@fedoraproject.org> 1.5.2-1
- akonadi-1.5.2

* Mon Mar 14 2011 Rex Dieter <rdieter@fedoraproject.org> 1.5.1-1
- akonadi-1.5.1

* Tue Feb 15 2011 Rex Dieter <rdieter@fedoraproject.org> 1.5.0-4
- arch'ify qt4-mysql dep

* Fri Feb 11 2011 Rex Dieter <rdieter@fedoraproject.org> 1.5.0-3.1
- shrinky-dink db on f15 too

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Rex Dieter <rdieter@fedoraproject.org> 1.5.0-2
- rebuild (boost)

* Sat Jan 22 2011 Rex Dieter <rdieter@fedoraproject.org> 1.5.0-1
- akonadi-1.5.0

* Fri Jan 07 2011 Rex Dieter <rdieter@fedoraproject.org> 1.4.95-1
- akonadi-1.4.95

* Fri Jan 07 2011 <rdieter@fedoraproject.org> - 1.4.90-2
- rebuild (mysql)
- %%check: make test should pass 100% now

* Tue Dec 21 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.4.90-1
- akonadi-1.4.90

* Sun Nov 21 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.4.80-1
- akonadi-1.4.80

* Sat Nov 20 2010 Rex Dieter <rdieter@fedoraproject.org> 1.4.54-1.20101120
- akonadi-1.4.54-20101120 snapshot

* Fri Oct 22 2010 Rex Dieter <rdieter@fedoraproject.org> 1.4.1-2
- patch out (paranoid) assert

* Fri Oct 22 2010 Rex Dieter <rdieter@fedoraproject.org> 1.4.1-1
- akonadi-1.4.1

* Tue Oct 19 2010 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-3
- own %%_libdir/akonadi (#644540)

* Sat Oct 09 2010 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-2
- apply mysql_conf patch only for < f15

* Sat Aug 07 2010 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-1
- akonadi-1.4.0

* Thu Aug  5 2010 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.90-3
- rebuild for boost again

* Tue Jul 27 2010 Rex Dieter <rdieter@fedoraproject.org> 1.3.90-2
- rebuild (boost)

* Thu Jul 15 2010 Rex Dieter <rdieter@fedoraproject.org> 1.3.90-1
- akonadi-1.3.90

* Wed Jun 09 2010 Rex Dieter <rdieter@fedoraproject.org> 1.3.85-1
- akonadi-1.3.85

* Wed May 26 2010 Rex Dieter <rdieter@fedoraproject.org> 1.3.80-1
- akonadi-1.3.80

* Sun May 23 2010 Rex Dieter <rdieter@fedoraproject.org> 1.3.60-1.20100523
- akonadi-1.3.60 (20100523 snapshot)

* Tue Mar 30 2010 Rex Dieter <rdieter@fedoraproject.org> 1.3.1-4
- fix typo on qt4 dep

* Tue Mar 30 2010 Rex Dieter <rdieter@fedoraproject.org> 1.3.1-3
- backport mysql_update patch (kde#232702)
- add (versioned) Requires: qt4 ...

* Wed Feb 10 2010 Rex Dieter <rdieter@fedoraproject.org> 1.3.1-2
- mysql_conf_timestamp 20100209 (ie, force a config resync)

* Tue Feb 09 2010 Rex Dieter <rdieter@fedoraproject.org> 1.3.1-1
- akonadi-1.3.1

* Wed Jan 20 2010 Rex Dieter <rdieter@fedoraproject.org> 1.3.0-1
- akonadi-1.3.0

* Tue Jan 19 2010 Rex Dieter <rdieter@fedoraproject.org> 1.2.90-3
- Client applications freeze because of hanging Nepomuk search job (kde#219687)

* Sat Jan 16 2010 Rex Dieter <rdieter@fedoraproject.org> 1.2.90-2
- rebuild (boost)

* Wed Jan 06 2010 Rex Dieter <rdieter@fedoraproject.org> 1.2.90-1
- akonadi-1.2.90

* Mon Dec 07 2009 Rex Dieter <rdieter@fedoraproject.org> 1.2.80-1
- Akonadi 1.2.80
- restore mysql deps

* Sat Nov 21 2009 Ben Boeckel <MathStuf@gmail.com> - 1.2.61-0.1.svn1052261
- Update to SVN snapshot of 1.2.61

* Tue Sep  1 2009 Lukáš Tinkl <ltinkl@redhat.com> - 1.2.1-1
- Akonadi 1.2.1

* Fri Aug 28 2009 Rex Dieter <rdieter@fedoraproject.org> 1.2.0-2.2
- temporarily drop mysql-related bits, to workaround broken rawhide deps

* Tue Aug 25 2009 Karsten Hopp <karsten@redhat.com> 1.2.0-2
- bump and rebuild, as s390x picked up an old boost library

* Thu Jul 30 2009 Lukáš Tinkl <ltinkl@redhat.com> - 1.2.0-1
- Akonadi 1.2.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.95-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 25 2009 Than Ngo <than@redhat.com> - 1.1.95-1
- 1.1.95

* Wed Jun 03 2009 Rex Dieter <rdieter@fedoraproject.org> 1.1.90-1
- akonadi-1.1.90

* Tue May 26 2009 Rex Dieter <rdieter@fedoraproject.org> 1.1.85-3
- akonadi.pc.cmake: s/AKONADI_LIB_VERSION_STRING/AKONADI_VERSION_STRING/

* Tue May 12 2009 Than Ngo <than@redhat.com> 1.1.85-2
- fix rpm file list

* Wed May 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.85-1
- akonadi-1.1.85

* Thu Apr 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.2-1
- akonadi-1.1.2
- optimize scriptlets a bit

* Wed Feb 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-6
- rev startup patch
- BR: cmake >= 2.6.0
- preserve timestamp's on mysql*.conf's

* Tue Feb 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-5
- own %%_sysconfig/akonadi/mysql-local.conf
- startup patch: reset conf only when needed, and clear mysql log file on update

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-3
- shrink default db initial size a bit (approx 140mb->28mb)
- drop extraneous RPATH-cmake baggage

* Wed Jan 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-1
- 1.1.1

* Sun Jan 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-1
- 1.1.0

* Tue Dec 16 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.0.81-1
- 1.0.81

* Mon Dec 08 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.0.80-3
- restore Requires: mysql-server

* Mon Dec 01 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.0.80-2
- own /usr/share/akonadi and /usr/share/akonadi/agents (#473595)

* Wed Nov 26 2008 Than Ngo <than@redhat.com> -  1.0.80-1
- 1.0.80

* Wed Oct 22 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-4
- drop Requires: mysql-server (for now), mention in %%description

* Wed Jul 30 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-3
- Requires: mysql-server

* Wed Jul 30 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-2
- BR: mysql-server
- Requires: qt4-mysql
- cleanup spec

* Wed Jul 23 2008 Than Ngo <than@redhat.com> -  1.0.0-1
- 1.0.0

* Wed Jun 18 2008 Rex Dieter <rdieter@fedoraproject.org> 0.82.0-1
- akonadi-0.82.0

* Tue Jun  3 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.81.0-0.2.20080526svn812787
- BR automoc, drop automoc hack

* Mon May 26 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.81.0-0.1.20080526svn812787
- update to revision 812787 from KDE SVN (to match KDE 4.1 Beta 1)
- restore builtin automoc4 for now
- update file list, require pkgconfig in -devel (.pc file now included)

* Mon May  5 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.80.0-2
- -devel: remove bogus Requires: pkgconfig

* Sat May  3 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.80.0-1
- first Fedora package
