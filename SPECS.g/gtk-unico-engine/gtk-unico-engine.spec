%global engine_name unico
%global revision 152
%global revision_date 20140109

Name:           gtk-unico-engine
Version:        1.0.3
Release:        0.5.%{revision_date}bzr%{revision}%{?dist}
Summary:        Unico Gtk+ theming engine
Summary(zh_CN.UTF-8): Unico Gtk+ 主题引擎

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        LGPLv2
URL:            https://launchpad.net/unico/
# The source for this package was pulled from upstream's VCS. Use the following
# commands to generate the tarball:
# $ bzr export -r %%{revision} %%{engine_name}-%%{version}-bzr%%{revision}.tar.xz lp:unico
Source0:        %{engine_name}-%{version}-bzr%{revision}.tar.xz

BuildRequires:  gnome-common
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)

%description
Unico is a Gtk+ engine that aims to be the more complete yet powerful theming
engine for Gtk+ 3.0 and newer. It’s the first Gtk+ engine written with Gtk+
style context APIs in mind, using CSS as first class citizen.

%description -l zh_CN.UTF-8
Unico Gtk+ 主题引擎。

%prep
%setup -q -n %{engine_name}-%{version}-bzr%{revision}


%build
[ -f autogen.sh ] && NOCONFIGURE=1 ./autogen.sh
%configure \
  --disable-silent-rules \
  --disable-static
make %{?_smp_mflags}


%install
%make_install

rm $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/3.0.0/theming-engines/*.la
magic_rpm_clean.sh

%files
# TODO: add ChangeLog and README if non-empty
%doc AUTHORS COPYING NEWS
%{_libdir}/gtk-3.0/3.0.0/theming-engines/lib%{engine_name}.so


%changelog
* Mon Aug 11 2014 Liu Di <liudidi@gmail.com> - 1.0.3-0.5.20140109bzr152
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.4.20140109bzr152
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.0.3-0.3.20140109bzr152
- Update to a newer bzr snapshot (sync with Ubuntu 14.04)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.2.20121212bzr146
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Apr 07 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.0.3-0.1.20121212bzr146
- Update to a newer bzr snapshot

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3.20120808bzr139
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 21 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.0.2-1.20120808bzr139
- Update to a newer bzr snapshot

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 30 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Thu Mar 22 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.0.1-5.20120229bzr132
- Update to a newer bzr snapshot

* Fri Feb 24 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.0.1-4.20120224bzr130
- Update to a newer bzr snapshot

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 03 2011 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.0.1-2
- Remove useless IM scriptlets

* Thu Sep 29 2011 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.0.1-1
- Initial RPM release
