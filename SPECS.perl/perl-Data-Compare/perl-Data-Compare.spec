Name:           perl-Data-Compare
Version:        1.22
Release:        16%{?dist}
Summary:        Compare perl data structures
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Data-Compare/
Source0:        http://www.cpan.org/authors/id/D/DC/DCANTRELL/Data-Compare-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(Scalar::Properties)
BuildRequires:  perl(Clone)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(JSON)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Not autodetected.
Requires:	perl(File::Find::Rule)

%description
This module compares arbitrary data structures to see if they are copies
of each other.


%prep
%setup -q -n Data-Compare-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%files
%doc CHANGES MAINTAINERS-NOTE README TODO
%{perl_vendorlib}/Data/
%{_mandir}/man3/*.3pm*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.22-16
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.22-15
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.22-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.22-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.22-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.22-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.22-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.22-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.22-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.22-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.22-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.22-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.22-4
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.22-2
- Perl mass rebuild

* Tue Jun  7 2011 Tom Callaway <spot@fedoraproject.org> - 1.22-1
- update to 1.22
- add Requires: perl(File::Find::Rule)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.21-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.21-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.21-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.21-1
- Upstream update.
- spec file massaging.

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17-2
- Rebuild for new perl

* Wed Nov 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17-1
- 0.17

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.16-1.2
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.16-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sun Mar 18 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.16-1
- Update to 0.16.

* Mon Feb 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.15-1
- Update to 0.15.

* Sun Nov  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.14-2
- New BR: perl(Clone) is needed by t/deep-objects.t.

* Sun Nov  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.14-1
- Update to 0.14.

* Sun Apr 09 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.13-1
- First build.
