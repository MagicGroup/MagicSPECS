
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           qedje
Version:        0.4.0
Release:        11%{?dist}
Summary:        A library combining the benefits of Edje and Qt

Group:          System Environment/Libraries
License:        GPLv3+
URL:            http://code.openbossa.org/projects/%{name}
Source0:        http://code.openbossa.org/projects/%{name}/repos/mainline/archive/0206ec8f2a802bf51455179933d8b7ab3e41a38b.tar.gz
Patch0:         qedje-0.4.0-fix_python_install.patch
Patch1:		qedje-0.4.0-fix_configure_paths.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  qt4-devel
BuildRequires:  eet-devel
BuildRequires:  qzion-devel
BuildRequires:  qzion-python-devel
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  python-devel
BuildRequires:  PyQt4-devel
BuildRequires:  sip-devel

%description
The main purpose of the QEdje project is to build a bridge among components
that proved to have great value for open source developers: Edje and Qt. This
will extend the Qt toolkit with the flexibility of a declarative language, such
as Edje, and also enable Qt widgets to be embedded into Edje UI design.

%package devel

Summary:   Development files for %{name}
Group:     Development/Libraries
Requires:  cmake
Requires:  pkgconfig
Requires:  %{name} = %{version}-%{release}
Requires:  qzion-devel
Requires:  eet-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package python

Summary:  Python bindings for %{name}
Group:    Development/Libraries
Requires: PyQt4
Requires: qzion-python
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}

%description python
The %{name}-python package contains python bindings for %{name}

%package python-devel

Summary:  Python bindings for %{name}
Group:    Development/Libraries
Requires: sip-devel
Requires: PyQt4-devel
Requires: qzion-python-devel
Requires: %{name}-python = %{version}-%{release}

%description python-devel
The %{name}-python-devel package contains the development files
for the python bindings for %{name}

%prep
%setup -q -n %{name}-mainline
%patch0 -p1
%patch1 -p1

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
-DPYTHON_SITE_PACKAGES_DIR=%{python_sitearch} \
-DQZION_SIP_DIR=%{_datadir}/sip/qzion \
..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast -C %{_target_platform} DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README COPYING
%{_libdir}/*.so.*
%{_bindir}/qedje_viewer

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc

%files python
%defattr(-,root,root,-)
%{python_sitearch}/%{name}

%files python-devel
%defattr(-,root,root,-)
%{_datadir}/sip/%{name}

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.4.0-11
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.4.0-10
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.4.0-8
- rebuild (sip)

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jan 12 2010 john5342 <john5342@fedoraproject.org> - 0.4.0-6
- Fix qedje.pc configuration. Same issue as qzion (#553715)

* Thu Jan 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.4.0-5 
- rebuild (sip)

* Mon Nov 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.4.0-4
- -python: Requires: sip-api(%%_sip_api_major) >= %%_sip_api

* Mon Nov 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.4.0-3
- drop extraneous BR: sip-devel

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 06 2009 John5342 <john5342 at, fedoraproject.org> 0.4.0-1
- Updated to new upstream release (0.4.0)

* Fri Mar 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.3.0-5
- revert (previous borkage probably due to qt-4.5-rc1)

* Wed Mar 05 2009 Caolán McNamara <caolanm@redhat.com> - 0.3.0-4
- BR: phonon-devel

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 19 2008 John5342 <john5342 at, fedoraproject.org> 0.3.0-2
- Fixed a license
- BR: qzion-devel
- devel R: qzion-devel, eet-devel

* Fri Dec 19 2008 John5342 <john5342 at, fedoraproject.org> 0.3.0-1
- Initial package
