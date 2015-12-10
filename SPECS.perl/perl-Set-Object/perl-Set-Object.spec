Name: perl-Set-Object
Version:	1.35
Release:	3%{?dist}
License: GPL+ or Artistic
Summary: Set of objects and strings
Group: Development/Libraries
URL: http://search.cpan.org/dist/Set-Object/
Source0: http://www.cpan.org/modules/by-module/Set/Set-Object-%{version}.tar.gz
Source1: license.txt
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: perl
BuildRequires: perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires: perl(AutoLoader)
BuildRequires: perl(base)
BuildRequires: perl(Carp)
BuildRequires: perl(DynaLoader)
BuildRequires: perl(Exporter)
BuildRequires: perl(overload)
BuildRequires: perl(Scalar::Util)
BuildRequires: perl(strict)
BuildRequires: perl(vars)
# Tests
BuildRequires: perl(Config)
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(Devel::Peek)
BuildRequires: perl(Test::More)
# Optional tests
BuildRequires: perl(Storable)
BuildRequires: perl(Test::Pod) >= 1.00
BuildRequires: perl(Test::Pod::Coverage)
BuildRequires: perl(threads)
BuildRequires: perl(threads::shared)
BuildRequires: perl(warnings)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: perl(overload)
Requires: perl(Scalar::Util)

%description
This modules implements a set of objects, that is, an unordered
collection of objects without duplication.

The term *objects* is applied loosely - for the sake of Set::Object,
anything that is a reference is considered an object.

%prep
%setup -q -n Set-Object-%{version}
cp %{SOURCE1} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}

# clean up buildroot
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc Changes.pod META.yml README license.txt
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Set*
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.35-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.35-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.35-1
- 更新到 1.35

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 1.31-4
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 1.31-1
- 1.31 bump

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 1.26-15
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.26-12
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.26-10
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.26-8
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.26-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.26-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 9 2008 - Gerd Hoffmann <kraxel@redhat.com> - 1.26-3
- add test suite support.
- simplify files section.
- pick up some bits from cpanspec-generated specfile.

* Thu Nov 27 2008 - Gerd Hoffmann <kraxel@redhat.com> - 1.26-2
- include text file documenting the relicensing.

* Tue Nov 11 2008 - Gerd Hoffmann <kraxel@redhat.com> - 1.26-1
- update to version 1.26

* Tue Nov 11 2008 - Gerd Hoffmann <kraxel@redhat.com> - 1.25-3
- update license tag.

* Wed Oct 15 2008 - Gerd Hoffmann <kraxel@redhat.com> - 1.25-2
- add dist tag to release.
- fix rpmlint errors and warnings.

* Wed Aug 13 2008 - Patrick Steiner <patrick.steiner@a1.net> - 1.25-1
- update to 1.25

* Wed Aug 13 2008 - Patrick Steiner <patrick.steiner@a1.net> - 1.22-2
- Upadted to Fedora 9

* Sun Nov 18 2007 Dag Wieers <dag@wieers.com> - 1.22-1
- Updated to release 1.22.

* Mon Sep 18 2006 Dries Verachtert <dries@ulyssis.org> - 1.18-1
- Updated to release 1.18.

* Sat Nov  5 2005 Dries Verachtert <dries@ulyssis.org> - 1.14-1
- Updated to release 1.14.

* Sat Apr  9 2005 Dries Verachtert <dries@ulyssis.org> - 1.10-1
- Initial package.
