Name:           userspace-rcu
Version:        0.8.6
Release:        2%{?dist}
Summary:        RCU (read-copy-update) implementation in user space

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://lttng.org/urcu/
Source0:        http://lttng.org/files/urcu/%{name}-%{version}.tar.bz2
Patch0:         userspace-rcu-aarch64.patch
BuildRequires:  autoconf automake libtool
BuildRequires:  pkgconfig 
# Upstream do not yet support mips
ExcludeArch:    mips

%description
This data synchronization library provides read-side access which scales
linearly with the number of cores. It does so by allowing multiples copies
of a given data structure to live at the same time, and by monitoring
the data structure accesses to detect grace periods after which memory
reclamation is possible.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1


%build
# Patch for AArch64 and PPC64LE needs it
autoreconf -vif
%configure --disable-static
#Remove Rpath from build system
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

V=1 make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -vf $RPM_BUILD_ROOT%{_libdir}/*.la


%check
#TODO greenscientist: make check currently fail in mockbuild
#make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc LICENSE gpl-2.0.txt lgpl-relicensing.txt lgpl-2.1.txt
%{_docdir}/%{name}/README
%{_docdir}/%{name}/ChangeLog
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/liburcu*.pc
%{_docdir}/%{name}/README
%{_docdir}/%{name}/*.txt


%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 26 2015 Scott Tsai <scottt.tw@gmail.com> - 0.8.6-1
- New upstream release

* Sun Nov 02 2014 Suchakra Sharma <suchakra@fedoraproject.org> - 0.8.5-1
- New upstream release

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.8.1-3
- Use upstream patch for aarch64 (includes ppc64le too)

* Thu May 22 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.8.1-2
- Added AArch64 support

* Mon Feb 10 2014 Yannick Brosseau <yannick.brosseau@gmail.com> 0.8.1-1
- New upstream release

* Sat Jan 18 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.9-1
- Update to 0.7.9

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 05 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.7-1
- New upstream version

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.6-1
- New upstream version

* Tue Oct 23 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.5-1
- New upstream version 

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.3-1
- New upstream version (#828716)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 26 2010 Jan "Yenya" Kasprzak <kas@fi.muni.cz> 0.4.1-1
- new upstream version.

* Tue Oct 20 2009 Jan "Yenya" Kasprzak <kas@fi.muni.cz> 0.2.4-1
- Initial revision.
