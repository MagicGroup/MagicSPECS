# Special note for RHEL4:
#  You must create symlink 'libgcj.so' manually because it does not exist by default.
# E.g:
#  ln -s /usr/lib/libgcj.so.5.0.0 /usr/lib/jvm/java/lib/libgcj.so
# or 64 bits:
#  ln -s /usr/lib64/libgcj.so.5.0.0 /usr/lib/jvm/java/lib/libgcj.so

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

# RHEL4 specific
Source91:  filter-requires.sh
%if 0%{?rhel} == 4
%define    _use_internal_dependency_generator 0
%define    __find_requires sh %{SOURCE91}
%endif

Name:			trinity-tdebindings
Summary:		TDE bindings to non-C++ languages
Version:		3.5.13.2
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}

License:		GPLv2
Group:			User Interface/Desktops

Vendor:			Trinity Project
Packager:		Francois Andriot <francois.andriot@free.fr>
URL:			http://www.trinitydesktop.org/

Prefix:			%{tde_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		kdebindings-trinity-%{version}%{?preversion:~%{preversion}}.tar.xz

# [kdebindings] Fix FTBFS in dcopjava/bindings
Patch7:		kdebindings-3.5.13.1-fix_dcopjava_ldflags.patch

# [tdebindings] Function 'rb_frame_this_func' does not exist in RHEL5
Patch18:	kdebindings-3.5.13.1-fix_rhel5_ftbfs.patch

# 临时的解决办法，不知道原因
Source100:	libtool

BuildRequires: autoconf automake libtool m4
BuildRequires: trinity-tqtinterface-devel >= %{version}
BuildRequires: trinity-arts-devel >= %{version}
BuildRequires: trinity-tdelibs-devel >= %{version}

BuildRequires: desktop-file-utils
BuildRequires: zlib-devel
BuildRequires: perl(ExtUtils::MakeMaker)

# GTK2 support
%if 0%{?rhel} == 4
BuildRequires:	evolution28-gtk2-devel
Requires:		evolution28-gtk2
BuildRequires:	evolution28-glib2-devel
Requires:		evolution28-glib2
BuildRequires:	evolution28-cairo-devel
Requires:		evolution28-cairo
BuildRequires:	evolution28-pango-devel
Requires:		evolution28-pango
BuildRequires:	evolution28-atk-devel
Requires:		evolution28-atk
%else
BuildRequires:	gtk2-devel
%endif

# XULRUNNER support
%if 0%{?fedora} || 0%{?rhel} >= 5 || 0%{?mgaversion} || 0%{?mdkversion} || 0%{?suse_version} >= 1220
BuildRequires: xulrunner-devel
%endif
%if 0%{?suse_version} == 1140
BuildRequires: mozilla-xulrunner20-devel
%endif

# GTK1 support
%if 0%{?fedora} || 0%{?rhel}
%define with_gtk1 1
BuildRequires: glib-devel
BuildRequires: gtk+-devel
%endif
%if 0%{?mdkversion} == 201100
%define with_gtk1 1
BuildRequires: %{_lib}glib1.2-devel
BuildRequires: %{_lib}gtk+-devel
%endif

%if 0%{?mgaversion} || 0%{?mdkversion}
%if 0%{?pclinuxos}
BuildRequires:	libgdk_pixbuf2.0-devel
%else
BuildRequires:	%{_lib}gdk_pixbuf2.0-devel
%endif
%else
%if 0%{?fedora} >= 17
BuildRequires: gdk-pixbuf2-devel
%else
BuildRequires: gdk-pixbuf-devel
%endif
%endif


## Python
BuildRequires: python-devel
%define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

## ruby
BuildRequires: ruby-devel >= 1.8, ruby
%{!?ruby_arch: %define ruby_arch %(ruby -rrbconfig -e 'puts Config::CONFIG["archdir"]')}
%{!?ruby_rubylibdir: %define ruby_rubylibdir %(ruby -rrbconfig -e 'puts Config::CONFIG["rubylibdir"]')}
# Ruby 1.9 includes are located in strance directories ... (taken from ruby 1.9 spec file)
%global	_normalized_cpu	%(echo %{_target_cpu} | sed 's/^ppc/powerpc/;s/i.86/i386/;s/sparcv./sparc/;s/armv.*/arm/')

## java
%if 0%{?rhel} >= 4 && 0%{?rhel} <= 5
BuildRequires:	java-1.4.2-gcj-compat-devel
BuildRequires:	libgcj-devel
BuildRequires:	gcc-java
%endif

%if 0%{?rhel} >= 6 || 0%{?fedora} || 0%{?mdkversion} || 0%{?mgaversion} || 0%{?suse_version}

# PCLinuxOS use SUN's Java
%if 0%{?pclinuxos}
BuildRequires:	java-1.6.0-sun
BuildRequires:	java-1.6.0-sun-devel
%else

# Others use OpenJDK
BuildRequires: jdk
%if 0%{?fedora} >= 17 || 0%{?suse_version} >= 1220 || 0%{?mgaversion} >= 3
BuildRequires: jdk
%else
BuildRequires: java-1.6.0-openjdk-devel
%endif

%endif
%endif

%if 0%{?suse_version}
%define java_home %{_usr}/%{_lib}/jvm/java
%else
%if 0%{?rhel} == 4
%define java_home %{_usr}/lib/jvm/java-1.4.2-gcj-1.4.2.0
%else
%define java_home %{_usr}/java/latest
%endif
%endif
%define _with_java --with-java=%{java_home}

## Perl
# There is no 'perl-devel' package on RHEL5
%if 0%{?rhel} >= 6 || 0%{?fedora} || 0%{?mdkversion} || 0%{?mgaversion}
BuildRequires:	perl-devel
%endif
%define perl_vendorarch %{expand:%%(eval `perl -V:installvendorarch`; echo $installvendorarch)}


Obsoletes:	trinity-kdebindings < %{version}-%{release}
Provides:	trinity-kdebindings = %{version}-%{release}

# Metapackage requires
Requires: trinity-tdebindings-java = %{version}-%{release}
Requires: trinity-libsmokeqt1 = %{version}-%{release}
Requires: trinity-libsmokekde1 = %{version}-%{release}
Requires: trinity-perl-dcop = %{version}-%{release}
Requires: trinity-python-dcop = %{version}-%{release}
Requires: trinity-libkjsembed1 = %{version}-%{release}
Requires: trinity-kjscmd = %{version}-%{release}
Requires: trinity-juic = %{version}-%{release}
Requires: trinity-libkorundum0-ruby = %{version}-%{release}
Requires: trinity-libqt0-ruby = %{version}-%{release}


%description
TDE/DCOP bindings to non-C++ languages

%files

##########

%package java
Summary:	TDE Java bindings metapackage [Trinity]
Group:		Environment/Libraries
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
Group:		Environment/Libraries

Requires:	trinity-libdcop3-jni = %{version}-%{release}

%description -n trinity-libdcop3-java
This package contains the Java classes necessary to run Java programs
using the Java DCOP bindings. DCOP is the TDE Desktop COmmunications
Protocol, used for communicating with running TDE applications.

This package is part of the official TDE bindings module.

%files -n trinity-libdcop3-java
%defattr(-,root,root,-)
#%{tde_datadir}/java/dcopjava*.jar
%{tde_libdir}/java/org/kde/DCOP/*.class

##########

%package -n trinity-libdcop3-java-devel
Summary:	DCOP bindings for Java (dcopidl2java program) [Trinity]
Group:		Development/Libraries
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
Group:		Environment/Libraries

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
Group:		Environment/Libraries
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
Group:		Environment/Libraries

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

##########

%package -n trinity-libqt3-jni-devel
Summary:	Development files fo Java bindings for Qt ( Native libraries ) [Trinity]
Group:		Development/Libraries
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
Summary:	tdelibs bindings for Java [Trinity]
Group:		Environment/Libraries

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
Summary:	tdelibs bindings for java ( Native libraries ) [Trinity]
Group:		Environment/Libraries

%description -n trinity-libtrinity-jni
This package contains the shared libraries necessary to run Java
programs using the Java tdelibs bindings. TDE is the Trinity Desktop
Environment, a very popular UNIX Desktop Environment.

This package is part of the official TDE bindings module.

%files -n trinity-libtrinity-jni
%defattr(-,root,root,-)
%{tde_libdir}/jni/libkdejava.la
%{tde_libdir}/jni/libkdejava.so.*
%doc kdejava/ChangeLog

##########

%package -n trinity-libtrinity-jni-devel
Summary:	Development files for tdelibs bindings for java ( Native libraries ) [Trinity]
Group:		Development/Libraries
Requires:	trinity-libtrinity-jni = %{version}-%{release}

%description -n trinity-libtrinity-jni-devel
This package contains the development files for trinity-libtrinity-jni.

This package is part of the official TDE bindings module.

%files -n trinity-libtrinity-jni-devel
%defattr(-,root,root,-)
%{tde_libdir}/jni/libkdejava.so

##########

%package -n trinity-libsmokeqt1
Summary:	SMOKE Binding Library to Qt
Group:		Environment/Libraries

%description -n trinity-libsmokeqt1
The "Scripting Meta Object Kompiler Engine" library is used by
various TDE language bindings packages to provide interfaces to the
Qt library.

This package is part of the official TDE bindings module.

%files -n trinity-libsmokeqt1
%defattr(-,root,root,-)
%{tde_libdir}/libsmokeqt.so.*

%post -n trinity-libsmokeqt1
/sbin/ldconfig || :

%postun -n trinity-libsmokeqt1
/sbin/ldconfig || :

##########

%package -n trinity-libsmokeqt-devel
Summary:	SMOKE Binding Library to Qt - Development Files
Group:		Development/Libraries
Requires:	trinity-libsmokeqt1 = %{version}-%{release}

%description -n trinity-libsmokeqt-devel
The "Scripting Meta Object Kompiler Engine" library is used by
various TDE language bindings packages to provide interfaces to the
Qt library. This package contains the development files for the
library.

If you are a normal user, you probably don't need this
package.

This package is part of the official TDE bindings module.

%files -n trinity-libsmokeqt-devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/smoke.h
%{tde_libdir}/libsmokeqt.so
%{tde_libdir}/libsmokeqt.la

%post -n trinity-libsmokeqt-devel
/sbin/ldconfig || :

%postun -n trinity-libsmokeqt-devel
/sbin/ldconfig || :

##########

%package -n trinity-libsmokekde1
Summary:	SMOKE Binding Library to TDE
Group:		Environment/Libraries

%description -n trinity-libsmokekde1
The "Scripting Meta Object Kompiler Engine" library is used by
various TDE language bindings packages to provide interfaces to the
TDE libraries.

This package is part of the official TDE bindings module.

%files -n trinity-libsmokekde1
%defattr(-,root,root,-)
%{tde_libdir}/libsmokekde.so.*

%post -n trinity-libsmokekde1
/sbin/ldconfig || :

%postun -n trinity-libsmokekde1
/sbin/ldconfig || :

##########

%package -n trinity-libsmokekde-devel
Summary:	SMOKE Binding Library to TDE - Development Files
Group:		Development/Libraries
Requires:	trinity-libsmokekde1 = %{version}-%{release}

%description -n trinity-libsmokekde-devel
The "Scripting Meta Object Kompiler Engine" library is used by
various TDE language bindings packages to provide interfaces to the
Qt and TDE libraries. This package contains the development files for
the library.

If you are a normal user, you probably don't need this
package.

This package is part of the official TDE bindings module.

%files -n trinity-libsmokekde-devel
%defattr(-,root,root,-)
%{tde_libdir}/libsmokekde.so
%{tde_libdir}/libsmokekde.la

%post -n trinity-libsmokekde-devel
/sbin/ldconfig || :

%postun -n trinity-libsmokekde-devel
/sbin/ldconfig || :

##########

%package -n trinity-perl-dcop
Summary:	DCOP Bindings for Perl 
Group:		Development/Libraries

Obsoletes:	trinity-kdebindings-dcopperl < %{version}-%{release}
Provides:	trinity-kdebindings-dcopperl = %{version}-%{release}

%description -n trinity-perl-dcop
Perl bindings to the DCOP interprocess communication protocol used by TDE

%files -n trinity-perl-dcop
%defattr(-,root,root,-)
%{perl_vendorarch}/auto/DCOP/*
%{perl_vendorarch}/DCOP.pm
%{perl_vendorarch}/DCOP/*
%doc dcopperl/AUTHORS dcopperl/Changes dcopperl/README dcopperl/TODO
%{tde_mandir}/man3/DCOP.3pm*

##########

%package -n trinity-python-dcop
Summary:	DCOP bindings for Python
Group:		Environment/Libraries
Requires:	python
#Provides:	%{name}-dcoppython = %{version}-%{release}

%description -n trinity-python-dcop
This package contains the shared libraries necessary to run and
develop Python programs using the Python DCOP bindings
libraries. DCOP is the TDE Desktop COmmunications Protocol, used for
communicating with running TDE applications.

This package is part of the official TDE bindings module.

%files -n trinity-python-dcop
%defattr(-,root,root,-)
%{python_sitearch}/pcop.la
%{python_sitearch}/pcop.so
%{python_sitearch}/pydcop.py*

##########

%package -n trinity-libkjsembed1
Summary:	Embedded JavaScript library
Group:		Environment/Libraries

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
%{tde_datadir}/services/kfileitem_plugin.desktop
%{tde_datadir}/apps/kjsembed/cmdline.js
%{tde_datadir}/servicetypes/binding_type.desktop
%{tde_bindir}/embedjs
%{tde_datadir}/apps/embedjs/embedjsui.rc
%{tde_datadir}/applnk/Utilities/embedjs.desktop
%{tde_datadir}/icons/hicolor/16x16/apps/embedjs.png
%{tde_datadir}/icons/hicolor/32x32/apps/embedjs.png
%{tde_tdelibdir}/libjavascript.la
%{tde_tdelibdir}/libjavascript.so
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
Group:		Development/Libraries
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
%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/

%post -n trinity-libkjsembed-devel
/sbin/ldconfig || :

%postun -n trinity-libkjsembed-devel
/sbin/ldconfig || :

##########

%package -n trinity-kjscmd
Summary:	A script interpreter using the TDE JavaScript library
Group:		Environment/Libraries

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
Group:		Environment/Libraries
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
Group:		Environment/Libraries
Requires:	trinity-libqt0-ruby = %{version}-%{release}

%description -n trinity-libkorundum0-ruby
This package contains the files necessary for running and developing
Ruby code using the Korundum TDE Ruby bindings.

It also includes some example programs and templates that make use of
these bindings.

This package is part of the official TDE bindings module.

%files -n trinity-libkorundum0-ruby
%defattr(-,root,root,-)
%{tde_bindir}/rbkdesh
%{tde_bindir}/rbkdeapi
%{tde_bindir}/krubyinit
%{tde_bindir}/rbkconfig_compiler
%{ruby_rubylibdir}/Korundum.rb
%{ruby_rubylibdir}/KDE/korundum.rb
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
Group:		Environment/Libraries
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
%{ruby_rubylibdir}/Qt/qtruby.rb
%{ruby_rubylibdir}/Qt.rb
%{ruby_arch}/qtruby.so*
%{ruby_arch}/qtruby.la
%{ruby_arch}/qui.so*
%{ruby_arch}/qui.la
%doc qtruby/ChangeLog

%post -n trinity-libqt0-ruby
/sbin/ldconfig || :

%postun -n trinity-libqt0-ruby
/sbin/ldconfig || :

##########

%if 0
%package -n trinity-kmozilla
Summary:	Kmozilla for TDE
Group:		Environment/Libraries

%description -n trinity-kmozilla
%{summary}

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
Group:		Applications/Utilities

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
Group:		Environment/Libraries

%description -n trinity-libgtkxparts1
%{summary}

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

%package -n trinity-libkdexparts1
Summary:	Xparts library for KDE
Group:		Environment/Libraries

%description -n trinity-libkdexparts1
%{summary}

%files -n trinity-libkdexparts1
%defattr(-,root,root,-)
%{tde_libdir}/libkdexparts.so.*
%{tde_libdir}/libkdexparts.la

%post -n trinity-libkdexparts1
/sbin/ldconfig || :

%postun -n trinity-libkdexparts1
/sbin/ldconfig || :

##########

%package -n trinity-libxparts-devel
Summary:	Xparts development files
Group:		Development/Libraries
%if 0%{?with_gtk1}
Requires:	trinity-libgtkxparts1 = %{version}-%{release}
%endif
Requires:	trinity-libkdexparts1 = %{version}-%{release}

%description -n trinity-libxparts-devel
%{summary}

%files -n trinity-libxparts-devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/xkparts/
%if 0%{?with_gtk1}
%{tde_libdir}/libgtkxparts.so
%endif
%{tde_libdir}/libkdexparts.so

%post -n trinity-libxparts-devel
/sbin/ldconfig || :

%postun -n trinity-libxparts-devel
/sbin/ldconfig || :

##########

%package xparts-extras
Summary:	Extra xparts for TDE [Trinity]
Group:		Environment/Libraries

# Metapckage requires
Requires:	trinity-xpart-notepad = %{version}-%{release}
%if 0%{?with_gtk1}
Requires:	trinity-libgtkxparts1 = %{version}-%{release}
%endif
Requires:	trinity-libkdexparts1 = %{version}-%{release}
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
Group:		Environment/Libraries

%description -n trinity-libdcop-c
%{summary}

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
Group:		Development/Libraries
Requires:	trinity-libdcop-c = %{version}-%{release}

%description -n trinity-libdcop-c-devel
%{summary}

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
Group:		Development/Libraries
Requires:	trinity-tdelibs-devel 
Requires:	%{name} = %{version}-%{release}

Obsoletes:	trinity-kdebindings-devel < %{version}-%{release}
Provides:	trinity-kdebindings-devel = %{version}-%{release}

# Metapackage
Requires:	trinity-libsmokeqt-devel = %{version}-%{release}
Requires:	trinity-libdcop3-java-devel = %{version}-%{release}
Requires:	trinity-libsmokekde-devel = %{version}-%{release}
Requires:	trinity-libkjsembed-devel = %{version}-%{release}
Requires:	trinity-libxparts-devel = %{version}-%{release}
Requires:	trinity-libdcop-c-devel = %{version}-%{release}
Requires:	trinity-libqt3-jni-devel = %{version}-%{release}
Requires:	trinity-libtrinity-jni-devel = %{version}-%{release}

%description devel
Development files for the TDE bindings.

%files devel

##########

%if 0%{?suse_version} || 0%{?pclinuxos}
%debug_package
%endif

##########

%prep
%setup -q -n kdebindings-trinity-%{version}%{?preversion:~%{preversion}}
%patch7 -p1 -b .dcopjavaldflags

%if "%{?perl_vendorarch}" == ""
exit 1
%endif

%if 0%{?rhel} >= 4 && 0%{?rhel} <= 5
%patch18 -p1 -b .ruby
%endif

# Workarounds strange issue in MGA3
%if 0%{?mgaversion} == 3 || 0%{?pclinuxos} >= 2013
%__cp /usr/share/automake-1.13/test-driver admin/
%endif

# Disable kmozilla, it does not build with recent xulrunner (missing 'libmozjs.so')
%__sed -i "xparts/Makefile.am" \
  -e "s|SUBDIRS = .*|SUBDIRS = src xpart_notepad|"

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i "admin/acinclude.m4.in" \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR || : ; source /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

unset JAVA_HOME ||:
%{?java_home:JAVA_HOME=%{java_home}; export JAVA_HOME}

# sip/PyQt/PyKDE built separately, not here
export DO_NOT_COMPILE="$DO_NOT_COMPILE python"

# Specific path for RHEL4
if [ -d /usr/X11R6 ]; then
  export CXXFLAGS="${RPM_OPT_FLAGS} -I/usr/X11R6/include -L/usr/X11R6/%{_lib}"
fi
if [ -d /usr/evolution28 ]; then
  export PATH="/usr/evolution28/bin:${PATH}"
  export PKG_CONFIG_PATH="/usr/evolution28/%{_lib}/pkgconfig:${PKG_CONFIG_PATH}"
fi

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --docdir=%{tde_docdir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --disable-rpath \
  --enable-new-ldflags \
  --disable-debug --disable-warnings \
  --disable-dependency-tracking \
  --with-extra-libs=%{tde_libdir} \
  --with-pythondir=%{_usr} \
  --enable-closure \
  --enable-final \
  %{?_with_java} %{!?_with_java:--without-java} \
  %{?_enable_qscintilla} %{!?_enable_qscintilla:--disable-qscintilla} \
  --with-extra-includes=%{tde_includedir}/tqt

pushd dcopperl
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL INSTALLDIRS=vendor

# Ugly hack to add TQT include directory in Makefile
# Also modifies the man pages directory
sed -i Makefile \
  -e "s|^\(INC = .*\)|\1 -I%{tde_includedir}/tqt|" \
  -e "s|/usr/share/man|%{tde_mandir}|g"

%__make OPTIMIZE="$RPM_OPT_FLAGS" ||:
popd

# smoke (not smp-safe)
%__make -C smoke

# The rest is smp-safe
%__make %{?_smp_mflags} PYTHON=%{__python}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf $RPM_BUILD_ROOT

cp %{SOURCE100} . -f

%__make install DESTDIR=%{?buildroot} \
  PYTHON=%{__python}

# Removes some perl files
find $RPM_BUILD_ROOT -type f -a \( -name perllocal.pod -o -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'

# locale's
%find_lang %{name} || touch %{name}.lang
HTML_DIR=$(kde-config --expandvars --install html)
if [ -d $RPM_BUILD_ROOT$HTML_DIR ]; then
for lang_dir in $RPM_BUILD_ROOT$HTML_DIR/* ; do
  if [ -d $lang_dir ]; then
    lang=$(basename $lang_dir)
    echo "%lang($lang) $HTML_DIR/$lang/*" >> %{name}.lang
    # replace absolute symlinks with relative ones
    pushd $lang_dir
      for i in *; do
        [ -d $i -a -L $i/common ] && ln -nsf ../common $i/common
      done
    popd
  fi
done  
fi  

# Installs juic
%__install -D -m 755 qtjava/designer/juic/bin/juic	%{?buildroot}%{tde_bindir}/juic
%__install -d -m 755 %{?buildroot}%{tde_datadir}/juic/common
%__install qtjava/designer/juic/common/*.xml %{?buildroot}%{tde_datadir}/juic/common
%__install qtjava/designer/juic/common/*.xsl %{?buildroot}%{tde_datadir}/juic/common
%__install -d -m 755 %{?buildroot}%{tde_datadir}/juic/java
%__install qtjava/designer/juic/java/*.xml %{?buildroot}%{tde_datadir}/juic/java
%__install qtjava/designer/juic/java/*.xsl %{?buildroot}%{tde_datadir}/juic/java
%__install qtjava/designer/juic/juic.xsl  %{?buildroot}%{tde_datadir}/juic

# kjsembed sample files
%__install -d -m 755 %{?buildroot}%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/
%__install kjsembed/plugins/customobject_plugin.cpp %{?buildroot}%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/
%__install kjsembed/plugins/customobject_plugin.h %{?buildroot}%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/
%__install kjsembed/plugins/customobject_plugin.desktop %{?buildroot}%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/
%__install kjsembed/plugins/customqobject_plugin.cpp %{?buildroot}%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/
%__install kjsembed/plugins/customqobject_plugin.h %{?buildroot}%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/
%__install kjsembed/plugins/customqobject_plugin.desktop %{?buildroot}%{tde_docdir}/trinity-libkjsembed-devel/plugin-examples/customobject/


# Man installation location is wrong on RHEL4...
if [ -d "%{buildroot}%{_mandir}/man3" ]; then
  mv -f %{buildroot}%{_mandir}/man3 %{buildroot}%{tde_mandir}/man3/
  rm -rf %{buildroot}%{_mandir}
fi


%clean
%__rm -rf $RPM_BUILD_ROOT


%changelog
* Mon Jun 03 2013 Francois Andriot <francois.andriot@free.fr> - 3.5.13.2-1
- Initial release for TDE 3.5.13.2
