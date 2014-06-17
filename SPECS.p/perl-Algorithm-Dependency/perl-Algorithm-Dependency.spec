Name: 		perl-Algorithm-Dependency
Version: 	1.110
Release: 	17%{?dist}
Summary: 	Algorithmic framework for implementing dependency trees
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Algorithm-Dependency/
Source0:	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Algorithm-Dependency-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: noarch

BuildRequires: perl(File::Spec)		>= 0.82
BuildRequires: perl(Test::ClassAPI)	>= 0.6
BuildRequires: perl(Test::More)		>= 0.47
BuildRequires: perl(Params::Util)	>= 0.06

BuildRequires: perl(Test::Pod)		>= 1.00
BuildRequires: perl(Test::CPAN::Meta)	>= 0.12
BuildRequires: perl(Perl::MinimumVersion) >= 1.20
BuildRequires: perl(Test::MinimumVersion) >= 0.008

%description
Algorithm::Dependency is a framework for creating simple read-only
dependency hierarchies, where you have a set of items that rely on other
items in the set, and require actions on them as well.

%prep
%setup -q -n Algorithm-Dependency-%{version}

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
 AUTOMATED_TESTING=1

%files
%defattr(-,root,root,-)
%doc Changes LICENSE
%{perl_vendorlib}/Algorithm
%{_mandir}/man3/*

%changelog
* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.110-17
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.110-16
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.110-15
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.110-14
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.110-13
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 1.110-12
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 1.110-11
- 为 Magic 3.0 重建

* Fri Jan 27 2012 Liu Di <liudidi@gmail.com> - 1.110-10
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.110-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.110-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.110-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.110-6
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 25 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.110-5
- Reactivate pmv test.

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.110-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.110-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.110-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.110-1
- Upstream update.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.108-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.108-1
- Upstream update.
- BR: perl(Test::CPAN::Meta).

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.106-2
- rebuild for new perl

* Mon Jan 21 2008 Ralf Corsépius <rc040203@freenet.de> - 1.106-1
- Upstream update.

* Sun Nov 25 2007 Ralf Corsépius <rc040203@freenet.de> - 1.104-2
- Add BR: perl(Test-MinimumVersion).

* Tue Nov 20 2007 Ralf Corsépius <rc040203@freenet.de> - 1.104-1
- Upstream update.

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 1.103-2
- Update license tag.

* Sun Jul 29 2007 Ralf Corsépius <rc040203@freenet.de> - 1.103-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.102-2
- Mass rebuild.

* Mon Apr 24 2006 Ralf Corsépius <rc040203@freenet.de> - 1.102-1
- Upstream update.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 1.101-2
- Rebuild for perl-5.8.8.

* Wed Oct 12 2005 Ralf Corsepius <rc040203@freenet.de> - 1.101-1
- Upstream update.

* Sat Sep 17 2005 Ralf Corsepius <rc040203@freenet.de> - 1.04-3
- Spec cleanup.

* Thu Sep 15 2005 Paul Howarth <paul@city-fan.org> - 1.04-2
- Fix Source0 URL
- Fix perl(Params::Util) BuildReq version
- Add BR: perl(Test::Pod) for improved test coverage

* Thu Sep 15 2005 Ralf Corsepius <rc040203@freenet.de> - 1.04-1
- Upstream update.
- Drop shipping README.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 1.03-1
- Spec file cleanup.
- FE submission.
