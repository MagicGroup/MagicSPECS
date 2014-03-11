Name:           perl-Tk-ProgressBar-Mac
Version:        1.2
Release:        13%{?dist}
Summary:        Mac ProgressBar for Perl::Tk

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Tk-ProgressBar-Mac/
Source0:        http://cpan.org/modules/by-module/Tk/Tk-ProgressBar-Mac-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Tk)
BuildRequires:  perl(Tk::MMutil)
BuildRequires:  xorg-x11-server-Xvfb, xorg-x11-fonts-base
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This widget provides a dynamic image that looks just like
a Mac OS 9 progress bar.  Packed around it are four
Frames, north, south, east and west, within which you can
stuff additional widgets. For example, see how Tk::Copy::Mac
uses several Labels and a CollapsableFrame widget to create
a reasonable facsimile of a Macintosh copy dialog.


%prep
%setup -q -n Tk-ProgressBar-Mac-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check
# disabled by default because it needs an x screen
%{?_with_tests:}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README
%{perl_vendorlib}/Tk*
%{_mandir}/man3/Tk*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.2-13
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.2-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 13 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2-9
- Add BR: perl(Tk::MMutil).

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2-8
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.2-4
- rebuild against perl 5.10.1

* Mon Sep 14 2009 David Hannequin <david.hannequin@gmail.com> 1.2-3
- Fix license 

* Tue May 30 2009 David Hannequin <david.hannequin@gmail.com> 1.2-2
- delete _xvfb
- modify man page

* Thu May 21 2009 David Hannequin <david.hannequin@gmail.com> 1.2-1
- First release.

