# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%define cmake_modules_dir %{tde_prefix}/share/cmake
%else
%define cmake_modules_dir %{_datadir}/cmake/Modules
%endif

# TQT include files may conflict with QT4 includes, so we move them to a subdirectory.
# Later compiled Trinity products should be aware of that !
%define tde_bindir %{tde_prefix}/bin
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

Name:		trinity-tqtinterface
Version:	3.5.13.2
Release:	1%{?dist}%{?_variant}
License:	GPL
Summary:	Trinity QT Interface
Group:		System Environment/Libraries

Vendor:		Trinity Project
URL:		http://www.trinitydesktop.org/
Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:	tqtinterface-trinity-%{version}.tar.xz

# [tqtinterface] Add missing endian-ness defines [Bug #727] [Commit #458e74a6]
Patch1:		tqtinterface-3.5.13-add_missing_endianness_defines.patch

# TDE 3.5.13 specific building variables
BuildRequires:	cmake >= 2.8
BuildRequires:	qt-devel
Requires:		qt

BuildRequires:	gcc-c++
%if 0%{?rhel} == 4
BuildRequires:	xorg-x11-devel
%else
BuildRequires:	pth-devel
%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}xi-devel
%else
BuildRequires:	libXi-devel
%endif
%endif

Obsoletes:	tqtinterface < %{version}-%{release}
Provides:	tqtinterface = %{version}-%{release}


%description
Trinity QT Interface

%package devel
Group:		Development/Libraries
Summary:	%{name} - Development files
Requires:	%{name} = %{version}-%{release}
Requires:	qt-devel

Obsoletes:	tqtinterface-devel < %{version}-%{release}
Provides:	tqtinterface-devel = %{version}-%{release}

%description devel
Development files for %{name}

%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n tqtinterface-trinity-%{version}
%patch1 -p1

%build
unset QTDIR; . /etc/profile.d/qt3.sh

%if 0%{?rhel} || 0%{?fedora} || 0%{?suse_version}
%__mkdir_p build
cd build
%endif

# Note: specifying 'QT_LIBRARY_DIR' allow using QT3 libraries under
#  another directory than QT3_PREFIX. (E.g. Mageia 2, Mandriva ...)
#  Otherwise, it defaults to ${QTDIR}/lib !
%cmake \
  -DQT_PREFIX_DIR=${QTDIR} \
  -DQT_VERSION=3 \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DINCLUDE_INSTALL_DIR=%{tde_includedir}/tqt \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DPKGCONFIG_INSTALL_DIR=%{tde_libdir}/pkgconfig \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DQT_LIBRARY_DIR=${QTLIB:-${QTDIR}/%{_lib}} \
  ..

%__make %{?_smp_mflags}


%install
%__rm -rf %{?buildroot}
%__mkdir_p %{?buildroot}%{_includedir}
%__make install DESTDIR=%{?buildroot} -C build

# RHEL 5: add newline at end of include files to avoid warnings
%if 0%{?rhel} && 0%{?rhel} <= 5
for i in %{?buildroot}%{tde_includedir}/tqt/*.h; do
  echo "" >>${i}
done
%endif

# Install 'cmake' modules for development use
%__mkdir_p %{?buildroot}%{cmake_modules_dir}
for i in cmake/modules/*.cmake; do
  %__install -m 644 $i %{?buildroot}%{cmake_modules_dir}
done

%clean
%__rm -rf %{?buildroot}

%post
/sbin/ldconfig || :

%postun
/sbin/ldconfig || :

%post devel
/sbin/ldconfig || :

%postun devel
/sbin/ldconfig || :

%files
%{tde_bindir}/*
%{tde_libdir}/*.so.*

%files devel
%{tde_includedir}/tqt
%{tde_libdir}/*.so
%{tde_libdir}/*.la
%{tde_libdir}/pkgconfig/*.pc
%{cmake_modules_dir}/*.cmake


%changelog
* Tue Sep 11 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Switch to v3.5.13-sru branch
