#需要换成 tde 的。
%define with_kde3 0

Name:		gambas2
Summary:	IDE based on a basic interpreter with object extensions
Version:	2.24.0
Release:	7%{?dist}
License:	GPL+
Group:		Development/Tools
URL:		http://gambas.sourceforge.net/
Source0:	http://downloads.sourceforge.net/gambas/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if 0%{?with_kde3}
BuildRequires:	kdelibs3-devel 
%endif
BuildRequires:  automake, autoconf, SDL-devel, SDL_mixer-devel
BuildRequires:	mysql-devel, postgresql-devel, gtk2-devel 
BuildRequires:	desktop-file-utils, gettext-devel, curl-devel, librsvg2-devel
BuildRequires:	poppler-glib-devel, bzip2-devel, zlib-devel, pkgconfig
BuildRequires:	unixODBC-devel, libXtst-devel, sqlite-devel, mesa-libGL-devel
BuildRequires:	mesa-libGLU-devel, libpng-devel, libjpeg-devel, libxml2-devel
BuildRequires:	libxslt-devel, pcre-devel, SDL_image-devel, libICE-devel
BuildRequires:	libXcursor-devel, libXft-devel, libtool-ltdl-devel
BuildRequires:	xdg-utils, glibc-devel, libffi-devel, firebird-devel
BuildRequires:	libtool
# We need this since linux/videodev.h is dead
BuildRequires:	libv4l-devel
# Code is not endian clean.
ExclusiveArch:	%{ix86} x86_64 %{arm} mips64el
Patch1:		%{name}-2.0.0-nolintl.patch
Patch2:		%{name}-2.0.0-noliconv.patch
# Support poppler 0.20
Patch3:		gambas2-2.24.0-poppler20.patch
# Use libv4l1
Patch4:		gambas2-2.23.1-use-libv4l1.patch

%description
Gambas2 is a free development environment based on a Basic interpreter
with object extensions, like Visual Basic (but it is NOT a clone !).
With Gambas2, you can quickly design your program GUI, access MySQL or
PostgreSQL databases, pilot KDE applications with DCOP, translate your
program into many languages, create network applications easily, and so
on...

%package runtime
Summary:	Runtime environment for Gambas2
Group:		Development/Tools

%description runtime
Gambas2 is a free development environment based on a Basic interpreter
with object extensions, like Visual Basic. This package contains the 
runtime components necessary to run programs designed in Gambas2. 

%package devel
Summary:	Development environment for Gambas2
Group:		Development/Tools

%description devel
The gambas2-devel package contains the tools needed to compile Gambas2
projects without having to install the complete development environment
(gambas2-ide).

%package script
Summary:	Scripter program that allows the creation of Gambas2 scripts
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}

%description script
This package includes the scripter program that allows the user to 
write script files in Gambas. 

%package ide
Summary:	The complete Gambas2 Development Environment
Group:		Development/Tools
License:	GPL+
Provides:	%{name} = %{version}-%{release}
Requires:	tar, gzip, rpm-build, gettext
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-script = %{version}-%{release}
Requires:	%{name}-gb-chart = %{version}-%{release}
Requires:	%{name}-gb-compress = %{version}-%{release}
Requires: 	%{name}-gb-crypt = %{version}-%{release}
Requires:	%{name}-gb-db = %{version}-%{release}
Requires:	%{name}-gb-db-firebird = %{version}-%{release}
Requires:	%{name}-gb-db-form = %{version}-%{release}
Requires:	%{name}-gb-db-mysql = %{version}-%{release}
Requires:	%{name}-gb-db-odbc = %{version}-%{release}
Requires:	%{name}-gb-db-postgresql = %{version}-%{release}
Requires:	%{name}-gb-db-sqlite3 = %{version}-%{release}
Requires:	%{name}-gb-desktop = %{version}-%{release}
Requires:	%{name}-gb-form = %{version}-%{release}
Requires:	%{name}-gb-form-dialog = %{version}-%{release}
Requires:	%{name}-gb-form-mdi = %{version}-%{release}
Requires:	%{name}-gb-gtk = %{version}-%{release}
Requires:	%{name}-gb-gtk-ext = %{version}-%{release}
Requires:	%{name}-gb-gtk-svg = %{version}-%{release}
Requires:	%{name}-gb-gui = %{version}-%{release}
Requires: 	%{name}-gb-image = %{version}-%{release}
Requires:	%{name}-gb-info = %{version}-%{release}
Requires:	%{name}-gb-net-curl = %{version}-%{release}
Requires:	%{name}-gb-net-smtp = %{version}-%{release}
Requires: 	%{name}-gb-net = %{version}-%{release}
Requires:	%{name}-gb-opengl = %{version}-%{release}
Requires:	%{name}-gb-option = %{version}-%{release}
Requires:	%{name}-gb-pcre = %{version}-%{release}
Requires:	%{name}-gb-pdf = %{version}-%{release}
Requires:	%{name}-gb-qt = %{version}-%{release}
Requires:	%{name}-gb-qt-ext = %{version}-%{release}
%if 0%{with_kde3}
Requires:	%{name}-gb-qt-kde = %{version}-%{release}
Requires:	%{name}-gb-qt-kde-html = %{version}-%{release}
%endif
Requires:	%{name}-gb-qt-opengl = %{version}-%{release}
Requires:	%{name}-gb-report = %{version}-%{release}
Requires:	%{name}-gb-sdl = %{version}-%{release}
Requires:	%{name}-gb-sdl-sound = %{version}-%{release}
Requires:	%{name}-gb-settings = %{version}-%{release}
Requires:	%{name}-gb-v4l = %{version}-%{release}
Requires:	%{name}-gb-vb = %{version}-%{release}
Requires:	%{name}-gb-web = %{version}-%{release}
Requires:	%{name}-gb-xml = %{version}-%{release}
Requires:	%{name}-gb-xml-rpc = %{version}-%{release}
Requires:	%{name}-gb-xml-xslt = %{version}-%{release}
# No better place to put this
Provides:	%{name}-gb-ldap = %{version}-%{release}
Obsoletes:	%{name}-gb-ldap = %{version}-%{release}

%description ide
This package includes the complete Gambas2 Development Environment and the 
database manager. Installing this package will give you all of the Gambas2 
components.

%package examples
Summary: 	Example projects provided with Gambas2
Group:   	Development/Tools
# Some of the examples are GPLv2+
# Database/PictureDatabase
# Games/RobotFindsKitten
# OpenGL/GambasGears
# Printing/Printing
# Everything else is GPL+
License: 	GPL+ and GPLv2+
# Since gambas2-ide requires every other subpackage, this is all we need here.
Requires:	%{name}-ide = %{version}-%{release}

%description examples
This package includes all the example projects provided with Gambas2.

%package help
Summary:	Help files provided with Gambas2
Group:		Development/Tools
# The tree help scripts are also GPLv2+
# Everything else is GPL+
License:	GPL+ and GPLv2+
Requires:	%{name}-ide = %{version}-%{release}

%description help
This package includes the help files generated from the Gambas2 wiki.

%package gb-chart
Summary:	Gambas2 component package for chart
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-chart
%{summary}

%package gb-compress
Summary:	Gambas2 component package for compress
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-compress
%{summary}

%package gb-crypt
Summary:	Gambas2 component package for crypt
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-crypt
%{summary}

%package gb-db
Summary:	Gambas2 component package for db
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-db
%{summary}

%package gb-db-firebird
Summary:	Gambas2 component package for db-firebird
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-db-firebird
%{summary}

%package gb-db-form
Summary:	Gambas2 component package for db-form
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-db-form
%{summary}

%package gb-db-mysql
Summary:	Gambas2 component package for db-mysql
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-db-mysql
%{summary}

%package gb-db-odbc
Summary:	Gambas2 component package for db-odbc
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-db-odbc
%{summary}

%package gb-db-postgresql
Summary:	Gambas2 component package for db-postgresql
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-db-postgresql
%{summary}

%package gb-db-sqlite3
Summary:	Gambas2 component package for db-sqlite3
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-db-sqlite3
%{summary}

%package gb-desktop
Summary:	Gambas2 component package for desktop
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-desktop
%{summary}

%package gb-form
Summary:	Gambas2 component package for form
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-form
%{summary}

%package gb-form-dialog
Summary:	Gambas2 component package for form-dialog
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-form-dialog
%{summary}

