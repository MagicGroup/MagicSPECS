Name:           perl-Net-IP-CMatch
Version:        0.02
Release:        21%{?dist}
Summary:        Efficiently match IP addresses against IP ranges with C

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Net-IP-CMatch/
Source0:        http://search.cpan.org/CPAN/authors/id/B/BE/BEAU/Net-IP-CMatch-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Net::IP::CMatch is based upon, and does the same thing as Net::IP::Match. The
unconditionally exported subroutine 'match_ip' determines if the IP to match
(first argument) matches any of the subsequent IP arguments. Match arguments
may be absolute quads, as '127.0.0.1', or contain mask bits as
'111.245.76.248/29'. A true return value indicates a match. It was written in
C, rather than a macro, preprocessed through perl's source filter mechanism
(as is Net::IP::Match), so that the IP arguments could be traditional perl
scalars. The C code is lean and mean (IMHO).

%prep
%setup -q -n Net-IP-CMatch-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorarch}/auto/Net/
%{perl_vendorarch}/Net/
%{_mandir}/man3/*.3*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.02-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.02-20
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.02-19
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 0.02-17
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.02-15
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-13
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-12
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.02-11
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.02-8
Rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.02-7
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 - Orion Poplawski <orion@cora.nwra.com> - 0.02-6
- Add BR perl(Test::More)

* Thu Aug 23 2007 - Orion Poplawski <orion@cora.nwra.com> - 0.02-5
- Update license tag to GPL+ or Artistic
- Rebuild for BuildID

* Tue Aug 29 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.02-4
- Rebuild for FC6

* Mon Feb 27 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.02-3
- Rebuild for FC5

* Tue Oct 18 2005 Paul Howarth <paul@city-fan.org> - 0.02-2
- Add Changes as %%doc
- Fix directory ownership
- Remove redundant BR: perl
- Simplify compiler optimization
- Tidy up %%description

* Mon Oct 3 2005 - Orion Poplawski <orion@cora.nwra.com> - 0.02-1
- Initial version
