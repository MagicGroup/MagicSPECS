Name:           perl-autobox
Version:	2.83
Release:	1%{?dist}
Summary:        Call methods on native types
Summary(zh_CN.UTF-8): 以基本类型调用方法
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/autobox/
Source0:        http://www.cpan.org/authors/id/C/CH/CHOCOLATE/autobox-%{version}.tar.gz
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Scope::Guard) >= 0.20
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?filter_setup:
%filter_from_requires /perl(autobox::universal)/d
%?perl_default_filter
}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(autobox::universal\\)

%description
The autobox pragma allows methods to be called on integers, floats,
strings, arrays, hashes, and code references in exactly the same manner as
blessed references.

%description -l zh_CN.UTF-8
以基本类型调用方法。

%prep
%setup -q -n autobox-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh


%check


%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/autobox*
%{_mandir}/man3/*

%changelog
* Fri Apr 17 2015 Liu Di <liudidi@gmail.com> - 2.83-1
- 更新到 2.83

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.75-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.75-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.75-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.75-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.75-4
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 2.75-3
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Aug 14 2011 Iain Arnell <iarnell@gmail.com> 2.75-1
- update to latest upstream version

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> 2.73-3
- update filters for rpm 4.9

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.73-2
- Perl mass rebuild

* Sat May 07 2011 Iain Arnell <iarnell@gmail.com> 2.73-1
- update to latest upstream version

* Sat Feb 19 2011 Iain Arnell <iarnell@gmail.com> 2.71-3
- update requires filtering to use standard macros

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Iain Arnell <iarnell@gmail.com> 2.71-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.55-6
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.55-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.55-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.55-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Allisson Azevedo <allisson@gmail.com> 2.55-1
- Initial rpm release.
