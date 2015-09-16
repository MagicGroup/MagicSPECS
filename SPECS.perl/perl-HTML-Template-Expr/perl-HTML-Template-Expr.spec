Name:           perl-HTML-Template-Expr
Version:        0.07
Release:        18%{?dist}
Summary:        Expression support extension for HTML::Template
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/HTML-Template-Expr/
Source0:        http://www.cpan.org/authors/id/S/SA/SAMTREGAR/HTML-Template-Expr-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTML::Template) >= 2.4
BuildRequires:  perl(Parse::RecDescent)
BuildRequires:  perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module provides an extension to HTML::Template which allows
expressions in the template syntax.  This is purely an addition - all
the normal HTML::Template options, syntax and behaviors will still
work.  Expression support includes comparisons, math operations,
string operations and a mechanism to allow you add your own functions
at runtime.

%prep
%setup -q -n HTML-Template-Expr-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ANNOUNCE ARTISTIC Changes GPL README
%{perl_vendorlib}/HTML/
%{_mandir}/man3/HTML::Template::Expr.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.07-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.07-17
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.07-16
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.07-15
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.07-13
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.07-11
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.07-10
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.07-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 08 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.07-6
- rebuild for new perl

* Wed Jan 02 2008 Ralf Corsépius <rc040203@freenet.de> 0.07-5
- Adjust License-tag.
- BR: perl(Test::More) (BZ 419631).

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 0.07-4
- Reformat to match cpanspec output.
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Thu Oct 19 2006 Steven Pritchard <steve@kspei.com> 0.07-3
- Rebuild.

* Wed Aug 30 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.07-2
- Fix order of arguments to find(1).

* Wed Apr 19 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.07-1
- 0.07.

* Sat Mar  4 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.06-1
- 0.06.

* Thu Dec 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.05-1
- 0.05.

* Tue Aug  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.04-1
- Bump for first FE build.

* Sat Jul  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.04-0.2
- Minor specfile cleanups.

* Tue Jun 14 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.04-0.1
- Rebuild for FC4.

* Sat Dec 11 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.04-0.fdr.1
- First build.
