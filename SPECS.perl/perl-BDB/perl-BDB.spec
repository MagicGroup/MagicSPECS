%global cpan_version 1.9

Name:           perl-BDB
# Extend to 2 digits to get higher RPM package version than 1.88
Version:	1.91
Release:	3%{?dist}
Summary:        Asynchronous Berkeley DB access
Summary(zh_CN.UTF-8): 异步的伯克利 DB 访问

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/BDB/
Source0:        http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/BDB-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(base)
BuildRequires:  perl(common::sense)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(XSLoader)
BuildRequires:  libdb-devel
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:  perl(XSLoader)

%{?perl_default_filter}

%description
Asynchronous Berkeley DB access.

%description -l zh_CN.UTF-8
异步的伯克利 DB 访问。

%prep
%setup -q -n BDB-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes COPYING README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/BDB.pm
%{_mandir}/man3/*.3*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.91-3
- 为 Magic 3.0 重建

* Fri Apr 24 2015 Liu Di <liudidi@gmail.com> - 1.91-2
- 为 Magic 3.0 重建

* Fri Apr 24 2015 Liu Di <liudidi@gmail.com> - 1.91-1
- 更新到 1.91

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.90-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.90-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.90-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.90-2
- Perl 5.16 rebuild

* Thu Apr 19 2012 Petr Pisar <ppisar@redhat.com> - 1.90-1
- 1.9 bump
- Use Berkeley database version 5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.88-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.88-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.88-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.88-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Aug 22 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.88-1
- Update to 1.88

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.87-2
- Mass rebuild with perl-5.12.0

* Tue Jan 19 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.87-1
- Update to 1.87
- Drop patch BDB-1.86-db_48

* Sun Dec 13 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.86-3
- Drop Patch0

* Tue Dec 8 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.86-2
- Patch to force db 4.8.

* Mon Dec 7 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.86-1
- Update to 1.86

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.84-2
- rebuild against perl 5.10.1

* Mon Aug 31 2009 kwizart < kwizart at gmail.com > - 1.84-1
- Update to 1.84
- Add Patch to get rid of common:sense

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb  3 2009 kwizart < kwizart at gmail.com > - 1.83-1
- Update to 1.83

* Wed Jan  7 2009 kwizart < kwizart at gmail.com > - 1.82-1
- Update to 1.82

* Fri Nov 28 2008 kwizart < kwizart at gmail.com > - 1.81-1
- Update to 1.81

* Thu Jul 17 2008 kwizart < kwizart at gmail.com > - 1.7-1
- Update to 1.7

* Tue May 27 2008 kwizart < kwizart at gmail.com > - 1.5-1
- Update to 1.5

* Wed Apr 30 2008 kwizart < kwizart at gmail.com > - 1.45-1
- Initial package for Fedora
