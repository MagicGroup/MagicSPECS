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


Name:		trinity-tdegames
Summary:	Trinity Desktop Environment - Games
Version:	3.5.13.2
Release:	1%{?dist}%{?_variant}

License:	GPLv2
Group:		Amusements/Games

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source: 	kdegames-trinity-%{version}.tar.xz

BuildRequires:	autoconf automake libtool m4
BuildRequires:	trinity-tdelibs-devel
BuildRequires:	libtool

BuildRequires:	tqtinterface-devel >= %{version}
BuildRequires:	trinity-arts-devel >= %{version}
BuildRequires:	trinity-tdemultimedia-devel >= %{version}
BuildRequires:	qt-devel

Obsoletes:		trinity-kdegames < %{version}-%{release}
Provides:		trinity-kdegames = %{version}-%{release}
Obsoletes:		trinity-kdegames-libs < %{version}-%{release}
Provides:		trinity-kdegames-libs = %{version}-%{release}

Requires: trinity-libtdegames1 = %{version}-%{release}
Requires: trinity-tdegames-card-data = %{version}-%{release}
Requires: trinity-atlantik = %{version}-%{release}
Requires: trinity-kasteroids = %{version}-%{release}
Requires: trinity-katomic = %{version}-%{release}
Requires: trinity-kbackgammon = %{version}-%{release}
Requires: trinity-kbattleship = %{version}-%{release}
Requires: trinity-kblackbox = %{version}-%{release}
Requires: trinity-kbounce = %{version}-%{release}
Requires: trinity-kenolaba = %{version}-%{release}
Requires: trinity-kfouleggs = %{version}-%{release}
Requires: trinity-kgoldrunner = %{version}-%{release}
Requires: trinity-kjumpingcube = %{version}-%{release}
Requires: trinity-klickety = %{version}-%{release}
Requires: trinity-klines = %{version}-%{release}
Requires: trinity-kmahjongg = %{version}-%{release}
Requires: trinity-kmines = %{version}-%{release}
Requires: trinity-knetwalk = %{version}-%{release}
Requires: trinity-kolf = %{version}-%{release}
Requires: trinity-konquest = %{version}-%{release}
Requires: trinity-kpat = %{version}-%{release}
Requires: trinity-kpoker = %{version}-%{release}
Requires: trinity-kreversi = %{version}-%{release}
Requires: trinity-ksame = %{version}-%{release}
Requires: trinity-kshisen = %{version}-%{release}
Requires: trinity-ksirtet = %{version}-%{release}
Requires: trinity-ksmiletris = %{version}-%{release}
Requires: trinity-ksnake = %{version}-%{release}
Requires: trinity-ksokoban = %{version}-%{release}
Requires: trinity-kspaceduel = %{version}-%{release}
Requires: trinity-ktron = %{version}-%{release}
Requires: trinity-ktuberling = %{version}-%{release}
Requires: trinity-twin4 = %{version}-%{release}
Requires: trinity-lskat = %{version}-%{release}


%description
Games and gaming libraries for the Trinity Desktop Environment.
Included with this package are: kenolaba, kasteroids, kblackbox, kmahjongg,
kmines, konquest, kpat, kpoker, kreversi, ksame, kshisen, ksmiletris,
ksnake, ksirtet, katomic, kjumpingcube, ktuberling.

%files

##########

%package devel
Summary:	Development files for %{name} 
Group:		Development/Libraries
License:	LGPLv2

Requires:	%{name} = %{version}-%{release}
Requires:	trinity-tdelibs-devel >= 3.5.13
Requires:	trinity-libtdegames-devel = %{version}-%{release}
Requires:	trinity-atlantik-devel = %{version}-%{release}
Requires:	trinity-kolf-devel = %{version}-%{release}

Obsoletes:		trinity-kdegames-devel < %{version}-%{release}
Provides:		trinity-kdegames-devel = %{version}-%{release}

%description devel
%{summary}.

Install %{name}-devel if you wish to develop or compile games for the
TDE desktop.

%files devel
%defattr(-,root,root,-)

##########

%package -n trinity-libtdegames1
Summary:	Trinity games library and common files
Group:		Amusements/Games

%description -n trinity-libtdegames1
This library provides a common infrastructure for several of the
games in the TDE distribution. Features include standardized menu
items, high score handling, card display, and network connections
including chat capabilities.

This package is part of TDE, and a component of the TDE games module.

