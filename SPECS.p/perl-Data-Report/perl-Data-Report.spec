Name:		perl-Data-Report
Version:	0.10
Release:	12%{?dist}
Summary:	A flexible plugin-driven reporting framework

Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Data-Report/
Source0:	http://search.cpan.org/CPAN/authors/id/JV/Data-Report-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	perl(Text::CSV)

BuildArch:	noarch

BuildRequires:	perl(Module::Build)

# For test suite
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Text::CSV)

%description
Data::Report is a framework for report generation.

You define the columns, add the data row by row, and get reports in
text, HTML, CSV and so on. Textual ornaments like extra empty lines,
dashed lines, and cell lines can be added in a way similar to HTML
style sheets.

%prep
%setup -q -n Data-Report-%{version}

%build
%{__perl} Build.PL --installdirs=vendor
./Build

%check
./Build test verbose=1

%install
%{__rm} -rf $RPM_BUILD_ROOT
./Build install --installdirs=vendor --destdir %{buildroot}
/usr/bin/find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
/usr/bin/find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{__chmod} -R u+w %{buildroot}/*

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.10-12
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.10-11
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.10-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-7
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-6
- Mass rebuild with perl-5.12.0

* Sat Apr  3 2010 Johan Vromans <jvromans@squirrel.nl> - 0.10-5
- Solve the dist puzzle.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.10-4
- rebuild against perl 5.10.1

* Sun Oct 11 2009 Johan Vromans <jvromans@squirrel.nl> 0.10-3
- Remove Text::CSV_XS kludge now Text::CVS is packaged as well.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jan 30 2009 Johan Vromans <jvromans@squirrel.nl> 0.10-1
- Initial Fedora RPM version
