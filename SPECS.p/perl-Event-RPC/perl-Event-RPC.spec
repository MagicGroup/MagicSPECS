Name:           perl-Event-RPC
Version:        1.01
Release:        14%{?dist}
Summary:        Event based transparent Client/Server RPC framework

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Event-RPC/
Source0:        http://search.cpan.org/CPAN/authors/id/J/JR/JRED/Event-RPC-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Event), perl(IO::Socket::SSL)
# Required for test
BuildRequires:  perl(Test::Simple)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Event based transparent Client/Server RPC framework.


%prep
%setup -q -n Event-RPC-%{version}
# Make it so that the .pl scripts in %%doc don't add bogus requirements
chmod -x examples/*.pl
# Convert encoding
for f in $(find lib/ -name *.pm) README examples/Test_class.pm ; do
cp -p ${f} ${f}.noutf8
iconv -f ISO-8859-1 -t UTF-8 ${f}.noutf8 > ${f}
touch -r ${f}.noutf8 ${f}
rm ${f}.noutf8
done

# Filter unwanted Provides:
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* | \
  sed -e '/perl(Test_class)/d'

EOF

%define __perl_provides %{_builddir}/Event-RPC-%{version}/%{name}-prov
chmod +x %{name}-prov

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes examples/ README
%{perl_vendorlib}/Event/
%{_mandir}/man3/*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.01-14
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 1.01-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.01-10
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.01-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-6
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.01-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec  16 2008 kwizart < kwizart at gmail.com > - 1.01-1
- Update to 1.01

* Thu Jul  17 2008 kwizart < kwizart at gmail.com > - 1.00-1
- Update to 1.00

* Thu May  29 2008 kwizart < kwizart at gmail.com > - 0.90-3
- Fix directory ownership
- Remove unwanted provides Test_class
- Fix non-utf8 encoding

* Thu May  8 2008 kwizart < kwizart at gmail.com > - 0.90-2
- Fix encoding and permission for examples

* Wed Apr 30 2008 kwizart < kwizart at gmail.com > - 0.90-1
- Initial package for Fedora

