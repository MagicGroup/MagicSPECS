
%define soversion 0.8
#define test_data 1

Name: OpenGTL
Summary: Graphics Transformation Languages
Version: 0.9.18
Release: 8%{?dist}

License: LGPLv2
URL: http://opengtl.org/
Source0: http://download.opengtl.org/OpenGTL-%{version}.tar.bz2
%if 0%{?test_data}
Source1: http://download.opengtl.org/tests-data-%{version}.tar.bz2
%endif

## upstreamable patches
# link llvm libs only private/static
Patch50: OpenGTL-0.9.18-pkgconfig_llvm_libs_private.patch
# allow linking against llvm 3.3svn
Patch51: opengtl-0.9.18-llvm-3.3svn.patch

## upstream patches
Patch1792: 1792.patch
Patch1793: 1793.patch

BuildRequires: cmake
%if 0%{?fedora} > 17
BuildRequires: doxygen-latex
%endif
BuildRequires: doxygen graphviz
BuildRequires: llvm-devel >= 3.3
BuildRequires: pkgconfig(libpng)
# docs 
BuildRequires: ImageMagick ghostscript texlive-latex texlive-dvips
BuildRequires: zlib-devel

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
OpenGTL provides tools, languages and libraries to create generic
transformations for graphics. These transformations can be used by
different programs, e.g. Krita, Gimp, CinePaint, etc.

%package libs
Summary: Runtime libraries for %{name} 
Requires: %{name} = %{version}-%{release}
%description libs
%{summary}.

%package devel
Summary: Libraries and header files for %{name} 
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
This package contains library and header files needed to develop new
native programs that use the OpenGTL libraries.


%prep
%setup -q %{?test_data: -a 1}

%patch50 -p1 -b .pkgconfig_llvm_libs_private
%patch51 -p1 -b .llvm33
%patch1792 -p1 -b .1792
%patch1793 -p1 -b .1793


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DOPENGTL_BUILD_TESTS:BOOL=ON \
  %{?test_data:-DOPENGTL_TESTS_DATA:PATH=$PWD/../tests-data} \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}

doxygen OpenGTL.doxy


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

## unpackaged files
rm -rf %{buildroot}%{_docdir}/OpenGTL


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion GTLCore)" = "%{version}"
test "$(pkg-config --modversion GTLImageIO)" = "%{version}"
test "$(pkg-config --modversion OpenCTL)" = "%{version}"
test "$(pkg-config --modversion OpenShiva)" = "%{version}"
# some known failures due to missing test data , 17 tests failed out of 189
# *with* test data, down to 2:
# The following tests FAILED:
#        177 - PerlinNoise.shiva (Failed)
#        189 - grayscaliser.shiva (Failed)
make test -C  %{_target_platform} ||:


%files
%doc COPYING OpenGTL/README
%{_bindir}/ctli
%{_bindir}/ctltc
%{_bindir}/gtlconvert
%{_bindir}/imagecompare
%{_bindir}/shiva
%{_bindir}/shivacheck
%{_bindir}/shivainfo
%{_bindir}/shivanimator
%{_datadir}/OpenGTL/

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_libdir}/libGTLCore.so.%{version}
%{_libdir}/libGTLFragment.so.%{version}
%{_libdir}/libGTLImageIO.so.%{version}
%{_libdir}/libOpenCTL.so.%{version}
%{_libdir}/libOpenShiva.so.%{version}
%{_libdir}/libGTLCore.so.%{soversion}
%{_libdir}/libGTLFragment.so.%{soversion}
%{_libdir}/libGTLImageIO.so.%{soversion}
%{_libdir}/libOpenCTL.so.%{soversion}
%{_libdir}/libOpenShiva.so.%{soversion}
%{_libdir}/GTLImageIO/                                                     

