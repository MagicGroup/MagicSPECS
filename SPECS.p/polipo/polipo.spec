Name:           polipo
Version:	1.1.1
Release:	3%{?dist}
Summary:        Lightweight caching web proxy
Summary(zh_CN.UTF-8): 轻量级的 Web 缓存代理
License:        MIT
Source0:        http://www.pps.univ-paris-diderot.fr/~jch/software/files/%{name}/%{name}-%{version}.tar.gz
Source2:        %{name}.config
Source3:        %{name}.forbidden
Source4:        %{name}.logrotate
Source5:        %{name}.nm
Source6:        %{name}.tmpfiles
Source7:        %{name}.service
Source8:        %{name}.sysconfig
Source9:        %{name}.cron
Patch0:         http-assertion-failure.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Group:          System Environment/Daemons
URL:            http://www.pps.jussieu.fr/~jch/software/%{name}/
BuildRequires:  texinfo
BuildRequires:  systemd-units
Requires:       logrotate
Requires(post): info
Requires(preun):info
Requires(pre):  shadow-utils
Requires(post): chkconfig
Requires(preun):chkconfig

Requires(pre):  %{_sbindir}/useradd

Requires(preun):systemd-units
Requires(post): systemd-units, %{_sbindir}/usermod
Requires(postun):systemd-units


%description
Polipo is a lightweight caching web proxy that was designed as a personal
cache. It is able to cache incomplete objects and will complete them using
range requests. It will use HTTP/1.1 pipelining if supported by the remote
server.

%description -l zh_CN.UTF-8
轻量级的 Web 缓存代理。

%prep
%setup -q

#patch0 -p1 -b .http-assertion-failure

%build
make %{?_smp_mflags} PREFIX=%{_prefix} BINDIR=%{_bindir} CDEBUGFLAGS="%{optflags}"

%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=%{_prefix} BINDIR=%{_bindir} MANDIR=%{_mandir} \
    INFODIR=%{_infodir} TARGET=$RPM_BUILD_ROOT
install -m 0755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}
install -m 0750 -d $RPM_BUILD_ROOT/%{_localstatedir}/cache/%{name}
install -D -p -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/config
install -D -p -m 0644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/forbidden
install -D -p -m 0644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/%{name}
install -D -p -m 0755 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/NetworkManager/dispatcher.d/25-%{name}
install -D -p -m 0755 %{SOURCE9} $RPM_BUILD_ROOT/%{_sysconfdir}/cron.daily/%{name}

install -D -p -m 0644 %{SOURCE6} $RPM_BUILD_ROOT/%{_sysconfdir}/tmpfiles.d/%{name}.conf
install -d -m 0755 $RPM_BUILD_ROOT/%{_localstatedir}/run/%{name}
install -d $RPM_BUILD_ROOT/%{_localstatedir}/log/%{name}

install -D -p -m 0644 %{SOURCE7} $RPM_BUILD_ROOT/%{_unitdir}/%{name}.service
install -D -p -m 0644 %{SOURCE8} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/%{name}

rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
useradd -r -g %{name} -d %{_localstatedir}/cache/%{name} -s /sbin/nologin -c "Polipo Web Proxy" %{name}
for i in %{_localstatedir}/run/%{name} %{_localstatedir}/cache/%{name} ; do
    if [ -d $i ] ; then
        for adir in `find $i -maxdepth 0 \! -user %{name}`; do
            /bin/chown -Rf %{name}:%{name} $adir
            /bin/chmod -Rf u+rwX $adir
        done
    fi
done
exit 0

%post
[ -e %{_localstatedir}/log/%{name}/%{name}.log ] || /bin/touch %{_localstatedir}/log/%{name}/%{name}.log
/bin/chmod -f 0640 %{_localstatedir}/log/%{name}/%{name}.log
/bin/chown -f %{name}:%{name} %{_localstatedir}/log/%{name}/%{name}.log
/sbin/restorecon %{_localstatedir}/log/%{name}/%{name}.log || :

