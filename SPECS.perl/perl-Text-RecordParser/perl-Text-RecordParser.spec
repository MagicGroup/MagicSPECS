Name:           perl-Text-RecordParser
Version:        1.6.5
Release:        5%{?dist}
Summary:        Read record-oriented files
License:        GPLv2
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Text-RecordParser/
Source0:        http://search.cpan.org/CPAN/authors/id/K/KC/KCLARK/Text-RecordParser-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  perl
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(ExtUtils::MM_Unix)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Accessor)
BuildRequires:  perl(English)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(GraphViz)
BuildRequires:  perl(IO::Scalar)
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Readonly)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Text::Autoformat)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(Text::TabularDisplay)
BuildRequires:  perl(version)
BuildRequires:  perl(warnings)
# Tests only
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
# Optional tests only
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))

%description
This module is for reading record-oriented data in a delimited text file.
The most common example have records separated by newlines and fields
separated by commas or tabs, but this module aims to provide a consistent
interface for handling sequential records in a file however they may be
delimited. Typically this data lists the fields in the first line of the
file, in which case you should call bind_header to bind the field name (or
not, and it will be called implicitly). If the first line contains data,
you can still bind your own field names via bind_fields. Either way, you
can then use many methods to get at the data as arrays or hashes.

%prep
%setup -q -n Text-RecordParser-%{version}
perl -pi -e 's|^#!perl|#!%{__perl}|' t/*.t

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README TODO
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man[13]/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.6.5-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.6.5-4
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.6.5-1
- 更新到 1.6.5

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.5.0-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.5.0-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.5.0-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.5.0-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.5.0-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.5.0-6
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 1.5.0-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.5.0-2
- Perl mass rebuild

* Sat May 07 2011 Iain Arnell <iarnell@gmail.com> 1.5.0-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3.0-5
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3.0-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.3.0-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.3.0-1
- auto-update to 1.3.0 (by cpan-spec-update 0.01)
- added a new br on perl(List::Util) (version 0)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.1-4
- rebuild for new perl

* Wed May 16 2007 Chris Weyl <cweyl@alumni.drew.edu> v1.2.1-3
- bump

* Wed May 16 2007 Chris Weyl <cweyl@alumni.drew.edu> v1.2.1-2
- additional BR for test suite: perl(IO::Scalar)

* Mon May 14 2007 Chris Weyl <cweyl@alumni.drew.edu> v1.2.1-1
- Specfile autogenerated by cpanspec 1.71.
