Name:           perl-MooX-late
Version:	0.015
Release:	1%{?dist}
Summary:        Easily translate Moose code to Moo
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/MooX-late/
Source0:        http://www.cpan.org/authors/id/T/TO/TOBYINK/MooX-late-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl >= 1:5.8.0
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Module::Runtime)
BuildRequires:  perl(Moo) >= 1.003000
BuildRequires:  perl(Moo::Role)
BuildRequires:  perl(MooX)
BuildRequires:  perl(MooX::HandlesVia) >= 0.001004
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Fatal) >= 0.010
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Requires) >= 0.06
BuildRequires:  perl(Type::Utils) >= 0.016
BuildRequires:  perl(Types::Standard)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

# Indirect BR:s from inc/*
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(vars)
BuildRequires:  perl(Cwd)

Requires:       perl(Moo) >= 1.003000
Requires:       perl(MooX::HandlesVia) >= 0.001004
Requires:       perl(Type::Utils) >= 0.016
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Filter under-specified requires
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Moo\\)$

%description
Moo is a light-weight object oriented programming framework which aims to
be compatible with Moose. It does this by detecting when Moose has been
loaded, and automatically "inflating" its classes and roles to full Moose
classes and roles. This way, Moo classes can consume Moose roles, Moose
classes can extend Moo classes, and so forth.

%prep
%setup -q -n MooX-late-%{version}

%build
# --skipdeps causes ExtUtils::AutoInstall not to try auto-installing
%{__perl} Makefile.PL INSTALLDIRS=vendor --skipdeps
make %{?_smp_mflags}

%install
make pure_install DESTDIR="$RPM_BUILD_ROOT"

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.015-1
- 更新到 0.015

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.014-5
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.014-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 01 2014 Ralf Corsépius <corsepiu@fedoraproject.org> 0.014-3
- Add more unnecessary BR:-dependency bloat.

* Mon Mar 31 2014 Ralf Corsépius <corsepiu@fedoraproject.org> 0.014-2
- Reflect review.

* Sat Mar 22 2014 Ralf Corsépius <corsepiu@fedoraproject.org> 0.014-1
- Initial fedora package.
