#
# spec file for package libkdcraw (version R14)
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
%define tde_pkg libkdcraw
%define tde_prefix /opt/trinity
%define tde_datadir %{tde_prefix}/share
%define tde_includedir %{tde_prefix}/include
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_libdir %{tde_prefix}/%{_lib}

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define libkdcraw %{_lib}kdcraw
%else
%define libkdcraw libkdcraw
%endif


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.1.9
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1
Summary:	Raw picture decoding C++ library (runtime) [Trinity]
Summary(zh_CN.UTF-8): RAW 图像解码 C++ 库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		/usr
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		trinity-libkdcraw-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-filesystem >= %{tde_version}

BuildRequires: automake autoconf libtool
BuildRequires: gcc-c++
BuildRequires: desktop-file-utils
BuildRequires: pkgconfig
BuildRequires: gettext

# LCMS support
BuildRequires: lcms-devel

# JPEG support
BuildRequires: libjpeg-devel

# AUTOTOOLS
BuildRequires:	libtool-ltdl-devel

%description
C++ interface around dcraw binary program used to decode RAW
picture files.
This library is used by kipi-plugins, digiKam and others kipi host programs.
libkdcraw contains the library of libkdcraw.

%description -l zh_CN.UTF-8
RAW 图像解码库。

##########

%package -n trinity-%{libkdcraw}4
Summary:	Raw picture decoding C++ library (runtime) [Trinity]
Summary(zh_CN.UTF-8): %{name} 的运行库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:	trinity-libkdcraw-common = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:	trinity-%{tde_pkg} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-%{tde_pkg} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n trinity-%{libkdcraw}4
C++ interface around dcraw binary program used to decode RAW
picture files.
This library is used by kipi-plugins, digiKam and others kipi host programs.
libkdcraw contains the library of libkdcraw.

%description -n trinity-%{libkdcraw}4 -l zh_CN.UTF-8
%{name} 的运行库。

%files -n trinity-%{libkdcraw}4
%defattr(-,root,root,-)
%{tde_libdir}/libkdcraw.so.4
%{tde_libdir}/libkdcraw.so.4.0.3

%post -n trinity-%{libkdcraw}4
/sbin/ldconfig || :

%postun -n trinity-%{libkdcraw}4
/sbin/ldconfig || :

##########

%package -n trinity-libkdcraw-common
Summary:	Raw picture decoding C++ library (runtime) [Trinity]
Summary(zh_CN.UTF-8): RAW 图像解码 C++ 库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:	trinity-filesystem >= %{tde_version}

%description -n trinity-libkdcraw-common
C++ interface around dcraw binary program used to decode RAW
picture files.
This library is used by kipi-plugins, digiKam and others kipi host programs.
libkdcraw contains the library of libkdcraw.

%description -n trinity-libkdcraw-common -l zh_CN.UTF-8
RAW 图像解码 C++ 库。

%files -n trinity-libkdcraw-common 
%defattr(-,root,root,-)
%{tde_datadir}/icons/hicolor/*/apps/kdcraw.png

%post -n trinity-libkdcraw-common
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${f} 2> /dev/null ||:
done

%postun -n trinity-libkdcraw-common
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${f} 2> /dev/null ||:
done

##########

%package -n trinity-%{libkdcraw}-devel
Summary:	RAW picture decoding C++ library (development) [Trinity]
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	trinity-%{libkdcraw}4 = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:	trinity-%{tde_pkg}-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-%{tde_pkg}-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n trinity-%{libkdcraw}-devel
Libkdcraw is a C++ interface around dcraw binary program used to
decode Raw picture files.
libkdcraw-devel contains development files and documentation. The
library documentation is available on kdcraw.h header file.

%description  -n trinity-%{libkdcraw}-devel -l zh_CN.UTF-8
%{name} 的开发包。

%files -n trinity-%{libkdcraw}-devel
%defattr(-,root,root,-)
%{tde_libdir}/libkdcraw.so
%{tde_libdir}/libkdcraw.la
%{tde_tdeincludedir}/libkdcraw/
%{tde_libdir}/pkgconfig/libkdcraw.pc

%post -n trinity-%{libkdcraw}-devel
/sbin/ldconfig || :

%postun -n trinity-%{libkdcraw}-devel
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

# Warning: gcc-hidden-visibility causes FTBFS in digikam !
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
%find_lang %{tde_pkg} || :

%clean
%__rm -rf %{buildroot}


%Changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:0.1.9-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.1.9-1
- Initial release for TDE R14.0.0
