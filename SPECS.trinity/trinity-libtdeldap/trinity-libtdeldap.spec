#
# spec file for package libtdeldap (version R14)
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

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg libtdeldap
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif


Name:		trinity-%{tde_pkg}
Summary:	LDAP interface library for TDE
Summary(zh_CN.UTF-8): TDE 的 LDAP 接口库
Group:		System/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Epoch:		%{tde_epoch}
Version:	0.5
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{tde_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}

BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gcc-c++

# AUTOTOOLS
BuildRequires: automake autoconf libtool
BuildRequires:	libtool-ltdl-devel

# SASL support
BuildRequires:	cyrus-sasl-devel

# OPENLDAP support
BuildRequires:	openldap-devel

%description
LDAP interface library for TDE management modules.

%description -l zh_CN.UTF-8
TDE 的 LDAP 接口库。

%post
/sbin/ldconfig || :

%postun
/sbin/ldconfig || :

%files
%defattr(-,root,root,-)
%{tde_libdir}/libtdeldap.so.1
%{tde_libdir}/libtdeldap.so.1.0.0

##########

%package devel
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary(zh_CN.UTF-8): %{name} 的开发包
Summary:	Trinity image viewer
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
LDAP interface library for TDE management modules.

libtdeldap-trinity-dev contains development files and documentation.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%post devel
/sbin/ldconfig || :

%postun devel
/sbin/ldconfig || :

%files devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/ldappasswddlg.h
%{tde_tdeincludedir}/libtdeldap.h
%{tde_libdir}/libtdeldap.la
%{tde_libdir}/libtdeldap.so

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility \
  \

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}
magic_rpm_clean.sh

%clean
%__rm -rf %{buildroot}


%Changelog
* Sun Oct 11 2015 Liu Di <liudidi@gmail.com> - 2:0.5-1.opt.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 20.5-1
- Initial release for TDE 14.0.0
