Name:           perl-POE-Component-Client-SMTP
Version:        0.22
Release:        14%{?dist}
Summary:        Asynchronous mail sending with POE

Group:          Development/Libraries
License:        GPL+ or Artistic        
URL:            http://search.cpan.org/dist/POE-Component-Client-SMTP/
Source0:        http://search.cpan.org/CPAN/authors/id/U/UL/ULTRADM/POE-Component-Client-SMTP-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(POE) >= 0.31
BuildRequires:  perl(POE::Filter::Transparent::SMTP)

# tests...
BuildRequires:  perl(Test::Pod), perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::More)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
POE::Component::Client::SMTP allows you to send email messages 
in an asynchronous manner, using POE.


%prep
%setup -q -n POE-Component-Client-SMTP-%{version}
chmod -x LICENSE README Changes COPYING TODO eg/*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*


%check



%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README Changes COPYING TODO eg

%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.22-14
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.22-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.22-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.22-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.22-10
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.22-8
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.22-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-4
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.22-2
- rebuild against perl 5.10.1

* Wed Sep  2 2009 Yanko Kaneti <yaneti@declera.com> - 0.22-1
- New upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Yanko Kaneti <yaneti@declera.com> - 0.21-5
- Must own everyting under %%{perl_vendorlib}

* Sat Jun  6 2009 Yanko Kaneti <yaneti@declera.com> - 0.21-4
- Implement review feedback from Mamoru Tasaka
  https://bugzilla.redhat.com/show_bug.cgi?id=495885#c4
- Do not own %%{perl_vendorlib}/POE + Component + Client
- Drop explicit perl , sed BR
- Use perl instead of %%{__perl}

* Mon Apr 20 2009 Yanko Kaneti <yaneti@declera.com> 0.21-3
- Add eg/ to the installed documentation

* Sun Apr 19 2009 Yanko Kaneti <yaneti@declera.com> 0.21-2
- Remove executable bits from doc files

* Wed Apr 15 2009 Yanko Kaneti <yaneti@declera.com> 0.21-1
- First attempt at packaging. based on perl-POE-Component-Client-HTTP spec
