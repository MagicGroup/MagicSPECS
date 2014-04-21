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


Name:			trinity-tdesdk
Summary:		The KDE Software Development Kit (SDK)
Version:		3.5.13.2
Release:		1%{?dist}%{?_variant}

License:		GPLv2
Group:			User Interface/Desktops
URL:			http://www.trinitydesktop.org/
Vendor:			Trinity Project
Packager:		Francois Andriot <francois.andriot@free.fr>

Prefix:			%{tde_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source: 		kdesdk-trinity-%{version}.tar.xz

# [tdesdk] fixes for RHEL/Fedora/MGA2 after previous patch
Patch4:		kdesdk-3.5.13-misc_ftbfs.patch
# [tdesdk] Fix FTBFS on newer subversion libraries [Bug #872] [Commit #572169a2]
Patch5:		kdesdk-3.5.13-fix_ftbfs_on_newer_svn.patch
# [tdesdk] Fix unknown macro 'tde_save_and_set'
Patch6:		kdesdk-3.5.13.1-fix_cmake_macros.patch
# [tdesdk] Fix build of kcachegrind
Patch7:		kdesdk-3.5.13.1-add_missing_files.patch
# [tdesdk] Use 'flex' instead of 'lex'
Patch8:		kdesdk-3.5.13.1-use_flex_instead_of_lex.patch

BuildRequires: cmake >= 2.8
BuildRequires: libtool
BuildRequires: pcre-devel
BuildRequires: trinity-tqtinterface-devel >= %{version}
BuildRequires: trinity-tdelibs-devel >= %{version}
# for kbugbuster/libkcal
BuildRequires: trinity-tdepim-devel >= %{version}
%if 0%{?mgaversion} || 0%{?mdkversion}
#BuildRequires:	%{_lib}db4.8-devel
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires: libdb-devel
%endif
%if 0%{?suse_version}
BuildRequires:	libdb-4_8-devel
%endif
BuildRequires: desktop-file-utils
# kbabel,  F-7+: flex >= 2.5.33-9
BuildRequires: flex
# umbrello
BuildRequires:	libxslt-devel
BuildRequires:	libxml2-devel
BuildRequires:	perl
BuildRequires:	subversion-devel neon-devel

%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}ltdl-devel
BuildRequires:	%{_lib}binutils-devel
%else
BuildRequires:	libtool-ltdl-devel
%if 0%{?fedora} >= 6 || 0%{?rhel} >= 5 || 0%{?suse_version}
BuildRequires: binutils-devel
%endif
%endif

Obsoletes:		trinity-kdesdk < %{version}-%{release}
Provides:		trinity-kdesdk = %{version}-%{release}
Obsoletes:		trinity-kdesdk-libs < %{version}-%{release}
Provides:		trinity-kdesdk-libs = %{version}-%{release}

Requires: trinity-cervisia = %{version}-%{release}
Requires: trinity-kapptemplate = %{version}-%{release}
Requires: trinity-kbabel = %{version}-%{release}
Requires: trinity-kbugbuster = %{version}-%{release}
Requires: trinity-tdecachegrind = %{version}-%{release}
Requires: trinity-tdecachegrind-converters = %{version}-%{release}
Requires: %{name}-kfile-plugins = %{version}-%{release}
Requires: %{name}-misc = %{version}-%{release}
Requires: %{name}-scripts = %{version}-%{release}
Requires: trinity-kmtrace = %{version}-%{release}
Requires: trinity-kompare = %{version}-%{release}
Requires: trinity-kspy = %{version}-%{release}
Requires: trinity-kuiviewer = %{version}-%{release}
Requires: trinity-libcvsservice0 = %{version}-%{release}
Requires: trinity-libcvsservice-devel = %{version}-%{release}
Requires: trinity-poxml = %{version}-%{release}
Requires: trinity-umbrello = %{version}-%{release}
Requires: %{name}-kio-plugins = %{version}-%{release}
Requires: trinity-kunittest = %{version}-%{release}


%description
A collection of applications and tools used by developers, including:
* cervisia: a CVS frontend
* kbabel: PO file management
* kbugbuster: a tool to manage the TDE bug report system
* kcachegrind: a browser for data produced by profiling tools (e.g. cachegrind)
* kompare: diff tool
* kuiviewer: displays designer's UI files
* umbrello: UML modeller and UML diagram tool

%files

##########

%package -n trinity-cervisia
Summary:	A graphical CVS front end for Trinity
Group:		Development/Utilities

%description -n trinity-cervisia
Cervisia is a TDE-based graphical front end for the CVS client.

