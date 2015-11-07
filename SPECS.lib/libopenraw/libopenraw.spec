Summary:	Decode camera RAW files
Summary(zh_CN.UTF-8): 解码数码相机的 RAW 文件
Name:		libopenraw
Version: 	0.0.9
Release:	3%{?dist}
License:	LGPLv3+
URL:		http://libopenraw.freedesktop.org/wiki
Source0:	http://libopenraw.freedesktop.org/download/%{name}-%{version}.tar.bz2

BuildRequires:	libtool autoconf automake
BuildRequires:	boost-devel
BuildRequires:	exempi-devel >= 1.99.5
BuildRequires:	gtk2-devel
BuildRequires:	libcurl-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libxml2-devel

%description
libopenraw is an ongoing project to provide a free software
implementation for camera RAW files decoding. One of the main reason is
that dcraw is not suited for easy integration into applications, and
there is a need for an easy to use API to build free software digital
image processing application.

%description -l zh_CN.UTF-8
解码数码相机的 RAW 文件。

%package gnome
Summary:	GUI components of %{name}
Summary(zh_CN.UTF-8): %{name} 的图形界面组件

Requires:	%{name} = %{version}-%{release}

%description gnome 
The %{name}-gnome package contains gui components of %{name}.

%description gnome -l zh_CN.UTF-8
%{name} 的图形界面组件。

%package devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包

Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package gnome-devel
Summary:	Development files for %{name}-gnome
Summary(zh_CN.UTF-8): %{name}-gnome 的开发包
Requires:	%{name}-gnome = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	pkgconfig

%description    gnome-devel
The %{name}-gnome-devel package contains libraries and header files for
developing applications that use %{name}-gnome.

%description gnome-devel -l zh_CN.UTF-8
%{name}-gnome 的开发包。

%package pixbuf-loader
Summary:	RAW image loader for GTK+ applications
Summary(zh_CN.UTF-8): GTK+ 程序的 RAW 图像载入器

Requires:	gtk2
Requires:	%{name} = %{version}-%{release}
Requires(post):   gdk-pixbuf2
Requires(postun): gdk-pixbuf2

%description pixbuf-loader
%{name}-pixbuf-loader contains a plugin to load RAW images, as created by
digital cameras, in GTK+ applications.

%description pixbuf-loader -l zh_CN.UTF-8
GTK+ 程序的 RAW 图像载入器。

%prep
%setup -q

%build
%configure --disable-static --enable-gnome

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -delete
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post gnome -p /sbin/ldconfig

%postun gnome -p /sbin/ldconfig

%post pixbuf-loader
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :


%postun pixbuf-loader
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :

%files
%doc AUTHORS
%doc ChangeLog
%doc COPYING
%doc NEWS
%doc README
%doc TODO 
%{_libdir}/%{name}.so.*

%files gnome
%{_libdir}/%{name}gnome.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}-1.0.pc

%dir %{_includedir}/%{name}-1.0
%{_includedir}/%{name}-1.0/%{name}/*.h

%files gnome-devel
%{_libdir}/%{name}gnome.so
%{_libdir}/pkgconfig/%{name}-gnome-1.0.pc

%dir %{_includedir}/%{name}-1.0/%{name}-gnome
%{_includedir}/%{name}-1.0/%{name}-gnome/gdkpixbuf.h

%files pixbuf-loader
%{_libdir}/gdk-pixbuf-2.0/*/loaders/*.so

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.0.9-3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.0.9-2
- 为 Magic 3.0 重建

* Sun Sep 30 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.0.9-1
- Updated to 0.0.9
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Switched to .bz2 sources
- Dropped included patches

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-7
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 24 2010 Christian Krause <chkr@fedoraproject.org> - 0.0.8-4
- fix %%post and %%postun scripts and install directory for
  pixbuf-loader

* Sun Oct 24 2010 Christian Krause <chkr@fedoraproject.org> - 0.0.8-3
- add upstream patch 22287584fbfa4657098ee997957a6c4fc972a53b to
  properly decompress CFA from certain cameras (BZ 624283)

* Wed Sep 08 2010 Christian Krause <chkr@fedoraproject.org> - 0.0.8-2
- add upstream patch 1b15acdcfdc4664bc6c0be473cb6e096071a4e62
  to support certain PEF files and to fix a crash when opening
  such files (BZ 606898)

* Sat Dec 05 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.0.8-1
- Version bump to 0.0.8.
  * Fixed a huge memory leak. (FreeDesktop Bugzilla #21435)
  * cfa output should write the data in PGM as big endian.
  * Better handling of Canon CR2 "slices" to fix crasher with Canon
    450D/Digital Rebel XSi files (and possibly others).
  * Added new API or_rawfile_new_from_memory() to load a Raw file from a
    memory buffer.
  * Added new API or_rawfile_get_typeid() and the associated consts.
  * Added new API or_rawdata_get_minmax().
  * Added new API or_get_file_extensions().
  * Added new API or_rawfile_get_rendered_image() to get a rendered image.
  * Added new API or_bitmapdata_*().
  * New GdkPixbuf loader.
  * Decompress NEF files.
- License changed to LGPLv3 or later.
- Missing includes fixed by upstream.
- Replaced 'BuildRequires: chrpath glib2-devel' with 'BuildRequires:
  exempi-devel libcurl-devel'.
- Added 'Requires: gtk2' to pixbuf-loader for directory ownership.
- Added a %%check stanza.

* Fri Jul 24 2009 Release Engineering <rel-eng@fedoraproject.org> - 0.0.5-4
- Autorebuild for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Caolán McNamara <caolanm@redhat.com> - 0.0.5-3
- add stdio.h for fopen and friends

* Wed Feb 25 2009 Release Engineering <rel-eng@fedoraproject.org> - 0.0.5-2
- Autorebuild for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 04 2008 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.5-1
- New upstream version.

* Wed Feb 20 2008 Release Engineering <rel-eng@fedoraproject.org> - 0.0.4-3
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.4-2
- Added missing dependency on libxml

* Wed Jan 30 2008 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.4-1
- New upstream version.

* Fri Dec 28 2007 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.3-1
- New upstream version.
- Updated license tag.
- Fixed rpath error.

* Thu May 03 2007 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.2-5
- Added unowned directory to list of files.
- Changed license from GPL to LGPL.

* Wed May 02 2007 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.2-4
- Moved gui components to a separate package.

* Tue May 01 2007 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.2-3
- Added missing BuildRequirement.

* Mon Apr 30 2007 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.2-2
- Added missing BuildRequirement.

* Sun Apr 29 2007 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.2-1
- Inital version.
