# $Id: perl-Class-MakeMethods.spec,v 1.10 2010/04/30 09:53:24 mmaslano Exp $

Name:           perl-Class-MakeMethods
Version:	1.009
Release:	2%{?dist}
Summary:        Generate common types of methods

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Class-MakeMethods            
Source0: http://search.cpan.org/CPAN/authors/id/E/EV/EVO/Class-MakeMethods-%{version}.tar.gz        
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch 
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The Class::MakeMethods framework allows Perl class developers to quickly
define common types of methods. When a module uses Class::MakeMethods or one
of its subclasses, it can select from a variety of supported method types, and
specify a name for each method desired. The methods are dynamically generated
and installed in the calling package.

Construction of the individual methods is handled by subclasses. This
delegation approach allows for a wide variety of method-generation techniques
to be supported, each by a different subclass. Subclasses can also be added to
provide support for new types of methods.

Over a dozen subclasses are available, including implementations of a variety
of different method-generation techniques. Each subclass generates several
types of methods, with some supporting their own open-eneded extension syntax,
for hundreds of possible combinations of method types.

%prep
%setup -q -n Class-MakeMethods-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

# make sure the man page is UTF-8...
cd blib/man3
for i in Docs::ReadMe.3pm Attribute.3pm ; do
    iconv --from=ISO-8859-1 --to=UTF-8 Class::MakeMethods::$i > new
    mv new Class::MakeMethods::$i
done

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*


%check


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc CHANGES README 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.009-2
- 更新到

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.009-1
- 更新到 1.009

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.01-16
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.01-15
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.01-14
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.01-13
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.01-11
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.01-10
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-8
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-7
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.01-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.01-3
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.01-2.2
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.01-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Aug 31 2006 Chris Weyl <cweyl.drew.edu> 1.01-2
- bump for mass rebuild

* Wed Jul  5 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.01-1
- release bump for F-E

* Sun Jul 02 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.01-0
- Initial spec file for F-E
