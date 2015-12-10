# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name libxml-sax

Name:           ghc-%{pkg_name}
Version:        0.7.5
Release:        8%{?dist}
Summary:        Haskell bindings for the libxml2 SAX interface

License:        MIT
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-xml-types-devel
#BuildRequires:  libxml2-devel%{?_isa}
BuildRequires:  pkgconfig(libxml-2.0)
# End cabal-rpm deps

%description
Bindings for the libXML2 SAX interface.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Begin cabal-rpm deps:
#Requires:       libxml2-devel%{?_isa}
Requires:       pkgconfig(libxml-2.0)
# End cabal-rpm deps

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
%doc license.txt
%{_docdir}/%{name}-%{version}/license.txt

%files devel -f %{name}-devel.files


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.7.5-8
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.7.5-7
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Jens Petersen <petersen@fedoraproject.org> - 0.7.5-5
- cblrpm refresh

* Fri Aug 22 2014 Dan Callaghan <dcallagh@redhat.com> - 0.7.5-4
- rebuilt for updated ghc-text

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 19 2014 Dan Callaghan <dcallagh@redhat.com> - 0.7.5-1
- upstream release 0.7.5 (no effective changes, just relaxing of version 
  requirements)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Dan Callaghan <dcallagh@redhat.com> - 0.7.4-2
- update for new guidelines (cabal-rpm 0.8.2)

* Mon May 13 2013 Dan Callaghan <dcallagh@redhat.com> - 0.7.4-1
- initial version
