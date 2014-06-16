Name:           perl-Dist-Zilla
Version:        5.015
Release:        2%{?dist}
Summary:        Distribution builder; installer not included!
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Dist-Zilla/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/Dist-Zilla-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(File::ShareDir::Install) >= 0.03
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(App::Cmd::Command::version)
BuildRequires:  perl(App::Cmd::Setup) >= 0.309
BuildRequires:  perl(App::Cmd::Tester) >= 0.306
BuildRequires:  perl(App::Cmd::Tester::CaptureExternal)
# Archive::Tar is a fall-back for missing optional Archive::Tar::Wrapper 0.15
BuildRequires:  perl(Archive::Tar)
BuildRequires:  perl(autodie)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Load) >= 0.17
BuildRequires:  perl(Config)
BuildRequires:  perl(Config::INI::Reader)
BuildRequires:  perl(Config::MVP::Assembler)
BuildRequires:  perl(Config::MVP::Assembler::WithBundles)
BuildRequires:  perl(Config::MVP::Reader) >= 2.101540
BuildRequires:  perl(Config::MVP::Reader::Findable::ByExtension)
BuildRequires:  perl(Config::MVP::Reader::Finder)
# I have no clue how Config::MVP::Reader::INI is used. Without it the tests
# fail.
BuildRequires:  perl(Config::MVP::Reader::INI) >= 2
BuildRequires:  perl(Config::MVP::Section) >= 2.200002
BuildRequires:  perl(CPAN::Meta::Converter) >= 2.101550
BuildRequires:  perl(CPAN::Meta::Prereqs) >= 2.120630
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.121
BuildRequires:  perl(CPAN::Meta::Validator) >= 2.101550
BuildRequires:  perl(CPAN::Uploader) >= 0.103004
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Data::Section) >= 0.200002
BuildRequires:  perl(DateTime) >= 0.44
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Encode)
BuildRequires:  perl(ExtUtils::Manifest) >= 1.54
BuildRequires:  perl(File::Copy::Recursive)
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(File::HomeDir)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::pushd)
BuildRequires:  perl(File::ShareDir)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Hash::Merge::Simple)
BuildRequires:  perl(JSON) >= 2
BuildRequires:  perl(List::AllUtils)
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Log::Dispatchouli) >= 1.102220
BuildRequires:  perl(Moose) >= 0.92
BuildRequires:  perl(Moose::Autobox) >= 0.10
BuildRequires:  perl(Moose::Role)
BuildRequires:  perl(Moose::Util::TypeConstraints)
BuildRequires:  perl(MooseX::LazyRequire)
BuildRequires:  perl(MooseX::Role::Parameterized)
BuildRequires:  perl(MooseX::SetOnce)
BuildRequires:  perl(MooseX::Types)
BuildRequires:  perl(MooseX::Types::Moose)
BuildRequires:  perl(MooseX::Types::Path::Class)
BuildRequires:  perl(MooseX::Types::Perl)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(Params::Util)
BuildRequires:  perl(parent)
BuildRequires:  perl(Path::Class) >= 0.22
BuildRequires:  perl(Path::Tiny)
BuildRequires:  perl(Perl::PrereqScanner) >= 1.016
BuildRequires:  perl(Perl::Version)
BuildRequires:  perl(Pod::Eventual) >= 0.091480
BuildRequires:  perl(PPI)
BuildRequires:  perl(PPI::Document)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Software::License) >= 0.101370
BuildRequires:  perl(Software::LicenseUtils)
BuildRequires:  perl(Storable)
BuildRequires:  perl(String::Formatter) >= 0.100680
BuildRequires:  perl(String::RewritePrefix) >= 0.005
BuildRequires:  perl(Sub::Exporter)
BuildRequires:  perl(Sub::Exporter::ForMethods)
BuildRequires:  perl(Sub::Exporter::Util)
BuildRequires:  perl(Term::Encoding)
BuildRequires:  perl(Term::ReadKey)
BuildRequires:  perl(Term::ReadLine)
BuildRequires:  perl(Term::UI)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Text::Glob) >= 0.08
BuildRequires:  perl(Text::Template)
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(version)
BuildRequires:  perl(YAML::Tiny)
# Optional run-time:
# Archive::Tar::Wrapper 0.15
# Tests:
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(lib)
BuildRequires:  perl(Software::License::None)
BuildRequires:  perl(Test::FailWarnings)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::File::ShareDir)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(utf8)
# Optional tests:
BuildRequires:  perl(CPAN::Meta)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(App::Cmd::Command::version)
# Archive::Tar is a fall-back for missing optional Archive::Tar::Wrapper 0.15
Requires:       perl(Archive::Tar)
#Requires:       perl(autobox) >= 2.53
Requires:       perl(Class::Load) >= 0.17
Requires:       perl(Config::INI::Reader)
Requires:       perl(Config::MVP::Assembler)
Requires:       perl(Config::MVP::Assembler::WithBundles)
Requires:       perl(Config::MVP::Reader::Findable::ByExtension)
Requires:       perl(Config::MVP::Reader::Finder)
# I have no clue how Config::MVP::Reader::INI is used. Without it the tests
# fail.
Requires:       perl(Config::MVP::Reader::INI) >= 2
Requires:       perl(CPAN::Meta::Converter) >= 2.101550
Requires:       perl(CPAN::Meta::Validator) >= 2.101550
Requires:       perl(CPAN::Uploader) >= 0.103004
Requires:       perl(Encode)
Requires:       perl(ExtUtils::Manifest) >= 1.54
Requires:       perl(File::Path)
Requires:       perl(File::ShareDir::Install) >= 0.03
Requires:       perl(Hash::Merge::Simple)
Requires:       perl(Path::Class) >= 0.22
Requires:       perl(Perl::Version)
Requires:       perl(Pod::Eventual) >= 0.091480
Requires:       perl(PPI::Document)
Requires:       perl(Software::LicenseUtils)
Requires:       perl(Term::Encoding)
Requires:       perl(Term::ReadKey)
Requires:       perl(Term::ReadLine)
Requires:       perl(Term::UI)

