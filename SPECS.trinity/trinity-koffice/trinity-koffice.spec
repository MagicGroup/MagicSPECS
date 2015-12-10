#
# spec file for package koffice (version R14)
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
%define tde_pkg koffice
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

# Disable Kross support for RHEL <= 5 (python is too old)
%define with_kross 1

# Ruby support
%define with_ruby 1

# Ruby 1.9 includes are located in strance directories ... (taken from ruby 1.9 spec file)
%global	_normalized_cpu	%(echo %{_target_cpu} | sed 's/^ppc/powerpc/;s/i.86/i386/;s/sparcv./sparc/;s/armv.*/arm/')

# Required for Mageia 2: removes the ldflag '--no-undefined'
%define _disable_ld_no_undefined 1


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.6.3
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.2
Summary:	An integrated office suite
Summary(zh_CN.UTF-8): 集成办公套件
Group:		Applications/Productivity
Group(zh_CN.UTF-8): 应用程序/生产力
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Patch1:		%{name}-14.0.1-tqt.patch

# BuildRequires: world-devel ;)
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	trinity-tdegraphics-devel >= %{tde_version}
BuildRequires:	trinity-libpoppler-tqt-devel >= %{tde_version}

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes


BuildRequires:	fontconfig-devel
BuildRequires:	libart_lgpl-devel
BuildRequires:	libtiff-devel
BuildRequires:	libjpeg-devel
BuildRequires:	ImageMagick-devel
BuildRequires:	zlib-devel
BuildRequires:	openssl-devel
BuildRequires:	python-devel
BuildRequires:	pcre-devel
BuildRequires:	gettext-devel
BuildRequires:	mysql-devel
BuildRequires:	perl
BuildRequires:	doxygen
BuildRequires:	aspell-devel
BuildRequires:	libxslt-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	libexif-devel
BuildRequires:	readline-devel

BuildRequires:	bzip2-devel
BuildRequires:	lcms-devel

BuildRequires:	libpaper-devel

# RUBY support
%if 0%{?with_ruby}
BuildRequires:	ruby ruby-devel >= 1.8.1
BuildRequires:	rubypick
%endif

# FREETYPE support
BuildRequires:	freetype-devel

# LIBPNG support
BuildRequires:	libpng-devel

# GRAPHICSMAGICK support
%define with_graphicsmagick 1
BuildRequires:	GraphicsMagick-devel >= 1.1.0

# UTEMPTER support
BuildRequires:	libutempter-devel

# POPPLER support
BuildRequires: poppler-devel >= 0.12

# POSTGRESQL support
#  Requires 'libpqxx', for kexi-driver-pgqsl
%define with_postgresql 1
BuildRequires:	postgresql-devel
BuildRequires:	libpqxx-devel
Obsoletes:		trinity-libpqxx

# WPD support
#  For chalk and filters
BuildRequires:	libwpd-devel
Obsoletes:		trinity-libwpd

# WV2 support
BuildRequires:	wv2-devel

# MESA support
BuildRequires:	libGL-devel
BuildRequires:	libGLU-devel

# OPENJPEG
#BuildRequires:	%{_lib}openjpeg-devel

# LIBXI support
BuildRequires:	libXi-devel


%description
KOffice is an integrated office suite.

##########

%package suite
Summary:		An integrated office suite
Group:			Applications/Productivity
Obsoletes:      %{name} <= %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release} 
Requires:		%{name}-kword = %{?epoch:%{epoch}:}%{version}-%{release} 
Requires:		%{name}-kspread = %{?epoch:%{epoch}:}%{version}-%{release} 
Requires:		%{name}-kpresenter = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{name}-kivio = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{name}-karbon = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{name}-kugar = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{name}-kexi = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{name}-kexi-driver-mysql = %{?epoch:%{epoch}:}%{version}-%{release}
%{?with_postgresql:Requires:       %{name}-kexi-driver-pgsql = %{?epoch:%{epoch}:}%{version}-%{release}}
Requires:		%{name}-kchart = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{name}-kformula = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{name}-filters = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{name}-kplato = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{name}-chalk = %{?epoch:%{epoch}:}%{version}-%{release}

%description suite
KOffice is an integrated office suite.

%files suite
#empty => virtual package

##########

