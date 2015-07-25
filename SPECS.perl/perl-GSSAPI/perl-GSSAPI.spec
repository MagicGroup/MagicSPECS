#
# Rebuild option:
#
#   --with testsuite         - run the test suite
#

Name:           perl-GSSAPI
Version:        0.28
Release:        8%{?dist}
Summary:        Perl extension providing access to the GSSAPIv2 library
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/GSSAPI/
Source0:        http://www.cpan.org/authors/id/A/AG/AGROLMS/GSSAPI-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  krb5-devel
BuildRequires:  which
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Pod) >= 1.00
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module gives access to the routines of the GSSAPI library, as
described in rfc2743 and rfc2744 and implemented by the Kerberos-1.2
distribution from MIT.

%prep
%setup -q -n GSSAPI-%{version}
chmod -c a-x examples/*.pl

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
# fails a couple of tests if network not available
%{?_with_testsuite:}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README examples/
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/GSSAPI*
%{_mandir}/man3/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.28-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.28-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.28-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.28-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 27 2010 Steven Pritchard <steve@kspei.com> 0.28-1
- Update to 0.28.

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.26-7
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Jun  3 2010 Petr Pisar <ppisar@redhat.com> - 0.26-6
- Do not source /etc/profile.d/krb5-devel.sh as krb5-devel-1.8.1-6 does not
  provide it and places executables into standard PATH.

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.26-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.26-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 15 2008 Steven Pritchard <steve@kspei.com> 0.26-1
- Update to 0.26.
- Cleanup a little to more closely match cpanspec output.
- BR ExtUtils::MakeMaker.

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.24-6
- rebuild for new perl (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.24-5
- Autorebuild for GCC 4.3

* Thu Feb 07 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.24-4
- rebuild for new perl

* Thu Jan 03 2008 Steven Pritchard <steve@kspei.com> 0.24-3
- Use sysconfdir macro instead of hard-coding /etc.

* Sat Dec 08 2007 Steven Pritchard <steve@kspei.com> 0.24-2
- Update License tag.
- Use fixperms macro instead of our own chmod incantation.
- Source in /etc/profile.d/krb5-devel.sh to get our path right.

* Thu Feb 22 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.24-1
- Update to 0.24.

* Sun Sep 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-2
- Rebuild for FC6.

* Thu Aug  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-1
- Update to 0.23.

* Mon May 29 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-1
- Update to 0.22.

* Thu Apr  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-1
- Update to 0.21.

* Fri Mar 31 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-1
- First build.
