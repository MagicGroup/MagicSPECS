Name:           perl-Text-Shellwords
Version:        1.08
Release:        16%{?dist}
Summary:        A thin wrapper around the shellwords.pl package

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Text-Shellwords/
Source0:        http://www.cpan.org/authors/id/L/LD/LDS/Text-Shellwords-1.08.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This is a thin wrapper around the shellwords.pl package, which comes
preinstalled with Perl.  This module imports a single subroutine,
shellwords().  The shellwords() routine parses lines of text and
returns a set of tokens using the same rules that the Unix shell does
for its command-line arguments.  Tokens are separated by whitespace,
and can be delimited by single or double quotes.  The module also
respects backslash escapes.


%prep
%setup -q -n Text-Shellwords-%{version}
# Clean up /usr/local/bin/perl mess
#%{__perl} -pi -e 's|/usr/local/bin/perl\b|%{__perl}|' \
#  qd.pl bdf_scripts/cvtbdf.pl demos/{*.{pl,cgi},truetype_test}

# avoid dependencies
#chmod 644 examples/* 


%build 
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} 


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -a \( -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.08-16
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.08-14
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.08-12
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.08-10
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.08-9
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.08-8
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jun  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.08-5
- Remove old check construct that prevents F-10+ build (#449489)

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.08-4
- rebuild for new perl

* Mon Oct 15 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.08-3
- Add missing BR: perl(ExtUtils::MakeMaker)

* Tue Sep 04 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.08-2
- Clarified license terms: GPL+ or Artistic

* Wed Mar 23 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.08-1
- Updated to 1.08
- Removed superfluous BR: Perl as per suggestion from Ralf Corsepius

* Wed Apr 06 2005 Hunter Matthews <thm@duke.edu> 1.07-2
- Review suggestions by José Pedro Oliveira

* Tue Mar 22 2005 Hunter Matthews <thm@duke.edu> 1.07-1
- Initial build.
