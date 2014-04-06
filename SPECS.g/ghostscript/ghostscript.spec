%define gs_ver 9.10
%define gs_dot_ver 9.10
%{expand: %%define build_with_freetype %{?_with_freetype:1}%{!?_with_freetype:0}}
Summary: A PostScript interpreter and renderer
Summary(zh_CN.UTF-8): PostScript 解释器和渲染器
Name: ghostscript
Version: %{gs_ver}

Release: 6%{?dist}

# Included CMap data is Redistributable, no modification permitted,
# see http://bugzilla.redhat.com/487510
License: AGPLv3+ and Redistributable, no modification permitted
URL: http://www.ghostscript.com/
Group: Applications/Publishing
Group(zh_CN.UTF): 应用程序/出版
Source0: ghostscript-%{gs_ver}-cleaned.tar.bz2
# ghostscript contains a jpegxr directory containing code we cannot
# ship due to licensing concerns. Therefore we use this script to
# remove that directory before shipping it. Download the upstream
# tarball and invoke this script while in the tarball's directory:
Source1: generate-tarball.sh
Source2: CIDFnmap
Source4: cidfmap

Patch1: ghostscript-multilib.patch
Patch2: ghostscript-scripts.patch
Patch3: ghostscript-noopt.patch
Patch4: ghostscript-runlibfileifexists.patch
Patch5: ghostscript-icc-missing-check.patch
Patch6: ghostscript-Fontmap.local.patch
Patch7: ghostscript-iccprofiles-initdir.patch
Patch8: ghostscript-gdevcups-debug-uninit.patch
Patch9: ghostscript-wrf-snprintf.patch
Patch10: ghostscript-gs694154.patch
Patch11: ghostscript-gs694809.patch
Patch12: ghostscript-duplex.patch

Requires: urw-fonts >= 1.1, ghostscript-fonts
Requires: poppler-data
BuildRequires: xz
BuildRequires: libjpeg-devel, libXt-devel
BuildRequires: zlib-devel, libpng-devel, unzip, gtk3-devel
BuildRequires: glib2-devel, gnutls-devel
# Omni requires libxml
BuildRequires: libxml2-devel
BuildRequires: libtiff-devel
BuildRequires: cups-devel >= 1.1.13
BuildRequires: libtool
BuildRequires: jasper-devel
BuildRequires: dbus-devel
BuildRequires: poppler-data
BuildRequires: lcms2-devel >= 2.4-5
BuildRequires: openjpeg-devel
%{?_with_freetype:BuildRequires: freetype-devel}
BuildRoot: %{_tmppath}/%{name}-%{gs_ver}-root

# See bug #83516.
Conflicts: ttfonts-ja < 1.2-23
Conflicts: ttfonts-ko < 1.0.11-27
Conflicts: ttfonts-zh_CN < 2.12-2
Conflicts: ttfonts-zh_TW < 2.11-20

%description
Ghostscript is a set of software that provides a PostScript
interpreter, a set of C procedures (the Ghostscript library, which
implements the graphics capabilities in the PostScript language) and
an interpreter for Portable Document Format (PDF) files. Ghostscript
translates PostScript code into many common, bitmapped formats, like
those understood by your printer or screen. Ghostscript is normally
used to display PostScript files and to print PostScript files to
non-PostScript printers.

If you need to display PostScript files or print them to
non-PostScript printers, you should install ghostscript. If you
install ghostscript, you also need to install the ghostscript-fonts
package.

%description -l zh_CN.UTF-8
Postscripts 解释器和渲染器。

%package devel
Summary: Files for developing applications that use ghostscript
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name} = %{version}-%{release}
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description devel
The header files for developing applications that use ghostscript.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: Documentation for ghostscript
Summary(zh_CN.UTF-8): %{name} 的文档
Requires: %{name} = %{version}-%{release}
Group: Documentation
Group(zh_CN.UTF): 文档
BuildArch: noarch

%description doc
The documentation files that come with ghostscript.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%package gtk
Summary: A GTK-enabled PostScript interpreter and renderer
Summary(zh_CN.UTF-8): 使用 GTK 的 PostScript 解释器和渲染器
Requires: %{name} = %{version}-%{release}
Group: Applications/Publishing
Group(zh_CN.UTF): 应用程序/出版

%description gtk
A GTK-enabled version of Ghostscript, called 'gsx'.

%description gtk -l zh_CN.UTF-8
使用 GTK 的 PostScript 解释器和渲染器，命名为 gsx。

%prep
%setup -q -n %{name}-%{gs_ver}
rm -rf expat freetype icclib jasper jpeg jpegxr lcms lcms2 libpng openjpeg zlib cups/libs

# Fix ijs-config not to have multilib conflicts (bug #192672)
%patch1 -p1 -b .multilib

# Fix some shell scripts
%patch2 -p1 -b .scripts

# Build igcref.c with -O0 to work around bug #150771.
%patch3 -p1 -b .noopt

# Define .runlibfileifexists.
%patch4 -p1

# Fixed missing error check when setting ICC profile.
%patch5 -p1 -b .icc-missing-check

# Restored Fontmap.local patch, incorrectly dropped after
# ghostscript-8.15.4-3 (bug #610301).
# Note: don't use -b here to avoid the backup file ending up in the
# package manifest.
%patch6 -p1

# Don't assume %%rom%% device is available for initial ICC profile dir.
%patch7 -p1 -b .iccprofiles-initdir

# gdevcups: don't use uninitialized variables in debugging output.
%patch8 -p1 -b .gdevcups-debug-uninit

# Use more caution when converting floats to strings (bug #980085).
%patch9 -p1 -b .wrf-snprintf

# Use upstream patch to fix gs segfault (bug #1036428).
%patch10 -p1 -b .gs694154

# Use upstream patch to fix gs segfault (bug #1039718).
%patch11 -p1 -b .gs694809

# Use upstream patch to fix duplex for some devices (bug #1068896).
%patch12 -p1 -b .duplex

