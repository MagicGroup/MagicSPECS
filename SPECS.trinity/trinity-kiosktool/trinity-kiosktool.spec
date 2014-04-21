# Default version for this component
%define kdecomp kiosktool
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
%define tde_appdir %{tde_datadir}/applications

%define tde_tdeappdir %{tde_appdir}/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}


Name:		trinity-%{kdecomp}
Version:	1.0
Release:	4%{?dist}%{?_variant}
Summary:	tool to configure the TDE kiosk framework

License:	GPLv2+
Group:		Applications/Multimedia

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/


Source0: %{kdecomp}-trinity-%{tdeversion}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gettext
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1


%description
A Point&Click tool for system administrators to enable 
TDE's KIOSK features or otherwise preconfigure TDE for 
groups of users.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-trinity-%{tdeversion}

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
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --disable-rpath \
  --enable-new-ldflags \
  --disable-debug --disable-warnings \
  --disable-dependency-tracking --enable-final \
  --enable-closure \
  --with-extra-includes=%{tde_includedir}/tqt
  

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


%clean
%__rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{tde_datadir}/icons/crystalsvg ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/crystalsvg 2> /dev/null ||:
update-desktop-database >& /dev/null ||:

%postun
touch --no-create %{tde_datadir}/icons/crystalsvg ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/crystalsvg 2> /dev/null ||:
update-desktop-database >& /dev/null ||:



%files -f %{kdecomp}.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING README TODO
%{tde_bindir}/kiosktool
%{tde_bindir}/kiosktool-kdedirs
%{tde_tdeappdir}/kiosktool.desktop
%{tde_datadir}/apps/kiosktool/*.png
%{tde_tdedocdir}/HTML/en/kiosktool/
%{tde_datadir}/icons/crystalsvg/*/apps/kiosktool.png
%{tde_datadir}/apps/kiosktool/kiosk_data.xml
%{tde_datadir}/apps/kiosktool/kiosktoolui.rc

%changelog
* Fri Aug 02 2013 Liu Di <liudidi@gmail.com> - 1.0-4.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 1.0-3
- Initial build for TDE 3.5.13.1

* Wed May 02 2012 Francois Andriot <francois.andriot@free.fr> - 1.0-2
- Rebuilt for Fedora 17
- Fix post and postun

* Sat Nov 19 2011 Francois Andriot <francois.andriot@free.fr> - 1.0-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16
