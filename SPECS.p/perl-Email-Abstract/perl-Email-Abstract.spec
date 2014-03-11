Name:           perl-Email-Abstract
Version:        3.002
Release:        7%{?dist}
Summary:        Unified interface to mail representations
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Email-Abstract/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Email-Abstract-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(ExtUtils::MakeMaker), perl(Test::More), perl(Class::ISA), perl(Email::Simple)
BuildRequires:  perl(MIME::Entity), perl(Module::Pluggable), perl(Mail::Message), perl(Scalar::Util)
BuildRequires:  perl(Email::MIME), perl(Test::Pod), perl(Test::Pod::Coverage), perl(Test::More)
BuildArch:      noarch
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
"Email::Abstract" provides module writers with the ability to write
representation-independent mail handling code. For instance, in the
cases of "Mail::Thread" or "Mail::ListDetector", a key part of the code
involves reading the headers from a mail object. Where previously one
would either have to specify the mail class required, or to build a new
object from scratch, "Email::Abstract" can be used to perform certain
simple operations on an object regardless of its underlying
representation.

%prep
%setup -q -n Email-Abstract-%{version}
%build
sed -i '/LICENSE/ d' Makefile.PL
%{__perl} Makefile.PL INSTALLDIRS=vendor
make

%install
rm -rf $RPM_BUILD_ROOT _docs
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE Changes
%{perl_vendorlib}/Email/
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 3.002-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 3.002-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.002-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 3.002-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.002-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jul 12 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.002-1
- update to 3.002

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.001-5
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.001-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.001-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.001-1
- update to 3.001

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.134-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.134-3
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.134-2
- rebuild for new perl

* Wed Nov 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.134-1
- 2.134

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.132-4
- license fix

* Mon Apr 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.132-3
- add missing BR Email::MIME, Test::Pod, Test::Pod::Coverage

* Mon Apr  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.132-2
- remove LICENSE line from Makefile.PL
- add BR Module::Pluggable, Mail::Message

* Sun Apr  1 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.132-1
- Initial package for Fedora
