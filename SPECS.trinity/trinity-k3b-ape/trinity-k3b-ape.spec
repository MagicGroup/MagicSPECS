#
# spec file for package k3b (version R14)
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
%define tde_pkg k3b-ape
%define tde_prefix /opt/trinity
%define tde_appdir %{tde_datadir}/applications
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		1.0.5
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1
Summary:		CD/DVD burning application
Summary(zh_CN.UTF-8): 光盘刻录程序
Group:			Applications/Archiving
Group(zh_CN.UTF-8): 应用程序/归档
URL:			http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.bz2

Patch1:			trinity-k3b-ape-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

BuildRequires:	alsa-lib-devel
BuildRequires:	audiofile-devel
BuildRequires:	gettext
BuildRequires:	libmpcdec-devel
BuildRequires:	libmusicbrainz-devel
BuildRequires:	libvorbis-devel
BuildRequires:	taglib-devel
BuildRequires:	zlib-devel

Requires(post): coreutils
Requires(postun): coreutils

Requires:		trinity-k3b-libs = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		trinity-k3b-common = %{?epoch:%{epoch}:}%{version}-%{release}

Requires:		cdrecord
REquires:		mkisofs
Requires:		dvd+rw-tools

# CDRDAO support
Requires:		cdrdao

# UDEV support
BuildRequires:	libudev-devel

# DBUS support
#  TQT bindings not available for RHEL4
BuildRequires:	trinity-dbus-tqt-devel >= 1:0.63
Requires:		trinity-dbus-tqt >= 1:0.63


%description
K3b provides a comfortable user interface to perform most CD/DVD
burning tasks. While the experienced user can take influence in all
steps of the burning process the beginner may find comfort in the
automatic settings and the reasonable k3b defaults which allow a quick
start.

%description -l zh_CN.UTF-8
TDE 下的光盘刻录程序。

%package plugin-ape
Summary:		The MAD plugin for K3B
Summary(zh_CN.UTF-8): %{name} 的 MAD 插件
Group:			System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:               trinity-k3b-libs = %{?epoch:%{epoch}:}%{version}
Requires:               trinity-k3b-common = %{?epoch:%{epoch}:}%{version}

%description plugin-ape
%{summary}.

MAD is a high-quality MPEG audio decoder. It currently supports MPEG-1
and the MPEG-2  extension to Lower Sampling Frequencies, as well as the
so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are fully implemented.

%description plugin-ape -l zh_CN.UTF-8
%{name} 的 MAD 插件。

%files plugin-ape
%defattr(-,root,root,-)
%{tde_tdelibdir}/libk3bmonkey*.la
%{tde_tdelibdir}/libk3bmonkey*.so
%{tde_tdelibdir}/libk3bmonkeydecoder.so.*
%{tde_tdelibdir}/libk3bmonkeyencoder.so.*
%{tde_datadir}/apps/k3b/plugins/k3bmonkey*coder.plugin

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
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig:${PKG_CONFIG_PATH}"
export kde_confdir="%{tde_confdir}"

# FFMPEG trick ...
if [ -d /usr/include/ffmpeg ]; then
	export CXXFLAGS="${RPM_OPT_FLAGS} -I/usr/include/ffmpeg"
fi

# Notice: extra-includes is required to find arts headers
%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
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
  --with-extra-includes=%{tde_includedir} \
  \
  --with-k3bsetup=no \
  --without-cdrecord-suid-root 

# Strange behaviour on RHEL4 ...
%if 0%{?rhel} == 4
%__sed -i "libk3b/jobs/Makefile" -e "/^am_libjobs_la_final_OBJECTS/ s/ lo//g"
%__mkdir_p "libk3bdevice/.libs"
%__ln_s . "libk3bdevice/.libs/.libs"
%endif

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# remove the .la files
%__rm -f %{buildroot}%{tde_libdir}/libk3b*.la 
magic_rpm_clean.sh

%clean
%__rm -rf %{buildroot}


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:1.0.5-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.0.5-1
- Initial release for TDE 14.0.0
