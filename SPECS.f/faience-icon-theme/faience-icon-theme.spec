%global themes Faience Faience-Azur Faience-Ocre Faience-Claire

Name:           faience-icon-theme
Version:        0.5
Release:        2%{?dist}
Summary:        Faience icon theme
Group:          User Interface/Desktops

License:        GPLv3
URL:            https://code.google.com/p/faience-theme
Source0:        http://raveit65.fedorapeople.org/Others/Source/%{name}_%{version}.tar.xz

# source0 is re-released and cleaned from icons with copyrighted trademarks
# Therefore we use this script to remove them before shipping it.
# runtime require faenza-icon-theme is also removed from index.theme.
# Invoke this script to generate the faience-icon-theme tarball
Source1:        faience-icon-theme-generate-tarball.sh
BuildArch:      noarch

Requires:       gnome-icon-theme


%description
The faience icon theme include Faience, Faience-Azur,
Faience-Claire and Faience-Ocre theme.
It is cleaned from any nonfree icons.


%prep
%setup -q -n %{name}_%{version}

# unpack the icon tarballs
for theme in %{themes}
do
    tar -zxvf ${theme}.tar.gz &>/dev/null
done

# fix permissions
find . -type d -exec chmod 0755 {} \;
find . -type f -exec chmod 0644 {} \;

# delete icon-cache from source
find -type f -name "icon-theme.cache" -delete -print


%build
# nothing to build


%install
install -dpm 755 $RPM_BUILD_ROOT%{_datadir}/icons

cp -ar %{themes} $RPM_BUILD_ROOT%{_datadir}/icons


%post
for theme in %{themes}
do
    touch --no-create %{_datadir}/icons/${theme} &>/dev/null ||:
done


%postun
if [ $1 -eq 0 ] ; then
    for theme in %{themes}
    do
        touch --no-create %{_datadir}/icons/${theme} &>/dev/null
        gtk-update-icon-cache -q %{_datadir}/icons/${theme} &>/dev/null || :
    done
fi


%posttrans
for theme in %{themes}
do
    gtk-update-icon-cache %{_datadir}/icons/${theme} &>/dev/null || :
done


%files
%doc AUTHORS ChangeLog COPYING README
%{_datadir}/icons/Faience/
%{_datadir}/icons/Faience-Azur/
%{_datadir}/icons/Faience-Claire/
%{_datadir}/icons/Faience-Ocre/


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 09 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> 0.5-1
- initial build for fedora
- clean macros
- add gnome-icon-theme as runtime require
- Add time-stamp preserving flags
- remove icon-cache's from source
- add script to generate a tarball without nonfree icons
- filter source
- remove faenza-icon-theme require from index.theme
- add runtime require gnome-icon-theme
- improve install section

