Name:           perl-Module-ScanDeps
Summary:        Recursively scan Perl code for dependencies
Version:        1.08
Release:        4%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/R/RS/RSCHUPP/Module-ScanDeps-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Module-ScanDeps/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(Module::Build::ModuleInfo)
BuildRequires:  perl(Module::Pluggable)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(constant)
BuildRequires:  perl(prefork)
BuildRequires:  perl(vars)
BuildRequires:  perl(version)

Requires:       perl(DynaLoader)
Requires:       perl(Encode)
Requires:       perl(Exporter)
Requires:       perl(File::Find)
Requires:       perl(File::Spec)
Requires:       perl(File::Temp)
Requires:       perl(Module::Build::ModuleInfo)
Requires:       perl(version)


%{?perl_default_filter}
%{?perl_default_subpackage_tests}

%description
This module scans potential modules used by perl programs and returns a
hash reference.  Its keys are the module names as appears in %INC (e.g.
Test/More.pm).  The values are hash references.

%prep
%setup -q -n Module-ScanDeps-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*

%check


%files
%doc AUTHORS Changes README
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.08-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 1.08-2
- Perl 5.16 rebuild

* Thu Feb 23 2012 Petr Šabata <contyk@redhat.com> - 1.08-1
- 1.08 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Petr Šabata <contyk@redhat.com> - 1.07-1
- 1.07 bump

* Tue Nov 29 2011 Petr Šabata <contyk@redhat.com> - 1.06-1
- 1.06 bump

* Thu Nov 03 2011 Petr Sabata <contyk@redhat.com> - 1.05-1
- 1.05 bump

* Mon Jul 25 2011 Petr Sabata <contyk@redhat.com> - 1.04-1
- 1.04 bump

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.02-2
- Perl mass rebuild

* Thu May  5 2011 Petr sabata <psabata@redhat.com> - 1.02-1
- 1.02 bump (rhbz#691369)
- Removing now obsolete Buildroot and defattr
- Correcting BRs/Rs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 23 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.98-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.98)
- added a new br on perl(File::Spec) (version 0)
- added a new br on perl(File::Temp) (version 0)
- added a new req on perl(File::Spec) (version 0)
- added a new req on perl(File::Temp) (version 0)
- added a new req on perl(Module::Build::ModuleInfo) (version 0)
- added a new req on perl(version) (version 0)

* Fri Jun 11 2010 Petr Sabata <psabata@redhat.com> - 0.97-1
- Update to the latest version

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.95-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.95-2
- rebuild against perl 5.10.1

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.95-1
- auto-update to 0.95 (by cpan-spec-update 0.01)
- add perl_default_filter (pro forma)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.89-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.89-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Steven Pritchard <steve@kspei.com> 0.89-1
- Update to 0.89.
- BR Test::More and prefork.
- Improve description.

* Fri May 16 2008 Steven Pritchard <steve@kspei.com> 0.84-1
- Update to 0.84.

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.82-2
- rebuild for new perl

* Mon Jan 28 2008 Steven Pritchard <steve@kspei.com> 0.82-1
- Update to 0.82.
- BR version.

* Thu Jan 24 2008 Steven Pritchard <steve@kspei.com> 0.81-1
- Update to 0.81.
- Use fixperms macro instead of our own chmod incantation.
- Reformat to match cpanspec output.
- BR ExtUtils::MakeMaker.

* Wed Jun 27 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.75-1
- Update to 0.75.

* Sat May  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.74-1
- Update to 0.74.

* Sat Mar 31 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.73-1
- Update to 0.73.

* Sun Feb  4 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.72-1
- Update to 0.72.
- Added perl(Module::Pluggable) to the build requirements list (t/2-pluggable.t).

* Fri Jan  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.71-1
- Update to 0.71.

* Wed Nov 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.70-1
- Update to 0.70.

* Sat Nov 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.69-1
- Update to 0.69.

* Sat Oct 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.68-1
- Update to 0.68.

* Sun Sep 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.66-1
- Update to 0.66.

* Sat Sep 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.64-1
- Update to 0.64.

* Mon Sep  4 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.63-1
- Update to 0.63.

* Sun Jul 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.62-1
- Update to 0.62.

* Sat Jul  1 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.61-1
- Update to 0.61.

* Wed May 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.60-1
- Update to 0.60.

* Sun May  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.59-2
- Source URL corrected (failed to detect the maintainer change).

* Wed May  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.59-1
- Update to 0.59.

* Thu Mar 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.57-1
- Update to 0.57.

* Tue Feb 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.56-1
- Update to 0.56.

* Tue Jan 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.53-1
- Update to 0.53.

* Fri Sep  9 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.51-1
- Update to Fedora Extras Template.

* Sat Jan 08 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.51-0.fdr.1
- First build.
