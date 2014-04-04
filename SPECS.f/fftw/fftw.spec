Name:           fftw
Version:        3.3
Release:        5%{?dist}
Summary:        A Fast Fourier Transform library
Summary(zh_CN.UTF-8): 快速傅里叶变换库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2+
URL:            http://www.fftw.org
Source0:        http://www.fftw.org/fftw-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# OpenMP support not available on RHEL 4
%if 0%{?rhel} == 4
BuildRequires:  gcc-g77
%global openmp 0
%else
BuildRequires:  gcc-gfortran
%global openmp 1
%endif

%global quad 0
# Quad precision support only available with gcc >= 4.6
%if 0%{?fedora} >= 15
# and only on these arches
%ifarch %{ix86} x86_64 ia64
%global quad 1
%endif
%endif

# For check phase
BuildRequires:  time
BuildRequires:  perl

Requires(post): info 
Requires(preun): info


%description
FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

%description -l zh_CN.UTF-8
快速的傅里叶变换库，支持实数和复数。

%package libs
Summary:        FFTW run-time library
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Provides:       fftw3 = %{version}-%{release}
Obsoletes:      fftw3 < 3.3
# Libs branched from rpm containing binaries in version 3.3
Obsoletes:      fftw < 3.3

%description libs
This package contains the FFTW run-time libraries.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package devel
Summary:        Headers, libraries and docs for the FFTW library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       pkgconfig
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs-threads%{?_isa} = %{version}-%{release}
%if %{openmp}
Requires:       %{name}-libs-openmp%{?_isa} = %{version}-%{release}
%endif
Provides:       fftw3-devel%{?_isa} = %{version}-%{release}
Provides:       fftw3-devel = %{version}-%{release}
Obsoletes:      fftw3-devel < 3.3

%description devel
FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package libs-threads
Summary:        FFTW library with threading support
Group:          Development/Libraries

%description libs-threads
This package contains the FFTW library compiled with threading support.

%if %{openmp}
%package libs-openmp
Summary:        FFTW library with OpenMP support
Group:          Development/Libraries

%description libs-openmp
This package contains the FFTW library compiled with OpenMP support.
%endif

%package        static
Summary:        Static versions of the FFTW libraries
Group:          Development/Libraries
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Provides:       fftw3-static%{?_isa} = %{version}-%{release}
Provides:       fftw3-static = %{version}-%{release}
Obsoletes:      fftw3-static < 3.3

%description static
The fftw-static package contains the statically linkable version of
the FFTW fast Fourier transform library.

%package doc
Summary:        FFTW library manual
Group:          Documentation
%if 0%{?rhel} > 5 || 0%{?fedora} > 12
BuildArch:      noarch
%endif

%description doc
This package contains the manual for the FFTW fast Fourier transform
library.

%prep
%setup -q

%build
%if 0%{?rhel} == 4
# System fortran compiler is g77
export F77=g77
%else
# Configure uses g77 by default, if present on system
export F77=gfortran
%endif

BASEFLAGS="--enable-shared --disable-dependency-tracking --enable-threads"
%if %{openmp}
BASEFLAGS="$BASEFLAGS --enable-openmp"
%endif

# Precisions to build
prec_name[0]=single
prec_name[1]=double
prec_name[2]=long
prec_name[3]=quad

# Corresponding flags
prec_flags[0]=--enable-single
prec_flags[1]=--enable-double
prec_flags[2]=--enable-long-double
prec_flags[3]=--enable-quad-precision

# Loop over precisions
%if %{quad}
for((iprec=0;iprec<4;iprec++))
%else
for((iprec=0;iprec<3;iprec++))
%endif
do
 mkdir ${prec_name[iprec]}${ver_name[iver]}
 cd ${prec_name[iprec]}${ver_name[iver]}
 ln -s ../configure .
 %{configure} ${BASEFLAGS} ${prec_flags[iprec]}
 sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
 sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
 make %{?_smp_mflags}
 cd ..
done

%install
rm -rf %{buildroot}
%if %{quad}
for ver in single double long quad
%else
for ver in single double long
%endif
do
 make -C $ver install DESTDIR=%{buildroot}
