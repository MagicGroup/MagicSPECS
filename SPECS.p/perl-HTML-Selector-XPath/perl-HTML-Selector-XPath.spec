Name:           perl-HTML-Selector-XPath
Version:        0.14
Release:        5%{?dist}
Summary:        CSS Selector to XPath compiler
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/HTML-Selector-XPath/
Source0:        http://www.cpan.org/authors/id/C/CO/CORION/HTML-Selector-XPath-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl >= 1:5.8.1
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Base)
BuildRequires:  perl(Test::More)

# for improved tests
BuildRequires:  perl(HTML::TreeBuilder::XPath)
BuildRequires:  perl(Test::Pod) >= 1.00

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
HTML::Selector::XPath is a utility function to compile CSS2 selector to the
equivalent XPath expression.

%prep
%setup -q -n HTML-Selector-XPath-%{version}

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
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.14-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.14-2
- 为 Magic 3.0 重建

* Wed Jan 18 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.14-1
- Upstream update.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.12-1
- Upstream update.

* Sat Oct 22 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.09-1
- Upstream update.

* Mon Sep 19 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.08-1
- Upstream update.

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.07-2
- Perl mass rebuild

* Sun Mar 27 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.07-1
- Upstream update.

* Fri Feb 18 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.06-2
- Fix bogus changelog entry.

* Fri Feb 18 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.06-1
- Upstream update.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Ralf Corsépius <corsepiu@fedoraproject.org> 0.04-1
- Initial Fedora package.
