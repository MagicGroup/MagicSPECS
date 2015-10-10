#
# spec file for package libkipi (version R14)
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
%define tde_pkg libkipi
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

%define libkipi libkipi


Name:		trinity-%{tde_pkg}
Summary:	Library for apps that want to use kipi-plugins (runtime version) [Trinity]
Summary(zh_CN.UTF-8): 使用 kipi-plugins 的程序使用的库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Epoch:		%{tde_epoch}
Version:	0.1.5
Release:	%{?!preversion:2}%{?preversion:1_%{preversion}}%{?dist}%{?_variant}
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{tde_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Patch1:			trinity-libkipi-14.0.1-tqt.patch

BuildRequires: trinity-tdelibs-devel >= %{tde_version}

BuildRequires: desktop-file-utils
BuildRequires: pkgconfig
BuildRequires: gettext
BuildRequires: gcc-c++

# LCMS support
BuildRequires: lcms-devel

# JPEG support
BuildRequires: libjpeg-devel

# AUTOTOOLS
BuildRequires: automake autoconf libtool
BuildRequires:	libtool-ltdl-devel

%description
Libkipi is a library
- that contains common routines and widget used by kipi-plugins
- to ease implementation of the kipi-plugins interface in an application
  that wants to use kipi-plugins
    
Homepage: http://www.kipi-plugins.org/

%description -l zh_CN.UTF-8
使用 kipi-plugins 的程序使用的库。

##########

%package -n trinity-%{libkipi}0
Summary:	library for apps that want to use kipi-plugins (runtime version) [Trinity]
Summary(zh_CN.UTF-8): %{name} 的运行库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

Obsoletes:	trinity-%{tde_pkg} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-%{tde_pkg} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n trinity-%{libkipi}0
Libkipi is a library
  o that contains common routines and widget used by kipi-plugins
  o to ease implementation of the kipi-plugins interface in an application
    that wants to use kipi-plugins
    
Homepage: http://www.kipi-plugins.org/

%description -n trinity-%{libkipi}0 -l zh_CN.UTF-8
%{name} 的运行库。

%post -n trinity-%{libkipi}0
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${f} 2> /dev/null ||:
done
/sbin/ldconfig || :

%postun -n trinity-%{libkipi}0
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${f} 2> /dev/null ||:
done
/sbin/ldconfig || :

%files -n trinity-%{libkipi}0 -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_libdir}/libkipi.so.0
%{tde_libdir}/libkipi.so.0.1.1
%{tde_datadir}/apps/kipi/
%{tde_datadir}/icons/hicolor/*/apps/kipi.png
%{tde_datadir}/servicetypes/kipiplugin.desktop

##########

%package -n trinity-%{libkipi}-devel
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:	library for apps that want to use kipi-plugins (development version) [Trinity]
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:	trinity-%{tde_pkg}-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-%{tde_pkg}-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n trinity-%{libkipi}-devel
Libkipi is a library
  o that contains common routines and widget used by kipi-plugins
  o to ease implementation of the kipi-plugins interface in an application
    that wants to use kipi-plugins
    
This package contains development files and documentation for libkipi library.
Homepage: http://www.kipi-plugins.org/

%description  -n trinity-%{libkipi}-devel -l zh_CN.UTF-8
%{name} 的开发包。

%files -n trinity-%{libkipi}-devel
%defattr(-,root,root,-)
%{tde_libdir}/libkipi.so
%{tde_libdir}/libkipi.la
%{tde_tdeincludedir}/libkipi/
%{tde_libdir}/pkgconfig/libkipi.pc

%post -n trinity-%{libkipi}-devel
/sbin/ldconfig || :

%postun -n trinity-%{libkipi}-devel
/sbin/ldconfig || :

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
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{tde_pkg}


%clean
%__rm -rf %{buildroot}





%Changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 0.1.5-2
- Initial release for TDE 14.0.0
