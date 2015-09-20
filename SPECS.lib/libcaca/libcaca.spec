%define beta beta19

%{!?ruby_vendorlibdir: %global ruby_vendorlibdir %(ruby -r rbconfig -e 'print RbConfig::CONFIG["vendorlibdir"]')}
%{!?ruby_vendorarchdir: %global ruby_vendorarchdir %(ruby -r rbconfig -e 'print RbConfig::CONFIG["vendorarchdir"]')}

Summary: Library for Colour AsCii Art, text mode graphics
Summary(zh_CN.UTF-8): 彩色 AsCii 艺术字，文本界面图形库
Name: libcaca
Version: 0.99
Release: 0.20.%{beta}%{?dist}
License: WTFPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://caca.zoy.org/wiki/libcaca
Source: http://caca.zoy.org/files/libcaca/libcaca-%{version}.%{beta}.tar.gz
Patch0: libcaca-0.99.beta16-multilib.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: slang-devel
BuildRequires: ncurses-devel
BuildRequires: libX11-devel
BuildRequires: glut-devel
BuildRequires: libGLU-devel
BuildRequires: imlib2-devel
BuildRequires: pango-devel
# For the docs
Buildrequires: doxygen
Buildrequires: tetex-latex
Buildrequires: tetex-dvips

%description
libcaca is the Colour AsCii Art library. It provides high level functions
for color text drawing, simple primitives for line, polygon and ellipse
drawing, as well as powerful image to text conversion routines.

%description -l zh_CN.UTF-8
彩色 AsCii 艺术字，文本界面图形库。

%package devel
Summary: Development files for libcaca, the library for Colour AsCii Art
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: slang-devel
Requires: ncurses-devel
Requires: libX11-devel
Requires: glut-devel
Requires: libGLU-devel
Requires: imlib2-devel
Requires: pango-devel

%description devel
libcaca is the Colour AsCii Art library. It provides high level functions
for color text drawing, simple primitives for line, polygon and ellipse
drawing, as well as powerful image to text conversion routines.

This package contains the header files and static libraries needed to
compile applications or shared objects that use libcaca.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package -n caca-utils
Summary: Colour AsCii Art Text mode graphics utilities based on libcaca
Summary(zh_CN.UTF-8): 基于 libcaca 的工具
Group: Amusements/Graphics
Group(zh_CN.UTF-8): 娱乐/图形

%description -n caca-utils
This package contains utilities and demonstration programs for libcaca, the
Colour AsCii Art library.

cacaview is a simple image viewer for the terminal. It opens most image
formats such as JPEG, PNG, GIF etc. and renders them on the terminal using
ASCII art. The user can zoom and scroll the image, set the dithering method
or enable anti-aliasing.

cacaball is a tiny graphic program that renders animated ASCII metaballs on
the screen, cacafire is a port of AALib's aafire and displays burning ASCII
art flames, and cacademo is a simple application that shows the libcaca
rendering features such as line and ellipses drawing, triangle filling and
sprite blitting.

%description -n caca-utils -l zh_CN.UTF-8
基于 libcaca 的工具

%package -n python-caca
Summary: Python bindings for libcaca
Summary(zh_CN.UTF-8): libcaca 的 Python 绑定
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
BuildRequires: python2-devel

%description -n python-caca
This package contains the python bindings for using libcaca from python.

%description -n python-caca -l zh_CN.UTF-8
libcaca 的 Python 绑定。

%package -n ruby-caca
Summary: Ruby bindings for libcaca
Summary(zh_CN.UTF-8): libcaca 的 Ruby 绑定
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: ruby(release)
BuildRequires: ruby, ruby-devel
Provides: ruby(caca) = %{version}-%{release}

%description -n ruby-caca
This package contains the ruby bindings for using libcaca from ruby.

%description -n ruby-caca -l zh_CN.UTF-8
libcaca 的 Ruby 绑定。

%prep
%setup -q -n libcaca-%{version}.%{beta}
%patch0 -p1 -b .multilib


%build
sed -i -e 's|Config::CONFIG\["sitearchdir"\]|Config::CONFIG["vendorarchdir"]|' \
       -e 's|Config::CONFIG\["sitelibdir"\]|Config::CONFIG["vendorlibdir"]|' \
       -e "s|rbconfig -e 'print Config|rbconfig -e 'print RbConfig|" \
       configure

%configure \
  --disable-static \
  --disable-csharp \
  --disable-java \
  --disable-doc
