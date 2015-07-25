Name:           perl-DateTime-Set
Version:        0.3400
Release:        2%{?dist}
Summary:        Datetime sets and set math
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/DateTime-Set/
Source0:        http://www.cpan.org/authors/id/F/FG/FGLOCK/DateTime-Set-%{version}.tar.gz
Patch0:         DateTime-Set-0.32-version.patch
BuildArch:      noarch
# Build
BuildRequires:  perl(Module::Build)
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(DateTime::Duration)
BuildRequires:  perl(DateTime::Infinite)
BuildRequires:  perl(Params::Validate)
BuildRequires:  perl(Set::Infinite) >= 0.59
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Test Suite
BuildRequires:  perl(DateTime) >= 0.12
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
# Optional Tests
# DateTime::Event::Recurrence requires DateTime::Set itself
%if 0%{!?perl_bootstrap:1}
BuildRequires:  perl(DateTime::Event::Recurrence)
%endif
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
DateTime::Set is a module for datetime sets. It can be used to handle two
different types of sets. The first is a fixed set of predefined datetime
objects. For example, if we wanted to create a set of datetimes containing
the birthdays of people in our family. The second type of set that it can
handle is one based on the idea of a recurrence, such as "every Wednesday",
or "noon on the 15th day of every month". This type of set can have fixed
starting and ending datetimes, but neither is required. So our "every
Wednesday set" could be "every Wednesday from the beginning of time until
the end of time", or "every Wednesday after 2003-03-05 until the end of
time", or "every Wednesday between 2003-03-05 and 2004-01-07".

%prep
%setup -q -n DateTime-Set-%{version}

# Make perl/rpm version comparisons work the same way
%patch0

%build
perl Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT

%check
./Build test

%files
%doc Changes LICENSE README TODO
%{perl_vendorlib}/DateTime/
%{perl_vendorlib}/Set/
%{_mandir}/man3/DateTime::Set.3pm*
%{_mandir}/man3/DateTime::Span.3pm*
%{_mandir}/man3/DateTime::SpanSet.3pm*
%{_mandir}/man3/Set::Infinite::_recurrence.3pm*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3400-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 12 2014 Paul Howarth <paul@city-fan.org> - 0.3400-1
- Update to 0.3400
  - Documentation and packaging fixes
  - Version number using 4 digits

* Thu Jan 23 2014 Paul Howarth <paul@city-fan.org> - 0.33-3
- Bootstrap of epel7 done

* Thu Jan 23 2014 Paul Howarth <paul@city-fan.org> - 0.33-2
- Bootstrap epel7 build

* Tue Oct 15 2013 Paul Howarth <paul@city-fan.org> - 0.33-1
- Update to 0.33
  - Bugfix in SpanSet->grep

* Thu Oct  3 2013 Paul Howarth <paul@city-fan.org> - 0.32-1
- Update to 0.32
  - New method is_empty_set (CPAN RT#50750)
  - New test t/21from_recurrence.t
  - Ignore duration signal in DateTime::Span->from_datetime_and_duration() and
    use the 'end'/'start' parameters as a cue for the time direction
  - More tests of intersections with open/closed ended spans
- Tweak the Set::Infinite version requirement to avoid the need for rpm
  dependency filters
- Specify all dependencies
- BR: perl(DateTime::Event::Recurrence) for the test suite except when
  bootstrapping
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit
- Don't need to remove empty directories from the buildroot
- Don't use macros for commands

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 0.28-13
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.28-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> 0.28-8
- update filtering macros for rpm 4.9

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.28-7
- Perl mass rebuild

* Sat Feb 19 2011 Iain Arnell <iarnell@gmail.com> 0.28-6
- remove perl(DateTime::Event::Recurrence) buildreq to avoid circular
  dependency

* Tue Feb 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.28-5
- remove useless filter & add new because of RPM4.9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.28-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.28-2
- Mass rebuild with perl-5.12.0

* Sat Feb 13 2010 Steven Pritchard <steve@kspei.com> 0.28-1
- Update to 0.28.
- BR DateTime::Event::Recurrence for better test coverage.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.26-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Steven Pritchard <steve@kspei.com> 0.26-1
- Update to 0.26.

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.25-6
- rebuild for new perl

* Sun Dec 30 2007 Ralf Corsépius <rc040203@freenet.de> - 0.25-5
- Adjust License-tag.
- BR: perl(Test::More) (BZ 419631).

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 0.25-4
- Use fixperms macro instead of our own chmod incantation.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.25-3
- Fix find option order.

* Fri Jul 07 2006 Steven Pritchard <steve@kspei.com> 0.25-2
- Drop explicit versioned dependency on Set::Infinite.

* Wed Jul 05 2006 Steven Pritchard <steve@kspei.com> 0.25-1
- Specfile autogenerated by cpanspec 1.66.
- Fix License.
- Exclude Set::Infinite auto-requires due to version comparison issue
  (0.5502 > 0.59 to rpm).
- Drop explicit DateTime dependency.  (rpmbuild figures it out.)
- Add a bit to the description.
