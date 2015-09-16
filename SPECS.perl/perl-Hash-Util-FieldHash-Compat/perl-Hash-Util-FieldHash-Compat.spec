Name:		perl-Hash-Util-FieldHash-Compat
Version:	0.09
Release:	1%{?dist}
Summary:	Use Hash::Util::FieldHash or ties, depending on availability
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Hash-Util-FieldHash-Compat/
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Hash-Util-FieldHash-Compat-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Test::use::ok)
BuildRequires:	perl(Tie::RefHash)
BuildRequires:	perl(Tie::RefHash::Weak)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Filter unversioned provide, leaving just the versioned one (rpm 4.9 onwards)
%global __provides_exclude ^perl\\(Hash::Util::FieldHash::Compat\\)$

%description
Under older perls this module provides a drop in compatible API to
Hash::Util::FieldHash using perltie. When Hash::Util::FieldHash is
available, it will use that instead.

%prep
%setup -q -n Hash-Util-FieldHash-Compat-%{version}

# Filter unversioned provide, leaving just the versioned one (prior to rpm 4.9)
%global provfilt /bin/sh -c "%{__perl_provides} | grep -Fvx 'perl(Hash::Util::FieldHash::Compat)'"
%define __perl_provides %{provfilt}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \; 2>/dev/null
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/Hash/
%{_mandir}/man3/Hash::Util::FieldHash::Compat.3pm*
%{_mandir}/man3/Hash::Util::FieldHash::Compat::Heavy.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.09-1
- 更新到 0.09

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.03-23
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.03-22
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.03-21
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.03-20
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.03-19
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.03-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.03-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.03-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.03-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.03-14
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.03-13
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.03-12
- 为 Magic 3.0 重建

* Mon Jan 23 2012 Paul Howarth <paul@city-fan.org> - 0.03-11
- Spec clean-up
  - BR: perl(Scalar::Util), perl(Tie::RefHash) and perl(Tie::RefHash::Weak)
  - Make %%files list more explicit
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Don't use macros for commands
  - Use search.cpan.org source URL

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.03-9
- Perl mass rebuild

* Wed May  4 2011 Paul Howarth <paul@city-fan.org> - 0.03-8
- Fix provides filter for rpm 4.9.x and filter the unversioned provide rather
  than the versioned one

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.03-4
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 29 2009 Allisson Azevedo <allisson@gmail.com> - 0.03-1
- Initial rpm release
