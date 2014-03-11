Name:           fuse
Version:        2.9.2
Release:        2%{?dist}
Summary:        File System in Userspace (FUSE) utilities

Group:          System Environment/Base
License:        GPL+
URL:            http://fuse.sf.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.conf

Patch1:		fuse-0001-More-parentheses.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       kernel >= 2.6.14
Requires:       which
Conflicts:      filesystem < 3

Requires(preun): chkconfig
Requires(preun): initscripts

%description
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE userspace tools to
mount a FUSE filesystem.

%package libs
Summary:        File System in Userspace (FUSE) libraries
Group:          System Environment/Libraries
License:        LGPLv2+
Conflicts:      filesystem < 3

%description libs
Devel With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE libraries.


%package devel
Summary:        File System in Userspace (FUSE) devel files
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig
License:        LGPLv2+
Conflicts:      filesystem < 3

%description devel
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains development files (headers,
pgk-config) to develop FUSE based applications/filesystems.


%prep
%setup -q
#disable device creation during build/install
sed -i 's|mknod|echo Disabled: mknod |g' util/Makefile.in
%patch1 -p1 -b .add_parentheses

%build
# Can't pass --disable-static here, or else the utils don't build
export MOUNT_FUSE_PATH="%{_sbindir}"
CFLAGS="%{optflags} -D_GNU_SOURCE" %configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
# change from 4755 to 0755 to allow stripping -- fixed later in files
chmod 0755 $RPM_BUILD_ROOT/%{_bindir}/fusermount

# Get rid of static libs
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a
# No need to create init-script
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/init.d/fuse

# Install config-file
install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}

# Delete pointless udev rules, which do not belong in /etc (brc#748204)
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/99-fuse.rules

%clean
rm -rf $RPM_BUILD_ROOT


%preun
if [ -f /etc/init.d/fuse ] ; then
    /sbin/service fuse stop >/dev/null 2>&1
    /sbin/chkconfig --del fuse
fi


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ Filesystems NEWS README README.NFS
%{_sbindir}/mount.fuse
%attr(4755,root,root) %{_bindir}/fusermount
%{_bindir}/ulockmgr_server
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_mandir}/man1/*
%{_mandir}/man8/*

%files libs
%defattr(-,root,root,-)
%doc COPYING.LIB
%{_libdir}/libfuse.so.*
%{_libdir}/libulockmgr.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libfuse.so
%{_libdir}/libulockmgr.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fuse.h
%{_includedir}/ulockmgr.h
%{_includedir}/fuse

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 2.9.2-2
- 为 Magic 3.0 重建


