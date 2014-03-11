Summary: Update notification daemon
Name: yum-updatesd
Epoch: 1
Version: 0.9
Release: 14%{?dist}
License: GPLv2
Group: System Environment/Base
Source0: %{name}-%{version}.tar.bz2
Source1: %{name}.service

#Fixed in upstream
Patch0: %{name}.nm-online.patch
Patch1: %{name}.typo-packages.patch

URL: http://linux.duke.edu/yum/
BuildArch: noarch
BuildRequires: python
BuildRequires: systemd-units
Requires: python >= 2.4
Requires: yum >= 3.2.0
Requires: dbus-python
Requires: pygobject2
Requires: gamin-python
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
yum-updatesd provides a daemon which checks for available updates and 
can notify you when they are available via email, syslog or dbus. 

%prep
%setup -q

%patch0
%patch1

%build
make

%install
make DESTDIR=$RPM_BUILD_ROOT install

# Don't need the old sysv initscript anymore
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/

mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable yum-updatesd.service > /dev/null 2>&1 || :
    /bin/systemctl stop yum-updatesd.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart yum-updatesd.service >/dev/null 2>&1 || :
fi

# one off fix for bug #807006
%triggerun -- %{name} < 1:0.9-11
/bin/systemctl --no-reload enable %{name}.service >/dev/null 2>&1 || :

%triggerun -- %{name} < 1:0.9-6
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply yum-updatesd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save %{name} >/dev/null 2>&1 || :

# This package is allowed to autostart:
/bin/systemctl --no-reload enable %{name}.service >/dev/null 2>&1 || :

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del yum-updatesd >/dev/null 2>&1 || :
/bin/systemctl try-restart yum-updatesd.service >/dev/null 2>&1 || :

%files
%doc COPYING
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/yum/yum-updatesd.conf
%config %{_sysconfdir}/dbus-1/system.d/yum-updatesd.conf
%{_sbindir}/yum-updatesd
%{_libexecdir}/yum-updatesd-helper
%{_mandir}/man*/yum-updatesd*


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1:0.9-14
- 为 Magic 3.0 重建

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 01 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 1:0.9-12
- patch terminology in email subject 

* Mon Mar 26 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 1:0.9-11
- enable the service by default on upgrades (fix bug #807006)

* Fri Feb 17 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 1:0.9-10
- adapt to new networkmanager dbus interface

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep  9 2011 Tom Callaway <spot@fedoraproject.org> - 1:0.9-8
- and fix Requires(post)... :P

* Fri Sep  9 2011 Tom Callaway <spot@fedoraproject.org> - 1:0.9-7
- add missing scriptlets

* Thu Sep 08 2011 Tom Callaway <spot@fedoraproject.org> - 1:0.9-6
- fix broken scriptlets

* Thu Sep 08 2011 Tom Callaway <spot@fedoraproject.org> - 1:0.9-5
- update to systemd service

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 17 2007 Jeremy Katz <katzj@redhat.com> - 1:0.9-1
- More mail fixes (Pierre Ossman)

* Wed Dec  5 2007 Jeremy Katz <katzj@redhat.com> - 1:0.8-1
- Use sendmail (Pierre Ossman, #397711)
- Don't wake up as often (#391571)
- Improve mail output (Pierre Ossman, #387181)
- Fix some tracebacks (#387051, #374801)

* Fri Oct 12 2007 Jeremy Katz <katzj@redhat.com> - 1:0.7-1
- fix error when download is set, but no packages are available (#329361)

* Wed Oct 10 2007 Jeremy Katz <katzj@redhat.com> - 1:0.6-1
- add lsb initscript header (#247106)
- overly simplistic service start speed-up

* Wed Sep  5 2007 Jeremy Katz <katzj@redhat.com> - 1:0.5-1
- add option for configurable SMTP server
- fix email sending (Rich Fearn, #251196)
- make updates checking in the presence of NetworkManager smarter (#213732)
- ensure group info gets updated
- work with yum 3.0.x (jantill)
- don't poll gamin

* Tue Jul 24 2007 Jeremy Katz <katzj@redhat.com> - 1:0.4-1
- minor review fixes.  add --oneshot mode

* Mon Jul 23 2007 Jeremy Katz <katzj@redhat.com> - 1:0.3-1
- update to new version

* Thu Jul 19 2007 Jeremy Katz <katzj@redhat.com> - 1:0.1-1
- new package for standalone yum-updatesd
