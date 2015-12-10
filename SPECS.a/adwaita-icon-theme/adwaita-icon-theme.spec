Name:           adwaita-icon-theme
Version:        3.13.3
Release:        4%{?dist}
Summary:        Adwaita icon theme
Summary(zh_CN.UTF-8): Adwaita 图标主题

License:        LGPLv3+ or CC-BY-SA
URL:            http://www.gnome.org
Source0:        http://download.gnome.org/sources/adwaita-icon-theme/3.13/%{name}-%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  intltool
BuildRequires:  /usr/bin/gtk-update-icon-cache

# Replace adwaita-cursor-theme subpackage from gnome-themes-standard
Provides:       adwaita-cursor-theme = %{version}-%{release}
Obsoletes:      adwaita-cursor-theme < 3.13.1-2

%description
This package contains the Adwaita icon theme used by the GNOME desktop.

%description -l zh_CN.UTF-8
Adwaita 图标主题。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains the pkgconfig file for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
%make_install

touch $RPM_BUILD_ROOT%{_datadir}/icons/Adwaita/icon-theme.cache
magic_rpm_clean.sh

%post
touch --no-create %{_datadir}/icons/Adwaita &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/Adwaita &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/Adwaita &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/Adwaita &>/dev/null || :

%files
%doc COPYING*
%{_datadir}/icons/Adwaita/8x8/
%{_datadir}/icons/Adwaita/16x16/
%{_datadir}/icons/Adwaita/22x22/
%{_datadir}/icons/Adwaita/24x24/
%{_datadir}/icons/Adwaita/32x32/
%{_datadir}/icons/Adwaita/48x48/
%{_datadir}/icons/Adwaita/256x256/
%{_datadir}/icons/Adwaita/cursors/
%{_datadir}/icons/Adwaita/scalable/
%{_datadir}/icons/Adwaita/scalable-up-to-32/
%{_datadir}/icons/Adwaita/index.theme
%ghost %{_datadir}/icons/Adwaita/icon-theme.cache

%files devel
%{_datadir}/pkgconfig/adwaita-icon-theme.pc

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 3.13.3-4
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 3.13.3-3
- 为 Magic 3.0 重建

* Thu Jul 10 2014 Liu Di <liudidi@gmail.com> - 3.13.3-2
- 为 Magic 3.0 重建

* Thu Jun 26 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3-1
- Update to 3.13.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-1
- Update to 3.13.2

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-2
- Replace adwaita-cursor-theme subpackage from gnome-themes-standard

* Mon Apr 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-1
- Initial Fedora packaging
