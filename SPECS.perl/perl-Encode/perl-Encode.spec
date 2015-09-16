# Because encoding sub-package has independent version, version macro gets
# redefined.
%global cpan_version 2.76
Name:           perl-Encode
Epoch:          3
Version:        %{cpan_version}
# Keep increasing release number even when rebasing version because
# perl-encoding sub-package has independent version which does not change
# often and consecutive builds would clash on perl-encoding NEVRA. This is the
# same case as in perl.spec.
Release:        3%{?dist}
Summary:        Character encodings in Perl
# ucm:          UCD
# other files:  GPL+ or Artistic
License:        (GPL+ or Artistic) and UCD
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Encode/
Source0:        http://www.cpan.org/authors/id/D/DA/DANKOGAI/Encode-%{cpan_version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# enc2xs is run at build-time
# Run-time:
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(Filter::Util::Call)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Getopt::Std)
# I18N::Langinfo is optional
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent) >= 0.221
# PerlIO::encoding is optional
# POSIX is optional
BuildRequires:  perl(re)
# Storable is optional
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(XSLoader)
# Tests:
# Benchmark not used
BuildRequires:  perl(charnames)
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

%package -n perl-encoding
Summary:        Write your Perl script in non-ASCII or non-UTF-8
Version:        2.16
License:        GPL+ or Artistic
Group:          Development/Libraries
# Keeping this sub-package arch-specific because it installs files into
# arch-specific directories.
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
# Config not needed on perl ≥ 5.008
# Consider Filter::Util::Call as mandatory, bug #1165183, CPAN RT#100427
Requires:       perl(Filter::Util::Call)
# I18N::Langinfo is optional
# PerlIO::encoding is optional
Requires:       perl(utf8)
Conflicts:      perl-Encode < 2:2.64-2

%description -n perl-encoding
With the encoding pragma, you can write your Perl script in any encoding you
like (so long as the Encode module supports it) and still enjoy Unicode
support.

However, this encoding module is deprecated under perl 5.18. It uses
a mechanism provided by perl that is deprecated under 5.18 and higher, and may
be removed in a future version.

The easiest and the best alternative is to write your script in UTF-8.

# To mirror files from perl-devel (bug #456534)
# Keep architecture specific because files go into vendorarch
%package devel
Summary:        Perl Encode Module Generator
Version:        %{cpan_version}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{epoch}:%{cpan_version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl-devel
Requires:       perl(Encode)

%description devel
enc2xs builds a Perl extension for use by Encode from either Unicode Character
Mapping files (.ucm) or Tcl Encoding Files (.enc). You can use enc2xs to add
your own encoding to perl. No knowledge of XS is necessary.


%prep
%setup -q -n Encode-%{cpan_version}

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
%{_bindir}/encguess
%{_bindir}/piconv
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Encode*
%exclude %{perl_vendorarch}/Encode/*.e2x
%exclude %{perl_vendorarch}/Encode/encode.h
%{_mandir}/man1/encguess.*
%{_mandir}/man1/piconv.*
%{_mandir}/man3/Encode.*
%{_mandir}/man3/Encode::*

%files -n perl-encoding
%doc AUTHORS Changes README
%{perl_vendorarch}/encoding.pm
%{_mandir}/man3/encoding.*

%files devel
%{_bindir}/enc2xs
%{_mandir}/man1/enc2xs.*
%{perl_vendorarch}/Encode/*.e2x
%{perl_vendorarch}/Encode/encode.h

%changelog
* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 3:2.76-3
- 为 Magic 3.0 重建

* Fri Jul 31 2015 Petr Pisar <ppisar@redhat.com> - 3:2.76-2
- Increase release number to have unique perl-encoding NEVRA

* Fri Jul 31 2015 Petr Pisar <ppisar@redhat.com> - 3:2.76-1
- 2.76 bump

* Wed Jul 01 2015 Petr Pisar <ppisar@redhat.com> - 3:2.75-1
- 2.75 bump

* Thu Jun 25 2015 Petr Pisar <ppisar@redhat.com> - 3:2.74-1
- 2.74 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:2.73-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2:2.73-2
- Perl 5.22 rebuild
- Increase Epoch to favour standalone package

* Mon Apr 20 2015 Petr Pisar <ppisar@redhat.com> - 2:2.73-1
- 2.73 bump

* Mon Mar 16 2015 Petr Pisar <ppisar@redhat.com> - 2:2.72-1
- 2.72 bump

* Thu Mar 12 2015 Petr Pisar <ppisar@redhat.com> - 2:2.71-1
- 2.71 bump

* Wed Mar 04 2015 Petr Pisar <ppisar@redhat.com> - 2:2.70-2
- Correct license from (GPL+ or Artistic) to ((GPL+ or Artistic) and UCD)

* Thu Feb 05 2015 Petr Pisar <ppisar@redhat.com> - 2:2.70-1
- 2.70 bump

* Fri Jan 23 2015 Petr Pisar <ppisar@redhat.com> - 2:2.68-1
- 2.68 bump

* Fri Dec 05 2014 Petr Pisar <ppisar@redhat.com> - 2:2.67-1
- 2.67 bump

* Wed Dec 03 2014 Petr Pisar <ppisar@redhat.com> - 2:2.66-1
- 2.66 bump

* Tue Nov 18 2014 Petr Pisar <ppisar@redhat.com> - 2:2.64-2
- Consider Filter::Util::Call dependency as mandatory (bug #1165183)
- Sub-package encoding module

* Mon Nov 03 2014 Petr Pisar <ppisar@redhat.com> - 2:2.64-1
- 2.64 bump

* Mon Oct 20 2014 Petr Pisar <ppisar@redhat.com> - 2:2.63-1
- 2.63 bump

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:2.62-5
- Increase Epoch to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.62-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

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
