Name:           perl-HTML-PrettyPrinter
Version:        0.03
Release:        15%{?dist}

Summary:        Generate nice HTML files from HTML syntax trees

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/HTML-PrettyPrinter/
Source0:        http://search.cpan.org/CPAN/authors/id/C/CL/CLMS/HTML-PrettyPrinter-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(HTML::Element)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
HTML::PrettyPrinter produces nicely formatted HTML code from a HTML syntax
tree. It is especially useful if the produced HTML file shall be read or
edited manually afterwards. Various parameters let you adapt the output to
different styles and requirements.


%prep
%setup -q -n HTML-PrettyPrinter-%{version}
iconv -f iso8859-1 -t utf-8 PrettyPrinter.pm > PrettyPrinter.pm.conv \
&& mv -f PrettyPrinter.pm.conv PrettyPrinter.pm 


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
%{perl_vendorlib}/*
%{_mandir}/man3/*3pm.gz


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.03-15
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.03-14
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.03-13
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.03-11
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-9
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.03-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.03-4
- rebuild for new perl

* Sat Jan 12 2008 Xavier Bachelot <xavier@bachelot.org> - 0.03-3
- Fix URL:.

* Wed Jan 09 2008 Xavier Bachelot <xavier@bachelot.org> - 0.03-2
- Remove set -x and set +x from %%prep section.
- Remove '|| :' from %%check section.

* Fri Dec 21 2007 Xavier Bachelot <xavier@bachelot.org> - 0.03-1
- Initial build.
