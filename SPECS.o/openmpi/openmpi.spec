%global _hardened_build 1
# We only compile with gcc, but other people may want other compilers.
# Set the compiler here.
%global opt_cc gcc
# Optional CFLAGS to use with the specific compiler...gcc doesn't need any,
# so uncomment and define to use
#global opt_cflags
%global opt_cxx g++
#global opt_cxxflags
%global opt_f77 gfortran
#global opt_fflags
%global opt_fc gfortran
#global opt_fcflags

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
# Optional name suffix to use...we leave it off when compiling with gcc, but
# for other compiled versions to install side by side, it will need a
# suffix in order to keep the names from conflicting.
#global _cc_name_suffix -gcc

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Name:			openmpi%{?_cc_name_suffix}
Version:		1.10.1
Release:		3%{?dist}
Summary:		Open Message Passing Interface
Group:			Development/Libraries
License:		BSD, MIT and Romio
URL:			http://www.open-mpi.org/

# We can't use %{name} here because of _cc_name_suffix
Source0:		http://www.open-mpi.org/software/ompi/v1.10/downloads/openmpi-%{version}.tar.bz2
Source1:		openmpi.module.in
Source2:		openmpi.pth.py2
Source3:		openmpi.pth.py3
Source4:		macros.openmpi
# Upstream fix for mpi4py tests
# http://www.open-mpi.org/community/lists/users/2015/11/28027.php
Patch0:                 http://www.open-mpi.org/community/lists/users/att-28030/nbc_copy.patch

BuildRequires:		gcc-gfortran
%ifnarch s390
BuildRequires:		valgrind-devel
%endif
BuildRequires:		libibverbs-devel >= 1.1.3, opensm-devel > 3.3.0
BuildRequires:		librdmacm-devel libibcm-devel
# Doesn't compile:
# vt_dyn.cc:958:28: error: 'class BPatch_basicBlockLoop' has no member named 'getLoopHead'
#                      loop->getLoopHead()->getStartAddress(), loop_stmts );
#BuildRequires:		dyninst-devel
BuildRequires:		hwloc-devel
# So configure can find lstopo
BuildRequires:		hwloc-gui
BuildRequires:		java-devel
BuildRequires:		libevent-devel
BuildRequires:		libfabric-devel
BuildRequires:		papi-devel
BuildRequires:		perl(Getopt::Long)
BuildRequires:		python
BuildRequires:		python2-devel
BuildRequires:		python3-devel
BuildRequires:		libtool-ltdl-devel
BuildRequires:		torque-devel
BuildRequires:		zlib-devel
BuildRequires:		rpm-mpi-hooks

Provides:		mpi
Requires:		environment(modules)
# openmpi currently requires ssh to run
# https://svn.open-mpi.org/trac/ompi/ticket/4228
Requires:		openssh-clients
# otf appears to be bundled
Provides:               bundled(otf) =  1.12.3

# s390 is unlikely to have the hardware we want, and some of the -devel
# packages we require aren't available there.
ExcludeArch: s390 s390x

# Private openmpi libraries
%global __provides_exclude_from %{_libdir}/openmpi/lib/(lib(mca|ompi|open-(pal|rte|trace)|otf)|openmpi/).*.so
%global __requires_exclude lib(mca|ompi|open-(pal|rte|trace)|otf|vt).*

%description
Open MPI is an open source, freely available implementation of both the 
MPI-1 and MPI-2 standards, combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.  A completely new MPI-2
compliant implementation, Open MPI offers advantages for system and
software vendors, application developers, and computer science
researchers. For more information, see http://www.open-mpi.org/ .

%package devel
Summary:	Development files for openmpi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}, gcc-gfortran
Provides:	mpi-devel
Requires:	rpm-mpi-hooks

%description devel
Contains development headers and libraries for openmpi.

%package java
Summary:	Java library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
Requires:	java-headless
%else
Requires:	java
%endif

%description java
Java library.

%package java-devel
Summary:	Java development files for openmpi
Group:		Development/Libraries
Requires:	%{name}-java = %{version}-%{release}
Requires:	java-devel

%description java-devel
Contains development wrapper for compiling Java with openmpi.