# Convert manual pages to UTF-8
from8859_1() {
        iconv -f iso-8859-1 -t utf-8 < "$1" > "${1}_"
        mv "${1}_" "$1"
}
for i in man/de/*.1; do
  if [ "$(file --brief --mime-encoding "$i")" = iso-8859-1 ]; then
    from8859_1 "$i"
  fi
done

# Convert ps files to UTF-8
for i in examples/cjk/gsc*.ps; do from8859_1 "$i"; done

%build
# Compile without strict aliasing opts due to these files:
# gdevescv.c gdevl4v.c gdevopvp.c gdevbbox.c gdevdbit.c gdevddrw.c 
# gdevp14.c gdevpdfd.c gdevpdfi.c gdevpdfo.c gdevpdft.c gdevpdfv.c 
# gdevpdte.c gdevpdtt.c gdevps.c gdevpx.c gscoord.c gscparam.c gscrd.c 
# gsdps1.c gsimage.c gspath1.c gsptype1.c gsptype2.c gstype2.c 
# gstype42.c gxccache.c gxchar.c gxclimag.c gxclpath.c gxfcopy.c 
# gximag3x.c gximage3.c gxipixel.c gxshade1.c gxstroke.c gxtype1.c 
# ibnum.c iscanbin.c zchar1.c zchar.c zcharx.c zfapi.c zfont32.c 
# zfunc0.c zfunc3.c zfunc4.c zpcolor.c zshade.c
EXTRACFLAGS="-fno-strict-aliasing"

FONTPATH=
for path in \
        %{_datadir}/fonts/default/%{name} \
        %{_datadir}/fonts/default/Type1 \
        %{_datadir}/fonts/default/amspsfnt/pfb \
        %{_datadir}/fonts/default/cmpsfont/pfb \
        %{_datadir}/fonts \
        %{_datadir}/%{name}/conf.d \
        %{_sysconfdir}/%{name} \
        %{_sysconfdir}/%{name}/%{gs_dot_ver} \
        %{_datadir}/poppler/cMap/*
do
  FONTPATH="$FONTPATH${FONTPATH:+:}$path"
done
autoconf --force
%configure --with-ijs --enable-dynamic --with-fontpath="$FONTPATH" \
        --with-drivers=ALL --disable-compile-inits --with-system-libtiff \
        --with-install-cups \
        CFLAGS="$CFLAGS $EXTRACFLAGS"

# Build IJS
cd ijs
./autogen.sh
%configure --enable-shared --disable-static
make
cd ..

%if %{build_with_freetype}
FT_CFLAGS=$(pkg-config --cflags freetype2)
make so RPM_OPT_FLAGS="$RPM_OPT_FLAGS $EXTRACFLAGS" prefix=%{_prefix} \
        FT_BRIDGE=1 FT_CFLAGS="$FT_CFLAGS" FT_LIB=freetype
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS $EXTRACFLAGS" prefix=%{_prefix} \
        FT_BRIDGE=1 FT_CFLAGS="$FT_CFLAGS" FT_LIB=freetype
%else
make so RPM_OPT_FLAGS="$RPM_OPT_FLAGS $EXTRACFLAGS" prefix=%{_prefix}
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS $EXTRACFLAGS" prefix=%{_prefix}
%endif
make cups

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%{_mandir},%{_bindir},%{_datadir},%{_docdir}}
mkdir -p $RPM_BUILD_ROOT/{%{_libdir},%{_includedir}/ijs}

make install soinstall \
%{?_with_freetype:FT_BRIDGE=1} \
        prefix=$RPM_BUILD_ROOT%{_prefix} \
        mandir=$RPM_BUILD_ROOT%{_mandir} \
        datadir=$RPM_BUILD_ROOT%{_datadir} \
        gsincludedir=$RPM_BUILD_ROOT%{_includedir}/ghostscript/ \
        bindir=$RPM_BUILD_ROOT%{_bindir} \
        libdir=$RPM_BUILD_ROOT%{_libdir} \
        docdir=$RPM_BUILD_ROOT%{_docdir}/%{name}-%{gs_dot_ver} \
        gsdir=$RPM_BUILD_ROOT%{_datadir}/%{name} \
        gsdatadir=$RPM_BUILD_ROOT%{_datadir}/%{name}/%{gs_dot_ver} \
        gssharedir=$RPM_BUILD_ROOT%{_libdir}/%{name}/%{gs_dot_ver} \
        CUPSSERVERROOT=$RPM_BUILD_ROOT`cups-config --serverroot` \
        CUPSSERVERBIN=$RPM_BUILD_ROOT`cups-config --serverbin` \
        CUPSDATA=$RPM_BUILD_ROOT`cups-config --datadir`

mv -f $RPM_BUILD_ROOT%{_bindir}/gsc $RPM_BUILD_ROOT%{_bindir}/gs

cd ijs
%makeinstall
cd ..

echo ".so man1/gs.1" > $RPM_BUILD_ROOT/%{_mandir}/man1/ghostscript.1
ln -sf gs $RPM_BUILD_ROOT%{_bindir}/ghostscript

# Rename an original cidfmap to cidfmap.GS
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/%{gs_dot_ver}/Resource/Init/cidfmap{,.GS}
# Install our own cidfmap to allow the separated
# cidfmap which the font packages own.
install -m0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{name}/%{gs_dot_ver}/Resource/Init/CIDFnmap
install -m0644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/%{name}/%{gs_dot_ver}/Resource/Init/cidfmap

# Documentation
install -m0644 doc/COPYING $RPM_BUILD_ROOT%{_docdir}/%{name}-%{gs_dot_ver}

# Don't ship libtool la files.
rm -f $RPM_BUILD_ROOT%{_libdir}/libijs.la

# Don't ship ijs example client or server
rm -f $RPM_BUILD_ROOT%{_bindir}/ijs_{client,server}_example

# Don't ship URW fonts; we already have them.
rm -rf $RPM_BUILD_ROOT%{_datadir}/ghostscript/%{gs_dot_ver}/Resource/Font

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ghostscript/%{gs_dot_ver}
touch $RPM_BUILD_ROOT%{_sysconfdir}/ghostscript/%{gs_dot_ver}/Fontmap.local
touch $RPM_BUILD_ROOT%{_sysconfdir}/ghostscript/%{gs_dot_ver}/cidfmap.local
touch $RPM_BUILD_ROOT%{_sysconfdir}/ghostscript/%{gs_dot_ver}/CIDFnmap.local

# The man/de/man1 symlinks are broken (bug #66238).
find $RPM_BUILD_ROOT%{_mandir}/de/man1 -type l | xargs rm -f

# Don't ship fixmswrd.pl as it pulls in perl (bug #463948).
rm -f $RPM_BUILD_ROOT%{_bindir}/fixmswrd.pl

# Don't ship CMaps (instead poppler-data paths are in search path).
rm -f $RPM_BUILD_ROOT%{_datadir}/ghostscript/%{gs_dot_ver}/Resource/CMap/*

MAIN_PWD=`pwd`
(cd $RPM_BUILD_ROOT; find .%{_datadir}/ghostscript/%{gs_dot_ver}/Resource -type f | \
                sed -e 's/\.//;' | grep -v Fontmap | grep -v gs_init.ps > $MAIN_PWD/rpm.sharelist
 find .%{_bindir}/ | sed -e 's/\.//;' | \
                grep -v '/$\|/hpijs$\|/gsx$\|/ijs-config$' \
                >> $MAIN_PWD/rpm.sharelist)
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f rpm.sharelist
%defattr(-,root,root)
%dir %{_sysconfdir}/ghostscript
%dir %{_sysconfdir}/ghostscript/%{gs_dot_ver}
%dir %{_datadir}/ghostscript/%{gs_dot_ver}
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/Init
%config %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/Init/gs_init.ps
%config %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/Init/Fontmap*
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/CMap
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/CIDFont
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/CIDFSubst
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/ColorSpace
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/Decoding
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/Encoding
%dir %{_datadir}/ghostscript/%{gs_dot_ver}/Resource/SubstCID
%{_datadir}/ghostscript/%{gs_dot_ver}/lib
%{_datadir}/ghostscript/%{gs_dot_ver}/iccprofiles
%{_mandir}/man*/*
%lang(de) %{_mandir}/de/man*/*
%{_libdir}/libgs.so.*
%{_libdir}/libijs-*.so*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/%{gs_dot_ver}
%config(noreplace) %{_sysconfdir}/ghostscript/%{gs_dot_ver}/*

%files doc
%defattr(-,root,root)
%doc %{_datadir}/ghostscript/%{gs_dot_ver}/examples
%doc %{_docdir}/%{name}-%{gs_dot_ver}

%files gtk
%defattr(-,root,root)
%{_bindir}/gsx

%files devel
%defattr(-,root,root)
%dir %{_includedir}/ghostscript
%{_includedir}/ghostscript/*.h
%dir %{_includedir}/ijs
%{_includedir}/ijs/*
%{_bindir}/ijs-config
%{_libdir}/pkgconfig/ijs.pc
%{_libdir}/libijs.so
%{_libdir}/libgs.so

%changelog
* Thu Feb 27 2014 Tim Waugh <twaugh@redhat.com> 9.10-6
- Use upstream patch to fix duplex for some devices (bug #1068896).

* Tue Dec 10 2013 Tim Waugh <twaugh@redhat.com> 9.10-5
- Use upstream patches to fix gs segfaults (bug #1026428, bug #1039718).

* Wed Sep 25 2013 Tim Waugh <twaugh@redhat.com> 9.09-4
- Regenerate tarball (bug #1000387).

* Wed Aug 28 2013 Tim Waugh <twaugh@redhat.com> 9.09-3
- Remove jpegxr to ensure it isn't built (bug #1000387).

* Thu Aug 22 2013 Tim Waugh <twaugh@redhat.com> 9.09-2
- Fixed character set conversion issue in pdfwrite (bug #999927).

* Thu Aug 22 2013 Tim Waugh <twaugh@redhat.com> 9.09-1
- 9.09.

* Sat Aug 17 2013 Tim Waugh <twaugh@redhat.com> 9.09-0.rc1.1
- 9.09rc1.

* Thu Aug 15 2013 Tim Waugh <twaugh@redhat.com> 9.08-1
- 9.08.

* Mon Aug 12 2013 Tim Waugh <twaugh@redhat.com> 9.08-0.rc1.1
- 9.08rc1.  CUPS filters moved to the cups-filters package.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.07-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Tim Waugh <twaugh@redhat.com> 9.07-11
- Remove bundled (and unused) lcms source.
- Fixed license tag (AGPLv3+).

* Wed Jul 17 2013 Tim Waugh <twaugh@redhat.com> 9.07-10
- Added in missing part of gs_sprintf backport: add in the header to
  stdio_.h. Without this there are problems with va_args on some
  platforms (bug #979681).

* Mon Jul  8 2013 Tim Waugh <twaugh@redhat.com> 9.07-9
- Upstream patch from bug #693921 to avoid zfapi crash (bug #969785).

* Mon Jul  1 2013 Tim Waugh <twaugh@redhat.com> 9.07-8
- Use correct colord device ID in gstoraster.

* Mon Jul  1 2013 Tim Waugh <twaugh@redhat.com> 9.07-7
- Use more caution when converting floats to strings (bug #980085).

* Tue Jun 18 2013 Tim Waugh <twaugh@redhat.com> 9.07-6
- Upstream patch from bug #690692 to handle strange fonts (bug #969660).

* Fri May 17 2013 Tim Waugh <twaugh@redhat.com> 9.07-5
- Remove pdfopt man pages which were mistakenly left in (bug #963882).

* Thu May 16 2013 Tim Waugh <twaugh@redhat.com> 9.07-4
- Upstream patch to fix pdfwrite segfault (bug #962120).

* Thu May  9 2013 Tim Waugh <twaugh@redhat.com> - 9.07-3
- Back-ported locale fix (bug #961149).

* Thu Apr 25 2013 Tim Waugh <twaugh@redhat.com>
- Unowned directories (bug #902525).

* Mon Apr  8 2013 Tim Waugh <twaugh@redhat.com> - 9.07-2
- Rebuilt.

* Fri Mar  8 2013 Tim Waugh <twaugh@redhat.com> - 9.07-1
- 9.07.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.06-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 9.06-6
- rebuild due to "jpeg8-ABI" feature drop

* Fri Jan  4 2013 Tim Waugh <twaugh@redhat.com> - 9.06-5
- Updated build requirement from gtk2-devel to gtk3-devel so that gsx
  gets built using the correct loader (bug #884483).

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 9.06-4
- rebuild against new libjpeg

* Thu Sep 27 2012 Tim Waugh <twaugh@redhat.com> - 9.06-3
- Remove cups/libs to avoid bundling, although it isn't built in any
  case.

* Tue Sep  4 2012 Tim Waugh <twaugh@redhat.com> - 9.06-2
- Fixed encoding of German ps2pdf man page (bug #853764).

* Wed Aug  8 2012 Tim Waugh <twaugh@redhat.com> - 9.06-1
- 9.06.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Tim Waugh <twaugh@redhat.com> - 9.05-4
- Ship pkg-config file for ijs (bug #840830).

* Mon Apr 30 2012 Tim Waugh <twaugh@redhat.com> - 9.05-3
- Removed more bundled packages (bug #816747).
- Fixed missing error check when setting ICC profile.

* Thu Apr 26 2012 Jon Ciesla <limburgher@gmail.com> - 9.05-2
- Fixed encodings and changelog version for merge review BZ 225795.

* Thu Feb  9 2012 Tim Waugh <twaugh@redhat.com> 9.05-1.1
- Avoid mixed tabs and spaces in spec file.

* Thu Feb  9 2012 Tim Waugh <twaugh@redhat.com> 9.05-1
- 9.05.

* Fri Jan  6 2012 Tim Waugh <twaugh@redhat.com> 9.04-9
- Use %%_cups_serverbin macro.

* Fri Jan  6 2012 Tim Waugh <twaugh@redhat.com> 9.04-8
- Rebuilt for GCC 4.7.

* Tue Nov  8 2011 Tim Waugh <twaugh@redhat.com> 9.04-7
- Applied fix for type 1 font copying code SEAC scanner (bug #728710).

* Mon Nov  7 2011 Tim Waugh <twaugh@redhat.com> 9.04-6
- Rebuilt for new libpng.

* Tue Nov  1 2011 Tim Waugh <twaugh@redhat.com> 9.04-5
- Applied upstream fix for skipping "cached" outline glyphs (bug #742349).

* Wed Aug 31 2011 Tim Waugh <twaugh@redhat.com> 9.04-4
- Fixed typo (EXTRAFLAGS -> EXTRACFLAGS).

* Mon Aug 22 2011 Tim Waugh <twaugh@redhat.com> 9.04-3
- Updated upstream fix for gdevcups RGBW handling (Ghostscript bug #691922).

* Tue Aug 16 2011 Tim Waugh <twaugh@redhat.com> 9.04-2
- Applied upstream fix for gdevcups handling of RGBW (Ghostscript
  bug #691922).

* Mon Aug  1 2011 Tim Waugh <twaugh@redhat.com> 9.04-1
- 9.04.

* Mon Aug  1 2011 Tim Waugh <twaugh@redhat.com> 9.02-5
- No longer need jbig2-image-refcount patch.
- Fixed error reporting in the gstoraster filter.

* Wed May 25 2011 Tim Waugh <twaugh@redhat.com> 9.02-4
- colord is optional (bug #706619).

* Tue Apr 12 2011 Tim Waugh <twaugh@redhat.com> 9.02-3
- Prevent segfault when running gstoraster outside CUPS.

* Thu Apr  7 2011 Tim Waugh <twaugh@redhat.com>
- Remove bundled expat directory.  Not used, but this makes it
  clearer.

* Wed Apr  6 2011 Tim Waugh <twaugh@redhat.com> 9.02-2
- pxl: match landscape page sizes (bug #692165).

* Mon Apr  4 2011 Tim Waugh <twaugh@redhat.com>
- Fixed source URL.

* Mon Apr  4 2011 Tim Waugh <twaugh@redhat.com> 9.02-1
- 9.02.

* Thu Mar 10 2011 Tim Waugh <twaugh@redhat.com> 9.01-3
- colord support: prefix printer name with "cups-" to get device ID.

* Thu Feb 10 2011 Richard Hughes <rhughes@redhat.com> 9.01-2
- Backport a patch from svn trunk to enable colord support.

* Thu Feb 10 2011 Tim Waugh <twaugh@redhat.com> 9.01-1
- 9.01.  No longer needed gdevcups-691733, glyph-stretch-691920,
  icc-fix, scan_token, or system-jasper patches.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.00-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Tim Waugh <twaugh@redhat.com> 9.00-13
- Applied fix for upstream bug #691920.

* Fri Jan 28 2011 Tim Waugh <twaugh@redhat.com> 9.00-12
- Use poppler-data for CMaps (bug #630632).

* Mon Jan 17 2011 Tim Waugh <twaugh@redhat.com> 9.00-11
- Fixed macro in comment.
- Include full source URL.

* Fri Jan 14 2011 Tim Waugh <twaugh@redhat.com> 9.00-10
- Avoid symbol clash with scan_token (bug #590914).

* Mon Jan 10 2011 Tim Waugh <twaugh@redhat.com> 9.00-9
- Replaced width-and-height patch with the one actually used upstream.

* Fri Jan  7 2011 Tim Waugh <twaugh@redhat.com> 9.00-8
- Applied upstream ICC fix (bug #655449).
- gdevcups: use correct width and height values when allocating memory
  (upstream bug 691733).

* Fri Nov 26 2010 Tim Waugh <twaugh@redhat.com> 9.00-7
- Fixed more summaries ending with ".".

* Thu Oct 21 2010 Tim Waugh <twaugh@redhat.com> 9.00-6
- Own more directories (bug #645075).

* Thu Oct 14 2010 Tim Waugh <twaugh@redhat.com> 9.00-5
- gdevcups: don't use uninitialized variables in debugging output
  (Ghostscript bug #691683).

* Fri Oct  1 2010 Tim Waugh <twaugh@redhat.com> 9.00-4
- Reverted incorrect change introduced to fix bug #635786.

* Thu Sep 30 2010 Tim Waugh <twaugh@redhat.com> 9.00-3
- Don't use carriage return in ps2epsi output (bug #635786).
- Include more documentation (bug #634354).

* Wed Sep 29 2010 jkeating - 9.00-2
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Tim Waugh <twaugh@redhat.com> 9.00-1
- Updated to 9.00.  No longer need -P-, CVE-2009-4270, CVE-2010-1628,
  SEARCH_HERE_FIRST, bbox-close, cups-realloc-color-depth,
  epstopdf-failure, fPIC, gdevcups-ripcache, iname-segfault, ldfalgs,
  pdf2dsc, pdftoraster-exit, tif-fail-close, tiff-default-strip-size,
  or tiff-fixes patches.

* Mon Sep 13 2010 Tim Waugh <twaugh@redhat.com> 8.71-16
- Pulled in gs_fonts.ps modification for .runlibfileifexists from
  OpenSUSE package (bug #610301).

* Fri Sep  3 2010 Tim Waugh <twaugh@redhat.com> 8.71-15
- Restored Fontmap.local patch, incorrectly dropped after
  ghostscript-8.15.4-3 (bug #610301).
- Applied patch to let gdevcups use automatic memory allocation.  Use
  RIPCache=auto in /etc/cups/cupsd.conf to enable.
- Applied patch to fix NULL dereference in bbox driver (bug #591624).
- Applied upstream patch to fix iname.c segfault (bug #465311).

* Thu Aug 26 2010 Tim Waugh <twaugh@redhat.com> 8.71-14
- Avoid epstopdf failure using upstream patch (bug #627390).
- More upstream fixes for bug #599564.

* Wed Aug 25 2010 Tim Waugh <twaugh@redhat.com> 8.71-13
- Fix implementation of -P- (bug #599564).
- Use -P- and -dSAFER in scripts (bug #599564).

* Wed Aug 25 2010 Tim Waugh <twaugh@redhat.com> 8.71-12
- Change SEARCH_HERE_FIRST default to make -P- default instead of -P
  (bug #599564).
- Removed redundant gs-executable patch (bug #502550).

* Thu Aug  5 2010 Tim Waugh <twaugh@redhat.com> 8.71-11
- Avoid another NULL pointer dereference in jbig2 code (bug #621569).

* Fri Jul 16 2010 Tim Waugh <twaugh@redhat.com> 8.71-10
- Applied patch to fix CVE-2010-1628 (memory corruption at PS stack
  overflow, bug #592492).

* Tue Mar 16 2010 Tim Waugh <twaugh@redhat.com> 8.71-9
- Backported some more TIFF fixes (bug #573970).
- Use upstream fix for TIFF default strip size (bug #571520).

* Mon Mar 15 2010 Tim Waugh <twaugh@redhat.com> 8.71-8
- Restore the TIFF default strip size of 0 (bug #571520).
- Don't segfault closing tiffg3 device if opening failed (bug #571520).
- Don't revert gdevcups y-axis change (bug #541604).
- Reallocate memory in gdevcups when color depth changes (bug #563313).

* Fri Mar  5 2010 Tim Waugh <twaugh@redhat.com> 8.71-7
- Don't own the %%{_datadir}/ghostscript or
  %%{_datadir}/ghostscript/conf.d directories as the filesystem
  package already does (bug #569442).

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> 8.71-6
- Fixed summary.
- Fixed macros in changelog.
- Avoid mixed spaces and tabs.
- Ship COPYING file.
- Added comments for all patches.
- More consistent macro use.

* Mon Feb 22 2010 Tim Waugh <twaugh@redhat.com> 8.71-5
- The doc subpackage is now noarch (bug #567179).

* Sat Feb 20 2010 Tim Waugh <twaugh@redhat.com> 8.71-4
- Actually revert the upstream gdevcups changes (bug #563313).
- Fixed pdf2dsc.ps (bug #565935).
- Use fixed patch for LDFLAGS to make sure libgs.so gets a soname
  (bug #565935).

* Fri Feb 19 2010 Tim Waugh <twaugh@redhat.com> 8.71-3
- Fixed LDFLAGS when building dynamically linked executables (bug #565935).

* Wed Feb 17 2010 Tim Waugh <twaugh@redhat.com> 8.71-2
- Use system libtiff.

* Wed Feb 17 2010 Tim Waugh <twaugh@redhat.com> 8.71-1
- 8.71 (bug #565935).

* Tue Feb 16 2010 Tim Waugh <twaugh@redhat.com> 8.70-7
- Reverted gdevcups duplex changes as they cause a regression
  (see bug #563313).

* Mon Jan 25 2010 Tim Waugh <twaugh@redhat.com> 8.70-6
- Fixed pdftoraster so that it waits for its sub-process to exit.
- Another gdevcups duplex fix from upstream revision 10631
  (bug #541604).

* Fri Jan 22 2010 Tim Waugh <twaugh@redhat.com> 8.70-5
- Don't build static library for ijs (bug #556051).

* Thu Jan 21 2010 Tim Waugh <twaugh@redhat.com> 8.70-4
- Fixed gdevcups duplex output (bug #541604) by backporting upstream
  revision 10625.

* Thu Dec 24 2009 Tim Waugh <twaugh@redhat.com> 8.70-3
- Don't ship libtool la files (bug #542674).
- Fix debugging output from gdevcups (CVE-2009-4270, bug #540760).
- Harden ghostscript's debugging output functions (bug #540760).

* Thu Oct 15 2009 Tim Waugh <twaugh@redhat.com> 8.70-2
- New cups sub-package for pstoraster/pdftoraster/pstopxl.

* Mon Aug  3 2009 Tim Waugh <twaugh@redhat.com> 8.70-1
- 8.70.
- License has changed to GPLv3+.  Packages containing programs that
  link to libgs/libijs are:
  - foomatic (GPLv2+)
  - libspectre (GPLv2+)
  - ImageMagick (ImageMagick, listed on Licensing wiki page under
    "Good Licenses" and marked as GPLv3 compat)
  - gutenprint (GPLv2+)

* Mon Aug  3 2009 Tim Waugh <twaugh@redhat.com> 8.64-12
- Moved examples to doc subpackage (bug #515167).
- Converted spec file to UTF-8.

* Thu Jul 30 2009 Tim Waugh <twaugh@redhat.com> 8.64-11
- Fixed CVE-2009-0583,0584 patch by using 255 as the maximum number of
  points, not 100, and by not treating a missing black point tag as an
  error (bug #487744).

* Thu Jul 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 8.64-10
- License: GPLv2 and Redistributable, no modification permitted (bug #487510)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.64-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Tim Waugh <twaugh@redhat.com> 8.64-8
- Fix scripts so they don't get broken on install (bug #502550).

* Thu Jun  4 2009 Tim Waugh <twaugh@redhat.com> 8.64-7
- Applied patch to fix NULL dereference in JBIG2 decoder (bug #503995).

* Wed Apr 15 2009 Tim Waugh <twaugh@redhat.com> 8.64-6
- Applied patch to fix CVE-2009-0792 (bug #491853).
- Applied patch to fix CVE-2009-0196 (bug #493379).

* Fri Mar 20 2009 Tim Waugh <twaugh@redhat.com> 8.64-5
- Applied patch to fix CVE-2009-0583 (bug #487742) and CVE-2009-0584
  (bug #487744).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.64-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Tim Waugh <twaugh@redhat.com> 8.64-3
- Fix bitcmyk driver (bug #486644).

* Wed Feb  4 2009 Tim Waugh <twaugh@redhat.com> 8.64-2
- 8.64 (bug #483958).
- Removed trade marks to avoid any potential confusion.

* Fri Oct 17 2008 Tim Waugh <twaugh@redhat.com>
- Removed last patch (unsuccessful).

* Fri Oct 17 2008 Tim Waugh <twaugh@redhat.com> 8.63-4
- Try out a work-around for bug #465311.

* Wed Oct 15 2008 Tim Waugh <twaugh@redhat.com> 8.63-3
- Don't ship fixmswrd.pl as it pulls in perl (bug #463948).

* Tue Oct 14 2008 Tim Waugh <twaugh@redhat.com> 8.63-2
- Split out a doc sub-package (bug #466507).

* Mon Aug  4 2008 Tim Waugh <twaugh@redhat.com> 8.63-1
- 8.63.  No longer need r8591 or incomplete-ccittfax patches.
- Compile without strict aliasing opts due to warnings across several
  files.
- Don't run autogen.sh for main package, just for ijs which doesn't
  ship with a configure script.

* Mon Jun 23 2008 Tim Waugh <twaugh@redhat.com> 8.62-4
- Applied patch to work around bug #229174.
- Applied patch from upstream to fix box_fill_path for shfill (bug #452348).

* Mon Mar 31 2008 Tim Waugh <twaugh@redhat.com> 8.62-3
- Fix pksmraw output (bug #308211).

* Tue Mar  4 2008 Tim Waugh <twaugh@redhat.com> 8.62-2
- No longer need CVE-2008-0411 patch.
- Don't ship URW fonts; we already have them.

* Tue Mar  4 2008 Tim Waugh <twaugh@redhat.com> 8.62-1
- 8.62.  No longer need IJS KRGB patch, or patch for gs bug 689577.

* Wed Feb 27 2008 Tim Waugh <twaugh@redhat.com> 8.61-10
- Applied patch to fix CVE-2008-0411 (bug #431536).

* Fri Feb 22 2008 Tim Waugh <twaugh@redhat.com> 8.61-9
- Build with jasper again (bug #433897).  Build requires jasper-devel, and
  a patch to remove jas_set_error_cb reference.

* Wed Feb 13 2008 Tim Waugh <twaugh@redhat.com> 8.61-8
- Rebuild for GCC 4.3.

* Mon Jan 28 2008 Tim Waugh <twaugh@redhat.com> 8.61-7
- Don't build with jasper support.
- Remove bundled libraries.

* Tue Dec 11 2007 Tim Waugh <twaugh@redhat.com> 8.61-6
- Applied upstream patch for bug #416321.

* Fri Nov 30 2007 Tim Waugh <twaugh@redhat.com> 8.61-5
- Fixed runlibfileifexists patch.

* Fri Nov 30 2007 Tim Waugh <twaugh@redhat.com> 8.61-4
- Revert previous change, but define .runlibfileifexists, not just
  runlibfileifexists.

* Wed Nov 28 2007 Tim Waugh <twaugh@redhat.com> 8.61-3
- No longer need runlibfileifexists.
- Use runlibfile in cidfmap.

* Wed Nov 28 2007 Tim Waugh <twaugh@redhat.com> 8.61-2
- Add /usr/share/fonts to fontpath (bug #402551).
- Restore cidfmap-switching bits, except for FAPIcidfmap which is no
  longer used.
- Add runlibfileifexists to gs_init.ps.
- Build with --disable-compile-inits (bug #402501).

* Fri Nov 23 2007 Tim Waugh <twaugh@redhat.com> 8.61-1
- 8.61.

* Tue Oct 23 2007 Tim Waugh <twaugh@redhat.com> 8.60-5
- Applied patch from upstream to fix CVE-2007-2721 (bug #346511).

* Tue Oct  9 2007 Tim Waugh <twaugh@redhat.com> 8.60-4
- Marked localized man pages as %%lang (bug #322321).

* Thu Sep 27 2007 Tim Waugh <twaugh@redhat.com> 8.60-3
- Back-ported mkstemp64 patch (bug #308211).

* Thu Aug 23 2007 Tim Waugh <twaugh@redhat.com> 8.60-2
- More specific license tag.

* Fri Aug  3 2007 Tim Waugh <twaugh@redhat.com> 8.60-1
- 8.60.

* Mon Jul 16 2007 Tim Waugh <twaugh@redhat.com> 8.60-0.r8112.2
- Own %%{_libdir}/ghostscript (bug #246026).

* Tue Jul 10 2007 Tim Waugh <twaugh@redhat.com> 8.60-0.r8112.1
- 8.60 snapshot from svn.  Patches dropped:
  - big-cmap-post
  - split-cidfnmap
  - exactly-enable-cidfnmap
  - Fontmap.local
  No longer needed:
  - gxcht-64bit-crash

* Tue Apr 17 2007 Tim Waugh <twaugh@redhat.com> 8.15.4-3
- Apply fonts in CIDFnmap even if the same fontnames are already registered
  (bug #163231).
- New file CIDFmap (bug #233966).
- Allow local overrides for FAPIcidfmap, cidfmap and Fontmap (bug #233966).

* Tue Apr  3 2007 Tim Waugh <twaugh@redhat.com> 8.15.4-2
- Fixed configuration file locations (bug #233966).

* Wed Mar 14 2007 Tim Waugh <twaugh@redhat.com> 8.15.4-1
- 8.15.4.

* Thu Jan 25 2007 Tim Waugh <twaugh@redhat.com> 8.15.3-7
- dvipdf script fixes (bug #88906).
- Moved libijs.so and libgs.so into devel package (bug #203623).

* Wed Jan 24 2007 Tim Waugh <twaugh@redhat.com> 8.15.3-6
- Configure with --with-drivers=ALL since the advertised default is not
  what gets used (bug #223819).

* Thu Jan 18 2007 Tim Waugh <twaugh@redhat.com> 8.15.3-5
- Backported gxcht 64bit crash fix from GPL trunk (bug #177763).

* Fri Jan 12 2007 Tim Waugh <twaugh@redhat.com> 8.15.3-4
- Own cjkv directory (bug #221380, bug #222375).

* Tue Dec  5 2006 Tim Waugh <twaugh@redhat.com> 8.15.3-3
- Added split-cidfnmap patch (bug #194592).

* Thu Nov 16 2006 Tim Waugh <twaugh@redhat.com> 8.15.3-2
- 8.15.3.  No longer need gtk2, ps2epsi, badc, pagesize,
  use-external-freetype, split-font-configuration or cjkv patches.
- Renumbered patches.

* Tue Oct  3 2006 Tim Waugh <twaugh@redhat.com> 8.15.2-9
- Apply CJKV patch from svn164:165 plus the fix from svn173:174 (bug #194592,
  bug #203712, possibly bug #167596).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 8.15.2-8.1
- rebuild

* Fri Jun 23 2006 Tim Waugh <twaugh@redhat.com> 8.15.2-8
- Revert CJKV patch.

* Wed Jun 14 2006 Tomas Mraz <tmraz@redhat.com> - 8.15.2-7
- rebuilt with new gnutls

* Tue Jun 13 2006 Tim Waugh <twaugh@redhat.com> 8.15.2-6
- Undo svn sync.
- Apply CJKV patch from svn164:165.

* Fri Jun  9 2006 Tim Waugh <twaugh@redhat.com> 8.15.2-5
- Sync to svn165.

* Fri May 26 2006 Tim Waugh <twaugh@redhat.com> 8.15.2-4
- Fix ijs-config not to have multilib conflicts (bug #192672)

* Tue May  2 2006 Tim Waugh <twaugh@redhat.com> 8.15.2-3
- Remove adobe-cmaps and acro5-cmaps, since latest CMaps are already
  included (bug #190463).

* Tue Apr 25 2006 Tim Waugh <twaugh@redhat.com> 8.15.2-2
- 8.15.2.
- No longer need build, krgb, pdfwrite, str1570 patches.

* Mon Apr 24 2006 Tim Waugh <twaugh@redhat.com> 8.15.1-10
- Fix emacs interaction (bug #189321, STR #1570).

* Mon Apr 10 2006 Tim Waugh <twaugh@redhat.com> 8.15.1-9
- Add %%{_datadir}/fonts/japanese to font path (bug #188448).
- Spec file cleanups (bug #188066).

* Sat Apr  8 2006 Tim Waugh <twaugh@redhat.com>
- Build requires libtool (bug #188341).

* Thu Apr  6 2006 Tim Waugh <twaugh@redhat.com> 8.15.1-8
- Fix pdfwrite (bug #187834).
- CUPS filters go in /usr/lib/cups/filter even on lib64 platforms.

* Thu Mar  2 2006 Tim Waugh <twaugh@redhat.com> 8.15.1-7
- BuildRequires: gnutls-devel
- Updated KRGB patch for gdevijs.

* Tue Feb 28 2006 Karsten Hopp <karsten@redhat.de> 8.15.1-6
- BuildRequires: libXt-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 8.15.1-5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 8.15.1-5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Tim Waugh <twaugh@redhat.com> 8.15.1-5
- Updated adobe-cmaps to 200406 (bug #173613).

* Fri Jan 27 2006 Tim Waugh <twaugh@redhat.com> 8.15.1-4
- Support reading a big cmap/post table from a TrueType font.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> 8.15.1-3
- Build does not explicitly require xorg-x11-devel.

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> 8.15.1-2
- rebuilt with new openssl

* Mon Sep 26 2005 Tim Waugh <twaugh@redhat.com> 8.15.1-1
- Some directories should be "8.15" not "8.15.1" (bug #169198).

* Thu Sep 22 2005 Tim Waugh <twaugh@redhat.com> 8.15.1-0.1
- 8.15.1.
- No longer need overflow patch.

* Tue Aug 16 2005 Tim Waugh <twaugh@redhat.com> 8.15-0.rc4.3
- Rebuilt for new cairo.

* Mon Aug 15 2005 Tim Waugh <twaugh@redhat.com> 8.15-0.rc4.2
- Parametrize freetype, and disable it (bug #165962).

* Fri Aug 12 2005 Tim Waugh <twaugh@redhat.com> 8.15-0.rc4.1
- 8.15rc4.
- Fixed lips4v driver (bug #165713).

* Tue Aug  9 2005 Tim Waugh <twaugh@redhat.com> 8.15-0.rc3.7
- Install adobe/acro5 CMaps (bug #165428).

* Mon Jul 18 2005 Tim Waugh <twaugh@redhat.com> 8.15-0.rc3.6
- Fixed split font configuration patch (bug #161187).

* Wed Jul 13 2005 Tim Waugh <twaugh@redhat.com> 8.15-0.rc3.5
- Split font configuration (bug #161187).
- Reverted this change:
  - Build requires xorg-x11-devel, not XFree86-devel.

* Tue Jul 12 2005 Tim Waugh <twaugh@redhat.com> 8.15-0.rc3.4
- Add Japanese fonts to FAPIcidfmap (bug #161187).
- Moved Resource directory.
- Added use-external-freetype patch (bug #161187).

* Mon Jul 11 2005 Tim Waugh <twaugh@redhat.com>
- Build requires libtiff-devel (bug #162826).

* Thu Jun  9 2005 Tim Waugh <twaugh@redhat.com> 8.15-0.rc3.3
- Build requires xorg-x11-devel, not XFree86-devel.
- Include ierrors.h in the devel package.

* Wed Jun  8 2005 Tim Waugh <twaugh@redhat.com> 8.15-0.rc3.2
- Drop 'Provides: libijs.so' because it is incorrect.
- Build igcref.c with -O0 to work around bug #150771.
- Renumber patches.

* Fri Jun  3 2005 Tim Waugh <twaugh@redhat.com> 8.15-0.rc3.1
- Switch to ESP Ghostscript.
- 8.15rc3.
- Lots of patches dropped.  Perhaps some will need to be re-added.

* Thu Mar 10 2005 Tim Waugh <twaugh@redhat.com> 7.07-40
- Build igcref.c with -O0 to work around bug #150771.

* Tue Mar  1 2005 Tim Waugh <twaugh@redhat.com> 7.07-39
- Rebuilt for new GCC.

* Mon Feb 21 2005 Tim Waugh <twaugh@redhat.com> 7.07-38
- Fixes inspired by GCC 4.

* Tue Jan 18 2005 Tim Waugh <twaugh@redhat.com>
- Correct permissions for %%{_datadir}/ghostscript/Resource (bug #145420).

* Fri Dec 10 2004 Tim Waugh <twaugh@redhat.com> 7.07-37
- Fixed missing return statement (bug #136757).

* Thu Dec  9 2004 Tim Waugh <twaugh@redhat.com> 7.07-36
- Remove VFlib2 bits (bug #120498).

* Fri Dec  3 2004 Tim Waugh <twaugh@redhat.com> 7.07-35
- Added /etc/ghostscript to search path and to file manifest (bug #98974).

* Sat Nov 20 2004 Miloslav Trmac <mitr@redhat.com> - 7.07-34
- Convert man pages to UTF-8

* Wed Oct 20 2004 Tim Waugh <twaugh@redhat.com> 7.07-33
- Fix for bug #136322 (temporary files).

* Tue Sep 28 2004 Tim Waugh <twaugh@redhat.com> 7.07-32
- Turn off fontconfig until it's fixed (bug #133353).

* Wed Aug 18 2004 Tim Waugh <twaugh@redhat.com> 7.07-31
- Only ship gsx in the gtk subpackage.

* Fri Aug  6 2004 Tim Waugh <twaugh@redhat.com>
- Run /sbin/ldconfig in %%post/%%postun.
- Stricter requirements for the main package in the subpackages.

* Tue Jul 20 2004 Tim Waugh <twaugh@redhat.com> 7.07-30
- Updated eplaser driver to add alc4000 (bug #128007).

* Fri Jun 25 2004 Tim Waugh <twaugh@redhat.com> 7.07-29
- Prevent pdf2ps generating "null setpagesize" (bug #126446).

* Thu Jun 24 2004 Tim Waugh <twaugh@redhat.com> 7.07-28
- Fix Omni patch assumption about /usr/lib which breaks for multilib
  architectures.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  1 2004 Tim Waugh <twaugh@redhat.com> 7.07-26
- Removed another debug message from the fontconfig patch.

* Tue Mar  9 2004 Tim Waugh <twaugh@redhat.com> 7.07-25
- Added bjc250gs driver (bug #117860).

* Thu Mar  4 2004 Tim Waugh <twaugh@redhat.com> 7.07-24
- Fix compilation with GCC 3.4.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 18 2004 Tim Waugh <twaugh@redhat.com> 7.07-23
- Build against gtk2/glib2 (bug #115619).  Patch from W. Michael Petullo.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 7.07-22
- rebuilt

* Thu Feb 12 2004 Tim Waugh <twaugh@redhat.com> 7.07-21
- Leave gdevpdfm.c seemingly-mistaken bitwise ops alone (bug #115396).

* Thu Feb  5 2004 Tim Waugh <twaugh@redhat.com> 7.07-20
- Fix compilation with GCC 3.4.

* Wed Jan 28 2004 Tim Waugh <twaugh@redhat.com> 7.07-19
- Attempt to fix gdevcups crash (bug #114256).
- Make gs dynamically link to libgs (bug #114276).
- Fix gdevesmv.c's misuse of const (bug #114250).

* Tue Jan 20 2004 Tim Waugh <twaugh@redhat.com> 7.07-18
- Turn on libgs again (bug #88175).

* Mon Jan 19 2004 Tim Waugh <twaugh@redhat.com> 7.07-17
- Removed stp driver.  Use the IJS version (ijsgimpprint) instead.
- No longer conflicts with foomatic for hpijs versioning.

* Mon Jan 12 2004 Tim Waugh <twaugh@redhat.com> 7.07-16
- Split hpijs out into separate source package.

* Thu Jan 8  2004 Tim Waugh <twaugh@redhat.com>
- Fix several mistakenly-used bitwise operations.

* Tue Jan 6  2004 Tim Waugh <twaugh@redhat.com> 7.07-15
- Build for Fedora Core 1 printer drivers update.
- Conflicts with foomatic before hpijs 1.5 data.
- Make fontconfig optional.

* Sat Dec 13 2003 Tim Waugh <twaugh@redhat.com> 7.07-14
- Disable unnecessary debug messages from fontconfig support.

* Fri Dec  5 2003 Tim Waugh <twaugh@redhat.com> 7.07-13
- Add fontconfig support (bug #111412).

* Thu Nov 27 2003 Tim Waugh <twaugh@redhat.com>
- Build requires libjpeg-devel (bug #110737).

* Tue Nov 11 2003 Tim Waugh <twaugh@redhat.com> 7.07-12
- Updated hpijs to 1.5 (bug #109714).

* Mon Nov 10 2003 Tim Waugh <twaugh@redhat.com>
- Updated lxm3200 patch (bug #109625).

* Tue Sep 30 2003 Tim Waugh <twaugh@redhat.com> 7.07-11
- Updated gdevcups.c from CUPS 1.1.19.
- Apply NOMEDIAATTRS patch from CUPS 1.1.19 (bug #105401).

* Thu Aug 28 2003 Tim Waugh <twaugh@redhat.com>
- Fix lips4v driver (bug #92337).

* Wed Aug 20 2003 Tim Waugh <twaugh@redhat.com> 7.07-10
- Fix compilation problems in hpijs.

* Mon Aug  4 2003 Tim Waugh <twaugh@redhat.com> 7.07-9
- Further fix from bug #100685.

* Thu Jul 31 2003 Tim Waugh <twaugh@redhat.com> 7.07-8
- Further fix from bug #100685.

* Tue Jul 29 2003 Tim Waugh <twaugh@redhat.com> 7.07-7
- Further fix from bug #100685.

* Fri Jul 25 2003 Tim Waugh <twaugh@redhat.com> 7.07-6
- Further fix from bug #100557.

* Thu Jul 24 2003 Tim Waugh <twaugh@redhat.com> 7.07-5
- Further fix from bug #100557.
- Fix bug #100685.

* Wed Jul 23 2003 Tim Waugh <twaugh@redhat.com> 7.07-4
- Fix bug #100557.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 7.07-3
- rebuilt

* Tue May 27 2003 Tim Waugh <twaugh@redhat.com>
- Fix sed usage in ps2epsi (bug #89300).

* Tue May 20 2003 Tim Waugh <twaugh@redhat.com> 7.07-2
- HPIJS 1.4 (bug #91219).

* Sun May 18 2003 Tim Waugh <twaugh@redhat.com> 7.07-1
- 7.07.
- Parametrize build_libgs.
- Remove Omni requirement (bug #88177).
- Fix ghostscript-gtk obsoletes: line (bug #88175).

* Thu Apr  3 2003 Tim Waugh <twaugh@redhat.com> 7.06-1
- 7.06.
- Updated config, vflib.fixup patches.
- No longer need dx6, jpeg patches.
- No longer need to add in missed GNU drivers.
- Turn off dj970 driver (hpijs drives that).

* Mon Mar 31 2003 Tim Waugh <twaugh@redhat.com> 7.05-34
- Apply fix for CJK font search method when the fonts are not available
  (bug #83516).
- The gb18030 patch no longer applies here.

* Thu Mar 27 2003 Tim Waugh <twaugh@redhat.com> 7.05-33
- Add some missing font aliases (bug #73342).
- Use the system jpeg library.
- Update hpijs to 1.3.1.
- Update gdevcups.c from cups-1.1.18.

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com> 7.05-32
- debuginfo rebuild

* Fri Feb 21 2003 Elliot Lee <sopwith@redhat.com> 7.05-31
- Add ghostscript-7.05-oob-66421.patch to fix the segfault behind #66421

* Thu Jan 30 2003 Tim Waugh <twaugh@redhat.com> 7.05-30
- Remove rss patch from hpijs (not needed).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 7.05-29
- rebuilt

* Thu Jan 16 2003 Tim Waugh <twaugh@redhat.com> 7.05-28
- Add Korean font aliases to CIDFnmap CJK resource files (bug #81924).

* Sat Dec 14 2002 Tim Waugh <twaugh@redhat.com> 7.05-27
- Obsolete ghostscript-gtk (bug #79585).
- Omni 121002 patch.

* Tue Dec 10 2002 Tim Waugh <twaugh@redhat.com> 7.05-26
- Don't ship the shared object yet (part of bug #79340).
- Don't make the gtk package, since that needs the shared object.

* Tue Nov 26 2002 Tim Waugh <twaugh@redhat.com> 7.05-25
- Fix level 1 PostScript output (bug #78450).
- No need to carry gomni.c, since it comes from the patch.

* Mon Nov 11 2002 Tim Waugh <twaugh@redhat.com> 7.05-24
- Omni 071902 patch.

* Mon Nov 11 2002 Tim Waugh <twaugh@redhat.com> 7.05-23
- hpijs-1.3, with updated rss patch.
- Fix XLIBDIRS.

* Fri Oct 25 2002 Tim Waugh <twaugh@redhat.com> 7.05-22
- hpijs-rss 1.2.2.

* Mon Oct 14 2002 Tim Waugh <twaugh@redhat.com> 7.05-21
- Set libdir when installing.

* Thu Aug 15 2002 Tim Waugh <twaugh@redhat.com> 7.05-20
- Add cups device (bug #69573).

* Mon Aug 12 2002 Tim Waugh <twaugh@redhat.com> 7.05-19
- Fix the gb18030 patch (bug #71135, bug #71303).

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com> 7.05-18
- rebuilt with gcc-3.2 (we hope)

* Fri Aug  9 2002 Tim Waugh <twaugh@redhat.com> 7.05-17
- Add CIDnmap for GB18030 font (bug #71135).
- Fix URL (bug #70734).

* Tue Jul 23 2002 Tim Waugh <twaugh@redhat.com> 7.05-16
- Rebuild in new environment.

* Tue Jul  9 2002 Tim Waugh <twaugh@redhat.com> 7.05-15
- Remove the chp2200 driver again, to fix cdj890 (bug #67578).

* Fri Jul  5 2002 Tim Waugh <twaugh@redhat.com> 7.05-14
- For CJK font support, use CIDFnmap instead of CIDFont
  resources (bug #68009).

* Wed Jul  3 2002 Tim Waugh <twaugh@redhat.com> 7.05-13
- Build requires unzip and gtk+-devel (bug #67799).

* Wed Jun 26 2002 Tim Waugh <twaugh@redhat.com> 7.05-12
- File list tweaking.
- More file list tweaking.

* Tue Jun 25 2002 Tim Waugh <twaugh@redhat.com> 7.05-10
- Rebuild for bootstrap.

* Wed Jun 19 2002 Tim Waugh <twaugh@redhat.com> 7.05-9
- Omni 052902 patch.

* Mon Jun 10 2002 Tim Waugh <twaugh@redhat.com> 7.05-8
- Requires recent version of patchutils (bug #65947).
- Don't ship broken man page symlinks (bug #66238).

* Wed May 29 2002 Tim Waugh <twaugh@redhat.com> 7.05-7
- Put gsx in its own package.

* Tue May 28 2002 Tim Waugh <twaugh@redhat.com> 7.05-6
- New gomni.c from IBM to fix an A4 media size problem.
- Use new Adobe CMaps (bug #65362).

* Sun May 26 2002 Tim Powers <timp@redhat.com> 7.05-5
- automated rebuild

* Wed May 22 2002 Tim Waugh <twaugh@redhat.com> 7.05-4
- New gomni.c from IBM to fix bug #65269 (again).

* Tue May 21 2002 Tim Waugh <twaugh@redhat.com> 7.05-2
- Don't apply bogus parts of vflib patch (bug #65268).
- Work around Omni -sPAPERSIZE=a4 problem (bug #65269).

* Mon May 20 2002 Tim Waugh <twaugh@redhat.com> 7.05-1
- 7.05.
- No longer need mkstemp, vflib.fixup, quoting, or PARANOIDSAFER
  patches.
- Don't apply CJK patches any more (no longer needed).
- Updated Source15, Patch0, Patch10, Patch5, Patch24, Patch14, Patch12.
- Made gdevdmpr.c compile again.
- Move gimp-print to a separate package.
- Ship the shared object too (and a .so file that is dlopened).
- Update Omni patch.  No longer need Omni_path, Omni_quiet, Omni_glib patches.
- Require Omni >= 0.6.1.
- Add patch to fix gtk+ initial window size.
- Add devel package with header files.
- Turn on IJS support.
- Update hpijs to 1.1.
- Don't ship the hpijs binary in the ghostscript package.
- Use -fPIC when building ijs.

* Wed Apr  3 2002 Tim Waugh <twaugh@redhat.com> 6.52-8
- New CIDFonts (bug #61015).

* Wed Apr  3 2002 Tim Waugh <twaugh@redhat.com> 6.52-7
- Fix release numbers of sub packages.
- Handle info files, use ldconfig (bug #62574).

* Tue Mar 19 2002 Tim Waugh <twaugh@redhat.com> 6.52-6
- Fix config patch so that gs --help displays the right thing.
- Don't ship sysvlp.sh.
- Fix some shell scripts.
- Ship escputil man page (bug #58919).

* Mon Feb 11 2002 Tim Waugh <twaugh@redhat.com> 6.52-5
- Add CHP2200 driver (bug #57516).
- Fix gimp-print-4.2.0 so that it builds without cups-config.

* Sat Feb  2 2002 Bill Nottingham <notting@redhat.com> 6.52-4
- do condrestart in %%postun, not %%post

* Fri Feb  1 2002 Bernhard Rosenkraenzer <bero@redhat.com> 6.52-3
- Restart service cups after installing gimp-print-cups

* Sun Jan 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 6.52-2
- hpijs is finally free - support it.
- Add extra package for CUPS support

* Mon Jan 21 2002 Bernhard Rosenkraenzer <bero@redhat.com> 6.52-1
- Updates:
  - ghostscript 6.52
  - hpdj 2.6 -> pcl3 3.3
  - CJK Patchlevel 3, adobe-cmaps 200109
  - gimp-print 4.2.0
- Adapt patches
- Fix various URLs
- Begin cleaning up spec file
- Fix bugs #21879 and #50923

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Oct 18 2001 Crutcher Dunnavant <crutcher@redhat.com> 6.51-16
- update the Omni driver, and patch it to seek in /usr/lib/Omni/ first
- require Omni

* Mon Oct 01 2001 Crutcher Dunnavant <crutcher@redhat.com> 6.51-15
- change -dPARANOIDSAFER to punch a hole for OutputFile

* Mon Sep 17 2001 Crutcher Dunnavant <crutcher@redhat.com> 6.51-14
- add -dPARANOIDSAFER to let us breathe a little easier in the print spooler.

* Thu Sep 13 2001 Crutcher Dunnavant <crutcher@redhat.com> 6.51-13
- apply jakub's fix to ghostscript's jmp_buf problems; #49591

* Wed Sep  5 2001 Crutcher Dunnavant <crutcher@redhat.com> 6.51-12
- fix lprsetup.sh; #50925

* Fri Aug 24 2001 Crutcher Dunnavant <crutcher@redhat.com> 6.51-11
- added Epson's old eplaseren drivers,
- pointed out by Till Kamppeter <till.kamppeter@gmx.net>

* Tue Aug 21 2001 Paul Howarth <paul@city-fan.org> 6.51-10
- included Samsung GDI driver for ML-4500 printer support.

* Sun Aug 19 2001 Crutcher Dunnavant <crutcher@redhat.com> 6.51-9
- applied IBM's glib patches for Omni, which now works.
- BE AWARE: we now link against libstdc++ and glib for this, and use a c++
- link stage to do the dirty.
- added glib-devel buildreq and glib req, I don't think we require everything
- yet, I could pull in sasl.

* Sun Aug 19 2001 David Suffield <david_suffield@hp.com> 6.51-8
- Added gs device hpijs and updated gdevhpij.c to hpijs 0.97

* Wed Aug 15 2001 Crutcher Dunnavant <crutcher@redhat.com> 6.51-7
- pull in ynakai's update to the cjk resources.

* Thu Aug  9 2001 Crutcher Dunnavant <crutcher@redhat.com> 6.51-6
- turn dmprt and cdj880 back on. for some reason, they work now.
- voodoo, who knows.

* Thu Aug  9 2001 Yukihiro Nakai <ynakai@redhat.com> 6.51-5
- Add cjk resources

* Wed Aug  1 2001 Crutcher Dunnavant <crutcher@redhat.com> 6.51-4
- applied drepper@redhat.com's patch for #50300
- fixed build deps on zlib-devel and libpng-devel, #49853
- made gs_init.ps a config file; #25096
- O\^/nZ the daTa directorieZ now; #50693

* Tue Jul 24 2001 Crutcher Dunnavant <crutcher@redhat.com> 6.51-3
- wired up the Resource dir and the Font and CIDFont maps.

* Mon Jul 23 2001 Crutcher Dunnavant <crutcher@redhat.com> 6.51-2
- luckily, I had a spare chicken. Thanks to some work by Nakai, and one last
- desperate search through google, everything /seems/ to be working. I know
- that there are going to be problems in the japanese code, and I need to turn
- on the cjk font map from adobe, but it /works/ at the moment.

* Thu Jun 21 2001 Crutcher Dunnavant <crutcher@redhat.com>
- upgraded to 6.51, a major version upgrade
- rewrote spec file, threw out some patches
- turned on IBM's Omni print drivers interface
- turned on HP's hpijs print drivers interface
- turned on every driver that looked usable from linux
- sacrificed a chicken to integrate the old Japanese drivers
- - This didn't work. The japanese patches are turned off, pending review.
- - I can do loops with C, but the bugs are in Postscript init files

* Wed Apr 11 2001 Crutcher Dunnavant <crutcher@redhat.com>
- added P. B. West's lx5000 driver

* Tue Feb 27 2001 Crutcher Dunnavant <crutcher@redhat.com>
- added xtt-fonts requirement (for VFlib)

* Fri Feb  9 2001 Adrian Havill <havill@redhat.com>
- cmpskit removed as a build prereq

* Thu Feb  8 2001 Crutcher Dunnavant <crutcher@redhat.com>
- merged in some patches that got away:
  * Fri Sep  1 2000 Mitsuo Hamada <mhamada@redhat.com>
  - add support JIS B size
  - fix the problem of reconverting GNUPLOT output

* Thu Feb  8 2001 Crutcher Dunnavant <crutcher@redhat.com>
- switched to japanese for everybody

* Thu Feb  8 2001 Crutcher Dunnavant <crutcher@redhat.com>
- tweaked time_.h to test for linux, and include the right
- header

* Wed Feb  7 2001 Crutcher Dunnavnat <crutcher@redhat.com>
- added the lxm3200 driver

* Mon Dec 11 2000 Crutcher Dunnavant <crutcher@redhat.com>
- merged in the (accendental) branch that contained the mktemp
- and LD_RUN_PATH bug fixes.

* Tue Oct 17 2000 Jeff Johnson <jbj@redhat.com>
- tetex using xdvi with ghostscript patch (#19212).

* Tue Sep 12 2000 Michael Stefaniuc <mstefani@redhat.com>
- expanded the gcc296 patch to fix a compilation issue with the new stp
  driver

* Mon Sep 11 2000 Michael Stefaniuc <mstefani@redhat.com>
- added the stp driver from the gimp-print project.
  It supports high quality printing especialy with Epson Stylus Photo.

* Wed Aug  2 2000 Matt Wilson <msw@redhat.com>
- rebuilt against new libpng

* Wed Aug  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up the cdj880 patch (Bug #14978)
- Fix build with gcc 2.96

* Fri Jul 21 2000 Bill Nottingham <notting@redhat.com>
- turn off japanese support

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fixed the broken inclusion of files in /usr/doc
- Build requires freetype-devel

* Fri Jun 16 2000 Matt Wilson <msw@redhat.com>
- build japanese support in main distribution
- FHS manpage paths

* Sun Mar 26 2000 Chris Ding <cding@redhat.com>
- enabled bmp16m driver

* Thu Mar 23 2000 Matt Wilson <msw@redhat.com>
- added a boatload of Japanese printers

* Thu Mar 16 2000 Matt Wilson <msw@redhat.com>
- add japanese support, enable_japanese macro

* Mon Feb 14 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.50 at last...
- hpdj 2.6
- Added 3rd party drivers:
  - Lexmark 5700 (lxm5700m)
  - Alps MD-* (md2k, md5k)
  - Lexmark 2050, 3200, 5700 and 7000 (lex2050, lex3200, lex5700, lex7000)

* Fri Feb  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild to compress man page
- fix gs.1 symlink

* Wed Jan 26 2000 Bill Nottingham <notting@redhat.com>
- add stylus 740 uniprint files

* Thu Jan 13 2000 Preston Brown <pbrown@redhat.com>
- add lq850 dot matrix driver (#6357)

* Thu Oct 28 1999 Bill Nottingham <notting@redhat.com>
- oops, include oki182 driver.

* Tue Aug 24 1999 Bill Nottingham <notting@redhat.com>
- don't optimize on Alpha. This way it works.

* Thu Jul 29 1999 Michael K. Johnson <johnsonm@redhat.com>
- added hpdj driver
- changed build to use tar_cat so adding new drivers is sane

* Thu Jul  1 1999 Bill Nottingham <notting@redhat.com>
- add OkiPage 4w+, HP 8xx drivers
* Mon Apr  5 1999 Bill Nottingham <notting@redhat.com>
- fix typo in config patch.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 6)

* Mon Mar 15 1999 Cristian Gafton <gafton@redhat.com>
- added patch from rth to fix alignement problems on the alpha.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Feb 08 1999 Bill Nottingham <notting@redhat.com>
- add uniprint .upp files

* Sat Feb 06 1999 Preston Brown <pbrown@redhat.com>
- fontpath update.

* Wed Dec 23 1998 Preston Brown <pbrown@redhat.com>
- updates for ghostscript 5.10

* Fri Nov 13 1998 Preston Brown <pbrown@redhat.com>
- updated to use shared urw-fonts package.
* Mon Nov 09 1998 Preston Brown <pbrown@redhat.com>
- turned on truetype (ttf) font support.

* Thu Jul  2 1998 Jeff Johnson <jbj@redhat.com>
- updated to 4.03.

* Tue May 05 1998 Cristian Gafton <gafton@redhat.com>
- enabled more printer drivers
- buildroot

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Mar 03 1997 Erik Troan <ewt@redhat.com>
- Made /usr/share/ghostscript/3.33/Fontmap a config file.
