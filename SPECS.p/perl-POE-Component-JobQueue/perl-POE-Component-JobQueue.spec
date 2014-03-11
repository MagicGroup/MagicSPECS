Name:           perl-POE-Component-JobQueue
Version:        0.571
Release:        4%{?dist}
Summary:        Process a large number of tasks with a finite number of workers
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/POE-Component-JobQueue
Source0: http://search.cpan.org/CPAN/authors/id/R/RC/RCAPUTO/POE-Component-JobQueue-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(POE) >= 1.007
BuildRequires:  perl(POE::Session)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(POE) >= 1.007

%description
POE::Component::JobQueue manages a finite pool of worker sessions as
they handle an arbitrarily large number of tasks.  It often is used as
a form of flow control, preventing an arbitrarily large number of
worker sessions from exhausting some finite resource.

%{?perl_default_filter}

%prep
%setup -q -n POE-Component-JobQueue-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
# readme says this is a good example.  So, why not?
cp t/01_queues.t example_01_queues
chmod -x example_01_queues

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check


%files
%doc CHANGES README example_01_queues
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.571-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.571-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.571-2
- Perl 5.16 rebuild

* Tue Jan 17 2012 Petr Šabata <contyk@redhat.com> - 0.571-1
- 0.571 bump
- Spec cleanup

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.570-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.570-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.570-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.570-4
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.570-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.570-2
- rebuild against perl 5.10.1

* Tue Aug 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.570-1
- auto-update to 0.570 (by cpan-spec-update 0.01)
- added a new br on perl(ExtUtils::MakeMaker) (version 0)
- altered br on perl(POE) (0.11 => 1.007)
- added a new req on perl(POE) (version 1.007)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5500-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5500-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.5500-3
Rebuild for new perl

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.5500-2
- bump for mass rebuild

* Wed Aug 09 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.5500-1
- update to cpan ver 0.55

* Sat Jul  8 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.5402-1
- bump for fe build/release

* Fri Jul 07 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.5402-0
- Initial spec file for F-E
