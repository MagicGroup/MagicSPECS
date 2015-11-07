Name:           perl-mime-construct
Version:        1.11
Release:        12%{?dist}
Summary:        Construct/send MIME messages from the command line 

Group:          Development/Libraries
License:        GPLv2+
URL:            http://search.cpan.org/~rosch/mime-construct-%{version}
Source0:        http://search.cpan.org/CPAN/authors/id/R/RO/ROSCH/mime-construct-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(MIME::Types)
BuildRequires:  perl(Proc::WaitStat)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
mime-construct constructs and (by default) mails MIME messages.  
It is entirely driven from the command line, it is designed to be used 
by other programs, or people who act like programs.


%prep
%setup -q -n mime-construct-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor 
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README debian/changelog debian/copyright
%{_bindir}/*
%{_mandir}/man?/*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.11-12
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.11-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.11-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.11-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.11-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.11-7
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.11-5
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.11-3
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Jun 29 2010 Matthias Runge <mrunge@matthias-runge.de> 1.11-2
- fix up dependencies

* Thu Jun 22 2010 Matthias Runge <mrunge@matthias-runge.de> 1.11-1
- version updated to 1.11

* Tue Jun 22 2010 Matthias Runge <mrunge@matthias-runge.de> 1.10-2
- SPEC-file fixes (URL, include changelog)

* Tue Jun 8 2010 Matthias Runge <mrunge@matthias-runge.de> 1.10-1
- initial version
