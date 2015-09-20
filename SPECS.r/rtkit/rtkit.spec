Name:             rtkit
Version:	0.11
Release:	2%{?dist}
Summary:          Realtime Policy and Watchdog Daemon
Summary(zh_CN.UTF-8): 实时策略和看门狗服务
Group:            System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
# The daemon itself is GPLv3+, the reference implementation for the client BSD
License:          GPLv3+ and BSD
URL:              http://git.0pointer.de/?p=rtkit.git
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:         dbus
Requires:         polkit
Requires:         systemd-units
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
BuildRequires:    dbus-devel >= 1.2
BuildRequires:    libcap-devel
BuildRequires:    polkit-devel
Source0:          http://0pointer.de/public/%{name}-%{version}.tar.xz
Patch1:           rtkit-mq_getattr.patch
Patch2:           0001-SECURITY-Pass-uid-of-caller-to-polkit.patch
Patch3:           rtkit-controlgroup.patch

%description
RealtimeKit is a D-Bus system service that changes the
scheduling policy of user processes/threads to SCHED_RR (i.e. realtime
scheduling mode) on request. It is intended to be used as a secure
mechanism to allow real-time scheduling to be used by normal user
processes.

%description -l zh_CN.UTF-8
实时策略和看门狗服务。

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure --with-systemdsystemunitdir=/lib/systemd/system
make %{?_smp_mflags}
./rtkit-daemon --introspect > org.freedesktop.RealtimeKit1.xml

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -D org.freedesktop.RealtimeKit1.xml $RPM_BUILD_ROOT/%{_datadir}/dbus-1/interfaces/org.freedesktop.RealtimeKit1.xml

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group rtkit >/dev/null 2>&1 || groupadd \
        -r \
        -g 172 \
        rtkit
getent passwd rtkit >/dev/null 2>&1 || useradd \
        -r -l \
        -u 172 \
        -g rtkit \
        -d /proc \
        -s /sbin/nologin \
        -c "RealtimeKit" \
        rtkit
:;

%post
if [ $1 -eq 1 ]; then
        /bin/systemctl enable rtkit.service >/dev/null 2>&1 || :
fi
dbus-send --system --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ReloadConfig >/dev/null 2>&1 || :

%preun
if [ "$1" -eq 0 ]; then
        /bin/systemctl --no-reload disable rtkit-daemon.service >/dev/null 2>&1 || :
        /bin/systemctl stop rtkit-daemon.service >/dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%files
%defattr(0644,root,root,0755)
%doc README GPL LICENSE rtkit.c rtkit.h
%attr(0755,root,root) %{_sbindir}/rtkitctl
%attr(0755,root,root) %{_libexecdir}/rtkit-daemon
%{_datadir}/dbus-1/system-services/org.freedesktop.RealtimeKit1.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.RealtimeKit1.xml
%{_datadir}/polkit-1/actions/org.freedesktop.RealtimeKit1.policy
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.RealtimeKit1.conf
/lib/systemd/system/rtkit-daemon.service
%{_mandir}/man8/*

%changelog
* Fri Sep 18 2015 Liu Di <liudidi@gmail.com> - 0.11-2
- 为 Magic 3.0 重建

* Fri Sep 18 2015 Liu Di <liudidi@gmail.com> - 0.11-1
- 更新到 0.11

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.10-3
- 为 Magic 3.0 重建

* Sun Feb 05 2012 Liu Di <liudidi@gmail.com> - 0.10-2
- 为 Magic 3.0 重建

* Thu Feb 17 2011 Lennart Poettering <lpoetter@redhat.com> - 0.10-1
- new upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug  4 2010 Lennart Poettering <lpoetter@redhat.com> - 0.9-2
- Convert systemd-install to systemctl

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> - 0.9-1
- New upstream release

* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> - 0.8-1
- New upstream release

* Fri Dec 18 2009 Lennart Poettering <lpoetter@redhat.com> - 0.5-1
- New release
- By default don't demote unknown threads
- Make messages less cute
- Fixes 530582

* Wed Aug 5 2009 Lennart Poettering <lpoetter@redhat.com> - 0.4-1
- New release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 2 2009 Lennart Poettering <lpoetter@redhat.com> - 0.3-1
- New release

* Thu Jun 17 2009 Lennart Poettering <lpoetter@redhat.com> - 0.2-1
- Initial packaging
