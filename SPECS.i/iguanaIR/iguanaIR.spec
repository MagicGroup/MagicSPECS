Name:           iguanaIR
Version:        1.0.5
Release:        5%{?dist}
Summary:        Driver for Iguanaworks USB IR transceiver

Group:          System Environment/Daemons
License:        GPLv2 and LGPLv2
URL:            http://iguanaworks.net/ir
Source0:        http://iguanaworks.net/downloads/%{name}-%{version}.tar.bz2
Source1:        iguanaIR.service
Source2:        iguanaIR-rescan
Source3:        README.fedora
# https://iguanaworks.net/projects/IguanaIR/ticket/205 for patch 5, 3, 2.
Patch3:         0003-Use-platform-specific-python-extension-dir.patch
# Fedora only
Patch6:         0006-udev-invoke-systemd-support-not-sysV-init-file.patch

Requires:       lirc, udev
BuildRequires:  popt-devel, libusb1-devel, libusb-devel, systemd-units
Requires(post): systemd-units, systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units


# some features can be disabled during the rpm build
%{?_without_clock_gettime: %define _disable_clock_gettime --disable-clock_gettime}

# Don't add provides for python .so files
%define __provides_exclude_from %{python_sitearch}/.*\.so$

%description
This package provides igdaemon and igclient, the programs necessary to
control the Iguanaworks USB IR transceiver.

%package devel
Summary: Library and header files for iguanaIR
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The development files needed to interact with the iguanaIR igdaemon are
included in this package.

%package python
Group: System Environment/Daemons
Summary: Python module for Iguanaworks USB IR transceiver
Requires: %{name} = %{version}-%{release}, python >= 2.4
BuildRequires: python-devel swig

%description python
This package provides the swig-generated Python module for interfacing
with the Iguanaworks USB IR transceiver.

%package reflasher
Group: System Environment/Daemons
Summary: Reflasher for Iguanaworks USB IR transceiver
BuildArch: noarch

%description reflasher
This package provides the reflasher/testing script and assorted firmware
versions for the Iguanaworks USB IR transceiver.  If you have no idea
what this means, you don't need it.


%prep
%setup -q -n %{name}-%{version}
%patch3 -p1
%patch6 -p1
cp %{SOURCE3} README.fedora


%build
%configure %{?_disable_clock_gettime}
make CFLAGS="%{optflags} -fpic -DFEDORA=1" %{?_smp_mflags}


%install
make install PREFIX=$RPM_BUILD_ROOT/usr DESTDIR=$RPM_BUILD_ROOT INLIBDIR=$RPM_BUILD_ROOT%{_libdir}

install -m755 -d $RPM_BUILD_ROOT%{_localstatedir}/run/%{name}

# Use /etc/sysconfig instead of /etc/default
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig || :
mv  $RPM_BUILD_ROOT/etc/default/iguanaIR \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig

# Fix up some stray file permissions issues
chmod -x $RPM_BUILD_ROOT%{python_sitearch}/*.py \
         $RPM_BUILD_ROOT%{_includedir}/%{name}.h \
         $RPM_BUILD_ROOT%{_datadir}/%{name}-reflasher/hex/*

# Remove the installed initfile and install the systemd support instead.
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/init.d/
install -m644 -D %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
install -m755 -D %{SOURCE2} $RPM_BUILD_ROOT%{_libexecdir}/iguanaIR/rescan

# Install private log dir, tmpfiles.d setup.
install -m755 -d $RPM_BUILD_ROOT%{_localstatedir}/log/iguanaIR

install -m755 -d $RPM_BUILD_ROOT/etc/tmpfiles.d
cat > $RPM_BUILD_ROOT/etc/tmpfiles.d/%{name}.conf <<EOF
d   /run/%{name}    0755    iguanair   iguanair
EOF
install -m755 -d $RPM_BUILD_ROOT/run/%{name}


%pre
getent group iguanair >/dev/null || groupadd -r iguanair
getent passwd iguanair >/dev/null || \
    useradd -r -g iguanair -d %{_localstatedir}/run/%{name} -s /sbin/nologin \
    -c "Iguanaworks IR Daemon" iguanair
exit 0

%post
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
/sbin/ldconfig

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable %{name}.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi
/sbin/ldconfig


%files
%doc AUTHORS LICENSE LICENSE-LGPL WHY protocols.txt
%doc README.txt notes.txt ChangeLog
%doc README.fedora
%{_bindir}/igdaemon
%{_bindir}/igclient
%{_libdir}/lib%{name}.so.*
%{_libdir}/%{name}/*.so
%{_libexecdir}/%{name}/
%{_unitdir}/%{name}.service
/lib/udev/rules.d/80-%{name}.rules
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%attr(755, iguanair, iguanair) /run/%{name}
%attr(775, iguanair, iguanair) %{_localstatedir}/log/%{name}

%files devel
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so

%files python
%{python_sitearch}/*

%files reflasher
%{_datadir}/%{name}-reflasher/
%{_bindir}/%{name}-reflasher

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.0.5-5
- 为 Magic 3.0 重建

* Tue Jul 01 2014 Liu Di <liudidi@gmail.com> - 1.0.5-4
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Apr 21 2013 Alec Leamas <leamas.alec@gmail.com> - 1.0.5-1
- Update to latest upstream 1.0.5
- Most patches merged upstream.

* Tue Dec 25 2012 Alec Leamas <leamas.alec@gmail.com> - 1.0.3-1
- Updated to 1.0.3
- Moved most of fixes.patch to spec file, split rest to smaller ones.
- Support sysconfig configuration file.
- Include documentation files
- Install udev rule in /lib/udev, not /etc/udev.
- Fixed udev issue invoking '/etc/init.d/iguanaIR rescan'.

* Wed Apr 18 2012 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.0.1-3
- Some systemd and dependency filtering suggestions.

* Fri Jan 28 2011 Jarod Wilson <jarod@redhat.com> 1.0.1-2
- Address Fedora package review concerns (#642773)

* Thu Jan 20 2011 Jarod Wilson <jarod@redhat.com> 1.0.1-1
- Update to 1.0.1 release

* Wed Oct 13 2010 Jarod Wilson <jarod@redhat.com> 1.0-0.2.pre2.svn1419
- Update to 1.0pre2 snapshot plus svn rev 1419 additions
- Patch in additional changes to use more suitable locations for
  plugins, socket directory and reflasher files

* Wed Jul 21 2010 Jarod Wilson <jarod@redhat.com> 1.0-0.1.pre2
- Update to 1.0pre2 snapshot
- Revamp spec to be more compliant with Fedora packaging guidelines

* Sat Jun 27 2008 Joseph Dunn <jdunn@iguanaworks.net> 0.96-1
- Bug fix release.

* Fri Mar 27 2008 Joseph Dunn <jdunn@iguanaworks.net> 0.95-1
- Decided to do another release to fix a udev problem.

* Sun Mar 23 2008 Joseph Dunn <jdunn@iguanaworks.net> 0.94-1
- Better windows support, a pile of bugs fixed.  Works with newer
  firmwares (version 0x102) including frequency and channel support
  with or without LIRC.

* Sat Mar 10 2007 Joseph Dunn <jdunn@iguanaworks.net> 0.31-1
- First release with tentative win32 and darwin support.  Darwin needs
  some work, and windows needs to interface with applications.

* Thu Feb 1 2007 Joseph Dunn <jdunn@iguanaworks.net> 0.30-1
- Added a utility to change the frequency on firmware version 3, and
  had to make iguanaRemoveData accessible to python code.

* Sun Jan 21 2007 Joseph Dunn <jdunn@iguanaworks.net> 0.29-1
- Last currently known problem in the driver.  Using clock_gettime
  instead of gettimeofday to avoid clock rollbacks.

* Sun Dec 31 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.26-1
- Happy New Years! and a bugfix.  Long standing bug that caused the
  igdaemon to hang is fixed.

* Sun Dec 10 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.25-1
- The socket specification accept a path instead of just an index or
  label.

* Wed Dec 6 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.24-1
- Fixes bad argument parsing in igdaemon, and the init script *should*
  work for fedora and debian now.

* Wed Oct 18 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.19-1
- A real release has been made, and we'll try to keep track of version
  numbers a bit better now.

* Sat Sep 23 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.10-1
- Preparing for a real release.

* Wed Jul 11 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.9-1
- Switch to using udev instead of hotplug.

* Mon Jul 10 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.8-1
- Version number bumps, and added python support and package.

* Mon Mar 27 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.5-1
- Version number bump.

* Mon Mar 20 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.4-1
- Version number bump.

* Tue Mar 07 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.3-1
- Packaged a client library, and header file.

* Tue Mar 07 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.2-2
- Added support for chkconfig

* Tue Mar 07 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.2-1
- Added files for hotplug.

* Tue Mar 07 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.1-1
- Initial RPM spec file.
