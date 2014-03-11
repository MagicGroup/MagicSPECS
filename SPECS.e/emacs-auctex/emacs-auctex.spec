# AucTeX includes preview-latex which allows previeweing directly in the Emacs
# buffer. This makes use of preview.sty, a LaTeX class, which is also included
# with AucTex. preview-latex can either use a privately installed copy of
# preview.sty, or it can use one installed in the system texmf tree. If the
# following is set to 1, an add-on LaTeX package will be created which installs
# into the system texmf tree, and preview-latex will use that. However, TeXLive
# already includes preview.sty and so this may not be desireable -- setting the
# following value to 0 means that preview-latex/AucTeX will use a privately
# installed copy of preview.sty.
%global separate_preview 1

Summary: 	Enhanced TeX modes for Emacs
Name: 		emacs-auctex
Version: 	11.87
Release: 	2%{?dist}
License: 	GPLv3+ and GFDL
Group: 		Applications/Editors
URL: 		http://www.gnu.org/software/auctex/
Requires: 	emacs(bin) >= %{_emacs_version}
Requires:	ghostscript dvipng
Requires:	tex(latex) tex(dvips)
Requires(pre): 	/sbin/install-info
Requires(post): /sbin/install-info
Obsoletes:	emacs-auctex-el <= 11.86-9
Provides:	emacs-auctex-el <= 11.86-9
%if %{separate_preview}
Requires: 	tex-preview = %{version}-%{release}
%endif

Source0: 	ftp://ftp.gnu.org/pub/gnu/auctex/auctex-%{version}.tar.gz

BuildArch: 	noarch
BuildRequires: 	emacs tex(latex) texinfo-tex ghostscript

%description
AUCTeX is an extensible package that supports writing and formatting
TeX files for most variants of Emacs.

AUCTeX supports many different TeX macro packages, including AMS-TeX,
LaTeX, Texinfo and basic support for ConTeXt.  Documentation can be
found under /usr/share/doc, e.g. the reference card (tex-ref.pdf) and
the FAQ. The AUCTeX manual is available in Emacs info (C-h i d m
AUCTeX RET). On the AUCTeX home page, we provide manuals in various
formats.

AUCTeX includes preview-latex support which makes LaTeX a tightly
integrated component of your editing workflow by visualizing selected
source chunks (such as single formulas or graphics) directly as images
in the source buffer.

This package is for GNU Emacs.

%package doc
Summary:	Documentation in various formats for AUCTeX
Group:		Documentation
License: 	GFDL

%description doc
Documentation for the AUCTeX package for emacs in various formats,
including HTML and PDF.

%if %{separate_preview}
%package -n tex-preview
Summary: 	Preview style files for LaTeX
Group: 		Applications/Publishing
Requires: 	tex(latex)
Obsoletes:	tetex-preview
Provides:	tetex-preview

%description -n tex-preview
The preview package for LaTeX allows for the processing of selected
parts of a LaTeX input file.  This package extracts indicated pieces
from a source file (typically displayed equations, figures and
graphics) and typesets with their base point at the (1in,1in) magic
location, shipping out the individual pieces on separate pages without
any page markup.  You can produce either DVI or PDF files, and options
exist that will set the page size separately for each page.  In that
manner, further processing (as with Ghostscript or dvipng) will be
able to work in a single pass.

The main purpose of this package is the extraction of certain
environments (most notably displayed formulas) from LaTeX sources as
graphics. This works with DVI files postprocessed by either Dvips and
Ghostscript or dvipng, but it also works when you are using PDFTeX for
generating PDF files (usually also postprocessed by Ghostscript).

The tex-preview package is generated from the AUCTeX package for
Emacs.
%endif

%prep
%setup -q -n auctex-%{version}

%build
%if %{separate_preview}
%configure --with-emacs --with-texmf-dir=%{_datadir}/texmf
%else
%configure --with-emacs --without-texmf-dir
%endif

make

# Build documentation in various formats
pushd doc
#make extradist
make
popd

# Fix some encodings
iconv -f ISO-8859-1 -t UTF8 RELEASE > RELEASE.utf8 && touch -r RELEASE RELEASE.utf8 && mv RELEASE.utf8 RELEASE

%install
mkdir -p %{buildroot}%{_emacs_sitestartdir}
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_var}

# Remove /usr/share/doc/auctex directory from buildroot since we don't want doc
# files installed here
rm -rf %{buildroot}%{_docdir}/auctex

