Name:           perl-Test-Dist-VersionSync
Version:	v1.1.4
Release:	3%{?dist}
Summary:        Verify that all the modules in a distribution have the same version number
License:        GPLv3
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-Dist-VersionSync/
Source0:        http://www.cpan.org/authors/id/A/AU/AUBERTG/Test-Dist-VersionSync-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
The Test-Dist-VersionSync gives perl developers an easy way to verify that all
the modules in a distribution have the same version number.

%prep
%setup -q -n Test-Dist-VersionSync-%{version}

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
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - v1.1.4-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - v1.1.4-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - v1.1.4-1
- 更新到 v1.1.4

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.1.0-8
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.1.0-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.1.0-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.1.0-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.1.0-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.1.0-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.1.0-2
- 为 Magic 3.0 重建

* Mon Sep 24 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> 1.1.0-1
- Specfile autogenerated by cpanspec 1.78.
