Name:           perl-Pango
Version:        1.221
Release:        6%{?dist}
Summary:        Perl interface to the pango library
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://search.cpan.org/dist/Pango/
Source0:        http://www.cpan.org/authors/id/T/TS/TSCH/Pango-%{version}.tar.gz
BuildRequires:  perl(ExtUtils::Depends) >= 0.300 
BuildRequires:  perl(ExtUtils::PkgConfig)
BuildRequires:  perl(Cairo) >= 1.000
BuildRequires:  perl(Glib) >= 1.220
BuildRequires:  perl(Glib::MakeHelper)
BuildRequires:  pango-devel >= 1.0.0
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Cairo) >= 1.000

%description
perl-Pango provides Perl bindings for the text layout/rendering library 
pango. Pango is a library for laying out and rendering text, with an 
emphasis on internationalization. Pango can be used anywhere that text layout 
is needed, but using Pango in conjunction with Cairo and/or Gtk2 provides a 
complete solution with high quality text handling and graphics rendering.

%prep
%setup -q -n Pango-%{version}
%{?perl_default_filter}

chmod -c a-x examples/*.pl

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
# Tests break in odd ways on koji, possibly no-display to blame?
# make test

%files
%defattr(-,root,root,-)
%doc LICENSE NEWS README examples/
%{perl_vendorarch}/Pango*
%{perl_vendorarch}/auto/Pango/
%{_mandir}/man3/*.3pm*

%changelog
* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.221-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.221-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.221-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.221-3
- Perl mass rebuild

* Thu Mar  3 2011 Tom Callaway <spot@fedoraproject.org> - 1.221-2
- drop duplicated requires
- add default perl filtering

* Wed Jan 26 2011 Tom Callaway <spot@fedoraproject.org> - 1.221-1
- initial package
