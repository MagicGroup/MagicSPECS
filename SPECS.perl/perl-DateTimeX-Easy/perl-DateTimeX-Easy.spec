Name:       perl-DateTimeX-Easy
Version:    0.089
Release:    16%{?dist}
# see lib/DateTimeX/Easy.pm
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Parse a date/time string using the best method available
Source:     http://search.cpan.org/CPAN/authors/id/R/RO/ROKR/DateTimeX-Easy-%{version}.tar.gz
Url:        http://search.cpan.org/dist/DateTimeX-Easy
BuildArch:  noarch

BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.31
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(base)
BuildRequires:  perl(Date::Parse)
BuildRequires:  perl(DateTime)
BuildRequires:  perl(DateTime::Format::Flexible)
BuildRequires:  perl(DateTime::Format::Natural)
BuildRequires:  perl(DateTime::TimeZone)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Time::Zone)
# Optional run-time
# perl(DateTime::Format::DateManip) has been made optional due to instability
BuildRequires:  perl(DateTime::Format::ICal)
# Test only
BuildRequires:  perl(Test::Most)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Do not export dependency on private module
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(DateTimeX::Easy::DateParse\\)

%description
DateTimeX::Easy makes DateTime object creation quick and easy. It uses a
variety of DateTime::Format packages to do the bulk of the parsing, with
some custom tweaks to smooth out the rough edges (mainly concerning
timezone detection and selection).

%prep
%setup -q -n DateTimeX-Easy-%{version}
# Remove bundled modules
rm -rf inc

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.089-16
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.089-15
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.089-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.089-13
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.089-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.089-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.089-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.089-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.089-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.089-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.089-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.089-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.089-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.089-3
- 为 Magic 3.0 重建

* Wed Jan 25 2012 Petr Pisar <ppisar@redhat.com> - 0.089-2
- Do not export dependency on private module DateTimeX::Easy::DateParse

* Tue Jan 24 2012 Petr Pisar <ppisar@redhat.com> - 0.089-1
- 0.089 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.088-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.088-6
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.088-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.088-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.088-3
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Dec 08 2010 Ralf Corsépius <corsepiu@fedoraproject.org> 0.088-2
- Add missing changelog entry for 0.088-1.

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.088-1
- Update to 0.88.

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.087-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.087-4
- rebuild against perl 5.10.1

* Tue Aug 04 2009 Ralf Corsépius <corsepiu@fedoraproject.org> 0.087-3
- Fix mass rebuild breakdown: Add --skipdeps.
- Use Test::Most.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.087-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.087-1
- auto-update to 0.087 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.085-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.085-1
- update to 0.085
- touch up for review

* Sun Dec 07 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.084-0.1
- update to 0.084

* Sat Oct 11 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.082-1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.1)
