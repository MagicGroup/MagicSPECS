Name:           perl-MooseX-GlobRef
Version:        0.0701
Release:        6%{?dist}
Summary:        Store a Moose object in glob reference
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/MooseX-GlobRef/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DE/DEXTER/MooseX-GlobRef-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Moose) >= 0.94
BuildRequires:  perl(parent)
BuildRequires:  perl(Test::Assert)
BuildRequires:  perl(Test::Unit::Lite) >= 0.12
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Obsoletes:      perl-MooseX-GlobRef-Object <= 0.0701-2.fc15

%description
This meta-policy allows to store Moose object in glob reference or file
handle. The class attributes will be stored in anonymous hash associated
with glob reference. It allows to create a Moose version of IO::Handle.

%prep
%setup -q -n MooseX-GlobRef-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0701-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 0.0701-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0701-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.0701-3
- Perl mass rebuild

* Mon Mar 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.0701-2
- remove obsoletes -> causing coflicts

* Mon Mar  7 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.0701-1
- rename package to correct name

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0701-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 09 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.0701-1
- Upstream update (Fix FTBFS: BZ 660747).
- Remove requires-filter, adjust BRs.

* Thu May 18 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.07-5
- Fix build directory.
- Reflect build directory having changed.

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.07-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.07-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- auto-update to 0.07 (by cpan-spec-update 0.01)
- altered br on perl(Test::Unit::Lite) (0.11 => 0.12)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Allisson Azevedo <allisson@gmail.com> 0.06-1
- Update to 0.06.
- Added filter requires.

* Thu Jan 29 2009 Allisson Azevedo <allisson@gmail.com> 0.04-1
- Initial rpm release.