%post
/sbin/install-info %{_infodir}/auctex.info %{_infodir}/dir 2>/dev/null || :
/sbin/install-info %{_infodir}/preview-latex.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/auctex.info %{_infodir}/dir 2>/dev/null || :
  /sbin/install-info --delete %{_infodir}/preview-latex.info %{_infodir}/dir 2>/dev/null || :
fi

%if %{separate_preview}
%post -n tex-preview
/usr/bin/texhash > /dev/null 2>&1 || :

%postun -n tex-preview
/usr/bin/texhash > /dev/null 2>&1 || :
%endif

%files
%doc RELEASE COPYING README TODO FAQ CHANGES
%doc %{_infodir}/*.info*
%exclude %{_infodir}/dir
%{_emacs_sitestartdir}/*
%dir %{_emacs_sitelispdir}/auctex
%dir %{_emacs_sitelispdir}/auctex/style
%{_emacs_sitelispdir}/auctex/*.el
%{_emacs_sitelispdir}/auctex/*.elc
%{_emacs_sitelispdir}/auctex/style/*.el
%{_emacs_sitelispdir}/auctex/style/*.elc
%{_emacs_sitelispdir}/auctex/.nosearch
%{_emacs_sitelispdir}/auctex/style/.nosearch
%{_emacs_sitelispdir}/auctex/images
%{_emacs_sitelispdir}/tex-site.el
%if !%{separate_preview}
%{_emacs_sitelispdir}/auctex/latex
%{_emacs_sitelispdir}/auctex/doc
%endif

%if %{separate_preview}
%files -n tex-preview
%doc COPYING
%{_datadir}/texmf/tex/latex/preview
%{_datadir}/texmf/doc/latex/styles
%endif

%files doc
%doc doc/*.pdf
#%doc doc/*.{dvi,ps,pdf}
#%doc doc/html

%changelog
* Tue Dec  4 2012 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.87-2
- Fix the install location of the preview tex files
- Fix the BuildRequires for latex

* Mon Dec  3 2012 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.87-1
- Update to new upstream version 11.87

* Wed Oct  3 2012 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.86-10
- Fix the Obsoletes and Provides to allow package updating (BZ 862398)

* Wed Sep 19 2012 Karel Klíč <kklic@redhat.com> - 11.86-9
- ELisp source code is no longer distributed in a separate package
- License filed includes GFDL for the documentation

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.86-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.86-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar  8 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.86-6
- Replace define with global in macro definitions
- Add patch to fix previewing of equations courtesy of Sato Ichi (BZ 646632)
- Add defattr to doc sub-package

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.86-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 16 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.86-4
- Duplicate only the COPYING file and not the other docs in the tex-preview
  subpackage

* Fri Jul 16 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.86-3
- Add COPYING file and other docs to the tex-preview subpackage to comply with
  updated licensing guidelines
- Remove the no longer needed BuildRoot, %%clean and cleaning of Buildroot
  inside %%install

* Sun May 23 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.86-2
- Drop Requires for evince (rhbz 595104)

* Sat Mar  6 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.86-1
- Update to 11.86
- Drop unneeded patch for PDF and HTML viewing

* Thu Jan 28 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-11
- Add patch to use evince for PDF file viewing and xdg-open for html file
  viewing
- Add Requires for evince

* Sat Nov  7 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-10
- Update spec file to use macros defined in /etc/rpm/macros.emacs
- Fix typo in spec comments

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.85-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.85-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 24 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-7
- Add Requires for dvipng

* Sat Feb 16 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-6
- Preserve timestamp of RELEASE when converting to UTF8

* Wed Feb 13 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-5
- Re-add creation of emacs_startdir

* Tue Feb 12 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-4
- Remove BuildRequires for pkgconfig - not needed
- Clean out uneeded creation of site start directory
- Remove /usr/share/doc/auctex directory from buildroot

* Tue Feb 12 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-3
- Bump release and rebuild - had forgotten to upload the new sources

* Tue Feb 12 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-2
- Add BuilddRequires for pkgconfig

* Tue Feb 12 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.85-1
- Update to version 11.85
- Change license to GPLv3+ accordingly

* Wed Jan 23 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-7
- tex-preview no longer Requires ghostscript (#429811)
- Use virtual provides for tex(latex) etc.

* Tue Dec 25 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-6
- Add Obsolotes and Provides for tetex-preview to tex-preview (#426758)

* Sun Dec 23 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-5
- Enable building of separate tex-preview package
- Remove a few residual tetex references

* Sun Dec 16 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-4
- Add macros for automatic detection of Emacs version, site-lisp directory etc
- Make building of tex-preview subpackage optional, and disable for now
- Adjust Requires and BuildRequires for texlive
- Remove auctex-init.el since not needed
- Make RELEASE utf8

* Sat Aug  4 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-3
- Clarify license version
- Correct version and release requirement for the el package

* Sat Jan 13 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-2
- Update BuildRequires for texinfo-tex package

* Sat Jan 13 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-1
- Update to version 11.84
- Build all documentation and package in a -doc package

* Mon Aug 28 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-7
- Bump release for FC-6 mass rebuild

* Sun Jun 18 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-6
- Remove debug patch entry

* Sun Jun 18 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-5
- Bump release

* Sun Jun 18 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-4
- Bump release

* Sun Jun 18 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-3
- Sync with FC-5 spec file which includes the following changes
- No longer use makeinstall macro
- No longer specify texmf-dir, tex-dir for configure
- Main package now owns the site-lisp auctex and styles directories
- Place preview.dvi in correct directory, and have tetex-preview own
  it
- General cleanups

* Sat Jun 10 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-4
- Bump release

* Sat Jun 10 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-3
- Bump release. Wrap descriptions at column 70.

* Sat Jun 10 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-1
- Update to 11.83
- Add specific release requirement to tetex-preview Requires of main package

* Wed May 24 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-12
- Bump version number.

* Wed May 24 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-11
- Fix up whitespace for Ed. Bump version number.

* Thu May 18 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-9
- Split out tetex-preview subpackage
- Split out source elisp files
- Update package descriptions

* Mon May  1 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-8
- Add tetex-latex to BuildRequires

* Mon May  1 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-7
- Add ghostscript to Requires and BuildRequires

* Mon May  1 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-6
- Leave .nosearch file in styles directory - this directory shouldn't be in the load-path

* Mon May  1 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-5
- Move installation of the preview style files out of the texmf tree for now

* Mon Apr 24 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-4
- Added preview-latex
- Removed INSTALL document from package (not necessary)
- Clean up generation of startup files from spec file

* Thu Apr 20 2006 Ed Hill <ed@eh3.com> - 11.82-3
- fix startup file per bug# 189488

* Sun Apr  9 2006 Ed Hill <ed@eh3.com> - 11.82-2
- rebuild

* Sun Apr  9 2006 Ed Hill <ed@eh3.com> - 11.82-1
- update to 11.82

* Fri Sep 30 2005 Ed Hill <ed@eh3.com> - 11.81-2
- fix stupid tagging mistake

* Fri Sep 30 2005 Ed Hill <ed@eh3.com> - 11.81-1
- update to 11.81
- disable preview for now since it needs some packaging work

* Tue Sep  6 2005 Ed Hill <ed@eh3.com> - 11.55-5
- bugzilla 167439

* Tue Aug  9 2005 Ed Hill <ed@eh3.com> - 11.55-4
- call it BuildArch

* Tue Aug  9 2005 Ed Hill <ed@eh3.com> - 11.55-3
- add Requires and BuildRequires

* Mon Aug  8 2005 Ed Hill <ed@eh3.com> - 11.55-2
- modify for acceptance into Fedora Extras

* Fri Jan 21 2005 David Kastrup <dak@gnu.org>
- Conflict with outdated Emacspeak versions

* Fri Jan 14 2005 David Kastrup <dak@gnu.org>
- Install and remove auctex.info, not auctex

* Thu Aug 19 2004 David Kastrup <dak@gnu.org>
- Change tex-site.el to overwriting config file mode.  New naming scheme.

* Mon Aug 16 2004 David Kastrup <dak@gnu.org>
- Attempt a bit of SuSEism.  Might work if we are lucky.

* Sat Dec  7 2002 David Kastrup <David.Kastrup@t-online.de>
- Change addresses to fit move to Savannah.

* Mon Apr 15 2002 Jan-Ake Larsson <jalar@imf.au.dk>
- Adjusted TeX-macro-global and put autoactivation in preinstall
  script so that it can be chosen at install time.

* Tue Feb 19 2002 Jan-Ake Larsson <jalar@imf.au.dk>
- Added site-start.el support

* Sat Feb 16 2002 Jan-Ake Larsson <jalar@imf.au.dk>
- Prerelease 11.11