As well as providing both common and advanced CVS operations, it offers
a variety of methods for graphically viewing information about the CVS
repository, your own sandbox and the relationships between different
versions of files.  A Changelog editor is also included and is coupled
with the commit dialog.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-cervisia
%{tde_bindir}/cervisia
%{tde_libdir}/lib[kt]deinit_cervisia.la
%{tde_libdir}/lib[kt]deinit_cervisia.so
%{tde_tdelibdir}/cervisia.la
%{tde_tdelibdir}/cervisia.so
%{tde_tdelibdir}/libcervisiapart.la
%{tde_tdelibdir}/libcervisiapart.so
%{tde_tdeappdir}/cervisia.desktop
%{tde_datadir}/apps/cervisia/
%{tde_datadir}/apps/cervisiapart/cervisiaui.rc
%{tde_datadir}/apps/kconf_update/cervisia.upd
%{tde_datadir}/apps/kconf_update/cervisia-change_repos_list.pl
%{tde_datadir}/apps/kconf_update/cervisia-normalize_cvsroot.pl
%{tde_datadir}/apps/kconf_update/move_repositories.pl
%{tde_datadir}/apps/kconf_update/change_colors.pl
%{tde_datadir}/config.kcfg/cervisiapart.kcfg
%{tde_datadir}/icons/hicolor/*/apps/cervisia.png
%{tde_datadir}/icons/crystalsvg/*/actions/vcs_*.png
%{tde_datadir}/icons/crystalsvg/scalable/actions/vcs_*.svgz
%{tde_mandir}/man1/man1/cervisia.1*
%{tde_tdedocdir}/HTML/en/cervisia/

%post -n trinity-cervisia
/sbin/ldconfig || :
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-cervisia
/sbin/ldconfig || :
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kapptemplate
Summary:	Creates a framework to develop a Trinity application
Group:		Development/Utilities

%description -n trinity-kapptemplate
KAppTemplate is a shell script that will create the necessary
framework to develop various TDE applications.  It takes care of the
autoconf/automake code as well as providing a skeleton and example of
what the code typically looks like.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-kapptemplate
%{tde_bindir}/kapptemplate
%{tde_datadir}/apps/kapptemplate/

##########

%package -n trinity-kbabel
Summary:	PO-file editing suite for Trinity
Group:		Development/Utilities

%description -n trinity-kbabel
This is a suite of programs for editing gettext message files (PO-files).
It is designed to help you translate fast and consistently.

This suite includes KBabel, CatalogManager and KBabelDict.  KBabel is an
advanced and easy to use PO-file editor with full navigational and editing
capabilities, syntax checking and statistics.  CatalogManager is a multi
functional catalog manager which allows you to keep track of many
PO-files at once.  KBabelDict is a dictionary to assist with searching
for common translations.

This package is part of Trinity, and a component of the TDE SDK module.
See the 'kde-trinity' and 'tdesdk-trinity' packages for more information.

