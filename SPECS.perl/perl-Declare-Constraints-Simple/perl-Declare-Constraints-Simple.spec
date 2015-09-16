Name:		perl-Declare-Constraints-Simple
Version:	0.03
Release:	21%{?dist}
Summary:	Declarative Validation of Data Structures
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Declare-Constraints-Simple/
Source0:	http://search.cpan.org/CPAN/authors/id/P/PH/PHAYLON/Declare-Constraints-Simple-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	perl(ExtUtils::MakeMaker) 
# Module
BuildRequires:	perl(aliased)
BuildRequires:	perl(Carp::Clan)
BuildRequires:	perl(Class::Inspector)
BuildRequires:	perl(Scalar::Util)
# Test suite
BuildRequires:	perl(Test::More) 
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Filter unwanted Requires: (rpm 4.9 onwards)
%global __requires_exclude ^perl\\(Declare::Constraints::Simple-Library\\)

%description
The main purpose of this module is to provide an easy way to build a
profile to validate a data structure. It does this by giving you a set of
declarative keywords in the importing namespace.

%prep
%setup -q -n Declare-Constraints-Simple-%{version}

# Filter unwanted Requires (prior to rpm 4.9)
%global reqfilt /bin/sh -c "%{__perl_requires} | grep -Fvx 'perl(Declare::Constraints::Simple-Library)'"
%define __perl_requires %{reqfilt}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \; 2>/dev/null
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README t/
%{perl_vendorlib}/Declare/
%{_mandir}/man3/Declare::Constraints::Simple.3pm*
%{_mandir}/man3/Declare::Constraints::Simple::Library.3pm*
%{_mandir}/man3/Declare::Constraints::Simple::Library::Array.3pm*
%{_mandir}/man3/Declare::Constraints::Simple::Library::Base.3pm*
%{_mandir}/man3/Declare::Constraints::Simple::Library::Exportable.3pm*
%{_mandir}/man3/Declare::Constraints::Simple::Library::General.3pm*
%{_mandir}/man3/Declare::Constraints::Simple::Library::Hash.3pm*
%{_mandir}/man3/Declare::Constraints::Simple::Library::Numerical.3pm*
%{_mandir}/man3/Declare::Constraints::Simple::Library::OO.3pm*
%{_mandir}/man3/Declare::Constraints::Simple::Library::Operators.3pm*
%{_mandir}/man3/Declare::Constraints::Simple::Library::Referencial.3pm*
%{_mandir}/man3/Declare::Constraints::Simple::Library::Scalar.3pm*
%{_mandir}/man3/Declare::Constraints::Simple::Result.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.03-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.03-20
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.03-19
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.03-18
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.03-16
- Perl 5.16 rebuild

* Mon Jan 23 2012 Paul Howarth <paul@city-fan.org> - 0.03-15
- Spec clean-up
  - Make %%files list more explicit
  - Classify buildreqs by build/module/test
  - Use search.cpan.org source URL
  - Don't use macros for commands
  - Use tabs

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 0.03-14
- Spec clean-up
  - Simplify pre-rpm-4.9 provides filter
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Make %%files list more specific

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.03-13
- Perl mass rebuild

* Sun Feb 13 2011 Paul Howarth <paul@city-fan.org> - 0.03-12
- Fix dependency filter for rpm 4.9 onwards

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-10
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-9
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-8
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.03-6
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.03-3
- Rebuild for new perl

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.03-2
- Bump

* Tue May 01 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.03-1
- Specfile autogenerated by cpanspec 1.71
