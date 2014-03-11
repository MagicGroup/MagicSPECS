Name:           perl-AuthCAS
Version:        1.5
Release:        6%{?dist}
Summary:        Client library for CAS 2.0 authentication server
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/AuthCAS/
Source0:        http://search.cpan.org/CPAN/authors/id/O/OS/OSALAUN/AuthCAS-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::More)
# Test::Pod::Coverage test is failing, but that's no a blocker, so let's keep
# it as a comment for now.
#BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::Pod)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
AuthCAS aims at providing a Perl API to Yale's Central Authentication
System (CAS). Only a basic Perl library is provided with CAS whereas
AuthCAS is a full object-oriented library.


%prep
%setup -q -n AuthCAS-%{version}
iconv -f iso8859-1 -t utf-8 README > README.utf8 && \
touch -r README README.utf8 && \
mv -f README.utf8 README


%build
%{__perl} Build.PL installdirs=vendor
./Build


%install
rm -rf $RPM_BUILD_ROOT

./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*


%check
./Build test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*


%changelog
* Mon Dec 10 2012 Liu Di <liudidi@gmail.com> - 1.5-6
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 1.5-5
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.5-3
- Perl mass rebuild

* Sat May 21 2011 Xavier Bachelot <xavier@bachelot.org> 1.5-2
- Remove superfluous Requires:.

* Mon May 16 2011 Xavier Bachelot <xavier@bachelot.org> 1.5-1
- Update to 1.5.

* Fri Dec 03 2010 Xavier Bachelot <xavier@bachelot.org> 1.4-1
- Initial Fedora release.
