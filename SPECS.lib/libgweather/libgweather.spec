Name:           libgweather
Version:	3.18.1
Release:        2%{?dist}
Summary:        A library for weather information
Summary(zh_CN.UTF-8): 天气信息库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2+
URL:            http://www.gnome.org
#VCS: git:git://git.gnome.org/libgweather
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.gnome.org/sources/libgweather/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires:  dbus-devel
BuildRequires:  glade-devel
BuildRequires:  gtk3-devel >= 2.90.0
BuildRequires:  gtk-doc
BuildRequires:  libsoup-devel >= 2.4
BuildRequires:  libxml2-devel >= 2.6
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  autoconf automake libtool
BuildRequires:  gobject-introspection-devel >= 0.10
BuildRequires:  gnome-common
BuildRequires:  vala-devel
BuildRequires:  vala-tools

# for directories
Requires: gnome-icon-theme

%description
libgweather is a library to access weather information from online
services for numerous locations.

%description -l zh_CN.UTF-8
这是一个可以从网上获得很多地点天气信息的库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static --disable-gtk-doc
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang %{name} --all-name

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/gnome &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/gnome &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -q %{_datadir}/icons/gnome &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%files -f %{name}.lang
%doc COPYING
%{_libdir}/libgweather-3.so.*
%{_libdir}/girepository-1.0/GWeather-3.0.typelib
%dir %{_datadir}/libgweather
%{_datadir}/libgweather/Locations.xml
%{_datadir}/libgweather/locations.dtd
#%{_datadir}/icons/gnome/*/status/*
%{_datadir}/glib-2.0/schemas/org.gnome.GWeather.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.GWeather.gschema.xml

%files devel
%{_includedir}/libgweather-3.0
%{_libdir}/libgweather-3.so
%{_libdir}/pkgconfig/gweather-3.0.pc
%{_datadir}/gir-1.0/GWeather-3.0.gir
%dir %{_datadir}/glade/
%dir %{_datadir}/glade/catalogs/
%{_datadir}/glade/catalogs/libgweather.xml
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/libgweather-3.0
%dir %{_datadir}/vala/
%dir %{_datadir}/vala/vapi/
%{_datadir}/vala/vapi/gweather-3.0.vapi


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 3.18.1-2
- 更新到 3.18.1

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 3.13.3-1
- 更新到 3.13.3

* Thu Apr 10 2014 Liu Di <liudidi@gmail.com> - 3.12.0-1
- 更新到 3.12.0

* Thu Apr 10 2014 Liu Di <liudidi@gmail.com> - 3.11.90-1
- 更新到 3.12.0

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Mon Feb 03 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Tue Jan 14 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Wed Jan 08 2014 Richard Hughes <rhughes@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92

* Wed Sep 04 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-1
- Update to 3.9.91
- Install the glade catalog
- Enable vala support

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Mon Aug 05 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.9.5-1
- Update to 3.9.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.3-2
- Tighten the -devel subpackage deps

* Thu Jun 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.3-1
- Update to 3.9.3

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.2-1
- Update to 3.9.2

* Sat May 04 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.1-1
- Update to 3.9.1
- Remove old gnome-applets-devel obsoletes

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Thu Mar  7 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.5-1
- Update to 3.7.5

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.3-1
- Update to 3.7.3

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Tue Nov 13 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.2-1
- Update to 3.6.2

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.92-2
- Silence glib-compile-schemas scriplets

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 3.5.92-1
- Update to 3.5.92

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.1-1
- Update to 3.5.1

* Thu Jan 12 2012 Matthias Clasen <mclasen@redhat.com> - 3.2.1-2
- Drop gtk-doc dependency

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Mon Apr  4 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-3
- Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Bastien Nocera <bnocera@redhat.com> 2.91.6-1
- Update to 2.91.6

* Sun Jan 30 2011 Matthew Barnes <mbarnes@redhat.com> - 2.91.0-1
- Update to 2.91.0

* Thu Sep 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.3-1
- Update to 2.30.3

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Tue Mar 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-1
- Update to 2.29.92

* Tue Feb 23 2010 Matthias Clasen <mclasen@redhat.com> 2.29.91-1
- Update to 2.29.91

* Wed Feb 10 2010 Bastien Nocera <bnocera@redhat.com> 2.29.90-1
- Update to 2.29.90

* Tue Jan 12 2010 Matthias Clasen <mclasen@redhat.com> 2.29.5-1
- Update to 2.29.5

