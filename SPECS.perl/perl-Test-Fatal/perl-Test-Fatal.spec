Summary:	Incredibly simple helpers for testing code with exceptions 
Name:		perl-Test-Fatal
Version:	0.014
Release:	3%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Test-Fatal/
Source0:	http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Test-Fatal-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Test::Builder::Tester)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Try::Tiny) >= 0.07
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Test::Builder)

%description
Test::Fatal is an alternative to the popular Test::Exception. It does much
less, but should allow greater flexibility in testing exception-throwing code
with about the same amount of typing.

%prep
%setup -q -n Test-Fatal-%{version}

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
 RELEASE_TESTING=1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Fatal.3pm*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.014-3
- 为 Magic 3.0 重建

* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 0.014-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.014-1
- 更新到 0.014

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.010-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.010-5
- 为 Magic 3.0 重建

* Thu Oct 18 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.010-4
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.010-2
- Perl 5.16 rebuild

* Thu Feb 16 2012 Paul Howarth <paul@city-fan.org> 0.010-1
- Update to 0.010
  - Avoid tickling an overloading bug in perl 5.6 during testing
    (CPAN RT#74847)

* Fri Feb 10 2012 Paul Howarth <paul@city-fan.org> 0.009-1
- Update to 0.009
  - Advise against using isnt(exception{...},undef)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov  7 2011 Paul Howarth <paul@city-fan.org> 0.008-1
- Update to 0.008
  - Revert the mistake by which 0.004 allowed blocks after "exception" as well
    as "success"
- BR: perl(Carp)
- Update patch for building with ExtUtils::MakeMaker < 6.30

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> 0.006-2
- Perl mass rebuild

* Thu Jun  2 2011 Paul Howarth <paul@city-fan.org> 0.006-1
- Update to 0.006
  - Crank back the Test::More and Exporter requirements (CPAN RT#62699)
  - Add lives_ok and dies_ok emulation (CPAN RT#67598)
- Versions patch replaced by workaround for old ExtUtils::MakeMaker
- BR: perl(Test::Builder::Tester)

* Tue Apr 26 2011 Paul Howarth <paul@city-fan.org> 0.005-1
- Update to 0.005
  - Fix the logic that picks tests for 5.13.1+

* Tue Apr 26 2011 Paul Howarth <paul@city-fan.org> 0.004-1
- Update to 0.004
  - success blocks now allow trailing blocks like finally, catch, etc.
- Remove remaining uses of macros for commands
- Re-order %%install section to conventional position in spec

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 29 2010 Paul Howarth <paul@city-fan.org> 0.003-1
- Update to 0.003
  - More tests for false exceptions, especially on 5.13
- Update versions patch

* Thu Oct 28 2010 Paul Howarth <paul@city-fan.org> 0.002-1
- Update to 0.002
  - Add tests for handling of false exceptions
  - Fix precedence error in documentation
- Update versions patch

* Wed Oct 27 2010 Paul Howarth <paul@city-fan.org> 0.001-2
- Sanitize spec for Fedora submission

* Tue Oct 26 2010 Paul Howarth <paul@city-fan.org> 0.001-1
- Initial RPM version
