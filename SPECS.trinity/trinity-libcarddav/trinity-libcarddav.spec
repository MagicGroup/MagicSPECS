#
# spec file for package libcarddav (version R14)
#
# Copyright (c) 2014 Trinity Desktop Environment
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.0
%endif
%define tde_pkg libcarddav
%define tde_prefix /opt/trinity
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define libcarddav %{_lib}carddav
%else
%define libcarddav libcarddav
%endif


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.6.2
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}
Summary:	A portable CardDAV client implementation
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Deskio
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		/usr
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		libcarddav-14.0.1-rhel5.patch

BuildRequires:	make
BuildRequires:	libtool

# CURL support
%if 0%{?fedora} || 0%{?rhel} >= 6 || 0%{?suse_version} || 0%{?mgaversion} || 0%{?mdkversion}
%define libcurl_devel libcurl-devel >= 7.15.5
%else
# Specific CURL version for TDE on RHEL 5 (and older)
%define libcurl_devel curl-devel >= 7.15.5
%endif
%{?libcurl_devel:BuildRequires: %{libcurl_devel}}

# GTK2 support
%if 0%{?rhel} == 4
BuildRequires:	evolution28-gtk2-devel
%else
BuildRequires:	glib2-devel
BuildRequires:	gtk2-devel
%endif

%description
Libcarddav is a portable CardDAV client implementation originally developed for the Trinity PIM suite. 
It incorporates full list, get, add, modify, and delete functionality per the latest CardDAV standards. 
Build dependencies are minimal, requiring only libcurl.

##########

%package -n %{libcarddav}0
Summary:	A portable CardDAV client implementation
Group:		System/Libraries

Obsoletes:	trinity-libcarddav < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-libcarddav = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	libcarddav = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libcarddav}0
Libcarddav is a portable CardDAV client implementation originally developed for the Trinity PIM suite. 
It incorporates full list, get, add, modify, and delete functionality per the latest CardDAV standards. 
Build dependencies are minimal, requiring only libcurl.

%files -n %{libcarddav}0
%defattr(-,root,root,-)
%{_libdir}/libcarddav.so.0
%{_libdir}/libcarddav.so.0.0.6

%post -n %{libcarddav}0
/sbin/ldconfig

%postun -n %{libcarddav}0
/sbin/ldconfig


##########

%package -n %{libcarddav}-devel
Summary:	A portable CardDAV client implementation (Development Files)
Group:		Development/Libraries/Other
Requires:	%{libcarddav}0 = %{?epoch:%{epoch}:}%{version}-%{release}
%{?libcurl_devel:Requires: %{libcurl_devel}}
Requires:	glib2-devel

Obsoletes:	trinity-libcarddav-devel < %{version}-%{release}
Provides:	trinity-libcarddav-devel = %{version}-%{release}
Provides:	libcarddav-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libcarddav}-devel
Libcarddav is a portable CardDAV client implementation originally developed for the Trinity PIM suite. 
It incorporates full list, get, add, modify, and delete functionality per the latest CardDAV standards. 
Build dependencies are minimal, requiring only libcurl.

This package contains the development files.

%files -n %{libcarddav}-devel
%defattr(-,root,root,-)
%{_includedir}/libcarddav/
%{_libdir}/libcarddav.la
%{_libdir}/libcarddav.so
%{_libdir}/pkgconfig/libcarddav.pc

%post -n %{libcarddav}-devel
/sbin/ldconfig

%postun -n %{libcarddav}-devel
/sbin/ldconfig

##########

%if 0%{?pclinuxos} || 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%if 0%{?rhel} == 5
%patch1 -p1 -b .ftbfs
%endif

# Fix empty ChangeLog cause invalid macro in 'configure.ac'
echo "%{name} (%{version})" >ChangeLog

autoreconf -fiv


%build
unset QTDIR QTINC QTLIB

# CFLAGS required if CURL is installed on /opt/trinity, e.g. RHEL 5
export CFLAGS="-I%{tde_includedir} -L%{tde_libdir} ${RPM_OPT_FLAGS}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

# RHEL4 stuff
if [ -d /usr/evolution28 ]; then
  export PKG_CONFIG_PATH="/usr/evolution28/%{_lib}/pkgconfig:${PKG_CONFIG_PATH}"
fi

%configure \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  \
  --disable-dependency-tracking

%__make %{?_smp_mflags}


%install
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# Unwanted files
%__rm -f %{buildroot}%{_libdir}/libcarddav.a


%clean
%__rm -rf %{buildroot}


%Changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.6.2-1
- Initial release for TDE R14.0.0
