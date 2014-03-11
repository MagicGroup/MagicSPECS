Name:           perl-Crypt-Simple
Version:        0.06
Release:        16%{?dist}
Summary:        Encrypt stuff simply 

Group:          Development/Libraries
License:        GPLv2+
URL:            http://search.cpan.org/dist/Crypt-Simple/
Source0:        http://search.cpan.org/CPAN/authors/id/K/KA/KASEI/Crypt-Simple-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  perl(Crypt::Blowfish) perl(FreezeThaw) perl(Compress::Zlib)
BuildRequires:  perl(ExtUtils::MakeMaker) perl(Test::Simple)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This little module will convert all your data into nice base64 text that
you can save in a text file, send in an email, store in a cookie or web
page, or bounce around the Net. The data you encrypt can be as simple or
as complicated as you like.

%prep
%setup -q -n Crypt-Simple-%{version}


%build
# Remove OPTIMIZE=... from noarch packages (unneeded)
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
# Remove the next line from noarch packages (unneeded)
#find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README
# For noarch packages: vendorlib
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.06-16
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.06-15
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-13
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-11
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-10
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.06-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild


* Fri Jan 23 2009 Allisson Azevedo <allisson@gmail.com> 0.06-7
- Rebuild

* Mon Jul 07 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.06-6
- fix conditional comparison

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.06-5
- Rebuild for new perl

* Mon Jul 9 2007 Allisson Azevedo <allisson@gmail.com> 0.06-4
- Add exception for FC-6

* Mon Jun 25 2007 Allisson Azevedo <allisson@gmail.com> 0.06-3
- Remove perl-Test-Simple and perl-ExtUtils-MakeMaker

* Sat Jun 23 2007 Allisson Azevedo <allisson@gmail.com> 0.06-2
- Add missing buildrequires

* Mon Jun 11 2007 Allisson Azevedo <allisson@gmail.com> 0.06-1
- Initial RPM release
