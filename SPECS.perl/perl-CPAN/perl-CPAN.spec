%global base_version 2.10

Name:           perl-CPAN
Version:        2.11
Release:        348%{?dist}
Summary:        Query, download and build perl modules from CPAN sites
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/CPAN/
Source0:        http://www.cpan.org/authors/id/A/AN/ANDK/CPAN-%{base_version}.tar.gz
# Unbundled from perl 5.21.11
Patch0:         CPAN-2.10-Upgrade-to-2.11.patch
# Create site paths for the first time, bug #1158873, CPAN RT#99905
Patch1:         CPAN-2.11-Attemp-to-create-site-library-directories-on-first-t.patch
# Change configuration directory name
Patch2:         CPAN-2.11-Replace-configuration-directory-string-with-a-marke.patch
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Optional:
BuildRequires:  perl(File::Spec)
%if !%{defined perl_bootstrap}
BuildRequires:  perl(YAML::Syck)
%endif

# Run-time:
# Prefer Archive::Tar and Compress::Zlib over tar and gzip
BuildRequires:  perl(Archive::Tar) >= 1.50
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Archive::Zip)
%endif
BuildRequires:  perl(autouse)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.121
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
# Devel::Size not used at tests
BuildRequires:  perl(DirHandle)
BuildRequires:  perl(Dumpvalue)
BuildRequires:  perl(Exporter)
# ExtUtils::Manifest not used at tests
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
# File::HomeDir 0.65 not used at tests
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp) >= 0.16
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(Getopt::Std)
# HTTP::Date is optional, prefer in-core Time::Local
# HTTP::Request is optional
BuildRequires:  perl(HTTP::Tiny) >= 0.005
BuildRequires:  perl(if)
BuildRequires:  perl(lib)
# local::lib is optional
# LWP is optional, prefer HTTP::Tiny and Net::FTP
# LWP::UserAgent is optional
# Mac::BuildTools not needed
# Mac::Files not needed
# Module::Signature is optional
# Net::Config not used at tests
# Net::FTP not used at tests
BuildRequires:  perl(Net::Ping)
BuildRequires:  perl(overload)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Safe)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl(Term::ReadLine)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(Text::Wrap)
# Time::Local not used at tests
# URI not used at tests
# URI::Escape not used at tests
# URI::URL 0.08 is optional 
# User::pwent not used at tests
BuildRequires:  perl(warnings)
# Optional:
BuildRequires:  perl(CPAN::Meta) >= 2.110350
# Crypt::OpenPGP not used at tests
# Digest::MD5 not used at tests
BuildRequires:  perl(Digest::SHA)
# Keep MIME::Base64 optional
BuildRequires:  perl(Module::Build)

# Tests:
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Test::More)

# Optional tests:
BuildRequires:  %{_bindir}/gpg
# Digest::SHA1 not needed if Digest::SHA is available
# Digest::SHA::PurePerl not needed if Digest::SHA is available
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Expect)
%endif
BuildRequires:  perl(Hash::Util)
%if !%{defined perl_bootstrap}
# Kwalify not yet packaged
BuildRequires:  perl(Module::Signature) >= 0.66
BuildRequires:  perl(Perl::Version)
%endif
BuildRequires:  perl(Socket)
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Sort::Versions)
# Test::MinimumVersion not used
# Test::Perl::Critic not used
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 0.18
BuildRequires:  perl(YAML) >= 0.60
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Archive::Tar) >= 1.50
Requires:       perl(CPAN::Meta::Requirements) >= 2.121
Requires:       perl(Data::Dumper)
%if !%{defined perl_bootstrap}
Requires:       perl(Devel::Size)
%endif
Requires:       perl(ExtUtils::Manifest)
%if !%{defined perl_bootstrap}
Requires:       perl(File::HomeDir) >= 0.65
%endif
Requires:       perl(File::Temp) >= 0.16
Requires:       perl(lib)
Requires:       perl(Net::Config)
Requires:       perl(Net::FTP)
Requires:       perl(POSIX)
Requires:       perl(Term::ReadLine)
Requires:       perl(Time::Local)
%if !%{defined perl_bootstrap}
Requires:       perl(URI)
Requires:       perl(URI::Escape)
%endif
Requires:       perl(User::pwent)
# Optional but higly recommended:
%if !%{defined perl_bootstrap}
Requires:       perl(Archive::Zip)
Requires:       perl(Compress::Bzip2)
Requires:       perl(CPAN::Meta) >= 2.110350
%endif
Requires:       perl(Compress::Zlib)
Requires:       perl(Digest::MD5)
# CPAN encourages Digest::SHA strongly because of integrity checks
Requires:       perl(Digest::SHA)
Requires:       perl(Dumpvalue)
Requires:       perl(ExtUtils::CBuilder)
%if ! %{defined perl_bootstrap}
# Avoid circular deps local::lib -> Module::Install -> CPAN when bootstraping
# local::lib recommended by CPAN::FirstTime default choice, bug #1122498
Requires:       perl(local::lib)
%endif
Requires:       perl(Module::Build)
%if !%{defined perl_bootstrap}
Requires:       perl(Text::Glob)
%endif
Provides:       cpan = %{version}

# Filter non-Linux dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Mac::BuildTools\\)
# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(CPAN::Meta::Requirements\\)


%description
The CPAN module automates or at least simplifies the make and install of
perl modules and extensions. It includes some primitive searching
capabilities and knows how to use LWP, HTTP::Tiny, Net::FTP and certain
external download clients to fetch distributions from the net.

%prep
%setup -q -n CPAN-%{base_version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
# Change configuration name
find -type f -exec sed -i -e 's/XCPANCONFIGNAMEX/cpan/g' {} \;
# Remove bundled modules
rm -r ./inc/*
sed -i -e '/inc\//d' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes PAUSE*.pub README Todo
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 2.11-348
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.11-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.11-345
- Increase release to favour standalone package

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.11-2
- Perl 5.22 rebuild

* Wed May 06 2015 Petr Pisar <ppisar@redhat.com> - 2.11-1
- 2.11 bump in order to dual-live with perl 5.22

* Fri Mar 13 2015 Petr Pisar <ppisar@redhat.com> - 2.10-1
- 2.10 bump

* Wed Jan 28 2015 Petr Pisar <ppisar@redhat.com> - 2.05-309
- Allow changing the configuration directory name

* Thu Oct 30 2014 Petr Pisar <ppisar@redhat.com> - 2.05-308
- Create site paths for the first time (bug #1158873)

* Wed Sep 10 2014 Petr Pisar <ppisar@redhat.com> 2.05-307
- Synchronize to perl.spec modifications
- Disable non-core modules when bootstrapping

* Tue Apr 22 2014 Petr Pisar <ppisar@redhat.com> 2.05-1
- Specfile autogenerated by cpanspec 1.78.
