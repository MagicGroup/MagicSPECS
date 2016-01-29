%global xfceversion 4.10

Name:           libxfcegui4
Version:        4.10.0
Release:        5%{?dist}
Summary:        GTK widgets for Xfce

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.xfce.org/
#VCS git:git://git.xfce.org/xfce/libxfcegui4
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{xfceversion}/%{name}-%{version}.tar.bz2
Patch1:         libxfcegui4-4.10.0-fix-xfce_setenv.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  pkgconfig(gtk+-2.0) >= 2.10.0
BuildRequires:  pkgconfig(libxfce4util-1.0) >= %{xfceversion}
BuildRequires:  pkgconfig(libstartup-notification-1.0) >= 0.5
BuildRequires:  pkgconfig(libglade-2.0) >= 2.0.0
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  gtk-doc
BuildRequires:  libSM-devel
%if 0%{?fedora}
Requires:       gnome-icon-theme-legacy
%endif
%if 0%{?rhel}
Requires:       gnome-icon-theme
%endif

%description
The package includes various gtk widgets for Xfce.

%package devel
Summary:        Development tools for libxfcegui4 library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gtk2-devel
Requires:       libxfce4util-devel
Requires:       pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch1 -p1


%build
%configure --enable-gtk-doc --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# The LD_LIBRARY_PATH hack is needed for --enable-gtk-doc
# because lt-libxfce4ui-scan is linked against libxfce4ui
export LD_LIBRARY_PATH=$( pwd )/%{name}/.libs

make %{?_smp_mflags} V=1


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL='install -p'
find %{buildroot} -name '*.la' -exec rm -f {} ';'
%find_lang %{name}


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING COPYING.LIB NEWS README
%{_libdir}/lib*.so.*
%{_libdir}/libglade/*/lib*.so
%{_datadir}/icons/hicolor/*/*/*

%files devel
%defattr(-, root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/xfce4/*
%doc %{_datadir}/gtk-doc
#glade3
%{_libdir}/glade3/modules/libgladexfce4.so
%{_datadir}/glade3/catalogs/*
%{_datadir}/glade3/pixmaps/hicolor/*x*/actions/widget-xfce4-xfce-*.png

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 4.10.0-5
- 为 Magic 3.0 重建

* Thu Jan 17 2013 Liu Di <liudidi@gmail.com> - 4.10.0-4
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 29 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-2
- Fix Dependencies

* Sat Apr 28 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-1
- Update to 4.10.0 final
- Make build verbose
- Add VCS key
- Drop Xfce 4.10 patch (upstreamed) and Thunar patch (obsolete)
- Drop obsolete Xinerama support
- Build GTK documentation

* Wed Apr 04 2012 Kevin Fenzi <kevin@scrye.com> - 4.8.1-6
- Add patch and rebuild for Xfce 4.10

* Fri Jan 20 2012 Kevin Fenzi <kevin@scrye.com> - 4.8.1-5
- Remove glade3 support. It's gtk3 only and this library shouldn't be used for new projects anyhow.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 4.8.1-3
- Rebuild for new libpng

* Thu May 19 2011 Orion Poplawski <orion@cora.nwra.com> - 4.8.1-2
- Require gnome-icon-theme on EL

* Thu Feb 10 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.1-1
- Update to 4.8.1
- Add COPYING.LIB, NEWS and README to %%doc

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-1
- Update to 4.8.0

* Mon Nov 08 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.0-1
- Update to 4.7.0

