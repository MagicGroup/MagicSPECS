# Default version for this component
%define kdecomp libkdcraw

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

%define tde_tdeappdir %{tde_datadir}/applications/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}


Name:		trinity-%{kdecomp}
Summary:	Raw picture decoding C++ library (runtime) [Trinity]

Version:	3.5.13.2
Release:	1%{?dist}%{?_variant}

License:	GPLv2+
Group:		Environment/Libraries

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:		%{_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{version}.tar.xz

BuildRequires: trinity-tqtinterface-devel >= %{version}
BuildRequires: trinity-arts-devel >= %{version}
BuildRequires: trinity-tdelibs-devel >= %{version}
BuildRequires: desktop-file-utils
%if 0%{?suse_version}
BuildRequires: liblcms-devel
%else
BuildRequires: lcms-devel
%endif
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig
BuildRequires: automake autoconf libtool
BuildRequires: gettext


%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}ltdl-devel
%else
BuildRequires:	libtool-ltdl-devel
%endif

%description
C++ interface around dcraw binary program used to decode RAW
picture files.
This library is used by kipi-plugins, digiKam and others kipi host programs.
libkdcraw contains the library of libkdcraw.

%package devel
Group:		Development/Libraries
Summary:	RAW picture decoding C++ library (development) [Trinity]
Requires:	%{name} = %{version}

%description devel
Libkdcraw is a C++ interface around dcraw binary program used to
decode Raw picture files.
libkdcraw-devel contains development files and documentation. The
library documentation is available on kdcraw.h header file.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-trinity-%{version}

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR || : ; source /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

%configure \
    --prefix=%{tde_prefix} \
    --exec-prefix=%{tde_prefix} \
	--datadir=%{tde_datadir} \
	--libdir=%{tde_libdir} \
	--includedir=%{tde_tdeincludedir} \
	--disable-rpath \
    --with-extra-includes=%{tde_includedir}/tqt

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%find_lang %{kdecomp}


%clean
%__rm -rf %{buildroot}


%post
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${f} 2> /dev/null ||:
done
/sbin/ldconfig || :

%postun
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${f} 2> /dev/null ||:
done
/sbin/ldconfig || :

%post devel
/sbin/ldconfig || :

%postun devel
/sbin/ldconfig || :


%files -f %{kdecomp}.lang
%defattr(-,root,root,-)
%{tde_libdir}/libkdcraw.so.4
%{tde_libdir}/libkdcraw.so.4.0.3
%{tde_datadir}/icons/hicolor/*/apps/kdcraw.png

%files devel
%defattr(-,root,root,-)
%{tde_libdir}/libkdcraw.so
%{tde_libdir}/libkdcraw.la
%{tde_tdeincludedir}/libkdcraw/
%{tde_libdir}/pkgconfig/libkdcraw.pc

%Changelog
* Tue Oct 02 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial release for TDE 3.5.13.1
