Name:           perl-Spoon
Version:        0.24
Release:        25%{?dist}
Summary:        Spiffy Application Building Framework
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Spoon/
Source0:        http://www.cpan.org/authors/id/I/IN/INGY/Spoon-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(ExtUtils::MM_Unix)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(CGI)
# CGI::Util not used for tests
# Config not used for tests
# Data::Dumper not used for tests
BuildRequires:  perl(DB_File)
BuildRequires:  perl(Encode)
BuildRequires:  perl(IO::All) >= 0.32
# MIME::Base64 not used for tests
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Spiffy) >= 0.24
BuildRequires:  perl(Storable)
BuildRequires:  perl(Template) >= 2.10
BuildRequires:  perl(Time::HiRes)
# Tests:
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(warnings)
# Optional tests:
BuildRequires:  perl(Test::Memory::Cycle)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(CGI::Util)
Requires:       perl(Config)
Requires:       perl(Data::Dumper)
Requires:       perl(Encode)
Requires:       perl(IO::All) >= 0.32
Requires:       perl(MIME::Base64)
Requires:       perl(Spiffy) >= 0.24
Requires:       perl(Storable)
Requires:       perl(Template) >= 2.10

%{?perl_default_filter:
%filter_from_provides /^perl(IO::All)$/d
%filter_from_requires /^perl(IO::All)$/d /^perl(Spiffy)$/d /^perl(Template)$/d
%{?perl_default_filter}
}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(IO::All|Spiffy|Template\\)$
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(IO::All\\)$


%description
Spoon is an Application Framework that is designed primarily for
building Social Software web applications. The Kwiki wiki software is
built on top of Spoon.

%prep
%setup -q -n Spoon-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.24-25
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.24-24
- 为 Magic 3.0 重建

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.24-23
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 Petr Pisar <ppisar@redhat.com> - 0.24-20
- Perl 5.18 rebuild
- Specify all dependencies

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 0.24-17
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.24-15
- add new filter

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.24-14
- Perl mass rebuild

* Wed Feb 16 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.24-13
- Remove bogus rm %%{__perl_provides}.

* Wed Feb 16 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.24-12
- Revert temporary hack "BR: perl-IO-All" (Not required anymore).

* Tue Feb 15 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.24-11
- BR: perl-IO-All, to assure getting the right perl(IO::All)
  (was bogusly provided by perl-Spoon-0.24-9).

* Tue Feb 15 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.24-10
- Rework filters (Cause of broken deps).

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.24-8
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.24-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.24-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.24-3
- rebuild for new perl

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 0.24-2
- BR ExtUtils::MakeMaker.

* Tue Dec 26 2006 Steven Pritchard <steve@kspei.com> 0.24-1
- Update to 0.24.
- Use fixperms macro instead of our own chmod incantation.
- Other minor cleanup to more closely match current cpanspec output.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.23-5
- Fix find option order.

* Mon Jun 12 2006 Steven Pritchard <steve@kspei.com> 0.23-4
- BR URI::Escape.

* Thu Mar 02 2006 Steven Pritchard <steve@kspei.com> 0.23-3
- Improve Summary.
- Fix Source0.

* Mon Feb 27 2006 Steven Pritchard <steve@kspei.com> 0.23-2
- Drop explicit BR: perl.

* Wed Dec 28 2005 Steven Pritchard <steve@kspei.com> 0.23-1
- Specfile autogenerated.
