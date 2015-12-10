Name:           perl-Crypt-OpenSSL-DSA
Version:	0.15
Release:	3%{?dist}
Summary:        Perl interface to OpenSSL for DSA
License:        GPL+ or Artistic 
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Crypt-OpenSSL-DSA/
Source0:        http://search.cpan.org/CPAN/authors/id/K/KM/KMX/Crypt-OpenSSL-DSA-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  openssl openssl-devel perl(Test) perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Digest::SHA1) perl(File::Temp)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Patch1: Crypt-OpenSSL-DSA-0.13-security_croak-in-do_verify-too.patch

%description
Crypt::OpenSSL::DSA - Digital Signature Algorithm using OpenSSL

%prep
%setup -q -n Crypt-OpenSSL-DSA-%{version}

%patch1 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;

%{_fixperms} %{buildroot}/*

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Crypt/
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.15-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.15-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.15-1
- 更新到 0.15

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.13-24
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.13-23
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.13-22
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.13-21
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.13-19
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-17
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-16
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.13-15
- rebuild against perl 5.10.1

* Mon Aug 31 2009 Stepan Kasal <skasal@redhat.com> - 0.13-14
- re-enable tests

* Fri Aug 28 2009 Stepan Kasal <skasal@redhat.com> - 0.13-13
- disable tests to work around bug #520152

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.13-12
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Wes Hardaker <wjhns174@hardakers.net> - 0.13-9
- Fix CVE-2009-0129 and have do_verify croak on fatal error

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.13-8
- rebuild with new openssl

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-7
- rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.13-6
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 0.13-5
 - Rebuild for deps

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.13-4
- Rebuild for selinux ppc32 issue.

* Mon May 14 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.13-3
- BuildRequire perl(Test) perl(ExtUtils::MakeMaker) perl(Digest::SHA1)
  and perl(File::Temp)
- Fixed source code URL

* Tue May  8 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.13-2
- Add BuildRequire openssl-devel
- Don't manually require openssl
- Use vendorarch instead of vendorlib 

* Thu Apr 19 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.13-1
- Initial version
