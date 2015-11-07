Name:           perl-Class-Inner
Version:        0.200001
Release:        11%{?dist}
Summary:        A perlish implementation of Java like inner classes

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Class-Inner/
SOurce0:        http://search.cpan.org/CPAN/authors/id/A/AR/ARUNBEAR/Class-Inner-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Yet another implementation of an anonymous class with per object overrideable
methods, but with the added attraction of sort of working dispatch to the
parent class's method.


%prep
%setup -q -n Class-Inner-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.200001-11
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.200001-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.200001-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.200001-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.200001-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.200001-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.200001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.200001-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.200001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.200001-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Jul  1 2010 Xavier Bachelot <xavier@bachelot.org> - 0.200001-1
- Update to 0.200001.

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.1-10
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.1-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.1-6
- fix test for perl 5.10

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.1-5
- rebuild for new perl

* Thu Dec 20 2007 Xavier Bachelot <xavier@bachelot.org> - 0.1-4
- Remove unneeded comment.
- Import into Fedora.

* Thu Dec 20 2007 Xavier Bachelot <xavier@bachelot.org> - 0.1-3
- Fix Summary, License and URL.
- Use %%{version} macro in Source.
- Properly own directory.

* Thu Dec 20 2007 Xavier Bachelot <xavier@bachelot.org> - 0.1-2
- Add missing BR:

* Tue Dec 11 2007 Xavier Bachelot <xavier@bachelot.org> - 0.1-1
- Initial build.
