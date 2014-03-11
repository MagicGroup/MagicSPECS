Name:           perl-Time-Duration
Summary:        Time-Duration - rounded or exact English expression of durations
Version:        1.06
Release:        14%{?dist}
License:        GPLv2+ or Artistic 2.0
Group:          Development/Libraries
Url:            http://search.cpan.org/dist/Time-Duration/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Buildarch:      noarch
Source:         http://search.cpan.org/CPAN/authors/id/A/AV/AVIF/Time-Duration-%{version}.tar.gz
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(Test::Pod::Coverage) perl(Test::Pod) perl(ExtUtils::MakeMaker)

%description
This module provides functions for expressing durations in rounded or exact
terms.


%prep
%setup -q -n Time-Duration-%{version} 


%check
make test


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth  -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README ChangeLog
%{_mandir}/man3/*
%{perl_vendorlib}/Time


%changelog
* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.06-13
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.06-11
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.06-9
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.06-8
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.06-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jun 29 2008 Marc Bradshaw <fedora@marcbradshaw.co.uk> 1.06-4
- A few bugs fixed in specfile

* Sun Jun 29 2008 Marc Bradshaw <fedora@marcbradshaw.co.uk> 1.06-3
- Rebuild for F9

* Thu Sep 20 2007 Marc Bradshaw <fedora@marcbradshaw.co.uk> 1.06-2
- Tidied build flags

* Wed Sep 19 2007 Marc Bradshaw <fedora@marcbradshaw.co.uk> 1.06-1
- Version update, Licence versions added

* Mon Jul 02 2007 Marc Bradshaw <fedora@marcbradshaw.co.uk> 1.04-4
- Add ChangeLog to docs

* Tue Jun 05 2007 Marc Bradshaw <fedora@marcbradshaw.co.uk> 1.04-3
- Specfile cleanup

* Fri Jun 01 2007 Marc Bradshaw <fedora@marcbradshaw.co.uk> 1.04-2
- Specfile cleanup

* Thu May 24 2007 Marc Bradshaw <fedora@marcbradshaw.co.uk> 1.04-1
- Initial fedora release
