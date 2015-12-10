Name:           perl-Sentinel
Version:        0.05
Release:        8%{?dist}
Summary:        Create lightweight SCALARs with get/set callbacks
License:        GPL+ or Artistic

URL:            http://search.cpan.org/dist/Sentinel/
Source0:        http://www.cpan.org/authors/id/P/PE/PEVANS/Sentinel-%{version}.tar.gz

BuildRequires:  perl
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Refcount)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(XSLoader)

%{?perl_default_filter}

%description
This module provides a single lvalue function, sentinel, which yields a
scalar that invoke callbacks to get or set its value. Primarily this is
useful to create lvalue object accessors or other functions, to invoke
actual code when a new value is set, rather than simply updating a
scalar variable.

%prep
%setup -q -n Sentinel-%{version}

%build
%{__perl} Build.PL installdirs=vendor optimize="$RPM_OPT_FLAGS"
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;

%{_fixperms} $RPM_BUILD_ROOT/*


%check
./Build test

%files
%doc Changes README
%license LICENSE
%{perl_vendorarch}/auto/Sentinel
%{perl_vendorarch}/Sentinel*
%{_mandir}/man3/Sentinel*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.05-8
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.05-7
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 0.05-6
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-4
- Perl 5.22 rebuild

* Mon Sep 08 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-3
- Perl 5.20 mass

* Sun Sep 07 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 0.05-2
- Take into account review comments (#1139007)

* Wed Sep 03 2014 Emmanuel Seyman <emmanuel@seyman.fr> 0.05-1
- Specfile autogenerated by cpanspec 1.78.
