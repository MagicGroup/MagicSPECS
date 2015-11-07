Name:           perl-POE-Filter-Transparent-SMTP
Version:        0.2
Release:        18%{?dist}
Summary:        A POE filter for SMTP

# note license definition in Makefile.PL
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/POE-Filter-Transparent-SMTP/
Source0:        http://search.cpan.org/CPAN/authors/id/U/UL/ULTRADM/POE-Filter-Transparent-SMTP-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(POE)
BuildRequires:  perl(Test::Pod), perl(Test::Pod::Coverage)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
POE data filter which aims to make SMTP data transparent 
just before going onto the wire as per RFC 821 Section 4.5.2.

%prep
%setup -q -n POE-Filter-Transparent-SMTP-%{version}
chmod -x LICENSE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.2-18
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.2-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.2-16
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.2-15
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.2-13
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.2-11
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.2-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.2-8
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.2-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.2-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Yanko Kaneti <yaneti@declera.com> - 0.2-4
- Must own everything under %%{perl_vendorlib}

* Wed Jun  1 2009 Yanko Kaneti <yaneti@declera.com> - 0.2-3
- Don't own %%{perl_vendorlib}/POE + Filter
- Initial import

* Thu Apr 16 2009 Yanko Kaneti <yaneti@declera.com> - 0.2-2
- fix LICENSE permissions

* Wed Apr 15 2009 Yanko Kaneti <yaneti@declera.com> - 0.2-1
- First attempt on packaging. Based on perl-POE-Filter-Zlib
