%bcond_without python
%if %{with python}
%define python_sitearch %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%define python_prefix %(python -c "import sys; print sys.prefix")
%{?filter_setup:
%filter_provides_in %{python_sitearch}/perfmon/.*\.so$
%filter_setup
}
%endif

Name:		libpfm
Version:	4.6.0
Release:	1%{?dist}

Summary:	Library to encode performance events for use by perf tool

Group:		System Environment/Libraries
License:	MIT
URL:		http://perfmon2.sourceforge.net/
Source0:	http://sourceforge.net/projects/perfmon2/files/libpfm4/%{name}-%{version}.tar.gz

%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	swig
%endif

%description

libpfm4 is a library to help encode events for use with operating system
kernels performance monitoring interfaces. The current version provides support
for the perf_events interface available in upstream Linux kernels since v2.6.31.

%package devel
Summary:	Development library to encode performance events for perf_events based tools
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}

%description devel
Development library and header files to create performance monitoring
applications for the perf_events interface.

%package static
Summary:	Static library to encode performance events for perf_events based tools
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}

%description static
Static version of the libpfm library for performance monitoring
applications for the perf_events interface.

%if %{with python}
%package python
Summary:	Python bindings for libpfm and perf_event_open system call
Group:		Development/Languages
Requires:	%{name}%{?_isa} = %{version}

%description python
Python bindings for libpfm4 and perf_event_open system call.
%endif

%prep
%setup -q

%build
%if %{with python}
%global python_config CONFIG_PFMLIB_NOPYTHON=n
%else
%global python_config CONFIG_PFMLIB_NOPYTHON=y
%endif
make %{python_config} %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

%if %{with python}
%global python_config CONFIG_PFMLIB_NOPYTHON=n PYTHON_PREFIX=$RPM_BUILD_ROOT/%{python_prefix}
%else
%global python_config CONFIG_PFMLIB_NOPYTHON=y
%endif

make \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
    %{python_config} \
    LDCONFIG=/bin/true \
    install

%post -p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%doc README
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/lib*.so

%files static
%{_libdir}/lib*.a

%if %{with python}
%files python
%{python_sitearch}/*
%endif

%changelog
* Thu Mar 5 2015 William Cohen <wcohen@redhat.com> - 4.6.0-1
- Rebase on libpfm-4.6.0.

* Wed Feb 11 2015 William Cohen <wcohen@redhat.com> - 4.5.0-6
- Bump version and rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 4.5.0-4
- Replace python-setuptools-devel BR with python-setuptools

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 William Cohen <wcohen@redhat.com> 4.5.0-2
- Add cortex a53 support.

* Fri May 23 2014 William Cohen <wcohen@redhat.com> 4.5.0-1
- Rebase on libpfm-4.5.0.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 William Cohen <wcohen@redhat.com> 4.4.0-2
- Add IBM power 8 support.

* Mon Jun 17 2013 William Cohen <wcohen@redhat.com> 4.4.0-1
- Rebase on libpfm-4.4.0.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 William Cohen <wcohen@redhat.com> 4.3.0-2
- Turn off LDCONFIG and remove patch.

* Tue Aug 28 2012 William Cohen <wcohen@redhat.com> 4.3.0-1
- Rebase on libpfm-4.3.0.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 8 2012 William Cohen <wcohen@redhat.com> 4.2.0-7
- Eliminate swig error.

* Thu Jun 7 2012 William Cohen <wcohen@redhat.com> 4.2.0-6
- Eliminate rpm_build_root macro in build section.
- Correct location of shared library files.

* Thu Jun 7 2012 William Cohen <wcohen@redhat.com> 4.2.0-5
- Use siginfo_t for some examples.

* Mon Jun 4 2012 William Cohen <wcohen@redhat.com> 4.2.0-4
- Correct python files.

* Wed Mar 28 2012 William Cohen <wcohen@redhat.com> 4.2.0-3
- Additional spec file fixup for rhbz804666.

* Wed Mar 14 2012 William Cohen <wcohen@redhat.com> 4.2.0-2
- Some spec file fixup.

* Wed Jan 12 2011 Arun Sharma <asharma@fb.com> 4.2.0-0
Initial revision
