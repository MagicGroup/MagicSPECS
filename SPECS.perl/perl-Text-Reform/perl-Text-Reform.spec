Name:           perl-Text-Reform
Version:        1.20
Release:        18%{?dist}
Summary:        Manual text wrapping and reformatting
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Text-Reform/
Source0:        http://www.cpan.org/authors/id/C/CH/CHORNY/Text-Reform-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.14 
BuildRequires:  perl(version)

Requires:       perl(TeX::Hyphen)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The module supplies a re-entrant, highly configurable replacement for the
built-in Perl format() mechanism.

%prep
%setup -q -n Text-Reform-%{version}
chmod 644 Changes README lib/Text/*.pm

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT

./Build install destdir=$RPM_BUILD_ROOT create_packlist=0

find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
# the testsuite fails for locales with decimal point != ".", i.e. it
# fails for almost all European languages except en
LC_NUMERIC=C ./Build test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README demo/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.20-18
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.20-17
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.20-16
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.20-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.20-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.20-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.20-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.20-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.20-10
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.20-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.20-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.20-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Steven Pritchard <steve@kspei.com> 1.20-1
- Update to 1.20.
- Update Source0 URL.
- BR Module::Build and build with it.
- Add demo directory to docs.

* Fri May 14 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.12.2-11
- Bump release for perl-5.12.0.

* Fri May 07 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.12.2-10
- Add BR: perl(version) (Fix perl-5.12.x build breakdown).
- Add BR: perl(Test::Pod).

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.12.2-9
- Mass rebuild with perl-5.12.0

* Wed Feb 17 2010 Stepan Kasal <skasal@redhat.com> - 1.12.2-8
- fix check for non-English languages

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.12.2-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12.2-4
- Rebuild for perl 5.10 (again)

* Tue Jan 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.2-3
- BR: Test::More

* Tue Jan 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.2-2
- retag

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.2-1
- rebuild for new perl
- drop demo*.pl scripts
- Upstream license changed to GPL+ or Artistic

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 1.11-7
- BR ExtUtils::MakeMaker.
- Use fixperms macro instead of our own chmod incantation.

* Mon Aug 28 2006 Steven Pritchard <steve@kspei.com> 0.11-6
- Minor spec cleanup to more closely resemble current cpanspec output.

* Mon Sep 05 2005 Steven Pritchard <steve@kspei.com> 0.11-5
- Minor spec cleanup.
- Add Artistic.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Jul 14 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.11-0.fdr.3
- Better summary info (bug 1353 comment #4).
- Canonical source URL (bug 1353 comment #4).
- Missing requirement: TeX::Hyphen (bug 1353 comment #4).
- Replaced /usr/bin/perl by %%{__perl} (bug 1353 comment #4).
- Corrected file permissions (bug 1353 comment #4).

* Wed Jun 09 2004 Steven Pritchard <steve@kspei.com> 0:1.11-0.fdr.2
- Fix License (Artistic only, not GPL or Artistic).

* Wed Jun 09 2004 Steven Pritchard <steve@kspei.com> 0:1.11-0.fdr.1
- Specfile autogenerated.
