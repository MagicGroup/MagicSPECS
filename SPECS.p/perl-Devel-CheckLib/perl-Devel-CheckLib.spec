Name:           perl-Devel-CheckLib
Version:        0.98
Release:        5%{?dist}
Summary:        Check that a library is available

License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Devel-CheckLib/
Source0:        http://www.cpan.org/modules/by-module/Devel/Devel-CheckLib-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp) >= 0.16
BuildRequires:  perl(Text::ParseWords)
# Tests:
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::CaptureOutput) >= 1.0801
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.62

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Devel::CheckLib is a perl module that checks whether a particular C library
and its headers are available.

%prep
%setup -q -n Devel-CheckLib-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check


%files
%doc CHANGES README TODO
%{_bindir}/*
%{perl_vendorlib}/Devel*
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.98-5
- 为 Magic 3.0 重建

* Thu Oct 18 2012 Petr Pisar <ppisar@redhat.com> - 0.98-4
- Specify all dependencies
- Package TODO

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 0.98-2
- Perl 5.16 rebuild

* Sat Mar 17 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.98-1
- Update to 0.98.

* Mon Feb 27 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.97-1
- Update to 0.97.

* Fri Feb  3 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.96-1
- Update to 0.96.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 23 2011 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.95-1
- Update to 0.95.

* Wed Oct 19 2011 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.94-1
- First build.
