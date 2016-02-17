%global rev 20151216git476
%global rev_l10n 49b7fa0
%global genericplugins attentionplugin autoreplyplugin birthdayreminderplugin captchaformsplugin chessplugin cleanerplugin clientswitcherplugin conferenceloggerplugin contentdownloaderplugin extendedmenuplugin extendedoptionsplugin gmailserviceplugin gomokugameplugin historykeeperplugin icqdieplugin imageplugin jabberdiskplugin juickplugin pepchangenotifyplugin qipxstatusesplugin screenshotplugin skinsplugin stopspamplugin storagenotesplugin translateplugin videostatusplugin watcherplugin gnupgplugin otrplugin
%global unixplugins gnome3supportplugin
%global devplugins pstoplugin

%global qtmajor 5
Summary:        Jabber client based on Qt
Name:           psi-plus
Version:        0.16
Release:        0.25.%{rev}%{?dist}
Epoch:          1

URL:            http://code.google.com/p/psi-dev/
# GPLv2+ - core of Psi+
# LGPLv2.1+ - iris library, Psi+ widgets, several Psi+ tools
# zlib/libpng - UnZip 0.15 additionnal library
License:        GPLv2+ and LGPLv2+ and zlib
# Sources is latest snapshot from git://github.com/psi-im/psi.git with applyed all worked patches from psi-dev team.
# Sources also include plugins. There isn't development files therefore plugin interface very unstable.
# So i can't split plugins to separate package. I need to maintain it together.
Source0:        http://files.psi-plus.com/sources/%{name}-%{version}-%{rev}.tar.bz2
# Translation from  https://github.com/psi-plus/psi-plus-l10n
Source1:        http://files.psi-plus.com/sources/%{name}-l10n-%{rev_l10n}.tar.bz2
# I use this script to make tarballs with Psi+ sources and translations
Source2:        generate-tarball.sh

# https://github.com/psi-plus/main/blob/master/patches/dev/psi-plus-psimedia.patch
Patch0:         psi-plus-psimedia.patch
# https://github.com/psi-plus/main/blob/master/patches/dev/psi-new-history.patch
Patch1:         psi-new-history.patch
# https://github.com/psi-plus/main/blob/master/patches/dev/fix_historydb_qt5.diff
Patch2:         fix_historydb_qt5.diff

%if %{qtmajor} == 5
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5WebKit)
BuildRequires:  pkgconfig(Qt5WebKitWidgets)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(Qt5XmlPatterns)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5Script)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(qca2-qt5)
BuildRequires:  pkgconfig(qjdns-qt5)
BuildRequires:  qt5-linguist
%else
BuildRequires:  pkgconfig(QtCore)
BuildRequires:  pkgconfig(QtGui)
BuildRequires:  pkgconfig(QtWebKit)
BuildRequires:  pkgconfig(QtSvg)
BuildRequires:  pkgconfig(QtXml)
BuildRequires:  pkgconfig(QtXmlPatterns)
BuildRequires:  pkgconfig(QtNetwork)
BuildRequires:  pkgconfig(QtDBus)
BuildRequires:  pkgconfig(QtSql)
BuildRequires:  pkgconfig(QtScript)
BuildRequires:  pkgconfig(QJson)
BuildRequires:  pkgconfig(qca2)
BuildRequires:  pkgconfig(qjdns-qt4)
%endif

BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(enchant)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(minizip)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libotr)
BuildRequires:  pkgconfig(libidn)

BuildRequires:  desktop-file-utils
BuildRequires:  qconf >= 1:2.0
BuildRequires:  gettext
BuildRequires:  libtidy-devel

Requires:       %{name}-common = %{epoch}:%{version}-%{release}
Requires:       sox%{?_isa}
Requires:       gnupg
# Required for SSL/TLS connections
%if %{qtmajor} == 5
Requires:       qca-qt5-ossl%{?_isa}
%else
Requires:       qca-ossl%{?_isa}
%endif

# epel7 has no qca-gnupg package
# Required for GnuPG encryption
%if %{qtmajor} == 5
Requires:       qca-qt5-gnupg%{?_isa}
%endif

# hicolor-icon-theme is owner of themed icons folders
Requires:       hicolor-icon-theme

# New Fedora rules allow to use bundled libraries
# https://bugzilla.redhat.com/show_bug.cgi?id=737304#c15
Provides:       bundled(iris)

%description
Psi+ - Psi IM Mod by psi-dev@conference.jabber.ru

