Name:           perl-XML-Handler-YAWriter
Version:        0.23
Release:        19%{?dist}

Summary:        Yet another Perl SAX XML Writer

Group:          Development/Libraries
License:        GPL+
URL:            http://search.cpan.org/dist/XML-Handler-YAWriter/
Source0:        http://search.cpan.org/CPAN/authors/id/K/KR/KRAEHE/XML-Handler-YAWriter-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(XML::Parser::PerlSAX)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
YAWriter implements Yet Another XML::Handler::Writer.


%prep
%setup -q -n XML-Handler-YAWriter-%{version}
for i in YAWriter.pm README; do {
  iconv -f iso8859-1 -t utf-8 $i > $i.conv && mv -f $i.conv $i;
};
done;


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
%doc Changes README
%{_bindir}/xmlpretty
%{perl_vendorlib}/*
%{_mandir}/man1/xmlpretty.1.gz
%{_mandir}/man3/XML::Handler::YAWriter.3pm.gz


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.23-19
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.23-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.23-17
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.23-16
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 Petr Pisar <ppisar@redhat.com> - 0.23-14
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.23-12
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-10
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.23-8
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.23-5
Rebuild for new perl

* Sat Jan 12 2008 Xavier Bachelot <xavier@bachelot.org> - 0.23-4
- Remove '|| :' from %%check section.

* Thu Dec 27 2007 Xavier Bachelot <xavier@bachelot.org> - 0.23-3
- Fix License:.

* Sat Dec 22 2007 Xavier Bachelot <xavier@bachelot.org> - 0.23-2
- Clean up spec.

* Tue May 23 2006 Xavier Bachelot <xavier@bachelot.org> - 0.23-1
- Initial build.
