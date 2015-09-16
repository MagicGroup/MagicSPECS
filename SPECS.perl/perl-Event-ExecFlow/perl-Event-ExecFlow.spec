Name:           perl-Event-ExecFlow
Version:        0.64
Release:        12%{?dist}
Summary:        High level API for event-based execution flow control

Group:          Development/Libraries
License:        (GPL+ or Artistic) and LGPLv2+
URL:            http://search.cpan.org/dist/Event-ExecFlow/
Source0:        http://search.cpan.org/CPAN/authors/id/J/JR/JRED/Event-ExecFlow-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(AnyEvent)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Locale::TextDomain)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Event::ExecFlow offers a high level API to declare jobs, which mainly execute
external commands, parse their output to get progress or other status
information, triggers actions when the command has been finished etc. Such jobs
can be chained together in a recursive fashion to fulfill rather complex tasks
which consist of many jobs.


%prep
%setup -q -n Event-ExecFlow-%{version}

# Convert encoding
for f in $(find lib/ -name *.pm) README ; do
cp -p ${f} ${f}.noutf8
iconv -f ISO-8859-1 -t UTF-8 ${f}.noutf8 > ${f}
touch -r ${f}.noutf8 ${f}
rm ${f}.noutf8
done


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'

# Fix perm
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/execflow


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
# This file is GPL+ or Artistic
%{_bindir}/execflow
# Theses files are LGPLv2+
%{perl_vendorlib}/Event/
%{_mandir}/man3/*.3*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.64-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.64-11
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.64-10
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.64-9
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.64-8
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.64-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.64-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.64-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.64-4
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.64-3
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.64-2
- Mass rebuild with perl-5.12.0

* Fri Mar 12 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.64-1
- Update to 0.64
- Drop Filter provides

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.63-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jul 20 2008 kwizart < kwizart at gmail.com > - 0.63-4
- Update license to (GPL+ or Artistic) and LGPLv2+

* Mon Jul 14 2008 kwizart < kwizart at gmail.com > - 0.63-3
- Fix directory ownership
- Fix execflow perm
- Fix perl Encoding
- Fix License to LGPLv2+

* Thu Jul 10 2008 kwizart < kwizart at gmail.com > - 0.63-2
- Add BR Test::More and Locale::TextDomain

* Wed Apr 30 2008 kwizart < kwizart at gmail.com > - 0.63-1
- Initial package for Fedora
