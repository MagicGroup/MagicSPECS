Name:           mate-menus
Version: 1.9.0
Release: 1%{?dist}
Summary:        Displays menus for MATE Desktop
Summary(zh_CN.UTF-8): MATE 桌面的显示菜单
License:        GPLv2+ and LGPLv2+
URL:            http://mate-desktop.org
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://pub.mate-desktop.org/releases/%{majorver}/%{name}-%{version}.tar.xz
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

%description -l zh_CN.UTF-8
MATE 桌面的显示菜单。

%package libs
Summary: Shared libraries for mate-menus
Summary(zh_CN.UTF-8): %{name} 的运行库
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description libs
Shared libraries for mate-menus

%description libs -l zh_CN.UTF-8
mate-menus 的运行库。

%package preferences-category-menu
Summary: Categories for the preferences menu
Summary(zh_CN.UTF-8): 参数菜单的分类
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description preferences-category-menu
Categories for the preferences menu

%description preferences-category-menu -l zh_CN.UTF-8
参数菜单的分类。

%package devel
Summary: Development files for mate-menus
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development files for mate-menus

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

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
magic_rpm_clean.sh
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
* Mon Aug 11 2014 Liu Di <liudidi@gmail.com> - 1.9.0-1
- 更新到 1.9.0

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1.8.0-2
- 为 Magic 3.0 重建

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

