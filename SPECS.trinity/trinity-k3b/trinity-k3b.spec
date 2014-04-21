# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_appdir %{tde_datadir}/applications

%define tde_tdeappdir %{tde_appdir}/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}


Name:		trinity-k3b
Summary:	CD/DVD burning application
Version:	3.5.13.2
Release:	1%{?dist}%{?_variant}

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Group:		Applications/Archiving
License:	GPLv2+

Source0:	k3b-trinity-%{version}.tar.xz
Source2:	k3brc

# Legacy RedHat / Fedora patches
# manual bufsize (upstream?)
Patch4:		k3b-1.0.4-manualbufsize.patch
# RHEL6: Fix K3B icon
Patch106:	trinity-k3b-icons.patch

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-dbus-tqt-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-arts-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	alsa-lib-devel
BuildRequires:	audiofile-devel
BuildRequires:	hal-devel
BuildRequires:	gettext
BuildRequires:	libdvdread-devel
BuildRequires:	libmpcdec-devel
BuildRequires:	libmusicbrainz-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libvorbis-devel
BuildRequires:	taglib-devel
BuildRequires:	zlib-devel

%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}flac-devel
BuildRequires:	%{_lib}flac++-devel
%else
BuildRequires:	flac-devel
%endif

Requires(post): coreutils
Requires(postun): coreutils

Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}

Requires: cdrecord mkisofs
Requires: cdrdao
Requires: dvd+rw-tools

%description
K3b provides a comfortable user interface to perform most CD/DVD
burning tasks. While the experienced user can take influence in all
steps of the burning process the beginner may find comfort in the
automatic settings and the reasonable k3b defaults which allow a quick
start.

%files
%defattr(-,root,root,-)
%doc AUTHORS README COPYING TODO ChangeLog
%{tde_bindir}/k3b
%{tde_tdelibdir}/kfile_k3b.la
%{tde_tdelibdir}/kfile_k3b.so
%{tde_tdelibdir}/kio_videodvd.la
%{tde_tdelibdir}/kio_videodvd.so
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
%{tde_tdelibdir}/libk3blibsndfiledecoder.la
%{tde_tdelibdir}/libk3blibsndfiledecoder.so
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
Summary:  Common files of %{name}
Group:    Applications/Archiving
Requires: %{name} = %{version}-%{release}
%if 0%{?rhel} >= 6 || 0%{?fedora} >= 15 || 0%{?mgaversion} || 0%{?mdkversion}
BuildArch: noarch
%endif

%description common
%{summary}.

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
%{tde_datadir}/config/k3brc
%{tde_datadir}/mimelnk/application/x-k3b.desktop
%{tde_datadir}/icons/hicolor/*/apps/k3b.png
%{tde_datadir}/services/kfile_k3b.desktop
%{tde_datadir}/services/videodvd.protocol
%{tde_datadir}/sounds/k3b_error1.wav
%{tde_datadir}/sounds/k3b_success1.wav
%{tde_datadir}/sounds/k3b_wait_media1.wav


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
Summary: Runtime libraries for %{name}
Group:   System Environment/Libraries
Requires: %{name} = %{version}-%{release}

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
Summary: Files for the development of applications which will use %{name} 
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}

%description devel
%{summary}.

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

%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -a 0 -n k3b-trinity-%{version}

# set in k3brc too 
%patch4 -p1 -b .manualbufsize
%patch106 -p1 -b .desktopfile


# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i "admin/acinclude.m4.in" \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR || : ; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  --disable-rpath \
  --enable-new-ldflags \
  --disable-debug --disable-warnings \
  --disable-dependency-tracking --enable-final \
  --with-k3bsetup=no \
  --without-cdrecord-suid-root \
  --with-oggvorbis \
  --with-flac \
  --with-external-libsamplerate \
  --with-libdvdread \
  --with-musicbrainz \
  --with-sndfile \
  --without-ffmpeg --without-lame --without-libmad \
  --with-musepack \
  --with-extra-includes=%{tde_includedir}/tqt:%{tde_includedir}

%__make %{?_smp_mflags}

%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}
%__install -D -m 644 -p %{SOURCE2} %{buildroot}%{tde_datadir}/config/k3brc

# remove the .la files
%__rm -f %{buildroot}%{tde_libdir}/libk3b*.la 

# remove i18n for Plattdeutsch (Low Saxon)
#%__rm -fr %{buildroot}%{tde_datadir}/locale/nds



%clean
%__rm -rf %{buildroot}



%changelog
* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial build for TDE 3.5.13.1
- Remove requirement for resmgr

* Sat Aug 04 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13-5
- Add support for Mageia 2 and Mandriva 2011
- Fix DBUS-TQT detection that prevented HAL support
- Adds requirement for resmgr

* Wed May 09 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13-4
- Removes i18 files (built separately)

* Tue May 01 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13-3
- Rebuilt for Fedora 17
- Fix compilation with GCC 4.7 [Bug #958]

* Sat Nov 05 2011 Francois Andriot <francois.andriot@free.fr> - 3.5.13-2
- Updates BuildRequires

* Sun Oct 30 2011 Francois Andriot <francois.andriot@free.fr> - 3.5.13-1
- Initial release for RHEL 6, RHEL 5 and Fedora 15

* Sun Sep 11 2011 Francois Andriot <francois.andriot@free.fr> - 3.5.13-0
- Import to GIT
