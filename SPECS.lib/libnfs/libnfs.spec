%global SERVICE_NUMBER 1330914571  

Name: libnfs
Summary: NFS client library
Version: 1.3
Release: 2%{?dist}
License: GNU LGPL version 2.1
Group: Development/Libraries/C and C++
URL: http://www.github.com/sahlberg/libnfs
Source0: %{name}-%{SERVICE_NUMBER}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-build
BuildRequires: automake pkgconfig libtool

%description
LibNFS is a NFS client library

%package devel
Summary: Development libraries for LibNFS
Group: Development/Libraries/C and C++
Requires: libnfs

%description devel
Development libraries for LibNFS

%prep
%setup -n libnfs-%{SERVICE_NUMBER} -q

%build
## check for ccache
if ccache -h >/dev/null 2>&1 ; then
        CC="ccache gcc"
else
        CC="gcc"
fi
export CC

./bootstrap

CFLAGS="$RPM_OPT_FLAGS $EXTRA -O0 -g -D_GNU_SOURCE" ./configure \
        --prefix=%{_prefix} \
        --libdir=%{_libdir}


%install
# Clean up in case there is trash left from a previous build
rm -rf $RPM_BUILD_ROOT

# Create the target build directory hierarchy
make DESTDIR=$RPM_BUILD_ROOT install

# Remove "*.old" files
find $RPM_BUILD_ROOT -name "*.old" -exec rm -f {} \;
%{__rm} %{buildroot}/%{_libdir}/libnfs.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{name} -p /sbin/ldconfig
%postun -n %{name} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/%{name}.so.*


%files devel
%defattr(-,root,root)
%dir %{_includedir}/nfsc
%{_includedir}/nfsc/libnfs.h
%{_includedir}/nfsc/libnfs-raw.h
%{_includedir}/nfsc/libnfs-raw-mount.h
%{_includedir}/nfsc/libnfs-raw-nfs.h
%{_includedir}/nfsc/libnfs-raw-portmap.h
%{_includedir}/nfsc/libnfs-raw-rquota.h
%{_libdir}/libnfs.a
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/libnfs.pc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.3-2
- 为 Magic 3.0 重建

* Sat Mar 3 2012 : Version 1.3
 - add set/unset to portmapper
 - add mount v1
 - try to rotate to find a free port better
 - minor fixes
* Tue Dec 6 2011 : Version 1.2
 - Add support for MKNOD
 - Add support for HaneWin NFS server
 - Change all [s]size_t offset_t to be 64bit clean scalars
* Sun Nov 27 2011 : Version 1.1
 - Fix definition and use of AUTH
 - Only call the "connect" callback if non-NULL
 - make sure the callback for connect is only invoked once for the sync api
 - make file offset bits 64 bits always
* Sun Jul 31 2011 : Version 1.0
 - Initial version

