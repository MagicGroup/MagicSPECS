Name:           perl-libxml-perl
Version:        0.08
Release:        19%{?dist}
Summary:        A collection of Perl modules for working with XML

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/libxml-perl/
Source0:        http://www.cpan.org/authors/id/K/KM/KMACLEOD/libxml-perl-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(XML::Parser)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
libxml-perl is a collection of smaller Perl modules, scripts, and
documents for working with XML in Perl.  libxml-perl software works in
combination with XML::Parser, PerlSAX, XML::DOM, XML::Grove and
others.


%prep
%setup -q -n libxml-perl-%{version}

# Filter unwanted Provides:
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
  sed -e '/perl(Data::Grove)$/d'
EOF

%define __perl_provides %{_builddir}/libxml-perl-%{version}/%{name}-prov
chmod +x %{__perl_provides}


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

%check



%clean 
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog Changes README
%{perl_vendorlib}/Data/
%{perl_vendorlib}/XML/
%{_mandir}/man3/*.3*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.08-19
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.08-18
- 为 Magic 3.0 重建

* Fri Oct 19 2012 Liu Di <liudidi@gmail.com> - 0.08-17
- 为 Magic 3.0 重建

* Fri Oct 19 2012 Liu Di <liudidi@gmail.com> - 0.08-16
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.08-14
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-12
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-11
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.08-10
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08-6
- don't filter out all Data::Grove provides, only unversioned one

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08-5
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08-4
- rebuild for new perl

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 0.08-3
- Fix old changelog entry
- Fix issues from package review:
- Remove extra BR: perl
- Remove "|| :" from check section
- Add dist tag to release
- Remove extra Provides: perl(Data::Grove)
- Clean up tabs and spacing
- Resolves: bz#226269

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08-2
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.08-1.3
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.08-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Sat Apr 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.08-1
- Update to 0.08.
- spec cleanup (#153199)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 0.07-30
- rebuild

* Fri Apr 23 2004 Chip Turner <cturner@redhat.com> 0.07-29
- bump

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Wed Mar 27 2002 Chip Turner <cturner@redhat.com>
- move to vendor_perl

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jul 18 2001 Crutcher Dunnavant <crutcher@redhat.com> 0.07-5
- imported from mandrake. tweaked man path.

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.07-4mdk
- Rebuild for the latest perl.
- Remove Distribution and Vendor tag.
- Don't run  for now.

* Tue Mar 13 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.07-3mdk
- BuildArch: noarch
- add docs
- rename spec file
- clean up spec a bit
- run automated tests

* Sat Sep 16 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 0.07-2mdk
- Call spec-helper before creating filelist

* Wed Aug 09 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.07-1mdk
- Macroize package
