%define glib2_version 2.3.0
%define gtk3_version 2.99.0
%define desktop_file_utils_version 0.9

Name:           gucharmap
Version:        3.2.2
Release:        3%{?dist}
Summary:        Unicode character picker and font browser
Summary(zh_CN.UTF-8): Unicode 字符选择程序和字体浏览器

Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
License:        GPLv3+ and GFDL and MIT
# GPL for the source code, GFDL for the docs, MIT for Unicode data
URL:            http://live.gnome.org/Gucharmap
#VCS: git:git://git.gnome.org/gucharmap
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source:         http://download.gnome.org/sources/gucharmap/%{majorver}/gucharmap-%{version}.tar.xz

BuildRequires: gnome-doc-utils >= 0.3.2
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: gobject-introspection-devel
BuildRequires: GConf2-devel
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: scrollkeeper
BuildRequires: gettext
BuildRequires: intltool

%description
This program allows you to browse through all the available Unicode
characters and categories for the installed fonts, and to examine their
detailed properties. It is an easy way to find the character you might
only know by its Unicode name or code point.

%description -l zh_CN.UTF-8 
Unicode 字符选择程序和字体浏览器。

%package devel
Summary: Libraries and headers for libgucharmap
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: glib2-devel >= %{glib2_version}
Requires: gtk3-devel >= %{gtk3_version}
Requires: gucharmap = %{version}-%{release}

%description devel
The gucharmap-devel package contains header files and other resources
needed to use the libgucharmap library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n  %{name}-%{version}

%build
%configure --with-gtk=3.0 \
           --disable-gtk-immodules \
           --disable-scrollkeeper \
           --enable-introspection
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT RUN_QUERY_IMMODULES_TEST=false

rm $RPM_BUILD_ROOT/%{_libdir}/*.la

sed -i -e "s#Icon=gucharmap.png#Icon=/usr/share/icons/hicolor/48x48/apps/gucharmap.png#" \
  $RPM_BUILD_ROOT%{_datadir}/applications/gucharmap.desktop

desktop-file-install --vendor gnome --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  $RPM_BUILD_ROOT%{_datadir}/applications/*

magic_rpm_clean.sh
%find_lang gucharmap --with-gnome


%post
/sbin/ldconfig
update-desktop-database &> /dev/null || :
%gconf_schema_upgrade gucharmap
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%pre
%gconf_schema_prepare gucharmap

%preun
%gconf_schema_remove gucharmap

%files -f gucharmap.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/charmap
%{_bindir}/gucharmap
%{_bindir}/gnome-character-map
%{_libdir}/libgucharmap_2_90.so.*
%{_datadir}/applications/gnome-gucharmap.desktop
%{_sysconfdir}/gconf/schemas/gucharmap.schemas
%{_libdir}/girepository-1.0


%files devel
%{_includedir}/gucharmap-2.90
%{_libdir}/libgucharmap_2_90.so
%{_libdir}/pkgconfig/gucharmap-2.90.pc
%{_datadir}/gir-1.0


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.2.2-3
- 为 Magic 3.0 重建

* Fri Dec 09 2011 Liu Di <liudidi@gmail.com> - 3.2.2-2
- 为 Magic 3.0 重建

* Tue Nov 22 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.2-1
- Update to 3.2.2

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 3.0.1-2
- Update scriptlets

* Mon Apr 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Thu Feb 24 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.2-6
- Enable introspection

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.2-5
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.2-3
- Rebuild

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.2-2
- Rebuild

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.2-1
- Update to 2.33.2

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.2-0.2.gitc50414f
- Rebuild against new gtk

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.2-0.1.gitc50414f
- Git snapshot that builds against new gtk3

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.0-3
- Update license field to match changed license (#639133)

* Wed Oct  6 2010 Paul Howarth <paul@city-fan.org> - 2.33.0-2
- gtk2 dependencies become gtk3 dependencies

* Mon Oct  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.0-1
- Update to 2.33.0

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.91-1
- Update to 2.31.91

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.90-1
- Update to 2.31.90

* Mon Apr 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Thu Mar 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.92-1
- Update to 2.29.92

* Fri Dec  4 2009 Matthias Clasen <mclasen@redhat.com> - 2.29.1-1
- Update to 2.29.1

* Mon Oct 19 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.3.1-2
- Fix some stubborn button images

* Sun Jul 12 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.3.1-1
- Update to 2.26.3.1

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Thu Jan 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.24.3-1
- Update to 2.24.3

* Mon Oct 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Wed Oct  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Save some space

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Mon Aug  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Tue Jul 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.23.4-2
- fix license tag

* Tue Jun 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Sun Mar  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Wed Jan 30 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Tue Jan 15 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.5-1
- Update to 2.21.5

* Tue Dec 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Thu Dec  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.3-1
- Update to 2.21.3

* Tue Sep 18 2007 Matthias Clasen <mclasen@redhat.com> - 1.10.1-1
- Update to 1.10.1

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 1.10.0-2
- Update license field
- Use %%find_lang for help files

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 1.8.0-1
- Update to 1.8.0
- Require pgkconfig for the -devel package

* Thu Aug 02 2006 Matthias Clasen <mclasen@redhat.com> 
- Rebuild 

* Wed Aug 02 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.7.0-1
- Update to 1.7.0

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.6.0-8.1
- rebuild

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-8
- Add missing BuildRequires

* Fri Jun  2 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-7
- Rebuild

* Tue Apr 18 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-6
- Make -devel require the exact n-v-r

* Tue Apr 18 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-5
- incorporate more package review feedback

* Mon Apr 17 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-4
- split off a -devel package

* Mon Apr 17 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-3
- fix issues pointed out in package review

* Tue Apr 11 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-2
- Initial revision
