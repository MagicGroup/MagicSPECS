Name:           perl-URL-Encode-XS
Version:        0.03
Release:        5%{?dist}
Summary:        XS implementation of URL::Encode
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/URL-Encode-XS/
Source0:        http://www.cpan.org/authors/id/C/CH/CHANSEN/URL-Encode-XS-%{version}.tar.gz
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::MM_Unix)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(warnings)
Requires:       perl(Exporter)
Requires:       perl(XSLoader)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This package implements the original URL::Encode via XS interface. The main
URL::Encode package will use this package automatically if it can find it. 
Do not use this package directly, use URL::Encode instead.

%prep
%setup -qn URL-Encode-XS-%{version}
chmod -c -x dev/*

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -delete -print

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README dev
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/URL*
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.03-5
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 0.03-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.03-2
- Perl 5.22 rebuild

* Mon Jan 12 2015 David Dick <ddick@cpan.org> - 0.03-1
- Initial Package.
