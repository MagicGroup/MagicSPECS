Name:           perl-Proc-Wait3
Version:        0.04
Release:        11%{?dist}
Summary:        Perl extension for wait3 system call
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Proc-Wait3/
Source0:        http://www.cpan.org/authors/id/C/CT/CTILMES/Proc-Wait3-%{version}.tar.gz
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
If any child processes have exited, this call will "reap" the zombies
similar to the perl "wait" function.

%prep
%setup -q -n Proc-Wait3-%{version}
iconv -f ISO-8859-1 -t utf-8 < Changes > Changes~
mv Changes~ Changes

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%defattr(-,root,root,-)
%doc Changes README LICENSE
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Proc*
%{_mandir}/man3/*

%changelog
* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.04-11
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.04-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.04-5
- Perl 5.16 rebuild

* Sun Jan 22 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.04-4
- Modernize spec.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.04-2
- Perl mass rebuild

* Fri Feb 18 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.04-1
- Upstream update (License clarified).

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 09 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.03-2
- Add perl_default_filter.

* Wed Dec 22 2010 Ralf Corsépius <corsepiu@fedoraproject.org> 0.03-1
- Initial Fedora package.
