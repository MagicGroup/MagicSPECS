Name:       perl-Data-TreeDumper 
Version:    0.40 
Release:    14%{?dist}
# see TreeDumper.pm
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Improved replacement for Data::Dumper
Source:     http://search.cpan.org/CPAN/authors/id/N/NK/NKH/Data-TreeDumper-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/Data-TreeDumper
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker) 
BuildRequires: perl(Check::ISA)
BuildRequires: perl(Class::ISA)
BuildRequires: perl(Devel::Size) >= 0.58
BuildRequires: perl(Sort::Naturally)
BuildRequires: perl(Term::Size) >= 0.2
BuildRequires: perl(Text::Wrap) >= 2001.0929

# not automagically picked up
Requires: perl(Term::Size) >= 0.2

%description
Data::Dumper and other modules do a great job of dumping data structures.
Their output, however, often takes more brain power to understand than the
data itself.  When dumping large amounts of data, the output can be 
overwhelming and it can be difficult to see the relationship between each 
piece of the dumped data.

Data::TreeDumper also dumps data in a tree-like fashion but hopefully in a
format more easily understood.

%prep
%setup -q -n Data-TreeDumper-%{version}

# F-11 appears to be more sensitive to bits in _docdir.  grr. see RHBZ#473874
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} `perl -p -e 's|\S+%{_docdir}/%{name}-%{version}\S+||'`
EOF

%define __perl_provides %{_builddir}/Data-TreeDumper-%{version}/%{name}-prov
chmod +x %{__perl_provides}

cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} `perl -p -e 's|\S+%{_docdir}/%{name}-%{version}\S+||'`
EOF

%define __perl_requires %{_builddir}/Data-TreeDumper-%{version}/%{name}-req
chmod +x %{__perl_requires}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

# hrm.
find %{buildroot} -name '*.pl' -exec rm -v {} +

%check
make test

%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc README Changes Todo *.pl
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.40-14
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.40-13
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.40-12
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.40-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.40-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.40-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.40-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.40-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.40-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.40-5
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.40-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.40-2
- Perl 5.16 rebuild

* Fri Jan 27 2012 Marcela Maslanova <mmaslano@redhat.com> - 0.40-1
- update to 0.40

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.35-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.35-8
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.35-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.35-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.35-3
- manually require Term::Size

* Thu Dec 04 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.35-2
- filter requires as well.  See RHBZ#473874

* Wed Nov 19 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.35-1
- update for submission

* Wed Nov 19 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.35-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)

