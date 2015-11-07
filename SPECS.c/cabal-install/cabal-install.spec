# https://fedoraproject.org/wiki/Packaging:Haskell

%bcond_with tests
%bcond_without static

%global binname cabal

Name:           cabal-install
# part of haskell-platform
Version:        1.18.1.0
Release:        4%{?dist}
Summary:        Command-line interface for Cabal and Hackage

License:        BSD
URL:            http://hackage.haskell.org/package/%{name}
Source0:        http://hackage.haskell.org/package/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:        cabal-install.sh
Patch0:         cabal-install-quieter-selfupgrade.patch
Patch1:         cabal-install-no-network-uri.patch

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-HTTP-devel
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-pretty-devel
BuildRequires:  ghc-process-devel
BuildRequires:  ghc-random-devel
BuildRequires:  ghc-stm-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-unix-devel
BuildRequires:  ghc-zlib-devel
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-test-framework-devel
BuildRequires:  ghc-test-framework-hunit-devel
BuildRequires:  ghc-test-framework-quickcheck2-devel
%endif
# End cabal-rpm deps
Requires:       ghc-compiler
# for /etc/bash_completion.d/
Requires:       filesystem
# for /etc/profile.d/
Requires:       setup
Obsoletes:      cabal-dev < 0.9.2-5
%if %{with static}
Requires:       %{name}-common = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
%endif

%description
The 'cabal' command-line program simplifies the process of managing Haskell
software by automating the fetching, configuration, compilation and
installation of Haskell libraries and programs from Hackage.


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
%patch0 -p1 -b .orig
%patch1 -p1 -b .orig

cabal-tweak-flag network-uri False


%build
%if %{with static}
%define ghc_without_dynamic 1
%ghc_bin_build
mv dist/build/%{binname}/%{binname}{,.static}
%undefine ghc_without_dynamic
%endif
%ghc_bin_build


%install
%ghc_bin_install
%if %{with static}
mv %{buildroot}%{_bindir}/%{binname}{,.dynamic}
install dist/build/%{binname}/%{binname}.static %{buildroot}%{_bindir}
touch %{buildroot}%{_bindir}/%{binname}
rm %{buildroot}%{_pkgdocdir}/LICENSE
%endif

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
cp -p bash-completion/cabal $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d


%check
%if %{with tests}
%cabal test
%endif


%if %{with static}
# avoid rpm ghost keeping pre-alternatives binary around
%pre
if [ $1 -gt 1 ] ; then
  if [ -f %{_bindir}/%{binname} -a ! -L %{_bindir}/%{binname} ]; then
      rm %{_bindir}/%{binname}
  fi
fi


%post
%{_sbindir}/update-alternatives --install %{_bindir}/%{binname} \
  %{name} %{_bindir}/%{binname}.dynamic 70


%postun
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{binname}.dynamic
fi


# avoid rpm ghost keeping pre-alternatives binary around
%pre static
if [ $1 -gt 1 ] ; then
  if [ -f %{_bindir}/%{binname} -a ! -L %{_bindir}/%{binname} ]; then
      rm %{_bindir}/%{binname}
  fi
fi


%post static
%{_sbindir}/update-alternatives --install %{_bindir}/%{binname} \
  %{name} %{_bindir}/%{binname}.static 30


%postun static
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{binname}.static
fi
%endif


%files
%if %{with static}
%ghost %{_bindir}/%{binname}
%{_bindir}/%{binname}.dynamic
%else
%doc LICENSE README
%{_bindir}/cabal
%config(noreplace) %{_sysconfdir}/bash_completion.d/cabal
%config(noreplace) %{_sysconfdir}/profile.d/cabal-install.sh
%endif


%if %{with static}
%files common
%doc LICENSE README
%config(noreplace) %{_sysconfdir}/bash_completion.d/cabal
%config(noreplace) %{_sysconfdir}/profile.d/cabal-install.sh


%files static
%ghost %{_bindir}/%{binname}
%{_bindir}/%{binname}.static
%endif


%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.18.1.0-4
- 为 Magic 3.0 重建

* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 1.18.1.0-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Jens Petersen <petersen@redhat.com> - 1.18.1.0-1
- security version update for upload command

* Thu Apr  2 2015 Jens Petersen <petersen@redhat.com> - 1.18.0.8-1
- update to 1.18.0.8

* Thu Aug  7 2014 Jens Petersen <petersen@redhat.com> - 1.18.0.5-1
- update to 1.18.0.5
- obsolete cabal-dev
- add static and common subpackages

* Tue Jul  8 2014 Jens Petersen <petersen@redhat.com> - 1.16.0.2-35
- f21 rebuild

