Name:           perl-HTML-Mason
Version:	1.56
Release:	1%{?dist}
Epoch:          1
Summary:        Powerful Perl-based web site development and delivery engine
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://www.masonhq.com/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/HTML-Mason-%{version}.tar.gz
Source1:        perl-HTML-Mason.conf

BuildArch:      noarch
BuildRequires:  perl(Cache::Cache) >= 1
BuildRequires:  perl(CHI) >= 0.21
BuildRequires:  perl(CGI) >= 2.46
BuildRequires:  perl(Class::Container) >= 0.07
BuildRequires:  perl(Exception::Class) >= 1.15
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(Log::Any) >= 0.08
BuildRequires:  perl(mod_perl2)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Params::Validate) >= 0.7
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Memory::Cycle)
BuildRequires:  perl(Test::Pod) >= 1.20
Requires:       perl(Cache::Cache) >= 1
Requires:       perl(Class::Container) >= 0.07
Requires:       perl(Exception::Class) >= 1.15
Requires:       perl(Params::Validate) >= 0.7
Requires:       perl(mod_perl2)
Requires:       perl(HTML::Entities)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       %{_sysconfdir}/httpd/conf.d

%{?perl_default_filter}

%description
Mason is a powerful Perl-based web site development and delivery
engine. With Mason you can embed Perl code in your HTML and construct
pages from shared, reusable components.  Mason solves the common
problems of site development: caching, debugging, templating,
maintaining development and production sites, and more.

%prep
%setup -q -n HTML-Mason-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} $RPM_BUILD_ROOT/*

rm -f $RPM_BUILD_ROOT%{_bindir}/*.README
for file in $RPM_BUILD_ROOT%{_bindir}/convert*.pl ; do
    mv -f $file $( echo $file | sed 's,/\(convert.*\)\.pl$,/mason_\1,' )
done
mv -f $RPM_BUILD_ROOT%{_bindir}/mason.pl $RPM_BUILD_ROOT%{_bindir}/mason

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d
install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/

# Apache:: (Apache1) module
# Not applicable on Fedora.
rm -rf $RPM_BUILD_ROOT%{perl_vendorlib}/HTML/Mason/Apache

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/www/mason
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/mason

%check
make test

%files
%doc Changes CREDITS LICENSE README.md UPGRADE
%doc eg/ samples/
%{_bindir}/mason*
%{perl_vendorlib}/*
%{_mandir}/man3/*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/perl-HTML-Mason.conf
%dir %attr(775,root,apache) %{_localstatedir}/cache/mason
%dir %{_localstatedir}/www/mason


%changelog
* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 1:1.56-1
- 更新到 1.56

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1:1.48-13
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1:1.48-12
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1:1.48-11
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1:1.48-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1:1.48-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1:1.48-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:1.48-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:1.48-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:1.48-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:1.48-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 04 2012 Petr Pisar <ppisar@redhat.com> - 1:1.48-2
- Perl 5.16 rebuild

* Sun Feb 05 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1:1.48-1
- Upstream update.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 26 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1:1.47-1
- Upstream update.
- Spec file cleanup.

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1:1.45-7
- Perl mass rebuild

* Fri Apr 08 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1:1.45-6
- Add optional testsuite requirement perl(CHI). 

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.45-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 04 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1:1.45-4
- Fix spec-file typo.
- Add commented-out BR: perl(CHI).

* Thu Feb 04 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1:1.45-3
- Remove %%{perl_vendorlib}/HTML/Mason/Apache/.
- Re-activate testsuite.

* Thu Feb 03 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1:1.45-2
- Rebuild package (Was missing in rawhide).
- Switch to using perl_default_filter.
- Add explicit Require:/Provides: config(perl-HTML-Mason) to work-around
  https://bugzilla.redhat.com/show_bug.cgi?id=674765.

* Fri Dec 17 2010 Steven Pritchard <steve@kspei.com> 1:1.45-1
- Update to 1.45.
- Drop build.patch (now in the upstream release).
- BR CGI, Log::Any, and Test::Deep.

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.42-6
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.42-5
- switch off test for meantime, before update of this package

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.42-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:1.42-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 10 2009 Steven Pritchard <steve@kspei.com> 1:1.42-1
- Update to 1.42.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Aug 02 2008 Steven Pritchard <steve@kspei.com> 1:1.40-1
- Update to 1.40.
- BR Test::Builder.

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:1.39-2
- rebuild for new perl

* Wed Jan 30 2008 Steven Pritchard <steve@kspei.com> 1:1.39-1
- Update to 1.39.

* Mon Jan 07 2008 Steven Pritchard <steve@kspei.com> 1:1.38-1
- Update to 1.38.
- Update License tag.

* Mon Sep 17 2007 Steven Pritchard <steve@kspei.com> 1:1.37-1
- Update to 1.37.

* Tue Jun 26 2007 Steven Pritchard <steve@kspei.com> 1:1.36-1
- Update to 1.36.
- BR Test::Pod.

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 1:1.35-2
- Rebuild.

* Tue Oct 17 2006 Steven Pritchard <steve@kspei.com> 1:1.35-1
- Update to 1.35.
- BR Test::Memory::Cycle for better test coverage.

* Mon Oct 16 2006 Steven Pritchard <steve@kspei.com> 1:1.34-1
- Update to 1.34.
- Use fixperms macro instead of our own chmod incantation.
- Reformat a bit to more closely resemble current cpanspec output.
- Rename filter-*.sh to HTML-Mason-filter-*.sh.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 1:1.33-3
- Fix find option order.

* Thu Jun 08 2006 Steven Pritchard <steve@kspei.com> 1:1.33-2
- Add explicit dependency on HTML::Entities

* Mon May 29 2006 Steven Pritchard <steve@kspei.com> 1:1.33-1
- Update to 1.33
- Switch to Module::Build-based build
- Add various bindir mason scripts

* Thu Jan 19 2006 Steven Pritchard <steve@kspei.com> 1:1.32-2
- Epoch bump to resolve rpm thinking 1.3101 > 1.32

* Tue Jan 10 2006 Steven Pritchard <steve@kspei.com> 1.32-1
- Update to 1.32

* Thu Sep 15 2005 Steven Pritchard <steve@kspei.com> 1.3101-3
- Filter bogus provides/requires introduced by eg/ and samples/

* Thu Sep 15 2005 Steven Pritchard <steve@kspei.com> 1.3101-2
- More spec cleanup (jpo)

* Mon Aug 29 2005 Steven Pritchard <steve@kspei.com> 1.3101-1
- Update to 1.3101
- Spec cleanup (jpo)
- Include sample config file from Chris Grau

* Wed Aug 24 2005 Steven Pritchard <steve@kspei.com> 1.31-3
- Use /var/www/mason instead of /var/www/comp
- Spec cleanup

* Tue Aug 23 2005 Steven Pritchard <steve@kspei.com> 1.31-2
- Add some missing dependencies

* Tue Aug 23 2005 Steven Pritchard <steve@kspei.com> 1.31-1
- Update to 1.31
- Use /var/cache/mason instead of /var/www/mason
- Fix perl-HTML-Mason.conf
- Fix URL

* Thu Aug 11 2005 Steven Pritchard <steve@kspei.com> 1.30-1
- Specfile autogenerated.
- Add perl-HTML-Mason.conf and /var/www/*
