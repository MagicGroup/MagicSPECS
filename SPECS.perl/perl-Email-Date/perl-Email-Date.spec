Name:           perl-Email-Date
Version:	1.104
Release:	1%{?dist}
Summary:        Find and format date headers
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Email-Date/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Email-Date-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(ExtUtils::MakeMaker), perl(Date::Parse), perl(Email::Abstract)
BuildRequires:  perl(Test::More), perl(Time::Local), perl(Time::Piece), perl(Module::Pluggable)
BuildRequires:  perl(Test::Pod), perl(Test::Pod::Coverage), perl(Email::Date::Format) >= 1.000
BuildArch:      noarch
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Bugzilla 468716
Requires:  perl(Email::Abstract)

%description
RFC 2822 defines the "Date:" header. It declares the header a required
part of an email message. The syntax for date headers is clearly laid
out. Stil, even a perfectly planned world has storms. The truth is, many
programs get it wrong. Very wrong. Or, they don't include a "Date:"
header at all. This often forces you to look elsewhere for the date, and
hoping to find something.

For this reason, the tedious process of looking for a valid date has
been encapsulated in this software. Further, the process of creating RFC
compliant date strings is also found in this software.

%prep
%setup -q -n Email-Date-%{version}

%build
sed -i '/LICENSE/ d' Makefile.PL
%{__perl} Makefile.PL INSTALLDIRS=vendor
make

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
%doc README LICENSE
%{perl_vendorlib}/Email/
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.104-1
- 更新到 1.104

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.103-22
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.103-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.103-20
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.103-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.103-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.103-17
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.103-16
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.103-15
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.103-14
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.103-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.103-12
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.103-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.103-10
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.103-9
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.103-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.103-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.103-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.103-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.103-4
- add Requires: perl(Email::Abstract) to fix bz 468716

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.103-3
- rebuild for new perl

* Thu Dec 20 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.103-2
- add BR: Module::Pluggable

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.103-1
- bump to 1.103

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.102-3
- fix license

* Tue Apr 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.102-2
- add missing BR: perl(Test::Pod), perl(Test::Pod::Coverage)
- get rid of WARNING: License

* Sun Apr  1 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.102-1
- Initial package for Fedora
