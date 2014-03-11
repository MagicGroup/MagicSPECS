# Default version for this component
%define kdecomp kaffeine
%define tdeversion 3.5.13.2

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
Summary:	Xine-based media player

Version:	0.8.8
Release:	5%{?dist}%{?_variant}

License: GPLv2+
Group:   Applications/Multimedia
URL:     http://kaffeine.sourceforge.net/

Source0:	kaffeine-trinity-%{tdeversion}.tar.xz

# [kaffeine] Add Xine 1.2 support
Patch1:		kaffeine-3.5.13.1-add_xine12_support.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gettext
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires: libvorbis-devel
BuildRequires: libcdio-devel

%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	libcdda-devel
BuildRequires:	%{_lib}xext%{?mgaversion:6}-devel
BuildRequires:	%{_lib}xtst-devel
BuildRequires:	%{_lib}xinerama%{?mgaversion:1}-devel
# dvb
BuildRequires:	kernel-headers
BuildRequires:	libgstreamer-devel >= 0.10
BuildRequires:	libgstreamer-plugins-base-devel >= 0.10
%else
BuildRequires:	cdparanoia
BuildRequires:	cdparanoia-devel
%if 0%{?suse_version}
BuildRequires:	libcdio-paranoia-devel
%endif
BuildRequires:	libXext-devel 
BuildRequires:	libXtst-devel
BuildRequires:	libXinerama-devel
# dvb
BuildRequires:	gstreamer-devel >= 0.10
%if 0%{?suse_version}
BuildRequires:	gstreamer-0_10-plugins-base-devel
%else
BuildRequires:	gstreamer-plugins-base-devel >= 0.10
BuildRequires:	glibc-kernheaders 
%endif
%endif

%if 0%{?rhel} >= 6 || 0%{?fedora} >= 15
BuildRequires: libxcb-devel
%endif

# xine-lib
%if 0%{?mgaversion} || 0%{?mdkversion} || 0%{?suse_version}
BuildRequires:  libxine-devel
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:  xine-lib-devel
%endif

Requires: %{name}-libs = %{version}-%{release}

%description
Kaffeine is a xine-based media player for KDE.  It plays back CDs,
and VCDs, and can decode all (local or streamed) multimedia formats 
supported by xine-lib.
Additionally, Kaffeine is fully integrated in KDE, it supports drag
and drop and provides an editable playlist, a bookmark system, a
Konqueror plugin, OSD and much more.

%files -f %{kdecomp}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{tde_bindir}/kaffeine
%{tde_libdir}/libkaffeinepart.so
%{tde_tdelibdir}/lib*.*
%{tde_datadir}/appl*/*/*.desktop
%{tde_datadir}/apps/gstreamerpart/
%{tde_datadir}/apps/kaffeine/
%{tde_datadir}/apps/konqueror/servicemenus/*.desktop
%{tde_datadir}/apps/profiles/
%{tde_datadir}/icons/hicolor/*/*/*
%{tde_datadir}/mimelnk/*/*.desktop
%{tde_datadir}/service*/*.desktop
%{tde_tdedocdir}/HTML/en/kaffeine/

%post
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database >& /dev/null ||:
/sbin/ldconfig || :

%postun
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database >& /dev/null ||:
/sbin/ldconfig || :

##########

%package devel
Summary: Development files for %{name}
Group:   Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	trinity-tdelibs-devel

%description devel
%{summary}.

%files devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/kaffeine/
%{tde_libdir}/lib*.so
%exclude %{tde_libdir}/libkaffeinepart.so

%post devel
/sbin/ldconfig || :

%postun devel
/sbin/ldconfig || :

##########

%package libs
Summary: %{name} runtime libraries
Group:   System Environment/Libraries

# include to be paranoid, installing libs-only is still mostly untested -- Rex
Requires: %{name} = %{version}-%{release}

%description libs
%{summary}.

%files libs
%defattr(-,root,root,-)
%{tde_libdir}/lib*.so.*

%post libs
/sbin/ldconfig || :

%postun libs
/sbin/ldconfig || :

##########


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n kaffeine-trinity-%{tdeversion}

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"

%build
unset QTDIR || : ; source /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"


%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --mandir=%{tde_mandir} \
  --enable-new-ldflags \
  --disable-debug --disable-warnings \
  --disable-dependency-tracking --enable-final \
  --disable-rpath \
  --with-xinerama \
  --with-gstreamer \
  --without-lame \
  --with-extra-includes=%{tde_includedir}/tqt \
  --with-extra-libs=%{_prefix}/%{_lib} \
  --enable-closure \
%if 0%{?rhel} > 0 && 0%{?rhel} <= 5
  --without-dvb \
%endif
  

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf $RPM_BUILD_ROOT
%__make install DESTDIR=$RPM_BUILD_ROOT

## File lists
# locale's
%find_lang %{kdecomp}
# HTML (1.0)
HTML_DIR=$(kde-config --expandvars --install html)
if [ -d $RPM_BUILD_ROOT$HTML_DIR ]; then
for lang_dir in $RPM_BUILD_ROOT$HTML_DIR/* ; do
  if [ -d $lang_dir ]; then
    lang=$(basename $lang_dir)
    echo "%lang($lang) $HTML_DIR/$lang/*" >> %{name}.lang
    # replace absolute symlinks with relative ones
    pushd $lang_dir
      for i in *; do
        [ -d $i -a -L $i/common ] && rm -f $i/common && ln -sf ../common $i/common
      done
    popd
  fi
done
fi

# Unpackaged files
rm -f $RPM_BUILD_ROOT%{tde_libdir}/lib*.la
rm -f $RPM_BUILD_ROOT%{tde_datadir}/mimelnk/application/x-mplayer2.desktop

%clean
rm -rf $RPM_BUILD_ROOT



%changelog
* Wed Jul 31 2013 Liu Di <liudidi@gmail.com> - 0.8.8-5.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.8.8-4
- Initial build for TDE 3.5.13.1

* Fri Aug 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.8.8-3
- Add support for Mageia 2 and Mandriva 2011
- Added automake initialization with proper program name and version [Bug #858] [Commit #4e982fa3]
- Fixed online hyperlink to win32 codecs download location. [Commit #5086f358]

* Tue May 01 2012 Francois Andriot <francois.andriot@free.fr> - 0.8.8-2
- Rebuilt for Fedora 17
- Adds more patches from GIT.

* Mon Apr 23 2012 Francois Andriot <francois.andriot@free.fr> - 0.8.8-1
- Updates version to 0.8.8
- Fix nominal "tqt" typos and fix slow DVB start. [Bug #729, #899]
- Change location where Kaffeine stores temporary pipe files from $HOME to the more appropriate $KDEHOME/tmp-$HOSTNAME.
- Work around Xine crash when displaying still logo image by creating a small movie file to replace it [Bug #511, #559]
- Add man page

* Sun Dec 04 2011 Francois Andriot <francois.andriot@free.fr> - 0.8.6-2
- Disable 'libxcb-devel' for RHEL 5 compilation
- Fix HTML directory location

* Wed Nov 09 2011 Francois Andriot <francois.andriot@free.fr> - 0.8.6-1
- Spec file based on Fedora 8 'kaffeine-0.8.6-3'
