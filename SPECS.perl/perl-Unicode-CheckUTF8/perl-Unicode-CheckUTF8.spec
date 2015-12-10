# License information:
#
# This code is largely a Perl wrapper around data tables provided by the
# Unicode Consortium under their Unicode Character Database Terms Of Use
#
# Upstream is happy for us to distribute the Perl parts under any terms
# we like, so I have selected the standard "same as Perl" terms of
# "GPL+ or Artistic"
#
# Ref: https://rt.cpan.org/Public/Bug/Display.html?id=70210

Summary:	Checks if scalar is valid UTF-8
Name:		perl-Unicode-CheckUTF8
Version:	1.03
Release:	13%{?dist}
License:	UCD and (GPL+ or Artistic)
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Unicode-String/
Source0:	http://search.cpan.org/CPAN/authors/id/B/BR/BRADFITZ/Unicode-CheckUTF8-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(base)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(XSLoader)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This is an XS wrapper around some Unicode Consortium code to check if a string
is valid UTF-8, revised to conform to what expat/Mozilla think is valid UTF-8,
especially with regard to low-ASCII characters.

Note that this module has NOTHING to do with Perl's internal UTF8 flag on
scalars.

This module is for use when you're getting input from users and want to make
sure it's valid UTF-8 before continuing.

%prep
%setup -q -n Unicode-CheckUTF8-%{version} 

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES
%{perl_vendorarch}/Unicode/
%{perl_vendorarch}/auto/Unicode/
%{_mandir}/man3/Unicode::CheckUTF8.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.03-13
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.03-12
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.03-11
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.03-10
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.03-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.03-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 24 2011 Paul Howarth <paul@city-fan.org> - 1.03-2
- Sanitize for Fedora submission

* Thu Aug 11 2011 Paul Howarth <paul@city-fan.org> - 1.03-1
- Initial RPM version
