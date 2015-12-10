# https://fedoraproject.org/wiki/Packaging:Haskell

# should get fixed in 3.1.5
# https://github.com/simonmar/alex/issues/62
%bcond_with tests
%bcond_without static

# no useful debuginfo for Haskell packages without C sources
%global debug_package %{nil}

Name:           alex
# part of haskell-platform
Version:        3.1.4
Release:        7%{?dist}
Summary:        Tool for generating lexical analysers in Haskell

License:        BSD
URL:            http://hackage.haskell.org/package/%{name}
Source0:        http://hackage.haskell.org/package/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-directory-devel
%if %{with tests}
BuildRequires:  ghc-process-devel
%endif
# End cabal-rpm deps
BuildRequires:  autoconf
BuildRequires:  docbook-style-xsl
BuildRequires:  libxslt
%if %{with static}
Requires:       %{name}-common = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
%endif

%description
Alex is a tool for generating lexical analysers in Haskell. It takes a
description of tokens based on regular expressions and generates a Haskell
module containing code for scanning text efficiently. It is similar to the tool
lex or flex for C/C++.


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


%prep
%setup -q


%build
%if %{with static}
%define ghc_without_dynamic 1
%ghc_bin_build
mv dist/build/%{name}/%{name}{,.static}
%undefine ghc_without_dynamic
%endif
%ghc_bin_build

cd doc
autoreconf
./configure --prefix=%{_prefix} --libdir=%{_libdir}
make html
cd ..


%install
%ghc_bin_install
%if %{with static}
mv %{buildroot}%{_bindir}/%{name}{,.dynamic}
install dist/build/%{name}/%{name}.static %{buildroot}%{_bindir}
touch %{buildroot}%{_bindir}/%{name}
rm %{buildroot}%{_pkgdocdir}/LICENSE
%endif


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


%files
%if %{with static}
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.dynamic
%else
%doc ANNOUNCE LICENSE README TODO doc/alex examples
%{_bindir}/%{name}
%{_datadir}/%{name}-%{version}
%endif


%if %{with static}
%files common
%doc ANNOUNCE LICENSE README TODO doc/alex examples
%{_datadir}/%{name}-%{version}


%files static
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.static
%endif


%changelog
* Fri Dec 04 2015 Liu Di <liudidi@gmail.com> - 3.1.4-7
- 为 Magic 3.0 重建

* Tue Nov 17 2015 Liu Di <liudidi@gmail.com> - 3.1.4-6
- 为 Magic 3.0 重建

* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 3.1.4-5
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 3.1.4-4
- 为 Magic 3.0 重建

* Mon Sep 21 2015 Liu Di <liudidi@gmail.com> - 3.1.4-3
- 为 Magic 3.0 重建

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 02 2015 Jens Petersen <petersen@redhat.com>
- update to 3.1.4

* Sun Aug  3 2014 Jens Petersen <petersen@redhat.com> - 3.1.3-1
- update to 3.1.3
- add static and common subpackages
- dynamic and static are handled as alternatives

* Tue Jun 10 2014 Jens Petersen <petersen@redhat.com> - 3.0.5-37
- update to cblrpm-0.8.11
- turn on tests

* Mon Apr 21 2014 Jens Petersen <petersen@redhat.com> - 3.0.5-36
- bang pattern patch no longer needed for ppc with ghc-7.6

* Mon Apr 21 2014 Jens Petersen <petersen@redhat.com> - 3.0.5-35
- bump over haskell-platform

* Fri Apr 11 2014 Jens Petersen <petersen@redhat.com> - 3.0.5-34
- split out of haskell-platform
- update to 3.0.5

* Wed Jun  6 2012 Jens Petersen <petersen@redhat.com> - 3.0.1-3
- BR alex on ppc archs!
- also apply bang pattern patch on ppc64

* Wed Jun  6 2012 Jens Petersen <petersen@redhat.com> - 3.0.1-2
- add fix-bang-pattern.diff patch from Debian to fix build on ppc

* Tue Mar 20 2012 Jens Petersen <petersen@redhat.com> - 3.0.1-1
- update to 3.0.1
- depends on QuickCheck

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.5-6.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.3.5-5.2
- rebuild with new gmp without compat lib

