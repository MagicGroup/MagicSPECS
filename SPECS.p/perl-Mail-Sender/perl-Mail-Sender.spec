Name:           perl-Mail-Sender
Version:        0.8.16
Release:        12%{?dist}
Summary:        Module for sending mails with attachments through an SMTP server

Group:          Development/Libraries
# There is also a clause which says that it may not be used for SPAM.
# However, since spamming is illegal in the US, this isn't really a use restriction.
# Instead, its a friendly reminder of the law, so we won't list it here.
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Mail-Sender/
Source0:        http://www.cpan.org/authors/id/J/JE/JENDA/Mail-Sender-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker), perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
%{summary}.


%prep
%setup -q -n Mail-Sender-%{version}
%{__perl} -pi -e 's/\r\n/\n/' README


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} < /dev/null


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

# Remove the Win32 module in order to avoid requiring perl(Win32API::Registry)
find $RPM_BUILD_ROOT -type f -name Win32.pm -exec rm -f {} ';'
magic_rpm_clean.sh

%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
# License: perl + spam exception.
# See the main POD page for the copyright information.
# For the Artistic and GPL license text(s), see the perl package.
%doc Changes README
%{perl_vendorlib}/Mail/
%{_mandir}/man3/*.3pm*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.8.16-12
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.8.16-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.8.16-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8.16-6
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8.16-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.8.16-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.16-2
- missing BR on Test::More

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.16-1
- update to 0.8.16

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.13-3
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.13-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.13-2
- Update to 0.8.13.

* Wed Mar 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.13-1
- Update to 0.8.13.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.10-3
- Rebuild for FC5 (perl 5.8.8).

* Mon Sep 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.10-2
- License clarification.

* Sat Sep 10 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.10-1
- First build.
