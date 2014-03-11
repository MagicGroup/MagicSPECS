%define inst_xinput %{_sbindir}/update-alternatives --install %{_sysconfdir}/X11/xinit/xinputrc xinputrc %{_sysconfdir}/X11/xinit/xinput.d/uim.conf 50
%define uninst_xinput %{_sbindir}/update-alternatives --remove xinputrc %{_sysconfdir}/X11/xinit/xinput.d/uim.conf

Name:		uim
Version:	1.8.6
Release:	3%{?dist}
# uim itself is licensed under BSD
# scm/py.scm, helper/eggtrayicon.[ch], qt/pref-kseparator.{cpp,h}
#   and qt/chardict/chardict-kseparator.{cpp,h} is licensed under LGPLv2+
# pixmaps/*.{svg,png} is licensed under BSD or LGPLv2
License:	BSD and LGPLv2+ and (BSD or LGPLv2)
URL:		http://code.google.com/p/uim/

BuildRequires:	libXft-devel libX11-devel libXext-devel libXrender-devel libXau-devel libXdmcp-devel libXt-devel
BuildRequires:	libgcroots-devel
BuildRequires:	gtk2-devel gtk3-devel ncurses-devel
BuildRequires:	anthy-devel Canna-devel eb-devel gettext desktop-file-utils
BuildRequires:	qt-devel
BuildRequires:	qt4-devel cmake kdelibs4-devel
BuildRequires:	libedit-devel openssl-devel libcurl-devel sqlite-devel expat-devel
BuildRequires:	m17n-lib-devel m17n-db-devel
BuildRequires:	m17n-db m17n-db-extras
BuildRequires:	emacs libtool automake autoconf intltool
Source0:	http://uim.googlecode.com/files/%{name}-%{version}.tar.bz2
Source1:	xinput.d-uim
Source2:	uim-init.el
Patch1:		uim-emacs-utf8.patch
Patch2:		uim-enable-libgcroots.patch


Summary:	A multilingual input method library
Group:		System Environment/Libraries
Requires(post): %{_sbindir}/update-alternatives /sbin/ldconfig
Requires(postun): %{_sbindir}/update-alternatives /sbin/ldconfig
Requires:	imsettings im-chooser

%package	devel
Summary:	Development files for the Uim library
Group:		Development/Libraries
Requires:	uim = %{version}-%{release}

%package	gtk2
Summary:	GTK+2 support for Uim
Group:		User Interface/Desktops
Requires:	uim = %{version}-%{release}
# for update-gtk-immodules
Requires(post):	gtk2 >= 2.9.1-2
Requires(postun): gtk2
Obsoletes:	%{name}-gnome < 1.8.5-4

%package	gtk3
Summary:	GTK+3 support for Uim
Group:		User Interface/Desktops
Requires:	uim = %{version}-%{release}
# for update-gtk-immodules
Requires(post):	gtk3
Requires(postun): gtk3
Obsoletes:	%{name}-gnome < 1.8.5-4

%package	qt
Summary:	Qt4 support for Uim
Group:		User Interface/Desktops

%package	qt3
Summary:	Qt3 support for Uim
Group:		User Interface/Desktops
Provides:	%{name}-qt-common = %{version}-%{release}

%package	kde
Summary:	KDE Applet for Uim
Group:		User Interface/Desktops
Requires:	uim = %{version}-%{release}
Requires:	uim-qt

%package	kde3
Summary:	KDE3 Applet for Uim
Group:		User Interface/Desktops
Requires:	uim = %{version}-%{release}
Requires:	uim-qt3

%package	-n emacs-uim
Summary:	Emacs support for Uim
Group:		System Environment/Libraries
Requires:	emacs-common-uim = %{version}-%{release}
Requires:	emacs(bin)
Provides:	uim-el = %{version}-%{release}

%package	-n emacs-common-uim
Summary:	Common package for Emacsen support for Uim
Group:		System Environment/Libraries
Requires:	uim = %{version}-%{release}
Provides:	uim-el-common = %{version}-%{release}

%package	-n xemacs-uim
Summary:	XEmacs support for Uim
Group:		System Environment/Libraries
Requires:	emacs-common-uim = %{version}-%{release}
Requires:	xemacs(bin) xemacs-packages-extra

%package	anthy
Summary:	Anthy support for Uim
Group:		System Environment/Libraries
Requires:	anthy >= 9100h-11
Requires:	uim = %{version}-%{release}
Requires(post):	gtk3 /usr/bin/uim-module-manager
Requires(postun): gtk3 /usr/bin/uim-module-manager

%package	canna
Summary:	Canna support for Uim
Group:		System Environment/Libraries
Requires:	Canna
Requires:	uim = %{version}-%{release}
Requires(post):	gtk3 /usr/bin/uim-module-manager
Requires(postun): gtk3 /usr/bin/uim-module-manager

