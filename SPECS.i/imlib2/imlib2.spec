Summary:        Image loading, saving, rendering, and manipulation library
Name:           imlib2
Version:        1.4.5
Release:        8%{?dist}
License:        Imlib2
Group:          System Environment/Libraries
URL:            http://docs.enlightenment.org/api/imlib2/html/
Source0:        http://downloads.sourceforge.net/enlightenment/%{name}-%{version}.tar.bz2
# Fedora specific multilib hack, upstream should switch to pkgconfig one day
Patch0:         imlib2-1.3.0-multilib.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libjpeg-devel libpng-devel libtiff-devel
BuildRequires:  giflib-devel freetype-devel >= 2.1.9-4 libtool bzip2-devel
BuildRequires:  libX11-devel libXext-devel libid3tag-devel pkgconfig

%description
Imlib 2 is a library that does image file loading and saving as well
as rendering, manipulation, arbitrary polygon support, etc.  It does
ALL of these operations FAST. Imlib2 also tries to be highly
intelligent about doing them, so writing naive programs can be done
easily, without sacrificing speed.  This is a complete rewrite over
the Imlib 1.x series. The architecture is more modular, simple, and
flexible.


%package devel
Summary:        Development package for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libX11-devel libXext-devel freetype-devel >= 2.1.9-4 pkgconfig

%description devel
This package contains development files for %{name}.

Imlib 2 is a library that does image file loading and saving as well
as rendering, manipulation, arbitrary polygon support, etc.  It does
ALL of these operations FAST. Imlib2 also tries to be highly
intelligent about doing them, so writing naive programs can be done
easily, without sacrificing speed.  This is a complete rewrite over
the Imlib 1.x series. The architecture is more modular, simple, and
flexible.


%package id3tag-loader
Summary:        Imlib2 id3tag-loader
License:        GPLv2+
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description id3tag-loader
This package contains a plugin which makes imlib2 capable of parsing id3 tags
of mp3 files. This plugin is packaged separately because it links with
libid3tag which is GPLv2+, thus making imlib2 and apps using it subject to the
conditions of the GPL version 2 (or at your option) any later version.


%prep
%setup -q
%patch0 -p1 -b .multilib

%build
asmopts="--disable-mmx --disable-amd64"
%ifarch x86_64
asmopts="--disable-mmx --enable-amd64"
%else
%ifarch %{ix86}
asmopts="--enable-mmx --disable-amd64"
%endif
%endif

