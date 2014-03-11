Name: 		perl-File-Flat
Version: 	1.04
Release: 	13%{?dist}
Summary: 	Implements a flat filesystem
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/File-Flat/
Source0: 	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/File-Flat-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: 	noarch

BuildRequires: perl(ExtUtils::AutoInstall) >= 0.49
BuildRequires: perl(Test::More) >= 0.47
BuildRequires: perl(Test::ClassAPI) >= 1.02
BuildRequires: perl(File::Find)
BuildRequires: perl(prefork) >= 0.02
BuildRequires: perl(File::Spec) >= 0.85
BuildRequires: perl(File::Copy)
BuildRequires: perl(File::Copy::Recursive)
BuildRequires: perl(File::Remove) >= 0.21
BuildRequires: perl(File::Temp) >= 0.17
BuildRequires: perl(IO::File)

# For improved tests
BuildRequires: perl(Test::Pod)
BuildRequires: perl(Test::MinimumVersion)
BuildRequires: perl(Test::CPAN::Meta)

%description
File::Flat implements a flat filesystem. A flat filesystem is a filesystem
in which directories do not exist. It provides an abstraction over any 
normal filesystem which makes it appear as if directories do not exist.

%prep
%setup -q -n File-Flat-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%clean
rm -rf $RPM_BUILD_ROOT

%check
# remove until fix of Perl::MinimalVersion and version.pm
rm -rf t/99_pmv.t

 AUTOMATED_TESTING=1

%files
%defattr(-,root,root,-)
%doc Changes README LICENSE
%{perl_vendorlib}/File
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.04-13
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 1.04-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.04-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.04-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.04-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.04-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 01 2008 Ralf Corsépius <rc040203@freenet.de> - 1.04-2
- BR: perl(Test::CPAN::Meta).

* Mon Apr 07 2008 Ralf Corsépius <rc040203@freenet.de> - 1.04-1
- Upstream update.
- Remove dep on perl(File::Slurp).

* Fri Mar 14 2008 Ralf Corsépius <rc040203@freenet.de> - 1.03-1
- Upstream update.
- BR: perl(Test::MinimumVersion).

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.00-3
- rebuild for new perl

* Sun Sep 02 2007 Ralf Corsépius <rc040203@freenet.de> - 1.00-2
- License update.

* Thu Jan 18 2007 Ralf Corsépius <rc040203@freenet.de> - 1.00-1
- Upstream update.
- BR: perl(File::Copy::Recursive).
- Drop BR: perl(File::NCopy).
- Activate AUTOMATED_TESTING (t/99_author.t).

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.96-3
- Mass rebuild.

* Thu Jul 20 2006 Ralf Corsépius <rc040203@freenet.de> - 0.96-2
- BR: perl(Test::Pod).

* Thu Jul 20 2006 Ralf Corsépius <rc040203@freenet.de> - 0.96-1
- Upstream update.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 0.95-3
- Rebuild for perl-5.8.8.

* Mon Sep 19 2005 Ralf Corsepius <rc040203@freenet.de> - 0.95-2
- Spec file cleanup.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 0.95-1
- Spec file cleanup.
- FE submission.

* Tue Jun 28 2005 Ralf Corsepius <ralf@links2linux.de> - 0.95-0.pm.1
- Initial packman version.
