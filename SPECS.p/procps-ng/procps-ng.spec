# The testsuite is unsuitable for running on buildsystems
%global tests_enabled 0

Summary: System and process monitoring utilities
Name: procps-ng
Version: 3.3.9
Release: 5%{?dist}
License: GPL+ and GPLv2 and GPLv2+ and GPLv3+ and LGPLv2+
Group: Applications/System
URL: https://sourceforge.net/projects/procps-ng/

Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz

Patch0: vmstat-wide-not-wide-enough.patch
Patch1: ksh-skip-trailing-zeros.patch
Patch2: vmstat-timestamps.patch
Patch3: watch-fd-leak.patch
Patch4: vmstat-format-security.patch

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Requires: systemd-libs

BuildRequires: ncurses-devel
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gettext-devel
BuildRequires: systemd-devel

%if %{tests_enabled}
BuildRequires: dejagnu
%endif

Provides: procps = %{version}-%{release}
Obsoletes: procps < 3.2.9-1

# usrmove hack - will be removed once initscripts are fixed
Provides: /sbin/sysctl
Provides: /bin/ps

# sysvinit removal in Fedora 21
Obsoletes: sysvinit-tools < 0:2.89
Provides: /sbin/pidof


%description
The procps package contains a set of system utilities that provide
system information. Procps includes ps, free, skill, pkill, pgrep,
snice, tload, top, uptime, vmstat, w, watch and pwdx. The ps command
displays a snapshot of running processes. The top command provides
a repetitive update of the statuses of running processes. The free
command displays the amounts of free and used memory on your
system. The skill command sends a terminate command (or another
specified signal) to a specified set of processes. The snice
command is used to change the scheduling priority of specified
processes. The tload command prints a graph of the current system
load average to a specified tty. The uptime command displays the
current time, how long the system has been running, how many users
are logged on, and system load averages for the past one, five,
and fifteen minutes. The w command displays a list of the users
who are currently logged on and what they are running. The watch
program watches a running program. The vmstat command displays
virtual memory statistics about processes, memory, paging, block
I/O, traps, and CPU activity. The pwdx command reports the current
working directory of a process or processes.

%package devel
Summary:  System and process monitoring utilities
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: procps-devel = %{version}-%{release}
Obsoletes: procps-devel < 3.2.9-1

%description devel
System and process monitoring utilities development headers

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1


%build
# The following stuff is needed for git archives only
#echo "%{version}" > .tarball-version
#./autogen.sh

autoreconf --verbose --force --install

./configure --prefix=/ \
            --bindir=%{_bindir} \
            --sbindir=%{_sbindir} \
            --libdir=%{_libdir} \
            --mandir=%{_mandir} \
            --includedir=%{_includedir} \
            --sysconfdir=%{_sysconfdir} \
            --docdir=/unwanted \
            --disable-static \
            --disable-w-from \
            --disable-kill \
            --disable-rpath \
            --enable-watch8bit \
            --enable-skill \
            --enable-sigwinch \
            --enable-libselinux \
            --with-systemd

make CFLAGS="%{optflags}"


%if %{tests_enabled}
%check
make check
%endif


%install
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{_sysconfdir}/sysctl.d

ln -s %{_bindir}/pidof %{buildroot}%{_sbindir}/pidof

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS Documentation/BUGS COPYING COPYING.LIB Documentation/FAQ NEWS README top/README.top Documentation/TODO

