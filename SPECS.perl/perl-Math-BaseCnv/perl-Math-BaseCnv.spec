Name:           perl-Math-BaseCnv
Version:        1.8.B59BrZX
Release:        7%{?dist}
Summary:        Fast functions to CoNVert between number Bases

Group:          Development/Libraries
License:        GPLv2
URL:            http://search.cpan.org/dist/Math-BaseCnv
Source0:        http://search.cpan.org/CPAN/authors/id/P/PI/PIP/Math-BaseCnv-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
BaseCnv provides a few simple functions for converting between arbitrary
number bases. It is as fast as I currently know how to make it (of course
relying only on the lovely Perl). If you would rather utilize an object syntax
for number-base conversion, please see Ken Williams's
<Ken@Forum.Swarthmore.Edu> fine Math::BaseCalc module.


%prep
%setup -q -n Math-BaseCnv-%{version}


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
%doc CHANGES README ex
%{perl_vendorlib}/*
%{_mandir}/man3/Math::BaseCnv.3pm.*
%{_bindir}/cnv


%changelog
* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 1.8.B59BrZX-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.8.B59BrZX-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.8.B59BrZX-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.8.B59BrZX-4
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.B59BrZX-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.8.B59BrZX-2
- Perl mass rebuild

* Thu May 12 2011 Xavier Bachelot <xavier@bachelot.org> - 1.8.B59BrZX-1
- Update to 1.8.B59BrZX
.
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.A6FGHKE-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.6.A6FGHKE-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Dec 17 2010 Xavier Bachelot <xavier@bachelot.org> - 1.6.A6FGHKE-1
- Update to latest version.

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.4.75O6Pbr-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.4.75O6Pbr-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.75O6Pbr-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.75O6Pbr-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.7506Pbr-3
- rebuild for new perl

* Fri Dec 21 2007 Xavier Bachelot <xavier@bachelot.org> - 1.4.75O6Pbr-2
- Clean up spec.

* Thu Aug 30 2007 Xavier Bachelot <xavier@bachelot.org> - 1.4.75O6Pbr-1
- Initial build.
