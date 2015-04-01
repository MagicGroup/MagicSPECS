%bcond_with bundled_libpfm
Summary: Performance Application Programming Interface
Name: papi
Version: 5.4.1
Release: 2%{?dist}
License: BSD
Group: Development/System
Requires: papi-libs = %{version}-%{release}
URL: http://icl.cs.utk.edu/papi/
Source0: http://icl.cs.utk.edu/projects/papi/downloads/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: autoconf
BuildRequires: doxygen
BuildRequires: ncurses-devel
BuildRequires: gcc-gfortran
BuildRequires: kernel-headers >= 2.6.32
BuildRequires: chrpath
BuildRequires: lm_sensors-devel
%if %{without bundled_libpfm}
BuildRequires: libpfm-devel >= 4.6.0-1
BuildRequires: libpfm-static >= 4.6.0-1
%endif
# Following required for net component
BuildRequires: net-tools
# Following required for inifiband component
BuildRequires: libibmad-devel
#Right now libpfm does not know anything about s390 and will fail
ExcludeArch: s390 s390x

%description
PAPI provides a programmer interface to monitor the performance of
running programs.

%package libs
Summary: Libraries for PAPI clients
Group: Development/System
%description libs
This package contains the run-time libraries for any application that wishes
to use PAPI.

%package devel
Summary: Header files for the compiling programs with PAPI
Group: Development/System
Requires: papi = %{version}-%{release}
Requires: pkgconfig
%description devel
PAPI-devel includes the C header files that specify the PAPI user-space
libraries and interfaces. This is required for rebuilding any program
that uses PAPI.

%package testsuite
Summary: Set of tests for checking PAPI functionality
Group: Development/System
Requires: papi = %{version}-%{release}
%description testsuite
PAPI-testuiste includes compiled versions of papi tests to ensure
that PAPI functions on particular hardware.

%package static
Summary: Static libraries for the compiling programs with PAPI
Group: Development/System
Requires: papi = %{version}-%{release}
%description static
PAPI-static includes the static versions of the library files for
the PAPI user-space libraries and interfaces.

%prep
%setup -q

%build
%if %{without bundled_libpfm}
# Build our own copy of libpfm.
%global libpfm_config --with-pfm-incdir=%{_includedir} --with-pfm-libdir=%{_libdir}
%endif

cd src
autoconf
%configure --with-perf-events \
%{?libpfm_config} \
--with-static-lib=yes --with-shared-lib=yes --with-shlib \
--with-components="appio coretemp example infiniband lmsensors lustre micpower mx net rapl stealtime"
# implicit enabled components: perf_event perf_event_uncore
#components currently left out because of build configure/build issues
# --with-components="bgpm coretemp_freebsd cuda host_micpower nvml vmware"

pushd components
#pushd cuda; ./configure; popd
#pushd host_micpower; ./configure; popd
pushd infiniband_umad; %configure; popd
pushd lmsensors; \
 %configure --with-sensors_incdir=/usr/include/sensors \
 --with-sensors_libdir=%{_libdir}; \
 popd
#pushd vmware; ./configure; popd
popd

#DBG workaround to make sure libpfm just uses the normal CFLAGS
DBG="" make %{?_smp_mflags}

#generate updated versions of the documentation
#DBG workaround to make sure libpfm just uses the normal CFLAGS
pushd ../doc
DBG="" make
DBG="" make install
popd

%install
rm -rf $RPM_BUILD_ROOT
cd src
make DESTDIR=$RPM_BUILD_ROOT LDCONFIG=/bin/true install-all

chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%dir /usr/share/papi
/usr/share/papi/papi_events.csv
%doc INSTALL.txt README LICENSE.txt RELEASENOTES.txt
%doc %{_mandir}/man1/*

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%doc INSTALL.txt README LICENSE.txt RELEASENOTES.txt

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%if %{with bundled_libpfm}
%{_includedir}/perfmon/*.h
%endif
%{_libdir}/*.so
%{_libdir}/pkgconfig/papi*.pc
%doc %{_mandir}/man3/*

%files testsuite
%defattr(-,root,root,-)
/usr/share/papi/run_tests*
/usr/share/papi/ctests
/usr/share/papi/ftests
/usr/share/papi/components
/usr/share/papi/testlib

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%changelog
* Fri Mar 6 2015 William Cohen <wcohen@redhat.com> - 5.4.1-2
- Make sure using libpfm-4.6.0.

* Tue Mar 3 2015 William Cohen <wcohen@redhat.com> - 5.4.1-1
- Rebase to papi-5.4.1.

* Wed Feb 11 2015 William Cohen <wcohen@redhat.com> - 5.4.0-3
- Bump version and rebuild.

* Thu Dec 18 2014 William Cohen <wcohen@redhat.com> - 5.4.0-2
- Split out papi-libs as separate subpackage. (#1172875)

* Mon Nov 17 2014 William Cohen <wcohen@redhat.com> - 5.4.0-1
- Rebase to papi-5.4.0.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 4 2014 William Cohen <wcohen@redhat.com> - 5.3.2-1
- Rebase to 5.3.2.

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2.16.ga7f6159
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 17 2014 Lukas Berk <lberk@redhat.com> - 5.3.0-1.16.ga7f6159
- Automated weekly rawhide release

* Thu Jan 16 2014 William Cohen <wcohen@redhat.com> - 5.3.0-1
- Rebase to 5.3.0.

* Tue Jan 14 2014 William Cohen <wcohen@redhat.com> - 5.2.0-5
- Add presets for Intel Silvermont.

* Mon Jan 13 2014 William Cohen <wcohen@redhat.com> - 5.2.0-4
- Add presets for Haswell and Ivy Bridge.

* Wed Aug 14 2013 William Cohen <wcohen@redhat.com> - 5.2.0-2
- Enable infiniband and stealtime components.

* Wed Aug 07 2013 William Cohen <wcohen@redhat.com> - 5.2.0-1
- Rebase to 5.2.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 William Cohen <wcohen@redhat.com> - 5.1.1-7
- rhbz830275 - Add support for POWER8 processor to PAPI

* Mon Jul 22 2013 William Cohen <wcohen@redhat.com> - 5.1.1-6
- Add autoconf buildrequires.

* Mon Jul 22 2013 William Cohen <wcohen@redhat.com> - 5.1.1-5
- rhbz986673 - /usr/lib64/libpapi.so is unowned
- Package files in /usr/share/papi only once.
- Avoid dependency problem with parallel make of man pages.

* Fri Jul 19 2013 William Cohen <wcohen@redhat.com> - 5.1.1-4
- Correct changelog.

* Fri Jul 5 2013 William Cohen <wcohen@redhat.com> - 5.1.1-3
- Add man page corrections/updates.

* Fri Jun 28 2013 William Cohen <wcohen@redhat.com> - 5.1.1-2
- Add testsuite subpackage.

* Thu May 30 2013 William Cohen <wcohen@redhat.com> - 5.1.1-1
- Rebase to 5.1.1

* Mon Apr 15 2013 William Cohen <wcohen@redhat.com> - 5.1.0.2-2
- Fix arm FTBS rhbz 951806.

* Tue Apr 9 2013 William Cohen <wcohen@redhat.com> - 5.1.0.2-1
- Rebase to 5.1.0.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 William Cohen <wcohen@redhat.com> - 5.0.1-5
- Add armv7 cortex a15 presets.

* Tue Dec 04 2012 William Cohen <wcohen@redhat.com> - 5.0.1-4
- Disable ldconfig on install.

* Thu Nov 08 2012 William Cohen <wcohen@redhat.com> - 5.0.1-3
- Avoid duplicated shared library.

* Wed Oct 03 2012 William Cohen <wcohen@redhat.com> - 5.0.1-2
- Make sure using compatible version of libpfm.

* Thu Sep 20 2012 William Cohen <wcohen@redhat.com> - 5.0.1-1
- Rebase to 5.0.1.

* Mon Sep 10 2012 William Cohen <wcohen@redhat.com> - 5.0.0-6
- Back port fixes for Intel Ivy Bridge event presets.

* Thu Aug 30 2012 William Cohen <wcohen@redhat.com> - 5.0.0-5
- Fixes to make papi with unbundled libpfm.

* Mon Aug 27 2012 William Cohen <wcohen@redhat.com> - 5.0.0-2
- Keep libpfm unbundled.

* Fri Aug 24 2012 William Cohen <wcohen@redhat.com> - 5.0.0-1
- Rebase to 5.0.0.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 William Cohen <wcohen@redhat.com> - 4.4.0-4
- Use siginfo_t rather than struct siginfo.

* Mon Jun 11 2012 William Cohen <wcohen@redhat.com> - 4.4.0-3
- Correct build requires.

* Mon Jun 11 2012 William Cohen <wcohen@redhat.com> - 4.4.0-2
- Unbundle libpfm4 from papi.
- Correct description spellings.
- Remove unused test section.

* Fri Apr 20 2012 William Cohen <wcohen@redhat.com> - 4.4.0-1
- Rebase to 4.4.0.

* Fri Mar 9 2012 William Cohen <wcohen@redhat.com> - 4.2.1-2
- Fix overrun in lmsensor component. (rhbz797692)

* Tue Feb 14 2012 William Cohen <wcohen@redhat.com> - 4.2.1-1
- Rebase to 4.2.1.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 02 2011 William Cohen <wcohen@redhat.com> - 4.2.0-3
- Remove unwanted man1/*.c.1 files. (rhbz749725)

* Mon Oct 31 2011 William Cohen <wcohen@redhat.com> - 4.2.0-2
- Include appropirate man pages with papi rpm. (rhbz749725)
- Rebase to papi-4.2.0, fixup for coretemp component. (rhbz746851)

* Thu Oct 27 2011 William Cohen <wcohen@redhat.com> - 4.2.0-1
- Rebase to papi-4.2.0.

* Fri Aug 12 2011 William Cohen <wcohen@redhat.com> - 4.1.3-3
- Provide papi-static.

* Thu May 12 2011 William Cohen <wcohen@redhat.com> - 4.1.3-2
- Use corrected papi-4.1.3.

* Thu May 12 2011 William Cohen <wcohen@redhat.com> - 4.1.3-1
- Rebase to papi-4.1.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 William Cohen <wcohen@redhat.com> - 4.1.2.1-1
- Rebase to papi-4.1.2.1

* Fri Oct 1 2010 William Cohen <wcohen@redhat.com> - 4.1.1-1
- Rebase to papi-4.1.1

* Tue Jun 22 2010 William Cohen <wcohen@redhat.com> - 4.1.0-1
- Rebase to papi-4.1.0

* Mon May 17 2010 William Cohen <wcohen@redhat.com> - 4.0.0-5
- Test run with upstream cvs version.

* Wed Feb 10 2010 William Cohen <wcohen@redhat.com> - 4.0.0-4
- Resolves: rhbz562935 Rebase to papi-4.0.0 (correct ExcludeArch).

* Wed Feb 10 2010 William Cohen <wcohen@redhat.com> - 4.0.0-3
- Resolves: rhbz562935 Rebase to papi-4.0.0 (bump nvr).

* Wed Feb 10 2010 William Cohen <wcohen@redhat.com> - 4.0.0-2
- correct the ctests/shlib test
- have PAPI_set_multiplex() return proper value
- properly handle event unit masks
- correct PAPI_name_to_code() to match events
- Resolves: rhbz562935 Rebase to papi-4.0.0 

* Wed Jan 13 2010 William Cohen <wcohen@redhat.com> - 4.0.0-1
- Generate papi.spec file for papi-4.0.0.
