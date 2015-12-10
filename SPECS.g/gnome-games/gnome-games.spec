%define gettext_package gnome-games

%define build_tali 1
%define have_sudoku 1

%if %{build_tali}
%define gtali gtali
%else
%define gtali %{nil}
%endif

%if !%{build_tali}
%define omitgames --enable-omitgames=gtali
%else
%define omitgames %{nil}
%endif

%if %{have_sudoku}
%define sudoku gnome-sudoku
%else
%define sudoku %{nil}
%endif

%define gnome_games_split_version 1:3.5.5-3
%define gnome_games_compat_removed_version 1:3.6.0.2-2

%define glib2_version 2.32.0
%define pango_version 1.29.0
%define desktop_file_utils_version 0.2.90
%define gstreamer_version 0.10.11

Summary: Games for the GNOME desktop
Name: gnome-games
Version: 3.6.1
Release: 6%{?dist}
Epoch: 1
License: GPLv2+ and GPLv3 and GFDL
#VCS: git:git://git.gnome.org/gnome-games
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source: http://download.gnome.org/sources/gnome-games/%{majorver}/gnome-games-%{version}.tar.xz
Patch0: glchess-respect-engine-args.patch

Obsoletes: gnome-games-devel < %{epoch}:%{version}-%{release}
URL: http://projects.gnome.org/gnome-games/

Requires: pygobject2
Requires: hicolor-icon-theme
Requires: gobject-introspection

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: gtk3-devel
BuildRequires: pygobject2-devel
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: librsvg2-devel
BuildRequires: expat-devel
BuildRequires: gstreamer-devel >= %{gstreamer_version}
BuildRequires: libcanberra-devel
BuildRequires: clutter-devel clutter-gtk-devel
BuildRequires: intltool
BuildRequires: vala-devel

# Newer than internal gettext needed
BuildRequires: gettext
BuildRequires: autoconf >= 2.60
BuildRequires: automake libtool
BuildRequires: gnome-doc-utils >= 0.3.2
BuildRequires: scrollkeeper
BuildRequires: gnome-common
BuildRequires: gobject-introspection-devel
BuildRequires: sqlite-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: libICE-devel
BuildRequires: libSM-devel
# for autoreconf
BuildRequires: itstool
BuildRequires: yelp-tools

%description
The gnome-games package is a collection of some small "five-minute" games
in a variety of styles and genres for the GNOME desktop.


%package data
Summary: Data files for the GNOME games
BuildArch: noarch
Obsoletes: gnome-games < 1:3.6.0.2-2

%description data
This package contains translations and common files used by the GNOME games.


%package gnomine
Summary: GNOME Mines Sweeper game
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Obsoletes: gnome-games < %{gnome_games_split_version}
Obsoletes: gnome-games-help < %{gnome_games_split_version}
Obsoletes: gnome-games-compat < %{gnome_games_compat_removed_version}

%description gnomine
The popular logic puzzle minesweeper. Find mines on a grid using hints from
squares you have already cleared.


%package iagno
Summary: GNOME Reversi game.
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Obsoletes: gnome-games < %{gnome_games_split_version}
Obsoletes: gnome-games-help < %{gnome_games_split_version}
Obsoletes: gnome-games-compat < %{gnome_games_compat_removed_version}

%description iagno
The GNOME version of Reversi. The goal is to control the most disks on the
board.


%package swell-foop
Summary: GNOME Swell-Foop game
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Obsoletes: gnome-games < %{gnome_games_split_version}
Obsoletes: gnome-games-help < %{gnome_games_split_version}
Obsoletes: gnome-games-compat < %{gnome_games_compat_removed_version}

%description swell-foop
"I want to play that game! You know, they all go whirly-round and you click on
them and they vanish!" - Telsa.


%if %{have_sudoku}
%package sudoku
Summary: GNOME Sudoku game.
BuildArch: noarch
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Obsoletes: gnome-games < %{gnome_games_split_version}
Obsoletes: gnome-games-help < %{gnome_games_split_version}
Obsoletes: gnome-games-compat < %{gnome_games_compat_removed_version}
Provides: gnome-sudoku = %{epoch}:%{version}-%{release}
Obsoletes: gnome-sudoku < %{epoch}:%{version}-%{release}

%description sudoku
A logic game with a Japanese name that has recently exploded in popularity.
%endif


%package glchess
Summary: GNOME Chess game
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Requires: gnuchess
Obsoletes: gnome-games-extra < %{gnome_games_split_version}
Obsoletes: gnome-games-extra-compat < %{gnome_games_compat_removed_version}
Provides: glchess = %{epoch}:%{version}-%{release}
Obsoletes: glchess < 2.0

%description glchess
A chess game which supports several chess engines, with 2D and optionally 3D
support if OpenGL is present.


%package glines
Summary: GNOME "Five or More" game
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Obsoletes: gnome-games-extra < %{gnome_games_split_version}
Obsoletes: gnome-games-extra-compat < %{gnome_games_compat_removed_version}

%description glines
Move balls around the grid and try and form lines. Once you form five in a
row, the line disappears. Unfortunately more balls keep dropping in.


%package gnect
Summary: GNOME "Four in a row" game
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Obsoletes: gnome-games-extra < %{gnome_games_split_version}
Obsoletes: gnome-games-extra-compat < %{gnome_games_compat_removed_version}

%description gnect
Place disks one at a time and try to form a row of four. Tic-tac-toe for those
who like to think.


%package gnibbles
Summary: GNOME Nibbles game
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Obsoletes: gnome-games-extra < %{gnome_games_split_version}
Obsoletes: gnome-games-extra-compat < %{gnome_games_compat_removed_version}

%description gnibbles
Pilot a worm around a maze trying to collect diamonds and at the same time
avoiding the walls and yourself. With each diamond your worm grows longer and
navigation becomes more and more difficult. Playable by up to four people.


%package gnobots2
Summary: GNOME Robots game
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Obsoletes: gnome-games-extra < %{gnome_games_split_version}
Obsoletes: gnome-games-extra-compat < %{gnome_games_compat_removed_version}

