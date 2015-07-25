Name:           perl-Sub-Uplevel
Summary:        Apparently run a function in a higher stack frame
Epoch:          1
Version:        0.24
Release:        11%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/Sub-Uplevel-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Sub-Uplevel
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
# Tests:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::More)
# Optional:
BuildRequires:  perl(Test::Script) >= 1.05
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Carp)

%{?perl_default_filter}

%description
Like Tcl's uplevel() function, but not quite so dangerous. The idea is
just to fool caller(). All the really naughty bits of Tcl's uplevel()
are avoided.

%prep
%setup -q -n Sub-Uplevel-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes LICENSE README README.PATCHING examples/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1:0.24-11
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1:0.24-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1:0.24-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1:0.24-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:0.24-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:0.24-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:0.24-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1:0.24-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1:0.24-2
- Perl 5.16 rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1:0.24-1
- 0.24 bump

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1:0.22-7
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.22-5
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.22-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.22-2
- Mass rebuild with perl-5.12.0

* Sat Feb 13 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.22-1
- don't run tests explicitly marked as "AUTHOR"
- add perl_default_filter
- auto-update by cpan-spec-update 0.002
- Add epoch of 1 (0.2002 => 0.22)
- added a new br on perl(Carp) (version 0)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.2002-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Steven Pritchard <steve@kspei.com> 0.2002-1
- Update to 0.2002.
- BR Test::More.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.1901-2
- Rebuild for perl 5.10 (again)

* Wed Feb 20 2008 Steven Pritchard <steve@kspei.com> 0.1901-1
- Update to 0.1901.
- Use fixperms macro instead of our own chmod incantation.
- Reformat to match cpanspec output.

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.18-2
- rebuild for new perl

* Mon Dec 17 2007 Ralf Corsépius <rc040203@freenet.de> - 0.18-1
- Update to 0.18.

* Sat Nov 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.14-1
- Update to 0.14.

* Fri Jun 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.13-1
- Update to 0.13.

* Sat May 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.12-1
- Update to 0.12.
- Makefile.PL -> Build.PL.

* Fri Apr 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.10-1
- Update to 0.10.
- New upstream maintainer.
- Patch dropped.

* Wed Feb 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.09-4
- Uplevel.pm patch (perl 5.8.8). See bugzilla entry #182488.

* Thu Dec 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.09-3
- Dist tag.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.09-2
- rebuilt

* Thu Jul  8 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.09-1
- Update to 0.09 (with license info).

* Sun Jul  4 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.08-0.fdr.1
- First build.
