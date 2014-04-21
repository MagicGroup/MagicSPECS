Name:		htmldoc
Version:	1.8.27
Release:	21%{?dist}
Summary:	Converter from HTML into indexed HTML, PostScript, or PDF

Group:		Applications/Publishing

# GPLv2 with OpenSSL exception
License:	GPLv2 with exceptions
URL:		http://www.htmldoc.org/
Source:		http://ftp.easysw.com/pub/%{name}/%{version}/%{name}-%{version}-source.tar.bz2

Patch0:		htmldoc-1.8.27-desktop-icon.patch
Patch1:		htmldoc-1.8.27-dingbats-standard.patch
Patch2:		htmldoc-1.8.27-system-fonts.patch
Patch3:		htmldoc-1.8.27-scanf-overflows.patch
Patch4:		htmldoc-1.8.27-fortify-fail.patch
Patch5:		htmldoc-1.8.27-fixdso.patch
# http://www.htmldoc.org/str.php?L243+P0+S-2+C0+I0+E0+M10+Q
# http://www.htmldoc.org/strfiles/243/patch-ae
Patch6: 	htmldoc-1.8.27-libpng15.patch

BuildRequires:	openssl-devel libjpeg-devel libpng-devel zlib-devel
BuildRequires:	fltk-devel libXpm-devel desktop-file-utils
BuildRequires:	dejavu-sans-fonts dejavu-sans-mono-fonts dejavu-serif-fonts
BuildRequires:	urw-fonts fontpackages-devel
BuildRequires:	ttf2pt1 t1utils

Requires:	dejavu-sans-fonts dejavu-sans-mono-fonts dejavu-serif-fonts
Requires:	urw-fonts
Requires:	ttf2pt1 t1utils


%description
HTMLDOC converts HTML source files into indexed HTML, PostScript, or
Portable Document Format (PDF) files that can be viewed online or
printed. With no options a HTML document is produced on stdout.

The second form of HTMLDOC reads HTML source from stdin, which allows
you to use HTMLDOC as a filter.

The third form of HTMLDOC launches a graphical interface that allows
you to change options and generate documents interactively.


%prep
%setup -q

# fix up hardcoded documentation path
sed -i 's/\(\$prefix\/share\/doc\/htmldoc\)/\1-%{version}/g' configure

# Fix DSO linking
%patch5 -p1 -b .fixdso

# fix desktop icon (http://www.htmldoc.org/str.php?L169)
%patch0 -p1 -b .desktop-icon

# make Dingbats standard (http://www.htmldoc.org/str.php?L198)
%patch1 -p1 -b .dingbats

