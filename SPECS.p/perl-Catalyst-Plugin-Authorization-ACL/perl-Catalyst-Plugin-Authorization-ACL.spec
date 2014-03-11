Name:      perl-Catalyst-Plugin-Authorization-ACL
Version:   0.15
Release:   10%{?dist}
Summary:   ACL Support for Catalyst Applications
License:   GPL+ or Artistic
Group:     Development/Libraries
URL:       http://search.cpan.org/dist/Catalyst-Plugin-Authorization-ACL/
Source0:   http://search.cpan.org/CPAN/authors/id/R/RK/RKITOVER/Catalyst-Plugin-Authorization-ACL-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(CPAN)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Catalyst::Runtime)
BuildRequires:  perl(Class::Data::Inheritable)
BuildRequires:  perl(Class::Throwable)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tree::Simple::Visitor::FindByPath)
BuildRequires:  perl(Tree::Simple::Visitor::GetAllDescendents)
## required for tests
BuildRequires: perl(Test::Pod)
BuildRequires: perl(Test::Pod::Coverage)
BuildRequires: perl(Test::WWW::Mechanize::Catalyst)
BuildRequires: perl(Catalyst::Plugin::Authorization::Roles)
BuildRequires: perl(Catalyst::Plugin::Authentication)
BuildRequires: perl(Catalyst::Plugin::Session::State::Cookie)

%description
This module provides Access Control List style path protection, with
arbitrary rules for Catalyst applications. It operates only on the
Catalyst private namespace, at least at the moment.

%prep
%setup -q -n Catalyst-Plugin-Authorization-ACL-%{version} 

# make sure doc/tests don't generate provides
# note we first filter out the bits in _docdir...
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} `perl -p -e 's|\S+%{_docdir}/%{name}-%{version}\S+||'`
EOF

%define __perl_provides %{_builddir}/Catalyst-Plugin-Authorization-ACL-%{version}/%{name}-prov
chmod +x %{__perl_provides}

cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} `perl -p -e 's|\S+%{_docdir}/%{name}-%{version}\S+||'`
EOF

%define __perl_requires %{_builddir}/Catalyst-Plugin-Authorization-ACL-%{version}/%{name}-req
chmod +x %{__perl_requires}

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
TEST_POD=1 

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.15-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.15-9
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.15-8
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.15-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.15-4
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.15-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.15-2
- rebuild against perl 5.10.1

* Tue Dec 01 2009 Gabriel Somlo <somlo at cmu.edu> 0.15-1
- update to 0.15

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 Gabriel Somlo <somlo at cmu.edu> 0.10-2
- specfile cleanup

* Tue Jan 6 2009 Gabriel Somlo <somlo at cmu.edu> 0.10-1
- initial specfile based on cpan2rpm and other catalyst examples by Chris Weyl
