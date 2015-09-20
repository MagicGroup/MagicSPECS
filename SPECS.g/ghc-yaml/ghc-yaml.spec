# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name yaml

%bcond_with tests

Name:           ghc-%{pkg_name}
Version:        0.8.10
Release:        3%{?dist}
Summary:        Support for parsing and rendering YAML documents

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  chrpath
BuildRequires:  ghc-aeson-devel
BuildRequires:  ghc-attoparsec-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-conduit-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-resourcet-devel
BuildRequires:  ghc-scientific-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-transformers-devel
BuildRequires:  ghc-unordered-containers-devel
BuildRequires:  ghc-vector-devel
BuildRequires:  pkgconfig(yaml-0.1)
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-aeson-qq-devel
BuildRequires:  ghc-hspec-devel
%endif
# End cabal-rpm deps

%description
Provides support for parsing and emitting Yaml documents.

The package is broken down into two modules. "Data.Yaml" provides a high-level
interface based around the JSON datatypes provided by the 'aeson' package.
"Text.Libyaml" provides a lower-level, streaming interface. For most users,
"Data.Yaml" is recommended.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Begin cabal-rpm deps:
Requires:       pkgconfig(yaml-0.1)
# End cabal-rpm deps

%description devel
This package provides the Haskell %{pkg_name} library development files.


%prep
%setup -q -n %{pkg_name}-%{version}

cabal-tweak-flag system-libyaml True
# remove the bundled lib
rm -r libyaml


%build
%ghc_lib_build


%install
%ghc_lib_install

%ghc_fix_dynamic_rpath json2yaml yaml2json


%check
%if %{with tests}
%cabal test
%endif


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE


%files devel -f %{name}-devel.files
%doc README.md
%{_bindir}/json2yaml
%{_bindir}/yaml2json


%changelog
* Mon Aug 31 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.10-3
- Rebuild (aarch64 vector hashes)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar  4 2015 Jens Petersen <petersen@fedoraproject.org> - 0.8.10-1
- update to 0.8.10

* Wed Jan 28 2015 Jens Petersen <petersen@redhat.com> - 0.8.8.2-5
- cblrpm refresh

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Adam Williamson <awilliam@redhat.com> - 0.8.8.2-2
- rebuild for new ghc-scientific

* Fri May 02 2014 Jens Petersen <petersen@redhat.com> - 0.8.8.2-1
- update to 0.8.8.2
- no longer exclude arm

* Wed Jan 22 2014 Jens Petersen <petersen@redhat.com> - 0.8.5.3-1
- update to 0.8.5.3

* Thu Dec 5 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.8.5.2-1
- Latest upstream version.

* Tue Nov 19 2013 Jens Petersen <petersen@redhat.com> - 0.8.5-3
- run chrpath on yaml2json (#1008787)

* Wed Oct 16 2013 Jens Petersen <petersen@redhat.com> - 0.8.5-2
- add static provides and pkgconfig requires to devel

* Tue Sep 17 2013 Jens Petersen <petersen@redhat.com> - 0.8.5-1
- build with system libyaml
- package yaml2json in devel subpackage
- exclude armv7hl because of conduit

* Tue Sep 17 2013 Fedora Haskell SIG <haskell@lists.fedoraproject.org> - 0.8.5-0
- spec file generated by cabal-rpm-0.8.3