Name:           perl-String-Formatter
Version:        0.102082
Release:        8%{?dist}
Summary:        Build sprintf-like functions of your own
License:        GPLv2
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/String-Formatter/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/String-Formatter-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl >= 0:5.006
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Params::Util)
BuildRequires:  perl(Sub::Exporter)
# tests
BuildRequires:  perl(Pod::Coverage::TrustPod)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
String::Formatter is a tool for building sprintf-like formatting routines.
It supports named or positional formatting, custom conversions, fixed
string interpolation, and simple width-matching out of the box. It is easy
to alter its behavior to write new kinds of format string expanders. For
most cases, it should be easy to build all sorts of formatters out of the
options built into String::Formatter.

%prep
%setup -q -n String-Formatter-%{version}

# don't install benchmark
sed -i -e '1s~#!perl~#!%{__perl}~' bench.pl
mkdir eg
mv bench.pl eg

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
RELEASE_TESTING=1 

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README eg/bench.pl
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.102082-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.102082-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102082-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.102082-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102082-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.102082-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102082-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 03 2010 Iain Arnell <iarnell@gmail.com> 0.102082-1
- update to latest upstream

* Fri Jul 30 2010 Iain Arnell <iarnell@gmail.com> 0.102080-1
- update to latest upstream
- update spec for modern rpmbuild

* Tue Jun 15 2010 Iain Arnell <iarnell@gmail.com> 0.101620-1
- update to latest upstream

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.100720-2
- Mass rebuild with perl-5.12.0

* Fri Apr 02 2010 Iain Arnell <iarnell@gmail.com> 0.100720-1
- Specfile autogenerated by cpanspec 1.78.
- use perl_default_filter and DESTDIR
- install bench.pl as documentation