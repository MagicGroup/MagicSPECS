Name:           perl-Finance-YahooQuote
Version:        0.24
Release:        8%{?dist}
Summary:        Perl interface to get stock quotes from Yahoo! Finance

Group:          Development/Libraries
License:        GPLv2+
URL:            http://search.cpan.org/~edd/Finance-YahooQuote/
Source0:        http://www.cpan.org/authors/id/E/ED/EDD/Finance-YahooQuote-%{version}.tar.gz

BuildArch:      noarch 
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Perl interface to get stock quotes from Yahoo! Finance


%prep
%setup -q -n Finance-YahooQuote-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

# Check is disabled because a package build must not use the network.
#%check
#


%files
%doc GNU-LICENSE
%{_bindir}/yahooquote
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.24-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.24-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Petr Sabata <contyk@redhat.com> - 0.24-5
- Perl mass rebuild
- Buildroot and defattr removed

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.24-3
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.24-2
- Mass rebuild with perl-5.12.0

* Mon Mar 30 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.24-1
- Update to 0.24

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.22-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 13 2009 Warren Togami <wtogami@redhat.com> - 0.22-1
- 0.22

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.21-3.1
Rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.21-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sun Sep 24 2006 Warren Togami <wtogami@redhat.com> 0.21-2
- disable %%check because it required network

* Sun Sep 24 2006 Warren Togami <wtogami@redhat.com> 0.21-1
- initial Fedora package
