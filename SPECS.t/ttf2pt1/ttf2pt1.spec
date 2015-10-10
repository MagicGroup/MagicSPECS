Name: ttf2pt1
Version: 3.4.4
Release: 14%{?dist}
Summary: TrueType to Adobe Type 1 font converter
Summary(zh_CN.UTF-8): TrueType 到 Adobe Type 1 字体转换器

Group: Applications/Publishing
Group(zh_CN.UTF-8): 应用程序/出版
License: GPLv2+ and BSD with advertising
URL: http://%name.sourceforge.net
Source: http://download.sourceforge.net/%name/%name-%version.tgz
Patch0: ttf2pt1-destdir.patch
Patch1: ttf2pt1-freetype.patch
Patch2: ttf2pt1-sed.patch
Patch3: ttf2pt1-doc.patch
BuildRoot: %(mktemp -ud %_tmppath/%name-%version-%release-XXXXXX)

BuildRequires: freetype-devel >= 2.0.3
BuildRequires: perl
BuildRequires: fakeroot
BuildRequires: t1lib-devel

Requires: t1utils

%description
Ttf2pt1 is a font converter from the True Type format (and some other formats
supported by the FreeType library as well) to the Adobe Type1 format.

%description -l zh_CN.UTF-8
TrueType 到 Adobe Type 1 字体转换器。

%prep
%setup -q
%patch0
%patch1
%patch2
%patch3

%build
make CFLAGS_SYS='%optflags -D_GNU_SOURCE' CFLAGS_FT="`pkg-config --cflags freetype2`" LIBS_FT="`pkg-config --libs freetype2`" VERSION=%version all
rm -rf __dist_other
mkdir -p __dist_other/other
cp -p other/bz* other/Makefile other/README* __dist_other/other
make -C other cmpf dmpf

%install
rm -rf %buildroot
# The installation does explicit chown to root and chgrp to bin.
# Use fakeroot to avoid getting errors in the build.  RPM will
# make sure the ownership is correct in the final package.
fakeroot make DESTDIR=%buildroot INSTDIR=%_prefix TXTFILES= MANDIR=%_mandir VERSION=%version install
# Use the system t1asm from t1utils instead of a local version.
rm -r %buildroot/%_libexecdir
# Remove scripts only used during build
rm %buildroot%_datadir/%name/scripts/{convert,convert.cfg.sample,frommap,html2man,inst_dir,inst_file,mkrel,unhtml}
# Put tools in the standard path
mv %buildroot/%_datadir/%name/other/cmpf %buildroot/%_bindir/%{name}_cmpf
mv %buildroot/%_datadir/%name/other/dmpf %buildroot/%_bindir/%{name}_dmpf
cp other/cntstems.pl %buildroot/%_bindir/%{name}_cntstems
cp other/lst.pl %buildroot/%_bindir/%{name}_lst
cp other/showdf %buildroot/%_bindir/%{name}_showdf
cp other/showg %buildroot/%_bindir/%{name}_showg

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%doc CHANGES* README* FONTS FONTS.html COPYRIGHT app/TeX __dist_other/other
%doc scripts/convert.cfg.sample
%_bindir/%{name}*
%_datadir/%name
%exclude %_datadir/%name/app
%exclude %_datadir/%name/other
%_mandir/man1/*


%changelog
* Sun Oct 04 2015 Liu Di <liudidi@gmail.com> - 3.4.4-14
- 为 Magic 3.0 重建

* Thu Apr 17 2014 Liu Di <liudidi@gmail.com> - 3.4.4-13
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 3.4.4-12
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Oct 18 2008 Göran Uddeborg <goeran@uddeborg.se> 3.4.4-7
- Don't build in parallel.  Two calls of scripts/html2man on
  FONTS.html could step on each other toes.

* Tue Oct 14 2008 Göran Uddeborg <goeran@uddeborg.se> 3.4.4-6
- Install cmpf and dmpf with a ttf2pt1 prefix.
- Install scripts from "other" directory in the standard path with a
  ttf2pt1_ prefix.
- Update documentation with the new names and paths of the scripts,
  and remove any references to obsolete code not included in the
  package.

* Tue Sep 30 2008 Göran Uddeborg <goeran@uddeborg.se> 3.4.4-5
- Several updates from review (BZ 462446 up to comment 11)

* Mon Sep 29 2008 Göran Uddeborg <goeran@uddeborg.se> 3.4.4-4
- Moved example code to /usr/share/doc. (review BZ 462446)
- Excluded unused patch code for old XFree86 versions.

* Tue Sep 16 2008 Göran Uddeborg <goeran@uddeborg.se> 3.4.4-3
- Removed Swedish translations for public package

* Tue Sep 16 2008 Göran Uddeborg <goeran@uddeborg.se> 3.4.4-2
- Repackaged according to Fedora packaging guidelines

* Sun Sep  5 2004 Göran Uddeborg <goeran@uddeborg.se> 3.4.4-1
- Upgraded to 3.4.4.

* Tue Oct  7 2003 Göran Uddeborg <goeran@uddeborg.pp.se> 3.4.3-1
- Upgraded to 3.4.3.

* Tue Oct 15 2002 Göran Uddeborg <goeran@uddeborg.pp.se> 3.4.2-1
- Upgraded to 3.4.2.

* Thu Dec 27 2001 Göran Uddeborg <goeran@uddeborg.pp.se>
- Added build requirement on freetype-devel.

* Mon Nov 26 2001 Göran Uddeborg <goeran@uddeborg.pp.se>
- First RPM packaging.
