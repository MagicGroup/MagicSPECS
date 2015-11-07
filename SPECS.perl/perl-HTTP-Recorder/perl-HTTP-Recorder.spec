Name:           perl-HTTP-Recorder
Version:	0.07
Release:	3%{?dist}
Summary:        Record interaction with web sites

Group:          Development/Libraries
License:        GPL+
URL:            http://search.cpan.org/dist/HTTP-Recorder/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SE/SEMUELF/HTTP-Recorder-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(HTML::TokeParser)
BuildRequires:  perl(HTTP::Request::Params)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(Test::Pod)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Browser-independent recorder for recording interactions with web sites.


%prep
%setup -q -n HTTP-Recorder-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES README
%{perl_vendorlib}/HTTP/
%{_mandir}/man3/*.3pm*
%{_bindir}/httprecorder
%{_mandir}/man1/httprecorder.1*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.07-3
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.07-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.07-1
- 更新到 0.07

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.05-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.05-13
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.05-12
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.05-11
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.05-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.05-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.05-2
Rebuild for new perl

* Thu Sep  8 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.05-1
- Update to 0.05.

* Sun Jul 04 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.02-0.fdr.1
- First build.
