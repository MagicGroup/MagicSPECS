Summary: DjVu viewers, encoders, and utilities
Summary(zh_CN.UTF-8): DjVu 查看器，编码器和工具
Name: djvulibre
Version: 3.5.25.3
Release: 5%{?dist}
License: GPLv2+
Group: Applications/Publishing
Group(zh_CN.UTF-8): 应用程序/出版
URL: http://djvu.sourceforge.net/
Source: http://dl.sf.net/djvu/djvulibre-%{version}.tar.gz
Patch0: djvulibre-3.5.22-cdefs.patch
Patch1: djvulibre-3.5.25.3-cflags.patch

Requires(post): xdg-utils
Requires(preun): xdg-utils
%if (0%{?fedora} > 15 || 0%{?rhel} > 6)
BuildRequires: libjpeg-turbo-devel
%else
BuildRequires: libjpeg-devel
%endif
BuildRequires: libtiff-devel
BuildRequires: xdg-utils chrpath
BuildRequires: hicolor-icon-theme
BuildRequires: inkscape

Provides: %{name}-mozplugin = %{version}
Obsoletes: %{name}-mozplugin < 3.5.24

%description
DjVu is a web-centric format and software platform for distributing documents
and images. DjVu can advantageously replace PDF, PS, TIFF, JPEG, and GIF for
distributing scanned documents, digital documents, or high-resolution pictures.
DjVu content downloads faster, displays and renders faster, looks nicer on a
screen, and consume less client resources than competing formats. DjVu images
display instantly and can be smoothly zoomed and panned with no lengthy
re-rendering.

