%global rh_backgrounds_version 15
%global waves_version 0.1.2
%global fedora_release_name beefy-miracle
%global Fedora_Release_Name Beefy_Miracle
#此包是fedora特有包，需要改成Magic的。
Name:           desktop-backgrounds
Version:        17.0.0
Release:        2%{?dist}
Summary:        Desktop backgrounds

Group:          User Interface/Desktops
License:        LGPLv2
Source0:        redhat-backgrounds-%{rh_backgrounds_version}.tar.bz2
Source2:        Propaganda-1.0.0.tar.gz
Source3:        README.Propaganda
Source5:        waves-%{waves_version}.tar.bz2
Source6:        FedoraWaves-metadata.desktop
Source7:        desktop-backgrounds-fedora.xml
Source8:        fedora-metadata.desktop
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
The desktop-backgrounds package contains artwork intended to be used as
desktop background image.


%package        basic
Summary:        Desktop backgrounds
Group:          User Interface/Desktops
Provides:       desktop-backgrounds = %{version}-%{release}
Obsoletes:      desktop-backgrounds < %{version}-%{release}

%description    basic
The desktop-backgrounds-basic package contains artwork intended to be used as
desktop background image.

%package        gnome
Summary:        The default Fedora wallpaper from GNOME desktop
Group:          User Interface/Desktops
%if 0%{?fedora} == 15
Requires:       lovelock-backgrounds-stripes-gnome
%else
#Requires:       %{fedora_release_name}-backgrounds-gnome
%endif
# starting with this release, gnome uses picture-uri instead of picture-filename
# see gnome bz #633983
Requires:       gsettings-desktop-schemas >= 2.91.92
Provides:       system-backgrounds-gnome = %{version}-%{release}
License:        CC-BY-SA

%description    gnome
The desktop-backgrounds-gnome package sets default background in gnome.

%package        xfce
Summary:        The default Fedora wallpaper from XFCE desktop
Group:          User Interface/Desktops
#Requires:       %{fedora_release_name}-backgrounds-xfce
Provides:       system-backgrounds-xfce = %{version}-%{release}
License:        CC-BY-SA

%description    xfce
The desktop-backgrounds-xfce package contains file-names used by XFCE desktop
environment to set up the default backdrop.

%package        compat
Summary:        The default Fedora wallpaper for less common DEs
Group:          User Interface/Desktops
#Requires:       %{fedora_release_name}-backgrounds-single
Provides:       system-backgrounds-compat = %{version}-%{release}
License:        CC-BY-SA

%description    compat
The desktop-backgrounds-compat package contains file-names used
by less common Desktop Environments such as LXDE to set up the
default wallpaper.

%package        waves
Summary:        Desktop backgrounds for the Waves theme
Group:          User Interface/Desktops

%description    waves
The desktop-backgrounds-waves package contains the "Waves" desktop backgrounds
which were used in Fedora 9.

%prep
%setup -qn redhat-backgrounds-%{rh_backgrounds_version}

