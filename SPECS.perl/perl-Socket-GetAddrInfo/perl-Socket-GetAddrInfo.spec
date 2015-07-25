Name:           perl-Socket-GetAddrInfo
Version:        0.19
Release:        10%{?dist}
Summary:        RFC 2553's "getaddrinfo" and "getnameinfo" functions

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Socket-GetAddrInfo/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PEVANS/Socket-GetAddrInfo-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(ExtUtils::CChecker)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Module::Build::Compat)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Warn)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The RFC 2553 functions getaddrinfo and getnameinfo provide an abstracted
way to convert between a pair of host name/service name and socket
addresses, or vice versa. getaddrinfo converts names into a set of
arguments to pass to the socket() and connect() syscalls, and getnameinfo
converts a socket address back into its host name/service name pair.

%prep
%setup -q -n Socket-GetAddrInfo-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} $RPM_BUILD_ROOT/*


%check
%{?_with_tests:export I_CAN_HAS_INTERNETS=1}



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes examples LICENSE README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Socket*
%{_mandir}/man3/*.3*


%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.19-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.19-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.19-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.19-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.19-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.19-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.19-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.19-2
- Perl 5.16 rebuild

* Thu Jan 19 2012 Petr Šabata <contyk@redhat.com> - 0.19-1
- Just updating to 0.19, as it's needed by current POE::* packages

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.16-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.16-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Aug 22 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.16-1
- Update to 0.16

* Wed Jun  2 2010 Petr Pisar <ppisar@redhat.com> - 0.15-6
- Rebuild against perl-5.12

* Fri May 07 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.15-5
- Add BR perl(ExtUtils::CChecker)
- Add BR perl(Test::Warn)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.15-2
- Mass rebuild with perl-5.12.0

* Mon Apr 19 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.15-1
- Update to 0.15

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.12-2
- rebuild against perl 5.10.1

* Thu Jul  9 2009 kwizart < kwizart at gmail.com > - 0.12-1
- Initial spec
