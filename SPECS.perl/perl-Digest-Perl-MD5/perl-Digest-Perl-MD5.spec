Name:		perl-Digest-Perl-MD5
Version:	1.9
Release:	3%{?dist}
Summary:	Perl implementation of Ron Rivest's MD5 Algorithm
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Digest-Perl-MD5/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DE/DELTA/Digest-Perl-MD5-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
A pure-perl implementation of Ron Rivest's MD5 Algorithm.

%prep
%setup -q -n Digest-Perl-MD5-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/Digest/
%{_mandir}/man3/Digest::Perl::MD5.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.9-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.9-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.9-1
- 更新到 1.9

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.8-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.8-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.8-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.8-4
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 1.8-3
- Fedora 17 mass rebuild

* Mon Aug 22 2011 Paul Howarth <paul@city-fan.org> - 1.8-2
- BR: perl (Exporter) and perl(Test) (#732484)

* Mon Aug 22 2011 Paul Howarth <paul@city-fan.org> - 1.8-1
- Initial RPM version
