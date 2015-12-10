Name:           perl-CGI-FormBuilder
%global         cpanversion 3.09
Version:        %{cpanversion}00
Release:        4%{?dist}
Summary:        Easily generate and process stateful forms

License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/CGI-FormBuilder/
Source0:        http://search.cpan.org/CPAN/authors/id/N/NW/NWIGER/CGI-FormBuilder-%{cpanversion}.tgz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(CGI::Session)
BuildRequires:  perl(CGI::FastTemplate)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(HTML::Template)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Template)
BuildRequires:  perl(Test)
BuildRequires:  perl(Text::Template)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  sed
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%if 0%{?el6}
%filter_from_requires /perl(CGI::SSI)/d
%filter_setup
%else
%?perl_default_filter
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(CGI::SSI\\)$
%endif

%description
The goal of CGI::FormBuilder (FormBuilder) is to provide an easy way
for you to generate and process entire CGI form-based
applications.

%prep
%setup -q -n CGI-FormBuilder-%{cpanversion}
find . -name \*.orig -delete
sed -i -e '/\.orig$/d' MANIFEST
# skip failing tests due to hash randomization
# see https://rt.cpan.org/Public/Bug/Display.html?id=81650
rm -f t/2d-template-fast.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 3.0900-4
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 3.0900-3
- 为 Magic 3.0 重建

* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 3.0900-2
- 为 Magic 3.0 重建

* Fri Aug 28 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.0900-1
- 3.09 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0800-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.0800-6
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.0800-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0800-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.0800-3
- filter CGI::SSI from requires on EL6

* Sat Aug 10 2013 Iain Arnell <iarnell@gmail.com> 3.0800-2
- filter optional CGI::SSI from requires

* Sat Aug 10 2013 Iain Arnell <iarnell@gmail.com> 3.0800-1
- update to latest upstream version
- skip failing tests due to hash randomization
- clean up spec for modern rpmbuild
- use perl_default filter

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0501-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 Petr Pisar <ppisar@redhat.com> - 3.0501-18
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0501-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0501-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 3.0501-15
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0501-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 3.0501-13
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 3.0501-12
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0501-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.0501-10
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.0501-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.0501-8
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0501-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0501-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callway <tcallawa@redhat.com> - 3.0501-5
- rebuild for new perl

* Wed Jun 20 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 3.0501-4
- Trim the description to something reasonable.
- Delete odd .orig file

* Fri Jun 15 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 3.0501-3
- BR perl(CGI::FastTemplate)

* Fri Jun 15 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 3.0501-2
- Don't BR perl or perl-devel, instead BR specific Perl modules needed to build.
- Proper license tag

* Fri Jun  1 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 3.0501-1
- First version for Fedora

