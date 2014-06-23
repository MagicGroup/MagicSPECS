Name:           perl-Hash-Merge
Version:        0.12
Release:        9%{?dist}
Summary:        Merges arbitrary deep hashes into a single hash
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Hash-Merge/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DM/DMUEY/Hash-Merge-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  perl(Test::More), perl(Clone), perl(ExtUtils::MakeMaker)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
%{summary}.

%prep
%setup -q -n Hash-Merge-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -x %{buildroot}%{perl_vendorlib}/Hash/Merge.pm
%{_fixperms} %{buildroot}/*

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/Hash/
%{_mandir}/man3/*.3*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.12-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.12-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.12-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.12-3
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.12-2
- Mass rebuild with perl-5.12.0

* Wed Mar 17 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.12-1
- PERL_INSTALL_ROOT => DESTDIR, add perl_default_filter
- auto-update to 0.12 (by cpan-spec-update 0.01) (for DBIx::Class)
- added a new br on perl(ExtUtils::MakeMaker) (version 0)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.11-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.11-2
- fix permissions (silence rpmlint too)
- own Hash/ directory

* Fri Jun 26 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.11-1
- initial package for Fedora
