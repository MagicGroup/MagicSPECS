Name:           perl-Context-Preserve
Summary:        Run code after a subroutine call, preserving context
Version:        0.01
Release:        8%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/J/JR/JROCKWAY/Context-Preserve-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Context-Preserve
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ok)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)

%{?perl_default_filter}
%{?perl_default_subpackage_tests}

%description
Sometimes you need to call a function, get the results, act on the
results, then return the result of the function. This is painful because
of contexts; the original function can behave different if it's called
in void, scalar, or list context. You can ignore the various cases and
just pick one, but that's fragile. To do things right, you need to see
which case you're being called in, and then call the function in that
context. This results in 3 code paths, which is a pain to type in (and
maintain).  This module automates the process. You provide a coderef that
is the "original function", and another coderef to run after the
original runs. You can modify the return value (aliased to @_) here, and
do whatever else you need to do. 'wantarray' is correct inside both
coderefs; in "after", though, the return value is ignored and the value
'wantarray' returns is related to the context that the original function
was called in.

%prep
%setup -q -n Context-Preserve-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README Changes 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.01-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.01-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.01-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-2
- Mass rebuild with perl-5.12.0

* Fri Mar 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.01-1
- specfile by Fedora::App::MaintainerTools 0.004


