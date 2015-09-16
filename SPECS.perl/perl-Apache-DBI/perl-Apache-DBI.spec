%global perlname Apache-DBI

Name:      perl-Apache-DBI
Version:	1.12
Release:	3%{?dist}
Summary:   Persistent database connections with Apache/mod_perl
Summary(zh_CN.UTF-8): 使用 Apache/mod_perl 的持久数据库连接

Group:     Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:   GPL+ or Artistic
URL:       http://search.cpan.org/dist/Apache-DBI/
Source:    http://search.cpan.org/CPAN/authors/id/P/PH/PHRED/%{perlname}-%{version}.tar.gz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: perl(Test::More)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(DBD::mysql)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}


%description
This is version %{version} of Apache::AuthDBI and Apache::DBI.

These modules are supposed to be used with the Apache server together with 
an embedded perl interpreter like mod_perl. They provide support for basic 
authentication and authorization as well as support for persistent database 
connections via Perl's Database Independent Interface (DBI). 

o DBI.pm provides persistent database connections: 
  - connections can be established during server-startup 
  - configurable rollback to ensure data integrity 
  - configurable verification of the connections to avoid time-outs. 

o AuthDBI.pm provides authentication and authorization: 
  - optional shared cache for passwords to minimize database load 
  - configurable cleanup-handler deletes outdated entries from the cache 

Apache::DBI has been in widespread deployment on many platforms for
years.  Apache::DBI is one of the most widely used mod_perl related
modules.  It can be considered stable.

%description -l zh_CN.UTF-8
使用 Apache/mod_perl 的持久数据库连接。

%prep
%setup -q -n %{perlname}-%{version}
%{__perl} -pi -e 's|/usr/local/bin/perl|%{__perl}|' eg/startup.pl
chmod 644 eg/startup.pl


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';' -print
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';' -print
chmod -R u+rwX,go+rX,go-w %{buildroot}/*
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%check


%files
%defattr(-, root, root, -)
%doc Changes README TODO traces.txt eg/
%{_mandir}/man3/Apache*
%{perl_vendorlib}/Apache

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.12-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.12-2
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1.12-1
- 更新到 1.12

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.11-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.11-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.11-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.11-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.11-5
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 1.11-4
- 为 Magic 3.0 重建

* Fri Jan 27 2012 Liu Di <liudidi@gmail.com> - 1.11-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 15 2011 Remi Collet <Fedora@famillecollet.com> 1.11-1
- update to 1.11 (bugfix)

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.10-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Remi Collet <Fedora@famillecollet.com> 1.10-1
- update to 1.10 (bugfix)

* Tue Nov 23 2010 Remi Collet <Fedora@famillecollet.com> 1.09-1
- update to 1.09 (bugfix)

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.08-2
- Mass rebuild with perl-5.12.0

* Tue Feb 09 2010 Remi Collet <Fedora@famillecollet.com> 1.08-1
- update to 1.08 (bugfix)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.07-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat May 17 2008 Remi Collet <Fedora@famillecollet.com> 1.07-1
- update to 1.07

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.06-2.2
Rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.06-1.2
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.06-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sun Mar 25 2007 Remi Collet <Fedora@famillecollet.com> 1.06-1
- update to 1.06

* Sat Nov 25 2006 Remi Collet <Fedora@famillecollet.com> 1.05-2
- change from review (-perldoc +traces +eg)

* Sat Nov 25 2006 Remi Collet <Fedora@famillecollet.com> 1.05-1
- initial spec
