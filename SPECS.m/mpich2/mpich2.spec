%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	A high-performance implementation of MPI
Name:		mpich2
Version:	1.5
Release:	3%{?dist}
License:	MIT
Group:		Development/Libraries
URL:		http://www.mcs.anl.gov/research/projects/mpich2

Source0:	http://www.mcs.anl.gov/research/projects/mpich2/downloads/tarballs/%{version}/%{name}-%{version}.tar.gz
Source1:	mpich2.macros	
Patch0:		mpich2-modules.patch

BuildRequires:	libXt-devel, bison, flex, libuuid-devel
BuildRequires:	jdk, gcc-gfortran
BuildRequires:  hwloc-devel >= 1.5
BuildRequires:	perl, python
BuildRequires:	automake autoconf libtool gettext
%ifnarch s390 s390x %{arm} mips64el
BuildRequires:	valgrind-devel
%endif
Provides:	mpi
Obsoletes:	%{name}-libs < 1.1.1
Obsoletes:	%{name}-mpd < 1.4.1
Requires:	environment-modules
Requires:	chkconfig
#Requires chkconfig for /usr/sbin/alternatives

%description
MPICH2 is a high-performance and widely portable implementation of the
MPI standard (both MPI-1 and MPI-2). This release has all MPI-2.2 functions and
features required by the standard with the exeption of support for the
"external32" portable I/O format and user-defined data representations for I/O.

The mpich2 binaries in this RPM packages were configured to use the default
process manager (Hydra) using the default device (ch3). The ch3 device
was configured with support for the nemesis channel that allows for
shared-memory and TCP/IP sockets based communication.

This build also include support for using the 'module environment' to select
which MPI implementation to use when multiple implementations are installed.
If you want MPICH2 support to be automatically loaded, you need to install the
mpich2-autoload package.

%package autoload
Summary:	Load mpich2 automatically into profile
Group:		System Environment/Base
Requires:	mpich2 = %{version}-%{release}
# Branched at 1.4.1p1-3 (but f16 branch got -2 bumped to -3),
# this makes the transition smooth.
Obsoletes:	mpich2 < 1.4.1p1-4

%description autoload
This package contains profile files that make mpich2 automatically loaded.

%package devel
Summary:	Development files for mpich2
Group:		Development/Libraries
Provides:	%{name}-devel-static = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	gcc-gfortran 
Requires(pre):	chkconfig
#Requires chkconfig for /usr/sbin/alternatives

%description devel
Contains development headers and libraries for mpich2

%package doc
Summary:	Documentations and examples for mpich2
Group:		Documentation
BuildArch:	noarch
Requires:	%{name}-devel = %{version}-%{release}

%description doc
Contains documentations, examples and manpages for mpich2

# We only compile with gcc, but other people may want other compilers.
# Set the compiler here.
%{!?opt_cc: %global opt_cc gcc}
%{!?opt_fc: %global opt_fc gfortran}
%{!?opt_f77: %global opt_f77 gfortran}
# Optional CFLAGS to use with the specific compiler...gcc doesn't need any,
# so uncomment and undefine to NOT use
%{!?opt_cc_cflags: %global opt_cc_cflags %{optflags}}
%{!?opt_fc_fflags: %global opt_fc_fflags %{optflags}}
#%{!?opt_fc_fflags: %global opt_fc_fflags %{optflags} -I%{_fmoddir}}
%{!?opt_f77_fflags: %global opt_f77_fflags %{optflags}}

%ifarch s390
%global m_option -m31
%else
%global m_option -m%{__isa_bits}
%endif

%ifarch mips64el
%global m_option -mabi=64
%endif

%ifarch %{arm}
%global m_option ""
%endif

%ifarch %{ix86} x86_64
%global selected_channels ch3:nemesis
%else
%global selected_channels ch3:sock
%endif

%ifarch x86_64 ia64 ppc64 s390x sparc64 mips64el
%global priority 41
%else
%global priority 40
%endif

%ifarch %{ix86} x86_64 s390 %{arm} mips64el
%global XFLAGS -fPIC
%endif

%prep
%setup -q
%patch0 -p0 -b .modu

