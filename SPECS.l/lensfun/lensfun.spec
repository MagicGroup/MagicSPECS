
Name:    lensfun
Version: 0.2.8
Summary: Library to rectify defects introduced by photographic lenses
Release: 2%{?dist}

License: LGPLv3 and CC-BY-SA
URL: http://lensfun.berlios.de/
# sf link doesn't work anymore
#Source0: http://downloads.sourceforge.net/project/lensfun.berlios/lensfun-%{version}.tar.bz2
# this one's a bit wierd too, spectool -g gets the filename wrong
Source0:  http://download.berlios.de/lensfun/lensfun-%{version}.tar.bz2

BuildRequires: cmake >= 2.8
BuildRequires: doxygen
BuildRequires: pkgconfig(glib-2.0) 
BuildRequires: pkgconfig(libpng) 
BuildRequires: pkgconfig(zlib)

%description
The lensfun library provides an open source database of photographic lenses and
their characteristics. It not only provides a way to read and search the
database, but also provides a set of algorithms for correcting images based on
detailed knowledge of lens properties. Right now lensfun is designed to correct
distortion, transversal (also known as lateral) chromatic aberrations,
vignetting and color contribution of a lens.

%package devel
Summary: Development toolkit for %{name}
License: LGPLv3
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
This package contains library and header files needed to build applications
using lensfun.


%prep
%setup -q 


%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DBUILD_DOC:BOOL=ON \
  -DBUILD_TESTS:BOOL=OFF \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}
make doc -C %{_target_platform}


%install
make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}

## unpackaged files
# omit cmake-installed doxygen docs, we handle that manually
rm -rfv %{buildroot}%{_docdir}/%{name}-%{version}*


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README
%doc docs/cc-by-sa-3.0.txt docs/lgpl-3.0.txt
%doc docs/adobe-lens-profile.txt 
%{_datadir}/lensfun/
%{_libdir}/liblensfun.so.0*

%files devel
%doc %{_target_platform}/doc_doxygen/*
%{_includedir}/lensfun/
%{_libdir}/liblensfun.so
%{_libdir}/pkgconfig/lensfun.pc


%changelog
* Sat Jun 07 2014 Liu Di <liudidi@gmail.com> - 0.2.8-2
- 为 Magic 3.0 重建

* Mon Jan 06 2014 Rex Dieter <rdieter@fedoraproject.org> 0.2.8-1
- 0.2.8 (#1048784)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Rex Dieter <rdieter@fedoraproject.org> 0.2.7-1
- 0.2.7

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 25 2012 Nils Philippsen <nils@redhat.com> - 0.2.6-3
- pkgconfig: fix cflags so lensfun.h is found

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Rex Dieter <rdieter@fedoraproject.org>
- 0.2.6-1
- lensfun-0.2.6 (#836156)
- use cmake
- use pkgconfig-style deps

* Thu Jun 21 2012 Nils Philippsen <nils@redhat.com> - 0.2.5-8
- don't modify doxygen configuration anymore as doxygen carries fixes now
  (#831399)

* Fri Jun 15 2012 Nils Philippsen <nils@redhat.com> - 0.2.5-7
- multilib: don't embed creation dates in generated docs (#831399)

* Tue Jan 10 2012 Nils Philippsen <nils@redhat.com> - 0.2.5-6
- rebuild for gcc 4.7

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.2.5-4
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Nils Philippsen <nils@redhat.com> 0.2.5-3
- backport cpuid fixes (#631674)

* Mon Jul 26 2010 Dan Horák <dan[at]danny.cz> 0.2.5-2
- disable SSE vectorization on non x86 arches

* Mon Jun 07 2010 Nils Philippsen <nils@redhat.com> 0.2.5-1
- lensfun-0.2.5
- add CC-BY-SA to main package license tag for lens data
- don't ship GPLv3 text as nothing is licensed under it currently
- mark documentation files as such
- shorten summaries, expand package descriptions

* Sun Oct 18 2009 Rex Dieter <rdieter@fedoraproject.orG> 0.2.4-1
- lensfun-0.2.4 (#529506)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.3-3
- rebuild for pkgconfig deps

* Mon Nov 10 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.3-2
- -devel: Requires: pkgconfig

* Mon Nov 10 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.3-1
- lensfun-0.2.3
- fix SOURCE Url
- configure --target=..generic

* Mon Oct 13 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.2b-3
- BR: doxygen

* Mon Oct 13 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.2b-2
- fix subpkg deps

* Sun Sep 28 2008 Rex Dieter <rdieter@fedoraproject.org> 0.2.2b-1
- adapt for fedora

* Tue Jun 24 2008 Helio Chissini de Castro <helio@mandriva.com> 0.2.2b-1mdv2009.0
+ Revision: 228769
- Added missing buildrequires
- import lensfun
