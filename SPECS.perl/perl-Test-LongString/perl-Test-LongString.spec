Name:		perl-Test-LongString
Version:	0.17
Release:	1%{?dist}
Summary:	Perl module to test long strings
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Test-LongString/
Source0:	http://search.cpan.org/CPAN/authors/id/R/RG/RGARCIA/Test-LongString-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

BuildRequires:	perl(ExtUtils::MakeMaker)
# Required by the tests
BuildRequires:	perl(Test::Builder) >= 0.12
BuildRequires:	perl(Test::Builder::Tester) >= 1.04

BuildRequires:	perl(Test::Pod::Coverage) >= 1.04
BuildRequires:	perl(Test::Pod) >= 1.14 

Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module provides some drop-in replacements for the string comparison
functions of Test::More, but which are more suitable when you test against
long strings. If you've ever had to search for text in a multi-line string
like an HTML document, or find specific items in binary data, this is the
module for you.

%prep
%setup -q -n Test-LongString-%{version}

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


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/Test
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.17-1
- 更新到 0.17

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.15-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.15-6
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.15-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.15-2
- Perl mass rebuild

* Fri Feb 18 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.15-1
- Upstream update.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 03 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.14-1
- Upstream update.
- Minor spec cleanups.

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-2
- Mass rebuild with perl-5.12.0

* Mon Mar 01 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.13-1
- Upstream update.
- Minor spec cleanups.

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.11-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.11-3
- rebuild for new perl

* Thu Sep 06 2007 Ralf Corsépius <rc040203@freenet.de> - 0.11-2
- BR: perl(ExtUtils::MakeMaker).
- Update license tag.

* Wed Feb 21 2007 Ralf Corsépius <rc040203@freenet.de> - 0.11-1
- Upstream update.
- For now, ignore BR: perl(Test::Builder::Tester) > 1.04.

* Wed Feb 21 2007 Ralf Corsépius <rc040203@freenet.de>
- Preps for 0.11. Deactivated, because perl(Test::Builder::Tester) on
  all current Fedoras is too old for this to be applicable.

* Fri Nov 03 2006 Ralf Corsépius <rc040203@freenet.de> - 0.10-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.09-3
- Mass rebuild.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 0.09-2
- Rebuild for perl-5.8.8.

* Fri Oct 07 2005 Ralf Corsepius <rc040203@freenet.de> - 0.09-1
- Upstream update.

* Fri Aug 19 2005 Ralf Corsepius <ralf@links2linux.de> - 0.08-2
- Spec cleanup.

* Thu Aug 11 2005 Ralf Corsepius <ralf@links2linux.de> - 0.08-1
- FE submission.
