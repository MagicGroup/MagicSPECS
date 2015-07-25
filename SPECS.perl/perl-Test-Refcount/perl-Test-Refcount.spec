Name:           perl-Test-Refcount
Version:        0.07
Release:        14%{?dist}
Summary:        Assert reference counts on objects

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Test-Refcount/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PEVANS/Test-Refcount-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Devel::Refcount)
BuildRequires:  perl(Devel::FindRef)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The Perl garbage collector uses simple reference counting during the normal
execution of a program. This means that cycles or unweakened references in
other parts of code can keep an object around for longer than intended. To
help avoid this problem, the reference count of a new object from its class
constructor ought to be 1. This way, the caller can know the object will be
properly DESTROYed when it drops all of its references to it.


%prep
%setup -q -n Test-Refcount-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'

%{_fixperms} $RPM_BUILD_ROOT/*


%check


%files
%doc Changes LICENSE README
%{perl_vendorlib}/Test
%{_mandir}/man3/Test*.3*


%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.07-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.07-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.07-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.07-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.07-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.07-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.07-8
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.07-6
- Perl 5.16 rebuild

* Sun Apr 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.07-5
- Rebuilt for f17

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Petr Sabata <contyk@redhat.com> - 0.07-2
- Perl mass rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.07-1
- update to 0.07

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-5
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-2
- Mass rebuild with perl-5.12.0

* Sun Dec 27 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.06-1
- Update to 0.06
- Remove workaround at  for perl with debug - rhbz#514942

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.05-3
- rebuild against perl 5.10.1

* Fri Jul 31 2009 kwizart < kwizart at gmail.com > - 0.05-2
- Add missing BR
- Use %%{_fixperms}
- Fix %%files section
- Add comment about why it fails

* Thu Jul  9 2009 kwizart < kwizart at gmail.com > - 0.05-1
- Initial spec

