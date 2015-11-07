Summary: 	Extra gtk-2/3 themes for gtk based desktops
Summary(zh_CN.UTF-8): 基于 gtk 的桌面的额外 gtk-2/3 主题
Name: 		mate-themes-extras
Version: 3.16.3
Release: 2%{?dist}

# upstream is located at github, but links from tag releases doesn't match copied link in
# web-browser, in result fedora-rewiew-tool will fail.
# so i decided to release on fedorapeople to have a valid download link
# There are different releases for GTK3 versions in f18, f19 and f20
URL: 		https://github.com/NiceandGently/mate-themes-extras
Source0:	http://raveit65.fedorapeople.org/Mate/SOURCE/%{name}-%{version}.tar.xz

License: 	LGPLv2 and GPLv2
Group: 		User Interface/Desktops
BuildArch: 	noarch

Requires: 	gtk-murrine-engine
Requires: 	gtk-unico-engine
Requires: 	faience-icon-theme
Requires: 	dmz-cursor-themes
Requires: 	adwaita-cursor-theme
Requires: 	gtk-smooth-engine
Requires:   adwaita-gtk3-theme
Requires:   mate-icon-theme
Requires:   gnome-icon-theme
# not needed for the momment
#Requires:   gnome-colors-icon-theme

BuildRequires: 	gtk2-devel
BuildRequires: 	mate-common
BuildRequires:  hardlink

# for obsoleting external Repo versions f18 and f19
Obsoletes: mate-themes-extras-3 < %{version}-%{release}
Obsoletes: mate-themes-extras-4 < %{version}-%{release}

%description
The mate-themes-extras package contains a collection of GTK2/3 desktop
themes for all gtk based desktops.
These themes can change the appearance of application widgets, icons,
window borders, cursors, etc.
This package is optimized for GTK3-3.12.
Theme list: Blue-Submarine, DeLorean-Dark, GnomishBeige,
Green-Submarine, Smoothly, Smoothly-Black.

%description -l zh_CN.UTF-8
基于 gtk 的桌面的额外 gtk-2/3 主题。

%prep
%setup -q

%build
%configure \
    --enable-Blue-Submarine \
    --enable-DeLorean-Dark \
    --enable-GnomishBeige \
    --enable-Green-Submarine \
    --enable-Smoothly \
    --enable-Smoothly-Black

make %{?_smp_mflags}

%install
%{make_install}

# remove unecessaries non-executable-scripts to avoid rpmlint errors
#rm -f $RPM_BUILD_ROOT%{_datadir}/themes/Faience-Ocre/gtk-3.0/render-assets.sh
#rm -f $RPM_BUILD_ROOT%{_datadir}/themes/Faience-Ocre/gtk-3.0/render-assets-dark.sh
#rm -f $RPM_BUILD_ROOT%{_datadir}/themes/Faience/gtk-3.0/render-assets.sh
#rm -f $RPM_BUILD_ROOT%{_datadir}/themes/Faience/gtk-3.0/render-assets-dark.sh

# save space by linking identical images
hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Blue-Submarine
hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/DeLorean-Dark
#hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Gnome-Cupertino
#hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Gnome-Cupertino-Mint
hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/GnomishBeige
hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Green-Submarine
#hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Faience
#hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Faience-Ocre
hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Smoothly
hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Smoothly-Black
#hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Zukitwo
#hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Zukitwo-Colors
#hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Zukitwo-Brave
#hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Zukitwo-Dust
#hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Zukitwo-Human
#hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Zukitwo-Illustrious
#hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Zukitwo-Noble
#hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Zukitwo-Wine
#hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/themes/Zukitwo-Wise
magic_rpm_clean.sh

%files
%doc AUTHORS COPYING README ChangeLog
%{_datadir}/themes/Blue-Submarine/
%{_datadir}/themes/DeLorean-Dark/
#%{_datadir}/themes/Faience/
#%{_datadir}/themes/Faience-Ocre/
#%{_datadir}/themes/Gnome-Cupertino/
#%{_datadir}/themes/Gnome-Cupertino-Mint/
%{_datadir}/themes/GnomishBeige/
%{_datadir}/themes/Green-Submarine/
%{_datadir}/themes/Smoothly/
%{_datadir}/themes/Smoothly-Black/
#%{_datadir}/themes/Zukitwo/
#%{_datadir}/themes/Zukitwo-Colors/
#%{_datadir}/themes/Zukitwo-Brave/
#%{_datadir}/themes/Zukitwo-Dust/
#%{_datadir}/themes/Zukitwo-Human/
#%{_datadir}/themes/Zukitwo-Illustrious/
#%{_datadir}/themes/Zukitwo-Noble/
#%{_datadir}/themes/Zukitwo-Wine/
#%{_datadir}/themes/Zukitwo-Wise/


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 3.16.3-2
- 更新到 3.16.3

* Mon Aug 11 2014 Liu Di <liudidi@gmail.com> - 1.9.1-1
- 更新到 1.9.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update gnomishbeige to Gtk+-3.12
- disable themes which aren't working with GTK+-3.12

* Sun May 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0.2
- drop forgoten gtk-xfce-engine requires

* Sun May 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0.1
- update to 1.8.0 release
- Blue-Submarine: update to GTK 3.12
- Green-Submarine: update to GTK 3.12
- Gnome-Cupertino: update to GTK 3.10
- Smoothly: update to GTK 3.10
- Smootly-Black: update to GTK 3.10
- GnomishBeige: complete GTK3-3.10
- DeloreanDark: update to GTK3-3.10
- drop Cologne theme, get rid of xfce theme engine
- several improvements

* Sat Dec 07 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.11-2
- rebuild against fixed 1.7.11 tarball

* Sat Dec 07 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.11-1
- update to 1.7.11 release
- gtk2, syncronize panel-applets menus
- several theme improvements

* Wed Nov 06 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.10-2
- disable Menta-Blue, moved to mate-themes

* Wed Nov 06 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.10-1
- update to 1.7.10 for > f19
- support GTK3-3.10

* Mon Oct 28 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.4-2
- add missing runtime require gnome-colors-icon-theme

* Sat Oct 26 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.4-1
- update to 1.7.4
- switch to gnome-colors-icon-theme
- clean up runtime requires

* Wed Sep 11 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.3-1
- update to 1.7.3
- switch to faience instead of faenza icon theme
- remove runtime require humanity-icon-theme
- add runtime require mate-icon-theme and gnome-icon-theme

* Wed Sep 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-3
- Fix broken deps

* Fri Aug 16 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.2-2
- initial for fedora

* Fri Aug 16 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.2-1
- update to 1.7.2
- update GnomihBeige theme to GTk3-3.8
- disable Zukwito theme, already in fedora

* Sat Jul 27 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1
- update Dolorean-Dark, Smoothly and Smoothly-Black to GTK3-8 

* Thu Jun 27 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-1
- initial build
