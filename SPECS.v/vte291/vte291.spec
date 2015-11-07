%global apiver 2.91

Name:           vte291
Version:	0.43.0
Release:        2%{?dist}
Summary:        Terminal emulator library
Summary(zh_CN.UTF-8): 终端模拟器库

License:        LGPLv2+
URL:            http://www.gnome.org/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.gnome.org/sources/vte/%{majorver}/vte-%{version}.tar.xz

BuildRequires:  gettext
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk3-devel
BuildRequires:  intltool
BuildRequires:  ncurses-devel
BuildRequires:  vala-tools

# initscripts creates the utmp group
Requires:       initscripts
Requires:       vte-profile

%description
VTE is a library implementing a terminal emulator widget for GTK+. VTE
is mainly used in gnome-terminal, but can also be used to embed a
console/terminal in games, editors, IDEs, etc.

VTE supports Unicode and character set conversion, as well as emulating
any terminal known to the system's terminfo database.

%description -l zh_CN.UTF-8
终端模拟器库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

# vte-profile is deliberately not noarch to avoid having to obsolete a noarch
# subpackage in the future when we get rid of the vte3 / vte291 split. Yum is
# notoriously bad when handling noarch obsoletes and insists on installing both
# of the multilib packages (i686 + x86_64) as the replacement.
%package -n     vte-profile
Summary:        Profile script for VTE terminal emulator library
Summary(zh_CN.UTF-8): VTE 的配置文件脚本
License:        GPLv3+
# vte.sh was previously part of the vte3 package
Conflicts:      vte3 < 0.36.1-3

%description -n vte-profile
The vte-profile package contains a profile.d script for the VTE terminal
emulator library.

%description -n vte-profile -l zh_CN.UTF-8
VTE 的配置文件脚本。

%prep
%setup -q -n vte-%{version}

%build
CFLAGS="%optflags -fPIE -DPIE" \
CXXFLAGS="$CFLAGS" \
LDFLAGS="$LDFLAGS -Wl,-z,relro -Wl,-z,now -pie" \
%configure \
        --disable-static \
        --with-gtk=3.0 \
        --libexecdir=%{_libdir}/vte-%{apiver} \
        --disable-gtk-doc \
        --enable-introspection
make %{?_smp_mflags} V=1

%install
%make_install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh
%find_lang vte-%{apiver}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f vte-%{apiver}.lang
%doc COPYING NEWS README
%{_libdir}/libvte-%{apiver}.so.0*
%{_libdir}/girepository-1.0/

%files devel
%{_bindir}/vte-%{apiver}
%{_includedir}/vte-%{apiver}/
%{_libdir}/libvte-%{apiver}.so
%{_libdir}/pkgconfig/vte-%{apiver}.pc
%{_datadir}/gir-1.0/
%doc %{_datadir}/gtk-doc/
%{_datadir}/vala/

%files -n vte-profile
%{_sysconfdir}/profile.d/vte.sh

%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 0.43.0-2
- 更新到 0.43.0

* Mon Oct 19 2015 Liu Di <liudidi@gmail.com> - 0.42.1-1
- 更新到 0.42.1

* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 0.42.0-1
- 更新到 0.42.0

* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 0.41.90-1
- 更新到 0.41.90

* Mon May 19 2014 Liu Di <liudidi@gmail.com> - 0.37.0-3
- 为 Magic 3.0 重建

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.0-2
- Split out a vte-profile subpackage that can be used with both vte291 / vte3

* Tue May 06 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.0-1
- Initial Fedora package, based on previous vte3 0.36 packaging
