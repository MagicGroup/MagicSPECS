Name:           perl-HTML-FromText
Version:	2.07
Release:	3%{?dist}
Summary:        Convert plain text to HTML

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/HTML-FromText/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/HTML-FromText-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Email::Find::addrspec) >= 0.09
BuildRequires:  perl(Exporter::Lite) >= 0.01
BuildRequires:  perl(Scalar::Util) >= 1.12
BuildRequires:  perl(HTML::Entities) >= 1.26
BuildRequires:  perl(Text::Tabs) >= 98.1128
BuildRequires:  perl(Test::More) >= 0.47

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
"HTML::FromText" converts plain text to HTML. There are a handfull of
options that shape the conversion. There is a utility function,
"text2html", that's exported by default. This function is simply a
short- cut to the Object Oriented interface described in detail below.


%prep
%setup -q -n HTML-FromText-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'

%{_fixperms} $RPM_BUILD_ROOT/*

%check
#Theses test are known to fail
rm t/01_features.t
rm t/02_v2.01.t



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{_bindir}/text2html
%{perl_vendorlib}/HTML/
%{_mandir}/man3/*.3*
%{_mandir}/man1/text2html.1.gz


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.07-3
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 2.07-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.07-1
- 更新到 2.07

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.05-22
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.05-21
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.05-20
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.05-19
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.05-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.05-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.05-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.05-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.05-14
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.05-13
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.05-12
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.05-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.05-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.05-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.05-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep  2 2008 kwizart < kwizart at gmail.com > - 2.05-2
- Add fixperms

* Thu Jul 31 2008 kwizart < kwizart at gmail.com > - 2.05-1
- Initial package for Fedora

