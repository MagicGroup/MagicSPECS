%global shortver	3
%global mediumver       %{shortver}.5

%ifarch x86_64 ppc64
%global arch64 1
%else
%global arch64 0
%endif

Summary: Numerical linear algebra package libraries
Name: lapack
Version: %{mediumver}.0
Release: 1%{?dist}
License: BSD
Group: Development/Libraries
URL: http://www.netlib.org/lapack/
Source0: http://www.netlib.org/lapack/lapack-%{version}.tgz
Source1: http://www.netlib.org/lapack/manpages.tgz
Source2: Makefile.blas
Source3: Makefile.lapack
Source4: http://www.netlib.org/lapack/lapackqref.ps
Source5: http://www.netlib.org/blas/blasqr.ps
Patch3: lapack-3.4.0-make.inc.patch
Patch4: lapack-3.4.1-lapacke-shared.patch
Patch5: lapack-3.4.1-lapacke-disable-testing-functions.patch
BuildRequires: gcc-gfortran

%description
LAPACK (Linear Algebra PACKage) is a standard library for numerical
linear algebra. LAPACK provides routines for solving systems of
simultaneous linear equations, least-squares solutions of linear
systems of equations, eigenvalue problems, and singular value
problems. Associated matrix factorizations (LU, Cholesky, QR, SVD,
Schur, and generalized Schur) and related computations (i.e.,
reordering of Schur factorizations and estimating condition numbers)
are also included. LAPACK can handle dense and banded matrices, but
not general sparse matrices. Similar functionality is provided for
real and complex matrices in both single and double precision. LAPACK
is coded in Fortran90 and built with gcc.

%package devel
Summary: LAPACK development libraries
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: blas-devel%{?_isa} = %{version}-%{release}

%description devel
LAPACK development libraries (shared).

%package static
Summary: LAPACK static libraries
Group: Development/Libraries
Requires: lapack-devel%{?_isa} = %{version}-%{release}

%description static
LAPACK static libraries.

%package -n blas
Summary: The Basic Linear Algebra Subprograms library
Group: Development/Libraries

%description -n blas
BLAS (Basic Linear Algebra Subprograms) is a standard library which
provides a number of basic algorithms for numerical algebra. 

%package -n blas-devel
Summary: BLAS development libraries
Group: Development/Libraries
Requires: blas%{?_isa} = %{version}-%{release}
Requires: gcc-gfortran

%description -n blas-devel
BLAS development libraries (shared).

%package -n blas-static
Summary: BLAS static libraries
Group: Development/Libraries
Requires: blas-devel%{?_isa} = %{version}-%{release}

%description -n blas-static
BLAS static libraries.

%if 0%{?arch64}
%package -n lapack64
Summary: Numerical linear algebra package libraries
Group: Development/Libraries

%description -n lapack64
LAPACK (Linear Algebra PACKage) is a standard library for numerical
linear algebra. LAPACK provides routines for solving systems of
simultaneous linear equations, least-squares solutions of linear
systems of equations, eigenvalue problems, and singular value
problems. Associated matrix factorizations (LU, Cholesky, QR, SVD,
Schur, and generalized Schur) and related computations (i.e.,
reordering of Schur factorizations and estimating condition numbers)
are also included. LAPACK can handle dense and banded matrices, but
not general sparse matrices. Similar functionality is provided for
real and complex matrices in both single and double precision. LAPACK
is coded in Fortran90 and built with gcc.
This build has 64bit INTEGER support.

%package -n lapack64-devel
Summary: LAPACK development libraries (64bit INTEGER)
Group: Development/Libraries
Requires: lapack-devel%{?_isa} = %{version}-%{release}
Requires: blas64-devel%{?_isa} = %{version}-%{release}

%description -n lapack64-devel
LAPACK development libraries (shared, 64bit INTEGER).

%package -n lapack64-static
Summary: LAPACK static libraries (64bit INTEGER)
Group: Development/Libraries
Requires: lapack64-devel%{?_isa} = %{version}-%{release}

%description -n lapack64-static
LAPACK static libraries (64bit INTEGER).

%package -n blas64
Summary: The Basic Linear Algebra Subprograms library (64bit INTEGER)
Group: Development/Libraries

