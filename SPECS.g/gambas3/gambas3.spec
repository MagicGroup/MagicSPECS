Name:		gambas3
Summary:	IDE based on a basic interpreter with object extensions
Version:	3.5.2
Release:	2%{?dist}
License:	GPL+
Group:		Development/Tools
URL:		http://gambas.sourceforge.net/
Source0:	http://downloads.sourceforge.net/gambas/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
BuildRequires:	automake, autoconf, SDL-devel, SDL_mixer-devel
BuildRequires:	mysql-devel, postgresql-devel, gtk2-devel 
BuildRequires:	desktop-file-utils, gettext-devel, curl-devel, librsvg2-devel
BuildRequires:	poppler-devel, bzip2-devel, zlib-devel, pkgconfig
BuildRequires:	unixODBC-devel, libXtst-devel, sqlite-devel, mesa-libGL-devel
BuildRequires:	mesa-libGLU-devel, libpng-devel, libjpeg-devel, libxml2-devel
BuildRequires:	libxslt-devel, pcre-devel, SDL_image-devel, libICE-devel
BuildRequires:	libXcursor-devel, libXft-devel, libtool-ltdl-devel
BuildRequires:	xdg-utils, glibc-devel, libffi-devel
BuildRequires:	cairo-devel, qt4-devel, dbus-devel, libXcursor-devel
BuildRequires:	SDL_ttf-devel, sqlite2-devel, glew-devel
BuildRequires:	imlib2-devel, qt-webkit-devel, gsl-devel
BuildRequires:	libtool, ncurses-devel, gstreamer-plugins-base-devel >= 0.10.31
BuildRequires:	gtkglext-devel, gmime-devel, libgnome-keyring-devel
%if 0%{?fedora} >= 18
BuildRequires:	llvm-devel >= 3.3
%endif
# We need this since linux/videodev.h is dead
BuildRequires:	libv4l-devel
BuildRequires:	openssl-devel, gmp-devel, glew-devel
BuildRequires:	gstreamer1-plugins-base-devel gstreamer1-devel
BuildRequires:	openal-soft-devel, alure-devel

# Code is not endian clean.
ExcludeArch:	ppc ppc64
Patch1:		%{name}-3.2.0-nolintl.patch
Patch2:		%{name}-3.2.0-noliconv.patch
# Don't conflict with siginfo_t define
Patch5:		gambas3-3.1.1-linux-siginfo.patch

%description
Gambas3 is a free development environment based on a Basic interpreter
with object extensions, like Visual Basic (but it is NOT a clone !).
With Gambas3, you can quickly design your program GUI, access MySQL or
PostgreSQL databases, pilot KDE applications with DCOP, translate your
program into many languages, create network applications easily, and so
on...

%package runtime
Summary:	Runtime environment for Gambas3
Group:		Development/Tools
Provides:	%{name}-gb-gui = %{version}-%{release}
Obsoletes:	%{name}-gb-gui >= 3.3.3

%description runtime
Gambas3 is a free development environment based on a Basic interpreter
with object extensions, like Visual Basic. This package contains the 
runtime components necessary to run programs designed in Gambas3. 

%package devel
Summary:	Development environment for Gambas3
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description devel
The gambas3-devel package contains the tools needed to compile Gambas3
projects without having to install the complete development environment
(gambas3-ide).

%package scripter
Summary:	Scripter program that allows the creation of Gambas3 scripts
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}

%description scripter
This package includes the scripter program that allows the user to 
write script files in Gambas. 

%package ide
Summary:	The complete Gambas3 Development Environment
Group:		Development/Tools
License:	GPL+
Provides:	%{name} = %{version}-%{release}
Requires:	tar, gzip, rpm-build, gettext
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-gb-args = %{version}-%{release}
Requires:	%{name}-gb-clipper = %{version}-%{release}
Requires:	%{name}-gb-db = %{version}-%{release}
Requires:	%{name}-gb-db-form = %{version}-%{release}
Requires:	%{name}-gb-desktop = %{version}-%{release}
Requires:	%{name}-gb-eval-highlight = %{version}-%{release}
Requires:	%{name}-gb-form = %{version}-%{release}
Requires:	%{name}-gb-form-dialog = %{version}-%{release}
Requires:	%{name}-gb-form-mdi = %{version}-%{release}
Requires:	%{name}-gb-form-stock = %{version}-%{release}
Requires:	%{name}-gb-gtk = %{version}-%{release}
Requires:	%{name}-gb-image = %{version}-%{release}
Requires:	%{name}-gb-image-effect = %{version}-%{release}
Requires:	%{name}-gb-qt4 = %{version}-%{release}
Requires:	%{name}-gb-qt4-ext = %{version}-%{release}
Requires:	%{name}-gb-qt4-webkit = %{version}-%{release}
Requires:	%{name}-gb-settings = %{version}-%{release}

%description ide
This package includes the complete Gambas3 Development Environment and the 
database manager. Installing this package will give you all of the Gambas3 
components.

%package examples
Summary:	Example projects provided with Gambas3
Group:		Development/Tools
# Some of the examples are GPLv2+
# Database/PictureDatabase
# Games/RobotFindsKitten
# OpenGL/GambasGears
# Printing/Printing
# Everything else is GPL+
License:	GPL+ and GPLv2+
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-ide = %{version}-%{release}
# From http://gambasdoc.org/help/howto/package#t1
# It depends on "All gambas components."
Requires:	%{name}-gb-args = %{version}-%{release}
Requires:	%{name}-gb-cairo = %{version}-%{release}
Requires:	%{name}-gb-chart = %{version}-%{release}
Requires:	%{name}-gb-clipper = %{version}-%{release}
Requires:	%{name}-gb-complex = %{version}-%{release}
Requires:	%{name}-gb-compress = %{version}-%{release}
Requires:	%{name}-gb-crypt = %{version}-%{release}
Requires:	%{name}-gb-data = %{version}-%{release}
Requires:	%{name}-gb-db = %{version}-%{release}
Requires:	%{name}-gb-db-form = %{version}-%{release}
Requires:	%{name}-gb-db-mysql = %{version}-%{release}
Requires:	%{name}-gb-db-odbc = %{version}-%{release}
Requires:	%{name}-gb-db-postgresql = %{version}-%{release}
Requires:	%{name}-gb-db-sqlite2 = %{version}-%{release}
Requires:	%{name}-gb-db-sqlite3 = %{version}-%{release}
Requires:	%{name}-gb-dbus = %{version}-%{release}
Requires:	%{name}-gb-desktop = %{version}-%{release}
Requires:	%{name}-gb-desktop-gnome = %{version}-%{release}
Requires:	%{name}-gb-eval-highlight = %{version}-%{release}
Requires:	%{name}-gb-form = %{version}-%{release}
Requires:	%{name}-gb-form-dialog = %{version}-%{release}
Requires:	%{name}-gb-form-mdi = %{version}-%{release}
Requires:	%{name}-gb-form-stock = %{version}-%{release}
Requires:	%{name}-gb-gmp = %{version}-%{release}
Requires:	%{name}-gb-gsl = %{version}-%{release}
Requires:	%{name}-gb-gtk = %{version}-%{release}
Requires:	%{name}-gb-gtk-opengl = %{version}-%{release}
Requires:	%{name}-gb-httpd = %{version}-%{release}
Requires:	%{name}-gb-image = %{version}-%{release}
Requires:	%{name}-gb-image-effect = %{version}-%{release}
Requires:	%{name}-gb-image-imlib = %{version}-%{release}
Requires:	%{name}-gb-image-io = %{version}-%{release}
%if 0%{?fedora} >= 18
Requires:	%{name}-gb-jit = %{version}-%{release}
%endif
Requires:	%{name}-gb-libxml = %{version}-%{release}
Requires:	%{name}-gb-logging = %{version}-%{release}
Requires:	%{name}-gb-map = %{version}-%{release}
Requires:	%{name}-gb-media = %{version}-%{release}
Requires:	%{name}-gb-memcached = %{version}-%{release}
Requires:	%{name}-gb-mime = %{version}-%{release}
Requires:	%{name}-gb-mysql = %{version}-%{release}
Requires:	%{name}-gb-ncurses = %{version}-%{release}
Requires:	%{name}-gb-net = %{version}-%{release}
Requires:	%{name}-gb-net-curl = %{version}-%{release}
Requires:	%{name}-gb-net-pop3 = %{version}-%{release}
Requires:	%{name}-gb-net-smtp = %{version}-%{release}
Requires:	%{name}-gb-openal = %{version}-%{release}
Requires:	%{name}-gb-opengl = %{version}-%{release}
Requires:	%{name}-gb-opengl-glu = %{version}-%{release}
Requires:	%{name}-gb-opengl-glsl = %{version}-%{release}
Requires:	%{name}-gb-opengl-sge = %{version}-%{release}
Requires:	%{name}-gb-openssl = %{version}-%{release}
Requires:	%{name}-gb-option = %{version}-%{release}
Requires:	%{name}-gb-pcre = %{version}-%{release}
Requires:	%{name}-gb-pdf = %{version}-%{release}
Requires:	%{name}-gb-qt4 = %{version}-%{release}
Requires:	%{name}-gb-qt4-ext = %{version}-%{release}
Requires:	%{name}-gb-qt4-webkit = %{version}-%{release}
Requires:	%{name}-gb-qt4-opengl = %{version}-%{release}
Requires:	%{name}-gb-report = %{version}-%{release}
Requires:	%{name}-gb-sdl = %{version}-%{release}
Requires:	%{name}-gb-sdl-sound = %{version}-%{release}
Requires:	%{name}-gb-settings = %{version}-%{release}
Requires:	%{name}-gb-signal = %{version}-%{release}
Requires:	%{name}-gb-v4l = %{version}-%{release}
Requires:	%{name}-gb-vb = %{version}-%{release}
Requires:	%{name}-gb-xml = %{version}-%{release}
Requires:	%{name}-gb-xml-html = %{version}-%{release}
Requires:	%{name}-gb-xml-rpc = %{version}-%{release}
Requires:	%{name}-gb-xml-xslt = %{version}-%{release}
Requires:	%{name}-gb-web = %{version}-%{release}

%description examples
This package includes all the example projects provided with Gambas3.

%package gb-args
Summary:	Gambas3 component package for args
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-args
%{summary}

%package gb-cairo
Summary:	Gambas3 component package for cairo
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-cairo
%{summary}
	
%package gb-chart
Summary:	Gambas3 component package for chart
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-form = %{version}-%{release}

%description gb-chart
%{summary}

%package gb-clipper
Summary:	Gambas3 component package for clipper
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-clipper
%{summary}

%package gb-complex
Summary:	Gambas3 component package for complex
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-complex
%{summary}

%package gb-compress
Summary:	Gambas3 component package for compress
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-compress
%{summary}

%package gb-crypt
Summary:	Gambas3 component package for crypt
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-crypt
%{summary}

%package gb-data
Summary:	Gambas3 component package for data
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-data
%{summary}

%package gb-db
Summary:	Gambas3 component package for db
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-db
%{summary}

%package gb-db-form
Summary:	Gambas3 component package for db-form
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-db = %{version}-%{release}
Requires:	%{name}-gb-form = %{version}-%{release}

%description gb-db-form
%{summary}

%package gb-db-mysql
Summary:	Gambas3 component package for db-mysql
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-db =	%{version}-%{release}

%description gb-db-mysql
%{summary}

%package gb-db-odbc
Summary:	Gambas3 component package for db-odbc
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-db =	%{version}-%{release}

%description gb-db-odbc
%{summary}

%package gb-db-postgresql
Summary:	Gambas3 component package for db-postgresql
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-db =	%{version}-%{release}

%description gb-db-postgresql
%{summary}

%package gb-db-sqlite2
Summary:	Gambas3 component package for db-sqlite2
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-db =	%{version}-%{release}

%description gb-db-sqlite2
%{summary}

%package gb-db-sqlite3
Summary:	Gambas3 component package for db-sqlite3
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-db =	%{version}-%{release}

%description gb-db-sqlite3
%{summary}

%package gb-desktop
Summary:	Gambas3 component package for desktop
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-desktop
%{summary}

%package gb-desktop-gnome
Summary:	Gambas3 component package for GNOME Desktop
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-desktop = %{version}-%{release}

%description gb-desktop-gnome
%{summary}

%package gb-dbus
Summary:	Gambas3 component package for dbus
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-dbus
%{summary}

%package gb-eval-highlight
Summary:	Gambas3 component package for eval highlight
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-eval-highlight
%{summary}

%package gb-form
Summary:	Gambas3 component package for form
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-form
%{summary}

%package gb-form-dialog
Summary:	Gambas3 component package for form-dialog
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-form = %{version}-%{release}

%description gb-form-dialog
%{summary}

%package gb-form-mdi
Summary:	Gambas3 component package for form-mdi
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-form = %{version}-%{release}
Requires:	%{name}-gb-settings = %{version}-%{release}

