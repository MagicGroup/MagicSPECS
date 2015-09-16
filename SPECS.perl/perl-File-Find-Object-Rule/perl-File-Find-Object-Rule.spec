%global pkgname File-Find-Object-Rule

Name:           perl-File-Find-Object-Rule
Version:        0.0305
Release:        5%{?dist}
Summary:        Alternative interface to File::Find::Object
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/File-Find-Object-Rule/
Source0:        http://www.cpan.org/authors/id/S/SH/SHLOMIF/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::XSAccessor)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Find::Object)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Number::Compare)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Text::Glob)
Requires:       perl(Class::XSAccessor)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
File::Find::Object::Rule is a friendlier interface to File::Find::Object. It 
allows you to build rules which specify the desired files and directories.

%prep
%setup -qn %{pkgname}-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}/*

%check
./Build test

%files
%doc Changes LICENSE README
%{_bindir}/findorule
%{perl_vendorlib}/*
%{_mandir}/man1/findorule.1*
%{_mandir}/man3/*

%changelog
* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.0305-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0305-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.0305-3
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.0305-2
- Perl 5.20 rebuild

* Sun Jun 08 2014 Christopher Meng <rpm@cicku.me> - 0.0305-1
- Update to 0.0305

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0304-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 13 2014 Christopher Meng <rpm@cicku.me> - 0.0304-1
- Update to 0.0304

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0303-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 26 2013 Christopher Meng <rpm@cicku.me> - 0.0303-1
- Initial Package.
