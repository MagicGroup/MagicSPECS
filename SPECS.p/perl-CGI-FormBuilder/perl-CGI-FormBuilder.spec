Name:           perl-CGI-FormBuilder
Version:        3.0501
Release:        16%{?dist}
Summary:        Easily generate and process stateful forms

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/CGI-FormBuilder/
Source0:        http://search.cpan.org/CPAN/authors/id/N/NW/NWIGER/CGI-FormBuilder-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTML::Template)
BuildRequires:  perl(Text::Template)
BuildRequires:  perl(Template)
BuildRequires:  perl(CGI::Session)
BuildRequires:  perl(CGI::FastTemplate)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The goal of CGI::FormBuilder (FormBuilder) is to provide an easy way
for you to generate and process entire CGI form-based
applications.

%prep
%setup -q -n CGI-FormBuilder-%{version}
find . -name \*.orig -delete
sed -i -e '/\.orig$/d' MANIFEST

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 3.0501-16
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 3.0501-15
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0501-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 3.0501-13
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 3.0501-12
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0501-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.0501-10
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.0501-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.0501-8
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0501-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0501-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callway <tcallawa@redhat.com> - 3.0501-5
- rebuild for new perl

* Wed Jun 20 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 3.0501-4
- Trim the description to something reasonable.
- Delete odd .orig file

* Fri Jun 15 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 3.0501-3
- BR perl(CGI::FastTemplate)

* Fri Jun 15 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 3.0501-2
- Don't BR perl or perl-devel, instead BR specific Perl modules needed to build.
- Proper license tag

* Fri Jun  1 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 3.0501-1
- First version for Fedora

