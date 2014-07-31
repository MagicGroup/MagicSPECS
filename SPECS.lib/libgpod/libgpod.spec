%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# python-gpod should not advertise _gpod.so in its Provides
%define __provides_exclude_from %{python_sitearch}/.*\.so$

%ifarch %ix86 x86_64 ppc ppc64 ia64 %{arm} sparcv9 alpha s390x
%global with_mono 1
%else
%global with_mono 0
%endif
%if 0%{?rhel}
%global with_mono 0
%endif

Summary: Library to access the contents of an iPod
Summary(zh_CN.UTF-8): 访问 iPod 内容的库
Name: libgpod
Version: 0.8.3
Release: 3%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.gtkpod.org/libgpod.html
Source0: http://downloads.sourceforge.net/gtkpod/%{name}-%{version}.tar.bz2

# upstreamable patch: reduce pkgconfig-related overlinking
# 
Patch50:  libgpod-0.8.2-pkgconfig_overlinking.patch

BuildRequires: automake libtool
BuildRequires: docbook-style-xsl
BuildRequires: glib2-devel
BuildRequires: gdk-pixbuf2-devel
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: libimobiledevice-devel
BuildRequires: libplist-devel
BuildRequires: libusb1-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt
%if %{with_mono}
BuildRequires: mono-devel
BuildRequires: gtk-sharp2-devel
%endif
BuildRequires: pygobject2-devel
BuildRequires: python-devel
BuildRequires: python-mutagen
BuildRequires: sg3_utils-devel
BuildRequires: sqlite-devel
BuildRequires: swig
Requires: udev

%description
Libgpod is a library to access the contents of an iPod. It supports playlists,
smart playlists, playcounts, ratings, podcasts, album artwork, photos, etc.

%description -l zh_CN.UTF-8
访问 iPod 内容的库。

%package devel
Summary: Development files for the libgpod library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Libgpod is a library to access the contents of an iPod. It supports playlists,
smart playlists, playcounts, ratings, podcasts, album artwork, photos, etc.

This package contains the files required to develop programs that will use
libgpod.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: API documentation for the libgpod library
Summary(zh_CN.UTF-8): %{name} 库的 API 文档
Group: Documentation
Group(zh_CN.UTF-8): 文档
License: GFDL
%if 0%{?fedora}
BuildArch: noarch
%endif
Requires: %{name} = %{version}-%{release}

%description doc
Libgpod is a library to access the contents of an iPod. It supports playlists,
smart playlists, playcounts, ratings, podcasts, album artwork, photos, etc.

This package contains the API documentation.

%description doc -l zh_CN.UTF-8
%{name} 库的 API 文档。

%package -n python-gpod
Summary: Python module to access iPod content
Summary(zh_CN.UTF-8): 访问 iPod 内容的 Python 模块
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: python-mutagen

%description -n python-gpod
A python module to access iPod content.  This module provides bindings to the
libgpod library.

%description -n python-gpod -l zh_CN.UTF-8
访问 iPod 内容的 Python 模块

%if %{with_mono}
%package sharp
Summary: C#/.NET library to access iPod content
Summary(zh_CN.UTF-8): 访问 iPod 内容的 C#/.NET 库
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
Requires: %{name}%{?_isa} = %{version}-%{release}

%description sharp
C#/.NET library to access iPod content.  Provides bindings to the libgpod
library.

%description sharp -l zh_CN.UTF-8
访问 iPod 内容的 C#/.NET 库。

%package sharp-devel
Summary: Development files for libgpod-sharp
Summary(zh_CN.UTF-8): %{name}-sharp 的开发包
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
Requires: %{name}-sharp%{?_isa} = %{version}-%{release}

%description sharp-devel
C#/.NET library to access iPod content.  Provides bindings to the libgpod
library.

This package contains the files required to develop programs that will use
libgpod-sharp.

%description sharp-devel -l zh_CN.UTF-8
%{name}-sharp 的开发包。
%endif


%prep
%setup -q

%patch50 -p1 -b .pkgconfig_overlinking

#autoreconf -f

