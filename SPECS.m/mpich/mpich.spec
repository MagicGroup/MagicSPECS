%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	A high-performance implementation of MPI
Summary(zh_CN.UTF-8): MPI 的一个高性能实现
Name:		mpich
Version: 3.1.4
Release: 10%{?dist}
License:	MIT
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:		http://www.mpich.org/

Source0:	http://www.mpich.org/static/downloads/%{version}/%{name}-%{version}.tar.gz
Source1:	mpich.macros	
Source2:	mpich.pth.py2
Source3:	mpich.pth.py3
Patch0:		mpich-modules.patch

BuildRequires:	gcc-gfortran
BuildRequires:  hwloc-devel >= 1.8
%ifnarch s390 
BuildRequires:	valgrind-devel
%endif
# For python[23]_sitearch
BuildRequires:  python2-devel
BuildRequires:  python3-devel
BuildRequires:  rpm-mpi-hooks
Provides:	mpi
Provides:	mpich2 = 3.0.1
Obsoletes:	mpich2 < 3.0
Requires:	environment-modules

%description
MPICH is a high-performance and widely portable implementation of the Message
Passing Interface (MPI) standard (MPI-1, MPI-2 and MPI-3). The goals of MPICH
are: (1) to provide an MPI implementation that efficiently supports different
computation and communication platforms including commodity clusters (desktop
systems, shared-memory systems, multicore architectures), high-speed networks
(10 Gigabit Ethernet, InfiniBand, Myrinet, Quadrics) and proprietary high-end
computing systems (Blue Gene, Cray) and (2) to enable cutting-edge research in
MPI through an easy-to-extend modular framework for other derived
implementations.

The mpich binaries in this RPM packages were configured to use the default
process manager (Hydra) using the default device (ch3). The ch3 device
was configured with support for the nemesis channel that allows for
shared-memory and TCP/IP sockets based communication.

This build also include support for using the 'module environment' to select
which MPI implementation to use when multiple implementations are installed.
If you want MPICH support to be automatically loaded, you need to install the
mpich-autoload package.

%description -l zh_CN.UTF-8
MPI 的一个高性能实现。

%package autoload
Summary:	Load mpich automatically into profile
Summary(zh_CN.UTF-8): 自动载入 mpich 到配置文件
Group:		System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Requires:	mpich = %{version}-%{release}
Provides:	mpich2-autoload = 3.0.1
Obsoletes:	mpich2-autoload < 3.0

%description autoload
This package contains profile files that make mpich automatically loaded.

%description autoload -l zh_CN.UTF-8
自动载入 mpich 到配置文件。

%package devel
Summary:	Development files for mpich
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Provides:	%{name}-devel-static = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	gcc-gfortran 
Provides:	mpich2-devel = 3.0.1
Obsoletes:	mpich2-devel < 3.0

%description devel
Contains development headers and libraries for mpich

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary:	Documentations and examples for mpich
Summary(zh_CN.UTF-8): %{name} 的文档和样例
Group:		Documentation
Group(zh_CN.UTF-8): 文档
BuildArch:	noarch
Requires:	%{name}-devel = %{version}-%{release}
Provides:	mpich2-doc = 3.0.1
Obsoletes:	mpich2-doc < 3.0

%description doc
Contains documentations, examples and man-pages for mpich

%description doc -l zh_CN.UTF-8
%{name} 的文档和样例。

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
%global m_option "-mabi=64"
%endif

%ifarch %{arm} aarch64
%global m_option ""
%endif

%ifarch %{ix86} x86_64
%global selected_channels ch3:nemesis
%else
%global selected_channels ch3:sock
%endif

%ifarch %{ix86} x86_64 s390 %{arm} aarch64
%global XFLAGS -fPIC
%endif

%prep
%autosetup -p0

