
# use cmake-buildsys, else autofoo
# will probably rip this macro out soon, did so to help make
# upstreamable patches -- Rex
%define cmake_build 1

## enable conformance tests, bloats srpm
# enable for rawhide only, should disable in production releases
%if 0%{?fedora} > 15
%define runcheck 0
%endif

Name:    openjpeg
Version: 1.4
Release: 10%{?dist}
Summary: JPEG 2000 command line tools

Group:   Applications/Multimedia
License: BSD
URL:     http://code.google.com/p/openjpeg/ 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: http://openjpeg.googlecode.com/files/openjpeg_v1_4_sources_r697.tgz 
%if 0%{?runcheck}
Source1: http://www.crc.ricoh.com/~gormish/jpeg2000conformance/j2kp4files_v1_5.zip
%endif

%if 0%{?cmake_build}
BuildRequires: cmake 
%else
BuildRequires: automake libtool 
%endif
BuildRequires: libtiff-devel

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

## upstreamable patches
# libopenjpeg has undefined references, http://bugzilla.redhat.com/467661
# http://groups.google.com/group/openjpeg/browse_thread/thread/fba9ad2a35b12e6a
Patch50: openjpeg-1.4-no_undefined.patch
# Use soversion 3 (instead of 1.4)
# http://groups.google.com/group/openjpeg/browse_thread/thread/b9a1d1bfb6f8d09a
Patch51: openjpeg-1.4-cmake_soversion_3.patch
# fix autoconf buildsys (+DESTDIR support mostly) 
# http://groups.google.com/group/openjpeg/browse_thread/thread/6326363ebb969a99
Patch52: openjpeg-1.4-autoconf.patch
# fix cmake to install pkgconfig file(s)
# http://groups.google.com/group/openjpeg/browse_thread/thread/545a90cf2b0e4af2
Patch53: openjpeg-1.4-cmake_pkgconfig.patch
# fix cmake create_symlink usage
Patch54: openjpeg-1.4-cmake_symlink_fix.patch
#  fix OpenJPEGConfig.cmake, https://bugzilla.redhat.com/show_bug.cgi?id=669425
Patch55: openjpeg-1.4-OpenJPEGConfig.patch
# 修正在 libpng 1.5 上的编译错误
Patch56: openjpeg-libpng15.patch

%description
OpenJPEG is an open-source JPEG 2000 codec written in C. It has been
developed in order to promote the use of JPEG 2000, the new still-image
compression standard from the Joint Photographic Experts Group (JPEG).

%package libs
Summary: JPEG 2000 codec runtime library
Group:   System Environment/Libraries
%description libs
The %{name}-libs package contains runtime libraries for applications that use
OpenJPEG.

%package  devel
Summary:  Development files for %{name} 
Group:    Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use OpenJPEG.


%prep
%setup -q -n openjpeg_v1_4_sources_r697 

# Make sure we use system libraries
rm -rf libs

%patch50 -p1 -b .no_undefined
%if 0%{?cmake_build}
%patch51 -p1 -b .cmake_soversion_3
%patch53 -p1 -b .cmake_pkgconfig
%patch54 -p1 -b .cmake_symlink_fix
%patch55 -p1 -b .cmake_OpenJPEGConfig
%else
%patch52 -p1 -b .autoconf
autoreconf -i -f
%endif
%patch56 -p1

%build

%if 0%{?cmake_build}
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DBUILD_EXAMPLES:BOOL=ON \
  -DBUILD_SHARED_LIBS:BOOL=ON \
  %{?runcheck:-DBUILD_TESTING:BOOL=ON} \
  -DJPEG2000_CONFORMANCE_DATA_ROOT:PATH=../J2KP4files/ \
  -DOPENJPEG_INSTALL_BIN_DIR:PATH=%{_bindir} \
  -DOPENJPEG_INSTALL_DATA_DIR:PATH=%{_datadir} \
  -DOPENJPEG_INSTALL_INCLUDE_DIR:PATH=%{_includedir} \
  -DOPENJPEG_INSTALL_LIB_DIR:PATH=%{_libdir} \
   ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%else
%configure \
  --enable-shared \
  --disable-static

# smp build busted
make 
%endif


%install
rm -rf %{buildroot}

%if 0%{?cmake_build}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%else
make install DESTDIR=%{buildroot}
%endif

ln -s openjpeg-1.4 %{buildroot}%{_includedir}/openjpeg

## unpackaged files
# we use %%doc in -libs below instead
rm -rfv %buildroot%{_docdir}/openjpeg-1.4/


%check
## known failures (on rex's f14/x86_64 box anyway)
# lots, all raw image tests fail atm (command-line options need tweaking)
%if 0%{?runcheck}
make test -C %{_target_platform} ||:
%endif


