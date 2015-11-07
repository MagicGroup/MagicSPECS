Summary: X.Org X11 libXt runtime library
Summary(zh_CN.UTF-8): X.Org X11 libXt 运行库
Name: libXt
Version: 1.1.5
Release: 2%{?dist}
License: MIT
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: pkgconfig(xproto) pkgconfig(x11) pkgconfig(sm)

%description
X.Org X11 libXt runtime library

%description -l zh_CN.UTF-8
X.Org X11 libXt 运行库。

%package devel
Summary: X.Org X11 libXt development package
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libXt development package

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
# FIXME: Work around pointer aliasing warnings from compiler for now
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure --disable-static \
  --with-xfile-search-path="%{_sysconfdir}/X11/%%L/%%T/%%N%%C%%S:%{_sysconfdir}/X11/%%l/%%T/\%%N%%C%%S:%{_sysconfdir}/X11/%%T/%%N%%C%%S:%{_sysconfdir}/X11/%%L/%%T/%%N%%S:%{_sysconfdir}/X\11/%%l/%%T/%%N%%S:%{_sysconfdir}/X11/%%T/%%N%%S:%{_datadir}/X11/%%L/%%T/%%N%%C%%S:%{_datadir}/X1\1/%%l/%%T/%%N%%C%%S:%{_datadir}/X11/%%T/%%N%%C%%S:%{_datadir}/X11/%%L/%%T/%%N%%S:%{_datadir}/X11/%%\l/%%T/%%N%%S:%{_datadir}/X11/%%T/%%N%%S"

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p -m 0755 $RPM_BUILD_ROOT%{_datadir}/X11/app-defaults
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_docdir}/libXt
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog
%{_libdir}/libXt.so.6
%{_libdir}/libXt.so.6.0.0
%dir %{_datadir}/X11/app-defaults

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/CallbackI.h
%{_includedir}/X11/Composite.h
%{_includedir}/X11/CompositeP.h
%{_includedir}/X11/ConstrainP.h
%{_includedir}/X11/Constraint.h
%{_includedir}/X11/ConvertI.h
%{_includedir}/X11/Core.h
%{_includedir}/X11/CoreP.h
%{_includedir}/X11/CreateI.h
%{_includedir}/X11/EventI.h
%{_includedir}/X11/HookObjI.h
%{_includedir}/X11/InitialI.h
%{_includedir}/X11/Intrinsic.h
%{_includedir}/X11/IntrinsicI.h
%{_includedir}/X11/IntrinsicP.h
%{_includedir}/X11/Object.h
%{_includedir}/X11/ObjectP.h
%{_includedir}/X11/PassivGraI.h
%{_includedir}/X11/RectObj.h
%{_includedir}/X11/RectObjP.h
%{_includedir}/X11/ResConfigP.h
%{_includedir}/X11/ResourceI.h
%{_includedir}/X11/SelectionI.h
%{_includedir}/X11/Shell.h
%{_includedir}/X11/ShellI.h
%{_includedir}/X11/ShellP.h
%{_includedir}/X11/StringDefs.h
%{_includedir}/X11/ThreadsI.h
%{_includedir}/X11/TranslateI.h
%{_includedir}/X11/VarargsI.h
%{_includedir}/X11/Vendor.h
%{_includedir}/X11/VendorP.h
%{_includedir}/X11/Xtos.h
%{_libdir}/libXt.so
%{_libdir}/pkgconfig/xt.pc
%{_mandir}/man3/*.3*

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.1.5-2
- 更新到 1.1.5

* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 1.1.4-1
- 更新到 1.1.4

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1.3-2
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 1.1.1-2
- 为 Magic 3.0 重建

* Thu Mar 10 2011 Adam Jackson <ajax@redhat.com> 1.1.1-1
- libXt 1.1.1

* Mon Mar 07 2011 Adam Jackson <ajax@redhat.com> 1.1.0-1
- libXt 1.1.0

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Adam Jackson <ajax@redhat.com> 1.0.9-1
- libXt 1.0.9

* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 1.0.7-1
- libXt 1.0.7

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.6-2
- Un-require xorg-x11-filesystem
- Remove useless %%dir

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 1.0.6-1
- libXt 1.0.6

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 04 2008 Adam Jackson <ajax@redhat.com> 1.0.5-1
- libXt 1.0.5

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.4-5
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 parag <paragn@fedoraproject.org> - 1.0.4-4
- Merge-Review #226090
- Removed XFree86-libs, xorg-x11-libs XFree86-devel, xorg-x11-devel as Obsoletes
- Removed BR:pkgconfig
- Removed zero-length README AUTHORS NEWS file

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.4-3
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1.0.4-2
- Don't install INSTALL

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 1.0.4-1.fc7
- Update to 1.0.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.0.2-3.1.fc6
- rebuild

* Tue Jul 11 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-3.fc6
- Add the {_datadir}/X11/app-defaults directory to the file manifest, as
  libXt is the canonical owner of the directory.  Discovered in (#198025).

* Wed Jun 28 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-2
- Added libXt-1.0.2-libsm-fix.patch to remove libSM from the Requires: line
  in the installed pkgconfig file.  Apps should link against libSM if they
  need it, but we shouldn't force them to link against it if they don't.

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-1
- Updated libXt to version 1.0.2 from X11R7.1

* Fri Jun 09 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-3
- Added "Requires: xorg-x11-proto-devel" to devel package for xt.pc

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Added "BuildRequires: pkgconfig" for (#193503)
- Replace "makeinstall" with "make install DESTDIR=..."
- Remove package ownership of mandir/libdir/etc.

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.0.1-1
- Update to 1.0.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libXt to version 1.0.0 from X11R7 RC4
- Added makestrs and it's manpage to the devel subpackage.

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-1
- Updated libXt to version 0.99.3 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec 02 2005 Kristian Høgsberg <krh@redhat.com> 0.99.2-3
- Use the default value from configure.ac for --with-xfile-search-path
  except with %%{_datadir} instead of $(libdir), so Xt can search for
  app-default files as usual.
- Move the --with-xfile-search-path outside the with_static condition.

* Tue Nov 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Invoke ./configure --with-xfile-search-path=%%{_datadir}/X11/app-defaults
  to make sure Xt is looking in the right place for app-defaults files.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libXt to version 0.99.2 from X11R7 RC2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Wed Nov 02 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-3
- Actually spell RPM_OPT_FLAGS correctly this time.

* Mon Oct 31 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Build with -fno-strict-aliasing to work around possible pointer aliasing
  issue

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated libXt to version 0.99.1 from X11R7 RC1
- Updated file manifest to find manpages in 'man3x'

* Thu Oct 06 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-5
- Added Requires: libX11-devel to libXt-devel subpackage, as Xt headers
  include Xlib headers causing xterm and other things to fail to compile.

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-4
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro
- Fix BuildRequires to use new style X library package names

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-3
- Changed all virtual BuildRequires to the "xorg-x11-" prefixed non-virtual
  package names, as we want xorg-x11 libs to explicitly build against
  X.Org supplied libs, rather than "any implementation", which is what the
  virtual provides is intended for.

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
