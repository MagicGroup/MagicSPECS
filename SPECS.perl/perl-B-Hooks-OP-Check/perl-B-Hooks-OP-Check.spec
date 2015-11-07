Name:           perl-B-Hooks-OP-Check
Summary:        Wrap OP check callbacks
Summary(zh_CN.UTF-8): OP 检查回退的接口
Version:        0.19
Release:        16%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Source0:        http://search.cpan.org/CPAN/authors/id/Z/ZE/ZEFRAM/B-Hooks-OP-Check-%{version}.tar.gz
URL:            http://search.cpan.org/dist/B-Hooks-OP-Check
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(ExtUtils::Depends) >= 0.302
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(parent)
BuildRequires:  perl(Test::More)

Requires:       perl(parent)

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.19-3
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
This module provides a C API for XS modules to hook into the callbacks
of 'PL_check'.

%description -l zh_CN.UTF-8
OP 检查回退的接口。

%prep
%setup -q -n B-Hooks-OP-Check-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh

%check


%files
%doc Changes README t/
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto
%{_mandir}/man3/*.3*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.19-16
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.19-15
- 为 Magic 3.0 重建

* Fri Apr 24 2015 Liu Di <liudidi@gmail.com> - 0.19-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.19-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.19-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.19-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.19-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.19-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.19-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.19-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.19-6
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.19-4
- Perl 5.16 rebuild

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.19-3
- drop old tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 23 2011 Iain Arnell <iarnell@gmail.com> 0.19-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.18-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-2
- Mass rebuild with perl-5.12.0

* Sun Feb 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.18-1
- auto-update by cpan-spec-update 0.002
- altered br on perl(ExtUtils::Depends) (0 => 0.302)
- added a new req on perl(parent) (version 0)
- PERL_INSTALL_ROOT => DESTDIR

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.17-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.17-1
- auto-update to 0.17 (by cpan-spec-update 0.01)

* Sat Apr 18 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.15-1
- submission

* Sat Apr 18 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.15-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