%description gb-form-mdi
%{summary}

%package gb-form-stock
Summary:	Gambas3 component package for form-stock
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-form-stock
%{summary}

%package gb-gmp
Summary:	Gambas3 component package for gmp
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-gmp
%{summary}

%package gb-gsl
Summary:	Gambas3 component package for gsl
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-gsl
%{summary}

%package gb-gtk
Summary:	Gambas3 component package for gtk
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-gtk
%{summary}

%package gb-gtk-opengl
Summary:	Gambas3 component package for gtk-opengl
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-gtk = %{version}-%{release}
Requires:	%{name}-gb-opengl = %{version}-%{release}

%description gb-gtk-opengl
%{summary}

%package gb-httpd
Summary:	Gambas3 component package for httpd
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-httpd
%{summary}.

%package gb-image 
Summary:	Gambas3 component package for image 
License:	GPLv2 or QPL
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-image 
%{summary}

%package gb-image-effect
Summary:	Gambas3 component package for image-effect
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-image = %{version}-%{release}

%description gb-image-effect
%{summary}

%package gb-image-imlib
Summary:	Gambas3 component package for image-imlib
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-image = %{version}-%{release}

%description gb-image-imlib
%{summary}

%package gb-image-io
Summary:	Gambas3 component package for image-io
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-image = %{version}-%{release}

%description gb-image-io
%{summary}

%if 0%{?fedora} >= 18
%package gb-jit
Summary:	Gambas3 component package for jit
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-jit
%{summary}
%endif

%package gb-libxml
Summary:	Gambas3 component package for libxml
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-libxml
%{summary}

%package gb-logging
Summary:	Gambas3 component package for logging
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-logging
%{summary}

%package gb-map
Summary:	Gambas3 component package for map
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-map
%{summary}.

%package gb-media
Summary:	Gambas3 component package for media
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-media
%{summary}

%package gb-memcached
Summary:	Gambas3 component package for memcached
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-memcached
%{summary}.

%package gb-mime
Summary:	Gambas3 component package for mime
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-mime
%{summary}

%package gb-mysql
Summary:	Gambas3 component package for mysql
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-db = %{version}-%{release}
Requires:	%{name}-gb-db-mysql = %{version}-%{release}

%description gb-mysql
%{summary}

%package gb-ncurses
Summary:	Gambas3 component package for ncurses
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-ncurses
%{summary}

%package gb-net
Summary:	Gambas3 component package for net
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-net
%{summary}

%package gb-net-curl
Summary:	Gambas3 component package for net.curl
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-net = %{version}-%{release}

%description gb-net-curl
%{summary}

%package gb-net-pop3
Summary:	Gambas3 component package for net-pop3
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-net = %{version}-%{release}
Requires:	%{name}-gb-mime = %{version}-%{release}

%description gb-net-pop3
%{summary}

%package gb-net-smtp 
Summary:	Gambas3 component package for net-smtp 
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-net-smtp
%{summary}

%package gb-openal
Summary:	Gambas3 component package for openal
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-openal
%{summary}

%package gb-opengl 
Summary:	Gambas3 component package for opengl 
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-opengl 
%{summary}

%package gb-opengl-glu
Summary:	Gambas3 component package for opengl-glu
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-opengl = %{version}-%{release}

%description gb-opengl-glu
%{summary}

%package gb-opengl-glsl
Summary:	Gambas3 component package for opengl-glsl
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-opengl = %{version}-%{release}

%description gb-opengl-glsl
%{summary}

%package gb-opengl-sge
Summary:	Gambas3 component package for opengl-sge
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-opengl = %{version}-%{release}

%description gb-opengl-sge
%{summary}

%package gb-openssl
Summary:	Gambas3 component package for openssl
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-openssl
%{summary}

%package gb-option
Summary:	Gambas3 component package for option
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-option
%{summary}

%package gb-pcre 
Summary:	Gambas3 component package for pcre 
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-pcre 
%{summary}

%package gb-pdf
Summary:	Gambas3 component package for pdf
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-pdf
%{summary}

%package gb-qt4
Summary:	Gambas3 component package for qt4
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-qt4
%{summary}

%package gb-qt4-ext
Summary:	Gambas3 component package for qt4.ext
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-qt4 = %{version}-%{release}

%description gb-qt4-ext
%{summary}

%package gb-qt4-opengl
Summary:	Gambas3 component package for qt4-opengl
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-qt4 = %{version}-%{release}
Requires:	%{name}-gb-opengl = %{version}-%{release}

%description gb-qt4-opengl
%{summary}

%package gb-qt4-webkit
Summary:	Gambas3 component package for qt4-webkit
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-qt4 = %{version}-%{release}

%description gb-qt4-webkit
%{summary}

%package gb-report
Summary:	Gambas3 component package for report
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-report
%{summary}

%package gb-sdl
Summary:	Gambas3 component package for sdl
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	dejavu-sans-fonts

%description gb-sdl
%{summary}

%package gb-sdl-sound
Summary:	Gambas3 component package for sdl-sound
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-sdl-sound
%{summary}

%package gb-settings
Summary:	Gambas3 component package for settings
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-settings
%{summary}

%package gb-signal
Summary:	Gambas3 component package for signal
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-signal
%{summary}

%package gb-v4l 
Summary:	Gambas3 component package for v4l 
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-v4l 
%{summary}

%package gb-vb
Summary:	Gambas3 component package for vb
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-vb
%{summary}

%package gb-web
Summary:	Gambas3 component package for web
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-web
%{summary}

%package gb-xml
Summary:	Gambas3 component package for xml
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-xml
%{summary}

%package gb-xml-html
Summary:	Gambas3 component package for xml.html
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-xml = %{version}-%{release}

%description gb-xml-html
%{summary}

%package gb-xml-rpc
Summary:	Gambas3 component package for xml.rpc
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-xml = %{version}-%{release}

%description gb-xml-rpc
%{summary}

%package gb-xml-xslt
Summary:	Gambas3 component package for xml.xslt
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-xml = %{version}-%{release}

%description gb-xml-xslt
%{summary}

%prep
%setup -q
%patch1 -p1 -b .nolintl
%patch2 -p1 -b .noliconv
# %%patch5 -p1 -b .linux-siginfo
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
chmod -x main/gbx/gbx_local.h
chmod -x main/gbx/gbx_subr_file.c
chmod -x gb.qt4/src/CContainer.cpp
chmod -x main/lib/option/getoptions.*
chmod -x main/lib/option/main.c

%build
# Gambas can't deal with -Wp,-D_FORTIFY_SOURCE=2
MY_CFLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//g'`
%configure \
	--datadir="%{_datadir}" \
	--enable-intl \
	--enable-conv \
	--enable-qt4 \
	--enable-kde \
	--enable-net \
	--enable-curl \
	--enable-postgresql \
	--enable-mysql \
	--enable-sqlite3 \
	--enable-sdl \
	--enable-vb \
	--enable-pdf \
	--with-bzlib2-libraries=%{_libdir} \
	--with-crypt-libraries=%{_libdir} \
	--with-curl-libraries=%{_libdir} \
	--with-desktop-libraries=%{_libdir} \
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
	--with-qt4-libraries=%{_libdir} \
	--with-qtopengl-libraries=%{_libdir} \
	--with-sdl-libraries=%{_libdir} \
	--with-sdl_sound-libraries=%{_libdir} \
	--with-smtp-libraries=%{_libdir} \
	--with-sqlite2-libraries=%{_libdir} \
	--with-sqlite3-libraries=%{_libdir} \
	--with-v4l-libraries=%{_libdir} \
	--with-xml-libraries=%{_libdir} \
	--with-xslt-libraries=%{_libdir} \
	--with-zlib-libraries=%{_libdir} \
	AM_CFLAGS="$MY_CFLAGS" AM_CXXFLAGS="$MY_CFLAGS"
# rpath removal
for i in main; do
	sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' $i/libtool
	sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' $i/libtool
done
%{__make} LIBTOOL=%{_bindir}/libtool %{?_smp_mflags}

%install
export PATH=%{buildroot}%{_bindir}:$PATH
make LIBTOOL=%{_bindir}/libtool DESTDIR=%{buildroot} INSTALL="install -p" install
# Yes, I know. Normally we'd nuke the .la files, but Gambas is retar^Wspecial.
# rm -rf %%{buildroot}%%{_libdir}/%%{name}/*.la
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_datadir}/applications
install -m0644 -p ./app/src/%{name}/.icon.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications	\
  %{SOURCE1}

# get the buildroot out of the examples
for i in `grep -lr "%{buildroot}" %{buildroot}%{_datadir}/%{name}/examples/`; 
do
  sed -i "s|%{buildroot}||g" $i; 
done

# Get the SVN noise out of the main tree
find %{buildroot}%{_datadir}/%{name}/ -type d -name .svn -exec rm -rf {} 2>/dev/null ';' || :

# Upstream says we don't need those files. Not sure why they install them then. :/
rm -rf %{buildroot}%{_libdir}/%{name}/gb.la %{buildroot}%{_libdir}/%{name}/gb.so*

