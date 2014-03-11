# Default version for this component
%define kdecomp basket
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
Summary:	Taking care of your ideas.
Version:	1.0.3.1
Release:	4%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz

# [basket] Fix compilation with GCC 4.7
Patch1:	basket-3.5.13-fix_gcc47_compilation.patch

BuildRequires: trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires: trinity-tdelibs-devel >= 3.5.13.1
BuildRequires: trinity-tdebase-devel >= 3.5.13.1
BuildRequires: trinity-tdepim-devel >= 3.5.13.1
BuildRequires: desktop-file-utils

BuildRequires: gpgme-devel

%description
This application is mainly an all-purpose notes taker. It provide several baskets where
to drop every sort of items: text, rich text, links, images, sounds, files, colors,
application launcher... Objects can be edited, copied, dragged... So, you can arrange
them as you want ! This application can be used to quickly drop web objects (link, text,
images...) or notes, as well as to free your clutered desktop (if any). It is also useful
to collect informations for a report. Those data can be shared with co-workers by exporting
baskets to HTML.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-trinity-%{tdeversion}
%patch1 -p1

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
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
	--includedir=%{tde_tdeincludedir} \
	--libdir=%{tde_libdir} \
	--datadir=%{tde_datadir} \
	--disable-rpath \
    --with-extra-includes=%{tde_includedir}/tqt \
    --disable-static

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%find_lang %{kdecomp}

%clean
%__rm -rf %{buildroot}


%post
for f in crystalsvg ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig

%postun
for f in crystalsvg ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig


%files -f %{kdecomp}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_bindir}/basket
%{tde_tdeappdir}/basket.desktop
%{tde_datadir}/apps/basket/
%{tde_datadir}/apps/kontact/ksettingsdialog/kontact_basketplugin.setdlg
%{tde_libdir}/libbasketcommon.la
%{tde_libdir}/libbasketcommon.so
%{tde_tdelibdir}/basketthumbcreator.la
%{tde_tdelibdir}/basketthumbcreator.so
%{tde_tdelibdir}/kcm_basket.la
%{tde_tdelibdir}/kcm_basket.so
%{tde_tdelibdir}/libbasketpart.la
%{tde_tdelibdir}/libbasketpart.so
%{tde_tdelibdir}/libkontact_basket.la
%{tde_tdelibdir}/libkontact_basket.so
%{tde_datadir}/config/magic/basket.magic
%{tde_datadir}/icons/crystalsvg/*/*/*
%{tde_datadir}/mimelnk/application/x-basket-archive.desktop
%{tde_datadir}/mimelnk/application/x-basket-template.desktop
%{tde_datadir}/services/basket_config_apps.desktop
%{tde_datadir}/services/basket_config_baskets.desktop
%{tde_datadir}/services/basket_config_features.desktop
%{tde_datadir}/services/basket_config_general.desktop
%{tde_datadir}/services/basket_config_new_notes.desktop
%{tde_datadir}/services/basket_config_notes.desktop
%{tde_datadir}/services/basket_config_notes_appearance.desktop
%{tde_datadir}/services/basket_part.desktop
%{tde_datadir}/services/basketthumbcreator.desktop
%{tde_datadir}/services/kontact/basket.desktop
%{tde_datadir}/services/kontact/basket_v4.desktop
%{tde_tdedocdir}/HTML/en/basket/


%Changelog
* Tue Oct 02 2012 Francois Andriot <francois.andriot@free.fr> - 1.0.3.1-3
- Initial release for TDE 3.5.13.1
