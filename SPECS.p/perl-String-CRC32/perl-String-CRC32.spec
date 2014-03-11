Name:           perl-String-CRC32
Version:        1.4
Release:        13%{?dist}
Summary:        Perl interface for cyclic redundancy check generation
Group:          Development/Libraries
License:        Public Domain
URL:            http://search.cpan.org/dist/String-CRC32/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SO/SOENKE/String-CRC32-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This packages provides a perl module to generate checksums from strings and
from files.

The checksums are the same as those calculated by ZMODEM, PKZIP, PICCHECK and
many others.

There's another perl module called String::CRC, which supports calculation of
CRC values of various widths (i.e. not just 32 bits), but the generated sums
differ from those of the programs mentioned above.

%prep
%setup -q -n String-CRC32-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README
%{perl_vendorarch}/String/
%{perl_vendorarch}/auto/String/
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.4-13
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.4-11
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.4-10
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.4-9
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4-6
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4-5
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4-4
- rebuild for new perl

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 1.4-3
- fix typo in %%summary and tidy up %%description
- remove redundant dependency on perl >= 1:5.6.1
- fix argument order for find with -depth
- drop "|| :" from %%check (only required for ancient rpmbuild versions)
- add buildreq perl(ExtUtils::MakeMaker)

* Wed Aug 02 2006 Warren Togami <wtogami@redhat.com> 1.4-2
- bump

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 
- rebuild

* Wed May 31 2006 Jason Vas Dias <jvdias@redhat.com> - 1.4-1.FC6
- upgrade to upstream version 1.4

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3-3.FC5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3-3.FC5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0:1.03-3.FC5
- rebuild for new perl-5.8.8

* Thu Jan 19 2006 Jason Vas Dias <jvdias@redhat.com> - 0:1.03-2.FC5
- bug 176175 addendum: license should be 'Public Domain'

* Fri Jan 13 2006 Jason Vas Dias <jvdias@redhat.com> - 0.1.03-1.4.FC5
- fix bug 177700: differentiate version from FE4, FE dev versions

* Fri Dec 16 2005 Jason Vas Dias <jvdias@redhat.com> - 0:1.03-1
- Initial build.
- Required by lftp-3.3.x+ 
- Imported to fix bug 176175