%package gb-form-mdi
Summary:	Gambas2 component package for form-mdi
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-form-mdi
%{summary}

%package gb-gtk
Summary:	Gambas2 component package for gtk
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-gtk
%{summary}

%package gb-gtk-ext
Summary:	Gambas2 component package for gtk-ext 
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-gtk-ext
%{summary}

%package gb-gtk-svg
Summary:	Gambas2 component package for gtk-svg
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-gtk-svg
%{summary}

%package gb-gui
Summary:	Gambas2 component package for gui
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-gui
%{summary}

%package gb-image 
Summary:	Gambas2 component package for image 
License:	GPLv2 or QPL
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-image 
%{summary}

%package gb-info
Summary:	Gambas2 component package for info
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-info
%{summary}

%package gb-net
Summary:	Gambas2 component package for net
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-net
%{summary}

%package gb-net-curl
Summary:	Gambas2 component package for net.curl
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-net-curl
%{summary}

%package gb-net-smtp 
Summary:	Gambas2 component package for net-smtp 
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-net-smtp
%{summary}

%package gb-opengl 
Summary:	Gambas2 component package for opengl 
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-opengl 
%{summary}

%package gb-option
Summary:	Gambas2 component package for option
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-option
%{summary}

%package gb-pcre 
Summary:	Gambas2 component package for pcre 
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-pcre 
%{summary}

%package gb-pdf
Summary:	Gambas2 component package for pdf
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-pdf
%{summary}

%package gb-qt
Summary:	Gambas2 component package for qt
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-qt
%{summary}

%package gb-qt-ext
Summary:	Gambas2 component package for qt.ext
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-qt-ext
%{summary}

%if 0%{?with_kde3}
%package gb-qt-kde
Summary:	Gambas2 component package for qt.kde
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-qt-kde
%{summary}

%package gb-qt-kde-html
Summary:	Gambas2 component package for qt.kde.html
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-qt-kde-html
%{summary}
%endif

%package gb-qt-opengl 
Summary:	Gambas2 component package for qt-opengl 
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-qt-opengl
%{summary}

%package gb-report
Summary:	Gambas2 component package for report
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-report
%{summary}

%package gb-sdl
Summary:	Gambas2 component package for sdl
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-sdl
%{summary}

%package gb-sdl-sound
Summary:	Gambas2 component package for sdl-sound
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-sdl-sound
%{summary}

%package gb-settings
Summary:	Gambas2 component package for settings
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-settings
%{summary}

%package gb-v4l 
Summary:	Gambas2 component package for v4l 
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-v4l 
%{summary}

%package gb-vb
Summary:	Gambas2 component package for vb
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-vb
%{summary}

%package gb-web
Summary:	Gambas2 component package for web
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-web
%{summary}

%package gb-xml
Summary:	Gambas2 component package for xml
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-xml
%{summary}

%package gb-xml-rpc
Summary:	Gambas2 component package for xml.rpc
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-xml-rpc
%{summary}

%package gb-xml-xslt
Summary:	Gambas2 component package for xml.xslt
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-xml-xslt
%{summary}

%prep
%setup -q
%patch1 -p1 -b .nolintl
%patch2 -p1 -b .noliconv
%patch3 -p1 -b .poppler20
%patch4 -p1 -b .libv4l1
# We used to patch these out, but this is simpler.
for i in `find . |grep acinclude.m4`; do
        sed -i 's|$AM_CFLAGS -O3|$AM_CFLAGS|g' $i
        sed -i 's|$AM_CXXFLAGS -Os -fno-omit-frame-pointer|$AM_CXXFLAGS|g' $i
        sed -i 's|$AM_CFLAGS -Os|$AM_CFLAGS|g' $i
        sed -i 's|$AM_CFLAGS -O0|$AM_CFLAGS|g' $i
        sed -i 's|$AM_CXXFLAGS -O0|$AM_CXXFLAGS|g' $i
done
# Need this for gcc44
sed -i 's|-fno-exceptions||g' gb.db.sqlite3/acinclude.m4

./reconf-all

# clean up some spurious exec perms
chmod -x main/lib/option/getoptions.h
chmod -x main/lib/option/getoptions.c
chmod -x main/gbx/gbx_local.h
chmod -x main/gbx/gbx_subr_file.c
chmod -x main/lib/option/main.h
chmod -x gb.qt/src/CContainer.cpp
chmod -x main/lib/option/main.c

%build
# Gambas can't deal with -Wp,-D_FORTIFY_SOURCE=2
MY_CFLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//g'`
%configure \
	--datadir="%{_datadir}" \
	--enable-intl \
	--enable-conv \
	--enable-qt \
%if 0%{with_kde3}
	--enable-kde \
%endif
	--enable-net \
	--enable-curl \
	--enable-firebird \
	--enable-postgresql \
	--enable-mysql \
	--enable-sqlite3 \
	--enable-sdl \
	--enable-vb \
	--enable-pdf \
	--disable-corba \
	--disable-sqlite2 \
	--disable-qte \
	--with-bzlib2-libraries=%{_libdir} \
	--with-crypt-libraries=%{_libdir} \
	--with-curl-libraries=%{_libdir} \
	--with-desktop-libraries=%{_libdir} \
	--with-firebird-includes=%{_includedir}/firebird \
	--with-firebird-libraries=%{_libdir} \
	--with-ffi-includes=`pkg-config libffi --variable=includedir` \
	--with-ffi-libraries=`pkg-config libffi --variable=libdir` \
	--with-intl-libraries=%{_libdir} \
	--with-conv-libraries=%{_libdir} \
	--with-gettext-libraries=%{_libdir} \
	--with-gtk-libraries=%{_libdir} \
	--with-gtk_svg-libraries=%{_libdir} \
	--with-image-libraries=%{_libdir} \
	--with-kde-libraries=%{_libdir} \
	--with-mysql-libraries=%{_libdir}/mysql \
	--with-net-libraries=%{_libdir} \
	--with-odbc-libraries=%{_libdir} \
	--with-opengl-libraries=%{_libdir} \
	--with-pcre-libraries=%{_libdir} \
	--with-poppler-libraries=%{_libdir} \
	--with-postgresql-libraries=%{_libdir} \
	--with-qt-libraries=%{_libdir}/qt-3.3/lib \
	--with-qt-includes=%{_libdir}/qt-3.3/include/ \
	--with-qtopengl-libraries=%{_libdir} \
	--with-sdl-libraries=%{_libdir} \
	--with-sdl_sound-libraries=%{_libdir} \
	--with-smtp-libraries=%{_libdir} \
	--with-sqlite3-libraries=%{_libdir} \
	--with-v4l-libraries=%{_libdir} \
	--with-xml-libraries=%{_libdir} \
	--with-xslt-libraries=%{_libdir} \
	--with-zlib-libraries=%{_libdir} \
	AM_CFLAGS="$MY_CFLAGS" AM_CXXFLAGS="$MY_CFLAGS"
# rpath removal
for i in main gb.qt.kde; do
	sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' $i/libtool
	sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' $i/libtool
done
%{__make} LIBTOOL=%{_bindir}/libtool %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
export PATH=$RPM_BUILD_ROOT%{_bindir}:$PATH
make LIBTOOL=%{_bindir}/libtool DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" install
# Yes, I know. Normally we'd nuke the .la files, but Gambas is retar^Wspecial.
# rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
install -m0644 -p ./app/src/%{name}/.icon.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.png

desktop-file-install --vendor="fedora"			\
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications	\
  %{SOURCE1}

# get the buildroot out of the examples
for i in `grep -lr "$RPM_BUILD_ROOT" $RPM_BUILD_ROOT%{_datadir}/%{name}/examples/`; 
do
  sed -i "s|$RPM_BUILD_ROOT||g" $i; 
done

# Get the SVN noise out of the main tree
find $RPM_BUILD_ROOT%{_datadir}/%{name}/ -type d -name .svn -exec rm -rf {} 2>/dev/null ';' || :

# Upstream says we don't need those files. Not sure why they install them then. :/
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/gb.la $RPM_BUILD_ROOT%{_libdir}/%{name}/gb.so*

