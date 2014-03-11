# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

Name:		trinity-dbus-tqt
Version:	3.5.13.2
Release:	1%{?dist}%{?_variant}
License:	GPL
Summary:	Dbus TQT Interface
Group:		System Environment/Libraries

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	dbus-tqt-trinity-%{version}.tar.xz

# [dbus-tqt] Fix build on RHEL 4
Patch1:		dbus-tqt-3.5.13-fix_old_dbus_types.patch

BuildRequires:	gcc-c++
%if 0%{?suse_version}
BuildRequires:	dbus-1-devel
%else
BuildRequires:	dbus-devel
%endif
BuildRequires:	trinity-tqtinterface-devel >= %{version}

# TDE 3.5.13 specific building variables
BuildRequires:	cmake >= 2.8
BuildRequires:	qt-devel

Requires:		qt

Obsoletes:		dbus-tqt < %{version}-%{release}
Provides:		dbus-tqt = %{version}-%{release}


%description
Dbus TQT Interface


%package devel
Requires:		%{name}
Summary:		%{name} - Development files
Group:			Development/Libraries

Obsoletes:		dbus-tqt-devel < %{version}-%{release}
Provides:		dbus-tqt-devel = %{version}-%{release}

%description devel
Development files for %{name}


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n dbus-tqt-trinity-%{version}

%if 0%{?rhel} == 4
%patch1 -p1 -b .dbustypes
%endif

%build
unset QTDIR || : ; . /etc/profile.d/qt3.sh
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

%if 0%{?rhel} == 4
export CXXFLAGS="-DDBUS_API_SUBJECT_TO_CHANGE ${CXXFLAGS}"
%endif

%if 0%{?rhel} || 0%{?fedora} || 0%{?suse_version}
%__mkdir_p build
cd build
%endif

%cmake \
  -DTDE_PREFIX=%{tde_prefix} \
  -DINCLUDE_INSTALL_DIR=%{tde_includedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  ..

%__make %{?_smp_mflags}


%install
%__rm -rf %{?buildroot}
%__make install DESTDIR=%{?buildroot} -C build

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
%{tde_libdir}/libdbus-tqt-1.so.0
%{tde_libdir}/libdbus-tqt-1.so.0.0.0

%files devel
%{tde_includedir}/dbus-1.0/*
%{tde_libdir}/libdbus-tqt-1.so
%{tde_libdir}/libdbus-tqt-1.la
%{tde_libdir}/pkgconfig/dbus-tqt.pc

%changelog
* Tue Sep 11 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial build for TDE 3.5.13.1
