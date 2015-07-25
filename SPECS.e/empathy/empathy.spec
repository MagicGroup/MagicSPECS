## Minimum required versions.
%global	gtk3_min_version	3.9.4
%global	glib2_min_version	2.37.6
%global	tp_mc_min_version	5.12.0
%global	tp_glib_min_version	0.19.9
%global	enchant_version		1.2.0
%global network_manager_version 0.7.0
%global libcanberra_version	0.4
%global webkit_version		1.3.13
%global goa_version		3.5.1
%global libnotify_version	0.7.0
%global libchamplain_version	0.12.1
%global folks_version		0.9.5
%global gstreamer_version	0.10.32
%global libsecret_version	0.5
%global gcr_version		2.91.4

Name:		empathy
Version:	3.12.10
Release:	2%{?dist}
Summary:	Instant Messaging Client for GNOME
Summary(zh_CN.UTF-8): GNOME 下的即时消息客户端

License:	GPLv2+
URL:		http://live.gnome.org/Empathy

%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:	http://download.gnome.org/sources/%{name}/%{majorver}/%{name}-%{version}.tar.xz
Source1:	%{name}-README.ConnectionManagers

BuildRequires:	enchant-devel >= %{enchant_version}
BuildRequires:	iso-codes-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	glib2-devel >= %{glib2_min_version}
BuildRequires:	libcanberra-devel >= %{libcanberra_version}
BuildRequires:	webkitgtk3-devel >= %{webkit_version}
BuildRequires:	gtk3-devel >= %{gtk3_min_version}
BuildRequires:	intltool
BuildRequires:	libxml2-devel
BuildRequires:	scrollkeeper
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	telepathy-glib-devel >= %{tp_glib_min_version}
BuildRequires:	telepathy-farstream-devel >= 0.2.1
BuildRequires:	libnotify-devel >= %{libnotify_version}
BuildRequires:	NetworkManager-glib-devel >= %{network_manager_version}
BuildRequires:	libchamplain-gtk-devel >= %{libchamplain_version}
BuildRequires:	clutter-gtk-devel >= 1.1.2
BuildRequires:	geoclue2-devel
BuildRequires:	geocode-glib-devel
BuildRequires:	telepathy-logger-devel >= 0.8.0
BuildRequires:	folks-devel >= 1:%{folks_version}
BuildRequires:	clutter-gst2-devel
BuildRequires:	gstreamer1-devel >= %{gstreamer_version}
BuildRequires:	cogl-devel
BuildRequires:	cheese-libs-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	libgudev1-devel
BuildRequires:	telepathy-mission-control-devel
BuildRequires:	gnome-online-accounts-devel >= %{goa_version}
BuildRequires:	libsecret-devel >= %{libsecret_version}
BuildRequires:	gcr-devel >= %{gcr_version}
BuildRequires:	pkgconfig(gee-0.8)
BuildRequires:	itstool
# hack to conserve space on the live cd
BuildRequires:	/usr/bin/convert

Requires:	telepathy-filesystem
Requires:	telepathy-mission-control >= %{tp_mc_min_version}
## We install the following connection managers by default.
Requires:	telepathy-gabble >= 0.16.0
Requires:	telepathy-salut >= 0.8.0
Requires:	telepathy-idle
Requires:	telepathy-haze >= 0.6.0

Requires(post): /usr/bin/gtk-update-icon-cache
Requires(postun): /usr/bin/gtk-update-icon-cache


%description
Empathy is powerful multi-protocol instant messaging client which
supports Jabber, GTalk, MSN, IRC, Salut, and other protocols.
It is built on top of the Telepathy framework.

%description -l zh_CN.UTF-8
这是一个支持多种协议的即时消息客户端，包括 Jabber, GTalk, MSN, IRC,
Salut 和其它的协议。这是在 Telepathy 框架上是创建的。

%prep
%setup -q
# force this to be regenerated
rm data/empathy.desktop


%build
## GCC complains about some unused functions, so we forcibly show those as
## simple warnings instead of build-halting errors.
%configure --disable-static --enable-ubuntu-online-accounts=no
# Parallel builds are broken.
make
install -m 0644 %{SOURCE1} ./README.ConnectionManagers


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang %{name} --with-gnome
%find_lang empathy-tpaw

