Name:           perl-Any-Moose
Summary:        Use Moose or Mouse automagically (DEPRECATED)
Summary(zh_CN.UTF-8): 自动化使用 Moose 或 Mouse（已过时）
Version:	0.26
Release:	3%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Any-Moose-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Any-Moose
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Moose)
BuildRequires:  perl(Mouse) >= 0.40
# MouseX::Types requires Any::Moose
%if !0%{?perl_bootstrap}
BuildRequires:  perl(MouseX::Types)
%endif
BuildRequires:  perl(Test::More)

# virtual provides in perl-Moose and perl-Mouse
Requires:       perl(Any-Moose) >= 0.40

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.18-2
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
Any::Moose is deprecated - please use Moo for new code.

This module allows one to take advantage of the features Moose/Mouse
provides, while allowing one to let the program author determine if Moose
or Mouse should be used; when use'd, we load Mouse if Moose isn't already
loaded, otherwise we go with Moose.

%description -l zh_CN.UTF-8
自动化使用 Moose 或 Mouse（已过时）。

%prep
%setup -q -n Any-Moose-%{version}

# silence rpmlint warnings
sed -i '1s,#!.*perl,#!%{__perl},' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh

%check
make test

%files
%doc Changes LICENSE README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.26-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.26-2
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 0.26-1
- 更新到 0.26

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.21-9
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.21-8
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.21-7
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 28 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.21-6
- Drop an extra dependency

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-5
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Petr Pisar <ppisar@redhat.com> - 0.21-4
- Perl 5.18 rebuild

* Sat Aug  3 2013 Jochen Schmitt <Jochen herr-schmitt de> - 0.21-3
- Rebuilt for perl-5.18.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 03 2013 Iain Arnell <iarnell@gmail.com> 0.21-1
- update to latest upstream version (still deprecated)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 31 2012 Iain Arnell <iarnell@gmail.com> 0.20-1
- update to latest upstream version which is deprecated in favor of perl-Moo

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.18-5
- Perl 5.16 re-rebuild of bootstrapped packages

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.18-4
- Perl 5.16 rebuild

* Fri Apr 06 2012 Iain Arnell <iarnell@gmail.com> 0.18-3
- avoid circular build-dependency with perl-MooseX-Types (patch from Paul
  Howarth rhbz#810521)

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.18-2
- drop tests-subpackage; move tests to main package documentation

* Fri Jan 13 2012 Robin Lee <cheeselee@fedoraproject.org> - 0.18-1
- Update to 0.18

* Sun Oct 09 2011 Iain Arnell <iarnell@gmail.com> 0.17-1
- update to latest upstream version
- require perl(Any-Moose) - provided by both perl-Moose and perl-Mouse

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.15-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.15-2
- Perl mass rebuild

* Sat Jul 02 2011 Iain Arnell <iarnell@gmail.com> 0.15-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Jun 27 2010 Iain Arnell <iarnell@gmail.com> 0.13-1
- update to latest upstream

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-2
- Mass rebuild with perl-5.12.0

* Mon Mar 01 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.11-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- altered br on perl(Mouse) (0.21 => 0.40)
- altered req on perl(Mouse) (0.21 => 0.40)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.10-2
- rebuild against perl 5.10.1

* Fri Jul 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- auto-update to 0.10 (by cpan-spec-update 0.01)
- altered req on perl(Mouse) (0.20 => 0.21)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 21 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- auto-update to 0.09 (by cpan-spec-update 0.01)
- altered br on perl(Mouse) (0.20 => 0.21)

* Sun May 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- submission

* Sun May 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.07-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