* Sun Nov 07 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.4-3
- Require gnome-icon-theme-legacy (fixes #647734 and #650504)

* Mon Aug 23 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.4-2
- Remove unneeded gtk-doc dep. Fixes bug #604401

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.4-1
- Update to 4.6.4

* Wed May 19 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.3-2
- Rebuild for new glade version. 

* Wed Jan 21 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.3-1
- Update to 4.6.3

* Tue Jan 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.2-1
- Update to 4.6.2
- Drop upstreamed patches
- Update BuildRoot tag and Sourc0 URL

* Mon Nov 02 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.1-3
- Fix SEGV inside disconnect() helper (#532179)
- Update gtk-icon-cache scriptlets

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 19 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.1-1
- Update to 4.6.1

* Mon Mar 02 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.0-3
- Patch to bring back missing keyboard shortcuts from Xfce 4.4
- Make devel package require glade3-libgladeui-devel, pkgconfig and gtk-doc
- Mark gtk-doc files as %%doc

* Fri Feb 27 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-2
- Add back in libSM-devel to BuildRequires

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-1
- Update to 4.6.0
- Remove some unneeded BuildRequires

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.99.1-1
- Update to 4.5.99.1

* Tue Jan 13 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.93-1
- Update to 4.5.93

* Sun Dec 21 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-1
- Update to 4.5.92

* Mon Oct 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 4.4.3-1
- Update to 4.4.3

* Fri Oct 03 2008 Christoph Wickert <cwickert@fedoraproject.org> - 4.4.2-3
- Make xfce-exec use Thunar

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-2
- Rebuild for gcc43

* Sun Nov 18 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.2-1
- Update to 4.4.2

* Sun Aug 26 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-3
- Update License tag

* Mon Apr 16 2007 Christoph Wickert <fedora@christoph-wickert.de> - 4.4.1-2
- Drop BuildRequires dbh-devel and intltool

* Wed Apr 11 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-1
- Upgrade to 4.4.1

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-1
- Upgrade to 4.4.0
- Add in new icons

* Thu Nov  9 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.2-1
- Upgrade to 4.3.99.2

* Thu Oct  5 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-3
- Fix defattr

* Wed Oct  4 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-2
- Bump release for devel build

* Sun Sep  3 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-1
- Upgrade to 4.3.99.1
- Add doc files
- Remove useless Prereq
- Remove useless Provides: libxfcegui4-devel

* Sun Aug 27 2006 <kevin@tummy.com> - 4.2.3-6
- fix .so included in main package instead of devel. (#203629)

* Mon Jun  5 2006  <kevin@tummy.com> - 4.2.3-5
- Add gettext and intltool BuildRequires (fixes #194138)

* Thu Feb 16 2006 Kevin Fenzi <kevin@tummy.com> - 4.2.3-4.fc5
- Rebuild for fc5

* Sun Jan 29 2006 Kevin Fenzi <kevin@scrye.com> - 4.2.3-3.fc5
- Add BuildRequires for modular xorg

* Thu Nov 10 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3-2.fc4
- disable-static instead of removing .a files

* Mon Nov  7 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3-1.fc4
- Update to 4.2.3
- Added dist tag
- Removed .la files. Fixes bug 172646
- Removed .a files. 

* Tue May 17 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.2-1.fc4
- Update to 4.2.2

* Fri Mar 25 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-4.fc4
- lowercase Release 

* Sat Mar 19 2005 Warren Togami <wtogami@redhat.com> - 4.2.1-3
- remove stuff, remove version from dbh-devel buildreq

* Wed Mar 16 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-2
- Fixed %%files bug that wasn't packaging .so files

* Tue Mar 15 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-1
- Updated to 4.2.1 version

* Tue Mar  8 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-3
- Fixed Xfce case

* Sun Mar  6 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-2
- Capitalized first letter of Summary in devel section to quiet rpmlint
- Added dbh-devel to BuildRequires
- Capitalized the GTK in the Summary to queit rpmlint
- Moved all the module *.a and *.la libraries to the devel package
- Added Provides: libxfcegui4-devel to devel package

* Sun Jan 23 2005 Than Ngo <than@redhat.com> 4.2.0-1
- update to 4.2.0

* Wed Dec 08 2004 Than Ngo <than@redhat.com> 4.1.99.1-1
- update to 4.2 rc1

* Mon Jul 19 2004 Than Ngo <than@redhat.com> 4.0.6-1
- update to 4.0.6

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr 15 2004 Than Ngo <than@redhat.com> 4.0.5-1
- update to 4.0.5

* Thu Mar 11 2004 Than Ngo <than@redhat.com> 4.0.3-4
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Than Ngo <than@redhat.com> 4.0.3-2
- fixed dependant libraries check on x86_64

* Fri Jan 09 2004 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3 release

* Thu Dec 25 2003 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2 release

* Tue Dec 16 2003 Than Ngo <than@redhat.com> 4.0.1-1
- initial build
