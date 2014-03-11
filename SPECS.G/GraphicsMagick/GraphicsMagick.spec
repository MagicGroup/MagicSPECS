
# should seriously consider using this as default everywhere -- Rex
%global quantum_depth 16

Summary: An ImageMagick fork, offering faster image generation and better quality
Name: GraphicsMagick
Version: 1.3.16
Release: 2%{?dist}
License: MIT
Group: Applications/Multimedia
Source0: http://downloads.sourceforge.net/sourceforge/graphicsmagick/GraphicsMagick-%{version}.tar.xz
Url: http://www.graphicsmagick.org/
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

## upstreamable patches
Patch50: GraphicsMagick-1.3.14-perl_linkage.patch

BuildRequires: bzip2-devel
BuildRequires: freetype-devel
BuildRequires: jasper-devel
BuildRequires: lcms-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: librsvg2-devel
BuildRequires: libtiff-devel
BuildRequires: libungif-devel
BuildRequires: libwmf-devel
BuildRequires: libxml2-devel
BuildRequires: libX11-devel libXext-devel libXt-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: zlib-devel
## FIXME: %%check stuff
#BuildRequires: xorg-x11-server-Xvfb

# depend on stuff referenced below
# --with-gs-font-dir=%{_datadir}/fonts/default/Type1
Requires: urw-fonts

%description
GraphicsMagick is a comprehensive image processing package which is initially
based on ImageMagick 5.5.2, but which has undergone significant re-work by
the GraphicsMagick Group to significantly improve the quality and performance
of the software.

%package devel
Summary: Libraries and header files for GraphicsMagick app development
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
GraphicsMagick-devel contains the Libraries and header files you'll
need to develop GraphicsMagick applications. GraphicsMagick is an image
manipulation program.

If you want to create applications that will use GraphicsMagick code or
APIs, you need to install GraphicsMagick-devel as well as GraphicsMagick.
You do not need to install it if you just want to use GraphicsMagick,
however.

%package perl
Summary: GraphicsMagick perl bindings
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
Perl bindings to GraphicsMagick.

Install GraphicsMagick-perl if you want to use any perl scripts that use
GraphicsMagick.

%package c++
Summary: GraphicsMagick Magick++ library (C++ bindings)
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description c++
This package contains the GraphicsMagick++ library, a C++ binding to the 
GraphicsMagick graphics manipulation library.

Install GraphicsMagick-c++ if you want to use any applications that use 
GraphicsMagick++.

%package c++-devel
Summary: C++ bindings for the GraphicsMagick library
Group: Development/Libraries
Requires: %{name}-c++%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description c++-devel
GraphicsMagick-devel contains the Libraries and header files you'll
need to develop GraphicsMagick applications using the Magick++ C++ bindings.
GraphicsMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install GraphicsMagick-c++-devel, ImageMagick-devel and
GraphicsMagick.
You don't need to install it if you just want to use GraphicsMagick, or if you
want to develop/compile applications using the GraphicsMagick C interface,
however.

%prep
%setup -q

%patch50 -p1 -b .perl_linkage

iconv -f iso-8859-2 -t utf8 < ChangeLog > ChangeLog.utf8
mv -f ChangeLog.utf8 ChangeLog

# Avoid lib64 rpaths (FIXME: recheck this on newer releases)
%if "%{_libdir}" != "/usr/lib"
sed -i.rpath -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif

sed -i -e "s|BrowseDelegateDefault=.*|BrowseDelegateDefault=\'xdg-open\'|" configure


%build
%configure --enable-shared --disable-static \
           --with-lcms \
           --with-magick_plus_plus \
           --with-modules \
           --with-perl \
           --with-perl-options="INSTALLDIRS=vendor %{?perl_prefix}" \
           %{?quantum_depth:--with-quantum-depth=%{quantum_depth}} \
           --with-threads \
           --with-wmf \
           --with-x \
           --with-xml \
           --without-dps \
           --without-gslib \
           --with-gs-font-dir=%{_datadir}/fonts/default/Type1

make %{?_smp_mflags}
make %{?_smp_mflags} perl-build


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot} -C PerlMagick

