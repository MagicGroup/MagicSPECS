#
# Rebuild option:
#
#   --with testsuite         - run the test suite
#

Name:           perl-Cairo
Version:        1.060
Release:        10%{?dist}
Summary:        Perl interface to the cairo library

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://search.cpan.org/dist/Cairo/
Source0:        http://www.cpan.org/authors/id/T/TS/TSCH/Cairo-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(ExtUtils::Depends), perl(ExtUtils::PkgConfig)
BuildRequires:  perl(Test::Number::Delta)
BuildRequires:  cairo-devel >= 1.0.0
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Cairo provides Perl bindings for the vector graphics library cairo.
It supports multiple output targets, including the X Window Systems,
PDF, and PNG.  Cairo produces identical output on all those targets
and makes use of hardware acceleration wherever possible.


%prep
%setup -q -n Cairo-%{version}
chmod -c a-x examples/*.pl


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
%{?_with_testsuite:}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE NEWS README TODO examples/
%{perl_vendorarch}/Cairo*
%{perl_vendorarch}/auto/Cairo/
%{_mandir}/man3/*.3pm*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.060-10
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 1.060-9
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.060-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.060-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.060-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.060-5
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.060-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.060-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.060-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.060-1
- update to 1.060

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.045-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Apr  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.045-1
- update to 1.045
- change references to ATSUI to QUARTZ (resolves bz 440741)

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.044-4
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.044-3
- Autorebuild for GCC 4.3

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.044-2
- rebuild for new perl

* Wed Nov 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.044-1
- 1.044

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.041-2
- Rebuild for selinux ppc32 issue.

* Tue Jun 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.041-1
- Update to 1.041.

* Sat Jun 16 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.040-1
- Update to 1.040.

* Mon Feb 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.023-1
- Update to 1.023.

* Sun Dec 31 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.022-1
- Update to 1.022.

* Sat Nov 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.021-1
- Update to 1.021.

* Sat Nov 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.02-1
- Update to 1.02.

* Mon Oct  2 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-2
- Rebuild (https://www.redhat.com/archives/fedora-maintainers/2006-October/msg00005.html).

* Tue Sep 26 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-1
- Update to 1.01.

* Tue Sep  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.00-1
- Update to 1.00.

* Wed Aug 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.92-1
- Update to 0.92.

* Sat Aug 12 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.91-1
- Update to 0.91.

* Sun Jul 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.90-1
- Update to 0.90.

* Tue Apr 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.03-2
- Disabled the test suite as it fails in mock.

* Sun Mar 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.03-1
- First build.
