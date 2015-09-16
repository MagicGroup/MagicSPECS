Name:           perl-Kwiki
Version:        0.39
Release:        27%{?dist}
Summary:        Kwiki Wiki Building Framework
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Kwiki/
Source0:        http://www.cpan.org/authors/id/I/IN/INGY/Kwiki-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::All)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Memory::Cycle)
BuildRequires:  perl(Spoon) >= 0.22

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# RPM 4.8 filters
%{?filter_setup:
%filter_from_requires /^perl(mixin)/d
%{?perl_default_filter}
}
# RPM 4.9 filters
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(mixin\\)$

%description
A Wiki is a website that allows its users to add pages, and edit any
existing pages. It is one of the most popular forms of web collaboration.
If you are new to wiki, visit http://c2.com/cgi/wiki?WelcomeVisitors
which is possibly the oldest wiki, and has lots of information about how
wikis work.

Kwiki is a Perl wiki implementation based on the Spoon application
architecture and using the Spiffy object orientation model. The major goals
of Kwiki are that it be easy to install, maintain and extend.

All the features of a Kwiki wiki come from plugin modules. The base
installation comes with the bare minimum plugins to make a working Kwiki.
To make a really nice Kwiki installation you need to install additional
plugins. Which plugins you pick is entirely up to you. Another goal of
Kwiki is that every installation will be unique. When there are hundreds of
plugins available, this will hopefully be the case.

%prep
%setup -q -n Kwiki-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.39-27
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.39-26
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.39-25
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.39-24
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.39-23
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.39-22
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.39-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.39-20
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.39-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.39-18
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.39-17
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.39-16
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 22 2011 Petr Sabata <contyk@redhat.com> - 0.39-14
- RPM 4.9 dependency filtering added
- BuildRequire IO::All

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.39-13
- Perl mass rebuild

* Wed Feb 16 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.39-12
- Revert temporary hack "BR: perl-IO-All" (Not required anymore).

* Tue Feb 15 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.39-11
- Switch to using perl-filters/Abandon filter-requires.sh
  (Work around broken deps caused by rpm dep-tracker changes).
- BR: perl-IO-All, to assure getting the right perl(IO::All)
  (was bogusly provided by perl-Spoon-0.24-9).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.39-9
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.39-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.39-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.39-3
- rebuild for new perl

* Fri Jan 04 2008 Ralf Corsépius <rc040203@freenet.de> 0.39-2
- Update License-tag.
- BR: perl(Test::Memory::Cycle).
- BR: perl(Test::More) (BZ 419631).

* Tue Mar 13 2007 Steven Pritchard <steve@kspei.com> 0.39-1
- Update to 0.39.
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Mon Sep 04 2006 Steven Pritchard <steve@kspei.com> 0.38-4
- Cleanup to more closely resemble current cpanspec output.
- kwiki is a program, not documentation.

* Fri Mar 10 2006 Steven Pritchard <steve@kspei.com> 0.38-3
- Improve Summary.
- Fix up dependency filtering.

* Mon Feb 27 2006 Steven Pritchard <steve@kspei.com> 0.38-2
- Drop explicit BR: perl.
- Filter perl(mixin) dependency.

* Wed Dec 28 2005 Steven Pritchard <steve@kspei.com> 0.38-1
- Specfile autogenerated.
