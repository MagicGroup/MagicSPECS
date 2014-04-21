# Default version for this component
%define kdecomp dolphin
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
Summary:	File manager for TDE focusing on usability 
Version:	0.9.2
Release:	7%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:    %{_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	gettext


%description
Dolphin focuses on being only a file manager.
This approach allows to optimize the user
interface for the task of file management.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-trinity-%{tdeversion}

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i "admin/acinclude.m4.in" \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --docdir=%{tde_tdedocdir} \
  --libdir=%{tde_libdir} \
  --disable-rpath \
  --with-extra-includes=%{tde_includedir}/tqt

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# TDE 3.5.12: dirty hack to prevent duplicate line in file 'd3lphin.desktop'
sed -i "%{buildroot}%{tde_datadir}/applications/kde/d3lphin.desktop" \
	-e "/^Name\[pa\].*/d"

desktop-file-install --vendor ""                \
    --delete-original                           \
    --dir %{buildroot}%{tde_datadir}/applications/ \
    %{buildroot}%{tde_datadir}/applications/kde/d3lphin.desktop


## File lists
# HTML (1.0)
HTML_DIR=$(kde-config --expandvars --install html)
if [ -d %{buildroot}$HTML_DIR ]; then
for lang_dir in %{buildroot}$HTML_DIR/* ; do
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

# Makes 'media_safelyremove.desktop' an alternative
%__mv -f %{buildroot}%{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop %{buildroot}%{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop_d3lphin
%__ln_s /etc/alternatives/media_safelyremove.desktop_d3lphin %{buildroot}%{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop

%find_lang d3lphin

%clean
%__rm -rf %{buildroot}


%post
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
%if 0%{?suse_version}
update-alternatives --install \
%else
alternatives --install \
%endif
  %{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop \
  media_safelyremove.desktop_d3lphin \
  %{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop_d3lphin \
  10


%postun
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
if [ $1 -eq 0 ]; then
%if 0%{?suse_version}
  update-alternatives --remove \
%else
  alternatives --remove \
%endif
    media_safelyremove.desktop_d3lphin \
    %{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop_d3lphin
fi


%files -f d3lphin.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING TODO
%{tde_bindir}/d3lphin
%{tde_datadir}/applications/d3lphin.desktop
%{tde_datadir}/apps/d3lphin/
%{tde_datadir}/icons/hicolor/*/apps/d3lphin.png
%lang(en) %{tde_tdedocdir}/HTML/en/d3lphin/


%changelog
* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.9.2-6
- Initial build for TDE 3.5.13.1

* Sun Jul 08 2012 Francois Andriot <francois.andriot@free.fr> - 0.9.2-5
- Add alternatives with 'kio-umountwrapper'

* Tue May 01 2012 Francois Andriot <francois.andriot@free.fr> - 0.9.2-4
- Rebuild for Fedora 17
- Fix HTML installation directory

* Sun Oct 30 2011 Francois Andriot <francois.andriot@free.fr> - 0.9.2-3
- Rebuilt for TDE 3.5.13 on RHEL 6, RHEL 5 and Fedora 15

* Tue Sep 14 2011 Francois Andriot <francois.andriot@free.fr> - 0.9.2-2
- Import to GIT

* Mon Aug 22 2011 Francois Andriot <francois.andriot@free.fr> - 0.9.2-1
- Correct macro to install under "/opt", if desired

* Thu Jun 30 2011 Francois Andriot <francois.andriot@free.fr> - 0.9.2-0
- Initial build for RHEL 6.0
- Based on FC7 'Dolphin 0.8.2-2" SPEC file.