# remove execute perms on the python examples as they'll be installed in %%doc
chmod -x bindings/python/examples/*.py


%build
%configure --without-hal --enable-udev --with-temp-mount-dir=%{_localstatedir}/run/%{name}
make %{?_smp_mflags}


%install
make DESTDIR=%{buildroot} install
magic_rpm_clean.sh
%find_lang %{name}

mkdir -p %{buildroot}/%{_libdir}/libgpod

# remove Makefiles from the python examples dir
rm -rf bindings/python/examples/Makefile*

%if %{with_mono}
# remove execute perms from some libgpod-sharp files
chmod -x %{buildroot}/%{_libdir}/%{name}/*.dll.config
%else
# remove unwanted file
rm -f %{buildroot}/%{_libdir}/pkgconfig/%{name}-sharp.pc
%endif

%if 0%{?fedora} >= 15
# Setup tmpfiles.d config
mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
echo "D /var/run/%{name} 0755 root root -" > \
    %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf
%endif


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README*
%if 0%{?fedora} >= 15
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%endif
%{_bindir}/*
%{_libdir}/*.so.*
%dir %{_localstatedir}/run/%{name}
/lib/udev/iphone-set-info
/lib/udev/ipod-set-info
/lib/udev/rules.d/*.rules
%dir %{_libdir}/libgpod/

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/gpod-1.0/
%{_libdir}/pkgconfig/%{name}-1.0.pc
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
%{_libdir}/*.so


%files doc
%defattr(-, root, root, 0755)
%{_datadir}/gtk-doc


%files -n python-gpod
%defattr(-, root, root, 0755)
%doc COPYING bindings/python/README bindings/python/examples
%{python_sitearch}/gpod
%exclude %{python_sitearch}/gpod/*.la


%if %{with_mono}
%files sharp
%defattr(-, root, root, 0755)
%{_libdir}/%{name}/%{name}-sharp*


%files sharp-devel
%defattr(-, root, root, 0755)
%{_libdir}/pkgconfig/%{name}-sharp.pc
%endif

%changelog
* Mon Jul 21 2014 Liu Di <liudidi@gmail.com> - 0.8.3-3
- 为 Magic 3.0 重建

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 0.8.3-2
- 为 Magic 3.0 重建

* Wed Sep 04 2013 Christophe Fergeau <cfergeau@redhat.com> 0.8.3-1
- Update to libgpod 0.8.3, this is a bugfix release which should fix
  rhbz#921831 rhbz#925750 rhbz#951167

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.2-9
- Rebuild for new libimobiledevice

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 10 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.8.2-7
- libgpod.pc Requires: libimobiledevice-1.0 ... overlinking (#818594)
- tighten subpkg deps (via %%_isa)
- omit -devel deps that (should) get autodetected already

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 Bastien Nocera <bnocera@redhat.com> 0.8.2-5
- Remove bogus gtk2-devel dep in devel sub-package

* Wed Apr 11 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.8.2-4
- Rebuild for new libimobiledevice and usbmuxd

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 08 2011 Adam Jackson <ajax@redhat.com> - 0.8.2-2
- Rebuild to break bogus libpng dep

* Wed Jul 27 2011 Christophe Fergeau <cfergeau@redhat.com>
- Remove duplicated call to autoreconf
- Small BuildRequires cleanups

* Mon Jul 25 2011 Christian Krause <chkr@fedoraproject.org> - 0.8.2-1
- Update to 0.8.2
- Drop upstreamed patches
- Prevent python-gpod from advertising _gpod.so in its Provides

* Mon Jul 18 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.0-12
- libgpod-0.8.0-10.fc16 grew a mono-core dependency (#722976)

* Mon Jul 18 2011 Dan Horák <dan@danny.cz> - 0.8.0-11
- rebuilt for sg3_utils 1.31

* Thu Jul 14 2011 Bastien Nocera <bnocera@redhat.com> 0.8.0-10
- Add hashDB support

* Wed May 25 2011 Todd Zullinger <tmz@pobox.com> - 0.8.0-9
- Fix tmpfiles.d user/group for /var/run/libgpod (#707787)

* Mon May 23 2011 Todd Zullinger <tmz@pobox.com> - 0.8.0-8
- Support tmpfiles.d for Fedora >= 15 (#707066)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Dan Horák <dan[at]danny.cz> - 0.8.0-6
- conditionalize mono support

* Sat Jan 08 2011 Christian Krause <chkr@fedoraproject.org> - 0.8.0-5
- Change patch to fix 32 bit issues in the mono bindings
  (Itdb_Track data structure contained wrong values on x86 systems)

* Sun Dec 26 2010 Bastien Nocera <bnocera@redhat.com> 0.8.0-4
- Rebuild for new libimobiledevice

* Thu Oct 28 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.8.0-3
- Rebuild against new gtk-sharp2 and mono-2.8

* Wed Oct 20 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.8.0-2
- Add patch to fix 32 bit issues in the mono bindings

* Tue Oct 12 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.8.0-1
- Update to 0.8.0

* Wed Sep 29 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.7.95-1
- Update to 0.7.95
- Drop upstreamed patches

* Sat Sep 04 2010 Todd Zullinger <tmz@pobox.com> - 0.7.94-1
- Update to 0.7.94
- Add mono subpackage (#630181)

* Mon Aug 23 2010 Todd Zullinger <tmz@pobox.com> - 0.7.93-4
- Own %%{_datadir}/gtk-doc rather than require gtk-doc (#604388)

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.93-3
- persuade configure to work with swig 2.0.0

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.93-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 15 2010 Todd Zullinger <tmz@pobox.com> - 0.7.93-1
- Update to 0.7.93
- Drop upstreamed mount-dir location patch
- Fix temp mount dir configure option typo
- Drop duplicate libimobiledevice-devel BR
- Remove pointless %%{__$command} macros

* Tue Apr 13 2010 Dan Horák <dan@danny.cz> - 0.7.91-3
- rebuilt for sg3_utils 1.29

* Mon Mar 22 2010 Rex Dieter <rdieter@fedoraproject.org> 0.7.91-2
- rebuild (libimobiledevice)

* Thu Mar 04 2010 Bastien Nocera <bnocera@redhat.com> 0.7.91-1
- Update to 0.7.91
- Use udev callout, disable HAL callouts
- Enable iPhone/iPod Touch support

* Tue Feb 09 2010 Todd Zullinger <tmz@pobox.com> - 0.7.90-1
- Update to 0.7.90
- Adjust default hal callout path (#547049)
  (Temporaily use --with-hal-callouts-dir=%%{_libexecdir}/scripts)

* Thu Dec 10 2009 Bastien Nocera <bnocera@redhat.com> 0.7.2-6
- Handle partial UTF-16 strings (#542176)

* Mon Oct 19 2009 Bastien Nocera <bnocera@redhat.com> 0.7.2-5
- Fix UTF-16 string parsing patch again

* Mon Oct 19 2009 Bastien Nocera <bnocera@redhat.com> 0.7.2-4
- Update UTF-16 string parsing patch

* Sat Oct 17 2009 Bastien Nocera <bnocera@redhat.com> 0.7.2-3
- Fix crasher when parsing UTF-16 strings with a BOM (#517642)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 05 2009 Todd Zullinger <tmz@pobox.com> - 0.7.2-1
- Update to 0.7.2
- Make doc subpackage noarch (on Fedora >= 10)
- Drop --with-hal-callouts-dir from configure, the upstream default works now

* Tue Apr 28 2009 Dan Horak <dan[at]danny.cz> - 0.7.0-3
- rebuild for sg3_utils 1.27

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Todd Zullinger <tmz@pobox.com> - 0.7.0-1
- Update to 0.7.0
- BR libxml2-devel

* Wed Jan 14 2009 Todd Zullinger <tmz@pobox.com> - 0.6.0-10
- Fix path to hal callout (this should help setup the SysInfoExtended
  file automagically)
- Use /var/run/hald as mount dir for hal callout
- Require hal
- Require main package for the -doc subpackage

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.0-9
- Rebuild for Python 2.6

* Thu Oct 02 2008 Todd Zullinger <tmz@pobox.com> - 0.6.0-8
- The -devel package should require gtk2-devel as well
- Add gdk-pixbuf-2.0 to the pkg-config file requirements

* Thu Aug 28 2008 Todd Zullinger <tmz@pobox.com> - 0.6.0-7
- Ensure patches apply with no fuzz

* Mon Jun 30 2008 Dan Horak <dan[at]danny.cz> - 0.6.0-6
- add patch for sg3_utils 1.26 and rebuild

* Wed May 14 2008 Todd Zullinger <tmz@pobox.com> - 0.6.0-5
- Make libgpod-devel require glib2-devel (#446442)

* Tue Feb 12 2008 Todd Zullinger <tmz@pobox.com> - 0.6.0-4
- rebuild for gcc 4.3

* Wed Dec 19 2007 Todd Zullinger <tmz@pobox.com> - 0.6.0-3
- BR docbook-style-xsl to ensure the python docs are built correctly

* Wed Dec 19 2007 Todd Zullinger <tmz@pobox.com> - 0.6.0-2
- add the NEWS file, which contains some info on getting newer iPods working
- split out API docs into a separate package
- set %%defattr for python-gpod

* Wed Nov 21 2007 Todd Zullinger <tmz@pobox.com> - 0.6.0-1
- update to 0.6.0
- apply a few upstream patches that just missed the release

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> - 0.5.2-2
- Rebuild for build ID

* Sat Aug 04 2007 Todd Zullinger <tmz@pobox.com> - 0.5.2-1
- update to 0.5.2
- replace %%makeinstall with %%{__make} DESTDIR=%%{buildroot} install
- build python bindings, merging python-gpod package from extras
- make %%setup quiet
- patch to fixup building of the python docs, BR libxslt
- update license tag

* Tue Jan 16 2007 Alexander Larsson <alexl@redhat.com> - 0.4.2-1
- update to 0.4.2
- Change %%description to reflect newer features
- Remove TODO file from %%doc as it's not included anymore
- Explicitly disable the python bindings, they are in the python-gpod package in
  Extras until the Core/Extras merge

* Mon Nov 20 2006 Alexander Larsson <alexl@redhat.com> - 0.4.0-2
- Add ldconfig calls in post/postun

* Mon Nov 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.4.0-1
- Update to 0.4.0
- Include docs in the -devel package
- Don't ship static libraries

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-3.1
- rebuild

* Tue Jun 06 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-3
- Add missing BR of perl-XML-Parser

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 04 2006 John (J5) Palmieri <johnp@redhat.com> 0.3.0-2
- Modified Matthias Saou's SPEC file found on freshrpms.net
- Added to Fedora Core

* Mon Dec 19 2005 Matthias Saou <http://freshrpms.net/> 0.3.0-1
- Initial RPM release.

