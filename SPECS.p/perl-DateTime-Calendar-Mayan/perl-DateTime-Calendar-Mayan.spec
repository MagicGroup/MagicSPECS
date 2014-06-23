Name:		perl-DateTime-Calendar-Mayan 
Version:	0.0601 
Release:	20%{?dist}
License:	GPL+ or Artistic 
Group:		Development/Libraries
Summary:	Mayan Long Count Calendar 
Url:		http://search.cpan.org/dist/DateTime-Calendar-Mayan
Source:		http://search.cpan.org/CPAN/authors/id/J/JH/JHOBLITT/DateTime-Calendar-Mayan-%{version}.tar.gz 
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu) 
BuildArch:	noarch
BuildRequires:	perl(DateTime) >= 0.15
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Module::Build::Compat)
BuildRequires:	perl(Params::Validate) >= 0.64
BuildRequires:	perl(Test::More)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
An implementation of the Mayan Long Count, Haab, and Tzolkin calendars
as defined in "Calendrical Calculations The Millennium Edition".
Supplemented by "Frequently Asked Questions about Calendars".

%prep
%setup -q -n DateTime-Calendar-Mayan-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc README Changes LICENSE Todo
%{perl_vendorlib}/DateTime/
%{_mandir}/man3/DateTime::Calendar::Mayan.3pm*

%changelog
* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.0601-20
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.0601-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.0601-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.0601-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.0601-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.0601-15
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.0601-14
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.0601-13
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0601-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.0601-11
- Perl 5.16 rebuild

* Mon Jan 23 2012 Paul Howarth <paul@city-fan.org> - 0.0601-10
- Spec clean-up:
  - Drop redundant buildreq perl(Class::ISA)
  - Make %%files list more explicit
  - Don't use macros for commands
  - Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0601-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.0601-8
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.0601-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0601-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.0601-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.0601-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.0601-3
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0601-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.0601-1
- Submission

* Mon May 18 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.0601-0
- Initial RPM packaging
- Generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