%build
%configure	\
	--enable-sharedlibs=gcc					\
	--enable-shared						\
	--enable-static=no					\
	--enable-lib-depend					\
	--disable-rpath						\
	--disable-silent-rules					\
	--enable-fc						\
	--with-device=%{selected_channels}			\
	--with-pm=hydra:gforker					\
	--includedir=%{_includedir}/%{name}-%{_arch}		\
	--bindir=%{_libdir}/%{name}/bin				\
	--libdir=%{_libdir}/%{name}/lib				\
	--datadir=%{_datadir}/%{name}				\
	--mandir=%{_mandir}/%{name}				\
	--docdir=%{_datadir}/%{name}/doc			\
	--htmldir=%{_datadir}/%{name}/doc			\
	--with-hwloc-prefix=system				\
	FC=%{opt_fc}						\
	F77=%{opt_f77}						\
	CFLAGS="%{m_option} -O2 %{?XFLAGS}"			\
	CXXFLAGS="%{m_option} -O2 %{?XFLAGS}"			\
	FCFLAGS="%{m_option} -O2 %{?XFLAGS}"			\
	FFLAGS="%{m_option} -O2 %{?XFLAGS}"			\
	LDFLAGS='-Wl,-z,noexecstack'				\
	MPICHLIB_CFLAGS="%{?opt_cc_cflags}"			\
	MPICHLIB_CXXFLAGS="%{optflags}"				\
	MPICHLIB_FCFLAGS="%{?opt_fc_fflags}"			\
	MPICHLIB_FFLAGS="%{?opt_f77_fflags}"	
#	MPICHLIB_LDFLAGS='-Wl,-z,noexecstack'			\
#	MPICH_MPICC_FLAGS="%{m_option} -O2 %{?XFLAGS}"	\
#	MPICH_MPICXX_FLAGS="%{m_option} -O2 %{?XFLAGS}"	\
#	MPICH_MPIFC_FLAGS="%{m_option} -O2 %{?XFLAGS}"	\
#	MPICH_MPIF77_FLAGS="%{m_option} -O2 %{?XFLAGS}"
#	--with-openpa-prefix=embe%description -l zh_CN.UTF-8ed				\

#	FCFLAGS="%{?opt_fc_fflags} -I%{_fmo%description -l zh_CN.UTF-8ir}/%{name} %{?XFLAGS}"	\

#Try and work around 'unused-direct-shlib-dependency' rpmlint warnning
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags} VERBOSE=1

%install
make DESTDIR=%{buildroot} install

#mkdir -p %{buildroot}/%{_fmo%description -l zh_CN.UTF-8ir}/%{name}
#mv  %{buildroot}%{_includedir}/%{name}/*.mod %{buildroot}/%{_fmo%description -l zh_CN.UTF-8ir}/%{name}/

# Install the module file
mkdir -p %{buildroot}%{_sysconfdir}/modulefiles/mpi
sed 's#%{_bindir}#%{_libdir}/%{name}/bin#;
     s#@LIBDIR@#%{_libdir}/%{name}#;
     s#@MPINAME@#%{name}#;
     s#@py2sitearch@#%{python2_sitearch}#;
     s#@py3sitearch@#%{python3_sitearch}#;
     s#@ARCH@#%{_arch}#' \
     <src/packaging/envmods/mpich.module \
     >%{buildroot}%{_sysconfdir}/modulefiles/mpi/%{name}-%{_arch}

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat << EOF > %{buildroot}%{_sysconfdir}/profile.d/mpich-%{_arch}.sh
# Load mpich environment module
module load mpi/%{name}-%{_arch}
EOF
cp -p %{buildroot}%{_sysconfdir}/profile.d/mpich-%{_arch}.{sh,csh}
 
# Install the RPM macros
install -pDm0644 %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d/macros.%{name}

# Install the .pth files
mkdir -p %{buildroot}%{python2_sitearch}/%{name}
install -pDm0644 %{SOURCE2} %{buildroot}%{python2_sitearch}/%{name}.pth
mkdir -p %{buildroot}%{python3_sitearch}/%{name}
install -pDm0644 %{SOURCE3} %{buildroot}%{python3_sitearch}/%{name}.pth

find %{buildroot} -type f -name "*.la" -delete