%package core
Summary:		Core support files for %{name} 
Group:			Applications/Productivity
Requires:		%{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		perl

%description core
%{summary}.

%posttrans core
gtk-update-icon-cache %{tde_datadir}/icons/crystalsvg &> /dev/null || :
gtk-update-icon-cache %{tde_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{tde_datadir}/icons/locolor &> /dev/null || :
update-desktop-database -q &> /dev/null ||:

%post core
touch --no-create %{tde_datadir}/icons/crystalsvg &> /dev/null || :
touch --no-create %{tde_datadir}/icons/hicolor &> /dev/null || :
touch --no-create %{tde_datadir}/icons/locolor &> /dev/null || :

%postun core
if [ $1 -eq 0 ]; then
  gtk-update-icon-cache %{tde_datadir}/icons/crystalsvg &> /dev/null || :
  gtk-update-icon-cache %{tde_datadir}/icons/hicolor &> /dev/null || :
  gtk-update-icon-cache %{tde_datadir}/icons/locolor &> /dev/null || :
  update-desktop-database -q &> /dev/null ||:
fi

%files core
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{tde_bindir}/koshell
%{tde_bindir}/kthesaurus
%{tde_bindir}/koconverter
%{tde_libdir}/libtdeinit_koshell.so
%{tde_libdir}/libtdeinit_kthesaurus.so
%{tde_tdelibdir}/tdefile_koffice.*
%{tde_tdelibdir}/tdefile_ooo.*
%{tde_tdelibdir}/tdefile_abiword.*
%{tde_tdelibdir}/tdefile_gnumeric.*
%{tde_tdelibdir}/kodocinfopropspage.*
%{tde_tdelibdir}/kofficescan.*
%{tde_tdelibdir}/kofficethumbnail.*
%{tde_tdelibdir}/koshell.*
%{tde_tdelibdir}/kthesaurus.*
%{tde_tdelibdir}/kwmailmerge_classic.*
%{tde_tdelibdir}/kwmailmerge_tdeabc.*
%{tde_tdelibdir}/kwmailmerge_qtsqldb_power.*
%{tde_tdelibdir}/kwmailmerge_qtsqldb.*
%{tde_tdelibdir}/libkounavailpart.*
%{tde_tdelibdir}/libkprkword.*
%{tde_tdelibdir}/libthesaurustool.*
%{tde_tdelibdir}/clipartthumbnail.*
%{tde_datadir}/apps/koffice/
%{tde_datadir}/apps/konqueror/servicemenus/*
%{tde_datadir}/apps/koshell/
%{tde_datadir}/apps/thesaurus/
%{tde_datadir}/config.kcfg/koshell.kcfg
%{tde_tdedocdir}/HTML/en/koffice/
%{tde_tdedocdir}/HTML/en/koshell/
%{tde_tdedocdir}/HTML/en/thesaurus/
%{tde_datadir}/icons/crystalsvg/*/*/*
%{tde_datadir}/icons/hicolor/*/*/*
%{tde_datadir}/icons/locolor/*/*/*
%{tde_datadir}/services/clipartthumbnail.desktop
%{tde_datadir}/services/tdefile_abiword.desktop
%{tde_datadir}/services/tdefile_gnumeric.desktop
%{tde_datadir}/services/tdefile_koffice.desktop
%{tde_datadir}/services/tdefile_ooo.desktop
%{tde_datadir}/services/kwmailmerge*.desktop
%{tde_datadir}/services/kodocinfopropspage.desktop
%{tde_datadir}/services/kofficethumbnail.desktop
%{tde_datadir}/services/kounavail.desktop
%{tde_datadir}/services/kprkword.desktop
%{tde_datadir}/services/thesaurustool.desktop
%{tde_datadir}/servicetypes/kochart.desktop
%{tde_datadir}/servicetypes/kofficepart.desktop
%{tde_datadir}/servicetypes/koplugin.desktop
%{tde_datadir}/servicetypes/kwmailmerge.desktop
%{tde_datadir}/servicetypes/widgetfactory.desktop
%{tde_tdeappdir}/*koffice.desktop
%{tde_tdeappdir}/KThesaurus.desktop
%{tde_tdeappdir}/*koshell.desktop
%{tde_datadir}/apps/kofficewidgets/
%if 0%{?with_kross}
%{tde_datadir}/apps/kross/
%{tde_tdelibdir}/krosspython.*
%if 0%{?with_ruby}
%{tde_tdelibdir}/krossruby.*
%endif
%endif

##########

%package libs
Summary:		Runtime libraries for %{name} 
Group:			System Environment/Libraries
Conflicts:      %{name} <= %{version}-%{release}
Requires:		trinity-tdelibs
License:		LGPLv2+

%description libs
%{summary}.

%files libs
%defattr(-,root,root,-)
%doc COPYING.LIB
#_libdir/libk*common.so.*
%{tde_libdir}/libkarboncommon.so.*
%{tde_libdir}/libkspreadcommon.so.*
%{tde_libdir}/libkdchart.so.*
%{tde_libdir}/libkochart.so.*
%{tde_libdir}/libkofficecore.so.*
%{tde_libdir}/libkofficeui.so.*
%{tde_libdir}/libkotext.so.*
%{tde_libdir}/libkowmf.so.*
%{tde_libdir}/libkopainter.so.*
%{tde_libdir}/libkstore.so.*
%{tde_libdir}/libkwmailmerge_interface.so.*
%{tde_libdir}/libkwmf.so.*
%{tde_libdir}/libkformulalib.so.*
%{tde_libdir}/libkopalette.so.*
%{tde_libdir}/libkoproperty.so.*
%if 0%{?with_kross}
%{tde_libdir}/libkrossapi.so.*
%{tde_libdir}/libkrossmain.so.*
%endif

%post libs
/sbin/ldconfig || :

%postun libs
/sbin/ldconfig || :

##########

%package devel
Summary:		Development files for %{name} 
Group:			Development/Libraries
Requires:		%{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}
License:		LGPLv2+

%description devel
%{summary}.

%files devel
%defattr(-,root,root,-)
%lang(en) %{tde_tdedocdir}/HTML/en/koffice-apidocs/
%{tde_includedir}/*
# FIXME: include only shlib symlinks we know/want to export
%{tde_libdir}/lib*.so
%exclude %{tde_libdir}/libtdeinit_*.so
%exclude %{tde_libdir}/libkudesignercore.so

##########

%package kword
Summary:		A frame-based word processor capable of professional standard documents
Group:			Applications/Productivity
Requires:		%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description kword
%{summary}.

%post kword
/sbin/ldconfig || :

%postun kword
/sbin/ldconfig || :

%posttrans kword
update-desktop-database -q &> /dev/null ||:

%files kword
%defattr(-,root,root,-)
%lang(en) %{tde_tdedocdir}/HTML/en/kword/
%{tde_bindir}/kword
%{tde_libdir}/libtdeinit_kword.so
%{tde_libdir}/libkwordprivate.so.*
%{tde_tdelibdir}/libkwordpart.*
%{tde_tdelibdir}/kword.*
%{tde_datadir}/apps/kword/
%{tde_datadir}/services/kword*.desktop
%{tde_datadir}/services/kwserial*.desktop
%{tde_datadir}/templates/TextDocument.desktop
%{tde_datadir}/templates/.source/TextDocument.kwt
%{tde_tdeappdir}/*kword.desktop

##########

%package kspread
Summary:		A powerful spreadsheet application
Group:			Applications/Productivity
Requires:		%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description kspread
%{summary}.

%files kspread
%defattr(-,root,root,-)
%lang(en) %{tde_tdedocdir}/HTML/en/kspread/
%{tde_bindir}/kspread
%{tde_libdir}/libtdeinit_kspread.so
%{tde_tdelibdir}/kspread.*
%{tde_tdelibdir}/libkspreadpart.*
%{tde_tdelibdir}/kwmailmerge_kspread.*
%{tde_tdelibdir}/libcsvexport.*
%{tde_tdelibdir}/libcsvimport.*
%{tde_tdelibdir}/libgnumericexport.*
%{tde_tdelibdir}/libgnumericimport.*
%{tde_tdelibdir}/libkspreadhtmlexport.*
%{tde_tdelibdir}/libkspreadinsertcalendar.*
%{tde_tdelibdir}/libopencalcexport.*
%{tde_tdelibdir}/libopencalcimport.*
%{tde_tdelibdir}/libqproimport.*
%{tde_datadir}/apps/kspread/
%{tde_datadir}/services/kspread*.desktop
%{tde_datadir}/templates/SpreadSheet.desktop
%{tde_datadir}/templates/.source/SpreadSheet.kst
%{tde_tdeappdir}/*kspread.desktop
%if 0%{?with_kross}
%{tde_tdelibdir}/kspreadscripting.*
%{tde_tdelibdir}/krosskspreadcore.*
%endif

##########

%package kpresenter
Summary:		A full-featured presentation program
Group:			Applications/Productivity
Requires:		%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description kpresenter
%{summary}.

%post kpresenter
/sbin/ldconfig || :

%postun kpresenter
/sbin/ldconfig || :

%posttrans kpresenter
update-desktop-database -q &> /dev/null ||:

%files kpresenter
%defattr(-,root,root,-)
%lang(en) %{tde_tdedocdir}/HTML/en/kpresenter/
%{tde_bindir}/kpresenter
%{tde_bindir}/kprconverter.pl
%{tde_libdir}/libtdeinit_kpresenter.so
%{tde_libdir}/libkpresenterimageexport.so.*
%{tde_libdir}/libkpresenterprivate.so.*
%{tde_tdelibdir}/*kpresenter*.*
%{tde_datadir}/apps/kpresenter/
%{tde_datadir}/services/kpresenter*.desktop
%{tde_datadir}/templates/Presentation.desktop
%{tde_datadir}/templates/.source/Presentation.kpt
%{tde_tdeappdir}/*kpresenter.desktop

##########

%package kivio
Summary:		A flowcharting application
Group:			Applications/Productivity
Requires:		%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      kivio < %{version}-%{release}

%description kivio
%{summary}.

%files kivio
%defattr(-,root,root,-)
%lang(en) %{tde_tdedocdir}/HTML/en/kivio/
%{tde_bindir}/kivio
%{tde_libdir}/libtdeinit_kivio.so
%{tde_libdir}/libkiviocommon.so.*
%{tde_tdelibdir}/*kivio*.*
%{tde_tdelibdir}/straight_connector.*
%{tde_datadir}/apps/kivio/
%{tde_datadir}/config.kcfg/kivio.kcfg
%{tde_datadir}/services/kivio*.desktop
%{tde_tdeappdir}/*kivio.desktop

##########

%package karbon
Summary:		A vector drawing application
Group:			Applications/Productivity
Requires:		%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description karbon
%{summary}.

%post karbon
/sbin/ldconfig || :

%postun karbon
/sbin/ldconfig || :

%files karbon
%defattr(-,root,root,-)
%lang(en) %{tde_tdedocdir}/HTML/en/karbon/
%{tde_bindir}/karbon
%{tde_libdir}/libtdeinit_karbon.so
%exclude %{tde_tdelibdir}/libkarbonepsimport.*
%{tde_tdelibdir}/*karbon*.*
%{tde_tdelibdir}/libwmfexport.*
%{tde_tdelibdir}/libwmfimport.*
%{tde_datadir}/apps/karbon/
%{tde_datadir}/services/karbon*
%{tde_datadir}/servicetypes/karbon_module.desktop
%{tde_datadir}/templates/Illustration.desktop
%{tde_datadir}/templates/.source/Illustration.karbon
%{tde_tdeappdir}/*karbon.desktop

##########

%package kugar
Summary:		A tool for generating business quality reports
Group:			Applications/Productivity
Requires:		%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description kugar
%{summary}.

%post kugar
/sbin/ldconfig || :

%postun kugar
/sbin/ldconfig || :

%posttrans kugar
update-desktop-database -q &> /dev/null ||:

%files kugar
%defattr(-,root,root,-)
%lang(en) %{tde_tdedocdir}/HTML/en/kugar/
%{tde_bindir}/kugar
%{tde_bindir}/kudesigner
%{tde_libdir}/libtdeinit_kugar.so
%{tde_libdir}/libtdeinit_kudesigner.so
%{tde_libdir}/libkugarlib.so.*
%{tde_libdir}/libkudesignercore.so
%{tde_tdelibdir}/kudesigner.*
%{tde_tdelibdir}/kugar.*
%{tde_tdelibdir}/libkudesignerpart.*
%{tde_tdelibdir}/libkugarpart.*
%{tde_datadir}/apps/kudesigner/
%{tde_datadir}/apps/kugar/
%{tde_datadir}/services/kugar*.desktop
%{tde_tdeappdir}/*kugar.desktop
%{tde_tdeappdir}/*kudesigner.desktop

##########

%package kexi
Summary:		An integrated environment for managing data
Group:			Applications/Productivity
Requires:		%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}

%if 0%{?with_postgresql} == 0
Obsoletes:		%{name}-kexi-driver-pgsql
%endif

%description kexi
%{summary}.
For additional database drivers take a look at %{name}-kexi-driver-*

%post kexi
/sbin/ldconfig || :

%postun kexi
/sbin/ldconfig || :

%posttrans kexi
update-desktop-database -q &> /dev/null ||:

%files kexi
%defattr(-,root,root,-)
%lang(en) %{tde_tdedocdir}/HTML/en/kexi/
%{tde_bindir}/kexi*
%{tde_bindir}/ksqlite*
%{tde_libdir}/libtdeinit_kexi.so
%{tde_libdir}/libkexi*.so.*
%{tde_libdir}/libkformdesigner.so.*
%{tde_tdelibdir}/kformdesigner_*.*
%{tde_tdelibdir}/kexidb_sqlite2driver.*
%{tde_tdelibdir}/kexidb_sqlite3driver.*
%{tde_tdelibdir}/kexihandler_*.*
%{tde_tdelibdir}/kexi.*
# moved here to workaround bug #394101, alternative is to move libkexi(db|dbparser|utils) to -libs)
%{tde_tdelibdir}/libkspreadkexiimport.*
%{tde_confdir}/kexirc
%{tde_confdir}/magic/kexi.magic
%{tde_datadir}/mimelnk/application/*
%{tde_datadir}/servicetypes/kexi*.desktop
%{tde_datadir}/services/kexi/
%{tde_datadir}/apps/kexi/
%{tde_datadir}/services/kformdesigner/
%{tde_tdeappdir}/*kexi.desktop
%{tde_datadir}/services/kexidb_sqlite*driver.desktop
%if 0%{?with_kross}
%{tde_bindir}/krossrunner
%{tde_tdelibdir}/krosskexiapp.*
%{tde_tdelibdir}/krosskexidb.*
%endif

##########

%package kexi-driver-mysql
Summary:		Mysql-driver for kexi
Group:			Applications/Productivity
Requires:		%{name}-kexi = %{?epoch:%{epoch}:}%{version}-%{release}

%description kexi-driver-mysql
%{summary}.

%files kexi-driver-mysql
%defattr(-,root,root,-)
%{tde_tdelibdir}/kexidb_mysqldriver.*
%{tde_tdelibdir}/keximigrate_mysql.*
%{tde_datadir}/services/keximigrate_mysql.desktop
%{tde_datadir}/services/kexidb_mysqldriver.desktop

##########

%if 0%{?with_postgresql}

%package kexi-driver-pgsql
Summary:		Postgresql driver for kexi
Group:			Applications/Productivity
Requires:		%{name}-kexi = %{?epoch:%{epoch}:}%{version}-%{release}

%description kexi-driver-pgsql
%{summary}.

%files kexi-driver-pgsql
%defattr(-,root,root,-)
%{tde_tdelibdir}/kexidb_pqxxsqldriver.*
%{tde_tdelibdir}/keximigrate_pqxx.*
%{tde_datadir}/services/kexidb_pqxxsqldriver.desktop
%{tde_datadir}/services/keximigrate_pqxx.desktop

%endif

##########

%package kchart
Summary:		An integrated graph and chart drawing tool
Group:			Applications/Productivity
Requires:		%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description kchart
%{summary}.

%post kchart
/sbin/ldconfig || :

%postun kchart
/sbin/ldconfig || :

%posttrans kchart
update-desktop-database -q &> /dev/null ||:

%files kchart
%defattr(-,root,root,-)
%lang(en) %{tde_tdedocdir}/HTML/en/kchart/
%{tde_bindir}/kchart
%{tde_libdir}/libkchart*.so.*
%{tde_libdir}/libtdeinit_kchart.so
%{tde_tdelibdir}/*kchart*.*
%{tde_datadir}/apps/kchart/
%{tde_datadir}/services/kchart*.desktop
%{tde_tdeappdir}/*kchart.desktop

##########

%package kformula
Summary:		A powerful formula editor
Group:			Applications/Productivity
Requires:		%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}

%if 0%{?mgaversion} || 0%{?mdkversion}
Requires:		fonts-ttf-dejavu
%else
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
Requires:		dejavu-lgc-sans-fonts
Requires:		lyx-cmex10-fonts
%endif
%if 0%{?rhel} == 5
Requires:		dejavu-lgc-fonts 
Requires:		lyx-cmex10-fonts
%endif
%if 0%{?suse_version} >= 1220
Requires:		dejavu-fonts 
%endif
%if 0%{?suse_version} == 1140
Requires:		dejavu
%endif
%endif

%description kformula
%{summary}.

%files kformula
%defattr(-,root,root,-)
%lang(en) %{tde_tdedocdir}/HTML/en/kformula/
%{tde_bindir}/kformula
%{tde_libdir}/libtdeinit_kformula.so
%{tde_tdelibdir}/*kformula*.*
%{tde_datadir}/apps/kformula/
%{tde_datadir}/services/kformula*.desktop
%{tde_tdeappdir}/*kformula.desktop

##########

%package filters
Summary:		Import and Export Filters for KOffice
Group:			Applications/Productivity
Requires:		%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description filters
%{summary}.

%post filters
/sbin/ldconfig || :

%postun filters
/sbin/ldconfig || :

%files filters
%defattr(-,root,root,-)
%{tde_libdir}/libkwordexportfilters.so.*
%{tde_tdelibdir}/libabiwordexport.*
%{tde_tdelibdir}/libabiwordimport.*
%{tde_tdelibdir}/libamiproexport.*
%{tde_tdelibdir}/libamiproimport.*
%{tde_tdelibdir}/libapplixspreadimport.*
%{tde_tdelibdir}/libapplixwordimport.*
%{tde_tdelibdir}/libasciiexport.*
%{tde_tdelibdir}/libasciiimport.*
%{tde_tdelibdir}/libdbaseimport.*
%{tde_tdelibdir}/libdocbookexport.*
%{tde_tdelibdir}/libexcelimport.*
%{tde_tdelibdir}/libgenerickofilter.*
%{tde_tdelibdir}/libhtmlexport.*
%{tde_tdelibdir}/libhtmlimport.*
%{tde_tdelibdir}/libkarbonepsimport.*
%{tde_tdelibdir}/libkfolatexexport.*
%{tde_tdelibdir}/libkfomathmlexport.*
%{tde_tdelibdir}/libkfomathmlimport.*
%{tde_tdelibdir}/libkfopngexport.*
%{tde_tdelibdir}/libkspreadlatexexport.*
%{tde_tdelibdir}/libkugarnopimport.*
%{tde_tdelibdir}/libkwordkword1dot3import.*
%{tde_tdelibdir}/libkwordlatexexport.*
%{tde_tdelibdir}/libmswriteexport.*
%{tde_tdelibdir}/libmswriteimport.*
%{tde_tdelibdir}/libooimpressexport.*
%{tde_tdelibdir}/libooimpressimport.*
%{tde_tdelibdir}/liboowriterexport.*
%{tde_tdelibdir}/liboowriterimport.*
%{tde_tdelibdir}/libpalmdocexport.*
%{tde_tdelibdir}/libpalmdocimport.*
%{tde_tdelibdir}/libpdfimport.*
%{tde_tdelibdir}/librtfexport.*
%{tde_tdelibdir}/librtfimport.*
%{tde_tdelibdir}/libwmlexport.*
%{tde_tdelibdir}/libwmlimport.*
%{tde_tdelibdir}/libwpexport.*
%{tde_tdelibdir}/libwpimport.*
%{tde_tdelibdir}/libmswordimport.*
%{tde_tdelibdir}/libxsltimport.*
%{tde_tdelibdir}/libxsltexport.*
%{tde_tdelibdir}/libhancomwordimport.*
%{tde_tdelibdir}/libkfosvgexport.*
%{tde_tdelibdir}/liboodrawimport.*
%{tde_tdelibdir}/libolefilter.*
%{tde_datadir}/apps/xsltfilter/
%{tde_datadir}/services/generic_filter.desktop
%{tde_datadir}/services/ole_powerpoint97_import.desktop
%{tde_datadir}/services/xslt*.desktop
%{tde_datadir}/servicetypes/kofilter*.desktop

##########

%package kplato
Summary:		An integrated project management and planning tool
Group:			Applications/Productivity
Requires:		%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description kplato
%{summary}.

%files kplato
%defattr(-,root,root,-)
%lang(en) %{tde_tdedocdir}/HTML/en/kplato/
%{tde_bindir}/kplato
%{tde_libdir}/libtdeinit_kplato.so
%{tde_tdelibdir}/kplato.*
%{tde_tdelibdir}/libkplatopart.*
%{tde_datadir}/apps/kplato/
%{tde_datadir}/services/kplatopart.desktop
%{tde_tdeappdir}/*kplato.desktop

##########

%package chalk
Summary:		pixel-based image manipulation program for the TDE Office Suite [Trinity]
Group:			Applications/Productivity
Requires:		%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{name}-chalk-data = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{name}-filters = %{?epoch:%{epoch}:}%{version}-%{release}

%description chalk
Chalk is a painting and image editing application for KOffice. Chalk contains
both ease-of-use and fun features like guided painting.

This package is part of the TDE Office Suite.

%post chalk
/sbin/ldconfig || :

%postun chalk
/sbin/ldconfig || :

%posttrans chalk
update-desktop-database -q &> /dev/null ||:

%files chalk
%defattr(-,root,root,-)
%{tde_bindir}/chalk
%{tde_tdelibdir}/chalkblurfilter.la
%{tde_tdelibdir}/chalkblurfilter.so
%{tde_tdelibdir}/chalkbumpmap.la
%{tde_tdelibdir}/chalkbumpmap.so
%{tde_tdelibdir}/chalkcimg.la
%{tde_tdelibdir}/chalkcimg.so
%{tde_tdelibdir}/chalk_cmyk_*
%{tde_tdelibdir}/chalkcmykplugin.la
%{tde_tdelibdir}/chalkcmykplugin.so
%{tde_tdelibdir}/chalkcolorify.la
%{tde_tdelibdir}/chalkcolorify.so
%{tde_tdelibdir}/chalkcolorrange.la
%{tde_tdelibdir}/chalkcolorrange.so
%{tde_tdelibdir}/chalkcolorsfilters.la
%{tde_tdelibdir}/chalkcolorsfilters.so
%{tde_tdelibdir}/chalkcolorspaceconversion.la
%{tde_tdelibdir}/chalkcolorspaceconversion.so
%{tde_tdelibdir}/chalkconvolutionfilters.la
%{tde_tdelibdir}/chalkconvolutionfilters.so
%{tde_tdelibdir}/chalkdefaultpaintops.la
%{tde_tdelibdir}/chalkdefaultpaintops.so
%{tde_tdelibdir}/chalkdefaulttools.la
%{tde_tdelibdir}/chalkdefaulttools.so
%{tde_tdelibdir}/chalkdropshadow.la
%{tde_tdelibdir}/chalkdropshadow.so
%{tde_tdelibdir}/chalkembossfilter.la
%{tde_tdelibdir}/chalkembossfilter.so
%{tde_tdelibdir}/chalkexample.la
%{tde_tdelibdir}/chalkexample.so
%{tde_tdelibdir}/chalkextensioncolorsfilters.la
%{tde_tdelibdir}/chalkextensioncolorsfilters.so
%{tde_tdelibdir}/chalkfastcolortransfer.la
%{tde_tdelibdir}/chalkfastcolortransfer.so
%{tde_tdelibdir}/chalkfiltersgallery.la
%{tde_tdelibdir}/chalkfiltersgallery.so
%{tde_tdelibdir}/chalk_gray_*
%{tde_tdelibdir}/chalkgrayplugin.la
%{tde_tdelibdir}/chalkgrayplugin.so
%{tde_tdelibdir}/chalkhistogramdocker.la
%{tde_tdelibdir}/chalkhistogramdocker.so
%{tde_tdelibdir}/chalkhistogram.la
%{tde_tdelibdir}/chalkhistogram.so
%{tde_tdelibdir}/chalkimageenhancement.la
%{tde_tdelibdir}/chalkimageenhancement.so
%{tde_tdelibdir}/chalkimagesize.la
%{tde_tdelibdir}/chalkimagesize.so
%{tde_tdelibdir}/chalk.la
%{tde_tdelibdir}/chalklenscorrectionfilter.la
%{tde_tdelibdir}/chalklenscorrectionfilter.so
%{tde_tdelibdir}/chalklevelfilter.la
%{tde_tdelibdir}/chalklevelfilter.so
%{tde_tdelibdir}/chalk_lms_*
%{tde_tdelibdir}/chalkmodifyselection.la
%{tde_tdelibdir}/chalkmodifyselection.so
%{tde_tdelibdir}/chalknoisefilter.la
%{tde_tdelibdir}/chalknoisefilter.so
%{tde_tdelibdir}/chalkoilpaintfilter.la
%{tde_tdelibdir}/chalkoilpaintfilter.so
%{tde_tdelibdir}/chalkpixelizefilter.la
%{tde_tdelibdir}/chalkpixelizefilter.so
%{tde_tdelibdir}/chalkraindropsfilter.la
%{tde_tdelibdir}/chalkraindropsfilter.so
%{tde_tdelibdir}/chalkrandompickfilter.la
%{tde_tdelibdir}/chalkrandompickfilter.so
%{tde_tdelibdir}/chalk_rgb_*
%{tde_tdelibdir}/chalkrgbplugin.la
%{tde_tdelibdir}/chalkrgbplugin.so
%{tde_tdelibdir}/chalkrotateimage.la
%{tde_tdelibdir}/chalkrotateimage.so
%{tde_tdelibdir}/chalkroundcornersfilter.la
%{tde_tdelibdir}/chalkroundcornersfilter.so
%{tde_tdelibdir}/chalkselectiontools.la
%{tde_tdelibdir}/chalkselectiontools.so
%{tde_tdelibdir}/chalkselectopaque.la
%{tde_tdelibdir}/chalkselectopaque.so
%{tde_tdelibdir}/chalkseparatechannels.la
%{tde_tdelibdir}/chalkseparatechannels.so
%{tde_tdelibdir}/chalkshearimage.la
%{tde_tdelibdir}/chalkshearimage.so
%{tde_tdelibdir}/chalksmalltilesfilter.la
%{tde_tdelibdir}/chalksmalltilesfilter.so
%{tde_tdelibdir}/chalk.so
%{tde_tdelibdir}/chalkscreenshot.la
%{tde_tdelibdir}/chalkscreenshot.so
%{tde_tdelibdir}/chalksobelfilter.la
%{tde_tdelibdir}/chalksobelfilter.so
%{tde_tdelibdir}/chalksubstrate.la
%{tde_tdelibdir}/chalksubstrate.so
%{tde_tdelibdir}/chalktoolcrop.la
%{tde_tdelibdir}/chalktoolcrop.so
%{tde_tdelibdir}/chalktoolcurves.la
%{tde_tdelibdir}/chalktoolcurves.so
%{tde_tdelibdir}/chalktoolfilter.la
%{tde_tdelibdir}/chalktoolfilter.so
%{tde_tdelibdir}/chalktoolperspectivegrid.la
%{tde_tdelibdir}/chalktoolperspectivegrid.so
%{tde_tdelibdir}/chalktoolperspectivetransform.la
%{tde_tdelibdir}/chalktoolperspectivetransform.so
%{tde_tdelibdir}/chalktoolpolygon.la
%{tde_tdelibdir}/chalktoolpolygon.so
%{tde_tdelibdir}/chalktoolpolyline.la
%{tde_tdelibdir}/chalktoolpolyline.so
%{tde_tdelibdir}/chalktoolselectsimilar.la
%{tde_tdelibdir}/chalktoolselectsimilar.so
%{tde_tdelibdir}/chalktoolstar.la
%{tde_tdelibdir}/chalktoolstar.so
%{tde_tdelibdir}/chalktooltransform.la
%{tde_tdelibdir}/chalktooltransform.so
%{tde_tdelibdir}/chalkunsharpfilter.la
%{tde_tdelibdir}/chalkunsharpfilter.so
%{tde_tdelibdir}/chalkwavefilter.la
%{tde_tdelibdir}/chalkwavefilter.so
%{tde_tdelibdir}/chalkwetplugin.la
%{tde_tdelibdir}/chalkwetplugin.so
%{tde_tdelibdir}/chalk_ycbcr_*
%if 0%{?with_graphicsmagick}
%{tde_tdelibdir}/libchalkgmagickexport.la
%{tde_tdelibdir}/libchalkgmagickexport.so
%{tde_tdelibdir}/libchalkgmagickimport.la
%{tde_tdelibdir}/libchalkgmagickimport.so
%{tde_tdelibdir}/libchalkjpegexport.la
%{tde_tdelibdir}/libchalkjpegexport.so
%{tde_tdelibdir}/libchalkjpegimport.la
%{tde_tdelibdir}/libchalkjpegimport.so
%endif
%{tde_tdelibdir}/libchalk_openexr_export.la
%{tde_tdelibdir}/libchalk_openexr_export.so
%{tde_tdelibdir}/libchalk_openexr_import.la
%{tde_tdelibdir}/libchalk_openexr_import.so
%{tde_tdelibdir}/libchalkpart.la
%{tde_tdelibdir}/libchalkpart.so
%{tde_tdelibdir}/libchalkpdfimport.la
%{tde_tdelibdir}/libchalkpdfimport.so
%{tde_tdelibdir}/libchalkpngexport.la
%{tde_tdelibdir}/libchalkpngexport.so
%{tde_tdelibdir}/libchalkpngimport.la
%{tde_tdelibdir}/libchalkpngimport.so
%{tde_tdelibdir}/libchalk_raw_import.la
%{tde_tdelibdir}/libchalk_raw_import.so
%if 0%{?with_graphicsmagick}
%{tde_tdelibdir}/libchalktiffexport.la
%{tde_tdelibdir}/libchalktiffexport.so
%{tde_tdelibdir}/libchalktiffimport.la
%{tde_tdelibdir}/libchalktiffimport.so
%endif
%{tde_libdir}/libtdeinit_chalk.so
%{tde_libdir}/libchalk_cmyk_*.so.*
%{tde_libdir}/libchalkcolor.so.*
%{tde_libdir}/libchalkcommon.so.*
%{tde_libdir}/libchalkgrayscale.so.*
%{tde_libdir}/libchalk_gray_*.so.*
%{tde_libdir}/libchalkimage.so.*
%{tde_libdir}/libchalk_lms_*.so.*
%{tde_libdir}/libchalk_rgb_*.so.*
%{tde_libdir}/libchalkrgb.so.*
%{tde_libdir}/libchalkui.so.*
%{tde_libdir}/libchalk_ycbcr_*.so.*
%if 0%{?with_kross}
%{tde_tdelibdir}/krosschalkcore.la
%{tde_tdelibdir}/krosschalkcore.so
%{tde_tdelibdir}/chalkscripting.la
%{tde_tdelibdir}/chalkscripting.so
%{tde_libdir}/libchalkscripting.so.*
%endif

##########

%package chalk-data
Summary:		data files for Chalk painting program [Trinity]
Group:			Applications/Productivity

%description chalk-data
This package contains architecture-independent data files for Chalk,
the painting program shipped with the TDE Office Suite.

See the chalk package for further information.

This package is part of the TDE Office Suite.

%files chalk-data
%defattr(-,root,root,-)
%{tde_tdeappdir}/chalk.desktop
%{tde_datadir}/applnk/.hidden/chalk_*.desktop
%{tde_datadir}/apps/chalk/
%{tde_datadir}/apps/chalkplugins/
%lang(en) %{tde_tdedocdir}/HTML/en/chalk/
%{tde_datadir}/services/chalk*.desktop
%{tde_datadir}/servicetypes/chalk*.desktop

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
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig:${PKG_CONFIG_PATH}"
export kde_confdir="%{tde_confdir}"

%if 0%{?suse_version} == 1220
RD=$(ruby -r rbconfig -e 'printf("%s",Config::CONFIG["rubyhdrdir"])')
export CXXFLAGS="${CXXFLAGS} -I${RD}/%_normalized_cpu-linux"
%endif

# FTBFS on RHEL 5
%if 0%{?rhel} == 5
%__sed -i "kexi/migration/keximigratetest.cpp" \
       -e "/TDEApplication/ s|\");|\", true, true, true);|"
%endif

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility \
  \
  --with-extra-libs=%{tde_libdir} \
  --with-extra-includes=%{tde_includedir}/arts \
  \
  --disable-kexi-macros \
  %{?with_kross:--enable-scripting} %{!?with_kross:--disable-scripting} \
  %{?with_postgresql:--enable-pgsql} %{!?with_postgresql:--disable-pgsql} \

%__make %{?_smp_mflags} || %__make


%install
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

#%__mkdir_p "%{buildroot}%{tde_datadir}/icons/hicolor/{16x16,22x22,32x32,48x48,64x64,128x128}/apps/"
#for i in {16x16,22x22,32x32,48x48,64x64,128x128}; do
#  mv "%{buildroot}%{tde_datadir}/icons/crystalsvg/$i/apps/kplato.png %{buildroot}/opt/kde3/share/icons/hicolor/$i/apps/;
#done

# Fix desktop icon location
%__mv -f "%{?buildroot}%{tde_datadir}/applnk/"*"/KThesaurus.desktop" "%{?buildroot}%{tde_tdeappdir}"

# Apps that should stay in TDE
for i in kivio kplato; do
  echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_tdeappdir}/${i}.desktop"
done

# Links duplicate files
%fdupes %{buildroot}

## unpackaged files
# fonts
rm -rfv %{buildroot}%{tde_datadir}/apps/kformula/fonts/
# libtool archives
rm -f %{buildroot}%{tde_libdir}/lib*.la
# shouldn't these be in koffice-l10n? 
rm -f %{buildroot}%{tde_datadir}/locale/pl/LC_MESSAGES/kexi_{add,delete}_column_gui_transl_pl.sh
# -devel symlinks to nuke
rm -f %{buildroot}%{tde_libdir}/lib*common.so
rm -f %{buildroot}%{tde_libdir}/lib*filters.so
rm -f %{buildroot}%{tde_libdir}/lib*private.so
rm -f %{buildroot}%{tde_libdir}/libkarbon*.so
rm -f %{buildroot}%{tde_libdir}/libkchart*.so
rm -f %{buildroot}%{tde_libdir}/libkexi*.so
rm -f %{buildroot}%{tde_libdir}/libkisexiv2.so
rm -f %{buildroot}%{tde_libdir}/libkformdesigner.so
rm -f %{buildroot}%{tde_libdir}/libkplato*.so
rm -f %{buildroot}%{tde_libdir}/libkpresenter*.so
rm -f %{buildroot}%{tde_libdir}/libkword*.so
rm -f %{buildroot}%{tde_libdir}/libkross*.so
rm -f %{buildroot}%{tde_libdir}/libkugar*.so

magic_rpm_clean.sh

%clean
%__rm -rf %{buildroot}


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 2:1.6.3-1.2
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:1.6.3-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.6.3-1
- Initial release for TDE 14.0.0