%clean
rm -rf %{buildroot}


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/image_to_j2k
%{_bindir}/j2k_dump
%{_bindir}/j2k_to_image
%{_mandir}/man1/image_to_j2k.1*
%{_mandir}/man1/j2k_dump.1*
%{_mandir}/man1/j2k_to_image.1*

%files libs
%defattr(-,root,root,-)
%doc CHANGES LICENSE 
%{_libdir}/libopenjpeg.so.3*
%{_mandir}/man3/libopenjpeg.3*

%files devel
%defattr(-,root,root,-)
%{_includedir}/openjpeg-1.4/
%{_libdir}/libopenjpeg.so
%{_libdir}/pkgconfig/libopenjpeg.pc
%{_libdir}/pkgconfig/libopenjpeg1.pc
%if 0%{?cmake_build}
%{_libdir}/openjpeg-1.4/
%endif
# legacy/compat header locations
%{_includedir}/openjpeg.h
%{_includedir}/openjpeg/


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.4-10
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 01 2011 Oliver Falk <oliver@linux-kernel.at> 1.4-8
- Remove pkgconfig from reqs (my fault)

* Mon Aug 01 2011 Oliver Falk <oliver@linux-kernel.at> 1.4-7
- devel package requires pkgconfig

* Wed Mar 30 2011 Rex Dieter <rdieter@fedoraproject.org> 1.4-6
- fix pkgconfig support (upstream issue 67)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.4-4
- actually apply patch for OpenJPEGConfig.cmake (#669425)

* Mon Jan 31 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.4-3
- fix OpenJPEGConfig.cmake (#669425)

* Thu Jan 13 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.4-2
- -devel: %%_includedir/openjpeg/ symlink
- add pkgconfig support (to cmake build)

* Mon Jan 03 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.4-1
- openjpeg-1.4

* Fri Oct  1 2010 Tomas Hoger <thoger@fedoraproject.org> - 1.3-10
- Use calloc in opj_image_create0 (SVN r501, rhbz#579548)
- Avoid NULL pointer deref in jp2_decode (SVN r505, rhbz#609385)

* Wed Jul 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.3-9
- include test samples, enable tests
- tighten subpkg deps
- explicitly set/use -DBUILD_SHARED_LIBS:BOOL=ON
- move %%doc files to -libs

* Wed Feb 17 2010 Adam Goode <adam@spicenitz.org> - 1.3-8
- Fix typo in description
- Fix charset of ChangeLog (rpmlint)
- Fix file permissions (rpmlint)
- Make summary more clear (rpmlint)

* Sun Feb 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.3-7
- FTBFS openjpeg-1.3-6.fc12: ImplicitDSOLinking (#564783)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.3-5
- libopenjpeg has undefined references (#467661)
- openjpeg.h is installed in a directory different from upstream's default (#484887)
- drop -O3 (#504663)
- add %%check section
- %%files: track libopenjpeg somajor (2)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 07 2008 Rex Dieter <rdieter@fedoraproject.org> 1.3-3
- FTBFS (#464949)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3-2
- Autorebuild for GCC 4.3

* Thu Dec 27 2007 Callum Lerwick <seg@haxxed.com> 1.3-1
- New upstream release.

* Tue Dec 11 2007 Callum Lerwick <seg@haxxed.com> 1.2-4.20071211svn484
- New snapshot. Fixes bz420811.

* Wed Nov 14 2007 Callum Lerwick <seg@haxxed.com> 1.2-3.20071114svn480
- Build using cmake.
- New snapshot.

* Thu Aug 09 2007 Callum Lerwick <seg@haxxed.com> 1.2-2.20070808svn
- Put binaries in main package, move libraries to -libs subpackage.

* Sun Jun 10 2007 Callum Lerwick <seg@haxxed.com> 1.2-1
- Build the mj2 tools as well.
- New upstream version, ABI has broken, upstream has bumped soname.

* Fri Mar 30 2007 Callum Lerwick <seg@haxxed.com> 1.1.1-3
- Build and package the command line tools.

* Fri Mar 16 2007 Callum Lerwick <seg@haxxed.com> 1.1.1-2
- Link with libm, fixes building on ppc. i386 and x86_64 are magical.

* Fri Feb 23 2007 Callum Lerwick <seg@haxxed.com> 1.1.1-1
- New upstream version, which has the SL patches merged.

* Sat Feb 17 2007 Callum Lerwick <seg@haxxed.com> 1.1-2
- Move header to a subdirectory.
- Fix makefile patch to preserve timestamps during install.

* Sun Feb 04 2007 Callum Lerwick <seg@haxxed.com> 1.1-1
- Initial packaging.