%package	skk
Summary:	SKK support for Uim
Group:		System Environment/Libraries
Requires:	skkdic
Requires:	uim = %{version}-%{release}
Requires(post):	gtk3 /usr/bin/uim-module-manager
Requires(postun): gtk3 /usr/bin/uim-module-manager

%package	m17n
Summary:	m17n-lib support for Uim
Group:		System Environment/Libraries
Requires:	uim = %{version}-%{release}
Requires(post):	gtk3 /usr/bin/uim-module-manager
Requires(postun): gtk3 /usr/bin/uim-module-manager


%description
Uim is a multilingual input method library. Uim aims to
provide secure and useful input methods for all
languages. Currently, it can input to applications which
support Gtk+'s immodule, Qt's immodule and XIM.

This package provides the input method library, the XIM
bridge and most of the input methods.

For the Japanese input methods you need to install
- uim-anthy for Anthy
- uim-canna for Canna
- uim-skk for SKK.

%description	devel
Uim is a multilingual input method library. Uim aims to
provide secure and useful input methods for all
languages.

This package contains the header files and the libraries which is
needed for developing Uim applications.

%description	gtk2
Uim is a multilingual input method library. Uim aims to
provide secure and useful input methods for all
languages.

This package provides the Gtk IM module and helper program.

%description	gtk3
Uim is a multilingual input method library. Uim aims to
provide secure and useful input methods for all
languages.

This package provides the Gtk IM module and helper program.

%description	qt
Uim is a multilingual input method library. Uim aims to
provide secure and useful input methods for all
languages.

This package provides the Qt4 IM module and helper programs.

%description	qt3
Uim is a multilingual input method library. Uim aims to
provide secure and useful input methods for all
languages.

This package provides the Qt3 IM module and helper programs.

%description	kde
Uim is a multilingual input method library. Uim aims to
provide secure and useful input methods for all
languages.

This package provides the KDE applet.

%description	kde3
Uim is a multilingual input method library. Uim aims to
provide secure and useful input methods for all
languages.

This package provides the KDE3 applet.

%description	-n emacs-uim
This package provides Emacs support.

%description	-n emacs-common-uim
This package provides an utility to use Emacsen support for Uim.

%description	-n xemacs-uim
This package provides XEmacs support.

%description	anthy
This package provides support for Anthy, a Japanese input method.

%description	canna
This package provides support for Canna, a Japanese input method.

%description	skk
This package provides support for SKK, a Japanese input method.

%description	m17n
This package provides support for m17n-lib, which allows input of
many languages using the input table map from m17n-db.


%prep
%setup -q
%patch1 -p1 -b .1-emacs
%patch2 -p1 -b .2-libgcroots
autoconf


%build
# assumes that this is built against qt-3.3.
export QTDIR=%{_libdir}/qt-3.3
%configure --with-x --with-xft \
	--with-canna \
	--with-anthy --with-anthy-utf8 \
	--with-m17nlib \
	--with-eb --with-eb-conf=%{_libdir}/eb.conf \
	--without-scim \
        --with-gtk2 --with-gnome2 \
	--with-gtk3 --enable-gnome3-applet \
	--with-qt --with-qt-immodule \
	--with-qt4 --with-qt4-immodule \
	--enable-kde-applet --enable-kde4-applet \
	--with-curl \
	--with-expat \
	--enable-openssl --with-ssl-engine \
	--with-sqlite3 \
	--with-lispdir=%{_datadir}/emacs/site-lisp \
	--enable-pref
#sed -i -e 's/^\(hardcode_direct=\)$/\1yes/' -e 's/^\(hardcode_minus_L=\)$/\1no/' -e 's/^\(libext=\)$/\1"a"/' -e 's/^hardcode_libdir_flag_spec.*$'/'hardcode_libdir_flag_spec=" -D__LIBTOOL_IS_A_FOOL__ "/' libtool
sed -i -e 's/^\(hardcode_direct=\)$/\1no/' -e 's/^\(hardcode_minus_L=\)$/\1no/' -e 's/^\(libext=\)$/\1"a"/' libtool
LD_LIBRARY_PATH=$RPM_BUILD_DIR/%{name}-%{version}/uim/.libs make

%install
LD_LIBRARY_PATH=$RPM_BUILD_DIR/%{name}-%{version}/uim/.libs make install DESTDIR=$RPM_BUILD_ROOT
# For XEmacs
(cd emacs; make install DESTDIR=$RPM_BUILD_ROOT UIMEL_LISP_DIR=%{_datadir}/xemacs/site-packages/lisp/uim-el)

# remove .desktop file (#240706)
rm -f $RPM_BUILD_ROOT%{_datadir}/applications/uim.desktop

