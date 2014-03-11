Name:       perl-File-RsyncP
Version:    0.70
Release:    6%{?dist}
Summary:    A perl implementation of an Rsync client
License:    GPLv2
Group:      Development/Libraries
URL:        http://search.cpan.org/dist/File-RsyncP/
Source0:    http://search.cpan.org/CPAN/authors/id/C/CB/CBARRATT/File-RsyncP-%{version}.tar.gz

Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires: %{_bindir}/iconv
BuildRequires: perl(ExtUtils::MakeMaker)

%description
File::RsyncP is a perl implementation of an Rsync client. It is compatible with
Rsync 2.5.5 - 2.6.3 (protocol versions 26-28). It can send or receive files,
either by running rsync on the remote machine, or connecting to an rsyncd
daemon on the remote machine.

%prep
%setup -q -n File-RsyncP-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_flags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorarch}/File/
%{perl_vendorarch}/auto/File/
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.70-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.70-5
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.70-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.70-3
- Own vendor_perl/File dirs.

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.70-2
- Perl mass rebuild

* Tue Apr 05 2011 Petr Sabata <psabata@redhat.com> - 0.70-1
- 0.70 bump
- Utilizing parallel make
- Removing obsolete Buildroot stuff

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.68-9
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.68-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.68-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.68-4
Rebuild for new perl

* Tue Feb 12 2008 Mike McGrath <mmcgrath@redhat.com> - 0.68-3
- Rebuild for gcc43

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.68-2.1
- add BR: perl(ExtUtils::MakeMaker)

* Wed Aug 22 2007 Mike McGrath <mmcgrath@redhat.com> - 0.68-2
- Rebuild for BuildID
- License change

* Mon Jun 04 2007 Mike McGrath <mmcgrath@redhat.com> - 0.68-1
- Upstream released new version

* Sun Sep 10 2006 Mike McGrath <imlinux@gmail.com> - 0.62-2
- Rebuild

* Fri Jul 21 2006 Mike McGrath <imlinux@gmail.com> - 0.62-2
- Fixed whitespace issue and removed SMP flags on make

* Thu Jul 20 2006 Mike McGrath <imlinux@gmail.com> - 0.62-1
- Updated to 0.62 and applied two known patches

* Thu Jul 20 2006 Mike McGrath <imlinux@gmail.com> - 0.52-1
- Initial Fedora Packaging
