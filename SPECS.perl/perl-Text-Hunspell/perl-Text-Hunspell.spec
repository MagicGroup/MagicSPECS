Name:		perl-Text-Hunspell
Version:	2.11
Release:	5%{?dist}
Summary:	Perl interface to the Hunspell library
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/text_hunspell/
Source0:	http://search.cpan.org/CPAN/authors/id/C/CO/COSIMO/Text-Hunspell-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
# Module Build
BuildRequires:	gcc-c++
BuildRequires:	hunspell-devel >= 1.2.8
BuildRequires:	perl
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.52
BuildRequires:	perl(ExtUtils::PkgConfig)
# Module Runtime
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(vars)
# Test Suite
BuildRequires:	hunspell-en
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod) >= 1.14
BuildRequires:	perl(warnings)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This module provides a Perl interface to the Hunspell library. This module
is to meet the need of looking up many words, one at a time, in a single
session, such as spell-checking a document in memory.

%prep
%setup -q -n Text-Hunspell-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
LANG=en_US make test TEST_POD=1 TEST_VERBOSE=1

%clean
rm -rf %{buildroot}

%files
%doc Changes README examples/
%{perl_vendorarch}/auto/Text/
%{perl_vendorarch}/Text/
%{_mandir}/man3/Text::Hunspell.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.11-5
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 2.11-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.11-2
- Perl 5.22 rebuild

* Wed May 13 2015 Paul Howarth <paul@city-fan.org> - 2.11-1
- Update to 2.11
  - Fix compilation on non-gcc based systems (CPAN RT#99810)
  - Minor clean-ups
  - No functional changes

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.10-2
- Rebuilt for GCC 5 C++11 ABI change

* Thu Mar 26 2015 Paul Howarth <paul@city-fan.org> - 2.10-1
- Update to 2.10
  - Fix ExtUtils::PkgConfig usage in metadata and Makefile.PL
    (http://github.com/cosimo/perl5-text-hunspell/issues/5)

* Mon Oct 20 2014 Paul Howarth <paul@city-fan.org> - 2.09-1
- Update to 2.09
  - Use ExtUtils::PkgConfig to find libhunspell (CPAN RT#99548)
- Classify buildreqs by usage

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.08-6
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.08-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.08-2
- Perl 5.18 rebuild

* Thu May  2 2013 Paul Howarth <paul@city-fan.org> - 2.08-1
- Update to 2.08
  - Improved main POD documentation for Hunspell.pm (CPAN RT#84964)

* Tue Mar 26 2013 Paul Howarth <paul@city-fan.org> - 2.07-1
- Update to 2.07
  - DEPRECATED the delete() method and implemented proper object handles in
    the hunspell XS glue so that multiple speller objects can coexist
    (CPAN RT#84054)

* Sat Mar  9 2013 Paul Howarth <paul@city-fan.org> - 2.06-1
- Update to 2.06
  - Implemented new add_dic() function from hunspell API (CPAN RT#83765)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 21 2012 Paul Howarth <paul@city-fan.org> - 2.05-1
- Update to 2.05 (fix pod encoding - CPAN RT#79630)
- Drop upstreamed pod encoding patch

* Fri Sep 21 2012 Paul Howarth <paul@city-fan.org> - 2.04-1
- Update to 2.04 (specify pod encoding to placate pod test - CPAN RT#79630)
- Add patch to fix pod encoding
- BR: perl(File::Spec)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Paul Howarth <paul@city-fan.org> - 2.03-4
- BR: perl(Data::Dumper)
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Use %%{_fixperms} macro rather than our own chmod incantation

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.03-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Paul Howarth <paul@city-fan.org> - 2.03-1
- Update to 2.03 (fixed use of "qw()" as parenthesis in inc/Devel/CheckLib.pm
  because it's deprecated in perl 5.14)

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.02-5
- Perl mass rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.02-4
- Perl mass rebuild

* Wed May 25 2011 Paul Howarth <paul@city-fan.org> - 2.02-3
- Rebuilt for new hunspell
- Remove remaining use of macros for system commands

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 24 2010 Paul Howarth <paul@city-fan.org> - 2.02-1
- Update to 2.02 (added an explicit warning if the unversioned libhunspell.so
  symlink or library is not found)

* Wed Sep 29 2010 jkeating - 2.01-3
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Paul Howarth <paul@city-fan.org> - 2.01-2
- Sanitize for Fedora submission

* Wed Sep  8 2010 Paul Howarth <paul@city-fan.org> - 2.01-1
- Initial RPM version