%files -n trinity-kbabel
%{tde_bindir}/catalogmanager
%{tde_bindir}/kbabel
%{tde_bindir}/kbabeldict
%{tde_libdir}/libkbabelcommon.so.*
%{tde_libdir}/libkbabeldictplugin.so.*
%{tde_tdelibdir}/kfile_po.la
%{tde_tdelibdir}/kfile_po.so
%{tde_tdelibdir}/pothumbnail.la
%{tde_tdelibdir}/pothumbnail.so
%{tde_tdelibdir}/kbabel_accelstool.la
%{tde_tdelibdir}/kbabel_accelstool.so
%{tde_tdelibdir}/kbabel_argstool.la
%{tde_tdelibdir}/kbabel_argstool.so
%{tde_tdelibdir}/kbabel_contexttool.la
%{tde_tdelibdir}/kbabel_contexttool.so
%{tde_tdelibdir}/kbabel_equationstool.la
%{tde_tdelibdir}/kbabel_equationstool.so
%{tde_tdelibdir}/kbabel_gettextexport.la
%{tde_tdelibdir}/kbabel_gettextexport.so
%{tde_tdelibdir}/kbabel_gettextimport.la
%{tde_tdelibdir}/kbabel_gettextimport.so
%{tde_tdelibdir}/kbabel_lengthtool.la
%{tde_tdelibdir}/kbabel_lengthtool.so
%{tde_tdelibdir}/kbabel_linguistexport.la
%{tde_tdelibdir}/kbabel_linguistexport.so
%{tde_tdelibdir}/kbabel_linguistimport.la
%{tde_tdelibdir}/kbabel_linguistimport.so
%{tde_tdelibdir}/kbabel_nottranslatedtool.la
%{tde_tdelibdir}/kbabel_nottranslatedtool.so
%{tde_tdelibdir}/kbabel_pluraltool.la
%{tde_tdelibdir}/kbabel_pluraltool.so
%{tde_tdelibdir}/kbabel_punctuationtool.la
%{tde_tdelibdir}/kbabel_punctuationtool.so
%{tde_tdelibdir}/kbabel_regexptool.la
%{tde_tdelibdir}/kbabel_regexptool.so
%{tde_tdelibdir}/kbabel_setfuzzytool.la
%{tde_tdelibdir}/kbabel_setfuzzytool.so
%{tde_tdelibdir}/kbabel_whitespacetool.la
%{tde_tdelibdir}/kbabel_whitespacetool.so
%{tde_tdelibdir}/kbabel_xliffexport.la
%{tde_tdelibdir}/kbabel_xliffexport.so
%{tde_tdelibdir}/kbabel_xliffimport.la
%{tde_tdelibdir}/kbabel_xliffimport.so
%{tde_tdelibdir}/kbabel_xmltool.la
%{tde_tdelibdir}/kbabel_xmltool.so
%{tde_tdelibdir}/kbabeldict_dbsearchengine.la
%{tde_tdelibdir}/kbabeldict_dbsearchengine.so
%{tde_tdelibdir}/kbabeldict_poauxiliary.la
%{tde_tdelibdir}/kbabeldict_poauxiliary.so
%{tde_tdelibdir}/kbabeldict_pocompendium.la
%{tde_tdelibdir}/kbabeldict_pocompendium.so
%{tde_tdelibdir}/kbabeldict_tmxcompendium.la
%{tde_tdelibdir}/kbabeldict_tmxcompendium.so
%{tde_tdeappdir}/catalogmanager.desktop
%{tde_tdeappdir}/kbabel.desktop
%{tde_tdeappdir}/kbabeldict.desktop
%{tde_datadir}/apps/catalogmanager/catalogmanagerui.rc
%{tde_datadir}/apps/kbabel/
%{tde_datadir}/apps/kconf_update/kbabel-difftoproject.upd
%{tde_datadir}/apps/kconf_update/kbabel-project.upd
%{tde_datadir}/apps/kconf_update/kbabel-projectrename.upd
%{tde_datadir}/config.kcfg/kbabel.kcfg
%{tde_datadir}/config.kcfg/kbprojectsettings.kcfg
%{tde_tdedocdir}/HTML/en/kbabel/
%{tde_datadir}/icons/hicolor/*/apps/catalogmanager.png
%{tde_datadir}/icons/hicolor/*/apps/kbabel.png
%{tde_datadir}/icons/hicolor/*/apps/kbabeldict.png
%{tde_datadir}/icons/locolor/*/apps/catalogmanager.png
%{tde_datadir}/icons/locolor/*/apps/kbabel.png
%{tde_datadir}/icons/locolor/*/apps/kbabeldict.png
%{tde_datadir}/services/dbsearchengine.desktop
%{tde_datadir}/services/kfile_po.desktop
%{tde_datadir}/services/pothumbnail.desktop
%{tde_datadir}/services/kbabel_accelstool.desktop
%{tde_datadir}/services/kbabel_argstool.desktop
%{tde_datadir}/services/kbabel_contexttool.desktop
%{tde_datadir}/services/kbabel_equationstool.desktop
%{tde_datadir}/services/kbabel_gettext_export.desktop
%{tde_datadir}/services/kbabel_gettext_import.desktop
%{tde_datadir}/services/kbabel_lengthtool.desktop
%{tde_datadir}/services/kbabel_linguist_export.desktop
%{tde_datadir}/services/kbabel_linguist_import.desktop
%{tde_datadir}/services/kbabel_nottranslatedtool.desktop
%{tde_datadir}/services/kbabel_pluralformstool.desktop
%{tde_datadir}/services/kbabel_punctuationtool.desktop
%{tde_datadir}/services/kbabel_regexptool.desktop
%{tde_datadir}/services/kbabel_setfuzzytool.desktop
%{tde_datadir}/services/kbabel_whitespacetool.desktop
%{tde_datadir}/services/kbabel_xliff_export.desktop
%{tde_datadir}/services/kbabel_xliff_import.desktop
%{tde_datadir}/services/kbabel_xmltool.desktop
%{tde_datadir}/services/pocompendium.desktop
%{tde_datadir}/services/poauxiliary.desktop
%{tde_datadir}/services/tmxcompendium.desktop
%{tde_datadir}/servicetypes/kbabel_tool.desktop
%{tde_datadir}/servicetypes/kbabel_validator.desktop
%{tde_datadir}/servicetypes/kbabeldict_module.desktop
%{tde_datadir}/servicetypes/kbabelfilter.desktop

%post -n trinity-kbabel
/sbin/ldconfig || :
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kbabel
/sbin/ldconfig || :
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kbabel-devel
Summary:	PO-file editing suite for Trinity (development files)
Group:		Development/Libraries
Requires:	trinity-kbabel = %{version}-%{release}

%description -n trinity-kbabel-devel
This is a suite of programs for editing gettext message files (PO-files).
It is designed to help you translate fast and consistently.

This suite includes KBabel, CatalogManager and KBabelDict.  KBabel is an
advanced and easy to use PO-file editor with full navigational and editing
capabilities, syntax checking and statistics.  CatalogManager is a multi
functional catalog manager which allows you to keep track of many
PO-files at once.  KBabelDict is a dictionary to assist with searching
for common translations.

This package contains the KBabel development files.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-kbabel-devel
%{tde_tdeincludedir}/kbabel/
%{tde_libdir}/libkbabelcommon.la
%{tde_libdir}/libkbabelcommon.so
%{tde_libdir}/libkbabeldictplugin.la
%{tde_libdir}/libkbabeldictplugin.so

%post -n trinity-kbabel-devel
/sbin/ldconfig || :

%postun -n trinity-kbabel-devel
/sbin/ldconfig || :

##########

%package -n trinity-kbugbuster
Summary:	a front end for the Trinity bug tracking system
Group:		Development/Utilities

%description -n trinity-kbugbuster
KBugBuster is a GUI front end for the TDE bug tracking system.
It allows the user to view and manipulate bug reports and provides a
variety of options for searching through reports.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-kbugbuster
%{tde_bindir}/kbugbuster
%{tde_tdelibdir}/kcal_bugzilla.la
%{tde_tdelibdir}/kcal_bugzilla.so
%{tde_tdeappdir}/kbugbuster.desktop
%{tde_datadir}/apps/kbugbuster/
%{tde_datadir}/icons/hicolor/*/apps/kbugbuster.png
%{tde_datadir}/icons/locolor/*/apps/kbugbuster.png
%{tde_datadir}/services/kresources/kcal/bugzilla.desktop
%{tde_tdedocdir}/HTML/en/kbugbuster/

