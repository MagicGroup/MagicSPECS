%define _xinputconf %{_sysconfdir}/X11/xinit/xinput.d/fcitx.conf
%{!?gtk2_binary_version: %define gtk2_binary_version %(pkg-config  --variable=gtk_binary_version gtk+-2.0)}
%{!?gtk3_binary_version: %define gtk3_binary_version %(pkg-config  --variable=gtk_binary_version gtk+-3.0)}

Name:			fcitx
Summary:		An input method framework
Version:		4.2.8.3
Release:		2%{?dist}
License:		GPLv2+
Group:			User Interface/Desktops
URL:			https://fcitx-im.org/wiki/Fcitx
Source0:		http://download.fcitx-im.org/fcitx/%{name}-%{version}_dict.tar.xz
Source1:		xinput-%{name}
BuildRequires:		pango-devel, dbus-devel, opencc-devel
BuildRequires:		wget, intltool, chrpath, sysconftool, opencc
BuildRequires:		cmake, libtool, doxygen, libicu-devel
BuildRequires:		qt4-devel, gtk3-devel, gtk2-devel, libicu
BuildRequires:		xorg-x11-proto-devel, xorg-x11-xtrans-devel
BuildRequires:		gobject-introspection-devel, libxkbfile-devel 
BuildRequires:		enchant-devel, iso-codes-devel, libicu-devel
BuildRequires:		libX11-devel, qt4, dbus-glib-devel, dbus-x11
BuildRequires:		desktop-file-utils, libxml2-devel
BuildRequires:		lua-devel
Requires:		%{name}-data = %{version}-%{release}
Requires:		imsettings
Requires(post):		%{_sbindir}/alternatives
Requires(postun):	%{_sbindir}/alternatives
Requires:		%{name}-libs = %{version}-%{release}
Requires:		%{name}-gtk3 = %{version}-%{release}
Requires:		%{name}-gtk2 = %{version}-%{release}

%description
Fcitx is an input method framework with extension support. Currently it
supports Linux and Unix systems like FreeBSD.

Fcitx tries to provide a native feeling under all desktop as well as a light
weight core. You can easily customize it to fit your requirements.

%package data
Summary:		Data files of Fcitx
Group:			System Environment/Libraries
BuildArch:		noarch
Requires:		hicolor-icon-theme
Requires:		dbus

%description data
The %{name}-data package provides shared datas for Fcitx.

%package libs
Summary:		Shared libraries for Fcitx
Group:			System Environment/Libraries
Provides:		%{name}-keyboard = %{version}-%{release}
Obsoletes:		%{name}-keyboard =< 4.2.3

%description libs
The %{name}-libs package provides shared libraries for Fcitx

%package devel
Summary:		Development files for Fcitx
Group:			Development/Libraries
Requires:		%{name}-libs = %{version}-%{release}
Requires:		/usr/bin/pkg-config
Requires:		libX11-devel

%description devel
The %{name}-devel package contains libraries and header files necessary for
developing programs using Fcitx libraries.

%package table-chinese
Summary:		Chinese table of Fcitx
Group:			System Environment/Libraries
BuildArch:		noarch
Requires:		%{name}-table = %{version}-%{release}

%description table-chinese
The %{name}-table-chinese package provides other Chinese table for Fcitx.

%package gtk2
Summary:		Fcitx IM module for gtk2
Group:			System Environment/Libraries
Requires:		%{name} = %{version}-%{release}
Requires:		%{name}-libs = %{version}-%{release}

%description gtk2
This package contains Fcitx IM module for gtk2.

%package gtk3
Summary:		Fcitx IM module for gtk3
Group:			System Environment/Libraries
Requires:		%{name} = %{version}-%{release}
Requires:		%{name}-libs = %{version}-%{release}
Requires:		imsettings-gnome

%description gtk3
This package contains Fcitx IM module for gtk3.

%package qt4
Summary:		Fcitx IM module for qt4
Group:			System Environment/Libraries
Requires:		%{name} = %{version}-%{release}
Requires:		%{name}-libs = %{version}-%{release}

%description qt4
This package contains Fcitx IM module for qt4.

%package pinyin
Summary:		Pinyin Engine for Fcitx
URL:			https://fcitx-im.org/wiki/Built-in_Pinyin
Group:			System Environment/Libraries
Requires:		%{name} = %{version}-%{release}
Requires:		%{name}-libs = %{version}-%{release}
Requires:		%{name}-data = %{version}-%{release}

%description pinyin
This package contains pinyin engine for Fcitx.

%package qw
Summary:		Quwei Engine for Fcitx
URL:			https://fcitx-im.org/wiki/QuWei
Group:			System Environment/Libraries
Requires:		%{name} = %{version}-%{release}
Requires:		%{name}-libs = %{version}-%{release}
Requires:		%{name}-data = %{version}-%{release}