%files -n trinity-libtdegames1
%defattr(-,root,root,-)
%{tde_libdir}/lib[kt]degames.so.*
%{tde_datadir}/apps/[kt]degames/pics/star.png
%{tde_datadir}/icons/crystalsvg/*/actions/roll.png
%{tde_datadir}/icons/crystalsvg/*/actions/highscore.png
%{tde_tdedocdir}/HTML/en/[kt]degames-trinity-%{version}-apidocs/

%post -n trinity-libtdegames1
for f in crystalsvg ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
/sbin/ldconfig || :

%postun -n trinity-libtdegames1
for f in crystalsvg ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
/sbin/ldconfig || :

##########

%package -n trinity-libtdegames-devel
Summary:	Trinity games library headers
Group:		Development/Libraries
Requires:	trinity-libtdegames1 = %{version}-%{release}

%description -n trinity-libtdegames-devel
This package is necessary if you want to develop your own games using
the TDE games library.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-libtdegames-devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/*.h
%{tde_tdeincludedir}/kgame
%{tde_libdir}/lib[kt]degames.so
%{tde_libdir}/lib[kt]degames.la

##########

%package card-data
Summary:	Card decks for Trinity games
Group:		Amusements/Games

%description card-data
Several different collections of card images for use by TDE games.

This package is part of Trinity, and a component of the TDE games module.

%files card-data
%defattr(-,root,root,-)
%{tde_datadir}/apps/carddecks/*

##########

%package -n trinity-atlantik
Summary:	TDE client for Monopoly-like network games
Group:		Amusements/Games

%description -n trinity-atlantik
This is a TDE client for playing Monopoly-like boardgames on the
monopd network.  It can play any board supported by the network
server, including the classic Monopoly game, as well as the Atlantik
game in which the property includes several major cities in North
America and Europe.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-atlantik
%defattr(-,root,root,-)
%{tde_bindir}/atlantik
%{tde_libdir}/libatlantic.so.*
%{tde_libdir}/libatlantikclient.so.*
%{tde_libdir}/libatlantikui.so.*
%{tde_tdelibdir}/kio_atlantik.la
%{tde_tdelibdir}/kio_atlantik.so
%{tde_datadir}/services/atlantik.protocol
%{tde_tdeappdir}/atlantik.desktop
%{tde_datadir}/icons/hicolor/*/apps/atlantik.png
%{tde_datadir}/apps/atlantik/
%{tde_tdedocdir}/HTML/en/atlantik/

%post -n trinity-atlantik
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
/sbin/ldconfig || :
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-atlantik
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
/sbin/ldconfig || :
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-atlantik-devel
Summary:	Development files for Atlantik
Group:		Development/Libraries
Requires:	trinity-atlantik = %{version}-%{release}

%description -n trinity-atlantik-devel
This package contains header files for compiling programs against the
libraries which come with Atlantik.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-atlantik-devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/atlantik
%{tde_tdeincludedir}/atlantic
%{tde_libdir}/libatlantic.so
%{tde_libdir}/libatlantic.la
%{tde_libdir}/libatlantikclient.so
%{tde_libdir}/libatlantikclient.la
%{tde_libdir}/libatlantikui.so
%{tde_libdir}/libatlantikui.la

%post -n trinity-atlantik-devel
/sbin/ldconfig || :

%postun -n trinity-atlantik-devel
/sbin/ldconfig || :

##########

%package -n trinity-kasteroids
Summary:	Asteroids for Trinity
Group:		Amusements/Games

%description -n trinity-kasteroids
You know this game.  It is based on Warwick Allison's QwSpriteField
widget.

The objective of kasteroids is to destroy all the asteroids on the
screen to advance to the next level. Your ship is destroyed if it
makes contact with an asteroid.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kasteroids
%defattr(-,root,root,-)
%{tde_bindir}/kasteroids
%{tde_datadir}/icons/hicolor/*/apps/kasteroids.png
%{tde_tdeappdir}/kasteroids.desktop
%{tde_datadir}/apps/kasteroids/
%{tde_datadir}/config.kcfg/kasteroids.kcfg
%{tde_tdedocdir}/HTML/en/kasteroids/

%post -n trinity-kasteroids
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kasteroids
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-katomic
Summary:	Atomic Entertainment game for Trinity
Group:		Amusements/Games

%description -n trinity-katomic
This is a puzzle game, in which the object is to assemble a molecule
from its atoms on a Sokoban-like board.  On each move, an atom goes
as far as it can in a specified direction before being stopped by a
wall or another atom.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-katomic
%defattr(-,root,root,-)
%{tde_datadir}/apps/katomic/
%{tde_datadir}/icons/hicolor/*/apps/katomic.png
%{tde_tdeappdir}/katomic.desktop
%{tde_bindir}/katomic
%{tde_tdedocdir}/HTML/en/katomic/

