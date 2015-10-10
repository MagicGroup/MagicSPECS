#
# spec file for package tdeedu (version R14)
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
%define tde_pkg tdeedu
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

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

%global _hardened_build 0
%define _hardened_cflags %{nil}
%define _hardened_ldflags %{nil}

Name:			trinity-%{tde_pkg}
Summary:		Educational/Edutainment applications
Group:			System/GUI/Other
Version:		%{tde_version}
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}
URL:			http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{tde_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{version}%{?preversion:~%{preversion}}.tar.gz

Patch1:			trinity-tdeedu-14.0.1-tqt.patch

BuildRequires: trinity-tdelibs-devel >= %{tde_version}

BuildRequires: autoconf automake libtool m4
BuildRequires: desktop-file-utils

# PYTHON support
BuildRequires:	python-devel
BuildRequires:	python
BuildRequires:	gcc-c++
BuildRequires:	desktop-file-utils
BuildRequires:	fdupes

# BOOST support
BuildRequires:	boost-devel

# OCAML support
BuildRequires: ocaml(compiler)

Obsoletes:		trinity-kdeedu < %{version}-%{release}
Provides:		trinity-kdeedu = %{version}-%{release}
Obsoletes:		trinity-kdeedu-libs < %{version}-%{release}
Provides:		trinity-kdeedu-libs = %{version}-%{release}

# Meta-package
Requires: %{name}-data = %{version}-%{release}
Requires: trinity-blinken = %{version}-%{release}
Requires: trinity-kalzium = %{version}-%{release}
Requires: trinity-kalzium-data = %{version}-%{release}
Requires: trinity-kanagram = %{version}-%{release}
Requires: trinity-kbruch = %{version}-%{release}
Requires: trinity-keduca = %{version}-%{release}
Requires: trinity-kgeography = %{version}-%{release}
Requires: trinity-kgeography-data = %{version}-%{release}
Requires: trinity-khangman = %{version}-%{release}
Requires: trinity-kig = %{version}-%{release}
Requires: trinity-kiten = %{version}-%{release}
Requires: trinity-klatin = %{version}-%{release}
Requires: trinity-klettres = %{version}-%{release}
Requires: trinity-klettres-data = %{version}-%{release}
Requires: trinity-kmplot = %{version}-%{release}
Requires: trinity-kpercentage = %{version}-%{release}
Requires: trinity-kstars = %{version}-%{release}
Requires: trinity-kstars-data = %{version}-%{release}
Requires: trinity-ktouch = %{version}-%{release}
Requires: trinity-kturtle = %{version}-%{release}
Requires: trinity-kverbos = %{version}-%{release}
Requires: trinity-kvoctrain = %{version}-%{release}
Requires: trinity-kwordquiz = %{version}-%{release}
Requires: trinity-libtdeedu3 = %{version}-%{release}
Requires: trinity-libkiten1 = %{version}-%{release}
Requires: trinity-indi = %{version}-%{release}


%description
Educational/Edutainment applications, including:
* blinken: Simon Says Game
* kalzium: Periodic Table of Elements
* kanagram: Letter Order Game
* kbruch: Exercise Fractions
* keduca: Tests and Exams
* kgeography: Geography Trainer
* khangman: Hangman Game
* kig: Interactive Geometry
* kiten: Japanese Reference/Study Tool
* klatin: Latin Reviser
* klettres: French alphabet tutor
* kmplot: Mathematical Function Plotter
* kpercentage: Excersie Percentages
* kstars: Desktop Planetarium
* ktouch: Touch Typing Tutor
* kturtle: Logo Programming Environment
* kverbos: Study Spanish Verbforms
* kvoctrain: Vocabulary Trainer
* kwordquiz: Vocabulary Trainer

%files
%defattr(-,root,root,-)
%doc COPYING README

##########

%package data
Summary:	Shared data for Trinity educational applications
Group:		System/GUI/Other

%description data
This package contains shared data necessary for running the
educational applications provided with KDE (the K Desktop
Environment).

This package is part of Trinity, as a component of the TDE education module.

%files data
%defattr(-,root,root,-)
%{tde_datadir}/applnk/Edutainment/Languages/.directory
%{tde_datadir}/applnk/Edutainment/Miscellaneous/.directory
%{tde_datadir}/applnk/Edutainment/Mathematics/.directory
%{tde_datadir}/applnk/Edutainment/Science/.directory
%{tde_datadir}/applnk/Edutainment/Tools/.directory

##########

%package -n trinity-blinken
Summary:	Trinity version of the Simon Says electronic memory game
Group:		System/GUI/Other
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-blinken
Blinken is based on an electronic game released in 1978, which
challenges players to remember sequences of increasing length.  On
the face of the device, there are 4 different color buttons, each
with its own distinctive sound.  These buttons light up randomly,
creating the sequence that the player must then recall.  If the
player is successful in remembering the sequence of lights in the
correct order, they advance to the next stage, where an identical
sequence with one extra step is presented.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-blinken
%defattr(-,root,root,-)
%{tde_bindir}/blinken
%{tde_tdeappdir}/blinken.desktop
%{tde_datadir}/apps/blinken/
%{tde_datadir}/config.kcfg/blinken.kcfg
%{tde_datadir}/icons/hicolor/*/apps/blinken.png
%{tde_datadir}/icons/hicolor/scalable/apps/blinken.svgz
%{tde_tdedocdir}/HTML/en/blinken/

%post -n trinity-blinken
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-blinken
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kalzium
Summary:	Chemistry teaching tool for Trinity
Group:		System/GUI/Other
Requires:	trinity-kalzium-data = %{version}-%{release}
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-kalzium
Kalzium is a program which shows you the Periodic System of Elements
(PSE).  You can use Kalzium to search for information about the
elements or to learn facts about the PSE.

Kalzium provides you with all kinds of information about the PSE.
You can look up lots of information about the elements and also use
visualisations to show them.

You can visualise the Periodic Table of the Elements by blocks,
groups, acidic behavior or different states of matter.  You can also
plot data for a range of elements (weight, mean weight, density, IE1,
IE2, electronegativity), and you can go back in time to see what
elements were known at a given date.  In addition, on platforms where
OCaml supports native code generation, Kalzium includes a chemical
equation solver.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kalzium
%defattr(-,root,root,-)
%{tde_bindir}/kalzium
%{tde_tdeappdir}/kalzium.desktop
%{tde_datadir}/config.kcfg/kalzium.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kalzium.png
%{tde_datadir}/icons/hicolor/scalable/apps/kalzium.svgz
%{tde_tdedocdir}/HTML/en/kalzium/

%post -n trinity-kalzium
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kalzium
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kalzium-data
Summary:	Data files for Kalzium
Group:		System/GUI/Other

%description -n trinity-kalzium-data
This package contains architecture-independent data files for
Kalzium, the KDE periodic table application.  This includes pictures
of various chemical equipment and of samples of several elements, in
addition to the actual chemical data.

See the kalzium package for further information.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kalzium-data
%defattr(-,root,root,-)
%{tde_datadir}/apps/kalzium/

##########

%package -n trinity-kanagram
Summary:	Letter order game for Trinity
Group:		System/GUI/Other
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-kanagram
KAnagram is a game that is based on the word/letter puzzles that the
author played as a child.  A word is picked at random and displayed
with its letters in a messed order, with difficulty dependent on the
chosen level.  You have an unlimited number of attempts, and scores
are kept.

It is a very simply constructed game, with 3 difficulty levels of
play.  It is fully customizable, allowing you to write in your own
words and set your own 'look and feel' of the game.  It is aimed for
children aged 10+ because of the difficulty, but of course everyone
is welcome to try.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kanagram
%defattr(-,root,root,-)
%{tde_bindir}/kanagram
%{tde_tdeappdir}/kanagram.desktop
%{tde_datadir}/apps/kanagram/
%{tde_datadir}/config.kcfg/kanagram.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kanagram.png
%{tde_datadir}/icons/hicolor/scalable/apps/kanagram.svgz
%{tde_tdedocdir}/HTML/en/kanagram/

%post -n trinity-kanagram
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kanagram
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kbruch
Summary:	Fraction calculation teaching tool for Trinity
Group:		System/GUI/Other
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-kbruch
KBruch is a small program to practice calculating with fractions.
Different exercises are provided for this purpose.  The program
checks the user's input and gives feedback.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kbruch
%defattr(-,root,root,-)
%{tde_bindir}/kbruch
%{tde_datadir}/apps/kbruch/
%{tde_tdeappdir}/kbruch.desktop
%{tde_datadir}/config.kcfg/kbruch.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kbruch.png
%{tde_datadir}/icons/hicolor/scalable/apps/kbruch.svgz
%{tde_datadir}/icons/crystalsvg/*/actions/kbruch_*.png
%{tde_tdedocdir}/HTML/en/kbruch/

%post -n trinity-kbruch
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kbruch
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-keduca
Summary:	Interactive form-based tests for Trinity
Group:		System/GUI/Other
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-keduca
KEduca is a flash-card application which allows you to make
interactive form-based tests.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-keduca
%defattr(-,root,root,-)
%{tde_bindir}/keduca
%{tde_bindir}/keducabuilder
%{tde_tdelibdir}/libkeducapart.la
%{tde_tdelibdir}/libkeducapart.so
%{tde_tdeappdir}/keduca.desktop
%{tde_tdeappdir}/keducabuilder.desktop
%{tde_datadir}/apps/keduca/
%{tde_datadir}/config.kcfg/keduca.kcfg
%{tde_datadir}/icons/hicolor/*/apps/keduca.png
%{tde_datadir}/mimelnk/application/x-edu.desktop
%{tde_datadir}/mimelnk/application/x-edugallery.desktop
%{tde_datadir}/services/keduca_part.desktop
%{tde_tdedocdir}/HTML/en/keduca/

%post -n trinity-keduca
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-keduca
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kgeography
Summary:	Geography learning tool for Trinity
Group:		System/GUI/Other
Requires:	trinity-kgeography-data = %{version}-%{release}
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-kgeography
KGeography contains maps allowing you to learn various countries or
the political divisions of several countries.  It has several modes,
including a map browser and games involving the names, capitals, or
flags of the map divisions.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kgeography
%defattr(-,root,root,-)
%{tde_bindir}/kgeography
%{tde_tdeappdir}/kgeography.desktop
%{tde_datadir}/config.kcfg/kgeography.kcfg
%{tde_datadir}/icons/crystalsvg/*/apps/kgeography.png
%{tde_datadir}/icons/crystalsvg/scalable/apps/kgeography.svgz
%{tde_datadir}/icons/hicolor/*/apps/kgeography.png
%{tde_tdedocdir}/HTML/en/kgeography

%post -n trinity-kgeography
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kgeography
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kgeography-data
Summary:	Data files for KGeography
Group:		System/GUI/Other

%description -n trinity-kgeography-data
This package contains architecture-independent data files for
KGeography, the geography learning tool for KDE. This includes map
and flag images.

See the kgeography package for further information.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kgeography-data
%defattr(-,root,root,-)
%{tde_datadir}/apps/kgeography/

##########

%package -n trinity-khangman
Summary:	The classical hangman game for Trinity
Group:		System/GUI/Other
#Requires:	dustin-dustismo-sans-fonts
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-khangman
KHangMan is a game based on the well known hangman game.  It is aimed
for children aged 6 and above.  It has four levels of difficulty:
Animals (animals words), Easy, Medium and Hard.

A word is picked at random and the letters are hidden.  You must
guess the word by trying one letter after another.  Each time you
guess a wrong letter, a picture of a hangman is drawn.  You must
guess the word before getting hanged!  You have 10 tries.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-khangman
%defattr(-,root,root,-)
%{tde_confdir}/khangmanrc
%{tde_bindir}/khangman
%{tde_tdeappdir}/khangman.desktop
%{tde_datadir}/apps/khangman/
%{tde_datadir}/config.kcfg/khangman.kcfg
%{tde_datadir}/icons/hicolor/*/apps/khangman.png
%{tde_datadir}/icons/hicolor/scalable/apps/khangman.svgz
%{tde_tdedocdir}/HTML/en/khangman/

%post -n trinity-khangman
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-khangman
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kig
Summary:	Interactive geometry program for KDE
Group:		System/GUI/Other
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-kig
Kig is an application for interactive geometry.  It is intended to
serve two purposes:

- to allow students to interactively explore mathematical figures and
  concepts using the computer;
- to serve as a WYSIWYG tool for drawing mathematical figures and
  including them in other documents.

With this program you can do geometry on a computer just like you
would on a blackboard in a classroom.  However, the program allows
you to move and change parts of a geometrical drawing so that you can
see how the other parts change as a result.

Kig supports loci and user-defined macros.  It also supports imports
and exports to/from foreign file formats including Cabri, Dr. Geo,
KGeo, KSeg and XFig.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kig
%defattr(-,root,root,-)
%{tde_confdir}/magic/cabri.magic
%{tde_confdir}/magic/drgeo.magic
%{tde_bindir}/kig
%{tde_bindir}/pykig.py*
%{tde_tdelibdir}/tdefile_drgeo.la
%{tde_tdelibdir}/tdefile_drgeo.so
%{tde_tdelibdir}/tdefile_kig.la
%{tde_tdelibdir}/tdefile_kig.so
%{tde_tdelibdir}/libkigpart.la
%{tde_tdelibdir}/libkigpart.so
%{tde_tdeappdir}/kig.desktop
%if 0%{?rhel} >= 6 || 0%{?fedora} || 0%{?mgaversion} || 0%{?mdkversion} || 0%{?suse_version}
%{tde_datadir}/apps/katepart/syntax/python-kig.xml
%endif
%{tde_datadir}/apps/kig/
%{tde_datadir}/icons/crystalsvg/*/mimetypes/kig_doc.png
%{tde_datadir}/icons/crystalsvg/scalable/mimetypes/kig_doc.svgz
%{tde_datadir}/icons/hicolor/*/apps/kig.png
%{tde_datadir}/icons/hicolor/scalable/apps/kig.svgz
%{tde_datadir}/mimelnk/application/x-cabri.desktop
%{tde_datadir}/mimelnk/application/x-drgeo.desktop
%{tde_datadir}/mimelnk/application/x-kig.desktop
%{tde_datadir}/mimelnk/application/x-kgeo.desktop
%{tde_datadir}/mimelnk/application/x-kseg.desktop
%{tde_datadir}/services/tdefile_drgeo.desktop
%{tde_datadir}/services/tdefile_kig.desktop
%{tde_datadir}/services/kig_part.desktop
%{tde_tdedocdir}/HTML/en/kig/

%post -n trinity-kig
for i in crystalsvg hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kig
for i in crystalsvg hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kiten
Summary:	Japanese reference/study tool for Trinity
Group:		System/GUI/Other
Requires:	trinity-tdeedu-data = %{version}-%{release}
#Requires:	ttf-kochi-gothic | ttf-kochi-mincho

%description -n trinity-kiten
Kiten is a Japanese reference and study tool for KDE.  It is an
application with multiple functions.  Firstly, it is a convenient
English to Japanese and Japanese to English dictionary.  Secondly, it
is a Kanji dictionary, with multiple ways to look up specific
characters.  Thirdly, it is a tool to help you learn Kanji.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kiten
%defattr(-,root,root,-)
%{tde_bindir}/kiten
%{tde_bindir}/kitengen
%{tde_tdeappdir}/kiten.desktop
%{tde_tdedocdir}/HTML/en/kiten/
%{tde_datadir}/icons/hicolor/*/apps/kiten.png
%{tde_datadir}/icons/hicolor/scalable/apps/kiten.svgz

%post -n trinity-kiten
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kiten
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-klatin
Summary:	Application to help revise/teach Latin
Group:		System/GUI/Other
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-klatin
KLatin is a program to help revise Latin.  There are three "sections"
in which different aspects of the language can be revised.  These are
the vocabulary, grammar and verb testing sections.  In addition there
is a set of revision notes that can be used for self-guided revision.

In the vocabulary section an XML file is loaded containing various
words and their local language translations.  KLatin asks you what
each of these words translate into.  The questions take place in a
multiple-choice environment.

In the grammar and verb sections KLatin asks for a particular part of
a noun or a verb, such as the "ablative singular", or the "1st person
indicative passive plural", and is not multiple choice.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-klatin
%defattr(-,root,root,-)
%{tde_bindir}/klatin
%{tde_tdeappdir}/klatin.desktop
%{tde_datadir}/apps/klatin/
%{tde_datadir}/config.kcfg/klatin.kcfg
%{tde_datadir}/icons/hicolor/*/apps/klatin.png
%{tde_datadir}/icons/hicolor/scalable/apps/klatin.svgz
%{tde_tdedocdir}/HTML/en/klatin/

%post -n trinity-klatin
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-klatin
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-klettres
Summary:	Foreign alphabet tutor for Trinity
Group:		System/GUI/Other
Requires:	trinity-klettres-data = %{version}-%{release}
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-klettres
KLettres is an application specially designed to help the user to
learn the alphabet in a new language and then to learn to read simple
syllables.  The user can be a young child aged from two and a half or
an adult that wants to learn the basics of a foreign language.

Seven languages are currently available: Czech, Danish, Dutch,
English, French, Italian and Slovak.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-klettres
%defattr(-,root,root,-)
%{tde_confdir}/klettresrc
%{tde_bindir}/klettres
%{tde_tdeappdir}/klettres.desktop
%{tde_datadir}/config.kcfg/klettres.kcfg
%{tde_datadir}/icons/hicolor/*/apps/klettres.png
%{tde_datadir}/icons/hicolor/scalable/apps/klettres.svgz
%{tde_tdedocdir}/HTML/en/klettres/

%post -n trinity-klettres
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-klettres
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-klettres-data
Summary:	Data files for KLettres foreign alphabet tutor
Group:		System/GUI/Other

%description -n trinity-klettres-data
This package contains architecture-independent data files for
KLettres, the foreign alphabet tutor for KDE.  This includes sound
files and graphics.

See the klettres package for further information.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-klettres-data
%defattr(-,root,root,-)
%{tde_datadir}/apps/klettres/

##########

%package -n trinity-kmplot
Summary:	Mathematical function plotter for Trinity
Group:		System/GUI/Other
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-kmplot
KmPlot is a mathematical function plotter for KDE.  It has a powerful
built-in parser.  You can plot different functions simultaneously and
combine them to build new functions.

KmPlot supports parametric functions and functions in polar
coordinates.  Several grid modes are supported.  Plots may be printed
with high precision in the correct scale.

KmPlot also provides some numerical and visual features, like filling
and calculating the area between the plot and the first axis, finding
maximum and minimum values, changing function parameters dynamically
and plotting derivatives and integral functions.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kmplot
%defattr(-,root,root,-)
%{tde_bindir}/kmplot
%{tde_tdelibdir}/libkmplotpart.la
%{tde_tdelibdir}/libkmplotpart.so
%{tde_tdeappdir}/kmplot.desktop
%{tde_datadir}/apps/kmplot/
%{tde_datadir}/config.kcfg/kmplot.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kmplot.png
%{tde_datadir}/icons/hicolor/scalable/apps/kmplot.svgz
%{tde_datadir}/mimelnk/application/x-kmplot.desktop
%{tde_datadir}/services/kmplot_part.desktop
%{tde_tdedocdir}/HTML/en/kmplot/

%post -n trinity-kmplot
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kmplot
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kpercentage
Summary:	Percentage calculation teaching tool for Trinity
Group:		System/GUI/Other
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-kpercentage
KPercentage is a small math application that will help pupils to
improve their skills in calculating percentages.

There is a special training section for the three basic tasks.
Finally the pupil can select a random mode, in which all three tasks
are mixed randomly.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kpercentage
%defattr(-,root,root,-)
%{tde_bindir}/kpercentage
%{tde_tdeappdir}/kpercentage.desktop
%{tde_datadir}/apps/kpercentage/
%{tde_datadir}/icons/hicolor/*/apps/kpercentage.png
%{tde_datadir}/icons/hicolor/scalable/apps/kpercentage.svgz
%{tde_tdedocdir}/HTML/en/kpercentage/

%post -n trinity-kpercentage
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kpercentage
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kstars
Summary:	Desktop planetarium for Trinity
Group:		System/GUI/Other
Requires:	trinity-tdeedu-data = %{version}-%{release}
Requires:	trinity-kstars-data = %{version}-%{release}
Requires:	trinity-indi = %{version}-%{release}

%description -n trinity-kstars
KStars is a graphical desktop planetarium for KDE.  It depicts an
accurate simulation of the night sky, including stars,
constellations, star clusters, nebulae, galaxies, all planets, the
Sun, the Moon, comets and asteroids.  You can see the sky as it
appears from any location on Earth, on any date.

The user interface is highly intuitive and flexible.  The display can
be panned and zoomed with the mouse, and you can easily identify
objects and track their motion across the sky.  KStars includes many
powerful features, yet the interface is clean and simple and fun to
use.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kstars
%defattr(-,root,root,-)
%{tde_confdir}/kstarsrc
%{tde_bindir}/kstars
%{tde_tdeappdir}/kstars.desktop
%{tde_datadir}/config.kcfg/kstars.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kstars.png
%{tde_datadir}/icons/hicolor/scalable/apps/kstars.svgz
%{tde_tdedocdir}/HTML/en/kstars/

%post -n trinity-kstars
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kstars
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kstars-data
Summary:	Data files for KStars desktop planetarium
Group:		System/GUI/Other

%description -n trinity-kstars-data
This package contains architecture-independent data files for KStars,
the graphical desktop planetarium for KDE.  This includes star
catalogues and astronomical images.

See the kstars package for further information.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kstars-data
%defattr(-,root,root,-)
%{tde_datadir}/apps/kstars/

##########

%package -n trinity-ktouch
Summary:	Touch typing tutor for Trinity
Group:		System/GUI/Other
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-ktouch
KTouch is a program for learning touch typing - it helps you learn to
type on a keyboard quickly and correctly.  Every finger has its place
on the keyboard with associated keys to press.

KTouch helps you learn to touch type by providing you with text to
train on, and adjusts to different levels depending on how good you
are.  It can display which key to press next, and the correct finger
to use.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-ktouch
%defattr(-,root,root,-)
%{tde_bindir}/ktouch
%{tde_tdeappdir}/ktouch.desktop
%{tde_datadir}/apps/ktouch/
%{tde_datadir}/config.kcfg/ktouch.kcfg
%{tde_datadir}/icons/hicolor/*/apps/ktouch.png
%{tde_datadir}/icons/hicolor/scalable/apps/ktouch.svgz
%{tde_tdedocdir}/HTML/en/ktouch/

%post -n trinity-ktouch
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-ktouch
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kturtle
Summary:	Educational Logo programming environment
Group:		System/GUI/Other
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-kturtle
KTurtle is an educational programming environment using the Logo
programming language.  It tries to make programming as easy and
accessible as possible.  This makes KTurtle suitable for teaching
kids the basics of mathematics, geometry and programming.

The commands used to program are in the style of the Logo programming
language.  The unique feature of Logo is that the commands are often
translated into the speaking language of the programmer.

KTurtle is named after "the turtle" that plays a central role in the
programming environment.  The user programs the turtle, using the
Logo commands, to draw a picture on the canvas.

Note that this version of Logo is only focused on the educational
qualities of the programming language and will not try to suit
professional programmers' needs.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kturtle
%defattr(-,root,root,-)
%{tde_bindir}/kturtle
%{tde_tdeappdir}/kturtle.desktop
%{tde_datadir}/apps/katepart/syntax/logohighlightstyle*
%{tde_datadir}/apps/kturtle/
%{tde_datadir}/config.kcfg/kturtle.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kturtle.png
%{tde_tdedocdir}/HTML/en/kturtle/

%post -n trinity-kturtle
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kturtle
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kverbos
Summary:	Spanish verb form study application for Trinity
Group:		System/GUI/Other
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-kverbos
Kverbos allows the user to learn the forms of Spanish verbs.  The
program suggests a verb and a time and the user enters the different
verb forms.  The program corrects the user input and gives feedback.

The user can edit the list of the verbs that can be studied.  The
program can build regular verb forms by itself.  Irregular verb forms
have to be entered by the user.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kverbos
%defattr(-,root,root,-)
%{tde_bindir}/kverbos
%{tde_tdeappdir}/kverbos.desktop
%{tde_datadir}/apps/kverbos/
%{tde_datadir}/config.kcfg/kverbos.kcfg
%{tde_datadir}/icons/crystalsvg/16x16/actions/kverbosuser.png
%{tde_datadir}/icons/hicolor/*/apps/kverbos.png
%{tde_datadir}/icons/hicolor/scalable/apps/kverbos.svgz
%{tde_tdedocdir}/HTML/en/kverbos/

%post -n trinity-kverbos
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kverbos
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kvoctrain
Summary:	Vocabulary trainer for Trinity
Group:		System/GUI/Other
Requires:	perl
Requires:	perl-libwww-perl
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-kvoctrain
KVocTrain is a little utility to help you train your vocabulary when
you are trying to learn a foreign language.  You can create your own
database with the words you need.  It is intended as a replacement
for index (flash) cards.

You probably remember flashcards from school.  The teacher would
write the original expression on the front side of the card and the
translation on the back.  Then look at the cards one after another.
If you knew the translation, you could put it away.  If you failed,
you put it back to try again.

KVocTrain is not intended to teach you grammar or other sophisticated
things.  This is and probably will stay beyond the scope of this
application.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kvoctrain
%defattr(-,root,root,-)
%{tde_confdir}/kvoctrainrc
%{tde_bindir}/kvoctrain
%{tde_bindir}/spotlight2kvtml
%{tde_libdir}/libkvoctraincore.so.*
%{tde_tdeappdir}/kvoctrain.desktop
%{tde_datadir}/apps/kvoctrain/
%{tde_datadir}/mimelnk/text/x-kvtml.desktop
%{tde_datadir}/config.kcfg/kvoctrain.kcfg
%{tde_datadir}/config.kcfg/languagesettings.kcfg
%{tde_datadir}/config.kcfg/presettings.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kvoctrain.png
%{tde_tdedocdir}/HTML/en/kvoctrain/

%post -n trinity-kvoctrain
/sbin/ldconfig || :
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kvoctrain
/sbin/ldconfig || :
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kwordquiz
Summary:	Flashcard and vocabulary learning program for Trinity
Group:		System/GUI/Other
Requires:	trinity-tdeedu-data = %{version}-%{release}

%description -n trinity-kwordquiz
KWordQuiz is a flashcard-based tool that helps you to master new
vocabularies. It may be a language or any other kind of terminology.

KWordQuiz can open several types of vocabulary data.  Supported are
kvtml files used by other KDE programs such as KVocTrain, wql files
used by WordQuiz for Windows, csv files with comma-separated text,
and xml.gz files created by Pauker (http://pauker.sourceforge.net).

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-kwordquiz
%defattr(-,root,root,-)
%{tde_confdir}/kwordquizrc
%{tde_bindir}/kwordquiz
%{tde_tdeappdir}/kwordquiz.desktop
%{tde_datadir}/apps/kwordquiz/
%{tde_datadir}/config.kcfg/kwordquiz.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kwordquiz.png
%{tde_datadir}/icons/hicolor/scalable/apps/kwordquiz.svg
%{tde_datadir}/icons/crystalsvg/*/mimetypes/kwordquiz_doc.png
%{tde_datadir}/icons/crystalsvg/scalable/mimetypes/kwordquiz_doc.svg
%{tde_datadir}/mimelnk/application/x-kwordquiz.desktop
%{tde_tdedocdir}/HTML/en/kwordquiz/

%post -n trinity-kwordquiz
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kwordquiz
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-libtdeedu3
Summary:	Library for use with Trinity educational apps
Group:		System/GUI/Other

%description -n trinity-libtdeedu3
The KDE-based library libtdeedu is used with educational
applications.  It currently provides support for data plotting and
vocabulary items (including a parser for kvtml vocabulary files).

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-libtdeedu3
%defattr(-,root,root,-)
%{tde_libdir}/libextdate.so.*
%{tde_libdir}/libtdeeducore.so.*
%{tde_libdir}/libtdeeduplot.so.*
%{tde_libdir}/libtdeeduui.so.*

%post -n trinity-libtdeedu3
/sbin/ldconfig || :

%postun -n trinity-libtdeedu3
/sbin/ldconfig || :

##########

%package -n trinity-libtdeedu-devel
Summary:	Development files for Trinity educational library
Group:		Development/Libraries/Other
Requires:	trinity-libtdeedu3 = %{version}-%{release}

%description -n trinity-libtdeedu-devel
The KDE-based library libtdeedu is used with educational
applications.  It currently provides support for data plotting and
vocabulary items (including a parser for kvtml vocabulary files).

Development files for libtdeedu are included in this package.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-libtdeedu-devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/libtdeedu/
%{tde_libdir}/libextdate.la
%{tde_libdir}/libextdate.so
%{tde_libdir}/libtdeeducore.la
%{tde_libdir}/libtdeeducore.so
%{tde_libdir}/libtdeeduui.la
%{tde_libdir}/libtdeeduui.so
%{tde_libdir}/libtdeeduplot.la
%{tde_libdir}/libtdeeduplot.so

%post -n trinity-libtdeedu-devel
/sbin/ldconfig || :

%postun -n trinity-libtdeedu-devel
/sbin/ldconfig || :


##########

%package -n trinity-libkiten1
Summary:	Library for Kiten Japanese reference/study tool
Group:		System/GUI/Other
#Requires:	kanjidic

%description -n trinity-libkiten1
Kiten is a Japanese reference/study tool for KDE.  The library
libkiten contains portions of Kiten that may be useful for other
applications.  These portions include dictionary, character lookup
and widget classes.

This package contains the libkiten library along with supporting
data, such as Japanese language data files and GUI resource files.
For further information, see the kiten package.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-libkiten1
%defattr(-,root,root,-)
%{tde_libdir}/libkiten.so.*
%{tde_datadir}/apps/kiten/
%{tde_datadir}/config.kcfg/kiten.kcfg
%{tde_datadir}/icons/crystalsvg/16x16/actions/kanjidic.png
%{tde_datadir}/icons/crystalsvg/22x22/actions/edit_add.png
%{tde_datadir}/icons/crystalsvg/22x22/actions/edit_remove.png
%{tde_datadir}/icons/crystalsvg/22x22/actions/kanjidic.png
%{tde_datadir}/icons/locolor/16x16/actions/edit_add.png
%{tde_datadir}/icons/locolor/16x16/actions/edit_remove.png

%post -n trinity-libkiten1
for i in crystalsvg locolor locolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
/sbin/ldconfig || :

%postun -n trinity-libkiten1
for i in crystalsvg locolor locolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
/sbin/ldconfig || :

##########

%package -n trinity-libkiten-devel
Summary:	Development files for Kiten library
Group:		Development/Libraries/Other
Requires:	trinity-libkiten1 = %{version}-%{release}
Requires:	trinity-tdelibs-devel >= %{version}

%description -n trinity-libkiten-devel
Kiten is a Japanese reference/study tool for KDE.  The library
libkiten contains portions of Kiten that may be useful for other
applications.  These portions include dictionary, character lookup
and widget classes.

Development files for libkiten are included in this package.  For
further information, see the kiten package.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-libkiten-devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/libkiten/
%{tde_libdir}/libkiten.la
%{tde_libdir}/libkiten.so

%post -n trinity-libkiten-devel
/sbin/ldconfig || :

%postun -n trinity-libkiten-devel
/sbin/ldconfig || :

##########

%package -n trinity-indi
Summary:	Instrument Neutral Distributed Interface for astronomical devices
Group:		System/GUI/Other

%description -n trinity-indi
INDI is an Instrument Neutral Distributed Interface control protocol for
astronomical devices, which provides a framework that decouples low level
hardware drivers from high level front end clients. Clients that use the
device drivers are completely unaware of the device capabilities and
communicate with the device drivers and build a completely dynamic GUI
based on the services provided by the device.

This package is part of Trinity, as a component of the TDE education module.

%files -n trinity-indi
%defattr(-,root,root,-)
%{tde_bindir}/apmount
%{tde_bindir}/apogee_ppi
%{tde_bindir}/celestrongps
%{tde_bindir}/fliccd
%{tde_bindir}/fliwheel
%{tde_bindir}/indiserver
%{tde_bindir}/lx200_16
%{tde_bindir}/lx200autostar
%{tde_bindir}/lx200basic
%{tde_bindir}/lx200classic
%{tde_bindir}/lx200generic
%{tde_bindir}/lx200gps
%{tde_bindir}/meade_lpi
%{tde_bindir}/sbigccd
%{tde_bindir}/skycommander
%{tde_bindir}/temma
%{tde_bindir}/v4ldriver
%{tde_bindir}/v4lphilips

##########

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries/Other
Requires:	%{name} = %{version}-%{release}
Requires:	trinity-libtdeedu-devel = %{version}-%{release}
Requires:	trinity-libkiten-devel = %{version}-%{release}

Obsoletes:	trinity-kdeedu-devel < %{version}-%{release}
Provides:	trinity-kdeedu-devel = %{version}-%{release}

%description devel
This package contains the development files for tdeedu.

%files devel
%defattr(-,root,root,-)
%doc libtdeedu/AUTHORS libtdeedu/README
# kstars
%{tde_tdeincludedir}/kstarsinterface.h
%{tde_tdeincludedir}/simclockinterface.h
# kvoctrain
%{tde_libdir}/libkvoctraincore.la
%{tde_libdir}/libkvoctraincore.so

%post devel
/sbin/ldconfig || :

%postun devel
/sbin/ldconfig || :

##########

%if 0%{?pclinuxos} || 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########


%prep
%setup -q -n %{name}-%{version}%{?preversion:~%{preversion}}
%patch1 -p1

# RHEL5 strange FTBFS on V4L stuff
%if 0%{?rhel} == 5
%__sed -i "admin/acinclude.m4.in" -e "s|-ansi||"
%endif

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export kde_confdir="%{tde_confdir}"

export CXXFLAGS="${RPM_OPT_FLAGS} -fPIC"
export CFLAGS="${RPM_OPT_FLAGS} -fPIC"
# Warning: GCC visibility causes FTBFS [Bug #1285]
%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
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
   --enable-kig-python-scripting \
   --enable-ocamlsolver

%__make %{_smp_mflags} \
  OCAMLLIB=$(ocamlc -where) \
  FACILELIB=$(ocamlc -where)


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# Updates applications categories for openSUSE
%if 0%{?suse_version}
%suse_update_desktop_file -r khangman      Education Languages Game KidsGame
%suse_update_desktop_file    kiten         Education Languages
%suse_update_desktop_file    klatin        Education Languages
%suse_update_desktop_file    klettres      Education Languages
%suse_update_desktop_file    kverbos       Education Languages
%suse_update_desktop_file    kvoctrain     Education Languages
%suse_update_desktop_file    kwordquiz     Education Languages
%suse_update_desktop_file    kbruch        Education Math
%suse_update_desktop_file    kig           Education Math
%suse_update_desktop_file    kmplot        Education Math
%suse_update_desktop_file    kturtle       Education Math
%suse_update_desktop_file    kpercentage   Education Math
%suse_update_desktop_file    kalzium       Education Chemistry
%suse_update_desktop_file    kstars        Education Astronomy
%suse_update_desktop_file    keduca        Education Teaching
%suse_update_desktop_file    keducabuilder Education Teaching
%suse_update_desktop_file    ktouch        Education Teaching
%suse_update_desktop_file -r blinken       Education Teaching Game KidsGame
%suse_update_desktop_file    kgeography    Education Teaching
%suse_update_desktop_file -r kanagram      Education Languages Game KidsGame
%endif

# Links duplicate files
%fdupes "%{?buildroot}%{tde_datadir}"


%clean
%__rm -rf %{buildroot}


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 14.0.0-1
- Initial release for TDE R14.0.0
