Name: 		perl-Crypt-PasswdMD5
Version:	1.3
Release:	16%{?dist}
Summary:	Provides interoperable MD5-based crypt() functions 
License:	GPL+ or Artistic
Group:		Development/Libraries
URL: 		http://search.cpan.org/dist/Crypt-PasswdMD5/
Source0: 	http://search.cpan.org/CPAN/authors/id/L/LU/LUISMUNOZ/Crypt-PasswdMD5-%{version}.tar.gz
Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: 	noarch
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  %{_bindir}/iconv

%description
This package provides MD5-based crypt() functions

%prep
%setup -q -n Crypt-PasswdMD5-%{version}
%{_bindir}/iconv -f iso-8859-1 -t utf-8 -o PasswdMD5.pm.new PasswdMD5.pm && mv PasswdMD5.pm.new PasswdMD5.pm
%{__sed} -i -e 's/ISO-8859-1/UTF-8/' PasswdMD5.pm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check


%files
%doc README
%{perl_vendorlib}/Crypt
%{_mandir}/man3/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.3-16
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.3-15
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.3-14
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.3-13
- 为 Magic 3.0 重建

* Fri Jan 16 2012 Petr Šabata <psabata@redhat.com> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
- Spec cleanup, fix dependencies

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3-11
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3-10
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3-8
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3-7
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.3-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-3.1
Rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Tue Feb 27 2007 Mike McGrath <mmcgrath@redhat.com> - 1.3-2
- Basic fixes (BZ 230228)

* Tue Feb 27 2007 Mike McGrath <mmcgrath@redhat.com> - 1.3-1
- Initial Packaging