%post -n trinity-katomic
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-katomic
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kbackgammon
Summary:	A Backgammon game for Trinity
Group:		Amusements/Games

%description -n trinity-kbackgammon
KBackgammon is a backgammon program for Trinity. It is based on the
code, ideas and concepts of KFibs (which is a FIBS client for
TDE1). For a short time, KBackgammon was called bacKgammon (if you
know somebody who is still using bacKgammon, please force them to
upgrade :-)).

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kbackgammon
%defattr(-,root,root,-)
%{tde_bindir}/kbackgammon
%{tde_tdeappdir}/kbackgammon.desktop
%{tde_datadir}/apps/kbackgammon/
%{tde_datadir}/icons/hicolor/*/apps/kbackgammon.png
%{tde_datadir}/icons/hicolor/*/apps/kbackgammon_engine.png
%{tde_tdedocdir}/HTML/en/kbackgammon/

%post -n trinity-kbackgammon
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kbackgammon
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kbattleship
Summary:	Battleship game for Trinity
Group:		Amusements/Games

%description -n trinity-kbattleship
This is an implementation of the Battleship game.  Each player tries
to be the first to sink all the opponent's ships by firing "blindly"
at them.  The game has options to play over a network connection or
against the computer.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kbattleship
%defattr(-,root,root,-)
%{tde_datadir}/apps/kbattleship/
%{tde_datadir}/apps/zeroconf/_kbattleship._tcp
%{tde_datadir}/icons/hicolor/*/apps/kbattleship.png
%{tde_tdeappdir}/kbattleship.desktop
%{tde_bindir}/kbattleship
%{tde_tdedocdir}/HTML/en/kbattleship/

%post -n trinity-kbattleship
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kbattleship
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kblackbox
Summary:	A simple logical game for the Trinity project
Group:		Amusements/Games

%description -n trinity-kblackbox
KBlackBox is a game of hide and seek played on an grid of boxes. Your
opponent (Random number generator, in this case) has hidden several
balls within this box. By shooting rays into the box and observing
where they emerge it is possible to deduce the positions of the
hidden balls. The fewer rays you use to find the balls, the lower
your score.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kblackbox
%defattr(-,root,root,-)
%{tde_datadir}/apps/kblackbox/
%{tde_datadir}/icons/hicolor/*/apps/kblackbox.png
%{tde_tdeappdir}/kblackbox.desktop
%{tde_bindir}/kblackbox
%{tde_tdedocdir}/HTML/en/kblackbox/

%post -n trinity-kblackbox
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kblackbox
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kbounce
Summary:	Jezzball clone for the K Desktop Environment
Group:		Amusements/Games

%description -n trinity-kbounce
This is a clone of the popular Jezzball game originally created by
Microsoft. Jezzball is one of the rare and simple games requiring
skill, timing, and patience in order to be successful.  A ball begins
to bounce off of an area enclosed by four borders (like a
square). You must move your pointer to certain areas within the
square. Upon clicking, a new border is constructed at a relatively
quick pace. You can change the direction of the borders by 90 degrees
as well. Ultimately, you must force the ball to bounce around in a
smaller, and smaller area as time goes by without the ball ever
touching the borders as they are being constructed. If a ball touches
a certain part of the border as it is being built, the game is over.
After 75% of the original space has been blocked off from the moving
ball, you advance one level, and one more ball is added to the mix in
the following level.

This game was previously known as kjezz.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kbounce
%defattr(-,root,root,-)
%{tde_datadir}/apps/kbounce/
%{tde_tdeappdir}/kbounce.desktop
%{tde_datadir}/icons/hicolor/*/apps/kbounce.png
%{tde_bindir}/kbounce
%{tde_tdedocdir}/HTML/en/kbounce/

%post -n trinity-kbounce
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kbounce
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kenolaba
Summary:	Enolaba board game for Trinity
Group:		Amusements/Games

%description -n trinity-kenolaba
kenolaba is a simple board strategy game that is played by two
players. There are red and yellow pieces for each player. Beginning
from a start position where each player has 14 pieces, moves are
drawn until one player has pushed 6 pieces of his opponent out of the
board.

This game was previously known as kabalone, and was inspired by the
board game Abalone by Abalone SA, France.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kenolaba
%defattr(-,root,root,-)
%{tde_datadir}/apps/kenolaba/
%{tde_datadir}/icons/hicolor/*/apps/kenolaba.png
%{tde_tdeappdir}/kenolaba.desktop
%{tde_bindir}/kenolaba
%{tde_tdedocdir}/HTML/en/kenolaba/