%package        i18n
Summary:        Language packs for Psi
Requires:       %{name} = %{epoch}:%{version}-%{release}
BuildArch:      noarch

%description    i18n
Psi+ - Psi IM Mod by psi-dev@conference.jabber.ru
This package adds internationalization to Psi+.

%package        common
Summary:        Noarch resources for Psi+
BuildArch:      noarch

%description    common
Psi+ - Psi IM Mod by psi-dev@conference.jabber.ru
This package contains huge of base mandatory resources for Psi+.

%package        plugins
Summary:        Plugins pack for Psi+
# GPLv2 is used for the most plugins
# BSD - screenshot plugin
# Beerware - icqdie plugin
License:        GPLv2+ and BSD and Beerware
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
# Filter out plugins from provides
%global __provides_exclude_from ^%{_libdir}/psi-plus


%description    plugins
Psi+ - Psi IM Mod by psi-dev@conference.jabber.ru

 * Attention Plugin
This plugin is designed to send and receive special messages such as
Attentions.

 * Autoreply Plugin
This plugin acts as an auto-answering machine.

 * Birthday Reminder Plugin
This plugin is designed to show reminders of upcoming birthdays.

 * Captcha Forms Plugin
This plugin is designed to pass of captcha directly from the Psi+.

 * Chess Plugin
This plugin allows you to play chess with your friends.
The plugin is compatible with a similar plugin for Tkabber.

 * Cleaner Plugin
This plugin is designed to clear the avatar cache, saved local copies
of vCards and history logs.

 * Client Switcher Plugin
This plugin is intended to spoof version of the Jabber client, the
name and type of operating system. It is possible to manually specify
the version of the client and the operating system or choose from a
predefined list.

 * Conference Logger Plugin
This plugin is designed to save conference logs in which the Psi+
user sits.

 * Content Downloader Plugin
This plugin can currently be used to download and install roster
iconsets and emoticons.

 * Extended Menu Plugin
This plugin adds roster submenu 'Extended Actions' to contact's
context menu. At the moment we have the following items: 'Copy JID',
'Copy the nickname', 'Copy the status message' and 'Ping'.

 * Extended Options Plugin
This plugin is designed to allow easy configuration of some advanced
options in Psi+. This plugin gives you access to advanced application
options, which do not have a graphical user interface.

 * Gmail Service Plugin
Shows notifications of new messages in your Gmailbox.

 * History Keeper Plugin
This plugin is designed to remove the history of selected contacts
when the Psi+ is closed.

 * ICQ Must Die Plugin
This plugin is designed to help you transfer as many contacts as
possible from ICQ to Jabber.

 * Image Plugin
This plugin is designed to send images to roster contacts.

 * Juick Plugin
This plugin is designed to work efficiently and comfortably with the
Juick microblogging service.

 * PEP Change Notify Plugin
The plugin is designed to display popup notifications on change of
moods, activities and tunes at the contacts of the roster. In the
settings you can choose which ones to include notification of events,
specify the time within which a notice will appear, as well as play a
sound specify.

 * Qip X-statuses Plugin
This plugin is designed to display X-statuses of contacts using the
QIP Infium jabber client.

 * Screenshot Plugin
This plugin allows you to make a snapshot (screenshot) of the screen,
edit the visible aria to make a screenshot and save the image to a
local drive or upload to HTTP/FTP server.

 * Stop Spam Plugin
This plugin is designed to block spam messages and other unwanted
information from Psi+ users.

 * Storage Notes Plugin
This plugin is an implementation of XEP-0049: Private XML Storage.
The plugin is fully compatible with notes saved using Miranda IM.
The plugin is designed to keep notes on the jabber server with the
ability to access them from anywhere using Psi+ or Miranda IM.

 * Translate Plugin
This plugin allows you to convert selected text into another language.

 * Video Status Changer Plugin
This plugin is designed to set the custom status when you see the
video in selected video player. Communication with players made by
D-Bus.

 * Skins Plugin
This plugin is designed to create, store and apply skins to Psi+.

 * Off-the-Record Messaging Plugin
a cryptographic protocol that provides strong encryption for instant
messaging conversations. OTR uses a combination of the AES
symmetric-key algorithm, the Diffie–Hellman key exchange, and the SHA-1
hash function. In addition to authentication and encryption, OTR
provides perfect forward secrecy and malleable encryption.

 * PSTO Plugin
Instant bloging service.

 * GnuPG Plugin
A front end for gpg. Allow to handle keys.

