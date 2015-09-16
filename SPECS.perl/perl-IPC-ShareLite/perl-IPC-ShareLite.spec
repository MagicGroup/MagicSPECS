Name:           perl-IPC-ShareLite
Version:        0.17
Release:        8%{?dist}
Summary:        Lightweight interface to shared memory
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/IPC-ShareLite/
Source0:        http://www.cpan.org/authors/id/A/AN/ANDYA/IPC-ShareLite-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
IPC::ShareLite provides a simple interface to shared memory, allowing
data to be efficiently communicated between processes.

%prep
%setup -q -n IPC-ShareLite-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/IPC*
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.17-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.17-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.17-5
- 为 Magic 3.0 重建

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.17-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.17-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Jun 25 2010 Xavier Bachelot <xavier@bachelot.org> 0.17-1
- Update to 0.17.

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.13-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 15 2008 Steven Pritchard <steve@kspei.com> 0.13-1
- Update to 0.13.
- Update Source0 URL.

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.12-1
- 0.12, works right now

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.09-12
- Autorebuild for GCC 4.3

* Wed Feb 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.09-11
- still not quite right on x86_64, but not segfaulting anymore.

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.09-10
- rebuild for new perl

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 0.09-9
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Mon Aug 28 2006 Steven Pritchard <steve@kspei.com> 0.09-8
- Rebuild.
- Fix find option order.
- Minor cleanup to more closely match cpanspec output.

* Sat Feb 18 2006 Steven Pritchard <steve@kspei.com> 0.09-7
- Rebuild.

* Mon Sep 05 2005 Steven Pritchard <steve@kspei.com> 0.09-6
- Cleanup (closer to current spec template).
- Include COPYING and Artistic.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Jun 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.09-0.fdr.4
- Avoid empty RPATHs.

* Mon May 10 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.09-0.fdr.3
- BuildRequire perl >= 1:5.6.1 for support for vendor installdirs.
- Use pure_install to avoid perllocal.pod workarounds.

* Mon Apr 26 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.09-0.fdr.2
- Reduce directory ownership bloat.
- Require perl(:MODULE_COMPAT_*).

* Tue Nov 18 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.09-0.fdr.1
- First build.