# No need for the static libs
rm -rf %{buildroot}%{_libdir}/%{name}/*.a

# Replace the bundled font with a symlink to our system copy
pushd %{buildroot}%{_datadir}/%{name}/gb.sdl/
rm -f DejaVuSans.ttf
ln -s ../../fonts/dejavu/DejaVuSans.ttf DejaVuSans.ttf
popd

chmod -x %{buildroot}%{_datadir}/%{name}/gb.sdl/LICENSE

# Mime types.
mkdir -p %{buildroot}%{_datadir}/mime/packages/
install -m 0644 -p app/mime/application-x-gambasscript.xml %{buildroot}%{_datadir}/mime/packages/
install -m 0644 -p main/mime/application-x-gambas3.xml %{buildroot}%{_datadir}/mime/packages/

%post runtime
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun runtime
update-mime-database %{_datadir}/mime &> /dev/null || :

%post scripter
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun scripter
update-mime-database %{_datadir}/mime &> /dev/null || :

%files runtime
%doc COPYING INSTALL README
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/gb.component
%{_libdir}/%{name}/gb.debug.*
%{_libdir}/%{name}/gb.draw.*
%{_libdir}/%{name}/gb.eval.*
%{_libdir}/%{name}/gb.geom.*
%{_libdir}/%{name}/gb.gui.*
%{_bindir}/gbr3
%{_bindir}/gbx3
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/*.desktop
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/info/
%{_datadir}/%{name}/info/gb.debug.*
%{_datadir}/%{name}/info/gb.eval.*
%{_datadir}/%{name}/info/gb.gui.*
%{_datadir}/%{name}/info/gb.info
%{_datadir}/%{name}/info/gb.list
%dir %{_datadir}/%{name}/icons/
%{_datadir}/%{name}/icons/application-x-gambas3.png
%{_datadir}/mime/packages/application-x-gambas3.xml
%{_datadir}/%{name}/icons/application-x-gambasserverpage.png

%files devel
%doc COPYING
%{_bindir}/gbc3
%{_bindir}/gba3
%{_bindir}/gbi3

%files scripter
%{_bindir}/gbs3
%{_bindir}/gbs3.gambas
%{_bindir}/gbw3
%{_datadir}/%{name}/icons/application-x-gambasscript.png
%{_datadir}/mime/packages/application-x-gambasscript.xml

%files ide
%{_bindir}/%{name}
%{_bindir}/%{name}.gambas
# The IDE crashes if it can't find this directory.
# Since -examples Requires: -ide, this is okay.
%dir %{_datadir}/%{name}/examples/

%files examples
%dir %{_datadir}/%{name}/examples/Automation/
%dir %{_datadir}/%{name}/examples/Basic/
%dir %{_datadir}/%{name}/examples/Control/
%dir %{_datadir}/%{name}/examples/Database/
%dir %{_datadir}/%{name}/examples/Drawing/
%dir %{_datadir}/%{name}/examples/Games/
%dir %{_datadir}/%{name}/examples/Image/
%dir %{_datadir}/%{name}/examples/Misc/
%dir %{_datadir}/%{name}/examples/Multimedia/
%dir %{_datadir}/%{name}/examples/Networking/
%dir %{_datadir}/%{name}/examples/OpenGL/
%dir %{_datadir}/%{name}/examples/Printing/
%dir %{_datadir}/%{name}/examples/Automation/DBusExplorer/
%{_datadir}/%{name}/examples/Automation/DBusExplorer/dbus*.png
%{_datadir}/%{name}/examples/Automation/DBusExplorer/DBusExplorer.gambas
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.directory
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.gambas/
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.hidden
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.icon.png
%{_datadir}/%{name}/examples/Automation/DBusExplorer/method.png
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.project
%{_datadir}/%{name}/examples/Automation/DBusExplorer/property.png
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.settings
%{_datadir}/%{name}/examples/Automation/DBusExplorer/signal.png
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.src/
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.startup

%dir %{_datadir}/%{name}/examples/Basic/Blights/
%dir %{_datadir}/%{name}/examples/Basic/Blights/.lang/
%{_datadir}/%{name}/examples/Basic/Blights/.directory
%{_datadir}/%{name}/examples/Basic/Blights/.gambas/
%{_datadir}/%{name}/examples/Basic/Blights/.hidden
%{_datadir}/%{name}/examples/Basic/Blights/.icon*
%{_datadir}/%{name}/examples/Basic/Blights/.project
%{_datadir}/%{name}/examples/Basic/Blights/.src/
%{_datadir}/%{name}/examples/Basic/Blights/.startup
%{_datadir}/%{name}/examples/Basic/Blights/Blights.gambas
%{_datadir}/%{name}/examples/Basic/Blights/ampoule.png
%{_datadir}/%{name}/examples/Basic/Blights/bloff.xpm
%{_datadir}/%{name}/examples/Basic/Blights/blon.xpm

%dir %{_datadir}/%{name}/examples/Basic/Collection/
%dir %{_datadir}/%{name}/examples/Basic/Collection/.lang/
%{_datadir}/%{name}/examples/Basic/Collection/.directory
%{_datadir}/%{name}/examples/Basic/Collection/.gambas/
%{_datadir}/%{name}/examples/Basic/Collection/.hidden
%{_datadir}/%{name}/examples/Basic/Collection/.icon*
%{_datadir}/%{name}/examples/Basic/Collection/.project
%{_datadir}/%{name}/examples/Basic/Collection/.startup
%{_datadir}/%{name}/examples/Basic/Collection/.src/
%{_datadir}/%{name}/examples/Basic/Collection/Collection.gambas
%{_datadir}/%{name}/examples/Basic/Collection/collection.png

%dir %{_datadir}/%{name}/examples/Basic/DragNDrop/
%{_datadir}/%{name}/examples/Basic/DragNDrop/.directory
%{_datadir}/%{name}/examples/Basic/DragNDrop/.gambas/
%{_datadir}/%{name}/examples/Basic/DragNDrop/.hidden
%{_datadir}/%{name}/examples/Basic/DragNDrop/.icon*
%{_datadir}/%{name}/examples/Basic/DragNDrop/.project
%{_datadir}/%{name}/examples/Basic/DragNDrop/.startup
%{_datadir}/%{name}/examples/Basic/DragNDrop/DragNDrop.gambas
%{_datadir}/%{name}/examples/Basic/DragNDrop/.src/
%{_datadir}/%{name}/examples/Basic/DragNDrop/drop.png

%dir %{_datadir}/%{name}/examples/Basic/Object/
%dir %{_datadir}/%{name}/examples/Basic/Object/.lang/
%{_datadir}/%{name}/examples/Basic/Object/.directory
%{_datadir}/%{name}/examples/Basic/Object/.gambas/
%{_datadir}/%{name}/examples/Basic/Object/.hidden
%{_datadir}/%{name}/examples/Basic/Object/.icon*
%{_datadir}/%{name}/examples/Basic/Object/.project
%{_datadir}/%{name}/examples/Basic/Object/.startup
%{_datadir}/%{name}/examples/Basic/Object/.src/
%{_datadir}/%{name}/examples/Basic/Object/Object.gambas
%{_datadir}/%{name}/examples/Basic/Object/object.png

%dir %{_datadir}/%{name}/examples/Basic/Timer/
%dir %{_datadir}/%{name}/examples/Basic/Timer/.lang/
%{_datadir}/%{name}/examples/Basic/Timer/.directory
%{_datadir}/%{name}/examples/Basic/Timer/.gambas/
%{_datadir}/%{name}/examples/Basic/Timer/.hidden
%{_datadir}/%{name}/examples/Basic/Timer/.icon*
%{_datadir}/%{name}/examples/Basic/Timer/.project
%{_datadir}/%{name}/examples/Basic/Timer/.startup
%{_datadir}/%{name}/examples/Basic/Timer/.src/
%{_datadir}/%{name}/examples/Basic/Timer/Timer.gambas
%{_datadir}/%{name}/examples/Basic/Timer/timer.png

%dir %{_datadir}/%{name}/examples/Control/ArrayOfControls/
%dir %{_datadir}/%{name}/examples/Control/ArrayOfControls/.lang/
%{_datadir}/%{name}/examples/Control/ArrayOfControls/.directory
%{_datadir}/%{name}/examples/Control/ArrayOfControls/.gambas/
%{_datadir}/%{name}/examples/Control/ArrayOfControls/.hidden
%{_datadir}/%{name}/examples/Control/ArrayOfControls/.icon*
%{_datadir}/%{name}/examples/Control/ArrayOfControls/.project
%{_datadir}/%{name}/examples/Control/ArrayOfControls/.startup
%{_datadir}/%{name}/examples/Control/ArrayOfControls/.src/
%{_datadir}/%{name}/examples/Control/ArrayOfControls/green1.png
%{_datadir}/%{name}/examples/Control/ArrayOfControls/green.png
%{_datadir}/%{name}/examples/Control/ArrayOfControls/phone.png
%{_datadir}/%{name}/examples/Control/ArrayOfControls/red1.png
%{_datadir}/%{name}/examples/Control/ArrayOfControls/red.png
%{_datadir}/%{name}/examples/Control/ArrayOfControls/ArrayOfControls.gambas

%dir %{_datadir}/%{name}/examples/Control/Embedder/
%dir %{_datadir}/%{name}/examples/Control/Embedder/.lang/
%{_datadir}/%{name}/examples/Control/Embedder/.directory
%{_datadir}/%{name}/examples/Control/Embedder/.gambas/
%{_datadir}/%{name}/examples/Control/Embedder/.hidden
%{_datadir}/%{name}/examples/Control/Embedder/.icon*
%{_datadir}/%{name}/examples/Control/Embedder/.project
%{_datadir}/%{name}/examples/Control/Embedder/.settings
%{_datadir}/%{name}/examples/Control/Embedder/.startup
%{_datadir}/%{name}/examples/Control/Embedder/.src/
%{_datadir}/%{name}/examples/Control/Embedder/Embedder.gambas
%{_datadir}/%{name}/examples/Control/Embedder/embedder.png

%dir %{_datadir}/%{name}/examples/Control/HighlightEditor/
%dir %{_datadir}/%{name}/examples/Control/HighlightEditor/.lang/
%{_datadir}/%{name}/examples/Control/HighlightEditor/.directory
%{_datadir}/%{name}/examples/Control/HighlightEditor/.gambas/
%{_datadir}/%{name}/examples/Control/HighlightEditor/.hidden
%{_datadir}/%{name}/examples/Control/HighlightEditor/.icon*
%{_datadir}/%{name}/examples/Control/HighlightEditor/.project
%{_datadir}/%{name}/examples/Control/HighlightEditor/.startup
%{_datadir}/%{name}/examples/Control/HighlightEditor/.src/
%{_datadir}/%{name}/examples/Control/HighlightEditor/HighlightEditor.gambas
%{_datadir}/%{name}/examples/Control/HighlightEditor/download.html
%{_datadir}/%{name}/examples/Control/HighlightEditor/editor.png

%dir %{_datadir}/%{name}/examples/Control/MapView/
%{_datadir}/%{name}/examples/Control/MapView/.directory
%{_datadir}/%{name}/examples/Control/MapView/.gambas/
%{_datadir}/%{name}/examples/Control/MapView/.hidden/
%{_datadir}/%{name}/examples/Control/MapView/.icon*
%{_datadir}/%{name}/examples/Control/MapView/.project
%{_datadir}/%{name}/examples/Control/MapView/.src/
%{_datadir}/%{name}/examples/Control/MapView/.startup
%{_datadir}/%{name}/examples/Control/MapView/MapView.gambas

%dir %{_datadir}/%{name}/examples/Control/TextEdit/
%dir %{_datadir}/%{name}/examples/Control/TextEdit/.lang/
%{_datadir}/%{name}/examples/Control/TextEdit/.directory
%{_datadir}/%{name}/examples/Control/TextEdit/.gambas/
%{_datadir}/%{name}/examples/Control/TextEdit/.hidden
%{_datadir}/%{name}/examples/Control/TextEdit/.icon*
%{_datadir}/%{name}/examples/Control/TextEdit/.project
%{_datadir}/%{name}/examples/Control/TextEdit/.startup
%{_datadir}/%{name}/examples/Control/TextEdit/.src/
%{_datadir}/%{name}/examples/Control/TextEdit/TextEdit.gambas
%{_datadir}/%{name}/examples/Control/TextEdit/edit.png
%{_datadir}/%{name}/examples/Control/TextEdit/text.html

%dir %{_datadir}/%{name}/examples/Control/TreeView/
%dir %{_datadir}/%{name}/examples/Control/TreeView/.lang/
%{_datadir}/%{name}/examples/Control/TreeView/.directory
%{_datadir}/%{name}/examples/Control/TreeView/.gambas/
%{_datadir}/%{name}/examples/Control/TreeView/.hidden
%{_datadir}/%{name}/examples/Control/TreeView/.icon*
%{_datadir}/%{name}/examples/Control/TreeView/.project
%{_datadir}/%{name}/examples/Control/TreeView/.startup
%{_datadir}/%{name}/examples/Control/TreeView/.src/
%{_datadir}/%{name}/examples/Control/TreeView/Female.png
%{_datadir}/%{name}/examples/Control/TreeView/Male.png
%{_datadir}/%{name}/examples/Control/TreeView/treeview.png
%{_datadir}/%{name}/examples/Control/TreeView/TreeView.gambas

%dir %{_datadir}/%{name}/examples/Control/Wizard/
%dir %{_datadir}/%{name}/examples/Control/Wizard/.lang/
%{_datadir}/%{name}/examples/Control/Wizard/.directory
%{_datadir}/%{name}/examples/Control/Wizard/.gambas/
%{_datadir}/%{name}/examples/Control/Wizard/.hidden
%{_datadir}/%{name}/examples/Control/Wizard/.icon*
%{_datadir}/%{name}/examples/Control/Wizard/.project
%{_datadir}/%{name}/examples/Control/Wizard/.startup
%{_datadir}/%{name}/examples/Control/Wizard/.src/
%{_datadir}/%{name}/examples/Control/Wizard/Wizard.gambas
%{_datadir}/%{name}/examples/Control/Wizard/wizard.png

%dir %{_datadir}/%{name}/examples/Database/Database/
%dir %{_datadir}/%{name}/examples/Database/Database/.lang/
%{_datadir}/%{name}/examples/Database/Database/.component
%{_datadir}/%{name}/examples/Database/Database/.directory
%{_datadir}/%{name}/examples/Database/Database/.gambas/
%{_datadir}/%{name}/examples/Database/Database/.hidden
%{_datadir}/%{name}/examples/Database/Database/.icon*
%{_datadir}/%{name}/examples/Database/Database/.project
%{_datadir}/%{name}/examples/Database/Database/.startup
%{_datadir}/%{name}/examples/Database/Database/.src/
%{_datadir}/%{name}/examples/Database/Database/Database.gambas
%{_datadir}/%{name}/examples/Database/Database/database.png

%dir %{_datadir}/%{name}/examples/Database/MySQLExample/
%dir %{_datadir}/%{name}/examples/Database/MySQLExample/.lang/
%{_datadir}/%{name}/examples/Database/MySQLExample/.action
%{_datadir}/%{name}/examples/Database/MySQLExample/.directory
%{_datadir}/%{name}/examples/Database/MySQLExample/.gambas/
%{_datadir}/%{name}/examples/Database/MySQLExample/.hidden
%{_datadir}/%{name}/examples/Database/MySQLExample/.icon*
%{_datadir}/%{name}/examples/Database/MySQLExample/icons/
%{_datadir}/%{name}/examples/Database/MySQLExample/MySQLExample.gambas
%{_datadir}/%{name}/examples/Database/MySQLExample/.project
%{_datadir}/%{name}/examples/Database/MySQLExample/.src/
%{_datadir}/%{name}/examples/Database/MySQLExample/.startup

%dir %{_datadir}/%{name}/examples/Database/PictureDatabase/
%dir %{_datadir}/%{name}/examples/Database/PictureDatabase/.lang/
%{_datadir}/%{name}/examples/Database/PictureDatabase/.directory
%{_datadir}/%{name}/examples/Database/PictureDatabase/.gambas/
%{_datadir}/%{name}/examples/Database/PictureDatabase/.hidden
%{_datadir}/%{name}/examples/Database/PictureDatabase/.icon*
%{_datadir}/%{name}/examples/Database/PictureDatabase/.project
%{_datadir}/%{name}/examples/Database/PictureDatabase/.startup
%{_datadir}/%{name}/examples/Database/PictureDatabase/.src/
%{_datadir}/%{name}/examples/Database/PictureDatabase/Images/
%{_datadir}/%{name}/examples/Database/PictureDatabase/PictureDatabase.gambas

%dir %{_datadir}/%{name}/examples/Drawing/AnalogWatch/
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.directory
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.gambas/
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.hidden
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.icon*
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.project
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.startup
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/AnalogWatch.gambas
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.src/
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/timer.png

%dir %{_datadir}/%{name}/examples/Drawing/Barcode/
%dir %{_datadir}/%{name}/examples/Drawing/Barcode/.lang/
%{_datadir}/%{name}/examples/Drawing/Barcode/.directory
%{_datadir}/%{name}/examples/Drawing/Barcode/.gambas/
%{_datadir}/%{name}/examples/Drawing/Barcode/.hidden
%{_datadir}/%{name}/examples/Drawing/Barcode/.icon*
%{_datadir}/%{name}/examples/Drawing/Barcode/.project
%{_datadir}/%{name}/examples/Drawing/Barcode/.settings
%{_datadir}/%{name}/examples/Drawing/Barcode/.startup
%{_datadir}/%{name}/examples/Drawing/Barcode/.src/
%{_datadir}/%{name}/examples/Drawing/Barcode/Barcode.gambas
%{_datadir}/%{name}/examples/Drawing/Barcode/barcode.png

%dir %{_datadir}/%{name}/examples/Drawing/Chart/
%dir %{_datadir}/%{name}/examples/Drawing/Chart/.lang/
%{_datadir}/%{name}/examples/Drawing/Chart/.directory
%{_datadir}/%{name}/examples/Drawing/Chart/.gambas/
%{_datadir}/%{name}/examples/Drawing/Chart/.hidden
%{_datadir}/%{name}/examples/Drawing/Chart/.icon*
%{_datadir}/%{name}/examples/Drawing/Chart/.project
%{_datadir}/%{name}/examples/Drawing/Chart/.src/
%{_datadir}/%{name}/examples/Drawing/Chart/.startup
%{_datadir}/%{name}/examples/Drawing/Chart/Chart.gambas
%{_datadir}/%{name}/examples/Drawing/Chart/graph.png

%dir %{_datadir}/%{name}/examples/Drawing/Clock/
%dir %{_datadir}/%{name}/examples/Drawing/Clock/.lang/
%{_datadir}/%{name}/examples/Drawing/Clock/.directory
%{_datadir}/%{name}/examples/Drawing/Clock/.gambas/
%{_datadir}/%{name}/examples/Drawing/Clock/.hidden
%{_datadir}/%{name}/examples/Drawing/Clock/.icon*
%{_datadir}/%{name}/examples/Drawing/Clock/.project
%{_datadir}/%{name}/examples/Drawing/Clock/.startup
%{_datadir}/%{name}/examples/Drawing/Clock/.src/
%{_datadir}/%{name}/examples/Drawing/Clock/Clock.gambas
%{_datadir}/%{name}/examples/Drawing/Clock/img/

%dir %{_datadir}/%{name}/examples/Drawing/Fractal/
%dir %{_datadir}/%{name}/examples/Drawing/Fractal/.lang
%{_datadir}/%{name}/examples/Drawing/Fractal/.directory
%{_datadir}/%{name}/examples/Drawing/Fractal/.gambas/
%{_datadir}/%{name}/examples/Drawing/Fractal/.icon*
%{_datadir}/%{name}/examples/Drawing/Fractal/.project
%{_datadir}/%{name}/examples/Drawing/Fractal/.startup
%{_datadir}/%{name}/examples/Drawing/Fractal/.src/
%{_datadir}/%{name}/examples/Drawing/Fractal/Fractal.gambas
%{_datadir}/%{name}/examples/Drawing/Fractal/icon.png
%{_datadir}/%{name}/examples/Drawing/Fractal/rose.jpg

%dir %{_datadir}/%{name}/examples/Drawing/Gravity/
%dir %{_datadir}/%{name}/examples/Drawing/Gravity/.lang/
%{_datadir}/%{name}/examples/Drawing/Gravity/.directory
%{_datadir}/%{name}/examples/Drawing/Gravity/.gambas/
%{_datadir}/%{name}/examples/Drawing/Gravity/.hidden
%{_datadir}/%{name}/examples/Drawing/Gravity/.icon*
%{_datadir}/%{name}/examples/Drawing/Gravity/.project
%{_datadir}/%{name}/examples/Drawing/Gravity/.startup
%{_datadir}/%{name}/examples/Drawing/Gravity/.src/
%{_datadir}/%{name}/examples/Drawing/Gravity/Gravity.gambas
%{_datadir}/%{name}/examples/Drawing/Gravity/gravity.png

%dir %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/
%dir %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.lang/
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.directory
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.gambas/
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.hidden
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.icon*
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.project
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.startup
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.src/
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/OnScreenDisplay.gambas
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/icon.png

%dir %{_datadir}/%{name}/examples/Drawing/Painting/
%dir %{_datadir}/%{name}/examples/Drawing/Painting/.lang
%{_datadir}/%{name}/examples/Drawing/Painting/.directory
%{_datadir}/%{name}/examples/Drawing/Painting/.gambas/
%{_datadir}/%{name}/examples/Drawing/Painting/.hidden
%{_datadir}/%{name}/examples/Drawing/Painting/.icon*
%{_datadir}/%{name}/examples/Drawing/Painting/.project
%{_datadir}/%{name}/examples/Drawing/Painting/.startup
%{_datadir}/%{name}/examples/Drawing/Painting/.src/
%{_datadir}/%{name}/examples/Drawing/Painting/Example*
%{_datadir}/%{name}/examples/Drawing/Painting/clovis.jpg
%{_datadir}/%{name}/examples/Drawing/Painting/gambas.*svg
%{_datadir}/%{name}/examples/Drawing/Painting/icon.png
%{_datadir}/%{name}/examples/Drawing/Painting/image.jpg
%{_datadir}/%{name}/examples/Drawing/Painting/Painting.gambas

%dir %{_datadir}/%{name}/examples/Drawing/GSLSpline/
%{_datadir}/%{name}/examples/Drawing/GSLSpline/.directory
%{_datadir}/%{name}/examples/Drawing/GSLSpline/.gambas/
%{_datadir}/%{name}/examples/Drawing/GSLSpline/.icon*
%{_datadir}/%{name}/examples/Drawing/GSLSpline/.project
%{_datadir}/%{name}/examples/Drawing/GSLSpline/.src/
%{_datadir}/%{name}/examples/Drawing/GSLSpline/.startup
%{_datadir}/%{name}/examples/Drawing/GSLSpline/GSLSpline.gambas
%{_datadir}/%{name}/examples/Drawing/GSLSpline/spline.png

%dir %{_datadir}/%{name}/examples/Drawing/Tablet/
%{_datadir}/%{name}/examples/Drawing/Tablet/.directory
%{_datadir}/%{name}/examples/Drawing/Tablet/.gambas/
%{_datadir}/%{name}/examples/Drawing/Tablet/.icon*
%{_datadir}/%{name}/examples/Drawing/Tablet/.project
%{_datadir}/%{name}/examples/Drawing/Tablet/.src/
%{_datadir}/%{name}/examples/Drawing/Tablet/.startup
%{_datadir}/%{name}/examples/Drawing/Tablet/Icon.png
%{_datadir}/%{name}/examples/Drawing/Tablet/Tablet.gambas

%dir %{_datadir}/%{name}/examples/Games/BeastScroll/
%{_datadir}/%{name}/examples/Games/BeastScroll/.dir_icon.png
%{_datadir}/%{name}/examples/Games/BeastScroll/.directory
%{_datadir}/%{name}/examples/Games/BeastScroll/.gambas/
%{_datadir}/%{name}/examples/Games/BeastScroll/.hidden
%{_datadir}/%{name}/examples/Games/BeastScroll/.icon*
%{_datadir}/%{name}/examples/Games/BeastScroll/.project
%{_datadir}/%{name}/examples/Games/BeastScroll/.startup
%{_datadir}/%{name}/examples/Games/BeastScroll/.src/
%{_datadir}/%{name}/examples/Games/BeastScroll/BeastScroll.gambas
%{_datadir}/%{name}/examples/Games/BeastScroll/b-title.mod
%{_datadir}/%{name}/examples/Games/BeastScroll/bgd*.png
%{_datadir}/%{name}/examples/Games/BeastScroll/fireworks.png
%{_datadir}/%{name}/examples/Games/BeastScroll/logo.png
%{_datadir}/%{name}/examples/Games/BeastScroll/scrolltext.png
%{_datadir}/%{name}/examples/Games/BeastScroll/sprite*.png

%dir %{_datadir}/%{name}/examples/Games/Concent/
%dir %{_datadir}/%{name}/examples/Games/Concent/.lang/
%{_datadir}/%{name}/examples/Games/Concent/.directory
%{_datadir}/%{name}/examples/Games/Concent/.gambas/
%{_datadir}/%{name}/examples/Games/Concent/.hidden
%{_datadir}/%{name}/examples/Games/Concent/.icon*
%{_datadir}/%{name}/examples/Games/Concent/.project
%{_datadir}/%{name}/examples/Games/Concent/.settings
%{_datadir}/%{name}/examples/Games/Concent/.startup
%{_datadir}/%{name}/examples/Games/Concent/*.wav
%{_datadir}/%{name}/examples/Games/Concent/CHANGELOG
%{_datadir}/%{name}/examples/Games/Concent/Concent.gambas
%{_datadir}/%{name}/examples/Games/Concent/.src/
%{_datadir}/%{name}/examples/Games/Concent/imagenes/

%dir %{_datadir}/%{name}/examples/Games/DeepSpace/
%dir %{_datadir}/%{name}/examples/Games/DeepSpace/.lang/
%{_datadir}/%{name}/examples/Games/DeepSpace/.directory
%{_datadir}/%{name}/examples/Games/DeepSpace/.gambas/
%{_datadir}/%{name}/examples/Games/DeepSpace/.hidden
%{_datadir}/%{name}/examples/Games/DeepSpace/.icon*
%{_datadir}/%{name}/examples/Games/DeepSpace/.project
%{_datadir}/%{name}/examples/Games/DeepSpace/.startup
%{_datadir}/%{name}/examples/Games/DeepSpace/.src/
%{_datadir}/%{name}/examples/Games/DeepSpace/DeepSpace.gambas
%{_datadir}/%{name}/examples/Games/DeepSpace/doc/
%{_datadir}/%{name}/examples/Games/DeepSpace/images/
%{_datadir}/%{name}/examples/Games/DeepSpace/object.data/

%dir %{_datadir}/%{name}/examples/Games/GameOfLife/
%dir %{_datadir}/%{name}/examples/Games/GameOfLife/.lang/
%{_datadir}/%{name}/examples/Games/GameOfLife/.debug
%{_datadir}/%{name}/examples/Games/GameOfLife/.directory
%{_datadir}/%{name}/examples/Games/GameOfLife/.gambas/
%{_datadir}/%{name}/examples/Games/GameOfLife/.hidden
%{_datadir}/%{name}/examples/Games/GameOfLife/.icon*
%{_datadir}/%{name}/examples/Games/GameOfLife/.project
%{_datadir}/%{name}/examples/Games/GameOfLife/.settings
%{_datadir}/%{name}/examples/Games/GameOfLife/.startup
%{_datadir}/%{name}/examples/Games/GameOfLife/.src/
%{_datadir}/%{name}/examples/Games/GameOfLife/GameOfLife.gambas
%{_datadir}/%{name}/examples/Games/GameOfLife/glob2*.png

%dir %{_datadir}/%{name}/examples/Games/GNUBoxWorld/
%dir %{_datadir}/%{name}/examples/Games/GNUBoxWorld/.lang/
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/.directory
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/.gambas/
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/.hidden
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/.icon*
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/License
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/.project
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/.startup
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/.src/
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/GNUBoxWorld.gambas
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/abajo.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/arriba.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/derecha.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/destino.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/ganador.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/izquierda.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/logo.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/movibleendestino.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/movible.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/obstaculo*.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/piso.png

%{_datadir}/%{name}/examples/Games/Invaders/invaders.png
%{_datadir}/%{name}/examples/Games/Invaders/.directory
%{_datadir}/%{name}/examples/Games/Invaders/.gambas/
%{_datadir}/%{name}/examples/Games/Invaders/.icon*
%{_datadir}/%{name}/examples/Games/Invaders/.project
%{_datadir}/%{name}/examples/Games/Invaders/.src/
%{_datadir}/%{name}/examples/Games/Invaders/.startup
%{_datadir}/%{name}/examples/Games/Invaders/Invaders.*

%dir %{_datadir}/%{name}/examples/Games/MineSweeper/
%dir %{_datadir}/%{name}/examples/Games/MineSweeper/.lang/
%{_datadir}/%{name}/examples/Games/MineSweeper/.directory
%{_datadir}/%{name}/examples/Games/MineSweeper/.gambas/
%{_datadir}/%{name}/examples/Games/MineSweeper/.icon*
%{_datadir}/%{name}/examples/Games/MineSweeper/.project
%{_datadir}/%{name}/examples/Games/MineSweeper/.src/
%{_datadir}/%{name}/examples/Games/MineSweeper/.startup
%{_datadir}/%{name}/examples/Games/MineSweeper/MineSweeper.gambas
%{_datadir}/%{name}/examples/Games/MineSweeper/image/

%dir %{_datadir}/%{name}/examples/Games/Pong/
%{_datadir}/%{name}/examples/Games/Pong/.directory
%{_datadir}/%{name}/examples/Games/Pong/.gambas/
%{_datadir}/%{name}/examples/Games/Pong/.icon*
%{_datadir}/%{name}/examples/Games/Pong/.project
%{_datadir}/%{name}/examples/Games/Pong/.src/
%{_datadir}/%{name}/examples/Games/Pong/.startup
%{_datadir}/%{name}/examples/Games/Pong/Pong.gambas
%{_datadir}/%{name}/examples/Games/Pong/SPEED
%{_datadir}/%{name}/examples/Games/Pong/pong.png

%dir %{_datadir}/%{name}/examples/Games/Puzzle1To8
%dir %{_datadir}/%{name}/examples/Games/Puzzle1To8/.lang/
%{_datadir}/%{name}/examples/Games/Puzzle1To8/.directory
%{_datadir}/%{name}/examples/Games/Puzzle1To8/.gambas/
%{_datadir}/%{name}/examples/Games/Puzzle1To8/.hidden
%{_datadir}/%{name}/examples/Games/Puzzle1To8/.icon*
%{_datadir}/%{name}/examples/Games/Puzzle1To8/.project
%{_datadir}/%{name}/examples/Games/Puzzle1To8/.startup
%{_datadir}/%{name}/examples/Games/Puzzle1To8/.src/
%{_datadir}/%{name}/examples/Games/Puzzle1To8/ejemplo1.png
%{_datadir}/%{name}/examples/Games/Puzzle1To8/ejemplo2.png
%{_datadir}/%{name}/examples/Games/Puzzle1To8/logo.png
%{_datadir}/%{name}/examples/Games/Puzzle1To8/Licence
%{_datadir}/%{name}/examples/Games/Puzzle1To8/Puzzle*.gambas

%dir %{_datadir}/%{name}/examples/Games/RobotFindsKitten/
%dir %{_datadir}/%{name}/examples/Games/RobotFindsKitten/.lang/
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.directory
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.gambas/
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.hidden
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.icon*
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.project
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.startup
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.src/
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/COPYING
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/RobotFindsKitten.gambas
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/heart.png
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/nkis.txt
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/readme.txt

%dir %{_datadir}/%{name}/examples/Games/Snake/
%dir %{_datadir}/%{name}/examples/Games/Snake/.lang/
%{_datadir}/%{name}/examples/Games/Snake/.directory
%{_datadir}/%{name}/examples/Games/Snake/.gambas/
%{_datadir}/%{name}/examples/Games/Snake/.hidden
%{_datadir}/%{name}/examples/Games/Snake/.icon*
%{_datadir}/%{name}/examples/Games/Snake/.project
%{_datadir}/%{name}/examples/Games/Snake/.startup
%{_datadir}/%{name}/examples/Games/Snake/.src/
%{_datadir}/%{name}/examples/Games/Snake/Snake.gambas
%{_datadir}/%{name}/examples/Games/Snake/apple.png
%{_datadir}/%{name}/examples/Games/Snake/body.png
%{_datadir}/%{name}/examples/Games/Snake/*.wav
%{_datadir}/%{name}/examples/Games/Snake/head.png

%dir %{_datadir}/%{name}/examples/Games/Solitaire/
%dir %{_datadir}/%{name}/examples/Games/Solitaire/.lang/
%{_datadir}/%{name}/examples/Games/Solitaire/.directory
%{_datadir}/%{name}/examples/Games/Solitaire/.gambas/
%{_datadir}/%{name}/examples/Games/Solitaire/.hidden
%{_datadir}/%{name}/examples/Games/Solitaire/.icon*
%{_datadir}/%{name}/examples/Games/Solitaire/.project
%{_datadir}/%{name}/examples/Games/Solitaire/.startup
%{_datadir}/%{name}/examples/Games/Solitaire/.src/
%{_datadir}/%{name}/examples/Games/Solitaire/Solitaire.gambas
%{_datadir}/%{name}/examples/Games/Solitaire/ball.png
%{_datadir}/%{name}/examples/Games/Solitaire/new.png
%{_datadir}/%{name}/examples/Games/Solitaire/quit.png
%{_datadir}/%{name}/examples/Games/Solitaire/redo.png
%{_datadir}/%{name}/examples/Games/Solitaire/undo.png

%dir %{_datadir}/%{name}/examples/Games/StarField/
%{_datadir}/%{name}/examples/Games/StarField/.directory
%{_datadir}/%{name}/examples/Games/StarField/.gambas/
%{_datadir}/%{name}/examples/Games/StarField/.icon*
%{_datadir}/%{name}/examples/Games/StarField/.project
%{_datadir}/%{name}/examples/Games/StarField/.src/
%{_datadir}/%{name}/examples/Games/StarField/.startup
%{_datadir}/%{name}/examples/Games/StarField/StarField.gambas
%{_datadir}/%{name}/examples/Games/StarField/enterprise.png
%{_datadir}/%{name}/examples/Games/StarField/logo.png

%dir %{_datadir}/%{name}/examples/Image/ImageViewer/
%dir %{_datadir}/%{name}/examples/Image/ImageViewer/.lang/
%{_datadir}/%{name}/examples/Image/ImageViewer/.directory
%{_datadir}/%{name}/examples/Image/ImageViewer/.gambas/
%{_datadir}/%{name}/examples/Image/ImageViewer/.hidden
%{_datadir}/%{name}/examples/Image/ImageViewer/.icon*
%{_datadir}/%{name}/examples/Image/ImageViewer/image.png
%{_datadir}/%{name}/examples/Image/ImageViewer/ImageViewer.gambas
%{_datadir}/%{name}/examples/Image/ImageViewer/.project
%{_datadir}/%{name}/examples/Image/ImageViewer/.startup
%{_datadir}/%{name}/examples/Image/ImageViewer/.src/
%{_datadir}/%{name}/examples/Image/ImageViewer/test.png

%dir %{_datadir}/%{name}/examples/Image/Lighttable/
%dir %{_datadir}/%{name}/examples/Image/Lighttable/.lang/
%{_datadir}/%{name}/examples/Image/Lighttable/.action/
%{_datadir}/%{name}/examples/Image/Lighttable/.gambas/
%{_datadir}/%{name}/examples/Image/Lighttable/.src/
%{_datadir}/%{name}/examples/Image/Lighttable/.directory
%{_datadir}/%{name}/examples/Image/Lighttable/.hidden
%{_datadir}/%{name}/examples/Image/Lighttable/.icon*
%{_datadir}/%{name}/examples/Image/Lighttable/.project
%{_datadir}/%{name}/examples/Image/Lighttable/.settings
%{_datadir}/%{name}/examples/Image/Lighttable/.startup
%{_datadir}/%{name}/examples/Image/Lighttable/CHANGELOG
%{_datadir}/%{name}/examples/Image/Lighttable/close.png
%{_datadir}/%{name}/examples/Image/Lighttable/FStart.*
%{_datadir}/%{name}/examples/Image/Lighttable/hand1.png
%{_datadir}/%{name}/examples/Image/Lighttable/help-contents.png
%{_datadir}/%{name}/examples/Image/Lighttable/Help*.html
%{_datadir}/%{name}/examples/Image/Lighttable/Liesmich.txt
%{_datadir}/%{name}/examples/Image/Lighttable/Lighttable.gambas
%{_datadir}/%{name}/examples/Image/Lighttable/lighttable.png
%{_datadir}/%{name}/examples/Image/Lighttable/LTicon.png
%{_datadir}/%{name}/examples/Image/Lighttable/move.png
%{_datadir}/%{name}/examples/Image/Lighttable/Readme.txt
%{_datadir}/%{name}/examples/Image/Lighttable/zoom-in.png

%dir %{_datadir}/%{name}/examples/Image/PhotoTouch/
%dir %{_datadir}/%{name}/examples/Image/PhotoTouch/.lang/
%{_datadir}/%{name}/examples/Image/PhotoTouch/.directory
%{_datadir}/%{name}/examples/Image/PhotoTouch/.gambas/
%{_datadir}/%{name}/examples/Image/PhotoTouch/.info
%{_datadir}/%{name}/examples/Image/PhotoTouch/.icon*
%{_datadir}/%{name}/examples/Image/PhotoTouch/.list
%{_datadir}/%{name}/examples/Image/PhotoTouch/.project
%{_datadir}/%{name}/examples/Image/PhotoTouch/.src/
%{_datadir}/%{name}/examples/Image/PhotoTouch/.startup
%{_datadir}/%{name}/examples/Image/PhotoTouch/PhotoTouch.gambas
%{_datadir}/%{name}/examples/Image/PhotoTouch/*.png

%dir %{_datadir}/%{name}/examples/Misc/Console/
%dir %{_datadir}/%{name}/examples/Misc/Console/.lang/
%{_datadir}/%{name}/examples/Misc/Console/.directory
%{_datadir}/%{name}/examples/Misc/Console/.gambas/
%{_datadir}/%{name}/examples/Misc/Console/.hidden
%{_datadir}/%{name}/examples/Misc/Console/.icon*
%{_datadir}/%{name}/examples/Misc/Console/.project
%{_datadir}/%{name}/examples/Misc/Console/.startup
%{_datadir}/%{name}/examples/Misc/Console/Console.gambas
%{_datadir}/%{name}/examples/Misc/Console/terminal.png
%{_datadir}/%{name}/examples/Misc/Console/.src/

%dir %{_datadir}/%{name}/examples/Misc/Evaluator/
%dir %{_datadir}/%{name}/examples/Misc/Evaluator/.lang/
%{_datadir}/%{name}/examples/Misc/Evaluator/.directory
%{_datadir}/%{name}/examples/Misc/Evaluator/.gambas/
%{_datadir}/%{name}/examples/Misc/Evaluator/.hidden
%{_datadir}/%{name}/examples/Misc/Evaluator/.icon*
%{_datadir}/%{name}/examples/Misc/Evaluator/.project
%{_datadir}/%{name}/examples/Misc/Evaluator/.startup
%{_datadir}/%{name}/examples/Misc/Evaluator/Evaluator.gambas
%{_datadir}/%{name}/examples/Misc/Evaluator/.src/
%{_datadir}/%{name}/examples/Misc/Evaluator/calculator.png

%dir %{_datadir}/%{name}/examples/Misc/Explorer/
%dir %{_datadir}/%{name}/examples/Misc/Explorer/.lang/
%{_datadir}/%{name}/examples/Misc/Explorer/.directory
%{_datadir}/%{name}/examples/Misc/Explorer/.gambas/
%{_datadir}/%{name}/examples/Misc/Explorer/.hidden
%{_datadir}/%{name}/examples/Misc/Explorer/.icon*
%{_datadir}/%{name}/examples/Misc/Explorer/.project
%{_datadir}/%{name}/examples/Misc/Explorer/.startup
%{_datadir}/%{name}/examples/Misc/Explorer/Explorer.gambas
%{_datadir}/%{name}/examples/Misc/Explorer/.src/
%{_datadir}/%{name}/examples/Misc/Explorer/folder.png

%dir %{_datadir}/%{name}/examples/Misc/Notepad/
%dir %{_datadir}/%{name}/examples/Misc/Notepad/.lang/
%{_datadir}/%{name}/examples/Misc/Notepad/.directory
%{_datadir}/%{name}/examples/Misc/Notepad/.gambas/
%{_datadir}/%{name}/examples/Misc/Notepad/.hidden
%{_datadir}/%{name}/examples/Misc/Notepad/.icon*
%{_datadir}/%{name}/examples/Misc/Notepad/.project
%{_datadir}/%{name}/examples/Misc/Notepad/.startup
%{_datadir}/%{name}/examples/Misc/Notepad/.src/
%{_datadir}/%{name}/examples/Misc/Notepad/Notepad.gambas
%{_datadir}/%{name}/examples/Misc/Notepad/notepad.png

%dir %{_datadir}/%{name}/examples/Misc/PDFViewer/
%dir %{_datadir}/%{name}/examples/Misc/PDFViewer/.lang/
%{_datadir}/%{name}/examples/Misc/PDFViewer/.directory
%{_datadir}/%{name}/examples/Misc/PDFViewer/.gambas/
%{_datadir}/%{name}/examples/Misc/PDFViewer/.hidden
%{_datadir}/%{name}/examples/Misc/PDFViewer/.icon*
%{_datadir}/%{name}/examples/Misc/PDFViewer/.project
%{_datadir}/%{name}/examples/Misc/PDFViewer/.startup
%{_datadir}/%{name}/examples/Misc/PDFViewer/.src/
%{_datadir}/%{name}/examples/Misc/PDFViewer/PDFViewer.gambas
%{_datadir}/%{name}/examples/Misc/PDFViewer/pdf.png

%dir %{_datadir}/%{name}/examples/Multimedia/CDPlayer/
%dir %{_datadir}/%{name}/examples/Multimedia/CDPlayer/.lang/
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/.directory
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/.gambas/
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/.icon*
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/.project
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/.src/
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/.startup
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/CDPlayer.gambas
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/cdrom.png

%dir %{_datadir}/%{name}/examples/Multimedia/MediaPlayer/
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.directory
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.icon*
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.info
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.gambas/
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.list
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.project
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.src/
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.startup
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/MediaPlayer.gambas
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/*.png

%dir %{_datadir}/%{name}/examples/Multimedia/MoviePlayer/
%dir %{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.lang/
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.directory
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.gambas/
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.icon*
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.project
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.src/
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.startup
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/MoviePlayer.gambas
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/video.png

%dir %{_datadir}/%{name}/examples/Multimedia/MusicPlayer/
%dir %{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.lang/
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.directory
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.gambas/
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.icon*
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.project
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.src/
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.startup
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/MusicPlayer.gambas
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/sound.png

%dir %{_datadir}/%{name}/examples/Multimedia/MyWebCam/
%dir %{_datadir}/%{name}/examples/Multimedia/MyWebCam/.lang/
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/.directory
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/.gambas/
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/.icon*
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/.project
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/.src/
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/.startup
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/MyWebCam.gambas
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/camera.png

%dir %{_datadir}/%{name}/examples/Multimedia/WebCam/
%{_datadir}/%{name}/examples/Multimedia/WebCam/.directory
%{_datadir}/%{name}/examples/Multimedia/WebCam/.gambas/
%{_datadir}/%{name}/examples/Multimedia/WebCam/.icon*
%{_datadir}/%{name}/examples/Multimedia/WebCam/.project
%{_datadir}/%{name}/examples/Multimedia/WebCam/.src/
%{_datadir}/%{name}/examples/Multimedia/WebCam/.startup
%{_datadir}/%{name}/examples/Multimedia/WebCam/WebCam.gambas
%{_datadir}/%{name}/examples/Multimedia/WebCam/camera.png
%{_datadir}/%{name}/examples/Multimedia/WebCam/settings.png

%dir %{_datadir}/%{name}/examples/Networking/ClientSocket/
%dir %{_datadir}/%{name}/examples/Networking/ClientSocket/.lang/
%{_datadir}/%{name}/examples/Networking/ClientSocket/.directory
%{_datadir}/%{name}/examples/Networking/ClientSocket/.gambas/
%{_datadir}/%{name}/examples/Networking/ClientSocket/.hidden
%{_datadir}/%{name}/examples/Networking/ClientSocket/.icon*
%{_datadir}/%{name}/examples/Networking/ClientSocket/.project
%{_datadir}/%{name}/examples/Networking/ClientSocket/.startup
%{_datadir}/%{name}/examples/Networking/ClientSocket/ClientSocket.gambas
%{_datadir}/%{name}/examples/Networking/ClientSocket/.src/
%{_datadir}/%{name}/examples/Networking/ClientSocket/socket.png

%dir %{_datadir}/%{name}/examples/Networking/DnsClient/
%dir %{_datadir}/%{name}/examples/Networking/DnsClient/.lang/
%{_datadir}/%{name}/examples/Networking/DnsClient/.directory
%{_datadir}/%{name}/examples/Networking/DnsClient/.gambas/
%{_datadir}/%{name}/examples/Networking/DnsClient/.hidden
%{_datadir}/%{name}/examples/Networking/DnsClient/.icon*
%{_datadir}/%{name}/examples/Networking/DnsClient/.project
%{_datadir}/%{name}/examples/Networking/DnsClient/.startup
%{_datadir}/%{name}/examples/Networking/DnsClient/DnsClient.gambas
%{_datadir}/%{name}/examples/Networking/DnsClient/.src/
%{_datadir}/%{name}/examples/Networking/DnsClient/dnsclient.png

%dir %{_datadir}/%{name}/examples/Networking/HTTPGet/
%dir %{_datadir}/%{name}/examples/Networking/HTTPGet/.lang/
%{_datadir}/%{name}/examples/Networking/HTTPGet/.directory
%{_datadir}/%{name}/examples/Networking/HTTPGet/.gambas/
%{_datadir}/%{name}/examples/Networking/HTTPGet/.hidden
%{_datadir}/%{name}/examples/Networking/HTTPGet/.icon*
%{_datadir}/%{name}/examples/Networking/HTTPGet/.project
%{_datadir}/%{name}/examples/Networking/HTTPGet/.startup
%{_datadir}/%{name}/examples/Networking/HTTPGet/.src/
%{_datadir}/%{name}/examples/Networking/HTTPGet/HTTPGet.gambas
%{_datadir}/%{name}/examples/Networking/HTTPGet/httpclient.png

%dir %{_datadir}/%{name}/examples/Networking/HTTPPost/
%dir %{_datadir}/%{name}/examples/Networking/HTTPPost/.lang/
%{_datadir}/%{name}/examples/Networking/HTTPPost/.directory
%{_datadir}/%{name}/examples/Networking/HTTPPost/.gambas/
%{_datadir}/%{name}/examples/Networking/HTTPPost/.hidden
%{_datadir}/%{name}/examples/Networking/HTTPPost/.icon*
%{_datadir}/%{name}/examples/Networking/HTTPPost/.project
%{_datadir}/%{name}/examples/Networking/HTTPPost/.startup
%{_datadir}/%{name}/examples/Networking/HTTPPost/.src/
%{_datadir}/%{name}/examples/Networking/HTTPPost/HTTPPost.gambas
%{_datadir}/%{name}/examples/Networking/HTTPPost/httpclient.png

%dir %{_datadir}/%{name}/examples/Networking/POPMailbox/
%{_datadir}/%{name}/examples/Networking/POPMailbox/.directory
%{_datadir}/%{name}/examples/Networking/POPMailbox/.gambas/
%{_datadir}/%{name}/examples/Networking/POPMailbox/.icon*
%{_datadir}/%{name}/examples/Networking/POPMailbox/.project
%{_datadir}/%{name}/examples/Networking/POPMailbox/.src/
%{_datadir}/%{name}/examples/Networking/POPMailbox/.startup
%{_datadir}/%{name}/examples/Networking/POPMailbox/POPMailbox.gambas
%{_datadir}/%{name}/examples/Networking/POPMailbox/pop3client.png

%dir %{_datadir}/%{name}/examples/Networking/SerialPort/
%dir %{_datadir}/%{name}/examples/Networking/SerialPort/.lang/
%{_datadir}/%{name}/examples/Networking/SerialPort/.directory
%{_datadir}/%{name}/examples/Networking/SerialPort/.gambas/
%{_datadir}/%{name}/examples/Networking/SerialPort/.hidden
%{_datadir}/%{name}/examples/Networking/SerialPort/.icon*
%{_datadir}/%{name}/examples/Networking/SerialPort/.project
%{_datadir}/%{name}/examples/Networking/SerialPort/.startup
%{_datadir}/%{name}/examples/Networking/SerialPort/.src/
%{_datadir}/%{name}/examples/Networking/SerialPort/SerialPort.gambas
%{_datadir}/%{name}/examples/Networking/SerialPort/serialport.png

%dir %{_datadir}/%{name}/examples/Networking/ServerSocket/
%dir %{_datadir}/%{name}/examples/Networking/ServerSocket/.lang/
%{_datadir}/%{name}/examples/Networking/ServerSocket/.directory
%{_datadir}/%{name}/examples/Networking/ServerSocket/.gambas/
%{_datadir}/%{name}/examples/Networking/ServerSocket/.hidden
%{_datadir}/%{name}/examples/Networking/ServerSocket/.icon*
%{_datadir}/%{name}/examples/Networking/ServerSocket/.project
%{_datadir}/%{name}/examples/Networking/ServerSocket/.startup
%{_datadir}/%{name}/examples/Networking/ServerSocket/.src/
%{_datadir}/%{name}/examples/Networking/ServerSocket/ServerSocket.gambas
%{_datadir}/%{name}/examples/Networking/ServerSocket/serversocket.png

%dir %{_datadir}/%{name}/examples/Networking/UDPServerClient/
%dir %{_datadir}/%{name}/examples/Networking/UDPServerClient/.lang/
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.directory
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.gambas/
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.hidden
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.icon*
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.project
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.startup
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.src/
%{_datadir}/%{name}/examples/Networking/UDPServerClient/UDPServerClient.gambas
%{_datadir}/%{name}/examples/Networking/UDPServerClient/udpsocket.png

%dir %{_datadir}/%{name}/examples/Networking/WebBrowser/
%dir %{_datadir}/%{name}/examples/Networking/WebBrowser/.lang/
%{_datadir}/%{name}/examples/Networking/WebBrowser/.directory
%{_datadir}/%{name}/examples/Networking/WebBrowser/.gambas/
%{_datadir}/%{name}/examples/Networking/WebBrowser/.hidden
%{_datadir}/%{name}/examples/Networking/WebBrowser/.icon*
%{_datadir}/%{name}/examples/Networking/WebBrowser/.project
%{_datadir}/%{name}/examples/Networking/WebBrowser/.startup
%{_datadir}/%{name}/examples/Networking/WebBrowser/.src/
%{_datadir}/%{name}/examples/Networking/WebBrowser/WebBrowser.gambas
%{_datadir}/%{name}/examples/Networking/WebBrowser/konqueror.png
%{_datadir}/%{name}/examples/Networking/WebBrowser/list-*.png

%dir %{_datadir}/%{name}/examples/OpenGL/3DWebCam/
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.directory
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.gambas/
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.hidden
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.icon*
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.project
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.startup
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/3DWebCam.gambas
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.src/
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/webcam.png

%dir %{_datadir}/%{name}/examples/OpenGL/GambasGears/
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.directory
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.gambas/
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.hidden
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.icon*
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.project
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.startup
%{_datadir}/%{name}/examples/OpenGL/GambasGears/GambasGears.gambas
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.src/
%{_datadir}/%{name}/examples/OpenGL/GambasGears/gears.png

%dir %{_datadir}/%{name}/examples/OpenGL/Md2Model/
%{_datadir}/%{name}/examples/OpenGL/Md2Model/.directory
%{_datadir}/%{name}/examples/OpenGL/Md2Model/.gambas/
%{_datadir}/%{name}/examples/OpenGL/Md2Model/.icon*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/.project
%{_datadir}/%{name}/examples/OpenGL/Md2Model/.settings
%{_datadir}/%{name}/examples/OpenGL/Md2Model/.src/
%{_datadir}/%{name}/examples/OpenGL/Md2Model/.startup
%{_datadir}/%{name}/examples/OpenGL/Md2Model/Md2Model.gambas
%{_datadir}/%{name}/examples/OpenGL/Md2Model/Weapon.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/bauul.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/goblin.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/icon.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/igdosh.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/knight.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/ogro.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/rat.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/rhino.*

%dir %{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/.directory
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/.gambas/
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/.icon*
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/.project
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/.src/
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/.startup
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/NeHe.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/NeHeTutorial.gambas
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/*.txt
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/Star.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/barrel.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/ceiling.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/crate.jpeg
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/floor.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/glass.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/icon.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/wall.jpeg

%dir %{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/.directory
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/.gambas/
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/.icon*
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/.project
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/.src/
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/.startup
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/NeHeTutorialShell.gambas
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/icon.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/nehe.png

%dir %{_datadir}/%{name}/examples/OpenGL/PDFPresentation/
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.directory
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.gambas/
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.hidden
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.icon*
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.project
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.settings
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.startup
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.src/
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/PDFPresentation.gambas
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/icon.png
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/logo.png
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/music.xm

%dir %{_datadir}/%{name}/examples/OpenGL/TunnelSDL/
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/.dir_icon.png
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/.directory
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/.gambas/
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/.icon*
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/.project
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/.src/
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/.startup
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/CHANGELOG
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/TunnelSDL.gambas
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/texture.png
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/tunnelsdl.png

%dir %{_datadir}/%{name}/examples/Printing/Printing/
%{_datadir}/%{name}/examples/Printing/Printing/.directory
%{_datadir}/%{name}/examples/Printing/Printing/.gambas/
%{_datadir}/%{name}/examples/Printing/Printing/.hidden
%{_datadir}/%{name}/examples/Printing/Printing/.icon*
%{_datadir}/%{name}/examples/Printing/Printing/.project
%{_datadir}/%{name}/examples/Printing/Printing/.startup
%{_datadir}/%{name}/examples/Printing/Printing/molly-malone.txt
%{_datadir}/%{name}/examples/Printing/Printing/printer-laser.png
%{_datadir}/%{name}/examples/Printing/Printing/.src/
%{_datadir}/%{name}/examples/Printing/Printing/Printing.gambas

%dir %{_datadir}/%{name}/examples/Printing/ReportExample/
%{_datadir}/%{name}/examples/Printing/ReportExample/.connection/
%{_datadir}/%{name}/examples/Printing/ReportExample/.directory
%{_datadir}/%{name}/examples/Printing/ReportExample/.gambas/
%{_datadir}/%{name}/examples/Printing/ReportExample/.hidden/
%{_datadir}/%{name}/examples/Printing/ReportExample/.icon*
%{_datadir}/%{name}/examples/Printing/ReportExample/.project
%{_datadir}/%{name}/examples/Printing/ReportExample/.settings
%{_datadir}/%{name}/examples/Printing/ReportExample/.src/
%{_datadir}/%{name}/examples/Printing/ReportExample/.startup
%{_datadir}/%{name}/examples/Printing/ReportExample/ReportExample.gambas
%{_datadir}/%{name}/examples/Printing/ReportExample/gambas.svg

# Translation files
%lang(ca) %{_datadir}/%{name}/examples/Basic/Blights/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Basic/Blights/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Basic/Blights/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Basic/Blights/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Basic/Blights/.lang/fr.*o
%lang(sv) %{_datadir}/%{name}/examples/Basic/Blights/.lang/sv.*o
%lang(ca) %{_datadir}/%{name}/examples/Basic/Collection/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Basic/Collection/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Basic/Collection/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Basic/Collection/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Basic/Object/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Basic/Object/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Basic/Object/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Basic/Object/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Basic/Timer/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Basic/Timer/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Basic/Timer/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Basic/Timer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/ArrayOfControls/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Control/ArrayOfControls/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Control/ArrayOfControls/.lang/de.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/Embedder/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Control/Embedder/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Control/Embedder/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Control/Embedder/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/HighlightEditor/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Control/HighlightEditor/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Control/HighlightEditor/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Control/HighlightEditor/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/fr.*o
%lang(sv) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/sv.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/TreeView/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Control/TreeView/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Control/TreeView/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Control/TreeView/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/Wizard/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Control/Wizard/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Control/Wizard/.lang/de.*o
%lang(ca) %{_datadir}/%{name}/examples/Database/Database/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Database/Database/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Database/Database/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Database/Database/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Database/MySQLExample/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Database/MySQLExample/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Database/MySQLExample/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Database/MySQLExample/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Database/MySQLExample/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Database/PictureDatabase/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Database/PictureDatabase/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Database/PictureDatabase/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Database/PictureDatabase/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/Barcode/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Drawing/Barcode/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Drawing/Barcode/.lang/de.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/Chart/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Drawing/Chart/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Drawing/Chart/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Drawing/Chart/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/Clock/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Drawing/Clock/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Drawing/Clock/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Drawing/Clock/.lang/es.*o
%lang(cs) %{_datadir}/%{name}/examples/Drawing/Fractal/.lang/cs.*o
%lang(fr) %{_datadir}/%{name}/examples/Drawing/Fractal/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/Gravity/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Drawing/Gravity/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Drawing/Gravity/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Drawing/Gravity/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/Painting/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Drawing/Painting/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Drawing/Painting/.lang/de.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/Concent/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/Concent/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/Concent/.lang/de.*o
%lang(en) %{_datadir}/%{name}/examples/Games/Concent/.lang/en.*o
%lang(es) %{_datadir}/%{name}/examples/Games/Concent/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Games/Concent/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/DeepSpace/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/DeepSpace/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/DeepSpace/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Games/DeepSpace/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/GameOfLife/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/GameOfLife/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/GameOfLife/.lang/de.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/GNUBoxWorld/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/GNUBoxWorld/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/GNUBoxWorld/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Games/GNUBoxWorld/.lang/es*.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/MineSweeper/.lang/cs.*o
%lang(ja) %{_datadir}/%{name}/examples/Games/MineSweeper/.lang/ja.*o
%lang(zh) %{_datadir}/%{name}/examples/Games/MineSweeper/.lang/zh*.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/Puzzle1To8/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/Puzzle1To8/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/Puzzle1To8/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Games/Puzzle1To8/.lang/es*.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/RobotFindsKitten/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/RobotFindsKitten/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/RobotFindsKitten/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Games/RobotFindsKitten/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/Snake/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/Snake/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/Snake/.lang/de.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/Solitaire/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/Solitaire/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/Solitaire/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Games/Solitaire/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Image/ImageViewer/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Image/ImageViewer/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Image/ImageViewer/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Image/ImageViewer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Image/Lighttable/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Image/Lighttable/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Image/Lighttable/.lang/de.*o
%lang(en) %{_datadir}/%{name}/examples/Image/Lighttable/.lang/en.*o
%lang(fr) %{_datadir}/%{name}/examples/Image/PhotoTouch/.lang/fr.*o
%lang(fr) %{_datadir}/%{name}/examples/Misc/Console/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Misc/Evaluator/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Misc/Evaluator/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Misc/Evaluator/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Misc/Evaluator/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Misc/Explorer/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Misc/Explorer/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Misc/Explorer/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Misc/Explorer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Misc/Notepad/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Misc/Notepad/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Misc/Notepad/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Misc/Notepad/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Misc/PDFViewer/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Misc/PDFViewer/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Misc/PDFViewer/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Misc/PDFViewer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Multimedia/CDPlayer/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Multimedia/CDPlayer/.lang/cs.*o
%lang(es) %{_datadir}/%{name}/examples/Multimedia/CDPlayer/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.lang/cs.*o
%lang(es) %{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.lang/cs.*o
%lang(es) %{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Multimedia/MyWebCam/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Multimedia/MyWebCam/.lang/cs.*o
%lang(es) %{_datadir}/%{name}/examples/Multimedia/MyWebCam/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/ClientSocket/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/ClientSocket/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Networking/ClientSocket/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/ClientSocket/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/DnsClient/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/DnsClient/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Networking/DnsClient/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/DnsClient/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/HTTPGet/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/HTTPGet/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Networking/HTTPGet/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/HTTPGet/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/HTTPPost/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/HTTPPost/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Networking/HTTPPost/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/HTTPPost/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/SerialPort/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/SerialPort/.lang/cs.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/SerialPort/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/ServerSocket/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/ServerSocket/.lang/cs.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/ServerSocket/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/UDPServerClient/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/UDPServerClient/.lang/cs.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/UDPServerClient/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/WebBrowser/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/WebBrowser/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Networking/WebBrowser/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/WebBrowser/.lang/es.*o

%files gb-args
%{_libdir}/%{name}/gb.args.*
%{_datadir}/%{name}/info/gb.args.*

%files gb-cairo
%{_libdir}/%{name}/gb.cairo.*
%{_datadir}/%{name}/info/gb.cairo.*

%files gb-chart
%{_libdir}/%{name}/gb.chart.*
%{_datadir}/%{name}/info/gb.chart.*

%files gb-clipper
%{_libdir}/%{name}/gb.clipper.*
%{_datadir}/%{name}/info/gb.clipper.*

%files gb-complex
%{_libdir}/%{name}/gb.complex.*
%{_datadir}/%{name}/info/gb.complex.*

%files gb-compress
%{_libdir}/%{name}/gb.compress.*
%{_datadir}/%{name}/info/gb.compress.*

%files gb-crypt
%{_libdir}/%{name}/gb.crypt.*
%{_datadir}/%{name}/info/gb.crypt.*

%files gb-data
%{_libdir}/%{name}/gb.data.*
%{_datadir}/%{name}/info/gb.data.*

%files gb-db
%{_libdir}/%{name}/gb.db.component
%{_libdir}/%{name}/gb.db.gambas
%{_libdir}/%{name}/gb.db.la
%{_libdir}/%{name}/gb.db.so*
%{_datadir}/%{name}/info/gb.db.info
%{_datadir}/%{name}/info/gb.db.list

%files gb-db-form
%{_libdir}/%{name}/gb.db.form.*
%{_datadir}/%{name}/control/gb.db.form/
%{_datadir}/%{name}/info/gb.db.form.*

%files gb-db-mysql
%{_libdir}/%{name}/gb.db.mysql.*
%{_datadir}/%{name}/info/gb.db.mysql.*

%files gb-db-odbc
%{_libdir}/%{name}/gb.db.odbc.*
%{_datadir}/%{name}/info/gb.db.odbc.*

%files gb-db-postgresql
%{_libdir}/%{name}/gb.db.postgresql.*
%{_datadir}/%{name}/info/gb.db.postgresql.*

%files gb-db-sqlite2
%{_libdir}/%{name}/gb.db.sqlite2.*
%{_datadir}/%{name}/info/gb.db.sqlite2.*

%files gb-db-sqlite3
%{_libdir}/%{name}/gb.db.sqlite3.*
%{_datadir}/%{name}/info/gb.db.sqlite3.*

%files gb-dbus
%{_libdir}/%{name}/gb.dbus.*
%{_datadir}/%{name}/info/gb.dbus.*

%files gb-desktop
%{_libdir}/%{name}/gb.desktop.*
%exclude %{_libdir}/%{name}/gb.desktop.gnome.*
%{_datadir}/%{name}/control/gb.desktop/
%{_datadir}/%{name}/info/gb.desktop.*

%files gb-desktop-gnome
%{_libdir}/%{name}/gb.desktop.gnome.*

%files gb-eval-highlight
%{_libdir}/%{name}/gb.eval.highlight.*
%{_datadir}/%{name}/info/gb.eval.highlight.*

%files gb-form
%{_libdir}/%{name}/gb.form.component
%{_libdir}/%{name}/gb.form.gambas
%{_datadir}/%{name}/control/gb.form/
%{_datadir}/%{name}/info/gb.form.info
%{_datadir}/%{name}/info/gb.form.list

%files gb-form-dialog
%{_libdir}/%{name}/gb.form.dialog.component
%{_libdir}/%{name}/gb.form.dialog.gambas
%{_datadir}/%{name}/info/gb.form.dialog.info
%{_datadir}/%{name}/info/gb.form.dialog.list

%files gb-form-mdi
%{_libdir}/%{name}/gb.form.mdi.component
%{_libdir}/%{name}/gb.form.mdi.gambas
%{_datadir}/%{name}/control/gb.form.mdi/
%{_datadir}/%{name}/info/gb.form.mdi.info
%{_datadir}/%{name}/info/gb.form.mdi.list

%files gb-form-stock
%{_libdir}/%{name}/gb.form.stock.component
%{_libdir}/%{name}/gb.form.stock.gambas
%{_datadir}/%{name}/info/gb.form.stock.info
%{_datadir}/%{name}/info/gb.form.stock.list

%files gb-gmp
%{_libdir}/%{name}/gb.gmp.*
%{_datadir}/%{name}/info/gb.gmp.*

%files gb-gsl
%{_libdir}/%{name}/gb.gsl.component
%{_libdir}/%{name}/gb.gsl.so*
%{_libdir}/%{name}/gb.gsl.la
%{_datadir}/%{name}/info/gb.gsl.info
%{_datadir}/%{name}/info/gb.gsl.list

%files gb-gtk
%{_libdir}/%{name}/gb.gtk.component
# %{_libdir}/%{name}/gb.gtk.gambas
%{_libdir}/%{name}/gb.gtk.so*
%{_libdir}/%{name}/gb.gtk.la
%{_datadir}/%{name}/info/gb.gtk.info
%{_datadir}/%{name}/info/gb.gtk.list

%files gb-gtk-opengl
%{_libdir}/%{name}/gb.gtk.opengl.component
%{_libdir}/%{name}/gb.gtk.opengl.so*
%{_libdir}/%{name}/gb.gtk.opengl.la
%{_datadir}/%{name}/info/gb.gtk.opengl.info
%{_datadir}/%{name}/info/gb.gtk.opengl.list

%files gb-httpd
%{_libdir}/%{name}/gb.httpd.*
%{_datadir}/%{name}/info/gb.httpd.*

%files gb-image
%{_libdir}/%{name}/gb.image.component
%{_libdir}/%{name}/gb.image.so*
%{_libdir}/%{name}/gb.image.la
%{_datadir}/%{name}/info/gb.image.info
%{_datadir}/%{name}/info/gb.image.list

%files gb-image-effect
%{_libdir}/%{name}/gb.image.effect.*
%{_datadir}/%{name}/info/gb.image.effect.*

%files gb-image-imlib
%{_libdir}/%{name}/gb.image.imlib.*
%{_datadir}/%{name}/info/gb.image.imlib.*

%files gb-image-io
%{_libdir}/%{name}/gb.image.io.*
%{_datadir}/%{name}/info/gb.image.io.*

%if 0%{?fedora} >= 18
%files gb-jit
%{_libdir}/%{name}/gb.jit.*
%{_datadir}/%{name}/info/gb.jit.*
%endif

%files gb-libxml
%{_libdir}/%{name}/gb.libxml.component
%{_libdir}/%{name}/gb.libxml.la
%{_libdir}/%{name}/gb.libxml.so*
%{_datadir}/%{name}/info/gb.libxml.info
%{_datadir}/%{name}/info/gb.libxml.list

%files gb-logging
%{_libdir}/%{name}/gb.logging.*
%{_datadir}/%{name}/info/gb.logging.*

%files gb-map
%{_libdir}/%{name}/gb.map.component
%{_libdir}/%{name}/gb.map.gambas
%{_datadir}/%{name}/info/gb.map.*
%{_datadir}/%{name}/control/gb.map/

%files gb-media
%{_libdir}/%{name}/gb.media.component
%{_libdir}/%{name}/gb.media.la
%{_libdir}/%{name}/gb.media.so*
%{_datadir}/%{name}/info/gb.media.info
%{_datadir}/%{name}/info/gb.media.list

%files gb-memcached
%{_libdir}/%{name}/gb.memcached.*
%{_datadir}/%{name}/info/gb.memcached.*

%files gb-mime
%{_libdir}/%{name}/gb.mime.*
%{_datadir}/%{name}/info/gb.mime.*

%files gb-mysql
%{_libdir}/%{name}/gb.mysql.*
%{_datadir}/%{name}/info/gb.mysql.*

%files gb-ncurses
%{_libdir}/%{name}/gb.ncurses.component
%{_libdir}/%{name}/gb.ncurses.la
%{_libdir}/%{name}/gb.ncurses.so*
%{_datadir}/%{name}/info/gb.ncurses.info
%{_datadir}/%{name}/info/gb.ncurses.list

%files gb-net
%{_libdir}/%{name}/gb.net.component
%{_libdir}/%{name}/gb.net.so*
%{_libdir}/%{name}/gb.net.la
%{_datadir}/%{name}/info/gb.net.info
%{_datadir}/%{name}/info/gb.net.list

%files gb-net-curl
%{_libdir}/%{name}/gb.net.curl.*
%{_datadir}/%{name}/info/gb.net.curl.*

%files gb-net-pop3
%{_libdir}/%{name}/gb.net.pop3.*
%{_datadir}/%{name}/info/gb.net.pop3.*

%files gb-net-smtp
%{_libdir}/%{name}/gb.net.smtp.*
%{_datadir}/%{name}/info/gb.net.smtp.*

%files gb-openal
%{_libdir}/%{name}/gb.openal.*
%{_datadir}/%{name}/info/gb.openal.*

%files gb-opengl
%{_libdir}/%{name}/gb.opengl.component
%{_libdir}/%{name}/gb.opengl.so*
%{_libdir}/%{name}/gb.opengl.la
%{_datadir}/%{name}/info/gb.opengl.info
%{_datadir}/%{name}/info/gb.opengl.list

%files gb-opengl-sge
%{_libdir}/%{name}/gb.opengl.sge.*
%{_datadir}/%{name}/info/gb.opengl.sge.*

%files gb-opengl-glu
%{_libdir}/%{name}/gb.opengl.glu.*
%{_datadir}/%{name}/info/gb.opengl.glu.*

%files gb-opengl-glsl
%{_libdir}/%{name}/gb.opengl.glsl.*
%{_datadir}/%{name}/info/gb.opengl.glsl.*

%files gb-openssl
%{_libdir}/%{name}/gb.openssl.*
%{_datadir}/%{name}/info/gb.openssl.*


%files gb-option
%{_libdir}/%{name}/gb.option.*
%{_datadir}/%{name}/info/gb.option.*

%files gb-pcre
%{_libdir}/%{name}/gb.pcre.*
%{_datadir}/%{name}/info/gb.pcre.*

%files gb-pdf
%{_libdir}/%{name}/gb.pdf.component
%{_libdir}/%{name}/gb.pdf.so*
%{_libdir}/%{name}/gb.pdf.la
%{_datadir}/%{name}/info/gb.pdf.info
%{_datadir}/%{name}/info/gb.pdf.list

%files gb-qt4 
%{_libdir}/%{name}/gb.qt4.component
# %{_libdir}/%{name}/gb.qt4.gambas 
%{_libdir}/%{name}/gb.qt4.so* 
%{_libdir}/%{name}/gb.qt4.la 
%{_datadir}/%{name}/info/gb.qt4.info 
%{_datadir}/%{name}/info/gb.qt4.list

%files gb-qt4-ext
%{_libdir}/%{name}/gb.qt4.ext.*
%{_datadir}/%{name}/info/gb.qt4.ext.*

%files gb-qt4-opengl
%{_libdir}/%{name}/gb.qt4.opengl.*
%{_datadir}/%{name}/info/gb.qt4.opengl.*

%files gb-qt4-webkit
%{_libdir}/%{name}/gb.qt4.webkit.*
%{_datadir}/%{name}/info/gb.qt4.webkit.*

%files gb-report
%{_libdir}/%{name}/gb.report.*
%{_datadir}/%{name}/control/gb.report/
%{_datadir}/%{name}/info/gb.report.*

%files gb-sdl
%{_libdir}/%{name}/gb.sdl.component
%{_libdir}/%{name}/gb.sdl.so
%{_libdir}/%{name}/gb.sdl.so.*
%{_libdir}/%{name}/gb.sdl.la
%{_datadir}/%{name}/info/gb.sdl.info
%{_datadir}/%{name}/info/gb.sdl.list
%{_datadir}/%{name}/gb.sdl/

%files gb-sdl-sound
%{_libdir}/%{name}/gb.sdl.sound.*
%{_datadir}/%{name}/info/gb.sdl.sound.*

%files gb-settings
%{_libdir}/%{name}/gb.settings.*
%{_datadir}/%{name}/info/gb.settings.*

%files gb-signal
%{_libdir}/%{name}/gb.signal.*
%{_datadir}/%{name}/info/gb.signal.*

%files gb-v4l
%{_libdir}/%{name}/gb.v4l.*
%{_datadir}/%{name}/info/gb.v4l.*

%files gb-vb
%{_libdir}/%{name}/gb.vb.*
%{_datadir}/%{name}/info/gb.vb.*

%files gb-web
%{_libdir}/%{name}/gb.web.*
%{_datadir}/%{name}/info/gb.web.*

%files gb-xml
%{_libdir}/%{name}/gb.xml.component
%{_libdir}/%{name}/gb.xml.gambas
%{_libdir}/%{name}/gb.xml.so*
%{_libdir}/%{name}/gb.xml.la
%{_datadir}/%{name}/info/gb.xml.info
%{_datadir}/%{name}/info/gb.xml.list

%files gb-xml-html
%{_libdir}/%{name}/gb.xml.html.component
%{_libdir}/%{name}/gb.xml.html.so*
%{_libdir}/%{name}/gb.xml.html.la
%{_datadir}/%{name}/info/gb.xml.html.info
%{_datadir}/%{name}/info/gb.xml.html.list

%files gb-xml-rpc
%{_libdir}/%{name}/gb.xml.rpc.*
%{_datadir}/%{name}/info/gb.xml.rpc.info
%{_datadir}/%{name}/info/gb.xml.rpc.list

%files gb-xml-xslt
%{_libdir}/%{name}/gb.xml.xslt.*
%{_datadir}/%{name}/info/gb.xml.xslt.*

%changelog
* Wed Jan 15 2014 Dave Airlie <airlied@redhat.com> 3.5.2-2
- rebuild against llvm 3.4

* Mon Jan  6 2014 Tom Callaway <spot@fedoraproject.org> - 3.5.2-1
- update to 3.5.2

* Mon Nov 18 2013 Dave Airlie <airlied@redhat.com> - 3.5.1-2
- rebuilt for GLEW 1.10

* Fri Nov  8 2013 Tom Callaway <spot@fedoraproject.org> - 3.5.1-1
- update to 3.5.1
- fix ide requires (bz 1026988)

* Mon Oct 21 2013 Tom Callaway <spot@fedoraproject.org> - 3.5.0-2
- add missing Requires 

* Mon Oct 21 2013 Tom Callaway <spot@fedoraproject.org> - 3.5.0-1
- update to 3.5.0

* Mon Aug 19 2013 Marek Kasik <mkasik@redhat.com> - 3.4.2-2
- Rebuild (poppler-0.24.0)

* Fri Aug 16 2013 Tom Callaway <spot@fedoraproject.org> - 3.4.2-1
- update to 3.4.2

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Marek Kasik <mkasik@redhat.com> 3.4.1-5
- Rebuild (poppler-0.22.5)

* Tue May 28 2013 Adam Jackson <ajax@redhat.com> 3.4.1-4
- Rebuild for final llvm 3.3 soname

* Wed May 08 2013 Adam Jackson <ajax@redhat.com> 3.4.1-3
- Fix build against llvm 3.3

* Mon Apr 08 2013 Jon Ciesla <limburgher@gmail.com> - 3.4.1-2
- Drop desktop vendor tag.

* Mon Apr  1 2013 Tom Callaway <spot@fedoraproject.org> - 3.4.1-1
- update to 3.4.1

* Tue Feb 19 2013 Jens Petersen <petersen@redhat.com> - 3.4.0-2
- f19 rebuild against llvm-3.2

* Thu Feb  7 2013 Tom Callaway <spot@fedoraproject.org> - 3.4.0-1
- update to 3.4.0

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 3.3.4-4
- rebuild due to "jpeg8-ABI" feature drop

* Thu Dec 13 2012 Adam Jackson <ajax@redhat.com> - 3.3.4-3
- Rebuild for glew 1.9.0

* Thu Nov 29 2012 Tom Callaway <spot@fedoraproject.org> - 3.3.4-2
- conditionalize the jit subpackage, needs llvm-config >= 3.1,
  which is only in Fedora 18+.

* Wed Nov 28 2012 Tom Callaway <spot@fedoraproject.org> - 3.3.4-1
- update to 3.3.4

* Wed Oct 24 2012 Tom Callaway <spot@fedoraproject.org> - 3.3.3-1
- update to 3.3.3

* Mon Oct  1 2012 Tom Callaway <spot@fedoraproject.org> - 3.3.2-1
- update to 3.3.2

* Mon Sep 24 2012 Tom Callaway <spot@fedoraproject.org> - 3.3.0-1
- update to 3.3.0

* Wed Aug 22 2012 Tom Callaway <spot@fedoraproject.org> - 3.2.1-2
- rebuild to fix broken deps

* Wed Jul 25 2012 Tom Callaway <spot@fedoraproject.org> - 3.2.1-1
- update to 3.2.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Tom Callaway <spot@fedoraproject.org> - 3.2.0-1
- update to 3.2.0

* Mon Jul  2 2012 Marek Kasik <mkasik@redhat.com> - 3.1.1-4
- Rebuild (poppler-0.20.1)

* Tue May 29 2012 Tom Callaway <spot@fedoraproject.org> - 3.1.1-3
- add support for poppler 0.20

* Wed May  2 2012 Tom Callaway <spot@fedoraproject.org> - 3.1.1-2
- add BR: gsl-devel

* Wed May  2 2012 Tom Callaway <spot@fedoraproject.org> - 3.1.1-1
- update to 3.1.1

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 3.0.0-2
- Rebuild against PCRE 8.30

* Tue Jan 17 2012 Tom Callaway <spot@fedoraproject.org> - 3.0.0-1
- update to 3.0.0 final

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.99.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.99.6-2
- Rebuild for new libpng

* Fri Nov  4 2011 Tom Callaway <spot@fedoraproject.org> - 2.99.6-1
- update to 2.99.6

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> - 2.99.5-2
- rebuild(poppler)

* Tue Oct 11 2011 Tom Callaway <spot@fedoraproject.org> - 2.99.5-1
- update to 2.99.5

* Fri Sep 30 2011 Marek Kasik <mkasik@redhat.com> - 2.99.4-2
- Rebuild (poppler-0.18.0)

* Mon Sep 26 2011 Tom Callaway <spot@fedoraproject.org> - 2.99.4-1
- 2.99.4

* Tue Sep 20 2011 Marek Kasik <mkasik@redhat.com> - 2.99.3-3
- Rebuild (poppler-0.17.3)

* Wed Sep  7 2011 Tom Callaway <spot@fedoraproject.org> - 2.99.3-2
- make -devel Require -runtime

* Tue Sep  6 2011 Tom Callaway <spot@fedoraproject.org> - 2.99.3-1
- 2.99.3

* Thu Aug 11 2011 Tom Callaway <spot@fedoraproject.org> - 2.99.2-1
- 2.99.2
- clean up exec permissions on gb.sdl/LICENSE

* Tue Aug  9 2011 Tom Callaway <spot@fedoraproject.org> - 2.99.1-3
- disable insecure permissions on example dirs

* Tue Jun  7 2011 Tom Callaway <spot@fedoraproject.org> - 2.99.1-2
- drop kdelibs3-devel BR

* Wed Apr  6 2011 Tom Callaway <spot@fedoraproject.org> - 2.99.1-1
- new package for Gambas3
