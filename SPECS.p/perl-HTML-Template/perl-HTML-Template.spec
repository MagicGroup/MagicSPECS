Name:           perl-HTML-Template
Version:        2.10
Release:        9%{?dist}
Summary:        Perl module to use HTML Templates

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/HTML-Template/
Source0:        http://www.cpan.org/authors/id/W/WO/WONKO/HTML-Template-%{version}.tar.gz
Patch0:         perl-HTML-Template-manpages.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=734253
Patch1:         perl-HTML-Template-2.10-versioning.patch
%global         __provides_exclude ^perl\\(HTML::Template\\)\\s*=\\s*2\\.91$
Provides:       perl(HTML::Template) = %{version}

BuildArch:      noarch
BuildRequires:  perl(CGI)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IPC::SharedCache)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module attempts make using HTML templates simple and natural.  It
extends standard HTML with a few new HTML-esque tags - <TMPL_VAR>,
<TMPL_LOOP>, <TMPL_INCLUDE>, <TMPL_IF> and <TMPL_ELSE>.  The file
written with HTML and these new tags is called a template.  It is
usually saved separate from your script - possibly even created by
someone else!  Using this module you fill in the values for the
variables, loops and branches declared in the template.  This allows
you to separate design - the HTML - from the data, which you generate
in the Perl script.


%prep
%setup -q -n HTML-Template-%{version}
%patch0 -p1 -b .manpages
%patch1 -p1 -b .versioning


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
TEST_SHARED_MEMORY=1 


%files
%doc Changes LICENSE README
%{perl_vendorlib}/HTML/
%{_mandir}/man3/*.3pm*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.10-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.10-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.10-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.10-6
- 为 Magic 3.0 重建

* Mon Jan 16 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.10-5
- Add BR: perl(Digest::MD5) (Fix gcc-4.7 FTBFS).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 30 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.10-3
- Set module version to fake 2.91 to work around versioning issue (#734253).
- Fix source URL, drop no longer needed README linefeed conversion.

* Mon Jul 18 2011 Petr Sabata <contyk@redhat.com> - 2.10-2
- Perl mass rebuild

* Thu Jul 14 2011 Tom Callaway <spot@fedoraproject.org>  - 2.10-1
- update to 2.10

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.9-11
- Perl mass rebuild

* Sun Apr 24 2011 Tom Callaway <spot@fedoraproject.org> - 2.9-10
- actually apply man page fixes patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.9-8
- 661697 rebuild for fixing problems with vendorach/lib
- add missing BR CGI
- add man page fixes from Debian

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.9-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.9-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9-2
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9-1.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.9-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Tue Jan 30 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.9-1
- Update to 2.9.

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.8-3
- Rebuild for FC6.

* Sat Feb 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.8-2
- Rebuild for FC5 (perl 5.8.8).

* Thu Dec 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.8-1
- Update to 2.8.

* Sat Aug 13 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.7-4
- README file: corrected the end-of-line encoding (#165874).
- Bring up to date with Fedora Extras template.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.7-3
- rebuilt

* Mon Oct 25 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.7-0.fdr.2
- Typo correction (rpmlint warning).
- Build requirements: removed perl(CGI).

* Fri Jun 25 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:2.7-0.fdr.1
- First build after 2nd time of losing the specfile somewhere :(