%build
%configure	\
	--enable-sharedlibs=gcc					\
	--enable-shared						\
	--enable-lib-depend					\
	--disable-rpath						\
	--enable-fc						\
	--with-device=%{selected_channels}			\
	--with-pm=hydra:gforker					\
	--sysconfdir=%{_sysconfdir}/%{name}-%{_arch}		\
	--includedir=%{_includedir}/%{name}-%{_arch}		\
	--bindir=%{_libdir}/%{name}/bin				\
	--libdir=%{_libdir}/%{name}/lib				\
	--datadir=%{_datadir}/%{name}				\
	--mandir=%{_mandir}/%{name}				\
	--docdir=%{_datadir}/%{name}/doc			\
	--htmldir=%{_datadir}/%{name}/doc			\
	--with-hwloc-prefix=system				\
	--with-java=%{_sysconfdir}/alternatives/java_sdk	\
	FC=%{opt_fc}						\
	F77=%{opt_f77}						\
	CFLAGS="%{m_option} -O2 %{?XFLAGS}"			\
	CXXFLAGS="%{m_option} -O2 %{?XFLAGS}"			\
	FCFLAGS="%{m_option} -O2 %{?XFLAGS}"			\
	FFLAGS="%{m_option} -O2 %{?XFLAGS}"			\
	LDFLAGS='-Wl,-z,noexecstack'				\
	MPICH2LIB_CFLAGS="%{?opt_cc_cflags}"			\
	MPICH2LIB_CXXFLAGS="%{optflags}"			\
	MPICH2LIB_FCFLAGS="%{?opt_fc_fflags}"			\
	MPICH2LIB_FFLAGS="%{?opt_f77_fflags}"	
#	MPICH2LIB_LDFLAGS='-Wl,-z,noexecstack'			\
#	MPICH2_MPICC_FLAGS="%{m_option} -O2 %{?XFLAGS}"	\
#	MPICH2_MPICXX_FLAGS="%{m_option} -O2 %{?XFLAGS}"	\
#	MPICH2_MPIFC_FLAGS="%{m_option} -O2 %{?XFLAGS}"	\
#	MPICH2_MPIF77_FLAGS="%{m_option} -O2 %{?XFLAGS}"
#	--with-openpa-prefix=embedded				\

#	FCFLAGS="%{?opt_fc_fflags} -I%{_fmoddir}/%{name} %{?XFLAGS}"	\
#make %{?_smp_mflags} doesn't work
make VERBOSE=1

%install
make DESTDIR=%{buildroot} install

# Workaround 1.4.1 broken destdir
for fichier in mpif77 mpif90 mpicxx mpicc ; do
  sed -i 's#'%{buildroot}'##' %{buildroot}%{_libdir}/%{name}/bin/$fichier
  sed -i 's#'%{buildroot}'##' %{buildroot}%{_sysconfdir}/%{name}-%{_arch}/$fichier.conf
done

