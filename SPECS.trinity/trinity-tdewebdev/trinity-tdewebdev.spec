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

Name:		trinity-tdewebdev
Version:	3.5.13.2
Release:	1%{?dist}%{?_variant}
License:	GPL
Summary:	Web development applications 
Group:		Applications/Editors

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	kdewebdev-trinity-%{version}.tar.xz
Source1:	http://download.sourceforge.net/quanta/css.tar.bz2
Source2:	http://download.sourceforge.net/quanta/html.tar.bz2
Source3:	http://download.sourceforge.net/quanta/php_manual_en_20030401.tar.bz2
Source4:	http://download.sourceforge.net/quanta/javascript.tar.bz2
Source5:	hi48-app-kxsldbg.png

Patch1:		kdewebdev-3.5.4-kxsldbg-icons.patch

BuildRequires:	autoconf automake libtool m4
BuildRequires:	desktop-file-utils
BuildRequires:	trinity-tdelibs-devel >= %{version}
BuildRequires:	trinity-tdesdk-devel >= %{version}
BuildRequires:	libxslt-devel
BuildRequires:	libxml2-devel
%if 0%{?rhel} == 4
# a bogus dep in libexslt.la file from EL-4 (WONTFIX bug http://bugzilla.redhat.com/142241)
BuildRequires:	libgcrypt-devel
%endif
BuildRequires:	perl

# KXSLDBG requires libxml2
#if 0%{?mgaversion} || 0%{?mdkversion} || 0%{?rhel} >= 5 || ( 0%{?fedora} > 0 && %{?fedora} <= 17 ) || 0%{?suse_version}
%define build_kxsldbg 1
#endif


Obsoletes:	trinity-kdewebdev-libs < %{version}-%{release}
Provides:	trinity-kdewebdev-libs = %{version}-%{release}
Obsoletes:	trinity-kdewebdev < %{version}-%{release}
Provides:	trinity-kdewebdev = %{version}-%{release}

Requires: trinity-quanta = %{version}-%{release}
Requires: trinity-quanta-data = %{version}-%{release}
Requires: trinity-kfilereplace = %{version}-%{release}
Requires: trinity-kimagemapeditor = %{version}-%{release}
Requires: trinity-klinkstatus = %{version}-%{release}
Requires: trinity-kommander = %{version}-%{release}
%{?build_kxsldbg:Requires: trinity-kxsldbg = %{version}-%{release}}

%description
%{summary}, including:
* kfilereplace: batch search and replace tool
* kimagemapeditor: HTML image map editor
* klinkstatus: link checker
* kommander: visual dialog building tool
* quanta+: web development
%{?build_kxsldbg:* kxsldbg: xslt Debugger}

%files

##########

%package -n trinity-quanta
Summary:	web development environment for KDE [Trinity]
Group:		Applications/Development
Requires:	trinity-kfilereplace = %{version}-%{release}
Requires:	trinity-klinkstatus = %{version}-%{release}
Requires:	trinity-kommander = %{version}-%{release}
Requires:	trinity-quanta-data = %{version}-%{release}
#Requires:	trinity-kimagemapeditor = %{version}-%{release}
#Requires:	trinity-kxsldbg = %{version}-%{release}
Requires:	tidy

%description -n trinity-quanta
Quanta Plus is a web development environment for working with HTML
and associated languages. It strives to be neutral and transparent
to all markup languages, while supporting popular web-based scripting
languages, CSS and other emerging W3C recommendations.

Quanta Plus supports many external components, debuggers and other tools
for web development, several of which are shipped with the KDE web
development module.

Quanta Plus is not in any way affiliated with any commercial versions
of Quanta. The primary coders from the original team left the GPL'd
version to produce a commercial product.

This package is part of TDE, as a component of the TDE web development module.

