Name:           perl-CSS-Tiny
Version:        1.19
Release:        5%{?dist}
Summary:        Read/Write .css files with as little code as possible

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/CSS-Tiny/
Source0:        http://www.cpan.org/authors/id/A/AD/ADAMK/CSS-Tiny-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl(Clone)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Clone)

%{?perl_default_filter}

%description
CSS::Tiny is a perl class to read and write .css style-sheets with as
little code as possible, reducing load time and memory overhead.


%prep
%setup -q -n CSS-Tiny-%{version}


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
%doc Changes LICENSE README
%{perl_vendorlib}/CSS/
%{_mandir}/man3/*.3pm*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.19-5
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.19-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.19-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.19-2
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 1.19-1
- Update to 1.19
- Add perl default filter

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> 1.18-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.15-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.15-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.15-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.15-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.15-1
- update to 1.15

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.14-3
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.14-2
- rebuild for new perl

* Mon Sep  4 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-1
- Update to 1.14.

* Sat May 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-1
- First build.
