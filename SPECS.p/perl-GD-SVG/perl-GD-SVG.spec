Name:           perl-GD-SVG
Version:        0.33
Release:        10%{?dist}
Summary:        GD::SVG enables SVG output from scripts written using GD

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/GD-SVG/
Source0:        http://www.cpan.org/authors/id/T/TW/TWH/GD-SVG-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
# The  needs these.
BuildRequires:  perl(SVG)
BuildRequires:  perl(GD)
BuildRequires:  perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
GD::SVG seamlessly enables the scalable vector graphics (SVG) output
from scripts written using GD.  It accomplishes this by translating GD
functions into SVG functions.


%prep
%setup -q -n GD-SVG-%{version}

# avoid extra dependencies
chmod 644 examples/generate_test_image.pl

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



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README Changes examples
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.33-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.33-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.33-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.33-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.33-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.33-3
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.33-2
- Mass rebuild with perl-5.12.0

* Tue Dec 22 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.33-1
- Update to upstream 0.33

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.32-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.32-1
- Update to upstream 0.32

* Wed Jun  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.28-5
- Remove old check construct that prevents build in F-10+ (#449503)

* Fri Feb 08 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.28-4
- rebuild for new perl

* Tue Sep 04 2007 Alex Lancaster <alexl@users.sourceforge.net> 0.28-3
- Add missing BuildRequires: perl(Test::More)

* Tue Sep 04 2007 Alex Lancaster <alexl@users.sourceforge.net> 0.28-2
- Clarified license terms: GPL+ or Artistic

* Wed Mar 14 2007 Alex Lancaster <alexl@users.sourceforge.net> 0.28-1
- Update to 0.28
- Fix rpmlint errors

* Wed Apr 06 2005 Hunter Matthews <thm@duke.edu> 0.25-2
- Review changes from José Pedro Oliveira

* Fri Mar 18 2005 Hunter Matthews <thm@duke.edu> 0.25-1
- Initial Packaging.