# remove unnecessary files
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/uim/plugin/*la
rm -rf $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/2.*/immodules/im-uim.*a
rm -rf $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/3.*/immodules/im-uim.*a
rm -rf $RPM_BUILD_ROOT%{_libdir}/qt-3.*/plugins/inputmethods/lib*.*a
#rm -rf $RPM_BUILD_ROOT%{_libdir}/libgcroots.*
#rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gcroots.pc
#rm -rf $RPM_BUILD_ROOT%{_includedir}/gcroots.h
rm -rf $RPM_BUILD_ROOT%{_includedir}/sigscheme
rm -rf $RPM_BUILD_ROOT%{_docdir}/sigscheme
rm -rf $RPM_BUILD_ROOT%{_datadir}/uim/{installed-modules,loader}.scm
rm -rf $RPM_BUILD_ROOT%{_libdir}/kde3/*.la
#rm -rf $RPM_BUILD_ROOT%{_datadir}/apps/kicker/applets/uimapplet.desktop

install -d $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinput.d
install -m 0644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinput.d/uim.conf
install -d $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d
install -m 0644 -p %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d/
install -d $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lisp/site-start.d
install -m 0644 -p %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lisp/site-start.d/

cp -a fep/README fep/README.fep
cp -a fep/README.ja fep/README.fep.ja
cp -a fep/README.key fep/README.fep.key
cp -a xim/README xim/README.xim

install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/uim
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/uim/{installed-modules,loader}.scm
ln -sf %{_localstatedir}/lib/uim/installed-modules.scm $RPM_BUILD_ROOT%{_datadir}/uim/
ln -sf %{_localstatedir}/lib/uim/loader.scm $RPM_BUILD_ROOT%{_datadir}/uim/

# https://fedoraproject.org/wiki/packagingDrafts/UsingAlternatives
touch $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinputrc
%find_lang %{name}

find $RPM_BUILD_ROOT -name "*.scm" -type f | egrep -v ".*/(anthy|canna|m17n|mana|prime|scim|sj3|skk|wnn|installed-modules|loader)" > scm.list
cat scm.list | sed -e s,$RPM_BUILD_ROOT,,g >> %{name}.lang
find $RPM_BUILD_ROOT -name "*.png" -type f | egrep -v ".*/(anthy|canna|m17n|mana|prime|scim|sj3|skk|wnn)" > png.list
cat png.list | sed -e s,$RPM_BUILD_ROOT,,g >> %{name}.lang
find $RPM_BUILD_ROOT -name "*.svg" -type f | egrep -v ".*/(anthy|canna|m17n|mana|prime|scim|sj3|skk|wnn)" > svg.list
cat svg.list | sed -e s,$RPM_BUILD_ROOT,,g >> %{name}.lang

# compress large doc
bzip2 ChangeLog


%post
/sbin/ldconfig
%{inst_xinput}
/usr/bin/uim-module-manager --path %{_localstatedir}/lib/uim --register tcode trycode tutcode byeoru latin pyload hangul viqr ipa-x-sampa > /dev/null 2>&1 || :

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%{uninst_xinput}
	/usr/bin/uim-module-manager --path %{_localstatedir}/lib/uim --unregister tcode trycode tutcode byeoru latin pyload hangul viqr ipa-x-sampa > /dev/null 2>&1 || :
fi

%post gtk2
umask 022
%{_bindir}/update-gtk-immodules %{_host} || :

%postun gtk2
umask 022
%{_bindir}/update-gtk-immodules %{_host} || :

%post gtk3
umask 022
%{_bindir}/gtk-query-immodules-3.0-%{__isa_bits} --update-cache || :

%postun gtk3
umask 022
%{_bindir}/gtk-query-immodules-3.0-%{__isa_bits} --update-cache || :

%post anthy
# since F-13
## get rid of anthy for inconvenience, because anthy-utf8 is default now.
/usr/bin/uim-module-manager --path %{_localstatedir}/lib/uim --unregister anthy > /dev/null 2>&1 || :
/usr/bin/uim-module-manager --path %{_localstatedir}/lib/uim --register anthy-utf8 > /dev/null 2>&1 || :

%postun anthy
if [ "$1" = "0" ]; then
	/usr/bin/uim-module-manager --path %{_localstatedir}/lib/uim --unregister anthy-utf8 > /dev/null 2>&1 || :
fi

%post canna
/usr/bin/uim-module-manager --path %{_localstatedir}/lib/uim --register canna > /dev/null 2>&1 || :

%postun canna
if [ "$1" = "0" ]; then
	/usr/bin/uim-module-manager --path %{_localstatedir}/lib/uim --unregister canna > /dev/null 2>&1 || :
fi

%post skk
/usr/bin/uim-module-manager --path %{_localstatedir}/lib/uim --register skk > /dev/null 2>&1 || :

%postun skk
if [ "$1" = "0" ]; then
	/usr/bin/uim-module-manager --path %{_localstatedir}/lib/uim --unregister skk > /dev/null 2>&1 || :
