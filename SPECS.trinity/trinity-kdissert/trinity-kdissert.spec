#
# spec file for package kdissert (version R14)
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

# Default version for this component
%define tde_pkg kdissert
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif

%define tde_prefix /opt/trinity

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_appdir %{tde_datadir}/applications

%define tde_tdeappdir %{tde_appdir}/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}


Name:			trinity-%{tde_pkg}
Summary:        Mindmapping Tool
Summary(zh_CN.UTF-8): 思维导图工具
Version:		1.0.6c
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1

License:		GPLv2+
Group:			Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
Vendor:			Trinity Project
Packager:		Francois Andriot <francois.andriot@free.fr>
#URL:			http://www.trinitydesktop.org/
URL:            http://freehackers.org/~tnagy/kdissert/

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{tde_pkg}-14.0.0.tar.gz
Source1:		TDE.py

BuildRequires:	trinity-tqtinterface-devel >= %{tde_version}
BuildRequires:	trinity-arts-devel >= 1:1.5.10
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext


%description
KDissert is a mindmapping tool dedicated to the creation of complex
documents: dissertations, thesis, presentations, and reports. It
features several document generators: latex reports, latex slides
(based on Prosper and Beamer), OpenOffice.org writer and impress, html,
and plain text.

%description -l zh_CN.UTF-8
思维导图工具。


%prep
%setup -q -n %{tde_pkg}-%{version}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%__rm -rf "$HOME/.waf*" 
./waf || :
%__install -D "%{SOURCE1}" "$HOME/.waf-0.9.0/wafadmin/Tools/KDE3.py"

export CPPFLAGS="${CPPFLAGS} -I%{tde_tdeincludedir} -I%{_includedir}/tqt -I%{_includedir}/tqt3"

./waf configure --libsuffix=64 \
%ifarch x86_64 ppc64 s390x
	--libsuffix=64 \
%endif
	--prefix=%{tde_prefix} \
	--qtdir=/usr \
	--qtincludes=/usr/include/tqt3 \
	--kdeincludes=%{tde_tdeincludedir}

./waf


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
./waf --destdir=%{buildroot} install
magic_rpm_clean.sh
%find_lang %{tde_pkg} || :


%clean
%__rm -rf %{buildroot}
%__rm -rf "$HOME/.waf*" 


%post
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig


%postun
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig


%files
%defattr(-,root,root,-)
%{tde_bindir}/kdissert
%{tde_tdelibdir}/libkdissOOOdoc.la
%{tde_tdelibdir}/libkdissOOOdoc.so
%{tde_tdelibdir}/libkdissOOOimpress.la
%{tde_tdelibdir}/libkdissOOOimpress.so
%{tde_tdelibdir}/libkdissapplet.la
%{tde_tdelibdir}/libkdissapplet.so
%{tde_tdelibdir}/libkdissasciidoc.la
%{tde_tdelibdir}/libkdissasciidoc.so
%{tde_tdelibdir}/libkdissbeamerslides.la
%{tde_tdelibdir}/libkdissbeamerslides.so
%{tde_tdelibdir}/libkdissdocbook.la
%{tde_tdelibdir}/libkdissdocbook.so
%{tde_tdelibdir}/libkdisshtmldoc.la
%{tde_tdelibdir}/libkdisshtmldoc.so
%{tde_tdelibdir}/libkdisspdflatexarticle.la
%{tde_tdelibdir}/libkdisspdflatexarticle.so
%{tde_tdelibdir}/libkdisspdflatexbook.la
%{tde_tdelibdir}/libkdisspdflatexbook.so
%{tde_tdelibdir}/libkdissprosperslides.la
%{tde_tdelibdir}/libkdissprosperslides.so
%{tde_tdelibdir}/libkdissstx.la
%{tde_tdelibdir}/libkdissstx.so
%{tde_tdeappdir}/kdissert.desktop
%{tde_datadir}/apps/kdissert/
%{tde_datadir}/apps/kdissertpart/kdissertpart.rc
%{tde_datadir}/config.kcfg/kdissert.kcfg
%{tde_datadir}/doc/tde/HTML/en/kdissert/
%lang(fr) %{tde_datadir}/doc/tde/HTML/fr/kdissert/
%{tde_datadir}/icons/hicolor/128x128/actions/kdissert_sort.png
%{tde_datadir}/icons/hicolor/128x128/apps/kdissert.png
%{tde_datadir}/icons/hicolor/16x16/actions/kdissert_link.png
%{tde_datadir}/icons/hicolor/16x16/actions/kdissert_point.png
%{tde_datadir}/icons/hicolor/16x16/actions/kdissert_sort.png
%{tde_datadir}/icons/hicolor/16x16/apps/kdissert.png
%{tde_datadir}/icons/hicolor/22x22/actions/kdissert_link.png
%{tde_datadir}/icons/hicolor/22x22/actions/kdissert_point.png
%{tde_datadir}/icons/hicolor/22x22/actions/kdissert_sort.png
%{tde_datadir}/icons/hicolor/22x22/apps/kdissert.png
%{tde_datadir}/icons/hicolor/32x32/actions/kdissert_link.png
%{tde_datadir}/icons/hicolor/32x32/actions/kdissert_point.png
%{tde_datadir}/icons/hicolor/32x32/actions/kdissert_sort.png
%{tde_datadir}/icons/hicolor/32x32/apps/kdissert.png
%{tde_datadir}/icons/hicolor/64x64/actions/kdissert_sort.png
%{tde_datadir}/icons/hicolor/64x64/apps/kdissert.png
%{tde_datadir}/mimelnk/application/x-kdissert.desktop
%{tde_datadir}/services/kdissertpart.desktop


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.6c-1.opt.1
- 为 Magic 3.0 重建

* Sat Sep 20 2014 Francois Andriot <francois.andriot@free.fr> - 1.0.6c-1
- Initial release for TDE 14.0.0
