Name:           perl-CGI-Ex
Version:        2.32
Release:        19%{?dist}
Summary:        CGI utility suite - makes powerful application writing fun and easy
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/CGI-Ex/
Source0:        http://www.cpan.org/authors/id/R/RH/RHANDOM/CGI-Ex-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# core
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Template::Alloy)       >= 1.004
BuildRequires:  perl(Test::More)
# test
BuildRequires:  perl(CGI)
BuildRequires:  perl(Config::IniHash)
BuildRequires:  perl(Crypt::Blowfish)
BuildRequires:  perl(Hash::Case)
BuildRequires:  perl(JSON)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Taint::Runtime)
BuildRequires:  perl(Template::View)
BuildRequires:  perl(YAML)
BuildRequires:  perl(XML::Simple)


%description
CGI::Ex provides a suite of utilities to make writing CGI scripts more
enjoyable. Although they can all be used separately, the main functionality
of each of the modules is best represented in the CGI::Ex::App module.
CGI::Ex::App takes CGI application building to the next step. CGI::Ex::App
is not quite a framework (which normally includes pre-built html) instead
CGI::Ex::App is an extended application flow that dramatically reduces CGI
build time in most cases. It does so using as little magic as possible. See
CGI::Ex::App.

%prep
%setup -q -n CGI-Ex-%{version}

# make rpmlint happy :)
find samples/ -type f -exec chmod -c -x {} \;
perl -pi -e 's|^#!perl|#!/usr/bin/perl|' t/1_validate_14_untaint.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README samples/ t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.32-19
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.32-18
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.32-17
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.32-16
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.32-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.32-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.32-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.32-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.32-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.32-10
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.32-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.32-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.32-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.32-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.32-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.32-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Aug 08 2010 Iain Arnell <iarnell@gmail.com> 2.32-1
- update to latest upstream version

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.27-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.27-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.27-1
- update to 2.27

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.24-1
- update to 2.24

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.21-2
- rebuild for new perl

* Mon Nov 05 2007 Chris Weyl <cweyl@alumni.drew.edu> 2.21-1
- update to 2.21
- license tag: GPL -> GPL+

* Thu May 31 2007 Chris Weyl <cweyl@alumni.drew.edu> 2.13-1
- update to 2.13

* Sun May 13 2007 Chris Weyl <cweyl@alumni.drew.edu> 2.12-1
- update to 2.12

* Wed May 09 2007 Chris Weyl <cweyl@alumni.drew.edu> 2.11-1
- update to 2.11
- add split br's

* Mon Apr 30 2007 Chris Weyl <cweyl@alumni.drew.edu> 2.10-2
- bump

* Sat Apr 28 2007 Chris Weyl <cweyl@alumni.drew.edu> 2.10-1
- add perl(Hash::Case) as a BR
- update to 2.10

* Wed Apr 18 2007 Chris Weyl <cweyl@alumni.drew.edu> 2.09-2
- add additional BR's

* Sat Apr 07 2007 Chris Weyl <cweyl@alumni.drew.edu> 2.09-1
- Specfile autogenerated by cpanspec 1.70.
