Name:           perl-Dist-Zilla
Version:        4.300006
Release:        4%{?dist}
Summary:        Distribution builder; installer not included!
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Dist-Zilla/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/Dist-Zilla-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl >= 1:v5.8.5
BuildRequires:  perl(App::Cmd) >= 0.307
BuildRequires:  perl(App::Cmd::Setup) >= 0.309
BuildRequires:  perl(App::Cmd::Tester) >= 0.306
BuildRequires:  perl(Archive::Tar)
BuildRequires:  perl(autobox) >= 2.53
BuildRequires:  perl(Config::INI::Reader)
BuildRequires:  perl(Config::MVP::Assembler)
BuildRequires:  perl(Config::MVP::Assembler::WithBundles)
BuildRequires:  perl(Config::MVP::Reader) >= 2.101540
BuildRequires:  perl(Config::MVP::Reader::Findable::ByExtension)
BuildRequires:  perl(Config::MVP::Reader::Finder)
BuildRequires:  perl(Config::MVP::Reader::INI) >= 2
BuildRequires:  perl(Config::MVP::Section) >= 2.200001
BuildRequires:  perl(CPAN::Meta::Converter) >= 2.101550
BuildRequires:  perl(CPAN::Meta::Prereqs) >= 2.101390
BuildRequires:  perl(CPAN::Meta::Requirements)
BuildRequires:  perl(CPAN::Meta::Validator) >= 2.101550
BuildRequires:  perl(CPAN::Uploader) >= 0.101550
BuildRequires:  perl(Data::Section) >= 0.004
BuildRequires:  perl(DateTime) >= 0.44
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Encode)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::Manifest) >= 1.54
BuildRequires:  perl(File::Copy::Recursive)
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(File::HomeDir)
BuildRequires:  perl(File::pushd)
BuildRequires:  perl(File::ShareDir)
BuildRequires:  perl(File::ShareDir::Install) >= 0.03
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Hash::Merge::Simple)
BuildRequires:  perl(JSON) >= 2
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
BuildRequires:  perl(Path::Class)
BuildRequires:  perl(Perl::PrereqScanner) >= 1.005
BuildRequires:  perl(Perl::Version)
BuildRequires:  perl(Pod::Eventual) >= 0.091480
BuildRequires:  perl(PPI)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Software::License) >= 0.101370
BuildRequires:  perl(Software::LicenseUtils)
BuildRequires:  perl(String::Formatter) >= 0.100680
BuildRequires:  perl(String::RewritePrefix) >= 0.005
BuildRequires:  perl(Sub::Exporter)
BuildRequires:  perl(Sub::Exporter::ForMethods)
BuildRequires:  perl(Sub::Exporter::Util)
BuildRequires:  perl(Term::ReadKey)
BuildRequires:  perl(Term::ReadLine)
BuildRequires:  perl(Term::ReadLine::Gnu)
BuildRequires:  perl(Term::UI)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Text::Glob) >= 0.08
BuildRequires:  perl(Text::Template)
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(version)
BuildRequires:  perl(YAML::Tiny)
Requires:       perl(autobox) >= 2.53
Requires:       perl(Class::Load)
Requires:       perl(Config::INI::Reader)
Requires:       perl(Config::MVP::Reader::INI)
Requires:       perl(Config::MVP::Assembler)
Requires:       perl(Config::MVP::Assembler::WithBundles)
Requires:       perl(Config::MVP::Reader::Findable)
Requires:       perl(Config::MVP::Reader::Finder)
Requires:       perl(File::chdir)
Requires:       perl(File::ShareDir::Install) >= 0.03
Requires:       perl(Perl::Version)
Requires:       perl(Software::LicenseUtils)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

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
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

# install bash_completion script
install -D -m 0644 misc/dzil-bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/dzil

%check


%files
%doc Changes LICENSE README todo
%{perl_vendorlib}/*
%{_bindir}/dzil
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_sysconfdir}/bash_completion.d

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 4.300006-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 4.300006-3
- 为 Magic 3.0 重建

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
