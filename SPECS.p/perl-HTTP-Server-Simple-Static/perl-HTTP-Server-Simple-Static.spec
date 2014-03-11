Name:		perl-HTTP-Server-Simple-Static
Version:	0.07
Release:	11%{?dist}
Summary:	Serve static files with HTTP::Server::Simple
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/HTTP-Server-Simple-Static/
Source0:	http://search.cpan.org/CPAN/authors/id/S/SJ/SJQUINNEY/HTTP-Server-Simple-Static-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	perl(URI::Escape), perl(Exporter), perl(File::MMagic), perl(File::Spec::Functions)
BuildRequires:	perl(Test::Pod), perl(Test::Pod::Coverage), perl(HTTP::Server::Simple), perl(IO::File)
BuildRequires:	perl(MIME::Types)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
HTTP::Server::Simple::Static adds a method to serve static files from your
HTTP::Server::Simple subclass.

%prep
%setup -q -n HTTP-Server-Simple-Static-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

# We'll get this as a doc file instead.
rm -rf $RPM_BUILD_ROOT%{perl_vendorlib}/HTTP/Server/Simple/example.pl

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README example.pl
%{perl_vendorlib}/HTTP/
%{_mandir}/man3/*.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.07-11
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.07-10
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.07-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.07-6
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.07-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.07-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.07-2
- package example.pl as %%doc

* Sat Mar 28 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.07-1
- initial package for Fedora
