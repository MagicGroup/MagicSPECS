Name: 		perl-File-NCopy
Version: 	0.36
Release: 	11%{?dist}
Summary:	Copy files to directories, or a single file to another file
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/File-NCopy/
Source0:        http://search.cpan.org/CPAN/authors/id/C/CH/CHORNY/File-NCopy-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: noarch

%description
File::NCopy copies files to directories, or a single file to another
file. The functionality is very similar to cp.

Deprecated module. Use only if required by other module.
You can use File::Copy::Recursive instead.

%prep
%setup -q -n File-NCopy-%{version}

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


%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorlib}/File
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.36-11
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.36-10
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.36-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.36-6
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.36-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.36-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Apr 07 2008 Ralf Corsépius <rc040203@freenet.de> - 0.36-1
- Upstream update.

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.35-4
Rebuild for new perl

* Wed Oct 24 2007 Ralf Corsépius <rc040203@freenet.de> - 0.35-3
- Add BR: perl(Test::Pod).

* Wed Oct 24 2007 Ralf Corsépius <rc040203@freenet.de> - 0.35-2
- Add BR: perl(Test::More).

* Sun Oct 21 2007 Ralf Corsépius <rc040203@freenet.de> - 0.35-1
- Upstream update.
- Reflect Source-URL having changed.

* Sun Sep 02 2007 Ralf Corsépius <rc040203@freenet.de> - 0.34-6
- Update license tag.
- BR: perl(ExtUtils::MakeMaker).

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.34-5
- Mass rebuild.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 0.34-4
- Rebuild for perl-5.8.8.

* Mon Sep 19 2005 Ralf Corsepius <rc040203@freenet.de> - 0.34-3
- Spec cleanup.

* Thu Sep 01 2005 Ralf Corsepius <rc040203@freenet.de> - 0.34-1
- FE submission.
