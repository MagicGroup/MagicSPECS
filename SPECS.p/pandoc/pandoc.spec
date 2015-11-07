# https://fedoraproject.org/wiki/Packaging:Haskell

%bcond_without static

%global pkg_name pandoc

%bcond_with tests

Name:           %{pkg_name}
Version:        1.13.2
Release:        6%{?dist}
Summary:        Conversion between markup formats

License:        GPLv2+
Url:            https://hackage.haskell.org/package/%{name}
Source0:        https://hackage.haskell.org/package/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  chrpath
BuildRequires:  ghc-HTTP-devel
BuildRequires:  ghc-JuicyPixels-devel
BuildRequires:  ghc-SHA-devel
BuildRequires:  ghc-aeson-devel
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-base64-bytestring-devel
BuildRequires:  ghc-binary-devel
BuildRequires:  ghc-blaze-html-devel
BuildRequires:  ghc-blaze-markup-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-data-default-devel
BuildRequires:  ghc-deepseq-generics-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-extensible-exceptions-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-haddock-library-devel
BuildRequires:  ghc-highlighting-kate-devel
BuildRequires:  ghc-hslua-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-old-time-devel
BuildRequires:  ghc-pandoc-types-devel
BuildRequires:  ghc-parsec-devel
BuildRequires:  ghc-process-devel
BuildRequires:  ghc-random-devel
BuildRequires:  ghc-scientific-devel
BuildRequires:  ghc-syb-devel
BuildRequires:  ghc-tagsoup-devel
BuildRequires:  ghc-temporary-devel
BuildRequires:  ghc-texmath-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-unordered-containers-devel
BuildRequires:  ghc-vector-devel
BuildRequires:  ghc-xml-devel
BuildRequires:  ghc-yaml-devel
BuildRequires:  ghc-zip-archive-devel
BuildRequires:  ghc-zlib-devel
%if %{with tests}
BuildRequires:  ghc-Diff-devel
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-ansi-terminal-devel
BuildRequires:  ghc-executable-path-devel
BuildRequires:  ghc-test-framework-devel
BuildRequires:  ghc-test-framework-hunit-devel
BuildRequires:  ghc-test-framework-quickcheck2-devel
%endif
# End cabal-rpm deps
%if %{with static}
Requires:       %{name}-common = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
%endif

%description
Pandoc is a Haskell library for converting from one markup format to another,
and a command-line tool that uses this library. It can read markdown and
(subsets of) HTML, reStructuredText, LaTeX, DocBook, MediaWiki markup, TWiki
markup, Haddock markup, OPML, Emacs Org-Mode, txt2tags and Textile, and it can
write markdown, reStructuredText, XHTML, HTML 5, LaTeX, ConTeXt, DocBook, OPML,
OpenDocument, ODT, Word docx, RTF, MediaWiki, DokuWiki, Textile, groff man
pages, plain text, Emacs Org-Mode, AsciiDoc, Haddock markup, EPUB (v2 and v3),
FictionBook2, InDesign ICML, and several kinds of HTML/javascript slide shows
(S5, Slidy, Slideous, DZSlides, reveal.js).

Pandoc extends standard markdown syntax with footnotes, embedded LaTeX,
definition lists, tables, and other features. A compatibility mode is provided
for those who need a drop-in replacement for Markdown.pl.

In contrast to existing tools for converting markdown to HTML, which use regex
substitutions, pandoc has a modular design: it consists of a set of readers,
which parse text in a given format and produce a native representation of the
document, and a set of writers, which convert this native representation into a
target format. Thus, adding an input or output format requires only adding a
reader or writer.

For pdf output please also install pandoc-pdf.


%if %{with static}
%package common
Summary:        Common files for %{name}

%description common
This provides the common files for %{name}.


%package static
Summary:        Static Haskell build
Requires:       %{name}-common = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description static
This provides a build with Haskell libraries statically linked.
%endif


%package -n ghc-%{name}
Summary:        Haskell %{name} library
%if %{with static}
Requires:       %{name}-common = %{version}-%{release}
%endif

%description -n ghc-%{name}
This package provides the Haskell %{name} shared library.