done
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/*.la

%check
bdir=`pwd`
%if %{quad}
for ver in single double long quad
%else
for ver in single double long
%endif
do 
 export LD_LIBRARY_PATH=$bdir/$ver/.libs:$bdir/$ver/threads/.libs
 make -C $ver check
done

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig
%post libs-threads -p /sbin/ldconfig
%postun libs-threads -p /sbin/ldconfig
%if %{openmp}
%post libs-openmp -p /sbin/ldconfig
%postun libs-openmp -p /sbin/ldconfig
%endif

%post devel
/sbin/install-info --section="Math" %{_infodir}/%{name}.info.gz %{_infodir}/dir  2>/dev/null || :

%preun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc %{_mandir}/man1/fftw*.1.*
%{_bindir}/fftw*-wisdom*

%files libs
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%{_libdir}/libfftw3.so.*
%{_libdir}/libfftw3f.so.*
%{_libdir}/libfftw3l.so.*
%if %{quad}
%{_libdir}/libfftw3q.so.*
%endif

%if %{openmp}
%files libs-openmp
%defattr(-,root,root,-)
%{_libdir}/libfftw3_omp.so.*
%{_libdir}/libfftw3f_omp.so.*
%{_libdir}/libfftw3l_omp.so.*
%if %{quad}
%{_libdir}/libfftw3q_omp.so.*
%endif
%endif

%files libs-threads
%defattr(-,root,root,-)
%{_libdir}/libfftw3_threads.so.*
%{_libdir}/libfftw3f_threads.so.*
%{_libdir}/libfftw3l_threads.so.*
%if %{quad}
%{_libdir}/libfftw3q_threads.so.*
%endif

%files devel
%defattr(-,root,root,-)
%doc doc/FAQ/fftw-faq.html/
%doc %{_infodir}/fftw3.info*
%{_includedir}/fftw3.*
%{_libdir}/pkgconfig/fftw3*.pc
%{_libdir}/libfftw3*.so

%files doc
%defattr(-,root,root,-)
%doc doc/*.pdf doc/html/

%files static
%defattr(-,root,root,-)
%{_libdir}/libfftw3*.a

%changelog
* Wed Apr 02 2014 Liu Di <liudidi@gmail.com> - 3.3-5
- 更新到 3.3.4

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 3.3-5
- 为 Magic 3.0 重建

* Tue Oct 11 2011 Dan Horák <dan[at]danny.cz> - 3.3-4
- libquadmath exists only on x86/x86_64 and ia64

* Mon Oct 10 2011 Rex Dieter <rdieter@fedoraproject.org> 3.3-3
- -devel: Provides: fftw3-devel (#744758)
- -static: Provides: fftw3-static
- drop %%_isa from Obsoletes

* Sat Jul 30 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3-2
- Conditionalize OpenMP and quadruple precision support based on capabilities
  of system compiler.

* Thu Jul 28 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3-1
- Update to 3.3.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 9 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-4
- Get rid of rpath.

* Sat Jan 9 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-3
- Branch out developers' manual to -doc.

* Sat Jan 2 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-2
- Add check phase.
- Cosmetic changes to spec file (unified changelog format, removed unnecessary
  space).
- Use rm instead of find -delete, as latter is not present on EPEL-4.
- Generalize obsoletes of fftw3 packages. Add Obsoletes: fftw3-static.

* Fri Jan 1 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-1
- Update to 3.2.2.
- Make file listings more explicit.
- Don't use file dependencies for info.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Conrad Meyer <konrad@tylerc.org> - 3.2.1-1
- Bump to 3.2.1.

* Thu Dec 4 2008 Conrad Meyer <konrad@tylerc.org> - 3.2-1
- Bump to 3.2.

* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1.2-7
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.1.2-6
- Autorebuild for GCC 4.3

* Fri Aug 24 2007 Quentin Spencer <qspencer@users.sf.net> 3.1.2-5
- Rebuild for F8.

* Fri Jul 27 2007 Quentin Spencer <qspencer@users.sf.net> 3.1.2-4
- Split static libs into separate package (bug 249686).

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 3.1.2-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.2-2
- BuildRequires: pkgconfig for -devel (bug 206444).

* Fri Sep  8 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.2-1
- New release.

* Fri Jun  2 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.1-1
- New upstream release.

* Fri Feb 24 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-4
- Re-enable static libs (bug 181897).
- Build long-double version of libraries (bug 182587).

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-3
- Add Obsoletes and Provides.

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-2
- Rebuild for Fedora Extras 5.
- Disable static libs.
- Remove obsolete configure options.

* Wed Feb  1 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-1
- Upgrade to the 3.x branch, incorporating changes from the fftw3 spec file.
- Add dist tag.

* Mon May 23 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.1.5-8
- BuildReq gcc-gfortran (#156490).

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.1.5-7
- rebuild on all arches
- buildrequire compat-gcc-32-g77

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 2.1.5-5
- Bump release to provide Extras upgrade path.

* Tue Apr 06 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.4
- BuildReq gcc-g77.

* Mon Sep 22 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.3
- Dropped post/preun scripts for info.

* Wed Sep 17 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.2
- Remove aesthetic comments.
- buildroot -> RPM_BUILD_ROOT.
- post/preun for info files.

* Mon Apr 07 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.1
- Updated to 2.1.5.

* Tue Apr 01 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.4-0.fdr.2
- Added Epoch:0.
- Added ldconfig to post and postun.

* Sun Mar 22 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 2.1.4-0.fdr.1
- Updated to 2.1.4.

* Fri Mar 14 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 2.1.3-0.fdr.1
- Fedorafied.

* Mon Oct 21 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.
