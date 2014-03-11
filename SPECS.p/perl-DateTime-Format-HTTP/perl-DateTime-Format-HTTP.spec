Name:           perl-DateTime-Format-HTTP
Version:        0.40
Release:        8%{?dist}
Summary:        HTTP protocol date conversion routines

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/DateTime-Format-HTTP
Source0:        http://search.cpan.org/CPAN/authors/id/C/CK/CKRAS/DateTime-Format-HTTP-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl(Class::ISA)
BuildRequires:  perl(DateTime) >= 0.17
BuildRequires:  perl(HTTP::Date) => 1.44
BuildRequires:  perl(Test::More) >= 0.47
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(File::Find::Rule)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module provides functions that deal with the date formats used by the
HTTP protocol (and then some).


%prep
%setup -q -n DateTime-Format-HTTP-%{version}

# fix up crlf
sed -i -e 's/\r//' LICENSE README Changes CREDITS


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*


%check
# These will be VERY noisy.  Don't Panic.



%files
%defattr(-,root,root,-)
%doc LICENSE Changes CREDITS README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.40-8
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.40-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.40-4
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.40-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 18 2010 Iain Arnell <iarnell@gmail.com> 0.40-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- PERL_INSTALL_ROOT -> DESTDIR
- fix up crlf in docs

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.38-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.38-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.38-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.38-2
- rearrange the files in doc as the tarball has changed contents

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.38-1
- auto-update to 0.38 (by cpan-spec-update 0.01)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.37-3
- rebuild for new perl

* Thu Aug 31 2006 Chris Weyl <cweyl.drew.edu> 0.37-2
- bump for mass rebuild

* Wed Aug 09 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.37-1
- update to 0.37
- nix the SIGNATURE checking bits of the spec file as the author has dropped
  it from this version

* Sun Aug 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.36-3
- bump for build & release

* Sun Aug 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.36-2
- add missing buildrequires: perl(File::Find::Rule)

* Fri Aug 04 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.36-1
- Initial spec file for F-E
