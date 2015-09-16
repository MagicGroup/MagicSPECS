# Note: this package takes the approach of adding a hard dependency on
# upstream's preferred back-end, Cpanel::JSON::XS, rather than using
# a virtual provides/requires arrangement so that any of the supported
# back-ends could be used. This is not only much simpler and does not
# involve modifications to the back-end packages, but it also makes for
# consistent results as we're always using the same, most-tested
# back-end.

Name:		perl-JSON-MaybeXS
Summary:	Use Cpanel::JSON::XS with a fallback to JSON::XS and JSON::PP
Summary(zh_CN.UTF-8): 带有回调 JSON::XS 和 JSON::PP 的使用 Cpanel::JSON::XS
Version:	1.003005
Release:	3%{?dist}
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/JSON-MaybeXS/
Source0:	http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/JSON-MaybeXS-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	perl
BuildRequires:	perl(ExtUtils::CBuilder) >= 0.27
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
# Module Runtime
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Cpanel::JSON::XS) >= 2.3310
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite (wants JSON::PP ≥ 2.27202 really but EL-6 doesn't have that)
BuildRequires:	perl(if)
BuildRequires:	perl(JSON::PP)
BuildRequires:	perl(JSON::XS)
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(Test::Without::Module) >= 0.17
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Cpanel::JSON::XS) >= 2.3310

%description
This module first checks to see if either Cpanel::JSON::XS or JSON::XS
is already loaded, in which case it uses that module. Otherwise it tries
to load Cpanel::JSON::XS, then JSON::XS, then JSON::PP in order, and
either uses the first module it finds or throws an error.
 
It then exports the "encode_json" and "decode_json" functions from the
loaded module, along with a "JSON" constant that returns the class name
for calling "new" on.
 
If you're writing fresh code rather than replacing JSON.pm usage, you
might want to pass options as constructor args rather than calling
mutators, so we provide our own "new" method that supports that.

%description -l zh_CN.UTF-8
带有回调 JSON::XS 和 JSON::PP 的使用 Cpanel::JSON::XS。

%prep
%setup -q -n JSON-MaybeXS-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}
magic_rpm_clean.sh

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/JSON/
%{_mandir}/man3/JSON::MaybeXS.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.003005-3
- 为 Magic 3.0 重建

* Fri Jun 05 2015 Liu Di <liudidi@gmail.com> - 1.003005-2
- 为 Magic 3.0 重建

* Mon Mar 23 2015 Paul Howarth <paul@city-fan.org> - 1.003005-1
- Update to 1.003005
  - Fix x_contributors metadata that was killing metacpan (see
    https://github.com/CPAN-API/cpan-api/issues/401)

* Sun Mar 15 2015 Paul Howarth <paul@city-fan.org> - 1.003004-1
- Update to 1.003004
  - Caveat added to documentation about type checking the object returned by
    new() (CPAN RT#102733)

* Mon Dec  8 2014 Paul Howarth <paul@city-fan.org> - 1.003003-1
- Update to 1.003003
  - Ensure an old Cpanel::JSON::XS is upgraded if it is too old, as it will
    always be used in preference to JSON::XS
  - Avoid "JSON::XS::Boolean::* redefined" warnings caused by an old JSON::XS
    loaded at the same time as a newer Cpanel::JSON::XS

* Sun Nov 16 2014 Paul Howarth <paul@city-fan.org> - 1.003002-1
- Update to 1.003002
  - Correctly fix boolean interoperability with older Cpanel::JSON::MaybeXS

* Thu Nov 13 2014 Paul Howarth <paul@city-fan.org> - 1.003001-1
- Update to 1.003001
  - Add :legacy tag to support legacy apps
  - Fix boolean interoperability with older Cpanel::JSON::MaybeXS

* Wed Oct 22 2014 Paul Howarth <paul@city-fan.org> - 1.002006-1
- Update to 1.002006
  - Add some additional test diagnostics, to help find bad version combinations
    of JSON backends

* Wed Oct 15 2014 Paul Howarth <paul@city-fan.org> - 1.002005-1
- Update to 1.002005
  - Fix "can I haz XS?" logic precedence in Makefile.PL
  - Added the ':all' export tag
  - Removed dependency on Safe::Isa
  - Repository moved to git://git.shadowcat.co.uk/p5sagit/JSON-MaybeXS.git

* Sun Oct 12 2014 Paul Howarth <paul@city-fan.org> - 1.002004-1
- Update to 1.002004
  - Support use of PUREPERL_ONLY in Makefile.PL to avoid adding an XS
    dependency
  - New is_bool() interface

* Wed Oct  8 2014 Paul Howarth <paul@city-fan.org> - 1.002003-1
- Update to 1.002003
  - Document how to use booleans

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.002002-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May  9 2014 Paul Howarth <paul@city-fan.org> - 1.002002-2
- Sanitize for Fedora submission

* Thu Apr 24 2014 Paul Howarth <paul@city-fan.org> - 1.002002-1
- Update to 1.002002
  - More metadata fiddling, to remove the Cpanel::JSON::XS dependency visible
    to static analyzers (the prerequisites at install time remain unchanged)

* Wed Apr 23 2014 Paul Howarth <paul@city-fan.org> - 1.002001-1
- Update to 1.002001
  - Fix installation on older perls with an older ExtUtils::MakeMaker
    (CPAN RT#94964)
- Update patch for building with Test::More < 0.88

* Wed Apr 23 2014 Paul Howarth <paul@city-fan.org> - 1.002000-1
- Initial RPM version
