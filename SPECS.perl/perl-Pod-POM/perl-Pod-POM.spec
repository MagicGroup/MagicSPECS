%{!?perl_vendorlib: %define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)}

Name:           perl-Pod-POM
Version:	2.00
Release:	2%{?dist}

Summary:        Object-oriented interface to Perl POD documents

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Pod-POM/
Source0:        http://search.cpan.org/CPAN/authors/id/N/NE/NEILB/Pod-POM-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Path)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(parent)
BuildRequires:  perl(Text::Wrap)
# Tests:
BuildRequires:  perl(File::Slurp)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(YAML::Tiny)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module implements a parser to convert Pod documents into a simple
object model form known hereafter as the Pod Object Model.  The object
model is generated as a hierarchical tree of nodes, each of which
represents a different element of the original document.  The tree can
be walked manually and the nodes examined, printed or otherwise
manipulated.  In addition, Pod::POM supports and provides view objects
which can automatically traverse the tree, or section thereof, and
generate an output representation in one form or another.


%prep
%setup -q -n Pod-POM-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
# http://rt.cpan.org/NoAuth/Bug.html?id=3910
PERL_HASH_SEED=0 make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README TODO
%{_bindir}/pomdump
%{_bindir}/podlint
%{_bindir}/pom2
%{perl_vendorlib}/Pod
%{_mandir}/man[13]/*.[13]*


%changelog
* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 2.00-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.00-1
- 更新到 2.00

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.27-9
- 为 Magic 3.0 重建

* Thu Aug 16 2012 Petr Pisar <ppisar@redhat.com> - 0.27-8
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.27-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.27-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.27-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 15 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.27-1
- Upstream update (Fix several perl-5.12.0 build breakdowns).

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.25-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.25-2
- rebuild against perl 5.10.1

* Wed Aug 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.25-1
- update to 0.25

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> 0.18-1
- update to 0.18

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17-10
- fix FTBFS

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17-9
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.17-8
- rebuild for new perl

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.17-7
- license tag fix

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.17-6
- build for fc6

* Fri Jul  7 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.17-5
- add dist tag

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Mar 15 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.17-3
- Remove Epoch: 0.
- Improve summary.

* Sun Jul 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.17-0.fdr.3
- Bring up to date with current fedora.us Perl spec template.

* Fri Nov 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.17-0.fdr.2
- Add workaround for http://rt.cpan.org/NoAuth/Bug.html?id=3910.

* Sun Oct 12 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.17-0.fdr.1
- First build.
