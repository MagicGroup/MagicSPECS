Name:           perl-Email-Send
Version:        2.198
Release:        7%{?dist}
Summary:        Module for sending email
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Email-Send/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Email-Send-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(Email::Address), perl(Email::Simple), perl(File::Spec), perl(Module::Pluggable)
BuildRequires:  perl(Return::Value), perl(Scalar::Util), perl(Symbol), perl(Test::More)
BuildRequires:  perl(ExtUtils::MakeMaker), perl(IO::All), perl(Email::Abstract)
BuildRequires:  perl(Mail::Internet), perl(MIME::Entity), perl(Test::Pod), perl(Test::Pod::Coverage)
BuildRequires:  /usr/sbin/sendmail
BuildArch:      noarch
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module provides a very simple, very clean, very specific interface
to multiple Email mailers. The goal of this software is to be small and
simple, easy to use, and easy to extend.

%prep
%setup -q -n Email-Send-%{version}

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
%doc README LICENSE
%{perl_vendorlib}/Email/
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.198-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.198-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.198-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.198-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.198-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.198-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Jun 29 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.198-1
- update to 2.198

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.194-5
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.194-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.194-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.194-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.194-1
- update to 2.194

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.192-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.192-2
Rebuild for new perl

* Wed Nov 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.192-1
- bump to 2.192

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.185-3
- license tag fix

* Tue Apr 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.185-2
- get rid of WARNING: LICENSE... 
- add missing BR

* Sun Apr  1 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.185-1
- Initial package for Fedora