%description -n blas64
BLAS (Basic Linear Algebra Subprograms) is a standard library which
provides a number of basic algorithms for numerical algebra. This build
has 64bit INTEGER support.

%package -n blas64-devel
Summary: BLAS development libraries
Group: Development/Libraries
Requires: blas-devel%{?_isa} = %{version}-%{release}
Requires: gcc-gfortran

%description -n blas64-devel
BLAS development libraries (shared).

%package -n blas64-static
Summary: BLAS static libraries (64bit INTEGER)
Group: Development/Libraries
Requires: blas64-devel%{?_isa} = %{version}-%{release}

%description -n blas64-static
BLAS static libraries (64bit INTEGER).
%endif

%prep
%setup -q 
%setup -q -D -T -a1
%patch3 -p1 -b .fedora
%patch4 -p1 -b .shared
%patch5 -p1 -b .disable-functions

mkdir manpages
mv man/ manpages/

cp -f INSTALL/make.inc.gfortran make.inc
cp -f %{SOURCE2} BLAS/SRC/Makefile
cp -f %{SOURCE3} SRC/Makefile

sed -i "s|@SHORTVER@|%{shortver}|g" BLAS/SRC/Makefile
sed -i "s|@SHORTVER@|%{shortver}|g" SRC/Makefile
sed -i "s|@SHORTVER@|%{shortver}|g" lapacke/Makefile
sed -i "s|@LONGVER@|%{version}|g" BLAS/SRC/Makefile
sed -i "s|@LONGVER@|%{version}|g" SRC/Makefile
sed -i "s|@LONGVER@|%{version}|g" lapacke/Makefile

%build
RPM_OPT_O_FLAGS=$(echo $RPM_OPT_FLAGS | sed 's|-O2|-O0|')
export FC=gfortran

# Build BLAS
pushd BLAS/SRC
FFLAGS="$RPM_OPT_O_FLAGS" make dcabs1.o
FFLAGS="$RPM_OPT_FLAGS" CFLAGS="$RPM_OPT_FLAGS" make static
cp libblas.a ${RPM_BUILD_DIR}/%{name}-%{version}/
make clean
FFLAGS="$RPM_OPT_O_FLAGS -fPIC" make dcabs1.o
FFLAGS="$RPM_OPT_FLAGS -fPIC" CFLAGS="$RPM_OPT_FLAGS -fPIC" make shared
cp libblas.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/
%if 0%{?arch64}
make clean
FFLAGS="$RPM_OPT_O_FLAGS -fdefault-integer-8" make dcabs1.o
FFLAGS="$RPM_OPT_FLAGS -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS" make static
cp libblas.a ${RPM_BUILD_DIR}/%{name}-%{version}/libblas64.a
make clean
FFLAGS="$RPM_OPT_O_FLAGS -fPIC -fdefault-integer-8" make dcabs1.o
sed -i 's|-soname,libblas|-soname,libblas64|g' Makefile
FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS -fPIC" make shared
sed -i 's|-soname,libblas64|-soname,libblas|g' Makefile
cp libblas.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/libblas64.so.%{version}
%endif
popd

ln -s libblas.so.%{version} libblas.so
%if 0%{?arch64}
ln -s libblas64.so.%{version} libblas64.so
%endif

# Build the static dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make NOOPT="$RPM_OPT_O_FLAGS" OPTS="$RPM_OPT_FLAGS"
popd

# Build the static lapack library
pushd SRC
make FFLAGS="$RPM_OPT_FLAGS" CFLAGS="$RPM_OPT_FLAGS" static
cp liblapack.a ${RPM_BUILD_DIR}/%{name}-%{version}/
popd

# Build the static with pic dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make clean
make NOOPT="$RPM_OPT_O_FLAGS -fPIC" OPTS="$RPM_OPT_FLAGS -fPIC"
popd

# Build the static with pic lapack library
pushd SRC
make clean
make FFLAGS="$RPM_OPT_FLAGS -fPIC" CFLAGS="$RPM_OPT_FLAGS -fPIC" static
cp liblapack.a ${RPM_BUILD_DIR}/%{name}-%{version}/liblapack_pic.a
popd

