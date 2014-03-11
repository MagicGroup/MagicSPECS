Name:           swfdec-gnome
Version:        2.28.0
Release:        2%{?dist}
Summary:        Programs to integrate Flash into the GNOME desktop
Summary(zh_CN): 集成 Flash 到 GNOME 桌面的程序

Group:          Applications/Internet
Group(zh_CN):	应用程序/互联网
License:        GPLv2+
URL:            http://swfdec.freedesktop.org/
Source0:        http://swfdec.freedesktop.org/download/%{name}/2.28/%{name}-%{version}.tar.bz2
Patch0:		%{name}-2.24.0-build.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel >= 2.12.0
BuildRequires:	swfdec-gtk-devel >= 0.8.0
BuildRequires:	GConf2
BuildRequires:  desktop-file-utils
BuildRequires:	gettext
BuildRequires:  intltool

Requires(pre): GConf2
Requires(post):	GConf2
Requires(preun): GConf2

%description
This package contains programs to integrate Flash functionality into the GNOME
desktop.  It's main application is swfdec-player, a stand-alone viewer for
Flash files.  It also contains swfdec-thumbnailer, a program that provides
screenshots for files to display in the Nautilus file manager

%description -l zh_CN
集成 Flash 到 GNOME 桌面的程序

%prep
%setup -q
%patch0 -p1 -b .build


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install INSTALL='install -p'
%find_lang %{name}

desktop-file-install --vendor "fedora" --delete-original	\
  --dir $RPM_BUILD_ROOT%{_datadir}/applications			\
  $RPM_BUILD_ROOT%{_datadir}/applications/swfdec-player.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%pre
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/swfdec-thumbnailer.schemas >/dev/null || :
fi


%post
update-desktop-database &> /dev/null || :
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
  %{_sysconfdir}/gconf/schemas/swfdec-thumbnailer.schemas > /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/swfdec-thumbnailer.schemas > /dev/null || :
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING AUTHORS NEWS README
%{_bindir}/swfdec-player
%{_bindir}/swfdec-thumbnailer
%{_sysconfdir}/gconf/schemas/swfdec-thumbnailer.schemas
%{_datadir}/applications/fedora-swfdec-player.desktop
%{_datadir}/%{name}/
%{_mandir}/man1/swfdec*.1.gz
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.28.0-2
- 为 Magic 3.0 重建