%{?perl_default_filter}
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((App::Cmd::Setup|Class::Load|CPAN::Meta::Requirements|Moose|Moose::Autobox|Path::Class|String::RewritePrefix)\\)$

%description
Dist::Zilla builds distributions of code to be uploaded to the CPAN. In
this respect, it is like ExtUtils::MakeMaker, Module::Build, or
Module::Install. Unlike those tools, however, it is not also a system for
installing code that has been downloaded from the CPAN. Since it's only run
by authors, and is meant to be run on a repository checkout rather than on
published, released code, it can do much more than those tools, and is free
to make much more ludicrous demands in terms of prerequisites.

%prep
%setup -q -n Dist-Zilla-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

# install bash_completion script
install -D -m 0644 misc/dzil-bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/dzil

%check
make test

%files
%doc Changes LICENSE README todo
%{perl_vendorlib}/*
%{_bindir}/dzil
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_sysconfdir}/bash_completion.d

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.015-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 Petr Pisar <ppisar@redhat.com> - 5.015-1
- 5.015 bump

* Sun Aug 04 2013 Petr Pisar <ppisar@redhat.com> - 4.300023-4
- Perl 5.18 rebuild
- Specify all dependencies

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.300023-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.300023-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Sep 09 2012 Iain Arnell <iarnell@gmail.com> 4.300023-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.300018-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Petr Pisar <ppisar@redhat.com> - 4.300018-2
- Perl 5.16 rebuild

* Sat Jun 09 2012 Iain Arnell <iarnell@gmail.com> 4.300018-1
- update to latest upstream version

* Sat May 12 2012 Iain Arnell <iarnell@gmail.com> 4.300016-1
- update to latest upstream version

* Tue Apr 17 2012 Iain Arnell <iarnell@gmail.com> 4.300014-1
- update to latest upstream version

* Mon Mar 19 2012 Iain Arnell <iarnell@gmail.com> 4.300010-1
- update to latest upstream version

* Wed Feb 22 2012 Iain Arnell <iarnell@gmail.com> 4.300009-1
- update to latest upstream version

* Sun Feb 19 2012 Iain Arnell <iarnell@gmail.com> 4.300008-1
- update to latest upstream version

* Sat Feb 04 2012 Iain Arnell <iarnell@gmail.com> 4.300007-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.300006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan  3 2012 Marcela Mašláňová <mmaslano@redhat.com> 4.30006-1
- update to the latest upstream version
- change BR and R according to new release

* Fri Sep 23 2011 Iain Arnell <iarnell@gmail.com> 4.300002-1
- update to latest upstream version

* Sun Aug 28 2011 Iain Arnell <iarnell@gmail.com> 4.300000-1
- update to latest upstream version

* Thu Aug 18 2011 Iain Arnell <iarnell@gmail.com> 4.200017-1
- update to latest upstream version

* Tue Jul 26 2011 Iain Arnell <iarnell@gmail.com> 4.200012-1
- update to latest upstream

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 4.200008-2
- Perl mass rebuild

* Sat Jun 25 2011 Iain Arnell <iarnell@gmail.com> 4.200008-1
- update to latest upstream version

* Sun Jun 05 2011 Iain Arnell <iarnell@gmail.com> 4.200007-1
- update to latest upstream version

* Sat Apr 30 2011 Iain Arnell <iarnell@gmail.com> 4.200006-1
- update to latest upstream version

* Fri Apr 08 2011 Iain Arnell <iarnell@gmail.com> 4.200004-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.200001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Iain Arnell <iarnell@gmail.com> 4.200001-1
- update to latest upstream version

* Tue Dec 14 2010 Iain Arnell <iarnell@gmail.com> 4.200000-1
- update to latest upstream version
- install bash_completion script

* Sat Nov 20 2010 Iain Arnell <iarnell@gmail.com> 4.102344-1
- update to latest upstream version

* Sun Oct 03 2010 Iain Arnell <iarnell@gmail.com> 4.102341-1
- update to latest upstream
- clean up spec for modern rpmbuild
- requires Moose::Autobox >= 0.10

* Tue Aug 24 2010 Iain Arnell <iarnell@gmail.com> 4.102340-1
- update to latest upstream

* Sun Jul 11 2010 Iain Arnell <iarnell@gmail.com> 4.101900-1
- update to latest upstream

* Sat Jul 03 2010 Iain Arnell <iarnell@gmail.com> 4.101831-1
- update to latest upstream
- BR perl(Term::ReadKey), perl(Term::ReadLine), and perl(Term::UI)
- dzil has a man page now

* Wed Jun 23 2010 Iain Arnell <iarnell@gmail.com> 4.101612-1
- update to latest upstream
- update BRs

* Fri May 14 2010 Iain Arnell - 2.101310-2
- bump for rebuild in dist-f14

* Thu May 13 2010 Iain Arnell <iarnell@gmail.com> 2.101310-1
- update to latest upstream version

* Wed Apr 21 2010 Iain Arnell <iarnell@gmail.com> 2.101040-1
- update to latest upstream

* Wed Apr 07 2010 Iain Arnell <iarnell@gmail.com> 2.100960-1
- Specfile autogenerated by cpanspec 1.78.
- use perl_default_filter and DESTDIR
