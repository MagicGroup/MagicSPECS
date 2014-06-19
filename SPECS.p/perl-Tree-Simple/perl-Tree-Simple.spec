Name: 		perl-Tree-Simple
Version: 	1.23
Release: 	2%{?dist}
Summary: 	Tree::Simple Perl module
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Tree-Simple/
Source0: 	http://www.cpan.org/authors/id/R/RS/RSAVAGE/Tree-Simple-%{version}.tgz
BuildArch: 	noarch

BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Scalar::Util) >= 1.18
BuildRequires:  perl(Test::Exception) >= 0.15 
BuildRequires:  perl(Test::More) >= 0.47
BuildRequires:  perl(Test::Memory::Cycle)
BuildRequires:  perl(Test::Version) >= 1.002003

Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
A simple tree object.

%prep
%setup -q -n Tree-Simple-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Tree
%{_mandir}/man3/*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Nov 20 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.23-1
- Upstream update.
- BR: perl(Test::Version).

* Mon Sep 30 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.22-1
- Upstream update.

* Tue Sep 24 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.19-1
- Upstream update.
- Reflect upstream Source0-URL: having changed.
- Reflect upstream not being interested in Pod checks.
- Modernize spec.
- Fix bogus %%changelog date.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 1.18-14
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 1.18-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 22 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.18-9
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.18-7
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.18-6
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.18-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.18-2
- rebuild for new perl

* Mon Nov 19 2007 Ralf Corsépius <rc040203@freenet.de> - 1.18-1
- Upstream bugfix.

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 1.17-2
- Update license tag.

* Fri Nov 03 2006 Ralf Corsépius <rc040203@freenet.de> - 1.17-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.16-2
- Mass rebuild.

* Tue Apr 04 2006 Ralf Corsépius <rc040203@freenet.de> - 1.16-1
- Upsteam update.
- BR: Scalar::Util >= 1.18.

* Tue Feb 28 2006 Ralf Corsépius <rc040203@freenet.de> - 1.15-3
- Rebuild for perl-5.8.8.

* Sat Aug 20 2005 Ralf Corsepius <ralf@links2linux.de> - 1.15-2
- Spec cleanup.

* Thu Aug 11 2005 Ralf Corsepius <ralf@links2linux.de> - 1.15-1
- Upstream update.

* Thu Aug 11 2005 Ralf Corsepius <ralf@links2linux.de> - 1.14-1
- FE submission.
