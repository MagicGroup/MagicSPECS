Name:           perl-IO-CaptureOutput
Version:	1.1104
Release:	1%{?dist}
Summary:        Capture STDOUT/STDERR from sub-processes and XS/C modules
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/IO-CaptureOutput
Source0:        http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/IO-CaptureOutput-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Temp) >= 0.16
# Tests:
BuildRequires:  perl(File::Spec) >= 3.27
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Test::More) >= 0.62
# Optional test:
BuildRequires:  perl(Inline::C)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
%{summary}.

%prep
%setup -q -n IO-CaptureOutput-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{_smp_mflags}

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
%{perl_vendorlib}/IO
%{_mandir}/man3/*.3*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.1104-1
- 更新到 1.1104

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.1102-10
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.1102-9
- 为 Magic 3.0 重建

* Tue Oct 16 2012 Petr Pisar <ppisar@redhat.com> - 1.1102-8
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1102-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 1.1102-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1102-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.1102-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1102-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.1102-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jul 12 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1102-1
- update to 1.1102

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.1101-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.1101-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1101-1
- update to 1.1101

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.10-1
- update to 1.10

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.06-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.06-1
- bump to 1.06

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.03-6
- license fix

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.03-5
- bump for fc6

* Wed Aug 17 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.03-4
- add BR (Test::Pod)

* Wed Aug 17 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.03-3
- more cleanups
- add BR so testing passes

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.03-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.03-1
- Initial package for Fedora Extras
