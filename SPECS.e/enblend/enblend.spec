Summary: Image Blending with Multiresolution Splines
Name: enblend
Version: 4.0
Release: 17%{?dist}
License: GPLv2+
Group: Applications/Multimedia
Source: http://downloads.sourceforge.net/enblend/enblend-enfuse-%{version}.tar.gz
Patch0: enblend-enfuse-4.0-png14.patch
URL: http://enblend.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libtiff-devel boost-devel lcms-devel plotutils-devel
BuildRequires: freeglut-devel glew-devel libjpeg-devel libpng-devel OpenEXR-devel
Buildrequires: transfig gnuplot tidy texinfo

%if 0%{?fedora} >= 9
BuildRequires: libXmu-devel libXi-devel 
%endif
%if 0%{?rhl} >= 4
BuildRequires: xorg-x11-devel
%endif

Requires(post): info
Requires(preun): info

Provides: bundled(vigra) = 1.4.0

%description
Enblend is a tool for compositing images, given a set of images that overlap in
some irregular way, Enblend overlays them in such a way that the seam between
the images is invisible, or at least very difficult to see.  Enfuse combines
multiple images of the same subject into a single image with good exposure and
good focus.  Enblend and Enfuse do not line up the images for you, use a tool
like Hugin to do that.

%prep
%setup -q -n enblend-enfuse-4.0-753b534c819d
sed -i 's/info.arith_code = TRUE/info.arith_code = FALSE/' src/vigra_impex/jpeg.cxx
%patch0 -p0

%build
%configure --disable-static  LIBS="-lboost_filesystem -lboost_system"
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_infodir}/dir
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post
/usr/sbin/install-info %{_infodir}/enblend.info %{_infodir}/dir || :
/usr/sbin/install-info %{_infodir}/enfuse.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ] ; then
  /usr/sbin/install-info --delete %{_infodir}/enblend.info %{_infodir}/dir || :
  /usr/sbin/install-info --delete %{_infodir}/enfuse.info %{_infodir}/dir || :
fi

%files
%defattr(-, root, root)

%doc AUTHORS COPYING INSTALL NEWS README VIGRA_LICENSE

%{_bindir}/enblend
%{_bindir}/enfuse
%{_mandir}/man1/*
%{_infodir}/enblend.*
%{_infodir}/enfuse.*


%changelog
* Sun Apr 28 2013 Liu Di <liudidi@gmail.com> - 4.0-17
- 为 Magic 3.0 重建

* Sat Apr 20 2013 Liu Di <liudidi@gmail.com> - 4.0-16
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 4.0-15
- 为 Magic 3.0 重建

* Wed Aug 01 2012 Adam Jackson <ajax@redhat.com> - 4.0-14
- -Rebuild for new glew

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-12
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 07 2011 Bruno Postle <bruno@postle.net> - 4.0-10
- patch to build with new libpng

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 4.0-9
- Rebuild for new libpng

* Mon Jun 20 2011 ajax@redhat.com - 4.0-8
- Rebuild for new glew soname

* Fri Jun 17 2011 Bruno Postle <bruno@postle.net> - 4.0-7
- workaround vigra bug where arithmetic coded JPEG is always created with libjpeg-turbo

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 04 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 4.0-5
- rebuild for new boost

* Sat Feb 06 2010 Bruno Postle <bruno@postle.net> - 4.0-4
- add missing texinfo buildrequires

* Fri Feb 05 2010 Bruno Postle <bruno@postle.net> - 4.0-3
- Fixes for push to fedora

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild


* Wed Oct 08 2008 Bruno Postle <bruno@postle.net> - 3.2-2
- don't package /usr/share/info/dir

* Tue Sep 23 2008 Bruno Postle <bruno@postle.net> - 3.2-1
- upstream release

* Thu Jun 5 2008 Bruno Postle <bruno@postle.net> - 3.1-0.5.20080529cvs
- Add OpenEXR-devel build dependency

* Thu May 1 2008 Bruno Postle <bruno@postle.net> - 3.1-0.4.20080529cvs
- CVS snapshot with GCC 4.3 upstream fix

* Mon Apr 7 2008 Jef Spaleta <jspaleta AT fedoraproject Dot org> - 3.1-0.3.20080216cvs
- Patching for GCC 4.3

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.1-0.2.20080216cvs
- Autorebuild for GCC 4.3

* Sat Feb 16 2008 Bruno Postle <bruno@postle.net> 3.1-0.1.20090216cvs
  - CVS snapshot, 3.1 beta, tarball name change

* Mon Jan 21 2008 Bruno Postle <bruno@postle.net> 3.1-0.1.20090106cvs
  - CVS snapshot, 3.1 beta, switch to fedora cvs naming

* Sun Jan 06 2008 Bruno Postle <bruno@postle.net> 3.1-0cvs20090106
  - CVS snapshot, 3.1 beta

* Mon Aug 20 2007 Bruno Postle <bruno@postle.net> 3.0-6
  - glew is now in fedora, remove build-without-glew patch
  - update licence tag, GPL -> GPLv2+

* Tue Mar 20 2007 Bruno Postle <bruno@postle.net> 3.0-4
  - patch to build without glew library

* Sat Jan 28 2007 Bruno Postle <bruno@postle.net>
  - 3.0 release

* Tue Dec 13 2005 Bruno Postle <bruno@postle.net>
  - 2.5 release

* Tue Dec 06 2005 Bruno Postle <bruno@postle.net>
  - 2.4 release

* Mon Apr 18 2005 Bruno Postle <bruno@postle.net>
  - 2.3 release

* Mon Nov 15 2004 Bruno Postle <bruno@postle.net>
  - 2.1 release

* Mon Oct 18 2004 Bruno Postle <bruno@postle.net>
  - 2.0 release

* Wed Oct 13 2004 Bruno Postle <bruno@postle.net>
  - new build for fedora fc2

* Tue Jun 22 2004 Bruno Postle <bruno@postle.net>
  - found tarball of enblend-1.3 and updated to that

* Tue Jun 22 2004 Bruno Postle <bruno@postle.net>
  - added patch for reading nona multi-layer tiff files

* Tue Apr 27 2004 Bruno Postle <bruno@postle.net>
  - update to latest version

* Sat Apr 03 2004 Bruno Postle <bruno@postle.net>
  - update to latest version

* Tue Mar 09 2004 Bruno Postle <bruno@postle.net>
  - initial RPM

 
