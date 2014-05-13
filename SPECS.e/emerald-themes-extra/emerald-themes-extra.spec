%global  basever 0.8.8

Name:           emerald-themes-extra
URL:            http://packages.linuxmint.com
License:        GPLv2+
Group:          User Interface/Desktops
Version:        0.7
Release:        5%{?dist}
Summary:        Themes for Emerald, a window decorator for Compiz Fusion
Source0:        http://packages.linuxmint.com/pool/main/e/emerald-themes-extra/%{name}_%{version}-mint3.tar.gz
Source1:        emerald-themes-extra.license
Source2:        http://download.raveit.de/pub/Mate-Desktop/SOURCE/TraditionalGreen-emerald-theme.tar.bz2

BuildArch:      noarch

Requires:       compiz >= %{basever}
Requires:       emerald >= %{basever}


%description
Emerald is themeable window decorator and compositing 
manager for Compiz Fusion.

This package contains extra themes for emerald.


%prep
%setup -q
cp -p %{SOURCE1} COPYING
tar -xjf %{SOURCE2}

%build
#no build needed

%install

cp -p debian/changelog Changelog
cp -p debian/copyright Copyright
mv TraditionalGreen/COPYING COPYING.TraditionalOK

mkdir -p %{buildroot}%{_datadir}/emerald/themes
cp -R usr/share/emerald/themes/* %{buildroot}%{_datadir}/emerald/themes/
cp -R TraditionalGreen %{buildroot}%{_datadir}/emerald/themes/TraditionalGreen

rm -r %{buildroot}%{_datadir}/emerald/themes/BlackLine
rm -r %{buildroot}%{_datadir}/emerald/themes/Fogo



%files
%doc COPYING Changelog Copyright COPYING.TraditionalOK
%{_datadir}/emerald/themes/Blueray/
%{_datadir}/emerald/themes/beryl-clean/
%{_datadir}/emerald/themes/dark_blue/
%{_datadir}/emerald/themes/Eternal/
%{_datadir}/emerald/themes/fadeout/
%{_datadir}/emerald/themes/ghosts_edge_lime/
%{_datadir}/emerald/themes/gray-neu/
%{_datadir}/emerald/themes/Greenhouse_Effect/
%{_datadir}/emerald/themes/iridescence/
%{_datadir}/emerald/themes/JAGT/
%{_datadir}/emerald/themes/komar-blue/
%{_datadir}/emerald/themes/Mac4Lin_Emerald_Aqua_v1.0/
%{_datadir}/emerald/themes/Mac4Lin_Emerald_Graphite_v1.0/
%{_datadir}/emerald/themes/Metrosuave/
%{_datadir}/emerald/themes/ocean/
%{_datadir}/emerald/themes/Overglossed/
%{_datadir}/emerald/themes/slowy/
%{_datadir}/emerald/themes/starwindowtheme/
%{_datadir}/emerald/themes/TraditionalGreen/


%changelog
* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 0.7-5
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 27 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.7-3
- add TraditionalGreen theme

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 22 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.7-1
- initial build for fedora

