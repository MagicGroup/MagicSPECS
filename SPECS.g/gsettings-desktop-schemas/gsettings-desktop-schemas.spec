%global debug_package %{nil}

Name:           gsettings-desktop-schemas
Version:	3.18.1
Release:        3%{?dist}
Summary:        A collection of GSettings schemas
Summary(zh_CN.UTF-8): Gsettings 架构集合

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
# no homepage exists for this component
URL:            http://bugzilla.gnome.org/enter_bug.cgi?product=gsettings-desktop-schemas
#VCS: git:git://git.gnome.org/gsettings-desktop-schemas
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source:         http://download.gnome.org/sources/%{name}/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires: glib2-devel >= 2.31.0
BuildRequires: intltool
BuildRequires: gobject-introspection-devel

Requires: glib2 >= 2.31.0

%description
gsettings-desktop-schemas contains a collection of GSettings schemas for
settings shared by various components of a desktop.

%description -l zh_CN.UTF-8 
Gsettings 架构集合。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries
and header files for developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-schemas-compile --enable-introspection=yes
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
magic_rpm_clean.sh
%find_lang %{name} --with-gnome

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%postun
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi


%files -f %{name}.lang
%doc AUTHORS COPYING MAINTAINERS NEWS README
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/GConf/gsettings/gsettings-desktop-schemas.convert
%{_datadir}/GConf/gsettings/wm-schemas.convert
%{_libdir}/girepository-1.0/GDesktopEnums-3.0.typelib

%files devel
%doc HACKING
%{_includedir}/*
%{_datadir}/pkgconfig/*
%{_datadir}/gir-1.0/GDesktopEnums-3.0.gir


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 3.18.1-3
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.18.1-2
- 更新到 3.18.1

* Tue Dec 23 2014 Liu Di <liudidi@gmail.com> - 3.14.1-1
- 更新到 3.14.1

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 3.12.0-1
- 更新到 3.12.0

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Tue Jan 14 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Mon Dec 23 2013 Adam Williamson <awilliam@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Wed Oct 16 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-1
- Update to 3.9.91

* Wed Aug 21 2013 Richard Hughes <rhughes@redhat.com> - 3.9.90-1
- Update to 3.9.90

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.5-1
- Update to 3.9.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.3-1
- Update to 3.9.3

* Tue May 28 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.2-1
- Update to 3.9.2

* Tue May 14 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Thu Mar  7 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.90-1
- Update to 3.7.90

* Tue Feb 05 2013 Richard Hughes <rhughes@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.4-1
- Update to 3.7.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.3-1
- Update to 3.7.3

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Tue Nov 13 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Richard Hughes <hughsient@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 3.5.92-1
- Update to 3.5.92

* Thu Sep 06 2012 Richard Hughes <hughsient@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Wed Aug 22 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Wed Jul 18 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Wed Jun 06 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Fri May 18 2012 Richard Hughes <hughsient@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Mon Apr 16 2012 Richard Hughes <hughsient@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Mon Mar 19 2012 Richard Hughes <rhughes@redhat.com> 3.3.92-1
- Update to 3.3.92

* Wed Feb 22 2012 Bastien Nocera <bnocera@redhat.com> 3.3.90-1
- Update to 3.3.90

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.3.2-3
- Disable empty -debuginfo package.
- Fix minimum required glib2 version.

* Tue Nov 22 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-2
- Enable introspection
- Make the package archful, since we now install in libdir

* Tue Nov 22 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Mon Sep 26 2011 Bastien Nocera <bnocera@redhat.com> 3.2.0-1
- Update to 3.2.0

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> 3.0.1-1
- Update to 3.0.1

* Thu Apr  7 2011 Matthias Clasen <mclasen@redhat.com> 3.0.0-2
- Don't perform questionable migrations

* Mon Apr 04 2011 Bastien Nocera <bnocera@redhat.com> 3.0.0-1
- Update to 3.0.0

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> 2.91.92-1
- Update to 2.91.92

* Wed Mar 09 2011 Bastien Nocera <bnocera@redhat.com> 2.91.91-2
- Fix possible crasher when converting schemas

* Tue Mar 08 2011 Bastien Nocera <bnocera@redhat.com> 2.91.91-1
- Update to 2.91.91

* Thu Feb 24 2011 Colin Walters <walters@verbum.org> - 0.1.7-2
- Add patch from git to disable a11y by default; it makes
  gnome-shell totally unusable right now

* Mon Feb 21 2011 Bastien Nocera <bnocera@redhat.com> 0.1.7-1
- Update to 0.1.7

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.1.5-3
- Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.1.5-1
- Update to 0.1.5

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.1.4-1
- Update to 0.1.4

* Sat Jan  8 2011 Matthias Clasen <mclasen@redhat.com> - 0.1.3-1
- Update to 0.1.3

* Tue Nov 30 2010 Tomas Bzatek <tbzatek@redhat.com> - 0.1.2-1
- Update to 0.1.2

* Wed Nov 17 2010 Bastien Nocera <bnocera@redhat.com> 0.1.1-1
- Update to 0.1.1

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.0-1
- Update to 0.1.0

* Tue Aug 24 2010 Matthias Clasen <mclasen@redhat.com> - 0.0.1-1
- Update to 0.0.1

* Tue Aug  3 2010 Tomas Bzatek <tbzatek@redhat.com> - 0.0.1-1.git20100729
- Initial packaging
