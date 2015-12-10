Name:           perl-IO-Async
Version:	0.68
Release:	3%{?dist}
Summary:        A collection of modules that implement asynchronous filehandle IO

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/IO-Async/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PEVANS/IO-Async-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Heap)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Refcount)
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(Socket::GetAddrInfo) >= 0.08
BuildRequires:  perl(Async::MergePoint)
BuildRequires:  perl(Time::HiRes)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
A collection of modules that implement asynchronous filehandle IO

%prep
%setup -q -n IO-Async-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.68-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.68-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.68-1
- 更新到 0.68

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.29-17
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.29-16
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.29-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.29-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.29-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.29-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.29-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.29-10
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.29-8
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.29-6
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.29-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.29-3
- Add BR perl(Time::HiRes)

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.29-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Aug 22 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.29-1
- Update to 0.29
- Add Test::Warn BR

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.28-2
- Mass rebuild with perl-5.12.0

* Mon Apr 19 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.28-1
- Update to 0.28

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.23-2
- rebuild against perl 5.10.1

* Mon Aug 31 2009 kwizart < kwizart at gmail.com > - 0.23-1
- Update to 0.23

* Tue Aug 11 2009 kwizart < kwizart at gmail.com > - 0.22-2
- Add Missing BR

* Mon Jul 20 2009 kwizart < kwizart at gmail.com > - 0.22-1
- Update to 0.22

* Thu Jul  9 2009 kwizart < kwizart at gmail.com > - 0.21-1
- Initial spec
