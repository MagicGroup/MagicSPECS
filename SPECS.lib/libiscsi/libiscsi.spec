Name: libiscsi
Summary: iSCSI client library
Summary(zh_CN.UTF-8): iSCSI 客户端库
Version: 1.11.0
Release: 3%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: https://github.com/sahlberg/%{name}

Source: https://github.com/downloads/sahlberg/%{name}/%{name}-%{version}.tar.gz
Patch12: 0012-bump-soname.patch
Patch13: 0013-disable-ld_iscsi.patch
Patch20: 0020-reconnect-fix.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: popt-devel
BuildRequires: CUnit-devel
BuildRequires: libgcrypt-devel

%description
libiscsi is a library for attaching to iSCSI resources across
a network.

%description -l zh_CN.UTF-8
iSCSI 客户端库。


#######################################################################

# Conflict with iscsi-initiator-utils.

%global libiscsi_includedir %{_includedir}/iscsi
%global libiscsi_libdir %{_libdir}/iscsi

%prep
%setup -q
%patch12 -p1
%patch13 -p1
%patch20 -p1

%build
sh autogen.sh
%configure --libdir=%{libiscsi_libdir}
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install pkgconfigdir=%{_libdir}/pkgconfig %{?_smp_mflags}
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo %{libiscsi_libdir} > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf
rm $RPM_BUILD_ROOT/%{libiscsi_libdir}/libiscsi.a
rm $RPM_BUILD_ROOT/%{libiscsi_libdir}/libiscsi.la

# Remove "*.old" files
find $RPM_BUILD_ROOT -name "*.old" -exec rm -f {} \;

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING LICENCE-LGPL-2.1.txt README TODO
%{libiscsi_libdir}/libiscsi.so.*
%config /etc/ld.so.conf.d/*

%package utils
Summary: iSCSI Client Utilities
Group: Applications/System
License: GPLv2+
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
The libiscsi-utils package provides a set of assorted utilities to connect
to iSCSI servers without having to set up the Linux iSCSI initiator.

%files utils
%doc COPYING LICENCE-GPL-2.txt LICENCE-LGPL-2.1.txt README TODO
%{_bindir}/iscsi-ls
%{_bindir}/iscsi-inq
%{_bindir}/iscsi-readcapacity16
%{_bindir}/iscsi-swp
#%{_bindir}/iscsi-test-cu
%{_mandir}/man1/iscsi-ls.1.gz
%{_mandir}/man1/iscsi-inq.1.gz
%{_mandir}/man1/iscsi-swp.1.gz
%{_mandir}/man1/iscsi-test-cu.1.gz

%package devel
Summary: iSCSI client development libraries
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The libiscsi-devel package includes the header files for libiscsi.

%files devel
%defattr(-,root,root)
%doc COPYING LICENCE-LGPL-2.1.txt README TODO
%{libiscsi_includedir}/iscsi.h
%{libiscsi_includedir}/scsi-lowlevel.h
%{libiscsi_libdir}/libiscsi.so
%{_libdir}/pkgconfig/libiscsi.pc

%changelog
* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 1.11.0-3
- 为 Magic 3.0 重建

* Sun Jun 22 2014 Liu Di <liudidi@gmail.com> - 1.11.0-2
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Paolo Bonzini <pbonzini@redhat.com> - 1.11.0-1
- Rebased to version 1.11.0
- Most patches removed
- New tool iscsi-swp + manpages

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Tomáš Mráz <tmraz@redhat.com> - 1.9.0-5
- Rebuild for new libgcrypt

* Mon Aug 26 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.9.0-4
- Cleaned up patches 18/19 to match upstream more closely

* Mon Aug 26 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.9.0-3
- Improved patch 18 to cover write side too

* Mon Aug 26 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.9.0-2
- Add patch 18 to fix QEMU's scsi-generic mode

* Fri Aug 2 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.9.0-1
- Rebase to 1.9.0
- Cherry-pick selected patches from upstream

* Mon Jul 1 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-6
- Add patch 5 to silence strict aliasing warnings

* Wed Jun 26 2013 Andy Grover <agrover@redhat.com> - 1.7.0-5
- Add patch 4 to enable installing of iscsi-test binary

* Fri May 3 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-4
- Add patch 2 for FIPS mode
- Add patch 3 to avoid segmentation fault on iscsi-tools

* Thu Mar 7 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-3
- Correct license for libiscsi-utils, prefer %%global to %%define
- Add Requires
- Remove %clean section

* Fri Feb 22 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-2
- Use %config for ld.so.conf.d file.

* Fri Feb 22 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-1
- Initial version (bug 914752)
