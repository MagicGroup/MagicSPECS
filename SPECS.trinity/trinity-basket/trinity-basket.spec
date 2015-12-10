#
# spec file for package basket (version R14)
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
%define tde_pkg basket
%define tde_prefix /opt/trinity
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


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.0.3.1
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.2
Summary:	Taking care of your ideas
Summary(zh_CN.UTF-8): 知识管理工具
Group:		Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		trinity-basket-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	trinity-tdepim-devel >= %{tde_version}

BuildRequires:	desktop-file-utils
BuildRequires:	gpgme-devel

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	libtool

%description
This application is mainly an all-purpose notes taker. It provide several baskets where
to drop every sort of items: text, rich text, links, images, sounds, files, colors,
application launcher... Objects can be edited, copied, dragged... So, you can arrange
them as you want ! This application can be used to quickly drop web objects (link, text,
images...) or notes, as well as to free your clutered desktop (if any). It is also useful
to collect informations for a report. Those data can be shared with co-workers by exporting
baskets to HTML.

%description -l zh_CN.UTF-8
一款知识管理工具。

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export kde_confdir="%{tde_confdir}"

# Warning: --enable-final causes FTBFS
%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --disable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

magic_rpm_clean.sh
%find_lang %{tde_pkg}

# Apps that should stay in TDE
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_tdeappdir}/%{tde_pkg}.desktop"


%clean
%__rm -rf %{buildroot}


%post
for f in crystalsvg ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig
update-desktop-database %{tde_tdeappdir} -q &> /dev/null

%postun
for f in crystalsvg ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig
update-desktop-database %{tde_tdeappdir} -q &> /dev/null


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_bindir}/basket
%{tde_tdeappdir}/basket.desktop
%{tde_datadir}/apps/basket/
%dir %{tde_datadir}/apps/kontact/ksettingsdialog
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
%{tde_confdir}/magic/basket.magic
%{tde_datadir}/icons/crystalsvg/*/*/*
%{tde_datadir}/mimelnk/application/x-basket-archive.desktop
%{tde_datadir}/mimelnk/application/x-basket-template.desktop
%{tde_datadir}/services/basket_config_apps.desktop
%{tde_datadir}/services/basket_config_baskets.desktop
#%{tde_datadir}/services/basket_config_features.desktop
%{tde_datadir}/services/basket_config_general.desktop
%{tde_datadir}/services/basket_config_new_notes.desktop
#%{tde_datadir}/services/basket_config_notes.desktop
%{tde_datadir}/services/basket_config_notes_appearance.desktop
%{tde_datadir}/services/basket_part.desktop
%{tde_datadir}/services/basketthumbcreator.desktop
%{tde_datadir}/services/kontact/basket.desktop
%{tde_datadir}/services/kontact/basket_v4.desktop
%{tde_tdedocdir}/HTML/en/basket/


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 2:1.0.3.1-1.2
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:1.0.3.1-1.1
- 为 Magic 3.0 重建

* Mon Jul 29 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.0.3.1-1
- Initial release for TDE 14.0.0
