Name:           perl-Devel-StackTrace
Summary:        Perl module implementing stack trace and stack trace frame objects
Version:        1.27
Epoch:          1
Release:        7%{?dist}
License:        Artistic 2.0
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Devel-StackTrace/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Devel-StackTrace-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# --with release_tests ... also check "RELEASE_TESTS".
# Disabled by default
%bcond_with release_tests

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Scalar::Util)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%if %{with release_tests}
# for improved tests
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(Test::Kwalitee)
BuildRequires:  perl(Test::EOL)
BuildRequires:  perl(Test::NoTabs)
BuildRequires:  perl(Test::Spelling)
BuildRequires:  aspell-en
%endif

%description
The Devel::StackTrace module contains two classes, Devel::StackTrace
and Devel::StackTraceFrame.  The goal of this object is to encapsulate
the information that can found through using the caller() function, as
well as providing a simple interface to this data.

The Devel::StackTrace object contains a set of Devel::StackTraceFrame
objects, one for each level of the stack.  The frames contain all the
data available from caller() as of Perl 5.6.0.

%prep
%setup -q -n Devel-StackTrace-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
 %{?with_release_tests:RELEASE_TESTING=1}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README LICENSE Changes
%{perl_vendorlib}/Devel
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1:1.27-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 1:1.27-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.27-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1:1.27-1
- Upstream update.

* Wed Nov 03 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1:1.26-1
- Upstream update.

* Sun Sep 12 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1:1.25-1
- Upstream update.
- Spec overhaul.
- Add %%bcond_with release_tests

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.22-5
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.22-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:1.22-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1:1.22-1
- Upstream update.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1:1.20-2
- BR: perl(Test::Kwalitee).

* Sat Dec 13 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 1:1.20-1
- Upstream update.
- Bump epoch.

* Fri Aug 08 2008 Ralf Corsépius <rc040203@freenet.de> - 1.1902-1
- Upstream update.

* Wed Jun 25 2008 Ralf Corsépius <rc040203@freenet.de> - 1.1901-1
- Upstream update.

* Fri May 16 2008 Ralf Corsépius <rc040203@freenet.de> - 1.18-2
- Bump release.

* Mon Apr 07 2008 Ralf Corsépius <rc040203@freenet.de> - 1.18-1
- Upstream update.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.16-2
- Rebuild for perl 5.10 (again)

* Sun Feb 03 2008 Ralf Corsépius <rc040203@freenet.de> - 1.16-1
- Upstream update.
- Activate IS_MAINTAINER-tests.
- BR: perl(Test::Pod::Coverage).

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-3
- rebuild for new perl

* Wed Aug 29 2007 Ralf Corsépius <rc040203@freenet.de> - 1.15-2
- Update License.

* Mon Apr 30 2007 Ralf Corsépius <rc040203@freenet.de> - 1.15-1
- Upstream update.

* Sat Mar 17 2007 Ralf Corsépius <rc040203@freenet.de> - 1.14-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.13-2
- Mass rebuild.

* Wed Apr 04 2006 Ralf Corsépius <rc040203@freenet.de> - 1.13-1
- Upstream update.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 1.12-2
- Rebuild for perl-5.8.8.

* Sun Oct 02 2005 Ralf Corsepius <rc040203@freenet.de> - 1.12-1
- Upstream update.
