Name:       perl-Best 
Version:    0.14
Release:    3%{?dist}
License:    MIT 
Group:      Development/Libraries
Summary:    Fallbackable module loader 
Source:     http://search.cpan.org/CPAN/authors/id/G/GA/GAAL/Best-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/Best
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch
BuildRequires: perl(constant)
BuildRequires: perl(Carp)
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::Exception)
BuildRequires: perl(Test::More)
# optional
BuildRequires: perl(Test::Pod)
BuildRequires: perl(Test::Pod::Coverage)

%description
Often there are several possible providers of some functionality your
program needs, but you don't know which is available at the run site.
For example, one of the modules may be implemented with XS, or not in
the core Perl distribution and thus not necessarily installed.*Best*
attempts to load modules from a list, stopping at the first successful
load and failing only if no alternative was found.

%prep
%setup -q -n Best-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes README LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.14-3
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.14-2
- 为 Magic 3.0 重建

* Mon Jan 23 2012 Petr Šabata <contyk@redhat.com> - 0.14-1
- 0.14 bump
- Spec cleanup, license clarified, deps corrected

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.12-5
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.12-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.12-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 09 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.12-1
- submission

* Tue Mar 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.12-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)

