Name:           perl-Config-Record
Version:        1.1.2
Release:        11%{?dist}
Summary:        Perl module for Configuration file access

Group:          Development/Libraries
License:        GPLv2+
URL:            http://search.cpan.org/dist/Config-Record/
Source:         http://www.cpan.org/authors/id/D/DA/DANBERR/Config-Record-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# for improved tests
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)


%description
Config::Record provides a module for loading configuration
records. It supports scalar, array and hash parameters nested
to an arbitrary depth.

%prep
%setup -q -n Config-Record-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES LICENSE README
%{perl_vendorlib}/Config/
%{_mandir}/man3/*.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.1.2-11
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.1.2-10
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1.2-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.1.2-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.1.2-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.1.2-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 23 2008 Ralf Corsépius <rc040203@freenet.de> - 1.1.2-1
- Upstream update.
- Minor spec cleanup.

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.1-4
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.1-3.2
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.1-3.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep 21 2006  <dgregor@redhat.com> - 1.1.1-3
- Add the %%{?dist} tag, general cleanup (bz #207548)

* Fri Sep 15 2006  <dgregor@redhat.com> - 1.1.1-2
- Rebuild for FC6

* Wed Aug  2 2006  <dgregor@redhat.com> - 1.1.1-1
- Update to 1.1.1

* Fri Apr 22 2005 Oliver Falk <oliver@linux-kernel.at>   - 1.1.0-1_FC4
- Make devel branch RPM newer than the one in FC3 tree, by adding FC4
  to the release tag

* Tue Apr  5 2005 Dennis Gregorovic <dgregor@redhat.com> - 1.1.0-1
- First build.
