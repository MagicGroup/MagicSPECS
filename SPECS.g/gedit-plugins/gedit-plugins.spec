%global __python %{__python3}

Name:           gedit-plugins
Version:	3.12.0
Release:        1%{?dist}
Summary:        Plugins for gedit
Summary(zh_CN.UTF-8): gedit 的插件

Group:          Applications/Editors
Group(zh_CN.UTF-8): 应用程序/编辑器
License:        GPLv2+
URL:            http://live.gnome.org/GeditPlugins
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        ftp://ftp.gnome.org/pub/gnome/sources/gedit-plugins/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires:  gedit-devel
BuildRequires:  gnome-doc-utils
BuildRequires:  perl(XML::Parser)
BuildRequires:  gettext
BuildRequires:  cairo-devel
BuildRequires:  atk-devel
BuildRequires:  python3-devel
BuildRequires:  pygobject3-devel
BuildRequires:  python3-gobject
BuildRequires:  intltool
BuildRequires:  libpeas-devel
BuildRequires:  dbus-python-devel
BuildRequires:  vte3-devel
Requires:       gedit
Requires:       python3-gobject >= %{pygo_version}
# these are needed for gobject-introspection
Requires:       vte3 >= 0.27.90-2.fc15
Requires:       gucharmap >= 2.33.2-6.fc15

%description
A collection of plugins for gedit.

%description -l zh_CN.UTF-8
gedit 的插件集合。

%prep
%setup -q

%build
%configure --disable-schemas-install --enable-python
#--with-plugins=bracketcompletion,charmap,codecomment,colorpicker,drawspaces,joinlines,showtabbar,smartspaces,terminal,bookmarks
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh
%find_lang %{name}
find $RPM_BUILD_ROOT/%{_libdir}/gedit/plugins -name "*.la" -exec rm {} \;
rm -rf `ls %{buildroot}%{_datadir}/help/* |egrep -v '(C|zh_*)'`

%postun
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi


%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%check
[ -f ${RPM_BUILD_ROOT}%{_libdir}/gedit/plugins/terminal.py ]


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README NEWS AUTHORS COPYING
%{_libdir}/gedit/plugins/*
%{_datadir}/gedit/plugins/*
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.drawspaces.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.terminal.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.wordcompletion.gschema.xml
%{_datadir}/help/*

%changelog
* Sun Apr 06 2014 Liu Di <liudidi@gmail.com> - 3.12.0-1
- 更新到 3.12.0

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-2
- Rebuilt for gtksourceview3 soname bump

* Mon Mar 25 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 3.8.0-1
- Update to 3.8.0

* Sun Jan 27 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 3.7.1-1
- Update to 3.7.1

* Tue Oct 16 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 3.6.1-1
- Update to 3.6.1

* Mon Sep 24 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 3.5.2-1
- Update to 3.5.2

* Sat Aug 18 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 3.5.1-1
- Update to 3.5.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0-2
- Silence rpm scriptlet output

* Mon Mar 26 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 07 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 3.3.4-1
- Update to 3.3.4

* Sat Feb 25 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 3.3.3-1
- Update to 3.3.3

* Tue Feb 07 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 3.3.2-1
- Update to 3.3.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 03 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.3.1-1
- Update to 3.3.1

* Sun Oct 16 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.2.1-1
- Update to 3.2.1

* Mon Sep 26 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.2.0-1
- Update to 3.2.0
- Bump pygobject to 3.0

* Thu Sep 20 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.1.5-1
- Update to 3.1.5

* Thu Sep 06 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.1.4-1
- Update to 3.1.4

* Thu Sep 01 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.1.3-1
- Update to 3.1.3

* Tue Jul 05 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.1.2-1
- Update to 3.1.2

* Thu Jun 16 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Wed May 18 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.0.2-2
- Remove useless deps

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Wed Apr 13 2011 Christopher Aillon <caillon@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Wed Apr  6 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Sun Mar 27 2011 Christopher Aillon <caillon@redhat.com> - 2.91.3-1
- Update to 2.91.3

* Tue Mar  8 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.1-1
- Update to 2.91.1

* Mon Feb 28 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-3
- Rebuild against newer libpeas

* Thu Feb 24 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-2
- Add runtime dependencies to make introspection work

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.31.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct  7 2010 Matthias Clasen <mclasen@redhat.com> 2.31.6-1
- Rebuild against newer gucharmap

* Thu Sep 02 2010 Rakesh Pandit <rakesh@fedoraproject.org> 2.31.6-1
- Updated to 2.31.6
- FTBFS 599912

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 2.31.1-2
- recompiling .py files against Python 2.7 (rhbz#623308)

* Wed May 19 2010 Rakesh Pandit <rakesh@fedoraproject.org> 2.31.1-1
- Updated to 2.31.1

* Fri Apr 23 2010 Rakesh Pandit <rakesh@fedoraproject.org> 2.30.0-1
- Updated to 2.30.0

* Wed Jan 27 2010 Rakesh Pandit <rakesh@fedoraproject.org> 2.29.4-1
- Updated to 2.29.4

* Wed Dec 02 2009 Rakesh Pandit <rakesh@fedoraproject.org> 2.29.3-1
- Updated to 2.29.3

* Mon Nov 09 2009 Rakesh Pandit <rakesh@fedoraproject.org> 2.28.0-1
- Updated to 2.28.0

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.26.1-3
- Use bzipped upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 11 2009 Dodji Seketeli <dodji@redhat.org> - 2.26.1-1
- Update to upstream release 2..26.1
- Fixes GNOME bugzilla bug #576766 - Crash when Configuring "Draw Spaces"
- Make sure to remove all *.la files
- Remove BuildRequire libgnomeui-devel as needless now

* Fri Apr 10 2009 Dodji Seketeli <dodji@redhat.org> - 2.26.0-1
- Update to upstream release (2.26.1)
- Add plugin files from %%{_datadir}
- Don't check for vte anymore, the package checks it pkg-config
- Add 'bookmarks' to the plugin set

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.22.3-3
- Rebuild for Python 2.6

* Mon Sep 29 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 2.22.3-2
- Fixed buildrequires

* Mon Sep 29 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 2.22.3-1
- Updated to 2.22.3

* Mon Sep 29 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 2.22.0-2
- rebuild to pick latest gucharmap

* Tue Mar 18 2008 Trond Danielsen <trond.danielsen@gmail.com> - 2.22.0-1
- Updated.

* Mon Apr 30 2007 Trond Danielsen <trond.danielsen@gmail.com> - 2.18.0-2
- Disable buggy session saver plugin.
- Removed static libraries.

* Sun Apr 01 2007 Trond Danielsen <trond.danielsen@gmail.com> - 2.18.0-1
- Initial version.
