#
# spec file for package libkexiv2 (version R14)
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
%define tde_pkg libkexiv2
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

%define libkexiv libkexiv


Name:		trinity-%{tde_pkg}
Summary:	Qt like interface for the libexiv2 library (runtime) [Trinity]
Summary(zh_CN.UTF-8): libexiv2 库的 Qt 风格接口
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Epoch:		2
Version:	0.1.7
Release:	%{?!preversion:2}%{?preversion:1_%{preversion}}%{?dist}%{?_variant}.1
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{tde_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		trinity-libkexiv2-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gcc-c++

# AUTOTOOLS
BuildRequires: automake autoconf libtool
BuildRequires:	libtool-ltdl-devel

# EXIV2
BuildRequires:	exiv2-devel

%description
libkexif2 contains the library of libkexiv2.
Libkexif is a wrapper around Exiv2 library to manipulate pictures metadata.

##########

%package -n trinity-%{libkexiv}2-5
Summary:	Qt like interface for the libexiv2 library (runtime) [Trinity]
Summary(zh_CN.UTF-8): %{name} 的运行库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

Obsoletes:	trinity-%{tde_pkg} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-%{tde_pkg} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n trinity-%{libkexiv}2-5
libkexif2 contains the library of libkexiv2.
Libkexif is a wrapper around Exiv2 library to manipulate pictures metadata.

%description -n trinity-%{libkexiv}2-5 -l zh_CN.UTF-8
%{name} 的运行库。

%files -n trinity-%{libkexiv}2-5
%defattr(-,root,root,-)
%{tde_libdir}/libkexiv2.so.5
%{tde_libdir}/libkexiv2.so.5.0.0

%post -n trinity-%{libkexiv}2-5
/sbin/ldconfig || :

%postun -n trinity-%{libkexiv}2-5
/sbin/ldconfig || :

##########

%package -n trinity-%{libkexiv}2-devel
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:	Qt like interface for the libexiv2 library (development) [Trinity]
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:	trinity-%{libkexiv}2-5 = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:	trinity-%{tde_pkg}-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-%{tde_pkg}-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n trinity-%{libkexiv}2-devel
libkexif2-devel contains development files and documentation for libkexiv2
library.  The library documentation is available on kexiv2.h header file.
Libkexif is a wrapper around Exiv2 library to manipulate pictures metadata.

%description  -n trinity-%{libkexiv}2-devel -l zh_CN.UTF-8
%{name} 的开发包。

%files -n trinity-%{libkexiv}2-devel
%defattr(-,root,root,-)
%{tde_libdir}/libkexiv2.so
%{tde_libdir}/libkexiv2.la
%{tde_tdeincludedir}/libkexiv2/
%{tde_libdir}/pkgconfig/libkexiv2.pc

%post -n trinity-%{libkexiv}2-devel
/sbin/ldconfig || :

%postun -n trinity-%{libkexiv}2-devel
/sbin/ldconfig || :

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --libdir=%{tde_libdir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%clean
%__rm -rf %{buildroot}



%Changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:0.1.7-2.opt.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 0.1.7-2
- Initial release for TDE 14.0.0