%description gnobots2
The classic game where you have to avoid a hoard of robots who are trying to
kill you. Each step you take brings them closer toward you. Fortunately they
aren't very smart and you also have a helpful teleportation gadget.


%package mahjongg
Summary: GNOME Mahjongg game
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Obsoletes: gnome-games-extra < %{gnome_games_split_version}
Obsoletes: gnome-games-extra-compat < %{gnome_games_compat_removed_version}

%description mahjongg
Mahjongg is a simple pattern recognition game. You score points by matching
identical tiles.


%package gnotravex
Summary: GNOME Tetravex game
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Obsoletes: gnome-games-extra < %{gnome_games_split_version}
Obsoletes: gnome-games-extra-compat < %{gnome_games_compat_removed_version}

%description gnotravex
A puzzle game where you have to match a grid of tiles together. The skill
level ranges from the simple two by two up to the seriously mind-bending six
by six grid.


%package gnotski
Summary: GNOME Klotski game
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Obsoletes: gnome-games-extra < %{gnome_games_split_version}
Obsoletes: gnome-games-extra-compat < %{gnome_games_compat_removed_version}

%description gnotski
A series of sliding block puzzles. Try and solve them in the least number of
moves.


%if %{build_tali}
%package gtali
Summary: GNOME Tali game
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Obsoletes: gnome-games-extra < %{gnome_games_split_version}
Obsoletes: gnome-games-extra-compat < %{gnome_games_compat_removed_version}

%description gtali
Sort of poker with dice and less money. An ancient Roman game.
%endif


%package lightsoff
Summary: GNOME Lightsoff game
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Obsoletes: gnome-games-extra < %{gnome_games_split_version}
Obsoletes: gnome-games-extra-compat < %{gnome_games_compat_removed_version}

%description lightsoff
A puzzle played on an 5X5 grid with the aim to turn off all the lights. Each
click on a tile toggles the state of the clicked tile and its non-diagonal
neighbors.


%package quadrapassel
Summary: GNOME falling blocks game
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Obsoletes: gnome-games-extra < %{gnome_games_split_version}
Obsoletes: gnome-games-extra-compat < %{gnome_games_compat_removed_version}

%description quadrapassel
The Russian game of falling geometric shapes.


%prep
%setup -q
%patch0 -p1

%build
%configure --localstatedir=/var/lib \
           --enable-introspection \
           --enable-staging \
           %{omitgames}
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

## things we just don't want in the package
rm -rf $RPM_BUILD_ROOT%{_libdir}/libgdkcardimage.*a
rm -rf $RPM_BUILD_ROOT/var/lib/scrollkeeper

## install desktop files
desktop-file-install --vendor gnome --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --remove-category Application                             \
  --remove-category PuzzleGame                              \
  $RPM_BUILD_ROOT%{_datadir}/applications/*

desktop-file-install --vendor gnome --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  $RPM_BUILD_ROOT%{_datadir}/applications/gnome-glines.desktop \
  $RPM_BUILD_ROOT%{_datadir}/applications/gnome-gnect.desktop

rm -f $RPM_BUILD_ROOT%{_libdir}/gnome-games/libgames-support-gi.{l,}a

%find_lang %{gettext_package} --all-name --with-gnome
# Help files translation are split with each game
grep "/usr/share/locale" %{gettext_package}.lang > translations.lang


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%post gnomine
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gnomine
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans gnomine
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%post iagno
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun iagno
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans iagno
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%post swell-foop
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun swell-foop
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans swell-foop
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%if %{have_sudoku}
%post sudoku
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun sudoku
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
%endif

%posttrans sudoku
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%post glchess
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun glchess
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans glchess
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%post glines
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun glines
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans glines
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%post gnect
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gnect
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans gnect
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%post gnibbles
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gnibbles
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans gnibbles
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%post gnobots2
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gnobots2
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans gnobots2
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%post gnotravex
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gnotravex
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans gnotravex
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%post gnotski
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gnotski
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans gnotski
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%if %{build_tali}
%post gtali
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gtali
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans gtali
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
%endif

%post lightsoff
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun lightsoff
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans lightsoff
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%post mahjongg
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun mahjongg
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans mahjongg
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%post quadrapassel
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun quadrapassel
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans quadrapassel
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files data -f translations.lang
%doc AUTHORS COPYING README
%{_datadir}/icons/hicolor/*/actions/teleport*

%files gnomine
%doc AUTHORS COPYING README
%{_datadir}/applications/gnome-gnomine.desktop
%doc %{_datadir}/help/*/gnomine
%{_datadir}/icons/hicolor/*/apps/gnomine.*
%verify(not md5 size mtime) %config(noreplace) %attr(664, games, games) /var/lib/games/gnomine.*
%{_datadir}/glib-2.0/schemas/org.gnome.gnomine.gschema.xml
# this is a setgid game
%attr(2551, root, games) %{_bindir}/gnomine
%{_mandir}/man6/gnomine.6.gz
%{_datadir}/gnomine

%files iagno
%doc AUTHORS COPYING README
%{_datadir}/applications/gnome-iagno.desktop
%doc %{_datadir}/help/*/iagno
%{_datadir}/iagno
%{_datadir}/icons/hicolor/*/apps/iagno.png
%{_datadir}/glib-2.0/schemas/org.gnome.iagno.gschema.xml
# this is a setgid game
%attr(2551, root, games) %{_bindir}/iagno
%{_mandir}/man6/iagno.6.gz

%files swell-foop
%doc AUTHORS COPYING README
%{_datadir}/applications/gnome-swell-foop.desktop
%doc %{_datadir}/help/*/swell-foop
%{_datadir}/swell-foop
%{_datadir}/icons/hicolor/*/apps/swell-foop.*
# this is a setgid game
%attr(2551, root, games) %{_bindir}/swell-foop
%{_datadir}/glib-2.0/schemas/org.gnome.swell-foop.gschema.xml
%verify(not md5 size mtime) %config(noreplace) %attr(664, games, games) /var/lib/games/swell-foop.*

