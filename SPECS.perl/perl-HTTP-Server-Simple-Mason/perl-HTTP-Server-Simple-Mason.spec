Name: 		perl-HTTP-Server-Simple-Mason
Version: 	0.14
Release: 	18%{?dist}
Summary:	HTTP::Server::Simple::Mason Perl module
License:	GPL+ or Artistic
Group:		Development/Libraries
URL: 		http://search.cpan.org/dist/HTTP-Server-Simple-Mason/
Source: 	http://search.cpan.org/CPAN/authors/id/J/JE/JESSE/HTTP-Server-Simple-Mason-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: noarch

BuildRequires:	perl(HTML::Mason) >= 1.25
BuildRequires:	perl(HTTP::Server::Simple) >= 0.04
BuildRequires:	perl(Hook::LexWrap)

# Required by the tests
BuildRequires:  perl(Test::More)
BuildRequires: 	perl(Test::Pod) >= 1.14
BuildRequires: 	perl(Test::Pod::Coverage) >= 1.04

# Improved tests (dynamic requirement of HTML::Mason)
BuildRequires: 	perl(LWP::Simple)

Requires:	perl(HTTP::Server::Simple::CGI)

%description
An abstract baseclass for a standalone mason server

%prep
%setup -q -n HTTP-Server-Simple-Mason-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%clean
rm -rf $RPM_BUILD_ROOT

%check


%files
%defattr(-,root,root,-)
%doc Changes ex
%{perl_vendorlib}/HTTP
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.14-18
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.14-17
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.14-16
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.14-15
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.14-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.14-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.14-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.14-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.14-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.14-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Sep 13 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.14-1
- Upstream update.

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.13-2
- rebuild against perl 5.10.1

* Tue Oct 13 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.13-1
- Upstream update.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.12-1
- Upstream update.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.11-1
- Upstream update.

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.09-7
- rebuild for new perl

* Thu Sep 06 2007 Ralf Corsépius <rc040203@freenet.de> - 0.09-6
- Update license tag.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.09-5
- Mass rebuild.

* Mon Feb 20 2006 Ralf Corsépius <rc040203@freenet.de> - 0.09-4
- Rebuild.

* Wed Oct 12 2005 Ralf Corsepius <rc040203@freenet.de> - 0.09-3
- Spec cleanup.

* Sun Oct 09 2005 Ralf Corsepius <rc040203@freenet.de> - 0.09-2
- Fix Source0.
- Add BR: perl(HTTP::Server::Simple::CGI).
- Ship ex/.

* Tue Sep 13 2005 Ralf Corsepius <ralf@links2linux.de> - 0.09-1
- BR: Test::Pod.

* Sun Sep 04 2005 Ralf Corsepius <ralf@links2linux.de> - 0.09-0
- Update.
