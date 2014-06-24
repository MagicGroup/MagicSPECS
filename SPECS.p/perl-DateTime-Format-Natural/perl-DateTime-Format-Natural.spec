Name:           perl-DateTime-Format-Natural
Version:        1.01
Release:        6%{?dist}
Summary:        Create machine readable date/time with natural parsing logic
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/DateTime-Format-Natural/
Source0:        http://www.cpan.org/authors/id/S/SC/SCHUBIGER/DateTime-Format-Natural-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(boolean)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::ISA)
BuildRequires:  perl(Clone)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(DateTime)
BuildRequires:  perl(Date::Calc)
BuildRequires:  perl(DateTime)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Module::Util)
BuildRequires:  perl(Params::Validate)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Term::ReadLine)
BuildRequires:  perl(Test::MockTime)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
DateTime::Format::Natural takes a string with a human readable date/time
and creates a machine readable one by applying natural parsing logic.

%package -n perl-DateTime-Format-Natural-Test
Summary:        Common test routines/data for perl-DateTime-Format-Natural
Requires:       %{name} = %{version}-%{release}

%description -n perl-DateTime-Format-Natural-Test
The DateTime::Format::Natural::Test class exports common test routines.

%prep
%setup -q -n DateTime-Format-Natural-%{version}
for f in Changes README; do
        iconv -f iso8859-1 -t utf-8 $f >$f.conf && mv $f.conf $f
done

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes README
%exclude %{perl_vendorlib}/DateTime/Format/Natural/Test.pm
%exclude %{_mandir}/man3/DateTime::Format::Natural::Test.*
%{perl_vendorlib}/*
%{_bindir}/dateparse
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n perl-DateTime-Format-Natural-Test
%{perl_vendorlib}/DateTime/Format/Natural/Test.pm
%{_mandir}/man3/DateTime::Format::Natural::Test.*


%changelog
* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 1.01-6
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 1.01-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct 21 2012 Iain Arnell <iarnell@gmail.com> 1.01-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.00-2
- Perl 5.16 rebuild

* Sat Jun 09 2012 Iain Arnell <iarnell@gmail.com> 1.00-1
- update to latest upstream version

* Mon May 07 2012 Iain Arnell <iarnell@gmail.com> 0.99-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 06 2011 Iain Arnell <iarnell@gmail.com> 0.98-1
- update to latest upstream version

* Sat Aug 27 2011 Iain Arnell <iarnell@gmail.com> 0.97-1
- update to latest upstream version

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.96-2
- Perl mass rebuild

* Sun Jun 05 2011 Iain Arnell <iarnell@gmail.com> 0.96-1
- update to latest upstream version

* Wed May 18 2011 Iain Arnell <iarnell@gmail.com> 0.95-1
- update to latest upstream version

* Sun Apr 03 2011 Iain Arnell <iarnell@gmail.com> 0.94-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Iain Arnell <iarnell@gmail.com> 0.93-1
- update to latest upstream version

* Sat Jan 15 2011 Iain Arnell <iarnell@gmail.com> 0.92-1
- update to latest upstream version

* Sun Dec 12 2010 Iain Arnell <iarnell@gmail.com> 0.91-2
- split DateTime::Format::Natural::Test into separate sub-package to avoid
  runtime dependecy on Test::More

* Tue Nov 02 2010 Iain Arnell <iarnell@gmail.com> 0.91-1
- update to latest upstream version

* Thu Oct 07 2010 Iain Arnell <iarnell@gmail.com> 0.90-1
- regular update to latest upstream version
- clean up spec for modern rpmbuild

* Fri Aug 06 2010 Iain Arnell <iarnell@gmail.com> 0.89-1
- update to latest upstream version

* Fri Jun 18 2010 Iain Arnell <iarnell@gmail.com> 0.88-1
- update to latest upstream

* Sun May 30 2010 Iain Arnell <iarnell@gmail.com> 0.87-1
- update to latest upstream

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.86-2
- Mass rebuild with perl-5.12.0

* Wed Apr 21 2010 Iain Arnell <iarnell@gmail.com> 0.86-1
- update to latest upstream version

* Sun Mar 14 2010 Iain Arnell <iarnell@gmail.com> 0.85-1
- update to latest upstream version
- use perl_default_filter

* Thu Feb 25 2010 Iain Arnell <iarnell@gmail.com> 0.84-1
- update to latest upstream version

* Thu Jan 14 2010 Iain Arnell <iarnell@gmail.com> 0.83-1
- update to latest upstream version

* Mon Jan 04 2010 Iain Arnell <iarnell@gmail.com> 0.82-1
- update to latest upstream version

* Wed Dec 09 2009 Iain Arnell <iarnell@gmail.com> 0.81-1
- update to latest upstream version

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.80-2
- rebuild against perl 5.10.1

* Fri Oct 30 2009 Iain Arnell <iarnell@gmail.com> 0.80-1
- update to latest upstream version

* Sun Sep 20 2009 Iain Arnell <iarnell@gmail.com> 0.79-1
- update to latest upstream version

* Sat Aug 29 2009 Iain Arnell <iarnell@gmail.com> 0.78-1
- update to latest upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 21 2009 Iain Arnell <iarnell@gmail.com> 0.77-1
- update to latest upstream version

* Sat Apr 11 2009 Iain Arnell <iarnell@gmail.com> 0.76-1
- update to latest upstream release

* Sat Feb 28 2009 Iain Arnell <iarnell@gmail.com> 0.75-1
- update to 0.75

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.74-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 21 2008 Iain Arnell <iarnell@gmail.com> 0.74-1
- update to 0.74

* Tue Nov 18 2008 Iain Arnell <iarnell@gmail.com> 0.73-1
- Specfile autogenerated by cpanspec 1.77.
