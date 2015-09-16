Summary:        Test case module for Perl
Name:           perl-Test-Manifest
Version:	2.02
Release:	1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-Manifest/
Source0:        http://search.cpan.org/CPAN/authors/id/B/BD/BDFOY/Test-Manifest-%{version}.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(File::Spec)
Requires:       perl(Test::Harness)

%description
MakeMaker assumes that you want to run all of the .t files in the t/ directory
in ascii-betical order during  unless you say otherwise. This leads to
some interesting naming schemes for test files to get them in the desired
order.

You can specify any order or any files that you like, though, with the test
directive to WriteMakefile.

Test::Manifest looks in the t/test_manifest file to find out which tests you
want to run and the order in which you want to run them. It constructs the
right value for MakeMaker to do the right thing.

%prep
%setup -q -n Test-Manifest-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Manifest.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.02-1
- 更新到 2.02

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.23-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.23-2
- 为 Magic 3.0 重建

* Tue Jul 24 2012 Paul Howarth <paul@city-fan.org> - 1.23-1
- Update to 0.23
  - Fix bug for missing file (should warn and skip, not pass to run_t_files)
  - File path and unlink fixes for VMS (CPAN RT#32061)
- Add patch to reinstate manpage, dropped upstream
- BR:/R: perl(File::Spec) and perl(Test::Harness)
- BR: perl(base), perl(Carp), perl(Exporter) and perl(File::Spec::Functions)
- Don't use macros for commands
- Reformat %%description
- Don't need to remove empty directories from the buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Use %%{_fixperms} macro rather than our own chmod incantation
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit
- Package LICENSE and README files

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.22-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.22-10
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.22-8
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.22-7
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.22-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.22-3
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.22-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.22-1
- 1.22
- license fix

* Fri Feb 23 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.17-1
- Update to 1.17.

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-5
- Rebuild for FC6.

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-4
- Rebuild for FC5 (perl 5.8.8).

* Thu May 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-3
- Add dist tag.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.14-2
- rebuilt

* Tue Mar 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-1
- Update to 1.14.

* Wed Mar 23 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.13-1
- Update to 1.13.

* Sat Oct 30 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.11-1
- Update to 1.11.

* Sun Jun 13 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.93-0.fdr.2
- Bring up to date with current fedora.us perl spec template.
- Require perl >= 2:5.8.0 for vendor install dir support
  (also resolves the ExtUtils::MakeMaker version problem).

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.93-0.fdr.1
- Update to 0.93.
- Reduce directory ownership bloat.

* Sun Oct 12 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.92-0.fdr.1
- First build.
