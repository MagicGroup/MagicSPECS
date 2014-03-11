Name:		perl-PPIx-Utilities
Version:	1.001000
Release:	7%{?dist}
Summary:	Extensions to PPI
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/PPIx-Utilities/
Source0:	http://search.cpan.org/CPAN/authors/id/E/EL/ELLIOTJS/PPIx-Utilities-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(Exception::Class)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Slurp)
BuildRequires:	perl(PPI::Document) >= 1.208
BuildRequires:	perl(PPI::Dumper) >= 1.208
BuildRequires:	perl(Readonly)
BuildRequires:	perl(Task::Weaken)
BuildRequires:	perl(Test::Deep)
BuildRequires:	perl(Test::More)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	perl(Exporter)

%{?perl_default_filter}

%description
This is a collection of functions for dealing with PPI objects, many of
which originated in Perl::Critic. They are organized into modules by the
kind of PPI class they relate to, by replacing the "PPI" at the front of
the module name with "PPIx::Utilities", e.g. functionality related to
PPI::Nodes is in PPIx::Utilities::Node.

%prep
%setup -q -n PPIx-Utilities-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \; 2>/dev/null
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/PPIx/
%{_mandir}/man3/PPIx::Utilities.3pm*
%{_mandir}/man3/PPIx::Utilities::Exception::Bug.3pm*
%{_mandir}/man3/PPIx::Utilities::Node.3pm*
%{_mandir}/man3/PPIx::Utilities::Statement.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.001000-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001000-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 1.001000-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.001000-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Paul Howarth <paul@city-fan.org> - 1.001000-1
- Update to 1.001000
  - Add support for Const::Fast to PPIx::Utilities::Statement

* Thu Jul 29 2010 Paul Howarth <paul@city-fan.org> - 1.000001-2
- Re-jig for Fedora submission

* Wed Jun 23 2010 Paul Howarth <paul@city-fan.org> - 1.000001-1
- Initial RPM version
