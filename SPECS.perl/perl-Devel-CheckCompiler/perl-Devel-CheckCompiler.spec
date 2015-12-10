Name:		perl-Devel-CheckCompiler
Version:	0.06
Release:	4%{?dist}
Summary:	Check the compiler's availability
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Devel-CheckCompiler/
Source0:	http://search.cpan.org/CPAN/authors/id/S/SY/SYOHEX/Devel-CheckCompiler-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	perl
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Module::Build)
# Module Runtime
BuildRequires:	perl(Config)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::CBuilder)
BuildRequires:	perl(parent)
BuildRequires:	perl(strict)
BuildRequires:	perl(utf8)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Test::More) >= 0.96
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(File::Temp)

%description
Devel::CheckCompiler is checker for compiler's availability.

%prep
%setup -q -n Devel-CheckCompiler-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0

%check
./Build test

%files
%license LICENSE
%doc Changes README.md
%{perl_vendorlib}/Devel/
%{_mandir}/man3/Devel::AssertC99.3*
%{_mandir}/man3/Devel::CheckCompiler.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.06-4
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.06-3
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.06-2
- 为 Magic 3.0 重建

* Tue Jun 30 2015 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06
  - More strict C99 check code
  - Fix for older GCC(< 5.0)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-3
- Perl 5.22 rebuild

* Tue Oct  7 2014 Paul Howarth <paul@city-fan.org> - 0.05-2
- Sanitize for Fedora submission

* Sat Oct  4 2014 Paul Howarth <paul@city-fan.org> - 0.05-1
- Initial RPM version
