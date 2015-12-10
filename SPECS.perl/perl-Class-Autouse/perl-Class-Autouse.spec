Name:		perl-Class-Autouse
Version:	2.01
Release:	10%{?dist}
Summary:	Run-time class loading on first method call
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Class-Autouse/
Source0:	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Class-Autouse-%{version}.tar.gz

# Upstream does its very best to prevent us from running them.
%bcond_with	xt_tests

Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:	noarch

BuildRequires:	perl(Carp)
BuildRequires:	perl(File::Spec) >= 0.80
BuildRequires:	perl(File::Temp) >= 0.17
BuildRequires:	perl(prefork)
BuildRequires:	perl(List::Util) >= 1.18
BuildRequires:	perl(Test::More) >= 0.47

# for xt tests
%if %{with xt_tests}
BuildRequires:	perl(Perl::MinimumVersion) >= 1.27
BuildRequires:	perl(Pod::Simple) >= 3.14
BuildRequires:	perl(Test::Pod) >= 1.44
BuildRequires:	perl(Test::MinimumVersion) >= 0.101080
BuildRequires:	perl(Test::CPAN::Meta) >= 0.17
%endif

%description
Class::Autouse allows you to specify a class the will only load when a
method of that class is called. For large classes that might not be used
during the running of a program, such as Date::Manip, this can save you
large amounts of memory, and decrease the script load time.

%prep
%setup -q -n Class-Autouse-%{version}

%build
AUTOMATED_TESTING=1 %{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check

%if %{with xt_tests}
# Manually invoke xt-tests
AUTOMATED_TESTING=1 PERL_DL_NONLAZY=1 /usr/bin/perl "-MExtUtils::Command::MM" "-e" "test_harness(0, 'inc', 'blib/lib', 'blib/arch')" xt/*.t
%endif

%files
%defattr(-,root,root,-)
%doc Changes LICENSE
%{perl_vendorlib}/Class
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.01-10
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.01-9
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.01-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.01-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.01-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.01-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.01-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 2.01-2
- Perl 5.16 rebuild

* Sun Feb 05 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.01-1
- Upstream update.
- Adjust BR:'s.
- Modernize spec.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.00-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.00-1
- Upstream update.
- Adjust BR:'s.
- Add %%bcond_with xt_tests.

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.29-10
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Jul 20 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.29-9
- Reenable pmv test.

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.29-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.29-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.29-5
- Adjust minimum perl version in META.yml (Add Class-Autouse-1.29.diff).
- BR: perl(List::Util) >= 1.19.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.29-3
- rebuild for new perl

* Sun Nov 25 2007 Ralf Corsépius <rc040203@freenet.de> - 1.29-2
- Add BR: perl(Test-MinimumVersion).

* Tue Nov 20 2007 Ralf Corsépius <rc040203@freenet.de> - 1.29-1
- Upstream update.

* Wed Sep 05 2007 Ralf Corsépius <rc040203@freenet.de> - 1.28-1
- Upstream update.
- Update license.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.27-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.26-2
- Mass rebuild.

* Thu Apr 20 2006 Ralf Corsépius <rc040203@freenet.de> - 1.26-1
- Upstream update.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 1.21-3
- Rebuild for perl-5.8.8.

* Wed Feb 01 2006 Ralf Corsepius <rc040203@freenet.de> - 1.21-2
- Revert to 1.21 (List::Util in Perl is too old).

* Sat Jan 14 2006 Ralf Corsepius <rc040203@freenet.de> - 1.24-1
- Upstream update.

* Wed Sep 28 2005 Ralf Corsepius <rc040203@freenet.de> - 1.21-1
- Upstream update.
- Fix bogus dep on perl(Carp).

* Thu Sep 15 2005 Ralf Corsepius <rc040203@freenet.de> - 1.20-2
- Spec cleanup.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 1.20-1
- Spec cleanup.
- FE submission.