mv %{buildroot}%{_libdir}/%{name}/lib/pkgconfig %{buildroot}%{_libdir}/
chmod -x %{buildroot}%{_libdir}/pkgconfig/*.pc

#mkdir -p %{buildroot}/%{_fmoddir}/%{name}
#mv  %{buildroot}%{_includedir}/%{name}/*.mod %{buildroot}/%{_fmoddir}/%{name}/

# Install the module file
mkdir -p %{buildroot}%{_sysconfdir}/modulefiles/mpi
mkdir -p %{buildroot}%{python_sitearch}/%{name}
cp -pr src/packaging/envmods/mpich2.module %{buildroot}%{_sysconfdir}/modulefiles/mpi/%{name}-%{_arch}
sed -i 's#'%{_bindir}'#'%{_libdir}/%{name}/bin'#;s#@LIBDIR@#'%{_libdir}'#;s#@pysitearch@#'%{python_sitearch}'#;s#@ARCH@#'%{_arch}'#' %{buildroot}%{_sysconfdir}/modulefiles/mpi/%{name}-%{_arch}
cp -p %{buildroot}%{_sysconfdir}/modulefiles/mpi/%{name}-%{_arch} %{buildroot}%{_sysconfdir}/modulefiles/%{name}-%{_arch}

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat << EOF > %{buildroot}%{_sysconfdir}/profile.d/mpich2-%{_arch}.sh
# Load mpich2 environment module
module load mpi/%{name}-%{_arch}
EOF
cp -p %{buildroot}%{_sysconfdir}/profile.d/mpich2-%{_arch}.{sh,csh}
 
# Install the RPM macro
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cp -pr %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.%{name}

cp -pr src/mpe2/README src/mpe2/README.mpe2

# Silence rpmlint
sed -i '/^#! \//,1 d' %{buildroot}%{_sysconfdir}/%{name}-%{_arch}/{mpi*.conf,mpe_help.*}

# Work-around the multilib conflicts created by the makefiles
for dirs in collchk graphics logging; do 
  mv %{buildroot}%{_datadir}/%{name}/examples/$dirs/Makefile{,-%{_arch}}
done

# The uninstall script here is not needed/necesary for rpm packaging 
rm -rf %{buildroot}%{_sbindir}/mpe*

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
rm -f %{buildroot}%{_libdir}/%{name}/lib/lib{*mpich*,opa,mpl}.a

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%pre
if [ $1 -gt 1 ] ; then
	if [ -e %{_bindir}/mpiexec.py ] ; then
		/usr/sbin/alternatives --remove mpi-run %{_bindir}/mpiexec.py
	fi
fi

%pre devel
if [ $1 -gt 1 ] ; then
# Remove the old alternative
	if [ -e %{_bindir}/mp%{__isa_bits}-mpicc ] ; then
	/usr/sbin/alternatives --remove mpicc %{_bindir}/mp%{__isa_bits}-mpicc
	fi
fi

%files
%defattr(-,root,root,-)
%doc CHANGES COPYRIGHT README src/mpe2/README.mpe2 RELEASE_NOTES
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/lib
%dir %{_libdir}/%{name}/bin
%{_libdir}/%{name}/lib/*.jar
%{_libdir}/%{name}/lib/mpe*.o
%{_libdir}/%{name}/lib/*.so.*
%{_libdir}/%{name}/bin/*
%config %{_sysconfdir}/%{name}-%{_arch}/
%dir %{python_sitearch}/%{name}
%dir %{_mandir}/%{name}
%doc %{_mandir}/%{name}/man1/
%{_sysconfdir}/modulefiles/mpi/
%{_sysconfdir}/modulefiles/%{name}-%{_arch}
%exclude %{_libdir}/%{name}/bin/*log*
%exclude %{_libdir}/%{name}/bin/jumpshot

%files autoload
%defattr(-,root,root,-)
%{_sysconfdir}/profile.d/mpich2-%{_arch}.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/%{name}/bin/*log*
%{_libdir}/%{name}/bin/jumpshot
%{_includedir}/%{name}-%{_arch}/
#%{_fmoddir}/%{name}/
%{_libdir}/%{name}/lib/*.a
%{_libdir}/%{name}/lib/*.so
%{_libdir}/%{name}/lib/trace_rlog/libTraceInput.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/openpa.pc
%{_datadir}/%{name}/examples/*/Makefile-%{_arch}
%{_sysconfdir}/rpm/macros.%{name}

