# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

Name:		trinity-libcarddav
Version:	0.6.2
Release:	3%{?dist}%{?_variant}

Vendor:		Trinity Project
URL:		http://www.trinitydesktop.org/
Packager:	Francois Andriot <francois.andriot@free.fr>

License:	GPL
Group:		System Environment/Libraries
Summary:	A portable CardDAV client implementation originally developed for the Trinity PIM suite.

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	libcarddav_0.6.2-2debian2.tar.gz

# [libcarddav] Fix messy installation directories
Patch1:		libcarddav-0.6.5-fix_installation.patch

%if 0%{?fedora} || 0%{?rhel} >= 6 || 0%{?suse_version}
BuildRequires:	libcurl-devel
%else
%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}curl-devel
%else
# Specific CURL version for TDE on RHEL 5 (and older)
BuildRequires:	trinity-libcurl-devel
%endif
%endif

Obsoletes:	libcarddav < %{version}-%{release}
Provides:	libcarddav = %{version}-%{release}

%description
Libcarddav is a portable CardDAV client implementation originally developed for the Trinity PIM suite. 
It incorporates full list, get, add, modify, and delete functionality per the latest CardDAV standards. 
Build dependencies are minimal, requiring only libcurl.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}

Obsoletes:	libcarddav-devel < %{version}-%{release}
Provides:	libcarddav-devel = %{version}-%{release}

%description devel
%{summary}


%prep
%setup -q -n libcarddav-%{version}
%patch1 -p1 -b .dir

%build
# CFLAGS required if CURL is installed on /opt/trinity, e.g. RHEL 5
export CFLAGS="-I%{tde_includedir} -L%{tde_libdir} ${CFLAGS}"

autoreconf --force --install --symlink
%configure \
  --includedir=%{tde_includedir} \
  --libdir=%{tde_libdir} \
  
%__make %{?_smp_mflags} LIBTOOL=$(which libtool)

%install
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot} LIBTOOL=$(which libtool)

%__rm -f %{buildroot}%{tde_libdir}/libcarddav.a

%clean
%__rm -rf %{buildroot}


%files
%{tde_libdir}/*.so.*

%files devel
%{tde_includedir}/*.h
%{tde_libdir}/*.la
%{tde_libdir}/*.so
%{tde_libdir}/pkgconfig/libcarddav.pc

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post devel
/sbin/ldconfig

%postun devel
/sbin/ldconfig


%Changelog
* Sun Jul 28 2012 Francois Andriot <francois.andriot@free.fr> - 0.6.5-3
- Renames to 'trinity-libcaldav'
- Build on MGA2

* Sun Oct 30 2011 Francois Andriot <francois.andriot@free.fr> - 0.6.5-2debian2 .1
- Initial build for RHEL 6, RHEL 5, and Fedora 15