%post -n trinity-kbugbuster
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kbugbuster
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-tdecachegrind
Summary:	visualisation tool for valgrind profiling output
Group:		Development/Utilities

%description -n trinity-tdecachegrind
KCachegrind is a visualisation tool for the profiling data generated
by calltree, a profiling skin for valgrind.  Applications can be
profiled using calltree without being recompiled, and shared libraries
and plugin architectures are supported.

For visualising the output from other profiling tools, several converters
can be found in the tdecachegrind-converters package.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-tdecachegrind
%{tde_bindir}/kcachegrind
%{tde_tdeappdir}/kcachegrind.desktop
%{tde_datadir}/apps/kcachegrind/
%{tde_datadir}/icons/locolor/*/apps/kcachegrind.png
%{tde_datadir}/icons/hicolor/*/apps/kcachegrind.png
%{tde_datadir}/mimelnk/application/x-kcachegrind.desktop
%{tde_tdedocdir}/HTML/en/kcachegrind/

%post -n trinity-tdecachegrind
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-tdecachegrind
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-tdecachegrind-converters
Summary:	format converters for KCachegrind profiling visualisation tool
Group:		Development/Utilities
Requires:	python
%if 0%{?suse_version}
Requires:	php
%else
Requires:	php-cli
%endif

%description -n trinity-tdecachegrind-converters
This is a collection of scripts for converting the output from
different profiling tools into a format that KCachegrind can use.

KCachegrind is a visualisation tool for the profiling data generated
by calltree, a profiling skin for valgrind.  Applications can be
profiled using calltree without being recompiled, and shared libraries
and plugin architectures are supported.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-tdecachegrind-converters
%{tde_bindir}/dprof2calltree
%{tde_bindir}/hotshot2calltree
%{tde_bindir}/memprof2calltree
%{tde_bindir}/op2calltree
%{tde_bindir}/pprof2calltree

##########

%package kfile-plugins
Summary:	Trinity file dialog plugins for software development files
Group:		Environment/Libraries

%description kfile-plugins
This is a collection of plugins for the TDE file dialog.  These plugins
extend the file dialog to offer advanced meta-information for source files,
patch files and Qt Linguist data.

This package is part of Trinity, and a component of the TDE SDK module.

%files kfile-plugins
%{tde_tdelibdir}/kfile_cpp.so
%{tde_tdelibdir}/kfile_cpp.la
%{tde_tdelibdir}/kfile_diff.so
%{tde_tdelibdir}/kfile_diff.la
%{tde_tdelibdir}/kfile_ts.so
%{tde_tdelibdir}/kfile_ts.la
%{tde_datadir}/services/kfile_cpp.desktop
%{tde_datadir}/services/kfile_diff.desktop
%{tde_datadir}/services/kfile_h.desktop
%{tde_datadir}/services/kfile_ts.desktop

##########

%package misc
Summary:	various goodies from the Trinity Software Development Kit
Group:		Development/Libraries

%description misc
This package contains miscellaneous goodies provided with the official
TDE release to assist with TDE software development.

Included are:
- headers to assist with profiling TDE code;
- a widget style for checking conformity with the TDE/Qt style guide;
- palettes that match the KDE standard colour palette;
- a TDE address book plugin that reads the list of TDE CVS accounts.

This package is part of Trinity, and a component of the TDE SDK module.

%files misc
%{tde_tdeincludedir}/kprofilemethod.h
%{tde_tdelibdir}/kabcformat_kdeaccounts.la
%{tde_tdelibdir}/kabcformat_kdeaccounts.so
%{tde_tdelibdir}/plugins/styles/scheck.so
%{tde_tdelibdir}/plugins/styles/scheck.la
%{tde_datadir}/apps/kabc/formats/kdeaccountsplugin.desktop
%{tde_datadir}/apps/kstyle/themes/scheck.themerc
%{tde_datadir}/kdepalettes/

%{tde_libdir}/libkstartperf.so.*
%{tde_libdir}/libkstartperf.so
%{tde_libdir}/libkstartperf.la
%{tde_bindir}/kstartperf

%post misc
/sbin/ldconfig || :

%postun misc
/sbin/ldconfig || :

##########

%package scripts
Summary:	a set of useful development scripts for Trinity
Group:		Development/Utilities
Requires:	python

%description scripts
This package contains a number of scripts which can be used to help in
developing TDE-based applications.  Many of these scripts however are
not specific to TDE, and in particular there are several general-use
scripts to help users in working with SVN and CVS repositories.

In addition to these scripts, this package provides:
- gdb macros for Qt/TDE programming;
- vim and emacs helper files for Qt/TDE programming;
- bash and zsh completion controls for TDE apps;
- valgrind error suppressions for TDE apps.

This package is part of Trinity, and a component of the TDE SDK module.

