Name:       perl-Catalyst-View-PDF-Reuse 
Version:	0.05
Release:	2%{?dist}
# lib/Catalyst/Helper/View/PDF/Reuse.pm -> GPL+ or Artistic
# lib/Catalyst/View/PDF/Reuse.pm -> GPL+ or Artistic
# lib/Template/Plugin/Catalyst/View/PDF/Reuse.pm -> GPL+ or Artistic
License:    GPL+ or Artistic 
Group:      Development/Libraries
Summary:    Create PDF files from Catalyst using Template Toolkit templates 
Source:     http://search.cpan.org/CPAN/authors/id/A/AL/ALTREUS/Catalyst-View-PDF-Reuse-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/Catalyst-View-PDF-Reuse
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(Catalyst::View::TT)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(File::chdir)
BuildRequires: perl(parent)
BuildRequires: perl(PDF::Reuse)
BuildRequires: perl(Template::Plugin::Procedural)
BuildRequires: perl(Test::More)

# not picked up due to use base/parent
Requires:      perl(Catalyst::View::TT)
Requires:      perl(Template::Plugin::Procedural)

%description
Catalyst::View::PDF::Reuse provides the facility to generate PDF files
from a Catalyst application by embedding PDF::Reuse commands within a
Template::Toolkit template.  Within your template you will have access
to a 'pdf' object which has methods corresponding to all of PDF::Reuse's
functions.


%prep
%setup -q -n Catalyst-View-PDF-Reuse-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%files
%defattr(-,root,root,-)
%doc Changes README 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.05-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.05-1
- 更新到 0.05

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.04-17
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.04-16
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.04-15
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.04-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.04-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.04-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.04-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.04-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.04-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.04-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.04-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.04-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.04-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.04-4
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.04-2
- Perl mass rebuild

* Sun Mar 13 2011 Iain Arnell <iarnell@gmail.com> 0.04-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-5
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.03-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 09 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03-1
- submission

* Tue Jun 09 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)