# We set this to for convenience, since this is the unique dir we use for this
# particular package, version, compiler
%global namearch openmpi-%{_arch}%{?_cc_name_suffix}

%prep
%setup -q -n openmpi-%{version}
%patch0 -p1

%build
./configure --prefix=%{_libdir}/%{name} \
	--mandir=%{_mandir}/%{namearch} \
	--includedir=%{_includedir}/%{namearch} \
	--sysconfdir=%{_sysconfdir}/%{namearch} \
	--disable-silent-rules \
	--enable-mpi-java \
	--with-libevent=/usr \
	--with-sge \
%ifnarch s390
	--with-valgrind \
	--enable-memchecker \
%endif
	--with-hwloc=/usr \
	--with-libltdl=/usr \
	CC=%{opt_cc} CXX=%{opt_cxx} \
	LDFLAGS='%{__global_ldflags}' \
	CFLAGS="%{?opt_cflags} %{!?opt_cflags:$RPM_OPT_FLAGS}" \
	CXXFLAGS="%{?opt_cxxflags} %{!?opt_cxxflags:$RPM_OPT_FLAGS}" \
	FC=%{opt_fc} FCFLAGS="%{?opt_fcflags} %{!?opt_fcflags:$RPM_OPT_FLAGS}"
#        --with-contrib-vt-flags='CXXFLAGS="-I%{_includedir}/dyninst -L%{_libdir}/dyninst"' \

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}
find %{buildroot}%{_libdir}/%{name}/lib -name \*.la | xargs rm
find %{buildroot}%{_mandir}/%{namearch} -type f | xargs gzip -9
ln -s mpicc.1.gz %{buildroot}%{_mandir}/%{namearch}/man1/mpiCC.1.gz
rm -f %{buildroot}%{_mandir}/%{namearch}/man1/mpiCC.1
rm -f %{buildroot}%{_mandir}/%{namearch}/man1/orteCC.1*
rm -f %{buildroot}%{_libdir}/%{name}/share/vampirtrace/doc/opari/lacsi01.ps.gz
mkdir %{buildroot}%{_mandir}/%{namearch}/man{2,4,5,6,8,9,n}

# Make the environment-modules file
mkdir -p %{buildroot}%{_sysconfdir}/modulefiles/mpi
# Since we're doing our own substitution here, use our own definitions.
sed 's#@LIBDIR@#%{_libdir}/%{name}#;
     s#@ETCDIR@#%{_sysconfdir}/%{namearch}#;
     s#@FMODDIR@#%{_fmoddir}/%{name}#;
     s#@INCDIR@#%{_includedir}/%{namearch}#;
     s#@MANDIR@#%{_mandir}/%{namearch}#;
     s#@PY2SITEARCH@#%{python2_sitearch}/%{name}#;
     s#@PY3SITEARCH@#%{python3_sitearch}/%{name}#;
     s#@COMPILER@#openmpi-%{_arch}%{?_cc_name_suffix}#;
     s#@SUFFIX@#%{?_cc_name_suffix}_openmpi#' \
     <%{SOURCE1} \
     >%{buildroot}%{_sysconfdir}/modulefiles/mpi/%{namearch}

# make the rpm config file
install -Dpm 644 %{SOURCE4} %{buildroot}/%{macrosdir}/macros.%{namearch}

