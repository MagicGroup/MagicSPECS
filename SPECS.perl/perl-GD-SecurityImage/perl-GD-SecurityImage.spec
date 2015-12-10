Name:           perl-GD-SecurityImage
Version:	1.73
Release:	3%{?dist}
Summary:        Security image (captcha) generator
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/GD-SecurityImage/
Source0:        http://www.cpan.org/authors/id/B/BU/BURAK/GD-SecurityImage-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(GD)
BuildRequires:  perl(Image::Magick)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module gives you a basic interface to create "security images". Most
internet software use these in their registration screens to block robot
programs (which may register tons of fake member accounts). This module
gives you a basic interface to create such an image.

%prep
%setup -q -n GD-SecurityImage-%{version}
sed -i 's/\r//' LICENSE
iconv -f ISO-8859-1 -t UTF-8 README > README.UTF-8
mv -f README.UTF-8 README

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes eg LICENSE README SPEC StayPuft.ttf
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.73-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.73-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.73-1
- 更新到 1.73

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.72-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.72-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.72-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.72-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.72-3
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.72-2
- 为 Magic 3.0 重建

* Wed Aug 29 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 1.72-1
- Update to 1.72

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.71-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.71-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 05 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 1.71-1
- Update to 1.71
- Clean up spec file
- Add Test::Pod::Coverage as a BR to enable all tests

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.70-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.70-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Nov 23 2009 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> 1.70-1
- Specfile autogenerated by cpanspec 1.78.