%package -n ghc-%{name}-devel
Summary:        Haskell %{name} library development files
Provides:       ghc-%{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       ghc-%{name}%{?_isa} = %{version}-%{release}

%description -n ghc-%{name}-devel
This package provides the Haskell %{name} library development files.


%package pdf
Summary:        Metapackage for pandoc pdf support
Requires:       %{name} = %{version}
Requires:       texlive-collection-latex
Requires:       texlive-ec
Obsoletes:      pandoc-markdown2pdf < %{version}-%{release}

%description pdf
This package pulls in the TeXLive latex package collection needed by
pandoc to generate pdf output using pdflatex.

To use --latex-engine=xelatex or lualatex, install texlive-collection-xetex
or texlive-collection-luatex respectively.


%prep
%setup -q
cabal-tweak-flag https False
cabal-tweak-flag network-uri False


%build
%if %{with static}
%define ghc_without_dynamic 1
%ghc_bin_build
mv dist/build/%{name}/%{name}{,.static}
%undefine ghc_without_dynamic
%endif
%ghc_lib_build


%install
%ghc_lib_install
%ghc_fix_dynamic_rpath pandoc
%if %{with static}
mv %{buildroot}%{_bindir}/%{name}{,.dynamic}
install dist/build/%{name}/%{name}.static %{buildroot}%{_bindir}
touch %{buildroot}%{_bindir}/%{name}
rm %{buildroot}%{_pkgdocdir}/COPYING
%endif

rm %{buildroot}%{_datadir}/%{name}-%{version}/{COPYRIGHT,README}

ln -s pandoc %{buildroot}%{_bindir}/hsmarkdown

install -m 0644 -p -D man/man1/pandoc.1 %{buildroot}%{_mandir}/man1/pandoc.1
install -m 0644 -p -D man/man5/pandoc_markdown.5 %{buildroot}%{_mandir}/man5/pandoc_markdown.5


%check
%if %{with tests}
%cabal test
%endif


%if %{with static}
# avoid rpm ghost keeping pre-alternatives binary around
%pre
if [ $1 -gt 1 ] ; then
  if [ -f %{_bindir}/%{name} -a ! -L %{_bindir}/%{name} ]; then
      rm %{_bindir}/%{name}
  fi
fi


%post
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.dynamic 70


%postun
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.dynamic
fi


# avoid rpm ghost keeping pre-alternatives binary around
%pre static
if [ $1 -gt 1 ] ; then
  if [ -f %{_bindir}/%{name} -a ! -L %{_bindir}/%{name} ]; then
      rm %{_bindir}/%{name}
  fi
fi


%post static
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.static 30


%postun static
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.static
fi
%endif


%post -n ghc-%{name}-devel
%ghc_pkg_recache


%postun -n ghc-%{name}-devel
%ghc_pkg_recache


%files
%if %{with static}
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.dynamic
%else
%doc BUGS COPYING COPYRIGHT README* changelog
%attr(755,root,root) %{_bindir}/%{name}
%endif


%files pdf


%if %{with static}
%files common
%doc BUGS COPYING COPYRIGHT README* changelog
%attr(-,root,root) %{_bindir}/hsmarkdown
%{_datadir}/%{name}-%{version}
%attr(644,root,root) %{_mandir}/man1/pandoc.1*
%attr(644,root,root) %{_mandir}/man5/*


%files static
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.static
%endif


%files -n ghc-%{name} -f ghc-%{name}.files
%doc COPYING COPYRIGHT


%files -n ghc-%{name}-devel -f ghc-%{name}-devel.files


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.13.2-6
- 为 Magic 3.0 重建

* Mon Sep 21 2015 Liu Di <liudidi@gmail.com> - 1.13.2-5
- 为 Magic 3.0 重建

* Mon Aug 31 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.13.2-4
- Rebuild (aarch64 vector hashes)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar  4 2015 Jens Petersen <petersen@fedoraproject.org> - 1.13.2-2
- rebuild

* Mon Jan 26 2015 Jens Petersen <petersen@redhat.com> - 1.13.2-1
- update to 1.13.2

* Thu Dec 11 2014 Jens Petersen <petersen@redhat.com> - 1.12.3.3-6
- add a static alternative subpackage and a common subpackage

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Adam Williamson <awilliam@redhat.com> - 1.12.3.3-3
- rebuild for new ghc-scientific

* Tue May 13 2014 Jens Petersen <petersen@redhat.com> - 1.12.3.3-2
- fix building on ARM (llvm) by using -O1 (#992430)

* Thu May 08 2014 Jens Petersen <petersen@redhat.com> - 1.12.3.3-1
- update to 1.12.3.3

* Wed Jan 22 2014 Jens Petersen <petersen@redhat.com> - 1.12.3.1-1
- update to 1.12.3.1
- disable http-conduit

* Wed Aug 28 2013 Jens Petersen <petersen@redhat.com> - 1.11.1-6
- temporarily exclude armv7hl since build with ghc-7.6.3 and llvm-3.3 hanging
  mysteriously (#992430)

* Tue Aug 06 2013 Adam Williamson <awilliam@redhat.com> - 1.11.1-5
- rebuild for new libbibutils

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Jens Petersen <petersen@redhat.com>
- update to new simplified Haskell Packaging Guidelines

* Wed May  1 2013 Jens Petersen <petersen@redhat.com> - 1.11.1-2
- pandoc-pdf now requires texlive-collection-latex and texlive-ec (#957876)

* Fri Mar 22 2013 Jens Petersen <petersen@redhat.com> - 1.11.1-1
- update to 1.11.1

* Sun Mar 10 2013 Jens Petersen <petersen@redhat.com> - 1.10.1-1
- update to 1.10.1
- allow blaze-html-0.6

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Jens Petersen <petersen@redhat.com> - 1.9.4.5-4
- rebuild

* Mon Nov 19 2012 Jens Petersen <petersen@redhat.com> - 1.9.4.5-3
- rebuild

* Wed Oct 31 2012 Jens Petersen <petersen@redhat.com> - 1.9.4.5-2
- drop the latex template patch for old TeXLive

* Fri Oct 26 2012 Jens Petersen <petersen@redhat.com> - 1.9.4.5-1
- update to 1.9.4.5
- refresh with cabal-rpm

* Fri Oct 26 2012 Jens Petersen <petersen@redhat.com> - 1.9.4.2-6
- disable threaded rts with upstream patch copied from Debian (#862543)

* Tue Oct  2 2012 Jens Petersen <petersen@redhat.com> - 1.9.4.2-5
- add a files section for the pdf subpackage so it is actually created

* Tue Oct  2 2012 Jens Petersen <petersen@redhat.com> - 1.9.4.2-4
- add a pdf meta-subpackage for the texlive packages needed for pdf output

* Fri Sep 28 2012 Jens Petersen <petersen@redhat.com> - 1.9.4.2-3
- also disable luatex in the default.beamer template (#861300)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 15 2012 Jens Petersen <petersen@redhat.com> - 1.9.4.2-1
- update to 1.9.4.2
- add hsmarkdown symlink
- change prof BRs to devel

* Thu Jun 21 2012 Jens Petersen <petersen@redhat.com> - 1.9.4.1-2
- rebuild

* Sun Jun 10 2012 Jens Petersen <petersen@redhat.com> - 1.9.4.1-1
- update to 1.9.4.1

* Wed Apr 25 2012 Jens Petersen <petersen@redhat.com> - 1.9.2-1
- update to 1.9.2

* Wed Mar 21 2012 Jens Petersen <petersen@redhat.com> - 1.9.1.2-1
- update to 1.9.1.2

* Wed Mar  7 2012 Jens Petersen <petersen@redhat.com> - 1.9.1.1-2
- rebuild

* Mon Feb 13 2012 Jens Petersen <petersen@redhat.com> - 1.9.1.1-1
- update to 1.9.1.1
  http://johnmacfarlane.net/pandoc/releases.html#pandoc-1.9-2012-02-05
- new depends on blaze-html, temporary, zlib
- markdown2pdf is now handled by pandoc itself:
  add README.fedora file documenting required texlive packages
- add changelog file

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1.8.2.1-9
- Rebuild against PCRE 8.30

* Tue Feb  7 2012 Jens Petersen <petersen@redhat.com> - 1.8.2.1-8
- rebuild

* Thu Jan 26 2012 Jens Petersen <petersen@redhat.com> - 1.8.2.1-7
- set highlighting build flag by patching instead to help dependency tracking

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 1.8.2.1-6
- update to cabal2spec-0.25.2

* Thu Dec 22 2011 Jens Petersen <petersen@redhat.com> - 1.8.2.1-5
- workaround texlive-2007 xelatex outputting to current dir

* Wed Nov 30 2011 Jens Petersen <petersen@redhat.com> - 1.8.2.1-4
- add missing requires for pdflatex

* Thu Nov 17 2011 Jens Petersen <petersen@redhat.com> - 1.8.2.1-3
- disable ifluatex in default.latex for texlive-2007 (Luis Villa, #752621)
- subpackage markdown2pdf and make it require texlive-xetex

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.8.2.1-2.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 1.8.2.1-2.1
- rebuild with new gmp

* Mon Oct  3 2011 Jens Petersen <petersen@redhat.com> - 1.8.2.1-2
- rebuild against newer dependencies

* Thu Aug  4 2011 Jens Petersen <petersen@redhat.com> - 1.8.2.1-1
- update to 1.8.2.1
- depends on base64-bytestring

* Wed Jul 27 2011 Jens Petersen <petersen@redhat.com> - 1.8.1.2-3
- rebuild for xml-1.3.9

* Fri Jul 22 2011 Jens Petersen <petersen@redhat.com> - 1.8.1.2-2
- rebuild for highlighting-kate-0.2.10

* Thu Jul 21 2011 Jens Petersen <petersen@redhat.com> - 1.8.1.2-1
- update to 1.8.1.2

* Wed Jul 13 2011 Jens Petersen <petersen@redhat.com> - 1.8.1.1-3
- build with code highlighting support using highlighting-kate

* Wed Jun 22 2011 Jens Petersen <petersen@redhat.com> - 1.8.1.1-2
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Sat May 28 2011 Jens Petersen <petersen@redhat.com> - 1.8.1.1-1
- update to 1.8.1.1
- update to cabal2spec-0.23: add ppc64
- new depends on citeproc-hs, dlist, json, pandoc-types, tagsoup
- new pandoc_markdown.5 manpage

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.6.0.1-5
- Enable build on sparcv9

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 1.6.0.1-4
- rebuild for latest zip-archive and haskell-platform-2011.1 updates

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Jens Petersen <petersen@redhat.com> - 1.6.0.1-2
- fix manpage perms (narasim)
- improve the summary (#652582)

* Fri Jan 14 2011 Jens Petersen <petersen@redhat.com> - 1.6.0.1-1
- 1.6.0.1
- add description
- update to cabal2spec-0.22.4

* Fri Nov 12 2010 Jens Petersen <petersen@redhat.com> - 1.6-1
- GPLv2+
- take care of docdir files
- add dependencies

* Thu Nov 11 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 1.6-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