# Link the fortran module to proper location
mkdir -p %{buildroot}/%{_fmoddir}/%{name}
for mod in %{buildroot}%{_libdir}/%{name}/lib/*.mod
do
  modname=$(basename $mod)
  ln -s ../../../%{name}/lib/${modname} %{buildroot}/%{_fmoddir}/%{name}/
done

# Remove extraneous wrapper link libraries (bug 814798)
sed -i -e s/-ldl// -e s/-lhwloc// \
  %{buildroot}%{_libdir}/%{name}/share/openmpi/*-wrapper-data.txt

# install .pth files
mkdir -p %{buildroot}/%{python2_sitearch}/%{name}
install -pDm0644 %{SOURCE2} %{buildroot}/%{python2_sitearch}/openmpi.pth
mkdir -p %{buildroot}/%{python3_sitearch}/%{name}
install -pDm0644 %{SOURCE3} %{buildroot}/%{python3_sitearch}/openmpi.pth

%check
make check

%files
%dir %{_libdir}/%{name}
%dir %{_sysconfdir}/%{namearch}
%dir %{_libdir}/%{name}/bin
%dir %{_libdir}/%{name}/lib
%dir %{_libdir}/%{name}/lib/openmpi
%dir %{_mandir}/%{namearch}
%dir %{_mandir}/%{namearch}/man*
%dir %{python2_sitearch}/%{name}
%{python2_sitearch}/openmpi.pth
%dir %{python3_sitearch}/%{name}
%{python3_sitearch}/openmpi.pth
%config(noreplace) %{_sysconfdir}/%{namearch}/*
%{_libdir}/%{name}/bin/mpi[er]*
%{_libdir}/%{name}/bin/ompi*
%{_libdir}/%{name}/bin/opari
%{_libdir}/%{name}/bin/orte[-dr_]*
%{_libdir}/%{name}/bin/oshmem_info
%{_libdir}/%{name}/bin/oshrun
%{_libdir}/%{name}/bin/otf*
%{_libdir}/%{name}/bin/shmemrun
%{_libdir}/%{name}/lib/*.so.*
%{_mandir}/%{namearch}/man1/mpi[er]*
%{_mandir}/%{namearch}/man1/ompi*
%{_mandir}/%{namearch}/man1/orte[-dr_]*
%{_mandir}/%{namearch}/man1/oshmem_info*
%{_mandir}/%{namearch}/man1/oshrun*
%{_mandir}/%{namearch}/man1/shmemrun*
%{_mandir}/%{namearch}/man7/ompi*
%{_mandir}/%{namearch}/man7/orte*
%{_libdir}/%{name}/lib/openmpi/*
%{_sysconfdir}/modulefiles/mpi/
%dir %{_libdir}/%{name}/share
%dir %{_libdir}/%{name}/share/openmpi
%{_libdir}/%{name}/share/openmpi/doc
%{_libdir}/%{name}/share/openmpi/amca-param-sets
%{_libdir}/%{name}/share/openmpi/help*.txt
%{_libdir}/%{name}/share/openmpi/mca-btl-openib-device-params.ini
%{_libdir}/%{name}/share/openmpi/mca-coll-ml.config

%files devel
%dir %{_includedir}/%{namearch}
%dir %{_libdir}/%{name}/share/vampirtrace
%{_libdir}/%{name}/bin/mpi[cCf]*
%{_libdir}/%{name}/bin/opal_*
%{_libdir}/%{name}/bin/orte[cCf]*
%{_libdir}/%{name}/bin/osh[cf]*
%{_libdir}/%{name}/bin/shmem[cf]*
%{_libdir}/%{name}/bin/vt*
%{_includedir}/%{namearch}/*
%{_fmoddir}/%{name}/
%{_libdir}/%{name}/lib/*.so
%{_libdir}/%{name}/lib/lib*.a
%{_libdir}/%{name}/lib/*.mod
%{_libdir}/%{name}/lib/pkgconfig/
%{_mandir}/%{namearch}/man1/mpi[cCf]*
%{_mandir}/%{namearch}/man1/osh[cCf]*
%{_mandir}/%{namearch}/man1/shmem[cCf]*
%{_mandir}/%{namearch}/man1/opal_*
%{_mandir}/%{namearch}/man3/*
%{_mandir}/%{namearch}/man7/opal*
%{_libdir}/%{name}/share/openmpi/openmpi-valgrind.supp
%{_libdir}/%{name}/share/openmpi/*-wrapper-data.txt
%{_libdir}/%{name}/share/vampirtrace/*
%{macrosdir}/macros.%{namearch}

%files java
%{_libdir}/%{name}/lib/mpi.jar

%files java-devel
%{_libdir}/%{name}/bin/mpijavac
%{_libdir}/%{name}/bin/mpijavac.pl
# Currently this only contaings openmpi/javadoc
%{_libdir}/%{name}/share/doc/
%{_mandir}/%{namearch}/man1/mpijavac.1.gz


%changelog
* Tue Nov 10 2015 Orion Poplawski <orion@cora.nwra.com> - 1.10.1-3
- Add upstream patch to fix zero size message

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Nov 5 2015 Orion Poplawski <orion@cora.nwra.com> - 1.10.1-1
- Update to 1.10.1
- Require environment(modules)
- Fixup fortran module install (bug #1154982)

* Tue Oct 6 2015 Orion Poplawski <orion@cora.nwra.com> - 1.10.0-3
- Do not set CFLAGS in %%_openmpi_load

* Wed Sep 16 2015 Orion Poplawski <orion@cora.nwra.com> - 1.10.0-2
- Add patch to add needed opal/util/argv.h includes

* Tue Sep 15 2015 Orion Poplawski <orion@cora.nwra.com> - 1.10.0-1
- Update to 1.10.0

* Thu Aug 27 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.8.8-5
- Use .pth files to set the python path (https://fedorahosted.org/fpc/ticket/563)

* Mon Aug 24 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.8-4
- Disable valgrind only on s390

* Mon Aug 17 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.8-3
- Do not filter libvt* provides as some dependencies link to it

* Mon Aug 10 2015 Sandro Mani <manisandro@gmail.com> - 1.8.8-2
- Require, BuildRequire: rpm-mpi-hooks

* Mon Aug 10 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.8-1
- Update to 1.8.8
- Drop atomic patch applied upstream

* Wed Jul 15 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.7-1
- Update to 1.8.7

* Tue Jun 23 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.6-1
- Update to 1.8.6

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 5 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.5-1
- Update to 1.8.5

* Fri May 1 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.5-0.2.rc3
- Update to 1.8.5rc3

* Sun Apr 5 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.5-0.1.rc1
- Update to 1.8.5rc1

* Mon Mar 30 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.4-7.20150324gitg9ad2aa8
- Add upstream patch to fix race/hang on 32bit machines

* Fri Mar 27 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.4-6.20150324gitg9ad2aa8
- Update to latest 1.8.4 snapshot
- Add upstream patch to fix atomics on 32bit

* Mon Mar 23 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.8.4-5.20150228gitgd83fb30
- Rebuild for fortran update (#1204420)

* Mon Mar 16 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.4-4.99.20150228gitgd83fb30
- Own and ship pkgconfig files, set PKG_CONFIG_PATH in modulefile (bug #1113626)
- Drop old configure settings

* Wed Mar 4 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.4-3.99.20150228gitgd83fb30
- Update to 1.8.4.99 snapshot

* Fri Feb 13 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.4-2
- Fix MPI_FORTRAN_MOD_DIR (bug #1154982)

* Tue Dec 23 2014 Orion Poplawski <orion@cora.nwra.com> 1.8.4-1
- Update to 1.8.4

* Mon Nov 17 2014 Orion Poplawski <orion@cora.nwra.com> 1.8.3-3
- Rebuild for papi soname change

* Fri Oct 3 2014 Orion Poplawski <orion@cora.nwra.com> 1.8.3-2
- Fix typo in oshmem library name

* Sat Sep 27 2014 Orion Poplawski <orion@cora.nwra.com> 1.8.3-1
- Update to 1.8.3

* Tue Sep 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.8.2-2
- ppc64le now has valgrind

* Tue Aug 26 2014 Orion Poplawski <orion@cora.nwra.com> 1.8.2-1
- Update to 1.8.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug  6 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.8.1-6
- Rebuild (papi)

* Mon Aug  4 2014 Dan Horák <dan[at]danny.cz> 1.8.1-5
- no valgrind on ppc64le yet

* Sat Aug  2 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.8.1-4
- aarch64 now has valgrind

* Thu Jul 17 2014 Orion Poplawski <orion@cora.nwra.com> 1.8.1-3
- Add patch to prevent shmem wrappers from adding extra libs

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Orion Poplawski <orion@cora.nwra.com> 1.8.1-1
- Update to 1.8.1, fixes bug #1089044

* Tue Apr 1 2014 Orion Poplawski <orion@cora.nwra.com> 1.8-1
- Update to 1.8

* Tue Mar 25 2014 Orion Poplawski <orion@cora.nwra.com> 1.7.5-2
- Update provides filter

* Mon Mar 24 2014 Orion Poplawski <orion@cora.nwra.com> 1.7.5-1
- Update to 1.7.5

* Fri Feb 21 2014 Orion Poplawski <orion@cora.nwra.com> - 1.7.4-3
- Require java-headless

* Sat Feb  8 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.7.4-2
- Install macros to %%{_rpmconfdir}/macros.d where available.

* Wed Feb 5 2014 Orion Poplawski <orion@cora.nwra.com> 1.7.4-1
- Update to 1.7.4
- Drop format patch fixed upstream
- Build against system libevent
- Build Java mpi bindings, ship in -java sub-package
- Add requires openssh-clients

* Tue Jan 28 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.3-5
- Drop mode/modeflag. mode no longer used, modeflag obsolete as set in CFLAGS
- Use distro LDFLAGS for hardened build
- Drop armv5tel options
- General spec cleanups

* Thu Jan 16 2014 Orion Poplawski <orion@cora.nwra.com> 1.7.3-4
- Rebuild with papi 5.3.0

* Wed Dec  4 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.3-3
- valgrind not currently supported on aarch64

* Tue Dec 3 2013 Orion Poplawski <orion@cora.nwra.com> 1.7.3-2
- Fix compilation with -Werror=format-security (bug #1037231)

* Sun Oct 20 2013 Orion Poplawski <orion@cora.nwra.com> 1.7.3-1
- Update to 1.7.3
- Upstream no longer ships license incompatible files

* Fri Aug 16 2013 Orion Poplawski <orion@cora.nwra.com> 1.7.2-7
- Move orte* compiler wrappers to devel sub-package (bug #997330)

* Thu Aug 08 2013 Dennis Gilmore <dennis@ausil.us> - 1.7.2-6
- rebuild for papi soname bump bz#995092

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1.7.2-5
- Perl 5.18 rebuild

* Fri Jul 26 2013 Orion Poplawski <orion@cora.nwra.com> 1.7.2-4
- Fix build issue with _cc_name_suffix (bug #986664)

* Mon Jul 22 2013 Deji Akingunola <dakingun@gmail.com> - 1.7.2-3
- Rebuild for papi's shared lib fix

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.7.2-2
- Perl 5.18 rebuild

* Thu Jun 27 2013 Orion Poplawski <orion@cora.nwra.com> 1.7.2-1
- Update to 1.7.2

* Wed Apr 17 2013 Orion Poplawski <orion@cora.nwra.com> 1.7.1-1
- Update to 1.7.1
- Add BR on hwloc
- Add BR on papi-devel

* Tue Apr 16 2013 Orion Poplawski <orion@cora.nwra.com> 1.7-1
- Update to 1.7
- Rebase patch to handle removed components
- Drop esmtp - no longer used

* Sat Feb 23 2013 Orion Poplawski <orion@cora.nwra.com> 1.6.4-2
- Exclude libopen-trace.* from requires

* Fri Feb 22 2013 Orion Poplawski <orion@cora.nwra.com> 1.6.4-1
- Update to 1.6.4
- Drop f90sover and arm-atomics patch fixed upstream

* Mon Jan 28 2013 Orion Poplawski <orion@cora.nwra.com> 1.6.3-7
- Make __requires_exclude more specific so we don't exclude needed libs
  (bug #905263)

* Sun Nov 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.6.3-6
- Update atomics patch for ARM (thanks to Jon Masters)

* Sun Nov 11 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.6.3-5
- Atomics patch to fix building on ARM (thanks to Jon Masters)

* Mon Nov 5 2012 Orion Poplawski <orion@cora.nwra.com> 1.6.3-4
- Add patch to fix libmpi_f90.so version
- Add patch to link tests with system libltdl
- Run make check

* Fri Nov 2 2012 Orion Poplawski <orion@cora.nwra.com> 1.6.3-3
- Set enable-opal-multi-threads for IB support

* Thu Nov 1 2012 Orion Poplawski <orion@cora.nwra.com> 1.6.3-2
- Update rpm macros to use the new module location

* Wed Oct 31 2012 Orion Poplawski <orion@cora.nwra.com> 1.6.3-1
- Update to 1.6.3

* Sat Oct 13 2012 Orion Poplawski <orion@cora.nwra.com> 1.6.2-1
- Update to 1.6.2
- Add BR torque-devel to enable torque support
- Drop old module file location (bug #838467)

* Thu Sep 13 2012 Orion Poplawski <orion@cora.nwra.com> 1.6.1-2
- Drop adding -fPIC, no longer needed
- Set --disable-silent-rules for more verbose build logs
- Don't add opt_*flags to the wrappers
- Only use $RPM_OPT_FLAGS if not using the opt_*flags

* Thu Aug 23 2012 Orion Poplawski <orion@cora.nwra.com> 1.6.1-1
- Update to 1.6.1
- Drop hostfile patch applied upstream

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> 1.6-2
- Add patch from upstream to fix default hostfile location

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> 1.6-1
- Update to 1.6
- Drop arm patch, appears to be addressed upstream
- Remove extraneous wrapper link libraries (bug 814798)

* Tue Apr  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.5-1
- Update to 1.5.5

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-5.1
- Rebuilt for c++ ABI breakage

* Wed Feb 22 2012 Orion Poplawski <orion@cora.nwra.com> 1.5.4-4.1
- Rebuild with hwloc 1.4

* Wed Feb 15 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.4-4
- Rebuild for hwloc soname bump

* Fri Jan 20 2012 Doug Ledford <dledford@redhat.com> - 1.5.4-3
- Move modules file to mpi directory and make it conflict with any other
  mpi module (bug #651074)

* Sun Jan 8 2012 Orion Poplawski <orion@cora.nwra.com> 1.5.4-2
- Rebuild with gcc 4.7 (bug #772443)

* Thu Nov 17 2011 Orion Poplawski <orion@cora.nwra.com> 1.5.4-1
- Update to 1.5.4
- Drop dt-textrel patch fixed upstream
- Fixup handling removed files (bug #722534)
- Uses hwloc instead of plpa
- Exclude private libraries from provides/requires (bug #741104)
- Drop --enable-mpi-threads & --enable-openib-ibcm, no longer recognized

* Sat Jun 18 2011 Peter Robinson <pbrobinson@gmail.com> 1.5-4
- Exclude ARM platforms due to current lack of "atomic primitives" on the platform

* Thu Mar 17 2011 Jay Fenlason <fenlason@redhat.com> 1.5-3
- Add dt-textrel patch to close
  Resolves: bz679489
- Add memchecker and esmtp support
  Resolves: bz647011

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 18 2010 Jay Fenlason <fenlason@redhat.com> 1.5-1
- set MANPATH in openmpi module file
- Upgrade to 1.5
- Workaround for rhbz#617766 appears to no longer be needed for 1.5
- remove pkgconfig files in instal
- Remove orteCC.1 dangling symlink
- Adjust the files entries for share/openmpi/help* and share/openmpi/mca*
- Adjust the files entries for share/openmpi/mpi*
- Add files entry for share/openmpi/orte*.txt

* Sun Sep 05 2010 Dennis Gilmore <dennis@ausil.us> - 1.4.1-7
- disable valgrind support on sparc arches

* Sat Jul 24 2010 David Malcolm <dmalcolm@redhat.com> - 1.4.1-6
- workaround for rhbz#617766

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Mar 29 2010 Jay Fenlason <fenlason@redhat.com> - 1.4.1-4
- Update to fix licencing and packaging issues:
  Use the system plpa and ltdl librarires rather than the ones in the tarball
  Remove licence incompatible files from the tarball.
- update module.in to prepend-path		PYTHONPATH

* Tue Mar 9 2010 Jay Fenlason <fenlason@redhat.com> - 1.4.1-3
- remove the pkgconfig file completely like we did in RHEL.

* Tue Jan 26 2010 Jay Fenlason <fenlason@redhat.com> - 1.4.1-2
- BuildRequires: python

* Tue Jan 26 2010 Jay Fenlason <fenlason@redhat.com> - 1.4.1-1
- New upstream version, which includes the changeset_r22324 patch.
- Correct a typo in the Source0 line in this spec file.

* Fri Jan 15 2010 Doug Ledford <dledford@redhat.com> - 1.4-4
- Fix an issue with usage of _cc_name_suffix that cause a broken define in
  our module file

* Fri Jan 15 2010 Doug Ledford <dledford@redhat.com> - 1.4-3
- Fix pkgconfig file substitution
- Bump version so we are later than the equivalent version from Red Hat
  Enterprise Linux

* Wed Jan 13 2010 Doug Ledford <dledford@redhat.com> - 1.4-1
- Update to latest upstream stable version
- Add support for libibcm usage
- Enable sge support via configure options since it's no longer on by default
- Add patch to resolve allreduce issue (bz538199)
- Remove no longer needed patch for Chelsio cards

* Tue Sep 22 2009 Jay Fenlason <fenlason@redhat.com> - 1.3.3-6
- Create and own man* directories for use by dependent packages.

* Wed Sep 16 2009 Jay Fenlason <fenlason@redhat.com> - 1.3.3-5
- Move the module file from %{_datadir}/Modules/modulefiles/%{namearch} to
  %{_sysconfdir}/modulefiles/%{namearch} where it belongs.
- Have the -devel subpackage own the man1 and man7 directories for completeness.
- Add a blank line before the clean section.
- Remove --enable-mpirun-prefix-by-default from configure.

* Wed Sep 9 2009 Jay Fenlason <fenlason@redhat.com> - 1.3.3-4
- Modify packaging to conform to
  https://fedoraproject.org/wiki/PackagingDrafts/MPI (bz521334).
- remove --with-ft=cr from configure, as it was apparently causing problems
  for some people.
- Add librdmacm-devel and librdmacm to BuildRequires (related bz515565).
- Add openmpi-bz515567.patch to add support for the latest Chelsio device IDs
  (related bz515567).
- Add exclude-arch (s390 s390x) because we don't have required -devel packages
  there.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Doug Ledford <dledford@redhat.com> - 1.3.3-2
- Add MPI_BIN and MPI_LIB to the modules file (related bz511099)

* Tue Jul 21 2009 Doug Ledford <dledford@redhat.com> - 1.3.3-1
- Make sure all created dirs are owned (bz474677)
- Fix loading of pkgconfig file (bz476844)
- Resolve file conflict between us and libotf (bz496131)
- Resolve dangling symlinks issue (bz496909)
- Resolve unexpanded %%{mode} issues (bz496911)
- Restore -devel subpackage (bz499851)
- Make getting the default openmpi devel environment easier (bz504357)
- Make the -devel package pull in the base package (bz459458)
- Make it easier to use alternative compilers to build package (bz246484)

* Sat Jul 18 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.3.1-4
- Add Provides: openmpi-devel to fix other package builds in rawhide.

* Fri May 08 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.3.1-3
- Treat i586 the same way as i386

* Wed Apr 22 2009 Doug Ledford <dledford@redhat.com> - 1.3.1-2
- fixed broken update
- Resolves: bz496909, bz496131, bz496911

* Tue Apr 14 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3.1-1
- update to 1.3.1, cleanup alternatives, spec, make new vt subpackage

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.4-2
- Autorebuild for GCC 4.3

* Wed Oct 17 2007 Doug Ledford <dledford@redhat.com> - 1.2.4-1
- Update to 1.2.4 upstream version
- Build against libtorque
- Pass a valid mode to open
- Resolves: bz189441, bz265141

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.2.3-5
- Rebuild for selinux ppc32 issue.

* Mon Jul 16 2007 Doug Ledford <dledford@redhat.com> - 1.2.3-4
- Fix a directory permission problem on the base openmpi directories

* Thu Jul 12 2007 Florian La Roche <laroche@redhat.com> - 1.2.3-3
- requires alternatives for various sub-rpms

* Mon Jul 02 2007 Doug Ledford <dledford@redhat.com> - 1.2.3-2
- Fix dangling symlink issue caused by a bad macro usage
- Resolves: bz246450

* Wed Jun 27 2007 Doug Ledford <dledford@redhat.com> - 1.2.3-1
- Update to latest upstream version
- Fix file ownership on -libs package
- Take a swing at solving the multi-install compatibility issues

* Mon Feb 19 2007 Doug Ledford <dledford@redhat.com> - 1.1.1-7
- Bump version to be at least as high as the RHEL4U5 openmpi
- Integrate fixes made in RHEL4 openmpi into RHEL5 (fix a multilib conflict
  for the openmpi.module file by moving from _datadir to _libdir, make sure
  all sed replacements have the g flag so they replace all instances of
  the marker per line, not just the first, and add a %%defattr tag to the
  files section of the -libs package to avoid install errors about
  brewbuilder not being a user or group)
- Resolves: bz229298

* Wed Jan 17 2007 Doug Ledford <dledford@redhat.com> - 1.1.1-5
- Remove the FORTIFY_SOURCE and stack protect options
- Related: bz213075

* Fri Oct 20 2006 Doug Ledford <dledford@redhat.com> - 1.1.1-4
- Bump and build against the final openib-1.1 package

* Wed Oct 18 2006 Doug Ledford <dledford@redhat.com> - 1.1.1-3
- Fix an snprintf length bug in opal/util/cmd_line.c
- RESOLVES: rhbz#210714

* Wed Oct 18 2006 Doug Ledford <dledford@redhat.com> - 1.1.1-2
- Bump and build against openib-1.1-0.pre1.1 instead of 1.0

* Tue Oct 17 2006 Doug Ledford <dledford@redhat.com> - 1.1.1-1
- Update to upstream 1.1.1 version

* Fri Oct 13 2006 Doug Ledford <dledford@redhat.com> - 1.1-7
- ia64 can't take -m64 on the gcc command line, so don't set it there

* Wed Oct 11 2006 Doug Ledford <dledford@redhat.com> - 1.1-6
- Bump rev to match fc6 rev
- Fixup some issue with alternatives support
- Split the 32bit and 64bit libs ld.so.conf.d files into two files so
  multilib or single lib installs both work properly
- Put libs into their own package
- Add symlinks to /usr/share/openmpi/bin%%{mode} so that opal_wrapper-%%{mode}
  can be called even if it isn't the currently selected default method in
  the alternatives setup (opal_wrapper needs to be called by mpicc, mpic++,
  etc. in order to determine compile mode from argv[0]).

* Sun Aug 27 2006 Doug Ledford <dledford@redhat.com> - 1.1-4
- Make sure the post/preun scripts only add/remove alternatives on initial
  install and final removal, otherwise don't touch.

* Fri Aug 25 2006 Doug Ledford <dledford@redhat.com> - 1.1-3
- Don't ghost the mpi.conf file as that means it will get removed when
  you remove 1 out of a number of alternatives based packages
- Put the .mod file in -devel

* Mon Aug  7 2006 Doug Ledford <dledford@redhat.com> - 1.1-2
- Various lint cleanups
- Switch to using the standard alternatives mechanism instead of a home
  grown one

* Wed Aug  2 2006 Doug Ledford <dledford@redhat.com> - 1.1-1
- Upgrade to 1.1
- Build with Infiniband support via openib

* Mon Jun 12 2006 Jason Vas Dias <jvdias@redhat.com> - 1.0.2-1
- Upgrade to 1.0.2

* Wed Feb 15 2006 Jason Vas Dias <jvdias@redhat.com> - 1.0.1-1
- Import into Fedora Core
- Resolve LAM clashes 

* Wed Jan 25 2006 Orion Poplawski <orion@cora.nwra.com> - 1.0.1-2
- Use configure options to install includes and libraries
- Add ld.so.conf.d file to find libraries
- Add -fPIC for x86_64

* Tue Jan 24 2006 Orion Poplawski <orion@cora.nwra.com> - 1.0.1-1
- 1.0.1
- Use alternatives

* Sat Nov 19 2005 Ed Hill <ed@eh3.com> - 1.0-2
- fix lam conflicts

* Fri Nov 18 2005 Ed Hill <ed@eh3.com> - 1.0-1
- initial specfile created

