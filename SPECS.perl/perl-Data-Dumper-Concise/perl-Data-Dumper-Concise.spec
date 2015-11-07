Name:           perl-Data-Dumper-Concise
Summary:        A convenient way to reproduce a set of Dumper options
Version:	2.022
Release:	2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/F/FR/FREW/Data-Dumper-Concise-%{version}.tar.gz
URL:            http://search.cpan.org/dist/Data-Dumper-Concise
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Test::More)

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 2.020-3
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
This module always exports a single function, Dumper, which can be
called with an array of values to dump those values or with no arguments
to return the Data::Dumper object it has created.  It exists,
fundamentally, as a convenient way to reproduce a set of Dumper options
that we've found ourselves using across large numbers of applications.

%prep
%setup -q -n Data-Dumper-Concise-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.022-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.022-1
- 更新到 2.022

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.020-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.020-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.020-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.020-4
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 2.020-3
- drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.020-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> 2.020-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.200-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.200-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.200-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.200-2
- Mass rebuild with perl-5.12.0

* Mon Mar 08 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.200-1
- update by Fedora::App::MaintainerTools 0.004
- updating to latest GA CPAN version (1.200)

* Sat Feb 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.100-2
- fix certain typos

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.100-1
- submission

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.100-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
