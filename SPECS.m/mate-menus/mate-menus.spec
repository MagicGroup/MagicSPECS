Name:           mate-menus
Version:        1.8.0
Release:        1%{?dist}
Summary:        Displays menus for MATE Desktop
License:        GPLv2+ and LGPLv2+
URL:            http://mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
Source1:        mate-preferences-categories.menu

BuildRequires:  chrpath
BuildRequires:  gobject-introspection-devel
BuildRequires:  mate-common
BuildRequires:  python-devel

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

%description
Displays menus for MATE Desktop

%package libs
Summary: Shared libraries for mate-menus
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description libs
Shared libraries for mate-menus

%package preferences-category-menu
Summary: Categories for the preferences menu
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description preferences-category-menu
Categories for the preferences menu

%package devel
Summary: Development files for mate-menus
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development files for mate-menus

%prep
%setup -q

# fedora specific
# fix for usage of multimedia-menus package
sed -i -e '/<!-- End Other -->/ a\  <MergeFile>applications-merged/multimedia-categories.menu</MergeFile>' layout/mate-applications.menu



%build
%configure \
 --disable-static \
 --enable-python \
 --enable-introspection=yes

make %{?_smp_mflags} V=1


%install
%{make_install}

install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/menus
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'
chrpath --delete $RPM_BUILD_ROOT%{python_sitearch}/matemenu.so

%find_lang %{name} --with-gnome --all-name

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files -f %{name}.lang
%doc AUTHORS COPYING README
%config %{_sysconfdir}/xdg/menus/mate-applications.menu
%config %{_sysconfdir}/xdg/menus/mate-settings.menu
%{_datadir}/mate-menus
%{_datadir}/mate/desktop-directories

%files libs
%{_libdir}/girepository-1.0/MateMenu-2.0.typelib
%{_libdir}/libmate-menu.so.2
%{_libdir}/libmate-menu.so.2.4.9
%{python_sitearch}/matemenu.so

%files preferences-category-menu
%config %{_sysconfdir}/xdg/menus/mate-preferences-categories.menu

%files devel
%{_datadir}/gir-1.0/MateMenu-2.0.gir
%{_libdir}/libmate-menu.so
%{_includedir}/mate-menus
%{_libdir}/pkgconfig/libmate-menu.pc


%changelog
* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Sun Feb 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90 release

* Mon Jan 20 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> 1.7.1-1
- update to 1.7.1 release
- add missing changelog entry from previous build
- add --with-gnome --all-name for find language
- use modern 'make install' macro

* Fri Dec 06 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- update to 1.7.0 release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 04 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-4
- fix for usage of multimedia-menus package

* Fri Jun 07 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-3
- move preferences-category-menu to a subpackage

* Tue Jun 04 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-2
- add preferences-category-menu
- add requires mate-menus-libs
- mark *.menu files as %%config in %%{_sysconfdir} dir

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- clean up spec file
- remove un-needed build requires

* Thu Aug 16 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Fix devel package requirements. Removed libs requirement.

* Thu Aug 16 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Fix directory ownership for mate-menus dir.

* Thu Jul 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build