# use Fedora system fonts (http://www.htmldoc.org/str.php?L196)
%patch2 -p1 -b .system-fonts
cd fonts
rm -f *.pfa *.afm
ln -s %{_fontbasedir}/default/Type1/n022003l.afm Courier.afm
ln -s %{_fontbasedir}/default/Type1/n022004l.afm Courier-Bold.afm
ln -s %{_fontbasedir}/default/Type1/n022024l.afm Courier-BoldOblique.afm
ln -s %{_fontbasedir}/default/Type1/n022024l.pfb Courier-BoldOblique.pfb
ln -s %{_fontbasedir}/default/Type1/n022004l.pfb Courier-Bold.pfb
ln -s %{_fontbasedir}/default/Type1/n022023l.afm Courier-Oblique.afm
ln -s %{_fontbasedir}/default/Type1/n022023l.pfb Courier-Oblique.pfb
ln -s %{_fontbasedir}/default/Type1/n022003l.pfb Courier.pfb
ln -s %{_fontbasedir}/default/Type1/d050000l.afm Dingbats.afm
ln -s %{_fontbasedir}/default/Type1/d050000l.pfb Dingbats.pfb
ln -s %{_fontbasedir}/default/Type1/n019003l.afm Helvetica.afm
ln -s %{_fontbasedir}/default/Type1/n019004l.afm Helvetica-Bold.afm
ln -s %{_fontbasedir}/default/Type1/n019024l.afm Helvetica-BoldOblique.afm
ln -s %{_fontbasedir}/default/Type1/n019024l.pfb Helvetica-BoldOblique.pfb
ln -s %{_fontbasedir}/default/Type1/n019004l.pfb Helvetica-Bold.pfb
ln -s %{_fontbasedir}/default/Type1/n019023l.afm Helvetica-Oblique.afm
ln -s %{_fontbasedir}/default/Type1/n019023l.pfb Helvetica-Oblique.pfb
ln -s %{_fontbasedir}/default/Type1/n019003l.pfb Helvetica.pfb
ln -s %{_fontbasedir}/default/Type1/s050000l.afm Symbol.afm
ln -s %{_fontbasedir}/default/Type1/s050000l.pfb Symbol.pfb
ln -s %{_fontbasedir}/default/Type1/n021004l.afm Times-Bold.afm
ln -s %{_fontbasedir}/default/Type1/n021024l.afm Times-BoldItalic.afm
ln -s %{_fontbasedir}/default/Type1/n021024l.pfb Times-BoldItalic.pfb
ln -s %{_fontbasedir}/default/Type1/n021004l.pfb Times-Bold.pfb
ln -s %{_fontbasedir}/default/Type1/n021023l.afm Times-Italic.afm
ln -s %{_fontbasedir}/default/Type1/n021023l.pfb Times-Italic.pfb
ln -s %{_fontbasedir}/default/Type1/n021003l.afm Times-Roman.afm
ln -s %{_fontbasedir}/default/Type1/n021003l.pfb Times-Roman.pfb
ln -s %{_fontbasedir}/dejavu/DejaVuSans-BoldOblique.ttf
ln -s %{_fontbasedir}/dejavu/DejaVuSans-Bold.ttf
ln -s %{_fontbasedir}/dejavu/DejaVuSansMono-BoldOblique.ttf
ln -s %{_fontbasedir}/dejavu/DejaVuSansMono-Bold.ttf
ln -s %{_fontbasedir}/dejavu/DejaVuSansMono-Oblique.ttf
ln -s %{_fontbasedir}/dejavu/DejaVuSansMono.ttf
ln -s %{_fontbasedir}/dejavu/DejaVuSans-Oblique.ttf
ln -s %{_fontbasedir}/dejavu/DejaVuSans.ttf
ln -s %{_fontbasedir}/dejavu/DejaVuSerif-BoldItalic.ttf
ln -s %{_fontbasedir}/dejavu/DejaVuSerif-Bold.ttf
ln -s %{_fontbasedir}/dejavu/DejaVuSerif-Italic.ttf
ln -s %{_fontbasedir}/dejavu/DejaVuSerif.ttf
cd ..

# fix some scanf overflows (http://www.htmldoc.org/str.php?L214)
%patch3 -p1 -b .scanf-overflows

# fix limitation of -D_FORTIFY_SOURCE=2
%patch4 -p1 -b .fortify-fail

# fix build with libpng-1.5+
%patch6 -p0 -b .libpng15


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install prefix=${RPM_BUILD_ROOT}%{_prefix} mandir=${RPM_BUILD_ROOT}%{_mandir} bindir=${RPM_BUILD_ROOT}%{_bindir} datadir=${RPM_BUILD_ROOT}%{_datadir}

# kill thing which we get later in the right place with %doc
rm -rf ${RPM_BUILD_ROOT}%{_docdir}/htmldoc

