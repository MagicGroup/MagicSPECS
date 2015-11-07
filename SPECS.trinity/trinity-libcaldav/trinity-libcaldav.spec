#
# spec file for package libcaldav (version R14)
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
%define tde_version 14.0.1
%endif
%define tde_pkg libcaldav
%define tde_prefix /opt/trinity
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define libcaldav %{_lib}caldav
%else
%define libcaldav libcaldav
%endif


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.6.5
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1
Summary:	A client library that adds support for the CalDAV protocol (rfc4791)
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		/usr
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		trinity-libcaldav-14.0.1-tqt.patch

BuildRequires:	make
BuildRequires:	libtool
BuildRequires:	fdupes

# GTK2 support
BuildRequires:	glib2-devel
BuildRequires:	gtk2-devel

# CURL support
%define libcurl_devel libcurl-devel >= 7.15.5
%{?libcurl_devel:BuildRequires: %{libcurl_devel}}

%description
libcaldev is a client library that adds support for the CalDAV protocol (rfc4791).
The object is to have a library which fully implements the protocol so that it is
easy to integrate CalDAV support into any PIM application.

##########

%package -n %{libcaldav}0
Summary:	A client library that adds support for the CalDAV protocol (rfc4791)
Group:		System/Libraries

Obsoletes:	trinity-libcaldav < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-libcaldav = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	libcaldav = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libcaldav}0
libcaldev is a client library that adds support for the CalDAV protocol (rfc4791).
The object is to have a library which fully implements the protocol so that it is
easy to integrate CalDAV support into any PIM application.

%files -n %{libcaldav}0
%defattr(-,root,root,-)
%{_libdir}/libcaldav.so.0
%{_libdir}/libcaldav.so.0.0.6
%{_docdir}/libcaldav-%{version}/

%post -n %{libcaldav}0
/sbin/ldconfig

%postun -n %{libcaldav}0
/sbin/ldconfig

##########

%package -n %{libcaldav}-devel
Summary:	A client library that adds support for the CalDAV protocol (Development Files)
Group:		Development/Libraries/Other
Requires:	%{libcaldav}0 = %{?epoch:%{epoch}:}%{version}-%{release}
%{?libcurl_devel:Requires: %{libcurl_devel}}
Requires:	glib2-devel

Obsoletes:	trinity-libcaldav-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-libcaldav-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	libcaldav-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libcaldav}-devel
libcaldev is a client library that adds support for the CalDAV protocol (rfc4791).
The object is to have a library which fully implements the protocol so that it is
easy to integrate CalDAV support into any PIM application. 

This package includes the development files.

%files -n %{libcaldav}-devel
%defattr(-,root,root,-)
%{_includedir}/libcaldav/
%{_libdir}/libcaldav.la
%{_libdir}/libcaldav.so
%{_libdir}/pkgconfig/libcaldav.pc

%post -n %{libcaldav}-devel
/sbin/ldconfig

%postun -n %{libcaldav}-devel
/sbin/ldconfig

##########

%if 0%{?pclinuxos} || 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
#patch1 -p1 -b .tqt
autoreconf -fiv


%build
# CFLAGS required if CURL is installed on /opt/trinity, e.g. RHEL 5
export CFLAGS="-I%{tde_includedir} -L%{tde_libdir} ${RPM_OPT_FLAGS}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

# RHEL4 stuff
if [ -d /usr/evolution28 ]; then
  export PKG_CONFIG_PATH="/usr/evolution28/%{_lib}/pkgconfig:${PKG_CONFIG_PATH}"
fi

%configure \
  --docdir=%{_docdir}/libcaldav \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  \
  --disable-dependency-tracking

%__make %{?_smp_mflags}


%install
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# Unwanted files
%__rm -f %{buildroot}%{_libdir}/*.a

# Fix doc dir
mv -f %{?buildroot}%{_docdir}/libcaldav/ %{?buildroot}%{_docdir}/libcaldav-%{version}/

# Fix duplicate files
%fdupes %{?buildroot}


%clean
%__rm -rf %{buildroot}


%Changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:0.6.5-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.6.5-1
- Initial release for TDE R14.0.0
