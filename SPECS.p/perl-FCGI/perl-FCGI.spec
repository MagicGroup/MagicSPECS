Name:           perl-FCGI
Summary:        FastCGI Perl bindings
# needed to properly replace/obsolete fcgi-perl
Epoch:          1
Version:        0.74
Release:        6%{?dist}
# same as fcgi
License:        OML
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/F/FL/FLORA/FCGI-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/FCGI
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::File)
# Run-requires:
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
# Tests:
BuildRequires:  perl(Test)

Provides:       fcgi-perl =  %{epoch}:%{version}-%{release}
Obsoletes:      fcgi-perl =< 2.4.0

%{?perl_default_filter}
%{?perl_subpackage_tests: %perl_subpackage_tests test.pl .proverc test.t }

%description
%{summary}.

%prep
%setup -q -n FCGI-%{version}
find . -type f -exec chmod -c -x {} +

echo "test.pl" > .proverc
# limitation in the macros, currently -- must have at least one .t :\
cp test.pl test.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%files
%doc ChangeLog README LICENSE.TERMS echo.PL remote.PL threaded.PL
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1:0.74-6
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.74-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1:0.74-4
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 1:0.74-3
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.74-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Sep 24 2011 Iain Arnell <iarnell@gmail.com> 1:0.74-1
- update to latest upstream
- drop cve-2011-2766 patch

* Fri Sep 23 2011 Iain Arnell <iarnell@gmail.com> 1:0.73-3
- patch to resolve rhbz#736604 cve-2011-2766

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.73-2
- Perl mass rebuild

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.73-1
- update to 0.73, clean spec file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.71-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.71-4
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 15 2010 Chris Weyl <cweyl@alumni.drew.edu> 1:0.71-3
- and fix our tests subpackage included files

* Sat May 15 2010 Chris Weyl <cweyl@alumni.drew.edu> 1:0.71-2
- fix license: BSD => OML

* Sat May 08 2010 Chris Weyl <cweyl@alumni.drew.edu> 1:0.71-1
- specfile by Fedora::App::MaintainerTools 0.006