%if 0%{?arch64}
# Build the static dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make NOOPT="$RPM_OPT_O_FLAGS -fdefault-integer-8" OPTS="$RPM_OPT_FLAGS -fdefault-integer-8"
popd

# Build the static lapack library
pushd SRC
make FFLAGS="$RPM_OPT_FLAGS -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS" static
cp liblapack.a ${RPM_BUILD_DIR}/%{name}-%{version}/liblapack64.a
popd

# Build the static with pic dlamch, dsecnd, lsame, second, slamch bits (64bit INTEGER)
pushd INSTALL
make clean
make NOOPT="$RPM_OPT_O_FLAGS -fPIC -fdefault-integer-8" OPTS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8"
popd

# Build the static with pic lapack library (64bit INTEGER)
pushd SRC
make clean
make FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS -fPIC" static
cp liblapack.a ${RPM_BUILD_DIR}/%{name}-%{version}/liblapack64_pic.a
popd
%endif

# Build the shared dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make clean
make NOOPT="$RPM_OPT_O_FLAGS -fPIC" OPTS="$RPM_OPT_FLAGS -fPIC"
popd

# Build the shared lapack library
pushd SRC
make clean
make FFLAGS="$RPM_OPT_FLAGS -fPIC" CFLAGS="$RPM_OPT_FLAGS -fPIC" shared
cp liblapack.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/
popd

%if 0%{?arch64}
# Build the shared dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make clean
make NOOPT="$RPM_OPT_O_FLAGS -fPIC -fdefault-integer-8" OPTS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8"
popd

# Build the shared lapack library
pushd SRC
make clean
sed -i 's|-soname,liblapack|-soname,liblapack64|g' Makefile
make FFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8" CFLAGS="$RPM_OPT_FLAGS -fPIC -fdefault-integer-8" shared
cp liblapack.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/liblapack64.so.%{version}
sed -i 's|-soname,liblapack64|-soname,liblapack|g' Makefile
popd
%endif

ln -s liblapack.so.%{version} liblapack.so
%if 0%{?arch64}
ln -s liblapack64.so.%{version} liblapack64.so
%endif

# Build the lapacke libraries
pushd lapacke
make clean
make CFLAGS="$RPM_OPT_FLAGS" lapacke
make clean
make CFLAGS="$RPM_OPT_FLAGS -fPIC" shlib
cp liblapacke.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/
popd

cp -p %{SOURCE4} lapackqref.ps
cp -p %{SOURCE5} blasqr.ps

%install
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3
chmod 755 ${RPM_BUILD_ROOT}%{_mandir}/man3

for f in liblapack.so.%{version} libblas.so.%{version} liblapacke.so.%{version} libblas.a liblapack.a liblapack_pic.a liblapacke.a; do
  cp -f $f ${RPM_BUILD_ROOT}%{_libdir}/$f
done

%if 0%{?arch64}
for f in liblapack64.so.%{version} libblas64.so.%{version} libblas64.a liblapack64.a liblapack64_pic.a; do
  cp -f $f ${RPM_BUILD_ROOT}%{_libdir}/$f
done
%endif