%files -n trinity-quanta
%defattr(-,root,root,-)
%{tde_bindir}/quanta
%{tde_tdelibdir}/quantadebuggerdbgp.la
%{tde_tdelibdir}/quantadebuggerdbgp.so
%{tde_tdelibdir}/quantadebuggergubed.la
%{tde_tdelibdir}/quantadebuggergubed.so
%{tde_tdeappdir}/quanta.desktop
%{tde_datadir}/apps/kafkapart
%{tde_datadir}/icons/hicolor/*/apps/quanta.png
%{tde_datadir}/mimelnk/application/x-webprj.desktop
%{tde_datadir}/services/quantadebuggerdbgp.desktop
%{tde_datadir}/services/quantadebuggergubed.desktop
%{tde_datadir}/services/quanta_preview_config.desktop
%{tde_datadir}/servicetypes/quantadebugger.desktop
%{tde_tdedocdir}/HTML/en/quanta/

%post -n trinity-quanta
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-quanta
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :


##########

%package -n trinity-quanta-data
Summary:	data files for Quanta Plus web development environment [Trinity]
Group:		Applications/Development

%description -n trinity-quanta-data
This package contains architecture-independent data files for Quanta
Plus, a web development environment for working with HTML and associated
languages.

See the quanta package for further information.

This package is part of TDE, as a component of the TDE web development module.

%files -n trinity-quanta-data
%defattr(-,root,root,-)
%{tde_datadir}/apps/quanta/

##########

%package -n trinity-kfilereplace
Summary:	batch search-and-replace component for KDE [Trinity]
Group:		Applications/Development

%description -n trinity-kfilereplace
KFileReplace is an embedded component for KDE that acts as a batch
search-and-replace tool. It allows you to replace one expression with
another in many files at once.

Note that at the moment KFileReplace does not come as a standalone
application. An example of an application that uses the KFileReplace
component is Quanta Plus (found in the package quanta).

This package is part of TDE, as a component of the TDE web development module.

%files -n trinity-kfilereplace
%defattr(-,root,root,-)
%{tde_bindir}/kfilereplace
%{tde_tdelibdir}/libkfilereplacepart.la
%{tde_tdelibdir}/libkfilereplacepart.so
%{tde_tdeappdir}/kfilereplace.desktop
%{tde_datadir}/apps/kfilereplace/kfilereplaceui.rc
%{tde_datadir}/apps/kfilereplacepart
%{tde_datadir}/icons/hicolor/*/apps/kfilereplace.png
%{tde_datadir}/services/kfilereplacepart.desktop
%{tde_tdedocdir}/HTML/en/kfilereplace/

%post -n trinity-kfilereplace
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kfilereplace
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kimagemapeditor
Summary:	HTML image map editor for KDE [Trinity]
Group:		Applications/Development

%description -n trinity-kimagemapeditor
KImageMapEditor is a tool that allows you to edit image maps in HTML
files. As well as providing a standalone application, KImageMapEditor
makes itself available as a KPart for embedding into larger applications.

This package is part of TDE, as a component of the TDE web development module.

%files -n trinity-kimagemapeditor
%defattr(-,root,root,-)
%{tde_bindir}/kimagemapeditor
%{tde_tdelibdir}/libkimagemapeditor.la
%{tde_tdelibdir}/libkimagemapeditor.so
%{tde_tdeappdir}/kimagemapeditor.desktop
%{tde_datadir}/apps/kimagemapeditor/
%{tde_datadir}/icons/hicolor/*/apps/kimagemapeditor.png
%{tde_datadir}/icons/locolor/*/apps/kimagemapeditor.png
%{tde_datadir}/services/kimagemapeditorpart.desktop

%post -n trinity-kimagemapeditor
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kimagemapeditor
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-klinkstatus
Summary:	web link validity checker for KDE [Trinity]
Group:		Applications/Development

%description -n trinity-klinkstatus
KLinkStatus is KDE's web link validity checker. It allows you to
search internal and external links throughout your web site. Simply
point it to a single page and choose the depth to search.

You can also check local files, or files over ftp:, fish: or any other
KIO protocols. For performance, links can be checked simultaneously.

This package is part of TDE, as a component of the TDE web development module.