/sbin/install-info --quiet --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz || : 

if [ $1 -eq 1 ]; then
    # package install, not upgrade
    /bin/systemctl daemon-reload > /dev/null 2>&1 || :
fi

%preun
if [ $1 = 0 ] ; then
    # package removal, not upgrade
    /sbin/systemctl disable %{name}.service > /dev/null 2>&1 || :
    /sbin/systemctl stop %{name}.service > /dev/null 2>&1 || :

    /sbin/install-info --quiet --info-dir=%{_infodir} --delete %{_infodir}/%{name}.info.gz || :
fi

%postun
    /bin/systemctl daemon-reload > /dev/null 2>&1 || :

if [ $1 -ge 1 ] ; then
    # package upgrade, not uninstall
    /bin/systemctl try-restart %{name}.service > /dev/null 2>&1 || :
fi

%triggerun -- %{name} < 1.0.4.1-4
if /sbin/chkconfig %{name}; then
    /bin/systemctl enable %{name}.service > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc README CHANGES COPYING *.sample
%dir %{_sysconfdir}/%{name}
%dir %{_datadir}/%{name}
%attr(0750,polipo,root) %dir %{_localstatedir}/log/%{name}
%attr(0750,%{name},%{name}) %dir %{_localstatedir}/cache/%{name}
%{_bindir}/%{name}
%{_datadir}/%{name}/*
%{_mandir}/man1/%{name}.*
%{_infodir}/%{name}.*
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/forbidden
%attr(0755,root,root) %{_sysconfdir}/NetworkManager/dispatcher.d/*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0755,root,root) %{_sysconfdir}/cron.daily/%{name}

%{_unitdir}/%{name}.service
%{_sysconfdir}/sysconfig/%{name}

%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%attr(0755,%{name},%{name}) %dir %{_localstatedir}/run/%{name}

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.1.1-3
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.1.1-2
- 为 Magic 3.0 重建

* Sat Jul 25 2015 Liu Di <liudidi@gmail.com> - 1.1.1-1
- 更新到 1.1.1

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 1.0.4.1-12
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bernard Johnson <bjohnson@symetrix.com> - 1.0.4.1-9
- systemd unit file is strange (bz #872872)
- have NetworkMananger use systemctl to restart service if it's running
- SELinux is preventing /usr/bin/polipo from 'open' accesses on the file
  polipo. (bz #770878)
- removed _with_systemd build capability since it's now default, removed all
  init infrastructure
- removed _with_tmpfilesd infrastructure
- Can polipo please use runuser rather then su in its cron jobs. (bz #804673)
- /etc/cron.daily/polipo returns failure if polipo is not running (bz #835631)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 John C. Peterson <jcp@eskimo.com> - 1.0.4.1-7
- fixed the bad value of ExecStart in the polipo.service file (bz #818688)
- added the (missing) sysconfig environment file (bz #818688)
- modified the daily purge script to read the sysconfig environment file
- modified the logrotate script to eliminate unwanted messages from chkconfig
- renumbered the last few source files (cosmetic)

* Sun Jan 22 2012 Bernard Johnson <bjohnson@symetrix.com> - 1.0.4.1-6
- add daily cache cleanup
- fix missing creation of /var/run directory (bz #755198)
- make sure log directory context is set correctly (bz #741779)
- fix denial of service vulnerability CVE-2011-3596 (bz #742897)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 26 2011 Bernard Johnson <bjohnson@symetrix.com> - 1.0.4.1-4
- take file / dir creation & testing out of initscript (bz #708814)
- remove log file / dir creation in spec too
- NetworkManager integration should use restart rather than reload (bz #699677)
- add support for tmpfiles.d (bz #656669)
- add support for systemd starting in F17

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 21 2010 Chen Lei <supercyper@163.com> 1.0.4.1-2
- fix for rpmlint warnings

* Sun Feb 21 2010 Chen Lei <supercyper@163.com> 1.0.4.1-1
- initial rpm build

