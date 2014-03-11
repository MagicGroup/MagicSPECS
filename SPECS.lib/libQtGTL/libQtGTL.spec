
%define soversion 0.1

Summary: Qt bindings for OpenGTL
Name:    libQtGTL
Version: 0.9.2
Release: 3%{?dist}

License: LGPLv2 
Group:   System Environment/Libraries
URL:     http://www.opengtl.org/
Source0: http://download.opengtl.org/libQtGTL-%{version}.tar.bz2
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

## upstreamable patches
# TODO: double-check if this needs rebasing -- rex
Patch50: libQtGTL-0.9.1-dso_linking.patch
Patch51: libQtGTL-0.9.2-typo.patch

## upstream patches

BuildRequires: cmake
# aka OpenGTL-devel
BuildRequires: pkgconfig(GTLCore) >= 0.9.16
BuildRequires: pkgconfig(OpenShiva)
BuildRequires: pkgconfig(QtGui)

%{?_qt4:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q

#patch50 -p1 -b .dso_linking
%patch51 -p1 -b .typo


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion QtGTL)" = "%{version}"
test "$(pkg-config --modversion QtShiva)" = "%{version}"


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libQtGTL.so.%{soversion}
%{_libdir}/libQtShiva.so.%{soversion}
%{_libdir}/libQtGTL.so.%{version}
%{_libdir}/libQtShiva.so.%{version}

%files devel
%defattr(-,root,root,-)
%{_includedir}/QtGTL/
%{_libdir}/libQtGTL.so
%{_libdir}/pkgconfig/QtGTL.pc
%{_includedir}/QtShiva/
%{_libdir}/libQtShiva.so
%{_libdir}/pkgconfig/QtShiva.pc


%changelog
* Mon Sep 17 2012 Karsten Hopp <karsten@redhat.com> 0.9.2-3
- OpenGTL is available on ppc64 now, remove excludearch

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 28 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-1
- 0.9.2

* Sat Jan 14 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-6
- improved .dso_linking patch
- fix build against llvm3-ized OpenGTL

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-4
- pkgconfig-style deps
- %%check: pkg-config sanity

* Tue May 17 2011 Karsten Hopp <karsten@redhat.com> 0.9.1-3.1
- enable build on ppc, only ppc64 has no OpenGTL

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 08 2010 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-2
- fix dso linking

* Thu Apr 08 2010 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-1
- libQtGL-0.9.1

* Wed Mar 24 2010 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-1
- libQtGTL-0.9.0

