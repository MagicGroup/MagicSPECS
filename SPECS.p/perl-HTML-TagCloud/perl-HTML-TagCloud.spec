Name:       perl-HTML-TagCloud 
Version:    0.37
Release:    3%{?dist}
# lib/HTML/TagCloud.pm -> GPL+ or Artistic
License:    GPL+ or Artistic 
Group:      Development/Libraries
Summary:    Generate An HTML Tag Cloud 
Source:     http://search.cpan.org/CPAN/authors/id/R/RO/ROBERTSD/HTML-TagCloud-%{version}.tar.gz
Url:        http://search.cpan.org/dist/HTML-TagCloud
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Module::Build::Compat)
BuildRequires: perl(Test::More)
# optional tests
BuildRequires: perl(Test::Pod)
BuildRequires: perl(Test::Pod::Coverage)

%{?perl_default_filter}

%description
The HTML::TagCloud module enables you to generate "tag clouds" in HTML. Tag
clouds serve as a textual way to visualize terms and topics that are used
most frequently. The tags are sorted alphabetically and a larger font is
used to indicate more frequent term usage.

This module provides a simple interface to generating a CSS-based HTML tag
cloud. You simply pass in a set of tags, their URL and their count.  This
module outputs style-sheet-based HTML.  You may use the included CSS or use
your own.

%prep
%setup -q -n HTML-TagCloud-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%files
%doc CHANGES README 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.37-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.37-2
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.37-1
- Update to 0.37
- Clean up spec file
- Add perl default filter

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.34-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.34-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.34-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.34-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.34-1
- submission

* Tue Mar 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.34-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)

