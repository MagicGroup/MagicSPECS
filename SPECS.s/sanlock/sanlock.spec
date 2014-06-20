%define with_systemd 0%{!?_without_systemd:0}

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%define with_systemd 1
%endif

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%define with_systemd_macros 1
%else
%define with_systemd_macros 0
%endif

Name:           sanlock
Version:        3.1.0
Release:        2%{?dist}
Summary:        A shared storage lock manager

Group:          System Environment/Base
License:        GPLv2 and GPLv2+ and LGPLv2+
URL:            https://fedorahosted.org/sanlock/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libblkid-devel libaio-devel python python-devel
%if %{with_systemd}
BuildRequires:  systemd-units
%endif
%if 0%{?rhel} >= 6
ExclusiveArch:  x86_64
%endif
Requires:       %{name}-lib = %{version}-%{release}
Requires(pre):  /usr/sbin/groupadd
Requires(pre):  /usr/sbin/useradd
%if %{with_systemd}
Requires(post): systemd-units
Requires(post): systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif
Source0:        http://git.fedorahosted.org/cgit/sanlock.git/snapshot/%{name}-%{version}.tar.gz

#Patch0: foo.patch

%description
The sanlock daemon manages leases for applications running on a cluster
of hosts with shared storage.

%prep
%setup -q
#%patch0 -p1 -b .0001-foo.patch

%build
# upstream does not require configure
# upstream does not support _smp_mflags
CFLAGS=$RPM_OPT_FLAGS make -C wdmd
CFLAGS=$RPM_OPT_FLAGS make -C src
CFLAGS=$RPM_OPT_FLAGS make -C python
CFLAGS=$RPM_OPT_FLAGS make -C fence_sanlock

%install
rm -rf $RPM_BUILD_ROOT
make -C src \
        install LIBDIR=%{_libdir} \
        DESTDIR=$RPM_BUILD_ROOT
make -C wdmd \
        install LIBDIR=%{_libdir} \
        DESTDIR=$RPM_BUILD_ROOT
make -C python \
        install LIBDIR=%{_libdir} \
        DESTDIR=$RPM_BUILD_ROOT
make -C fence_sanlock \
        install LIBDIR=%{_libdir} \
        DESTDIR=$RPM_BUILD_ROOT


%if %{with_systemd}
install -D -m 0755 init.d/sanlock $RPM_BUILD_ROOT/lib/systemd/systemd-sanlock
install -D -m 0644 init.d/sanlock.service $RPM_BUILD_ROOT/%{_unitdir}/sanlock.service
install -D -m 0755 init.d/wdmd $RPM_BUILD_ROOT/lib/systemd/systemd-wdmd
install -D -m 0644 init.d/wdmd.service $RPM_BUILD_ROOT/%{_unitdir}/wdmd.service
install -D -m 0755 init.d/fence_sanlockd $RPM_BUILD_ROOT/lib/systemd/systemd-fence_sanlockd
install -D -m 0644 init.d/fence_sanlockd.service $RPM_BUILD_ROOT/%{_unitdir}/fence_sanlockd.service
%else
install -D -m 0755 init.d/sanlock $RPM_BUILD_ROOT/%{_initddir}/sanlock
install -D -m 0755 init.d/wdmd $RPM_BUILD_ROOT/%{_initddir}/wdmd
install -D -m 0755 init.d/fence_sanlockd $RPM_BUILD_ROOT/%{_initddir}/fence_sanlockd
%endif

install -D -m 0644 src/logrotate.sanlock \
	$RPM_BUILD_ROOT/etc/logrotate.d/sanlock

install -D -m 0644 init.d/sanlock.sysconfig \
	$RPM_BUILD_ROOT/etc/sysconfig/sanlock

install -D -m 0644 init.d/wdmd.sysconfig \
        $RPM_BUILD_ROOT/etc/sysconfig/wdmd

install -Dd -m 0755 $RPM_BUILD_ROOT/etc/wdmd.d
install -Dd -m 0775 $RPM_BUILD_ROOT/%{_localstatedir}/run/sanlock
install -Dd -m 0775 $RPM_BUILD_ROOT/%{_localstatedir}/run/fence_sanlock
install -Dd -m 0775 $RPM_BUILD_ROOT/%{_localstatedir}/run/fence_sanlockd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group sanlock > /dev/null || /usr/sbin/groupadd \
	-g 179 sanlock
getent passwd sanlock > /dev/null || /usr/sbin/useradd \
	-u 179 -c "sanlock" -s /sbin/nologin -r \
	-g 179 -d /var/run/sanlock sanlock
/usr/sbin/usermod -a -G disk sanlock

%post
%if %{with_systemd}
%if %{with_systemd_macros}
%systemd_post wdmd.service sanlock.service
%else
if [ $1 -eq 1 ] ; then
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%endif
%else
if [ $1 -eq 1 ] ; then
  /sbin/chkconfig --add sanlock
  /sbin/chkconfig --add wdmd
fi
%endif

%preun
%if %{with_systemd}
%if %{with_systemd_macros}
%systemd_preun sanlock.service
%systemd_preun wdmd.service
%else
if [ $1 = 0 ]; then
  /bin/systemctl --no-reload disable sanlock.service > /dev/null 2>&1 || :
  /bin/systemctl stop sanlock.service > /dev/null 2>&1 || :
  /bin/systemctl --no-reload disable wdmd.service > /dev/null 2>&1 || :
  /bin/systemctl stop wdmd.service > /dev/null 2>&1 || :
