%define         clutter_version 1.0

Name:           clutter-gtk
Version:	1.6.6
Release:        3%{?dist}
Summary:        A basic GTK clutter widget
Summary(zh_CN.UTF-8): 基本的 GTK clutter 组件

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        LGPLv2+
URL:            http://www.clutter-project.org
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        https://download.gnome.org/sources/clutter-gtk/%{majorver}/%{name}-%{version}.tar.xz
Patch0:         clutter-gtk-fixdso.patch

BuildRequires:  gtk3-devel >= 3.0.0
BuildRequires:  clutter-devel >= 1.9
BuildRequires:  gobject-introspection-devel

%description
clutter-gtk is a library which allows the embedding of a Clutter
canvas (or "stage") into a GTK+ application, as well as embedding
GTK+ widgets inside the stage.

%description -l zh_CN.UTF-8
基本的 GTK clutter 组件。

%package devel
Summary:        Clutter-gtk development environment
Summary(zh_CN.UTF-8): %{name} 的开发包
Group(zh_CN.UTF-8): 开发/库
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gtk3-devel clutter-devel

%description devel
Header files and libraries for building a extension library for the
clutter-gtk.

%description devel -l zh_CN.UTF-8 
%{name} 的开发包。

%prep
%setup -q


%build
%configure
make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%find_lang cluttergtk-1.0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f cluttergtk-1.0.lang
%doc COPYING NEWS
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/GtkClutter-%{clutter_version}.typelib

%files devel
%{_includedir}/clutter-gtk-%{clutter_version}/
%{_libdir}/pkgconfig/clutter-gtk-%{clutter_version}.pc
%{_libdir}/*.so
%{_datadir}/gir-1.0/GtkClutter-%{clutter_version}.gir
%{_datadir}/gtk-doc/html/clutter-gtk-1.0

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.6.6-3
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.6.6-2
- 更新到 1.6.6

* Wed Mar 12 2014 Liu Di <liudidi@gmail.com> - 1.5.2-1
- 更新到 1.5.2

* Wed Mar 12 2014 Liu Di <liudidi@gmail.com> - 1.5.0-1
- 更新到 1.5.2

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 1.4.4-1
- Update to 1.4.4

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 1.4.2-3
- Rebuilt for cogl soname bump

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.2-2
- Rebuild for new cogl

* Tue Dec 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.2-1
- New 1.4.2 stable release

* Fri Oct 19 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.0-1
- New 1.4.0 stable release

* Fri Aug 17 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3.2-3
- Rebuild for new cogl

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Tue Apr  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Sat Mar 10 2012 Matthias Clasen <mclasen@redhat.com> - 1.1.2-5
- Rebuild against new cogl

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 1.1.2-4
- Rebuild against new cogl

* Thu Jan 19 2012 Matthias Clasen <mclasen@redhat.com> - 1.1.2-3
- Rebuild against new cogl

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 24 2011 Matthias Clasen <mclasen@redhat.com> - 1.1.2-1
- Update to 1.1.2

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 1.0.4-1
- Update to 1.0.4

* Tue Sep 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.2-4
- Rebuild for clutter 1.8.0 again

* Tue Sep 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.2-3
- Rebuild for clutter 1.8.0

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> 1.0.2-2
- Rebuild

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> 1.0.2-1
- Update to 1.0.2

* Tue Apr  5 2011 Matthias Clasen <mclasen@redhat.com> 1.0.0-1
- Update to 1.0.0

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 0.91.8-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 0.91.8-2
- Rebuild against newer gtk

* Fri Jan 14 2011 Matthias Clasen <mclasen@redhat.com> 0.91.8-1
- Update to 0.91.8

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> 0.91.6-2
- Rebuild against GTK+ 2.99.0

* Tue Dec 28 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.91.6-1
- Update to 0.91.6
- Fix deps and other bits of spec file

* Wed Dec 22 2010 Dan Horák <dan[at]danny.cz> - 0.91.4-2
- Update to recent gtk (FTBFS)

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 0.91.4-1
- Update to 0.91.4

* Sun Oct 10 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.91.2-1
- Update to 0.91.2

* Wed Sep 29 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.90.2-3
- Add upstream patches to compile with latest gobject-introspection

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> 0.90.2-2
- Rebuild against newer gobject-introspection

* Wed Sep  1 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.90.2-1
- Update to 0.90.2

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 0.10.4-5
- Rebuild with new gobject-introspection
- Drop gir-repository-devel

* Mon May  3 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.4-3
- cleanup removal of libtool archives

* Wed Mar 24 2010 Bastien Nocera <bnocera@redhat.com> 0.10.4-2
- Move the API docs to -devel

* Sun Mar 21 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.4-1
- Update to 0.10.4

* Wed Jul 29 2009 Bastien Nocera <bnocera@redhat.com> 0.10.2-1
- Update to 0.10.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Bastien Nocera <bnocera@redhat.com> 0.9.2-1
- Update to 0.9.2

* Sat Jun 20 2009 Bastien Nocera <bnocera@redhat.com> 0.9.0-2
- Rebuild for new clutter

* Tue May 26 2009 Bastien Nocera <bnocera@redhat.com> 0.9.0-1
- Update to 0.9.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild


* Fri Jan 23 2009 Allisson Azevedo <allisson@gmail.com> 0.8.2-2
- Rebuild

* Wed Oct 15 2008 Allisson Azevedo <allisson@gmail.com> 0.8.2-1
- Update to 0.8.2

* Sat Sep  6 2008 Allisson Azevedo <allisson@gmail.com> 0.8.1-1
- Update to 0.8.1

* Thu Jun 26 2008 Colin Walters <walters@redhat.com> 0.6.1-1
- Update to 0.6.1 so we can make tweet go
- Loosen files globs so we don't have to touch them every version

* Thu Feb 21 2008 Allisson Azevedo <allisson@gmail.com> 0.6.0-1
- Update to 0.6.0

* Mon Sep  3 2007 Allisson Azevedo <allisson@gmail.com> 0.4.0-1
- Update to 0.4.0

* Thu May 10 2007 Allisson Azevedo <allisson@gmail.com> 0.1.0-3
- fix devel files section

* Thu May 10 2007 Allisson Azevedo <allisson@gmail.com> 0.1.0-2
- INSTALL removed from docs
- fix make install for keeping timestamps
- fix devel files section
- changed license for LGPL

* Fri Apr 13 2007 Allisson Azevedo <allisson@gmail.com> 0.1.0-1
- Initial RPM release
