Name:       perl-Archive-RPM
Version:    0.06
Release:    10%{?dist}
Summary:    Work with a RPM
# lib/Archive/RPM.pm -> LGPLv2+
# lib/Archive/RPM/ChangeLogEntry.pm -> LGPLv2+
License:    LGPLv2+
Group:      Development/Libraries
Url:        http://search.cpan.org/dist/Archive-RPM
Source:     http://search.cpan.org/CPAN/authors/id/R/RS/RSRCHBOY/Archive-RPM-%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

# non-perl
BuildRequires: rpm, cpio
Requires:      rpm, cpio

BuildRequires: perl(CPAN)
BuildRequires: perl(DateTime)
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires: perl(Moose)
BuildRequires: perl(MooseX::AttributeHelpers)
BuildRequires: perl(MooseX::MarkAsMethods)
BuildRequires: perl(MooseX::Traits)
BuildRequires: perl(MooseX::Types::DateTime)
BuildRequires: perl(MooseX::Types::DateTimeX)
BuildRequires: perl(MooseX::Types::Path::Class)
BuildRequires: perl(Path::Class)
BuildRequires: perl(RPM2) >= 0.68
BuildRequires: perl(Test::More)

Requires:      perl(MooseX::Traits)
Requires:      perl(MooseX::Types::DateTime)
Requires:      perl(RPM2) >= 0.68

%{?perl_default_filter}
%{?perl_default_subpackage_tests}

%description
Archive::RPM provides a more complete method of accessing an RPM's meta-
and actual data. We access this information by leveraging RPM2 where we
can, and by "exploding" the rpm with rpm2cpio and cpio when we need
information we can't get through RPM2.

%prep
%setup -q -n Archive-RPM-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Dec 10 2012 Liu Di <liudidi@gmail.com> - 0.06-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.06-9
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.06-8
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.06-7
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.06-6
- 为 Magic 3.0 重建

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.06-5
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.06-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Jun 18 2010 Petr Pisar <ppisar@redhat.com> - 0.06-1
- Update dependencies (bug #599859)
- Reorder spec headers

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-2
- Mass rebuild with perl-5.12.0

* Sat Feb 13 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- update to 0.05

* Sat Feb 13 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.04-5
- PERL_INSTALL_ROOT => DESTDIR
- add perl_default_subpackage_tests

* Wed Jan 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.04-4
- auto-update to 0.04 (by cpan-spec-update 0.01)
- added a new br on CPAN (inc::Module::AutoInstall found)
- added a new req on perl(DateTime) (version 0)
- added a new req on perl(Moose) (version 0)
- added a new req on perl(MooseX::AttributeHelpers) (version 0)
- added a new req on perl(MooseX::Types::DateTime) (version 0)
- added a new req on perl(MooseX::Types::Path::Class) (version 0)
- added a new req on perl(Path::Class) (version 0)
- added a new req on perl(RPM2) (version 0.67)
- added a new req on perl(namespace::clean) (version 0)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.04-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 26 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- update to 0.04

* Sun Mar 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03-1
- submission

* Sun Mar 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
