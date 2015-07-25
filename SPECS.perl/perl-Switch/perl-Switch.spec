Name:		perl-Switch
Version:	2.16
Release:	9%{?dist}
Summary:	A switch statement for Perl
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Switch/
Source0:	http://search.cpan.org/CPAN/authors/id/R/RG/RGARCIA/Switch-%{version}.tar.gz
# From OpenSUSE, fix test failures with perl 5.14
Patch0:		Switch-2.16-perl514.patch
BuildRequires:	perl
%if 0%(perl -e 'print $] > 5.011')
BuildRequires:	perl(deprecate)
%endif
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Filter::Util::Call)
BuildRequires:	perl(if)
BuildRequires:	perl(overload)
BuildRequires:	perl(Text::Balanced)
BuildRequires:	perl(vars)
BuildRequires:	perl(strict)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	perl(overload)
BuildArch:	noarch

%description
Switch.pm provides the syntax and semantics for an explicit case mechanism for 
Perl. The syntax is minimal, introducing only the keywords C<switch> and 
C<case> and conforming to the general pattern of existing Perl control 
structures. The semantics are particularly rich, allowing any one (or more) of 
nearly 30 forms of matching to be used when comparing a switch value with its 
various cases.

%prep
%setup -q -n Switch-%{version}
%patch0 -p1 -b .514

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Switch.pm
%{_mandir}/man3/*.3*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.16-9
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.16-7
- Perl 5.18 rebuild

* Fri Jul 12 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.16-6
- Specify all dependencies
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Remove buildroot cleaning

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.16-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 10 2011 Tom Callaway <spot@fedoraproject.org> - 2.16-1
- initial package
