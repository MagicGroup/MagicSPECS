Name: 		perl-Pod-Tests
Version: 	1.19
Release: 	15%{?dist}
Summary: 	Extract embedded tests and code examples from POD
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Pod-Tests/
Source0: 	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Pod-Tests-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: 	noarch

BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Harness) >= 1.22
BuildRequires:  perl(Test::More) >= 0.33

# for improved tests
BuildRequires:  perl(Test::CPAN::Meta) >= 0.12
BuildRequires:	perl(Test::Pod) >= 1.26
BuildRequires:  perl(Test::MinimumVersion) >= 0.008
# N/A in Fedora
# BuildRequires:  perl(Pod::Simple) >= 3.07
BuildRequires:  perl(Pod::Simple)

%description
Pod::Tests extracts embedded tests and code examples from POD.
pod2test convert embedded tests and code examples to .t files. 

%prep
%setup -q -n Pod-Tests-%{version}

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
# remove test until Perl-MinimumVersion will be fixed
rm -rf t/99_pmv.t
 AUTOMATED_TESTING=1

%files
%defattr(-,root,root,-)
%doc Changes LICENSE
%{_bindir}/*
%{perl_vendorlib}/Pod
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.19-15
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.19-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.19-13
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.19-12
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 1.19-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.19-8
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.19-6
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.19-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.19-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 10 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.19-1
- Upstream update.

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.18-6
- rebuild for new perl

* Tue Sep 04 2007 Ralf Corsépius <rc040203@freenet.de> - 0.18-5
- Update license tag.
- BR: perl(ExtUtils::MakeMaker).

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.18-4
- Mass rebuild.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 0.18-3
- Rebuild for perl-5.8.8.

* Sun Oct 02 2005 Ralf Corsepius <rc040203@freenet.de> - 0.18-2
- Pollute the spec file with dos2unix to accommodate PR 169112.

* Fri Sep 23 2005 Ralf Corsepius <rc040203@freenet.de> - 0.18-1
- FE submission.
