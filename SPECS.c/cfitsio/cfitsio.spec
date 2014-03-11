Name: cfitsio
Version: 3.360
Release: 5%{?dist}
Summary: Library for manipulating FITS data files
Group: Development/Libraries
License: MIT
URL: http://heasarc.gsfc.nasa.gov/fitsio/
%define tarversion 3290
Source0: ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/cfitsio%{tarversion}.tar.gz
Patch0: cfitsio.patch
Patch1: makefile.patch
Patch2: cfitsio-s390.patch
Patch3: cfitsio-zlib.patch

BuildRequires:     gcc-gfortran zlib-devel
Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%description
CFITSIO is a library of C and FORTRAN subroutines for reading and writing 
data files in FITS (Flexible Image Transport System) data format. CFITSIO 
simplifies the task of writing software that deals with FITS files by 
providing an easy to use set of high-level routines that insulate the 
programmer from the internal complexities of the FITS file format. At the 
same time, CFITSIO provides many advanced features that have made it the 
most widely used FITS file programming interface in the astronomical 
community.

%package devel
Group:  Development/Libraries
Summary: Headers required when building programs against cfitsio
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig glibc-headers

%description devel
Headers required when building a program against the cfitsio library.

%package static
Group: Development/Libraries
Summary: Static cfitsio library

%description static
Static cfitsio library; avoid use if possible.

%package docs
Summary: Documentation for cfitsio
Group:  Development/Libraries
BuildArch:  noarch

%description docs
Stand-alone documentation for cfitsio.

%package -n fpack
Summary: FITS image compression and decompression utilities
Group: Applications/Engineering
Requires: %{name} = %{version}-%{release}

%description -n fpack
fpack optimally compresses FITS format images and funpack restores them
to the original state.

* Integer format images are losslessly compressed using the Rice
compression algorithm.
    * typically 30% better compression than GZIP
    * about 3 times faster compression speed than GZIP
    * about the same uncompression speed as GUNZIP 

* Floating-point format images are compressed with a lossy algorithm
    * truncates the image pixel noise by a user-specified amount to
      produce much higher compression than by lossless techniques
    * the precision of scientific measurements in the compressed image
      (relative to those in the original image) depends on the selected
       amount of compression


%prep
%setup -q -n cfitsio
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
# Fixing cfitsio.pc.in
sed -e 's|3.29|3.290|' -i cfitsio.pc.in 
sed -e 's|Libs: -L${libdir} -lcfitsio @LIBS@|Libs: -L${libdir} -lcfitsio|' -i cfitsio.pc.in
sed -e 's|Libs.private: -lm|Libs.private: @LIBS@ -lz -lm|' -i cfitsio.pc.in 
sed -e 's|Cflags: -I${includedir}|Cflags: -D_REENTRANT -I${includedir}|' -i cfitsio.pc.in

rm zlib.h zconf.h

%build
FC=f95
export FC
export CC=gcc # fixes -O*, -g
%configure --enable-reentrant
make shared %{?_smp_mflags}
ln -s libcfitsio.so.0 libcfitsio.so
make fpack %{?_smp_mflags}
make funpack %{?_smp_mflags}
unset FC

%check
make testprog
LD_LIBRARY_PATH=. ./testprog > testprog.lis
cmp -s testprog.lis testprog.out
cmp -s testprog.fit testprog.std

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/%{name}
make LIBDIR=%{_lib} INCLUDEDIR=include/%{name} CFITSIO_LIB=%{buildroot}%{_libdir} \
     CFITSIO_INCLUDE=%{buildroot}%{_includedir}/%{name} install
pushd %{buildroot}%{_libdir}
ln -s libcfitsio.so.0 libcfitsio.so
popd
mkdir %{buildroot}%{_bindir}
cp -p f{,un}pack %{buildroot}%{_bindir}/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README License.txt changes.txt
%{_libdir}/libcfitsio.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/libcfitsio.so
%{_libdir}/pkgconfig/cfitsio.pc

%files static
%doc License.txt
%{_libdir}/libcfitsio.a

%files docs
%doc fitsio.doc fitsio.ps cfitsio.doc cfitsio.ps License.txt

%files -n fpack
%doc fpackguide.pdf License.txt
%{_bindir}/fpack
%{_bindir}/funpack

%changelog
* Sun Mar 09 2014 Liu Di <liudidi@gmail.com> - 3.360-5
- 更新到 3.360

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 3.290-5
- 为 Magic 3.0 重建

