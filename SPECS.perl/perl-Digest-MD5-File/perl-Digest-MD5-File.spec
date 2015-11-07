Name:		perl-Digest-MD5-File
Version:	0.08
Release:	2%{?dist}
Summary:	Perl extension for getting MD5 sums for files and URLs
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Digest-MD4/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DM/DMUEY/Digest-MD5-File-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Digest::MD5)
BuildRequires:	perl(Encode)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(LWP::UserAgent)
BuildRequires:	perl(Test::More)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Not picked up by rpm
Requires:	perl(Encode)
Requires:	perl(Exporter)
Requires:	perl(File::Spec)

%description
Get MD5 sums for files of a given path or content of a given URL.

%prep
%setup -q -n Digest-MD5-File-%{version}

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
%doc Changes README
%{perl_vendorlib}/Digest/
%{_mandir}/man3/Digest::MD5::File.3pm*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.08-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.08-1
- 更新到 0.08

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.07-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.07-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.07-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.07-5
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 0.07-4
- BR: perl(Carp)

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.07-3
- Perl mass rebuild

* Thu May  5 2011 Paul Howarth <paul@city-fan.org> - 0.07-2
- BR/R: perl(Encode), perl(Exporter), perl(File::Spec) (#702277)

* Thu May  5 2011 Paul Howarth <paul@city-fan.org> - 0.07-1
- Initial RPM version
