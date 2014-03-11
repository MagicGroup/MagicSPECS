Name:		perl-Finance-Quote
Version:        1.17
Release: 	10%{?dist}
Summary:        A Perl module that retrieves stock and mutual fund quotes
Group:          Development/Libraries
License:        GPLv2+
URL:		http://finance-quote.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/finance-quote/Finance-Quote-%{version}.tar.gz
Patch0:		tiaa-cref.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Required for compile tests; no 'online' tests are run during the build
BuildRequires:	perl(LWP::UserAgent)
BuildRequires:	perl(Crypt::SSLeay) perl(HTTP::Request::Common)
BuildRequires:	perl(HTML::TableExtract) perl(HTML::TreeBuilder)
BuildRequires:	perl(Test::More)
BuildRequires:  perl(CGI)

%description
This module retrieves stock and mutual fund quotes from various exchanges
using various source.

%prep
%setup -q -n Finance-Quote-%{version} 
%patch0 -p2
find . -name *.pm | xargs %{__sed} -i -e '/^#!.*\/usr\/bin\/perl/d'

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog* Documentation/*
%{perl_vendorlib}/Finance/
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.17-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.17-9
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.17-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Bill Nottingham <notting@redhat.com> - 1.17-5
- fix TIAA-CREF (#668935, <amessina@messinet.com>)

* Mon Dec 06 2010 Bill Nottingham <notting@redhat.com> - 1.17-4
- fix buildrequires for F-15

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.17-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.17-2
- rebuild against perl 5.10.1

* Mon Nov 23 2009 Bradley Baetz <bbaetz@gmail.com> - 1.17-1
- Update to 1.17
- Add extra BuildRequires needed for tests to pass

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-2
Rebuild for new perl

* Wed Sep 26 2007 Bill Nottingham <notting@redhat.com>
- add perl(ExtUtils::MakeMaker) buildreq

* Tue Sep 18 2007 Bill Nottingham <notting@redhat.com>
- fix source download URL

* Fri Aug  3 2007 Bill Nottingham <notting@redhat.com>
- tweak license tag

* Mon Jan  8 2007 Bill Nottingham <notting@redhat.com> - 1.13-1
- update to 1.13

* Thu Sep 14 2006 Bill Nottingham <notting@redhat.com> - 1.11-4
- bump for rebuild

* Mon Apr 10 2006 Bill Nottingham <notting@redhat.com> - 1.11-3
- add buildreq for perl-HTML-TableExtract
- clean up sed

* Mon Apr 10 2006 Bill Nottingham <notting@redhat.com> - 1.11-2
- clean up spec file

* Fri Apr  7 2006 Bill Nottingham <notting@redhat.com> - 1.11-1
- initial packaging
