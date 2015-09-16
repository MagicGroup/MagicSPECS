Name:           perl-Beanstalk-Client
Version:	1.07
Release:	2%{?dist}
Summary:        Client class to talk to a beanstalkd server
Summary(zh_CN.UTF-8): 与 beanstalkd 服务器对话的客户端
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/Beanstalk-Client/
Source0:        http://search.cpan.org/CPAN/authors/id/G/GB/GBARR/Beanstalk-Client-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Class::Accessor::Fast)
BuildRequires:  perl(Error)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(YAML::Syck)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Beanstalk::Client provides a Perl API of protocol version 1.0 to the
beanstalkd server, a fast, general-purpose, in-memory workqueue service by
Keith Rarick.

%description -l zh_CN.UTF-8
与 beanstalkd 服务器对话的客户端。

%prep
%setup -q -n Beanstalk-Client-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh

%check


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/Beanstalk
%{_mandir}/man3/Beanstalk::*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.07-2
- 为 Magic 3.0 重建

* Fri Apr 24 2015 Liu Di <liudidi@gmail.com> - 1.07-1
- 更新到 1.07

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.06-28
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.06-27
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.06-26
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.06-25
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.06-24
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.06-23
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.06-22
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.06-21
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.06-20
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.06-19
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.06-18
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.06-17
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.06-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.06-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.06-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.06-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.06-12
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.06-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.06-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.06-9
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.06-8
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 1.06-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.06-5
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.06-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.06-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Jun 22 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.06-1
- Upstream released new version

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.05-3
- rebuild against perl 5.10.1

* Wed Jul 29 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.05-2
- Review fixes (#513869)

* Sun Jul 26 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> - 1.05-1
- Initial import
