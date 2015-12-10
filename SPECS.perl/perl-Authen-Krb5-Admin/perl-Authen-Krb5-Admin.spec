Name:           perl-Authen-Krb5-Admin
Version:	0.17
Release:	4%{?dist}
Summary:        Perl extension for MIT Kerberos 5 admin interface
Summary(zh_CN.UTF-8): MIT kerberos 5 管理接口的 Perl 扩展
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
# admin.h - MIT
# ppport.h - GPL+ or Artisic (same as any version of Perl)
# everything else: BSD (two clause)
License:        MIT and BSD and (GPL+ or Artistic)
URL:            http://search.cpan.org/dist/Authen-Krb5-Admin/
Source0:        http://www.cpan.org/authors/id/S/SJ/SJQUINNEY/Authen-Krb5-Admin-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openssl-devel
BuildRequires:  perl(Authen::Krb5)
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Authen::Krb5::Admin is an object-oriented interface to the Kerberos 5 admin
server. Currently only MIT KDCs are supported, but the author envisions
seamless integration with other KDCs.

%description -l zh_CN.UTF-8
MIT kerberos 5 管理接口的 Perl 扩展。

%prep
%setup -q -n Authen-Krb5-Admin-%{version}

sed -i -e 's!$PREFIX/lib!$PREFIX/%{_lib}!' Makefile.PL

%build
# set some dummy values for the test to stop Makefile.PL from asking
# note: the values are never used
export PERL_KADM5_PRINCIPAL=dummy
export PERL_KADM5_TEST_NAME=dummy
export PERL_KADM5_TEST_NAME_2=dummy
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
chmod -R u+w $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check
# not possible due to required kerberso environment

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README COPYING ChangeLog
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Authen
%{_mandir}/man3/*.3pm*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.17-4
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.17-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.17-2
- 为 Magic 3.0 重建

* Fri Apr 24 2015 Liu Di <liudidi@gmail.com> - 0.17-1
- 更新到 0.17

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.11-16
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.11-15
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.11-14
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.11-13
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11-11
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Christian Krause <chkr@fedoraproject.org> - 0.11-9
- rebuild against new krb5-1.9

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-8
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-7
- Mass rebuild with perl-5.12.0

* Sat Mar 06 2010 Christian Krause <chkr@fedoraproject.org> - 0.11-6
- rebuild against new krb5-1.8

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.11-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 08 2009 Christian Krause <chkr@fedoraproject.org> - 0.11-3
- rebuild against new krb5-1.7

* Fri Mar 13 2009 Christian Krause <chkr@fedoraproject.org> - 0.11-2
- fixed build problem on x86_64 (libk5crypto not found)
- minor cleanup
- removed unnecessary build requirement

* Sat Mar 07 2009 Christian Krause <chkr@fedoraproject.org> - 0.11-1
- Initial spec file for Authen::Krb5::Admin
