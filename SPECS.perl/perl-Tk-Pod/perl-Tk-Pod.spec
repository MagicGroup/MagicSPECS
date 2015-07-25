%if %fedora >= 17
# F17 and newer has broken X11, re-enable once fixed.
%global use_x11_tests 0
%else
%global use_x11_tests 1
%endif

Name:           perl-Tk-Pod
Version:        0.9940
Release:        5%{?dist}
Summary:        Pod browser top-level widget
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Tk-Pod/
Source0:        http://www.cpan.org/authors/id/S/SR/SREZIC/Tk-Pod-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Pod::Simple) >= 2.05
BuildRequires:  perl(Tk) >= 800.004
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(Devel::Hide)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::Command::MM)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tk::Derived)
BuildRequires:  perl(Tk::ROText)
BuildRequires:  perl(Test)
# Optional tests:
#BuildRequires:  perl(Tk::HistEntry) >= 0.4
#BuildRequires:  perl(Text::English)
%if %{use_x11_tests}
# X11 tests:
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  xorg-x11-xinit
BuildRequires:  font(:lang=en)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(File::Temp)
Requires:       perl(Pod::Simple) >= 2.05
Requires:       perl(Tk) >= 800.004

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Tk(::Pod)?\\)\\s*$
# Remove not-yet-packages optional dependencies
%global __requires_exclude %__requires_exclude|^perl\\(Text::English\\)

%description
Simple Pod browser with hypertext capabilities in a Toplevel widget.

%prep
%setup -q -n Tk-Pod-%{version}
chmod -x Pod_usage.pod

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%if %{use_x11_tests}
    # TODO: Use xvfb-run instead of xinit
    xinit /bin/sh -c 'rm -f ok;  && touch ok' -- /usr/bin/Xvfb :666
    test -e ok
%else
    
%endif

%files
%doc Changes README TODO
%{perl_vendorlib}/*
%{_bindir}/*
%{_mandir}/man3/*
%{_mandir}/man1/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.9940-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.9940-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9940-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.9940-2
- Perl 5.16 rebuild

* Wed Mar 14 2012 Petr Pisar <ppisar@redhat.com> - 0.9940-1
- 0.9940 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9939-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Petr Pisar <ppisar@redhat.com> 0.9939-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot and defattr from spec code