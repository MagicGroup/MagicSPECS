Name:           perl-Email-MIME
Version:	1.936
Release:	1%{?dist}
Summary:        Easy MIME message parsing

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Email-MIME/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/Email-MIME-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Email::Date::Format)
BuildRequires:  perl(Email::MIME::ContentType) >= 1.011
BuildRequires:  perl(Email::MIME::Encodings) >= 1.313
BuildRequires:  perl(Email::MessageID)
BuildRequires:  perl(Email::Simple) >= 2.004
BuildRequires:  perl(MIME::Types) >= 1.13
BuildRequires:  perl(Test::MinimumVersion)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(MIME::Types) >= 1.13
Obsoletes:      perl-Email-MIME-Creator < 1.457
Obsoletes:      perl-Email-MIME-Modifier < 1.445
Provides:       perl-Email-MIME-Creator = %{version}
Provides:       perl-Email-MIME-Modifier = %{version}

%description
This is an extension of the Email::Simple module, to handle MIME
encoded messages. It takes a message as a string, splits it up
into its constituent parts, and allows you access to various
parts of the message. Headers are decoded from MIME encoding.


%prep
%setup -q -n Email-MIME-%{version}


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
%doc Changes LICENSE README
%{perl_vendorlib}/Email/
%{_mandir}/man3/*.3pm*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.936-1
- 更新到 1.936

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.906-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.906-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.906-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.906-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.906-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.906-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.906-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec  3 2010 Paul Howarth <paul@city-fan.oth> - 1.906-2
- Obsolete perl-Email-MIME-Creator and perl-Email-MIME-Modifier, merged into
  Email::MIME at version 1.900

* Fri Dec  3 2010 Paul Howarth <paul@city-fan.oth> - 1.906-1
- Update to 1.906 (#659635)
- BR: perl(Email::Date::Format) and perl(Email::MessageID)
- BR: perl(Test::MinimumVersion) for additional test coverage
- Bump perl(Email::MIME::Encodings) version requirement to 1.313
- Bump perl(Email::Simple) version requirement to 2.004

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.863-5
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.863-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.863-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.863-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.863-1
- update to 1.863

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.861-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.861-3
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.861-2
- rebuild for new perl

* Wed Nov 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.861-1
- bump to 1.861

* Fri Mar 23 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.859-1
- Update to 1.859.

* Sat Feb 10 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.858-1
- Update to 1.858.

* Fri Dec  1 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.857-1
- Update to 1.857.

* Thu Oct 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.855-1
- Update to 1.855.

* Sun Oct 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.854-1
- Update to 1.854.

* Fri Oct 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.853-1
- Update to 1.853.

* Wed Sep  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.852-1
- Update to 1.852.

* Mon Aug 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.851-1
- Update to 1.851.

* Fri Jul 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.85-1
- Update to 1.85.

* Thu Sep  8 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.82-2
- Requires Email::Simple (rpm "use base" shortcoming).

* Thu Sep 08 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.82-1
- First build.
