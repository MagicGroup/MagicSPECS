# hardened build if not overrided
%{!?_hardened_build:%global _hardened_build 1}

%if %{?_hardened_build:%{_hardened_build}}%{!?_hardened_build:0}
%global harden -pie -Wl,-z,relro,-z,now
%endif

Summary: ACPI Event Daemon
Summary(zh_CN.UTF-8): ACPI 事件服务
Name: acpid
Version: 2.0.25
Release: 3%{?dist}
License: GPLv2+
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
Source: http://downloads.sourceforge.net/acpid2/%{name}-%{version}.tar.xz
Source2: acpid.video.conf
Source3: acpid.power.conf
Source4: acpid.power.sh
Source5: acpid.service
Source6: acpid.sysconfig
Source7: acpid.socket
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch: ia64 x86_64 %{ix86} mips64el
URL: http://sourceforge.net/projects/acpid2/
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: systemd


%description
acpid is a daemon that dispatches ACPI events to user-space programs.

%description -l zh_CN.UTF-8
acpid 是一调度 ACPI 事件到用户空间的服务。

%prep
%setup -q


%build
%configure
make %{?_smp_mflags} CFLAGS="%{optflags} %{?harden}"


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
make install DESTDIR=%{buildroot} docdir=%{_docdir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/acpi/events
mkdir -p %{buildroot}%{_sysconfdir}/acpi/actions
mkdir -p %{buildroot}/lib/systemd/system
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig

chmod 755 %{buildroot}%{_sysconfdir}/acpi/events
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/acpi/events/videoconf
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/acpi/events/powerconf
install -m 755 %{SOURCE4} %{buildroot}%{_sysconfdir}/acpi/actions/power.sh
install -m 644 %{SOURCE5} %{SOURCE7} %{buildroot}/lib/systemd/system
install -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/acpid

magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}
/lib/systemd/system/%{name}.service
/lib/systemd/system/%{name}.socket
%dir %{_sysconfdir}/acpi
%dir %{_sysconfdir}/acpi/events
%dir %{_sysconfdir}/acpi/actions
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/acpi/events/videoconf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/acpi/events/powerconf
%config(noreplace) %attr(0755,root,root) %{_sysconfdir}/acpi/actions/power.sh
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/acpid
%{_bindir}/acpi_listen
%{_sbindir}/acpid
%{_sbindir}/kacpimon
%{_mandir}/man8/acpid.8.gz
%{_mandir}/man8/acpi_listen.8.gz
%{_mandir}/man8/kacpimon.8.gz

%pre
if [ "$1" = "2" ]; then
	conflist=`ls %{_sysconfdir}/acpi/events/*.conf 2> /dev/null`
	RETCODE=$?
	if [ $RETCODE -eq 0 ]; then
		for i in $conflist; do
			rmdot=`echo $i | sed 's/.conf/conf/'`
			mv $i $rmdot
		done
	fi
fi

%post
%systemd_post %{name}.socket %{name}.service

%preun
%systemd_preun %{name}.socket %{name}.service

%postun
%systemd_postun_with_restart %{name}.socket %{name}.service

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 2.0.25-3
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 2.0.25-2
- 更新到 2.0.25

* Thu Feb 27 2014 Liu Di <liudidi@gmail.com> - 2.0.21-1
- 升级到 2.0.21
- 去掉 sysvinit 包
