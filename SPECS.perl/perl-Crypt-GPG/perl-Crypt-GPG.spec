%define pkgname Crypt-GPG

Summary:	Perl Object Oriented Interface to GnuPG
Name:		perl-Crypt-GPG
Version:	1.63
Release:	17%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/%{pkgname}/
Source:		http://search.cpan.org/CPAN/authors/id/A/AG/AGUL/%{pkgname}-%{version}.tar.gz
Patch0:		perl-Crypt-GPG-1.63-fedora.patch
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version)), gnupg
BuildRequires:	perl(ExtUtils::MakeMaker), perl(IPC::Run), perl(Date::Parse), gnupg
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Crypt::GPG module provides access to the functionality of the
GnuPG (www.gnupg.org) encryption tool through an object oriented
interface. It provides methods for encryption, decryption, signing,
signature verification, key generation, key certification, export
and import.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1 -b .fedora

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT \( -name perllocal.pod -o -name .packlist \) -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README
%{perl_vendorlib}/Crypt
%{_mandir}/man3/Crypt::GPG.3pm*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.63-17
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.63-16
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.63-15
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.63-14
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.63-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.63-12
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.63-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Petr Pisar <ppisar@redhat.com> - 1.63-10
- Fix fedora patch

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.63-9
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.63-8
- Mass rebuild with perl-5.12.0

* Mon Jan 18 2010 Stepan Kasal <skasal@redhat.com> - 1.63-7
- re-enable tests

* Mon Jan 18 2010 Stepan Kasal <skasal@redhat.com> - 1.63-6
- rebuild against perl 5.10.1, temporarily disabling the tests, the
  package is known not to work with gnupg2, see #539150

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.63-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.63-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 01 2009 Robert Scheck <robert@fedoraproject.org> 1.63-3
- Changes to match with Fedora Packaging Guidelines (#503175)

* Mon Jun 01 2009 Robert Scheck <robert@fedoraproject.org> 1.63-2
- Enabled the %%check section (#503175 #c1)

* Fri May 29 2009 Robert Scheck <robert@fedoraproject.org> 1.63-1
- Upgrade to 1.63
- Initial spec file for Fedora and Red Hat Enterprise Linux
