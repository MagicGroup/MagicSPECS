Name:           perl-Object-Event
Version:        1.23
Release:        6%{?dist}
Summary:        Class that provides an event callback interface
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Object-Event/
Source0:        http://www.cpan.org/authors/id/E/EL/ELMEX/Object-Event-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(AnyEvent::Util)
BuildRequires:  perl(common::sense)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module was mainly written for Net::XMPP2, Net::IRC3, AnyEvent::HTTPD
and BS to provide a consistent API for registering and emitting events.
Even though I originally wrote it for those modules I released it
separately in case anyone may find this module useful.

%prep
%setup -q -n Object-Event-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.23-6
- 为 Magic 3.0 重建

* Tue Jan 15 2013 Liu Di <liudidi@gmail.com> - 1.23-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 1.23-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 09 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 1.23-1
- Update to 0.23
- Spec clean-up
- Add perl default filter to spec file

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.22-2
- Perl mass rebuild

* Sat Mar 12 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 1.22-1
- Update to 1.22

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.21-3
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.21-2
- Mass rebuild with perl-5.12.0

* Sun Apr 11 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 1.21-1
- Update to 1.21

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.7-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Allisson Azevedo <allisson@gmail.com> 0.7-1
- Initial rpm release.