%files devel
%doc html/*
%doc %{_target_platform}/OpenShiva/doc/reference/ShivaRef.pdf
%{_bindir}/ctlc
%{_bindir}/shivac
%{_bindir}/shivatester
%{_includedir}/GTLCore/
%{_includedir}/GTLFragment/
%{_includedir}/GTLImageIO/
%{_includedir}/OpenCTL/
%{_includedir}/OpenShiva/
%{_libdir}/libGTLCore.so
%{_libdir}/libGTLFragment.so
%{_libdir}/libGTLImageIO.so
%{_libdir}/libOpenCTL.so
%{_libdir}/libOpenShiva.so
%{_libdir}/pkgconfig/GTLCore.pc
%{_libdir}/pkgconfig/GTLImageIO.pc
%{_libdir}/pkgconfig/OpenCTL.pc
%{_libdir}/pkgconfig/OpenShiva.pc


%changelog
* Sun Aug 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.9.18-8
- upstream fix for underlinking
- upstream fix for libpng-1.6.x (#991938)

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Adam Jackson <ajax@redhat.com> 0.9.18-6
- Rebuild for final llvm 3.3 soname

* Wed May 08 2013 Adam Jackson <ajax@redhat.com> 0.9.18-5
- Fix build against (and require) llvm 3.3

* Mon Mar 18 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.18-3
- pkgconfig: mark llvm-libs private/static
- -devel: Drop Requires: llvm-devel

* Tue Feb 19 2013 Jens Petersen <petersen@redhat.com> - 0.9.18-2
- F19 rebuild against llvm-3.2

* Mon Feb 18 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.18-1
- 0.9.18

* Wed Feb 13 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.17-4
- BR: doxygen-latex

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.17-1
- 0.9.17

* Mon May 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.16-4
- Re-add unintentinal change

* Mon May 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.16-3
- Fix build with new doxygen, cleanup spec

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.16-2
- Rebuilt for c++ ABI breakage

* Sat Jan 28 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.16-1
- 0.9.16

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 10 2012 Tom Callaway <spot@fedoraproject.org> - 0.9.15.2-1
- update to 0.9.15.2
- apply patches to sync with tip, fix llvm3 compile
- fix gcc 4.7 compile

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.9.15.1-5
- Rebuild for new libpng

* Sun Nov 13 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9.15.1-4
- rebuild (llvm)

* Sat Nov 05 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9.15.1-3
- shared llvm patch

* Wed Aug  3 2011 Michel Salim <salimma@fedoraproject.org> - 0.9.15.1-2
- Rebuild against final LLVM 2.9 release
- Reenable ppc64 support (to match LLVM)

* Wed Apr 13 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9.15.1-1
- 0.9.15.1

* Thu Mar 24 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9.15-3
- build with -DOPENGTL_BUILD_TESTS=ON
- runtime tests fail/hang (#690516, kde#269172)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 05 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.9.15-1
- OpenGTL-0.9.15

* Wed Jun 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.9.14-2
- BR: llvm-static (#609699)

* Fri Jun 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.9.14-1
- OpenGTL-0.9.14

* Tue Apr 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.9.13-2
- %%files: track lib sonames better

* Mon Apr 05 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.9.13-1
- OpenGTL-0.9.13

* Sun Jan 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.9.12-3
- omit html/installdox

* Mon Nov 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.9.12-2
- BR: ImageMagick ghostscript texlive-latex texlive-dvips (docs)

* Fri Nov 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.9.12-1
- OpenGTL-0.9.12

* Wed Nov 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.9.11-1
- OpenGTL-0.9.11

* Fri Sep 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.9.10-1
- OpenGTL-0.9.10
- devel: move Requires: pkgconfig here

* Thu Sep 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.9.9-2
- generate doxygen docs
- ExcludeArch: ppc64 (to match llvm) 

* Wed Jun 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.9.9-1
- OpenGTL-0.9.9

* Fri Jul 25 2008 Matthew Woehlke <mw_triad@users.sourceforge.net> - 0.9.4-1
- Initial version
