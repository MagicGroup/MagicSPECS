Name:           iguanaIR
Version:        1.1.0
Release:        15%{?dist}
Epoch:          2
Summary:        Driver for Iguanaworks USB IR transceiver

Group:          System Environment/Daemons
License:        GPLv2 and LGPLv2
URL:            http://iguanaworks.net/ir
Source0:        http://iguanaworks.net/downloads/%{name}-%{version}.tar.bz2
Source1:        iguanaIR.service
Source2:        iguanaIR-rescan
Source3:        README.fedora
Source4:        patch-soname
Source5:        iguanaIR.logrotate
# https://iguanaworks.net/projects/IguanaIR/ticket/317
Patch1:         changeset_2710.patch
Patch2:         rpath.patch
Patch3:         cmake-args.patch

Requires:       udev

BuildRequires:  cmake
BuildRequires:  libusb1-devel, libusb-devel
BuildRequires:  popt-devel
BuildRequires:  systemd-units
                # For patch-soname (xxd, util-linux)
Buildrequires:  /usr/bin/xxd
BuildRequires:  util-linux

Requires(post): systemd-units, systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units

# resolve cyclic dep iguanaIR <-> lirc. Once removed
# in lirc, we can do the required so-bump.
%ifarch x86_64
Provides:       libiguanaIR.so.0()(64bit)
Provides:       libiguanaIR.so.0(IGUANAIR_0)(64bit)
%else
Provides:       libiguanaIR.so.0
Provides:       libiguanaIR.so.0(IGUANAIR_0)
%endif


# some features can be disabled during the rpm build
%{?_without_clock_gettime: %define _disable_clock_gettime --disable-clock_gettime}

# Don't add provides for python .so files
%define __provides_exclude_from %{python_sitearch}/.*\.so$

# Filter away patched soname form requires
%global __requires_exclude                     libiguanaIR.so.0.3

%description
This package provides igdaemon and igclient, the programs necessary to
control the Iguanaworks USB IR transceiver.

%package devel
Summary: Library and header files for iguanaIR
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
The development files needed to interact with the iguanaIR igdaemon are
included in this package.

%package python
Group: System Environment/Daemons
Summary: Python module for Iguanaworks USB IR transceiver
Requires: %{name} = %{epoch}:%{version}-%{release}, python >= 2.4
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
%patch1 -p3
%patch2 -p1
%patch3 -p1
cp %{SOURCE3} README.fedora
cp %{SOURCE4} .


%build
./runCmake -DLIBDIR="%{_libdir}"
cd build
make CFLAGS="%{optflags} -fpic -DFEDORA=1" %{?_smp_mflags}
cp %{SOURCE4} .



%install
cd build
make install PREFIX=$RPM_BUILD_ROOT/usr DESTDIR=$RPM_BUILD_ROOT INLIBDIR=$RPM_BUILD_ROOT%{_libdir}

install -m755 -d $RPM_BUILD_ROOT%{_localstatedir}/run/%{name}

# For now, patch bad soname introduced when they switched to cmake...
bash -c "./patch-soname $RPM_BUILD_ROOT%{_libdir}/libiguanaIR.so.0.3 \
         libiguanaIR.so.0.3 IGUANAIR_0"

# fix missing links
pushd  $RPM_BUILD_ROOT%{_libdir}
ln -sf libiguanaIR.so.0.3 libiguanaIR.so.0

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
install -m 755 -d $RPM_BUILD_ROOT/run/%{name}
install -m 644 -D %{SOURCE5} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}



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
%doc AUTHORS LICENSE LICENSE-LGPL
%doc README.txt WHY ChangeLog
%doc README.fedora
%{_bindir}/igdaemon
%{_bindir}/igclient
%{_bindir}/iguanaIR-rescan
%{_libdir}/lib%{name}.so.*
%{_libdir}/%{name}/*.so
%{_libexecdir}/%{name}/
%{_unitdir}/%{name}.service
/etc/logrotate.d/%{name}
/lib/udev/rules.d/80-%{name}.rules
%config(noreplace) /etc/sysconfig/%{name}
%config(noreplace) /etc/tmpfiles.d/%{name}.conf
%ghost %attr(755, iguanair, iguanair) /run/%{name}
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
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec 22 2014  Alec Leamas <leamas.alec@gmail.com> - 2:1.1.0-14
- Fixing #1176627: Update logrotate conf.

* Thu Dec 11 2014 Alec Leamas <leamas.alec@gmail.com> - 2:1.1.0-13
- Filter away bogus, patched so-name from Requires:

* Wed Dec 10 2014 Alec Leamas <leamas.alec@gmail.com> - 2:1.1.0-12
- Fixes #1159618.
- Re-install logrotate file, mysteriously dropped sometime.

* Wed Sep 10 2014  Alec Leamas <leamas.alec@nowhere.net> - 2:1.1.0-11
- Fixed 64-bit provides tweak.

* Tue Sep 09 2014  Alec Leamas <leamas.alec@nowhere.net> - 2:1.1.0-10
- Added 64-bit provides tweak.

* Wed Sep 03 2014 Alec Leamas <leamas.alec@nowhere.net> - 2:1.1.0-9
- Remove needless and circular dependency on lirc.

* Wed Sep 03 2014 Alec Leamas <leamas.alec@nowhere.net> - 2:1.1.0-8
- patch soname + add virtual compatibility Provides:

* Wed Sep 3 2014 Alec Leamas <leamas.alec@nowhere.net - 2:1.1.0-7
- Patch soname on rawhide to avoid unintended bump.

* Tue Sep 2 2014 Alec Leamas <leamas.alec@nowhere.net - 2:1.1.0-6
- Make a new try to sort out deps for 1.1.0

* Wed Aug 27 2014 Alec Leamas <leamas.alec@nowhere.net - 2:1.0.5-7
- Have to re-add sources as well.

* Wed Aug 27 2014 Alec Leamas <leamas.alec@nowhere.net - 2:1.0.5-6
- Backing out 1.1.0 again, broken dependencies problem

* Thu Aug 21 2014 Alec Leamas <leamas.alec@nowhere.net - 1:1.1.0-5
- Fixing typo, bad %%{epoch} requires:

* Thu Aug 21 2014 Alec Leamas <leamas.alec@nowhere.net> - 1:1.1.0-4
- New attempt to introduce 1.1.0 (ABI bump)

* Wed Aug 20 2014 Alec Leamas <leamas.alec@nowhere.net> - 1:1.0.5-5
- Updating dependencies with epoch (sigh...).

* Tue Aug 19 2014 Alec Leamas <leamas.alec@nowhere.net> - 1:1.0.5-4
- Backing out 1.1.0 due to ABI problems.
- Purged old changelog dating to 2006, partly outside Fedora.

* Mon Aug 18 2014 Alec Leamas <leamas.alec@gmail.com> - 1.1.0-3
- Add missing patch (how did this ever build?).

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 11 2014 Alec Leamas <leamas.alec@gmail.com> - 1.1.0-1
- Updating to latest version
- Old patches now upstreamed, new patches for cmake required. LIBDIR handling
  needs cleanup (not required part in rpath.patch).

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
