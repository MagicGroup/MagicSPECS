Name:           perl-HTTP-Headers-Fast
Version:        0.19
Release:        3%{?dist}
Summary:        Faster implementation of HTTP::Headers
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/HTTP-Headers-Fast/
Source0:        http://www.cpan.org/authors/id/T/TO/TOKUHIROM/HTTP-Headers-Fast-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Build) >= 0.38
BuildRequires:  perl(strict)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(HTTP::Date)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Storable)
# Tests
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(URI)
# Optional tests:
BuildRequires:  perl(HTTP::Headers) >= 5.822
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(HTTP::Date)
Requires:       perl(MIME::Base64)
Requires:       perl(Storable)

%description
HTTP::Headers::Fast is a perl class for parsing/writing HTTP headers.

%prep
%setup -q -n HTTP-Headers-Fast-%{version}

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes README.md
%license LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.19-3
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 0.19-2
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Petr Pisar <ppisar@redhat.com> - 0.19-1
- Packaging correction (bug #1230227)
- 0.19 bump

* Mon Jun 08 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.17-1
- Initial package.
