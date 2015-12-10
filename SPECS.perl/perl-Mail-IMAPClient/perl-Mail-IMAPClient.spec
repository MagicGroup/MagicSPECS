Name:           perl-Mail-IMAPClient
Version:	3.37
Release:	3%{?dist}
Summary:        An IMAP Client API
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Mail-IMAPClient/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PL/PLOBBES/Mail-IMAPClient-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(ExtUtils::MakeMaker), perl(IO::Socket), perl(constant), perl(Socket)
BuildRequires:  perl(IO::File), perl(IO::Select), perl(Fcntl), perl(Errno), perl(Carp)
BuildRequires:  perl(Data::Dumper), perl(Parse::RecDescent), perl(Test::More)
BuildArch:      noarch
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module provides perl routines that simplify a sockets connection 
to and an IMAP conversation with an IMAP server. 

%prep
%setup -q -n Mail-IMAPClient-%{version}
sed -i 's#/usr/local/bin/perl#/usr/bin/perl#' examples/*.pl

# Turn off exec bits in examples to avoid docfile dependencies
chmod -c -x examples/*.pl

# Fix character encoding in documentation
iconv -f iso-8859-1 -t utf-8 < Changes > Changes.utf8
mv Changes.utf8 Changes

%build
# the extended tests cannot be run without an IMAP server
yes n | %{__perl} Makefile.PL INSTALLDIRS=vendor
make

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README examples/
%{perl_vendorlib}/Mail/
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 3.37-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 3.37-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 3.37-1
- 更新到 3.37

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 3.30-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 3.30-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 3.30-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.30-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.30-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.30-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 3.30-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 3.30-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Nick Bebout <nb@fedoraproject.org> - 3.30-1
- Upgrade to 3.30

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.28-2
- Perl mass rebuild

* Wed Mar 16 2011 Nick Bebout <nb@fedoraproject.org> - 3.28-1
- Upgrade to 3.28

* Mon Feb 21 2011 Nick Bebout <nb@fedoraproject.org> - 3.27-1
- Upgrade to 3.27

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct  2 2010 Paul Howarth <paul@city-fan.org> - 3.25-2
- turn off exec bits on examples to avoid docfile dependencies (#639523)
- fix character encoding in documentation

* Mon Jul 12 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.25-1
- update to 3.25

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.21-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.21-2
- rebuild against perl 5.10.1

* Fri Sep 25 2009 Stepan Kasal <skasal@redhat.com> - 3.21-1
- new upstream source

* Sat Sep  5 2009 Stepan Kasal <skasal@redhat.com> - 3.20-1
- new upstream source

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.14-1
- update to 3.14

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.08-1
- 3.08

* Tue Mar 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.05-1
- 3.05

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.2.9-6
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.2.9-5
- rebuild for new perl

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.2.9-4
- license tag fix

* Mon Apr  9 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.2.9-3
- set examples as non-exec, fix intepreter

* Wed Apr  4 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.2.9-2
- add docs/ and examples/ as %%doc

* Mon Apr  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.2.9-1
- Initial package for Fedora
