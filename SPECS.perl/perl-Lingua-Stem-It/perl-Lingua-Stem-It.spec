Name:           perl-Lingua-Stem-It
Version:        0.02
Release:        12%{?dist}
Summary:        Porter's stemming algorithm for Italian
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Lingua-Stem-It/
Source0:        http://www.cpan.org/authors/id/A/AC/ACALPINI/Lingua-Stem-It-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module applies the Porter Stemming Algorithm to its parameters,
returning the stemmed words.

%prep
%setup -q -n Lingua-Stem-It-%{version}

sed -ie 's/\r//' Changes README It.pm
chmod -x Changes

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.02-12
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.02-11
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.02-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.02-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.02-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.02-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.02-5
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.02-4
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Aug 16 2010 Iain Arnell <iarnell@gmail.com> 0.02-1
- Specfile autogenerated by cpanspec 1.78.