fi

%post m17n
/usr/bin/uim-module-manager --path %{_localstatedir}/lib/uim --register m17nlib > /dev/null 2>&1 || :

%postun m17n
if [ "$1" = "0" ]; then
	/usr/bin/uim-module-manager --path %{_localstatedir}/lib/uim --unregister m17nlib > /dev/null 2>&1 || :
fi


%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog* NEWS README fep/README.fep fep/README.fep.key xim/README.xim
%lang(ja) %doc fep/README.fep.ja
%dir %{_libdir}/uim
%dir %{_libdir}/uim/plugin
%dir %{_datadir}/uim
%dir %{_datadir}/uim/lib
%dir %{_datadir}/uim/pixmaps
%dir %{_localstatedir}/lib/uim
%{_bindir}/uim-fep*
%{_bindir}/uim-help
%{_bindir}/uim-module-manager
%{_bindir}/uim-sh
%{_bindir}/uim-xim
%{_libdir}/lib*.so.*
%{_datadir}/uim/byeoru-data/byeoru-dict
%{_datadir}/uim/helperdata
%{_datadir}/uim/tables/*.table
%verify(not md5 size mtime) %{_datadir}/uim/installed-modules.scm
%verify(not md5 size mtime) %{_datadir}/uim/loader.scm
%ghost %{_localstatedir}/lib/uim/*.scm
%exclude %{_datadir}/uim/anthy*.scm
%exclude %{_datadir}/uim/canna*.scm
%exclude %{_datadir}/uim/m17nlib.scm
%exclude %{_datadir}/uim/mana*.scm
%exclude %{_datadir}/uim/prime*.scm
%exclude %{_datadir}/uim/scim.scm
%exclude %{_datadir}/uim/sj3*.scm
%exclude %{_datadir}/uim/skk*.scm
%exclude %{_datadir}/uim/wnn*.scm
## pixmaps are licensed under BSD or LGPLv2
%exclude %{_datadir}/uim/pixmaps/anthy*.png
%exclude %{_datadir}/uim/pixmaps/canna.png
%exclude %{_datadir}/uim/pixmaps/m17n*png
%exclude %{_datadir}/uim/pixmaps/mana.png
%exclude %{_datadir}/uim/pixmaps/mana.svg
%exclude %{_datadir}/uim/pixmaps/prime*.png
%exclude %{_datadir}/uim/pixmaps/prime*.svg
%exclude %{_datadir}/uim/pixmaps/scim.png
%exclude %{_datadir}/uim/pixmaps/scim.svg
%exclude %{_datadir}/uim/pixmaps/sj3.png
%exclude %{_datadir}/uim/pixmaps/sj3.svg
%exclude %{_datadir}/uim/pixmaps/skk.png
%exclude %{_datadir}/uim/pixmaps/skk.svg
%exclude %{_datadir}/uim/pixmaps/wnn.png
%exclude %{_datadir}/uim/pixmaps/wnn.svg
%{_sysconfdir}/X11/xinit/xinput.d
%ghost %{_sysconfdir}/X11/xinit/xinputrc
%{_libdir}/uim/plugin/libuim-curl.so
%{_libdir}/uim/plugin/libuim-custom-enabler.so
%{_libdir}/uim/plugin/libuim-eb.so
%{_libdir}/uim/plugin/libuim-editline.so
%{_libdir}/uim/plugin/libuim-expat.so
%{_libdir}/uim/plugin/libuim-fileio.so
%{_libdir}/uim/plugin/libuim-lolevel.so
%{_libdir}/uim/plugin/libuim-look.so
%{_libdir}/uim/plugin/libuim-openssl.so
%{_libdir}/uim/plugin/libuim-process.so
%{_libdir}/uim/plugin/libuim-socket.so
%{_libdir}/uim/plugin/libuim-sqlite3.so
%{_libexecdir}/uim-helper-server
%{_mandir}/man1/uim-xim.1*

%files	devel
%doc AUTHORS COPYING ChangeLog* NEWS README
%{_includedir}/uim/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

%files	gtk2
%doc AUTHORS COPYING ChangeLog* NEWS README
# BSD
%{_bindir}/uim-toolbar-gtk
# BSD and LGPLv2+
%{_bindir}/uim-toolbar-gtk-systray
# BSD
%{_bindir}/uim-pref-gtk
%{_bindir}/uim-im-switcher-gtk
%{_bindir}/uim-input-pad-ja
%{_libdir}/gtk-2.0/2.*/immodules/*.so
%{_libexecdir}/uim-candwin-gtk
%{_libexecdir}/uim-candwin-horizontal-gtk
%{_libexecdir}/uim-candwin-tbl-gtk

%files	gtk3
%doc AUTHORS COPYING ChangeLog* NEWS README
%{_bindir}/uim-im-switcher-gtk3
%{_bindir}/uim-input-pad-ja-gtk3
%{_bindir}/uim-pref-gtk3
%{_bindir}/uim-toolbar-gtk3
%{_bindir}/uim-toolbar-gtk3-systray
%{_libdir}/gtk-3.0/3.*/immodules/*.so
%{_libexecdir}/uim-candwin-gtk3
%{_libexecdir}/uim-candwin-horizontal-gtk3
%{_libexecdir}/uim-candwin-tbl-gtk3
#临时性
%{_libexecdir}/uim-toolbar-applet-gnome3
%{_datadir}/dbus-1/services/org.gnome.panel.applet.UimAppletFactory.service
%{_datadir}/gnome-panel/4.0/applets/UimApplet.panel-applet

%files qt
%doc AUTHORS COPYING ChangeLog* NEWS
%{_bindir}/uim-chardict-qt4
%{_bindir}/uim-im-switcher-qt4
%{_bindir}/uim-pref-qt4
%{_bindir}/uim-toolbar-qt4
%{_libexecdir}/uim-candwin-qt4
%{_libdir}/qt4/plugins/inputmethods/libuiminputcontextplugin.so

%files qt3
%doc AUTHORS COPYING ChangeLog* NEWS README
# BSD and LGPLv2+
%{_bindir}/uim-chardict-qt
# BSD
%{_bindir}/uim-im-switcher-qt
# BSD and LGPLv2+
%{_bindir}/uim-pref-qt
# BSD
%{_bindir}/uim-toolbar-qt
%{_libexecdir}/uim-candwin-qt
%{_libdir}/qt-3.*/plugins/inputmethods

