Name:           perl-Catalyst-Controller-ActionRole
Summary:        Apply roles to action instances
Summary(zh_CN.UTF-8): 对操作实例应用角色
Version:	0.17
Release:	1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Catalyst-Controller-ActionRole-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Catalyst-Controller-ActionRole/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Catalyst)
BuildRequires:  perl(Catalyst::Action)
BuildRequires:  perl(Catalyst::Action::REST)
BuildRequires:  perl(Catalyst::Controller)
BuildRequires:  perl(Catalyst::Runtime) >= 5.80025
BuildRequires:  perl(Catalyst::Test)
BuildRequires:  perl(Catalyst::Utils)
BuildRequires:  perl(Class::MOP) >= 0.80
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.31
BuildRequires:  perl(FindBin)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Moose) >= 0.90
BuildRequires:  perl(Moose::Meta::Class)
BuildRequires:  perl(Moose::Role)
BuildRequires:  perl(MooseX::Types::Moose)
BuildRequires:  perl(namespace::clean)
BuildRequires:  perl(parent)
BuildRequires:  perl(String::RewritePrefix) >= 0.004
BuildRequires:  perl(Test::More)

Requires:       perl(Catalyst::Controller)
Requires:       perl(Catalyst::Runtime) >= 5.80025
Requires:       perl(Class::MOP) >= 0.80
Requires:       perl(Moose) >= 0.90

%{?perl_default_filter}
#{?perl_default_subpackage_tests}

%description
This module allows to apply roles to the Catalyst::Actions for different
controller methods.

%description -l zh_CN.UTF-8
对操作实例应用角色。

%prep
%setup -q -n Catalyst-Controller-ActionRole-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jun 05 2015 Liu Di <liudidi@gmail.com> - 0.17-1
- 更新到 0.17

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.15-27
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.15-26
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.15-25
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.15-24
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.15-23
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.15-22
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.15-21
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.15-20
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.15-19
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.15-18
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.15-17
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.15-16
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.15-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.15-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.15-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.15-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.15-11
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.15-10
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.15-9
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.15-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.15-7
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.15-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.15-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.15-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Sep 10 2010 Iain Arnell <iarnell@gmail.com> 0.15-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.15)
- added a new br on perl(Catalyst) (version 0)
- added a new br on perl(Catalyst::Action) (version 0)
- added a new br on perl(Catalyst::Action::REST) (version 0)
- added a new br on perl(Catalyst::Controller) (version 0)
- altered br on perl(Catalyst::Runtime) (5.71001 => 5.80025)
- added a new br on perl(Catalyst::Test) (version 0)
- added a new br on perl(Catalyst::Utils) (version 0)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.31)
- added a new br on perl(FindBin) (version 0)
- added a new br on perl(List::Util) (version 0)
- added a new br on perl(Moose::Meta::Class) (version 0)
- added a new br on perl(Moose::Role) (version 0)
- added a new br on perl(Test::More) (version 0)
- added a new br on perl(parent) (version 0)
- added a new req on perl(Catalyst::Controller) (version 0)
- altered req on perl(Catalyst::Runtime) (5.71001 => 5.80025)

* Wed Jun 30 2010 Iain Arnell <iarnell@gmail.com> 0.14-1
- Specfile autogenerated by cpanspec 1.78.
