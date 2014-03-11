Name: 		perl-Class-Inspector
Version: 	1.27
Release: 	5%{?dist}
Summary: 	Get information about a class and its structure
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Class-Inspector/
Source0: 	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Class-Inspector-%{version}.tar.gz

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: noarch

BuildRequires:	perl(Test::More)

%if !%{defined perl_bootstrap}
BuildRequires: perl(Test::Pod) >= 1.00
BuildRequires: perl(Test::CPAN::Meta) >= 0.12
BuildRequires: perl(Perl::MinimumVersion) >= 1.20
BuildRequires: perl(Test::MinimumVersion) >= 0.008
%endif

%description
Class::Inspector allows you to get information about a loaded class.
Most or all of this information can be found in other ways, but they aren't
always very friendly, and usually involve a relatively high level of Perl
wizardry, or strange and unusual looking code. Class::Inspector attempts to
provide an easier, more friendly interface to this information.

%prep
%setup -q -n Class-Inspector-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
%if !%{defined perl_bootstrap}
 AUTOMATED_TESTING=1
%endif

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/Class
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.27-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.27-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1.27-2
- Perl 5.16 rebuild

* Fri Jan 27 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.27-1
- Upstream update.
- Spec file modernization.
- Fix perl_bootstrap handling.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 27 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.25-2
- rebuild with Perl 5.14.1

* Thu Feb 17 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.25-1
- Upstream update.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.24-7
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jun 23 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.24-6
- Re-enable pmv-test.

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.24-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.24-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.24-2
- BR: perl(Test::MinimumVersion) >= 0.008

* Mon May 11 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.24-1
- Upstream update.
- Remove Class-Inspector-1.23.diff.

* Fri Feb 27 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.23-3
- Unconditionally BR: perl(Test::CPAN::Meta).
- Adjust minimum perl version in META.yml (Add Class-Inspector-1.23.diff).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jun 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.23-1
- Upstream update.

* Tue Mar 11 2008 Ralf Corsépius <rc040203@freenet.de> - 1.22-1
- Upstream update.

* Thu Feb 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.20-3
- Rebuild normally, second pass

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.20-2
- Rebuild for perl 5.10 (again), first pass

* Thu Feb 14 2008 Ralf Corsépius <rc040203@freenet.de> - 1.20-1
- Upstream update.

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.18-3
- rebuild normally, second pass

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.18-2.1
- rebuild for new perl, first pass, disable TMV, tests

* Sun Nov 25 2007 Ralf Corsépius <rc040203@freenet.de> - 1.18-2
- Add BR: perl(Test::MinimumVersion).

* Tue Nov 20 2007 Ralf Corsépius <rc040203@freenet.de> - 1.18-1
- Upstream update.

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 1.17-1
- Upstream update.

* Thu Apr 19 2007 Ralf Corsépius <rc040203@freenet.de> - 1.16-3
- Reflect perl package split.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.16-2
- Mass rebuild.

* Mon May 21 2006 Ralf Corsépius <rc040203@freenet.de> - 1.16-1
- Upstream update.

* Mon May 08 2006 Ralf Corsépius <rc040203@freenet.de> - 1.15-1
- Upstream update.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 1.13-2
- Rebuild for perl-5.8.8.

* Thu Sep 29 2005 Ralf Corsepius <rc040203@freenet.de> - 1.13-1
- Upstream update.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de>
- Fix another typo in %%summary.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 1.12-2
- Fix typo in %%summary.
- Spec file cleanup.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 1.12-1
- FE submission.
