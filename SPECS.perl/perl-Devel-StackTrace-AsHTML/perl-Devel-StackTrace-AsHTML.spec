Name:           perl-Devel-StackTrace-AsHTML
Summary:        Displays a stack trace in HTML
Version:        0.11
Release:        9%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/M/MI/MIYAGAWA/Devel-StackTrace-AsHTML-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Devel-StackTrace-AsHTML
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Devel::StackTrace)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Filter::Util::Call)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Perl::Critic)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Spelling)
BuildRequires:  perl(Test::Synopsis)


%{?perl_default_filter}

# fedora < 15 had *-tests
Obsoletes:      %{name}-tests < %{version}-%{release}
Provides:       %{name}-tests = %{version}-%{release}

%description
Devel::StackTrace::AsHTML adds an 'as_html' method to Devel::StackTrace
which displays the stack trace in beautiful HTML, with code snippet
context and function parameters. If you call it on an instance of
Devel::StackTrace::WithLexicals, you even get to see the lexical
variables of each stack frame.

%prep
%setup -q -n Devel-StackTrace-AsHTML-%{version}

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


%files
%doc Changes README eg/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.11-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.11-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.11-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.11-5
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.11-1
- Upstream update.

* Tue Jan 25 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.10-1
- Upstream update.
- Abandon perl-Devel-StackTrace-AsHTML-tests.

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09-3
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Jun 22 2010 Petr Pisar <ppisar@redhat.com> - 0.09-2
- Rebuild against perl-5.12

* Sun Apr 11 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- specfile by Fedora::App::MaintainerTools 0.006