%post -n trinity-kenolaba
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kenolaba
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kfouleggs
Summary:	A TDE clone of the Japanese PuyoPuyo game
Group:		Amusements/Games

%description -n trinity-kfouleggs
KFouleggs is a clone of the Japanese PuyoPuyo game, with advanced
features such as multiplayer games against human or AI, and network
play.  If you have played Tetris or one of its many clones, you will
find KFouleggs easy to learn.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kfouleggs
%defattr(-,root,root,-)
%{tde_tdeappdir}/kfouleggs.desktop
%{tde_datadir}/apps/kfouleggs/
%{tde_datadir}/config.kcfg/kfouleggs.kcfg
%{tde_bindir}/kfouleggs
%{tde_datadir}/icons/hicolor/*/apps/kfouleggs.png
%{tde_tdedocdir}/HTML/en/kfouleggs/

%post -n trinity-kfouleggs
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kfouleggs
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kgoldrunner
Summary:	A Trinity clone of the Loderunner arcade game
Group:		Amusements/Games

%description -n trinity-kgoldrunner
KGoldrunner, a game of action and puzzle solving.  Run through the
maze, dodge your enemies, collect all the gold and climb up to the
next level.

You must guide the hero with the mouse or keyboard and collect all
the gold nuggets, then you can climb up into the next level.  Your
enemies are also after the gold and they will kill you if they catch
you!

The problem is you have no weapon to kill them.  All you can do is
run away, dig holes in the floor to trap them or lure them into some
area where they cannot hurt you.  After a short time a trapped enemy
climbs out of his hole, but if it closes before that, he will die and
reappear somewhere else.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kgoldrunner
%defattr(-,root,root,-)
%{tde_datadir}/apps/kgoldrunner/
%{tde_datadir}/icons/hicolor/*/apps/kgoldrunner.png
%{tde_tdeappdir}/KGoldrunner.desktop
%{tde_bindir}/kgoldrunner
%{tde_tdedocdir}/HTML/en/kgoldrunner/

%post -n trinity-kgoldrunner
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kgoldrunner
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kjumpingcube
Summary:	Tactical one or two player game
Group:		Amusements/Games

%description -n trinity-kjumpingcube
KJumpingCube is a simple tactical game. You can play it against the
computer or against a friend. The playing field consists of squares
that contains points.  By clicking on the squares you can increase
the points and if the points reach a maximum the points will jump to
the squares neighbours and take them over. Winner is the one, who
owns all squares.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kjumpingcube
%defattr(-,root,root,-)
%{tde_bindir}/kjumpingcube
%{tde_datadir}/icons/hicolor/*/apps/kjumpingcube.png
%{tde_datadir}/apps/kjumpingcube/
%{tde_tdeappdir}/kjumpingcube.desktop
%{tde_datadir}/config.kcfg/kjumpingcube.kcfg
%{tde_tdedocdir}/HTML/en/kjumpingcube/

%post -n trinity-kjumpingcube
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kjumpingcube
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-klickety
Summary:	A Clickomania-like game for Trinity
Group:		Amusements/Games

%description -n trinity-klickety
Klickety is an adaptation of the (perhaps) well-known Clickomania
game; it is very similar to the "same" game.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-klickety
%defattr(-,root,root,-)
%{tde_bindir}/klickety
%{tde_tdeappdir}/klickety.desktop
%{tde_datadir}/icons/hicolor/*/apps/klickety.png
%{tde_datadir}/icons/crystalsvg/*/actions/endturn.png
%{tde_datadir}/apps/klickety/klicketyui.rc
%{tde_datadir}/apps/klickety/eventsrc
%{tde_tdedocdir}/HTML/en/klickety/

%post -n trinity-klickety
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-klickety
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-klines
Summary:	Color lines for Trinity
Group:		Amusements/Games

%description -n trinity-klines
KLines is a simple game. It is played by one player, so there is only
one winner :-). You play for fun and against the high score. It was
inspired by a well known game - "Color lines", written for DOS by
Olga Demina, Igor Demina, Igor Ivkin and Gennady Denisov back in
1992.

The main rules of the game are as simple as possible: you move (using
the mouse) marbles from cell to cell and build lines (horizontal,
vertical or diagonal). When a line contains 5 or more marbles, they
are removed and your score grows. After each turn the computer drops
three more marbles.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-klines
%defattr(-,root,root,-)
%{tde_datadir}/apps/klines/
%{tde_tdeappdir}/klines.desktop
%{tde_bindir}/klines
%{tde_datadir}/config.kcfg/klines.kcfg
%{tde_datadir}/icons/hicolor/*/apps/klines.png
%{tde_tdedocdir}/HTML/en/klines/

