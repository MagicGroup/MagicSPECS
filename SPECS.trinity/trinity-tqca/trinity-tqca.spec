#
# spec file for package tqca (version R14)
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
%define tde_pkg tqca
%define tde_prefix /opt/trinity
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

%define libtqca libtqca


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.0
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.2
Summary:	TQt Cryptographic Architecture
Summary(zh_CN.UTF-8): TQt 加密架构
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Source1:		trinity-tqca-rpmlintrc

BuildRequires:  libtqt4-devel >= %{tde_epoch}:4.2.0
BuildRequires:	gcc-c++

%description
Taking a hint from the similarly-named Java Cryptography Architecture,
TQCA aims to provide a straightforward and cross-platform crypto API,
using TQt datatypes and conventions. TQCA separates the API from the
implementation, using plugins known as Providers. The advantage of this
model is to allow applications to avoid linking to or explicitly depending
on any particular cryptographic library. This allows one to easily change
or upgrade crypto implementations without even needing to recompile the
application!

%description -l zh_CN.UTF-8
TQt 加密架构。

##########

%package -n %{libtqca}1
Summary:	TQt Cryptographic Architecture
Summary(zh_CN.UTF-8): TQt 加密架构
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库

Obsoletes:	trinity-libtqca < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-libtqca = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	libtqca = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	libtqca1 = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libtqca}1
Taking a hint from the similarly-named Java Cryptography Architecture,
TQCA aims to provide a straightforward and cross-platform crypto API,
using TQt datatypes and conventions. TQCA separates the API from the
implementation, using plugins known as Providers. The advantage of this
model is to allow applications to avoid linking to or explicitly depending
on any particular cryptographic library. This allows one to easily change
or upgrade crypto implementations without even needing to recompile the
application!

%description -n %{libtqca}1 -l zh_CN.UTF-8
TQt 加密架构。

%post -n %{libtqca}1
/sbin/ldconfig

%postun -n %{libtqca}1
/sbin/ldconfig

%files -n %{libtqca}1
%defattr(-,root,root,-)
%doc COPYING README TODO
%{_libdir}/libqca.so.1
%{_libdir}/libqca.so.1.0
%{_libdir}/libqca.so.1.0.0

##########

%package -n %{libtqca}-devel
Summary:	TQt Cryptographic Architecture development files
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{libtqca}1 = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:	trinity-libtqca-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-libtqca-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	libtqca-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libtqca}-devel
This packages contains the development files for TQCA

%description -n %{libtqca}-devel -l zh_CN.UTF-8
%{name} 的开发包。

%post -n %{libtqca}-devel
/sbin/ldconfig

%postun -n %{libtqca}-devel
/sbin/ldconfig

%files -n %{libtqca}-devel
%defattr(-,root,root,-)
%{_includedir}/qca.h
%{_libdir}/libqca.so

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}

# Fix 'lib64' library directory
perl -pi -e 's,target\.path=\$PREFIX/lib,target.path=\$PREFIX/%{_lib},g' qcextra


%build
unset QTDIR QTINC QTLIB

./configure \
  --prefix=%{_prefix} \
  --qtdir=/usr \
  --debug


# Workaround strange tqmake behaviour in RHEL5
%if 0%{?rhel} == 5
%__sed -i "Makefile" -e "s|..\/..\/..\/..|%{_prefix}|g"
%endif

%__make %{?_smp_mflags}


%install
%__rm -rf $RPM_BUILD_ROOT
%__make install INSTALL_ROOT="${RPM_BUILD_ROOT}/"


%clean
%__rm -rf $RPM_BUILD_ROOT


%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:1.0-1.2
- 为 Magic 3.0 重建

* Tue Oct 06 2015 Liu Di <liudidi@gmail.com> - 2:1.0-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.0-1
- Initial release for TDE 14.0.0
