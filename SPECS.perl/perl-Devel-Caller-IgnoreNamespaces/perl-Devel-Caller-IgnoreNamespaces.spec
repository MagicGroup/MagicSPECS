Name:           perl-Devel-Caller-IgnoreNamespaces
Version:        1.0
Release:        12%{?dist}
Summary:        Make available a function which can ignore name-spaces that you tell it about
License:        GPLv2 or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Devel-Caller-IgnoreNamespaces/
Source0:        http://www.cpan.org/authors/id/D/DC/DCANTRELL/Devel-Caller-IgnoreNamespaces-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
If your module should be ignored by caller(), just like Hook::LexWrap is
by its magic caller(), then call this module's register() subroutine
with its name.

%prep
%setup -q -n Devel-Caller-IgnoreNamespaces-%{version}

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
%doc ARTISTIC.txt CHANGES GPL2.txt README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.0-12
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.0-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.0-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.0-9
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.0-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.0-5
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.0-4
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.0-3
- Mass rebuild with perl-5.12.0

* Sat Mar 13 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> 1.0-2
- Add perl(Test::More) and perl(Test::Pod) to BuildRequires.

* Sat Mar 13 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> 1.0-1
- Specfile autogenerated by cpanspec 1.78.