%post -n trinity-klines
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-klines
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kmahjongg
Summary:	the classic mahjongg game for Trinity project
Group:		Amusements/Games

%description -n trinity-kmahjongg
Your mission in this game is to remove all tiles from the game board. A
matching pair of tiles can be removed, if they are 'free', which means that
no other tiles block them on the left or right side.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kmahjongg
%defattr(-,root,root,-)
%{tde_datadir}/apps/kmahjongg/
%{tde_datadir}/icons/hicolor/*/apps/kmahjongg.png
%{tde_tdeappdir}/kmahjongg.desktop
%{tde_bindir}/kmahjongg
%{tde_datadir}/config.kcfg/kmahjongg.kcfg
%{tde_tdedocdir}/HTML/en/kmahjongg/

%post -n trinity-kmahjongg
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kmahjongg
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kmines
Summary:	Minesweeper for Trinity
Group:		Amusements/Games

%description -n trinity-kmines
KMines is the classic Minesweeper game. You must uncover all the
empty cases without blowing on a mine.

When you uncover a case, a number appears : it indicates how many
mines surround this case. If there is no number the neighbour cases
are automatically uncovered. In your process of uncovering secure
cases, it is very useful to put a flag on the cases which contain a
mine.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kmines
%defattr(-,root,root,-)
%{tde_datadir}/icons/hicolor/*/apps/kmines.png
%{tde_tdeappdir}/kmines.desktop
%{tde_datadir}/apps/kmines/
%{tde_bindir}/kmines
%{tde_tdedocdir}/HTML/en/kmines/

%post -n trinity-kmines
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kmines
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-knetwalk
Summary:	A game for system administrators
Group:		Amusements/Games

%description -n trinity-knetwalk
This game presents the player with a rectangular field consisting of
a server, several clients, and pieces of wire.  The object is to
rotate these elements until every client is connected to the server,
and no wires are left unconnected.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-knetwalk
%defattr(-,root,root,-)
%{tde_bindir}/knetwalk
%{tde_datadir}/apps/knetwalk
%{tde_datadir}/icons/hicolor/*/apps/knetwalk.png
%{tde_tdeappdir}/knetwalk.desktop

%post -n trinity-knetwalk
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-knetwalk
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kolf
Summary:	Minigolf game for TDE
Group:		Amusements/Games

%description -n trinity-kolf
This is a minigolf game for TDE that allows you to go through different
golf courses and waste an exorbitant amount of time.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kolf
%defattr(-,root,root,-)
%{tde_datadir}/config/magic/kolf.magic
%{tde_datadir}/apps/kolf/
%{tde_bindir}/kolf
%{tde_tdeappdir}/kolf.desktop
%{tde_datadir}/icons/hicolor/*/apps/kolf.png
%{tde_datadir}/mimelnk/application/x-kolf.desktop
%{tde_datadir}/mimelnk/application/x-kourse.desktop
%{tde_libdir}/lib[kt]deinit_kolf.so
%{tde_libdir}/lib[kt]deinit_kolf.la
%{tde_tdelibdir}/kolf.la
%{tde_tdelibdir}/kolf.so
%{tde_libdir}/libkolf.so.1
%{tde_libdir}/libkolf.so.1.2.0
%{tde_tdedocdir}/HTML/en/kolf/

%post -n trinity-kolf
/sbin/ldconfig || :
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kolf
/sbin/ldconfig || :
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kolf-devel
Summary:	Development files for Kolf
Group:		Development/Libraries
Requires:	trinity-kolf = %{version}-%{release}

%description -n trinity-kolf-devel
This package contains headers and development libraries for compiling
Kolf plugins.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kolf-devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/kolf
%{tde_libdir}/libkolf.la
%{tde_libdir}/libkolf.so

%post -n trinity-kolf-devel
/sbin/ldconfig || :

%postun -n trinity-kolf-devel
/sbin/ldconfig || :

##########

%package -n trinity-konquest
Summary:	TDE based GNU-Lactic Konquest game
Group:		Amusements/Games