# Blas manpages
pushd manpages/
mkdir -p blas/man/man3
cd man/man3/
mv caxpy.f.3 caxpy.3 ccopy.f.3 ccopy.3 cdotc.f.3 cdotc.3 cdotu.f.3 cdotu.3 cgbmv.f.3 cgbmv.3 \
cgemm.f.3 cgemm.3 cgemv.f.3 cgemv.3 cgerc.f.3 cgerc.3 cgeru.f.3 cgeru.3 chbmv.f.3 chbmv.3 \
chemm.f.3 chemm.3 chemv.f.3 chemv.3 cher.f.3 cher.3 cher2.f.3 cher2.3 cher2k.f.3 cher2k.3 \
cherk.f.3 cherk.3 chpmv.f.3 chpmv.3 chpr.f.3 chpr.3 chpr2.f.3 chpr2.3 crotg.f.3 crotg.3 \
cscal.f.3 cscal.3 csrot.f.3 csrot.3 csscal.f.3 csscal.3 cswap.f.3 cswap.3 csymm.f.3 \
csymm.3 csyr2k.f.3 csyr2k.3 csyrk.f.3 csyrk.3 ctbmv.f.3 ctbmv.3 ctbsv.f.3 ctbsv.3 ctpmv.f.3 \
ctpmv.3 ctpsv.f.3 ctpsv.3 ctrmm.f.3 ctrmm.3 ctrmv.f.3 ctrmv.3 ctrsm.f.3 ctrsm.3 ctrsv.f.3 \
ctrsv.3 dasum.f.3 dasum.3 daxpy.f.3 daxpy.3 dcabs1.f.3 dcabs1.3 dcopy.f.3 dcopy.3 ddot.f.3 \
ddot.3 dgbmv.f.3 dgbmv.3 dgemm.f.3 dgemm.3 dgemv.f.3 dgemv.3 dger.f.3 dger.3 dnrm2.f.3 \
dnrm2.3 drot.f.3 drot.3 drotg.f.3 drotg.3 drotm.f.3 drotm.3 drotmg.f.3 drotmg.3 dsbmv.f.3 \
dsbmv.3 dscal.f.3 dscal.3 dsdot.f.3 dsdot.3 dspmv.f.3 dspmv.3 dspr.f.3 dspr.3 dspr2.f.3 \
dspr2.3 dswap.f.3 dswap.3 dsymm.f.3 dsymm.3 dsymv.f.3 dsymv.3 dsyr.f.3 dsyr.3 dsyr2.f.3 \
dsyr2.3 dsyr2k.f.3 dsyr2k.3 dsyrk.f.3 dsyrk.3 dtbmv.f.3 dtbmv.3 dtbsv.f.3 dtbsv.3 dtpmv.f.3 \
dtpmv.3 dtpsv.f.3 dtpsv.3 dtrmm.f.3 dtrmm.3 dtrmv.f.3 dtrmv.3 dtrsm.f.3 dtrsm.3 dtrsv.f.3 \
dtrsv.3 dzasum.f.3 dzasum.3 dznrm2.f.3 dznrm2.3 icamax.f.3 icamax.3 idamax.f.3 idamax.3 \
isamax.f.3 isamax.3 izamax.f.3 izamax.3 lsame.3 sasum.f.3 sasum.3 saxpy.f.3 saxpy.3 \
scabs1.f.3 scabs1.3 scasum.f.3 scasum.3 scnrm2.f.3 scnrm2.3 scopy.f.3 scopy.3 sdot.f.3 sdot.3 \
sdsdot.f.3 sdsdot.3 sgbmv.f.3 sgbmv.3 sgemm.f.3 sgemm.3 sgemv.f.3 sgemv.3 sger.f.3 sger.3 \
snrm2.f.3 snrm2.3 srot.f.3 srot.3 srotg.f.3 srotg.3 srotm.f.3 srotm.3 srotmg.f.3 srotmg.3 \
ssbmv.f.3 ssbmv.3 sscal.f.3 sscal.3 sspmv.f.3 sspmv.3 sspr.f.3 sspr.3 sspr2.f.3 sspr2.3 \
sswap.f.3 sswap.3 ssymm.f.3 ssymm.3 ssymv.f.3 ssymv.3 ssyr.f.3 ssyr.3 ssyr2.f.3 ssyr2.3 \
ssyr2k.f.3 ssyr2k.3 ssyrk.f.3 ssyrk.3 stbmv.f.3 stbmv.3 stbsv.f.3 stbsv.3 stpmv.f.3 stpmv.3 \
stpsv.f.3 stpsv.3 strmm.f.3 strmm.3 strmv.f.3 strmv.3 strsm.f.3 strsm.3 strsv.f.3 strsv.3 \
xerbla.3 xerbla_array.3 zaxpy.f.3 zaxpy.3 zcopy.f.3 zcopy.3 \
zdotc.f.3 zdotc.3 zdotu.f.3 zdotu.3 zdrot.f.3 zdrot.3 zdscal.f.3 zdscal.3 zgbmv.f.3 zgbmv.3 \
zgemm.f.3 zgemm.3 zgemv.f.3 zgemv.3 zgerc.f.3 zgerc.3 zgeru.f.3 zgeru.3 zhbmv.f.3 zhbmv.3 \
zhemm.f.3 zhemm.3 zhemv.f.3 zhemv.3 zher.f.3 zher.3 zher2.f.3 zher2.3 zher2k.f.3 zher2k.3 \
zherk.f.3 zherk.3 zhpmv.f.3 zhpmv.3 zhpr.f.3 zhpr.3 zhpr2.f.3 zhpr2.3 zrotg.f.3 zrotg.3 \
zscal.f.3 zscal.3 zswap.f.3 zswap.3 zsymm.f.3 zsymm.3 zsyr2k.f.3 zsyr2k.3 zsyrk.f.3 zsyrk.3 \
ztbmv.f.3 ztbmv.3 ztbsv.f.3 ztbsv.3 ztpmv.f.3 ztpmv.3 ztpsv.f.3 ztpsv.3 ztrmm.f.3 ztrmm.3 \
ztrmv.f.3 ztrmv.3 ztrsm.f.3 ztrsm.3 ztrsv.f.3 ztrsv.3 ../../blas/man/man3
cd ../..
popd

