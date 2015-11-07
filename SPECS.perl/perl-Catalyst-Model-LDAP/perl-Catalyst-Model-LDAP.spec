Name:           perl-Catalyst-Model-LDAP
Version:	0.17
Release:	3%{?dist}
Summary:        LDAP model class for Catalyst
Summary(zh_CN.UTF-8): Catalyst 的 LDAP 模型类
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/Catalyst-Model-LDAP/
Source0:        http://www.cpan.org/authors/id/D/DA/DANIELTWC/Catalyst-Model-LDAP-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  perl >= 1:5.8.1
BuildRequires:  perl(Catalyst) >= 5.62
BuildRequires:  perl(Catalyst::Model)
BuildRequires:  perl(Catalyst::Test)
BuildRequires:  perl(Class::Accessor::Fast)
BuildRequires:  perl(Class::C3)
BuildRequires:  perl(Data::Page)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Net::LDAP) >= 0.34
BuildRequires:  perl(Net::LDAP::Constant)
BuildRequires:  perl(Net::LDAP::Control::Sort)
BuildRequires:  perl(Net::LDAP::Control::VLV)
BuildRequires:  perl(Net::LDAP::Entry)
BuildRequires:  perl(Net::LDAP::Search)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04

Requires:       perl(Catalyst) >= 5.62
Requires:       perl(Catalyst::Model)
Requires:       perl(Class::Accessor::Fast)
Requires:       perl(Class::C3)
Requires:       perl(Data::Page)
Requires:       perl(Net::LDAP) >= 0.34
Requires:       perl(Net::LDAP::Constant)
Requires:       perl(Net::LDAP::Control::Sort)
Requires:       perl(Net::LDAP::Control::VLV)
Requires:       perl(Net::LDAP::Entry)
Requires:       perl(Net::LDAP::Search)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This is the Net::LDAP model class for Catalyst. It is nothing more than a
simple wrapper for Net::LDAP.

%description -l zh_CN.UTF-8
Catalyst 的 LDAP 模型类。

%prep
%setup -q -n Catalyst-Model-LDAP-%{version}

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
TEST_POD=1 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.17-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.17-2
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Liu Di <liudidi@gmail.com> - 0.17-1
- 更新到 0.17

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-27
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-26
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.16-25
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.16-24
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.16-23
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.16-22
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-20
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-18
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.16-17
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.16-16
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.16-15
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.16-14
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.16-13
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.16-11
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.16-9
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.16-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.16-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jun 07 2008 Caolán McNamara <caolanm@redhat.com> 0.16-4
- rebuild for dependancies

* Sat Apr 12 2008 Simon Wilkinson <simon@sxw.org.uk> 0.16-3
- Make test also check POD coverage
- Fix license to have correct value

* Thu Mar 27 2008 Simon Wilkinson <simon@sxw.org.uk> 0.16-2
- Add build dependencies on Test::Pod and Test::Pod::Coverage for tests

* Thu Mar 27 2008 Simon Wilkinson <simon@sxw.org.uk> 0.16-1
- Specfile autogenerated by cpanspec 1.73.
