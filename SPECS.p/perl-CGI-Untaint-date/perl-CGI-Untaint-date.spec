Name:           perl-CGI-Untaint-date
Version:        1.00
Release:        21%{?dist}
Summary:        Validate a date
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/CGI-Untaint-date/
Source0:        http://search.cpan.org/CPAN/authors/id/T/TM/TMTM/CGI-Untaint-date-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(CGI::Untaint) >= 0.07
BuildRequires:  perl(Date::Simple) >= 0.01
BuildRequires:  perl(Date::Manip) >= 5.00
BuildRequires:  perl(Test::More)
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:	perl(Test::Pod::Coverage) >= 1.00
BuildRequires:	perl(Pod::Perldoc)
Requires:	perl(CGI::Untaint) >= 0.07
Requires:	perl(Date::Simple) >= 0.01
Requires:	perl(Date::Manip) >= 5.00
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
%{summary}.

%prep
%setup -q -n CGI-Untaint-date-%{version}
perldoc -t perlgpl > COPYING
perldoc -t perlartistic > Artistic

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
# These tests fail on koji for some odd reason, but they work fine locally.
# 

%files
%doc Changes COPYING Artistic
%{perl_vendorlib}/CGI/Untaint
%{_mandir}/man3/*.3*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.00-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.00-20
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.00-19
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.00-18
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.00-17
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Tom Callaway <spot@fedoraproject.org> - 1.00-16
- fix build

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.00-14
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.00-12
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.00-11
- Mass rebuild with perl-5.12.0

* Fri Feb 19 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.00-10
- disable tests completely, they fail on koji for some unknown reason

* Fri Feb 19 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.00-9
- fix missing BR for test coverage

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.00-8
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.00-5
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.00-4
- rebuild for new perl

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.00-3
- fix license tag

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.00-2
- bump for fc6

* Mon Jan  9 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.00-1
- bump to 1.00

* Tue Aug 23 2005 Paul Howarth <paul@city-fan.org> 0.03-3
- add BR: perl(Date::Simple) and perl(Date::Manip)
- add license text for GPL and Artistic licenses

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.03-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.03-1
- Initial package for Fedora Extras
