Name:           perl-Term-ANSIColor
Version:        4.03
Release:        346%{?dist}
Summary:        Color screen output using ANSI escape sequences
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Term-ANSIColor/
Source0:        http://www.cpan.org/modules/by-module/Term/Term-ANSIColor-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(lib)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module has two interfaces, one through color() and colored() and the
other through constants. It also offers the utility functions uncolor(),
colorstrip(), colorvalid(), and coloralias(), which have to be explicitly
imported to be used. 

%prep
%setup -q -n Term-ANSIColor-%{version}
chmod -c -x examples/*

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc examples LICENSE NEWS README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.03-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.03-345
- Increase release to favour standalone package

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.03-4
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.03-3
- Perl 5.20 rebuild

* Mon Aug 11 2014 David Dick <ddick@cpan.org> - 4.03-2
- Re-adding for master

* Tue Jul 22 2014 David Dick <ddick@cpan.org> - 4.03-1
- Initial release