* Mon Jan 16 2012 Orion Poplawski <orion@cora.nwra.com> - 3.290-4
- Drop incluedir mod in package config file (bug #782213)

* Fri Jan 06 2012 Sergio Pascual <sergiopr@fedoraproject.org> - 3.290-3
- Adding the libz patch

* Fri Jan 06 2012 Sergio Pascual <sergiopr@fedoraproject.org> - 3.290-2
- Using system libz

* Mon Dec 05 2011 Sergio Pascual <sergiopr@fedoraproject.org> - 3.290-1
- New upstream version
- Reorganizing patches

* Sat Oct 29 2011 Sergio Pascual <sergiopr@fedoraproject.org> - 3.280-2
- Enable multithreading support

* Thu Jun 09 2011 Sergio Pascual <sergiopr@fedoraproject.org> - 3.280-1
- New upstream version, with improved image compression floating-point FITS

* Mon Apr 11 2011 Matthew Truch <matt at truch.net> - 3.270-1
- Upstream 3.270 release.
-   Several bugfixes.
-   A few new library functions.
-   License change (no longer uses GPL code).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.250-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 31 2010 Matthew Truch <matt at truch.net> - 3.250-5
- Require fully versioned cfitsio for fpack as cfitsio doesn't properly soname itself.

* Mon Jul 26 2010 Matthew Truch <matt at truch.net> - 3.250-4
- Re-fix cfitsio.pc file (BZ 618291)
- Fix typo in date of previous changelog entry.

* Thu Jul 22 2010 Orion Poplawski <orion@cora.nwra.com> - 3.250-3
- Build and ship fpack/funpack in fpack package

* Wed Jul 7 2010 Matthew Truch <matt at truch.net> - 3.250-2
- Include license as %%doc in -static and -docs subpackages.

* Sun Jul 4 2010 Matthew Truch <matt at truch.net> - 3.250-1
- Upstream 2.250 release.

* Wed Jun 30 2010 Karsten Hopp <karsten@redhat.com> 3.240-4
- add s390(x) as bigendian machines

* Sun Feb 21 2010 Matthew Truch <matt at truch.net> - 3.240-3
- Fix pkgconfig file which contains the wrong version number.

* Sat Feb 20 2010 Matthew Truch <matt at truch.net> - 3.240-2
- Bump for rebuild.

* Wed Jan 27 2010 Matthew Truch <matt at truch.net> - 3.240-1
- Update to upstream 3.240 release.

* Mon Nov 2 2009 Matthew Truch <matt at truch.net> - 3.210-2
- Re-introduce library soname patch (accidentally removed it).  

* Tue Oct 20 2009 Matthew Truch <matt at truch.net> - 3.210-1
- Update to upstream 3.210 release.

* Fri Jul 24 2009 Matthew Truch <matt at truch.net> - 3.140-2
- Bump to include proper tarball.

* Tue Jul 21 2009 Matthew Truch <matt at truch.net> - 3.140-1
- Update to upstream 3.140 release.
- Bump for mass rebuild.

* Wed Jun 17 2009 Matthew Truch <matt at truch.net> - 3.130-5
- Separate -docs noarch subpackage as per BZ 492438.
- Explicitly set file attributes correctly.  

* Tue Mar 10 2009 Matthew Truch <matt at truch.net> - 3.130-4
- Set correct version in pkgconfig .pc file.  

* Sun Feb 22 2009 Matthew Truch <matt at truch.net> - 3.130-3
- Re-check testprogram output.
- Build for koji, rpm, gcc upgrade.  

* Thu Feb 5 2009 Matthew Truch <matt at truch.net> - 3.130-2
- Fix source file naming typo.

* Wed Feb 4 2009 Matthew Truch <matt at truch.net> - 3.130-1
- Update to 3.130 upstream.

* Sat Sep 20 2008 Matthew Truch <matt at truch.net> - 3.100-2
- Test library with included test-suite.  

* Fri Sep 19 2008 Matthew Truch <matt at truch.net> - 3.100-1
- Update to 3.100 upstream.
  Includes bugfixes and new compression scheme.

* Fri Mar 7 2008 Matthew Truch <matt at truch.net> - 3.060-3
- Properly indicated include and lib directories in .pc file
  (BZ 436539)
- Fix typo in -static descrition.

* Mon Feb 11 2008 Matthew Truch <matt at truch.net> - 3.060-2
- Bump release for rebuild.

* Fri Nov 9 2007 Matthew Truch <matt at truch.net> - 3.060-1
- Update to 3.060 bugfix release.
- Add static package (BZ 372801)

* Tue Aug 21 2007 Matthew Truch <matt at truch.net> - 3.040-3
- Bump release for rebuild (build-id etc.)

* Thu Aug 2 2007 Matthew Truch <matt at truch.net> - 3.040-2
- Update License tag

* Mon Jul 9 2007 Matthew Truch <matt at truch.net> - 3.040-1
- Upgrade to version 3.040 of cfitsio.

* Fri Feb 16 2007 Matthew Truch <matt at truch.net> - 3.030-2
- Require pkgconfig for -devel.
- export CC=gcc so we don't clobber $RPM_OPT_FLAGS, thereby 
  ruining any -debuginfo packages.  
  See RedHat Bugzilla 229041.

* Fri Jan 5 2007 Matthew Truch <matt at truch.net> - 3.030-1
- Upgrade to version 3.020 of cfitsio.

* Fri Dec 8 2006 Matthew Truch <matt at truch.net> - 3.020-3
- Commit correct patch to configure and Makefiles.

* Fri Dec 8 2006 Matthew Truch <matt at truch.net> - 3.020-2
- Modify spec file to install to correct directories.
- Package cfitsio.pc file in -devel package.

* Wed Dec 6 2006 Matthew Truch <matt at truch.net> - 3.020-1
- Upgrade to revision 3.020 of cfitsio.

* Mon Aug 28 2006 Matthew Truch <matt at truch.net> - 3.006-6
- Bump release for rebuild in prep. for FC6.

* Thu Mar 30 2006 Matthew Truch <matt at truch.net> - 3.006-5
- Include defattr() for devel package as well - bug 187366

* Sun Mar 19 2006 Matthew Truch <matt at truch.net> - 3.006-4
- Don't use macro {buildroot} in build, only in install as per 
  appended comments to Bugzilla bug 172042
  
* Fri Mar 10 2006 Matthew Truch <matt at truch.net> - 3.006-3
- Point to f95 instead of g95 as per bugzilla bug 185107

* Tue Feb 28 2006 Matthew Truch <matt at truch.net> - 3.006-2
- Fix spelling typo in name of License.txt file.

* Tue Feb 28 2006 Matthew Truch <matt at truch.net> - 3.006-1
- Use new 3.006 fully official stable (non-beta) upstream package.

* Tue Feb 28 2006 Matthew Truch <matt at truch.net> - 3.005-0.2.beta
- Bump release for FC5 extras rebuild.

* Fri Dec 23 2005 Matthew Truch <matt at truch.net> - 3.005-0.1.beta
- Update to 3.005beta release.

* Mon Nov 14 2005 Matthew Truch <matt at truch.net> - 3.004-0.12.b
- Put in proper URL and Source addresses.
- Sync up spec files.

* Sun Nov 13 2005 Matthew Truch <matt at truch.net> - 3.004-0.11.b
- Clean up unused code in spec file.

* Sun Nov 13 2005 Matthew Truch <matt at truch.net> - 3.004-0.10.b
- Set environment variables correctly.
- Include patch so Makefile will put things where they belong.

* Sun Nov 13 2005 Matthew Truch <matt at truch.net> - 3.004-0.9.b
- Set libdir and includedir correctly for build process.

* Sat Nov 12 2005 Matthew Truch <matt at truch.net> - 3.004-0.8.b
- unset FC once we are done with the build

* Sat Nov 12 2005 Ed Hill <ed@eh3.com> - 3.004-0.7.b
- shared libs and small cleanups

* Sun Nov 06 2005 Matthew Truch <matt at truch.net> - 3.004-0.6.b
- Own include directory created by the devel package.

* Sun Nov 06 2005 Matthew Truch <matt at truch.net> - 3.004-0.5.b
- Shorten summary.
- Improve specfile post and postun syntax.
- Install headers in cfitsio include subdir.
- Include more documentation provided in tarball.

* Sun Nov 06 2005 Matthew Truch <matt at truch.net> - 3.004-0.4.b
- Require cfitsio for cfitsio-devel

* Sat Nov 05 2005 Matthew Truch <matt at truch.net> - 3.004-0.3.b
- Use proper virgin tarball from upstream.

* Sun Oct 30 2005 Matthew Truch <matt at truch.net> - 3.004-0.2.b
- Include gcc-gfortran build requirment and make sure it gets used.
- Use macros instead of hard coded paths.
- Include home page in description

* Sat Oct 29 2005 Matthew Truch <matt at truch.net> - 3.004-0.1.b
- Initial spec file for Fedora Extras.

