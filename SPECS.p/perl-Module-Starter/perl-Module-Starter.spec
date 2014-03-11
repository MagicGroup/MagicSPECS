Name:           perl-Module-Starter
Epoch:          1
Version:        1.60
Release:        2%{?dist}
Summary:        A simple starter kit for any module
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Module-Starter
Source0:        http://search.cpan.org/CPAN/authors/id/X/XS/XSAWYERX/Module-Starter-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::Command)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(parent)
BuildRequires:  perl(Path::Class)
BuildRequires:  perl(Pod::Usage)
# Tests:
BuildRequires:  perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:  perl(Cwd)
Requires:  perl(ExtUtils::Command)
Requires:  perl(File::Spec)
Requires:  perl(parent)

%{?perl_default_filter}
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}%{perl_vendorlib}/Module/Starter/Simple\\.pm

%description
This is a CPAN module/utility to assist in the creation of new modules in a
sensible and sane fashion.  Unless you're interested in extending the
functionality of this module, you should examine the documentation for
'module-starter', for information on how to use this tool.

It is noted that there are a number of extensions to this tool, including
plugins to create modules using templates as recommended by Damian Conway's
"Perl Best Practices" (O'Reilly, 2005).  (See also the package
perl-Module-Starter-PBP for the aformentioned templates.)


%prep
%setup -q -n Module-Starter-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_bindir}/*
%{_mandir}/man[13]/*.[13]*


%changelog
* Fri Oct 26 2012 Petr Pisar <ppisar@redhat.com> - 1:1.60-2
- Drop build-time dependencies for unused author tests

* Fri Oct 26 2012 Petr Pisar <ppisar@redhat.com> - 1:1.60-1
- 1.60 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.58-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1:1.58-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> 1:1.58-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- remove explicit requires
- update filtering macros

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.54-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.54-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.54-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> 1:1.54-1
- update
- rebuild with perl-5.12

* Tue Aug 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 1:1.52-1
- auto-update to 1.52 (by cpan-spec-update 0.01)
- added a new br on perl(ExtUtils::Command) (version 0)
- added a new br on perl(ExtUtils::MakeMaker) (version 0)
- added a new br on perl(File::Spec) (version 0)
- added a new br on perl(Getopt::Long) (version 0)
- added a new br on perl(Pod::Usage) (version 0)
- added a new br on perl(Test::More) (version 0)
- added a new req on perl(ExtUtils::Command) (version 0)
- added a new req on perl(File::Spec) (version 0)
- added a new req on perl(Getopt::Long) (version 0)
- added a new req on perl(Pod::Usage) (version 0)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.50-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 05 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.50-2
- correct source

* Wed Nov 05 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.50-1
- update to 1.50

* Sat Jul 05 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.470-1
- update to 1.470

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.42-5
- rebuild for new perl

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.42-4
- bump for mass rebuild

* Mon Aug 07 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.42-3
- bump for build & release

* Sun Aug 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.42-2
- add additional br's for test suite:
  perl(Test::Pod::Coverage), perl(Test::Pod)

* Sat Aug 05 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.42-1
- Initial spec file for F-E
