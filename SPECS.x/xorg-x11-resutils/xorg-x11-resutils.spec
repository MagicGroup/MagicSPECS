%define pkgname resutils

Summary: X.Org X11 X resource utilities
Summary(zh_CN.UTF-8): X.Org X11 X 资源工具
Name: xorg-x11-%{pkgname}
Version: 7.5
Release: 7%{?dist}
License: MIT
Group: User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
URL: http://www.x.org

Source0:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/appres-1.0.4.tar.bz2
Source1:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/editres-1.0.6.tar.bz2
Source2:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/listres-1.0.3.tar.bz2
Source3:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/viewres-1.0.4.tar.bz2

Patch0:     editres-1.0.6-format-security.patch

BuildRequires: pkgconfig
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: libXmu-devel
BuildRequires: libXext-devel
BuildRequires: libSM-devel
BuildRequires: libICE-devel
BuildRequires: libXaw-devel >= 1.0.2-6
# FIXME: appres has 'x11 xt' as a dependency check, which fails.  While it
# does not check for Xdmcp, installing libXdmcp-devel resolves the problem.
# This implies that one of the other library devel packages should probably
# have a Requires: libXdmcp-devel instead, but it isn't completely clear
# what the best solution is yet, so I'm putting this here.
BuildRequires: libXdmcp-devel

Provides: appres editres listres viewres

# NOTE: appres, editres used to be in the XFree86/xorg-x11 package, whereas
# oddly enough, the listres, viewres utilities were in the *-tools subpackage.
Obsoletes: XFree86, xorg-x11
Obsoletes: XFree86-tools, xorg-x11-tools

%description
A collection of utilities for managing X resources.

%description -l zh_CN.UTF-8
X.Org X11 X 资源工具。

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3
%patch0 -p0 -b .fmt

%build
# Build all apps
{
   for app in * ; do
      pushd $app
#      aclocal --force ; autoconf
      %configure --disable-xprint
      make
      popd
   done
}

%install
rm -rf $RPM_BUILD_ROOT
# Install all apps
{
   for app in * ; do
      pushd $app
      make install DESTDIR=$RPM_BUILD_ROOT
      popd
   done
}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
%{_bindir}/appres
%{_bindir}/editres
%{_bindir}/listres
%{_bindir}/viewres
%{_datadir}/X11/app-defaults/Editres
%{_datadir}/X11/app-defaults/Editres-color
%{_datadir}/X11/app-defaults/Viewres
%{_datadir}/X11/app-defaults/Viewres-color
%{_mandir}/man1/appres.1*
%{_mandir}/man1/editres.1*
%{_mandir}/man1/listres.1*
%{_mandir}/man1/viewres.1*

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 7.5-7
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 7.5-6
- 为 Magic 3.0 重建

* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 7.5-5
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 7.5-4
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 02 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-1
- appres 1.0.3
- editres 1.0.5
- viewres 1.0.3
- listres 1.0.2

* Fri Mar 05 2010 Matěj Cepl <mcepl@redhat.com> - 7.1-10
- Fixed bad directory ownership of /usr/share/X11

* Mon Aug 03 2009 Adam Jackson <ajax@redhat.com> 7.1-9
- Un-Requires xorg-x11-filesystem

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 7.1-6
- Fix license tag.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 7.1-5
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 7.1-4
- Rebuild for build id

* Tue Jan 23 2007 Adam Jackson <ajax@redhat.com> 7.1-3
- appres 1.0.1

* Wed Jul 19 2006 Mike A. Harris <mharris@redhat.com> 7.1-2.fc6
- Remove app-defaults dir from file manifest, as it is owned by libXt (#174021)
- Add 'dist' tag to package release string.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 7.1-1.1
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 7.1-1
- Bump package version to 7.1 to match the X11 release the packages were
  last synced with.
- Bump build dep to libXaw-devel >= 1.0.2-6, to pick up indirect dependency
  on libXpm-devel which was fixed in that release.

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Fix all SourceN lines in spec file to not have to update them every time.
- Remove package ownership of mandir/libdir/etc.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Update all resource utils to version 1.0.1 from X11R7.0

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Update all resource utils to version 1.0.0 from X11R7 RC4.
- Move app-defaults files to _datadir
- Change manpage dir from man1x to man1 to match RC4 default.
- Added "BuildRequires: libX11-devel, libXt-devel"

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> 0.99.1-3
- require newer filesystem package (#172610)

* Sun Nov 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Add "Obsoletes: XFree86, XFree86-tools, xorg-x11, xorg-x11-tools", as 
  appres, editres used to be in the XFree86/xorg-x11 package, whereas
  oddly enough, the listres, viewres utilities were in the *-tools subpackage.
- Rebuild against new libXaw 0.99.2-2, which has fixed DT_SONAME. (#173027)

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Initial build, with all apps taken from X11R7 RC2
- Use "make install DESTDIR=$RPM_BUILD_ROOT" as the makeinstall macro fails on
  some packages.
