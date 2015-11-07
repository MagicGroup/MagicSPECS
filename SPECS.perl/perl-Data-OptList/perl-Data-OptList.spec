Name:           perl-Data-OptList
Summary:        Parse and validate simple name/value option pairs
Version:	0.109
Release:	2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Data-OptList/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Data-OptList-%{version}.tar.gz 
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Params::Util)
BuildRequires:  perl(Sub::Install) >= 0.921
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Obsolete/provide old -tests subpackage (can be removed in F19 development cycle)
Obsoletes:      %{name}-tests < %{version}-%{release}
Provides:       %{name}-tests = %{version}-%{release}

%description
Hashes are great for storing named data, but if you want more than one entry
for a name, you have to use a list of pairs. Even then, this is really boring
to write:

$values = [
    foo => undef,
    bar => undef,
    baz => undef,
    xyz => { ... },
];

With Data::OptList, you can do this instead:

$values = Data::OptList::mkopt([
    qw(foo bar baz),
    xyz => { ... },
]);

This works by assuming that any defined scalar is a name and any reference
following a name is its value.

%prep
%setup -q -n Data-OptList-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \; 2>/dev/null
%{_fixperms} %{buildroot}

%check
 RELEASE_TESTING=1

%files
%doc Changes LICENSE README t/
%{perl_vendorlib}/Data/
%{_mandir}/man3/Data::OptList.3pm*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.109-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.109-1
- 更新到 0.109

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.107-10
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.107-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.107-8
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.107-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.107-6
- Perl 5.16 rebuild

* Sat Jan 21 2012 Paul Howarth <paul@city-fan.org> - 0.107-5
- obsolete/provide old -tests subpackage to support upgrades

* Fri Jan 20 2012 Paul Howarth <paul@city-fan.org> - 0.107-4
- drop -tests subpackage (general lack of interest in this), but include
  them as documentation for the main package
- drop redundant %%{?perl_default_filter}
- don't use macros for commands
- can't find any dependency cycle so drop %%{?perl_bootstrap} usage
- drop ExtUtils::MakeMaker version requirement to 6.30, actual working minimum

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 0.107-3
- package LICENSE file
- run test suite even when bootstrapping, as it should still pass
- run release tests too
- enhance %%description so it makes sense
- BR: perl(Test::More)

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.107-2
- Perl mass rebuild
- add perl_bootstrap macro

* Wed May 11 2011 Iain Arnell <iarnell@gmail.com> 0.107-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.106-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.106-3
- rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.106-2
- Mass rebuild with perl-5.12.0

* Mon Mar 08 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.106-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (0.106)
- added a new br on perl(ExtUtils::MakeMaker) (version 6.42)
- added a new br on perl(List::Util) (version 0)
- altered br on perl(Sub::Install) (0.92 => 0.921)
- added a new req on perl(List::Util) (version 0)
- added a new req on perl(Params::Util) (version 0.14)
- added a new req on perl(Sub::Install) (version 0.921)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.104-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.104-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.104-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.104-1
- update to 0.104

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.103-2
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.103-1
- rebuild for new perl
- bump to 0.103
- fix license tag

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.101-2
- bump

* Sat Sep 02 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.101-1
- Specfile autogenerated by cpanspec 1.69.1.
