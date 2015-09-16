Summary:	Pure-perl Lanman and NT MD4 hash functions
Name:		perl-Crypt-SmbHash
Version:	0.12
Release:	30%{?dist}
License:	GPLv2+
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Crypt-SmbHash/
Source0:	http://search.cpan.org/CPAN/authors/id/B/BJ/BJKUIT/Crypt-SmbHash-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Digest::MD4)
BuildRequires:	perl(ExtUtils::MakeMaker)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Digest::MD4)

%description
This module generates Lanman and NT MD4 style password hashes, using perl-only
code for portability. The module aids in the administration of Samba style
systems.

%prep
%setup -q -n Crypt-SmbHash-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/Crypt/
%{_mandir}/man3/Crypt::SmbHash.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.12-30
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.12-29
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.12-28
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.12-27
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.12-26
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.12-25
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.12-24
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.12-23
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.12-22
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.12-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.12-20
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.12-19
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.12-18
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.12-17
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> 0.12-16
- Nobody else likes macros for commands
- BR: perl(Carp)

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> 0.12-15
- Perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.12-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> 0.12-13
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> 0.12-12
- Mass rebuild with perl 5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> 0.12-11
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.12-8
- Rebuild for new perl

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.12-7
- Rebuild for new perl

* Sun Aug 12 2007 Paul Howarth <paul@city-fan.org> 0.12-6
- Clarify license as GPL version 2 or later

* Thu Mar  8 2007 Paul Howarth <paul@city-fan.org> 0.12-5
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 0.12-4
- FE6 mass rebuild

* Thu Feb 16 2006 Paul Howarth <paul@city-fan.org> 0.12-3
- Rebuild for perl 5.8.8 (FC5)

* Wed Jan 25 2006 Paul Howarth <paul@city-fan.org> 0.12-2
- Added buildreq perl(Digest::MD4) to ensure that the test suite runs in the
  same environment as the installed package will do (i.e. with the optional
  Digest::MD4 module installed)

* Tue Jan 17 2006 Paul Howarth <paul@city-fan.org> 0.12-1
- Initial build