%description -n trinity-konquest
This the TDE version of Gnu-Lactic Konquest, a multi-player strategy
game. The goal of the game is to expand your interstellar empire
across the galaxy and, of course, crush your rivals in the process.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-konquest
%defattr(-,root,root,-)
%{tde_datadir}/apps/konquest/
%{tde_datadir}/icons/hicolor/*/apps/konquest.png
%{tde_tdeappdir}/konquest.desktop
%{tde_bindir}/konquest
%{tde_tdedocdir}/HTML/en/konquest/

%post -n trinity-konquest
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-konquest
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kpat
Summary:	Trinity solitaire patience game
Group:		Amusements/Games

%description -n trinity-kpat
KPatience is a collection of 14 card games. All the games are single
player games.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kpat
%defattr(-,root,root,-)
%{tde_datadir}/icons/hicolor/*/apps/kpat.png
%{tde_datadir}/apps/kpat/
%{tde_tdeappdir}/kpat.desktop
%{tde_bindir}/kpat
%{tde_tdedocdir}/HTML/en/kpat/

%post -n trinity-kpat
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kpat
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kpoker
Summary:	Trinity based Poker clone
Group:		Amusements/Games

%description -n trinity-kpoker
KPoker is a TDE compliant clone of those highly addictive pocket
video poker games which are sometimes called "Videopoker" as well.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kpoker
%defattr(-,root,root,-)
%{tde_datadir}/apps/kpoker/
%{tde_datadir}/icons/hicolor/*/apps/kpoker.png
%{tde_tdeappdir}/kpoker.desktop
%{tde_bindir}/kpoker
%{tde_tdedocdir}/HTML/en/kpoker/

%post -n trinity-kpoker
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kpoker
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kreversi
Summary:	Reversi for Trinity
Group:		Amusements/Games

%description -n trinity-kreversi
Reversi is a simple strategy game that is played by two
players. There is only one type of piece - one side of it is black,
the other white. If a player captures a piece on the board, that
piece is turned and belongs to that player. The winner is the person
that has more pieces of his own color on the board and if there are
no more moves possible.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kreversi
%defattr(-,root,root,-)
%{tde_bindir}/kreversi
%{tde_tdeappdir}/kreversi.desktop
%{tde_datadir}/apps/kreversi/
%{tde_datadir}/config.kcfg/kreversi.kcfg
%{tde_datadir}/icons/crystalsvg/*/actions/lastmoves.png
%{tde_datadir}/icons/crystalsvg/*/actions/legalmoves.png
%{tde_datadir}/icons/crystalsvg/scalable/actions/lastmoves.svgz
%{tde_datadir}/icons/crystalsvg/scalable/actions/legalmoves.svgz
%{tde_datadir}/icons/hicolor/*/apps/kreversi.png
%{tde_tdedocdir}/HTML/en/kreversi/

%post -n trinity-kreversi
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kreversi
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-ksame
Summary:	SameGame for Trinity
Group:		Amusements/Games

%description -n trinity-ksame
KSame is a simple game. It's played by one player, so there is only
one winner :-) You play for fun and against the high score. It has
been inspired by SameGame, that is only famous on the Macintosh
platform.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-ksame
%defattr(-,root,root,-)
%{tde_bindir}/ksame
%{tde_datadir}/icons/hicolor/*/apps/ksame.png
%{tde_datadir}/apps/ksame/*
%{tde_tdeappdir}/ksame.desktop
%{tde_tdedocdir}/HTML/en/ksame/

%post -n trinity-ksame
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-ksame
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kshisen
Summary:	Shisen-Sho for Trinity
Group:		Amusements/Games

%description -n trinity-kshisen
KShisen-Sho is a single-player-game similar to Mahjongg and uses the
same set of tiles as Mahjongg.

The object of the game is to remove all tiles from the field.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kshisen
%defattr(-,root,root,-)
%{tde_datadir}/apps/kshisen/
%{tde_datadir}/config.kcfg/kshisen.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kshisen.png
%{tde_tdeappdir}/kshisen.desktop
%{tde_bindir}/kshisen
%{tde_tdedocdir}/HTML/en/kshisen/

%post -n trinity-kshisen
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kshisen
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-ksirtet
Summary:	Tetris and Puyo-Puyo games for Trinity
Group:		Amusements/Games

%description -n trinity-ksirtet
This program is a clone of the well known game Tetris. You must fit
the falling pieces to form full lines. You can rotate and translate
the falling piece. The game ends when no more piece can fall ie when
your incomplete lines reach the top of the board.

Every time you have destroyed 10 lines, you gain a level and the
pieces fall quicker (exactly the piece falls from a line each
1/(1+level) second).

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-ksirtet
%defattr(-,root,root,-)
%{tde_tdeappdir}/ksirtet.desktop
%{tde_datadir}/icons/hicolor/*/apps/ksirtet.png
%{tde_datadir}/apps/ksirtet/
%{tde_bindir}/ksirtet
%{tde_datadir}/config.kcfg/ksirtet.kcfg
%{tde_tdedocdir}/HTML/en/ksirtet/

