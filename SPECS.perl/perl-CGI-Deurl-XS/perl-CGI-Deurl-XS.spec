Name:           perl-CGI-Deurl-XS
Version:        0.08
Release:        5%{?dist}
Summary:        Fast decoder for URL parameter strings
License:        (GPL+ or Artistic) and ASL 2.0
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/CGI-Deurl-XS/
Source0:        http://www.cpan.org/modules/by-module/CGI/CGI-Deurl-XS-%{version}.tar.gz
BuildRequires:  perl
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::Constant)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module decodes a URL-encoded parameter string in the manner of CGI.pm.
However, as it uses C code from libapreq to perform the task, it's
somewhere from slightly to much faster (depending on your strings) than
using CGI or a functionally similar module like CGI::Deurl.

%prep
%setup -q -n CGI-Deurl-XS-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/CGI*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.08-5
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 0.08-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-2
- Perl 5.22 rebuild

* Mon May 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-1
- 0.08 bump

* Fri Oct 03 2014 David Dick <ddick@cpan.org> - 0.07-1
- Initial release
