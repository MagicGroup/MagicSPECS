Summary: Symbolic GNOME icons
Name: gnome-icon-theme-symbolic
Version: 3.8.0.1
Release: 1%{?dist}
#VCS: git:git://git.gnome.org/gnome-icon-theme-symbolic
Source0: http://download.gnome.org/sources/gnome-icon-theme-symbolic/3.8/%{name}-%{version}.tar.xz
License: CC-BY-SA
BuildArch: noarch
Group: User Interface/Desktops
BuildRequires: icon-naming-utils >= 0.8.7
Requires: gnome-icon-theme >= 2.30.2.1-2

%description
This package contains symbolic icons for use by the GNOME desktop.

%prep
%setup -q

%build
# Avoid a BuildRequires on gtk2-devel
export ac_cv_path_GTK_UPDATE_ICON_CACHE=/bin/true

%configure

%install
make install DESTDIR=$RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/gnome &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/gnome &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :

%files
%doc COPYING AUTHORS
%{_datadir}/icons/gnome/*
%{_datadir}/pkgconfig/gnome-icon-theme-symbolic.pc

%changelog
* Wed Mar 27 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0.1-1
- Update to 3.8.0.1

* Tue Mar 26 2013 Richard Hughes <rhughes@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Wed Mar  6 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.5-1
- Update to 3.7.5

* Thu Jan 17 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.4.1-1
- Update to 3.7.4.1

* Wed Nov 14 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.2-1
- Update to 3.6.2

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Tue Aug 28 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.91.1-1
- Update to 3.3.91.1

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.91-1
- Update to 3.3.91

* Mon Jan 16 2012 Matthias Clasen <mclasen@redhat.com> - 3.2.2-1
- Update to 3.2.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-2
- Update icon cache scriptlet

* Tue Apr  5 2011 Christopher Aillon <caillon@redhat.com> 3.0.0-1
- Update to 3.0.0

* Tue Mar 29 2011 Matthias Clasen <mclasen@redhat.com> 2.91.93-1
- Update to 2.91.93

* Tue Mar 22 2011 Christopher Aillon <caillon@redhat.com> 2.91.92-1
- Update to 2.91.92

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.7-1
- Update to 2.91.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Christopher Aillon <caillon@redhat.com> - 2.91.6-1
- Update to 2.91.6

* Wed Aug 18 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.0-1
- Update to 2.31.0

* Fri May 21 2010 Bastien Nocera <bnocera@redhat.com> 2.30.0-3
- Require gnome-icon-theme-2.30.2.1-2 so that we have scalable
  directories

* Fri Apr 30 2010 Bastien Nocera <bnocera@redhat.com> 2.30.0-2
- Updated for review comments

* Thu Apr 29 2010 Bastien Nocera <bnocera@redhat.com> 2.30.0-1
- First build

