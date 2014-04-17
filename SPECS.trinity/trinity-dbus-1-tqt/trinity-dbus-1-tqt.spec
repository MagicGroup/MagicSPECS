# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

%define tde_bindir %{tde_prefix}/bin
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

Name:		trinity-dbus-1-tqt
Version:	3.5.13.2
Release:	1%{?dist}%{?_variant}
License:	GPL
Summary:	Dbus TQT Interface
Group:		System Environment/Libraries

Obsoletes:		dbus-1-tqt < %{version}-%{release}
Provides:		dbus-1-tqt = %{version}-%{release}

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	dbus-1-tqt-trinity-%{version}.tar.xz

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


%description
Dbus TQT Interface


%package devel
Requires:	%{name}
Summary:	%{name} - Development files
Group:		Development/Libraries

Obsoletes:		dbus-1-tqt-devel < %{version}-%{release}
Provides:		dbus-1-tqt-devel = %{version}-%{release}

%description devel
Development files for %{name}

%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n dbus-1-tqt-trinity-%{version}

%build
unset QTDIR || : ; . /etc/profile.d/qt?.sh
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

%if 0%{?rhel} || 0%{?fedora} || 0%{?suse_version}
%__mkdir_p build
cd build
%endif

%cmake \
  -DTDE_PREFIX=%{tde_prefix} \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
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
%{tde_bindir}/dbusxml2qt3
%{tde_libdir}/libdbus-1-tqt.so.0
%{tde_libdir}/libdbus-1-tqt.so.0.0.0

%files devel
%{tde_includedir}/*.h
%{tde_libdir}/libdbus-1-tqt.so
%{tde_libdir}/libdbus-1-tqt.la
%{tde_libdir}/pkgconfig/*.pc

%changelog
* Tue Sep 11 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial build for TDE 3.5.13.1