%post -n trinity-ksirtet
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-ksirtet
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-ksmiletris
Summary:	Tetris like game for Trinity
Group:		Amusements/Games

%description -n trinity-ksmiletris
This is a game with falling blocks composed of different types of
smilies. The object of the game is to "crack a smile" by guiding
blocks so there are two or more of the same symbol vertically.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-ksmiletris
%defattr(-,root,root,-)
%{tde_datadir}/apps/ksmiletris/
%{tde_datadir}/icons/hicolor/*/apps/ksmiletris.png
%{tde_tdeappdir}/ksmiletris.desktop
%{tde_bindir}/ksmiletris
%{tde_tdedocdir}/HTML/en/ksmiletris/

%post -n trinity-ksmiletris
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-ksmiletris
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-ksnake
Summary:	Snake Race for Trinity
Group:		Amusements/Games

%description -n trinity-ksnake
Snake Race is a game of speed and agility. You are a hungry snake and
are trying to eat all the apples in the room before getting out!

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-ksnake
%defattr(-,root,root,-)
%{tde_datadir}/apps/ksnake/
%{tde_datadir}/config.kcfg/ksnake.kcfg
%{tde_datadir}/icons/hicolor/*/apps/ksnake.png
%{tde_tdeappdir}/ksnake.desktop
%{tde_bindir}/ksnake
%{tde_tdedocdir}/HTML/en/ksnake/

%post -n trinity-ksnake
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-ksnake
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-ksokoban
Summary:	Sokoban game for Trinity
Group:		Amusements/Games

%description -n trinity-ksokoban
The first sokoban game was created in 1982 by Hiroyuki Imabayashi at
the Japanese company Thinking Rabbit, Inc. "Sokoban" is japanese for
"warehouse keeper". The idea is that you are a warehouse keeper
trying to push crates to their proper locations in a warehouse.

The problem is that you cannot pull the crates or step over them. If
you are not careful, some of the crates can get stuck in wrong places
and/or block your way.

It can be rather difficult just to solve a level. But if you want to
make it even harder, you can try to minimise the number of moves
and/or pushes you use to solve the level.

To make the game more fun for small kids (below 10 years or so), some
collections with easier levels are also included in KSokoban. These
are marked (easy) in the level collection menu. Of course, these
levels can be fun for adults too, for example if you don't want to
expose yourself to too much mental strain.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-ksokoban
%defattr(-,root,root,-)
%{tde_tdeappdir}/ksokoban.desktop
%{tde_datadir}/icons/hicolor/*/apps/ksokoban.png
%{tde_bindir}/ksokoban
%{tde_tdedocdir}/HTML/en/ksokoban/

%post -n trinity-ksokoban
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-ksokoban
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kspaceduel
Summary:	Arcade two-player space game for Trinity
Group:		Amusements/Games

%description -n trinity-kspaceduel
KSpaceduel is an space arcade game for two players.

Each player controls a ship that flies around the sun and tries to
shoot at the other ship. You can play KSpaceduel with another person,
against the computer, or you can have the computer control both ships
and play each other.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-kspaceduel
%defattr(-,root,root,-)
%{tde_datadir}/apps/kspaceduel/
%{tde_datadir}/icons/hicolor/*/apps/kspaceduel.png
%{tde_tdeappdir}/kspaceduel.desktop
%{tde_bindir}/kspaceduel
%{tde_datadir}/config.kcfg/kspaceduel.kcfg
%{tde_tdedocdir}/HTML/en/kspaceduel/

%post -n trinity-kspaceduel
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kspaceduel
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-ktron
Summary:	Tron clone for the K Desktop Environment
Group:		Amusements/Games

