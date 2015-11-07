Name:       perl-MooseX-Types-DateTime
Version:	0.13
Release:	2%{?dist}
# see, e.g., lib/MooseX/Types/DateTime.pm
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    DateTime related constraints and coercions for Moose
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/MooseX-Types-DateTime-%{version}.tar.gz
Url:        http://search.cpan.org/dist/MooseX-Types-DateTime
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(DateTime)
BuildRequires: perl(DateTime::Duration)
BuildRequires: perl(DateTime::Locale)
BuildRequires: perl(DateTime::TimeZone) >= 0.95
BuildRequires: perl(Moose) >= 0.41
BuildRequires: perl(MooseX::Types) >= 0.30
BuildRequires: perl(MooseX::Types::Moose) >= 0.30
BuildRequires: perl(namespace::clean) >= 0.08
BuildRequires: perl(Test::More)
BuildRequires: perl(Test::Exception) >= 0.27
BuildRequires: perl(Test::use::ok) >= 0.02

# Clamp version to decimal 2 digits
Requires:   perl(DateTime) >= 0.43
Requires:   perl(DateTime::Duration) >= 0.43
Requires:   perl(DateTime::Locale) >= 0.40

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.07-3
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

# Remove over-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(DateTime[:)].*\\.[0-9]{3,}$

%description
This module packages several type constraints (Moose::Util::TypeConstraints)
and coercions designed to work with the DateTime suite of objects.


%prep
%setup -q -n MooseX-Types-DateTime-%{version}

find . -type f -exec chmod -c -x {} +

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.13-2
- 更新到 0.13

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.11-1
- 更新到 0.11

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.07-6
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.07-4
- Perl 5.16 rebuild

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.07-3
- drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Petr Pisar <ppisar@redhat.com> - 0.07-2
- Adjust Perl versions to RPM versions

* Thu Jan 12 2012 Iain Arnell <iarnell@gmail.com> 0.07-1
- update to latest upstream version
- remove unnecessary explicit requires

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.05-8
- Perl mass rebuild

* Sun Jun 26 2011 Iain Arnell <iarnell@gmail.com> 0.05-7
- remove unnecessary explicit requires
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-5
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-4
- Mass rebuild with perl-5.12.0

* Sat Feb 13 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.05-3
- PERL_INSTALL_ROOT => DESTDIR
- add perl_default_filter, _default_subpackage_tests
- drop version req on DateTime (buildfailures with latest perl-DateTime)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.05-2
- rebuild against perl 5.10.1

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- auto-update to 0.05 (by cpan-spec-update 0.01)
- altered br on perl(MooseX::Types) (0.04 => 0.19)
- altered req on perl(MooseX::Types) (0.04 => 0.19)
- added a new req on perl(Test::Exception) (version 0.27)
- added a new req on perl(Test::use::ok) (version 0.02)

* Mon Aug 24 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- auto-update to 0.04 (by cpan-spec-update 0.01)
- altered br on perl(DateTime::Locale) (0 => 0.4001)
- altered br on perl(DateTime::TimeZone) (0.7701 => 0.95)
- added a new req on perl(DateTime) (version 0.4302)
- added a new req on perl(DateTime::Format::DateParse) (version 0.04)
- added a new req on perl(DateTime::Format::Flexible) (version 0.05)
- added a new req on perl(DateTime::Format::Natural) (version 0.71)
- added a new req on perl(DateTime::Locale) (version 0.4001)
- added a new req on perl(DateTime::TimeZone) (version 0.95)
- added a new req on perl(DateTimeX::Easy) (version 0.082)
- added a new req on perl(Moose) (version 0.41)
- added a new req on perl(MooseX::Types) (version 0.04)
- added a new req on perl(Time::Duration::Parse) (version 0.06)
- added a new req on perl(namespace::clean) (version 0.08)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03-3
- add DateTime::Format::DateManip as a br

* Sat Dec 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.03-2
- touchup for submission

* Sat Oct 11 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.03-1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.1)
