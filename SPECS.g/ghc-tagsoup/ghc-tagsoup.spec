# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name tagsoup

Name:           ghc-%{pkg_name}
Version:        0.13.3
Release:        4%{?dist}
Summary:        Parsing and extracting from HTML/XML documents

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-text-devel
# End cabal-rpm deps

%description
TagSoup is a library for parsing HTML/XML. It supports the HTML 5
specification, and can be used to parse either well-formed XML, or unstructured
and malformed HTML from the web. The library also provides useful functions to
extract information from an HTML document, making it ideal for screen-scraping.

Users should start from the "Text.HTML.TagSoup" module.


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


%build
%ghc_lib_build


%install
%ghc_lib_install


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE
%{_docdir}/%{name}-%{version}/LICENSE

%files devel -f %{name}-devel.files
%doc README.md


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.13.3-4
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.13.3-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 22 2015 Jens Petersen <petersen@redhat.com> - 0.13.3-1
- update to 0.13.3

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 Jens Petersen <petersen@redhat.com> - 0.13.1-1
- update to 0.13.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Jens Petersen <petersen@redhat.com> - 0.12.8-3
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Jens Petersen <petersen@redhat.com> - 0.12.8-1
- update to 0.12.8

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 0.12.6-3
- rebuild

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 0.12.6-2
- add license to ghc_files

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.12.6-1
- update to 0.12.6 and cabal2spec-0.25.2

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12.2-2.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.12.2-2.1
- rebuild with new gmp

* Sat Jul 09 2011 Ben Boeckel <mathstuf@gmail.com> - 0.12.2-2
- Update to cabal2spec-0.24

* Wed Jun 22 2011 Jens Petersen <petersen@redhat.com> - 0.12.2-1
- update to 0.12.2
- update deps
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.12-4
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.12-2
- Update to cabal2spec-0.22.4
- Rebuild

* Fri Dec 17 2010 Ben Boeckel <mathstuf@gmail.com> - 0.12-1
- Update to 0.12

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 0.11.1-4
- rebuild for network-2.3

* Sun Nov 28 2010 Ben Boeckel <mathstuf@gmail.com> - 0.11.1-3
- Rebuild for GHC7

* Sun Nov 07 2010 Ben Boeckel <mathstuf@gmail.com> - 0.11.1-2
- Rebuild

* Fri Oct 08 2010 Ben Boeckel <mathstuf@gmail.com> - 0.11.1-1
- Update to 0.11.1

* Tue Sep 21 2010 Ben Boeckel <mathstuf@gmail.com> - 0.11-2
- Ship the tagsoup.htm file

* Sun Sep 12 2010 Ben Boeckel <mathstuf@gmail.com> - 0.11-1
- Update to 0.11

* Sat Sep 04 2010 Ben Boeckel <mathstuf@gmail.com> - 0.10.1-1
- Initial package

* Sat Sep  4 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.10.1-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