# stop -L/usr/lib[64] getting added to imlib2-config
export x_libs=" "
%configure --disable-static --with-pic $asmopts
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# remove demos and their dependencies
rm $RPM_BUILD_ROOT%{_bindir}/imlib2_*
rm -rf $RPM_BUILD_ROOT%{_datadir}/imlib2/data/
# remove static libraries
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f \{\} \;


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS README TODO
%{_libdir}/libImlib2.so.*
%dir %{_libdir}/imlib2/
%dir %{_libdir}/imlib2/filters/
%{_libdir}/imlib2/filters/*.so
%dir %{_libdir}/imlib2/loaders/
%{_libdir}/imlib2/loaders/*.so
%exclude %{_libdir}/imlib2/loaders/id3.*

%files devel
%defattr(-,root,root,-)
%doc doc/*.gif doc/*.html
%{_bindir}/imlib2-config
%{_includedir}/Imlib2.h
%{_libdir}/libImlib2.so
%{_libdir}/pkgconfig/imlib2.pc

%files id3tag-loader
%{_libdir}/imlib2/loaders/id3.*


%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.4.5-8
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.5-7
- 为 Magic 3.0 重建

* Wed Mar 28 2012 Liu Di <liudidi@gmail.com> - 1.4.5-6
- 为 Magic 3.0 重建

* Wed Mar 28 2012 Liu Di <liudidi@gmail.com> - 1.4.5-5
- 为 Magic 3.0 重建

* Wed Mar 28 2012 Liu Di <liudidi@gmail.com> - 1.4.5-4
- 为 Magic 3.0 重建

* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 1.4.5-3
- 为 Magic 3.0 重建

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.4.5-2
- Rebuild for new libpng

* Mon Sep 19 2011 Tomas Smetana <tsmetana@redhat.com> - 1.4.5-1
- new upstream version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 07 2010 Tomas Smetana <tsmetana@redhat.com> - 1.4.4-1
- new upstream version

* Fri Apr 23 2010 Tomas Smetana <tsmetana@redhat.com> - 1.4.3-1
- new upstream version
- patch for CVE-2010-0991

* Mon Feb 01 2010 Tomas Smetana <tsmetana@redhat.com> - 1.4.2-6
- fix #542607 - remove static libraries

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 03 2009 Tomas Smetana <tsmetana@redhat.com> 1.4.2-3
- fix #477400 - remove fonts
- remove demo programs and images

* Sun Nov 23 2008 Tomas Smetana <tsmetana@redhat.com> 1.4.2-2
- patch for CVE-2008-5187

* Tue Oct 21 2008 Tomas Smetana <tsmetana@redhat.com> 1.4.2-1
- new upstream version 1.4.2

* Thu Jun 12 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.1-1
- New upstream release 1.4.1
- Stop shipping static lib in -devel

* Fri May 30 2008 Tomas Smetana <tsmetana@redhat.com> 1.4.0-7
- patch for CVE-2008-2426

* Tue Mar 11 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-6
- Disable amd64 assembly optimization. (Kills idesk - #222998, #436924)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.0-5
- Autorebuild for GCC 4.3

* Tue Oct 23 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-4
- Fix building on ia64 (bz 349171)

* Thu Sep  6 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-3
- Update license tag

* Wed Aug  8 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-2
- put the id3tag loader in its own imlib2-id3tag-loader subpackage as it links
  to libid3tag, which is GPLv2+, and we don't want the imlib2 main package to
  become GPLv2+ (bz 251054) (WIP) (*)
- fix the URL tag (bz 251277)
- Update License tag for new Licensing Guidelines compliance (WIP) (*)
(*) waiting for feedback from Spot, do not build yet!!

* Sun May 27 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-1
- New upstream release 1.4.0

* Thu Nov  9 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.0-3
- Fix CVE-2006-4806, CVE-2006-4807, CVE-2006-4808, CVE-2006-4809, thanks to
  Ubuntu for the patch (bug 214676)

* Thu Oct 26 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.0-2
- Multilib devel goodness (make -devel i386 and x86_64 parallel installable)
- Fix bug 212469
- Add libid3tag-devel to the BR's so id3tag support gets build in

* Tue Oct 24 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.0-1
- New upstream release 1.3.0

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.2-2
- FE6 Rebuild

* Sun Jul 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.2-1
- New upstream release 1.2.2

* Sun Jul 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.1-6
- Taking over as maintainer since Anvil has other priorities
- Long long due rebuild with new gcc for FC-5 (bug 185871)

* Thu Nov 24 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.1-5
- Make XPM loader use /usr/share/X11/rgb.txt.
- Drop no longer needed multilib configure options.

* Sun Nov 13 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.1-4
- Adapt to modular X.Org (#172613).

* Wed Sep 21 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.1-3
- Make XPM loader use /usr/lib/X11/rgb.txt instead of /usr/X11R6/...

* Sun Aug 28 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.1-2
- 1.2.1, patches applied/obsoleted upstream.
- Improve summary and description, fix URL.
- Move HTML docs to -devel.
- Build with dependency tracking disabled.
- Drop x86_64 freetype rpath hack, require a fixed freetype-devel.

* Mon May  9 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.0-8.fc4
- Fix segfault in XPM loader (#156058).

* Tue Apr  5 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.0-7.fc4
- Fix broken pkgconfig file.

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.0-6
- Include imlib2 directory in datadir and libdir.

* Wed Feb  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-5
- Link loaders with the main lib, fixes load/save problems with some apps.

* Tue Jan 18 2005 Michael Schwendt <mschwendt[AT[users.sf.net> - 0:1.2.0-4
- Really include libtool archives to fix fedora.us bug #2284.

* Fri Jan 14 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.2.0-3
- Move filters and loaders back into main package where they belong

* Mon Jan 10 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.2.0-2
- Don't ship *.?.a in {_libdir}/imlib/filters/ and loaders/

* Sun Jan 09 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.2.0-1
- Ship .la files ue to a bug in kdelibs; see
  https://bugzilla.fedora.us/show_bug.cgi?id=2284
  http://bugzilla.redhat.com/bugzilla/142244
  http://bugs.kde.org/93359
- Use make param LIBTOOL=/usr/bin/libtool - fixes hardcoded rpath on x86_64
- fix hardcoded rpath im Makefiles on x86_64 due to freetype-config --libs
  returning "-L/usr/lib64 -Wl,--rpath -Wl,/usr/lib64 -lfreetype -lz"
- Update to 1.2.0 -- fixes several security issues
- remove explicit libdir=_libdir - 1.2.9 does not need it anymore
- removeddemo compile/install;
- use configure param --x-libraries={_prefix}/X11R6/{_lib} and patch to fix
  "cannot find -lX11"

* Thu Dec 30 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.1.2-2
- Disable mmx on x86_64 (fixes Build error)
- Add explicit libdir=_libdir to make calls to avoid install errors on x86_64
- Add --with-pic configure option (taken from Matthias Saou's package)

* Sat Sep 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-0.fdr.1
- Update to 1.1.2, fixes CAN-2004-0802.
- Enable MMX on all ix86, x86_64 and ia64, it seems runtime-detected.
- Update URL.

* Tue Nov 18 2003 Dams <anvil[AT]livna.org> 0:1.0.6-0.fdr.3
- s#_prefix/lib#_libdir#

* Tue Nov 18 2003 Dams <anvil[AT]livna.org> 0:1.0.6-0.fdr.2
- Moved some binaries and loaders into main package
- Added missing Requires and BuildRequires

* Sun Oct 26 2003 Dams <anvil[AT]livna.org>
- Initial build.
