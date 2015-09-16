Name:		perl-Test-Synopsis
Version:	0.11
Release:	1%{?dist}
Summary:	Test your SYNOPSIS code
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Test-Synopsis/
Source0:        http://search.cpan.org/CPAN/authors/id/Z/ZO/ZOFFIX/Test-Synopsis-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(base)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(ExtUtils::Manifest)
BuildRequires:	perl(Test::Builder::Module)
BuildRequires:	perl(Test::Pod) >= 1.00
# Test::Perl::Critic -> Perl::Critic -> List::MoreUtils -> Test::LeakTrace -> Test::Synopsis
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Test::Perl::Critic)
%endif
# RHEL-7 package cannot have buildreqs from EPEL-7 (aspell-en), so skip the
# spell check there; we won't need Test::Spelling either in that case
%if 0%{?rhel} < 7
BuildRequires:	aspell-en
BuildRequires:	perl(Test::Spelling)
%endif
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Test::Builder::Module)

%description
Test::Synopsis is an (author) test module to find .pm or .pod files under your
lib directory and then make sure the example snippet code in your SYNOPSIS
section passes the perl compile check.

Note that this module only checks the perl syntax (by wrapping the code with
sub) and doesn't actually run the code.

%prep
%setup -q -n Test-Synopsis-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check

 TEST_FILES="xt/*.t"

%clean
rm -rf %{buildroot}

%files
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Synopsis.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.11-1
- 更新到 0.11

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-16
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.06-15
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.06-13
- Perl 5.16 re-rebuild of bootstrapped packages

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.06-12
- Perl 5.16 rebuild

* Thu Jun  7 2012 Paul Howarth <paul@city-fan.org> - 0.06-11
- Separate bootstrap and RHEL conditionals
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from buildroot
- BR: perl(base)

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-10
- Conditionalize aspell-en & friends

* Wed Jan 25 2012 Paul Howarth <paul@city-fan.org> - 0.06-9
- Can run spelling test unconditionally now
- BR: perl(ExtUtils::Manifest)
- Don't BR: perl(Test::Perl::Critic) if we're bootstrapping
- Use %%{_fixperms} macro rather than our own chmod incantation
- Run developer tests in a separate test run
- Drop redundant %%{?perl_default_filter}
- Don't use macros for commands

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.06-7
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue Jun 15 2010 Paul Howarth <paul@city-fan.org> - 0.06-4
- Whittle down for Fedora submission

* Mon May 17 2010 Paul Howarth <paul@city-fan.org> - 0.06-3
- Fix dist tag for RHEL-6 Beta

* Tue Feb  2 2010 Paul Howarth <paul@city-fan.org> - 0.06-2
- Add buildreq perl(Test::Perl::Critic) if we have Perl 5.8.8 or later

* Fri Nov 27 2009 Paul Howarth <paul@city-fan.org> - 0.06-1
- Initial RPM version
