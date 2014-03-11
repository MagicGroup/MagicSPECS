%define _root_libdir    %{_libdir}

Summary: Generic Security Services Application Programming Interface Library
Name: libgssglue
Version: 0.3
Release: 2%{?dist}
URL: http://www.citi.umich.edu/projects/nfsv4/linux/
License: GPL+
Source0:http://www.citi.umich.edu/projects/nfsv4/linux/%{name}/%{name}-%{version}.tar.gz
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: krb5-libs >= 1.5

Provides: libgssapi = %{version}-%{release}
Provides: libgssapi-devel = %{version}-%{release}
Obsoletes: libgssapi <= 0.11 libgssapi-devel <= 0.11

Patch0: libgssglue-0.1-gssglue.patch

%description
This library exports a gssapi interface, but doesn't implement any gssapi
mechanisms itself; instead it calls gssapi routines in other libraries,
depending on the mechanism.

%package devel
Summary: Development files for the gssclug library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package includes header files and libraries necessary for
developing programs which use the gssapi library.

%prep
%setup -q
%patch0 -p1

%build
%configure
make %{?_smp_mflags} all 

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}
mkdir -p %{buildroot}%{_root_libdir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
make DESTDIR=%{buildroot} install \
	libdir=%{_root_libdir} pkgconfigdir=%{_libdir}/pkgconfig
install -p -m 644 doc/gssapi_mech.conf %{buildroot}/%{_sysconfdir}/gssapi_mech.conf
rm -f %{buildroot}/%{_root_libdir}/*.{a,la}

magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS README
%{_root_libdir}/libgssglue.so.*
%config(noreplace) %{_sysconfdir}/gssapi_mech.conf

%files devel
%defattr(0644,root,root,755)
%{_root_libdir}/libgssglue.so
%dir %{_includedir}/gssglue
%dir %{_includedir}/gssglue/gssapi
%{_includedir}/gssglue/gssapi/gssapi.h
%{_libdir}/pkgconfig/libgssglue.pc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.3-2
- 为 Magic 3.0 重建

* Wed Apr 18 2012 Liu Di <liudidi@gmail.com> - 0.3-1
- 为 Magic 3.0 重建

* Mon Jun 27 2011 Steve Dickson  <steved@redhat.com> 0.3-0
- Upated to the latest upstream release: 0.3

* Thu Mar 17 2011 Steve Dickson  <steved@redhat.com> 0.2-0
- Upated to the latest upstream release: 0.2
  * Modify the gss_acquire_cred() code to accept, and
    properly handle, an input name of GSS_C_NO_NAME.
    Other misc. changes to support this change.
  * Remove some generated files from git.  Change
    autogen.sh to clean up files that might become

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Steve Dickson  <steved@redhat.com> 0.1-9
- Moved the libraries from /usr/lib to /lib 

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jun 27 2008 Steve Dickson <steved@redhat.com> 0.1-6
- Changed gssapi_mech.conf to use libgssapi_krb5.so.2 
  instead of libgssapi_krb5.so (bz 447503)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1-5
- Autorebuild for GCC 4.3

* Wed Oct 17 2007 Steve Dickson <steved@redhat.com> 0.1-4
- updated Obsoletes: (0.1-3)
- Obsolete -devel package

* Mon Sep 17 2007 Steve Dickson <steved@redhat.com> 0.1-2
- RPM review

* Tue Sep 11 2007 Steve Dickson <steved@redhat.com>
- Initial commit
