Name:           perl-Graph
Version:	0.96
Release:	1%{?dist}
Summary:        Perl module for dealing with graphs, the abstract data structures

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Graph/
Source0:        http://www.cpan.org/authors/id/J/JH/JHI/Graph-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Heap)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This is Graph, a Perl module for dealing with graphs, the abstract
data structures. 
 
This is a full rewrite of the Graph module 0.2xx series as discussed
in the book "Mastering Algorithms with Perl", written by Jarkko
Hietaniemi (the undersigned), John Macdonald, and Jon Orwant,
and published by O'Reilly and Associates.  This rewrite is not
fully compatible with the 0.2xx series.


%prep
%setup -q -n Graph-%{version}

# avoid extra dependencies
chmod 644 util/cover.sh


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
%doc README RELEASE DESIGN Changes TODO util
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.96-1
- 更新到 0.96

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.91-12
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.91-11
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.91-10
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.91-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.91-6
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.91-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.91-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.91-1
- Update to upstream 0.91

* Wed Jun  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.84-3
- Remove old check construct that prevents build in F-10+ (#449571)

* Fri Feb 08 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.84-2
- rebuild for new perl

* Wed Sep 05 2007 Alex Lancaster <alexl@users.sourceforge.net> 0.84-1
- Update to latest upstream.

* Thu Aug 23 2007 Alex Lancaster <alexl@users.sourceforge.net> 0.83-3
- License tag to GPL+ or Artistic as per new guidelines.

* Sat Aug 18 2007 Alex Lancaster <alexl@users.sourceforge.net> 0.83-2
- Add missing BR: perl(Test::More)

* Sat Aug 18 2007 Alex Lancaster <alexl@users.sourceforge.net> 0.83-1
- Update to latest upstream

* Wed Mar 23 2007 Alex Lancaster <alexl@users.sourceforge.net> 0.81-1
- Update to 0.81

* Wed Apr 06 2005 Hunter Matthews <thm@duke.edu> 0.59-2
- Review suggestions from José Pedro Oliveira

* Fri Mar 18 2005 Hunter Matthews <thm@duke.edu> 0.59-1
- Initial Packageing.