DjVuLibre is a free (GPL'ed) implementation of DjVu, including viewers,
decoders, simple encoders, and utilities. The browser plugin is in its own
separate sub-package.

%description -l zh_CN.UTF-8
DjVu 查看器，编码器和工具，djvu 是一种文档和图像格式及发布的软件平台，可以用来
代替 PDF 等。

%package libs
Summary: Library files for DjVuLibre
Summary(zh_CN.UTF-8): %{name} 的运行库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description libs
Library files for DjVuLibre.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package devel
Summary: Development files for DjVuLibre
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig

%description devel
Development files for DjVuLibre.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-3.5.25
%patch0 -p1 -b .cdefs
%patch1 -p1 -b .cflags


%build 
%configure --with-qt=%{_libdir}/qt-3.3 --enable-threads
# Disable rpath on 64bit - NOT! It makes the build fail (still as of 3.5.20-2)
#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

# Fix for the libs to get stripped correctly (still required in 3.5.20-2)
find %{buildroot}%{_libdir} -name '*.so*' | xargs %{__chmod} +x

# Remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvutoxml
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvused
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/cjb2
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/csepdjvu
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvuserve
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvm
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvuxmlparser
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvutxt
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/ddjvu
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvumake
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/cpaldjvu
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvuextract
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/c44
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvups
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvudump
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvmcvt
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/bzz

# MIME types (icons and desktop file) - this installs icon files under
# /usr/share/icons/hicolor/ and an xml file under /usr/share/mime/image/
# Taken from {_datadir}/djvu/osi/desktop/register-djvu-mime install
# See also the README file in the desktopfiles directory of the source distribution
pushd desktopfiles
for i in 22 32 48 64 ; do
    install -d $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/
    cp -a ./hi${i}-djvu.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/image-vnd.djvu.mime.png
#    cp -a ./hi${i}-djvu.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/gnome-mime-image-vnd.djvu.png
done
popd

magic_rpm_clean.sh

%post
# Unregister menu entry for djview3 if it is present as we no longer
# ship this in favour of the djview4 package. These files were
# installed in %post by the older djvulibre packages, but not actually
# owned by the package (packaging bug)
rm -f %{_datadir}/applications/djvulibre-djview3.desktop || :
rm -f %{_datadir}/icons/hicolor/32x32/apps/djvulibre-djview3.png || :

/usr/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%preun
# This is the legacy script, not compliant with current packaging
# guidelines. However, we leave it in, as the old packages didn't own
# the icon and xml files, so we want to be sure we remove them
if [ $1 -eq 0 ]; then
    # MIME types (icons and desktop file)
    %{_datadir}/djvu/osi/desktop/register-djvu-mime uninstall || :
fi

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/djvu/
%{_datadir}/icons/hicolor/22x22/mimetypes/*
%{_datadir}/icons/hicolor/32x32/mimetypes/*
%{_datadir}/icons/hicolor/64x64/mimetypes/*
%{_datadir}/icons/hicolor/48x48/mimetypes/*


%files libs
%defattr(-,root,root,-)
%doc README COPYRIGHT COPYING NEWS
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/*.*
%{_includedir}/libdjvu/
%{_libdir}/pkgconfig/ddjvuapi.pc
%exclude %{_libdir}/*.la
%{_libdir}/*.so


%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 3.5.25.3-5
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 3.5.25.3-3
- 为 Magic 3.0 重建

* Tue Oct  9 2012 Ville Skyttä <ville.skytta@iki.fi> - 3.5.25.3-2
- Build with $RPM_OPT_FLAGS (#729469).

* Wed Oct  3 2012 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 3.5.25.3-1
- Update to version 3.5.25.3
- Add BuildRequires for inkscape

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May  8 2012 Jonathan G. Underwood <rpmb@mia.theory.phys.ucl.ac.uk> - 3.5.24-4
- Properly remove the djview3 menu entries
- Correctly package the icon files

* Sat May  5 2012 Jonathan G. Underwood <rpmb@mia.theory.phys.ucl.ac.uk> - 3.5.24-4
- Merge in changes from Fedora master branch to el6 branch to bring version 3.5.24
- Unregister djview3 menu/desktop entry on install if present
- Replace BuildRequire for libjpeg-turbo-devel with libjpeg-devel
  depending on fedora/rhel version

* Fri Feb 17 2012 Orion Poplawski <orion@cora.nwra.com> - 3.5.24-3
- Don't call register-djview-menu since we don't build djview3 anymore (bug 734856)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug  8 2011 Peter Robinson <pbrobinson@gmail.com> 3.5.24-1
- 3.5.24
- Obsolete mozplugin, dropped upstream
- Dropped djview3, use djview4

* Mon Jan 31 2011 Karsten Hopp <karsten@redhat.com> 3.5.22-2
- add include cstddefs for size_t

* Mon Nov 30 2009 Ralesh Pandit  <rakesh@fedoraproject.org> 3.5.22-1
- Updated to 3.5.22 (#542221) (Spec patch by Michal Schmidt)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.5.21-1
- Updated to 3.5.21

* Fri Jun 06 2008 Dennis Gilmore <dennis@ausil.us> 3.5.20-3
- BR qt3-devel

* Sun Feb  3 2008 Matthias Saou <http://freshrpms.net/> 3.5.20-2
- Update to 3.5.20-2 (#431025).
- Split off a -libs sub-package (#391201).
- Split off a -mozplugin sub-package.

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 3.5.19-4
- Rebuild for new BuildID feature.

* Mon Aug  6 2007 Matthias Saou <http://freshrpms.net/> 3.5.19-3
- Update License field.

* Mon Jun 11 2007 Matthias Saou <http://freshrpms.net/> 3.5.19-2
- Include patch to remove LC_CTYPE for ja man pages, fixes sed 100% CPU issue.

* Fri Jun  8 2007 Matthias Saou <http://freshrpms.net/> 3.5.19-1
- Update to 3.5.19.
- Disable rpath on 64bit... not.
- Convert ja man pages to UTF-8.

* Tue Feb 13 2007 Matthias Saou <http://freshrpms.net/> 3.5.18-2
- Include man page patch to have man pages be identical across archs (#228359).

* Mon Feb  5 2007 Matthias Saou <http://freshrpms.net/> 3.5.18-1
- Update to 3.5.18.
- Remove no longer needed /usr/include/qt3 replacing.
- Replace desktop build requirements and scriplets with new xdg utils way.
- Include new de and fr man page translations... not! Directories are empty.
- Split -devel sub-package, as the new djview4 should build require it.
- No longer build require a web browser, the plugin always gets built now.

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 3.5.17-2
- FC6 rebuild.
- Use mozilla up to FC5, and seamonkey for FC6+ and non-Fedora.
- Build require gnome-mime-data to get build time detected dirs in place.

* Sun Jul  2 2006 Matthias Saou <http://freshrpms.net/> 3.5.17-1
- Update to 3.5.17.

* Tue Mar 14 2006 Matthias Saou <http://freshrpms.net/> 3.5.16-3
- Update to CVS snapshot, fixes the build with gcc 4.1 (sf.net #1420522).. NOT!
- Include workaround for wrong qt3 includes in gui/djview/Makefile.dep.
- Add new pkgconfig ddjvuapi.pc file.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 3.5.16-2
- FC5 rebuild... nope.

* Mon Jan 30 2006 Matthias Saou <http://freshrpms.net/> 3.5.16-1
- Update to 3.5.16.
- Add conditional to build with/without modular X depending on FC version.
- Remove no longer needed gcc4 patch.
- Add extra qualification patch.

* Thu Aug  4 2005 Matthias Saou <http://freshrpms.net/> 3.5.15-2
- Include djvulibre-3.5.15-gcc401.patch to fix compilation with gcc 4.0.1.
- Add hicolor-icon-theme build req for /usr/share/icons/hicolor/48x48/mimetypes
  to exist.

* Thu Aug  4 2005 Matthias Saou <http://freshrpms.net/> 3.5.15-1
- Update to 3.5.15.
- Move desktop icon to datadir/icons/hicolor.
- Add gtk-update-icon-cache calls for the new icon.
- Move browser plugin from netscape to mozilla directory instead of symlinking.
- Clean build requirements and add libtiff-devel.
- Add redhat-menus build req since it owns /etc/xdg/menus/applications.menu,
  which the configure script checks to install the desktop file.
- Add OPTS to the make line (#156208 - Michael Schwendt).

* Tue May  3 2005 David Woodhouse <dwmw2@infradead.org> 3.5.14-6
- Remove files that were installed only for older KDE versions.

* Mon Feb 14 2005 David Woodhouse <dwmw2@infradead.org> 3.5.14-4
- Include %%{_datadir}/mimelnk/image/x-djvu.desktop

* Tue Nov 16 2004 Matthias Saou <http://freshrpms.net/> 3.5.14-3
- Bump release to provide Extras upgrade path.

* Fri Nov  5 2004 Matthias Saou <http://freshrpms.net/> 3.5.14-2
- Re-enable the lib/mozilla/ symlink to the plugin.
- Add source of /etc/profile.d/qt.sh to fix weird detection problem on FC3...
  ...doesn't fix it, some lib required by qt is probably installed after and
  ldconfig not run.
- Added lib +x chmod'ing to get proper stripping and debuginfo package.

* Sat Oct 16 2004 Matthias Saou <http://freshrpms.net/> 3.5.14-2
- Added update-desktop-database scriplet calls.

* Mon Aug 16 2004 Matthias Saou <http://freshrpms.net/> 3.5.14-1
- Update to 3.5.14.
- Added newly introduced files to the package.

* Mon May 17 2004 Matthias Saou <http://freshrpms.net/> 3.5.13-1
- Update to 3.5.13.
- Added new Japanese man pages.

* Wed May  5 2004 Matthias Saou <http://freshrpms.net/> 3.5.12-4
- Changed the plugin directory for mozilla to %%{_libdir}/mozilla,
  as suggested by Matteo Corti.
- Shortened the description.

* Wed Jan 14 2004 Matthias Saou <http://freshrpms.net/> 3.5.12-3
- Added XFree86-devel and libjpeg-devel build requirements.

* Fri Nov  7 2003 Matthias Saou <http://freshrpms.net/> 3.5.12-2
- Rebuild for Fedora Core 1.

* Mon Sep  1 2003 Matthias Saou <http://freshrpms.net/>
- Update to 3.5.12.

* Thu May  1 2003 Matthias Saou <http://freshrpms.net/>
- Update to 3.5.11.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.

* Thu Mar 20 2003 Matthias Saou <http://freshrpms.net/>
- Update to 3.5.10.

* Wed Jul 24 2002 Matthias Saou <http://freshrpms.net/>
- Update to 3.5.7.

* Fri Jul 19 2002 Matthias Saou <http://freshrpms.net/>
- Spec file cleanup and fixes.

* Wed May 29 2002 Leon Bottou <leon@bottou.org>
- bumped to version 3.5.6-1

* Mon Apr 1 2002 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.5-2
- changed group to Applications/Publishing

* Tue Mar 25 2002 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.5-2

* Tue Jan 22 2002 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.4-1.
- fixed for properly locating the man directory.
- bumped to version 3.5.4-2.

* Wed Jan 16 2002 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.3-1

* Fri Dec  7 2001 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.2-1.

* Wed Dec  5 2001 Leon Bottou <leonb@users.sourceforge.net>
- created spec file for rh7.x.

