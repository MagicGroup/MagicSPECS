Name:           perl-POE-Filter-IRCD
Version:	2.44
Release:	2%{?dist}
Summary:        A POE-based parser for the IRC protocol

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/POE-Filter-IRCD
Source0: http://search.cpan.org/CPAN/authors/id/B/BI/BINGOS/POE-Filter-IRCD-%{version}.tar.gz

Source100:      README.licensing

BuildArch:      noarch

BuildRequires:  perl(POE) >= 0.3202
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)

Requires:  perl(POE::Filter)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

### auto-added brs!
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(POE::Filter)
BuildRequires:  perl(Test::More) >= 0.47

BuildRequires:  /usr/bin/iconv

%description
POE::Filter::IRCD provides a convenient way of parsing and creating IRC
protocol lines.


%prep
%setup -q -n POE-Filter-IRCD-%{version}

iconv -f iso8859-2 -t utf8 < Changes > Changes.1
mv Changes.1 Changes

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

cp %{SOURCE100} .

%check



%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc Changes README*
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.44-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.44-1
- 更新到 2.44

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.42-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.42-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.42-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 2.42-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.42-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov  4 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.42-1
- update because of POE::Comoponent::IRC

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.40-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.40-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 21 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.40-1
- auto-update to 2.40 (by cpan-spec-update 0.01)
- added a new br on perl(ExtUtils::MakeMaker) (version 6.42)
- added a new br on perl(POE::Filter) (version 0)
- altered br on perl(POE) (0 => 0.3202)
- added a new br on perl(Test::More) (version 0.47)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.2-2
- rebuild for new perl

* Tue Dec 05 2006 Chris Weyl <cweyl@alumni.drew.edu> 2.2-1
- update to 2.2

* Sun Sep 17 2006 Chris Weyl <cweyl@alumni.drew.edu> 2.1-1
- update to 2.1

* Wed Sep 13 2006 Chris Weyl <cweyl@alumni.drew.edu> 2.0-1
- update to 2.0

* Mon Sep 04 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.9-1
- update to 1.9
- Add additional BR's 1.9 requires: Test::Pod::Coverage, Test::Pod

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.8-2
- bump for mass rebuild

* Thu Jul 27 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.8-1
- update to 1.8

* Tue Jul 18 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.7-1
- Update for first F-E build

* Tue Jul 18 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.7-0.1
- Added licensing statement/clarification

* Thu Jul 13 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.7-0
- Initial spec file for F-E