%files -n trinity-klinkstatus
%defattr(-,root,root,-)
%{tde_bindir}/klinkstatus
%{tde_tdelibdir}/libklinkstatuspart.la
%{tde_tdelibdir}/libklinkstatuspart.so
%{tde_tdeappdir}/klinkstatus.desktop
%{tde_datadir}/apps/klinkstatus/
%{tde_datadir}/apps/klinkstatuspart/
%{tde_datadir}/config.kcfg/klinkstatus.kcfg
%{tde_datadir}/icons/crystalsvg/16x16/actions/bug.png
%{tde_datadir}/icons/hicolor/*/apps/klinkstatus.png
%{tde_datadir}/services/klinkstatus_part.desktop
%{tde_tdedocdir}/HTML/en/klinkstatus/

%post -n trinity-klinkstatus
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-klinkstatus
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kommander
Summary:	visual dialog builder and executor tool [Trinity]
Group:		Applications/Development
Requires:	gettext

%description -n trinity-kommander
Kommander is a visual dialog building tool whose primary objective is
to create as much functionality as possible without using any scripting
language.

More specifically, Kommander is a set of tools that allow you to create
dynamic GUI dialogs that generate, based on their state, a piece of
text. The piece of text can be a command line to a program, any piece
of code, business documents that contain a lot of repetitious or
templated text and so on.

The resulting generated text can then be executed as a command line
program (hence the name "Kommander"), written to a file, passed to a
script for extended processing, and literally anything else you can
think of. And you aren't required to write a single line of code!

As well as building dialogs, Kommander may be expanded to create full
mainwindow applications.

This package is part of TDE, as a component of the TDE web development module.

%files -n trinity-kommander
%defattr(-,root,root,-)
%{tde_bindir}/kmdr-editor
%{tde_bindir}/kmdr-executor
%{tde_bindir}/kmdr-plugins
%{tde_libdir}/libkommanderplugin.so.*
%{tde_libdir}/libkommanderwidgets.la
%{tde_libdir}/libkommanderwidget.so.*
%{tde_libdir}/libkommanderwidgets.so.*
%{tde_tdeappdir}/kmdr-editor.desktop
%{tde_datadir}/applnk/.hidden/kmdr-executor.desktop
%{tde_datadir}/apps/katepart/syntax/kommander.xml
%{tde_tdedocdir}/HTML/en/kommander/
%{tde_datadir}/icons/crystalsvg/*/apps/kommander.png
%{tde_datadir}/mimelnk/application/x-kommander.desktop
#kommander/examples /opt/trinity/share/doc/kommander
#kommander/working/extractkmdr /opt/trinity/bin
#kommander/working/kmdr2po /opt/trinity/bin
%{tde_tdelibdir}/libkommander_part.so
%{tde_tdelibdir}/libkommander_part.la
%{tde_datadir}/apps/kommander/
%{tde_datadir}/apps/kmdr-editor/editor/
%{tde_datadir}/apps/katepart/syntax/kommander-new.xml
%{tde_datadir}/apps/kdevappwizard/kommanderplugin.png
%{tde_datadir}/apps/kdevappwizard/kommanderplugin.tar.gz
%{tde_datadir}/apps/kdevappwizard/templates/kommanderplugin.kdevtemplate
%{tde_datadir}/services/kommander_part.desktop

%post -n trinity-kommander
/sbin/ldconfig || :
for f in crystalsvg ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kommander
/sbin/ldconfig || :
for f in crystalsvg ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kommander-devel
Summary:	development files for Kommander [Trinity]
Group:		Development/Libraries
Requires:	trinity-kommander = %{version}-%{release}

%description -n trinity-kommander-devel
This package contains the headers and other development files for
building plugins or otherwise extending Kommander.

Kommander is a visual dialog building tool whose primary objective is
to create as much functionality as possible without using any scripting
language.

See the kommander package for further information.

This package is part of TDE, as a component of the TDE web development module.

%files -n trinity-kommander-devel
%defattr(-,root,root,-)
%{tde_libdir}/libkommanderplugin.la
%{tde_libdir}/libkommanderplugin.so
%{tde_libdir}/libkommanderwidget.la
%{tde_libdir}/libkommanderwidget.so
%{tde_libdir}/libkommanderwidgets.so
%{tde_tdeincludedir}/kommander*
%{tde_tdeincludedir}/specials.h

%post -n trinity-kommander-devel
/sbin/ldconfig || :

%postun -n trinity-kommander-devel
/sbin/ldconfig || :

##########

%if 0%{?build_kxsldbg}

%package -n trinity-kxsldbg
Summary:	graphical XSLT debugger for KDE [Trinity]
Group:		Applications/Development

%description -n trinity-kxsldbg
KXSLDbg is a debugger for XSLT scripts. It includes a graphical user
interface as well as a text-based debugger. KXSLDbg can be run as a
standalone application or as an embedded KDE part.