%if %{have_sudoku}
%files sudoku
%doc AUTHORS COPYING README
%{_datadir}/applications/gnome-sudoku.desktop
%doc %{_datadir}/help/*/gnome-sudoku
%{_datadir}/gnome-sudoku
%{_datadir}/icons/hicolor/*/apps/gnome-sudoku.*
%{python_sitelib}/gnome_sudoku
%{_bindir}/gnome-sudoku
%{_mandir}/man6/gnome-sudoku.6.gz
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-sudoku.gschema.xml
%endif

%files glchess
%doc AUTHORS COPYING README
#%{python_sitelib}/glchess
%{_datadir}/glchess
%{_datadir}/glib-2.0/schemas/org.gnome.glchess.gschema.xml
%{_datadir}/applications/gnome-glchess.desktop
%{_mandir}/man6/glchess.6.gz
%{_bindir}/glchess
%{_datadir}/icons/hicolor/*/apps/glchess.*
%{_datadir}/help/*/glchess

%files glines
%doc AUTHORS COPYING README
%{_datadir}/glib-2.0/schemas/org.gnome.glines.gschema.xml
%{_datadir}/applications/gnome-glines.desktop
%{_mandir}/man6/glines.6.gz
%verify(not md5 size mtime) %config(noreplace) %attr(664, games, games) /var/lib/games/glines.*
# this is a setgid game
%attr(2551, root, games) %{_bindir}/glines
%{_datadir}/glines
%{_datadir}/icons/hicolor/*/apps/glines.*
%{_datadir}/help/*/glines

%files gnect
%doc AUTHORS COPYING README
%{_datadir}/applications/gnome-gnect.desktop
%{_mandir}/man6/gnect.6.gz
%{_bindir}/gnect
%{_datadir}/gnect
%{_datadir}/icons/hicolor/*/apps/gnect.*
%{_datadir}/glib-2.0/schemas/org.gnome.gnect.gschema.xml
%{_datadir}/help/*/gnect

%files gnibbles
%doc AUTHORS COPYING README
%{_datadir}/applications/gnome-gnibbles.desktop
%{_mandir}/man6/gnibbles.6.gz
%verify(not md5 size mtime) %config(noreplace) %attr(664, games, games) /var/lib/games/gnibbles.*
# this is a setgid game
%attr(2551, root, games) %{_bindir}/gnibbles
%{_datadir}/gnibbles
%{_datadir}/icons/hicolor/*/apps/gnibbles.*
%{_datadir}/glib-2.0/schemas/org.gnome.gnibbles.gschema.xml
%{_datadir}/help/*/gnibbles

%files gnobots2
%doc AUTHORS COPYING README
%{_datadir}/applications/gnome-gnobots2.desktop
%{_mandir}/man6/gnobots2.6.gz
%verify(not md5 size mtime) %config(noreplace) %attr(664, games, games) /var/lib/games/gnobots2*
# this is a setgid game
%attr(2551, root, games) %{_bindir}/gnobots2
%{_datadir}/gnobots2
%{_datadir}/icons/hicolor/*/apps/gnobots2.*
%{_datadir}/glib-2.0/schemas/org.gnome.gnobots2.gschema.xml
%{_datadir}/help/*/gnobots2

%files gnotravex
%doc AUTHORS COPYING README
%{_datadir}/gnotravex
%{_datadir}/applications/gnome-gnotravex.desktop
%{_mandir}/man6/gnotravex.6.gz
%verify(not md5 size mtime) %config(noreplace) %attr(664, games, games) /var/lib/games/gnotravex.*
# this is a setgid game
%attr(2551, root, games) %{_bindir}/gnotravex
%{_datadir}/icons/hicolor/*/apps/gnotravex.*
%{_datadir}/glib-2.0/schemas/org.gnome.gnotravex.gschema.xml
%{_datadir}/help/*/gnotravex

%files gnotski
%doc AUTHORS COPYING README
%{_datadir}/applications/gnome-gnotski.desktop
%{_mandir}/man6/gnotski.6.gz
%verify(not md5 size mtime) %config(noreplace) %attr(664, games, games) /var/lib/games/gnotski.*
# this is a setgid game
%attr(2551, root, games) %{_bindir}/gnotski
%{_datadir}/gnotski
%{_datadir}/icons/hicolor/*/apps/gnotski.*
%{_datadir}/glib-2.0/schemas/org.gnome.gnotski.gschema.xml
%{_datadir}/help/*/gnotski

%if %{build_tali}
%files gtali
%doc AUTHORS COPYING README
%{_datadir}/applications/gnome-gtali.desktop
%{_mandir}/man6/gtali.6.gz
%verify(not md5 size mtime) %config(noreplace) %attr(664, games, games) /var/lib/games/gtali.*
# this is a setgid game
%attr(2551, root, games) %{_bindir}/gtali
%{_datadir}/gtali
%{_datadir}/icons/hicolor/*/apps/gtali.*
%{_datadir}/glib-2.0/schemas/org.gnome.gtali.gschema.xml
%{_datadir}/help/*/gtali
%endif

%files lightsoff
%doc AUTHORS COPYING README
%{_datadir}/applications/gnome-lightsoff.desktop
%{_bindir}/lightsoff
%{_datadir}/lightsoff
%{_datadir}/icons/hicolor/*/apps/lightsoff.*
%{_datadir}/glib-2.0/schemas/org.gnome.lightsoff.gschema.xml
%{_datadir}/help/*/lightsoff

%files mahjongg
%doc AUTHORS COPYING README
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-mahjongg.gschema.xml
%{_datadir}/applications/gnome-mahjongg.desktop
%{_mandir}/man6/gnome-mahjongg.6.gz
%verify(not md5 size mtime) %config(noreplace) %attr(664, games, games) /var/lib/games/gnome-mahjongg.*
# this is a setgid game
%attr(2551, root, games) %{_bindir}/gnome-mahjongg
%{_datadir}/gnome-mahjongg
%{_datadir}/icons/hicolor/*/apps/gnome-mahjongg.*
%{_datadir}/help/*/gnome-mahjongg

