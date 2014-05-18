Name:		lilypond
Version:	2.16.2
Release:	2%{?dist}
Summary:	A typesetting system for music notation

Group:		Applications/Publishing
License:	GPLv3
URL:		http://www.lilypond.org
Source0:	http://download.linuxaudio.org/lilypond/sources/v2.15/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0:		lilypond-2.11.65-python26.patch
Patch1:		lilypond-2.21.2-gcc44-relocate.patch
#Patch2:		lilypond-2.15.38-backintime.patch

Requires:	ghostscript >= 8.15
Obsoletes: 	lilypond-fonts <= 2.12.1-1
Requires:	lilypond-century-schoolbook-l-fonts = %{version}-%{release}
Requires:	lilypond-emmentaler-fonts = %{version}-%{release}

Buildrequires:  t1utils bison flex ImageMagick gettext tetex
BuildRequires:  python-devel >= 2.4.0
BuildRequires:  mftrace >= 1.1.19
BuildRequires:  texinfo >= 4.8
BuildRequires:  compat-guile18-devel
BuildRequires:  ghostscript >= 8.15
BuildRequires:  pango-devel >= 1.12.0
BuildRequires:  fontpackages-devel
BuildRequires:	texlive-base
BuildRequires:	texi2html
BuildRequires:	perl-Pod-Parser

%description
LilyPond is an automated music engraving system. It formats music
beautifully and automatically, and has a friendly syntax for its input
files.

%package century-schoolbook-l-fonts
Summary:        Lilypond Century Schoolbook L fonts
Group:          User Interface/X
Requires:       fontpackages-filesystem
Requires:	lilypond-fonts-common = %{version}-%{release}
Obsoletes:	lilypond-centuryschl-fonts <= 2.12.1-3
BuildArch:	noarch

%description century-schoolbook-l-fonts 
LilyPond is an automated music engraving system. It formats music
beautifully and automatically, and has a friendly syntax for its input
files.

These are the Century Schoolbook L fonts included in the package.

%package emmentaler-fonts
Summary:        Lilypond emmentaler fonts
Group:          User Interface/X
Requires:       fontpackages-filesystem
Requires:	lilypond-fonts-common = %{version}-%{release}
BuildArch:	noarch

%description emmentaler-fonts 
LilyPond is an automated music engraving system. It formats music
beautifully and automatically, and has a friendly syntax for its input
files.

These are the emmentaler fonts included in the package.


%package fonts-common
Summary:        Lilypond fonts common dir
Group:          User Interface/X
Requires:       fontpackages-filesystem
Obsoletes:	lilypond-aybabtu-fonts <= 2.12.3-3
Obsoletes:	lilypond-feta-fonts <= 2.12.3-3
Obsoletes:	lilypond-feta-alphabet-fonts <= 2.12.3-3
Obsoletes:	lilypond-feta-braces-fonts <= 2.12.3-3
Obsoletes:	lilypond-parmesan-fonts <= 2.12.3-3
BuildArch:	noarch

%description fonts-common
LilyPond is an automated music engraving system. It formats music
beautifully and automatically, and has a friendly syntax for its input
files.

This contains the directory common to all lilypond fonts.

%prep
%setup -q

%patch0 -p0
%patch1 -p0
#%patch2 -p0

%build
export GUILE=/usr/bin/guile1.8
export GUILE_CONFIG=/usr/bin/guile1.8-config
export GUILE_TOOLS=/usr/bin/guile1.8-tools
%configure --without-kpathsea --disable-checking \
	--with-ncsb-dir=%{_datadir}/fonts/default/Type1
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT package_infodir=%{_infodir} \
	vimdir=%{_datadir}/vim/vim73

chmod +x $RPM_BUILD_ROOT%{_libdir}/%{name}/%{version}/python/midi.so

# Symlink lilypond-init.el in emacs' site-start.d directory
pushd $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
mkdir site-start.d
ln -s ../lilypond-init.el site-start.d
popd

# Change encoding to UTF8
pushd $RPM_BUILD_ROOT%{_infodir}
iconv -f iso-8859-1 -t utf-8 music-glossary.info > music-glossary.info.utf8
mv music-glossary.info.utf8 music-glossary.info
sed -e s,lilypond/,, -i *.info
popd

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%find_lang %{name}

