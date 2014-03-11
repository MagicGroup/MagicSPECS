# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_includedir %{tde_prefix}/include
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_libdir %{tde_prefix}/%{_lib}


Name:		trinity-avahi-tqt
Version:	3.5.13.2
Release:	1%{?dist}%{?_variant}
License:	GPL
Summary:	Avahi TQT Interface
Group:		System Environment/Libraries

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	avahi-tqt-trinity-%{version}.tar.xz

BuildRequires:	gcc-c++
BuildRequires:	cmake >= 2.8
BuildRequires:	qt-devel
BuildRequires:	tqtinterface-devel >= 3.5.13.1
BuildRequires:	gettext-devel
BuildRequires:	libtool
%if 0%{?suse_version}
BuildRequires:	dbus-1-devel
%else
BuildRequires:	dbus-devel
%endif

%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}avahi-client-devel
# On Mageia 2, package is 'lib64expat1-devel', but on Mandriva, 'lib64expat-devel'
BuildRequires:	%{_lib}expat%{?mgaversion:1}-devel
Provides:		%{_lib}avahi-qt3
%else
BuildRequires:	avahi-devel
%if 0%{?suse_version}
BuildRequires:	libexpat-devel
%else
BuildRequires:	expat-devel
%endif
%endif

Requires:		qt
Requires:		trinity-tqtinterface >= 3.5.13

Obsoletes:		avahi-tqt < %{version}-%{release}
Provides:		avahi-tqt = %{version}-%{release}


%description
Avahi TQT Interface


%package devel
Requires:	%{name}
Summary:	%{name} - Development files
Group:		Development/Libraries

%if 0%{?mgaversion} || 0%{?mdkversion}
Provides:		%{_lib}avahi-qt3-devel
%endif

Obsoletes:		avahi-tqt-devel < %{version}-%{release}
Provides:		avahi-tqt-devel = %{version}-%{release}

%description devel
Development files for %{name}


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n avahi-tqt-trinity-%{version}

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i "acinclude.m4" \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g"

%__cp -f "/usr/share/libtool/config/ltmain.sh" "./ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "./ltmain.sh"

# Removes stale libtool stuff
%__rm -f common/libtool.m4 common/ltoptions.m4 common/lt~obsolete.m4 common/ltsugar.m4 common/ltversion.m4

%build
unset QTDIR || : ; . /etc/profile.d/qt.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir} -I%{tde_includedir}/tqt"
export CXXFLAGS="${CXXFLAGS} ${LDFLAGS}"

./autogen.sh

%configure \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --docdir=%{tde_docdir} \
  --includedir=%{tde_includedir} \
  --libdir=%{tde_libdir} \
  --enable-compat-libdns_sd \
  --with-systemdsystemunitdir=/lib/systemd/system  \
  MOC_QT3=%{tde_bindir}/moc-tqt

%__make %{?_smp_mflags}

%install
%__rm -rf %{?buildroot}
%__make install DESTDIR=%{?buildroot}

# Removes '.a' file
%__rm -f %{?buildroot}%{tde_libdir}/libavahi-tqt.a

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
%{tde_libdir}/libavahi-tqt.so.1
%{tde_libdir}/libavahi-tqt.so.1.0.0

%files devel
%{tde_includedir}/avahi-tqt/
%{tde_libdir}/libavahi-tqt.so
%{tde_libdir}/libavahi-tqt.la
%{tde_libdir}/pkgconfig/avahi-tqt.pc

%changelog
* Tue Sep 11 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial build for TDE 3.5.13.1
