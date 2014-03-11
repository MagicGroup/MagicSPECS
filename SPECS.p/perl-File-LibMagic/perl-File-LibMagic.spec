# Filter the Perl extension module
%{?perl_default_filter}

%define module	File-LibMagic

Name:		perl-%{module}
Version:	0.96
Release:	6%{?dist}
Summary:	Perl wrapper/interface for libmagic
License:	GPL+ or Artistic
Group:		Development/Libraries
Source:		http://search.cpan.org/CPAN/authors/id/F/FI/FITZNER/%{module}-%{version}.tgz
URL:		http://search.cpan.org/dist/%{module}/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	%{_includedir}/magic.h, zlib-devel, perl(ExtUtils::MakeMaker), perl(Test::More)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The File::LibMagic is a simple perl interface to libmagic from the
file (4.x or 5.x) package.

%prep
%setup -q -n %{module}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name LibMagic.bs -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc Changes README
%{perl_vendorarch}/File/
%{perl_vendorarch}/auto/File/
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.96-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.96-5
- 为 Magic 3.0 重建

* Wed Nov 23 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.96-4
- Own vendor_perl/File dirs.
- Include Changes in docs.

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.96-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 04 2010 Robert Scheck <robert@fedoraproject.org> 0.96-1
- Upgrade to 0.96 and some spec file cleanup
- Replaced Test::Base by Test::More (thanks to Andreas Koenig)

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.91-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.91-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 22 2009 Robert Scheck <robert@fedoraproject.org> 0.91-1
- Upgrade to 0.91 and some spec file cleanup

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.88-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 28 2008 Josh Kayse <josh.kayse@gtri.gatech.edu> 0.88-0.f10
- update to 0.88

* Sat Mar 01 2008 Josh Kayse <josh.kayse@gtri.gatech.edu> 0.85-3
- add perl Require
- specify specific directories in files

* Fri Feb 29 2008 Josh Kayse <josh.kayse@gtri.gatech.edu> 0.85-2
- added patch to fix test cases

* Thu Feb 28 2008 Josh Kayse <josh.kayse@gtri.gatech.edu> 0.85-1
- update to 0.85

* Mon Oct 10 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.82-5mdk
- Fix previous mistake

* Fri Sep 30 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.82-4mdk
 - buildrequires fix

* Thu Sep 29 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.82-3mdk
- fix url
- fix buildrequires

* Sun Jun 19 2005 Olivier Thauvin <nanardon@mandriva.org> 0.82-2mdk
- patch0: add search ldflags
- BuildRequires libmagic-devel

* Wed Jun 15 2005 Olivier Thauvin <nanardon@mandriva.org> 0.82-1mdk
- First mandriva spec
