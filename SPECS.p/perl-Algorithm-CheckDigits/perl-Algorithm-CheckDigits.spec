Name:		perl-Algorithm-CheckDigits
Version:	0.53
Release:	7%{?dist}

Summary:	Perl extension to generate and test check digits

Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Algorithm-CheckDigits/
Source0:	http://search.cpan.org/CPAN/authors/id/M/MA/MAMAWE/Algorithm-CheckDigits-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(Test::Pod)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
This module provides a number of methods to test and generate check digits.


%prep
%setup -q -n Algorithm-CheckDigits-%{version}
cd CheckDigits
for i in M11_006 MBase_002 MXX_006 M11_004 MXX_003; do
  {
  iconv -f iso-8859-1 -t utf-8 -o $i.pm{.utf8,}
  mv $i.pm{.utf8,}
  };
done;


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/Algorithm::CheckDigits*3pm.gz


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.53-7
- 为 Magic 3.0 重建

* Fri Jan 27 2012 Liu Di <liudidi@gmail.com> - 0.53-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.53-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.53-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.53-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.53-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Jul 01 2010 Xavier Bachelot <xavier@bachelot.org> - 0.53-1
- Update to 0.53.

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.50-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.50-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 08 2008 Xavier Bachelot <xavier@bachelot.org> - 0.50-1
- Update to 0.50.

* Thu May 22 2008 Xavier Bachelot <xavier@bachelot.org> - 0.49-1
- Update to 0.49.

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.48-3
- Rebuild for new perl.

* Sat Jan 12 2008 Xavier Bachelot <xavier@bachelot.org> - 0.48-2
- Remove '|| :' from %%check section.

* Fri Dec 21 2007 Xavier Bachelot <xavier@bachelot.org> - 0.48-1
- Update to 0.48
- Clean up spec.

* Wed Oct 18 2006 Xavier Bachelot <xavier@bachelot.org> - 0.41-1
- Initial build.
