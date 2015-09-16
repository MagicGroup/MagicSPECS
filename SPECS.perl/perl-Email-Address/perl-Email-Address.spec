Name:           perl-Email-Address
Version:	1.907
Release:	1%{?dist}
Summary:        RFC 2822 Address Parsing and Creation

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Email-Address/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/Email-Address-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More) >= 0.47
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This class implements a regex-based RFC 2822 parser that locates email
addresses in strings and returns a list of Email::Address objects found.
Alternatively you may construct objects manually. The goal of this software
is to be correct, and very very fast.

%prep
%setup -q -n Email-Address-%{version}
%{__perl} -pi -e 's|^#!/usr/local/bin/perl\b|#!%{__perl}|' bench/ea-vs-ma.pl


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes LICENSE README META.json bench/
%{perl_vendorlib}/Email/
%{_mandir}/man3/*.3pm*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.907-1
- 更新到 1.907

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.896-4
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.896-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.896-2
- 为 Magic 3.0 重建

* Tue Sep 18 2012 Marcela Mašláňová <mmaslano@redhat.com> 1.896-1
- update to 1.896

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.889-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.889-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.889-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.889-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.889-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.889-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.889-6
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.889-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.889-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.889-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.889-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.889-1
- Upstream update.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.888-3
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.888-2
- rebuild for new perl

* Sat Jun 23 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.888-1
- Update to 1.888.

* Thu Apr  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.887-1
- Update to 1.887.

* Sun Mar 18 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.886-1
- Update to 1.886.

* Tue Dec 12 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.884-1
- Update to 1.884.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.883-1
- Update to 1.883.

* Wed Nov 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.882-1
- Update to 1.882.

* Sat Nov 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.880-1
- Update to 1.880.

* Fri Oct 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.871-1
- Update to 1.871.

* Sat Aug 12 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.870-1
- Update to 1.870.

* Sat Jul 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.86-1
- Update to 1.86.

* Tue Jul 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.85-1
- Update to 1.85.

* Thu Sep 08 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.80-1
- First build.
