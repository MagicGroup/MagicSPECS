Name:       perl-Term-Size 
Version:    0.207
Release:    7%{?dist}
# see Copyright
License:    GPL+ or Artistic 
Group:      Development/Libraries
Summary:    Simple way to get terminal size 
Source0:    http://search.cpan.org/CPAN/authors/id/F/FE/FERREIRA/Term-Size-%{version}.tar.gz
Url:        http://search.cpan.org/dist/Term-Size
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# see http://rt.cpan.org/Public/Bug/Display.html?id=38594
Patch0:     perl-Term-Size-0.207-perlio.patch
BuildRequires: perl(ExtUtils::MakeMaker)
%{?_with_display_tests: BuildRequires: perl(Carp), perl(Exporter) }

# don't "provide" private Perl libs
%global _use_internal_dependency_generator 0
%global __deploop() while read FILE; do /usr/lib/rpm/rpmdeps -%{1} ${FILE}; done | /bin/sort -u
%global __find_provides /bin/sh -c "%{__grep} -v '%{perl_vendorarch}/.*\\.so$' | %{__deploop P}"
%global __find_requires /bin/sh -c "%{__deploop R}"

%description
*Term::Size* is a Perl module which provides a straightforward way to
retrieve the terminal size.

Both functions take an optional filehandle argument, which defaults to
'*STDIN{IO}'. They both return a list of two values, which are the current
width and height, respectively, of the terminal associated with the
specified filehandle.

'Term::Size::chars' returns the size in units of characters, whereas
'Term::Size::pixels' uses units of pixels.

%prep
%setup -q -n Term-Size-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
# tests will fail under mock (no terminal size to get!) In particular, tests
# 2, 3 and 5 fail regardless of what platform they're being complied for under
# mock.
%{?_with_display_tests: make test }

%files
%doc Changes README Copyright
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.207-7
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.207-6
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.207-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.207-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.207-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.207-2
- Perl 5.16 rebuild

* Fri Jan 13 2012 Petr Šabata <contyk@redhat.com> - 0.207-1
- 0.207 bump

* Mon Jun 20 2011 Petr Sabata <contyk@redhat.com> - 0.2-9
- Perl mass rebuild
- Removing now obsolete Buildroot and defattr

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.2-7
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.2-6
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.2-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 26 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.2-3
- Stripping bad provides of private Perl extension libs

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 29 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.2-1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.1)