%prep
%setup -q -n %{name}-%{version}-%{rev}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# fix rpmlint spurious-executable-perm
find . -name '*.cpp' -or -name '*.h' | xargs chmod 644

# Remove bundled libraries
rm -fr src/libpsi/tools/zip/minizip
rm -fr iris/src/jdns

# Psi+ always uses last iris version. So I need to provide bundled
# iris to guarantee efficiency of program.
# rm -fr iris

# Untar russian language
%{__tar} xjf %{SOURCE1} -C .

%build
unset QTDIR
qconf-qt4
./configure                        \
        --prefix=%{_prefix}        \
        --bindir=%{_bindir}        \
        --libdir=%{_libdir}        \
        --datadir=%{_datadir}      \
        --release                  \
        --no-separate-debug-info   \
        --enable-webkit            \
        --enable-plugins           \
        --enable-whiteboarding     \
        --qtselect=%{qtmajor}      \
        --psimedia-path=%{_libdir}/psi/plugins/libgstprovider.so

make %{?_smp_mflags}

pushd translations
lrelease-qt%{qtmajor} *.ts
popd

pushd src/plugins

# Make paths for generic plugins
allplugins=""
for dir in %{genericplugins}
do
  allplugins="${allplugins} generic/$dir"
done

# Make paths for unix plugins
for dir in %{unixplugins}
do
  allplugins="${allplugins} unix/$dir"
done

# Make paths for dev plugins
for dir in %{devplugins}
do
  allplugins="${allplugins} dev/$dir"
done

# Compile all plugins
for dir in ${allplugins}
do
  pushd $dir
%if %{qtmajor} == 5
  %{qmake_qt5}
%else
  %{qmake_qt4}
%endif
  make %{?_smp_mflags}
  popd
done
popd

%install
# Qt doesn't understand DESTDIR. So I need to use INSTALL_ROOT instead of.
# %%make_install can't be used here.
INSTALL_ROOT=$RPM_BUILD_ROOT make install

# README and COPYING must be holds in doc dir. See %%doc tag in %%files
rm $RPM_BUILD_ROOT%{_datadir}/psi-plus/README
rm $RPM_BUILD_ROOT%{_datadir}/psi-plus/COPYING

# Install languages
cp -p translations/*.qm $RPM_BUILD_ROOT%{_datadir}/%{name}
%find_lang psi --with-qt

mkdir -p $RPM_BUILD_ROOT%{_libdir}/psi-plus/plugins

# Make paths for generic plugins
allplugins=""
for dir in %{genericplugins}
do
  allplugins="${allplugins} generic/$dir"
done

# Make paths for unix plugins
for dir in %{unixplugins}
do
  allplugins="${allplugins} unix/$dir"
done

# Make paths for dev plugins
for dir in %{devplugins}
do
  allplugins="${allplugins} dev/$dir"
done

pushd src/plugins

# Install all plugins
for dir in ${allplugins}
do
  install -p -m 0755 $dir/*.so $RPM_BUILD_ROOT%{_libdir}/psi-plus/plugins/
done
popd

%check
# Menu file is being installed when make install
# so it need only to check this allready installed file
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/psi-plus.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license COPYING
%doc README
%{_bindir}/psi-plus
%{_datadir}/applications/psi-plus.desktop
%{_datadir}/icons/hicolor/*/apps/psi-plus.png

%files i18n -f psi.lang

%files plugins
%{_libdir}/psi-plus

