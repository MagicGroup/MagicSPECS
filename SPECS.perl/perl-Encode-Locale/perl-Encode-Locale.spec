Name:           perl-Encode-Locale
Version:	1.05
Release:	1%{?dist}
Summary:        Determine the locale encoding
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Encode-Locale/
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/Encode-Locale-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(Encode) >= 2
BuildRequires:  perl(Encode::Alias)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
# Tests only:
BuildRequires:  perl(Test)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Multiline our @EXPORT_OK = qw( ... ) trips perl dep extractor
Requires:       perl(Encode) >= 2
Requires:       perl(Encode::Alias)
# Recommended:
Requires:       perl(I18N::Langinfo)

%description
In many applications it's wise to let Perl use Unicode for the strings
it processes.  Most of the interfaces Perl has to the outside world is
still byte based.  Programs therefore needs to decode byte strings
that enter the program from the outside and encode them again on the
way out.

%prep
%setup -q -n Encode-Locale-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check


%files
%doc Changes README
%{perl_vendorlib}/Encode/
%{_mandir}/man3/Encode::Locale.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.05-1
- 更新到 1.05

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.03-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.03-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.03-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.03-2
- Perl 5.16 rebuild

* Mon Feb 13 2012 Petr Pisar <ppisar@redhat.com> - 1.03-1
- 1.03 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 27 2011 Petr Pisar <ppisar@redhat.com> - 1.02-4
- BuildRequire perl(base)

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.02-3
- Perl mass rebuild

* Thu May 26 2011 Petr Pisar <ppisar@redhat.com> - 1.02-2
- Remove explicit defattr

* Thu May 26 2011 Petr Pisar <ppisar@redhat.com> - 1.02-1
- 1.02 bump

* Wed Mar 16 2011 Petr Pisar <ppisar@redhat.com> - 1.01-1
- Spec file provided by Ville Skyttä
- BuildRoot stuff removed
- Dependencies adjusted
