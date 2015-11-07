%global libname Math-Calc-Units
Name:           perl-%{libname}
Version:        1.07
Release:        10%{?dist}
Summary:        Human-readable unit-aware calculator
License:        GPLv2+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/%{libname}/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SF/SFINK/%{libname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Math::Calc::Units is a simple calculator that keeps track of units. It
currently handles combinations of byte sizes and duration only, although
adding any other multiplicative types is easy. Any unknown type is treated
as a unique user type (with some effort to map English plurals to their
singular forms).

%prep
%setup -q -n %{libname}-%{version}

# filter unwanted Provides
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
sed -e '/perl(Parse::Yapp::Driver)/d'
EOF

%global __perl_provides %{_builddir}/%{libname}-%{version}/%{name}-prov
chmod +x %{__perl_provides}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
rm -vf %{buildroot}%{perl_vendorlib}/Math/Calc/Units/Grammar.y


%{_fixperms} %{buildroot}/*

%check


%files
%defattr(-,root,root,-)
%doc Artistic.html Changes COPYING LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*
%{_bindir}/ucalc

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.07-10
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.07-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.07-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.07-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.07-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.07-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.07-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Jun 24 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.07-1
- Upstream released new version

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.06-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.06-3
- rebuild against perl 5.10.1

* Wed Jul 29 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.06-2
- Review fixes (#513874)

* Sun Jul 26 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> - 1.06-1
- Initial import
