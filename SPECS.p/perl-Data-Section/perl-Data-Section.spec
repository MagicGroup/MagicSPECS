Name:           perl-Data-Section
Version:        0.200006
Release:        3%{?dist}
Summary:        Read multiple hunks of data out of your DATA section
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Data-Section/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/Data-Section-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(Encode)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(lib)
BuildRequires:  perl(MRO::Compat) >= 0.09
BuildRequires:  perl(Sub::Exporter) >= 0.979
BuildRequires:  perl(Test::FailWarnings)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(utf8)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Data::Section provides an easy way to access multiple named chunks of
line-oriented data in your module's DATA section. It was written to allow
modules to store their own templates, but probably has other uses.

%prep
%setup -q -n Data-Section-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT

%check
make test
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Data/
%{_mandir}/man3/Data::Section.3pm*

%changelog
* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.200006-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.200006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 10 2014 Paul Howarth <paul@city-fan.org> - 0.200006-1
- Update to 0.200006
  - Skip tests on Win32 pre-5.14 related to line endings; perl munges the data
    before we're able to get at it

* Wed Dec 11 2013 Paul Howarth <paul@city-fan.org> - 0.200005-1
- Update to 0.200005
  - Open DATA handles both :raw and :bytes to avoid content munging on Win32
  - This is not yet a perfect solution for Win32

* Mon Dec  2 2013 Paul Howarth <paul@city-fan.org> - 0.200004-1
- Update to 0.200004
  - Avoid confusion between \n, \x0d\x0a, and Win32

* Mon Nov  4 2013 Paul Howarth <paul@city-fan.org> - 0.200003-1
- Update to 0.200003
  [THIS MIGHT BREAK STUFF]
  - Add an "encoding" parameter to set encoding of data section contents; this
    defaults to UTF-8
- Drop support for old distributions as we now need Test::FailWarnings, which
  isn't available there

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.101622-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.101622-2
- Perl 5.18 rebuild

* Thu Jun 20 2013 Paul Howarth <paul@city-fan.org> - 0.101622-1
- Update to 0.101622
  - Add a link to an Advent article about Data-Section
  - Update bugtracker, repo, etc.
- Run the release tests separately
- BR: perl(base), perl(File::Find), perl(File::Temp) and perl(lib) for the test
  suite
- Drop BR: perl(Pod::Coverage::TrustPod) and perl(Test::Pod::Coverage) as
  upstream has dropped their Pod coverage test
- Update patch for building with old Test::More versions

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.101621-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.101621-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.101621-3
- Perl 5.16 rebuild

* Wed Mar  7 2012 Paul Howarth <paul@city-fan.org> - 0.101621-2
- Add test suite patch to support building with Test::More < 0.88 so that we
  can build for EPEL-5, only applying the patch when necessary
- BR: at least version 0.09 of perl(MRO::Compat)
- BR: perl(Pod::Coverage::TrustPod), perl(Test::Pod) and
  perl(Test::Pod::Coverage) for full test coverage
- Run the release tests too
- Drop redundant explicit versioned dependency on perl(Sub::Exporter)
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit

* Mon Jan 30 2012 Daniel P. Berrange <berrange@redhat.com> - 0.101621-1
- Update to 0.101621 release (rhbz #785362)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.101620-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.101620-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.101620-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.101620-3
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jun 30 2010 Mark Chappell <tremble@fedoraproject.org> - 0.101620-2
- Add in missing BuildRequires MRO::Compat

* Wed Jun 30 2010 Mark Chappell <tremble@fedoraproject.org> - 0.101620-1
- Update for release 0.101620

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.093410-3
- Mass rebuild with perl-5.12.0

* Tue Jan 12 2010 Daniel P. Berrange <berrange@redhat.com> - 0.093410-2
- Fix source URL

* Thu Jan  7 2010 Daniel P. Berrange <berrange@redhat.com> - 0.093410-1
- Update to 0.093410 release

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.091820-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.091820-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Daniel P. Berrange <berrange@redhat.com> - 0.091820-1
- Update to 0.091820 release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep 06 2008 Daniel P. Berrange <berrange@redhat.com> 0.005-2
- Add Test::More BR

* Fri Sep 05 2008 Daniel P. Berrange <berrange@redhat.com> 0.005-1
- Specfile autogenerated by cpanspec 1.77.
