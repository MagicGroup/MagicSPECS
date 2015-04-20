
# re-enable pdf doc generation when/if ghostscript/texi2pdf is fixed,
# https://bugzilla.redhat.com/921706
# else, use pregenerated docs
%if 0%{?fedora} < 19
%define doc 1
%endif

Summary: Image Blending with Multiresolution Splines
Summary(zh_CN.UTF-8): 图像的多分辨率样条融合
Name: enblend
Version: 4.1.3
Release: 8%{?dist}
License: GPLv2+
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Source0: http://downloads.sourceforge.net/enblend/enblend-enfuse-%{version}.tar.gz
URL: http://enblend.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libtiff-devel boost-devel lcms2-devel plotutils-devel
BuildRequires: freeglut-devel glew-devel libjpeg-devel libpng-devel OpenEXR-devel
BuildRequires: libXmu-devel libXi-devel
BuildRequires: vigra-devel >= 1.9.0
BuildRequires: gsl-devel
%if 0%{?doc}
BuildRequires: transfig gnuplot tidy texinfo
BuildRequires: help2man ImageMagick texinfo-tex
%if 0%{?fedora} >= 17
BuildRequires: texlive-latex-fonts texlive-thumbpdf
%endif
%endif

# pregenerated info/pdf docs
Source1: enblend-enfuse-doc-4.1.2.tar.gz

Requires(post): info
Requires(preun): info

%description
Enblend is a tool for compositing images, given a set of images that overlap in
some irregular way, Enblend overlays them in such a way that the seam between
the images is invisible, or at least very difficult to see.  Enfuse combines
multiple images of the same subject into a single image with good exposure and
good focus.  Enblend and Enfuse do not line up the images for you, use a tool
like Hugin to do that.

%description -l zh_CN.UTF-8
图像的多分辨率样条融合。

%package doc
Summary: Usage Documentation for enblend and enfuse
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Documentation
Group(zh_CN.UTF-8): 文档

%description doc
PDF usage documentation for the enblend and enfuse command line tools

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n enblend-enfuse-%{version} %{!?doc:-a 1}

%build
sed -i 's/can_build_doc=yes/can_build_doc=no/g' configure
%ifarch mips64el
# Decrease debuginfo verbosity to reduce memory consumption even more
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

%configure --with-boost-filesystem

make %{?_smp_mflags}

%if 0%{?doc}
(cd doc && make pdf )
%endif


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%if 0%{?doc}
rm -f %{buildroot}%{_infodir}/dir
%else
install -m644 -p -D doc/enblend.info %{buildroot}%{_infodir}/enblend.info
install -m644 -p -D doc/enfuse.info %{buildroot}%{_infodir}/enfuse.info
%endif

magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post
/sbin/install-info %{_infodir}/enblend.info %{_infodir}/dir || :
/sbin/install-info %{_infodir}/enfuse.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/enblend.info %{_infodir}/dir || :
  /sbin/install-info --delete %{_infodir}/enfuse.info %{_infodir}/dir || :
fi

%files
%defattr(-, root, root)

%doc AUTHORS COPYING NEWS README

%{_bindir}/enblend
%{_bindir}/enfuse
%{_mandir}/man1/*
%{_infodir}/enblend.*
%{_infodir}/enfuse.*

%files doc
%defattr(-,root,root,-)
%doc COPYING doc/enblend.pdf doc/enfuse.pdf

%changelog
* Sun Mar 01 2015 Liu Di <liudidi@gmail.com> - 4.1.3-8
- 为 Magic 3.0 重建

* Sat Dec 27 2014 Liu Di <liudidi@gmail.com> - 4.1.3-7
- 为 Magic 3.0 重建

* Wed May 28 2014 Liu Di <liudidi@gmail.com> - 4.1.3-6
- 为 Magic 3.0 重建

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 4.1.3-5
- 为 Magic 3.0 重建

* Mon Mar 31 2014 Liu Di <liudidi@gmail.com> - 4.1.3-4
- 更新到 4.1.3

* Mon Dec 30 2013 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-4
- rebuild (vigra)

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.1.2-3
- rebuild (openexr)

* Mon Nov 18 2013 Dave Airlie <airlied@redhat.com> - 4.1.2-2
- rebuilt for GLEW 1.10

* Mon Oct 07 2013 Bruno Postle - 4.1.2-1
- stable release

* Sat Sep 14 2013 Bruno Wolff III <bruno@wolff.to> - 4.1.1-6
- Rebuild for ilmbase related soname bumps

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Petr Machata <pmachata@redhat.com> - 4.1.1-4
- Rebuild for boost 1.54.0

* Mon Mar 11 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.1.1-3
- avoid/fix pitfalls associated with texinfo-5.x (#919935)

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.1.1-2
- rebuild (OpenEXR)

* Fri Feb 15 2013 Bruno Postle - 4.1.1-1
- stable release

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 4.1-3
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 4.1-2
- Rebuild for Boost-1.53.0

* Sun Jan 20 2013 Bruno Postle <bruno@postle.net> - 4.1-1
- Upstream release
- No longer provides bundled(vigra)
- New enblend-doc sub package containing pdf documentation

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 4.0-17
- rebuild due to "jpeg8-ABI" feature drop

* Thu Dec 13 2012 Adam Jackson <ajax@redhat.com> - 4.0-16
- Rebuild for glew 1.9.0

* Tue Nov 13 2012 Dan Horák <dan[at]danny.cz> - 4.0-15
- fix FTBFS due new boost

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

* Sun Jan 28 2007 Bruno Postle <bruno@postle.net>
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

 
