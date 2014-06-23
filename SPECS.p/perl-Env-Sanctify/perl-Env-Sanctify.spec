Name:		perl-Env-Sanctify
Summary:	Lexically scoped sanctification of %%ENV
Version:	1.06
Release:	6%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Env-Sanctify/
Source0:	http://search.cpan.org/CPAN/authors/id/B/BI/BINGOS/Env-Sanctify-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	perl(ExtUtils::MakeMaker)
# Test suite
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Env::Sanctify is a module that provides lexically-scoped manipulation and
sanctification of %%ENV. You can specify that it alter or add additional
environment variables or remove existing ones according to a list of matching
regexen. You can then either restore the environment back manually or let the
object fall out of scope, which automagically restores. It's useful for
manipulating the environment that forked processes and sub-processes will
inherit.

%prep
%setup -q -n Env-Sanctify-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
 RELEASE_TESTING=1

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README examples/
%{perl_vendorlib}/Env/
%{_mandir}/man3/Env::Sanctify.3pm*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.06-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.06-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.06-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 1.06-2
- Perl 5.16 rebuild

* Thu Mar 15 2012 Paul Howarth <paul@city-fan.org> - 1.06-1
- Update to 1.06
  - Convert distribution to dzil using dzooky (fixes CPAN RT#75714)
- BR: perl(Pod::Coverage::TrustPod)
- Module::Install no longer bundled, so drop buildreqs needed by it
- Drop UTF8 patch, no longer needed

* Mon Mar 12 2012 Paul Howarth <paul@city-fan.org> - 1.04-2
- Add buildreqs for modules used by bundled Module::Install (#802377)

* Mon Mar 12 2012 Paul Howarth <paul@city-fan.org> - 1.04-1
- Initial RPM package
