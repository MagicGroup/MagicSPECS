Name:		perl-Test-Valgrind
Summary:	Generate suppressions, analyze and test any command with valgrind
Version:	1.13
Release:	7%{?dist}
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Test-Valgrind/
Source0:	http://search.cpan.org/CPAN/authors/id/V/VP/VPIT/Test-Valgrind-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Digest::MD5)
BuildRequires:	perl(Env::Sanctify)
BuildRequires:	perl(ExtUtils::Install)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Fcntl)
BuildRequires:	perl(File::HomeDir) >= 0.86
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp) >= 0.14
BuildRequires:	perl(Filter::Util::Call)
BuildRequires:	perl(lib)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(POSIX)
BuildRequires:	perl(Perl::Destruct::Level)
BuildRequires:	perl(Pod::Coverage) >= 0.18
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Test::Builder)
# Test::Kwalitee -> Module::CPANTS::Analyse -> List::MoreUtils -> Test::LeakTrace -> Test::Valgrind
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Test::Kwalitee)
%endif
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod) >= 1.22
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
BuildRequires:	perl(Test::Portability::Files)
BuildRequires:	perl(XML::Twig)
BuildRequires:	perl(XSLoader)
BuildRequires:	perl(version)
BuildRequires:	valgrind >= 3.1.0
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Carp)
Requires:	perl(Digest::MD5)
Requires:	perl(File::HomeDir) >= 0.86
Requires:	perl(File::Path)
Requires:	perl(File::Temp) >= 0.14
Requires:	perl(Filter::Util::Call)
Requires:	perl(List::Util)
Requires:	perl(Perl::Destruct::Level)
Requires:	perl(XML::Twig)
Requires:	valgrind >= 3.1.0

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
The Test::Valgrind::* API lets you run Perl code through the memcheck tool of
the valgrind memory debugger, to test for memory errors and leaks. The
Test::Valgrind module itself is a front-end to this API. If they aren't
available yet, it will first generate suppressions for the current perl
interpreter and store them in the portable flavor of
~/.perl/Test-Valgrind/suppressions/$VERSION. The actual run will then take
place, and tests will be passed or failed according to the result of the
analysis.

The complete API is much more versatile than this. By declaring an appropriate
Test::Valgrind::Command class, you can run any executable (that is, not only
Perl scripts) under valgrind, generate the corresponding suppressions
on-the-fly and convert the analysis result to TAP output so that it can be
incorporated into your project's test suite. If you're not interested in
producing TAP, you can output the results in whatever format you like (for
example HTML pages) by defining your own Test::Valgrind::Action class.

%prep
%setup -q -n Test-Valgrind-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}

# The package is noarch; the XS code included is for testing purposes and is
# not part of the module itself
if [ "%{perl_vendorarch}" != "%{perl_vendorlib}" ]; then
	mkdir -p %{buildroot}%{perl_vendorlib}
	mv %{buildroot}%{perl_vendorarch}/* %{buildroot}%{perl_vendorlib}/
fi

# If we have ExtUtils::Install < 1.3702, INSTALL.SKIP will be ignored
# and valgrind.so will have been installed, so remove it
if perl -MExtUtils::Install -e 'exit (($ExtUtils::Install::VERSION < 1.3702) ? 0 : 1);'; then
	rm %{buildroot}%{perl_vendorlib}/auto/Test/Valgrind/Valgrind.so
fi

%check


%clean
rm -rf %{buildroot}

%files
%doc Changes README samples/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Valgrind.3pm*
%{_mandir}/man3/Test::Valgrind::Action.3pm*
%{_mandir}/man3/Test::Valgrind::Action::Captor.3pm*
%{_mandir}/man3/Test::Valgrind::Action::Suppressions.3pm*
%{_mandir}/man3/Test::Valgrind::Action::Test.3pm*
%{_mandir}/man3/Test::Valgrind::Carp.3pm*
%{_mandir}/man3/Test::Valgrind::Command.3pm*
%{_mandir}/man3/Test::Valgrind::Command::Aggregate.3pm*
%{_mandir}/man3/Test::Valgrind::Command::Perl.3pm*
%{_mandir}/man3/Test::Valgrind::Command::PerlScript.3pm*
%{_mandir}/man3/Test::Valgrind::Component.3pm*
%{_mandir}/man3/Test::Valgrind::Parser.3pm*
%{_mandir}/man3/Test::Valgrind::Parser::Suppressions::Text.3pm*
%{_mandir}/man3/Test::Valgrind::Parser::Text.3pm*
%{_mandir}/man3/Test::Valgrind::Parser::XML.3pm*
%{_mandir}/man3/Test::Valgrind::Parser::XML::Twig.3pm*
%{_mandir}/man3/Test::Valgrind::Report.3pm*
%{_mandir}/man3/Test::Valgrind::Session.3pm*
%{_mandir}/man3/Test::Valgrind::Suppressions.3pm*
%{_mandir}/man3/Test::Valgrind::Tool.3pm*
%{_mandir}/man3/Test::Valgrind::Tool::memcheck.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.13-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.13-5
- Perl 5.16 re-rebuild of bootstrapped packages

* Mon Jun 18 2012 Petr Pisar <ppisar@redhat.com> - 1.13-4
- Perl 5.16 rebuild

* Thu May  3 2012 Paul Howarth <paul@city-fan.org> - 1.13-3
- Incorporate suggestions from package review (#803057)
  - BR: perl(Pod::Coverage) ≥ 0.18
  - BR: perl(XSLoader)
  - BR: at least version 1.22 of perl(Test::Pod)
  - BR: at least version 1.08 of perl(Test::Pod::Coverage)

* Tue Mar 13 2012 Paul Howarth <paul@city-fan.org> - 1.13-2
- Sanitize for Fedora submission
  - Use Fedora-style dist tag
  - Drop %%defattr, redundant since rpm 4.4

* Mon Mar 12 2012 Paul Howarth <paul@city-fan.org> - 1.13-1
- Initial RPM version
