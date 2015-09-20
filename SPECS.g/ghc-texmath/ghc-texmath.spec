# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name texmath

%ifnarch armv7hl
%bcond_without tests
%endif

Name:           ghc-%{pkg_name}
Version:        0.8.0.1
Release:        4%{?dist}
Summary:        Conversion between formats used to represent mathematics

License:        GPLv2+
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-pandoc-types-devel
BuildRequires:  ghc-parsec-devel
BuildRequires:  ghc-syb-devel
BuildRequires:  ghc-xml-devel
%if %{with tests}
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-process-devel
BuildRequires:  ghc-split-devel
BuildRequires:  ghc-temporary-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-utf8-string-devel
%endif
# End cabal-rpm deps

%description
The texmath library provides functions to read and write TeX math, presentation
MathML, and OMML (Office Math Markup Language, used in Microsoft Office).
Support is also included for converting math formats to pandoc's native format
(allowing conversion, via pandoc, to a variety of different markup formats).
The TeX reader supports basic LaTeX and AMS extensions, and it can parse and
apply LaTeX macros. (See <http://johnmacfarlane.net/texmath here> for a live
demo of bidirectional conversion between LaTeX and MathML.)


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides the Haskell %{pkg_name} library development files.


%prep
%setup -q -n %{pkg_name}-%{version}
cabal-tweak-flag network-uri False


%build
%ghc_lib_build


%install
%ghc_lib_install


%check
%ifarch aarch64
LANG=en_US.utf8
%endif
%cabal_test


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE


%files devel -f %{name}-devel.files
%doc README.markdown


%changelog
* Mon Aug 31 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.0.1-4
- Rebuild (aarch64 vector hashes)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 15 2015 Jens Petersen <petersen@redhat.com> - 0.8.0.1-2
- run tests in utf8 on aarch64

* Sun Feb  1 2015 Jens Petersen <petersen@redhat.com> - 0.8.0.1-1
- update to 0.8.0.1
- disable tests on armv7

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 08 2014 Jens Petersen <petersen@redhat.com> - 0.6.6.1-1
- update to 0.6.6.1

* Wed Jan 22 2014 Jens Petersen <petersen@redhat.com> - 0.6.6-1
- update to 0.6.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 05 2013 Jens Petersen <petersen@redhat.com> - 0.6.1.5-2
- update to new simplified Haskell Packaging Guidelines

* Wed Jun 05 2013 Jens Petersen <petersen@redhat.com> - 0.6.1.5-1
- update to 0.6.1.5

* Sun Mar 10 2013 Jens Petersen <petersen@redhat.com> - 0.6.1.3-1
- update to 0.6.1.3

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Jens Petersen <petersen@redhat.com> - 0.6.1.1-1
- update to 0.6.1.1
- update summary and description

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.6.0.6-2
- change prof BRs to devel

* Wed Jun 13 2012 Jens Petersen <petersen@redhat.com> - 0.6.0.6-1
- update to 0.6.0.6

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 0.6.0.3-2
- add license to ghc_files

* Sun Feb 12 2012 Jens Petersen <petersen@redhat.com> - 0.6.0.3-1
- update to 0.6.0.3

* Tue Feb  7 2012 Jens Petersen <petersen@redhat.com> - 0.5.0.4-2
- rebuild

* Thu Jan  5 2012 Jens Petersen <petersen@redhat.com> - 0.5.0.4-1
- update to 0.5.0.4 and cabal2spec-0.25.2

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.5.0.1-3.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.5.0.1-3.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.5.0.1-3.1
- rebuild with new gmp

* Wed Jul 27 2011 Jens Petersen <petersen@redhat.com> - 0.5.0.1-3
- rebuild for xml-1.3.9

* Wed Jun 22 2011 Jens Petersen <petersen@redhat.com> - 0.5.0.1-2
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Sat May 28 2011 Jens Petersen <petersen@redhat.com> - 0.5.0.1-1
- update to 0.5.0.1
- update to cabal2spec-0.23: add ppc64

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.4-6
- Enable build on sparcv9

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 0.4-5
- rebuild for haskell-platform-2011.1 updates

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Jens Petersen <petersen@redhat.com> - 0.4-3
- update to cabal2spec-0.22.4

* Tue Dec 21 2010 Jens Petersen <petersen@redhat.com> - 0.4-2
- need depends on syb for ghc-7.0

* Fri Nov 12 2010 Jens Petersen <petersen@redhat.com> - 0.4-1
- GPLv2+
- add deps and description
- remove unused tests and cgi data files

* Fri Nov 12 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.4-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