# perlmagick: fix perl path of demo files
%{__perl} -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

find %{buildroot} -name "*.bs" |xargs rm -fv
find %{buildroot} -name ".packlist" |xargs rm -fv
find %{buildroot} -name "perllocal.pod" |xargs rm -fv

chmod 755 %{buildroot}%{perl_vendorarch}/auto/Graphics/Magick/Magick.so

# perlmagick: build files list
echo "%defattr(-,root,root)" > perl-pkg-files
find %{buildroot}/%{_libdir}/perl* -type f -print \
    | sed "s@^%{buildroot}@@g" > perl-pkg-files 
find %{buildroot}%{perl_vendorarch} -type d -print \
    | sed "s@^%{buildroot}@%dir @g" \
    | grep -v '^%dir %{perl_vendorarch}$' \
    | grep -v '/auto$' >> perl-pkg-files 
if [ -z perl-pkg-files ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi

rm -rf %{buildroot}%{_datadir}/GraphicsMagick
# Keep config
rm -rf %{buildroot}%{_datadir}/%{name}-%{version}/[a-b,d-z,A-Z]*
rm -vf  %{buildroot}%{_libdir}/lib*.la

# fix multilib issues
%ifarch x86_64 s390x ia64 ppc64 sparc64
%define wordsize 64
%else
%define wordsize 32
%endif

mv %{buildroot}%{_includedir}/GraphicsMagick/magick/magick_config.h \
   %{buildroot}%{_includedir}/GraphicsMagick/magick/magick_config-%{wordsize}.h

cat >%{buildroot}%{_includedir}/GraphicsMagick/magick/magick_config.h <<EOF
#ifndef ORBIT_MULTILIB
#define ORBIT_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "magick_config-32.h"
#elif __WORDSIZE == 64
# include "magick_config-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF
magic_rpm_clean.sh

%check
%if 0%{?test}
make check #|| cat PerlMagick/PerlMagickCheck.log ; make check-perl
%endif

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc Copyright.txt
%doc README.txt
%doc %{_datadir}/doc/%{name}/
%{_libdir}/libGraphicsMagick.so.3*
%{_libdir}/libGraphicsMagickWand.so.2*
%{_bindir}/[a-z]*
%{_libdir}/GraphicsMagick*
%{_datadir}/GraphicsMagick*
%{_mandir}/man[145]/[a-z]*

%files devel
%defattr(-,root,root,-)
%{_bindir}/GraphicsMagick-config
%{_bindir}/GraphicsMagickWand-config
%{_libdir}/libGraphicsMagick.so
%{_libdir}/libGraphicsMagickWand.so
%{_libdir}/pkgconfig/GraphicsMagick.pc
%{_libdir}/pkgconfig/GraphicsMagickWand.pc
%dir %{_includedir}/GraphicsMagick/
%{_includedir}/GraphicsMagick/magick/
%{_includedir}/GraphicsMagick/wand/
%{_mandir}/man1/GraphicsMagick-config.*
%{_mandir}/man1/GraphicsMagickWand-config.*

%post c++ -p /sbin/ldconfig
%postun c++ -p /sbin/ldconfig

%files c++
%defattr(-,root,root,-)
%{_libdir}/libGraphicsMagick++.so.3*

%files c++-devel
%defattr(-,root,root,-)
%{_bindir}/GraphicsMagick++-config
%{_includedir}/GraphicsMagick/Magick++/
%{_includedir}/GraphicsMagick/Magick++.h
%{_libdir}/libGraphicsMagick++.so
%{_libdir}/pkgconfig/GraphicsMagick++.pc
%{_mandir}/man1/GraphicsMagick++-config.*

%files perl -f perl-pkg-files
%defattr(-,root,root,-)
%{_mandir}/man3/*
%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.3.16-2
- 为 Magic 3.0 重建

* Tue Mar 27 2012 Liu Di <liudidi@gmail.com>
- 为 Magic 3.0 重建

* Tue Mar 27 2012 Liu Di <liudidi@gmail.com> - 1.3.14-2
- 为 Magic 3.0 重建

* Sun Feb 26 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.14-1
- 1.3.14

* Mon Jan 23 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.13-4
- -devel: omit seemingly extraneous dependencies

* Mon Jan 23 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.13-3
- BR: perl(ExtUtils::MakeMaker)

* Mon Jan 23 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.13-2
- Bad font configuration (#783906)
- re-introduce perl_linkage patch, fixes %%check

* Thu Jan 12 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.13-1
- 1.3.13

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.3.12-7
- Rebuild for new libpng

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3.12-6
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3.12-5
- Perl 5.14 mass rebuild

* Tue Apr 26 2011 Rex Dieter <rdieter@fedoraproject.org> 1.3.12-4
- delegates.mgk could use some care (#527117)
- -perl build is bad (#527143)
- wrong default font paths (#661664)
- need for 16-bit support, f16+ for now (#699414)
- tighten subpkg deps via %%_isa

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3.12-2
- Mass rebuild with perl-5.12.0

* Mon Mar 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.3.12-1
- GraphicsMagick-1.3.12

* Tue Feb 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.3.11-1
- GraphicsMagick-1.3.11

* Mon Dec 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.3.7-4
- CVE-2009-1882 (#503017)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.3.7-3
- rebuild against perl 5.10.1

* Fri Nov 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.3.7-2
- cleanup/uncruftify .spec

* Thu Sep 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.3.7-1
- GraphicsMagick-1.3.7

* Mon Aug  3 2009 Ville Skyttä <ville.skytta at iki.fi> - 1.3.6-2
- Use lzma-compressed upstream source tarball.

* Wed Jul 29 2009 Rex Dieter <rdieter@fedoraproject.org> 1.3.6-1
- GraphicsMagick-1.3.6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.3.5-1
- GraphicsMagick-1.3.5, ABI break (#487605)
- --without-libgs (for now, per upstream advice)
- BR: jasper-devel

* Tue Jun 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.15-1
- GraphicsMagick-1.1.15
- fix BuildRoot
- multiarch conflicts in GraphicsMagick (#341381)
- broken -L in GraphicsMagick.pc (#456466)
- %%files: track sonames

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.14-3
- own all files properly

* Thu Sep 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.14-2
- turns out we do need gcc43 patch

* Thu Sep 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.14-1
- update to 1.1.14
- fix perl issue (bz 454087)

* Sun Jun 01 2008 Dennis Gilmore <dennis@ausil.us> - 1.1.10-4
- sparc64 is a 64 bit arch

* Mon Feb 11 2008 Andreas Thienemann <andreas@bawue.net> - 1.1.10-3
- Added patch to include cstring instead of string, fixing gcc4.3 build issue

* Mon Feb 11 2008 Andreas Thienemann <andreas@bawue.net> - 1.1.10-2
- Rebuilt against gcc 4.3

* Mon Jan 28 2008 Andreas Thienemann <andreas@bawue.net> - 1.1.10-1
- Upgraded to 1.1.10
- Fixed linking problem with the Perl module. #365901

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.1.8-3
- Rebuild for selinux ppc32 issue.

* Sun Jul 29 2007 Andreas Thienemann <andreas@bawue.net> - 1.1.8-2
- Building without gslib support as it results in segfaults.

* Sat Jul 28 2007 Andreas Thienemann <andreas@bawue.net> - 1.1.8-1
- Update to new maintainance release 1.1.8

* Wed Mar 07 2007 Andreas Thienemann <andreas@bawue.net> - 1.1.7-7
- Fix potential CVE-2007-0770 issue.
- Added perl-devel BuildReq

* Fri Dec 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.1.7-6
- *really* fix magick_config-64.h (bug #217959)
- make buildable on rhel4 too.

* Fri Dec 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.1.7-5
- fix magick-config-64.h (bug #217959)

* Sun Nov 29 2006 Andreas Thienemann <andreas@bawue.net> - 1.1.7-3
- Fixed devel requirement.

* Sun Nov 26 2006 Andreas Thienemann <andreas@bawue.net> - 1.1.7-2
- Fixed various stuff

* Mon Jul 24 2006 Andreas Thienemann <andreas@bawue.net> - 1.1.7-1
- Initial Package for FE based on ImageMagick.spec
