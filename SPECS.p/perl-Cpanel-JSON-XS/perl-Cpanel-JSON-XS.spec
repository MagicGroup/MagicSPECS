Name:		perl-Cpanel-JSON-XS
Summary:	JSON::XS for Cpanel, fast and correct serializing
Version:	3.0104
Release:	2%{?dist}
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Cpanel-JSON-XS/
Source0:	http://search.cpan.org/CPAN/authors/id/R/RU/RURBAN/Cpanel-JSON-XS-%{version}.tar.gz
# Module Build
BuildRequires:	perl
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(overload)
BuildRequires:	perl(XSLoader)
# Script Runtime
BuildRequires:	perl(Compress::LZF)
BuildRequires:	perl(Convert::Bencode)
BuildRequires:	perl(Data::Dump)
BuildRequires:	perl(YAML)
# Test Suite
BuildRequires:	perl(common::sense) >= 3.5
BuildRequires:	perl(Config)
BuildRequires:	perl(constant)
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(Encode) >= 1.9081
BuildRequires:	perl(Hash::Util)
BuildRequires:	perl(JSON)
BuildRequires:	perl(JSON::XS)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test)
BuildRequires:	perl(Test::LeakTrace)
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(Tie::Array)
BuildRequires:	perl(Tie::Hash)
BuildRequires:	perl(utf8)
BuildRequires:	perl(warnings)
# Maintainer Tests
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(Perl::MinimumVersion) >= 1.20
BuildRequires:	perl(Test::CPAN::Meta) >= 0.12
BuildRequires:	perl(Test::Kwalitee)
BuildRequires:	perl(Test::MinimumVersion) >= 0.008
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:	perl(Test::Pod::Coverage) >= 1.04
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Carp)
Requires:	perl(Compress::LZF)
Requires:	perl(Convert::Bencode)
Requires:	perl(Data::Dump)
Requires:	perl(YAML)

# Avoid unwanted provides and dependencies
%{?perl_default_filter}

%description
This module converts Perl data structures to JSON and vice versa. Its
primary goal is to be correct and its secondary goal is to be fast. To
reach the latter goal it was written in C.

%prep
%setup -q -n Cpanel-JSON-XS-%{version}

# Fix shellbangs
perl -pi -e 's|^#!/opt/bin/perl|#!/usr/bin/perl|' eg/*

# Make sure we don't try to do a signature check
rm SIGNATURE
perl -ni -e 'print unless /SIGNATURE/;' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test IS_MAINTAINER=1 RELEASE_TESTING=1

%files
%doc Changes COPYING README eg/
%{_bindir}/cpanel_json_xs
%{perl_vendorarch}/auto/Cpanel/
%{perl_vendorarch}/Cpanel/
%{_mandir}/man1/cpanel_json_xs.1*
%{_mandir}/man3/Cpanel::JSON::XS.3pm*
%{_mandir}/man3/Cpanel::JSON::XS::Boolean.3pm*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0104-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 26 2014 Paul Howarth <paul@city-fan.org> - 3.0104-1
- Update to 3.0104
  - Add t/z_leaktrace.t
  - Restore build on C89
  - Fix small cxt->sv_json leak on interp exit

* Tue Apr 22 2014 Paul Howarth <paul@city-fan.org> - 3.0103-1
- Update to 3.0103
  - Change booleans interop logic (again) for JSON-XS-3.01
    - Check now for Types::Serialiser::Boolean i.e. JSON::PP::Boolean refs
      (https://github.com/rurban/Cpanel-JSON-XS/issues/18) to avoid
      allow_blessed for JSON-XS-3.01 booleans
  - Fix boolean representation for JSON-XS-3.01/Types::Serialiser::Boolean
    interop (arrayref, not hashref)
  - Add t/52_object.t from JSON::XS
  - Backport encode_hv HE sort on stack < 64 or heap to avoid stack overflows
    from JSON-XS-3.01; do not use alloca
  - Backport allow_tags, decode_tag, FREEZE/THAW callbacks from JSON-XS-3.01
  - Added pod for OBJECT SERIALISATION (allow_tags, FREEZE/THAW)

* Thu Apr 17 2014 Paul Howarth <paul@city-fan.org> - 3.0102-1
- Update to 3.0102
  - Added PERL_NO_GET_CONTEXT for better performance on threaded Perls
  - MANIFEST: added t/96_interop.t
  - Document deprecated functions
  - Change booleans interop logic for JSON-XS-3.01
- Enable CLZF support via Compress::LZF

* Wed Apr 16 2014 Paul Howarth <paul@city-fan.org> - 3.0101-1
- Update to 3.0101
  - Added ithreads support: Cpanel::JSON::XS is now thread-safe
  - const'ed a translation table for memory savings
  - Fixed booleans for JSON 2.9 and JSON-XS-3.01 interop; JSON does not
    support JSON::XS booleans anymore, so I cannot think of any reason to
    still use JSON::XS

* Thu Apr 10 2014 Paul Howarth <paul@city-fan.org> - 2.3404-2
- Incorporate feedback from package review (#1085975)
  - Simplify %%summary
  - Temporarily drop Compress::LZF format support from cpanel_json_xs client
  - Add optional dependencies for module, tests and cpanel_json_xs client

* Wed Apr  9 2014 Paul Howarth <paul@city-fan.org> - 2.3404-1
- Initial RPM version
