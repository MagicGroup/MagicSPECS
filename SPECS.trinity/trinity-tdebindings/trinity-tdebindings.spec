#
# spec file for package tdebindings (version R14)
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

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg tdebindings
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

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# Special note for RHEL4:
#  You must create symlink 'libgcj.so' manually because it does not exist by default.
# E.g:
#  ln -s /usr/lib/libgcj.so.5.0.0 /usr/lib/jvm/java/lib/libgcj.so
# or 64 bits:
#  ln -s /usr/lib64/libgcj.so.5.0.0 /usr/lib/jvm/java/lib/libgcj.so

Name:			trinity-%{tde_pkg}
Summary:		TDE bindings to non-C++ languages
Version:		%{tde_version}
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1
Group:			System/GUI/Other
URL:			http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{tde_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{version}%{?preversion:~%{preversion}}.tar.gz
Patch0:			trinity-tdebindings-14.0.1-tqt.patch

BuildRequires:	trinity-arts-devel >= %{tde_epoch}:1.5.10
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	desktop-file-utils

# ZLIB support
BuildRequires: zlib-devel

# PERL module support
BuildRequires: perl(ExtUtils::MakeMaker)

# GTK2 support
BuildRequires:	gtk2-devel

# XULRUNNER support
#BuildRequires: xulrunner-devel

# OPENSSL support
BuildRequires:	openssl-devel

# GTK1 support
%define with_gtk1 1
BuildRequires: glib-devel
BuildRequires: gtk+-devel

BuildRequires: gdk-pixbuf2-devel

# MESA support
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libGLU-devel

## Python
BuildRequires: python-devel
%define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

## ruby
BuildRequires:	ruby-devel >= 1.8
BuildRequires:	ruby >= 1.8
BuildRequires:	rubypick
%if "%{?ruby_libarchdir}" != ""
%define ruby_arch %{?ruby_libarchdir}
%else
%{!?ruby_arch: %define ruby_arch %(ruby -rrbconfig -e 'puts Config::CONFIG["archdir"]')}
%endif

%if "%{?ruby_libdir}" != ""
%define ruby_rubylibdir %{?ruby_libdir}
%else
%{!?ruby_rubylibdir: %define ruby_rubylibdir %(ruby -rrbconfig -e 'puts Config::CONFIG["rubylibdir"]')}
%endif

# Ruby 1.9 includes are located in strance directories ... (taken from ruby 1.9 spec file)
%global	_normalized_cpu	%(echo %{_target_cpu} | sed 's/^ppc/powerpc/;s/i.86/i386/;s/sparcv./sparc/;s/armv.*/arm/')

## java

# Others use OpenJDK
BuildRequires: java-openjdk
BuildRequires: java-devel >= 1.4.2
BuildRequires: java-1.8.0-openjdk-devel

%define java_home %{_usr}/lib/jvm/java
%define _with_java --with-java=%{java_home}

## Perl
# There is no 'perl-devel' package on RHEL5
BuildRequires:	perl-devel
%define perl_vendorarch %{expand:%%(eval `perl -V:installvendorarch`; echo $installvendorarch)}

## QScintilla
BuildRequires:	libtqscintilla-devel >= %{?tde_epoch:%{tde_epoch}:}1.7.1
%define _enable_qscintilla --enable-qscintilla

Obsoletes:	trinity-kdebindings < %{version}-%{release}
Provides:	trinity-kdebindings = %{version}-%{release}

# Metapackage requires
Requires: trinity-tdebindings-java = %{version}-%{release}
Requires: trinity-libsmoketqt = %{version}-%{release}
Requires: trinity-libsmoketde = %{version}-%{release}
Requires: perl-dcop = %{version}-%{release}
Requires: python-dcop = %{version}-%{release}
Requires: trinity-libkjsembed1 = %{version}-%{release}
Requires: trinity-kjscmd = %{version}-%{release}
Requires: trinity-juic = %{version}-%{release}
Requires: trinity-libkorundum0-ruby = %{version}-%{release}
Requires: trinity-libqt0-ruby = %{version}-%{release}


%description
TDE/DCOP bindings to non-C++ languages

%files
%defattr(-,root,root,-)

##########

%package java
Summary:	TDE Java bindings metapackage [Trinity]
Group:		System/Libraries
Requires:	trinity-libdcop3-java = %{version}-%{release}
Requires:	trinity-libdcop3-jni = %{version}-%{release}
Requires:	trinity-libqt3-java = %{version}-%{release}
Requires:	trinity-libqt3-jni = %{version}-%{release}
Requires:	trinity-libtrinity-java = %{version}-%{release}
Requires:	trinity-libtrinity-jni = %{version}-%{release}

%description java
A metapackage depending on all TDE, Qt and DCOP bindings libraries
related to the Java language.

This package is part of the official TDE bindings module.

%files java
%defattr(-,root,root,-)

##########

%package -n trinity-libdcop3-java
Summary:	DCOP bindings for Java [Trinity]
Group:		System/Libraries

Requires:	trinity-libdcop3-jni = %{version}-%{release}

%description -n trinity-libdcop3-java
This package contains the Java classes necessary to run Java programs
using the Java DCOP bindings. DCOP is the TDE Desktop COmmunications
Protocol, used for communicating with running TDE applications.

This package is part of the official TDE bindings module.

%files -n trinity-libdcop3-java
%defattr(-,root,root,-)
%{tde_libdir}/java/org/

##########

%package -n trinity-libdcop3-java-devel
Summary:	DCOP bindings for Java (dcopidl2java program) [Trinity]
Group:		Development/Languages/Java
Requires:	trinity-libdcop3-java = %{version}-%{release}

%description -n trinity-libdcop3-java-devel
This package contains the dcopidl2java program which generates Java 
stubs from DCOP IDL files, necessary to do development with the DCOP Java
bindings. DCOP is the TDE Desktop COmmunications Protocol, used for
communicating with running TDE applications.

This package is part of the official TDE bindings module.

%files -n trinity-libdcop3-java-devel
%defattr(-,root,root,-)
%{tde_bindir}/dcopidl2java

##########

%package -n trinity-libdcop3-jni
Summary:	DCOP bindings for Java ( Native libraries ) [Trinity]
Group:		System/Libraries

%description -n trinity-libdcop3-jni
This package contains the shared libraries and scripts necessary to
run programs using the Java DCOP bindings. DCOP is the TDE Desktop
COmmunications Protocol, used for communicating with running TDE
applications.

This package is part of the official TDE bindings module.

%files -n trinity-libdcop3-jni
%defattr(-,root,root,-)
%{tde_libdir}/libjavadcop.la
%{tde_libdir}/libjavadcop.so

%post -n trinity-libdcop3-jni
/sbin/ldconfig || :

%postun -n trinity-libdcop3-jni
/sbin/ldconfig || :

##########

%package -n trinity-libqt3-java
Summary:	Java bindings for Qt [Trinity]
Group:		System/Libraries
Requires:	trinity-libdcop3-jni = %{version}-%{release}
Requires:	trinity-libqt3-jni = %{version}-%{release}
Requires:	trinity-juic = %{version}-%{release}

%description -n trinity-libqt3-java
This package contains the Java classes necessary to run Java programs
using the Java Qt bindings. Qt is a very popular GUI toolkit, used by
the TDE desktop environment.

It also includes many example programs that make use of these bindings,
plus many of the Qt Tutorial examples translated into Java.

This package is part of the official TDE bindings module.

%files -n trinity-libqt3-java
%defattr(-,root,root,-)
%{tde_libdir}/java/qtjava*.jar
%{tde_tdedocdir}/HTML/en/javalib/

##########

%package -n trinity-libqt3-jni
Summary:	Java bindings for Qt ( Native libraries ) [Trinity]
Group:		System/Libraries

%description -n trinity-libqt3-jni
This package contains the shared libraries necessary to run Java
programs using the Java Qt bindings. Qt is a very popular GUI
toolkit, used by the TDE desktop environment.

This package is part of the official TDE bindings module.

%files -n trinity-libqt3-jni
%defattr(-,root,root,-)
%{tde_libdir}/libqtjavasupport.la
%{tde_libdir}/libqtjavasupport.so.*
%{tde_libdir}/jni/libqtjava.la
%{tde_libdir}/jni/libqtjava.so.*
%doc qtjava/ChangeLog

%post -n trinity-libqt3-jni
/sbin/ldconfig || :

%postun -n trinity-libqt3-jni
/sbin/ldconfig || :

##########

%package -n trinity-libqt3-jni-devel
Summary:	Development files fo Java bindings for Qt ( Native libraries ) [Trinity]
Group:		Development/Languages/Java
Requires:	trinity-libqt3-jni = %{version}-%{release}

%description -n trinity-libqt3-jni-devel
This package contains the development files for trinity-libqt3-jni.

This package is part of the official TDE bindings module.

%files -n trinity-libqt3-jni-devel
%defattr(-,root,root,-)
%{tde_libdir}/libqtjavasupport.so
%{tde_libdir}/jni/libqtjava.so

##########

%package -n trinity-libtrinity-java
Summary:	Tdelibs bindings for Java [Trinity]
Group:		System/Libraries

Requires:	trinity-libtrinity-jni = %{version}-%{release}

%description -n trinity-libtrinity-java
This package contains the Java classes necessary to run Java programs
using the Java tdelibs bindings. TDE is the Trinity Desktop Environment, a
very popular UNIX Desktop Environment.

It also includes some example applications that use these Java
classes, and multiple usage samples of the most common TDE classes.

This package is part of the official TDE bindings module.

%files -n trinity-libtrinity-java
%defattr(-,root,root,-)
%{tde_libdir}/java/koala*.jar

##########

%package -n trinity-libtrinity-jni
Summary:	Tdelibs bindings for java ( Native libraries ) [Trinity]
Group:		System/Libraries

%description -n trinity-libtrinity-jni
This package contains the shared libraries necessary to run Java
programs using the Java tdelibs bindings. TDE is the Trinity Desktop
Environment, a very popular UNIX Desktop Environment.

This package is part of the official TDE bindings module.

%files -n trinity-libtrinity-jni
%defattr(-,root,root,-)
%{tde_libdir}/jni/libtdejava.la
%{tde_libdir}/jni/libtdejava.so.*
%doc tdejava/ChangeLog

##########

%package -n trinity-libtrinity-jni-devel
Summary:	Development files for tdelibs bindings for java ( Native libraries ) [Trinity]
Group:		Development/Languages/Java
Requires:	trinity-libtrinity-jni = %{version}-%{release}

%description -n trinity-libtrinity-jni-devel
This package contains the development files for trinity-libtrinity-jni.

This package is part of the official TDE bindings module.

%files -n trinity-libtrinity-jni-devel
%defattr(-,root,root,-)
%{tde_libdir}/jni/libtdejava.so

##########

%package -n trinity-libsmoketqt
Summary:	SMOKE Binding Library to Qt
Group:		System/Libraries

Obsoletes:	trinity-libsmokeqt1 < %{version}-%{release}
Provides:	trinity-libsmokeqt1 = %{version}-%{release}

%description -n trinity-libsmoketqt
The "Scripting Meta Object Kompiler Engine" library is used by
various TDE language bindings packages to provide interfaces to the
Qt library.

This package is part of the official TDE bindings module.

%files -n trinity-libsmoketqt
%defattr(-,root,root,-)
%{tde_libdir}/libsmoketqt.so.*

%post -n trinity-libsmoketqt
/sbin/ldconfig || :

%postun -n trinity-libsmoketqt
/sbin/ldconfig || :

##########

%package -n trinity-libsmoketqt-devel
Summary:	SMOKE Binding Library to TQt - Development Files
Group:		Development/Languages/Other
Requires:	trinity-libsmoketqt = %{version}-%{release}

Obsoletes:	trinity-libsmokeqt-devel < %{version}-%{release}
Provides:	trinity-libsmokeqt-devel = %{version}-%{release}

%description -n trinity-libsmoketqt-devel
The "Scripting Meta Object Kompiler Engine" library is used by
various TDE language bindings packages to provide interfaces to the
Qt library. This package contains the development files for the
library.

If you are a normal user, you probably don't need this
package.

This package is part of the official TDE bindings module.

%files -n trinity-libsmoketqt-devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/smoke.h
%{tde_libdir}/libsmoketqt.so
%{tde_libdir}/libsmoketqt.la

%post -n trinity-libsmoketqt-devel
/sbin/ldconfig || :

%postun -n trinity-libsmoketqt-devel
/sbin/ldconfig || :

##########

%package -n trinity-libsmoketde
Summary:	SMOKE Binding Library to TDE
Group:		System/Libraries

Obsoletes:	trinity-libsmokekde1 < %{version}-%{release}
Provides:	trinity-libsmokekde1 = %{version}-%{release}

%description -n trinity-libsmoketde
The "Scripting Meta Object Kompiler Engine" library is used by
various TDE language bindings packages to provide interfaces to the
TDE libraries.

This package is part of the official TDE bindings module.

%files -n trinity-libsmoketde
%defattr(-,root,root,-)
%{tde_libdir}/libsmoketde.so.*

%post -n trinity-libsmoketde
/sbin/ldconfig || :

%postun -n trinity-libsmoketde
/sbin/ldconfig || :

##########

%package -n trinity-libsmoketde-devel
Summary:	SMOKE Binding Library to TDE - Development Files
Group:		Development/Languages/Other
Requires:	trinity-libsmoketde = %{version}-%{release}

Obsoletes:	trinity-libsmokekde-devel < %{version}-%{release}
Provides:	trinity-libsmokekde-devel = %{version}-%{release}

%description -n trinity-libsmoketde-devel
The "Scripting Meta Object Kompiler Engine" library is used by
various TDE language bindings packages to provide interfaces to the
Qt and TDE libraries. This package contains the development files for
the library.

If you are a normal user, you probably don't need this
package.

This package is part of the official TDE bindings module.

%files -n trinity-libsmoketde-devel
%defattr(-,root,root,-)
%{tde_libdir}/libsmoketde.so
%{tde_libdir}/libsmoketde.la

%post -n trinity-libsmoketde-devel
/sbin/ldconfig || :

%postun -n trinity-libsmoketde-devel
/sbin/ldconfig || :

##########

%package -n perl-dcop
Summary:	DCOP Bindings for Perl 
Group:		System/Libraries
Requires:	perl

Obsoletes:	trinity-kdebindings-dcopperl < %{version}-%{release}
Provides:	trinity-kdebindings-dcopperl = %{version}-%{release}

Obsoletes:	trinity-perl-dcop < %{version}-%{release}
Provides:	trinity-perl-dcop = %{version}-%{release}

%description -n perl-dcop
Perl bindings to the DCOP interprocess communication protocol used by TDE

%files -n perl-dcop
%defattr(-,root,root,-)
%{perl_vendorarch}/auto/DCOP/
%{perl_vendorarch}/DCOP.pm
%{perl_vendorarch}/DCOP/
%doc dcopperl/AUTHORS dcopperl/Changes dcopperl/README dcopperl/TODO
%{tde_mandir}/man3/DCOP.3pm*

##########

%package -n python-dcop
Summary:	DCOP bindings for Python
Group:		System/Libraries
Requires:	python

Obsoletes:	trinity-python-dcop < %{version}-%{release}
Provides:	trinity-python-dcop = %{version}-%{release}

%description -n python-dcop
This package contains the shared libraries necessary to run and
develop Python programs using the Python DCOP bindings
libraries. DCOP is the TDE Desktop COmmunications Protocol, used for
communicating with running TDE applications.

This package is part of the official TDE bindings module.

%files -n python-dcop
%defattr(-,root,root,-)
%{python_sitearch}/pcop.la
%{python_sitearch}/pcop.so
%{python_sitearch}/pydcop.py*

##########

%package -n trinity-libkjsembed1
Summary:	Embedded JavaScript library
Group:		System/Libraries

%description -n trinity-libkjsembed1
This package contains the shared libraries necessary to run programs
linked with the KJSEmbed library. This library provides JavaScript
embedded scripting facilities to TDE applications.

This package is part of the official TDE bindings module.

%files -n trinity-libkjsembed1
%defattr(-,root,root,-)
%{tde_libdir}/libkjsembed.so.*
%{tde_tdelibdir}/libimagefxplugin.la
%{tde_tdelibdir}/libimagefxplugin.so
%{tde_datadir}/services/imagefx_plugin.desktop
%{tde_tdelibdir}/libqprocessplugin.so
%{tde_tdelibdir}/libqprocessplugin.la
%{tde_datadir}/services/qprocess_plugin.desktop
%{tde_tdelibdir}/libfileitemplugin.la
%{tde_tdelibdir}/libfileitemplugin.so
%{tde_datadir}/services/tdefileitem_plugin.desktop
%{tde_datadir}/apps/kjsembed/
%{tde_datadir}/servicetypes/binding_type.desktop
%{tde_bindir}/embedjs
%{tde_datadir}/apps/embedjs/
%{tde_tdeappdir}/embedjs.desktop
%{tde_datadir}/icons/hicolor/16x16/apps/embedjs.png
%{tde_datadir}/icons/hicolor/32x32/apps/embedjs.png
%{tde_tdelibdir}/libjavascript.la
%{tde_tdelibdir}/libjavascript.so
%dir %{tde_datadir}/apps/kate
%dir %{tde_datadir}/apps/kate/scripts
%{tde_datadir}/apps/kate/scripts/swaptabs.js
%{tde_datadir}/apps/kate/scripts/swaptabs.ui
%{tde_datadir}/apps/kate/scripts/swaptabs.desktop
%{tde_datadir}/services/javascript.desktop
%doc kjsembed/docs/ChangeLog

%post -n trinity-libkjsembed1
/sbin/ldconfig ||:
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database >& /dev/null ||:

%postun -n trinity-libkjsembed1
/sbin/ldconfig ||:
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database >& /dev/null ||:

##########

%package -n trinity-libkjsembed-devel
Summary:	Embedded JavaScript library (Development files)
Group:		Development/Libraries/Other
Requires:	trinity-libkjsembed1 = %{version}-%{release}

%description -n trinity-libkjsembed-devel
This package contains the header files and symbolic links necessary
to develop and compile programs using the KJSEmbed library. This
library provides JavaScript embedded scripting facilities to TDE
applications.

It also includes lots of example programs that make use of these
bindings, plus comprehensive documentation of the bindings.

This package is part of the official TDE bindings module.

%files -n trinity-libkjsembed-devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/kjsembed/
%{tde_libdir}/libkjsembed.so
%{tde_libdir}/libkjsembed.la
%{tde_docdir}/trinity-libkjsembed-devel/

%post -n trinity-libkjsembed-devel
/sbin/ldconfig || :

%postun -n trinity-libkjsembed-devel
/sbin/ldconfig || :

##########

%package -n trinity-kjscmd
Summary:	A script interpreter using the TDE JavaScript library
Group:		System/Libraries

%description -n trinity-kjscmd
This package contains the kjscmd program, which is a standalone
JavaScript interpreter using the KJSEmbed library.

This package is part of the official TDE bindings module.

%files -n trinity-kjscmd
%defattr(-,root,root,-)
%{tde_bindir}/kjscmd
%{tde_tdeappdir}/kjscmd.desktop
%{tde_mandir}/man1/kjscmd.*
%{tde_tdelibdir}/libjsconsoleplugin.la
%{tde_tdelibdir}/libjsconsoleplugin.so

%post -n trinity-kjscmd
update-desktop-database >& /dev/null ||:

%postun -n trinity-kjscmd
update-desktop-database >& /dev/null ||:

##########

%package -n trinity-juic
Summary:	The Qt Java UI Compiler
Group:		Development/Languages/Java
Requires:	trinity-libqt3-java = %{version}-%{release}

%description -n trinity-juic
This package contains the juic program, which is used to convert
a UI description file generated by the Qt Designer, and converts
it into a Qt Java class. It is necessary for compiling and 
developing programs using the Qt Java bindings together with Qt
Designer.

This package is part of the official TDE bindings module.

%files -n trinity-juic
%defattr(-,root,root,-)
%{tde_bindir}/juic
%{tde_datadir}/juic/

##########

%package -n trinity-libkorundum0-ruby
Summary:	TDE bindings for Ruby [Trinity]
Group:		System/Libraries
Requires:	trinity-libqt0-ruby = %{version}-%{release}

%description -n trinity-libkorundum0-ruby
This package contains the files necessary for running and developing
Ruby code using the Korundum TDE Ruby bindings.

It also includes some example programs and templates that make use of
these bindings.

This package is part of the official TDE bindings module.

%files -n trinity-libkorundum0-ruby
%defattr(-,root,root,-)
%{tde_bindir}/rbtdesh
%{tde_bindir}/rbtdeapi
%{tde_bindir}/krubyinit
%{tde_bindir}/rbtdeconfig_compiler
%{ruby_rubylibdir}/Korundum.rb
%dir %{ruby_rubylibdir}/TDE
%{ruby_rubylibdir}/TDE/korundum.rb
%{ruby_arch}/korundum.la
%{ruby_arch}/korundum.so*
%doc korundum/ChangeLog

%post -n trinity-libkorundum0-ruby
/sbin/ldconfig || :

%postun -n trinity-libkorundum0-ruby
/sbin/ldconfig || :

##########

%package -n trinity-libqt0-ruby
Summary:	Qt bindings for Ruby [Trinity]
Group:		System/Libraries
Requires:	ruby

%description -n trinity-libqt0-ruby
This package contains the files necessary for running and developing
Ruby code using the Qt Ruby bindings.

It also includes some example programs that make use of these bindings,
plus many of the Qt Tutorial examples translated into Ruby.

This package is part of the official TDE bindings module.

%files -n trinity-libqt0-ruby
%defattr(-,root,root,-)
%{tde_bindir}/rbqtsh
%{tde_bindir}/rbqtapi
%{tde_bindir}/rbuic
%{tde_bindir}/qtrubyinit
%dir %{ruby_rubylibdir}/Qt
%{ruby_rubylibdir}/Qt/qtruby.rb
%{ruby_rubylibdir}/Qt.rb
%{ruby_arch}/qtruby.so*
%{ruby_arch}/qtruby.la
%{ruby_arch}/tqui.so*
%{ruby_arch}/tqui.la
%doc qtruby/ChangeLog

%post -n trinity-libqt0-ruby
/sbin/ldconfig || :

%postun -n trinity-libqt0-ruby
/sbin/ldconfig || :

##########

%if 0
%package -n trinity-kmozilla
Summary:	Kmozilla for TDE
Group:		System/Libraries

%description -n trinity-kmozilla
This package contains the kmozilla library fro TDE.

%files -n trinity-kmozilla
%defattr(-,root,root,-)
%{tde_bindir}/kmozilla
%{tde_libdir}/libkmozillapart.so.*
%{tde_libdir}/libkmozillapart.so
%{tde_libdir}/libkmozillapart.la
%{tde_datadir}/services/kmozilla.desktop
%endif

##########

%package -n trinity-xpart-notepad
Summary:	A small XPart editor
Group:		Productivity/Scientific/Math

%description -n trinity-xpart-notepad
xpart_notepad is a small XPart editor. Use it to understand how to use XPart.

%files -n trinity-xpart-notepad
%defattr(-,root,root,-)
%{tde_bindir}/shell_xparthost
%{tde_bindir}/xp_notepad
%{tde_libdir}/libxp_notepadpart.la
%{tde_libdir}/libxp_notepadpart.so
%{tde_libdir}/libxp_notepadpart.so.*
%{tde_datadir}/services/xp_notepad.desktop
%doc xparts/xpart_notepad/README

%post -n trinity-xpart-notepad
/sbin/ldconfig || :

%postun -n trinity-xpart-notepad
/sbin/ldconfig || :

##########

%if 0%{?with_gtk1}
%package -n trinity-libgtkxparts1
Summary:	Xparts library for GTK
Group:		Development/Languages/Other

%description -n trinity-libgtkxparts1
This package contains the xparts library for GTK.

%files -n trinity-libgtkxparts1
%defattr(-,root,root,-)
%{tde_libdir}/libgtkxparts.so.*
%{tde_libdir}/libgtkxparts.la

%post -n trinity-libgtkxparts1
/sbin/ldconfig || :

%postun -n trinity-libgtkxparts1
/sbin/ldconfig || :
%endif

##########

%package -n trinity-libtdexparts
Summary:	Xparts library for TDE
Group:		Development/Languages/Other

Obsoletes:	trinity-libkdexparts1 < %{version}-%{release}
Provides:	trinity-libkdexparts1 = %{version}-%{release}

%description -n trinity-libtdexparts
This package contains the xparts library for TDE.

%files -n trinity-libtdexparts
%defattr(-,root,root,-)
%{tde_libdir}/libtdexparts.so.*
%{tde_libdir}/libtdexparts.la

%post -n trinity-libtdexparts
/sbin/ldconfig || :

%postun -n trinity-libtdexparts
/sbin/ldconfig || :

##########

%package -n trinity-libxparts-devel
Summary:	Xparts development files
Group:		Development/Languages/Other
%if 0%{?with_gtk1}
Requires:	trinity-libgtkxparts1 = %{version}-%{release}
%endif
Requires:	trinity-libtdexparts = %{version}-%{release}

%description -n trinity-libxparts-devel
This package contains the development files for Xparts library.

%files -n trinity-libxparts-devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/xtdeparts/
%if 0%{?with_gtk1}
%{tde_libdir}/libgtkxparts.so
%endif
%{tde_libdir}/libtdexparts.so

%post -n trinity-libxparts-devel
/sbin/ldconfig || :

%postun -n trinity-libxparts-devel
/sbin/ldconfig || :

##########

%package xparts-extras
Summary:	Extra xparts for TDE [Trinity]
Group:		Development/Languages/Other

# Metapckage requires
Requires:	trinity-xpart-notepad = %{version}-%{release}
%if 0%{?with_gtk1}
Requires:	trinity-libgtkxparts1 = %{version}-%{release}
%endif
Requires:	trinity-libtdexparts = %{version}-%{release}
Requires:	trinity-libdcop-c = %{version}-%{release}

%description xparts-extras
This package contains extra xparts-based modules for Trinity
This includes the mozilla-konqueror plugin

This package is part of the official TDE bindings module.

%files xparts-extras
%defattr(-,root,root,-)

###########

%package -n trinity-libdcop-c
Summary:	DCOP bindings for C [Trinity]
Group:		System/Libraries

%description -n trinity-libdcop-c
This package contains the DCOP bindings for C.

%files -n trinity-libdcop-c
%defattr(-,root,root,-)
%{tde_libdir}/libdcopc.so.*

%post -n trinity-libdcop-c
/sbin/ldconfig || :

%postun -n trinity-libdcop-c
/sbin/ldconfig || :

###########

%package -n trinity-libdcop-c-devel
Summary:	DCOP bindings for C, development files [Trinity]
Group:		Development/Languages/C and C++
Requires:	trinity-libdcop-c = %{version}-%{release}

%description -n trinity-libdcop-c-devel
This package contains the development files for DCOP bindings for C.

%files -n trinity-libdcop-c-devel
%defattr(-,root,root,-)
%{tde_libdir}/libdcopc.so
%{tde_libdir}/libdcopc.la
%{tde_tdeincludedir}/dcopc/

%post -n trinity-libdcop-c-devel
/sbin/ldconfig || :

%postun -n trinity-libdcop-c-devel
/sbin/ldconfig || :

##########

%package devel
Summary:	Development files for %{name}
Group:		Development/Languages/Other

Requires:	trinity-tdelibs-devel >= %{tde_version}
Requires:	%{name} = %{version}-%{release}

Obsoletes:	trinity-kdebindings-devel < %{version}-%{release}
Provides:	trinity-kdebindings-devel = %{version}-%{release}

# Metapackage
Requires:	trinity-libsmoketqt-devel = %{version}-%{release}
Requires:	trinity-libdcop3-java-devel = %{version}-%{release}
Requires:	trinity-libsmoketde-devel = %{version}-%{release}
Requires:	trinity-libkjsembed-devel = %{version}-%{release}
Requires:	trinity-libxparts-devel = %{version}-%{release}
Requires:	trinity-libdcop-c-devel = %{version}-%{release}
Requires:	trinity-libqt3-jni-devel = %{version}-%{release}
Requires:	trinity-libtrinity-jni-devel = %{version}-%{release}

%description devel
This package contains the development files for the TDE bindings.

%files devel
%defattr(-,root,root,-)

##########

%prep
%setup -q -n %{name}-%{version}%{?preversion:~%{preversion}}
%patch0 -p1

%if "%{?perl_vendorarch}" == ""
exit 1
%endif

# [tdebindings] Function 'rb_frame_this_func' does not exist in RHEL4/5
%if 0%{?rhel} >= 4 && 0%{?rhel} <= 5
%__sed -i "qtruby/rubylib/qtruby/Qt.cpp" \
       -i "korundum/rubylib/korundum/Korundum.cpp" \
       -e "s|rb_frame_this_func|rb_frame_last_func|g"
%endif

# Another strange FTBFS in RHEL 5
%if 0%{?rhel} >= 4 && 0%{?rhel} <= 5
%__sed -i "xparts/xpart_notepad/shell_xparthost.cpp" \
       -i "xparts/xpart_notepad/xp_notepad.cpp" \
       -e "/TDEApplication/ s| );|, true, true, true);|"
%endif

# Disable kmozilla, it does not build with recent xulrunner (missing 'libmozjs.so')
%__sed -i "xparts/Makefile.am" \
       -e "s|SUBDIRS = .*|SUBDIRS = src xpart_notepad|"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export TDEDIR=%{tde_prefix}

unset JAVA_HOME ||:
%{?java_home:JAVA_HOME=%{java_home}; export JAVA_HOME}

# sip/PyQt/PyKDE built separately, not here
export DO_NOT_COMPILE="$DO_NOT_COMPILE python"

# Ruby headers, strange location ...
if [ -d "/usr/include/%{_normalized_cpu}-linux" ]; then
  export EXTRA_INCLUDES="/usr/include/%{_normalized_cpu}-linux"
fi

# Specific path for RHEL4
if [ -d /usr/X11R6 ]; then
  export RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -I/usr/X11R6/include -L/usr/X11R6/%{_lib}"
fi
if [ -d /usr/evolution28 ]; then
  export PATH="/usr/evolution28/bin:${PATH}"
  export PKG_CONFIG_PATH="/usr/evolution28/%{_lib}/pkgconfig:${PKG_CONFIG_PATH}"
fi

export QTINC=%{_includedir}/tqt3
export QTLIB=%{_libdir}

# Warning: GCC visibility causes FTBFS [Bug #1285]
%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --docdir=%{tde_docdir} \
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
  --disable-gcc-hidden-visibility \
  --with-qt-includes=%{_includedir}/tqt3\
  --with-extra-includes=%{_includedir}/tqscintilla:%{_includedir}/tqt3:${EXTRA_INCLUDES} \
  --with-extra-libs=%{tde_libdir} \
  --with-pythondir=%{_usr} \
  \
  %{?_with_java} %{!?_with_java:--without-java} \
  %{?_enable_qscintilla} %{!?_enable_qscintilla:--disable-qscintilla}

# Build dcopperl with specific options
pushd dcopperl
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL INSTALLDIRS=vendor

# [Bug #348] Ugly hack to modify the man pages directory
sed -i "Makefile" -e "s|/usr/share/man|%{tde_mandir}|g"

%__make OPTIMIZE="$RPM_OPT_FLAGS" ||:
popd

# smoke (not smp-safe)
%__make -C smoke

# The rest is smp-safe
%__make %{?_smp_mflags} PYTHON=%{__python}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf $RPM_BUILD_ROOT

%__make install DESTDIR=%{?buildroot} \
  PYTHON=%{__python}

# Removes some perl files
find $RPM_BUILD_ROOT -type f -a \( -name perllocal.pod -o -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'

# Installs juic
%__install -D -m 755 qtjava/designer/juic/bin/juic	%{?buildroot}%{tde_bindir}/juic
%__install -d -m 755 %{?buildroot}%{tde_datadir}/juic/common
%__install -m 644 qtjava/designer/juic/common/*.xml %{?buildroot}%{tde_datadir}/juic/common
%__install -m 644 qtjava/designer/juic/common/*.xsl %{?buildroot}%{tde_datadir}/juic/common
%__install -d -m 755 %{?buildroot}%{tde_datadir}/juic/java
%__install -m 644 qtjava/designer/juic/java/*.xml %{?buildroot}%{tde_datadir}/juic/java
%__install -m 644 qtjava/designer/juic/java/*.xsl %{?buildroot}%{tde_datadir}/juic/java
%__install -m 644 qtjava/designer/juic/juic.xsl  %{?buildroot}%{tde_datadir}/juic

# kjsembed sample files
%__install -d -m 755 %{?buildroot}%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/
%__install -m 644 kjsembed/plugins/customobject_plugin.cpp %{?buildroot}%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/
%__install -m 644 kjsembed/plugins/customobject_plugin.h %{?buildroot}%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/
%__install -m 644 kjsembed/plugins/customobject_plugin.desktop %{?buildroot}%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/
%__install -m 644 kjsembed/plugins/customqobject_plugin.cpp %{?buildroot}%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/
%__install -m 644 kjsembed/plugins/customqobject_plugin.h %{?buildroot}%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/
%__install -m 644 kjsembed/plugins/customqobject_plugin.desktop %{?buildroot}%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/

# Man installation location is wrong on RHEL4...
if [ -d "%{buildroot}%{_mandir}/man3" ]; then
  mv -f %{buildroot}%{_mandir}/man3 %{buildroot}%{tde_mandir}/man3/
  rm -rf %{buildroot}%{_mandir}
fi

# Move 'embedjs.desktop' to correct location
%__mv -f "%{?buildroot}%{tde_datadir}/applnk/Utilities/embedjs.desktop" "%{?buildroot}%{tde_tdeappdir}/embedjs.desktop"
%__rm -rf "%{?buildroot}%{tde_datadir}/applnk"

%clean
%__rm -rf $RPM_BUILD_ROOT


%changelog
* Wed Oct 07 2015 Liu Di <liudidi@gmail.com> - 14.0.1-1.opt.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 14.0.0-1
- Initial release for TDE R14.0.0