%check
make check VERBOSE=1

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYRIGHT
%doc CHANGES README README.envvar RELEASE_NOTES
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/lib
%dir %{_libdir}/%{name}/bin
%{_libdir}/%{name}/lib/*.so.*
%{_libdir}/%{name}/bin/*
%dir %{python2_sitearch}/%{name}
%{python2_sitearch}/%{name}.pth
%dir %{python3_sitearch}/%{name}
%{python3_sitearch}/%{name}.pth
%dir %{_mandir}/%{name}
%doc %{_mandir}/%{name}/man1/
%{_sysconfdir}/modulefiles/mpi/

%files autoload
%{_sysconfdir}/profile.d/mpich-%{_arch}.*

%files devel
%{_includedir}/%{name}-%{_arch}/
%{_libdir}/%{name}/lib/pkgconfig/
##%%{_fmo%description -l zh_CN.UTF-8ir}/%%{name}/
%{_libdir}/%{name}/lib/*.so
%{_rpmconfigdir}/macros.d/macros.%{name}

%files doc
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/doc/
%{_mandir}/%{name}/man3/

%changelog
* Tue Nov 17 2015 Liu Di <liudidi@gmail.com> - 3.1.4-10
- 为 Magic 3.0 重建

* Tue Nov 17 2015 Liu Di <liudidi@gmail.com> - 3.1.4-9
- 为 Magic 3.0 重建

* Mon Nov 16 2015 Liu Di <liudidi@gmail.com> - 3.1.4-8
- 为 Magic 3.0 重建

* Mon Nov 16 2015 Liu Di <liudidi@gmail.com> - 3.1.4-7
- 为 Magic 3.0 重建

* Mon Nov 16 2015 Liu Di <liudidi@gmail.com> - 3.1.4-6
- 为 Magic 3.0 重建

* Mon Nov 16 2015 Liu Di <liudidi@gmail.com> - 3.1.4-5
- 为 Magic 3.0 重建

* Mon Nov 16 2015 Liu Di <liudidi@gmail.com> - 3.1.4-4
- 为 Magic 3.0 重建

* Mon Nov 16 2015 Liu Di <liudidi@gmail.com> - 3.1.4-3
- 为 Magic 3.0 重建

* Mon Nov 16 2015 Liu Di <liudidi@gmail.com> - 3.1.4-2
- 为 Magic 3.0 重建

* Mon Nov 16 2015 Liu Di <liudidi@gmail.com> - 3.1.4-1
- 为 Magic 3.0 重建

* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 3.1.3-2
- 为 Magic 3.0 重建

* Fri Dec 26 2014 Liu Di <liudidi@gmail.com> - 3.1.3-1
- 更新到 3.1.3

* Fri Feb 21 2014 Ville Skyttä <ville.skytta@iki.fi> - 3.1-2
- Install rpm macros to %%{_rpmconfigdir}/macros.d as non-%%config.

* Fri Feb 21 2014 Deji Akingunola <dakingun@gmail.com> - 3.1-1
- Update to 3.1

* Mon Jan  6 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.0.4-7
- Set the aarch64 compiler options

* Fri Dec 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.0.4-6
- Now have valgrind on ARMv7
- No valgrind on aarch64

* Fri Aug 23 2013 Orion Poplawski <orion@cora.nwra.com> - 3.0.4-5
- Add %%check

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Deji Akingunola <dakingun@gmail.com> - 3.0.4-3
- Add proper Provides and Obsoletes for the sub-packages  

* Thu Jul 18 2013 Deji Akingunola <dakingun@gmail.com> - 3.0.4-2
- Fix some of the rpmlint warnings from package review (BZ #973493) 

* Wed Jun 12 2013 Deji Akingunola <dakingun@gmail.com> - 3.0.4-1
- Update to 3.0.4

* Thu Feb 21 2013 Deji Akingunola <dakingun@gmail.com> - 3.0.2-1
- Update to 3.0.2
- Rename to mpich.
- Drop check for old alternatives' installation

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
