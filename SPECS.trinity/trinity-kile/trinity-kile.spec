#
# spec file for package kile (version R14)
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
%define tde_pkg kile
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		2.0.3
Release:		%{?!preversion:8}%{?preversion:7_%{preversion}}%{?dist}%{?_variant}.3
Summary:		TDE Integrated LaTeX Environment [Trinity]
Summary(zh_CN.UTF-8): TDE 下的 LaTeX 集成环境
Group:			Applications/Publishing
Group(zh_CN.UTF-8): 应用程序/出版
URL:			http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

Obsoletes: %{name}-i18n-ar
Obsoletes: %{name}-i18n-bg
Obsoletes: %{name}-i18n-br
Obsoletes: %{name}-i18n-ca
Obsoletes: %{name}-i18n-cs
Obsoletes: %{name}-i18n-cy
Obsoletes: %{name}-i18n-da
Obsoletes: %{name}-i18n-de
Obsoletes: %{name}-i18n-el
Obsoletes: %{name}-i18n-engb
Obsoletes: %{name}-i18n-es
Obsoletes: %{name}-i18n-et
Obsoletes: %{name}-i18n-eu
Obsoletes: %{name}-i18n-fi
Obsoletes: %{name}-i18n-fr
Obsoletes: %{name}-i18n-ga
Obsoletes: %{name}-i18n-gl
Obsoletes: %{name}-i18n-hi
Obsoletes: %{name}-i18n-hu
Obsoletes: %{name}-i18n-is
Obsoletes: %{name}-i18n-it
Obsoletes: %{name}-i18n-ja
Obsoletes: %{name}-i18n-lt
Obsoletes: %{name}-i18n-ms
Obsoletes: %{name}-i18n-mt
Obsoletes: %{name}-i18n-nb
Obsoletes: %{name}-i18n-nds
Obsoletes: %{name}-i18n-nl
Obsoletes: %{name}-i18n-nn
Obsoletes: %{name}-i18n-pa
Obsoletes: %{name}-i18n-pl
Obsoletes: %{name}-i18n-pt
Obsoletes: %{name}-i18n-ptbr
Obsoletes: %{name}-i18n-ro
Obsoletes: %{name}-i18n-ru
Obsoletes: %{name}-i18n-rw
Obsoletes: %{name}-i18n-sk
Obsoletes: %{name}-i18n-sr
Obsoletes: %{name}-i18n-srlatin
Obsoletes: %{name}-i18n-sv
Obsoletes: %{name}-i18n-ta
Obsoletes: %{name}-i18n-th
Obsoletes: %{name}-i18n-tr
Obsoletes: %{name}-i18n-uk
Obsoletes: %{name}-i18n-zhcn


%description
Kile is a user-friendly LaTeX source editor and TeX shell for TDE.

The source editor is a multi-document editor designed for .tex and .bib
files.  Menus, wizards and auto-completion are provided to assist with
tag insertion and code generation.  A structural view of the document
assists with navigation within source files.

The TeX shell integrates the various tools required for TeX processing.
It assists with LaTeX compilation, DVI and postscript document viewing,
generation of bibliographies and indices and other common tasks.

Kile can support large projects consisting of several smaller files.

%description -l zh_CN.UTF-8
TDE 下的 LaTeX 集成环境。

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

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%__chmod +x %{buildroot}%{tde_datadir}/apps/kile/test/runTests.sh

# Unwanted files ...
%__rm -f %{?buildroot}%{tde_datadir}/apps/katepart/syntax/bibtex.xml
%__rm -f %{?buildroot}%{tde_datadir}/apps/katepart/syntax/latex.xml
%__rm -rf %{?buildroot}%{tde_datadir}/doc/tde/HTML/da
%__rm -rf %{?buildroot}%{tde_datadir}/doc/tde/HTML/es
%__rm -rf %{?buildroot}%{tde_datadir}/doc/tde/HTML/et
%__rm -rf %{?buildroot}%{tde_datadir}/doc/tde/HTML/it
%__rm -rf %{?buildroot}%{tde_datadir}/doc/tde/HTML/nl
%__rm -rf %{?buildroot}%{tde_datadir}/doc/tde/HTML/pt
%__rm -rf %{?buildroot}%{tde_datadir}/doc/tde/HTML/sv
magic_rpm_clean.sh
%find_lang %{tde_pkg} || :

%clean
%__rm -rf %{buildroot}


%post
update-desktop-database %{tde_tdeappdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :

%postun
update-desktop-database %{tde_tdeappdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_bindir}/kile
%{tde_tdeappdir}/kile.desktop
%{tde_datadir}/apps/tdeconf_update
%{tde_datadir}/apps/kile
%{tde_datadir}/config.kcfg/kile.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kile.png
%{tde_datadir}/icons/hicolor/scalable/apps/kile.svgz
%{tde_tdedocdir}/HTML/en/kile
%{tde_datadir}/mimelnk/text/x-kilepr.desktop

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 2:2.0.3-8.3
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:2.0.3-8.2
- 为 Magic 3.0 重建

* Sun Oct 11 2015 Liu Di <liudidi@gmail.com> - 2:2.0.3-8.1
- 为 Magic 3.0 重建

* Mon Jul 29 2013 Francois Andriot <francois.andriot@free.fr> - 2:2.0.2-1
- Initial release for TDE 14.0.0
