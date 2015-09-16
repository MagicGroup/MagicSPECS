Name:           perl-CGI-Prototype
Version:        0.9054
Release:        14%{?dist}
Summary:        Create a CGI application by subclassing
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/CGI-Prototype/
Source0:        http://www.cpan.org/authors/id/M/ME/MERLYN/CGI-Prototype-%{version}.tar.gz
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# core
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
# cpan
BuildRequires:  perl(Class::Prototyped)
BuildRequires:  perl(Template)
# test
BuildRequires:  perl(Test::Pod), perl(Test::Pod::Coverage)

# use base masks these...
Requires:       perl(Class::Prototyped)
Requires:       perl(Template)

%{?filter_setup:
%filter_from_provides /perl(My::/d
}
%?perl_default_filter
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(My::

%description
The core of every CGI application seems to be roughly the same:

*   Analyze the incoming parameters, cookies, and URLs to determine the state
of the application (let's call this "dispatch").  
* Based on the current state, analyze the incoming parameters to respond to 
any form submitted ("respond").  
*   From there, decide what response page should be generated, and produce it
("render").

CGI::Prototype creates a "Class::Prototyped" engine for doing all this, with 
the right amount of callback hooks to customize the process.  Because I'm 
biased toward Template Toolkit for rendering HTML, I've also integrated that 
as my rendering engine of choice. And, being a fan of clean MVC designs, the
classes become the controllers, and the templates become the views, with clean 
separation of responsibilities, and "CGI::Prototype" a sort of "archetypal" 
controller.


%prep
%setup -q -n CGI-Prototype-%{version}

# make rpmlint happy
perl -pi -e 's|^#! ?perl|#!/usr/bin/perl|' t/*.t t/cprove
chmod -c -x t/cprove

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
# note the "skipped: CGI::Prototype::Mecha not found" is expected; this module
# is a runtime requirement of that module, resulting in a
# plugin-before-the-base-module sorta deal.


%files
%doc Changes README TODO t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.9054-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.9054-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.9054-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.9054-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.9054-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.9054-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.9054-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.9054-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.9054-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.9054-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.9054-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.9054-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9054-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> 0.9054-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- update provides filtering to use macros

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.9053-13
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.9053-12
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9053-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.9053-10
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.9053-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.9053-8
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9053-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9053-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.9053-5
- rebuild for new perl

* Thu May 03 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.9053-4
- bump

* Mon Apr 30 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.9053-3
- switch to filtering deps, rather than doing it manually

* Mon Apr 30 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.9053-2
- include full test suite in %%doc
- disable autoprov -- with this small of a package it's easier than filtering

* Mon Apr 09 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.9053-1
- Specfile autogenerated by cpanspec 1.70.