%description qw
This package contains Quwei engine for Fcitx.

%package table
Summary:		Table Engine for Fcitx
URL:			https://fcitx-im.org/wiki/Table
Group:			System Environment/Libraries
Requires:		%{name} = %{version}-%{release}
Requires:		%{name}-libs = %{version}-%{release}
Requires:		%{name}-data = %{version}-%{release}
Requires:		%{name}-pinyin = %{version}-%{release}

%description table
This package contains table engine for Fcitx.


%prep
%setup -q

%build
mkdir -p build
pushd build
%cmake .. -DENABLE_GTK3_IM_MODULE=On -DENABLE_QT_IM_MODULE=On -DENABLE_OPENCC=On -DENABLE_LUA=On -DENABLE_GIR=On -DENABLE_XDGAUTOSTART=Off
make VERBOSE=1 %{?_smp_mflags}

%install
pushd build
make install INSTALL="install -p" DESTDIR=$RPM_BUILD_ROOT
rm -f %{buildroot}%{_libdir}/*.la
popd

install -pm 644 -D %{SOURCE1} %{buildroot}%{_xinputconf}

install -pm 644 AUTHORS ChangeLog THANKS TODO COPYING %{buildroot}/%{_docdir}/%{name}/

# patch fcitx4-config to use pkg-config to solve libdir to avoid multiarch
# confilict
sed -i -e 's:%{_libdir}:`pkg-config --variable=libdir fcitx`:g' \
  ${RPM_BUILD_ROOT}%{_bindir}/fcitx4-config
magic_rpm_clean.sh
%find_lang %{name}

desktop-file-install --delete-original \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}-skin-installer.desktop

desktop-file-install --delete-original \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}-configtool.desktop

desktop-file-install --delete-original \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

%clean
rm -rf %{buildroot}

%post 
%{_sbindir}/alternatives --install %{_sysconfdir}/X11/xinit/xinputrc xinputrc %{_xinputconf} 55 || :
update-desktop-database %{_datadir}/applications &>/dev/null || :

%postun  
if [ "$1" = "0" ]; then
  %{_sbindir}/alternatives --remove xinputrc %{_xinputconf} || :
  # if alternative was set to manual, reset to auto
  [ -L %{_sysconfdir}/alternatives/xinputrc -a "`readlink %{_sysconfdir}/alternatives/xinputrc`" = "%{_xinputconf}" ] && %{_sbindir}/alternatives --auto xinputrc || :
fi
update-desktop-database %{_datadir}/applications &>/dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post data
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun data
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans data
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post gtk2
%{_bindir}/update-gtk-immodules %{_host} || :

%postun gtk2
%{_bindir}/update-gtk-immodules %{_host} || :

%post gtk3
%{_bindir}/gtk-query-immodules-3.0-%{__isa_bits} --update-cache || :

%postun gtk3
%{_bindir}/gtk-query-immodules-3.0-%{__isa_bits} --update-cache || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%config %{_xinputconf}
%{_bindir}/fcitx-*
%{_bindir}/fcitx
%{_bindir}/createPYMB
%{_bindir}/mb2org
%{_bindir}/mb2txt
%{_bindir}/readPYBase
%{_bindir}/readPYMB
%{_bindir}/scel2org
%{_bindir}/txt2mb
%{_datadir}/applications/%{name}-skin-installer.desktop
%dir %{_datadir}/%{name}/dbus/
%{_datadir}/%{name}/dbus/daemon.conf
%{_datadir}/applications/%{name}-configtool.desktop
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/x-fskin.xml
%{_docdir}/%{name}/
%{_mandir}/man1/createPYMB.1.gz
%{_mandir}/man1/fcitx-remote.1.gz
%{_mandir}/man1/fcitx.1.gz
%{_mandir}/man1/mb2org.1.gz
%{_mandir}/man1/mb2txt.1.gz
%{_mandir}/man1/readPYBase.1.gz
%{_mandir}/man1/readPYMB.1.gz
%{_mandir}/man1/scel2org.1.gz
%{_mandir}/man1/txt2mb.1.gz

%files libs
%defattr(-,root,root,-)
%doc
%{_libdir}/libfcitx*.so.*
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/%{name}-[!pqt]*.so
%{_libdir}/%{name}/%{name}-punc.so
%{_libdir}/%{name}/%{name}-quickphrase.so
%{_libdir}/%{name}/qt/
%{_libdir}/%{name}/libexec/
%dir %{_libdir}/girepository-1.0/
%{_libdir}/girepository-1.0/Fcitx-1.0.typelib

%files data
%defattr(-,root,root,-)
%doc 
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/16x16/status/*.png
%{_datadir}/icons/hicolor/22x22/status/*.png
%{_datadir}/icons/hicolor/24x24/status/*.png
%{_datadir}/icons/hicolor/48x48/status/*.png
%{_datadir}/icons/hicolor/scalable/status/*.svg
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/skin/
%dir %{_datadir}/%{name}/addon
%{_datadir}/%{name}/addon/%{name}-[!pqt]*.conf
%{_datadir}/%{name}/addon/%{name}-punc.conf
%{_datadir}/%{name}/addon/%{name}-quickphrase.conf
%{_datadir}/%{name}/data/
%{_datadir}/%{name}/spell/
%dir %{_datadir}/%{name}/imicon/
%dir %{_datadir}/%{name}/inputmethod/
%dir %{_datadir}/%{name}/configdesc/
%dir %{_datadir}/%{name}/table/
%{_datadir}/%{name}/configdesc/[!ft]*.desc
%{_datadir}/%{name}/configdesc/fcitx-[!p]*.desc
%{_datadir}/dbus-1/services/org.fcitx.Fcitx.service

%files devel
%defattr(-,root,root,-)
%doc 
%{_bindir}/fcitx4-config
%{_libdir}/libfcitx*.so
%{_libdir}/pkgconfig/fcitx*.pc
%{_includedir}/fcitx*
%{_datadir}/cmake/%{name}/
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Fcitx-1.0.gir

%files table-chinese
%defattr(-,root,root,-)
%doc
%{_datadir}/%{name}/table/*
%{_datadir}/%{name}/imicon/[!ps]*.png

%files pinyin
%defattr(-,root,root,-)
%doc
%{_datadir}/%{name}/inputmethod/pinyin.conf
%{_datadir}/%{name}/inputmethod/shuangpin.conf
%{_datadir}/%{name}/pinyin/
%{_datadir}/%{name}/configdesc/fcitx-pinyin.desc
%{_datadir}/%{name}/configdesc/fcitx-pinyin-enhance.desc
%{_datadir}/%{name}/addon/fcitx-pinyin.conf
%{_datadir}/%{name}/addon/fcitx-pinyin-enhance.conf
%{_datadir}/%{name}/imicon/pinyin.png
%{_datadir}/%{name}/imicon/shuangpin.png
%{_libdir}/%{name}/%{name}-pinyin.so
%{_libdir}/%{name}/%{name}-pinyin-enhance.so
%{_datadir}/%{name}/py-enhance/

%files qw
%defattr(-,root,root,-)
%doc
%{_datadir}/%{name}/inputmethod/qw.conf
%{_libdir}/%{name}/%{name}-qw.so
%{_datadir}/%{name}/addon/fcitx-qw.conf

%files table
%defattr(-,root,root,-)
%doc
%{_datadir}/%{name}/configdesc/table.desc
%{_libdir}/%{name}/%{name}-table.so
%{_datadir}/%{name}/addon/fcitx-table.conf

%files gtk2
%defattr(-,root,root,-)
%{_libdir}/gtk-2.0/%{gtk2_binary_version}/immodules/im-fcitx.so

%files gtk3
%defattr(-,root,root,-)
%{_libdir}/gtk-3.0/%{gtk3_binary_version}/immodules/im-fcitx.so

%files qt4
%defattr(-,root,root,-)
%{_libdir}/qt4/plugins/inputmethods/qtim-fcitx.so


%changelog
* Fri Feb 14 2014 Parag Nemade <paragn AT fedoraproject DOT org> - 4.2.8.3-2
- Rebuild for icu 52

* Tue Oct 29 2013 Robin Lee <cheeselee@fedoraproject.org> - 4.2.8.3-1
- Update to 4.2.8.3
- Update summary of fcitx package
- Other minor spell fixes

* Fri Aug 23 2013 Robin Lee <cheeselee@fedoraproject.org> - 4.2.8-3
- Own some missed directories
- Update URL's and Source0 URL
- Revise description following upstream wiki

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul  2 2013 Robin Lee <cheeselee@fedoraproject.org> - 4.2.8-1
- Update to 4.2.8 (https://www.csslayer.info/wordpress/fcitx-dev/fcitx-4-2-8/)
- Add scriptlets to update icon cache (BZ#980309)

* Fri Jun 21 2013 Robin Lee <cheeselee@fedoraproject.org> - 4.2.7-6
- Move fcitx4-config to devel package and patch it to use pkg-config to solve
  libdir
- devel subpackage explicitly requires pkgconfig

* Fri Jun 21 2013 Robin Lee <cheeselee@fedoraproject.org> - 4.2.7-5
- Move fcitx4-config to base package to solve multiarch devel subpackage conflict

* Wed Jun 19 2013 Robin Lee <cheeselee@fedoraproject.org> - 4.2.7-4
- BR: lua-devel (BZ#974729)
- Move %%{_datadir}/gir-1.0/Fcitx-1.0.gir %%{_bindir}/fcitx4-config to devel
  subpackage (BZ#965914)
- Co-own %%{_datadir}/gir-1.0/, %%{_libdir}/girepository-1.0/
- Own %%{_libdir}/%%{name}/qt/, %%{_libdir}/%%{name}/
- Other minor cleanup

* Mon Apr 29 2013 Robin Lee <cheeselee@fedoraproject.org> - 4.2.7-3
- Fix gtk2 subpackage description (#830377)

* Sat Mar 23 2013 Liang Suilong <liangsuilong@gmail.com> - 4.2.7-2
- Fix to enable Lua support

* Fri Feb 01 2013 Liang Suilong <liangsuilong@gmail.com> - 4.2.7-1
- Upstream to fcitx-4.2.7

* Sat Jan 26 2013 Kevin Fenzi <kevin@scrye.com> 4.2.6.1-3
- Rebuild for new icu

* Mon Nov 26 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.6.1-2
- Disable xdg-autostart

* Wed Oct 31 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.6.1-1
- Upstream to fcitx-4.2.6.1

* Sun Jul 22 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.5-1
- Upstream to fcitx-4.2.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.4-2
- Drop fcitx-keyboard
- Divide Table Engine into fcitx-table
- Move GIR Binding into fcitx-libs

* Tue Jun 05 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.4-1
- Upgrade to fcitx-4.2.4
- Fix the ownership conflict on fcitx and fcitx-data
- Divide Pinyin engine into fcitx-pinyin
- Divide Quwei engine into fcitx-qw
- Divide XKB integration into fcitx-keyboard

* Mon May 07 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.3-1
- Upgrade to fcitx-4.2.3

* Thu Apr 26 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.2-2
- Upgrade to fcitx-4.2.2

* Sun Apr 22 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.2-1
- Upgrade to fcitx-4.2.2

* Sat Feb 04 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.0-1
- Upgrade to fcitx-4.2.0

* Sun Dec 25 2011 Liang Suilong <liangsuilong@gmail.com> - 4.1.2-3
- Fix the spec

* Sun Dec 25 2011 Liang Suilong <liangsuilong@gmail.com> - 4.1.2-2
- Fix the spec

* Sun Dec 25 2011 Liang Suilong <liangsuilong@gmail.com> - 4.1.2-1
- Update to 4.1.2
- move fcitx4-config to devel

* Fri Sep 09 2011 Liang Suilong <liangsuilong@gmail.com> - 4.1.1-2
- Update xinput-fcitx
- Add fcitx-gtk3 as fcitx requires

* Fri Sep 09 2011 Liang Suilong <liangsuilong@gmail.com> - 4.1.1-1
- Upstream to fcitx-4.1.1

* Fri Sep 09 2011 Liang Suilong <liangsuilong@gmail.com> - 4.1.0-1
- Upstream to fcitx-4.1.0
- Add fcitx-gtk2 as FCITX im module for gtk2
- Add fcitx-gtk3 as FCITX im module for gtk3
- Add fcitx-qt4 as FCITX im module for qt4

* Tue Aug 02 2011 Liang Suilong <liangsuilong@gmail.com> - 4.0.1-5
- Fix that %%files lists a wrong address
- Separate fcitx-libs again

* Tue Aug 02 2011 Liang Suilong <liangsuilong@gmail.com> - 4.0.1-4
- Separates varieties of tables from FCITX
- Merge fcitx-libs into fcitx 

* Sun Jul 03 2011 Liang Suilong <liangsuilong@gmail.com> - 4.0.1-3
- Support GNOME 3 tray icon
- Fix that main window is covered by GNOME Shell 

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 19 2010 Chen Lei <supercyper@163.com> - 4.0.0-1
- Update to 4.0.0

* Mon Jun 14 2010 Chen Lei <supercyper@163.com> - 3.6.3-5.20100514svn_utf8
- Remove BR:libXext-devel

* Fri May 14 2010 Chen Lei <supercyper@163.com> - 3.6.3-4.20100514svn_utf8
- svn 365

* Sun Apr 18 2010 Chen Lei <supercyper@163.com> - 3.6.3-3.20100410svn_utf8
- Exclude xpm files

* Sat Apr 17 2010 Chen Lei <supercyper@163.com> - 3.6.3-2.20100410svn_utf8
- Update License tag
- Add more explanation for UTF-8 branch

* Mon Apr 12 2010 Chen Lei <supercyper@163.com> - 3.6.3-1.20100410svn_utf8
- Initial Package
