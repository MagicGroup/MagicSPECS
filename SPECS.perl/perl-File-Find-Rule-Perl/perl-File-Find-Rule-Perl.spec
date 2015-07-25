Name:		perl-File-Find-Rule-Perl
Version:	1.12
Release:	8%{?dist}
Summary:	Common rules for searching for Perl things
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/File-Find-Rule-Perl/
Source0:	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/File-Find-Rule-Perl-%{version}.tar.gz

Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:	noarch

BuildRequires:	perl(File::Find::Rule) >= 0.20
BuildRequires:	perl(File::Spec) >= 0.82
BuildRequires:	perl(Test::More) >= 0.47
BuildRequires:  perl(Params::Util) >= 0.38
BuildRequires:  perl(Parse::CPAN::Meta) >= 0.04

# For improved tests
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Perl::MinimumVersion) >= 1.27
BuildRequires:  perl(Test::MinimumVersion) >= 0.101080
BuildRequires:  perl(Test::Pod) >= 1.44
BuildRequires:  perl(Test::CPAN::Meta) >= 0.17
%endif

%description
Common rules for searching for Perl things.

%prep
%setup -q -T -c
%setup -q -T -D -a0

%build
cd File-Find-Rule-Perl-%{version}
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
cd ..

%install
cd File-Find-Rule-Perl-%{version}
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
cd ..
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
%if !%{defined perl_bootstrap}
cd File-Find-Rule-Perl-%{version}
 AUTOMATED_TESTING=1
cd ..
%endif

%files
%defattr(-,root,root,-)
%doc File-Find-Rule-Perl-%{version}/Changes File-Find-Rule-Perl-%{version}/LICENSE
%{perl_vendorlib}/File
%{_mandir}/man3/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.12-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.12-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.12-6
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.12-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.12-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.12-1
- Upstream update.
- Update BRs.
- Spec file cleanup.

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.10-3
- rebuild with Perl 5.14.1
- add perl_bootstrap macro for test BR

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 03 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.10-1
- Upstream update.

* Sun May 09 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.09-5
- Re-enable pmv-test.

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.09-4
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.09-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.09-2
- rebuild against perl 5.10.1

* Fri Aug 07 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.09-1
- Upstream update.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.08-1
- Upstream update.

* Wed Jun 17 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.06-1
- Upstream update.
- Build in subdir to work-around rpm disturbing testsuite.
- Rework BRs.

* Fri Feb 27 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.04-4
- Adjust minimum perl version in META.yml (Add File-Find-Rule-Perl-1.04.diff).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jun 24 2008 Ralf Corsépius <rc040203@freenet.de> - 1.04-2
- Unconditionally BR: perl(Test::CPAN::Meta).

* Tue Jun 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.04-1
- Upstream update.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.03-3
- Rebuild for perl 5.10 (again)

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.03-2
- rebuild for new perl

* Mon Nov 19 2007 Ralf Corsépius <rc040203@freenet.de> - 0.03-1
- Initial version.
