Name:           perl-Tk-Stderr
Version:        1.2
Release:        18%{?dist}
Summary:        Capture standard error output, display in separate window for Perl::Tk

Group:          Development/Libraries
License:        GPLv2+
URL:            http://search.cpan.org/dist/Tk-Stderr/
Source0:        http://cpan.org/modules/by-module/Tk/Tk-Stderr-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Tk)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  xorg-x11-server-Xvfb, xorg-x11-fonts-base
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module captures that standard error of a program and redirects it
to a read only text widget, which doesn't appear until necessary. When
it does appear, the user can close it; it'll appear again when there is
more output.

%prep
%setup -q -n Tk-Stderr-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check
# disabled by default because it needs an x screen
%{?_with_tests:}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README
%{perl_vendorlib}/Tk
%{_mandir}/man3/Tk*.3*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.2-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.2-17
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.2-16
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.2-14
- Perl 5.16 rebuild

* Tue Jan 17 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2-13
- Add BR: perl(ExtUtils::MakeMaker) (Fix mass rebuild FTBFS).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2-11
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2-9
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2-8
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.2-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 30 2009 David Hannequin <david.hannequin@gmail.com> 1.2-5
- delete _xvfb
- modify man page

* Tue May 19 2009 David Hannequin <david.hannequin@gmail.com> 1.2-4
- Fix build require
- Fix  ( need X screen )

* Sun May 17 2009 David Hannequin <david.hannequin@gmail.com> 1.2-2
- First release.
