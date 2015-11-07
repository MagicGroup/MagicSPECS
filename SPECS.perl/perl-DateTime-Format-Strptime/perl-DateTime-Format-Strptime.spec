# RPM and CPAN versioning don't match
%global cpanversion 1.56

Name:           perl-DateTime-Format-Strptime
Version:	1.5600
Release:	7%{?dist}
Summary:        Parse and format strptime and strftime patterns
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/DateTime-Format-Strptime/
Source0:        http://www.cpan.org/authors/id/D/DR/DROLSKY/DateTime-Format-Strptime-%{cpanversion}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(DateTime) >= 1.00
BuildRequires:  perl(DateTime::Locale) >= 0.45
BuildRequires:  perl(DateTime::TimeZone) >= 0.79
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Params::Validate) >= 0.64
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
# Pod::Coverage::TrustPod not used
# Pod::Wordlist not used
BuildRequires:  perl(Test::More) >= 0.88
# Test::NoTabs not used
# Test::Pod 1.41 not used
# Test::Pod::Coverage 1.08 not used
# Test::Spelling 0.12 not used
BuildRequires:  perl(utf8)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module implements most of strptime(3), the POSIX function that is the
reverse of strftime(3), for DateTime. While strftime takes a DateTime and a
pattern and returns a string, strptime takes a string and a pattern and
returns the DateTime object associated.

%prep
%setup -q -n DateTime-Format-Strptime-%{cpanversion}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc Changes LICENSE README.md
%{perl_vendorlib}/DateTime/
%{_mandir}/man3/DateTime::Format::Strptime.3pm*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.5600-7
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 1.5600-6
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5600-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.5600-3
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.5600-2
- Perl 5.20 rebuild

* Tue Aug 12 2014 Petr Pisar <ppisar@redhat.com> - 1.5600-1
- 1.56 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5500-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May  4 2014 Paul Howarth <paul@city-fan.org> - 1.5500-1
- Update to 1.55 (rpm version 1.5500 to maintain upgrade path)
  - If diagnostic is true for an object, it will now use Test::More::diag()
    under the test harness rather than printing to STDOUT
  - The %%z specifier will now parse UTC offsets with a colon like "+01:00"
    (CPAN RT#91458)
  - Made the regexes to parse day and months abbreviations and names a little
    more specificl as it stood, they tended to eat up more non-word characters
    than they should, so a pattern like '%%a%%m%%d_%%Y' broke on a date like
    'Fri0215_2013' - the day name would be parsed as 'Fri02' and the month
    would not be parsed at all (CPAN RT#93863, CPAN RT#93865)
- Specify all dependencies
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5400-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 1.5400-2
- Perl 5.18 rebuild

* Wed Apr  3 2013 Paul Howarth <paul@city-fan.org> - 1.5400-1
- Update to 1.54 (rpm version 1.5400 to maintain upgrade path)
  - Packaging cleanup, including listing Test::More as a test prereq, not a
    runtime prereq (CPAN RT#76128)
  - Shut up "unescaped braces in regex" warning from 5.17.0 (CPAN RT#77514)
  - A fix in DateTime.pm 1.00 broke a test in this distro (CPAN RT#84371)
  - Require DateTime.pm 1.00 because without it tests will break
- Specify all dependencies
- This release by DROLSKY -> update source URL
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Don't use macros for commands
- Make %%files list more explicit

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5000-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5000-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.5000-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5000-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.5000-4
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.5000-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Steven Pritchard <steve@kspei.com> 1.5000-1
- Update to 1.5000.

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2000-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue Jun 15 2010 Petr Sabata <psabata@redhat.com> - 1.2000-1
- Update to the latest upstream release

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.1000-2
- Mass rebuild with perl-5.12.0

* Tue Feb 16 2010 Paul Howarth <paul@city-fan.org> 1.1000-1
- Fix FTBFS (#564718) by bumping buildreq version of perl(DateTime) from 0.4304
  to 0.44 (RPM considers 0.4304 > 0.44, unlike perl) and bumping version to
  1.1000 for compatibility with DateTime::Locale 0.43 (upstream ticket 19)
- Update buildreq version requirement for perl(DateTime::Locale) to 0.43
- Drop test patch, no longer needed
- Run additional tests for full locale coverage

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> 1.0800-4
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.0800-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.0800-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Steven Pritchard <steve@kspei.com> 1.0800-1
- Update to 1.0800.
- Update versions on build dependencies.

* Tue Jul 08 2008 Steven Pritchard <steve@kspei.com> 1.0702-3
- Patch t/004_locale_defaults.t to work around change in DateTime::Locale.

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0702-2
- Rebuild for new perl

* Thu Jan 03 2008 Steven Pritchard <steve@kspei.com> 1.0702-1
- Update to 1.0702.
- Drop charset patch.
- Update License tag.
- BR Test::More.

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 1.0700-3
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 1.0700-2
- Fix find option order.

* Mon Jul 03 2006 Steven Pritchard <steve@kspei.com> 1.0700-1
- Specfile autogenerated by cpanspec 1.66.
- Fix License.
- Remove versioned DateTime deps (0.1402 > 0.30 according to rpm).
- Remove versioned explicit dependencies that rpmbuild picks up.
- Substitute literal "©" for E<169> in pod documentation.  (The result
  should be the same, but apparently the man page conversion is generating
  something that rpmlint doesn't like.)