# move things where %%doc can find them
cp %{SOURCE3} .
mv images/space/*.ps .
mv images/space/README* .

# add propaganda
(cd tiles && tar zxf %{SOURCE2})

# add waves
tar xjf %{SOURCE5}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/backgrounds
cd $RPM_BUILD_ROOT%{_prefix}/share/backgrounds

cp -a $RPM_BUILD_DIR/redhat-backgrounds-%{rh_backgrounds_version}/images .
cp -a $RPM_BUILD_DIR/redhat-backgrounds-%{rh_backgrounds_version}/tiles .

mkdir waves
# copy actual image files
cp -a $RPM_BUILD_DIR/redhat-backgrounds-%{rh_backgrounds_version}/waves-%{waves_version}/*.png waves
# copy animation xml file
cp -a $RPM_BUILD_DIR/redhat-backgrounds-%{rh_backgrounds_version}/waves-%{waves_version}/waves.xml waves

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome-background-properties
cp -a $RPM_BUILD_DIR/redhat-backgrounds-%{rh_backgrounds_version}/desktop-backgrounds-basic.xml $RPM_BUILD_ROOT%{_prefix}/share/gnome-background-properties
cp -a $RPM_BUILD_DIR/redhat-backgrounds-%{rh_backgrounds_version}/waves-%{waves_version}/desktop-backgrounds-waves.xml $RPM_BUILD_ROOT%{_prefix}/share/gnome-background-properties

bgdir=$RPM_BUILD_ROOT%{_datadir}/backgrounds
for I in tiles/Propaganda images/dewdop_leaf.jpg images/dragonfly.jpg images/frosty_pipes.jpg images/in_flight.jpg images/leaf_veins.jpg \
        images/leafdrops.jpg images/lightrays-transparent.png images/lightrays.png images/lightrays2.png images/raingutter.jpg images/riverstreet_rail.jpg \
        images/sneaking_branch.jpg images/space images/yellow_flower.jpg; do
        rm -rf ${bgdir}/${I}
done

# FedoraWaves theme for KDE4
mkdir -p $RPM_BUILD_ROOT%{_datadir}/wallpapers/Fedora_Waves/contents/images
install -m 644 -p %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/wallpapers/Fedora_Waves/metadata.desktop
(cd $RPM_BUILD_ROOT%{_datadir}/wallpapers/Fedora_Waves/contents/;
ln -s ../../../backgrounds/waves/waves-eeepc-3-night.png screenshot.png
cd $RPM_BUILD_ROOT%{_datadir}/wallpapers/Fedora_Waves/contents/images
ln -s ../../../../backgrounds/waves/waves-normal-3-night.png 1024x768.png
ln -s ../../../../backgrounds/waves/waves-wide-3-night.png 1280x800.png
# FIXME: there doesn't seem to be a 5:4 image in the latest iteration
ln -s ../../../../backgrounds/waves/waves-wide-3-night.png 1280x1024.png
ln -s ../../../../backgrounds/waves/waves-wide-3-night.png 1440x900.png
ln -s ../../../../backgrounds/waves/waves-normal-3-night.png 1600x1200.png
ln -s ../../../../backgrounds/waves/waves-wide-3-night.png 1920x1200.png
)

# Defalts for various desktops:
#   for GNOME
mkdir -p $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas
/usr/bin/echo '[org.gnome.desktop.background]' > \
    $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/org.gnome.desktop.background.fedora.gschema.override
%if 0%{?fedora} == 15
/usr/bin/echo "picture-uri='file://%{_datadir}/backgrounds/lovelock/default-stripes/lovelock.xml'" >> \
    $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/org.gnome.desktop.background.fedora.gschema.override
%else
/usr/bin/echo "picture-uri='file://%{_datadir}/backgrounds/%{fedora_release_name}/default/%{fedora_release_name}.xml'" >> \
    $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/org.gnome.desktop.background.fedora.gschema.override
%endif
#   for KDE, this is handled in kde-settings
#   for XFCE
mkdir -p $RPM_BUILD_ROOT%{_datadir}/xfce4/backdrops
/usr/bin/ln -s %{fedora_release_name}.png \
           $RPM_BUILD_ROOT%{_datadir}/xfce4/backdrops/default.png
#   and for the rest (e.g. LXDE)
(cd $RPM_BUILD_ROOT%{_datadir}/backgrounds/images;
ln -s ../%{fedora_release_name}/default/standard/%{fedora_release_name}.png \
      default.png
ln -s ../%{fedora_release_name}/default/normalish/%{fedora_release_name}.png \
      default-5_4.png
ln -s ../%{fedora_release_name}/default/wide/%{fedora_release_name}.png \
      default-16_10.png
cd ..
ln -s ./%{fedora_release_name}/default/standard/%{fedora_release_name}.png \
      default.png
)
magic_rpm_clean.sh
%clean
rm -rf $RPM_BUILD_ROOT

%posttrans gnome
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%postun gnome
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%files basic
%defattr(-, root, root)
%dir %{_datadir}/backgrounds
%dir %{_datadir}/backgrounds/tiles
%dir %{_datadir}/backgrounds/images
%{_datadir}/backgrounds/tiles/*.png
%{_datadir}/backgrounds/tiles/*jpg
%{_datadir}/backgrounds/images/earth_from_space.jpg
%{_datadir}/backgrounds/images/flowers_and_leaves.jpg
%{_datadir}/backgrounds/images/ladybugs.jpg
%{_datadir}/backgrounds/images/stone_bird.jpg
%{_datadir}/backgrounds/images/tiny_blast_of_red.jpg
%dir %{_datadir}/gnome-background-properties
%{_datadir}/gnome-background-properties/desktop-backgrounds-basic.xml
%dir %{_datadir}/wallpapers

%files waves
%defattr(-, root, root)
%dir %{_datadir}/backgrounds/waves
%{_datadir}/backgrounds/waves/*.png
%{_datadir}/backgrounds/waves/waves.xml
%{_datadir}/gnome-background-properties/desktop-backgrounds-waves.xml
%{_datadir}/wallpapers/Fedora_Waves

%files gnome
%defattr(-, root, root)
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.background.fedora.gschema.override

%files xfce
%defattr(-, root, root)
%{_datadir}/xfce4/backdrops/default.png

%files compat
%defattr(-, root, root)
%{_datadir}/backgrounds/images/default*
%{_datadir}/backgrounds/default.png

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 17.0.0-2
- 为 Magic 3.0 重建


