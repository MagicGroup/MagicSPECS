Name:       perl-namespace-autoclean
Version:	0.27
Release:	1%{?dist}
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Keep imports out of your namespace
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/namespace-autoclean-%{version}.tar.gz
Url:        http://search.cpan.org/dist/namespace-autoclean
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(B::Hooks::EndOfScope)
BuildRequires: perl(Class::MOP) >= 0.80
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(List::Util)
BuildRequires: perl(namespace::clean) >= 0.20
BuildRequires: perl(Test::More)

%{?perl_default_filter}

%description
When you import a function into a Perl package, it will naturally also
be available as a method. The 'namespace::autoclean' pragma will remove
all imported symbols at the end of the current package's compile cycle.
Functions called in the package itself will still be bound by their
name, but they won't show up as methods on your class or instances. This
module is very similar to namespace::clean, except it will clean all
imported functions, no matter if you imported them before or after you
'use'd the pagma. It will also not touch anything that looks like a
method, according to 'Class::MOP::Class::get_method_list'.


%prep
%setup -q -n namespace-autoclean-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.27-1
- 更新到 0.27

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.13-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.13-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.13-2
- Perl 5.16 rebuild

* Sat Jan 14 2012 Iain Arnell <iarnell@gmail.com> 0.13-1
- update to latest upstream version

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.12-3
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.12-2
- Perl mass rebuild

* Sun Mar 13 2011 Iain Arnell <iarnell@gmail.com> 0.12-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.09-3
- rebuild against perl 5.10.1

* Thu Sep 17 2009 Stepan Kasal <skasal@redhat.com> 0.09-2
- fix the previous changelog entry

* Wed Sep 16 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- add %%perl_default_filter'ing
- auto-update to 0.09 (by cpan-spec-update 0.01)
- added a new req on perl(B::Hooks::EndOfScope) (version 0.07)
- added a new req on perl(Class::MOP) (version 0.80)
- added a new req on perl(List::Util) (version 0)
- added a new req on perl(namespace::clean) (version 0.11)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 01 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08-1
- submission

* Wed Jul 01 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
