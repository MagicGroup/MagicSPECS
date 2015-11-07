Name:           perl-Template-Toolkit
Version:	2.26
Release:	2%{?dist}
Summary:        Template processing system
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://www.template-toolkit.org/
Source0:        http://search.cpan.org/CPAN/authors/id/A/AB/ABW/Template-Toolkit-%{version}.tar.gz
Source1:        http://tt2.org/download/TT_v224_html_docs.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(AppConfig)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(lib)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(CGI)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
# Prefer Image::Info over Image::Size
BuildRequires:  perl(Image::Info)
BuildRequires:  perl(Pod::POM)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Text::Wrap)
# Tests:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(AppConfig)
Requires:       perl(Encode)
Requires:       perl(File::Temp)
# Prefer Image::Info over Image::Size
Requires:       perl(Image::Info)
Provides:       perl-Template-Toolkit-examples = %{version}-%{release}
Obsoletes:      perl-Template-Toolkit-examples < 2.22-1

%{?filter_setup:
%filter_from_provides /^perl(bytes)$/d
%?perl_default_filter
}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(bytes\\)

%description
The Template Toolkit is a collection of modules which implement a
fast, flexible, powerful and extensible template processing system.
It was originally designed and remains primarily useful for generating
dynamic web content, but it can be used equally well for processing
any other kind of text based documents: HTML, XML, POD, PostScript,
LaTeX, and so on.

%prep
%setup -q -n Template-Toolkit-%{version} -a 1
find lib -type f | xargs chmod -c -x
find TT_v*_html_docs -depth -name .svn -type d -exec rm -rf {} \;
find TT_v*_html_docs -type f -exec chmod -x {} +;

# Convert file to UTF-8
iconv -f iso-8859-1 -t utf-8 -o Changes{.utf8,}
mv Changes{.utf8,}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor \
  TT_DBI=n TT_ACCEPT=y
make %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
# install (+ INSTALLARCHLIB) instead of pure_install to get docs
# and the template library installed too
make install \
  PERL_INSTALL_ROOT=$RPM_BUILD_ROOT \
  INSTALLARCHLIB=$RPM_BUILD_ROOT%{perl_archlib} \
  TT_PREFIX=$RPM_BUILD_ROOT%{_datadir}/tt2
find $RPM_BUILD_ROOT -type f \( -name perllocal.pod -o \
  -name .packlist -o -name '*.bs' -size 0 \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -empty -exec rmdir -f {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*
# Nuke buildroot where it hides
sed -i "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{perl_vendorarch}/Template/Config.pm

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes HACKING README TODO TT_v*_html_docs/*
%{_bindir}/tpage
%{_bindir}/ttree
%{perl_vendorarch}/Template.pm
%{perl_vendorarch}/auto/Template
%{perl_vendorarch}/Template
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.26-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.26-1
- 更新到 2.26

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.24-3
- 为 Magic 3.0 重建

* Fri Nov 09 2012 Petr Pisar <ppisar@redhat.com> - 2.24-2
- Remove executable bit from documentation

* Thu Aug 23 2012 Tom Callaway <spot@fedoraproject.org> - 2.24-1
- update to 2.24

* Tue Aug 21 2012 Petr Pisar <ppisar@redhat.com> - 2.22-14
- Correct dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 2.22-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Iain Arnell <iarnell@gmail.com> 2.22-10
- update filtering for rpm 4.9

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.22-9
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.22-7
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.22-6
- Mass rebuild with perl-5.12.0

* Tue Feb  9 2010 Stepan Kasal <skasal@redhat.com> - 2.22-5
- delete the buildroot before install

* Fri Jan 15 2010 Stepan Kasal <skasal@redhat.com> - 2.22-4
- use filtering macros

* Fri Jan 15 2010 Stepan Kasal <skasal@redhat.com> - 2.22-3
- drop build requirements for TeX; LaTeX support has been removed in 2.14a
- fix the Obsoletes tag

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.22-2
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22-1
- update to 2.22
- obsolete examples package, upstream got rid of them

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.20-1
- update to 2.20

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.19-4
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.19-3
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.19-2
- rebuild for new perl

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.19-1
- 2.19
- license tag fix
- rebuild for BuildID

* Wed Feb 21 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.18-1
- go to 2.18

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.15-2
- bump for fc6

* Mon May 29 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.15-1
- bump to 2.15
- gd test is gone, don't need to patch anything

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-8
- really resolve bug 173756

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-7
- use proper TT_PREFIX setting everywhere, resolve bug 173756

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-6
- bump for FC-5

* Mon Jul 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-5
- don't need Tie::DBI as a BuildRequires, since we're not running 
  the tests

* Mon Jul 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-4
- put examples in their own subpackage

* Sat Jul  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.14-3
- Filter false positive provides.
- Include template library, switch to %%{_datadir}/tt2.
- Tune build dependencies for full test suite coverage.
- Fix and enable GD tests.
- Include more documentation.
- Fine tune dir ownerships and file permissions.

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.14-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.14-1
- Initial package for Fedora Extras