# Remove useless rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf %{buildroot} libcaca-dev-docs
make install DESTDIR=%{buildroot}
# We want to include the docs ourselves from the source directory
# mv %{buildroot}%{_docdir}/libcaca-dev libcaca-dev-docs
# Remove symlink to libcaca-dev
# rm -f %{buildroot}%{_docdir}/libcucul-dev
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
#%doc ChangeLog libcaca-dev-docs/html/
%doc ChangeLog
%{_bindir}/caca-config
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%exclude %{_libdir}/*.la
%{_libdir}/*.so
%{_mandir}/man1/caca-config.1*
#%{_mandir}/man3/*

%files -n caca-utils
%defattr(-,root,root,-)
%doc AUTHORS COPYING* NEWS NOTES README THANKS
%{_bindir}/cacademo
%{_bindir}/cacafire
%{_bindir}/cacaplay
%{_bindir}/cacaserver
%{_bindir}/cacaview
%{_bindir}/cacaclock
%{_bindir}/img2txt
%{_datadir}/libcaca/
%{_mandir}/man1/cacademo.1*
%{_mandir}/man1/cacafire.1*
%{_mandir}/man1/cacaplay.1*
%{_mandir}/man1/cacaserver.1*
%{_mandir}/man1/cacaview.1*
%{_mandir}/man1/img2txt.1*

%files -n python-caca
%defattr(-,root,root,-)
%doc python/examples
%{python2_sitelib}/caca/

%files -n ruby-caca
%defattr(-,root,root,-)
%doc ruby/README
%{ruby_vendorlibdir}/caca.rb
%exclude %{ruby_vendorarchdir}/caca.la
%{ruby_vendorarchdir}/caca.so


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.99-0.20.beta19
- 为 Magic 3.0 重建

* Thu Jul 10 2014 Liu Di <liudidi@gmail.com> - 0.99-0.17.beta19
- 升级到 0.99.beta19
- 添加 python-caca 包
- 临时禁止生成 doc

* Tue Mar 19 2013 Vít Ondruch <vondruch@redhat.com> - 0.99-0.17.beta17
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.16.beta17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.15.beta17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 29 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.99-0.14.beta17
- Rebuilt and patched for Ruby 1.9.3.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.13.beta17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 11 2011 Matthias Saou <http://freshrpms.net/> 0.99-0.12.beta17
- Explicitly disable building csharp and java bindings (#671206).

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.11.beta17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Apr 28 2010 Matthias Saou <http://freshrpms.net/> 0.99-0.10.beta17
- Update to 0.99.0beta17.
- Update spec file URLs.
- Switch to using DESTDIR for install, which is the preferred method.
- Remove the static library (#556062).
- Remove no longer needed libGLU patch.
- Enable new ruby bindings.
- Leave C# and Java disabled, I hope no one will ever ask to have them enabled.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.9.beta16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Matthias Saou <http://freshrpms.net/> 0.99-0.8.beta16
- Fix build now that glut no longer links against libGLU (#502296).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 21 2008 Matthias Saou <http://freshrpms.net/> 0.99-0.6.beta16
- Add patch to share the same caca-config for 32 and 64bit (#341951).
- Don't include the pdf devel doc, only html (again, fixed multilib conflict).

* Mon Oct 27 2008 Matthias Saou <http://freshrpms.net/> 0.99-0.5.beta16
- Update to 0.99beta16.
- Update Source URL.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.99-0.4.beta11
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 0.99-0.3.beta11
- Rebuild for new BuildID feature.

* Mon Aug  6 2007 Matthias Saou <http://freshrpms.net/> 0.99-0.2.beta11
- Update License field.

* Thu Mar 29 2007 Matthias Saou <http://freshrpms.net/> 0.99-0.1.beta11
- Update to 0.99beta11.
- We now have a main libcaca package with just the shared lib (built by default
  now), so make the devel sub-package require it too. Leave static lib for now.
- Enable opengl and pango support.
- Remove useless rpath.
- Remove no longer needed man3 patch.
- Remove all configure options, they're autodetected.

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 0.9-11
- FC6 rebuild.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 0.9-10
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 0.9-9
- Rebuild for new gcc/glibc.

* Mon Jan  2 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.9-8
- Include unpackaged man page symlinks.
- Rebuild against new slang.

* Thu Nov 17 2005 Matthias Saou <http://freshrpms.net/> 0.9-7
- Change XFree86-devel requirements to libX11-devel.
- Force --x-includes= and --x-libraries=, otherwise -L gets passed empty.

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.9-6
- Include libcaca datadir.

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 0.9-5
- Bump release to provide Extras upgrade path.

* Wed Nov  3 2004 Matthias Saou <http://freshrpms.net/> 0.9-4
- Disable man3 pages, they don't build on FC3, this needs fixing.
- Fix to not get the debuginfo files go into the devel package.

* Wed May 19 2004 Matthias Saou <http://freshrpms.net/> 0.9-3
- Rebuild for Fedora Core 2.

* Tue Feb 24 2004 Matthias Saou <http://freshrpms.net/> 0.9-2
- Fix License tag from GPL to LGPL.

* Mon Feb  9 2004 Matthias Saou <http://freshrpms.net/> 0.9-1
- Update to 0.9.
- Added cacamoir and cacaplas.

* Fri Jan  9 2004 Matthias Saou <http://freshrpms.net/> 0.7-1
- Spec file cleanup for Fedora Core 1.

* Sat Jan 7 2004 Sam Hocevar (RPM packages) <sam+rpm@zoy.org> 0.7-1
- new release

* Sat Jan 4 2004 Sam Hocevar (RPM packages) <sam+rpm@zoy.org> 0.6-2
- install documentation into {doc}/package-version instead of {doc}/package
- added tetex-dvips to the build dependencies

* Sat Jan 3 2004 Sam Hocevar (RPM packages) <sam+rpm@zoy.org> 0.6-1
- new release
- more detailed descriptions
- split the RPM into libcaca-devel and caca-utils
- packages are rpmlint clean

* Mon Dec 29 2003 Richard Zidlicky <rz@linux-m68k.org> 0.5-1
- created specfile

