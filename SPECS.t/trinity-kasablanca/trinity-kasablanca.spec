%define kdecomp kasablanca

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
Summary:	Graphical FTP client
Version:	0.4.0.2
Release:	2%{?dist}%{?_variant}

License:	GPLv2+
Url:		http://kasablanca.berlios.de/ 
Source:		http://download.berlios.de/kasablanca/kasablanca-%{version}.tar.gz
Group:		Applications/Internet 
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# [kasablanca] Fix bad content in icon (?)
Patch1:		kasablanca-0.4.0.2-dt.patch
# [kasablanca] Fix detection of newer autotools
Patch2:		kasablanca-0.4.0.2-fix_autotools_detection.patch
# [kasablanca] Missing LDFLAGS cause FTBFS
Patch3:		kasablanca-0.4.0.2-missing_ldflags.patch

BuildRequires: desktop-file-utils
BuildRequires: gettext 
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires: openssl-devel

%if 0%{?suse_version}
BuildRequires: utempter-devel
%else
BuildRequires: libutempter-devel
%endif

%description
Kasablanca is an ftp client, among its features are currently: 
* ftps encryption via AUTH TLS
* fxp (direct server to server transfer), supporting alternative mode.
* advanced bookmarking system.
* fast responsive multithreaded engine.
* concurrent connections to multiple hosts.
* interactive transfer queue, movable by drag and drop.
* small nifty features, like a skiplist.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-%{version}
%patch1 -p1 -b .dt
%patch2 -p1
%patch3 -p1 -b .ldflags

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

export KDEDIR=%{tde_prefix}

## Needed(?) for older/legacy setups, harmless otherwise
if pkg-config openssl ; then
	export CPPFLAGS="$CPPFLAGS $(pkg-config --cflags-only-I openssl)"
fi

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --includedir=%{tde_tdeincludedir} \
  --datadir=%{tde_datadir} \
  --with-qt-libraries=${QTLIB:-${QTDIR}/%{_lib}} \
  --disable-static \
  --disable-rpath \
  --disable-debug --disable-warnings \
  --disable-dependency-tracking --enable-final \
  --with-extra-includes=%{tde_includedir}/tqt

%__make %{?_smp_mflags} LIBTOOL=$(which libtool)


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf $RPM_BUILD_ROOT 

%__make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install \
  --dir $RPM_BUILD_ROOT%{tde_datadir}/applications/kde \
  --vendor="" \
  --add-category="Network" \
  --add-category="KDE" \
  --delete-original \
  $RPM_BUILD_ROOT%{tde_datadir}/applnk/*/*.desktop

## File lists
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

# locale's
%find_lang %{kdecomp}

%clean
%__rm -rf $RPM_BUILD_ROOT 


%post
touch --no-create %{tde_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{tde_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{tde_datadir}/icons/hicolor &> /dev/null || :


%files -f %{kdecomp}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README 
%{tde_bindir}/kasablanca
%{tde_tdeappdir}/kasablanca.desktop
%{tde_datadir}/apps/kasablanca/
%{tde_datadir}/config.kcfg/kbconfig.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kasablanca.png
%{tde_tdedocdir}/HTML/en/kasablanca/

%changelog
* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.4.0.2-2
- Initial build for TDE 3.5.13.1

* Sun Dec 04 2011 Francois Andriot <francois.andriot@free.fr> - 0.4.0.2-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16
- Based on Fedora 12 Spec 'kasablanca-0.4.0.2-17'
