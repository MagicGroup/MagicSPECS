Name:       perl-Jemplate 
Version:    0.261
Release:    14%{?dist}
# lib/Jemplate.pm -> GPL+ or Artistic
# lib/Jemplate/Directive.pm -> GPL+ or Artistic
# lib/Jemplate/Parser.pm -> GPL+ or Artistic
# lib/Jemplate/Runtime.pm -> GPL+ or Artistic
# lib/Jemplate/Runtime/Compact.pm -> GPL+ or Artistic
License:    GPL+ or Artistic 
Group:      Development/Libraries
Summary:    JavaScript Templating with Template Toolkit 
Source:     http://search.cpan.org/CPAN/authors/id/R/RK/RKRIMEN/Jemplate-%{version}.tar.gz 
#Patch0:     Jemplate.pm-0.23_1.patch 
#Patch0:     Jemplate-0.261-fix-quoted-test.patch
# http://rt.cpan.org/Public/Bug/Display.html?id=48564
# Fix test to work with newer Template::Toolkit Behavior
Patch1:     Jemplate-0.261-fix-quoted-test.patch
Url:        http://search.cpan.org/dist/Jemplate
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires: perl(File::Find::Rule) >= 0.30
BuildRequires: perl(Template) >= 2.22

# tests
BuildRequires: perl(Test::Base)
BuildRequires: perl(Test::Base::Filter)
BuildRequires: perl(Getopt::Long)
BuildRequires: perl(HTTP::Daemon)
BuildRequires: perl(HTTP::Status)
BuildRequires: perl(HTTP::Response)
BuildRequires: perl(IO::All)
BuildRequires: perl(LWP::MediaTypes)
BuildRequires: perl(Path::Class)
BuildRequires: perl(JSON)

%description
Jemplate is a templating framework for JavaScript that is built over
Perl's Template Toolkit (TT2). Jemplate parses TT2 templates using the
TT2 Perl framework, but with a twist. Instead of compiling the templates
into Perl code, it compiles them into JavaScript. Jemplate then provides
a JavaScript runtime module for processing the template code. Presto, we
have full featured JavaScript templating language!



%prep
%setup -q -n Jemplate-%{version}
#%patch0 -p1
%patch1 -p1

cat doc/text/Jemplate.text | iconv -f iso-8859-1 -t utf-8 > foo
cat foo > doc/text/Jemplate.text
rm foo

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README doc/ examples/ 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*
%{_bindir}/jemplate
%{_mandir}/man1/jemplate.1.gz

%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.261-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.261-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.261-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.261-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.261-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.261-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.261-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.261-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.261-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.261-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.261-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.261-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.261-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Aug  6 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.261-1
- update

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-6
- Mass rebuild with perl-5.12.0

* Fri Jan 15 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.23-5
- fix quoted test to work with newer Template::Toolkit behavior

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.23-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 28 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.23-2
- apply a partial patch to Jemplate.pm from 0.23_01, to resolve issues with
  this release and Catalyst::View::Jemplate

* Tue Mar 24 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.23-1
- touch-up

* Tue Mar 24 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.23-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)

