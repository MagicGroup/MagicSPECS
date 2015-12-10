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
%define tde_pkg k3b
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
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.2
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

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Source2:		k3brc

Patch1:			trinity-k3b-14.0.1-tqt.patch
# Legacy RedHat / Fedora patches
# manual bufsize (upstream?)
Patch4:			k3b-1.0.4-manualbufsize.patch

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

Requires:		%{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}

Requires:		cdrecord
REquires:		mkisofs
Requires:		dvd+rw-tools

# CDRDAO support
Requires:		cdrdao

# UDEV support
BuildRequires:	libudev-devel

# HAL support
%if 0%{?rhel} == 5
%define with_hal 1
BuildRequires:	hal-devel
%endif

# DBUS support
#  TQT bindings not available for RHEL4
BuildRequires:	trinity-dbus-tqt-devel >= 1:0.63
Requires:		trinity-dbus-tqt >= 1:0.63

# SNDFILE support
%define with_sndfile 1
BuildRequires:	libsndfile-devel

# SAMPLERATE support
%define with_samplerate 1
BuildRequires:	libsamplerate-devel

# DVDREAD support
%define with_dvdread 1
BuildRequires:	libdvdread-devel

BuildRequires:	flac-devel

# MAD support
%define with_libmad 1
BuildRequires:	libmad-devel

# LAME support
BuildRequires:	lame-devel

# FFMPEG support
BuildRequires:	ffmpeg-devel


%description
K3b provides a comfortable user interface to perform most CD/DVD
burning tasks. While the experienced user can take influence in all
steps of the burning process the beginner may find comfort in the
automatic settings and the reasonable k3b defaults which allow a quick
start.

%description -l zh_CN.UTF-8
TDE 下的光盘刻录程序。

%files
%defattr(-,root,root,-)
%doc AUTHORS README COPYING TODO ChangeLog
%{tde_bindir}/k3b
%{tde_tdelibdir}/tdefile_k3b.la
%{tde_tdelibdir}/tdefile_k3b.so
%{tde_tdelibdir}/tdeio_videodvd.la
%{tde_tdelibdir}/tdeio_videodvd.so
%{tde_tdelibdir}/libk3balsaoutputplugin.la
%{tde_tdelibdir}/libk3balsaoutputplugin.so
%{tde_tdelibdir}/libk3bartsoutputplugin.la
%{tde_tdelibdir}/libk3bartsoutputplugin.so
%{tde_tdelibdir}/libk3baudiometainforenamerplugin.la
%{tde_tdelibdir}/libk3baudiometainforenamerplugin.so
%{tde_tdelibdir}/libk3baudioprojectcddbplugin.la
%{tde_tdelibdir}/libk3baudioprojectcddbplugin.so
%{tde_tdelibdir}/libk3bexternalencoder.la
%{tde_tdelibdir}/libk3bexternalencoder.so
%{tde_tdelibdir}/libk3bflacdecoder.la
%{tde_tdelibdir}/libk3bflacdecoder.so
%if 0%{?with_sndfile}
%{tde_tdelibdir}/libk3blibsndfiledecoder.la
%{tde_tdelibdir}/libk3blibsndfiledecoder.so
%endif
%{tde_tdelibdir}/libk3bmpcdecoder.la
%{tde_tdelibdir}/libk3bmpcdecoder.so
%{tde_tdelibdir}/libk3boggvorbisdecoder.la
%{tde_tdelibdir}/libk3boggvorbisdecoder.so
%{tde_tdelibdir}/libk3boggvorbisencoder.la
%{tde_tdelibdir}/libk3boggvorbisencoder.so
%{tde_tdelibdir}/libk3bsoxencoder.la
%{tde_tdelibdir}/libk3bsoxencoder.so
%{tde_tdelibdir}/libk3bwavedecoder.la
%{tde_tdelibdir}/libk3bwavedecoder.so
%lang(en) %{tde_tdedocdir}/HTML/en/k3b/


##########

%package common
Summary:		Common files of %{name}
Summary(zh_CN.UTF-8): %{name} 的公用文件
Group:			Applications/Archiving
Group(zh_CN.UTF-8): 应用程序/归档
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch: noarch

%description common
%{summary}.

%description common -l zh_CN.UTF-8
%{name} 的公用文件。

