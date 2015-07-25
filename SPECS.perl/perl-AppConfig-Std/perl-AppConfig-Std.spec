
Name:       perl-AppConfig-Std 
Version:	1.09
Release:	1%{?dist}
# see lib/AppConfig/Std.pm
License:    GPL+ or Artistic 
Group:      Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:    Provides standard configuration options 
Summary(zh_CN.UTF-8): 提供了标准的配置选项
Source:     http://search.cpan.org/CPAN/authors/id/N/NE/NEILB/AppConfig-Std-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/AppConfig-Std
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker) 
BuildRequires: perl(AppConfig) >= 1.52
BuildRequires: perl(Pod::Usage) >= 1.14


%description
AppConfig::Std is a Perl module that provides a set of standard
configuration variables and command-line switches. It is implemented as a
subclass of AppConfig; AppConfig provides a general mechanism for handling
global configuration variables.

%description -l zh_CN.UTF-8
提供了标准的配置选项。

%prep
%setup -q -n AppConfig-Std-%{version}

perl -pi -e 's|^#!\./perl|#!/usr/bin/perl|' t/*

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh

%check


%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1.09-1
- 更新到 1.09

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.07-14
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.07-13
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.07-12
- 为 Magic 3.0 重建

* Fri Jan 27 2012 Liu Di <liudidi@gmail.com> - 1.07-11
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.07-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.07-7
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.07-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.07-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep 20 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.07-2
- bump

* Tue Sep 16 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.07-1
- initial Fedora packaging
- generated with cpan2dist (CPANPLUS::Dist::Fedora version 0.0.1)

