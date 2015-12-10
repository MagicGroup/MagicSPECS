%define base Text-Aspell

Name:		perl-%{base}
Version:	0.09
Release:	25%{?dist}
Summary:	Perl interface to the GNU Aspell library
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/%{base}/
Source0:	http://search.cpan.org/CPAN/authors/id/H/HA/HANK/%{base}-%{version}.tar.gz
BuildRequires:	aspell-devel >= 0.50.1,
BuildRequires:  aspell-en
BuildRequires:	perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires:  perl(DynaLoader)
# Tests
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test::More)
# Optional tests
BuildRequires:  perl(Test::Pod) >= 1.14
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	aspell >= 0.50.1

%{?perl_default_filter}

%description
This module provides a Perl interface to the GNU Aspell library.  This
module is to meet the need of looking up many words, one at a time, in a
single session, such as spell-checking a document in memory.

%prep
%setup -q -n %{base}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check
make test TEST_POD=t

%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Text
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.09-25
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.09-24
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.09-23
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-21
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-20
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.09-16
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.09-13
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct  4 2011 Tom Callaway <spot@fedoraproject.org> - 0.09-11
- add perl_default_filter

* Sun Oct  2 2011 Tom Callaway <spot@fedoraproject.org> - 0.09-10
- revive package

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09-8
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09-7
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.09-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.09-3
Rebuild for new perl

* Wed Feb 13 2008 Jerry James <loganjerry@gmail.com> - 0.09-2
- Rebuild for gcc 4.3

* Fri Oct 12 2007 Jerry James <loganjerry@gmail.com> - 0.09-1
- Update to 0.09
- Clarify license

* Mon Jul 16 2007 Jerry James <Jerry.James@usu.edu> - 0.08-1
- Update to 0.08

* Mon Apr 16 2007 Jerry James <Jerry.James@usu.edu> - 0.07-2
- Fix BuildRequires to match Fedora conventions

* Tue Apr 10 2007 Jerry James <Jerry.James@usu.edu> - 0.07-1
- Initial RPM