%files	kde
%doc AUTHORS COPYING ChangeLog* NEWS README
%{_libdir}/kde4/plasma_applet_uim.so
%{_datadir}/kde4/services/plasma-applet-uim.desktop

%if 0
%files	kde3
%doc AUTHORS COPYING ChangeLog* NEWS README
%{_libdir}/kde3/uim_panelapplet.so
%{_datadir}/apps/kicker/applets/uimapplet.desktop
%endif

%files	-n emacs-uim
%doc emacs/COPYING emacs/README
%lang(ja) %doc emacs/README.ja
%{_datadir}/emacs/site-lisp/uim-el
%{_datadir}/emacs/site-lisp/site-start.d/uim-init.el

%files	-n xemacs-uim
%doc emacs/COPYING emacs/README
%lang(ja) %doc emacs/README.ja
%{_datadir}/xemacs/site-packages/lisp/uim-el
%{_datadir}/xemacs/site-packages/lisp/site-start.d/uim-init.el

%files -n emacs-common-uim
%doc emacs/COPYING emacs/README
%{_bindir}/uim-el-agent
%{_bindir}/uim-el-helper-agent

%files	anthy
%doc AUTHORS COPYING ChangeLog* NEWS README
%{_libdir}/uim/plugin/libuim-anthy.so
%{_libdir}/uim/plugin/libuim-anthy-utf8.so
%{_datadir}/uim/anthy*.scm
# BSD or LGPLv2
%{_datadir}/uim/pixmaps/anthy*.png
%dir %{_datadir}/uim

%files	canna
%doc AUTHORS COPYING ChangeLog* NEWS README
%{_datadir}/uim/canna*.scm
# BSD or LGPLv2
%{_datadir}/uim/pixmaps/canna.png
%dir %{_datadir}/uim

%files	skk
%doc AUTHORS COPYING ChangeLog* NEWS README
%{_libdir}/uim/plugin/libuim-skk.so
%{_datadir}/uim/skk*.scm
%{_datadir}/uim/pixmaps/skk*.png
%{_datadir}/uim/pixmaps/skk*.svg
%dir %{_datadir}/uim

%files m17n
%doc AUTHORS COPYING ChangeLog* NEWS README
%{_bindir}/uim-m17nlib-relink-icons
%{_libdir}/uim/plugin/libuim-m17nlib.so
%{_datadir}/uim/m17nlib.scm
%{_datadir}/uim/m17nlib-custom.scm
# BSD or LGPLv2
%{_datadir}/uim/pixmaps/m17n*png
%dir %{_datadir}/uim