# No need for the static libs
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/*.a

# Mime types.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mime/packages/
# We no longer package this file to avoid conflict with gambas3.
# install -m 0644 -p app/mime/application-x-gambasscript.xml $RPM_BUILD_ROOT%{_datadir}/mime/packages/
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/icons/application-x-gambasscript.png
install -m 0644 -p main/mime/application-x-gambas.xml $RPM_BUILD_ROOT%{_datadir}/mime/packages/

%clean
rm -rf $RPM_BUILD_ROOT

%post runtime
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun runtime
update-mime-database %{_datadir}/mime &> /dev/null || :

%post script
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun script
update-mime-database %{_datadir}/mime &> /dev/null || :

%files runtime
%defattr(-, root, root, 0755)
%doc COPYING INSTALL README
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/gb.component
%{_libdir}/%{name}/gb.debug.*
%{_libdir}/%{name}/gb.draw.*
%{_libdir}/%{name}/gb.eval.*
%{_bindir}/gbr2
%{_bindir}/gbx2
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/*.desktop
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/info/
%{_datadir}/%{name}/info/gb.debug.*
%{_datadir}/%{name}/info/gb.eval.*
%{_datadir}/%{name}/info/gb.info
%{_datadir}/%{name}/info/gb.list
%dir %{_datadir}/%{name}/icons/
%{_datadir}/%{name}/icons/application-x-gambas.png
%{_datadir}/mime/packages/application-x-gambas.xml
%{_datadir}/%{name}/icons/application-x-gambasserverpage.png

%files devel
%defattr(-, root, root, 0755)
%doc COPYING
%{_bindir}/gbc2
%{_bindir}/gba2
%{_bindir}/gbi2

%files script
%defattr(-, root, root, 0755)
%{_bindir}/gbs2
%{_bindir}/gbw2
%{_bindir}/gbs2.gambas
# %%{_datadir}/%{name}/icons/application-x-gambasscript.png
# %%{_datadir}/mime/packages/application-x-gambasscript.xml

%files ide
%defattr(-, root, root, 0755)
%{_bindir}/%{name}
%{_bindir}/%{name}.gambas
%{_bindir}/%{name}-database-manager.gambas

%files examples
%defattr(-, root, root, 0755)
%dir %{_datadir}/%{name}/examples/
%dir %{_datadir}/%{name}/examples/Automation/
%dir %{_datadir}/%{name}/examples/Basic/
%dir %{_datadir}/%{name}/examples/Control/
%dir %{_datadir}/%{name}/examples/Database/
%dir %{_datadir}/%{name}/examples/Drawing/
%dir %{_datadir}/%{name}/examples/Games/
%dir %{_datadir}/%{name}/examples/Misc/
%dir %{_datadir}/%{name}/examples/Networking/
%dir %{_datadir}/%{name}/examples/OpenGL/
%dir %{_datadir}/%{name}/examples/Printing/
%dir %{_datadir}/%{name}/examples/Sound/
%dir %{_datadir}/%{name}/examples/Video/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Automation/KateBrowser/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Automation/KateBrowser/.lang/
%{_datadir}/%{name}/examples/Automation/KateBrowser/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Automation/KateBrowser/.gambas/
%{_datadir}/%{name}/examples/Automation/KateBrowser/.icon*
%{_datadir}/%{name}/examples/Automation/KateBrowser/.project
%{_datadir}/%{name}/examples/Automation/KateBrowser/CHANGELOG
%{_datadir}/%{name}/examples/Automation/KateBrowser/FBrowser.*
%{_datadir}/%{name}/examples/Automation/KateBrowser/KateBrowser.gambas
%{_datadir}/%{name}/examples/Automation/KateBrowser/arrow.png
%{_datadir}/%{name}/examples/Automation/KateBrowser/kate.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Automation/Scripting/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Automation/Scripting/.lang/
%{_datadir}/%{name}/examples/Automation/Scripting/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Automation/Scripting/.gambas/
%{_datadir}/%{name}/examples/Automation/Scripting/.icon.png
%{_datadir}/%{name}/examples/Automation/Scripting/.project
%{_datadir}/%{name}/examples/Automation/Scripting/FScript.*
%{_datadir}/%{name}/examples/Automation/Scripting/Scripting.gambas
%{_datadir}/%{name}/examples/Automation/Scripting/background.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Basic/Blights/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Basic/Blights/.lang/
%{_datadir}/%{name}/examples/Basic/Blights/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Basic/Blights/.gambas/
%{_datadir}/%{name}/examples/Basic/Blights/.icon*
%{_datadir}/%{name}/examples/Basic/Blights/.project
%{_datadir}/%{name}/examples/Basic/Blights/Blights.gambas
%{_datadir}/%{name}/examples/Basic/Blights/ampoule.png
%{_datadir}/%{name}/examples/Basic/Blights/bloff.xpm
%{_datadir}/%{name}/examples/Basic/Blights/blon.xpm
%{_datadir}/%{name}/examples/Basic/Blights/win1.*

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Basic/Collection/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Basic/Collection/.lang/
%{_datadir}/%{name}/examples/Basic/Collection/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Basic/Collection/.gambas/
%{_datadir}/%{name}/examples/Basic/Collection/.icon*
%{_datadir}/%{name}/examples/Basic/Collection/.project
%{_datadir}/%{name}/examples/Basic/Collection/CThing.class
%{_datadir}/%{name}/examples/Basic/Collection/Collection.gambas
%{_datadir}/%{name}/examples/Basic/Collection/FStart.*
%{_datadir}/%{name}/examples/Basic/Collection/collection.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Basic/DragNDrop/
%{_datadir}/%{name}/examples/Basic/DragNDrop/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Basic/DragNDrop/.gambas/
%{_datadir}/%{name}/examples/Basic/DragNDrop/.icon*
%{_datadir}/%{name}/examples/Basic/DragNDrop/.project
%{_datadir}/%{name}/examples/Basic/DragNDrop/BulletHole.xpm
%{_datadir}/%{name}/examples/Basic/DragNDrop/DragNDrop.gambas
%{_datadir}/%{name}/examples/Basic/DragNDrop/FDragNDrop.*
%{_datadir}/%{name}/examples/Basic/DragNDrop/*.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Basic/Object/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Basic/Object/.lang/
%{_datadir}/%{name}/examples/Basic/Object/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Basic/Object/.gambas/
%{_datadir}/%{name}/examples/Basic/Object/.icon*
%{_datadir}/%{name}/examples/Basic/Object/.project
%{_datadir}/%{name}/examples/Basic/Object/CThing.class
%{_datadir}/%{name}/examples/Basic/Object/FStart.*
%{_datadir}/%{name}/examples/Basic/Object/Object.*
%{_datadir}/%{name}/examples/Basic/Object/object.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Basic/Timer/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Basic/Timer/.lang/
%{_datadir}/%{name}/examples/Basic/Timer/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Basic/Timer/.gambas/
%{_datadir}/%{name}/examples/Basic/Timer/.icon*
%{_datadir}/%{name}/examples/Basic/Timer/.project
%{_datadir}/%{name}/examples/Basic/Timer/FOtherTimer.*
%{_datadir}/%{name}/examples/Basic/Timer/FTimer.*
%{_datadir}/%{name}/examples/Basic/Timer/Timer.gambas
%{_datadir}/%{name}/examples/Basic/Timer/timer.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Control/Embedder/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Control/Embedder/.lang/
%{_datadir}/%{name}/examples/Control/Embedder/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Control/Embedder/.gambas/
%{_datadir}/%{name}/examples/Control/Embedder/.icon*
%{_datadir}/%{name}/examples/Control/Embedder/.project
%{_datadir}/%{name}/examples/Control/Embedder/.settings
%{_datadir}/%{name}/examples/Control/Embedder/Embedder.gambas
%{_datadir}/%{name}/examples/Control/Embedder/FMain.*
%{_datadir}/%{name}/examples/Control/Embedder/embedder.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Control/HighlightEditor/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Control/HighlightEditor/.lang/
%{_datadir}/%{name}/examples/Control/HighlightEditor/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Control/HighlightEditor/.gambas/
%{_datadir}/%{name}/examples/Control/HighlightEditor/.icon*
%{_datadir}/%{name}/examples/Control/HighlightEditor/.project
%{_datadir}/%{name}/examples/Control/HighlightEditor/FEditor.*
%{_datadir}/%{name}/examples/Control/HighlightEditor/HighlightEditor.gambas
%{_datadir}/%{name}/examples/Control/HighlightEditor/download.html
%{_datadir}/%{name}/examples/Control/HighlightEditor/editor.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Control/TextEdit/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Control/TextEdit/.lang/
%{_datadir}/%{name}/examples/Control/TextEdit/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Control/TextEdit/.gambas/
%{_datadir}/%{name}/examples/Control/TextEdit/.icon*
%{_datadir}/%{name}/examples/Control/TextEdit/.project
%{_datadir}/%{name}/examples/Control/TextEdit/FMain.*
%{_datadir}/%{name}/examples/Control/TextEdit/TextEdit.gambas
%{_datadir}/%{name}/examples/Control/TextEdit/edit.png
%{_datadir}/%{name}/examples/Control/TextEdit/frmShowHtml.*
%{_datadir}/%{name}/examples/Control/TextEdit/text.html

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Control/TreeView/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Control/TreeView/.lang/
%{_datadir}/%{name}/examples/Control/TreeView/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Control/TreeView/.gambas/
%{_datadir}/%{name}/examples/Control/TreeView/.icon*
%{_datadir}/%{name}/examples/Control/TreeView/.project
%{_datadir}/%{name}/examples/Control/TreeView/Female.png
%{_datadir}/%{name}/examples/Control/TreeView/Male.png
%{_datadir}/%{name}/examples/Control/TreeView/TreeView*
%{_datadir}/%{name}/examples/Control/TreeView/treeview.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Database/DataReportExample/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Database/DataReportExample/.lang/
%{_datadir}/%{name}/examples/Database/DataReportExample/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Database/DataReportExample/.gambas/
%{_datadir}/%{name}/examples/Database/DataReportExample/.icon*
%{_datadir}/%{name}/examples/Database/DataReportExample/.project
%{_datadir}/%{name}/examples/Database/DataReportExample/DataReportExample.gambas
%{_datadir}/%{name}/examples/Database/DataReportExample/Fabout.*
%{_datadir}/%{name}/examples/Database/DataReportExample/Fconn.*
%{_datadir}/%{name}/examples/Database/DataReportExample/Fmain.*
%{_datadir}/%{name}/examples/Database/DataReportExample/Fpreview.*
%{_datadir}/%{name}/examples/Database/DataReportExample/Mglobal.module
%{_datadir}/%{name}/examples/Database/DataReportExample/pic/

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Database/Database/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Database/Database/.lang/
%{_datadir}/%{name}/examples/Database/Database/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Database/Database/.gambas/
%{_datadir}/%{name}/examples/Database/Database/.icon*
%{_datadir}/%{name}/examples/Database/Database/.project
%{_datadir}/%{name}/examples/Database/Database/Database.gambas
%{_datadir}/%{name}/examples/Database/Database/FMain.*
%{_datadir}/%{name}/examples/Database/Database/FRequest.*
%{_datadir}/%{name}/examples/Database/Database/FTest.*
%{_datadir}/%{name}/examples/Database/Database/database.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Database/PictureDatabase/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Database/PictureDatabase/.lang/
%{_datadir}/%{name}/examples/Database/PictureDatabase/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Database/PictureDatabase/.gambas/
%{_datadir}/%{name}/examples/Database/PictureDatabase/.icon*
%{_datadir}/%{name}/examples/Database/PictureDatabase/.project
%{_datadir}/%{name}/examples/Database/PictureDatabase/FormPictureDatabase.*
%{_datadir}/%{name}/examples/Database/PictureDatabase/Images/
%{_datadir}/%{name}/examples/Database/PictureDatabase/ModuleDatabase.module
%{_datadir}/%{name}/examples/Database/PictureDatabase/PictureDatabase.gambas

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Drawing/AnalogWatch/
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Drawing/AnalogWatch/.gambas/
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.icon*
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.project
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/AnalogWatch.gambas
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/FrmClock.*
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/timer.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Drawing/Barcode/
%{_datadir}/%{name}/examples/Drawing/Barcode/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Drawing/Barcode/.gambas/
%{_datadir}/%{name}/examples/Drawing/Barcode/.icon*
%{_datadir}/%{name}/examples/Drawing/Barcode/.project
%{_datadir}/%{name}/examples/Drawing/Barcode/.settings
%{_datadir}/%{name}/examples/Drawing/Barcode/Barcode.gambas
%{_datadir}/%{name}/examples/Drawing/Barcode/FMain.*
%{_datadir}/%{name}/examples/Drawing/Barcode/barcode.png
%{_datadir}/%{name}/examples/Drawing/Barcode/modCrBcode.module

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Drawing/Chart/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Drawing/Chart/.lang/
%{_datadir}/%{name}/examples/Drawing/Chart/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Drawing/Chart/.gambas/
%{_datadir}/%{name}/examples/Drawing/Chart/.icon*
%{_datadir}/%{name}/examples/Drawing/Chart/.project
%{_datadir}/%{name}/examples/Drawing/Chart/Chart.gambas
%{_datadir}/%{name}/examples/Drawing/Chart/FormChart.*
%{_datadir}/%{name}/examples/Drawing/Chart/FormData.*
%{_datadir}/%{name}/examples/Drawing/Chart/graph.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Drawing/Clock/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Drawing/Clock/.lang/
%{_datadir}/%{name}/examples/Drawing/Clock/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Drawing/Clock/.gambas/
%{_datadir}/%{name}/examples/Drawing/Clock/.icon*
%{_datadir}/%{name}/examples/Drawing/Clock/.project
%{_datadir}/%{name}/examples/Drawing/Clock/Clock.gambas
%{_datadir}/%{name}/examples/Drawing/Clock/FClock.*
%{_datadir}/%{name}/examples/Drawing/Clock/img/

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Drawing/Gravity/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Drawing/Gravity/.lang/
%{_datadir}/%{name}/examples/Drawing/Gravity/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Drawing/Gravity/.gambas/
%{_datadir}/%{name}/examples/Drawing/Gravity/.icon*
%{_datadir}/%{name}/examples/Drawing/Gravity/.project
%{_datadir}/%{name}/examples/Drawing/Gravity/FAbout.*
%{_datadir}/%{name}/examples/Drawing/Gravity/FMain.*
%{_datadir}/%{name}/examples/Drawing/Gravity/Gravity.gambas
%{_datadir}/%{name}/examples/Drawing/Gravity/cBall.class
%{_datadir}/%{name}/examples/Drawing/Gravity/gravity.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Drawing/ImageViewer/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Drawing/ImageViewer/.lang/
%{_datadir}/%{name}/examples/Drawing/ImageViewer/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Drawing/ImageViewer/.gambas/
%{_datadir}/%{name}/examples/Drawing/ImageViewer/.icon*
%{_datadir}/%{name}/examples/Drawing/ImageViewer/.project
%{_datadir}/%{name}/examples/Drawing/ImageViewer/FViewer.*
%{_datadir}/%{name}/examples/Drawing/ImageViewer/ImageViewer.gambas
%{_datadir}/%{name}/examples/Drawing/ImageViewer/image.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.lang/
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.gambas/
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.icon*
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.project
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/FOnScreenDisplay.*
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/OnScreenDisplay.gambas
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/icon.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Drawing/Sensor/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Drawing/Sensor/.lang/
%{_datadir}/%{name}/examples/Drawing/Sensor/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Drawing/Sensor/.gambas/
%{_datadir}/%{name}/examples/Drawing/Sensor/.icon*
%{_datadir}/%{name}/examples/Drawing/Sensor/.project
%{_datadir}/%{name}/examples/Drawing/Sensor/FSensor.*
%{_datadir}/%{name}/examples/Drawing/Sensor/Main.module
%{_datadir}/%{name}/examples/Drawing/Sensor/Sensor.gambas
%{_datadir}/%{name}/examples/Drawing/Sensor/orange.png
%{_datadir}/%{name}/examples/Drawing/Sensor/red.png
%{_datadir}/%{name}/examples/Drawing/Sensor/thermo*.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Games/BeastScroll/
%{_datadir}/%{name}/examples/Games/BeastScroll/.dir_icon.png
%{_datadir}/%{name}/examples/Games/BeastScroll/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Games/BeastScroll/.gambas/
%{_datadir}/%{name}/examples/Games/BeastScroll/.icon*
%{_datadir}/%{name}/examples/Games/BeastScroll/.project
%{_datadir}/%{name}/examples/Games/BeastScroll/BeastScroll.gambas
%{_datadir}/%{name}/examples/Games/BeastScroll/MMain.module
%{_datadir}/%{name}/examples/Games/BeastScroll/b-title.mod
%{_datadir}/%{name}/examples/Games/BeastScroll/bgd*.png
%{_datadir}/%{name}/examples/Games/BeastScroll/fireworks.png
%{_datadir}/%{name}/examples/Games/BeastScroll/logo.png
%{_datadir}/%{name}/examples/Games/BeastScroll/scrolltext.png
%{_datadir}/%{name}/examples/Games/BeastScroll/sprite*.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Games/Concent/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Games/Concent/.lang/
%{_datadir}/%{name}/examples/Games/Concent/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Games/Concent/.gambas/
%{_datadir}/%{name}/examples/Games/Concent/.icon*
%{_datadir}/%{name}/examples/Games/Concent/.project
%{_datadir}/%{name}/examples/Games/Concent/.settings
%{_datadir}/%{name}/examples/Games/Concent/*.wav
%{_datadir}/%{name}/examples/Games/Concent/CHANGELOG
%{_datadir}/%{name}/examples/Games/Concent/Concent.gambas
%{_datadir}/%{name}/examples/Games/Concent/fotos.*
%{_datadir}/%{name}/examples/Games/Concent/frmAcerca.*
%{_datadir}/%{name}/examples/Games/Concent/frmInstrucciones.*
%{_datadir}/%{name}/examples/Games/Concent/funciones.*
%{_datadir}/%{name}/examples/Games/Concent/imagenes/
%{_datadir}/%{name}/examples/Games/Concent/principal.*

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Games/DeepSpace/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Games/DeepSpace/.lang/
%{_datadir}/%{name}/examples/Games/DeepSpace/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Games/DeepSpace/.gambas/
%{_datadir}/%{name}/examples/Games/DeepSpace/.icon*
%{_datadir}/%{name}/examples/Games/DeepSpace/.project
%{_datadir}/%{name}/examples/Games/DeepSpace/CBullet.class
%{_datadir}/%{name}/examples/Games/DeepSpace/CObject.class
%{_datadir}/%{name}/examples/Games/DeepSpace/DeepSpace.gambas
%{_datadir}/%{name}/examples/Games/DeepSpace/FAbout.*
%{_datadir}/%{name}/examples/Games/DeepSpace/FMain.*
%{_datadir}/%{name}/examples/Games/DeepSpace/MMain.module
%{_datadir}/%{name}/examples/Games/DeepSpace/MMath.*
%{_datadir}/%{name}/examples/Games/DeepSpace/doc/
%{_datadir}/%{name}/examples/Games/DeepSpace/images/
%{_datadir}/%{name}/examples/Games/DeepSpace/object.data/

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Games/GameOfLife/
%{_datadir}/%{name}/examples/Games/GameOfLife/.debug
%{_datadir}/%{name}/examples/Games/GameOfLife/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Games/GameOfLife/.gambas/
%{_datadir}/%{name}/examples/Games/GameOfLife/.icon*
%{_datadir}/%{name}/examples/Games/GameOfLife/.project
%{_datadir}/%{name}/examples/Games/GameOfLife/.settings
%{_datadir}/%{name}/examples/Games/GameOfLife/CGameField.class
%{_datadir}/%{name}/examples/Games/GameOfLife/FMain.*
%{_datadir}/%{name}/examples/Games/GameOfLife/GameOfLife.gambas
%{_datadir}/%{name}/examples/Games/GameOfLife/glob2*.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Games/RobotFindsKitten/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Games/RobotFindsKitten/.lang/
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Games/RobotFindsKitten/.gambas/
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.icon*
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.project
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/COPYING
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/Frfk.*
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/RobotFindsKitten.gambas
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/heart.png
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/nkis.txt
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/readme.txt

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Games/Snake/
%{_datadir}/%{name}/examples/Games/Snake/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Games/Snake/.gambas/
%{_datadir}/%{name}/examples/Games/Snake/.icon*
%{_datadir}/%{name}/examples/Games/Snake/.project
%{_datadir}/%{name}/examples/Games/Snake/FrmMain.*
%{_datadir}/%{name}/examples/Games/Snake/Snake.gambas
%{_datadir}/%{name}/examples/Games/Snake/apple.png
%{_datadir}/%{name}/examples/Games/Snake/body.png
%{_datadir}/%{name}/examples/Games/Snake/*.wav
%{_datadir}/%{name}/examples/Games/Snake/head.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Games/Solitaire/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Games/Solitaire/.lang/
%{_datadir}/%{name}/examples/Games/Solitaire/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Games/Solitaire/.gambas/
%{_datadir}/%{name}/examples/Games/Solitaire/.icon*
%{_datadir}/%{name}/examples/Games/Solitaire/.project
%{_datadir}/%{name}/examples/Games/Solitaire/CBoardDesign.class
%{_datadir}/%{name}/examples/Games/Solitaire/CMove.class
%{_datadir}/%{name}/examples/Games/Solitaire/FBoardSelect.*
%{_datadir}/%{name}/examples/Games/Solitaire/FGameArea.*
%{_datadir}/%{name}/examples/Games/Solitaire/Global.class
%{_datadir}/%{name}/examples/Games/Solitaire/MBoards.module
%{_datadir}/%{name}/examples/Games/Solitaire/Solitaire.gambas
%{_datadir}/%{name}/examples/Games/Solitaire/ball.png
%{_datadir}/%{name}/examples/Games/Solitaire/new.png
%{_datadir}/%{name}/examples/Games/Solitaire/quit.png
%{_datadir}/%{name}/examples/Games/Solitaire/redo.png
%{_datadir}/%{name}/examples/Games/Solitaire/undo.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Misc/Console/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Misc/Console/.lang/
%{_datadir}/%{name}/examples/Misc/Console/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Misc/Console/.gambas/
%{_datadir}/%{name}/examples/Misc/Console/.icon*
%{_datadir}/%{name}/examples/Misc/Console/.project
%{_datadir}/%{name}/examples/Misc/Console/Console.gambas
%{_datadir}/%{name}/examples/Misc/Console/FConsole.*
%{_datadir}/%{name}/examples/Misc/Console/konsole.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Misc/Evaluator/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Misc/Evaluator/.lang/
%{_datadir}/%{name}/examples/Misc/Evaluator/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Misc/Evaluator/.gambas/
%{_datadir}/%{name}/examples/Misc/Evaluator/.icon*
%{_datadir}/%{name}/examples/Misc/Evaluator/.project
%{_datadir}/%{name}/examples/Misc/Evaluator/Evaluator.gambas
%{_datadir}/%{name}/examples/Misc/Evaluator/FEval.*
%{_datadir}/%{name}/examples/Misc/Evaluator/calculator.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Misc/Explorer/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Misc/Explorer/.lang/
%{_datadir}/%{name}/examples/Misc/Explorer/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Misc/Explorer/.gambas/
%{_datadir}/%{name}/examples/Misc/Explorer/.icon*
%{_datadir}/%{name}/examples/Misc/Explorer/.project
%{_datadir}/%{name}/examples/Misc/Explorer/Explorer.gambas
%{_datadir}/%{name}/examples/Misc/Explorer/FExplorer.*
%{_datadir}/%{name}/examples/Misc/Explorer/folder.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Misc/Notepad/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Misc/Notepad/.lang/
%{_datadir}/%{name}/examples/Misc/Notepad/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Misc/Notepad/.gambas/
%{_datadir}/%{name}/examples/Misc/Notepad/.icon*
%{_datadir}/%{name}/examples/Misc/Notepad/.project
%{_datadir}/%{name}/examples/Misc/Notepad/FAbout.*
%{_datadir}/%{name}/examples/Misc/Notepad/FNotepad.*
%{_datadir}/%{name}/examples/Misc/Notepad/Notepad.gambas
%{_datadir}/%{name}/examples/Misc/Notepad/notepad.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Misc/PDFViewer/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Misc/PDFViewer/.lang/
%{_datadir}/%{name}/examples/Misc/PDFViewer/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Misc/PDFViewer/.gambas/
%{_datadir}/%{name}/examples/Misc/PDFViewer/.icon*
%{_datadir}/%{name}/examples/Misc/PDFViewer/.project
%{_datadir}/%{name}/examples/Misc/PDFViewer/FMain.*
%{_datadir}/%{name}/examples/Misc/PDFViewer/Fabout.*
%{_datadir}/%{name}/examples/Misc/PDFViewer/PDFViewer.gambas
%{_datadir}/%{name}/examples/Misc/PDFViewer/pdf.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/ClientSocket/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/ClientSocket/.lang/
%{_datadir}/%{name}/examples/Networking/ClientSocket/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Networking/ClientSocket/.gambas/
%{_datadir}/%{name}/examples/Networking/ClientSocket/.icon*
%{_datadir}/%{name}/examples/Networking/ClientSocket/.project
%{_datadir}/%{name}/examples/Networking/ClientSocket/ClientSocket.gambas
%{_datadir}/%{name}/examples/Networking/ClientSocket/FrmMain.*
%{_datadir}/%{name}/examples/Networking/ClientSocket/socket.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/DnsClient/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/DnsClient/.lang/
%{_datadir}/%{name}/examples/Networking/DnsClient/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Networking/DnsClient/.gambas/
%{_datadir}/%{name}/examples/Networking/DnsClient/.icon*
%{_datadir}/%{name}/examples/Networking/DnsClient/.project
%{_datadir}/%{name}/examples/Networking/DnsClient/DnsClient.gambas
%{_datadir}/%{name}/examples/Networking/DnsClient/FMain.*
%{_datadir}/%{name}/examples/Networking/DnsClient/dnsclient.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/HTTPGet/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/HTTPGet/.lang/
%{_datadir}/%{name}/examples/Networking/HTTPGet/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Networking/HTTPGet/.gambas/
%{_datadir}/%{name}/examples/Networking/HTTPGet/.icon*
%{_datadir}/%{name}/examples/Networking/HTTPGet/.project
%{_datadir}/%{name}/examples/Networking/HTTPGet/ClsParams.class
%{_datadir}/%{name}/examples/Networking/HTTPGet/F.*
%{_datadir}/%{name}/examples/Networking/HTTPGet/FConfig.*
%{_datadir}/%{name}/examples/Networking/HTTPGet/HTTPGet.gambas
%{_datadir}/%{name}/examples/Networking/HTTPGet/httpclient.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/HTTPPost/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/HTTPPost/.lang/
%{_datadir}/%{name}/examples/Networking/HTTPPost/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Networking/HTTPPost/.gambas/
%{_datadir}/%{name}/examples/Networking/HTTPPost/.icon*
%{_datadir}/%{name}/examples/Networking/HTTPPost/.project
%{_datadir}/%{name}/examples/Networking/HTTPPost/F.*
%{_datadir}/%{name}/examples/Networking/HTTPPost/HTTPPost.gambas
%{_datadir}/%{name}/examples/Networking/HTTPPost/httpclient.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/SerialPort/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/SerialPort/.lang/
%{_datadir}/%{name}/examples/Networking/SerialPort/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Networking/SerialPort/.gambas/
%{_datadir}/%{name}/examples/Networking/SerialPort/.icon*
%{_datadir}/%{name}/examples/Networking/SerialPort/.project
%{_datadir}/%{name}/examples/Networking/SerialPort/FSerialPort.*
%{_datadir}/%{name}/examples/Networking/SerialPort/SerialPort.gambas
%{_datadir}/%{name}/examples/Networking/SerialPort/serialport.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/ServerSocket/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/ServerSocket/.lang/
%{_datadir}/%{name}/examples/Networking/ServerSocket/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Networking/ServerSocket/.gambas/
%{_datadir}/%{name}/examples/Networking/ServerSocket/.icon*
%{_datadir}/%{name}/examples/Networking/ServerSocket/.project
%{_datadir}/%{name}/examples/Networking/ServerSocket/FrmMain.*
%{_datadir}/%{name}/examples/Networking/ServerSocket/ServerSocket.gambas
%{_datadir}/%{name}/examples/Networking/ServerSocket/serversocket.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/UDPServerClient/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/UDPServerClient/.lang/
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Networking/UDPServerClient/.gambas/
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.icon*
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.project
%{_datadir}/%{name}/examples/Networking/UDPServerClient/FrmClient.*
%{_datadir}/%{name}/examples/Networking/UDPServerClient/FrmServer.*
%{_datadir}/%{name}/examples/Networking/UDPServerClient/UDPServerClient.gambas
%{_datadir}/%{name}/examples/Networking/UDPServerClient/udpsocket.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/WebBrowser/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Networking/WebBrowser/.lang/
%{_datadir}/%{name}/examples/Networking/WebBrowser/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Networking/WebBrowser/.gambas/
%{_datadir}/%{name}/examples/Networking/WebBrowser/.icon*
%{_datadir}/%{name}/examples/Networking/WebBrowser/.project
%{_datadir}/%{name}/examples/Networking/WebBrowser/FBrowser.*
%{_datadir}/%{name}/examples/Networking/WebBrowser/WebBrowser.gambas
%{_datadir}/%{name}/examples/Networking/WebBrowser/webbrowser.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/OpenGL/3DWebCam/
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/OpenGL/3DWebCam/.gambas/
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.icon*
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.project
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/3DWebCam.gambas
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/Mmain.module
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/webcam.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/OpenGL/GambasGears/
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/OpenGL/GambasGears/.gambas/
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.icon*
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.project
%{_datadir}/%{name}/examples/OpenGL/GambasGears/GambasGears.gambas
%{_datadir}/%{name}/examples/OpenGL/GambasGears/Module1.module
%{_datadir}/%{name}/examples/OpenGL/GambasGears/gears.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/OpenGL/PDFPresentation/
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.gambas/
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.icon*
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.project
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.settings
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/Clogo.class
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/CpdfPresentation.class
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/FMain.*
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/MMain.module
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/PDFPresentation.gambas
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/icon.png
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/logo.png
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/music.xm

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Printing/Printing/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Printing/Printing/.lang/
%{_datadir}/%{name}/examples/Printing/Printing/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Printing/Printing/.gambas/
%{_datadir}/%{name}/examples/Printing/Printing/.icon*
%{_datadir}/%{name}/examples/Printing/Printing/.project
%{_datadir}/%{name}/examples/Printing/Printing/FormPrinting.*
%{_datadir}/%{name}/examples/Printing/Printing/Images/
%{_datadir}/%{name}/examples/Printing/Printing/ModulePrint*
%{_datadir}/%{name}/examples/Printing/Printing/Printing.gambas
%{_datadir}/%{name}/examples/Printing/Printing/ReadMe.txt

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Sound/CDPlayer/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Sound/CDPlayer/.lang/
%{_datadir}/%{name}/examples/Sound/CDPlayer/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Sound/CDPlayer/.gambas/
%{_datadir}/%{name}/examples/Sound/CDPlayer/.icon*
%{_datadir}/%{name}/examples/Sound/CDPlayer/.project
%{_datadir}/%{name}/examples/Sound/CDPlayer/CDPlayer.*
%{_datadir}/%{name}/examples/Sound/CDPlayer/Fcdplayer.*
%{_datadir}/%{name}/examples/Sound/CDPlayer/cd.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Sound/MusicPlayer/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Sound/MusicPlayer/.lang/
%{_datadir}/%{name}/examples/Sound/MusicPlayer/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Sound/MusicPlayer/.gambas/
%{_datadir}/%{name}/examples/Sound/MusicPlayer/.icon*
%{_datadir}/%{name}/examples/Sound/MusicPlayer/.project
%{_datadir}/%{name}/examples/Sound/MusicPlayer/FSoundPlayer.*
%{_datadir}/%{name}/examples/Sound/MusicPlayer/MusicPlayer.gambas
%{_datadir}/%{name}/examples/Sound/MusicPlayer/sound.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Video/MoviePlayer/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Video/MoviePlayer/.lang/
%{_datadir}/%{name}/examples/Video/MoviePlayer/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Video/MoviePlayer/.gambas/
%{_datadir}/%{name}/examples/Video/MoviePlayer/.icon*
%{_datadir}/%{name}/examples/Video/MoviePlayer/.project
%{_datadir}/%{name}/examples/Video/MoviePlayer/FMoviePlayer.*
%{_datadir}/%{name}/examples/Video/MoviePlayer/MoviePlayer.gambas
%{_datadir}/%{name}/examples/Video/MoviePlayer/open.png
%{_datadir}/%{name}/examples/Video/MoviePlayer/pause.png
%{_datadir}/%{name}/examples/Video/MoviePlayer/play.png
%{_datadir}/%{name}/examples/Video/MoviePlayer/stop.png
%{_datadir}/%{name}/examples/Video/MoviePlayer/video.png

%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Video/MyWebCam/
%attr(0777,nobody,nobody) %dir %{_datadir}/%{name}/examples/Video/MyWebCam/.lang/
%{_datadir}/%{name}/examples/Video/MyWebCam/.directory
%attr(0777,nobody,nobody) %{_datadir}/%{name}/examples/Video/MyWebCam/.gambas/
%{_datadir}/%{name}/examples/Video/MyWebCam/.icon*
%{_datadir}/%{name}/examples/Video/MyWebCam/.project
%{_datadir}/%{name}/examples/Video/MyWebCam/Form1.*
%{_datadir}/%{name}/examples/Video/MyWebCam/Module1.module
%{_datadir}/%{name}/examples/Video/MyWebCam/MyWebCam.gambas
%{_datadir}/%{name}/examples/Video/MyWebCam/camera.png

# Translation files
%lang(ca) %{_datadir}/%{name}/examples/Automation/KateBrowser/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Automation/KateBrowser/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Automation/Scripting/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Automation/Scripting/.lang/es.*o
%lang(es) %{_datadir}/%{name}/examples/Basic/Blights/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Basic/Blights/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Basic/Collection/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Basic/Collection/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Basic/Object/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Basic/Object/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Basic/Timer/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Basic/Timer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/Embedder/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Control/Embedder/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/HighlightEditor/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Control/HighlightEditor/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/TreeView/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Control/TreeView/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Database/DataReportExample/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Database/DataReportExample/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Database/Database/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Database/Database/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Database/PictureDatabase/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Database/PictureDatabase/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/Chart/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Drawing/Chart/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/Clock/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Drawing/Clock/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/Gravity/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Drawing/Gravity/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/ImageViewer/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Drawing/ImageViewer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.lang/es.*o
%lang(es) %{_datadir}/%{name}/examples/Drawing/Sensor/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Drawing/Sensor/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/Concent/.lang/ca.*o
%lang(en) %{_datadir}/%{name}/examples/Games/Concent/.lang/en.*o
%lang(es) %{_datadir}/%{name}/examples/Games/Concent/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Games/Concent/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/DeepSpace/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Games/DeepSpace/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/RobotFindsKitten/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Games/RobotFindsKitten/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/Solitaire/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Games/Solitaire/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Misc/Console/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Misc/Evaluator/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Misc/Evaluator/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Misc/Explorer/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Misc/Explorer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Misc/Notepad/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Misc/Notepad/.lang/es.*o
%lang(es) %{_datadir}/%{name}/examples/Misc/PDFViewer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/ClientSocket/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/ClientSocket/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/DnsClient/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/DnsClient/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/HTTPGet/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/HTTPGet/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/HTTPPost/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/HTTPPost/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/SerialPort/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/SerialPort/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/ServerSocket/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/ServerSocket/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/UDPServerClient/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/UDPServerClient/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/WebBrowser/.lang/ca.*o
%lang(ca) %{_datadir}/%{name}/examples/Printing/Printing/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Printing/Printing/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Sound/CDPlayer/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Sound/CDPlayer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Sound/MusicPlayer/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Sound/MusicPlayer/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Sound/MusicPlayer/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Video/MoviePlayer/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Video/MoviePlayer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Video/MyWebCam/.lang/ca.*o
%lang(es) %{_datadir}/%{name}/examples/Video/MyWebCam/.lang/es.*o

%files help
%defattr(-, root, root, 0755)
%{_datadir}/%{name}/help/

%files gb-chart
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.chart.*
%{_datadir}/%{name}/info/gb.chart.*

%files gb-compress
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.compress.*
%{_datadir}/%{name}/info/gb.compress.*

%files gb-crypt
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.crypt.*
%{_datadir}/%{name}/info/gb.crypt.*

%files gb-db
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.db.component
%{_libdir}/%{name}/gb.db.la
%{_libdir}/%{name}/gb.db.so*
%{_datadir}/%{name}/info/gb.db.info
%{_datadir}/%{name}/info/gb.db.list

%files gb-db-firebird
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.db.firebird.*

%files gb-db-form
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.db.form.*
%{_datadir}/%{name}/info/gb.db.form.*

%files gb-db-mysql
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.db.mysql.*

%files gb-db-odbc
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.db.odbc.*

%files gb-db-postgresql
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.db.postgresql.*

%files gb-db-sqlite3
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.db.sqlite3.*

%files gb-desktop
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.desktop.*
%{_datadir}/%{name}/info/gb.desktop.*

%files gb-form
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.form.component
%{_libdir}/%{name}/gb.form.gambas
# %{_libdir}/%{name}/gb.form.so*
# %{_libdir}/%{name}/gb.form.la
%{_datadir}/%{name}/info/gb.form.info
%{_datadir}/%{name}/info/gb.form.list

%files gb-form-dialog
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.form.dialog.component
%{_libdir}/%{name}/gb.form.dialog.gambas
# %{_libdir}/%{name}/gb.form.dialog.so*
# %{_libdir}/%{name}/gb.form.dialog.la
%{_datadir}/%{name}/info/gb.form.dialog.info
%{_datadir}/%{name}/info/gb.form.dialog.list

%files gb-form-mdi
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.form.mdi.component
%{_libdir}/%{name}/gb.form.mdi.gambas
# %{_libdir}/%{name}/gb.form.mdi.so*
# %{_libdir}/%{name}/gb.form.mdi.la
%{_datadir}/%{name}/info/gb.form.mdi.info
%{_datadir}/%{name}/info/gb.form.mdi.list

%files gb-gtk
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.gtk.component
%{_libdir}/%{name}/gb.gtk.gambas
%{_libdir}/%{name}/gb.gtk.so*
%{_libdir}/%{name}/gb.gtk.la
%{_datadir}/%{name}/info/gb.gtk.info
%{_datadir}/%{name}/info/gb.gtk.list

%files gb-gtk-ext
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.gtk.ext.component
%{_libdir}/%{name}/gb.gtk.ext.so*
%{_libdir}/%{name}/gb.gtk.ext.la
%{_datadir}/%{name}/info/gb.gtk.ext.info
%{_datadir}/%{name}/info/gb.gtk.ext.list

%files gb-gtk-svg
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.gtk.svg.component
%{_libdir}/%{name}/gb.gtk.svg.so*
%{_libdir}/%{name}/gb.gtk.svg.la
%{_datadir}/%{name}/info/gb.gtk.svg.info
%{_datadir}/%{name}/info/gb.gtk.svg.list

%files gb-gui
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.gui.*
%{_datadir}/%{name}/info/gb.gui.*

%files gb-image
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.image.component
%{_libdir}/%{name}/gb.image.so*
%{_libdir}/%{name}/gb.image.la
%{_datadir}/%{name}/info/gb.image.info
%{_datadir}/%{name}/info/gb.image.list

%files gb-info
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.info.*
%{_datadir}/%{name}/info/gb.info.info
%{_datadir}/%{name}/info/gb.info.list

%files gb-net
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.net.component
%{_libdir}/%{name}/gb.net.so*
%{_libdir}/%{name}/gb.net.la
%{_datadir}/%{name}/info/gb.net.info
%{_datadir}/%{name}/info/gb.net.list

%files gb-net-curl
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.net.curl.*
%{_datadir}/%{name}/info/gb.net.curl.*

%files gb-net-smtp
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.net.smtp.*
%{_datadir}/%{name}/info/gb.net.smtp.*

%files gb-opengl
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.opengl.*
%{_datadir}/%{name}/info/gb.opengl.*

%files gb-option
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.option.*
%{_datadir}/%{name}/info/gb.option.*

%files gb-pcre
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.pcre.*
%{_datadir}/%{name}/info/gb.pcre.*

%files gb-pdf
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.pdf.component
%{_libdir}/%{name}/gb.pdf.so*
%{_libdir}/%{name}/gb.pdf.la
%{_datadir}/%{name}/info/gb.pdf.info
%{_datadir}/%{name}/info/gb.pdf.list

%files gb-qt 
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.qt.component
%{_libdir}/%{name}/gb.qt.gambas 
%{_libdir}/%{name}/gb.qt.so* 
%{_libdir}/%{name}/gb.qt.la 
%{_datadir}/%{name}/info/gb.qt.info 
%{_datadir}/%{name}/info/gb.qt.list

%files gb-qt-ext
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.qt.ext.*
%{_datadir}/%{name}/info/gb.qt.ext.*

%if 0%{?with_kde3}
%files gb-qt-kde
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.qt.kde.component
%{_libdir}/%{name}/gb.qt.kde.so*
%{_libdir}/%{name}/gb.qt.kde.la
%{_datadir}/%{name}/info/gb.qt.kde.info
%{_datadir}/%{name}/info/gb.qt.kde.list

%files gb-qt-kde-html
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.qt.kde.html.*
%{_datadir}/%{name}/info/gb.qt.kde.html.*
%endif

%files gb-qt-opengl
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.qt.opengl.*
%{_datadir}/%{name}/info/gb.qt.opengl.*

%files gb-report
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.report.*
%{_datadir}/%{name}/info/gb.report.*

%files gb-sdl
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.sdl.component
%{_libdir}/%{name}/gb.sdl.so
%{_libdir}/%{name}/gb.sdl.so.*
%{_libdir}/%{name}/gb.sdl.la
%{_datadir}/%{name}/info/gb.sdl.info
%{_datadir}/%{name}/info/gb.sdl.list

%files gb-sdl-sound
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.sdl.sound.*
%{_datadir}/%{name}/info/gb.sdl.sound.*

%files gb-settings
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.settings.*
%{_datadir}/%{name}/info/gb.settings.*

%files gb-v4l
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.v4l.*
%{_datadir}/%{name}/info/gb.v4l.*

%files gb-vb
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.vb.*
%{_datadir}/%{name}/info/gb.vb.*

%files gb-web
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.web.*
%{_datadir}/%{name}/info/gb.web.*

%files gb-xml
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.xml.component
%{_libdir}/%{name}/gb.xml.so*
%{_libdir}/%{name}/gb.xml.la
%{_datadir}/%{name}/info/gb.xml.info
%{_datadir}/%{name}/info/gb.xml.list

%files gb-xml-rpc
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.xml.rpc.*
%{_datadir}/%{name}/info/gb.xml.rpc.*

%files gb-xml-xslt
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/gb.xml.xslt.*
%{_datadir}/%{name}/info/gb.xml.xslt.*

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 2.24.0-7
- 为 Magic 3.0 重建

* Tue Jul 28 2015 Liu Di <liudidi@gmail.com> - 2.24.0-6
- 为 Magic 3.0 重建

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.24.0-4
- rebuild against new libjpeg

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Marek Kasik <mkasik@redhat.com> - 2.24.0-2
- Rebuild (poppler-0.20.1)

* Fri May 25 2012 Tom Callaway <spot@fedoraproject.org> - 2.24.0-1
- update to 2.24.0

* Mon Feb 27 2012 Tom Callaway <spot@fedoraproject.org> - 2.23.1-10
- drop conflicting mimetype definitions from gambas2 (gambas3 has identical defs, except they invoke gbs3)
  Resolves bugzilla 797826

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.23.1-9
- Rebuild against PCRE 8.30
- Adjust to glib/poppler-features.h move into poppler-glib-devel sub-package

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.23.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.23.1-7
- Rebuild for new libpng

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> - 2.23.1-6
- rebuild(poppler)

* Fri Sep 30 2011 Marek Kasik <mkasik@redhat.com> - 2.23.1-5
- Rebuild (poppler-0.18.0)

* Mon Sep 19 2011 Marek Kasik <mkasik@redhat.com> - 2.23.1-4
- Rebuild (poppler-0.17.3)

* Mon Aug  8 2011 Marek Kasik <mkasik@redhat.com> - 2.23.1-3
- Use new version of constructor of class Links (poppler-0.17.0)

* Fri Jul 15 2011 Marek Kasik <mkasik@redhat.com> - 2.23.1-2
- Rebuild (poppler-0.17.0)

* Sat May 28 2011 Tom Callaway <spot@fedoraproject.org> - 2.23.1-1
- update to 2.23.1

* Fri Apr 29 2011 Dan Horák <dan@danny.cz> - 2.23.0-2
- switch to ExclusiveArch containing only little endian arches

* Wed Apr  6 2011 Tom Callaway <spot@fedoraproject.org> - 2.23.0-1
- update to 2.23.0

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 2.22.0-8
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Wed Mar 23 2011 Tom Callaway <spot@fedoraproject.org> - 2.22.0-7
- rebuild for new mysql

* Mon Mar 21 2011 Tom Callaway <spot@fedoraproject.org> - 2.22.0-6
- add Marek's patch to fix temporary usage
- use libv4l1 since linux/videodev.h is dead

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 2.22.0-5
- Rebuild (poppler-0.16.3)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 02 2011 Rex Dieter <rdieter@fedoraproject.org> - 2.22.0-3
- rebuild (poppler)

* Wed Dec 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.22.0-2
- rebuild (poppler)

* Fri Dec 10 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22.0-1
- update to 2.22.0

* Sat Nov 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.21.0-5
- rebuilt (poppler)

* Wed Oct  6 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.21.0-4
- rebuild again (poppler)

* Thu Aug 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.21.0-3
- rebuild (poppler)

* Mon Aug  2 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.21.0-2
- add gbw2 binary to script subpackage

* Mon Jul 26 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.21.0-1
- update to 2.21.0

* Wed Jul  7 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.20.2-3
- add license file to gambas-devel

* Wed May  5 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.20.2-2
- Rebuild against new poppler

* Wed Mar 17 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.20.2-1
- update to 2.20.2

* Tue Mar  9 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.20.1-1
- update to 2.20.1

* Mon Mar  1 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.20.0-1
- update to 2.20.0

* Wed Jan 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.19.0-2
- fix bz 513772, don't double package the sdl-sound libs

* Mon Jan  4 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.19.0-1
- update to 2.19.0
- add new "required" subpackages, -help and -examples

* Fri Nov 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.18.0-1
- update to 2.18.0

* Thu Oct 29 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.17.0-1
- update to 2.17.0

* Fri Sep 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.16.0-1
- update to 2.16.0

* Mon Aug 17 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.15.2-1
- update to 2.15.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14.0-1
- update to 2.14.0
- fix missing subpackages (bz 507496)

* Wed May 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.13.1-1
- update to 2.13.1

* Mon May 18 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.13.0-1
- update to 2.13.0

* Wed Mar 25 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.12.0-1
- update to 2.12.0

* Wed Mar  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11.1-4
- fix desktop file (bz 487805)

* Fri Feb 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11.1-3
- fix gcc44 compile

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.11.1-1
- update to 2.11.1

* Fri Jan 23 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.10.2-2
- rebuild for new mysql

* Mon Jan  5 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.10.2-1
- update to 2.10.2

* Sat Nov 29 2008 Caolán McNamara <caolanm@redhat.com> 2.9.0-2
- rebuild for dependencies

* Thu Oct 30 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.9.0-1
- Update to 2.9.0

* Wed Sep 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.8.2-1
- update to 2.8.2
- make gb-db-form subpackage (bz 461595)

* Thu Aug 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.8.1-1
- update to 2.8.1

* Fri Jun 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-1
- update to 2.7.0

* Wed May 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.0-1
- update to 2.6.0

* Mon Mar 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.1-2
- fix Source0 url
- drop Requires(post|postun) for shared-mime-info

* Wed Mar 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.1-1
- update to 2.4.1

* Sat Mar 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-5
- fix for new poppler

* Sat Mar 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-4
- rework examples listing to minimize rpmlint noise
- cleanup executable perms on debuginfo bits

* Mon Mar 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-3
- install with -p for timestamps
- don't own mime directory
- use macros everywhere relevant
- don't call update-desktop-database
- get rid of duplicate files
- patch out -O0 override
- patch out -Os override
- use AM_CXXFLAGS

* Fri Feb 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-2
- excludearch ppc64

* Thu Feb 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-1
- bump to 2.2.1

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-1.20080128-svn1043
- go to svn checkout for x86_64 support

* Thu Jan  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-1
- 2.0.0

* Tue Apr 10 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.9.48-1
- Lets try 1.9.48. Maybe it will work.

* Tue Oct 31 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.9.45-1
- revisit this package

* Tue Dec 20 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.9.22-1
- new package for gambas2
