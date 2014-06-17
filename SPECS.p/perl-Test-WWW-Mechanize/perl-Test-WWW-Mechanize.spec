Name:           perl-Test-WWW-Mechanize
Version:        1.44
Release:        9%{?dist}
Summary:        Testing-specific WWW::Mechanize subclass

Group:          Development/Libraries
License:        Artistic 2.0
URL:            http://search.cpan.org/dist/Test-WWW-Mechanize/
Source0:        http://www.cpan.org/authors/id/P/PE/PETDANCE/Test-WWW-Mechanize-%{version}.tar.gz
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(Carp::Assert::More)
BuildRequires:  perl(CGI)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTML::Lint)
BuildRequires:  perl(HTML::TreeBuilder)
BuildRequires:  perl(HTTP::Server::Simple) >= 0.42
BuildRequires:  perl(HTTP::Server::Simple::CGI)
BuildRequires:  perl(LWP) >= 6.02
BuildRequires:  perl(Test::Builder::Tester) >= 1.09
BuildRequires:  perl(Test::LongString) >= 0.15
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Pod) >= 0.08
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
BuildRequires:  perl(URI::file)
BuildRequires:  perl(WWW::Mechanize) >= 1.68

Requires:       perl(WWW::Mechanize) >= 1.68
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(WWW::Mechanize\\)

%description
Test::WWW::Mechanize is a subclass of WWW::Mechanize that incorporates
features for web application testing.


%prep
%setup -q -n Test-WWW-Mechanize-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*


%check
make test

%files
%doc Changes README*
%{perl_vendorlib}/Test
%{_mandir}/man3/*.3pm*


%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.44-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.44-8
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.44-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.44-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.44-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.44-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Petr Pisar <ppisar@redhat.com> - 1.44-2
- Perl 5.16 rebuild

* Tue Jul 10 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.44-1
- Upstream update.

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.42-2
- Perl 5.16 rebuild

* Wed Jun 27 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.42-1
- Upstream update.

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 1.40-2
- Perl 5.16 rebuild

* Mon Apr 30 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40-1
- Upstream update.

* Sat Jan 14 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.38-1
- Upstream update.
- Add rpm-4.9 filter.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> 1.34-1
- update to latest upstream version
- license change again - Artistic 2.0 only

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.32-2
- Perl mass rebuild

* Sat May 14 2011 Iain Arnell <iarnell@gmail.com> 1.32-1
- update to latest upstream and drop patches
- fix license tag: GPL+ or Artistic 2.0

* Mon Apr 11 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.30-3
- Add Test-WWW-Mechanize-1.30-svn.r712.diff (Fix FTBS on f13/f14/f15).
- Add Test-WWW-Mechanize-1.30-Test-LongString.diff (Fix FTBS on f16).
- Spec file cleanup.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.30-1
- Upstream update.
- BR: perl(HTML::TreeBuilder).

* Wed Dec 08 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.28-2
- Add BR: perl(CGI) (Fix FTBFS: BZ 661092).

* Thu May 13 2010 Petr Pisar <ppisar@redhat.com> - 1.28-1
- Version bump
- Sort dependencies

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.24-6
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.24-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Ralf Corsepius <corsepiu@fedoraproject.org> - 1.24-2
- Add BR: perl(HTML::Lint).

* Fri Feb 20 2009 Ralf Corsepius <corsepiu@fedoraproject.org> - 1.24-1
- Upstream update.

* Wed Jun 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.20-1
- update to 1.20
- update BR's

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.14-2
- rebuild for new perl

* Thu Jun  7 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-1
- Update to 1.14.

* Fri Jul  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-1
- Update to 1.12.

* Mon Jun 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.10-1
- Update to 1.10.

* Thu Mar  2 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.08-2
- Rebuild for FC5 (perl 5.8.8).

* Tue Nov 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.08-1
- Update to 1.08.

* Thu Aug 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-1
- Update to 1.06.

* Tue Mar 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-1
- First build.
