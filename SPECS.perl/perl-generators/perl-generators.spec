Name:           perl-generators
Version:        1.04
Release:        3%{?dist}
Summary:        RPM Perl dependencies generators
Group:          Development/Libraries
License:        GPL+
URL:            http://jplesnik.fedorapeople.org/generators
Source0:        %{url}/generators-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# The generators and attribute files were split from rpm-build
Conflicts:      rpm-build < 4.11.2-15

%description
This package provides RPM Perl dependencies generators which are used for
getting provides and requires from Perl binaries and modules.

%prep
%setup -q -n generators-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor INSTALLVENDORSCRIPT=%{_rpmconfigdir}
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} $RPM_BUILD_ROOT/*

mkdir -p %{buildroot}%{_rpmconfigdir}/fileattrs/
install -p -m 644 fileattrs/* '%{buildroot}%{_rpmconfigdir}/fileattrs'

%check
make test

%files
%doc Changes TODO
%{_rpmconfigdir}/perl.*
%{_rpmconfigdir}/fileattrs/perl*.attr

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.04-3
- 为 Magic 3.0 重建

* Fri Aug 14 2015 Liu Di <liudidi@gmail.com> - 1.04-2
- 为 Magic 3.0 重建

* Wed Jul 29 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-1
- 1.04 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.03-2
- Perl 5.22 rebuild

* Mon Feb 02 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.03-1
- 1.03 bump
- Update parcing of here-doc and quoted section

* Fri Dec 12 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.02-1
- 1.02 bump

* Tue Oct 21 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-1
- 1.01 bump

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.00-2
- Perl 5.20 rebuild

* Mon Jun 16 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.00-1
- Introduce Perl generators as a standalone package