%files scripts
%{tde_bindir}/adddebug
%{tde_bindir}/build-progress.sh
%{tde_bindir}/cheatmake
%{tde_bindir}/create_cvsignore
%{tde_bindir}/create_makefile
%{tde_bindir}/create_makefiles
%{tde_bindir}/cvs-clean
%{tde_bindir}/cvs2dist
%{tde_bindir}/cvsbackport
%{tde_bindir}/cvsblame
%{tde_bindir}/cvscheck
%{tde_bindir}/cvsforwardport
%{tde_bindir}/cvslastchange
%{tde_bindir}/cvslastlog
%{tde_bindir}/cvsrevertlast
%{tde_bindir}/cvsversion
%{tde_bindir}/cxxmetric
%{tde_bindir}/extend_dmalloc
%{tde_bindir}/extractattr
%{tde_bindir}/extractrc
%{tde_bindir}/findmissingcrystal
%{tde_bindir}/fixkdeincludes
%{tde_bindir}/fixuifiles
%{tde_bindir}/includemocs
%{tde_bindir}/kde-build
%{tde_bindir}/kdedoc
%{tde_bindir}/kdekillall
%{tde_bindir}/kdelnk2desktop.py*
%{tde_bindir}/kdemangen.pl
%{tde_bindir}/makeobj
%{tde_bindir}/noncvslist
%{tde_bindir}/package_crystalsvg
%{tde_bindir}/png2mng.pl
%{tde_bindir}/pruneemptydirs
%{tde_bindir}/qtdoc
%{tde_bindir}/zonetab2pot.py*
%{tde_bindir}/svn2dist
%{tde_bindir}/svnrevertlast
%{tde_bindir}/svnforwardport
%{tde_bindir}/nonsvnlist
%{tde_bindir}/[kt]desvn-build
%{tde_bindir}/svnlastlog
%{tde_bindir}/svnversions
%{tde_bindir}/create_svnignore
%{tde_bindir}/svnlastchange
%{tde_bindir}/colorsvn
%{tde_bindir}/svnaddcurrentdir
%{tde_bindir}/svnbackport
%{tde_bindir}/svngettags
%{tde_bindir}/svnchangesince
%{tde_bindir}/svn-clean
%{tde_datadir}/apps/katepart/syntax/[kt]desvn-buildrc.xml
%{tde_mandir}/man1/man1/cvsblame.1*
%{tde_mandir}/man1/man1/cvscheck.1*
%{tde_mandir}/man1/man1/cvsversion.1*
%{tde_mandir}/man1/man1/kde-build.1*
%{tde_mandir}/man1/man1/includemocs.1*
%{tde_mandir}/man1/man1/noncvslist.1*
%{tde_mandir}/man1/man1/[kt]desvn-build.1*
%{tde_tdedocdir}/HTML/en/[kt]desvn-build/
#scripts/kde-devel-gdb /opt/trinity/share/tdesdk-scripts
#scripts/kde-devel-vim.vim /opt/trinity/share/tdesdk-scripts
#scripts/kde-emacs/*.el /opt/trinity/share/emacs/site-lisp/tdesdk-scripts
#scripts/kde.supp /opt/trinity/lib/valgrind
#scripts/completions /opt/trinity/share/tdesdk-scripts

#debian/desktop-i18n/createdesktop.pl /opt/trinity/lib/kubuntu-desktop-i18n/
#debian/desktop-i18n/findfiles /opt/trinity/lib/kubuntu-desktop-i18n/
#debian/desktop-i18n/msgsplit /opt/trinity/lib/kubuntu-desktop-i18n/

%if "%{?tde_prefix}" != "/usr"
%{tde_bindir}/licensecheck
%else
%exclude %{tde_bindir}/licensecheck
%endif

##########

%package -n trinity-kmtrace
Summary:	a Trinity memory leak tracer
Group:		Development/Utilities
Requires:	less

%description -n trinity-kmtrace
KMtrace is a TDE tool to assist with malloc debugging using glibc's
"mtrace" functionality.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-kmtrace
%{tde_bindir}/demangle
%{tde_bindir}/kminspector
%{tde_bindir}/kmmatch
%{tde_bindir}/kmtrace
%{tde_tdeincludedir}/ktrace.h
%{tde_libdir}/kmtrace/libktrace.la
%{tde_libdir}/kmtrace/libktrace.so
%{tde_libdir}/kmtrace/libktrace_s.a
%{tde_datadir}/apps/kmtrace/kde.excludes

##########

%package -n trinity-kompare
Summary:	a Trinity GUI for viewing differences between files
Group:		Development/Utilities