* Tue Dec 22 2009 Matthias Clasen <mclasen@redhat.com> 2.29.4-1
- Update to 2.29.4

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-1
- Update to 2.28.0

* Wed Sep  9 2009 Matthias Clasen <mclasen@redhat.com> 2.27.92-1
- Update to 2.27.92

* Tue Aug 25 2009 Matthias Clasen <mclasen@redhat.com> 2.27.91-1
- Update to 2.27.91

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Matthias Clasen <mclasen@redhat.com> 2.26.1-5
- Keep locations in gettext catalogs

* Wed Jun 10 2009 Matthias Clasen <mclasen@redhat.com> 2.26.1-3
- Fix multilib parallel-installability (#477672)
- Remove some old optimizations that are now no-ops

* Mon Apr 27 2009 Matthias Clasen <mclasen@redhat.com> 2.26.1-2
- Don't drop schemas translations from po files

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/libgweather/2.26/libgweather-2.26.1.news

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> 2.26.0-1
- Update to 2.26.0

* Tue Mar  3 2009 Matthias Clasen <mclasen@redhat.com> 2.25.92-1
- Update to 2.25.92

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> 2.25.91-1
- Update to 2.25.91

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> 2.25.5-1
- Upate to 2.25.5

* Mon Jan 05 2009 Matthew Barnes <mbarnes@redhat.com> 2.25.4-1
- Update to 2.25.4

* Tue Dec 16 2008 Matthias Clasen <mclasen@redhat.com> 2.25.3-2
- Update to 2.25.3

* Wed Dec  3 2008 Matthias Clasen <mclasen@redhat.com> 2.25.2-2
- Update to 2.25.2

* Wed Oct 22 2008 Matthias Clasen <mclasen@redhat.com> 2.24.1-1
- Update to 2.24.1

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> 2.24.0-2
- Apply %%lang tags to localized xml files

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> 2.24.0-1
- Update to 2.24.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> 2.23.92-1
- Update to 2.23.92

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> 2.23.91-1
- Update to 2.23.91

* Mon Aug  4 2008 Matthias Clasen <mclasen@redhat.com> 2.23.6-1
- Update to 2.23.6

* Fri Jul 25 2008 Matthias Clasen <mclasen@redhat.com> 2.23.5-2
- Fix pending request accounting

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> 2.23.5-1
- Update to 2.23.5

* Tue Jun 17 2008 Matthias Clasen <mclasen@redhat.com> 2.23.4-1
- Update to 2.23.4

* Wed Jun  4 2008 Matthias Clasen <mclasen@redhat.com> 2.23.3-1
- Update to 2.23.3

* Wed May 14 2008 Matthias Clasen <mclasen@redhat.com> 2.23.2-1
- Update to 2.23.2

* Thu Apr 24 2008 Matthias Clasen <mclasen@redhat.com> 2.23.1-1
- Update to 2.23.1

* Thu Apr 17 2008 Matthias Clasen <mclasen@redhat.com> 2.22.1.1-2
- Leave Cairo in Africa (#442793)

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> 2.22.1.1-1
- Update to 2.22.1.1

* Tue Mar 11 2008 Matthias Clasen <mclasen@redhat.com> 2.22.0-1
- Update to 2.22.0

* Tue Feb 26 2008 Matthias Clasen <mclasen@redhat.com> 2.21.92-1
- Update to 2.21.92

* Mon Feb 11 2008  Matthias Clasen <mclasen@redhat.com> 2.21.2-6
- Remove obsolete translations

* Sat Feb  9 2008  Matthias Clasen <mclasen@redhat.com> 2.21.2-5
- Rebuild for gcc 4.3

* Wed Jan 16 2008  Matthias Clasen <mclasen@redhat.com> 2.21.2-4
- Add Obsoletes for gnome-applets-devel

* Wed Jan 16 2008  Matthias Clasen <mclasen@redhat.com> 2.21.2-3
- Carry over space-saving hack from gnome-applets

* Tue Jan 15 2008  Matthias Clasen <mclasen@redhat.com> 2.21.2-2
- Incorporate review feedback (#428739)

* Mon Jan 14 2008  Matthias Clasen <mclasen@redhat.com> 2.21.2-1
- Update to 2.21.2

* Thu Jan 10 2008  Matthias Clasen <mclasen@redhat.com> 2.21.1-1
- Initial packaging

