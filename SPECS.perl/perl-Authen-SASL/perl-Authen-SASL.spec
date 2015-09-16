Name:           perl-Authen-SASL
Version:	2.16
Release:	2%{?dist}
Summary:        SASL Authentication framework for Perl
Summary(zh_CN.UTF-8): Perl 下的 SASL 认证框架
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/Authen-SASL/
Source0:        http://www.cpan.org/authors/id/G/GB/GBARR/Authen-SASL-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Digest::HMAC)
BuildRequires:  perl(GSSAPI)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
SASL is a generic mechanism for authentication used by several network
protocols. Authen::SASL provides an implementation framework that all
protocols should be able to share.

%description -l zh_CN.UTF-8
Perl 下的 SASL 认证框架。

%prep
%setup -q -n Authen-SASL-%{version}

chmod a-x example_pl

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc api.txt Changes example_pl
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.16-2
- 为 Magic 3.0 重建

* Fri Apr 24 2015 Liu Di <liudidi@gmail.com> - 2.16-1
- 更新到 2.16

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.15-10
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.15-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.15-8
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 2.15-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.15-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.15-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Dec 12 2010 Steven Pritchard <steve@kspei.com> 2.15-1
- Update to 2.15.
- Add example_pl to docs.

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.13-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.13-2
- rebuild against perl 5.10.1

* Mon Oct  5 2009 Stepan Kasal <skasal@redhat.com> - 2.13-1
- new upstream version, BR Test::More

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 01 2008 Steven Pritchard <steve@kspei.com> 2.12-1
- Update to 2.12.

* Thu May 15 2008 Steven Pritchard <steve@kspei.com> 2.11-1
- Update to 2.11.
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- Reformat to resemble cpanspec output.
- Drop explicit perl build dependency.

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10-2
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sat Apr 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.10-1
- Update to 2.10.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-4
- Rebuild for FC5 (perl 5.8.8).

* Sat May 14 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-3
- Add dist tag.

* Tue Apr 26 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-2
- Update to 2.09.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Apr  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.08-1
- Drop Epoch: 0 and 0.fdr release prefix.

* Wed Jul 21 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.08-0.fdr.1
- Update to 2.08.
- Bring up to date with current fedora.us Perl spec template.

* Fri Jan 30 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.06-0.fdr.1
- First build.
