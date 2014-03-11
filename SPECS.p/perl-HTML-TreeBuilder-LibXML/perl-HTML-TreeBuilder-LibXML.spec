Name:           perl-HTML-TreeBuilder-LibXML
Version:        0.17
Release:        4%{?dist}
Summary:        HTML::TreeBuilder and XPath compatible interface with libxml
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/HTML-TreeBuilder-LibXML/
Source0:        http://www.cpan.org/authors/id/T/TO/TOKUHIROM/HTML-TreeBuilder-LibXML-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(inc::Module::Install)
BuildRequires:  perl(HTML::TreeBuilder::XPath) >= 0.14
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(XML::LibXML) >= 1.7

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# not picked up by rpm deptracker
Requires:       perl(HTML::TreeBuilder::XPath) >= 0.14
Requires:       perl(XML::LibXML) >= 1.7

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(XML::LibXML\\)

%description
HTML::TreeBuilder::XPath is a libxml based compatible interface to
HTML::TreeBuilder, which could be slow for a large document.
HTML::TreeBuilder::LibXML is drop-in-replacement for HTML::TreeBuilder::XPath.

%prep
%setup -q -n HTML-TreeBuilder-LibXML-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.17-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.17-2
- Perl 5.16 rebuild

* Mon Jun 11 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.17-1
- Update to 0.17

* Wed Apr 04 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.16-2
- Take into account the review (#809633)

* Tue Apr 03 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.16-1
- Update to 0.16
