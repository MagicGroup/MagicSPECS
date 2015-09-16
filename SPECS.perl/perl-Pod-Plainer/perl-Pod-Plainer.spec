Name: perl-Pod-Plainer
Version:	1.04
Release:	1%{?dist}
Summary: Perl extension for converting Pod to old-style Pod

License: GPL+ or Artistic
URL: http://search.cpan.org/dist/Pod-Plainer/

Source0: http://search.cpan.org/CPAN/authors/id/R/RM/RMBARKER/Pod-Plainer-%{version}.tar.gz

BuildArch: noarch
# Correct for lots of packages, other common choices include eg. Module::Build
BuildRequires: perl(ExtUtils::MakeMaker), perl(Pod::Parser), perl(Test::More), perl(Test::Pod::Coverage) >= 1.00
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Pod::Plainer uses Pod::Parser which takes Pod with the (new) 'C<< .. >>'
constructs and returns the old(er) style with just 'C<>'; '<' and '>' are
replaced by 'E<lt>' and 'E<gt>'.
This can be used to pre-process Pod before using tools which do not
recognize the new style Pods.

%prep
%setup -q -n Pod-Plainer-%{version}

%build
# Remove OPTIMIZE=... from noarch packages (unneeded)
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
#rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
# Remove the next line from noarch packages (unneeded)
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
ls -lZ $RPM_BUILD_ROOT/*
%{_fixperms} $RPM_BUILD_ROOT/*

%check


%files
%doc README Changes
# For noarch packages: vendorlib
%{perl_vendorlib}/Pod/Plainer.pm
%{_mandir}/man3/Pod::Plainer.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.04-1
- 更新到 1.04

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.03-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.03-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.03-2
- Perl 5.16 rebuild

* Mon Mar 26 2012 xning <xning AT redhat DOT com> - 1.03-1
- modified as Petr Šabata's advice
* Fri Mar 02 2012 xning <xning AT redhat DOT com> - 1.03-1
- create for support LSB 4.1
