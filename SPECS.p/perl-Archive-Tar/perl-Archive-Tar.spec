Name:           perl-Archive-Tar
Version:        1.82
Release:        3%{?dist}
Summary:        A module for Perl manipulation of .tar files
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Archive-Tar/
Source0:        http://www.cpan.org/authors/id/B/BI/BINGOS/Archive-Tar-%{version}.tar.gz
BuildArch:      noarch
# Most of the BRS are needed only for tests, compression support at run-time
# is optional soft dependency.
BuildRequires:  perl(Carp)
BuildRequires:  perl(Compress::Zlib) >= 2.015
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Unix)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(IO::Compress::Base) >= 2.015
BuildRequires:  perl(IO::Compress::Bzip2) >= 2.015
BuildRequires:  perl(IO::Compress::Gzip) >= 2.015
BuildRequires:  perl(IO::String)
BuildRequires:  perl(IO::Zlib) >= 1.01
BuildRequires:  perl(Package::Constants)
BuildRequires:  perl(Test::Harness) >= 2.26
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Compress::Zlib) >= 2.015
Requires:       perl(IO::Zlib) >= 1.01

%description
Archive::Tar provides an object oriented mechanism for handling tar
files.  It provides class methods for quick and easy files handling
while also allowing for the creation of tar file objects for custom
manipulation.  If you have the IO::Zlib module installed, Archive::Tar
will also support compressed or gzipped tar files.

%prep
%setup -q -n Archive-Tar-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check
make test

%files
%doc CHANGES README
%{_bindir}/*
%{perl_vendorlib}/Archive/
%{_mandir}/man3/*.3*
%{_mandir}/man1/*.1*


%changelog
* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 1.82-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Petr Šabata <contyk@redhat.com> - 1.82-1
- 1.82 bump

* Fri Oct 14 2011 Petr Sabata <contyk@redhat.com> - 1.80-1
- 1.80 bump

* Fri Sep 09 2011 Petr Pisar <ppisar@redhat.com> - 1.78-1
- 1.78 bump
- Remove BuildRoot and defattr code from spec

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.76-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Petr Pisar <ppisar@redhat.com> - 1.76-1
- 1.76 bump

* Mon Jan 03 2011 Petr Sabata <psabata@redhat.com> - 1.74-1
- 1.74 bump

* Fri Nov 19 2010 Petr Pisar <ppisar@redhat.com> - 1.72-1
- 1.72 bump

* Tue Sep 14 2010 Petr Pisar <ppisar@redhat.com> - 1.68-1
- 1.68 bump

* Tue Jul 13 2010 Petr Pisar <ppisar@redhat.com> - 1.64-1
- 1.64 bump

* Tue Jul 13 2010 Petr Pisar <ppisar@redhat.com> - 1.62-1
- 1.62 bump (bug #607687)

* Thu Aug 23 2007 Robin Norwood <rnorwood@redhat.com> - 1.34-1
- Upgrade to latest upstream version: 1.34
- Fix license tag
- Fix BuildRequires for ExtUtils::MakeMaker and Test::Pod

* Mon Jun 04 2007 Robin Norwood <rnorwood@redhat.com> - 1.32-1
- Upgrade to latest upstream version: 1.32

* Mon Mar 05 2007 Robin Norwood <rnorwood@redhat.com> - 1.30-4
- Fix changelog

* Mon Feb 19 2007 Robin Norwood <rnorwood@redhat.com> - 1.30-3
- Incorporate specfile improvements from Jose Oliveira.

* Fri Feb 16 2007 Robin Norwood <rnorwood@redhat.com> - 1.30-2
- Resolves: rhbz#226239 - Remove tabs from spec file for package review

* Tue Sep 19 2006 Robin Norwood <rnorwood@redhat.com> - 1.30-1
- Bump to 1.30

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.29-1.1
- rebuild

* Wed Mar 08 2006 Jason Vas Dias <jvdias@redhat.com> - 1.29-1
- Upgrade to upstream version 1.29

* Fri Feb 02 2006 Jason Vas Dias <jvdias@redhat.com> - 1.28-1
- Upgrade to upstream version 1.28
- Rebuild for perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Sun Nov 06 2005 Florian La Roche <laroche@redhat.com>
- 1.26

* Mon Apr 25 2005 Warren Togami <wtogami@redhat.com> - 1.23-4
- remove beehive workaround

* Sun Apr 03 2005 Jose Pedro Oliveira <jpo@di.uminho.pt> - 1.23-1
- Update to 1.23.
- Bring up to date with current Fedora.Extras perl spec template.

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 1.08-3
- rebuild

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1.08-1
- update to upstream 1.08

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Fri Feb 08 2002 cturner@redhat.com
- Specfile autogenerated

