Name: 		perl-ExtUtils-AutoInstall
Version: 	0.63
Release: 	28%{?dist}
Summary: 	Automatic install of dependencies via CPAN
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/ExtUtils-AutoInstall/
Source: 	http://search.cpan.org/CPAN/authors/id/A/AU/AUTRIJUS/ExtUtils-AutoInstall-%{version}.tar.gz
Patch0:		eai.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: 	noarch

BuildRequires:  perl(CPANPLUS) >= 0.043
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Sort::Versions) >= 1.2
BuildRequires:	perl(LWP::Simple)
BuildRequires:	perl(CPAN)

%description
ExtUtils::AutoInstall lets module writers specify a more sophisticated
form of dependency information than the PREREQ_PM option offered by 
ExtUtils::MakeMaker.

%prep
%setup -q -n ExtUtils-AutoInstall-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor --defaultdeps
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
# For license text(s), see the perl package
%doc Changes AUTHORS README TODO
%{perl_vendorlib}/ExtUtils
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.63-28
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.63-27
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.63-26
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.63-25
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.63-24
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.63-23
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.63-22
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.63-21
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.63-20
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 0.63-18
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.63-16
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.63-14
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.63-13
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.63-12
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.63-11
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.63-8
- do not expand the glob if there are no disabled tests (#11960)
- enable CPANPLUS BR by default

* Fri Feb 08 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.63-7
- rebuild for new perl

* Wed Sep 05 2007 Ralf Corsépius <rc040203@freenet.de> - 0.63-6
- Update license tag.
- BR: perl(ExtUtils::MakeMaker).
- BR: perl(CPAN).

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.63-5
- Mass rebuild.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 0.63-4
- Rebuild for perl-5.8.8.

* Tue Sep 14 2005 Ralf Corsepius <rc040203@freenet.de> - 0.63-3
- Further spec file cleanup.

* Tue Sep 14 2005 Ralf Corsepius <rc040203@freenet.de> - 0.63-2
- Spec file cleanup.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 0.63-1
- FE submission.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 0.63-0
- Update to 0.63.
- FE submission preps.