XSLT is an XML language for defining transformations of XML files from
XML to some other arbitrary format, such as XML, HTML, plain text, etc.,
using standard XSLT stylesheets.

This package is part of TDE, as a component of the TDE web development module.

%files -n trinity-kxsldbg
%defattr(-,root,root,-)
%{tde_bindir}/kxsldbg
%{tde_bindir}/xsldbg
%{tde_tdelibdir}/libkxsldbgpart.la
%{tde_tdelibdir}/libkxsldbgpart.so
%{tde_tdeappdir}/kxsldbg.desktop
%{tde_datadir}/apps/kxsldbg
%{tde_datadir}/apps/kxsldbgpart
%{tde_tdedocdir}/HTML/en/kxsldbg/
%{tde_tdedocdir}/HTML/en/xsldbg/
%{tde_datadir}/icons/hicolor/*/actions/1downarrow.png
%{tde_datadir}/icons/hicolor/*/actions/configure.png
%{tde_datadir}/icons/hicolor/*/actions/exit.png
%{tde_datadir}/icons/hicolor/*/actions/hash.png
%{tde_datadir}/icons/hicolor/*/actions/mark.png
%{tde_datadir}/icons/hicolor/*/actions/next.png
%{tde_datadir}/icons/hicolor/*/actions/run.png
%{tde_datadir}/icons/hicolor/*/actions/step.png
%{tde_datadir}/icons/hicolor/*/actions/xsldbg_*.png
%{tde_datadir}/icons/hicolor/*/apps/kxsldbg.png
%{tde_datadir}/icons/locolor/*/apps/kxsldbg.png
%{tde_datadir}/services/kxsldbg_part.desktop

%post -n trinity-kxsldbg
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kxsldbg
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%endif

##########

%package devel
Group: Development/Libraries
Summary:	Header files and documentation for %{name} 

Obsoletes:	trinity-kdewebdev-devel < %{version}-%{release}
Provides:	trinity-kdewebdev-devel = %{version}-%{release}

Requires:	trinity-tdelibs-devel
Requires:	trinity-kommander-devel = %{version}-%{release}

%description devel
%{summary}.

%files devel

##########

%if 0%{?suse_version} || 0%{?pclinuxos}
%debug_package
%endif

##########

%prep
%setup -q -n kdewebdev-trinity-%{version} -a 1 -a 2 -a 3 -a 4
%patch1 -p1 -b .kxsldbg-icons

%__install -m644 -p %{SOURCE5} kxsldbg/
%if 0%{?build_kxsldbg} == 0
%__rm -rf kxsldbg/ doc/kxsldbg/ doc/xsldbg/
%endif

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

# Do not build against any "/usr" installed KDE
export KDEDIR="%{tde_prefix}"

# Specific path for RHEL4
if [ -d "/usr/X11R6" ]; then
  export CXXFLAGS="${RPM_OPT_FLAGS} -I/usr/X11R6/include -L/usr/X11R6/%{_lib}"
fi

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --includedir=%{tde_tdeincludedir} \
  --disable-rpath \
  --enable-new-ldflags \
  --enable-closure \
  --disable-debug --disable-warnings \
  --disable-dependancy-tracking --enable-final \
  --with-extra-includes=%{tde_includedir}/tqt \

# WTF hack for RHEL4
%if 0%{?rhel} == 4
mkdir  kommander/plugin/.libs/
ln -s . kommander/plugin/.libs/.libs
%endif

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{?buildroot}
%__make install DESTDIR=%{?buildroot}


## package separately?  Why doesn't upstream include this? -- Rex
# install docs
for i in css html javascript ; do
   pushd $i
   ./install.sh <<EOF
%{buildroot}%{tde_datadir}/apps/quanta/doc
EOF
   popd
   rm -rf $i
done
cp -a php php.docrc %{buildroot}%{tde_datadir}/apps/quanta/doc/

# make symlinks relative
pushd %{buildroot}%{tde_tdedocdir}/HTML/en
for i in *; do
   if [ -d $i -a -L $i/common ]; then
      rm -f $i/common
      ln -nfs ../common $i
   fi
done
popd



%clean
%__rm -rf %{buildroot}


%changelog
* Mon Jun 03 2013 Francois Andriot <francois.andriot@free.fr> - 3.5.13.2-1
- Initial release for TDE 3.5.13.2
