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

%define tde_tdeappdir %{tde_datadir}/applications/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}

Name:		trinity-tdevelop
Summary:	Integrated Development Environment for C++/C
Version:	3.5.13.2
Release:	1%{?dist}%{?_variant}

License:	GPLv2
Group:		Development/Tools

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source:		kdevelop-trinity-%{version}.tar.xz
Source1:	ftp://129.187.206.68/pub/unix/ide/KDevelop/c_cpp_reference-2.0.2_for_KDE_3.0.tar.bz2

# [c_cpp_ref] Fix library directories detection
Patch1: c_cpp_reference-2.0.2-config.patch

# [kdevelop] fix FTBFS
Patch2: kdevelop-3.5.13-kdevdesigner-ftbfs.patch

# [c_cpp_ref] Fix installation of 'asm' files
Patch4:	c_cpp_reference-2.0.2-install.patch

Requires: %{name}-libs = %{version}-%{release}


Requires: make
Requires: perl
Requires: flex >= 2.5.4
%if 0%{?rhel} || 0%{?fedora}
Requires:	qt-designer
%endif
%if 0%{?mgaversion} || 0%{?mdkversion}
Requires:	%{_lib}qt3-devel
%endif
%if 0%{?suse_version}
Requires:	qt3-devel
%endif
Requires: gettext
Requires: ctags

BuildRequires:	cmake >= 2.8
BuildRequires:	trinity-tqtinterface-devel >= %{version}
BuildRequires:	trinity-arts-devel >= %{version}
BuildRequires:	trinity-tdelibs-devel >= %{version}
BuildRequires:	trinity-tdesdk-devel >= %{version}
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	libdb-devel
%endif
BuildRequires:	flex
# FIXME: No CVS support in KDevelop? This is going to suck...
# Requires kdesdk3.
BuildRequires:	subversion-devel
BuildRequires:	neon-devel
# looks like this is dragged in by apr-devel (dep of subversion-devel), but not
# a dependency
%if 0%{?suse_version}
BuildRequires:	openldap2-devel
%else
BuildRequires:	openldap-devel
%endif

Obsoletes:	trinity-kdevelop < %{version}-%{release}
Provides:	trinity-kdevelop = %{version}-%{release}

%description
The TDevelop Integrated Development Environment provides many features
that developers need as well as providing a unified interface to programs
like gdb, the C/C++ compiler, and make. TDevelop manages or provides:

All development tools needed for C++ programming like Compiler,
Linker, automake and autoconf; KAppWizard, which generates complete,
ready-to-go sample applications; Classgenerator, for creating new
classes and integrating them into the current project; File management
for sources, headers, documentation etc. to be included in the
project; The creation of User-Handbooks written with SGML and the
automatic generation of HTML-output with the KDE look and feel;
Automatic HTML-based API-documentation for your project's classes with
cross-references to the used libraries; Internationalization support
for your application, allowing translators to easily add their target
language to a project;

KDevelop also includes WYSIWYG (What you see is what you get)-creation
of user interfaces with a built-in dialog editor; Debugging your
application by integrating KDbg; Editing of project-specific pixmaps
with KIconEdit; The inclusion of any other program you need for
development by adding it to the "Tools"-menu according to your
individual needs.

