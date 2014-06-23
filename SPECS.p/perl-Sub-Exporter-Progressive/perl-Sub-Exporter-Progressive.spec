# We need to patch the test suite if we have old versions of Test::More
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.88) ? 1 : 0);' 2>/dev/null || echo 0)

Name:		perl-Sub-Exporter-Progressive
Version:	0.001006
Release:	3%{?dist}
Summary:	Only use Sub::Exporter if you need it
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Sub-Exporter-Progressive/
Source0:	http://search.cpan.org/CPAN/authors/id/L/LE/LEONT/Sub-Exporter-Progressive-%{version}.tar.gz
Patch1:		Sub-Exporter-Progressive-0.001006-old-Test::More.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# =============== Module Build ======================
BuildRequires:	perl(ExtUtils::MakeMaker)
# =============== Module Runtime ====================
BuildRequires:	perl(Exporter)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(Sub::Exporter)
# =============== Test Suite ========================
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More)
# =============== Module Runtime ====================
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Exporter)
Requires:	perl(Sub::Exporter)

%description
Sub::Exporter is an incredibly powerful module, but with that power comes
great responsibility, er- as well as some runtime penalties. This module is a
Sub::Exporter wrapper that will let your users just use Exporter if all they
are doing is picking exports, but use Sub::Exporter if your users try to use
Sub::Exporter's more advanced features features, like renaming exports, if
they try to use them.

Note that this module will export @EXPORT and @EXPORT_OK package variables for
Exporter to work. Additionally, if your package uses advanced Sub::Exporter
features like currying, this module will only ever use Sub::Exporter, so you
might as well use it directly.

%prep
%setup -q -n Sub-Exporter-Progressive-%{version}

# We need to patch the test suite if we have old versions of Test::More
%if %{old_test_more}
%patch1
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%doc Changes README
%{perl_vendorlib}/Sub/
%{_mandir}/man3/Sub::Exporter::Progressive.3pm*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.001006-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.001006-2
- 为 Magic 3.0 重建

* Mon Aug 27 2012 Paul Howarth <paul@city-fan.org> - 0.001006-1
- Update to 0.001006
  - Handle ':all' correctly
- Update old Test::More patch
- Drop redundant buildreq perl(Test::Pod)

* Sat Aug 25 2012 Paul Howarth <paul@city-fan.org> - 0.001005-1
- Update to 0.001005
  - Add support for tags
  - Warn if defaults are not in exports
  - Add explicit dependency on Test::More 0.89
- This release by LEONT -> update source URL
- Update old Test::More patch

* Thu Aug  9 2012 Paul Howarth <paul@city-fan.org> - 0.001004-1
- Update to 0.001004 (fix skipping when Sub::Exporter isn't installed)
- This release by MSTROUT -> update source URL
- No LICENSE file in this release
- Update old Test::More patch

* Wed Aug  1 2012 Paul Howarth <paul@city-fan.org> - 0.001003-1
- Update to 0.001003 (remove warning if there are no defaults)

* Wed Aug  1 2012 Paul Howarth <paul@city-fan.org> - 0.001002-2
- Sanitize for Fedora submission

* Wed Aug  1 2012 Paul Howarth <paul@city-fan.org> - 0.001002-1
- Initial RPM build
