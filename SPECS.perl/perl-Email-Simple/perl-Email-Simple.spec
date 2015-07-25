Name:           perl-Email-Simple
Version:        2.100
Release:        9%{?dist}
Summary:        Simple parsing of RFC2822 message format and headers

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Email-Simple/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/Email-Simple-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
BuildRequires:  perl(Test::MinimumVersion)
BuildRequires:  perl(Test::More) >= 0.47
BuildRequires:	perl(ExtUtils::MakeMaker), perl(Email::Date::Format)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:	perl-Email-Simple-Creator = %{version}-%{release}
Obsoletes:	perl-Email-Simple-Creator <= 1.424

%description
"Email::Simple" is the first deliverable of the "Perl Email Project", a
reaction against the complexity and increasing bugginess of the
"Mail::*" modules. In contrast, "Email::*" modules are meant to be
simple to use and to maintain, pared to the bone, fast, minimal in their
external dependencies, and correct.


%prep
%setup -q -n Email-Simple-%{version}


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
# remove until fix of Perl::MinimalVersion and version.pm
rm -rf t/perl-minver.t



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/Email/
%{_mandir}/man3/*.3pm*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.100-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.100-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.100-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.100-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.100-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.100-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.100-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.100-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jul 12 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.100-1
- update to 2.100
- absorbs perl-Email-Simple-Creator

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.005-6
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.005-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.005-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.005-1
- Upstream update.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.003-3
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.003-2
- rebuild for new perl, disable unnecessary BR on perl-Email-MIME

* Wed Nov 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.003-1
- bump to 2.003

* Fri Mar 23 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.999-1
- Update to 1.999.

* Sat Feb 10 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.998-1
- Update to 1.998.

* Fri Dec  1 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.996-1
- Update to 1.996.

* Thu Oct 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.995-1
- Update to 1.995.

* Sat Oct  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.992-1
- Update to 1.992.

* Wed Sep  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.990-1
- Update to 1.990.

* Mon Aug 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.980-1
- Update to 1.980.

* Sat Jul 29 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.96-1
- Update to 1.96.

* Sat Jul 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.95-1
- Update to 1.95.

* Tue Jul 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.94-1
- Update to 1.94.

* Thu Sep 08 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.92-1
- First build.
