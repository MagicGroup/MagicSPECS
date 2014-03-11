
# Fedora review http://bugzilla.redhat.com/459705

%define _with_check -DEIGEN_BUILD_TESTS:BOOL=ON

Name:    eigen2
Summary: A lightweight C++ template library for vector and matrix math
Epoch:   1
Version: 2.0.17
Release: 5%{?dist}
Group:   System Environment/Libraries
License: GPLv2+ or LGPLv3+
URL:     http://eigen.tuxfamily.org/
%if 0%{?snap:1}
Source0: http://bitbucket.org/eigen/eigen/get/default.tar.bz2
%else
Source0: http://bitbucket.org/eigen/eigen/get/%{version}%{?pre:-%{pre}}.tar.bz2
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: cmake
#docs
BuildRequires: doxygen graphviz

#BuildRequires: %{_bindir}/latex
%if 0%{?fedora} > 8
BuildRequires: tex(latex)
%else
BuildRequires: tetex-latex
%endif

%if 0%{?_with_check:1}
BuildRequires: blas-devel
BuildRequires: gsl-devel
# can't use until undefined symbols are fixed: http://bugzilla.redhat.com/475411
%if 0%{?fedora} > 11
BuildRequires: suitesparse-devel
%endif
BuildRequires: qt4-devel
#-- Could NOT find TAUCS  (missing:  TAUCS_INCLUDES TAUCS_LIBRARIES)
#-- Could NOT find SUPERLU  (missing:  SUPERLU_INCLUDES SUPERLU_LIBRARIES)
#-- Could NOT find GOOGLEHASH  (missing:  GOOGLEHASH_INCLUDES)
%endif

%description
%{summary}

%package devel
Summary: A lightweight C++ template library for vector and matrix math
Group:   Development/Libraries
# -devel subpkg only atm, compat with other distros
Provides: %{name} = %{version}-%{release}
# not *strictly* a -static pkg, but the results are the same
Provides: %{name}-static = %{version}-%{release}
%description devel
%{summary}


%prep
%setup -q -n eigen-eigen-b23437e61a07 


%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} %{?_with_check}  ..
popd

# when building _with_check, memory usage is quite large, skip
# using smp_mflags in that case
make %{!?_with_check:%{?_smp_mflags}} -C %{_target_platform}

# docs
make %{?_smp_mflags} doc -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion eigen2)" = "%{version}"
%if 0%{?_with_check:1}
( cd %{_target_platform}/test; ctest ||:)
%endif


%clean 
rm -rf %{buildroot}


%files devel
%defattr(-,root,root,-)
%doc COPYING COPYING.LESSER
%doc %{_target_platform}/doc/html/
%{_datadir}/pkgconfig/eigen2.pc
%{_includedir}/eigen2/


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.17-2
- Documentation in eigen2-devel is not generated correctly (#813205)

* Fri Jan 13 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.17-1
- 2.0.17

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Rex Dieter <rdieter@fedoraproject.org> 1:2.0.16-1
- 2.0.16

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 Rex Dieter <rdieter@fedoraproject.org> 1:2.0.15-1
- eigen-2.0.15

* Wed Jun 23 2010 Rex Dieter <rdieter@fedoraproject.org> 1:2.0.14-1
- eigen-2.0.14

* Tue Mar 23 2010 Rex Dieter <rdieter@fedoraproject.org> 1:2.0.12-1
- eigen-2.0.12

* Wed Jan 20 2010 Rex Dieter <rdieter@fedoraproject.org> 1:2.0.11-1
- eigen-2.0.11

* Mon Dec 14 2009 Rex Dieter <rdieter@fedoraproject.org> 1:2.0.10-1
- eigen-2.0.10
- Provides: eigen2-static

* Tue Oct 20 2009 Rex Dieter <rdieter@fedoraproject.org> 1:2.0.6-1
- eigen-2.0.6

* Mon Jun 22 2009 Rex Dieter <rdieter@fedoraproject.org> 2.0.3-1
- eigen-2.0.3

* Tue May 19 2009 Rex Dieter <rdieter@fedoraproject.org> 2.0.1-1.1
- disable build tests (temporarily) to bootstrap secondary archs (s309)

* Mon Apr 15 2009 Rex Dieter <rdieter@fedoraproject.org> 2.0.1-1
- eigen-2.0.1

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Rex Dieter <rdieter@fedoraproject.org> 2.0-1
- eigen-2.0.0 (final)

* Wed Jan 28 2009 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.10.rc1
- eigen-2.0-rc1

* Thu Jan 22 2009 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.9.beta6
- eigen-2.0-beta6

* Fri Jan 09 2009 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.8.20090109svn
- eigen2-20090109svn snapshot

* Tue Jan 06 2009 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.7.beta5
- eigen-2.0-beta5

* Sun Jan 04 2009 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.6.beta4
- eigen-2.0-beta4

* Mon Dec 08 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.5.beta2
- eigen-2.0-beta2
- (re)enable buildtime test

* Mon Sep 22 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.4.beta1
- eigen-2.0-beta1

* Mon Aug 25 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.3.alpha7
- disable buildtime tests, which tickle gcc bugs

* Fri Aug 22 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.2.alpha7
- add working %%check

* Wed Aug 20 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.1.alpha7
- eigen-2.0-alpha7
