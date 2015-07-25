Name:               perl-Ham-Reference-QRZ
Version:            0.03
Release:            6%{?dist}
Summary:            An object oriented front end for the QRZ.COM Amateur Radio call-sign database	
Group:              Development/Libraries
License:            Artistic 2.0
URL:                http://search.cpan.org/dist/Ham-Reference-QRZ/
Source0:            http://www.cpan.org/modules/by-module/Ham/BRADMC/Ham-Reference-QRZ-%{version}.tar.gz
BuildArch:          noarch
BuildRequires:      perl(ExtUtils::MakeMaker)
BuildRequires:      perl(HTML::Entities)
BuildRequires:      perl(LWP::UserAgent)
BuildRequires:      perl(XML::Simple)
# Tests
BuildRequires:      perl(Pod::Coverage) >= 0.18
BuildRequires:      perl(Test::More)
BuildRequires:      perl(Test::Pod::Coverage) >= 1.08
BuildRequires:      perl(Test::Pod) >= 1.22
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
An object oriented front end for the QRZ.COM Amateur Radio call-sign database.

%prep
%setup -q -n Ham-Reference-QRZ-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes README LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.03-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.03-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.03-4
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.03-2
- Perl mass rebuild

* Wed Jun 22 2011 Petr Sabata <contyk@redhat.com> - 0.03-1
- 0.03 bump
- License change to Artistic 2.0
- General cleanup, removing Buildroot and defattr

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-4
- Mass rebuild with perl-5.12.0

* Wed Feb 24 2010 Jens Maucher <jensm@fedoraproject.org> - 0.02-3
- Added perl(Test::Pod::Coverage) and perl(Test::Pod) to BuildRequires
- Added MODULE_COMPAT Require

* Mon Feb 22 2010 Jens Maucher <jensm@fedoraproject.org> - 0.02-2
- Changed License
- Edit Summary
- Changed URL and SourceURL
- Added BuildArch
- Deleted Requires, because these are available as rpm in database
  and will automatically added

* Wed Feb 17 2010 Jens Maucher <jensm@fedoraproject.org> - 0.02-1
- Initial release