%files common
%license COPYING
%dir %{_datadir}/psi-plus
%{_datadir}/psi-plus/*
%exclude %{_datadir}/psi-plus/*.qm

%changelog
* Tue Dec 15 2015 Liu Di <liudidi@gmail.com> - 1:0.16-0.23.20141205git440
- 为 Magic 3.0 重建

* Wed Nov 18 2015 Rex Dieter <rdieter@fedoraproject.org> 1:0.16-0.22
- rebuild (tidy)

* Thu Oct 22 2015 Ivan Romanov <drizt@land.ru> - 1:0.16-0.21.20141205git440
- fixed qjdns BR for F22

* Tue Oct 20 2015 Ivan Romanov <drizt@land.ru> - 1:0.16-0.20.20141205git440
- set correct plugins permissions
- Filter out plugins from provides

* Mon Oct 19 2015 Ivan Romanov <drizt@land.ru> - 1:0.16-0.19.20141205git440
- Dropped .R suffix from changelog for Fedora review purposes
- Added license test to common subpackage

* Sat Oct 17 2015 Ivan Romanov <drizt@land.ru> - 1:0.16-0.18.20141205git440.R
- no %%make_build in epel7
- no qjdns-qt4 in epel7

* Sat Oct 17 2015 Ivan Romanov <drizt@land.ru> - 1:0.16-0.17.20141205git440.R
- dropped version for bundled iris
- added hicolor-icon-theme to Requires
- fixed post, postun and posttrans scriptlets
- moved noarch resources to common subpackage
- moved desktop-file-validate to %%check section
- use %%global instead of %%define
- preserve timestamp
- use modern %%make_build
- some fixes with licensies
- fixed %%{_libdir}/psi-plus is not owned any package
- fix duplicated /usr/share/psi-plus
- remove bundled jdns
- fix rpmlint spurious-executable-perm

* Wed Oct 14 2015 Ivan Romanov <drizt@land.ru> - 1:0.16-0.16.20141205git440.R
- use %%license tag

* Tue Oct 13 2015 Ivan Romanov <drizt@land.ru> - 1:0.16-0.15.20141205git440.R
- provide bundled iris

* Thu Aug 27 2015 Ivan Romanov <drizt@land.ru> - 1:0.16-0.14.20141205git440.R
- qjdns renamed

* Thu Jun 11 2015 Ivan Romanov <drizt@land.ru> - 1:0.16-0.13.20141205git440.R
- no qca-gnupg in epel7
- use pkgpath(...) style in BR

* Fri Dec  5 2014 Ivan Romanov <drizt@land.ru> - 1:0.16-0.12.20141205git440.R
- updated to r440
- updated history patch
- updated generate-tarball.sh

* Wed Jun 11 2014 Ivan Romanov <drizt@land.ru> - 1:0.16-0.11.20140611git366.R
- updated to r366
- use system qjdns
- dropped obsoletes Group tag

* Tue Jan 28 2014 Ivan Romanov <drizt@land.ru> - 1:0.16-0.10.20140128git271.R
- updated to r271
- updated psi-new-history patch

* Thu Oct 24 2013 Ivan Romanov <drizt@land.ru> - 1:0.16-0.9.20131024git242.R
- updated to r242
- added libidn to BR
- otr plugin now is stable
- dropped yandexnarod plugin

* Thu Apr 11 2013 Ivan Romanov <drizt@land.ru> - 1:0.16-0.8.20130412git109.R
- updated to r109

* Mon Feb 11 2013 Ivan Romanov <drizt@land.ru> - 1:0.16-0.7.20130212git90.R
- updated to r90

* Wed Jan 30 2013 Ivan Romanov <drizt@land.ru> - 1:0.16-0.6.20130131git75.R
- updated to r75

* Wed Jan 30 2013 Ivan Romanov <drizt@land.ru> - 1:0.16-0.5.20130131git72.R
- update to r72

* Wed Jan 30 2013 Ivan Romanov <drizt@land.ru> - 1:0.16-0.4.20130130git71.R
- updated to r71
- changes in psi-plus-psimedia patch

* Thu Jan 24 2013 Ivan Romanov <drizt@land.ru> - 1:0.16-0.3.20130124git61.R
- updated to r61
- added devel plugins. psto and otr.
- uses url for l10n tarball instead of local one
- i18n has no arch
- added libtidy and libotr BR for otrplugin
- added patch to make working psimedia with psi-plus

* Mon Oct 29 2012 Ivan Romanov <drizt@land.ru> - 1:0.16-0.2.20121029git29.R
- updated to r29
- dropped %%defattr

* Sat Oct 27 2012 Ivan Romanov <drizt@land.ru> - 1:0.16-0.1.20121027git21.R
- updated to version 0.16 rev 21
- added many translations
- new i18n subpackage
- improved generate-tarball script
- bundled qca was dropped from upstream

* Mon Jun 25 2012 Ivan Romanov <drizt@land.ru> - 1:0.15-0.25.20120625git5339.R
- update to r5339
- new Gnome3 Support Plugin

* Sat Mar 17 2012 Ivan Romanov <drizt@land.ru> - 1:0.15-0.24.20120314git5253.R
- %{?dist} allready has R suffix.

* Wed Mar 14 2012 Ivan Romanov <drizt@land.ru> - 1:0.15-0.23.20120314git5253.R
- updated to r5253
- corrected comment for Source0
- added %{?_isa} to requires
- less rpmlint warnings
- clarified qt version in BuildRequires
- use system minizip
- explicity removed bundled qca
- psi-plus russian translation new home

* Fri Dec 23 2011 Ivan Romanov <drizt@land.ru> - 0.15-0.22.20111220git5157.R
- reverted Webkit
- updated to r5157
- new Yandex Narod plugin
- Video Status plugin now is generic
- new place for tarball

* Fri Nov 18 2011 Ivan Romanov <drizt@land.ru> - 0.15-0.21.20110919git5117.R
- special for RFRemix 16. workaround to fix the bug 804.

* Sun Oct 09 2011 Ivan Romanov <drizt@land.ru> - 0.15-0.20.20110919git5117.R
- update to r5117
- dropped buildroot tag
- separated iconsets, skins, sounds and themes to standalone packages
- add generate-tarball scripts to make psi-plus source tarball
- skins plugin merged with plugins
- russian translated moved to github
- dropped README and COPYING from wrong site
- moved source tarball

* Tue Jun 21 2011 Ivan Romanov <drizt@land.ru> - 0.15-0.19.20110621svn4080
- update to r4080
- explaining for licenses
- compile all language files instead of only psi_ru.ts
- dropped useless rm from install stage
- dropped packager
- added checking of desktop file

* Mon May 30 2011 Ivan Romanov <drizt@land.ru> - 0.15-0.18.20110530svn3954
- update to r3954
- now will be used only .bz2 archives insted .gz
- moved psimedia to standalone package
- added skipped %{?_smp_mflags} to plugins building
- removed unusual desktop-file-utils. Really .desktop file will be
  installed in make install stage
- removed clean stage
- added whiteboarding
- added themes subpackage
- new plugins: Client Switcher, Gomoku Game, Extended Menu,
  Jabber Disk, PEP Change Notify, Video Status
- dropped hint flags from Required

* Wed Jan 19 2011 Ivan Romanov <drizt@land.ru> - 0.15-0.17.20110119svn3559
- all 'psi' dirs and files renamed to 'psi-plus'
- removed conflicts tag
- added psimedia sub-package
- update to r3559

* Sun Jan 09 2011 Ivan Romanov <drizt@land.ru> - 0.15-0.16.20110110svn3465
- some a bit fixes
- update to r3465

* Sat Dec 18 2010 Ivan Romanov <drizt@land.ru> - 0.15-0.15.20101218svn3411
- update to r3411

* Tue Nov 16 2010 Ivan Romanov <drizt@land.ru> - 0.15-0.14.20101116svn3216
- update to r3216
- removed libproxy from reques

* Mon Nov 01 2010 Ivan Romanov <drizt@land.ru> - 0.15-0.13.20101102svn3143
- update to r3143
- split main package to psi-plus-skins and psi-plus-icons

* Wed Oct 06 2010 Ivan Romanov <drizt@land.ru> - 0.15-0.12.20101006svn3066
- update to r3066
- removed obsoletes tags
- psi-plus now conflicts with psi

* Fri Sep 10 2010 Ivan Romanov <drizt@land.ru> - 0.15-0.11.20100919svn3026
- update to r3026
- added to obsoletes psi-i18n
- added Content Downloader Plugin
- added Captcha Plugin
- remove smiles.

* Thu Aug 12 2010 Ivan Romanov <drizt@land.ru> - 0.15-0.10.20100812svn2812
- update to r2812

* Wed Aug 04 2010 Ivan Romanov <drizt@land.ru> - 0.15-0.9.20100804svn2794
- update to r2794

* Mon Jul 26 2010 Ivan Romanov <drizt@land.ru> - 0.15-0.8.20100726svn2752
- update to r2752

* Mon Jul 5 2010 Ivan Romanov <drizt@land.ru> - 0.15-0.7.20100705svn2636
- fix for working with psimedia
- update to r2636

* Tue Jun 29 2010 Ivan Romanov <drizt@land.ru> - 0.15-0.6.20100629svn2620
- update to r2620

* Fri Jun 04 2010 Ivan Romanov <drizt@land.ru> - 0.15-0.6.20100603svn2507
- fix translations
- update to r2507

* Thu Jun 03 2010 Ivan Romanov <drizt@land.ru> - 0.15-0.5.20100603svn2500
- added skins
- update to r2500

* Thu May 20 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 0.15-0.4.20100520svn2439
- new Ivan Romanov <drizt@land.ru> build

* Tue Mar 02 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 0.15-0.3.20100122svn1671
- rebuilt with openssl

* Sat Jan 30 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 0.15-0.20100122svn1671
- initial Psi+ build
