
## build/include liblastfm_fingerprint
#define fingerprint 1

Name:	 liblastfm
Version: 1.0.1
Release: 3%{?dist}
Summary: Libraries to integrate Last.fm services

Group:	 System Environment/Libraries
License: GPLv2+
URL:     https://github.com/eartle/liblastfm       
# https://github.com/eartle/liblastfm/tarball/1.0.1
Source0: eartle-liblastfm-1.0.1-0-g5b65943.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: cmake
BuildRequires: pkgconfig(QtNetwork) pkgconfig(QtSql) pkgconfig(QtXml)
BuildRequires: ruby

%description
Liblastfm is a collection of libraries to help you integrate Last.fm services
into your rich desktop software.

%if 0%{?fingerprint}
%package fingerprint
Summary: Liblastfm fingerprint library
BuildRequires: fftw3-devel
BuildRequires: pkgconfig(samplerate)
Requires: %{name}%{?_isa} = %{version}-%{release}
# upgrade path
Obsoletes: liblastfm < 1.0
%description fingerprint
%{summary}.
%endif

%package devel
Summary: Development files for %{name}
Group:	 Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fingerprint}
Requires: %{name}-fingerprint%{?_isa} = %{version}-%{release}
%endif
%description devel
%{summary}.


%prep
%setup -q -n eartle-liblastfm-9b4efb5 


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  %{?fingerprint:-DBUILD_FINGERPRINT:BOOL=ON} \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf $RPM_BUILD_ROOT

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
magic_rpm_clean.sh

%check
# TODO: not all tests pass, ping upstream
make test -C %{_target_platform} ||:


%clean
rm -rf %{buildroot} 


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%doc README.md
%{_libdir}/liblastfm.so.1*

%if 0%{?fingerprint}
%post fingerprint -p /sbin/ldconfig
%postun fingerprint -p /sbin/ldconfig

%files fingerprint
%{_libdir}/liblastfm_fingerprint.so.1*
%endif

%files devel
%defattr(-,root,root,-)
%{_libdir}/liblastfm*.so
%{_includedir}/lastfm/


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.1-3
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-1
- liblastfm-1.0.1

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-5
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.3.3-2
- Rebuilt for gcc bug 634757

* Sat Sep 25 2010 Rex Dieter <rdieter@fedoraproject.org> 0.3.3-1
- liblastfm-0.3.3
- missing symbols in liblastfm-0.3.2 (#636729)

* Fri Sep 17 2010 Rex Dieter <rdieter@fedoraproject.org> 0.3.2-1
- liblastfm-0.3.2

* Tue Jun 30 2009 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-2
- rpmlint clean(er)
- BR: libsamplerate-devel
- -devel: fix Requires (typo, +%%?_isa)

* Tue Jun 09 2009 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-1
- liblastfm-0.3.0

* Tue May 05 2009 Rex Dieter <rdieter@fedoraproject.org> 0.2.1-1
- liblastfm-0.2.1, first try
