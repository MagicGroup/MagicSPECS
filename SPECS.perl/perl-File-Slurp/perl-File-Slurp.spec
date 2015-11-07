Name: 		perl-File-Slurp
Version: 	9999.19
Release: 	10%{?dist}
Summary: 	Efficient Reading/Writing of Complete Files
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/File-Slurp/
Source0: 	http://www.cpan.org/modules/by-module/File/File-Slurp-%{version}.tar.gz

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# Tests
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
# Optional tests
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04

%{?perl_default_filter}

%description
This module provides subs that allow you to read or write entire files with
one simple call. They are designed to be simple to use, have flexible ways
to pass in or get the file contents and to be very efficient. There is also
a sub to read in all the files in a directory other than . and ..

These slurp/spew subs work for files, pipes and sockets, and stdio, 
pseudo-files, and DATA.

%prep
%setup -q -n File-Slurp-%{version}
iconv -f iso8859-1 -t UTF-8 Changes > Changes~
mv Changes~ Changes

find \( -executable -a -type f \) -exec chmod -x {} \;
%{__perl} -pi -e 's|^#!/usr/local/bin/perl\b|#!%{__perl}|' extras/slurp_bench.pl

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%files
%defattr(-,root,root,-)
# For license text(s), see the perl package.
%doc Changes README extras/
%{perl_vendorlib}/File
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 9999.19-10
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 9999.19-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 9999.19-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 9999.19-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 9999.19-6
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9999.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 9999.19-4
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9999.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 9999.19-2
- Perl mass rebuild

* Wed Jun 08 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.19-1
- Upstream update.

* Sun May 15 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.18-1
- Upstream update.

* Thu Apr 28 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.16-1
- Upstream update.

* Tue Mar 29 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 9999.15-1
- Upstream update.
- Add perl_default_filter.
- Fix encoding of "Changes".
- Spec cleanup.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9999.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 9999.13-9
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 9999.13-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 9999.13-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9999.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9999.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 09 2008 Ralf Corsépius <rc040203@freenet.de> - 9999.13-4
- Re-activate tests.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 9999.13-3
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 9999.13-2
- disable tests, due to wacky Fedora builders

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 9999.13-1
- go to 9999.13 to fix build failures against perl 5.10.0

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 9999.12-4
- rebuild for new perl

* Sun Sep 02 2007 Ralf Corsépius <rc040203@freenet.de> - 9999.12-3
- Update license tag.
- BR: perl(ExtUtils::MakeMaker).

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 9999.12-2
- Mass rebuild.

* Sat Mar 18 2006 Ralf Corsépius <rc040203@freenet.de> - 9999.12-1
- Upstream update.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 9999.11-2
- Rebuild for perl-5.8.8.

* Wed Feb 01 2006 Ralf Corsépius <rc040203@freenet.de> - 9999.11-1
- Upstream update.
- BR perl(Test::Pod), perl(Test::Pod::Coverage).
