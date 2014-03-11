Name:		google-perftools
Version:	1.9.1
Release:	1%{?dist}
License:	BSD
Group:		Development/Tools
Summary:	Very fast malloc and performance analysis tools
URL:		http://code.google.com/p/google-perftools/
Source0:	http://google-perftools.googlecode.com/files/google-perftools-%{version}.tar.gz
# ppc64 still broken, bz 238390
ExclusiveArch:	%{ix86} x86_64 ppc
%ifnarch ppc ppc64
BuildRequires:	libunwind-devel
%endif
Requires:	gv, graphviz
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description
Perf Tools is a collection of performance analysis tools, including a 
high-performance multi-threaded malloc() implementation that works
particularly well with threads and STL, a thread-friendly heap-checker,
a heap profiler, and a cpu-profiler.

%package devel
Summary:	Development libraries and headers for google-perftools
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Libraries and headers for developing applications that use google-perftools.

%package libs
Summary:	Libraries provided by google-perftools

%description libs
Libraries provided by google-perftools, including libtcmalloc and libprofiler.

%prep
%setup -q

%build
CXXFLAGS=`echo $RPM_OPT_FLAGS -DTCMALLOC_LARGE_PAGES| sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//g'`
%configure --disable-static 

# Bad rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Can't build with smp_mflags
make 

%install
make DESTDIR=$RPM_BUILD_ROOT docdir=%{_docdir}/%{name}-%{version}/ install
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

# Zero files
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/NEWS

%check
# http://code.google.com/p/google-perftools/issues/detail?id=153
%ifnarch ppc
# Their test suite is junk. Disabling.
# LD_LIBRARY_PATH=./.libs make check
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%{_bindir}/pprof
%{_mandir}/man1/*
%{_docdir}/%{name}-%{version}/

%files devel
%{_includedir}/google
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files libs
%{_libdir}/*.so.*

%changelog
* Wed Jan  4 2012 Tom Callaway <spot@fedoraproject.org> - 1.9.1-1
- update to 1.9.1

* Mon Oct 24 2011 Tom Callaway <spot@fedoraproject.org> - 1.8.3-3
- split libraries out into subpackage to minimize dependencies

* Wed Sep 21 2011 Remi Collet <remi@fedoraproject.org> - 1.8.3-2
- rebuild for new libunwind

* Tue Aug 30 2011 Tom Callaway <spot@fedoraproject.org> - 1.8.3-1
- update to 1.8.3

* Mon Aug 22 2011 Tom Callaway <spot@fedoraproject.org> - 1.8.2-1
- update to 1.8.2

* Thu Jul 28 2011 Tom Callaway <spot@fedoraproject.org> - 1.8.1-1
- update to 1.8.1

* Mon Jul 18 2011 Tom Callaway <spot@fedoraproject.org> - 1.8-1
- update to 1.8

* Wed Jun 29 2011 Tom Callaway <spot@fedoraproject.org> - 1.7-4
- fix tcmalloc compile against current glibc, fix derived from:
  http://src.chromium.org/viewvc/chrome?view=rev&revision=89800

* Thu May 12 2011 Tom Callaway <spot@fedoraproject.org> - 1.7-3
- add Requires: graphviz, gv for pprof

* Fri Mar 11 2011 Dan Horák <dan[at]danny.cz> - 1.7-2
- switch to ExclusiveArch

* Fri Feb 18 2011 Tom Callaway <spot@fedoraproject.org> - 1.7-1
- update to 1.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6-2
- fix pprof to work properly with jemalloc (bz 657118)

* Fri Aug  6 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6-1
- update to 1.6

* Wed Jan 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.5-1
- update to 1.5
- disable broken test suite

* Sat Sep 12 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4-1
- update to 1.4

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-2
- disable tests for ppc, upstream ticket #153

* Thu Jul  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-1
- update to 1.3

* Wed May 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2-1
- update to 1.2

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.99.1-1
- update to 0.99.1
- previous patches in 0.98-1 were taken upstream

* Mon Aug 25 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.98-1
- update to 0.98
- fix linuxthreads.c compile (upstream issue 74)
- fix ppc compile (upstream issue 75)
- enable ppc

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.95-4
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.95-3
- re-disable ppc/ppc64

* Tue Feb 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.95-2
- ppc/ppc64 doesn't have libunwind

* Tue Feb 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.95-1
- 0.95 (all patches taken upstream)
- enable ppc support
- workaround broken ptrace header (no typedef for u32)

* Fri Jan  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.94.1-1
- bump to 0.94.1
- fix for gcc4.3
- fix unittest link issue

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.93-1
- upstream merged my patch!
- rebuild for BuildID

* Wed Aug  1 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.92-1
- bump to 0.92

* Thu May 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.91-3.1
- excludearch ppc64

* Sun Apr 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.91-3
- The tests work fine for me locally, but some of them fail inside mock.

* Sun Apr 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.91-2
- no support for ppc yet

* Mon Apr 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.91-1
- alright, lets see if this works now.

* Wed Oct 13 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.3-2
- change group to Development/Tools

* Mon Oct 10 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.3-1
- initial package for Fedora Extras