# install icons
for s in 16 24 32 48 64 96 128; do 			\
	install -d ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/${s}x${s}/apps; \
	cp -a desktop/htmldoc-$s.png 			\
	${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/${s}x${s}/apps/htmldoc.png;\
done

# install MIME
install -d ${RPM_BUILD_ROOT}%{_datadir}/mime/packages
cp -a desktop/htmldoc.xml ${RPM_BUILD_ROOT}%{_datadir}/mime/packages

# desktop file
desktop-file-install --vendor fedora				\
	--dir ${RPM_BUILD_ROOT}%{_datadir}/applications		\
	--remove-category=X-Red-Hat-Base			\
	--add-mime-type=application/vnd.htmldoc-book		\
	desktop/htmldoc.desktop


%post
# scriptlet for icons
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

# scriptlet for MIME
update-mime-database %{_datadir}/mime &> /dev/null || :

# scriptlet for desktop database
update-desktop-database &> /dev/null || :


%postun
# scriptlet for icons
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

# scriptlet for MIME
update-mime-database %{_datadir}/mime &> /dev/null || :

# scriptlet for desktop database
update-desktop-database &> /dev/null || :


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc/intro.html doc/c-relnotes.html doc/htmldoc.{html,pdf,ps} doc/help.html
%doc CHANGES.txt COPYING.txt README.txt
%{_datadir}/htmldoc
%{_datadir}/applications/*
%{_mandir}/man1/*
%{_bindir}/htmldoc
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/htmldoc.xml


%changelog
* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 1.8.27-21
- 为 Magic 3.0 重建

* Sat Sep  1 2012 Daniel Drake <dsd@laptop.org> - 1.8.27-20
- fix libpng-1.5 patch to not corrupt images

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.27-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Rex Dieter <rdieter@fedoraproject.org> 1.8.27-18
- fix build against libpng-1.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.27-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.8.27-16
- Rebuild for new libpng

* Tue Jun 14 2011 Peter Robinson <pbrobinson@gmail.com> - 1.8.27-15
- Fix DSO linking so htmldoc actually compiles and works - RHBZ 631135 and others

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.27-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.8.27-13
- rebuilt with new openssl

* Thu Aug 13 2009 Adam Goode <adam@spicenitz.org> - 1.8.27-12
- Fix limitation of -D_FORTIFY_SOURCE=2 (#511520)
- Fix scanf overflows (#512513)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.27-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.27-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Adam Goode <adam@spicenitz.org> - 1.8.27-9
- Patch to specify Dingbats as a standard PS and PDF font
- Use system fonts to conform to new font guidelines (#477397)

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> - 1.8.27-8
- rebuild with new openssl

* Sat Aug 30 2008 Adam Goode <adam@spicenitz.org> - 1.8.27-7
- RPM 4.6 fix for patch tag

* Sat Feb  9 2008 Adam Goode <adam@spicenitz.org> - 1.8.27-6
- GCC 4.3 mass rebuild

* Wed Dec  5 2007 Adam Goode <adam@spicenitz.org> - 1.8.27-5
- Fix desktop file validation

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.8.27-4
 - Rebuild for deps

* Wed Aug 22 2007 Adam Goode <adam@spicenitz.org> - 1.8.27-3
- Update license tag
- Rebuild for buildid

* Sat May  5 2007 Adam Goode <adam@spicenitz.org> - 1.8.27-2
- Remove X-Fedora

* Thu Aug 31 2006 Adam Goode <adam@spicenitz.org> - 1.8.27-1.1
- Mass rebuild

* Wed Aug  2 2006 Adam Goode <adam@spicenitz.org> - 1.8.27-1
- New upstream release

* Wed May 31 2006 Adam Goode <adam@spicenitz.org> - 1.8.26-4
- Fix hardcoded documentation path in configure
- Add help.html to documentation

* Mon May 29 2006 Adam Goode <adam@spicenitz.org> - 1.8.26-3
- Use upstream desktop file
- Install icons
- Install mime XML file
- Eliminate strange spaces in description

* Sat May 27 2006 Adam Goode <adam@spicenitz.org> - 1.8.26-2
- Add downloadable source

* Thu May 25 2006 Adam Goode <adam@spicenitz.org> - 1.8.26-1
- New upstream release
- Rebuild for FC5

* Mon Oct 24 2005 Thomas Chung <tchung@fedoranews.org> 1.8.24-1
- Rebuild for FC4

* Tue Feb 22 2005 Thomas Chung <tchung@fedoranews.org> 1.8.24-0
- Initial RPM build for FC3
