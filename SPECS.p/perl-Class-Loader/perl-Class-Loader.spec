Summary:	Load modules and create objects on demand
Name:		perl-Class-Loader
Version:	2.03
Release:	16%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Class-Loader/
Source0:	http://search.cpan.org/CPAN/authors/id/V/VI/VIPUL/Class-Loader-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(ExtUtils::MakeMaker)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Certain applications like to defer the decision to use a particular module till
runtime. This is possible in perl, and is a useful trick in situations where
the type of data is not known at compile time and the application doesn't wish
to pre-compile modules to handle all types of data it can work with. Loading
modules at runtime can also provide flexible interfaces for perl modules.
Modules can let the programmer decide what modules will be used by it instead
of hard-coding their names.

Class::Loader is an inheritable class that provides a method, _load(), to load
a module from disk and construct an object by calling its constructor. It also
provides a way to map modules' names and associated metadata with symbolic
names that can be used in place of module names at _load().

%prep
%setup -q -n Class-Loader-%{version}
sed -i -e '/^#! *\/usr\/bin\/perl /d' lib/Class/*.pm

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ARTISTIC Changes
%{perl_vendorlib}/Class/
%{_mandir}/man3/Class::Loader.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.03-16
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.03-15
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> 2.03-14
- Nobody else likes macros for commands

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> 2.03-13
- Perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.03-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> 2.03-11
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> 2.03-10
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> 2.03-9
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.03-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.03-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.03-6
- Rebuild for new perl

* Fri Aug 10 2007 Paul Howarth <paul@city-fan.org> 2.03-5
- Clarify license as GPL v1 or later, or Artistic (same as perl)

* Wed Apr 18 2007 Paul Howarth <paul@city-fan.org> 2.03-4
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 2.03-3
- FE6 mass rebuild

* Wed Feb 15 2006 Paul Howarth <paul@city-fan.org> 2.03-2
- Rebuild for perl 5.8.8 (FC5)

* Mon Dec  5 2005 Paul Howarth <paul@city-fan.org> 2.03-1
- Initial build
