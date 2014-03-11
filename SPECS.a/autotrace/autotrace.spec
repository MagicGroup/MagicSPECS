Name:           autotrace
Version:        0.31.1
Release:        37%{?dist}
Summary:        Utility for converting bitmaps to vector graphics
Summary(zh_CN.UTF-8): 转换位图文件到向量图形的工具
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:        GPLv2+ and LGPLv2+
URL:            http://autotrace.sourceforge.net/
Source0:        http://download.sf.net/autotrace/autotrace-0.31.1.tar.gz
Patch1:         autotrace-0001-Modify-GetOnePixel-usage-to-build-against-current-Im.patch
Patch2:         autotrace-0002-Fixed-underquoted-AM_PATH_AUTOTRACE-definition.patch
Patch3:         autotrace-0003-libpng-fix.patch
# Sent upstream
Patch4:         autotrace-0.31.1-CVE-2013-1953.patch
Patch5:         autotrace-0.31.1-multilib-fix.patch
BuildRequires:  ImageMagick-devel
BuildRequires:  libpng-devel > 2:1.2
BuildRequires:  libexif-devel
BuildRequires:  libtiff-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libxml2-devel
BuildRequires:  bzip2-devel
BuildRequires:  freetype-devel
BuildRequires:  pstoedit-devel
# For autoreconf
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool


%description
AutoTrace is a program for converting bitmaps to vector graphics.

Supported input formats include BMP, TGA, PNM, PPM, and any format
supported by ImageMagick, whereas output can be produced in
Postscript, SVG, xfig, SWF, and others.

%description -l zh_CN.UTF-8
转换位图文件到向量图形的工具，支持的输入格式包括 BMP, TGA, PNM, PPM,
以及任何 ImageMagick 支持的格式，输出可以是 Postscript, SVG, xfig ,
SWF 和其它格式

%package devel
Summary:        Header files for autotrace
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       ImageMagick-devel
Requires:       pstoedit-devel


%description devel
This package contains header files and development libraries for autotrace.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch1 -p1 -b .GetOnePixel
%patch2 -p1 -b .aclocal18
%patch3 -p1 -b .libpng15
%patch4 -p1 -b .CVE-2013-1953
%patch5 -p1 -b .multilib-fix
autoreconf -ivf

%build
%configure

# remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING COPYING.LIB ChangeLog FAQ NEWS README THANKS TODO
%{_bindir}/autotrace
%{_libdir}/*.so.*
%{_mandir}/man[^3]/*

%files devel
%doc HACKING
%{_bindir}/autotrace-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/autotrace.pc
%{_includedir}/autotrace/
%{_datadir}/aclocal/autotrace.m4


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.31.1-36
- Fix building on AArch64
- Enable pstoedit back

* Fri Jul 19 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.31.1-35
- Fixed multilib conflict in devel package (by multilib-fix patch)
- Removed rpaths

* Fri Jun 28 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.31.1-34
- Fixed buffer overflow when parsing BMP files
  Resolves: CVE-2013-1953

* Mon Mar 18 2013 Jon Ciesla <limburgher@gmail.com> - 0.31.1-33
- ImageMagick rebuild.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.31.1-31
- Cosmetic changes in the spec-file (closes rhbz #803928 and #817950)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-30.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 02 2012 Jon Ciesla <limburgher@gmail.com> - 0.31.1-29.1
- Libpng 1.5 fix.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-28.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.31.1-27.1
- Rebuild for new libpng

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-26.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.31.1-25.1
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.31.1-24.1
- rebuild (ImageMagick)

* Mon May 17 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.31.1-24
- Changed description (closes rhbz #591659).

* Mon Jul 27 2009 Peter Lemenkov <lemenkov@gmail.com> - 0.31.1-23
- Removed static libraries from -devel
- Changed %%makeinstall to "make install DESTDIR=blablabla"
- Fixed rhbz# 477980

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Hans de Goede <hdegoede@redhat.com> - 0.31.1-21
- Rebuild for new ImageMagick

* Mon Mar 02 2009 Caolán McNamara <caolanm@redhat.com> - 0.31.1-20
- Modify GetOnePixel usage to build against current ImageMagick api

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.31.1-18
- fix license tag

* Mon May 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.31.1-17
- Rebuild for new ImageMagick.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.31.1-16
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Quentin Spencer <qspencer@users.sourceforge.net> - 0.31.1-15
- Rebuild for F8.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.31.1-14
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Quentin Spencer <qspencer@users.sourceforge.net> - 0.31.1-13
- Rebuild for FC6.

* Mon Feb 13 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-12
- Rebuild for Fedora Extras 5

* Sat Jan 28 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-11
- rebuild

* Tue Jan 17 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-10
- add BuildRequires on freetype-devel

* Tue Jan 17 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-9
- remove BuildRequires on XFree86-devel

* Mon Jan 16 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-8
- add %%{?dist} tag
- add a BuildRequires on bzip2-devel
- add ldconfig to %%post and %%postun

* Thu May 26 2005 Jeremy Katz <katzj@redhat.com> - 0.31.1-7
- and more buildrequires

* Thu May 26 2005 Jeremy Katz <katzj@redhat.com> - 0.31.1-6
- BR libtiff-devel

* Wed May 25 2005 Jeremy Katz <katzj@redhat.com> - 0.31.1-5
- rebuild

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Aug 21 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.31.1-3
- Temporarily changed buildreq pstoedit-devel to buildconflicts.

* Thu Apr 22 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.31.1-0.fdr.2
- Added new BuildReq pstoedit-devel.
- Added missing BuildReq libexif-devel.
- Added missing -devel requires pkgconfig, ImageMagick-devel.
- Converted spec file to UTF-8.

* Mon Sep 29 2003 Marius L. Johndal <mariuslj at ifi.uio.no> 0:0.31.1-0.fdr.1
- Initial RPM release.

