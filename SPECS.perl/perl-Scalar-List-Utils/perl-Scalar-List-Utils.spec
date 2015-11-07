Name:           perl-Scalar-List-Utils
Version:	1.42
Release:	6%{?dist}
Summary:        A selection of general-utility scalar and list subroutines
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Scalar-List-Utils/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PEVANS/Scalar-List-Utils-%{version}.tar.gz
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
BuildRequires:  perl(Tie::Handle)
BuildRequires:  perl(Tie::Scalar)
BuildRequires:  perl(Tie::StdScalar)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Carp)

%{?perl_default_filter}

%description
This package contains a selection of subroutines that people have expressed
would be nice to have in the perl core, but the usage would not really be
high enough to warrant the use of a keyword, and the size so small such
that being individual extensions would be wasteful.

%prep
%setup -q -n Scalar-List-Utils-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/List*
%{perl_vendorarch}/Scalar*
%{perl_vendorarch}/Sub/Util.pm
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.42-6
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.42-5
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.42-4
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.42-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.42-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.42-1
- 更新到 1.42

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.38-4
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.38-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 26 2014 Paul Howarth <paul@city-fan.org> - 1.38-1
- Update to 1.38
  - Skip pairmap()'s MULTICALL implementation 5.8.9/5.10.0 as it doesn't work
    (CPAN RT#87857)
  - Comment on the fact that package "0" is defined but false (CPAN RT#88201)
  - TODO test in t/readonly.t now passes since 5.19.3 (CPAN RT#88223)
  - Added any, all, none, notall list reduction functions (inspired by
    List::MoreUtils)
  - Added List::Util::product()
  - Added Scalar::Util::unweaken()
  - Avoid C99/C++-style comments in XS code
  - Fix dualvar tests for perl 5.6; fix skip() test counts in dualvar.t
  - Neater documentation examples of other functions that can be built using
    reduce
  - Implement reduce() and first() even in the absence of MULTICALL
  - Various documentation changes/updates
  - Correct uses of overload operators in unit tests (CPAN RT#91969)

* Fri Aug 16 2013 Iain Arnell <iarnell@gmail.com> 1.31-293
- update to latest upstream version

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-292
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 1.27-291
- Specify all dependencies

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1.27-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1.27-247
- Link minimal build-root packages against libperl.so explicitly

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-246
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Iain Arnell <iarnell@gmail.com> 1.27-245
- update to latest upstream version

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 1.25-240
- Increase release to replace perl sub-package (bug #848961)

* Thu Aug 16 2012 Petr Pisar <ppisar@redhat.com> - 1.25-4
- Correct dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1.25-2
- Perl 5.16 rebuild

* Sun Mar 25 2012 Iain Arnell <iarnell@gmail.com> 1.25-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.23-2
- Perl mass rebuild

* Mon Feb 21 2011 Iain Arnell <iarnell@gmail.com> 1.23-1
- Specfile autogenerated by cpanspec 1.79.
