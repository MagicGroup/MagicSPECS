Name:           perl-Email-MIME-Attachment-Stripper
Version:        1.316
Release:        11%{?dist}
Summary:        Strip the attachments from a mail message
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Email-MIME-Attachment-Stripper/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Email-MIME-Attachment-Stripper-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(ExtUtils::MakeMaker), perl(Email::MIME), perl(Email::MIME::ContentType)
BuildRequires:  perl(Email::MIME::Modifier), perl(Test::More), perl(Test::Pod), perl(Test::Pod::Coverage)
BuildArch:      noarch
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Given a Email::MIME object, detach all attachments from the message.
These are then available separately.

%prep
%setup -q -n Email-MIME-Attachment-Stripper-%{version}

%build
sed -i '/LICENSE/ d' Makefile.PL
%{__perl} Makefile.PL INSTALLDIRS=vendor
make

%install
rm -rf $RPM_BUILD_ROOT _docs
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README LICENSE
%{perl_vendorlib}/Email/
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.316-11
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.316-10
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.316-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.316-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.316-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.316-6
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.316-5
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.316-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.316-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.316-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.316-1
- update to 1.316

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.314-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.314-3
Rebuild for new perl

* Fri Nov 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.314-2
- add missing BR

* Wed Nov 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.314-1
- bump to 1.314

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.313-3
- fix license tag

* Mon Apr  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.313-2
- Remove LICENSE line from Makefile.PL

* Sun Apr  1 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.313-1
- Initial package for Fedora
