Name:           perl-HTML-TreeBuilder-LibXML
Version:	0.25
Release:	1%{?dist}
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
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes README.md
%{perl_vendorlib}/HTML*
%{_mandir}/man3/HTML*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.25-1
- 更新到 0.25

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-5
- 为 Magic 3.0 重建

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
