Name:           glew
Version:	1.13.0
Release:        2%{?dist}
Summary:        The OpenGL Extension Wrangler Library
Summary(zh_CN.UTF-8): OpenGL 的扩展库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        BSD and MIT
URL:            http://glew.sourceforge.net

Source0:        http://downloads.sourceforge.net/project/glew/glew/%{version}/glew-%{version}.tgz
Patch0:		0001-BUILD-respect-DESTDIR-variable.patch
Patch1:         glew-1.9.0-makefile.patch
BuildRequires:  libGLU-devel

%description
The OpenGL Extension Wrangler Library (GLEW) is a cross-platform C/C++
extension loading library. GLEW provides efficient run-time mechanisms for
determining which OpenGL extensions are supported on the target platform.
OpenGL core and extension functionality is exposed in a single header file.
GLEW is available for a variety of operating systems, including Windows, Linux,
Mac OS X, FreeBSD, Irix, and Solaris.

This package contains the demo GLEW utilities.  The libraries themselves
are in libGLEW and libGLEWmx.

%description -l zh_CN.UTF-8
GLEW是一个跨平台的C++扩展库，基于OpenGL图形接口。

%package devel
Summary:        Development files for glew
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       libGLEW = %{version}-%{release}
Requires:       libGLEWmx = %{version}-%{release}
Requires:       libGLU-devel

%description devel
Development files for glew

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package -n libGLEW
Summary:        libGLEW
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description -n libGLEW
libGLEW

%package -n libGLEWmx
Summary:        libGLEWmx
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description -n libGLEWmx
libGLEWmx

%prep
%setup -q
%patch0 -p1 -b .bld
%patch1 -p1 -b .make

# update config.guess for new arch support
cp /usr/lib/rpm/magic/config.guess config/

%build

make %{?_smp_mflags} CFLAGS.EXTRA="$RPM_OPT_FLAGS -fPIC" includedir=%{_includedir} GLEW_DEST= STRIP= libdir=%{_libdir} bindir=%{_bindir} GLEW_DEST=

