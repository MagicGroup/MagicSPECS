Name:       perl-asa 
Version:    1.03
Release:    9%{?dist}
# see lib/asa.pm
License:    GPL+ or Artistic
Group:      Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:    Lets your class/object say it works like something else 
Summary(zh_CN.UTF-8): 让你的类/对象像其它的东西一样工作
Source:     http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/asa-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/asa
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker) 
BuildRequires: perl(base)
BuildRequires: perl(Carp)
BuildRequires: perl(File::Spec) >= 0.80
BuildRequires: perl(File::Spec::Functions)
BuildRequires: perl(Test::More) >= 0.47
# optional tests
BuildRequires: perl(Test::Pod)


%description
Perl 5 doesn't natively support Java-style interfaces, and it doesn't
support Perl 6 style roles either.

You can get both of these things in half a dozen different ways via various
CPAN modules, but they usually require that you buy into "their way" of
implementing your code.

This package overrides the isa() method, allowing your class to claim it's a
class it's not (that is, isn't in @ISA).

%description -l zh_CN.UTF-8
让你的类/对象像其它的东西一样工作。

%prep
%setup -q -n asa-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh

%check


%files
%doc Changes LICENSE README 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.03-9
- 为 Magic 3.0 重建

* Fri Apr 17 2015 Liu Di <liudidi@gmail.com> - 1.03-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.03-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.03-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.03-5
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 1.03-4
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.03-2
- Perl mass rebuild

* Sat May 07 2011 Iain Arnell <iarnell@gmail.com> 1.03-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-7
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.02-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-2
- bump

* Tue Nov 18 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-1
-  brushup for submission

* Tue Nov 18 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)

