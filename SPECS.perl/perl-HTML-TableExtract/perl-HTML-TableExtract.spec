Name:           perl-HTML-TableExtract
Version:        2.10
Release: 	15%{?dist}
Summary:        A Perl module for extracting content in HTML tables
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:		http://www.mojotoad.com/sisk/projects/HTML-TableExtract/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MS/MSISK/HTML-TableExtract-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:	perl(HTML::TreeBuilder) perl(Test::Pod) perl(Test::Pod::Coverage)

%description
HTML::TableExtract is a module that simplifies the extraction of
information contained in tables within HTML documents.

Tables of note may be specified using Headers, Depth, Count,
Attributes, or some combination of the three. See the module
documentation for details.

%prep
%setup -q -n HTML-TableExtract-%{version} 

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
%{perl_vendorlib}/HTML/
%{_mandir}/man3/*.3*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.10-15
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.10-14
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 2.10-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.10-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.10-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.10-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.10-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10-3
- rebuild for new perl

* Fri Aug  3 2007 Bill Nottingham <notting@redhat.com>
- clarify license tag

* Wed Jun 20 2007 Bill Nottingham <notting@redhat.com> - 2.10-2
- EPEL build tweaks

* Mon Jan  8 2007 Bill Nottingham <notting@redhat.com> - 2.10-1
- update to 2.10

* Thu Sep 14 2006 Bill Nottingham <notting@redhat.com> - 2.07-3
- bump for rebuild

* Mon Apr 10 2006 Bill Nottingham <notting@redhat.com> - 2.07-2
- add some buildprereqs for testing

* Fri Apr  7 2006 Bill Nottingham <notting@redhat.com> - 2.07-1
- initial packaging

