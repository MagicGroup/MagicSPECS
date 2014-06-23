Name:           perl-CGI
Summary:        Handle Common Gateway Interface requests and responses
Version:        3.51
Release:        8%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/M/MA/MARKSTOS/CGI.pm-%{version}.tar.gz
URL:            http://search.cpan.org/dist/CGI
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(FCGI) >= 0.67
# test
BuildRequires:  perl(Test::More) >= 0.80
Obsoletes:      %{name}-tests <= 3.49

%{?perl_default_filter}

%description
CGI.pm is a stable, complete and mature solution for processing and preparing
HTTP requests and responses. Major features including processing form 
submissions, file uploads, reading and writing cookies, query string generation
and manipulation, and processing and preparing HTTP headers. Some HTML 
generation utilities are included as well.

CGI.pm performs very well in in a vanilla CGI.pm environment and also comes 
with built-in support for mod_perl and mod_perl2 as well as FastCGI.

%prep
%setup -q -n CGI.pm-%{version}

# RPM 4.8 style
%{?filter_setup:
%filter_from_provides /^perl(Fh)$/d
%filter_from_provides /^perl(MultipartBuffer)$/d
%filter_from_provides /^perl(utf8)$/d
%filter_setup
}
# RPM 4.9 style
%global __provides_exclude %{?__provides_exclude:__provides_exclude|}^perl\\(Fh\\)$
%global __provides_exclude %__provides_exclude|^perl\\(MultipartBuffer\\)$
%global __provides_exclude %__provides_exclude|^perl\\(utf8\\)$

iconv -f iso8859-1 -t utf-8 < Changes > Changes.1
mv Changes.1 Changes
sed -i 's?usr/bin perl?usr/bin/perl?' t/init.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
make test


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README Changes
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.51-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 3.51-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 3.51-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.51-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 3.51-4
- RPM 4.9 dependency filtering added

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.51-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Marcela Mašláňová <mmaslano@redhat.com> 3.51-1
- update to fix CVE-2010-2761

* Mon Nov 29 2010 Marcela Mašláňová <mmaslano@redhat.com> 3.50-2
- remove -test sub-package, which would be needed also in perl-core

* Mon Nov 29 2010 Marcela Mašláňová <mmaslano@redhat.com> 3.50-1
- initial dual-life package

