# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

%define tde_bindir %{tde_prefix}/bin
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

%define tde_tdeincludedir %{tde_includedir}/tde

%define _docdir %{tde_prefix}/share/doc

Name:		trinity-arts
Version:	3.5.13.2
Release:	1%{?dist}%{?_variant}
License:	GPL
Summary:	aRts (analog realtime synthesizer) - the KDE sound system
Group:		System Environment/Daemons 

Vendor:		Trinity Project
URL:		http://www.trinitydesktop.org/
Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	arts-3.5.13.1.tar.gz

BuildRequires:	trinity-tqtinterface-devel >= %{version}
BuildRequires:	audiofile-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	glib2-devel
BuildRequires:	gsl-devel
BuildRequires:	libvorbis-devel
BuildRequires:	esound-devel

%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}jack-devel
BuildRequires:	%{_lib}ltdl-devel
%endif
%if 0%{?rhel} >= 5 || 0%{?fedora}
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libtool-ltdl-devel
%endif
%if 0%{?suse_version}
BuildRequires:	libjack-devel
BuildRequires:	libltdl-devel
%endif

# TDE 3.5.13 specific building variables
BuildRequires: cmake >= 2.8

Requires:		trinity-tqtinterface >= %{version}
Requires:		audiofile

%if "%{?tde_prefix}" == "/usr"
Obsoletes:	arts
%endif

%description
arts (analog real-time synthesizer) is the sound system of KDE 3.

The principle of arts is to create/process sound using small modules which do
certain tasks. These may be create a waveform (oscillators), play samples,
filter data, add signals, perform effects like delay/flanger/chorus, or
output the data to the soundcard.

By connecting all those small modules together, you can perform complex
tasks like simulating a mixer, generating an instrument or things like
playing a wave file with some effects.

%files
%defattr(-,root,root,-)
%doc COPYING.LIB
%dir %{tde_libdir}/mcop
%dir %{tde_libdir}/mcop/Arts
%{tde_libdir}/mcop/Arts/*
%{tde_libdir}/mcop/*.mcopclass
%{tde_libdir}/mcop/*.mcoptype
%{tde_libdir}/lib*.so.*
%{tde_bindir}/artscat
%{tde_bindir}/artsd
%{tde_bindir}/artsdsp
%{tde_bindir}/artsplay
%{tde_bindir}/artsrec
%{tde_bindir}/artsshell
%{tde_bindir}/artswrapper
# The '.la' files are runtime, not devel !
%{tde_libdir}/lib*.la

%post
/sbin/ldconfig || :

%postun
/sbin/ldconfig || :

##########

%package devel
Group:		Development/Libraries
Summary:	%{name} - Development files
Requires:	%{name} = %{version}-%{release}
%if "%{?tde_prefix}" == "/usr"
Obsoletes:	arts-devel
%endif

%description devel
Development files for %{name}

%files devel
%defattr(-,root,root,-)
%{tde_bindir}/mcopidl
# Arts includes are under 'tde' - this is on purpose !
%{tde_tdeincludedir}/arts/
# Artsc includes are not under 'tde'.
%{tde_includedir}/artsc/
%{tde_bindir}/artsc-config
%{tde_libdir}/lib*.so
%{tde_libdir}/pkgconfig/*.pc
%{tde_libdir}/*.a

%post devel
/sbin/ldconfig || :

%postun devel
/sbin/ldconfig || :

##########

%if 0%{?suse_version}
%debug_package
%endif

##########


%prep
%setup -q -n arts-3.5.13.1

%build
unset QTDIR || : ; . /etc/profile.d/qt.sh
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

%if 0%{?rhel} || 0%{?fedora} || 0%{?suse_version}
%__mkdir_p build
cd build
%endif

%cmake \
  -DCMAKE_INSTALL_PREFIX=%{tde_prefix} \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir}/arts \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DPKGCONFIG_INSTALL_DIR=%{tde_libdir}/pkgconfig \
  -DWITH_ALSA=ON \
  -DWITH_AUDIOFILE=ON \
  -DWITH_VORBIS=ON \
  -DWITH_MAD=OFF \
  -DWITH_ESOUND=ON \
%if 0%{?rhel} == 4
  -DWITH_JACK=OFF \
%else
  -DWITH_JACK=ON \
%endif
  -DCMAKE_SKIP_RPATH="OFF" \
  ..


%__make %{?_smp_mflags}

%install
%__rm -rf %{?buildroot}
%__make install -C build DESTDIR=%{?buildroot}

%clean
%__rm -rf %{?buildroot}


%changelog
* Tue Sep 11 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial build for TDE 3.5.13.1
