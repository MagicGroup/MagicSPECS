Name:           perl-Test-Pod
Version:        1.45
Release:        13%{?dist}
Summary:        Test POD files for correctness
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Test-Pod/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DW/DWHEELER/Test-Pod-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Build) >= 0.30
BuildRequires:  perl(Pod::Simple) >= 3.05
BuildRequires:  perl(Test::Builder::Tester) >= 1.02
BuildRequires:  perl(Test::More) >= 0.62
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Pod::Simple) >= 3.05
Requires:       perl(Test::Builder::Tester) >= 1.02
Requires:       perl(Test::More) >= 0.62

%description
Check POD files for errors or warnings in a test file, using Pod::Simple to do
the heavy lifting.


%prep
%setup -q -n Test-Pod-%{version}


%build
%{__perl} Build.PL installdirs=vendor
./Build


%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} \; 2>/dev/null
%{_fixperms} $RPM_BUILD_ROOT


%check
LC_ALL=C ./Build test


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Pod.3pm*


%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.45-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.45-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.45-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.45-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.45-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.45-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.45-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.45-5
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 1.45-4
- Round Module::Build version to 2 digits

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.45-2
- Perl mass rebuild

* Thu Mar 10 2011 Petr Sabata <psabata@redhat.com> - 1.45-1
- 1.45 bump
- Buildroot garbage cleanup

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Karsten Hopp <karsten@redhat.com> 1.44-3
- bump release and rebuild to fix dependency issues on s390x

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.44-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sat Jul 31 2010 Paul Howarth <paul@city-fan.org> - 1.44-1
- update to 1.44:
  - use Module::Build::Compat's "traditional" configuration
  - loosen version requirements for Test::More and Pod::Simple
  - add File::Spec to the list of prereqs
- drop perl(Test::More) version requirement to 0.62
- drop perl(Pod::Simple) version requirement to 3.05

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.42-2
- Mass rebuild with perl-5.12.0

* Thu Mar 11 2010 Paul Howarth <paul@city-fan.org> - 1.42-1
- update to 1.42
- new upstream maintainer
- use Module::Build flow
- include README
- use less generic %%description and %%summary
- use _fixperms macro instead of our own chmod incantation
- bump Test::More build requirement to 0.70
- add versioned requires for Pod::Simple, Test::Builder::Tester and Test::More

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.40-2
- rebuild against perl 5.10.1

* Fri Oct 30 2009 Stepan Kasal <skasal@redhat.com> - 1.40-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-6
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-5
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.26-4
- rebuild for perl 5.10 (again)

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.26-3
- rebuild for new perl

* Thu Dec 20 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.26-2
- license tag fix

* Fri Jul 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.26-1
- Update to 1.26.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.24-2
- Rebuild for FC5 (perl 5.8.8).

* Fri Feb  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.24-1
- Update to 1.24.

* Thu Dec 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.22-1
- Update to 1.22.

* Thu May 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.20-3
- Add dist tag.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.20-2
- rebuilt

* Thu Jun 24 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.20-0.fdr.1
- Update to 1.20.

* Wed May 12 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.16-0.fdr.2
- Avoid creation of the perllocal.pod file (make pure_install).

* Mon May  3 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.16-0.fdr.1
- Update to 1.16, dir handling patch applied upstream.

* Fri Apr 30 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.14-0.fdr.1
- Update to 1.14.
- Require perl(:MODULE_COMPAT_*).
- Add patch to avoid warnings from all_pod_files().

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.12-0.fdr.1
- Update to 1.12.

* Thu Jan 22 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.08-0.fdr.1
- Update to 1.08.
- Use %%{perl_vendorlib}.

* Wed Nov  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-0.fdr.1
- First build.
