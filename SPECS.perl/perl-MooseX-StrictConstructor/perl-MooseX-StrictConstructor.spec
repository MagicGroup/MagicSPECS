Name:           perl-MooseX-StrictConstructor 
Version:        0.19
Release:        9%{?dist}
# see lib/MooseX/StrictConstructor.pm
License:        Artistic 2.0
Group:          Development/Libraries
Summary:        Make your object constructors blow up on unknown attributes 
Source:         http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/MooseX-StrictConstructor-%{version}.tar.gz 
Url:            http://search.cpan.org/dist/MooseX-StrictConstructor
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch
BuildRequires:  perl(B)
BuildRequires:  perl(ExtUtils::MakeMaker) 
BuildRequires:  perl(Moose) >= 0.94
BuildRequires:  perl(Moose::Exporter)
BuildRequires:  perl(Moose::Role)
BuildRequires:  perl(Moose::Util::MetaRole)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::Moose)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(namespace::autoclean)

%{?perl_default_filter}

%description
Simply loading this module makes your constructors "strict". If your
constructor is called with an attribute init argument that your class does
not declare, then it calls "Carp::confess()". This is a great way to catch
small typos.

%prep
%setup -q -n MooseX-StrictConstructor-%{version}

# avoid rpmlint wrong-script-interpreter warning
sed -i '1s~#!.*perl~#!%{__perl}~' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.19-9
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.19-8
- 为 Magic 3.0 重建

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.19-7
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.19-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.19-2
- Perl 5.16 rebuild

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.19-1
- update to latest upstream version

* Tue Jan 17 2012 Iain Arnell <iarnell@gmail.com> - 0.18-2
- rebuilt again for F17 mass rebuild

* Sat Jan 14 2012 Iain Arnell <iarnell@gmail.com> 0.18-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.16-2
- Perl mass rebuild

* Sat Apr 23 2011 Iain Arnell <iarnell@gmail.com> 0.16-1
- update to latest upstream version

* Fri Apr 22 2011 Iain Arnell <iarnell@gmail.com> 0.15-1
- update to latest upstream version

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 0.13-1
- update to latest upstream version
- use perl_default_filter

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 08 2010 Iain Arnell <iarnell@epo.org> 0.11-1
- update to latest upstream
- license change from "GPL+ or Artistic" to "Artistic 2.0"
- clean up spec for modern rpmbuild

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.08-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08-1
- update to 0.08

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.07-3
- rebuild under new Moose level

* Wed Oct 29 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.07-2
- bump

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- clean up for submission

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.07-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)

