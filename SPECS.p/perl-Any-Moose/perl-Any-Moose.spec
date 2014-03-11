Name:           perl-Any-Moose
Summary:        Use Moose or Mouse automagically
Version:        0.18
Release:        6%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/S/SA/SARTAK/Any-Moose-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Any-Moose
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Moose)
BuildRequires:  perl(MooseX::Types)
BuildRequires:  perl(Mouse) >= 0.40
BuildRequires:  perl(MouseX::Types)
BuildRequires:  perl(Test::More)

# virtual provides in perl-Moose and perl-Mouse
Requires:       perl(Any-Moose) >= 0.40

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.18-2
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
This module allows one to take advantage of the features Moose/Mouse
provides, while allowing one to let the program author determine if Moose
or Mouse should be used; when use'd, we load Mouse if Moose isn't already
loaded, otherwise we go with Moose.

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

%check


%files
%doc Changes LICENSE README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.18-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.18-5
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.18-4
- 为 Magic 3.0 重建

* Fri Jan 27 2012 Liu Di <liudidi@gmail.com> - 0.18-3
- 为 Magic 3.0 重建

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