%description -n trinity-ktron
The object of the game is to avoid running into walls, your own tail,
and that of your opponent.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-ktron
%defattr(-,root,root,-)
%{tde_bindir}/ktron
%{tde_datadir}/icons/hicolor/*/apps/ktron.png
%{tde_tdeappdir}/ktron.desktop
%{tde_datadir}/apps/ktron/
%{tde_datadir}/config.kcfg/ktron.kcfg
%{tde_tdedocdir}/HTML/en/ktron/

%post -n trinity-ktron
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-ktron
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-ktuberling
Summary:	Potato Guy for Trinity
Group:		Amusements/Games

%description -n trinity-ktuberling
KTuberling is a game intended for small children. Of course, it may
be suitable for adults who have remained young at heart.

It is a potato editor. That means that you can drag and drop eyes,
mouths, moustache, and other parts of face and goodies onto a
potato-like guy.  Similarly, you have a penguin on which you can drop
other stuff.

There is no winner for the game. The only purpose is to make the
funniest faces you can.

There is a museum (like a "Madame Tusseau" gallery) where you can
find many funny examples of decorated potatoes. Of course, you can
send your own creations to the programmer, Eric Bischoff, who will
include them in the museum if he gets some spare time.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-ktuberling
%defattr(-,root,root,-)
%{tde_bindir}/ktuberling
%{tde_datadir}/icons/hicolor/*/apps/ktuberling.png
%{tde_tdeappdir}/ktuberling.desktop
%{tde_datadir}/apps/ktuberling/
%{tde_datadir}/mimelnk/application/x-tuberling.desktop
%{tde_tdedocdir}/HTML/en/ktuberling/

%post -n trinity-ktuberling
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-ktuberling
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-twin4
Summary:	Connect Four clone for Trinity
Group:		Amusements/Games

%description -n trinity-twin4
Four wins is a game for two players. Each player is represented by a
colour (yellow and red). The goal of the game is to get four
connected pieces of your colour into a row, column or any
diagonal. This is done by placing one of your pieces into any of the
seven columns. A piece will begin to fill a column from the bottom,
i.e. it will fall down until it reaches the ground level or another
stone. After a move is done it is the turn of the other player. This
is repeated until the game is over, i.e. one of the players has four
pieces in a row, column or diagonal or no more moves are possible
because the board is filled.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-twin4
%defattr(-,root,root,-)
%{tde_bindir}/[kt]win4
%{tde_bindir}/[kt]win4proc
%{tde_datadir}/apps/[kt]win4/
%{tde_datadir}/config.kcfg/[kt]win4.kcfg
%{tde_datadir}/icons/hicolor/*/apps/[kt]win4.png
%{tde_tdeappdir}/[kt]win4.desktop
%{tde_tdedocdir}/HTML/en/[kt]win4/

%post -n trinity-twin4
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-twin4
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-lskat
Summary:	Lieutnant Skat card game for Trinity
Group:		Amusements/Games

%description -n trinity-lskat
Lieutnant Skat (from German Offiziersskat) is a card game for two
players. It is roughly played according to the rules of Skat but with
only two players and simplified rules.

Every player has a set of cards in front of him/her, half of them
covered and half of them open. Both players try to win more than 60
of the 120 possible points. After 16 moves all cards are played and
the game ends.

This package is part of Trinity, and a component of the TDE games module.

%files -n trinity-lskat
%defattr(-,root,root,-)
%{tde_bindir}/lskat
%{tde_bindir}/lskatproc
%{tde_datadir}/apps/lskat/
%{tde_datadir}/icons/hicolor/*/apps/lskat.png
%{tde_tdeappdir}/lskat.desktop
%{tde_tdedocdir}/HTML/en/lskat/

%post -n trinity-lskat
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-lskat
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%if 0%{?suse_version}
%debug_package
%endif

##########


%prep
%setup -q -n kdegames-trinity-%{version}

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR || : ; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

%configure \
   --exec-prefix=%{tde_prefix} \
   --bindir=%{tde_bindir} \
   --libdir=%{tde_libdir} \
   --datadir=%{tde_datadir} \
   --includedir=%{tde_tdeincludedir} \
   --enable-new-ldflags \
   --disable-dependency-tracking \
   --disable-rpath \
   --enable-final \
   --disable-debug \
   --disable-warnings \
   --enable-closure \
   --disable-setgid \
   --with-extra-includes=%{tde_includedir}/tqt

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# locale's
HTML_DIR=$(kde-config --expandvars --install html)
if [ -d %{buildroot}$HTML_DIR ]; then
for lang_dir in %{buildroot}$HTML_DIR/* ; do
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


%clean
%__rm -rf %{buildroot}



%changelog
* Sun Sep 30 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial build for TDE 3.5.13.1
