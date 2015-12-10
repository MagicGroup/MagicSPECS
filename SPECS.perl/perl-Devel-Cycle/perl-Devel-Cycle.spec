Name:           perl-Devel-Cycle
Version:	1.12
Release:	3%{?dist}
Summary:        Find memory cycles in objects
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Devel-Cycle/
Source0:        http://www.cpan.org/authors/id/L/LD/LDS/Devel-Cycle-%{version}.tar.gz
Patch0:         perl-Devel-Cycle-1.11-512.patch
BuildArch:      noarch
BuildRequires:  perl(PadWalker) >= 1.0
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(PadWalker) >= 1.0

%description
This is a simple developer's tool for finding circular references in
objects and other types of references. Because of Perl's reference-count
based memory management, circular references will cause memory leaks.

%prep
%setup -q -n Devel-Cycle-%{version}
%patch0 -p1 -b .512

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
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.12-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.12-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.12-1
- 更新到 1.12

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.11-14
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.11-13
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.11-12
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.11-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Petr Šabata <contyk@redhat.com> - 1.11-8
- Fix a Perl 5.12 incompatibility (#757274, RT #56681)
- Remove BuildRoot and defattr

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.11-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.11-5
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.11-4
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.11-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.11-2
- rebuild against perl 5.10.1

* Mon Oct  5 2009 Stepan Kasal <skasal@redhat.com> - 1.11-1
- new upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Steven Pritchard <steve@kspei.com> 1.10-1
- Update to 1.10.

* Thu May 15 2008 Steven Pritchard <steve@kspei.com> 1.09-1
- Update to 1.09.
- Reformat to match cpanspec output.
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-3
- Rebuild for perl 5.10 (again)

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-2
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-1.2
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Wed May 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-1
- Update to 1.07.
- Requirement version: perl(PadWalker) >= 1.0.

* Mon May 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- Update to 1.05.
- New requirement: perl(PadWalker).

* Thu Feb 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-4
- Rebuild for FC5 (perl 5.8.8).

* Sat May 14 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-3
- Add dist tag.

* Mon May 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-2
- Update to 1.04.

* Fri Apr 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-2
- Fedora Extras: FC-4 version.

* Mon Jan 24 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.03-0.fdr.1
- Update to 1.03.

* Sun Jul 04 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.02-0.fdr.1
- First build.