%files doc
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/doc/
%{_datadir}/%{name}/examples/
%{_mandir}/%{name}/man3/
%{_mandir}/%{name}/man4/
%exclude %{_datadir}/%{name}/examples/*/Makefile-%{_arch}

%changelog
* Wed Mar 20 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5-3
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).
- Fix bogus dates in *.spec.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 1 2012 Orion Poplawski <orion@cora.nwra.com> - 1.5-1
- Update to 1.5
- Drop destdir-fix and mpicxx-und patches
- Update rpm macros to use the new module location

* Wed Oct 31 2012 Orion Poplawski <orion@cora.nwra.com> - 1.4.1p1-9
- Install module file in mpi subdirectory and conflict with other mpi modules
- Leave existing module file location for backwards compatibility for a while

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1p1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.1p1-7
- Rebuild for new hwloc

* Wed Feb 15 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.1p1-6
- Update ARM build configuration

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1p1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan  2 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.4.1p1-4
- Bump spec.

* Wed Nov 16 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.4.1p1-3
- Comply to MPI guidelines by separating autoloading into separate package
  (BZ #647147).

* Tue Oct 18 2011 Deji Akingunola <dakingun@gmail.com> - 1.4.1p1-2
- Rebuild for hwloc soname bump.

* Sun Sep 11 2011 Deji Akingunola <dakingun@gmail.com> - 1.4.1p1-1
- Update to 1.4.1p1 patch update
- Add enable-lib-depend to configure flags

* Sat Aug 27 2011 Deji Akingunola <dakingun@gmail.com> - 1.4.1-1
- Update to 1.4.1 final
- Drop the mpd subpackage, the PM is no longer supported upstream
- Fix undefined symbols in libmpichcxx (again) (#732926)

* Wed Aug 03 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.4-2
- Respect environment module guidelines wrt placement of module file.

* Fri Jun 17 2011 Deji Akingunola <dakingun@gmail.com> - 1.4-1
- Update to 1.4 final

* Tue Mar 29 2011 Deji Akingunola <dakingun@gmail.com> - 1.4-0.1.rc1
- Update to 1.4rc1

* Thu Feb 17 2011 Deji Akingunola <dakingun@gmail.com> - 1.3.2p1-1
- Update to version 1.3.2p1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Deji Akingunola <dakingun@gmail.com> - 1.3.2-1
- Update to 1.3.2

* Tue Jan 04 2011 Deji Akingunola <dakingun@gmail.com> - 1.3.1-2
- Rebuild for hwloc update

* Fri Nov 19 2010 Deji Akingunola <dakingun@gmail.com> - 1.3.1-1
- Update to 1.3.1

* Fri Nov 19 2010 Dan Horák <dan[at]danny.cz> - 1.3-2
- no valgrind on s390(x) yet

* Fri Oct 22 2010 Deji Akingunola <dakingun@gmail.com> - 1.3-1
- Update to 1.3 final

* Tue Oct 19 2010 Deji Akingunola <dakingun@gmail.com> - 1.3-0.1.rc2
- Update to 1.3 RC 2

* Thu Jul 15 2010 Dan Horák <dan[at]danny.cz> - 1.2.1p1-4
- build with -fPIC on s390

* Tue May 04 2010 Deji Akingunola <dakingun@gmail.com> - 1.2.1p1-3
- Fix multi-lib conflicts (BZ #577081)

* Tue Mar 02 2010 Deji Akingunola <dakingun@gmail.com> - 1.2.1p1-2
- Prevent the rpath link option from being included in the compiler wrappers

* Tue Feb 23 2010 Deji Akingunola <dakingun@gmail.com> - 1.2.1p1-1
- Update to 1.2.1p1
- Ship the mpi compilers in the main package
- Remove alternatives support
- Add script to load mpich2 module on login

* Mon Feb 08 2010 Deji Akingunola <dakingun@gmail.com> - 1.2.1-5
- Properly remove the lib*mpich2*.a files
- Backport the upstream fix for mpdboot hangs.
- add the m_option macro to replace hardcoding -m{__isa_bits}
  and define it correctly for s390, where __isa_bits is 32, but
  the option to pass to gcc et all is -m31. (Jay Fenlason )
- Remove the *.a libs that have the shared version
- Place the rpm macro in the -devel subpackage

* Thu Nov 26 2009 Deji Akingunola <dakingun@gmail.com> - 1.2.1-2
- Fix the mpich2.module patch.

* Tue Nov 10 2009 Deji Akingunola <dakingun@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Tue Nov 03 2009 Deji Akingunola <dakingun@gmail.com> - 1.2-2
- Backport upstream patch to workaround changes in Python behaviour in F-12
- Clean-up the spec file to remove its 'Fedora-ness'.

* Sat Oct 10 2009 Deji Akingunola <dakingun@gmail.com> - 1.2-1
- Adapt to the Fedora MPI packaging guildelines
- Split out a -doc subpackage
- New upstream version, v1.2

* Tue Aug 11 2009 Deji Akingunola <dakingun@gmail.com> - 1.1.1p1-1
- New upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Deji Akingunola <dakingun@gmail.com> - 1.1.1-1
- Update to 1.1.1
- Remove (and obsolete) the -libs subpackage, it is not necessary.
- Change e2fsprogs BR to libuuid

* Wed May 20 2009 Deji Akingunola <dakingun@gmail.com> - 1.1-1
- Update to 1.1

* Wed May 20 2009 Deji Akingunola <dakingun@gmail.com> - 1.1-0.4.rc1
- Install the libdir under /etc/ld.so.conf.d

* Mon May 18 2009 Deji Akingunola <dakingun@gmail.com> - 1.1-0.3.rc1
- Update to 1.1rc1
- Update spec to follow the proposed packaging guildelines wrt using alternatives
- Also change to use the global macro instead of define.

* Sun Mar 29 2009 Deji Akingunola <dakingun@gmail.com> - 1.1-0.2.b1
- Specifically build with openjdk Java, so Jumpshot works (Anthony Chan)

* Wed Mar 18 2009 Deji Akingunola <dakingun@gmail.com> - 1.1-0.1.b1
- Update for the 1.1 (beta) release
- Stop building with dllchan, it is not fully supported
- Fix un-owned directory (#490270)
- Add Posttrans scriplets to work around 1.0.8-3 scriplet brokenness

* Mon Mar 09 2009 Deji Akingunola <dakingun@gmail.com> - 1.0.8-3
- Drop the ssm channel from ppc* archs, it fails to build
- Python scripts in bindir and sbindir are no longer bytecompiled (F-11+)
- Enhance the spec file to support ia64 and sparc
- Include mpiexec and mpirun (symlinks) in the environment module bindir 

* Fri Mar 06 2009 Deji Akingunola <dakingun@gmail.com> - 1.0.8-2
- Fix the source url, pointed out from package review
- Finally accepted to go into Fedora

* Fri Oct 24 2008 Deji Akingunola <dakingun@gmail.com> - 1.0.8-1
- Update to the 1.0.8
- Configure with the default nemesis channel

* Fri May 16 2008 Deji Akingunola <dakingun@gmail.com> - 1.0.7-5
- Update the alternate compiler/compiler flags macro to allow overriding it
  from command-line

* Wed Apr 16 2008 Deji Akingunola <dakingun@gmail.com> - 1.0.7-4
- Apply patch from Orion Poplawski to silence rpmlint

* Tue Apr 15 2008 Deji Akingunola <dakingun@gmail.com> - 1.0.7-3
- Add a note on the device/channels configuration options used, and
- Fix logfile listings as suggested by Orion Poplawski (Package review, 171993)

* Tue Apr 15 2008 Deji Akingunola <dakingun@gmail.com> - 1.0.7-2
- Fix the source url

* Sat Apr 05 2008 Deji Akingunola <dakingun@gmail.com> - 1.0.7-1
- Update to 1.0.7

* Mon Oct 15 2007 Deji Akingunola <dakingun@gmail.com> - 1.0.6p1-1
- Update to 1.0.6p1

* Mon Oct 15 2007 Deji Akingunola <dakingun@gmail.com> - 1.0.6-1
- New version upgrade

* Tue Jul 31 2007 Deji Akingunola <dakingun@gmail.com> - 1.0.5p4-4
- Create a -mpi-manpages subpackage for the MPI routines manuals

* Fri Jul 27 2007 Deji Akingunola <dakingun@gmail.com> - 1.0.5p4-3
- Fix java-gcj-compat BR
- Handle upgrades in the post scripts

* Tue Jun 12 2007 Deji Akingunola <dakingun@gmail.com> - 1.0.5p4-2
- Fix typos and make other adjustments arising from Fedora package reviews

* Tue Jun 12 2007 Deji Akingunola <dakingun@gmail.com> - 1.0.5p4-1
- Patch #4 release

* Mon Feb 12 2007 Deji Akingunola <dakingun@gmail.com> - 1.0.5p2-1
- Patch #2 release

* Tue Jan 09 2007 Deji Akingunola <dakingun@gmail.com> - 1.0.5p1-1
- New release with manpages
- Create a -libs subpackage as it's done in Fedora's openmpi to help with
  multi-libs packaging
- Disable modules support (until I can properly figure it out)

* Wed Dec 27 2006 Deji Akingunola <dakingun@gmail.com> - 1.0.5-1
- New release

* Sat Nov 18 2006 Deji Akingunola <dakingun@gmail.com> - 1.0.4p1-2
- Set the java_sdk directory so all java bit work  

* Sat Sep 02 2006 Deji Akingunola <dakingun@gmail.com> - 1.0.4p1-1
- Update to version 1.0.4p1
- Cleanup up spec file to use alternatives similarly to FC's openmpi

* Wed Aug 02 2006 Deji Akingunola <dakingun@gmail.com> - 1.0.4-1
- Update to version 1.0.4

* Thu May 18 2006 Deji Akingunola <dakingun@gmail.com> - 1.0.3-3
- Add missing BRs (Orion Polawski)

* Mon Apr 10 2006 Deji Akingunola <dakingun@gmail.com> - 1.0.3-2
- Rewrite the spec, borrowing extensively from openmpi's spec by Jason Vas Dias
- Allows use of environment modules and alternatives

* Fri Nov 25 2005 Deji Akingunola <dakingun@gmail.com> - 1.0.3-1
- Update to new version

* Sat Oct 15 2005 Deji Akingunola <deji.aking@gmail.com> - 1.0.2p1-1
- Initial package
