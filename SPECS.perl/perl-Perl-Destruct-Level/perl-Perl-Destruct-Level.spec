Name:		perl-Perl-Destruct-Level
Summary:	Allows you to change perl's internal destruction level
Version:	0.02
Release:	8%{?dist}
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Perl-Destruct-Level/
Source0:	http://search.cpan.org/CPAN/authors/id/R/RG/RGARCIA/Perl-Destruct-Level-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(XSLoader)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This module allows you to change perl's internal destruction level. The
default value of the destruct level is 0; it means that perl won't bother
destroying all of its internal data structures and lets the OS do the cleanup
for it at exit.

For perls built with debugging support (-DDEBUGGING), an environment variable
PERL_DESTRUCT_LEVEL allows you to control the destruction level. This module
enables you to modify it on non-debugging perls too.

Note that some embedded environments might extend the meaning of the
destruction level for their own purposes: mod_perl does that, for example.

%prep
%setup -q -n Perl-Destruct-Level-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%{perl_vendorarch}/auto/Perl/
%{perl_vendorarch}/Perl/
%{_mandir}/man3/Perl::Destruct::Level.3pm*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.02-8
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.02-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.02-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.02-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.02-3
- Perl 5.16 rebuild

* Tue Mar 13 2012 Paul Howarth <paul@city-fan.org> - 0.02-2
- Sanitize for Fedora submission
  - Drop %%defattr, redundant since rpm 4.4
  - Use Fedora-style dist tag

* Mon Mar 12 2012 Paul Howarth <paul@city-fan.org> - 0.02-1
- Initial RPM version
