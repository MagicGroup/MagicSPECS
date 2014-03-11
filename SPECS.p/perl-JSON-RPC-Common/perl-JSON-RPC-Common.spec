Name:           perl-JSON-RPC-Common
Version:        0.06
Release:        10%{?dist}
Summary:        Perl module for handling JSON-RPC objects
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/JSON-RPC-Common
Source0:        http://www.cpan.org/authors/id/N/NU/NUFFIN/JSON-RPC-Common-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  perl(JSON)
BuildRequires:  perl(MooseX::Types)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::use::ok)
BuildRequires:  perl(URI)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module provides abstractions for JSON-RPC 1.0, 1.1 (both variations) and
2.0 (formerly 1.2) Procedure Call and Procedure Return objects (formerly known
as request and result), along with error objects.
It also provides marshalling objects to convert the model objects into JSON
text and HTTP requests/responses.

%prep
%setup -q -n JSON-RPC-Common-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorlib}/JSON/RPC/
%{_mandir}/man3/*.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.06-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.06-9
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.06-7
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.06-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-4
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-3
- Mass rebuild with perl-5.12.0

* Thu Mar 25 2010 Christian Krause <chkr@fedoraproject.org> - 0.06-2
- Add missing BR for ""

* Wed Mar 24 2010 Christian Krause <chkr@fedoraproject.org> - 0.06-1
- Update to new upstream version 0.06

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.03-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 01 2009 Christian Krause <chkr@fedoraproject.org> - 0.03-3
- fixed rpmlint warnings

* Thu Apr 30 2009 Christian Krause <chkr@fedoraproject.org> - 0.03-2
- fixed description
- added Changes file as %%doc
- removed unneeded build requirements
- package owns now %%{perl_vendorlib}/JSON/RPC/

* Wed Apr 29 2009 Christian Krause <chkr@fedoraproject.org> - 0.03-1
- Initial spec file for JSON-RPC-Common
