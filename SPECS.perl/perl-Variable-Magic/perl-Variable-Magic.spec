Name:           perl-Variable-Magic
Version:	0.59
Release:	2%{?dist}
Summary:        Associate user-defined magic to variables from Perl
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Variable-Magic/
Source0:        http://search.cpan.org/CPAN/authors/id/V/VP/VPIT/Variable-Magic-%{version}.tar.gz
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(Test::Portability::Files)
%if ! 0%{?rhel} >= 7
BuildRequires:  perl(Test::Kwalitee)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Magic is Perl way of enhancing objects. This mechanism let the user add
extra data to any variable and hook syntaxical operations (such as access,
assignation or destruction) that can be applied to it. With this module,
you can add your own magic to any variable without the pain of the C API.

%prep
%setup -q -n Variable-Magic-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Variable*
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.59-2
- 更新到 0.59

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.58-1
- 更新到 0.58

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.51-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.51-2
- 为 Magic 3.0 重建

* Sun Aug 19 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.51-1
- Update to 0.51

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 0.50-2
- Perl 5.16 rebuild

* Tue Jun 26 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.50-1
- Update to 0.50

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.49-2
- Perl 5.16 rebuild

* Sat Jun 09 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.49-1
- Update to 0.49

* Tue Apr 24 2012 Petr Pisar <ppisar@redhat.com> - 0.48-2
- Do not use Test::Kwalitee on RHEL >= 7 (#815750)

* Sat Feb 18 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.48-1
- Update to 0.48

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 30 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.47-1
- Update to 0.47
- Clean up spec file

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.46-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.46-1
- Update to 0.46

* Mon Nov 22 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.45-1
- Update to 0.45

* Wed Sep 29 2010 jkeating - 0.44-2
- Rebuilt for gcc bug 634757

* Fri Sep 25 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.44-1
- Update to 0.44.

* Sun Jun 26 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.43-1
- Update to 0.43.

* Wed May 19 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.42-1
- Update to 0.42.

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.41-2
- Mass rebuild with perl-5.12.0

* Sun Apr 11 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.41-1
- Update to 0.41

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.37-2
- rebuild against perl 5.10.1

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.37-1
- auto-update to 0.37 (by cpan-spec-update 0.01)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 16 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.34-1
- update to 0.34 (for B::Hooks::EndOfScope 0.08)
- filter private Perl .so's

* Mon Mar  9 2009 Allisson Azevedo <allisson@gmail.com> - 0.32-1
- Update to 0.32

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Allisson Azevedo <allisson@gmail.com> 0.30-1
- Initial rpm release.
