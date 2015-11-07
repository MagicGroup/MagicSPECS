Name:           perl-XML-DOM
Version:	1.45
Release:	2%{?dist}
Summary:        DOM extension to XML::Parser

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/XML-DOM/
Source0:        http://www.cpan.org/authors/id/T/TJ/TJMATHER/XML-DOM-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(XML::Parser) >= 2.30
BuildRequires:  perl(XML::Parser::PerlSAX) >= 0.07
BuildRequires:  perl(XML::RegExp)
BuildRequires:  perl(Test)
Requires:       perl(XML::Parser) >= 2.30
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Obsoletes:      perl-libxml-enno <= 1.02

%description
This is a Perl extension to XML::Parser. It adds a new 'Style' to
XML::Parser, called 'Dom', that allows XML::Parser to build an Object
Oriented datastructure with a DOM Level 1 compliant interface.  For a
description of the DOM (Document Object Model), see
http://www.w3.org/DOM/


%prep
%setup -q -n XML-DOM-%{version}

cat <<EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} \$* | grep -v 'perl(XML::XQL::Node)'
EOF
%define __perl_provides %{_builddir}/XML-DOM-%{version}/%{name}-prov
chmod +x %{__perl_provides}


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
%doc BUGS Changes README
%{perl_vendorlib}/XML/
%{_mandir}/man3/XML::*.3*


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.45-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.45-1
- 更新到 1.45

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.44-18
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.44-17
- 为 Magic 3.0 重建

* Thu Aug 16 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.44-16
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 1.44-14
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.44-12
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.44-11
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.44-9
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.44-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.44-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.44-4
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.44-3
- rebuild for new perl

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.44-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Jun 29 2006 Orion Poplawski <orion@cora.nwra.com> - 1.44-2
- Bump for new perl version (#196667)

* Sat Nov  5 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.44-1
- First Fedora Extras release (#172331).

* Thu Oct 27 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.44-0.1
- First build (#128879).
