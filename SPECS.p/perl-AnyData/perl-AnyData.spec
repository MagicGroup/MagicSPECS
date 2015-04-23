Name:           perl-AnyData
Version:	0.12
Release:	1%{?dist}
Summary:        Easy access to data in many formats
Summary(zh_CN.UTF-8): 以多种格式方便的访问数据
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/AnyData
Source0:        http://search.cpan.org/CPAN/authors/id/R/RE/REHSACK/AnyData-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
# Not tested:   perl(CGI)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
# Not tested:   perl(HTML::TableExtract)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::File)
# Not tested:   perl(XML::Twig)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:  perl(CGI)
Requires:  perl(constant)
Requires:  perl(Data::Dumper)
Requires:  perl(HTML::TableExtract)
Requires:  perl(Exporter)
Requires:  perl(IO::File)
Requires:  perl(XML::Twig)

%description
The AnyData modules provide simple and uniform access to data from
many sources -- perl arrays, local files, remote files retrievable via
http or ftp -- and in many formats including flat files (CSV, Fixed
Length, Tab Delimited, etc), standard format files (Web Logs,
Passwd files, etc.),  structured files (XML, HTML Tables) and binary 
files with parseable headers (mp3s, jpgs, pngs, etc).  

There are two separate modules, each providing a different interface:
AnyData.pm provides a simple tied hash interface and DBD::AnyData
provides a DBI/SQL interface.  You can use either or both depending on
your needs.

%description -l zh_CN.UTF-8
以多种格式方便的访问数据。

%prep
%setup -q -n AnyData-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/AnyData.pm
%{perl_vendorlib}/AnyData/
%{_mandir}/man3/*.3*


%changelog
* Wed Apr 22 2015 Liu Di <liudidi@gmail.com> - 0.12-1
- 更新到 0.12

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.10-19
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.10-18
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.10-17
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.10-15
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.10-13
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-11
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-10
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.10-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.10-6
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-5
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-4.1
- add BR: perl(ExtUtils::MakeMaker)

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-4
- license fix

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-3
- bump for FC-6

* Fri Mar 31 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-2
- minor cleanups

* Sun Jan  8 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-1
- Initial package for Fedora Extras