%{_libdir}/libprocps.so.*
%{_bindir}/*
%{_sbindir}/*
%{_sysconfdir}/sysctl.d
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_mandir}/man5/*

%exclude %{_libdir}/libprocps.la
%exclude %{_sysconfdir}/sysctl.conf
%exclude /unwanted/*

%files devel
%doc COPYING COPYING.LIB
%{_libdir}/libprocps.so
%{_libdir}/pkgconfig/libprocps.pc
%{_includedir}/proc

%changelog
* Wed Feb 05 2014 Jaromir Capik <jcapik@redhat.com> - 3.3.9-5
- Support for timestamps & wide diskstat (#1053428, #1025833)
- Fixing fd leak in watch
- Fixing format-security build issues

* Fri Jan 24 2014 Jaromir Capik <jcapik@redhat.com> - 3.3.9-4
- Skipping trailing zeros in read_unvectored (#1057600)

* Mon Jan 20 2014 Jaromir Capik <jcapik@redhat.com> - 3.3.9-3
- 'vmstat -w' was not wide enough (#1025833)

* Tue Jan 07 2014 Jaromir Capik <jcapik@redhat.com> - 3.3.9-2
- Replacing the /sbin/pidof wrapper with symlink

* Tue Dec 03 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.9-1
- Update to 3.3.9

* Mon Nov 04 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-17
- Fixing pidof compilation warnings
- RPM workaround - changing sysvinit-tools Conflicts/Obsoletes (#1026504)

* Wed Oct 16 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-16
- Introducing pidof (#987064)

* Tue Sep 17 2013 Aristeu Rozanski <aris@redhat.com> - 3.3.8-15
- Introduce namespaces support (#1016242)

* Tue Sep 17 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-14
- top: Fixing missing newline when running in the batch mode (#1008674)

* Fri Aug 09 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-13
- Including forgotten man fixes (#948522)

* Wed Aug 07 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-12
- Fixing the license tag

* Wed Aug 07 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-11
- Support for libselinux (#975459)
- Support for systemd (#994457)
- Support for 'Shmem' in free (#993271)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-9
- RH man page scan (#948522)

* Tue Jul 02 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-8
- Extending the end-of-job patch disabling the screen content restoration

* Mon Jul 01 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-7
- Disabling screen content restoration when exiting 'top' (#977561)
- Enabling SIGWINCH flood prevention

* Wed Jun 26 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-6
- Avoiding "write error" messages when piping to grep (#976199)

* Wed Jun 26 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-5
- Disabling tests - unsuitable for running on buildsystems

* Mon Jun 17 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-4
- Enabling skill and snice (#974752)

* Wed Jun 12 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-3
- Adding major version in the libnuma soname

* Thu May 30 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-2
- watch: enabling UTF-8 (#965867)

* Wed May 29 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-1
- Update to 3.3.8

* Wed May 22 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.7-4
- top: inoculated against a window manager like 'screen' (#962022)

* Tue Apr 16 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.7-3
- Avoid segfaults when reading zero bytes - file2str (#951391)

* Mon Apr 15 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.7-2
- Moving libprocps.pc to the devel subpackage (#951726)

* Tue Mar 26 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.7-1
- Update to 3.3.7
- Reverting upstream commit for testsuite/unix.exp

* Tue Feb 05 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.6-4
- Fixing empty pmap output on ppc/s390 (#906457)

* Tue Jan 15 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.6-3
- Typo in the description, pdwx instead of pwdx (#891476)

* Tue Jan 08 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.6-2
- Rebuilding with tests disabled (koji issue #853084)

* Tue Jan 08 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.6-1
- Update to 3.3.6
- Changing URL/Source from gitorious to recently created sourceforge page
- Replacing autogen.sh with autoreconf

* Mon Jan 07 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Tue Dec 11 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.4-2
- fixing the following regressions:
-   negative ETIME field in ps (#871819)
-   procps states a bug is hit when receiving a signal (#871824)
-   allow core file generation by ps command (#871825)

* Tue Dec 11 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Tue Sep 25 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.3-3.20120807git
- SELinux spelling fixes (#859900)

* Tue Aug 21 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.3-2.20120807git
- Tests enabled

* Tue Aug 07 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.3-1.20120807git
- Update to 3.3.3-20120807git

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 08 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.2-3
- Second usrmove hack - providing /bin/ps

* Tue Mar 06 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.2-2
- Fixing requires in the devel subpackage (missing %{?_isa} macro)
- License statement clarification (upstream patch referrenced in the spec header)

* Mon Feb 27 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.2-1
- Initial version