* Fri Apr 18 2014 Jens Petersen <petersen@redhat.com> - 1.16.0.2-34
- bump release over haskell-platform

* Thu Apr 17 2014 Jens Petersen <petersen@redhat.com> - 1.16.0.2-32
- mark bash_completion.d and profile.d files as config (#1069062)
- require filesystem and setup to own the sysconfig dirs (#1069062)

* Mon Feb 24 2014 Jens Petersen <petersen@redhat.com> - 1.16.0.2-31
- update to 1.16.0.2
- split out of haskell-platform (#1069062)
- only show cabal-install upgrade notice for verbose

* Tue May  8 2012 Jens Petersen <petersen@redhat.com> - 0.14.0-1
- update to 0.14.0 release

* Tue Mar 20 2012 Jens Petersen <petersen@redhat.com> - 0.13.3-0.1
- update to latest darcs

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 28 2011 Jens Petersen <petersen@redhat.com> - 0.10.2-6
- rebuild for haskell-platform-2011.4.0.0

* Fri Dec 16 2011 Jens Petersen <petersen@redhat.com> - 0.10.2-5
- bring back requires ghc-compiler (Stanislav Ochotnicky, #760461)

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.10.2-4.2
- rebuild with new gmp without compat lib

* Mon Oct 10 2011 Peter Schiffer <pschiffe@redhat.com> - 0.10.2-4.1
- rebuild with new gmp

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 0.10.2-4
- ghc_arches replaces ghc_excluded_archs

* Mon Jun 20 2011 Jens Petersen <petersen@redhat.com> - 0.10.2-3
- BR ghc-Cabal-devel and use ghc_excluded_archs
- drop ghc requires to allow local ghc

* Wed May 25 2011 Jens Petersen <petersen@redhat.com> - 0.10.2-2
- add ppc64

* Fri Mar 11 2011 Jens Petersen <petersen@redhat.com> - 0.10.2-1
- update to 0.10.2

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.9.6-0.2
- Enable build on sparcv9

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 0.9.6-0.1
- update to 0.9.6 pre snapshot

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 0.9.5-0.5
- rebuild for haskell-platform-2011.1 updates

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 23 2011 Jens Petersen <petersen@redhat.com> - 0.9.5-0.3
- update to cabal2spec-0.22.4
- BR ghc-devel

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 0.9.5-0.2
- rebuild with HTTP-4000.1.1

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 0.9.5-0.1
- update to current 0.9.5 snapshot

* Fri Jul 16 2010 Jens Petersen <petersen@redhat.com> - 0.8.2-1
- update to 0.8.2 for haskell-platform-2010.2.0.0

* Sun Jun 27 2010 Jens Petersen <petersen@redhat.com> - 0.8.0-5
- sync cabal2spec-0.22.1

* Wed May 19 2010 Jens Petersen <petersen@redhat.com> - 0.8.0-4
- append ~/.cabal/bin to PATH (if dir exists) with new
  /etc/profile.d/cabal-install.sh (#509699)

* Tue Apr 27 2010 Jens Petersen <petersen@redhat.com> - 0.8.0-3
- rebuild against ghc-6.12.2

* Tue Mar 23 2010 Jens Petersen <petersen@redhat.com> - 0.8.0-2
- rebuild against HTTP-4000.0.9 for haskell-platform-2010.1.0.0

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.8.0-1
- update to 0.8.0 for ghc-6.12.1
- add dynamic bcond
- drop redundant buildroot and its install cleaning

* Wed Sep 16 2009 Jens Petersen <petersen@redhat.com> - 0.6.2-6
- really rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Jens Petersen <petersen@redhat.com> - 0.6.2-4
- buildrequires ghc-rpm-macros (cabal-0.16)

* Sun Apr 26 2009 Jens Petersen <petersen@redhat.com> - 0.6.2-3
- rebuild against ghc-6.10.2

* Fri Feb 27 2009 Jens Petersen <petersen@redhat.com> - 0.6.2-2
- update for cabal2spec-0.11:
- use global
- fix source url
- add ix86 and alpha archs

* Mon Feb 23 2009 Jens Petersen <petersen@redhat.com> - 0.6.2-1
- update to 0.6.2 release

* Mon Feb  9 2009 Jens Petersen <petersen@redhat.com> - 0.6.0-3
- fix source url

* Wed Jan  7 2009 Jens Petersen <petersen@redhat.com> - 0.6.0-2
- add bash completion file
- update cabal build macro

* Tue Nov 11 2008 Jens Petersen <petersen@redhat.com> - 0.6.0-1
- initial package for Fedora