%changelog
* Tue Sep  3 2013 Akira TAGOH <tagoh@redhat.com> - 1.8.6-3
- Drop older Obsoletes and Conflicts lines (#1002125)
- Rebuilt against the latest eb.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul  5 2013 Akira TAGOH <tagoh@redhat.com> - 1.8.6-1
- New upstream release. (#981433)

* Mon Apr 22 2013 Akira TAGOH <tagoh@redhat.com> - 1.8.5-4
- Obsoletes uim-gnome. (#953986)

* Mon Apr 15 2013 Akira TAGOH <tagoh@redhat.com> - 1.8.5-3
- Create a socket file under XDG_RUNTIME_DIR. (#924005)

* Sun Apr 14 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.8.5-1
- Drop gnome-panel support as it's obsolete with gnome 3.8

* Mon Apr  1 2013 Akira TAGOH <tagoh@redhat.com> - 1.8.5-1
- New upstream release. (#946901)

* Wed Feb 20 2013 Akira TAGOH <tagoh@redhat.com> - 1.8.4-3
- Fix a crash issue in GTK+ immodule. (#879499)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 Akira TAGOH <tagoh@redhat.com> - 1.8.4-1
- New upstream release. (#890990)

* Mon Oct  1 2012 Akira TAGOH <tagoh@redhat.com> - 1.8.3-1
- New upstream release. (#861738)

* Tue Jul 31 2012 Akira TAGOH <tagoh@redhat.com> - 1.8.2-1
- New upstream release. (#844144)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun  5 2012 Akira TAGOH <tagoh@redhat.com> - 1.8.1-1
- New upstream release. (#828281)

* Mon Apr  2 2012 Akira TAGOH <tagoh@redhat.com> - 1.8.0-1
- New upstream release. (#808727)

* Fri Feb 17 2012 Akira TAGOH <tagoh@redhat.com> - 1.7.3-1
- New upstream release. (#790407)

* Wed Jan 18 2012 Akira TAGOH <tagoh@redhat.com> - 1.7.2-1
- New upstream release.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.7.1-3
- Rebuild for new libpng

* Mon Aug  8 2011 Akira TAGOH <tagoh@redhat.com> - 1.7.1-2
- check if gtk3 version of the prefs tool and immodule is available.

* Thu Aug  4 2011 Akira TAGOH <tagoh@redhat.com> - 1.7.1-1
- New upstream release.

* Tue May 24 2011 Akira TAGOH <tagoh@redhat.com> - 1.7.0-1
- New upstream release.

* Thu May 11 2011 Akira TAGOH <tagoh@redhat.com> - 1.7.0-0.1.20110511svn
- Update to the snapshot for gtk3 support.

* Tue Mar 22 2011 Akira TAGOH <tagoh@redhat.com> - 1.6.1-3
- backport patch from upstream to fix the modeline issue with
  other leim-enabled IM on Emacs.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Akira TAGOH <tagoh@redhat.com> - 1.6.1-1
- New upstream release.

* Thu Aug 12 2010 Akira TAGOH <tagoh@redhat.com> - 1.6.0-1
- new upstream release.

* Mon Mar 15 2010 Akira TAGOH <tagoh@redhat.com> - 1.5.7-3
- Use anthy-utf8 instead of anthy.
- Set the appropriate encoding for uim.el.

* Mon Feb 15 2010 Akira TAGOH <tagoh@redhat.com> - 1.5.7-2
- Fix the implicit DSO Linking issue. (#565169)

* Fri Dec 18 2009 Akira TAGOH <tagoh@redhat.com> - 1.5.7-1
- New upstream release.
  - Fix a crash in firefox. (#543813)
- uim-1.4.2-emacs23.patch: removed. it's not needed anymore.

* Mon Aug 31 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.6-2
- F-12: Rebuild against new eb

* Fri Aug 14 2009 Akira TAGOH <tagoh@redhat.com> - 1.5.6-1
- New upstream release.
- Remove patches because it has been applied in this release.
  - uim-qt-destdir.patch
  - uim-1.5.5-applet.patch
- Update the usage of alternatives according to PackagingDrafts/UsingAlternatives.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Akira TAGOH <tagoh@redhat.com> - 1.5.5-1
- New upstream release.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct 10 2008 Akira TAGOH <tagoh@redhat.com> - 1.5.3-1
- New upstream release.
- Add im-chooser to Requires again.

* Fri Aug 29 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.5.2-2
- Include directories /usr/share/uim/pixmaps and /usr/share/uim/lib

* Mon Aug 11 2008 Akira TAGOH <tagoh@redhat.com> - 1.5.2-1
- New upstream release.

* Tue Jul 15 2008 Akira TAGOH <tagoh@redhat.com> - 1.5.0-4
- Requires: imsettings instead of im-chooser.
- Add ICON parameter to uim.conf.
- Use Qt implementation of candidate window if the desktop
  session is KDE.
- set the appropriate immodule for multilib as scim does.

* Mon Jul 14 2008 Akira TAGOH <tagoh@redhat.com> - 1.5.0-3
- Add missing files. (#454957)

* Wed Jun  4 2008 Akira TAGOH <tagoh@redhat.com> - 1.5.0-2
- Obsoletes uim-el and uim-el-common.

* Thu May 22 2008 Akira TAGOH <tagoh@redhat.com> - 1.5.0-1
- New upstream release.
- Add xemacs-uim sub-package.
- Qt4 immodule is available in uim-qt now. (#440172)
- Build with --with-anthy-utf8 and --with-eb.
- Rename uim-el and uim-el-common to emacs-uim and emacs-common-uim.

* Tue Apr 22 2008 Akira TAGOH <tagoh@redhat.com> - 1.4.2-3
- uim-1.4.2-emacs23.patch: Apply to get uim.el working on Emacs 23. (#443572)

* Wed Apr  2 2008 Akira TAGOH <tagoh@redhat.com> - 1.4.2-2
- Move Qt3 immodule plugin to uim-qt3.
- Move the helper applications for Qt to uim-qt-common.
- Rebuild against qt3-devel. (#440870)

* Wed Mar  5 2008 Akira TAGOH <tagoh@redhat.com> - 1.4.2-1
- New upstream release.
- Remove patches because of no longer needed.
  - uim-1.4.1-m17n-not-list-nil-im.patch
  - uim-1.4.1-gcc43.patch
- Remove libgcroots.so.* (#436751)

* Thu Jan 31 2008 Akira TAGOH <tagoh@redhat.com> - 1.4.1-11
- Use full path to bring up XIM server.
- uim-1.4.1-gcc43.patch: Fix a build fail with gcc-4.3.

* Wed Oct 31 2007 Akira TAGOH <tagoh@redhat.com>
- Update the upstream URL.

* Fri Sep 28 2007 Akira TAGOH <tagoh@redhat.com> - 1.4.1-9
- Add Requires: uim-gtk2 in uim-gnome.

* Thu Sep 20 2007 Akira TAGOH <tagoh@redhat.com> - 1.4.1-8
- Add Requires: im-chooser and drop xorg-x11-xinit dependency. (#297231)
- Correct License tag. (Todd Zullinger)

* Mon Sep 10 2007 Akira TAGOH <tagoh@redhat.com> - 1.4.1-7
- Update the xinput script to support the new im-chooser.
  - bring up uim-toolbar-gtk-systray as the auxiliary program
  - support the config button.

* Mon Aug 20 2007 Akira TAGOH <tagoh@redhat.com> - 1.4.1-6
- uim-1.4.1-m17n-not-list-nil-im.patch: Fix appearing m17n-nil IME and crashing
  when it's selected. (#235331)

* Fri Aug 10 2007 Akira TAGOH <tagoh@redhat.com> - 1.4.1-5
- Update License tag.
- Update BuildReq.

* Tue May 29 2007 Akira TAGOH <tagoh@redhat.com> - 1.4.1-4
- Remove uim.desktop file. (#240706)

* Tue Apr  3 2007 Akira TAGOH <tagoh@redhat.com> - 1.4.1-3
- Register/Unregister the modules at %%post/%%postun. (#234804)
- Add X-GNOME-PersonalSettings to the desktop file categories.

* Mon Mar 26 2007 Akira TAGOH <tagoh@redhat.com> - 1.4.1-2
- Own %%{_libdir}/uim/plugin. (#233817)

* Mon Mar 19 2007 Akira TAGOH <tagoh@redhat.com> - 1.4.1-1
- New upstream release.
- add m17n-db-* and gettext to BR.

* Tue Jan 30 2007 Akira TAGOH <tagoh@redhat.com> - 1.4.0-1
- New upstream release.

* Mon Dec 18 2006 Akira TAGOH <tagoh@redhat.com> - 1.3.0-1
- New upstream release.

* Fri Sep 15 2006 Akira TAGOH <tagoh@redhat.com> - 1.2.1-2
- rebuilt

* Fri Sep  1 2006 Akira TAGOH <tagoh@redhat.com> - 1.2.1-1
- New upstream release.

* Fri Aug  4 2006 Akira TAGOH <tagoh@redhat.com> - 1.2.0-1
- New upstream release.

* Mon Jul 24 2006 Akira TAGOH <tagoh@redhat.com> - 1.1.1-2
- install a xinput file with .conf suffix.

* Fri Jul  7 2006 Akira TAGOH <tagoh@redhat.com> - 1.1.1-1
- New upstream release.

* Wed Jul  5 2006 Akira TAGOH <tagoh@redhat.com> - 1.1.0-2
- use %%{_host} not %%{_target_platform} for update-gtk-immodules.
- add PreReq: gtk2 >= 2.9.1-2 and ignore update-gtk-immodules errors.
- follow the new xinput.sh and added Requires: xorg-x11-xinit >= 1.0.2-5.fc6.
- removed the unnecessary %%post and %%postun.

* Mon Jun 19 2006 Akira TAGOH <tagoh@redhat.com> - 1.1.0-1
- New upstream release.

* Thu Mar  2 2006 Akira TAGOH <tagoh@redhat.com> - 1.0.1-2
- rebuilt.

* Tue Dec 27 2005 Akira TAGOH <tagoh@redhat.com> - 1.0.1-1
- New upstream release.

* Fri Dec 16 2005 Akira TAGOH <tagoh@redhat.com> - 1.0.0-0.2.beta
- updates to 1.0.0-beta.

* Thu Dec 15 2005 Akira TAGOH <tagoh@redhat.com> - 1.0.0-0.1.alpha
- New upstream release.
- added uim-m17n package. (#175600)
- added uim-el package.
- uim-0.4.6-dont-require-devel-pkgs.patch: removed.

* Fri Sep 30 2005 Akira TAGOH <tagoh@redhat.com> - 0.4.9.1-1
- New upstream release.

* Wed Aug 17 2005 Akira TAGOH <tagoh@redhat.com> - 0.4.8-1
- New upstream release.

* Thu Aug  4 2005 Akira TAGOH <tagoh@redhat.com> - 0.4.7.1-2
- removed Requires: Canna-devel from uim-canna. this is no longer needed
  since 0.4.6-4. (Warren Togami, #165088)

* Wed Aug  3 2005 Akira TAGOH <tagoh@redhat.com> - 0.4.7.1-1
- New upstream release.

* Tue Jul 12 2005 Akira TAGOH <tagoh@redhat.com> - 0.4.7-1
- New upstream release.
- removed the patches. fixed in upstream.
  - uim-0.4.6-multilib.patch
  - uim-0.4.6-fix-typo-in-configure.patch

* Wed Jun 29 2005 Akira TAGOH <tagoh@redhat.com> - 0.4.6-5
- built with --without-scim explicitly. it doesn't work actually.

* Mon Jun 13 2005 Akira TAGOH <tagoh@redhat.com> - 0.4.6-4
- uim-0.4.6-fix-typo-in-configure.patch: applied to get uim-pref-gtk building.
- uim-0.4.6-dont-require-devel-pkgs.patch: applied to be able to dlopen
  the shared libraries without -devel packages.

* Mon May 16 2005 Akira TAGOH <tagoh@redhat.com> - 0.4.6-3
- uim-0.4.6-multilib.patch: applied to fix a build issue for
  libquiminputcontextplugin.so. (John Thacker, #156880)

* Fri May  6 2005 Akira TAGOH <tagoh@redhat.com> - 0.4.6-2
- added BuildRequires: ncurses-devel. (#156880)

* Mon Apr 18 2005 Akira TAGOH <tagoh@redhat.com> - 0.4.6-1
- New upstream release. (#155173)
  - fixed missing return statement issue. (#150304)
- Updated upstream URL.
- ensure to build with Canna and anthy.
- enabled Qt immodule.
- added QT_IM_MODULE=uim to xinput.d-uim

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.4.5.1-2
- Include headers directory in -devel package.

* Fri Mar  4 2005 Ville Skyttä <ville.skytta at iki.fi>
- Split context marked dependency syntax to work around #118773.
- Add ldconfig scriptlet dependencies.

* Thu Feb 24 2005 Akira TAGOH <tagoh@redhat.com> - 0.4.5.1-1
- New upstream release.
  - security fix.
- support xinput script.

* Sun Feb 20 2005 Thorsten Leemhuis <fedora[AT]leemhuis[dot]info> 0.4.5-2
- Added autoreconf-patch; fixes build on x86_64

* Wed Jan 12 2005 Akira TAGOH <tagoh@redhat.com> 0.4.5-1
- New upstream release.

* Wed Sep 08 2004 Akira TAGOH <tagoh@redhat.com> 0.4.3-1
- New upstream release.
- moved out gtk2 related files to uim-gtk2 package.

* Mon Jul 12 2004 Jens Petersen <petersen@redhat.com> - 0.4.0-1
- no longer need to remove screen files
- include console fep programs

* Fri Jul  2 2004 Jens Petersen <petersen@redhat.com> - 0.3.9-3
- support both update-gtk-immodules of newer gtk2 and older
  gtk-query-immodules-2.0 with new %%gtk_im_update added

* Wed Jun 30 2004 Jens Petersen <petersen@redhat.com> - 0.3.9-2
- add uim-applet-category-cjk.patch to put applet in right submenu
- improve the summaries and descriptions
- make the Requires(postun) be Requires(post,postun)
- file ownership and other minor cleanup

* Wed Jun 23 2004 Akira TAGOH <tagoh@redhat.com> 0.3.9-1
- New upstream release.

* Fri Jun 04 2004 Akira TAGOH <tagoh@redhat.com> 0.3.8-4
- wrote the descriptions.
- uim-skk: fixed the dependency.

* Fri Jun 04 2004 Nils Philippsen <nphilipp@redhat.com> 0.3.8-3
- more spec cleanups

* Fri Jun 04 2004 Warren Togami <wtogami@redhat.com> 0.3.8-2
- many spec cleanups

* Thu Jun 03 2004 Akira TAGOH <tagoh@redhat.com> 0.3.8-1
- Initial package.