%files
%defattr(-,root,root,-)
%{tde_bindir}/kdevassistant
%{tde_bindir}/kdevdesigner
%{tde_bindir}/kdevelop
%{tde_bindir}/kdevelop-htdig
%{tde_bindir}/kdevprj2kdevelop
%{tde_bindir}/kdevprofileeditor
%{tde_libdir}/kconf_update_bin/kdev-gen-settings-kconf_update
%{tde_tdeappdir}/kdevassistant.desktop
%{tde_tdeappdir}/kdevdesigner.desktop
%{tde_tdeappdir}/kdevelop.desktop
%{tde_tdeappdir}/kdevelop_c_cpp.desktop
%{tde_tdeappdir}/kdevelop_kde_cpp.desktop
%{tde_tdeappdir}/kdevelop_ruby.desktop
%{tde_tdeappdir}/kdevelop_scripting.desktop
%{tde_tdelibdir}/kio_chm.la
%{tde_tdelibdir}/kio_chm.so
%{tde_tdelibdir}/kio_csharpdoc.la
%{tde_tdelibdir}/kio_csharpdoc.so
%{tde_tdelibdir}/kio_perldoc.la
%{tde_tdelibdir}/kio_perldoc.so
%{tde_tdelibdir}/kio_pydoc.la
%{tde_tdelibdir}/kio_pydoc.so
%{tde_tdelibdir}/libdocchmplugin.la
%{tde_tdelibdir}/libdocchmplugin.so
%{tde_tdelibdir}/libdoccustomplugin.la
%{tde_tdelibdir}/libdoccustomplugin.so
%{tde_tdelibdir}/libdocdevhelpplugin.la
%{tde_tdelibdir}/libdocdevhelpplugin.so
%{tde_tdelibdir}/libdocdoxygenplugin.la
%{tde_tdelibdir}/libdocdoxygenplugin.so
%{tde_tdelibdir}/libdockdevtocplugin.la
%{tde_tdelibdir}/libdockdevtocplugin.so
%{tde_tdelibdir}/libdocqtplugin.la
%{tde_tdelibdir}/libdocqtplugin.so
%{tde_tdelibdir}/libkchmpart.la
%{tde_tdelibdir}/libkchmpart.so
%{tde_tdelibdir}/libkdevabbrev.la
%{tde_tdelibdir}/libkdevabbrev.so
%{tde_tdelibdir}/libkdevadaproject.la
%{tde_tdelibdir}/libkdevadaproject.so
%{tde_tdelibdir}/libkdevadasupport.la
%{tde_tdelibdir}/libkdevadasupport.so
%{tde_tdelibdir}/libkdevantproject.la
%{tde_tdelibdir}/libkdevantproject.so
%{tde_tdelibdir}/libkdevappview.la
%{tde_tdelibdir}/libkdevappview.so
%{tde_tdelibdir}/libkdevappwizard.la
%{tde_tdelibdir}/libkdevappwizard.so
%{tde_tdelibdir}/libkdevastyle.la
%{tde_tdelibdir}/libkdevastyle.so
%{tde_tdelibdir}/libkdevautoproject.la
%{tde_tdelibdir}/libkdevautoproject.so
%{tde_tdelibdir}/libkdevbashsupport.la
%{tde_tdelibdir}/libkdevbashsupport.so
%{tde_tdelibdir}/libkdevbookmarks.la
%{tde_tdelibdir}/libkdevbookmarks.so
%{tde_tdelibdir}/libkdevclassview.la
%{tde_tdelibdir}/libkdevclassview.so
%{tde_tdelibdir}/libkdevcppsupport.la
%{tde_tdelibdir}/libkdevcppsupport.so
%{tde_tdelibdir}/libkdevcsharpsupport.la
%{tde_tdelibdir}/libkdevcsharpsupport.so
%{tde_tdelibdir}/libkdevctags2.la
%{tde_tdelibdir}/libkdevctags2.so
%{tde_tdelibdir}/libkdevcustompcsimporter.la
%{tde_tdelibdir}/libkdevcustompcsimporter.so
%{tde_tdelibdir}/libkdevcustomproject.la
%{tde_tdelibdir}/libkdevcustomproject.so
%{tde_tdelibdir}/libkdevdccoptions.la
%{tde_tdelibdir}/libkdevdccoptions.so
%{tde_tdelibdir}/libkdevdebugger.la
%{tde_tdelibdir}/libkdevdebugger.so
%{tde_tdelibdir}/libkdevdesignerpart.la
%{tde_tdelibdir}/libkdevdesignerpart.so
%{tde_tdelibdir}/libkdevdiff.la
%{tde_tdelibdir}/libkdevdiff.so
%{tde_tdelibdir}/libkdevdistpart.la
%{tde_tdelibdir}/libkdevdistpart.so
%{tde_tdelibdir}/libkdevdocumentation.la
%{tde_tdelibdir}/libkdevdocumentation.so
%{tde_tdelibdir}/libkdevdoxygen.la
%{tde_tdelibdir}/libkdevdoxygen.so
%{tde_tdelibdir}/libkdeveditorchooser.la
%{tde_tdelibdir}/libkdeveditorchooser.so
%{tde_tdelibdir}/libkdevfilecreate.la
%{tde_tdelibdir}/libkdevfilecreate.so
%{tde_tdelibdir}/libkdevfilegroups.la
%{tde_tdelibdir}/libkdevfilegroups.so
%{tde_tdelibdir}/libkdevfilelist.la
%{tde_tdelibdir}/libkdevfilelist.so
%{tde_tdelibdir}/libkdevfileselector.la
%{tde_tdelibdir}/libkdevfileselector.so
%{tde_tdelibdir}/libkdevfileview.la
%{tde_tdelibdir}/libkdevfileview.so
%{tde_tdelibdir}/libkdevfilter.la
%{tde_tdelibdir}/libkdevfilter.so
%{tde_tdelibdir}/libkdevfortransupport.la
%{tde_tdelibdir}/libkdevfortransupport.so
%{tde_tdelibdir}/libkdevfpcoptions.la
%{tde_tdelibdir}/libkdevfpcoptions.so
%{tde_tdelibdir}/libkdevfullscreen.la
%{tde_tdelibdir}/libkdevfullscreen.so
%{tde_tdelibdir}/libkdevgccoptions.la
%{tde_tdelibdir}/libkdevgccoptions.so
%{tde_tdelibdir}/libkdevgrepview.la
%{tde_tdelibdir}/libkdevgrepview.so
%{tde_tdelibdir}/libkdevjavasupport.la
%{tde_tdelibdir}/libkdevjavasupport.so
%{tde_tdelibdir}/libkdevkdelibsimporter.la
%{tde_tdelibdir}/libkdevkdelibsimporter.so
%{tde_tdelibdir}/libkdevkonsoleview.la
%{tde_tdelibdir}/libkdevkonsoleview.so
%{tde_tdelibdir}/libkdevmakeview.la
%{tde_tdelibdir}/libkdevmakeview.so
%{tde_tdelibdir}/libkdevopenwith.la
%{tde_tdelibdir}/libkdevopenwith.so
%{tde_tdelibdir}/libkdevpartexplorer.la
%{tde_tdelibdir}/libkdevpartexplorer.so
%{tde_tdelibdir}/libkdevpascalproject.la
%{tde_tdelibdir}/libkdevpascalproject.so
%{tde_tdelibdir}/libkdevpascalsupport.la
%{tde_tdelibdir}/libkdevpascalsupport.so
%{tde_tdelibdir}/libkdevperlsupport.la
%{tde_tdelibdir}/libkdevperlsupport.so
%{tde_tdelibdir}/libkdevpgioptions.la
%{tde_tdelibdir}/libkdevpgioptions.so
%{tde_tdelibdir}/libkdevphpsupport.la
%{tde_tdelibdir}/libkdevphpsupport.so
%{tde_tdelibdir}/libkdevpythonsupport.la
%{tde_tdelibdir}/libkdevpythonsupport.so
%{tde_tdelibdir}/libkdevqt4importer.la
%{tde_tdelibdir}/libkdevqt4importer.so
%{tde_tdelibdir}/libkdevqtimporter.la
%{tde_tdelibdir}/libkdevqtimporter.so
%{tde_tdelibdir}/libkdevquickopen.la
%{tde_tdelibdir}/libkdevquickopen.so
%{tde_tdelibdir}/libkdevrbdebugger.la
%{tde_tdelibdir}/libkdevrbdebugger.so
%{tde_tdelibdir}/libkdevregexptest.la
%{tde_tdelibdir}/libkdevregexptest.so
%{tde_tdelibdir}/libkdevreplace.la
%{tde_tdelibdir}/libkdevreplace.so
%{tde_tdelibdir}/libkdevrubysupport.la
%{tde_tdelibdir}/libkdevrubysupport.so
%{tde_tdelibdir}/libkdevscripting.la
%{tde_tdelibdir}/libkdevscripting.so
%{tde_tdelibdir}/libkdevscriptproject.la
%{tde_tdelibdir}/libkdevscriptproject.so
%{tde_tdelibdir}/libkdevsnippet.la
%{tde_tdelibdir}/libkdevsnippet.so
%{tde_tdelibdir}/libkdevsqlsupport.la
%{tde_tdelibdir}/libkdevsqlsupport.so
%{tde_tdelibdir}/libkdevtexttools.la
%{tde_tdelibdir}/libkdevtexttools.so
%{tde_tdelibdir}/libkdevtipofday.la
%{tde_tdelibdir}/libkdevtipofday.so
%{tde_tdelibdir}/libkdevtools.la
%{tde_tdelibdir}/libkdevtools.so
%{tde_tdelibdir}/libkdevtrollproject.la
%{tde_tdelibdir}/libkdevtrollproject.so
%{tde_tdelibdir}/libkdevuichooser.la
%{tde_tdelibdir}/libkdevuichooser.so
%{tde_tdelibdir}/libkdevvalgrind.la
%{tde_tdelibdir}/libkdevvalgrind.so
%{tde_tdelibdir}/libkdevvcsmanager.la
%{tde_tdelibdir}/libkdevvcsmanager.so
%{tde_datadir}/apps/kconf_update/
%{tde_datadir}/apps/kdevabbrev/
%{tde_datadir}/apps/kdevadaproject/kdevadaproject.rc
%{tde_datadir}/apps/kdevadasupport/kdevadasupport.rc
%{tde_datadir}/apps/kdevantproject/kdevantproject.rc
%{tde_datadir}/apps/kdevappoutputview/kdevmakeview.rc
%{tde_datadir}/apps/kdevappwizard/
%{tde_datadir}/apps/kdevassistant/kdevassistantui.rc
%{tde_datadir}/apps/kdevastyle/kdevpart_astyle.rc
%{tde_datadir}/apps/kdevautoproject/kdevautoproject.rc
%{tde_datadir}/apps/kdevbashsupport/kdevbashsupport.rc
%{tde_datadir}/apps/kdevclassview/
%{tde_datadir}/apps/kdevcppsupport/
%{tde_datadir}/icons/hicolor/*/actions/breakpoint_add.png
%{tde_datadir}/icons/hicolor/*/actions/breakpoint_delete.png
%{tde_datadir}/icons/hicolor/*/actions/breakpoint_delete_all.png
%{tde_datadir}/icons/hicolor/*/actions/breakpoint_edit.png
%{tde_datadir}/icons/hicolor/*/actions/ktip.png
%{tde_datadir}/icons/hicolor/*/apps/kdevassistant.png
%{tde_datadir}/icons/hicolor/*/apps/kdevdesigner.png
%{tde_datadir}/icons/hicolor/*/apps/kdevelop.png
%{tde_datadir}/icons/locolor/*/actions/kdevelop_tip.png
%{tde_datadir}/mimelnk/application/x-kdevelop.desktop
#%{tde_datadir}/mimelnk/x-fortran.desktop
%{tde_libdir}/libd.so.*
%{tde_libdir}/libkinterfacedesigner.so.*
%{tde_tdelibdir}/libkdevvisualboyadvance.la
%{tde_tdelibdir}/libkdevvisualboyadvance.so
%{tde_datadir}/apps/kdevdesignerpart/pics/*
%{tde_datadir}/apps/kdevvisualboyadvance/kdevpart_visualboyadvance.rc
%{tde_datadir}/doc/tde/HTML/en/kde_app_devel/*
%{tde_datadir}/mimelnk/text/x-fortran.desktop
%{tde_datadir}/services/kdevvisualboyadvance.desktop
%{tde_datadir}/services/chm.protocol
%{tde_datadir}/services/csharpdoc.protocol
%{tde_datadir}/services/docchmplugin.desktop
%{tde_datadir}/services/doccustomplugin.desktop
%{tde_datadir}/services/docdevhelpplugin.desktop
%{tde_datadir}/services/docdoxygenplugin.desktop
%{tde_datadir}/services/dockdevtocplugin.desktop
%{tde_datadir}/services/docqtplugin.desktop
%{tde_datadir}/services/kchmpart.desktop
%{tde_datadir}/services/kdevabbrev.desktop
%{tde_datadir}/services/kdevadaproject.desktop
%{tde_datadir}/services/kdevadasupport.desktop
%{tde_datadir}/services/kdevantproject.desktop
%{tde_datadir}/services/kdevappoutputview.desktop
%{tde_datadir}/services/kdevappwizard.desktop
%{tde_datadir}/services/kdevastyle.desktop
%{tde_datadir}/services/kdevautoproject.desktop
%{tde_datadir}/services/kdevbashsupport.desktop
%{tde_datadir}/services/kdevbookmarks.desktop
%{tde_datadir}/services/kdevclassview.desktop
%{tde_datadir}/services/kdevcppsupport.desktop
%{tde_datadir}/services/kdevcsharpsupport.desktop
%{tde_datadir}/services/kdevcsupport.desktop
%{tde_datadir}/services/kdevctags2.desktop
%{tde_datadir}/services/kdevcustomproject.desktop
%{tde_datadir}/services/kdevdccoptions.desktop
%{tde_datadir}/services/kdevdebugger.desktop
%{tde_datadir}/services/kdevdesigner_part.desktop
%{tde_datadir}/services/kdevdiff.desktop
%{tde_datadir}/services/kdevdistpart.desktop
%{tde_datadir}/services/kdevdocumentation.desktop
%{tde_datadir}/services/kdevdoxygen.desktop
%{tde_datadir}/services/kdeveditorchooser.desktop
%{tde_datadir}/services/kdevfilecreate.desktop
%{tde_datadir}/services/kdevfilegroups.desktop
%{tde_datadir}/services/kdevfilelist.desktop
%{tde_datadir}/services/kdevfileselector.desktop
%{tde_datadir}/services/kdevfileview.desktop
%{tde_datadir}/services/kdevfilter.desktop
%{tde_datadir}/services/kdevfortransupport.desktop
%{tde_datadir}/services/kdevfpcoptions.desktop
%{tde_datadir}/services/kdevfullscreen.desktop
%{tde_datadir}/services/kdevg77options.desktop
%{tde_datadir}/services/kdevgccoptions.desktop
%{tde_datadir}/services/kdevgppoptions.desktop
%{tde_datadir}/services/kdevgrepview.desktop
%{tde_datadir}/services/kdevjavasupport.desktop
%{tde_datadir}/services/kdevkdeautoproject.desktop
%{tde_datadir}/services/kdevkdelibsimporter.desktop
%{tde_datadir}/services/kdevkonsoleview.desktop
%{tde_datadir}/services/kdevmakeview.desktop
%{tde_datadir}/services/kdevopenwith.desktop
%{tde_datadir}/services/kdevpartexplorer.desktop
%{tde_datadir}/services/kdevpascalproject.desktop
%{tde_datadir}/services/kdevpascalsupport.desktop
%{tde_datadir}/services/kdevpcscustomimporter.desktop
%{tde_datadir}/services/kdevperlsupport.desktop
%{tde_datadir}/services/kdevpgf77options.desktop
%{tde_datadir}/services/kdevpghpfoptions.desktop
%{tde_datadir}/services/kdevphpsupport.desktop
%{tde_datadir}/services/kdevpythonsupport.desktop
%{tde_datadir}/services/kdevqt4importer.desktop
%{tde_datadir}/services/kdevqtimporter.desktop
%{tde_datadir}/services/kdevquickopen.desktop
%{tde_datadir}/services/kdevrbdebugger.desktop
%{tde_datadir}/services/kdevregexptest.desktop
%{tde_datadir}/services/kdevreplace.desktop
%{tde_datadir}/services/kdevrubysupport.desktop
%{tde_datadir}/services/kdevscripting.desktop
%{tde_datadir}/services/kdevscriptproject.desktop
%{tde_datadir}/services/kdevsnippet.desktop
%{tde_datadir}/services/kdevsqlsupport.desktop
%{tde_datadir}/services/kdevtexttools.desktop
%{tde_datadir}/services/kdevtipofday.desktop
%{tde_datadir}/services/kdevtmakeproject.desktop
%{tde_datadir}/services/kdevtools.desktop
%{tde_datadir}/services/kdevtrollproject.desktop
%{tde_datadir}/services/kdevuichooser.desktop
%{tde_datadir}/services/kdevvalgrind.desktop
%{tde_datadir}/services/kdevvcsmanager.desktop
%{tde_datadir}/services/perldoc.protocol
%{tde_datadir}/services/pydoc.protocol
%{tde_datadir}/servicetypes/kdevelopappfrontend.desktop
%{tde_datadir}/servicetypes/kdevelopcodebrowserfrontend.desktop
%{tde_datadir}/servicetypes/kdevelopcompileroptions.desktop
%{tde_datadir}/servicetypes/kdevelopcreatefile.desktop
%{tde_datadir}/servicetypes/kdevelopdifffrontend.desktop
%{tde_datadir}/servicetypes/kdevelopdocumentationplugins.desktop
%{tde_datadir}/servicetypes/kdeveloplanguagesupport.desktop
%{tde_datadir}/servicetypes/kdevelopmakefrontend.desktop
%{tde_datadir}/servicetypes/kdeveloppcsimporter.desktop
%{tde_datadir}/servicetypes/kdevelopplugin.desktop
%{tde_datadir}/servicetypes/kdevelopproject.desktop
%{tde_datadir}/servicetypes/kdevelopquickopen.desktop
%{tde_datadir}/servicetypes/kdevelopsourceformatter.desktop
%{tde_datadir}/servicetypes/kdevelopvcsintegrator.desktop
%{tde_datadir}/servicetypes/kdevelopversioncontrol.desktop
%{tde_datadir}/apps/kdevcsharpsupport/kdevcsharpsupport.rc
%{tde_datadir}/apps/kdevctags2/kdevpart_ctags2.rc
%{tde_datadir}/apps/kdevcustomproject/kdevcustomproject.rc
%{tde_datadir}/apps/kdevdebugger/
%{tde_datadir}/apps/kdevdesigner/kdevdesigner_shell.rc
%{tde_datadir}/apps/kdevdesignerpart/kdevdesigner_part.rc
%{tde_datadir}/apps/kdevdesignerpart/kdevdesigner_part_sh.rc
%{tde_datadir}/apps/kdevdiff/kdevdiff.rc
%{tde_datadir}/apps/kdevdistpart/kdevpart_distpart.rc
%{tde_datadir}/apps/kdevdocumentation/
%{tde_datadir}/apps/kdevdoxygen/kdevdoxygen.rc
%{tde_datadir}/apps/kdevelop/
%{tde_datadir}/apps/kdevfilecreate/
%{tde_datadir}/apps/kdevfilelist/kdevfilelist.rc
%{tde_datadir}/apps/kdevfilter/kdevfilter.rc
%{tde_datadir}/apps/kdevfortransupport/kdevfortransupport.rc
%{tde_datadir}/apps/kdevfullscreen/kdevpart_fullscreen.rc
%{tde_datadir}/apps/kdevgrepview/
%{tde_datadir}/apps/kdevjavasupport/kdevjavasupport.rc
%{tde_datadir}/apps/kdevmakeview/kdevmakeview.rc
%{tde_datadir}/apps/kdevpartexplorer/kdevpartexplorer.rc
%{tde_datadir}/apps/kdevpascalproject/kdevpascalproject.rc
%{tde_datadir}/apps/kdevpascalsupport/kdevpascalsupport.rc
%{tde_datadir}/apps/kdevperlsupport/kdevperlsupport.rc
%{tde_datadir}/apps/kdevphpsupport/kdevphpsupport.rc
%{tde_datadir}/apps/kdevphpsupport/phpfunctions
%{tde_datadir}/apps/kdevpythonsupport/kdevpythonsupport.rc
%{tde_datadir}/apps/kdevquickopen/kdevpart_quickopen.rc
%{tde_datadir}/apps/kdevrbdebugger/
%{tde_datadir}/apps/kdevregexptest/kdevregexptest.rc
%{tde_datadir}/apps/kdevreplace/kdevpart_replace.rc
%{tde_datadir}/apps/kdevrubysupport/kdevrubysupport.rc
%{tde_datadir}/apps/kdevrubysupport/pics/ruby_config.png
%{tde_datadir}/apps/kdevrubysupport/pics/ruby_run.png
%{tde_datadir}/apps/kdevscripting/kdevscripting.rc
%{tde_datadir}/apps/kdevscriptproject/kdevscriptproject.rc
%{tde_datadir}/apps/kdevsnippet/kdevpart_snippet.rc
%{tde_datadir}/apps/kdevsqlsupport/kdevsqlsupport.rc
%{tde_datadir}/apps/kdevtipofday/kdevpart_tipofday.rc
%{tde_datadir}/apps/kdevtipofday/tips
%{tde_datadir}/apps/kdevtools/kdevpart_tools.rc
%{tde_datadir}/apps/kdevtrollproject/kdevtrollproject.rc
%{tde_datadir}/apps/kdevvalgrind/kdevpart_valgrind.rc
%{tde_datadir}/apps/kio_pydoc/kde_pydoc.py*
%{tde_datadir}/config/kdevassistantrc
%{tde_datadir}/config/kdeveloprc
%{tde_datadir}/desktop-directories/kde-development-kdevelop.directory
%{tde_tdedocdir}/HTML/en/kdevelop/


%post
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}

Obsoletes:	trinity-kdevelop-devel < %{version}-%{release}
Provides:	trinity-kdevelop-devel = %{version}-%{release}

%description devel
%{summary}.

%files devel
%defattr(-,root,root,-)
%{tde_libdir}/lib*.so
%{tde_libdir}/lib*.la
%{tde_includedir}/*

%post devel
/sbin/ldconfig || :

%postun devel
/sbin/ldconfig || :

##########

%package libs
Summary: %{name} runtime libraries
Group:   System Environment/Libraries
Requires: trinity-kdelibs
# include to be paranoid, installing libs-only is still mostly untested -- Rex
Requires: %{name} = %{version}-%{release}

Obsoletes:	trinity-kdevelop-libs < %{version}-%{release}
Provides:	trinity-kdevelop-libs = %{version}-%{release}

%description libs
%{summary}.

%files libs
%defattr(-,root,root,-)
%{tde_libdir}/libdesignerintegration.so.0
%{tde_libdir}/libdesignerintegration.so.0.0.0
%{tde_libdir}/libdocumentation_interfaces.so.0
%{tde_libdir}/libdocumentation_interfaces.so.0.0.0
%{tde_libdir}/libgdbmi_parser.so.0
%{tde_libdir}/libgdbmi_parser.so.0.0.0
%{tde_libdir}/libkdevbuildbase.so.0
%{tde_libdir}/libkdevbuildbase.so.0.0.0
%{tde_libdir}/libkdevbuildtoolswidgets.so.0
%{tde_libdir}/libkdevbuildtoolswidgets.so.0.0.0
%{tde_libdir}/libkdevcatalog.so.0
%{tde_libdir}/libkdevcatalog.so.0.0.0
%{tde_libdir}/libkdevcppparser.so.0
%{tde_libdir}/libkdevcppparser.so.0.0.0
%{tde_libdir}/libkdevelop.so.1
%{tde_libdir}/libkdevelop.so.1.0.0
%{tde_libdir}/libkdevextras.so.0
%{tde_libdir}/libkdevextras.so.0.0.0
%{tde_libdir}/libkdevpropertyeditor.so.0
%{tde_libdir}/libkdevpropertyeditor.so.0.0.0
%{tde_libdir}/libkdevqmakeparser.so.0
%{tde_libdir}/libkdevqmakeparser.so.0.0.0
%{tde_libdir}/libkdevshell.so.0
%{tde_libdir}/libkdevshell.so.0.0.0
%{tde_libdir}/libkdevwidgets.so.0
%{tde_libdir}/libkdevwidgets.so.0.0.0
%{tde_libdir}/liblang_debugger.so.0
%{tde_libdir}/liblang_debugger.so.0.0.0
%{tde_libdir}/liblang_interfaces.so.0
%{tde_libdir}/liblang_interfaces.so.0.0.0
%{tde_libdir}/libprofileengine.so.0
%{tde_libdir}/libprofileengine.so.0.0.0

%post libs
/sbin/ldconfig || :

%postun libs
/sbin/ldconfig || :

##########

%if 0%{?suse_version}
%debug_package
%endif

##########

%prep
%setup -q -n kdevelop-trinity-%{version} -a1
%patch1 -p0 -b .config
%patch2 -p1
%patch4 -p1

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i "admin/acinclude.m4.in" \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"

%__rm -rf c_cpp_reference-2.0.2_for_KDE_3.0/admin
%__cp -ar admin c_cpp_reference-2.0.2_for_KDE_3.0/
%__make -C c_cpp_reference-2.0.2_for_KDE_3.0 -f admin/Makefile.common cvs


%__sed -i 's/TQT_PREFIX/TDE_PREFIX/g' cmake/modules/FindTQt.cmake

%build
unset QTDIR || : ; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"
export CMAKE_INCLUDE_PATH="%{tde_includedir}:%{tde_includedir}/tqt"
export LD_LIBRARY_PATH="%{tde_libdir}"

# c references
pushd c_cpp_reference-2.0.2_for_KDE_3.0
%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --with-qt-libraries=${QTLIB:-${QTDIR}/%{_lib}} \
  --with-qt-includes=${QTINC:-${QTDIR}/include} \
  --with-extra-libs=%{tde_libdir}
popd

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
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  -DCMAKE_SKIP_RPATH="OFF" \
  -DWITH_BUILDTOOL_ALL=ON \
  -DWITH_LANGUAGE_ALL=ON \
  -DWITH_VCS_ALL=OFF \
  -DBUILD_ALL=ON \
  ..
  

%__make %{?_smp_mflags}

# c references
cd ..
%__make %{?_smp_mflags} -C c_cpp_reference-2.0.2_for_KDE_3.0

%install
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot} -C build
%__make install DESTDIR=%{buildroot} -C c_cpp_reference-2.0.2_for_KDE_3.0


%clean
%__rm -rf %{buildroot}


%changelog
* Mon Oct 01 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial build for TDE 3.5.13.1
