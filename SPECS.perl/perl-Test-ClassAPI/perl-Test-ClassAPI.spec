Name: 		perl-Test-ClassAPI
Version: 	1.06
Release: 	16%{?dist}
Summary: 	Provides basic first-pass API testing for large class trees
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Test-ClassAPI/
Source0: 	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Test-ClassAPI-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: 	noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Config::Tiny) >= 2.00
BuildRequires:  perl(Class::Inspector) >= 1.12
BuildRequires:  perl(File::Spec) >= 0.83

# Explictly required by lib/Test/ClassAPI.pm
BuildRequires:  perl(Params::Util) >= 1.00

%if !%{defined perl_bootstrap}
# For improved tests
BuildRequires:  perl(Test::Pod)

# For improved tests
BuildRequires: perl(Test::CPAN::Meta) >= 0.12
BuildRequires: perl(Pod::Simple) >= 3.07
BuildRequires: perl(Test::MinimumVersion) >= 0.008
%endif

%description
Provides basic first-pass API testing for large class trees.

For many APIs with large numbers of classes, it can be very useful to be 
able to do a quick once-over to make sure that classes, methods, and 
inheritance is correct, before doing more comprehensive testing.
This module aims to provide such a capability.

%prep
%setup -q -n Test-ClassAPI-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%clean
rm -rf $RPM_BUILD_ROOT

%check
%if !%{defined perl_bootstrap}
# remove until fix of Perl::MinimalVersion and version.pm
rm -rf t/99_pmv.t
 AUTOMATED_TESTING=1
%endif

%files
%defattr(-,root,root,-)
%doc Changes LICENSE
%{perl_vendorlib}/Test
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.06-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.06-15
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.06-14
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.06-12
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.06-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.06-9
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.06-8
- Perl mass rebuild

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.06-7
- rebuild with Perl 5.14.1
- use perl_bootstrap macro

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.06-5
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.06-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.06-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.06-1
- Upstream update.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 16 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.05-3
- Reflect perl(Test::CPAN::Meta) >= 0.12 finally being available in Fedora.

* Tue Aug 26 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.05-2
- Bump release.

* Tue Aug 26 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.05-1
- Upstream update.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-4
- Rebuild for perl 5.10 (again)

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-3
- rebuild for new perl

* Thu Sep 06 2007 Ralf Corsépius <rc040203@freenet.de> - 1.04-2
- Update license tag.

* Mon Mar 12 2007 Ralf Corsépius <rc040203@freenet.de> - 1.04-1
- Upstream update.
- BR: perl(ExtUtils::MakeMaker).

* Fri Feb 16 2007 Ralf Corsépius <rc040203@freenet.de> - 1.03-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.02-4
- Mass rebuild.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 1.02-3
- Rebuild for perl-5.8.8.

* Tue Sep 14 2005 Ralf Corsepius <rc040203@freenet.de> - 1.02-2
- New %%summary.
- Extend %%description.
- Don't put README into %%doc (Redundant to man page).

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 1.02-1
- Spec file cleanup.
- FE submission.

* Wed Jun 22 2005 Ralf Corsepius <ralf@links2linux.de> - 1.02-0.pm.0
- Initial packman version.
