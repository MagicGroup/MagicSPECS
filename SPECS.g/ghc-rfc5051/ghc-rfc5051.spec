# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name rfc5051

Name:           ghc-%{pkg_name}
Version:        0.1.0.3
Release:        7%{?dist}
Summary:        Simple unicode collation as per RFC5051

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
# End cabal-rpm deps
BuildRequires:  unicode-ucd

%description
This library implements 'i;unicode-casemap', the simple, non locale-sensitive
unicode collation algorithm described in RFC 5051
(<http://www.rfc-editor.org/rfc/rfc5051.txt>). Proper unicode collation can be
done using text-icu, but that is a big dependency that depends on a large C
library, and rfc5051 might be better for some purposes.


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
rm UnicodeData.txt
ln -s %{_datadir}/unicode/ucd/UnicodeData.txt


%build
ghc --make MkUnicodeData.hs
./MkUnicodeData > Data/RFC5051/UnicodeData.hs
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


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.1.0.3-7
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.1.0.3-6
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Jens Petersen <petersen@redhat.com> - 0.1.0.3-4
- update urls

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 27 2014 Jens Petersen <petersen@redhat.com> - 0.1.0.3-1
- rebuild UnicodeData.hs with unicode-ucd

* Mon Jan 27 2014 Fedora Haskell SIG <haskell@lists.fedoraproject.org> - 0.1.0.3
- spec file generated by cabal-rpm-0.8.8
