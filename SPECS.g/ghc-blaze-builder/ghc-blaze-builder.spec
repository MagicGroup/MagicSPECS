# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name blaze-builder

# no useful debuginfo for Haskell packages without C sources
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
Version:        0.3.3.4
Release:        2%{?dist}
Summary:        Efficient buffered output

License:        BSD
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-text-devel
# End cabal-rpm deps

%description
This library provides an abstraction of buffered output of byte streams and
several convenience functions to exploit it. For example, it allows to
efficiently serialize Haskell values to lazy bytestrings with a large average
chunk size. The large average chunk size allows to make good use of cache
prefetching in later processing steps (e.g. compression) and reduces the system
call overhead when writing the resulting lazy bytestring to a file or sending
it over the network.


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


%files devel -f %{name}-devel.files
%doc CHANGES README.markdown TODO


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 15 2015 Jens Petersen <petersen@redhat.com> - 0.3.3.4-1
- update to 0.3.3.4
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Jens Petersen <petersen@redhat.com> - 0.3.1.1-1
- update to 0.3.1.1
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.3.1.0-6
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.3.1.0-4
- change prof BRs to devel

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 0.3.1.0-3
- rebuild

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.3.1.0-2
- rebuild

* Tue Feb 28 2012 Ben Boeckel <mathstuf@gmail.com> - 0.3.1.0-1
- Update to 0.3.1.0

* Thu Jan  5 2012 Jens Petersen <petersen@redhat.com> - 0.3.0.2-1
- update to 0.3.0.2 and cabal2spec-0.25.2

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.3.0.1-2.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.3.0.1-2.1
- rebuild with new gmp

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 0.3.0.1-2
- ghc_arches replaces ghc_excluded_archs

* Mon Jun 20 2011 Jens Petersen <petersen@redhat.com> - 0.3.0.1-1
- update to 0.3.0.1
- update to cabal2spec-0.23

* Thu Mar 24 2011 Ben Boeckel <mathstuf@gmail.com> - 0.3.0.0-1
- Update to 0.3.0.0

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.2.1.4-4
- Enable build on sparcv9

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 0.2.1.4-3
- rebuild for latest text-0.11.0.5

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.2.1.4-1
- Update to 0.2.1.4

* Fri Dec 10 2010 Ben Boeckel <mathstuf@gmail.com> - 0.2.0.3-1
- Update to 0.2.0.3

* Wed Dec 01 2010 Ben Boeckel <mathstuf@gmail.com> - 0.2.0.2-1
- Update to 0.2.0.2

* Fri Nov 12 2010 Ben Boeckel <mathstuf@gmail.com> - 0.2.0.1-1
- Update to 0.2.0.1

* Sat Sep 04 2010 Ben Boeckel <mathstuf@gmail.com> - 0.1-1
- Initial package

* Sat Sep  4 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.1-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2