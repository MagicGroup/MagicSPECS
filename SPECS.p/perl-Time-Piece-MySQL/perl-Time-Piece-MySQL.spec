Name:           perl-Time-Piece-MySQL
Version:        0.05
Release:        17%{?dist}
Summary:        MySQL-specific methods for Time::Piece

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Time-Piece-MySQL/
Source0:        http://search.cpan.org/CPAN/authors/id/K/KA/KASEI/Time-Piece-MySQL-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Time::Piece) >= 1.03
BuildRequires:  perl(Test::More) >= 0.47
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:  perl(Time::Piece) >= 1.03

%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Time::Piece\\)

%description
The Time::Piece::MySQL module can be used instead of, or in addition to,
Time::Piece to add MySQL-specific date-time methods to Time::Piece objects.


%prep
%setup -q -n Time-Piece-MySQL-%{version}

# Filter unwanted Provides:
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
    sed -e '/perl(Time::Piece)/d'
EOF

%define __perl_provides %{_builddir}/Time-Piece-MySQL-%{version}/%{name}-prov
chmod +x %{__perl_provides}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/Time/
%{_mandir}/man3/*.3*


%changelog
* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 0.05-16
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 15 2011 Petr Pisar <ppisar@redhat.com> - 0.05-14
- Do not provide private perl(Time::Piece) (bug #247253)

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.05-13
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-11
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-10
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.05-9
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.05-6
- Rebuild for perl 5.10 (again)

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.05-5
- rebuild for new perl
- fix license tag

* Fri Aug  3 2007 Chris Grau <chris@chrisgrau.com> 0.05-4
- Remove generation of license texts.
- Prevent automatic provide of perl(Time::Piece) (#247253).

* Thu Sep 14 2006 Chris Grau <chris@chrisgrau.com> 0.05-3
- Rebuild for FC-6.

* Wed Aug 24 2005 Chris Grau <chris@chrisgrau.com> 0.05-2
- Removed redundant perl BR.
- Added license texts.
- Fixed directory ownership (perl-Time-Piece doesn't really own those dirs).

* Tue Aug 23 2005 Chris Grau <chris@chrisgrau.com> 0.05-1
- Initial build.