fi
%endif
%else
if [ $1 = 0 ]; then
  /sbin/service sanlock stop > /dev/null 2>&1
  /sbin/chkconfig --del sanlock
  /sbin/service wdmd stop > /dev/null 2>&1
  /sbin/chkconfig --del wdmd
fi
%endif

%postun
%if %{with_systemd}
%if %{with_systemd_macros}
%systemd_postun_with_restart sanlock.service
%systemd_postun_with_restart wdmd.service
%else
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
  /bin/systemctl try-restart sanlock.service >/dev/null 2>&1 || :
  /bin/systemctl try-restart wdmd.service >/dev/null 2>&1 || :
fi
%endif
%else
if [ $1 -ge 1 ] ; then
  /sbin/service sanlock condrestart >/dev/null 2>&1 || :
  /sbin/service wdmd condrestart >/dev/null 2>&1 || :
fi
%endif

%files
%defattr(-,root,root,-)
%if %{with_systemd}
/lib/systemd/systemd-sanlock
/lib/systemd/systemd-wdmd
%{_unitdir}/sanlock.service
%{_unitdir}/wdmd.service
%else
%{_initddir}/sanlock
%{_initddir}/wdmd
%endif
%{_sbindir}/sanlock
%{_sbindir}/wdmd
%dir /etc/wdmd.d
%dir %attr(-,sanlock,sanlock) %{_localstatedir}/run/sanlock
%{_mandir}/man8/wdmd*
%{_mandir}/man8/sanlock*
%config(noreplace) %{_sysconfdir}/logrotate.d/sanlock
%config(noreplace) %{_sysconfdir}/sysconfig/sanlock
%config(noreplace) %{_sysconfdir}/sysconfig/wdmd

%package        lib
Summary:        A shared disk lock manager library
Group:          System Environment/Libraries

%description    lib
The %{name}-lib package contains the runtime libraries for sanlock,
a shared storage lock manager.
Hosts connected to a common SAN can use this to synchronize their
access to the shared disks.

%post lib -p /sbin/ldconfig

%postun lib -p /sbin/ldconfig

%files          lib
%defattr(-,root,root,-)
%{_libdir}/libsanlock.so.*
%{_libdir}/libsanlock_client.so.*
%{_libdir}/libwdmd.so.*

%package        python
Summary:        Python bindings for the sanlock library
Group:          Development/Libraries
Requires:       %{name}-lib = %{version}-%{release}

%description    python
The %{name}-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the sanlock library.

%files          python
%defattr(-,root,root,-)
%{python_sitearch}/Sanlock-1.0-py*.egg-info
%{python_sitearch}/sanlock.so

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-lib = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files          devel
%defattr(-,root,root,-)
%{_libdir}/libwdmd.so
%{_includedir}/wdmd.h
%{_libdir}/libsanlock.so
%{_libdir}/libsanlock_client.so
%{_includedir}/sanlock.h
%{_includedir}/sanlock_rv.h
%{_includedir}/sanlock_admin.h
%{_includedir}/sanlock_resource.h
%{_includedir}/sanlock_direct.h

%package -n     fence-sanlock
Summary:        Fence agent using sanlock and wdmd
Group:          System Environment/Base
Requires:       sanlock = %{version}-%{release}

%description -n fence-sanlock
The fence-sanlock package contains the fence agent and
daemon for using sanlock and wdmd as a cluster fence agent.

%files -n       fence-sanlock
%defattr(-,root,root,-)
%if %{with_systemd}
/lib/systemd/systemd-fence_sanlockd
%{_unitdir}/fence_sanlockd.service
%else
%{_initddir}/fence_sanlockd
%endif
%{_sbindir}/fence_sanlock
%{_sbindir}/fence_sanlockd
%dir %attr(-,root,root) %{_localstatedir}/run/fence_sanlock
%dir %attr(-,root,root) %{_localstatedir}/run/fence_sanlockd
%{_mandir}/man8/fence_sanlock*

%post -n        fence-sanlock
if [ $1 -eq 1 ] ; then
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
  /sbin/chkconfig --add fence_sanlockd
%endif
ccs_update_schema > /dev/null 2>&1 ||:
fi

%preun -n       fence-sanlock
if [ $1 = 0 ]; then
%if %{with_systemd}
  /bin/systemctl --no-reload fence_sanlockd.service > /dev/null 2>&1 || :
%else
  /sbin/service fence_sanlockd stop > /dev/null 2>&1
  /sbin/chkconfig --del fence_sanlockd
%endif
fi

%postun -n      fence-sanlock
if [ $1 -ge 1 ] ; then
%if %{with_systemd}
  /bin/systemctl try-restart fence_sanlockd.service > /dev/null 2>&1 || :
%else 
  /sbin/service fence_sanlockd condrestart >/dev/null 2>&1 || :
%endif
fi

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 15 2014 David Teigland <teigland@redhat.com> - 3.1.0-1
- Update to sanlock-3.1.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 David Teigland <teigland@redhat.com> - 3.0.0-1
- Update to sanlock-3.0.0

