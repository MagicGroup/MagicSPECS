Name:           perl-Apache-LogFormat-Compiler
Version:        0.32
Release:        4%{?dist}
Summary:        Compile a log format string to perl-code
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Apache-LogFormat-Compiler/
Source0:        http://www.cpan.org/authors/id/K/KA/KAZEBURO/Apache-LogFormat-Compiler-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl >= 0:5.008001
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(CPAN::Meta::Prereqs)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(HTTP::Request::Common)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(POSIX::strftime::Compiler)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::MockTime)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(Try::Tiny) >= 0.12
BuildRequires:  perl(URI::Escape) >= 1.60
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Compile a log format string to perl-code. For faster generation of
access_log lines.

%prep
%setup -q -n Apache-LogFormat-Compiler-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install

./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-3
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-2
- Perl 5.20 rebuild

* Tue Jun 24 2014 Ralf Corsépius <corsepiu@fedoraproject.org> 0.32-1
- Upstream update.
- Reflect upstream having lowered the required perl version.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Petr Pisar <ppisar@redhat.com> - 0.30-2
- Drop unneeded build-time dependencies

* Thu Apr 17 2014 Ralf Corsépius <corsepiu@fedoraproject.org> 0.30-1
- Upstream update.
- Reflect upstream R:/BR: changes.

* Fri Jan 17 2014 Ralf Corsépius <corsepiu@fedoraproject.org> 0.23-1
- Upstream update.
- Reflect upstream R:/BR: changes.

* Mon Sep 16 2013 Ralf Corsépius <corsepiu@fedoraproject.org> 0.13-1
- Initial fedora package.
