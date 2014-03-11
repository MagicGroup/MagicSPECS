# Default version for this component
%define kdecomp kdesvn

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


Name:		trinity-%{kdecomp}
Summary:	subversion client with tight KDE integration [Trinity]
Version:	1.0.4
Release:	4%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.elliptique.net/~ken/kima/

Prefix:    %{_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-3.5.13.1.tar.gz

# [kdesvn] Fix "not a string literal" error
Patch2:		kdesvn-3.5.13-fix_not_a_string_literal_error.patch

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	subversion-devel
Requires:		trinity-kdesvn-kio-plugins = %{version}-%{release}


%description
KDESvn is a graphical client for the subversion revision control
system (svn).

Besides offering common and advanced svn operations, it features
a tight integration into KDE and can be embedded into other KDE 
applications like konqueror via the KDE component technology KParts.


%package -n trinity-libsvnqt
Group:		Development/Libraries
Summary: Qt wrapper library for subversion [Trinity]

%description -n trinity-libsvnqt
This package provides svnqt, a Qt wrapper library around the 
subversion library.

It is based on the RapidSvn SvnCpp library, a subversion client API 
written in C++.

%package -n trinity-libsvnqt-devel
Group:		Development/Libraries
Requires:	trinity-libsvnqt = %{version}-%{release}
Requires:	qt-devel
Requires:	subversion-devel
Summary:	Qt wrapper library for subversion (development files) [Trinity]

%description -n trinity-libsvnqt-devel
This package contains the header files and symbolic links that developers
using svnqt will need.


%package kio-plugins
Group:		Development/Libraries
Conflicts:	trinity-kdesdk-kio-plugins
Summary:	subversion I/O slaves for Trinity

%description kio-plugins
This packages includes KIO slaves for svn, svn+file, svn+http, 
svn+https, svn+ssh. This allows you to access subversion repositories 
inside any KIO enabled KDE application.

This package is part of tdesvn-trinity.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-3.5.13.1
%patch2 -p1 -b .stringliteral

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
find . -name CMakeLists.txt -exec %__sed -i {} \
  -e "s,/usr/include/tqt,%{tde_includedir}/tqt,g" \
  -e "s,/usr/bin/tmoc,%{tde_bindir}/tmoc,g" \
  -e "s,/usr/bin/uic-tqt,%{tde_bindir}/uic-tqt,g" \
  \;

# More ugly hack to add TQT include directory in CMakeLists.txt	
%__sed -i CMakeLists.txt \
  -e "s,^\(INCLUDE_DIRECTORIES (\)$,\1\n%{tde_includedir}/tqt,"

# Moves HTML files to the correect location
find . -name "*.cmake" -exec %__sed -i {} \
  -e "s,/doc/HTML,/doc/kde/HTML,g" \
  \;

%build
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${QTDIR}/bin:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

export CMAKE_INCLUDE_PATH="%{tde_tdeincludedir}"

%if 0%{?rhel} || 0%{?fedora} || 0%{?suse_version}
%__mkdir_p build
cd build
%endif

%cmake \
  -DCMAKE_INSTALL_PREFIX=%{tde_prefix} \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DINCLUDE_INSTALL_DIR=%{tde_includedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DMAN_INSTALL_DIR=%{tde_mandir}/man1 \
  -DDATA_INSTALL_DIR=%{tde_datadir} \
  -DPKGCONFIG_INSTALL_DIR=%{tde_tdelibdir}/pkgconfig \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  -DCMAKE_SKIP_RPATH="OFF" \
  ..

# SMP safe !
%__make %{?_smp_mflags}


%install
export PATH="%{_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot} -C build


%find_lang %{kdecomp} || touch %{kdecomp}.lang

# Installs SVN protocols as alternatives
%__mv -f %{?buildroot}%{tde_datadir}/services/svn+file.protocol %{?buildroot}%{tde_datadir}/services/svn+file.protocol_tdesvn
%__mv -f %{?buildroot}%{tde_datadir}/services/svn+http.protocol %{?buildroot}%{tde_datadir}/services/svn+http.protocol_tdesvn
%__mv -f %{?buildroot}%{tde_datadir}/services/svn+https.protocol %{?buildroot}%{tde_datadir}/services/svn+https.protocol_tdesvn
%__mv -f %{?buildroot}%{tde_datadir}/services/svn+ssh.protocol %{?buildroot}%{tde_datadir}/services/svn+ssh.protocol_tdesvn
%__mv -f %{?buildroot}%{tde_datadir}/services/svn.protocol %{?buildroot}%{tde_datadir}/services/svn.protocol_tdesvn
%__ln_s /etc/alternatives/svn+file.protocol %{?buildroot}%{tde_datadir}/services/svn+file.protocol
%__ln_s /etc/alternatives/svn+http.protocol %{?buildroot}%{tde_datadir}/services/svn+http.protocol
%__ln_s /etc/alternatives/svn+https.protocol %{?buildroot}%{tde_datadir}/services/svn+https.protocol
%__ln_s /etc/alternatives/svn+ssh.protocol %{?buildroot}%{tde_datadir}/services/svn+ssh.protocol
%__ln_s /etc/alternatives/svn.protocol %{?buildroot}%{tde_datadir}/services/svn.protocol


%clean
%__rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%postun
touch --no-create %{_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%post -n trinity-libsvnqt
/sbin/ldconfig || :

%post kio-plugins
for proto in svn+file svn+http svn+https svn+ssh svn; do
%if 0%{?suse_version}
  update-alternatives --install \
%else
  alternatives --install \
%endif
    %{tde_datadir}/services/${proto}.protocol \
    ${proto}.protocol \
    %{tde_datadir}/services/${proto}.protocol_tdesvn \
    20
done

%preun kio-plugins
if [ $1 -eq 0 ]; then
  for proto in svn+file svn+http svn+https svn+ssh svn; do
%if 0%{?suse_version}
    update-alternatives --remove \
%else
    alternatives --remove \
%endif
      ${proto}.protocol \
      %{tde_datadir}/services/${proto}.protocol_tdesvn
  done
fi



%postun -n trinity-libsvnqt
/sbin/ldconfig || :


%files -f %{kdecomp}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{tde_bindir}/kdesvn
%{tde_bindir}/kdesvnaskpass
%{tde_tdelibdir}/libkdesvnpart.la
%{tde_tdelibdir}/libkdesvnpart.so
%{tde_datadir}/applications/kde/kdesvn.desktop
%{tde_datadir}/apps/kconf_update/kdesvn-use-external-update.sh
%{tde_datadir}/apps/kconf_update/kdesvnpartrc-use-external.upd
%{tde_datadir}/apps/kdesvn/kdesvnui.rc
%{tde_datadir}/apps/kdesvnpart/kdesvn_part.rc
%{tde_datadir}/apps/konqueror/servicemenus/kdesvn_subversion.desktop
%{tde_datadir}/config.kcfg/kdesvn_part.kcfg
%{tde_datadir}/icons/hicolor/*/*/*.png
%{tde_datadir}/icons/hicolor/*/*/*.svgz
%{tde_mandir}/man1/kdesvn.1
%{tde_mandir}/man1/kdesvnaskpass.1
%{tde_tdedocdir}/HTML/*/

%files -n trinity-libsvnqt
%{tde_libdir}/libsvnqt.so.4
%{tde_libdir}/libsvnqt.so.4.2.2

%files -n trinity-libsvnqt-devel
%{tde_includedir}/svnqt
%{tde_libdir}/libsvnqt.so

%files kio-plugins
%{tde_datadir}/services/kded/kdesvnd.desktop
%{tde_datadir}/services/ksvn+file.protocol
%{tde_datadir}/services/ksvn+http.protocol
%{tde_datadir}/services/ksvn+https.protocol
%{tde_datadir}/services/ksvn+ssh.protocol
%{tde_datadir}/services/ksvn.protocol
%{tde_datadir}/services/svn+file.protocol
%{tde_datadir}/services/svn+http.protocol
%{tde_datadir}/services/svn+https.protocol
%{tde_datadir}/services/svn+ssh.protocol
%{tde_datadir}/services/svn.protocol
%{tde_datadir}/services/svn+file.protocol_tdesvn
%{tde_datadir}/services/svn+http.protocol_tdesvn
%{tde_datadir}/services/svn+https.protocol_tdesvn
%{tde_datadir}/services/svn+ssh.protocol_tdesvn
%{tde_datadir}/services/svn.protocol_tdesvn
%{tde_tdelibdir}/kio_ksvn.la
%{tde_tdelibdir}/kio_ksvn.so
%{tde_tdelibdir}/kded_kdesvnd.la
%{tde_tdelibdir}/kded_kdesvnd.so


%changelog
* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 1.0.4-4
- Initial build for TDE 3.5.13.1

* Mon Jul 30 2012 Francois Andriot <francois.andriot@free.fr> - 1.0.4-3
- Installs SVN protocols as alternative, avoids conlict with TDESDK

* Tue May 01 2012 Francois Andriot <francois.andriot@free.fr> - 1.0.4-2
- Rebuilt for Fedora 17
- Fix post and postun
- Fix compilation with GCC 4.7
 
* Thu Dec 01 2011 Francois Andriot <francois.andriot@free.fr> - 1.0.4-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16