* Mon Oct 10 2011 Peter Schiffer <pschiffe@redhat.com> - 2.3.5-5.1
- rebuild with new gmp

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 2.3.5-5
- ghc_arches replaces ghc_excluded_archs

* Mon Jun 20 2011 Jens Petersen <petersen@redhat.com> - 2.3.5-4
- BR ghc-Cabal-devel
- use ghc_excluded_archs

* Wed May 18 2011 Jens Petersen <petersen@redhat.com> - 2.3.5-3
- add ppc64

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.3.5-2
- Enable build on sparcv9

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 2.3.5-1
- update to 2.3.5 for haskell-platform-2011.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Jens Petersen <petersen@redhat.com> - 2.3.4-2
- update to cabal2spec-0.22.4
- BR ghc-devel

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 2.3.4-1
- update to 2.3.4

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 2.3.3-2
- rebuild

* Fri Jul 30 2010 Jens Petersen <petersen@redhat.com>
- update to simpler url

* Fri Jul 16 2010 Jens Petersen <petersen@redhat.com> - 2.3.3-1
- 2.3.3 release for haskell-platform-2010.2.0.0

* Sun Jun 27 2010 Jens Petersen <petersen@redhat.com> - 2.3.2-3
- sync cabal2spec-0.22.1

* Sat Apr 24 2010 Jens Petersen <petersen@redhat.com> - 2.3.2-2
- rebuild against ghc-6.12.2

* Wed Mar 24 2010 Jens Petersen <petersen@redhat.com> - 2.3.2-1
- update to 2.3.2 for haskell-platform-2010.1.0.0

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 2.3.1-8
- dynamic bcond is now handled by cabal_configure
- drop redundant buildroot and its install cleaning

* Tue Dec 22 2009 Jens Petersen <petersen@redhat.com>
- add bcond for dynamic linking

* Mon Dec 21 2009 Jens Petersen <petersen@redhat.com> - 2.3.1-7
- build dynamically with ghc-6.12.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Jens Petersen <petersen@redhat.com> - 2.3.1-5
- buildrequires ghc-rpm-macros

* Fri Apr 24 2009 Jens Petersen <petersen@redhat.com> - 2.3.1-4
- rebuild against ghc-6.10.2

* Tue Mar 10 2009 Jens Petersen <petersen@redhat.com> - 2.3.1-3
- update arch list and bring closer to cabal2spec-0.12

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Jens Petersen <petersen@redhat.com> - 2.3.1-1
- update to 2.3.1
- no longer need alex-2.3-base3.patch

* Tue Nov 25 2008 Jens Petersen <petersen@redhat.com> - 2.3-2
- build with new macros
- update urls to point to hackage
- add alex-2.3-base3.patch to build with base-3 for ghc-6.10.1

* Mon Oct 13 2008 Bryan O'Sullivan <bos@serpentine.com> - 2.3-1
- Update to 2.3

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.2-3
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2-2
- Autorebuild for GCC 4.3

* Fri Jan  4 2008 Jens Petersen <petersen@redhat.com> - 2.2-1
- update to 2.2 release

* Fri Nov 23 2007 Bryan O'Sullivan <bos@serpentine.com> - 2.1.0-6
- Exclude alpha

* Tue Sep 25 2007 Bryan O'Sullivan <bos@serpentine.com> - 2.1.0-5
- don't try to build on ppc64

* Tue Sep 25 2007 Bryan O'Sullivan <bos@serpentine.com> - 2.1.0-4
- build requires autoconf

* Sun Jul 22 2007 Bryan O'Sullivan <bos@serpentine.com> - 2.1.0-3
- apply a few cleanups from Jens Petersen

* Thu Apr 26 2007 Bryan O'Sullivan <bos@serpentine.com> - 2.1.0-2
- fix a few style issues

* Fri Jan 19 2007 Bryan O'Sullivan <bos@serpentine.com> - 2.1.0-1
- update to 2.1.0
- fix rpmlint errors

* Fri May  6 2005 Jens Petersen <petersen@redhat.com> - 2.0.1-1
- initial packaging for Fedora Haskell based on upstream spec file
