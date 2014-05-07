%global  basever 0.8.8

Name:           emerald
URL:            http://www.compiz.org/
License:        GPLv2+
Group:          User Interface/Desktops
Version:        0.8.8
Release:        9%{?dist}
Epoch:          1
Summary:        Themeable window decorator and compositing manager for Compiz
Source0:        http://releases.compiz.org/%{version}/%{name}-%{version}.tar.bz2

Patch0:         emerald_new_DSO.patch
Patch1:         emerald_build_without_gtk_disable_deprecated.patch
Patch2:         emerald_new-mate.patch
Patch3:         emerald_improve_desktop_file.patch
Patch4:         emerald_manpage.patch
Patch5:         emerald_potfiles_skip.patch
Patch6:         emerald-aarch64.patch
Patch7:         emerald_automake-1.13.patch

# compiz-devel is not available on these arches
ExcludeArch:    s390 s390x

Requires:       compiz >= %{basever}

BuildRequires:  compiz-devel >= %{basever}
BuildRequires:  libwnck-devel
BuildRequires:  gtk2-devel
BuildRequires:  intltool 
BuildRequires:  desktop-file-utils
BuildRequires:  perl(XML::Parser) 
BuildRequires:  gettext-devel
BuildRequires:  libXres-devel
BuildRequires:  libtool


%description
Emerald is themeable window decorator and compositing
manager for Compiz.


%package devel
Summary: Development files for emerald
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: pkgconfig

%description devel
The emerald-devel package provides development files
for emerald, the themeable window decorator for Compiz.


%prep
%setup -q
%patch0 -p1 -b .DSO
%patch1 -p1 -b .gtk_disable_deprecated
%patch2 -p1 -b .mate
%patch3 -p1 -b .desktop_file
%patch4 -p1 -b .manpage
%patch5 -p1 -b .potfiles_skip
%patch6 -p1 -b .aarch64
%patch7 -p1 -b .automake

autoreconf -f -i

%build
%configure --disable-mime-update

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make DESTDIR=$RPM_BUILD_ROOT install

find $RPM_BUILD_ROOT -type f -name "*.a" -o -name "*.la" | xargs rm -f

%find_lang %{name}


%check
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/emerald-theme-manager.desktop


%post
/sbin/ldconfig
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor/48x48/mimetypes &>/dev/null || :

%postun
/sbin/ldconfig
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor/48x48/mimetypes &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor/48x48/mimetypes &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor/48x48/mimetypes &>/dev/null || :



%files -f %{name}.lang
%doc COPYING
%{_bindir}/*
%{_datadir}/pixmaps/emerald-theme-manager-icon.png
%dir %{_libdir}/emerald
%dir %{_libdir}/emerald/engines
%{_libdir}/emerald/engines/*.so
%{_libdir}/libemeraldengine.so.*
%dir %{_datadir}/emerald
%dir %{_datadir}/emerald/theme
%{_datadir}/emerald/theme/*
%{_datadir}/emerald/settings.ini
%{_datadir}/applications/emerald-theme-manager.desktop
%{_datadir}/mime-info/emerald.mime
%{_datadir}/mime/packages/emerald.xml
%{_datadir}/icons/hicolor/48x48/mimetypes/application-x-emerald-theme.png
%{_mandir}/man1/*.1.*

%files devel
%{_includedir}/emerald/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libemeraldengine.so


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 25 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-8
- fix build for aarch64
- re-work mate.patch again
- add libtool BR for autoreconf
- fix automake-1.13 build deprecations
- re-work DSO.patch

* Wed Feb 13 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-7
- rework mate-patch

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 26 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-5
- fix license information
- fix rpm scriptlets
- add icon cache rpm scriptlet
- rename DSO patch

* Mon Oct 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-4
- build for fedora
- review package
- fix unused-direct-shlib-dependency
- add basever
- add Epoch tag

* Mon Oct 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-3
- add patches from Jasmine Hassan jasmine.aura@gmail.com

* Wed Sep 19 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-2
- improve spec file
- add desktop-file-validate for emerald-theme-manager.desktop

* Tue May 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-1
- build for mate

* Sun Nov 14 2010 Leigh Scott <leigh123linux@googlemail.com> - 0.8.4-7
- apply more upstream gtk deprecated fixes

