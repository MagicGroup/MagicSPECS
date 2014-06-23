
Name:           libxfce4util
Version:	4.11.0
Release:        3%{?dist}
Summary:        Utility library for the Xfce4 desktop environment

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.xfce.org/
%global xfceversion %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{xfceversion}/%{name}-%{version}.tar.bz2
#VCS: git:git://git.xfce.org/xfce/libxfce4util
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  pkgconfig(glib-2.0) >= 2.24.0
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  gtk-doc

%description
This package includes basic utility non-GUI functions for Xfce4.

%package devel
Summary: Developpment tools for libxfce4util library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel
Requires: gtk2-devel
Requires: pkgconfig

%description devel
This package includes static libraries and header files for the
libxfce4util library.

%prep
%setup -q

%build
%configure --enable-gtk-doc --disable-static
# Remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# The LD_LIBRARY_PATH hack is needed for --enable-gtk-doc
# because lt-libxfce4util-scan is linked against libxfce4util
export LD_LIBRARY_PATH=$( pwd )/libxfce4util/.libs

make %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README README.Kiosk THANKS
%{_libdir}/lib*.so.*
%{_sbindir}/xfce4-kiosk-query

%files devel
%defattr(-, root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/xfce4
%doc %{_datadir}/gtk-doc/

%changelog
* Tue Jun 10 2014 Liu Di <liudidi@gmail.com> - 4.11.0-3
- 更新到 4.11.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.10.0-3
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-1
- Update to 4.10.0 final
- Make build verbose
- Add VCS key

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.1-1
- Update to 4.9.1 (Xfce 4.10pre2)

* Sun Apr 01 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.0-1
- Update to 4.9.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 12 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.2-1
- Update to 4.8.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.1-1
- Update to 4.8.1

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-1
- Update to 4.8.0 final 

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.5-1
- Update to 4.7.5

* Fri Dec 03 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.4-1
- Update to 4.7.4

* Sun Nov 07 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.3-1
- Update to 4.7.3

* Sun Sep 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.2-1
- Update to 4.7.2

* Mon Aug 23 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.2-2
- Remove unneeded gtk-doc dep. Fixes bug #604400

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.2-1
- Update to 4.6.2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 19 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.1-1
- Update to 4.6.1

* Mon Mar 02 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.0-2
- Make devel package require pkgconfig and gtk-doc
- Mark gtk-doc files as %%doc

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-1
- Update to 4.6.0

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

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-2
- Rebuild for gcc43

* Sun Dec  2 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.2-1
- Update to 4.4.2

* Sun Aug 26 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-3
- Update License tag

* Mon Apr 16 2007 Christoph Wickert <fedora@christoph-wickert.de> - 4.4.1-2
- BuildRequire gettext and include locales

* Wed Apr 11 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-1
- Update to 4.4.1

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-1
- Update to 4.4.0

* Thu Nov  9 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.2-1
- Update to 4.3.99.2

* Thu Oct  5 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-3
- Fix defattr

* Wed Oct  4 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-2
- Bump release for devel checkin

* Sun Sep  3 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-1
- Upgrade to 4.4rc1/4.3.99.1
- Remove unneeded PreReq
- Added doc files

* Sun Aug 27 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.2-2
- Make devel package own includedir/xfce4 (fixes #203644)

* Tue Jul 11 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.2-1
- Update to 4.3.90.2

* Thu Apr 27 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.1-1
- upgrade to 4.3.90.1

* Thu Feb 16 2006 Kevin Fenzi <kevin@tummy.com> - 4.2.3.2-2.fc5
- Rebuild for fc5

* Wed Nov 16 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3.2-1.fc5
- Update to 4.2.3.2

* Fri Nov 10 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3.1-4.fc5
- bump release for rebuild

* Thu Nov 10 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3.1-3.fc5
- disable-static instead of removing .a files. 
- sync release with FC-4 branch

* Mon Nov  7 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3.1-1.fc5
- Update to 4.2.3.1
- Added dist tag
- Removed .la files. Fixes bug 172645
- Removed .a files. 

* Tue May 17 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.2-1.fc4
- Update to 4.2.2

* Fri Mar 25 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-3.fc4
- lowercase Release

* Sat Mar 19 2005 Warren Togami <wtogami@redhat.com> - 4.2.1-2
- remove stuff 

* Tue Mar 15 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-1
- Updated to 4.2.1 version

* Tue Mar  8 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-3
- Fixed License to be BSD and LGPL
- Fixed case on Xfce

* Sun Mar  6 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-2
- Inital Fedora Extras version
- Capitalized first letter of Summary in devel section to quiet rpmlint
- Added LGPL to License as 2 files are under LGPL, the rest BSD

* Sun Jan 23 2005 Than Ngo <than@redhat.com> 4.2.0-1
- update to 4.2.0 release

* Wed Dec 08 2004 Than Ngo <than@redhat.com> 4.1.99.1-1
- update to 4.2 rc1

* Mon Jul 19 2004 Than Ngo <than@redhat.com> 4.0.6-1
- update to 4.0.6
- add requires on glib2-devel, bug #124200
- remove unneeded patch file, which is included in new upstream

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr 15 2004 Than Ngo <than@redhat.com> 4.0.5-1
- update to 4.0.5

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Than Ngo <than@redhat.com> 4.0.3-2
- fixed dependant libraries check on x86_64

* Fri Jan 09 2004 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3

* Thu Dec 25 2003 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2

* Tue Dec 16 2003 Than Ngo <than@redhat.com> 4.0.1-1
- initial build
