Name:           perl-Digest-CRC
Version:	0.21
Release:	1%{?dist}
Summary:        Generic CRC functions
Group:          Development/Libraries
License:        Public Domain
URL:            http://search.cpan.org/dist/Digest-CRC
Source0:        http://search.cpan.org/CPAN/authors/id/O/OL/OLIMAUL/Digest-CRC-%{version}.tar.gz
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(DynaLoader)
Requires:       perl(DynaLoader)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The Digest::CRC module calculates CRC sums of all sorts. It contains wrapper
functions with the correct parameters for CRC-CCITT, CRC-16 and CRC-32.

%prep
%setup -qn Digest-CRC-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;

%check


%files
%doc Changes META.yml README t
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Digest
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.21-1
- 更新到 0.21

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.18-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.18-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.18-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.18-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Petr Šabata <contyk@redhat.com> - 0.18-1
- 0.18 bump

* Mon Aug 29 2011 Petr Sabata <contyk@redhat.com> - 0.17-1
- 0.17 bump
- Removing now obsolete defattr

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.16-2
- Perl mass rebuild

* Tue Apr 26 2011 Petr Sabata <psabata@redhat.com> - 0.16-1
- 0.16 bump
- Buildroot removed, general cleanup
- Fixing [B]Requires...

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-6
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.14-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 22 2008 Christopher Stone <chris.stone@gmail.com> 0.14-1
- Upstream sync

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-4
- Rebuild for new perl

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> 0.10-3
- Autorebuild for GCC 4.3

* Tue Oct 16 2007 Christopher Stone <chris.stone@gmail.com> 0.10-2
- Remove zero length files.

* Tue Oct 16 2007 Christopher Stone <chris.stone@gmail.com> 0.10-1
- Initial Release.
