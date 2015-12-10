# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name highlighting-kate

%bcond_without tests

Name:           ghc-%{pkg_name}
Version:        0.5.11.1
Release:        3%{?dist}
Summary:        Sourcecode syntax highlighting

License:        GPLv2+
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  chrpath
BuildRequires:  ghc-blaze-html-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-parsec-devel
BuildRequires:  ghc-pcre-light-devel
BuildRequires:  ghc-utf8-string-devel
%if %{with tests}
BuildRequires:  ghc-Diff-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-process-devel
%endif
# End cabal-rpm deps

%description
Highlighting-kate is a syntax highlighting library with support for nearly 100
languages. The syntax parsers are automatically generated from Kate syntax
descriptions (<http://kate-editor.org/>), so any syntax supported by Kate can be
added.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# from F21 devel cycle
Obsoletes:      %{pkg_name} < %{version}-%{release}
Provides:       %{pkg_name} = %{version}-%{release}

%description devel
This package provides the Haskell %{pkg_name} library development
files.

It includes a command-line utility.


%prep
%setup -q -n %{pkg_name}-%{version}

cabal-tweak-flag executable True
cabal-tweak-flag pcre-light True


%build
%ghc_lib_build


%install
%ghc_lib_install

%ghc_fix_dynamic_rpath Highlight


%check
LANG=en_US.utf8
%cabal_test


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE
%{_docdir}/%{name}-%{version}/LICENSE

%files devel -f %{name}-devel.files
%doc README.md
%attr(755,root,root) %{_bindir}/Highlight


%changelog
* Fri Dec 04 2015 Liu Di <liudidi@gmail.com> - 0.5.11.1-3
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.5.11.1-2
- 为 Magic 3.0 重建

* Mon Jan 19 2015 Jens Petersen <petersen@redhat.com> - 0.5.11.1-1
- update to 0.5.11.1

* Thu Aug 28 2014 Jens Petersen <petersen@redhat.com> - 0.5.8.5-1
- update to 0.5.8.5

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb  3 2014 Jens Petersen <petersen@redhat.com> - 0.5.6-2
- bump

* Fri Jan 10 2014 Jens Petersen <petersen@redhat.com> - 0.5.6-1
- update to 0.5.6
- really fix the Highlight rpath (#1009842)

* Wed Oct 16 2013 Jens Petersen <petersen@redhat.com> - 0.5.5-2
- add static provides to devel

* Thu Sep 19 2013 Fedora Haskell SIG <haskell@lists.fedoraproject.org> - 0.5.5-1
- source package renamed from highlighting-kate
- update to 0.5.5
- spec file generated by cabal-rpm-0.8.3
- fix rpath for Highlight

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Jens Petersen <petersen@redhat.com> - 0.5.3.9-1
- update to 0.5.3.9
- update to new simplified Haskell Packaging Guidelines

* Sun Mar 10 2013 Jens Petersen <petersen@redhat.com> - 0.5.3.8-1
- update to 0.5.3.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 31 2012 Jens Petersen <petersen@redhat.com> - 0.5.3.3-1
- update to 0.5.3.3
- turn on .cabal executable flag with patch

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.5.1-2
- change prof BRs to devel

* Sun Jun 10 2012 Jens Petersen <petersen@redhat.com> - 0.5.1-1
- update to 0.5.1

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 0.5.0.5-2
- add license to ghc_files

* Mon Mar  5 2012 Jens Petersen <petersen@redhat.com> - 0.5.0.5-1
- update to 0.5.0.5

* Mon Feb 13 2012 Jens Petersen <petersen@redhat.com> - 0.5.0.3-1
- update to 0.5.0.3
- patch to use pcre-light and fix version
- new depends on blaze-html

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 0.2.10-3
- Rebuild against PCRE 8.30

* Thu Jan  5 2012 Jens Petersen <petersen@redhat.com> - 0.2.10-2
- update to cabal2spec-0.25.2

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.2.10-1.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.2.10-1.1
- rebuild with new gmp

* Fri Jul 22 2011 Jens Petersen <petersen@redhat.com> - 0.2.10-1
- update to 0.2.10

* Tue Jul 12 2011 Jens Petersen <petersen@redhat.com> - 0.2.9-2
- update to cabal2spec-0.23.2

* Thu Jun  2 2011 Jens Petersen <petersen@redhat.com> - 0.2.9-1
- GPLv2+
- add all dependencies

* Thu Jun  2 2011 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.2.9-0
- initial packaging for Fedora automatically generated by cabal2spec-0.23
