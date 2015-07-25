Name:           perl-File-ExtAttr
Version:        1.09
Release:        19%{?dist}
Summary:        Perl extension for accessing extended attributes of files
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/File-ExtAttr/
Source0:        http://www.cpan.org/authors/id/R/RI/RICHDAWE/File-ExtAttr-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Scalar::Util)

# this is odd, I know, but while the module requires libattr-devel to build,
# it will end up not requiring libattr.so*.  This is expected.
BuildRequires: libattr-devel

# TestBRs:
BuildRequires:  perl(Test::Distribution), perl(Test::Pod)
BuildRequires:  perl(File::Find::Rule), perl(Module::CoreList)

# don't "provide" private Perl libs
%global _use_internal_dependency_generator 0
%global __deploop() while read FILE; do /usr/lib/rpm/rpmdeps -%{1} ${FILE}; done | /bin/sort -u
%global __find_provides /bin/sh -c "%{__grep} -v '%{perl_vendorarch}/.*\\.so$' | %{__deploop P}"
%global __find_requires /bin/sh -c "%{__deploop R}"

%description
File::ExtAttr is a Perl module providing access to the extended
attributes of files.

%prep
%setup -q -n File-ExtAttr-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor optimize="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
# NOTE:  these are noisy; as near as I can tell this is expected
# NOTE2: if you're testing on a filesystem that does not support extended
#        attributes, in all likelyhood the tests will fail.  If anyone has 
#        a quick&easy non-priv'ed way to test for this, I'll be more than 
#        happy to include it.
# NOTE3: Tests disabled for now, pending a way to detect & disable on non-ea 
#        enabled filesystems
%{?_with_network_tests: }

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README TODO
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/File*
%{_mandir}/man3/*

%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.09-19
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.09-18
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.09-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.09-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.09-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.09-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.09-13
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.09-12
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.09-11
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.09-10
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.09-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.09-6
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.09-5
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.09-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.09-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.09-1
- update to 1.09

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.02-5
Rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.02-4
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.02-3
- bump

* Thu Apr 19 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.02-2
- add additional split BR's

* Sat Apr 07 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.02-1
- update to 1.02

* Thu Dec 07 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.01-3
- Tests disabled for now, pending a way to detect & disable on non-ea enabled
  filesystems

* Thu Dec 07 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.01-2
- bump

* Tue Oct 03 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.01-1
- Specfile autogenerated by cpanspec 1.69.