%install
make install.all GLEW_DEST= DESTDIR="$RPM_BUILD_ROOT" libdir=%{_libdir} bindir=%{_bindir} includedir=%{_includedir}
find $RPM_BUILD_ROOT -type f -name "*.a" -delete
# sigh
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/*.so*
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libGLEW -p /sbin/ldconfig

%postun -n libGLEW -p /sbin/ldconfig

%post -n libGLEWmx -p /sbin/ldconfig

%postun -n libGLEWmx -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_bindir}/*

%files -n libGLEW
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_libdir}/libGLEW.so.*

%files -n libGLEWmx
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_libdir}/libGLEWmx.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libGLEW.so
%{_libdir}/libGLEWmx.so
%{_libdir}/pkgconfig/glew.pc
%{_libdir}/pkgconfig/glewmx.pc
%{_includedir}/GL/*.h
%doc doc/*

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.13.0-2
- 更新到 1.13.0

* Tue May 27 2014 Liu Di <liudidi@gmail.com> - 1.10.0-1
- 更新到 1.10.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 18 2012 Ville Skyttä <ville.skytta@iki.fi> - 1.9.0-2
- Prevent stripping binaries before rpmbuild does it.

* Thu Dec 13 2012 Adam Jackson <ajax@redhat.com> 1.9.0-1
- glew 1.9.0

* Sun Jul 22 2012 Ville Skyttä <ville.skytta@iki.fi> - 1.7.0-3
- Move/add ldconfig post(un)install scriptlets to appropriate subpackages.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 13 2012 Adam Jackson <ajax@redhat.com> 1.7.0-1
- glew 1.7.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Adam Jackson <ajax@redhat.com> 1.6.0-1
- glew 1.6.0 (#714763)

* Wed Mar 23 2011 Adam Williamson <awilliam@redhat.com> - 1.5.8-3
- instead of taking flags out in makefile.patch and adding them back
  in add-needed.patch, let's just not take them out...

* Wed Mar 23 2011 Adam Jackson <ajax@redhat.com> 1.5.8-2
- glew-1.5.8-glewmx.patch: Install libGLEWmx 0755 so autoprovs work
- Split runtime libraries to their own packages

* Wed Mar 23 2011 Adam Williamson <awilliam@redhat.com> - 1.5.8-1
- bump to 1.5.8
- add soname.patch to fix the internal SONAME of the MX library

* Wed Mar 23 2011 Adam Williamson <awilliam@redhat.com> - 1.5.7-3
- add glewmx.patch (upstream commit 302c224016, always build the
  MX-enabled version of the library as well as non-MX version, under
  a different name)
- revise add-needed.patch to change the LDFLAGS in a better place
  and add -lGLU as well as -lX11

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Dave Airlie <airlied@redhat.com> 1.5.7-1
- glew 1.5.7

* Wed Aug 25 2010 Adam Jackson <ajax@redhat.com> 1.5.5-1
- glew 1.5.5

* Fri Jul 30 2010 Dave Airlie <airlied@redhat.com> 1.5.4-2
- fix glew.pc file as pointed out by David Aguilar

* Sat May 29 2010 Dave Airlie <airlied@redhat.com> 1.5.4-1
- glew 1.5.4 - add glew.pc

* Tue Feb 09 2010 Adam Jackson <ajax@redhat.com> 1.5.2-2
- glew-1.5.2-add-needed.patch: Fix FTBFS from --no-add-needed

* Tue Feb 02 2010 Adam Jackson <ajax@redhat.com> 1.5.2-1
- glew 1.5.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 13 2008 Jochen Schmitt <Jochen herr-schmitt de> - 1.5.1-1
- New upstream release (#469639)
- Fix licenseing issue with developer documentation

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.0-2
- Autorebuild for GCC 4.3

* Mon Jan 21 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5.0-1
- New upstream version, now SGI licensed stuff free out of the box!
- Unfortunately some of the included docs are under a non free license,
  therefor this package is based on a modified tarbal with these files removed

* Sat Jan 12 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-4
- Add missing GL_FLOAT_MATXxX defines

* Sat Aug 18 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-3
- Fix multiple unused direct shlib dependencies in libGLEW.so
- Remove the "SGI Free Software License B" and "GLX Public License" tekst from
  the doc dir in the tarbal
- Patch credits.html to no longer refer to the 2 non free licenses, instead it
  now points to LICENSE-README.fedora
- Put API docs in -devel instead of main package

* Mon Aug  6 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-2
- Remove SGI encumbered files to make this ok to go into Fedora
- Replace some removed files with (modified) mesa files
- Regenerate some of the removed files using the mesa replacemenmt files
  and the scripts in the auto directory
- Readd wglew.h, some programs may need this to compile
- Update License tag for new Licensing Guidelines compliance

* Sun May 06 2007 Ian Chapman <packages@amiga-hardware.com> 1.4.0-1%{?dist}
- Updated to 1.4.0

* Sun Mar 04 2007 Ian Chapman <packages@amiga-hardware.com> 1.3.6-1%{?dist}
- Updated to 1.3.6
- Updated pathandstrip patch
- Dropped xlib patch - fixed upstream
- Dropped sed EOL replacements - fixed upstream
- Changed license to GPL

* Fri Dec 01 2006 Ian Chapman <packages@amiga-hardware.com> 1.3.5-1%{?dist}
- Updated to 1.3.5
- Fixed stripping of the binaries
- Reinstate parallel building, no longer appears broken
- Removed FC4 specifics from spec (no longer supported)

* Tue Jun 20 2006 Ian Chapman <packages@amiga-hardware.com> 1.3.4-3%{?dist}
- Added buildrequire macros to determine fc4, fc5, fc6 due to X modularisation

* Sun Jun 04 2006 Ian Chapman <packages@amiga-hardware.com> 1.3.4-2%{?dist}
- Replaced %%{_sed} macro with sed
- Replaced xorg-x11-devel (build)requires with libGLU-devel for compatibility
  with modular / non-modular X
- Replaced source URL to use primary sf site rather than a mirror
- Removed superfluous docs from devel package
- Removed wglew.h, seems to be only useful for windows platforms

* Thu May 11 2006 Ian Chapman <packages@amiga-hardware.com> 1.3.4-1.iss
- Initial Release
