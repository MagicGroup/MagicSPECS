Name:       perl-Text-PDF
Version:    0.29a
Release:    21%{?dist}
# lib/Text/PDF.pm -> GPL+ or Artistic
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Module for manipulating PDF files
Source:     http://search.cpan.org/CPAN/authors/id/M/MH/MHOSKEN/Text-PDF-%{version}.tar.gz
Patch0:     Text-PDF-0.29-formats.patch
Url:        http://search.cpan.org/dist/Text-PDF
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(Compress::Zlib)
BuildRequires: perl(ExtUtils::MakeMaker)
Requires:      pdf-tools = %{version}-%{release}

%description
This module allows interaction with existing PDF files directly. It
includes various tools:

    pdfbklt   - make booklets out of existing PDF files
    pdfrevert - remove edits from a PDF file
    pdfstamp  - stamp text on each page of a PDF file

%package -n pdf-tools
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Manipulate PDF files
Requires:   %{name} = %{version}-%{release}

%description -n pdf-tools
This package allows existing PDF files to be modified; and includes various
tools:

    pdfbklt   - make booklets out of existing PDF files
    pdfrevert - remove edits from a PDF file
    pdfstamp  - stamp text on each page of a PDF file

%prep
# FIXME ugh.  This is the way upstream has it, tho
%setup -q -n Text-PDF-0.29
find . -type f -exec chmod -c -x     {} ';'
find . -type f -exec sed -i 's/\r//' {} ';'
%patch0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc readme.txt examples/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%files -n pdf-tools
%doc readme.txt
%{_bindir}/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.29a-21
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.29a-20
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.29a-19
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29a-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.29a-17
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.29a-16
- Perl 5.20 rebuild

* Wed Jun 18 2014 Petr Šabata <contyk@redhat.com> - 0.29a-15
- Support A0-A5 paper sizes (#1105775)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29a-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29a-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.29a-12
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29a-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29a-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.29a-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29a-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.29a-7
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29a-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.29a-5
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.29a-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.29a-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.29a-1
- submission
- add pdf-tools subpackage

* Mon Jun 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.29a-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)

