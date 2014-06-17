Name:           perl-Event-RPC
Version:        1.05
Release:        3%{?dist}
Summary:        Event based transparent client/server RPC framework
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Event-RPC/
Source0:        http://search.cpan.org/CPAN/authors/id/J/JR/JRED/Event-RPC-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(AnyEvent)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Event)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(Glib)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Sys::Hostname)
# Optional run-time:
BuildRequires:  perl(IO::Socket::SSL)
# Tests:
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# TODO:  Split dependencies on an event controller ||(AnyEvent Event Glib)

%description
Event::RPC supports you in developing Event based networking client/server
applications with transparent object/method access from the client to the
server. Network communication is optionally encrypted using IO::Socket::SSL.
Several event loop managers are supported due to an extensible API. Currently
Event, Glib, and AnyEvent are implemented. The latter lets you use nearly
every event loop implementation available for Perl.

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

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'

%check
make test

%files
%doc Changes examples README
%{perl_vendorlib}/Event/
%{_mandir}/man3/*.3*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.05-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 30 2014 Petr Pisar <ppisar@redhat.com> - 1.05-1
- 1.05 bump

* Mon Jan 27 2014 Petr Pisar <ppisar@redhat.com> - 1.04-1
- 1.04 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 1.03-2
- Perl 5.18 rebuild

* Mon Jun 17 2013 Petr Pisar <ppisar@redhat.com> - 1.03-1
- 1.03 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

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