%description -n trinity-kompare
Kompare is a graphical user interface for viewing the differences between
files.  It can compare two documents, create a diff file, display a diff
file and/or blend a diff file back into the original documents.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-kompare
%{tde_bindir}/kompare
%{tde_libdir}/libkompareinterface.la
%{tde_libdir}/libkompareinterface.so
%{tde_libdir}/libkompareinterface.so.*
%{tde_tdelibdir}/libkomparenavtreepart.la
%{tde_tdelibdir}/libkomparenavtreepart.so
%{tde_tdelibdir}/libkomparepart.la
%{tde_tdelibdir}/libkomparepart.so
%{tde_tdeappdir}/kompare.desktop
%{tde_datadir}/apps/kompare/komparepartui.rc
%{tde_datadir}/apps/kompare/kompareui.rc
%{tde_datadir}/services/komparenavtreepart.desktop
%{tde_datadir}/services/komparepart.desktop
%{tde_datadir}/servicetypes/komparenavigationpart.desktop
%{tde_datadir}/servicetypes/kompareviewpart.desktop
%{tde_datadir}/icons/hicolor/*/apps/kompare.png
%{tde_datadir}/icons/hicolor/scalable/apps/kompare.svgz
%{tde_tdedocdir}/HTML/en/kompare/

%post -n trinity-kompare
/sbin/ldconfig || :
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kompare
/sbin/ldconfig || :
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kspy
Summary:	examines the internal state of a Qt/TDE app
Group:		Environment/Libraries
Requires:	trinity-tdelibs-devel

%description -n trinity-kspy
KSpy is a tiny library which can be used to graphically display
the QObjects in use by a Qt/TDE app.  In addition to the object tree,
you can also view the properties, signals and slots of any QObject.

Basically it provides much the same info as QObject::dumpObjectTree() and
QObject::dumpObjectInfo(), but in a much more convenient form.  KSpy has
minimal overhead for the application, because the kspy library is
loaded dynamically using KLibLoader.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-kspy
%{tde_tdeincludedir}/kspy.h
%{tde_libdir}/libkspy.la
%{tde_libdir}/libkspy.so
%{tde_libdir}/libkspy.so.*

%post -n trinity-kspy
/sbin/ldconfig || :

%postun -n trinity-kspy
/sbin/ldconfig || :

##########

%package -n trinity-kuiviewer
Summary:	viewer for Qt Designer user interface files
Group:		Development/Utilities

%description -n trinity-kuiviewer
KUIViewer is a utility to display and test the user interface (.ui) files
generated by Qt Designer.  The interfaces can be displayed in a variety of
different widget styles.

The Qt Designer itself is in the package qt3-designer.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-kuiviewer
%{tde_bindir}/kuiviewer
%{tde_tdelibdir}/libkuiviewerpart.so
%{tde_tdelibdir}/libkuiviewerpart.la
%{tde_tdelibdir}/quithumbnail.so
%{tde_tdelibdir}/quithumbnail.la
%{tde_tdeappdir}/kuiviewer.desktop
%{tde_datadir}/apps/kuiviewer/kuiviewerui.rc
%{tde_datadir}/apps/kuiviewerpart/kuiviewer_part.rc
%{tde_datadir}/icons/hicolor/*/apps/kuiviewer.png
%{tde_datadir}/icons/locolor/*/apps/kuiviewer.png
%{tde_datadir}/services/designerthumbnail.desktop
%{tde_datadir}/services/kuiviewer_part.desktop

%post -n trinity-kuiviewer
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done

%postun -n trinity-kuiviewer
for f in crystalsvg hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done

##########

%package -n trinity-libcvsservice0
Summary:	DCOP service for accessing CVS repositories
Group:		Environment/Libraries
Requires:	cvs

%description -n trinity-libcvsservice0
This library provides a DCOP service for accessing and working with
remote CVS repositories.  Applications may link with this library to
access the DCOP service directly from C++.  Alternatively, scripts may
access the service using the standard "dcop" command-line tool.

DCOP is the Desktop Communication Protocol used throughout TDE.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-libcvsservice0
%{tde_bindir}/cvsaskpass
%{tde_bindir}/cvsservice
%{tde_libdir}/libcvsservice.so.*
%{tde_libdir}/lib[kt]deinit_cvsaskpass.so
%{tde_libdir}/lib[kt]deinit_cvsservice.so
%{tde_tdelibdir}/cvsaskpass.la
%{tde_tdelibdir}/cvsaskpass.so
%{tde_tdelibdir}/cvsservice.la
%{tde_tdelibdir}/cvsservice.so
%{tde_datadir}/services/cvsservice.desktop

%post -n trinity-libcvsservice0
/sbin/ldconfig || :

%postun -n trinity-libcvsservice0
/sbin/ldconfig || :

##########

%package -n trinity-libcvsservice-devel
Summary:	development files for CVS DCOP service
Group:		Development/Libraries
Requires:	trinity-libcvsservice0 = %{version}-%{release}

%description -n trinity-libcvsservice-devel
The library libcvsservice provides a DCOP service for accessing and
working with remote CVS repositories.  Applications may link with this
library to access the DCOP service directly from C++.  Alternatively,
scripts may access the service using the standard "dcop" command-line
tool.

Development files for libcvsservice are included in this package.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-libcvsservice-devel
%{tde_tdeincludedir}/cvsjob_stub.h
%{tde_tdeincludedir}/cvsservice_stub.h
%{tde_tdeincludedir}/repository_stub.h
%{tde_libdir}/libcvsservice.la
%{tde_libdir}/libcvsservice.so
%{tde_libdir}/lib[kt]deinit_cvsaskpass.la
%{tde_libdir}/lib[kt]deinit_cvsservice.la
%{tde_datadir}/cmake/cervisia.cmake

%post -n trinity-libcvsservice-devel
/sbin/ldconfig || :

%postun -n trinity-libcvsservice-devel
/sbin/ldconfig || :

##########

%package -n trinity-poxml
Summary:	tools for using PO-files to translate DocBook XML files
Group:		Development/Utilities

%description -n trinity-poxml
This is a collection of tools that facilitate translating DocBook XML
files using gettext message files (PO-files).

Also included are some miscellaneous command-line utilities for
manipulating DocBook XML files, PO-files and PO-template files.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-poxml
%{tde_bindir}/po2xml
%{tde_bindir}/split2po
%{tde_bindir}/swappo
%{tde_bindir}/transxx
%{tde_bindir}/xml2pot

##########

%package -n trinity-umbrello
Summary:	UML modelling tool and code generator
Group:		Development/Utilities

%description -n trinity-umbrello
Umbrello UML Modeller is a Unified Modelling Language editor for TDE.
With UML you can create diagrams of software and other systems in an
industry standard format.  Umbrello can also generate code from your
UML diagrams in a number of programming languages.

The program supports class diagrams, sequence diagrams, collaboration
diagrams, use case diagrams, state diagrams, activity diagrams, component
diagrams and deployment diagrams.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-umbrello
%{tde_bindir}/umbodoc
%{tde_bindir}/umbrello
%{tde_tdeappdir}/umbrello.desktop
%{tde_datadir}/apps/umbrello/
%{tde_datadir}/icons/crystalsvg/*/actions/umbrello_*.png
%{tde_datadir}/icons/crystalsvg/*/mimetypes/umbrellofile.png
%{tde_datadir}/icons/crystalsvg/scalable/mimetypes/umbrellofile.svgz
%{tde_datadir}/icons/hicolor/*/apps/umbrello.png
%{tde_datadir}/icons/hicolor/scalable/apps/umbrello.svgz
%{tde_datadir}/icons/hicolor/*/mimetypes/umbrellofile.png
%{tde_datadir}/mimelnk/application/x-umbrello.desktop
%{tde_tdedocdir}/HTML/en/umbrello/

%post -n trinity-umbrello
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-umbrello
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package kio-plugins
Summary:	subversion ioslave for Trinity
Group:		Environment/Libraries
Requires:	subversion

%description kio-plugins
This package provides easy access to remote SVN repositories from within
Konqueror, and TDE generally, by browsing them as if they were a
filesystem, using URLs like svn://hostname/path, or svn+ssh://, etc.

This package is part of Trinity, and a component of the TDE SDK module.

%files kio-plugins
%{tde_bindir}/kio_svn_helper
%{tde_tdelibdir}/kded_ksvnd.la
%{tde_tdelibdir}/kded_ksvnd.so
%{tde_tdelibdir}/kio_svn.la
%{tde_tdelibdir}/kio_svn.so
%{tde_datadir}/apps/konqueror/servicemenus/subversion_toplevel.desktop
%{tde_datadir}/apps/konqueror/servicemenus/subversion.desktop
%{tde_datadir}/services/kded/ksvnd.desktop
%{tde_datadir}/services/svn+file.protocol_tdesdk
%{tde_datadir}/services/svn+http.protocol_tdesdk
%{tde_datadir}/services/svn+https.protocol_tdesdk
%{tde_datadir}/services/svn+ssh.protocol_tdesdk
%{tde_datadir}/services/svn.protocol_tdesdk
%{tde_datadir}/services/svn+file.protocol
%{tde_datadir}/services/svn+http.protocol
%{tde_datadir}/services/svn+https.protocol
%{tde_datadir}/services/svn+ssh.protocol
%{tde_datadir}/services/svn.protocol
%{tde_datadir}/icons/crystalsvg/*/actions/svn_switch.png
%{tde_datadir}/icons/crystalsvg/*/actions/svn_merge.png
%{tde_datadir}/icons/crystalsvg/*/actions/svn_branch.png
%{tde_datadir}/icons/crystalsvg/*/actions/svn_remove.png
%{tde_datadir}/icons/crystalsvg/*/actions/svn_add.png
%{tde_datadir}/icons/crystalsvg/*/actions/svn_status.png
%{tde_datadir}/icons/crystalsvg/scalable/actions/svn_add.svgz
%{tde_datadir}/icons/crystalsvg/scalable/actions/svn_status.svgz
%{tde_datadir}/icons/crystalsvg/scalable/actions/svn_remove.svgz
%{tde_datadir}/icons/crystalsvg/scalable/actions/svn_switch.svgz
%{tde_datadir}/icons/crystalsvg/scalable/actions/svn_branch.svgz
%{tde_datadir}/icons/crystalsvg/scalable/actions/svn_merge.svgz

%post kio-plugins
for f in crystalsvg ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done

for proto in svn+file svn+http svn+https svn+ssh svn; do
%if 0%{?suse_version}
  update-alternatives --install \
%else
  alternatives --install \
%endif
    %{tde_datadir}/services/${proto}.protocol \
    ${proto}.protocol \
    %{tde_datadir}/services/${proto}.protocol_tdesdk \
    10
done

%postun kio-plugins
for f in crystalsvg ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
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
      %{tde_datadir}/services/${proto}.protocol_tdesdk
  done
fi

##########

%package -n trinity-kunittest
Summary:	unit testing library for Trinity
Group:		Development/Utilities

%description -n trinity-kunittest
KUnitTest is a small library that facilitates the writing of tests for
TDE developers. There are two ways to use the KUnitTest library. One is
to create dynamically loadable modules and use the kunittestmodrunner or
kunittestguimodrunner programs to run the tests. The other is to use the
libraries to create your own testing application.

This package is part of Trinity, and a component of the TDE SDK module.

%files -n trinity-kunittest
%{tde_bindir}/kunittest
%{tde_bindir}/kunittest_debughelper
%{tde_bindir}/kunittestmod
%{tde_bindir}/kunittestguimodrunner
%{tde_libdir}/libkunittestgui.la
%{tde_libdir}/libkunittestgui.so
%{tde_libdir}/libkunittestgui.so.*
%{tde_tdeincludedir}/kunittest/runnergui.h

%post -n trinity-kunittest
/sbin/ldconfig || :

%postun -n trinity-kunittest
/sbin/ldconfig || :

##########

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}
Requires:	trinity-kbabel-devel = %{version}-%{release}

Obsoletes:	trinity-kdesdk-devel < %{version}-%{release}
Provides:	trinity-kdesdk-devel = %{version}-%{release}

%description devel
%{summary}.

%files devel

##########

%if 0%{?suse_version}
%debug_package
%endif

##########


%prep
%setup -q -n kdesdk-trinity-%{version}
#%patch4 -p1 -b .ftbfs
#%patch5 -p1 -b .svn
%patch6 -p1 -b .cmake
#%patch7 -p1
#%patch8 -p1 -b .flex

%__sed -i 's/TQT_PREFIX/TDE_PREFIX/g' cmake/modules/FindTQt.cmake

%build
unset QTDIR || :; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LD_LIBRARY_PATH="%{tde_libdir}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"
export CMAKE_INCLUDE_PATH="%{tde_includedir}:%{tde_includedir}/tqt"

%if 0%{?rhel} || 0%{?fedora} || 0%{?suse_version}
%__mkdir_p build
cd build
%endif

%cmake \
  -DCMAKE_PREFIX_PATH=%{tde_prefix} \
  -DTDE_PREFIX=%{tde_prefix} \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DMAN_INSTALL_DIR=%{tde_mandir}/man1 \
  -DPKGCONFIG_INSTALL_DIR=%{tde_tdelibdir}/pkgconfig \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  -DCMAKE_SKIP_RPATH="OFF" \
  -DWITH_DBSEARCHENGINE=ON \
  -DWITH_KCAL=ON \
  -DBUILD_ALL=ON \
  ..

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot} 

%__make install DESTDIR=%{?buildroot} -C build

# make symlinks relative
if [ -d %{buildroot}%{tde_tdedocdir}/HTML/en ]; then
  pushd %{buildroot}%{tde_tdedocdir}/HTML/en
  for i in *; do
     if [ -d $i -a -L $i/common ]; then
        rm -f $i/common
        ln -nfs ../common $i
     fi
  done
  popd
fi

# Installs kdepalettes
%__install -D -m 644 kdepalettes/kde_xpaintrc %{?buildroot}%{tde_datadir}/kdepalettes
%__install -D -m 644 kdepalettes/KDE_Gimp %{?buildroot}%{tde_datadir}/kdepalettes
%__install -D -m 644 kdepalettes/README %{?buildroot}%{tde_datadir}/kdepalettes

# Installs SVN protocols as alternatives
%__mv -f %{?buildroot}%{tde_datadir}/services/svn+file.protocol %{?buildroot}%{tde_datadir}/services/svn+file.protocol_tdesdk
%__mv -f %{?buildroot}%{tde_datadir}/services/svn+http.protocol %{?buildroot}%{tde_datadir}/services/svn+http.protocol_tdesdk
%__mv -f %{?buildroot}%{tde_datadir}/services/svn+https.protocol %{?buildroot}%{tde_datadir}/services/svn+https.protocol_tdesdk
%__mv -f %{?buildroot}%{tde_datadir}/services/svn+ssh.protocol %{?buildroot}%{tde_datadir}/services/svn+ssh.protocol_tdesdk
%__mv -f %{?buildroot}%{tde_datadir}/services/svn.protocol %{?buildroot}%{tde_datadir}/services/svn.protocol_tdesdk
%__ln_s /etc/alternatives/svn+file.protocol %{?buildroot}%{tde_datadir}/services/svn+file.protocol
%__ln_s /etc/alternatives/svn+http.protocol %{?buildroot}%{tde_datadir}/services/svn+http.protocol
%__ln_s /etc/alternatives/svn+https.protocol %{?buildroot}%{tde_datadir}/services/svn+https.protocol
%__ln_s /etc/alternatives/svn+ssh.protocol %{?buildroot}%{tde_datadir}/services/svn+ssh.protocol
%__ln_s /etc/alternatives/svn.protocol %{?buildroot}%{tde_datadir}/services/svn.protocol

%clean
%__rm -rf %{buildroot}


# trick to replace a dir by a symlink -- Rex
%pre
if [ $1 -gt 0 -a ! -L  %{_docdir}/HTML/en/cervisia/common ]; then 
  rm -rf %{tde_tdedocdir}/HTML/en/cervisia/common ||:
fi



%changelog
* Sun Sep 30 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial build for TDE 3.5.13.1
