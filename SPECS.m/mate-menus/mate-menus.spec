Name:	mate-menus
Version:	1.4.0
Release:	4%{?dist}
Summary:	Displays menus for MATE Desktop
License:	GPLv2+ and LGPLv2+
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz

BuildRequires:	dbus-glib-devel gobject-introspection-devel gtk2-devel libsoup-devel mate-common mate-doc-utils mate-conf-devel mate-corba-devel pygobject2-codegen python-gudev pygtk2-devel

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

%package devel
Summary: Development files for mate-menus
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development files for mate-menus

%prep
%setup -q


%build
NOCONFIGURE=1 ./autogen.sh
%configure --disable-static --enable-python --enable-introspection=yes
make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang %{name}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS COPYING README
%config(noreplace) %{_sysconfdir}/xdg/menus/mate-applications.menu
%config(noreplace) %{_sysconfdir}/xdg/menus/mate-settings.menu
%{_datadir}/mate-menus/
%{_datadir}/mate/desktop-directories/

%files libs
%{_libdir}/girepository-1.0/MateMenu-2.0.typelib
%{_libdir}/libmate-menu.so.2
%{_libdir}/libmate-menu.so.2.4.9
%{python_sitearch}/matemenu.so

%files devel
%{_datadir}/gir-1.0/MateMenu-2.0.gir
%{_libdir}/libmate-menu.so
%{_includedir}/mate-menus/
%{_libdir}/pkgconfig/libmate-menu.pc


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.0-4
- 为 Magic 3.0 重建

* Thu Aug 16 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Fix devel package requirements. Removed libs requirement.

* Thu Aug 16 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Fix directory ownership for mate-menus dir.

* Thu Jul 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build

