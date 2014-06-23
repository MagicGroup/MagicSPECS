Name:           perl-Net-IP
Version:        1.25
Release:        22%{?dist}
Summary:        Perl module for manipulation of IPv4 and IPv6 addresses

Group:          Development/Libraries
# Some ambiguity here, see http://rt.cpan.org/Ticket/Display.html?id=28689
# MIT-like for the IP.pm itself, and "like Perl itself" for all the other
# scripts included.
License:        MIT and (GPL+ or Artistic)
URL:            http://search.cpan.org/dist/Net-IP/
Source:         http://www.cpan.org/authors/id/M/MA/MANU/Net-IP-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Patch0:         perl-Net-IP-1.25-bz197425.patch

%description
This is the Net::IP module for Perl, designed to allow easy
manipulation of IPv4 and IPv6 addresses.  Two applications using the
Net::IP module are included: ipcount, an IP address mini-calculator,
it can calculate the number of IP addresses in a prefix or all the
prefixes contained in a given range; and iptab, which prints out a
handy IP "cheat sheet".


%prep
%setup -q -n Net-IP-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -empty -exec rmdir {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
# These tests fail on ppc builders because of:
# http://rt.perl.org/rt3//Public/Bug/Display.html?id=50114
# Re-enable this when the upstream bug is resolved.
# 


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING Changes README
%{_bindir}/ipcount
%{_bindir}/iptab
%{perl_vendorlib}/Net/
%{_mandir}/man3/Net::IP.3*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.25-22
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.25-21
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.25-19
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.25-17
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.25-15
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.25-14
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 1.25-13
- fix the source URL

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 1.25-12
- fix license tag

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.25-11
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.25-8
- Rebuild for perl 5.10 (again)

* Fri Feb  1 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.25-7
- disable tests due to upstream bug 50114

* Fri Feb  1 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.25-6
- Work around http://rt.perl.org/rt3//Public/Bug/Display.html?id=50114

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.25-5
- rebuild for new perl

* Sun Aug 12 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.25-4
- BuildRequire perl(ExtUtils::MakeMaker)
- License: MIT

* Sun Feb 04 2007 Robin Norwood <rnorwood@redhat.com> - 1.25-3
- Resolves: bz#226271
- Incorporate some fixes to the spec file from Ville:

* Wed Jul 05 2006 Jason Vas Dias <jvdias@redhat.com> - 1.25-2
- fix bug 197925 - make intip handle zero-valued IP addresses

* Mon Jun 05 2006 Jason Vas Dias <jvdias@redhat.com> - 1.25-1
- upgrade to 1.25

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.24-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Mon Oct 31 2005 Warren Togami <wtogami@redhat.com> - 1.24-2
- import into FC5 because perl-Net-DNS needs it

* Wed Oct 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.24-1
- 1.24.

* Mon Jun  6 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.23-3
- 1.23, patches applied upstream.
- Improve description.

* Sun May 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.22-2
- 1.22, include test case for rt.cpan.org #7528 patch.
- Patch to mute stdout noise from ip_reverse().

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.21-2
- rebuilt

* Thu Dec  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.21-1
- Update to 1.21.

* Sat Nov  6 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20-0.fdr.7
- Apply fixes from rt.cpan.org #3844 and #7528.
- Some specfile cleanups.

* Sun May  9 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20-0.fdr.6
- BuildRequire perl >= 1:5.6.1-34.99.6 for support for vendor installdirs.
- Use pure_install to avoid perllocal.pod workarounds.

* Sun Apr 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20-0.fdr.5
- Require perl(:MODULE_COMPAT_*).

* Mon Feb  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20-0.fdr.4
- Reduce directory ownership bloat.

* Mon Dec  1 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20-0.fdr.3
- Specfile cleanup.

* Sun Aug 31 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20-0.fdr.2
- Install into vendor dirs.

* Wed Jul 16 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20-0.fdr.1
- First build.
