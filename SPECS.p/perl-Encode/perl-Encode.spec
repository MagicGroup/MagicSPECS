Name:           perl-Encode
Epoch:          1
Version:        2.62
Release:        2%{?dist}
Summary:        Character encodings in Perl
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Encode/
Source0:        http://www.cpan.org/authors/id/D/DA/DANKOGAI/Encode-%{version}.tar.gz
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter) >= 5.57
# Filter::Util::Call is optional
BuildRequires:  perl(Getopt::Long)
# I18N::Langinfo is optional
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent) >= 0.221
# PerlIO::encoding is optional
BuildRequires:  perl(re)
# Storable is optional
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(XSLoader)
# Tests:
# Benchmark not used
BuildRequires:  perl(charnames)
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IPC::Open3)
# IPC::Run not used
BuildRequires:  perl(lib)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Scalar)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(parent) >= 0.221

%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\((Encode::ConfigLocal|MY)\\)

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Exporter|parent)\\)$

%description
The Encode module provides the interface between Perl strings and the rest
of the system. Perl strings are sequences of characters.

# To mirror files from perl-devel (bug #456534)
# Keep architecture specific because files go into vendorarch
%package devel
Summary:        Perl Encode Module Generator
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl-devel
Requires:       perl(Encode)

%description devel
enc2xs builds a Perl extension for use by Encode from either Unicode Character
Mapping files (.ucm) or Tcl Encoding Files (.enc). You can use enc2xs to add
your own encoding to perl. No knowledge of XS is necessary.


%prep
%setup -q -n Encode-%{version}

%build
# Additional scripts can be installed by appending MORE_SCRIPTS, UCM files by
# INSTALL_UCM.
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc AUTHORS Changes README
%{_bindir}/piconv
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Encode*
%exclude %{perl_vendorarch}/Encode/*.e2x
%exclude %{perl_vendorarch}/Encode/encode.h
%{perl_vendorarch}/encoding.pm
%{_mandir}/man1/piconv.*
%{_mandir}/man3/*

%files devel
%{_bindir}/enc2xs
%{_mandir}/man1/enc2xs.*
%{perl_vendorarch}/Encode/*.e2x
%{perl_vendorarch}/Encode/encode.h

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Petr Pisar <ppisar@redhat.com> - 1:2.62-1
- 2.62 bump

* Wed Apr 30 2014 Petr Pisar <ppisar@redhat.com> - 1:2.60-1
- 2.60 bump

* Mon Apr 14 2014 Petr Pisar <ppisar@redhat.com> - 1:2.59-1
- 2.59 bump

* Mon Mar 31 2014 Petr Pisar <ppisar@redhat.com> - 1:2.58-1
- 2.58 bump

* Fri Jan 03 2014 Petr Pisar <ppisar@redhat.com> - 1:2.57-1
- 2.57 bump

* Mon Sep 16 2013 Petr Pisar <ppisar@redhat.com> - 1:2.55-1
- 2.55 bump

* Mon Sep 02 2013 Petr Pisar <ppisar@redhat.com> - 1:2.54-1
- 2.54 bump

* Wed Aug 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.52-1
- 2.52 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.51-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 1:2.51-6
- Specify more dependencies

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1:2.51-5
- Put epoch into dependecny declaration

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:2.51-4
- Link minimal build-root packages against libperl.so explicitly

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:2.51-3
- Perl 5.18 rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:2.51-2
- Perl 5.18 rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:2.51-1
- Increase epoch to compete with perl.spec

* Fri May 17 2013 Petr Pisar <ppisar@redhat.com> - 2.51-2
- Specify all dependencies

* Thu May 02 2013 Petr Pisar <ppisar@redhat.com> - 2.51-1
- 2.51 bump

* Mon Apr 29 2013 Petr Pisar <ppisar@redhat.com> - 2.50-1
- 2.50 bump (recoding does not launders taintedness)

* Tue Mar 05 2013 Petr Pisar <ppisar@redhat.com> - 2.49-1
- 2.49 bump

* Mon Feb 18 2013 Petr Pisar <ppisar@redhat.com> - 2.48-1
- 2.48 bump

* Thu Sep 20 2012 Petr Pisar <ppisar@redhat.com> 2.47-1
- Specfile autogenerated by cpanspec 1.78.
- Make devel sub-package architecture specific due to file location
