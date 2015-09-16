Name: 		perl-prefork
Version: 	1.04
Release: 	11%{?dist}
Summary: 	Optimized module loading for forking or non-forking processes
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/prefork/
Source0: 	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/prefork-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: noarch

BuildRequires: perl(Test::More) >= 0.47
BuildRequires: perl(File::Spec) >= 0.80
BuildRequires: perl(List::Util) >= 0.18
BuildRequires: perl(Scalar::Util) >= 1.18

# Required by tests
BuildRequires: perl(Test::Pod) >= 1.00
BuildRequires: perl(Test::MinimumVersion) >= 0.007
BuildRequires: perl(Perl::MinimumVersion) >= 1.20
BuildRequires: perl(Test::CPAN::Meta) >= 0.12

%description
Optimized module loading for forking or non-forking processes

prefork.pm is intended to serve as a central and optional marshalling
point for state detection (are we running in compile-time or run-time
mode) and to act as a relatively light-weight module loader.

%prep
%setup -q -n prefork-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%check
 AUTOMATED_TESTING=1

%files
%defattr(-,root,root,-)
%doc Changes README LICENSE
%{perl_vendorlib}/prefork*
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.04-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.04-10
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.04-9
- 为 Magic 3.0 重建

* Fri Oct 19 2012 Liu Di <liudidi@gmail.com> - 1.04-8
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.04-6
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.04-4
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.04-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.04-2
- rebuild against perl 5.10.1

* Wed Jul 29 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.04-1
- Upstream update.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.03-1
- Upstream update.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.02-2
- rebuild for new perl

* Sun Nov 25 2007 Ralf Corsépius <rc040203@freenet.de> - 1.02-1
- Upstream update.
- Add BR: perl(Test::MinimumVersion).

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 1.01-3
- Update license tag.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.01-2
- Mass rebuild.

* Mon Aug 07 2006 Ralf Corsépius <rc040203@freenet.de> - 1.01-1
- Upstream update.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 1.00-3
- Rebuild for perl-5.8.8.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 1.00-2
- Spec file cleanup.

* Sat Sep 10 2005 Ralf Corsepius <rc040203@freenet.de> - 1.00-1
- FE submission.
