%global cpan_version 2.14

Summary: XS Blowfish implementation for Perl
Name: perl-Crypt-Blowfish
Version:	2.14
Release:	3%{?dist}
License: Copyright only
Group: Development/Libraries
URL: http://search.cpan.org/dist/Crypt-Blowfish/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DP/DPARIS/Crypt-Blowfish-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Recommended:
Requires: perl(Crypt::CBC)
BuildRequires: perl
BuildRequires: perl(ExtUtils::MakeMaker)
# Runt-time:
BuildRequires: perl(Carp)
BuildRequires: perl(DynaLoader)
BuildRequires: perl(Exporter)
BuildRequires: perl(strict)
BuildRequires: perl(vars)
# Tests:
BuildRequires: perl(Benchmark)
# Optional tests:
BuildRequires: perl(Crypt::CBC) >= 1.22

%description
Crypt::Blowfish is an XS-based implementation of the Blowfish
cryptography algorithm designed by Bruce Schneier. It's designed to
take full advantage of Crypt::CBC when desired. Blowfish keys may be
up to 448 bits (56 bytes) long.

%prep
%setup -q -n Crypt-Blowfish-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYRIGHT Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Crypt/
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.14-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.14-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.14-1
- 更新到 2.14

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.12.001-4
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Petr Pisar <ppisar@redhat.com> - 2.12.001-1
- 2.12_001 bump

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.10-18
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.10-15
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.10-13
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.10-11
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.10-10
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.10-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10-6
- rebuild for new perl (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.10-5
- Autorebuild for GCC 4.3

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10-4
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10-3.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 2.10-3
- FE6 Rebuild

* Thu Apr 27 2006 Andreas Thienemann <andreas@bawue.net> - 2.10-1
- Updated to 2.10

* Thu Jul 14 2005 Andreas Thienemann <andreas@bawue.net> - 2.09-2
- Fixed find line to not shellexpand.

* Thu Jul 14 2005 Andreas Thienemann <andreas@bawue.net> - 2.09-1
- Initial package

