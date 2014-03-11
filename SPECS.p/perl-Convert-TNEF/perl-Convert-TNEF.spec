Name:           perl-Convert-TNEF
Version:        0.17
Release:        20%{?dist}
Summary:        Perl module to read TNEF files
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Convert-TNEF/
Source0:        http://www.cpan.org/authors/id/D/DO/DOUGW/Convert-TNEF-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::Wrap)
BuildRequires:  perl(MIME::Body) >= 4.109
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
TNEF stands for Transport Neutral Encapsulation Format, and if you've
ever been unfortunate enough to receive one of these files as an email
attachment, you may want to use this module.

%prep
%setup -q -n Convert-TNEF-%{version}

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
%doc Changes README
%{perl_vendorlib}/Convert
%{_mandir}/man3/Convert::TNEF.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.17-20
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.17-19
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.17-18
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.17-16
- Perl mass rebuild

* Wed Feb  9 2011 Paul Howarth <paul@city-fan.org> - 0.17-15
- BR: perl(IO::Wrap) as perl(MIME::Body) no longer pulls it in

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.17-13
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.17-12
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.17-11
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17-8
Rebuild for new perl

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 0.17-7
- Use fixperms macro instead of our own chmod incantation.
- Reformat to more closely match cpanspec output.
- BR MIME::Body instead of perl-MIME-tools.
- BR ExtUtils::MakeMaker.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.17-6
- Fix find option order.

* Mon Sep 05 2005 Steven Pritchard <steve@kspei.com> 0.17-5
- Spec cleanup (closer to FE perl spec template).
- Include COPYING and Artistic.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Apr 26 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.17-0.fdr.3
- Specfile rewrite according to current fedora.us perl spec template.
- Fix License.
- BuildRequires perl-MIME-tools (bug 370).

* Fri Jul 11 2003 Dams <anvil[AT]livna.org> 0:0.17-0.fdr.2
- Changed Group tag value
- Added "" in build section
- Added missing directory

* Sun Jun 15 2003 Dams <anvil[AT]livna.org>
- Initial build.