find manpages/blas/man/man3 -type f -printf "%{_mandir}/man3/%f*\n" > blasmans

find manpages/man/man3 -type f -printf "%{_mandir}/man3/%f*\n" > lapackmans

cp -f manpages/blas/man/man3/* ${RPM_BUILD_ROOT}%{_mandir}/man3
cp -f manpages/man/man3/* ${RPM_BUILD_ROOT}%{_mandir}/man3

# Lapacke headers
mkdir -p %{buildroot}%{_includedir}/lapacke/
cp -a lapacke/include/*.h %{buildroot}%{_includedir}/lapacke/

cd ${RPM_BUILD_ROOT}%{_libdir}
ln -sf liblapack.so.%{version} liblapack.so
ln -sf liblapack.so.%{version} liblapack.so.%{shortver}
ln -sf liblapack.so.%{version} liblapack.so.%{mediumver}
ln -sf libblas.so.%{version} libblas.so
ln -sf libblas.so.%{version} libblas.so.%{shortver}
ln -sf libblas.so.%{version} libblas.so.%{mediumver}
ln -sf liblapacke.so.%{version} liblapacke.so
ln -sf liblapacke.so.%{version} liblapacke.so.%{shortver}
ln -sf liblapacke.so.%{version} liblapacke.so.%{mediumver}
%if 0%{?arch64}
ln -sf liblapack64.so.%{version} liblapack64.so
ln -sf liblapack64.so.%{version} liblapack64.so.%{shortver}
ln -sf liblapack64.so.%{version} liblapack64.so.%{mediumver}
ln -sf libblas64.so.%{version} libblas64.so
ln -sf libblas64.so.%{version} libblas64.so.%{shortver}
ln -sf libblas64.so.%{version} libblas64.so.%{mediumver}
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n blas -p /sbin/ldconfig

%postun -n blas -p /sbin/ldconfig

%if 0%{?arch64}
%post -n lapack64 -p /sbin/ldconfig

%postun -n lapack64 -p /sbin/ldconfig

%post -n blas64 -p /sbin/ldconfig

%postun -n blas64 -p /sbin/ldconfig
%endif

%files -f lapackmans
%doc README LICENSE lapackqref.ps
%dir %{_mandir}/man3/
%{_libdir}/liblapack.so.*
%{_libdir}/liblapacke.so.*

%files devel
%{_includedir}/lapacke/
%{_libdir}/liblapack.so
%{_libdir}/liblapacke.so

%files static
%{_libdir}/liblapack.a
%{_libdir}/liblapack_pic.a
%{_libdir}/liblapacke.a

%files -n blas -f blasmans
%doc blasqr.ps LICENSE
%dir %{_mandir}/man3/
%{_libdir}/libblas.so.*

%files -n blas-devel
%{_libdir}/libblas.so

%files -n blas-static
%{_libdir}/libblas.a

%if 0%{?arch64}
%files -n blas64
%doc LICENSE
%{_libdir}/libblas64.so.*

%files -n blas64-devel
%{_libdir}/libblas64.so

%files -n blas64-static
%{_libdir}/libblas64.a

%files -n lapack64
%doc README LICENSE
%{_libdir}/liblapack64.so.*

%files -n lapack64-devel
%{_libdir}/liblapack64.so

%files -n lapack64-static
%{_libdir}/liblapack64.a
%{_libdir}/liblapack64_pic.a
%endif

%changelog
* Mon Nov 18 2013 Tom Callaway <spot@fedoraproject.org> - 3.5.0-1
- update to 3.5.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Tom Callaway <spot@fedoraproject.org> - 3.4.2-2
- clean out non-free example files from source tarball

* Thu Feb 21 2013 Tom Callaway <spot@fedoraproject.org> - 3.4.2-1
- update to 3.4.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan  7 2013 Tom Callaway <spot@fedoraproject.org> - 3.4.1-4
- fix 64bit sonames

* Fri Jan  4 2013 Tom Callaway <spot@fedoraproject.org> - 3.4.1-3
- enable 64bit INTEGER variant subpackages

* Wed Oct 24 2012 Tom Callaway <spot@fedoraproject.org> - 3.4.1-2
- fix issue where lapacke was linking to testing functions (bz860332)

* Thu Sep 06 2012 Orion Poplawski <orion@cora.nwra.com> - 3.4.1-1
- Update to 3.4.1
- Rebase lapacke shared lib patch

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Tom Callaway <spot@fedoraproject.org> - 3.4.0-1
- update to 3.4.0
- build and include lapacke

* Thu Jun 02 2011 Tom Callaway <spot@fedoraproject.org> - 3.3.1-1
- update to 3.3.1
- create /usr/share/man/manl/ as 0755 and own it in lapack and blas (bz634369)
- spec file cleanup

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Dan Horák <dan[at]danny.cz> - 3.2.2-2
- fix a typo in Makefile.lapack causing #615618

* Wed Jul  7 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.2-1
- update to 3.2.2
- properly include license text
- static subpackages depend on -devel (they're not useful without it)
- clean up makefiles
- pass on version into makefiles, rather than manually hacking on each update

* Wed Dec  9 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.1-4
- Move static libs to static subpackages (resolves bz 545143)

* Fri Sep  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.1-3
- use RPM_OPT_O_FLAGS (-O0) everywhere necessary, drop RPM_OPT_SIZE_FLAGS (-Os) (bz 520518)

* Thu Aug 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.1-2
- don't enable xblas yet

* Fri Aug 14 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.1-1
- update to 3.2.1, spec file cleanups

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 3.1.1-7
- Convert specfile to UTF-8.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.1.1-4
- fix missing dependencies (bz 442915)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.1.1-3
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.1.1-2
- fix license (BSD)
- rebuild for BuildID

* Fri May 25 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.1.1-1
- bump to 3.1.1

* Fri Jan  5 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.1.0-4
- fix bugzillas 219740,219741

* Wed Dec 20 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.1.0-3
- make clean everywhere

* Wed Dec 20 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.1.0-2
- fix the Makefiles

* Tue Nov 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.1.0-1
- bump to 3.1.0

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-38
- bump for fc-6

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-37
- bump for FC5

* Mon Dec 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-36
- bump for gcc4.1

* Tue Nov 15 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-35
- try not to patch files that do not exist

* Tue Nov 15 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-34
- finish fixing bz 143340

* Thu Oct  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-33
- fix bz 169558

* Wed Sep 28 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-32
- move to latest upstream 3.0 tarballs
- add 8 missing BLAS functions from upstream blas tarball (bz 143340)

* Thu Sep 22 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-31
- actually install liblapack_pic.a

* Wed Sep 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-30
- make -devel packages
- make liblapack_pic.a package
- use dist tag

* Thu Apr 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-29
- package moves to Fedora Extras, gcc4

* Tue Dec 21 2004 Ivana Varekova <varekova@redhat.com>
- fix bug #143420 problem with compiler optimalizations

* Tue Nov 30 2004 Ivana Varekova <varekova@redhat.com>
- fix bug #138683 problem with compilation

* Thu Nov 11 2004 Ivana Varekova <varekova@redhat.com>
- fix build problem bug #138447

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Dec 31 2003 Jeff Johnson <jbj@jbj.org> 3.0-23
- link -lg2c explicitly into liblapack and libblas (#109079).

* Wed Aug 20 2003 Jeremy Katz <katzj@redhat.com> 3.0-22
- nuke -man subpackages (#97506)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Nov 10 2002 Jeff Johnson <jbj@redhat.com> 3.0-19
- rebuild with x86_64.

* Thu Jul 18 2002 Trond Eivind Glomsrod <teg@redhat.com> 3.0-18
- Remove an empty man page (#63569)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May  1 2002 Trond Eivind Glomsrod <teg@redhat.com> 3.0-15
- Rebuild

* Thu Feb 21 2002 Trond Eivind Glomsrod <teg@redhat.com> 3.0-14
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Aug 13 2001 Trond Eivind Glomsrod <teg@redhat.com> 3.0-12
- The man-pages for xerbla and lsame were in blas-man and lapack-man (#51605)

* Fri Jun  8 2001 Trond Eivind Glomsrod <teg@redhat.com>
- Reenable optimization for IA64

* Fri May 25 2001 Trond Eivind Glomsrod <teg@redhat.com>
- Add all patches from the LAPACK site as of 2001-05-25
- Use this workaround for IA64 instead
- Remove SPARC workaround
- Don't exclude IA64

* Thu Dec 07 2000 Trond Eivind Glomsrod <teg@redhat.com>
- rebuild for main distribution

* Mon Nov 20 2000 Trond Eivind Glomsrod <teg@redhat.com>
- add the LAPACK Quick Reference Guide to the docs
- add the BLAS Quick Reference Guide to the docs

* Tue Aug 01 2000 Trond Eivind Glomsrod <teg@redhat.com>
- fix lack of ldconfig in postuninstall script

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 10 2000 Trond Eivind Glomsrod <teg@redhat.com>
- updated with the latest updates (new tarfile..) from netlib 

* Thu Jun 15 2000 Trond Eivind Glomsrod <teg@redhat.com>
- use %%{_mandir}
- added some flags to work around SPARC compiler bug

* Wed Jan 19 2000 Tim Powers <timp@redhat.com>
- bzipped sources to conserve space

* Tue Jan  4 2000 Jeff Johnson <jbj@redhat.com>
- build for PowerTools 6.2.

* Sat Dec 25 1999 Joachim Frieben <jfrieben@hotmail.com>
- updated to version v3.0 + update as of Tue Nov 30 1999

* Sat Oct 23 1999 Joachim Frieben <jfrieben@hotmail.com>
- updated Red Hat makefiles to v3.0

* Mon Aug 2 1999 Tim Powers <timp@redhat.com>
- updated to v3.0
- built for 6.1

* Mon Apr 12 1999 Michael Maher <mike@redhat.com>
- built package for 6.0

* Sat Oct 24 1998 Jeff Johnson <jbj@redhat.com>
- new description/summary text.

* Fri Jul 17 1998 Jeff Johnson <jbj@redhat.com>
- repackage for powertools.

* Sun Feb 15 1998 Trond Eivind Glomsrod <teg@pvv.ntnu.no>
 [lapack-2.0-9]
 - No code updates, just built with a customized rpm -
   this should make dependencies right.

* Sat Feb 07 1998 Trond Eivind Glomsrod <teg@pvv.ntnu.no>
 [lapack-2.0-8]
 - Total rewrite of the spec file
 - Added my own makefiles - libs should build better,
   static libs should work (and be faster than they
	would be if they had worked earlier ;)
 - No patch necessary anymore.
 - Renamed lapack-blas and lapack-blas-man to
   blas and blas-man. "Obsoletes:" tag added.
   (oh - and as always: Dedicated to the girl I
   love, Eline Skirnisdottir)

* Sat Dec 06 1997 Trond Eivind Glomsrod <teg@pvv.ntnu.no>
 [lapack-2.0-7]
  - added a dependency to glibc, so people don't try with libc5

* Thu Nov 20 1997 Trond Eivind Glomsrod <teg@pvv.ntnu.no>
  [lapack-2.0-6]
  - removed etime.c
  - compiled with egcs, and for glibc 2.0

* Sun Oct 12 1997 Trond Eivind Glomsrod <teg@pvv.ntnu.no>
  [lapack-2.0-5]
  - added a changelog
  - cleaned up building of shared libs
  - now uses a BuildRoot
  - cleaned up the specfile
