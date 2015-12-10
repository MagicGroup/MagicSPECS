Summary:        Random number generator related utilities
Summary(zh_CN.UTF-8): 随机数字生成器相关的工具
Name:           rng-tools
Version:	5
Release:	3%{?dist}
Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:        GPLv2+
URL:            http://sourceforge.net/projects/gkernel/
Source0:        http://downloads.sourceforge.net/project/gkernel/rng-tools/%{version}/rng-tools-%{version}.tar.gz
Source1:        rngd.service

BuildRequires:  groff gettext
BuildRequires:  systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
Hardware random number generation tools.

%description -l zh_CN.UTF-8
硬件随机数字生成工具。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

# install systemd unit file
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}

magic_rpm_clean.sh

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /usr/bin/systemctl --no-reload disable rngd.service > /dev/null 2>&1 || :
    /usr/bin/systemctl stop rngd.service > /dev/null 2>&1 || :
fi

%postun
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /usr/bin/systemctl try-restart rngd.service >/dev/null 2>&1 || :
fi

%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/rngtest
%{_sbindir}/rngd
%{_mandir}/man1/rngtest.1.*
%{_mandir}/man8/rngd.8.*
%attr(0644,root,root)   %{_unitdir}/rngd.service

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 5-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 5-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 5-1
- 更新到 5

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3-5
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Jiri Popelka <jpopelka@redhat.com> - 3-4
- 2 patches from RHEL-6
- systemd service
- man page fixes
- modernize spec file

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul  3 2010 Jeff Garzik <jgarzik@redhat.com> - 3-2
- comply with renaming guidelines, by Providing rng-utils = 1:2.0-4.2

* Sat Jul  3 2010 Jeff Garzik <jgarzik@redhat.com> - 3-1
- Update to release version 3.

* Fri Mar 26 2010 Jeff Garzik <jgarzik@redhat.com> - 2-3
- more minor updates for package review

* Thu Mar 25 2010 Jeff Garzik <jgarzik@redhat.com> - 2-2
- several minor updates for package review

* Wed Mar 24 2010 Jeff Garzik <jgarzik@redhat.com> - 2-1
- initial revision (as rng-tools)