desktop-file-install --delete-original			\
	--dir %{buildroot}%{_datadir}/applications	\
	%{buildroot}%{_datadir}/applications/%{name}.desktop

# hack to conserve space on the live image
for f in video_overview.png conf_overview.png croom_overview.png; do
  convert %{buildroot}%{_datadir}/help/C/empathy/figures/$f -resize 150x150 $f
  mv $f %{buildroot}%{_datadir}/help/C/empathy/figures
done


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/sbin/ldconfig


%postun
if [ $1 -eq 0 ]; then
   touch --no-create %{_datadir}/icons/hicolor &>/dev/null
   gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
   glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
/sbin/ldconfig


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang -f empathy-tpaw.lang
%doc AUTHORS COPYING README README.ConnectionManagers NEWS
%doc COPYING-DOCS COPYING.LGPL COPYING.SHARE-ALIKE
%{_bindir}/%{name}
%{_bindir}/%{name}-accounts
%{_bindir}/%{name}-debugger
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libempathy-%{version}.so
%{_libdir}/%{name}/libempathy-gtk-%{version}.so
%{_libdir}/%{name}/libempathy-gtk.so
%{_libdir}/%{name}/libempathy.so
%{_libdir}/mission-control-plugins.0/mcp-account-manager-goa.so
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/empathy/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Empathy.Call.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Empathy.Chat.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Empathy.Auth.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Empathy.FileTransfer.service
%{_datadir}/GConf/gsettings/empathy.convert
%{_datadir}/glib-2.0/schemas/org.gnome.Empathy.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.telepathy-account-widgets.gschema.xml
%{_datadir}/telepathy/clients/Empathy.Call.client
%{_datadir}/telepathy/clients/Empathy.Chat.client
%{_datadir}/telepathy/clients/Empathy.Auth.client
%{_datadir}/telepathy/clients/Empathy.FileTransfer.client
%{_mandir}/man1/empathy*.1.gz
%{_libexecdir}/empathy-auth-client
%{_libexecdir}/empathy-call
%{_libexecdir}/empathy-chat
%dir %{_datadir}/adium
%dir %{_datadir}/adium/message-styles
%dir %{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle
%dir %{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents
%dir %{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Info.plist
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources/Incoming/Content.html
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources/Incoming/NextContent.html
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources/Status.html
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources/Variants/Blue.css
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources/Variants/Clean.css
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources/Variants/Simple.css
%{_datadir}/adium/message-styles/Boxes.AdiumMessageStyle/Contents/Resources/main.css
%dir %{_datadir}/adium/message-styles/Classic.AdiumMessageStyle
%dir %{_datadir}/adium/message-styles/Classic.AdiumMessageStyle/Contents
%dir %{_datadir}/adium/message-styles/Classic.AdiumMessageStyle/Contents/Resources
%{_datadir}/adium/message-styles/Classic.AdiumMessageStyle/Contents/Info.plist
%{_datadir}/adium/message-styles/Classic.AdiumMessageStyle/Contents/Resources/Content.html
%{_datadir}/adium/message-styles/Classic.AdiumMessageStyle/Contents/Resources/Status.html
%{_datadir}/adium/message-styles/Classic.AdiumMessageStyle/Contents/Resources/main.css
%dir %{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle
%dir %{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents
%dir %{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Info.plist
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/Images/corners.png
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/Images/horizontal.png
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/Images/nipple.png
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/Images/vertical.png
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/Incoming/Content.html
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/Incoming/NextContent.html
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/Status.html
%{_datadir}/adium/message-styles/PlanetGNOME.AdiumMessageStyle/Contents/Resources/main.css

%changelog
* Tue Jul 14 2015 Liu Di <liudidi@gmail.com> - 3.12.10-2
- 更新到 3.12.10

* Tue Apr 01 2014 Liu Di <liudidi@gmail.com> - 3.12.0-2
- 更新到 3.12.0

* Mon Mar 31 2014 Liu Di <liudidi@gmail.com> - 3.11.92-2
- 更新到 3.11.92

* Thu Feb 20 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.90-2
- Rebuilt for cogl soname bump

* Mon Feb 17 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