%files quadrapassel
%doc AUTHORS COPYING README
%{_datadir}/applications/gnome-quadrapassel.desktop
%{_mandir}/man6/quadrapassel.6.gz
%verify(not md5 size mtime) %config(noreplace) %attr(664, games, games) /var/lib/games/quadrapassel.*
# this is a setgid game
%attr(2551, root, games) %{_bindir}/quadrapassel
%{_datadir}/quadrapassel
%{_datadir}/icons/hicolor/*/apps/quadrapassel.*
%{_datadir}/glib-2.0/schemas/org.gnome.quadrapassel.gschema.xml
%{_datadir}/help/*/quadrapassel


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1:3.6.1-6
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1:3.6.1-5
- 为 Magic 3.0 重建

* Tue Mar  5 2013 Hans de Goede <hdegoede@redhat.com> - 1:3.6.1-4
- Fix glchess not working when playing against the computer (rhbz#917305)

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.6.1-3
- Rebuilt for cogl soname bump

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1:3.6.1-2
- Rebuild for new cogl

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.6.1-1
- Update to 3.6.1

* Sat Oct 13 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.6.0.2-2
- Improvements to the way the package split is handled on upgrades

* Wed Sep 26 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.6.0.2-1
- Update to 3.6.0.2

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.6.0.1-1
- Update to 3.6.0.1

* Tue Aug 28 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.5.90-2
- Rebuild against new cogl/clutter

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.90-1
- Update to 3.5.90

* Sat Aug 11 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 1:3.5.5-3
- Specify the Epoch for Requires/Obsoletes. Not having it in the previous
  commit was breaking the upgrade path.
- Add missing doc/license files in all packages. This is especially important
  for the two 'compat' packages. Without it, they were empty and as such
  would not be generated, which broke the upgrade path.

* Wed Aug 08 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 1:3.5.5-2
- Split each game and its help into its own subpackage.
  https://bugzilla.redhat.com/show_bug.cgi?id=846274

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.4-1
- Update to 3.5.4

* Thu Jun 07 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.5.2-2
- Fix file lists

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.2-1
- Update to 3.5.2

* Fri May 18 2012 Richard Hughes <hughsient@gmail.com> - 1:3.4.2-1
- Update to 3.4.2

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.4.1-2
- Silence rpm scriptlet output

* Tue Apr 17 2012 Richard Hughes <hughsient@gmail.com> - 1:3.4.1-1
- Update to 3.4.1

* Mon Apr  2 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.4.0-3
- Install swell-foop setgid, so it can save its scores (#808367)

* Wed Mar 28 2012 Richard Hughes <rhughes@redhat.com> - 1:3.4.0-2
- Fix the build by fixing the French help translation.

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 1:3.4.0-1
- Update to 3.4.0

* Mon Mar 26 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.3.92-3
- Remove last traces of GConf handling

* Sat Mar 24 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.3.92-2
- Simplify spec file, seed games were rewritten in vala

* Wed Mar 21 2012 Richard Hughes <rhughes@redhat.com> 3.3.92-1
- Update to 3.3.92

* Thu Mar 15 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.3.91.1-3
- Move swell-foop icon to same package as binary (#798673)

* Sat Mar 10 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.3.91.1-2
- Rebuild against new cogl

* Tue Mar  6 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.3.91.1-1
- Update to 3.3.91.1

* Sun Feb 26 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.3.5-2
- Rebuild against new cogl

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.3.5-1
- Update to 3.3.5

* Wed Jan 18 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.3.4.1-1
- Update to 3.3.4.1

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 02 2012 John (J5) Palmieri <johnp@redhat.com> - 1:3.3.3-2
- add patch which fixes type check bug to work with newer PyGObject

* Fri Dec 23 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.3.3-1
- Update to 3.3.3

* Thu Nov 24 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.3.1-2
- Rebuild against new clutter

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.3.1-1
- Update to 3.3.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.1-2
- Rebuilt for glibc bug#747377

* Wed Oct 19 2011 Matthias Clsaen <mclasen@redhat.com> - 1:3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 1:3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.1.92-1
- Update to 3.1.92

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.1.91-1
- Update to 3.1.91

* Fri Sep  2 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.1.90-2
- Require gobject-introspection (#732777)

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.1.90-1
- Update to 3.1.90

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.1.5-1
- Update to 3.1.5

* Mon Aug  8 2011 Michel Salim <salimma@fedoraproject.org> - 1:3.1.4-3
- Reenable seed games

* Wed Jul 27 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-2
- Rebuild

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Wed Jul  6 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.3-1
- Update to 3.1.3

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Tue Apr 19 2011 Christopher Aillon <caillon@redhat.com> - 3.0.1.1-1
- Update to 3.0.1.1

* Mon Apr 18 2011 Christopher Aillon <caillon@redhat.com> - 3.0.1-2
- Drop unneeded patches

* Mon Apr 18 2011 Christopher Aillon <caillon@redhat.com> - 3.0.1-1
- Update to 3.0.1
- Re-enable seed games

* Thu Apr  7 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-2
- Make the install quiet (#691426)

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Thu Mar 31 2011 Jon McCann <jmccann@redhat.com> - 2.91.94-0.20110331.1
- Update to snapshot with new icons

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.93-1
- Update to 2.91.93

* Sat Mar 19 2011 Christopher Aillon <caillon@redhat.com> - 2.91.91-1
- Update to 2.91.91

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.91.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.2-1
- Update to 2.91.2

* Fri Nov  5 2010 Michel Salim <salimma@fedoraproject.org> - 1:2.32.0-4
- Only require seed if seed games are enabled
- spec cleanups

* Fri Oct 01 2010 Ray Strode <rstrode@redhat.com> 2.32.0-3
- Temporarily disable seed games
  Resolves: #636118

* Fri Oct 01 2010 Jesse Keating <jkeating@redhat.com> - 2.32.0-2
- Add missing dep in -extra  RHBZ 639130

* Thu Sep 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Fri Sep 24 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.92.1-1
- Update to 2.31.92

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.91.1-1
- Update to 2.31.91.1

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.90-1
- Update to 2.31.90

* Sat Aug  7 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.6-1
- Update to 2.31.6

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1:2.31.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.5-1
- Update to 2.31.5

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.4-1
- Update to 2.31.4

* Wed Jun 23 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-2
- Try with seed

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-1
- Update to 2.31.3

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.2-1
- Update to 2.31.2

* Tue Apr 27 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Tue Mar 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-1
- Update to 2.29.92

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.91-1
- Update to 2.29.91

* Sun Feb 14 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.6-2
- Add missing libs

* Tue Jan 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.6-1
- Update to 2.29.6

* Tue Jan 12 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.5-1
- Update to 2.29.5

* Thu Jan  7 2010 Hans de Goede <hdegoede@redhat.com> - 2.29.4-3
- Change python_sitelib macro to use %%global as the new rpm will break
  using %%define here, see:
  https://www.redhat.com/archives/fedora-devel-list/2010-January/msg00093.html

* Sat Jan  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.4-2
- Omit swell-foop

* Tue Dec 22 2009 Matthias Clasen <mclasen@redhat.com> 2.29.4-1
- Update to 2.29.4

* Sat Dec 05 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 2.29.3-2
- Fix syntax error on scriptlets

* Tue Dec 01 2009 Bastien Nocera <bnocera@redhat.com> 2.29.3-1
- Update to 2.29.3

* Mon Oct 19 2009 Matthias Clasen <mclasen@redhat.com> 2.28.1-1
- Update to 2.28.1

* Mon Sep 22 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-1
- Update to 2.28.0

* Mon Sep  7 2009 Matthias Clasen <mclasen@redhat.com> 2.27.92-1
- Update to 2.27.92

* Sun Aug 23 2009 Matthias Clasen <mclasen@redhat.com> 2.27.90-2
- Fix various issues in Mines

* Fri Aug 14 2009 Matthias Clasen <mclasen@redhat.com> 2.27.90-1
- Updated to 2.27.90

* Fri Jul 31 2009 Matthias Clasen <mclasen@redhat.com> 2.27.5-5
- Drop unneeded python deps

* Fri Jul 31 2009 Matthias Clasen <mclasen@redhat.com> 2.27.5-4
- Fix a typo (#515033)

* Fri Jul 31 2009 Matthias Clasen <mclasen@redhat.com> 2.27.5-3
- Split off a subset of games to include on the live cd

* Thu Jul 30 2009 Bastien Nocera <bnocera@redhat.com> 2.27.5-2
- Rebuild for new clutter-gtk and clutter

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> 2.27.5-1
- Update to 2.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Matthias Clasen <mclasen@redhat.com> 2.27.4-1
- Update to 2.27.4

* Sat Jun 20 2009 Bastien Nocera <bnocera@redhat.com> 2.27.3-1
- Update to 2.27.3

* Sun Jun 14 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.2-2
- Minor directory ownership cleanup

* Wed May 27 2009 Bastien Nocera <bnocera@redhat.com> 2.27.2-1
- Update to 2.27.2

* Mon May 18 2009 Bastien Nocera <bnocera@redhat.com> 2.27.1-1
- Update to 2.27.1

* Mon Apr 27 2009 Matthias Clasen <mclasen@redhat.com> - 1:2.26.1-2
- don't drop schemas translations from po files

* Tue Apr 14 2009 Matthias Clasen <mclasen@redhat.com> - 1:2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/gnome-games/2.26/gnome-games-2.26.1.news

* Wed Apr  1 2009 Matthias Clasen <mclasen@redhat.com> - 1:2.26.0-2
- Add a workaround for sudoku crashing on certain saved games (#492962)

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 1:2.26.0-1
- Update to 2.26.0

* Mon Mar  2 2009 Matthias Clasen <mclasen@redhat.com> - 1:2.25.92-1
- Update 2.25.92

* Tue Feb 24 2009 Matthias Clasen <mclasen@redhat.com> - 1:2.25.91-2
- Make gnome-games-help noarch

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Matthias Clasen <mclasen@redhat.com> - 1:2.25.91-1
- Update to 2.25.91

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 1:2.25.90-1
- Update to 2.25.90

* Fri Jan 23 2009 Matthias Clasen <mclasen@redhat.com> - 1:2.25.5-1
- Update to 2.25.5

* Tue Jan  6 2009 Matthias Clasen <mclasen@redhat.com> - 1:2.25.4-1
- Update to 2.25.4

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.25.3-1
- Update to 2.25.3

* Thu Dec  4 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.25.2-2
- Rebuild for Python 2.6

* Wed Dec  3 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.25.2-1
- Update to 2.25.2

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1:2.25.1-4
- Rebuild for Python 2.6

* Fri Nov 21 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.25.1-3
- Better URL
- Tweak description

* Thu Nov 13 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.25.1-2
- Update to 2.25.1

* Mon Oct 20 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.24.1-1
- Update to 2.24.1

* Thu Sep 25 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.24.0-2
- Save some space

* Sun Sep 21 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.24.0-1
- Update to 2.24.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.23.92-1
- Update to 2.23.92
- Adapt to api changes in the ggz snapshot we ship

* Sat Aug 23 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.23.90-1
- Update to 2.23.90

* Fri Aug  8 2008 Colin Walters <walters@redhat.com> - 1:2.23.6-2
- Split out -help into separate package for size reasons

* Tue Aug  5 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.23.6-1
- Update to 2.23.6

* Wed Jul 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:2.23.5-2
- fix license tag

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.23.5-1
- Update to 2.23.5

* Wed Jun 18 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.23.4-1
- Update to 2.23.4

* Tue Jun  3 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.23.3-1
- Update to 2.23.3

* Sun May 11 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.23.1-2
- Add missing Requires for gnome-sudoko (#445941)

* Fri Apr 25 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.23.1-1
- Update to 2.23.1

* Fri Apr 18 2008 Ray Strode <rstrode@redhat.com> - 1:2.22.1.1-4
- Use gtk-missing-image instead of image-missing since a lot of
  icon themes don't have missing-image and gtk-missing-image is
  guaranteed to be available (bug 440686)

* Thu Apr 17 2008 Ray Strode <rstrode@redhat.com> - 1:2.22.1.1-3
- Fix typo in previous patch (bug 440686)

* Wed Apr 16 2008 Ray Strode <rstrode@redhat.com> - 1:2.22.1.1-2
- Make glchess behave better in case of incomplete icon themes
  (bug 440686)

* Tue Apr  8 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.22.1.1-1
- Update to 2.22.1 (sudoko crasher fixes)

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.22.1-1
- Update to 2.22.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.22.0-1
- Update to 2.22.0

* Thu Mar  6 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.21.92-2
- Drop OnlyShowIn=GNOME

* Tue Feb 26 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.21.92-1
- Update to 2.21.92

* Wed Feb 13 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.21.91-1
- Update to 2.21.91

* Fri Feb  8 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.21.90-2
- Fix ggz deps

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.21.90-1
- Update to 2.21.90 

* Tue Jan 15 2008 Matthias Clasen <mclasen@redhat.com> - 1:2.21.5-1
- Update to 2.21.5

* Tue Dec 18 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.21.4-1
- Update to 2.21.4

* Tue Dec 11 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 1:2.21.3-2
- Fix rpm --verify complaining about the highscore files once a highscore has
  been added (bz 418991)

* Thu Dec  6 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.21.3-1
- Update to 2.21.3
- Build against system ggz packages

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.21.2-1
- Update to 2.21.2

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.20.1-1
- Update to 2.20.1 (bug fixes)
- Drop obsolete patch

* Tue Oct  9 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 1:2.20.0.1-2
- Fix gnobots from crashing with certain combinations of options (bz 324221)

* Tue Sep 18 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.20.0.1-1
- Update to 2.20.0.1

* Tue Sep 18 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.20.0-1
- Update to 2.20.0

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.19.92-1
- 2.19.92

* Tue Aug 28 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 1:2.19.90.1-2
- Rebuild for new expat 2.0

* Tue Aug 14 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.19.90.1-1
- 2.19.90.1

* Sun Aug 12 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.19.90b-1
- 2.19.90b

* Sat Aug 11 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.19.90-1
- 2.19.90

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.19.6-4
- Add documentation license

* Sun Aug  5 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.19.6-3
- Use find-lang for help files, too

* Fri Aug  3 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.19.6-2
- Update the license field

* Sat Jul 28 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.19.6-1
- Update to 2.19.6

* Sat Jul 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 1:2.19.4-3
- Don't build a private copy of gnuchess, instead require gnuchess (bz 215110)
- Rename / rebrand Gnometris to GnomeFallingBlocks, so that it stays clear of
  the Tetris trademark, and include it (bz 238651)
- Don't own dirs under /usr/share/icons/hicolor, instead add
  Requires: hicolor-icon-theme
- Cleanup handling of with_card and with_tali defines using --enable-omitgames

* Thu Jul  5 2007 Ray Strode <rstrode@redhat.com> - 1:2.19.4-2
- Add glchess back (bug 234127)

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.19.4-1
- Update to 2.19.4

* Sat Jun 16 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.19.3-2
- More complete runtime requirements for sudoko (#241884)

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.19.3-1
- Update to 2.19.3
- Add a BuildRequires for gstreamer

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.19.2-1
- Update to 2.19.2
- Fix file lists

* Mon May  7 2007 Ray Strode <rstrode@redhat.com> - 1:2.18.1.1-1
- update to 2.18.1.1 at the request of Andreas Røsdal

* Sun Apr  8 2007 Ray Strode <rstrode@redhat.com> - 1:2.18.0-5
- Add Obsoletes: gnome-chess (bug 234127)

* Mon Apr  2 2007 Ray Strode <rstrode@redhat.com> - 1:2.18.0-4
- Add minimum version to gnome-python2-desktop buildreq 
  (bug 234892)

* Wed Mar 28 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.18.0-3
- Split of gnome-games-extra-data as a separate package
- Correct the License tag

* Fri Mar 23 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.18.0-2
- Fix the icon in the blackjack about dialog (#233649)

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.18.0-1
- Update to 2.18.0

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.17.92-1
- Update to 2.17.92

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.17.91-1
- Update to 2.17.91

* Wed Jan 24 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.17.90.1-1
- Update to 2.17.90.1

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.17.90-2
- Update extra data to 2.17.90

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.17.90-1
- Update to 2.17.90
- Fix some directory ownership issues

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.17.5-1
- Update to 2.17.5

* Wed Dec 20 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.17.4.1-1
- Update to 2.17.4.1

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1:2.17.3-2
- rebuild for python 2.5

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.17.3-1
- Update to 2.17.3

* Thu Nov 16 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.17.2-4
- Use Conflicts for gnuchess instead

* Wed Nov 15 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.17.2-3
- Add Provides/Obsoletes for gnuchess (#215110)

* Wed Nov  8 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.17.2-2
- Add Provides/Obsoletes for gnome-sudoku (#214589)

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.17.2-1
- Update to 2.17.2

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.17.1-1
- Update to 2.17.1

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.16.0-1.fc6
- Update to 2.16.0

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.15.92-1.fc6
- Update to 2.15.92

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.15.6-1.fc6
- Update to 2.15.6

* Thu Aug  2 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.15.5-1.fc6
- Update to 2.15.5
- Bump glib requirement (#197566)

* Tue Jul 25 2006 Ray Strode <rstrode@redhat.com> - 1:2.15.4-3
- install new gconf schemas. rework the way we do it to be more
  future proof (bug 193777)

* Tue Jul 25 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.15.4-2
- Require librsvg2 (#191576)

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.15.4-1
- Update to 2.15.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:2.15.3-1.1
- rebuild

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.15.3-1
- Update to 2.15.3

* Wed May 16 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.15.2-1
- Update to 2.15.2

* Tue May 16 2006 Ray Strode <rstrode@redhat.com> - 1:2.15.1-2
- Apply spec file patch from 
  Hooman Mesgary <hooman@farsiweb.info> to conditionallly
  compile out some of the games (bug 192001)

* Wed May 10 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.15.1-1
- Update to 2.15.1

* Tue May 9 2006 Ray Strode <rstrode@redhat.com> - 1:2.14.1-4
- rebuild

* Mon Apr 24 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.14.1-3
- Update the extra data to 2.14.0

* Mon Apr 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-2
- Update to 2.14.1

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Thu Feb 23 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.8-1
- Update to 2.13.8

* Mon Feb 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.7-1
- Update to 2.13.7

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:2.13.6-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:2.13.6-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sat Feb  4 2006 Matthias Clasen <mclasen@redhat.com> 1:2.13.6-3
- Remove unneeded gstreamer dependency

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com> 1:2.13.6-1
- Update to 2.13.6

* Mon Jan 23 2006 Christopher Aillon <caillon@redhat.com> 1:2.13.5-2
- Add patch to fix parse errors with aunt mary.

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> 1:2.13.5-1
- Update to 2.13.5

* Fri Jan 06 2006 Ray Strode <rstrode@redhat.com> 1:2.13.4-2
- remove "Windows" theme from gnobots

* Tue Jan 03 2006 Matthias Clasen <mclasen@redhat.com> 1:2.13.4-1
- Update to 2.13.4

* Thu Dec 15 2005 Matthias Clasen <mclasen@redhat.com> 1:2.13.3-1
- Update to 2.13.3

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec 1 2005 Matthias Clasen <mclasen@redhat.com> 1:2.13.2-1
- Update to 2.13.2

* Wed Nov 2 2005 Ray Strode <rstrode@redhat.com> 1:2.12.1-4
- don't link to howl now that we aren't using it

* Mon Oct 31 2005 Ray Strode <rstrode@redhat.com> 1:2.12.1-3
- rebuild

* Mon Oct 31 2005 Ray Strode <rstrode@redhat.com> 1:2.12.1-2
- remove howl dependency
- modernize make install lines

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> 1:2.12.1-1
- Update to 2.12.1

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> 1:2.12.0-1
- Update to 2.12.0

* Tue Aug 16 2005 Matthias Clasen <mclasen@redhat.com> 
- New upstream version

* Fri Aug  5 2005 Matthias Clasen <mclasen@redhat.com> 1:2.11.3-1
- New upstream version

* Mon Jul 11 2005 Matthias Clasen <mclasen@redhat.com> 1:2.11.1-1
- Update to 2.11.1

* Fri May 20 2005 Ray Strode <rstrode@redhat.com> 1:2.10.0-5
- Fix gnibbles crasher, patch from 
  Richard Hoelscher <rah@rahga.com> (bug 158269).

* Thu May 19 2005 Ray Strode <rstrode@redhat.com> 1:2.10.0-4
- Change some sounds around

* Sun Apr 10 2005 Warren Togami <wtogami@redhat.com> 1:2.10.0-3
- undo previous change
- remove unnecessary ldconfig calls
- remove crack obsolete

* Sun Apr 10 2005 Ray Strode <rstrode@redhat.com> 1:2.10.0-2
- Add requires line for guile (bug 154297)

* Fri Apr  8 2005 Ray Strode <rstrode@redhat.com> 1:2.10.0-1
- Update to 2.10.0

* Wed Feb  9 2005 Matthias Clasen <mclasen@redhat.com> 1:2.9.6-1
- Update to 2.9.6
- Needs to wait for newer guile

* Tue Oct 19 2004 Christopher Aillon <caillon@redhat.com> 1:2.8.0-4
- Remove gnome-stones for now

* Thu Oct 14 2004 Marco Pesenti Gritti <mpg@redhat.com> 1:2.8.0-3
- 135591 Ataxx crashes on launch

* Thu Sep 30 2004 GNOME <jrb@redhat.com> - 1:2.8.0-2
- fix crasher, #134256

* Wed Sep 22 2004 Christopher Aillon <caillon@redhat.com> 2.8.0-1
- Update to 2.8.0 and gnome-games-extra-data 2.8.0

* Mon Aug 23 2004 Christopher Aillon <caillon@redhat.com> 2.7.7-1
- Update to 2.7.7 including gnome-games-extra-data-2.7.0

* Wed Aug 04 2004 Christopher Aillon <caillon@redhat.com> 2.7.6-1
- Update to 2.7.6

* Tue Aug 3 2004 Matthias Clasen <mclasen@redhat.com> 2.7.5-2
- Rebuilt

* Sat Jul 31 2004 Christopher Aillon <caillon@redhat.com> 2.7.5-1
- Bump to 2.7.5

* Wed Jun 30 2004 Christopher Aillon <caillon@redhat.com> 2.6.2-1
- Update to 2.6.2

* Wed Jun 16 2004 Christopher Aillon <caillon@redhat.com>
- Update to 2.6.1

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 21 2004 Matthias Clasen <mclasen@redhat.com> 2.6.0.1-3 
- rebuild

* Wed Apr 14 2004 Warren Togami <wtogami@redhat.com> 2.6.0.1-2
- #111114 BR perl-XML-Parser scrollkeeper librsvg2-devel gettext

* Fri Apr  2 2004 Mark McLoughlin <markmc@redhat.com> 2.6.0.1-1
- Update to 2.6.0.1

* Wed Mar 10 2004 Alex Larsson <alexl@redhat.com> 1:2.5.8-1
- update to 2.5.8

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Alexander Larsson <alexl@redhat.com> 1:2.5.7-1
- update to 2.5.7

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Jonathan Blandford <jrb@redhat.com> 1:2.5.5-1
- new version

* Tue Oct 21 2003 Jeremy Katz <katzj@redhat.com> 1:2.4.0-3
- add patch so that gtali doesn't crash (#106524)

* Fri Oct  3 2003 Alexander Larsson <alexl@redhat.com> 1:2.4.0-2
- 2.4.0

* Mon Aug 25 2003 Alexander Larsson <alexl@redhat.com> 1:2.3.8-1
- update for gnome 2.3
- don't build aisleriot on ia64 due to some strange guile lib issue

* Mon Jul 28 2003 Havoc Pennington <hp@redhat.com> 1:2.2.1-2
- rebuild

* Mon Jul  7 2003 Havoc Pennington <hp@redhat.com> 1:2.2.1-1
- 2.2.1
- remove "applyschemas" patch fixed upstream
- remove "stonescrash" patch also fixed upstream

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Sun Feb 23 2003 Jeremy Katz <katzj@redhat.com> 1:2.2.0-2
- apply the gnect schemas (#84905)
- gnome-stones shouldn't crash on startup (#84904)

* Wed Feb  5 2003 Havoc Pennington <hp@redhat.com> 1:2.2.0-1
- 2.2.0

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan  9 2003 Havoc Pennington <hp@redhat.com>
- 2.1.5

* Wed Dec  4 2002 Havoc Pennington <hp@redhat.com>
- munge empty string default value out of gtali.schemas
- increment version numbers on requirements

* Tue Dec  3 2002 Bill Nottingham <notting@redhat.com> 1:2.1.3-2
- rebuild against new guile

* Mon Dec  2 2002 Tim Powers <timp@redhat.com> 1:2.1.3-1
- update to 2.1.3

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- add some OnlyShowIn

* Mon Aug 12 2002 Havoc Pennington <hp@redhat.com>
- 2.0.3 from gnome 2.0.1

* Tue Aug  6 2002 Havoc Pennington <hp@redhat.com>
- 2.0.2

* Tue Jul 23 2002 Havoc Pennington <hp@redhat.com>
- gnect doesn't like being setgid games
- obsolete gnome-games-devel

* Fri Jul 12 2002 Havoc Pennington <hp@redhat.com>
- add gnect

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0
- remove noreplace from the .soundlist files
- add missing schemas
- get rid of gnometris again
- use desktop-file-install

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed Jun  5 2002 Havoc Pennington <hp@redhat.com>
- 1.93.0
- remove empty NEWS/README
- fix ldconfig in post

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- 1.92.0

* Fri May  3 2002 Havoc Pennington <hp@redhat.com>
- 1.91.0

* Fri Apr 19 2002 Havoc Pennington <hp@redhat.com>
- GNOME 2 version
- spec file cleanups
- no devel package
- don't run auto*, just use the "rm from buildroot" approach to lose xbill

* Tue Apr 09 2002 Phil Knirsch <pknirsch@redhat.com>
- Bumped version number for rebuild and relink agains new guile lib

* Tue Aug 14 2001 Jonathan Blandford <jrb@redhat.com>
- Add BuildRequires on ncurses-devel

* Mon Jul 23 2001 Jonathan Blandford <jrb@redhat.com>
- Add BuildRequires

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Fri Apr 20 2001  <jrb@redhat.com>
- New version (1.4.0)

* Tue Apr 17 2001 Jonathan Blandford <jrb@redhat.com>
- New Version.

* Tue Feb 27 2001 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath}
- langify

* Mon Aug 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- run ldconfig in post and postun (#16589)
- don't put the post and postun scripts in the middle of the files list --
  that tends to break things (oops)

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Fri Aug 04 2000 Havoc Pennington <hp@redhat.com>
- Remove .desktop for gturing

* Mon Jul 17 2000 Jonathan Blandford <jrb@redhat.com>
- Mark high-score files as %%config(noreplace).

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Sat Jul 8 2000 Havoc Pennington <hp@redhat.com>
- Remove Docdir

* Tue Jul 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Jun 15 2000 Owen Taylor <otaylor@redhat.com>
- 1.2.0
- remove gnometris, xbill from subdirs since we don't install
  them and they cause problems with new C compiler
- update autoconf stuff
- remove gturing, add gnotski to the file list

* Thu May 11 2000 Matt Wilson <msw@redhat.com>
- 1.1.90

* Thu Feb 10 2000 Preston Brown <pbrown@redhat.com>
- mark sound event files as config files

* Tue Sep 21 1999 Michael Fulbright <drmike@redhat.com>
- fixed gnotravex to not loop infinitely

* Mon Sep 20 1999 Elliot Lee <sopwith@redhat.com>
- Update to 1.0.40

* Sat Apr 10 1999 Jonathan Blandford <jrb@redhat.com>
- added new sol games and a fix for the old ones.

* Mon Mar 29 1999 Michael Fulbright <drmike@redhat.com>
- removed more offending t*tris stuff

* Thu Mar 18 1999 Michael Fulbright <drmike@redhat.com>
- version 1.0.2
- made gnibbles have correct attr since its setgid
- strip binaries

* Sun Mar 14 1999 Michael Fulbright <drmike@redhat.com>
- added score files to file list

* Thu Mar 04 1999 Michael Fulbright <drmike@redhat.com>
- Version 1.0.1

* Fri Feb 19 1999 Michael Fulbright <drmike@redhat.com>
- removed *tris games

* Mon Feb 15 1999 Michael Fulbright <drmike@redhat.com>
- version 0.99.8
- added sound event lists to file list
- touched up file list some more

* Wed Feb 03 1999 Michael Fulbright <drmike@redhat.com>
- added gnibbles data to file list

* Wed Feb 03 1999 Michael Fulbright <drmike@redhat.com>
- updated to 0.99.7

* Wed Feb 03 1999 Michael Fulbright <drmike@redhat.com>
- updated to 0.99.5

* Mon Jan 18 1999 Michael Fulbright <drmike@redhat.com>
- updated to 0.99.3

* Wed Jan 06 1999 Michael Fulbright <drmike@redhat.com>
- updated to 0.99.1

* Thu Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- updated to 0.99.0 in prep for GNOME 1.0

* Sat Nov 21 1998 Michael Fulbright <drmike@redhat.com>
- updated for 0.30 tree

* Fri Nov 20 1998 Pablo Saratxaga <srtxg@chanae.alphanet.ch>
- use --localstatedir=/var/lib in config state (score files for games
  for exemple will go there).

* Mon Mar 16 1998 Marc Ewing <marc@redhat.com>
- Integrate into gnome-games CVS source tree

