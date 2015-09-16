Name:           perl-Glib
Version:	1.313
Release:	1%{?dist}
Summary:        Perl interface to GLib
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://search.cpan.org/dist/Glib/
Source0:        http://www.cpan.org/authors/id/X/XA/XAOC/Glib-%{version}.tar.gz
BuildRequires:  perl >= 2:5.8.0
BuildRequires:  glib2-devel
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::Depends) >= 0.300
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::PkgConfig) >= 1.00
BuildRequires:  perl(File::Spec)
# Run-time
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Storable)
# Tests
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Hash)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Do not export private modules and libraries
%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(MY\\)

%description
This module provides perl access to GLib and GLib's GObject libraries.
GLib is a portability and utility library; GObject provides a generic
type system with inheritance and a powerful signal system.  Together
these libraries are used as the foundation for many of the libraries
that make up the Gnome environment, and are used in many unrelated
projects.

%package devel
Summary:    Development part of Perl interface to GLib
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development part of package perl-Glib, the Perl module providing interface
to GLib and GObject libraries.

%prep
%setup -q -n Glib-%{version}
for F in AUTHORS; do
    iconv -f ISO-8859-1 -t UTF-8 < "$F" > "${F}.utf8"
    touch -r "$F" "${F}.utf8"
    mv "${F}.utf8" "$F"
done

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
%ifnarch ppc ppc64

%endif

%files
%doc AUTHORS ChangeLog.pre-git LICENSE NEWS README TODO
%{perl_vendorarch}/auto/Glib/
%{perl_vendorarch}/Glib*
%{_mandir}/man3/*.3pm*
%exclude %{perl_vendorarch}/Glib/*/*.h
%exclude %{perl_vendorarch}/Glib/MakeHelper.pm
%exclude %{perl_vendorarch}/Glib/devel.pod
%exclude %{perl_vendorarch}/Glib/xsapi.pod
%exclude %{_mandir}/man3/Glib::MakeHelper.3pm.gz
%exclude %{_mandir}/man3/Glib::devel.3pm.gz
%exclude %{_mandir}/man3/Glib::xsapi.3pm.gz

%files devel
%{perl_vendorarch}/Glib/*/*.h
%{perl_vendorarch}/Glib/MakeHelper.pm
%{perl_vendorarch}/Glib/devel.pod
%{perl_vendorarch}/Glib/xsapi.pod
%{_mandir}/man3/Glib::MakeHelper.3pm.gz
%{_mandir}/man3/Glib::devel.3pm.gz
%{_mandir}/man3/Glib::xsapi.3pm.gz

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.313-1
- 更新到 1.313

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.260-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.260-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.260-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.260-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.260-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.260-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.260-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.260-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 1.260-2
- Perl 5.16 rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.260-1
- 1.260 bump

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.241-4
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 1.241-3
- Do not export private modules and libraries

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.241-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Tom Callaway <spot@fedoraproject.org> - 1.241-1
- update to 1.241

* Thu Oct 20 2011 Tom Callaway <spot@fedoraproject.org> - 1.240-1
- update to 1.240

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.223-3
- Perl mass rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.223-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Jul 01 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.223-1
- update to 1.223

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.201-5
- Mass rebuild with perl-5.12.0

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.201-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Stepan Kasal <skasal@redhat.com> - 1.201-3
- create devel subpackage, so that the main one does not require
  the whole perl-devel (#509419)

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.201-2
- dont run the tests on ppc

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.201-1
- update to 1.201

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.183-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.183-1
- update to 1.183

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.162-5
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.162-4
- Autorebuild for GCC 4.3

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.162-3
- rebuild for new perl

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.162-2
- disable smp_mflags, they break on massively SMP boxes (bz 428911)

* Mon Dec 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.162-1
- 1.162

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.144-1.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.144-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Mon Feb 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.144-1
- Update to 1.144.

* Sun Feb 11 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.143-1
- Update to 1.143.

* Thu Dec  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.142-1
- Update to 1.142.

* Wed Nov 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.141-1
- Update to 1.141.

* Wed Sep  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.140-1
- Update to 1.140.

* Tue Mar 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.120-1
- Update to 1.120.

* Mon Feb 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.105-2
- make tag problem.

* Mon Feb 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.105-1
- Update to 1.105.

* Mon Feb  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.104-1
- Update to 1.104 (fails one test in perl 5.8.8).

* Thu Jan 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.103-1
- Update to 1.103.
- Provides list: filtered out perl(MY) (#177956).

* Wed Nov 30 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.102-1
- Update to 1.102.

* Thu Oct  6 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.101-1
- Update to 1.101.

* Thu Sep  8 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.100-1
- Update to 1.100.

* Mon Jun 27 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.082-1
- Update to 1.082.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Mar  8 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.080-1
- Update to 1.080.

* Tue Feb 15 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.062-1
- Update to 1.062.

* Mon Oct 18 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.061-0.fdr.2
- Removed irrelevant documentation file - Glib.exports.

* Sun Oct  3 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.061-0.fdr.1
- Update to 1.061.

* Sun Jul 18 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.043-0.fdr.1
- First build.
