# We need to patch the test suite if we have an old version of Test::More
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.88) ? 1 : 0);' 2>/dev/null || echo 0)

Name:		perl-Data-Section-Simple
Version:	0.03
Release:	5%{?dist}
Summary:	Read data from __DATA__
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Data-Section-Simple/
Source0:	http://search.cpan.org/CPAN/authors/id/M/MI/MIYAGAWA/Data-Section-Simple-%{version}.tar.gz
Patch1:		Data-Section-Simple-0.02-old-Test::More.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod) >= 1.00
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Data::Section::Simple is a simple module to extract data from the __DATA__
section of the file.

%prep
%setup -q -n Data-Section-Simple-%{version}

# Hack for old Test::More versions
%if %{old_test_more}
%patch1 -p1
%endif

%build
# Note that the Makefile.PL complains about missing Test::Requires
# but the package doesn't actually use it (CPAN RT#69981)
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \; 2>/dev/null
%{_fixperms} %{buildroot}

%check

 TEST_FILES="xt/*.t"

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/Data/
%{_mandir}/man3/Data::Section::Simple.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.03-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.03-3
- Perl 5.16 rebuild

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 0.03-2
- Fedora 17 mass rebuild

* Mon Sep 19 2011 Paul Howarth <paul@city-fan.org> - 0.03-1
- Update to 0.03
  - Noted the use of utf8 pragma
  - Doc typo fixes (Util)

* Thu Aug  4 2011 Paul Howarth <paul@city-fan.org> - 0.02-2
- Sanitize for Fedora submission

* Wed Aug  3 2011 Paul Howarth <paul@city-fan.org> - 0.02-1
- Initial RPM version
