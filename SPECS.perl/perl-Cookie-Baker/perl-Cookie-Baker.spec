Name:           perl-Cookie-Baker
Summary:        Cookie string generator / parser  
Version:	0.06
Release:	3%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/K/KA/KAZEBURO/Cookie-Baker-%{version}.tar.gz
URL:            http://search.cpan.org/dist/CGI
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch


%{?perl_default_filter}

%description
Cookie string generator / parser  

%prep
%setup -q -n Cookie-Baker-%{version}

# RPM 4.9 style
%global __provides_exclude %__provides_exclude|^perl\\(utf8\\)$

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT

./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.06-3
- 为 Magic 3.0 重建

* Fri Sep 18 2015 Liu Di <liudidi@gmail.com> - 0.06-2
- 为 Magic 3.0 重建

* Fri Sep 18 2015 Liu Di <liudidi@gmail.com> - 0.06-1
- 更新到 0.06

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 4.21-1
- 更新到 4.21

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.51-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 3.51-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 3.51-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.51-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 3.51-4
- RPM 4.9 dependency filtering added

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.51-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Marcela Mašláňová <mmaslano@redhat.com> 3.51-1
- update to fix CVE-2010-2761

* Mon Nov 29 2010 Marcela Mašláňová <mmaslano@redhat.com> 3.50-2
- remove -test sub-package, which would be needed also in perl-core

* Mon Nov 29 2010 Marcela Mašláňová <mmaslano@redhat.com> 3.50-1
- initial dual-life package

