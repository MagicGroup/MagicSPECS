Name:           perl-Crypt-OpenSSL-PKCS10
Version:        0.06
Release:        21%{?dist}
Summary:        Perl interface to OpenSSL for PKCS10
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Crypt-OpenSSL-PKCS10/
Source0:        http://www.cpan.org/authors/id/J/JO/JONOZZZ/Crypt-OpenSSL-PKCS10-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  openssl openssl-devel
BuildRequires:  perl(Test::More) perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Crypt::OpenSSL::RSA)
Patch0: 	perl-Crypt-OpenSSL-PKCS10-build-paths.patch
Patch1:         perl-Crypt-OpenSSL-PKCS10-openssl.patch

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Crypt::OpenSSL::PKCS10 - Perl extension to OpenSSL's PKCS10 API.

%prep
%setup -q -n Crypt-OpenSSL-PKCS10-%{version}
chmod -c a-x Changes
chmod -c a-x *.xs

%patch0 -p1
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

# remove errant execute bit from the .pm's / .xs's
find %{buildroot} -type f -name '*.pm' -exec chmod -x {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Crypt/
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.06-21
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.06-20
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-18
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-16
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-15
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.06-14
- rebuild against perl 5.10.1

* Tue Aug 25 2009 Tomas Mraz <tmraz@redhat.com> - 0.06-13
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.06-10
- rebuild with new openssl

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.06-9
Rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.06-8
- Autorebuild for GCC 4.3

* Thu Dec  6 2007 Wes Hardaker <wjhns174@hardakers.net> - 0.06-7
- Bump to force rebuild with new openssl lib version

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.06-6
- Rebuild for selinux ppc32 issue.

* Fri Jun  1 2007 Wes Hardaker <wjhns174@hardakers.net> - 0.06-5
- really remove the README file this time

* Thu May 31 2007 Wes Hardaker <wjhns174@hardakers.net> - 0.06-4
- added a build requirement for Crypt::OpenSSL::RSA
- fix hard-coded include/library paths in the Makefile.PL
- unmodified template README removed from install
- Reverse terms in license to match perl rpm exactly

* Mon May 14 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.06-3
- BuildRequire perl(Test::More) perl(ExtUtils::MakeMaker)
- Fixed source code URL

* Tue May  8 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.06-2
- Add BuildRequire openssl-devel
- Don't manually require openssl
- Use vendorarch instead of vendorlib 

* Thu Apr 19 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.06-1
- Initial version