%files common
%defattr(-,root,root,-)
%{tde_tdeappdir}/k3b.desktop
%{tde_datadir}/applnk/.hidden/k3b-cue.desktop
%{tde_datadir}/applnk/.hidden/k3b-iso.desktop
%{tde_datadir}/apps/k3b/
%{tde_datadir}/apps/konqsidebartng/virtual_folders/services/videodvd.desktop
%{tde_datadir}/apps/konqueror/servicemenus/k3b_audiocd_rip.desktop
%{tde_datadir}/apps/konqueror/servicemenus/k3b_cd_copy.desktop
%{tde_datadir}/apps/konqueror/servicemenus/k3b_dvd_copy.desktop
%{tde_datadir}/apps/konqueror/servicemenus/k3b_handle_empty_cd.desktop
%{tde_datadir}/apps/konqueror/servicemenus/k3b_handle_empty_dvd.desktop
%{tde_datadir}/apps/konqueror/servicemenus/k3b_videodvd_rip.desktop
%{tde_confdir}/k3brc
%{tde_datadir}/mimelnk/application/x-k3b.desktop
%{tde_datadir}/icons/hicolor/*/apps/k3b.png
%{tde_datadir}/services/tdefile_k3b.desktop
%{tde_datadir}/services/videodvd.protocol
%{tde_datadir}/sounds/k3b_error1.wav
%{tde_datadir}/sounds/k3b_success1.wav
%{tde_datadir}/sounds/k3b_wait_media1.wav
%{tde_tdedocdir}/HTML/en/tdeioslave/videodvd/

%post common
touch --no-create %{tde_datadir}/icons/hicolor ||:

%postun common
if [ $1 -eq 0 ] ; then
  touch --no-create %{tde_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{tde_datadir}/icons/hicolor &> /dev/null || :
  update-desktop-database %{tde_appdir} -q &> /dev/null
fi

%posttrans common
gtk-update-icon-cache %{tde_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database %{tde_appdir} -q &> /dev/null

##########

%package libs
Summary:		Runtime libraries for %{name}
Group:			System Environment/Libraries
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libs
%{summary}.

%files libs
%defattr(-,root,root,-)
%{tde_libdir}/libk3b.so.3
%{tde_libdir}/libk3b.so.3.0.0
%{tde_libdir}/libk3bdevice.so.5
%{tde_libdir}/libk3bdevice.so.5.0.0

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

##########

%package devel
Summary:		Files for the development of applications which will use %{name} 
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:			Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:		%{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%files devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/*.h
%{tde_libdir}/libk3b.so
%{tde_libdir}/libk3bdevice.so

%post devel
/sbin/ldconfig

%postun devel
/sbin/ldconfig

##########

%if 0%{?with_libmad}
%package plugin-mad
Summary:		The MAD plugin for K3B
Summary(zh_CN.UTF-8): %{name} 的 MAD 插件
Group:			System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugin-mad
%{summary}.

MAD is a high-quality MPEG audio decoder. It currently supports MPEG-1
and the MPEG-2  extension to Lower Sampling Frequencies, as well as the
so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are fully implemented.

%description plugin-mad -l zh_CN.UTF-8
%{name} 的 MAD 插件。

%files plugin-mad
%defattr(-,root,root,-)
%{tde_tdelibdir}/libk3bmaddecoder.la
%{tde_tdelibdir}/libk3bmaddecoder.so
%endif

##########

%if 0%{?with_lame}
%package plugin-lame
Summary:		The LAME plugin for K3B
Summary(zh_CN.UTF-8): %{name} 的 LAME 插件
Group:			System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugin-lame
%{summary}.

Personal and commercial use of compiled versions of LAME (or any other mp3
encoder) requires a patent license in some countries.

This package is in tainted, as MP3 encoding is covered by software patents.

%description plugin-lame -l zh_CN.UTF-8
%{name} 的 LAME 插件。

%files plugin-lame
%defattr(-,root,root,-)
%{tde_tdelibdir}/libk3blameencoder.la
%{tde_tdelibdir}/libk3blameencoder.so
%endif

##########

%if 0%{?with_ffmpeg}
%package plugin-ffmpeg
Summary:		The FFMPEG plugin for K3B
Summary(zh_CN.UTF-8): %{name} 的 FFMPEG 插件
Group:			System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugin-ffmpeg
%{summary}.

ffmpeg is a hyper fast realtime audio/video encoder, a streaming server
and a generic audio and video file converter.

%description plugin-ffmpeg -l zh_CN.UTF-8
%{name} 的 FFMPEG 插件。

%files plugin-ffmpeg
%defattr(-,root,root,-)
%{tde_tdelibdir}/libk3bffmpegdecoder.la
%{tde_tdelibdir}/libk3bffmpegdecoder.so
%endif

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

# set in k3brc too 
%patch4 -p1 -b .manualbufsize

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
  --without-cdrecord-suid-root \
  --with-oggvorbis \
  --with-flac \
  %{?with_samplerate:--with-external-libsamplerate} \
  %{?with_dvdread:--with-libdvdread} %{?!with_dvdread:--without-libdvdread} \
  --with-musicbrainz \
  %{?with_sndfile:--with-sndfile} %{?!with_sndfile:--without-sndfile} \
  %{?with_ffmpeg:--with-ffmpeg} %{?!with_ffmpeg:--without-ffmpeg} \
  %{?with_lame:--with-lame} %{?!with_lame:--without-lame} \
  %{?with_libmad:--with-libmad} %{?!with_libmad:--without-libmad} \
  --with-musepack \
  --without-resmgr \
  %{?with_hal:--with-hal} %{?!with_hal:--without-hal} \

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
%__install -D -m 644 -p %{SOURCE2} %{buildroot}%{tde_confdir}/k3brc

# remove the .la files
%__rm -f %{buildroot}%{tde_libdir}/libk3b*.la 
magic_rpm_clean.sh

%clean
%__rm -rf %{buildroot}


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 2:1.0.5-1.2
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:1.0.5-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.0.5-1
- Initial release for TDE 14.0.0
