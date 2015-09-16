#TODO: BR: Test::Pod::No404s when available
#TODO: BR: Test::Pod::LinkCheck when available

Name:		perl-Class-Load-XS
Version:	0.09
Release:	1%{?dist}
Summary:	XS implementation of parts of Class::Load
Group:		Development/Libraries
License:	Artistic 2.0
URL:		http://search.cpan.org/dist/Class-Load-XS/
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Class-Load-XS-%{version}.tar.gz
# ===================================================================
# Module build requirements
# ===================================================================
BuildRequires:	perl(Module::Build)
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:	perl(Class::Load) >= 0.20
# ===================================================================
# Regular test suite requirements
# ===================================================================
BuildRequires:	perl(constant)
BuildRequires:	perl(Module::Implementation) >= 0.04
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Requires)
BuildRequires:	perl(Test::Without::Module)
BuildRequires:	perl(version)
# ===================================================================
# Author/Release test requirements
# ===================================================================
BuildRequires:	perl(Test::CPAN::Changes)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Pod)
# ===================================================================
# Runtime requirements
# ===================================================================
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module provides an XS implementation for portions of Class::Load.
See Class::Load for API details.
%prep
%setup -q -n Class-Load-XS-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%{perl_vendorarch}/auto/Class/
%{perl_vendorarch}/Class/
%{_mandir}/man3/Class::Load::XS.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.09-1
- 更新到 0.09

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.06-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.06-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-4
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.06-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.06-2
- 为 Magic 3.0 重建

* Mon Oct  8 2012 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06:
  - Require Class::Load 0.20 in the code, not just the distro metadata
    (CPAN RT#80002)
  - Weird classes with either an ISA or VERSION constant would cause the XS to
    blow up badly (CPAN RT#79998)
  - Fixed some broken logic that lead to a segfault from the
    014-weird-constants.t test on some Perls (CPAN RT#80059)
- Bump perl(Class::Load) version requirement to 0.20
- Drop explicit requirement for perl(Class::Load), no longer needed

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.04-2
- Perl 5.16 rebuild

* Thu Feb  9 2012 Paul Howarth <paul@city-fan.org> - 0.04-1
- Update to 0.04:
  - Some small test changes for the latest Module::Implementation and
    Class::Load
- Bump Class::Load version requirement to 0.15
- BR: perl(constant), perl(Module::Implementation) ≥ 0.04, 
  perl(Test::Requires), perl(Test::Without::Module) and perl(version) for test 
  suite

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 0.03-2
- Rebuild for gcc 4.7 in Rawhide

* Fri Nov 18 2011 Paul Howarth <paul@city-fan.org> - 0.03-1
- Update to 0.03:
  - Explicitly include Test::Fatal as a test prerequisite (CPAN RT#72493)

* Wed Nov 16 2011 Paul Howarth <paul@city-fan.org> - 0.02-2
- Sanitize spec for Fedora submission

* Wed Nov 16 2011 Paul Howarth <paul@city-fan.org> - 0.02-1
- Initial RPM version