mkdir -p $RPM_BUILD_ROOT%{_fontdir}
mv $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/otf/*.otf $RPM_BUILD_ROOT%{_fontdir}
rmdir $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/otf
ln -s %{_fontdir} $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/otf


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS.txt COPYING DEDICATION HACKING INSTALL.txt
%doc NEWS.txt README.txt ROADMAP THANKS VERSION
%{_bindir}/*
%{_libdir}/lilypond
%{_datadir}/lilypond
%{_datadir}/emacs/site-lisp
%{_datadir}/vim/vim*
%{_infodir}/*.gz
%{_mandir}/man1/*

%_font_pkg -n century-schoolbook-l CenturySchL*otf

%_font_pkg -n emmentaler emmentaler*otf

%files fonts-common
%doc COPYING
%defattr(0644,root,root,0755)

%dir %{_fontdir}


%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 07 2013 Jon Ciesla <limburgher@gmail.com> - 2.16.2-1
- New stable upstream.

* Sat Nov 10 2012 Jon Ciesla <limburgher@gmail.com> - 2.16.1-1
- New stable upstream.

* Fri Aug 24 2012 Jon Ciesla <limburgher@gmail.com> - 2.16.0-1
- New stable upstream.

* Sun Aug 12 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.95-1
- New upstream.

* Sat Aug 04 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.42-1
- New upstream.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 06 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.41-1
- New upstream.

* Wed Jun 06 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.40-2
- Make fonts noarch, BZ 826841.

* Wed Jun 06 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.40-1
- New upstream.

* Wed May 23 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.39-1
- RC.

* Fri May 11 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.38-2
- Patch for gcc bug, BZ 820998.

* Fri May 04 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.38-1
- New stable release.

* Fri Apr 20 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.37-1
- New upstream.
- Decruft spec.

* Mon Apr 09 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.36-1
- New upstream.

* Wed Mar 28 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.35-1
- New upstream.

* Tue Mar 20 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.34-1
- New upstream.

* Fri Mar 09 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.33-1
- New upstream.

* Tue Mar 06 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.32-1
- New upstream.

* Wed Feb 29 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.31-1
- New upstream.

* Sat Feb 18 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.30-1
- New upstream.

* Fri Feb 10 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.29-1
- New upstream.

* Sat Feb 04 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.28-1
- New upstream.

* Wed Jan 25 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.27-1
- New upstream.

* Tue Jan 17 2012 Dan Horák <dan[at]danny.cz> - 2.15.26-2
- excluding s390 is no longer needed

* Mon Jan 16 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.26-1
- New upstream.

* Sun Jan 08 2012 Jon Ciesla <limburgher@gmail.com> - 2.15.24-1
- New upstream.

* Wed Dec 28 2011 Jon Ciesla <limburgher@gmail.com> - 2.15.23-1
- New upstream.

* Fri Dec 16 2011 Jon Ciesla <limburgher@gmail.com> - 2.15.22-1
- New upstream.

* Thu Dec 08 2011 Jon Ciesla <limburgher@gmail.com> - 2.15.21-1
- New upstream.

* Mon Nov 28 2011 Jon Ciesla <limb@jcomserv.net> - 2.15.20-1
- New upstream.

* Tue Nov 22 2011 Jon Ciesla <limb@jcomserv.net> - 2.15.19-1
- New upstream.

* Sat Nov 12 2011 Jon Ciesla <limb@jcomserv.net> - 2.15.18-1
- New upstream.

* Fri Oct 28 2011 Jon Ciesla <limb@jcomserv.net> - 2.15.16-1
- New upstream.

* Fri Oct 21 2011 Jon Ciesla <limb@jcomserv.net> - 2.15.14-1
- New upstream.

* Thu Jul 28 2011 Jon Ciesla <limb@jcomserv.net> - 2.14.2-1
- New upstream.

* Mon Jun 13 2011 Jon Ciesla <limb@jcomserv.net> - 2.14.1-1
- New upstream.

* Mon Jun 06 2011 Jon Ciesla <limb@jcomserv.net> - 2.14.0-1
- New upstream.

* Tue May 31 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.63-1
- New upstream.

* Fri May 27 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.62-1
- New upstream.

* Mon May 02 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.61-1
- New upstream.

* Mon Apr 18 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.60-1
- New upstream.

* Mon Apr 11 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.59-1
- New upstream.

* Thu Apr 07 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.58-1
- New upstream.

* Mon Apr 04 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.57-1
- New upstream.

* Thu Mar 31 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.56-1
- New upstream.

* Fri Mar 25 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.55-1
- New upstream.

* Mon Mar 14 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.54-1
- New upstream.

* Fri Mar 11 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.53-2
- Fixed license tag, BZ 684215.

* Tue Mar 08 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.53-1
- New upstream.

* Wed Mar 02 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.52-1
- New upstream.

* Fri Feb 25 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.51-1
- New upstream.

* Mon Feb 14 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.50-1
- New upstream.

* Thu Feb 10 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.49-1
- New upstream.

* Tue Feb 08 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.48-1
- New upstream.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.47-1
- New upstream.

* Wed Jan 12 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.46-1
- New upstream.

* Wed Jan 12 2011 Dan Horák <dan[at]danny.cz> - 2.13.45-2
- exclude s390 because fontforge fails with an internal error

* Fri Jan 07 2011 Jon Ciesla <limb@jcomserv.net> - 2.13.45-1
- New upstream.

* Wed Dec 29 2010 Jon Ciesla <limb@jcomserv.net> - 2.13.39-3
- Scriptlet fix.

* Mon Dec 20 2010 Jon Ciesla <limb@jcomserv.net> - 2.13.39-2
- Update for new vim, BZ 663889.

* Mon Nov 15 2010 Jon Ciesla <limb@jcomserv.net> - 2.13.39-1
- Update to first Beta for 2.14.x to fix FTBFS BZ 631363.

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 2.12.3-3
- recompiling .py files against Python 2.7 (rhbz#623331)

* Thu Jul 15 2010 Jon Ciesla <limb@jcomserv.net> - 2.12.3-2
- Update for new licensing guidelines.

* Mon Jan 04 2010 Jon Ciesla <limb@jcomserv.net> - 2.12.3-1
- Update to 2.12.3.
- Dropped consts patch, upstreamed.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 01 2009 Jon Ciesla <limb@jcomserv.net> - 2.12.2-4
- Update for vim 7.2, BZ 503429.

* Wed Mar 04 2009 Caolán McNamara <caolanm@redhat.com> - 2.12.2-3
- fix up strchr const rets for const arg

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Jon Ciesla <limb@jcomserv.net> - 2.12.2-1
- Update to 2.12.2.
- Patch for gcc 4.4.

* Thu Feb 19 2009 Jon Ciesla <limb@jcomserv.net> - 2.12.1-6
- Split out feta and parmesan type1 fonts.

* Fri Jan 23 2009 Jon Ciesla <limb@jcomserv.net> - 2.12.1-5
- Final font corrections.

* Thu Jan 22 2009 Jon Ciesla <limb@jcomserv.net> - 2.12.1-4
- More font refinements.

* Wed Jan 21 2009 Jon Ciesla <limb@jcomserv.net> - 2.12.1-3
- Drop feta-fonts package cruft.

* Wed Jan 14 2009 Jon Ciesla <limb@jcomserv.net> - 2.12.1-2
- Implementing font_pkg.

* Tue Jan 06 2009 Jon Ciesla <limb@jcomserv.net> - 2.12.1-1
- Update to 2.12.1.
- Droppedn parse-scm patch, applied upstream.

* Tue Dec 30 2008 Jon Ciesla <limb@jcomserv.net> - 2.12.0-3
- Split out fonts subpackage, BZ 477416.

* Tue Dec 30 2008 Jon Ciesla <limb@jcomserv.net> - 2.12.0-2
- Re-fix Source0 URL.

* Wed Dec 17 2008 Jon Ciesla <limb@jcomserv.net> - 2.12.0-1
- New upstream, BZ 476836.
- Fixed Source0 URL.
- Patched to allow Python 2.6.
- Patch for parse-scm fix.

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.11.57-2
- Rebuild for Python 2.6

* Mon Sep 08 2008 Jon Ciesla <limb@jcomserv.net> - 2.11.57-1
- Upgrade to new upstream.

* Wed Aug 27 2008 Jon Ciesla <limb@jcomserv.net> - 2.10.33-4
- Spec cleanup, fix for BZ 456842, vim file locations.

* Mon Apr  7 2008 Christopher Aillon <caillon@redhat.com> - 2.10.33-3
- Fix the build against GCC 4.3; simply missing some #includes

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.10.33-2
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.10.33-1
- New release.
- Fix source URL.
- Change licence from GPL to GPLv2.

* Tue Aug 21 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.10.29-1
- New release. Remove old patch.

* Wed Aug  1 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.10.25-2
- Patch to fix problems with recent versions of fontforge.

* Fri Jul 27 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.10.25-1
- New release & new source URL.

* Tue Mar 20 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.10.20-1
- New release.

* Thu Feb 15 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.10.17-1
- New release. Fix bug 225410.

* Thu Jan 25 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.10.13-1
- New release.

* Wed Jan 17 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.10.11-1
- New release.

* Fri Jan  5 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.10.8-1
- New release.
- Fix source URL.

* Sat Dec 23 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.10.4-1
- New release.
- Finish fixing bug 219400.

* Wed Dec 13 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.10.2-2
- New release.
- Fix bug 219400.

* Mon Dec  4 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.10.1-1
- New release.

* Mon Nov 13 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.10.0-1
- New release. Update build requirements for 2.10 series.

* Fri Nov  3 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.8.8-1
- New release.

* Mon Oct  9 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.8.7-1
- New release.

* Wed Sep  6 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.8.6-2
- Rebuild for FC6
- Update directory for vim.
- Don't ghost .pyo files, as per changes in packaging guidelines (bug 205387).

* Thu Aug 10 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.8.6-1
- New release.

* Tue Jun  6 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.8.4-1
- New release.

* Sat May 20 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.8.3-1
- New upstream, remove patch.
- Put docs in separate SRPM.

* Mon May 15 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.8.2-3
- Fixes to dependencies, encoding of info files.
- Add docs as separate tarball (building them fails without ghostscript 8.50).

* Mon May 15 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.8.2-2
- Patch to fix segfault in fontconfig.

* Sat May 13 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.8.2-1
- New release.

* Tue May  2 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.8.1-4
- Add missing BuildRequires.
- Specify location of NCSB fonts to configure script.
- Disable parallel build.

* Tue Apr 25 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.8.1-3
- Make .so file executable.

* Tue Apr 25 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.8.1-2
- Use gettext.

* Mon Apr 10 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.8.1-1
- Initial build.
