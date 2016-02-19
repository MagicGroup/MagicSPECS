Name:           perl-Catalyst-Action-REST
Version:	1.20
Release:	2%{?dist}
Summary:        Automated REST Method Dispatching
Summary(zh_CN.UTF-8): REST 自动调度方法
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/Catalyst-Action-REST/
# upstream releases tend to flip between these locations
#Source0:        http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Catalyst-Action-REST-%{version}.tar.gz
Source0:        http://search.cpan.org/CPAN/authors/id/J/JJ/JJNAPIORK/Catalyst-Action-REST-%{version}.tar.gz
#Source0:        http://search.cpan.org/CPAN/authors/id/F/FL/FLORA/Catalyst-Action-REST-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Catalyst::Runtime) >= 5.80030
BuildRequires:  perl(Class::Inspector) >= 1.13
BuildRequires:  perl(Config::General)
BuildRequires:  perl(Data::Serializer) >= 0.36
BuildRequires:  perl(Data::Taxi)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(FreezeThaw)
BuildRequires:  perl(JSON) >= 2.12
BuildRequires:  perl(JSON::XS)
BuildRequires:  perl(LWP::UserAgent) >= 2.033
BuildRequires:  perl(Module::Pluggable::Object)
BuildRequires:  perl(Moose) >= 1.03
BuildRequires:  perl(MRO::Compat) >= 0.10
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(Params::Validate) >= 0.76
BuildRequires:  perl(PHP::Serialization)
BuildRequires:  perl(URI::Find)
BuildRequires:  perl(XML::Simple)
BuildRequires:  perl(YAML::Syck) >= 0.67
Requires:       perl(Catalyst::Runtime) >= 5.80030
Requires:       perl(Class::Inspector) >= 1.13
Requires:       perl(Config::General)
Requires:       perl(Data::Serializer) >= 0.36
Requires:       perl(Data::Taxi)
Requires:       perl(FreezeThaw)
Requires:       perl(JSON) >= 2.12
Requires:       perl(LWP::UserAgent) >= 2.033
Requires:       perl(Moose) >= 1.03
Requires:       perl(MRO::Compat) >= 0.10
Requires:       perl(Params::Validate) >= 0.76
Requires:       perl(PHP::Serialization)
Requires:       perl(XML::Simple)
Requires:       perl(YAML::Syck) >= 0.67
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This Action handles doing automatic method dispatching for REST requests.
It takes a normal Catalyst action, and changes the dispatch to append an
underscore and method name. First it will try dispatching to an action
with the generated name, and failing that it will try to dispatch to a
regular method.

%description -l zh_CN.UTF-8
REST 自动调度方法。

%prep
%setup -q -n Catalyst-Action-REST-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check


%files
%doc Changes README TODO
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.20-2
- 更新到 1.20

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.19-2
- 为 Magic 3.0 重建

* Fri Jun 05 2015 Liu Di <liudidi@gmail.com> - 1.19-1
- 更新到 1.19

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.95-21
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.95-20
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.95-19
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.95-18
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.95-17
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.95-16
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.95-15
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.95-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.95-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.95-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.95-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.95-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.95-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.95-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.95-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.95-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.95-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.95-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.95-3
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.95-2
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Iain Arnell <iarnell@gmail.com> 0.95-1
- update to latest upstream version

* Sat Aug 27 2011 Iain Arnell <iarnell@gmail.com> 0.91-1
- update to latest upstream version

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.90-2
- Perl mass rebuild

* Sat Feb 26 2011 Iain Arnell <iarnell@gmail.com> 0.90-1
- update to latest upstream version

* Sun Feb 20 2011 Iain Arnell <iarnell@gmail.com> 0.89-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.88-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Iain Arnell <iarnell@gmail.com> 0.88-1
- update to latest upstream version

* Sat Nov 06 2010 Iain Arnell <iarnell@gmail.com> 0.87-1
- update to latest upstream

* Sun Sep 05 2010 Iain Arnell <iarnell@gmail.com> 0.86-1
- update to latest upstream version

* Sat Jul 17 2010 Iain Arnell <iarnell@gmail.com> 0.85-2
- cleanup spec for modern rpmbuild

* Sun Jun 27 2010 Iain Arnell <iarnell@gmail.com> 0.85-1
- Specfile autogenerated by cpanspec 1.78.
