%define         realname DBIx-Safe
Name:           perl-DBIx-Safe
Version:        1.2.5
Release:        25%{?dist}
Summary:        Safer access to your database through a DBI database handle
License:        BSD
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/DBIx-Safe/
Source0:        http://search.cpan.org/CPAN/authors/id/T/TU/TURNSTEP/%{realname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# core
BuildRequires:  perl(ExtUtils::MakeMaker) 
BuildRequires:  perl(DBD::Pg)
BuildRequires:  perl(DBI)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Simple)

%description
The purpose of this module is to give controlled, limited access to an
application, rather than simply passing it a raw database handle through
DBI. DBIx::Safe acts as a wrapper to the database, by only allowing
through the commands you tell it to. It filters all things related to
the database handle - methods and attributes.

%prep
%setup -q -n %{realname}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} + 
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/* 

%check
# note this test suite is noisy! :-)


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes  INSTALL  LICENSE  README TODO SIGNATURE t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.2.5-25
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.2.5-24
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.2.5-23
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.2.5-22
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.2.5-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.2.5-20
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.2.5-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.2.5-18
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.2.5-17
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.2.5-16
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.2.5-15
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.5-13
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2.5-11
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2.5-10
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2.5-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.2.5-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 29 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 1.2.5-4
- include  in %%check section

* Mon Jan 29 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 1.2.5-3
- include %%{_fixperms} %%{buildroot}/* after %%install section, replace tab to space in spec.

* Mon Jan 26 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 1.2.5-2
- fix from BZ #481528  Comment #1
- fix source url
- Fix license tag (BSD)
- Include all BR's needed DBD::Pg, DBI, Test::More , Test::Simple

* Sun Jan 25 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 1.2.5-1
- Initial RPM release

