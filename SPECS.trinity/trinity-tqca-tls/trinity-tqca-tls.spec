#
# spec file for package tqca-tls (version R14)
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
%define tde_pkg tqca-tls
%define tde_prefix /opt/trinity
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define libtqt3 %{_lib}tqt3
%else
%define libtqt3 libtqt3
%endif


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.0
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}
Summary:	TLS plugin for the TQt Cryptographic Architecture
Group:		Applications/Internet
URL:		http://delta.affinix.com/qca/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

BuildRequires:  libtqt4-devel >= %{tde_epoch}:4.2.0
BuildRequires:	libtqca-devel >= %{tde_epoch}:1.0

BuildRequires:	gcc-c++
BuildRequires:	openssl-devel >= 0.9.8


%description
This is a plugin to provide SSL/TLS capability to programs that use the TQt
Cryptographic Architecture (TQCA).  TQCA is a library providing an easy API
for several cryptographic algorithms to TQt programs.  This package only
contains the TLS plugin.

##########

%package -n %{libtqt3}-mt-tqca-tls
Summary:	TLS plugin for the TQt Cryptographic Architecture
Group:		Applications/Internet

%description -n %{libtqt3}-mt-tqca-tls
This is a plugin to provide SSL/TLS capability to programs that use the TQt
Cryptographic Architecture (TQCA).  TQCA is a library providing an easy API
for several cryptographic algorithms to TQt programs.  This package only
contains the TLS plugin.

%files -n %{libtqt3}-mt-tqca-tls
%defattr(0644,root,root,0755)
%doc README COPYING
%dir %{_libdir}/tqt3/plugins/crypto
%{_libdir}/tqt3/plugins/crypto/libtqca-tls.so

##########

%if 0%{?pclinuxos} || 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB

./configure \
  --qtdir=%{_prefix}

%__make %{?_smp_mflags}


%install
%__rm -rf %{?buildroot}
%__make install INSTALL_ROOT=%{?buildroot}


%clean
%__rm -rf %{?buildroot}


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.0-1
- Initial release for TDE 14.0.0
