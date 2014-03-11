Name:           plpa
Version:        1.3.2
Release:        8%{?dist}
Summary:        Portable Linux Processor Affinity

Group:          Development/System
License:        BSD and AMDPLPA
URL:            http://www.open-mpi.org/projects/plpa/
Source0:        http://www.open-mpi.org/software/plpa/v1.3/downloads/plpa-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%ifnarch s390 s390x mips64el
%if 0%{?rhel}
BuildRequires:  valgrind
%else
BuildRequires:  valgrind-devel
%endif
%endif

Requires:       plpa-libs = %{version}-%{release}

%description
PLPA is an attempt to solve the problem that there are multiple API's for 
processor affinity within Linux. Specifically, the functions sched_setaffinity()
and sched_getaffinity() have numbers and types of parameters depending on your 
Linux vendor and/or version of GLibc. This is quite problematic for applications 
attempting to use processor affinity in Linux for compile-time, link-time, 
and run-time reasons.

%package libs
Summary:        Portable Linux Processor Affinity Libraries
Group:          Development/System

%description libs
PLPA is an attempt to solve the problem that there are multiple API's for 
processor affinity within Linux. Specifically, the functions sched_setaffinity()
and sched_getaffinity() have numbers and types of parameters depending on your 
Linux vendor and/or version of GLibc. This is quite problematic for applications 
attempting to use processor affinity in Linux for compile-time, link-time, 
and run-time reasons.

%{name}-libs contains runtime libraries.


%package devel
Summary:        Portable Linux Processor Affinity Header Files
Requires:       plpa-libs = %{version}-%{release}
Group:          Development/System

%description devel
PLPA is an attempt to solve the problem that there are multiple API's for 
processor affinity within Linux. Specifically, the functions sched_setaffinity() 
and sched_getaffinity() have numbers and types of parameters depending on your 
Linux vendor and/or version of GLibc. This is quite problematic for applications 
attempting to use processor affinity in Linux for compile-time, link-time, 
and run-time reasons.

%{name}-devel contains header files.

%prep
%setup -q

%build
%configure 
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libplpa.la

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/plpa-info
%{_bindir}/plpa-taskset

%files libs
%defattr(-,root,root,-)
%{_libdir}/libplpa.so.*
%doc LICENSE AUTHORS NEWS README VERSION

%files devel
%defattr(-,root,root,-)
%{_includedir}/plpa.h
%{_libdir}/libplpa.so

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.3.2-8
- 为 Magic 3.0 重建

* Thu Jan 26 2012 Liu Di <liudidi@gmail.com> - 1.3.2-7
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 11 2010 Dan Horák <dan[at]danny.cz>  - 1.3.2-5
- valgrind not available on s390(x)

* Sat Jan 16 2010 Steve Traylen  <steve.traylen@cern.ch>  - 1.3.2-4
- RHEL does not contain valgrind-devel as Fedora does.
* Thu Jan 14 2010 Steve Traylen  <steve.traylen@cern.ch>  - 1.3.2-3
- Add Groups to subpackages for EPEL5.
* Thu Jan 14 2010 Steve Traylen  <steve.traylen@cern.ch>  - 1.3.2-2
- Move all docs to lib package
- First version to be added to Fedora.
* Tue Jan 12 2010 Steve Traylen  <steve.traylen@cern.ch>  - 1.3.2-1
- License change from BSD to correct BSD and AMDPLPA
- New upstream - 1.3.2
* Fri Oct 23 2009  Steve Traylen  <steve.traylen@cern.ch>  - 1.3.1-2
- Future proof library version included in -libs package.
* Thu Oct 22 2009  Steve Traylen  <steve.traylen@cern.ch>  - 1.3.1-1
- First Build

